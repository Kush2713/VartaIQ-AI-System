from transformers import pipeline

from sentence_transformers import (
    SentenceTransformer
)


# =====================================
# GLOBAL MODEL CACHE
# =====================================

_models = {}


# =====================================
# SUMMARIZER MODEL
# =====================================

def get_summarizer_model():

    if "summarizer" not in _models:

        _models["summarizer"] = pipeline(

            "summarization",

            model="facebook/bart-large-cnn"
        )

    return _models["summarizer"]


# =====================================
# LLM GENERATION MODEL
# =====================================

def get_llm_model():

    if "llm" not in _models:

        _models["llm"] = pipeline(

            "text2text-generation",

            model="google/flan-t5-base"
        )

    return _models["llm"]


# =====================================
# EMBEDDING MODEL
# =====================================

def get_embedding_model():

    if "embedding" not in _models:

        _models["embedding"] = (
            SentenceTransformer(
                "all-MiniLM-L6-v2"
            )
        )

    return _models["embedding"]


# =====================================
# PRELOAD ALL MODELS
# =====================================

def preload_models():

    get_summarizer_model()

    get_llm_model()

    get_embedding_model()

    print(
        "\nAI models preloaded successfully."
    )