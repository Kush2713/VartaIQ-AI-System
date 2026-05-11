from transformers import pipeline

summarizer_model = None

def get_summarizer():
    global summarizer_model

    if summarizer_model is None:
        summarizer_model = pipeline(
            "summarization",
            model="facebook/bart-large-cnn"
        )

    return summarizer_model
