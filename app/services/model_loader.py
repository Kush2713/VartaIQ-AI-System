import torch

from transformers import (
    pipeline
)

from sentence_transformers import (
    SentenceTransformer
)


# =====================================
# DEVICE CONFIGURATION
# =====================================

DEVICE = 0 if torch.cuda.is_available() else -1


# =====================================
# GLOBAL MODEL REGISTRY
# =====================================

summarizer_model = None

embedding_model = None

llm_model = None


# =====================================
# SUMMARIZER MODEL
# =====================================

def get_summarizer():

    global summarizer_model

    if summarizer_model is None:

        summarizer_model = pipeline(

            "summarization",

            model="facebook/bart-large-cnn",

            device=DEVICE
        )

        # Warmup
        summarizer_model(
            "Warmup summarization model.",
            max_length=20,
            min_length=5
        )

    return summarizer_model


# =====================================
# EMBEDDING MODEL
# =====================================

def get_embedding_model():

    global embedding_model

    if embedding_model is None:

        embedding_model = (
            SentenceTransformer(
                "all-MiniLM-L6-v2"
            )
        )

        # GPU support
        if torch.cuda.is_available():

            embedding_model = (
                embedding_model.to("cuda")
            )

    return embedding_model


# =====================================
# LIGHTWEIGHT LLM
# =====================================

def get_llm():

    global llm_model

    if llm_model is None:

        llm_model = pipeline(

            "text2text-generation",

            model="google/flan-t5-base",

            device=DEVICE
        )

        # Warmup
        llm_model(

            "Warmup instruction model.",

            max_length=20
        )

    return llm_model







# from transformers import pipeline

# from sentence_transformers import (
#     SentenceTransformer
# )


# # =====================================
# # GLOBAL MODEL REGISTRY
# # =====================================

# summarizer_model = None

# embedding_model = None


# # =====================================
# # SUMMARIZER
# # =====================================

# def get_summarizer():

#     global summarizer_model

#     if summarizer_model is None:

#         summarizer_model = pipeline(

#             "summarization",

#             model="facebook/bart-large-cnn"
#         )

#     return summarizer_model


# # =====================================
# # EMBEDDING MODEL
# # =====================================

# def get_embedding_model():

#     global embedding_model

#     if embedding_model is None:

#         embedding_model = (
#             SentenceTransformer(
#                 "all-MiniLM-L6-v2"
#             )
#         )

#     return embedding_model


























# # from transformers import pipeline

# # summarizer_model = None

# # def get_summarizer():
# #     global summarizer_model

# #     if summarizer_model is None:   # Uses lazy loading, load model only for first time
# #         summarizer_model = pipeline(
# #             "summarization",
# #             model="facebook/bart-large-cnn"
# #         )

# #     return summarizer_model

# # # Load AI Models only once.
# # # Model reloads on every request
# # # → very slow
# # # → high memory usage
