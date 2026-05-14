import spacy

from app.modules.deduplication import (
    semantic_deduplicate
)

nlp = spacy.load("en_core_web_sm")


# =====================================
# STRONG DECISION SIGNALS
# =====================================

STRONG_DECISION_PHRASES = {

    "final plan",
    "we agreed",
    "agreed",
    "approved",
    "confirmed",
    "finalized",
    "decision is",
    "final decision",
    "we decided",
    "let's finalize",
    "must complete",
    "will proceed",
    "moving forward",
    "officially",
    "is officially",
    "moved to",
    "is moved"
}


# =====================================
# WEAK / UNCERTAIN PHRASES
# =====================================

UNCERTAIN_PHRASES = {

    "maybe",
    "probably",
    "might",
    "perhaps",
    "can possibly",
    "i think",
    "we can try",
    "hopefully"
}


# =====================================
# COMMITMENT VERBS
# =====================================

COMMITMENT_VERBS = {

    "finalize",
    "approve",
    "complete",
    "deploy",
    "implement",
    "confirm",
    "proceed",
    "release"
}


# =====================================
# CONFIDENCE SCORING
# =====================================

def calculate_decision_confidence(sent):

    text = sent.text.lower()

    confidence = 0.0

    for phrase in STRONG_DECISION_PHRASES:

        if phrase in text:
            confidence += 0.45

    for token in sent:

        if (
            token.lemma_.lower()
            in COMMITMENT_VERBS
        ):

            confidence += 0.20

    if any(

        token.text.lower() in {
            "will",
            "must",
            "shall"
        }

        for token in sent
    ):

        confidence += 0.20

    for phrase in UNCERTAIN_PHRASES:

        if phrase in text:
            confidence -= 0.40

    return round(
        max(0.0, min(confidence, 1.0)),
        2
    )


# =====================================
# MAIN DECISION EXTRACTION
# =====================================

def extract_decisions(transcript):

    decisions = []

    for item in transcript:

        doc = nlp(item["text"])

        for sent in doc.sents:

            confidence = (
                calculate_decision_confidence(
                    sent
                )
            )

            if confidence >= 0.40:

                decisions.append({

                    "speaker":
                        item["speaker"],

                    "decision":
                        sent.text.strip(),

                    "decision_confidence":
                        confidence
                })

    # =================================
    # SEMANTIC DEDUPLICATION
    # =================================

    decisions = semantic_deduplicate(

        decisions,

        "decision"
    )

    return decisions