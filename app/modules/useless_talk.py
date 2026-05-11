# def detect_useless_talk(data):
#     useless = []

#     for item in data:
#         words = item["text"].split()
#         filler_count = sum(1 for w in words if w.lower() in ["umm", "uh", "okay", "yeah"])

#         if len(words) <= 2 or (filler_count / len(words)) > 0.4:
#             useless.append(item)

#     return useless

import spacy

nlp = spacy.load("en_core_web_sm")

FILLER_WORDS = {
    "umm",
    "uh",
    "yeah",
    "okay",
    "hmm",
    "like"
}

IMPORTANT_VERBS = {
    "deploy",
    "complete",
    "finalize",
    "approve",
    "design",
    "integrate",
    "test",
    "review",
    "submit",
    "prepare"
}


def is_meaningful(sent):
    """
    Determines whether sentence contains meaningful intent.
    """

    for token in sent:

        # meaningful action verbs
        if token.lemma_.lower() in IMPORTANT_VERBS:
            return True

        # proper nouns often indicate entities/tasks
        if token.pos_ in {"PROPN", "NOUN"}:
            return True

    return False


def detect_useless_talk(data):
    useless = []

    for item in data:

        doc = nlp(item["text"])

        for sent in doc.sents:

            words = [token.text.lower() for token in sent if not token.is_punct]

            if not words:
                continue

            filler_count = sum(
                1 for word in words if word in FILLER_WORDS
            )

            filler_ratio = filler_count / len(words)

            meaningful = is_meaningful(sent)

            # useless if mostly filler + no meaningful intent
            if filler_ratio > 0.4 and not meaningful:

                useless.append({
                    "speaker": item["speaker"],
                    "text": sent.text.strip()
                })

    return useless

# CURRENT PROBLEMS
# - False Positives

# Example:

# "Okay approved"

# Important confirmation.

# Could be marked useless.

# - No semantic understanding

# Example:

# "Yeah let's deploy today"

# Actually important.

# But filler exists.

# - Short sentence ≠ useless

# Example:

# "Deployment confirmed"

# Very important.

# But short.