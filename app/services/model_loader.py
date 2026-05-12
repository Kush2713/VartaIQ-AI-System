from transformers import pipeline

summarizer_model = None

def get_summarizer():
    global summarizer_model

    if summarizer_model is None:   # Uses lazy loading, load model only for first time
        summarizer_model = pipeline(
            "summarization",
            model="facebook/bart-large-cnn"
        )

    return summarizer_model

# Load AI Models only once.
# Model reloads on every request
# → very slow
# → high memory usage
