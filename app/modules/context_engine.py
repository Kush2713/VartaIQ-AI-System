import hashlib
import numpy as np

from sklearn.metrics.pairwise import (
    cosine_similarity
)

from app.services.model_manager import (
    get_embedding_model
)


# =====================================
# LOAD EMBEDDING MODEL
# =====================================

embedding_model = (
    get_embedding_model()
)


# =====================================
# EMBEDDING CACHE
# =====================================

_embedding_cache = {}


# =====================================
# GENERATE CACHE KEY
# =====================================

def generate_cache_key(
    text
):

    return hashlib.md5(

        text.encode("utf-8")

    ).hexdigest()


# =====================================
# GENERATE SENTENCE EMBEDDING
# =====================================

def generate_sentence_embedding(
    text
):

    # ---------------------------------
    # Empty safety
    # ---------------------------------

    if not text:
        return np.zeros(384)

    # ---------------------------------
    # Cache lookup
    # ---------------------------------

    cache_key = generate_cache_key(
        text
    )

    if cache_key in _embedding_cache:

        return _embedding_cache[
            cache_key
        ]

    # ---------------------------------
    # Generate embedding
    # ---------------------------------

    embedding = embedding_model.encode(
        [text]
    )[0]

    # ---------------------------------
    # Store in cache
    # ---------------------------------

    _embedding_cache[
        cache_key
    ] = embedding

    return embedding


# =====================================
# GENERATE MEETING EMBEDDING
# =====================================

def generate_meeting_embedding(
    transcript
):

    all_text = []

    for item in transcript:

        all_text.append(
            item["text"]
        )

    combined_text = " ".join(
        all_text
    )

    return generate_sentence_embedding(
        combined_text
    )


# =====================================
# SEMANTIC SIMILARITY
# =====================================

def calculate_semantic_similarity(

    embedding_1,

    embedding_2
):

    similarity = cosine_similarity(

        [embedding_1],

        [embedding_2]

    )[0][0]

    return float(similarity)


# =====================================
# CONTEXT RELEVANCE
# =====================================

def calculate_context_relevance(

    sentence,

    meeting_embedding
):

    sentence_embedding = (
        generate_sentence_embedding(
            sentence
        )
    )

    return calculate_semantic_similarity(

        sentence_embedding,

        meeting_embedding
    )


# =====================================
# CACHE STATS
# =====================================

def get_embedding_cache_size():

    return len(_embedding_cache)


# =====================================
# CLEAR CACHE
# =====================================

def clear_embedding_cache():

    _embedding_cache.clear()