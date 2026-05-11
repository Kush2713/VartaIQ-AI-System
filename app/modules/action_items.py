# import spacy

# nlp = spacy.load("en_core_web_sm")


# def extract_action_items(data):
#     actions = []

#     for item in data:
#         doc = nlp(item["text"])

#         for sent in doc.sents:
#             if any(token.dep_ == "ROOT" and token.pos_ == "VERB" for token in sent):
#                 if "will" in sent.text.lower() or "should" in sent.text.lower():
#                     actions.append({
#                         "speaker": item["speaker"],
#                         "task": sent.text.strip()
#                     })

#     return actions

import spacy

nlp = spacy.load("en_core_web_sm")

ACTION_VERBS = {
    "complete",
    "finish",
    "submit",
    "prepare",
    "design",
    "implement",
    "integrate",
    "deploy",
    "test",
    "review",
    "create",
    "update",
    "fix",
    "send"
}

MODAL_WORDS = {
    "will",
    "should",
    "need",
    "must",
    "shall"
}


def is_actionable(sent):
    """
    Determines whether a sentence contains actionable intent.
    """

    text = sent.text.lower()

    # Rule 1: Modal commitment language
    if any(word in text for word in MODAL_WORDS):

        # Check if meaningful action verb exists
        for token in sent:
            if token.lemma_.lower() in ACTION_VERBS:
                return True

    # Rule 2: Imperative task detection
    root = sent.root

    if root.pos_ == "VERB":
        if root.lemma_.lower() in ACTION_VERBS:
            return True

    return False


def clean_task(task):
    fillers = ["yeah", "okay", "umm", "uh"]

    cleaned = task

    for filler in fillers:
        cleaned = cleaned.replace(filler, "")

    return " ".join(cleaned.split()).strip().capitalize()


def extract_action_items(data):
    actions = []

    for item in data:
        doc = nlp(item["text"])

        for sent in doc.sents:

            if is_actionable(sent):

                actions.append({
                    "speaker": item["speaker"],
                    "task": clean_task(sent.text)
                })

    return actions


# This module is already better than decisions.py, because it uses spaCy parsing.

# But it still has major limitations:

# too dependent on "will" and "should", missed: "Akshay needs to complete backend integration"
# weak semantic understanding
# misses many real tasks
# generates noisy tasks sometimes