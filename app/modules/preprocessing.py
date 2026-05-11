import re

def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)
    return text.strip()


def preprocess_data(data):
    processed = []

    for item in data:
        processed.append({
            "speaker": item["speaker"].strip(),
            "text": item["text"].strip(),
            "clean_text": clean_text(item["text"])
        })

    return processed