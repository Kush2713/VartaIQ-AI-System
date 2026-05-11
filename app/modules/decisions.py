# def extract_decisions(transcript):
#     decisions = []

#     keywords = [
#         "decide", "decided", "finalize", "agreed",
#         "we will", "let's", "plan is"
#     ]

#     for item in transcript:
#         text = item["text"].lower()

#         if any(k in text for k in keywords):
#             decisions.append({
#                 "speaker": item["speaker"],
#                 "decision": item["text"]
#             })

#     return decisions
import spacy

nlp = spacy.load("en_core_web_sm")

DECISION_KEYWORDS = {
    "finalize",
    "decide",
    "decided",
    "agreed",
    "approve",
    "approved",
    "confirm",
    "confirmed",
    "plan"
}

MODAL_DECISION_WORDS = {
    "will",
    "shall"
}


def is_decision_sentence(sent):
    text = sent.text.lower()

    # Rule 1: Important decision keywords
    if any(word in text for word in DECISION_KEYWORDS):
        return True

    # Rule 2: Detect commitment/finalization structure
    for token in sent:
        if token.lemma_.lower() in MODAL_DECISION_WORDS:
            if any(child.dep_ == "xcomp" or child.pos_ == "VERB" for child in token.children):
                return True

    # Rule 3: Detect planning intent
    if "let's" in text or "plan is" in text:
        return True

    return False


def extract_decisions(transcript):
    decisions = []

    for item in transcript:
        doc = nlp(item["text"])

        for sent in doc.sents:
            if is_decision_sentence(sent):
                decisions.append({
                    "speaker": item["speaker"],
                    "decision": sent.text.strip()
                })

    return decisions

# WHY THIS IS BETTER
# Before:
# keyword exists → decision

# Very weak.

# Now:

# We analyze:

# sentence structure
# verbs
# modal intent
# planning language
# commitment semantics

# This is:

# much more NLP-driven