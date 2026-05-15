import os
import time
import requests
import numpy as np
from sentence_transformers import SentenceTransformer

# =====================================
# HYBRID APPROACH
# - Embeddings: Local (sentence-transformers)
# - Summarizer, Sentiment: HF API
# - spaCy: Local (installed separately)
# =====================================

HF_API_TOKEN = os.getenv("HF_API_TOKEN", "")

if not HF_API_TOKEN:
    raise RuntimeError(
        "\n[STARTUP ERROR] HF_API_TOKEN is not set.\n"
        "Add it to your .env file:\n"
        "HF_API_TOKEN=hf_xxxxxxxxxxxxxxxx\n"
    )

HF_HEADERS = {
    "Authorization": f"Bearer {HF_API_TOKEN}"
}

# =====================================
# MODEL ENDPOINTS
# =====================================

# Use models that are confirmed to work with HF Inference API
SUMMARIZER_URL = (
    "https://api-inference.huggingface.co"
    "/models/sshleifer/distilbart-cnn-12-6"
)

LLM_URL = (
    "https://api-inference.huggingface.co"
    "/models/google/flan-t5-base"
)

SENTIMENT_URL = (
    "https://api-inference.huggingface.co"
    "/models/cardiffnlp/twitter-roberta-base-sentiment-latest"
)

EMBEDDING_URL = (
    "https://api-inference.huggingface.co"
    "/models/sentence-transformers/all-MiniLM-L6-v2"
)

# =====================================
# GLOBAL CACHE
# Stores API wrapper instances
# =====================================

_models = {}

# =====================================
# RETRY HELPER
# HF free tier sometimes returns 503
# while the model is loading (cold start)
# =====================================

def _hf_post(url, payload, retries=5, wait=20):
    """
    POST to HuggingFace Inference API with
    automatic retry on model loading (503).
    """
    for attempt in range(retries):

        try:
            response = requests.post(
                url,
                headers=HF_HEADERS,
                json=payload,
                timeout=120
            )

            if response.status_code == 200:
                return response.json()

            # Model still loading — wait and retry
            if response.status_code == 503:
                print(
                    f"[HF API] Model loading, "
                    f"retrying in {wait}s "
                    f"(attempt {attempt + 1}/{retries})..."
                )
                time.sleep(wait)
                continue

            # Any other error — raise immediately
            print(f"[HF API ERROR] Status: {response.status_code}, Response: {response.text}")
            response.raise_for_status()
        
        except requests.exceptions.Timeout:
            print(f"[HF API TIMEOUT] Attempt {attempt + 1}/{retries}")
            if attempt < retries - 1:
                time.sleep(wait)
                continue
            raise
        
        except requests.exceptions.RequestException as e:
            print(f"[HF API REQUEST ERROR] {str(e)}")
            if attempt < retries - 1:
                time.sleep(wait)
                continue
            raise

    raise RuntimeError(
        f"HF API failed after {retries} retries: {url}"
    )


# =====================================
# SUMMARIZER — HF API WRAPPER
# Mimics transformers pipeline interface:
# result = summarizer(text, max_length=X, min_length=Y)
# returns [{"summary_text": "..."}]
# =====================================

class SummarizerAPIWrapper:

    def __call__(
        self,
        text,
        max_length=120,
        min_length=40,
        do_sample=False
    ):
        payload = {
            "inputs": text,
            "parameters": {
                "max_length": max_length,
                "min_length": min_length,
                "do_sample": do_sample
            }
        }

        result = _hf_post(SUMMARIZER_URL, payload)

        # HF returns: [{"summary_text": "..."}]
        if isinstance(result, list):
            return result

        # Fallback if unexpected format
        return [{"summary_text": str(result)}]


# =====================================
# LLM — HF API WRAPPER
# Mimics transformers pipeline interface:
# result = generator(prompt, max_length=X)
# returns [{"generated_text": "..."}]
# =====================================

class LLMAPIWrapper:

    def __call__(
        self,
        prompt,
        max_length=180,
        do_sample=False
    ):
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_length": max_length,
                "do_sample": do_sample
            }
        }

        result = _hf_post(LLM_URL, payload)

        # HF text2text returns: [{"generated_text": "..."}]
        if isinstance(result, list):
            return result

        return [{"generated_text": str(result)}]


# =====================================
# SENTIMENT — HF API WRAPPER
# Mimics transformers pipeline interface:
# result = sentiment_pipeline(text)
# returns [{"label": "...", "score": 0.9}]
# =====================================

class SentimentAPIWrapper:

    def __call__(self, text):

        payload = {"inputs": text}

        result = _hf_post(SENTIMENT_URL, payload)

        # HF returns nested list: [[{"label":..,"score":..}]]
        if (
            isinstance(result, list)
            and len(result) > 0
            and isinstance(result[0], list)
        ):
            return result[0]

        # Already flat list: [{"label":..,"score":..}]
        if isinstance(result, list):
            return result

        return [{"label": "neutral", "score": 0.5}]


# =====================================
# GET SUMMARIZER
# =====================================

def get_summarizer_model():

    if "summarizer" not in _models:
        _models["summarizer"] = SummarizerAPIWrapper()
        print("[Model] Summarizer API wrapper ready.")

    return _models["summarizer"]


# =====================================
# GET LLM — removed (FLAN-T5 not
# supported on HF router API).
# Summary refinement is now handled
# in llm_enhancer.py with pure Python.
# =====================================

def get_llm_model():
    return None


# =====================================
# GET SENTIMENT MODEL
# =====================================

def get_sentiment_model():

    if "sentiment" not in _models:
        _models["sentiment"] = SentimentAPIWrapper()
        print("[Model] Sentiment API wrapper ready.")

    return _models["sentiment"]


# =====================================
# EMBEDDING MODEL — LOCAL
# Uses sentence-transformers locally
# (HF API has issues with this model)
# =====================================

def get_embedding_model():

    if "embedding" not in _models:
        _models["embedding"] = SentenceTransformer("all-MiniLM-L6-v2")
        print("[Model] Embedding model loaded locally.")

    return _models["embedding"]


# =====================================
# PRELOAD
# =====================================

def preload_models():

    get_summarizer_model()
    get_llm_model()
    get_sentiment_model()
    get_embedding_model()

    print("\nAll AI models ready (Hybrid: Local embeddings + HF API).")
