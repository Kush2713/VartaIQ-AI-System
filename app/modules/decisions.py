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

































# import spacy

# nlp = spacy.load("en_core_web_sm")


# CONFIRMED_DECISION_KEYWORDS = {
#     "finalize",
#     "finalized",
#     "decide",
#     "decided",
#     "agreed",
#     "approve",
#     "approved",
#     "confirm",
#     "confirmed"
# }


# PROPOSAL_KEYWORDS = {
#     "should",
#     "could",
#     "maybe",
#     "suggest",
#     "propose",
#     "plan"
# }


# PLANNING_PHRASES = {
#     "let's",
#     "plan is",
#     "we will"
# }


# def classify_decision(text):
#     """
#     Classifies decision intent.
#     """

#     lowered = text.lower()

#     # --------------------------
#     # Confirmed Decisions
#     # --------------------------

#     if any(
#         keyword in lowered
#         for keyword in
#         CONFIRMED_DECISION_KEYWORDS
#     ):
#         return (
#             "Confirmed Decision",
#             0.90
#         )

#     # --------------------------
#     # Planning Decisions
#     # --------------------------

#     if any(
#         phrase in lowered
#         for phrase in
#         PLANNING_PHRASES
#     ):
#         return (
#             "Planning Decision",
#             0.75
#         )

#     # --------------------------
#     # Proposal / Suggestion
#     # --------------------------

#     if any(
#         keyword in lowered
#         for keyword in
#         PROPOSAL_KEYWORDS
#     ):
#         return (
#             "Proposal",
#             0.60
#         )

#     return (
#         None,
#         0
#     )


# def extract_decisions(transcript):

#     decisions = []

#     for item in transcript:

#         doc = nlp(item["text"])

#         for sent in doc.sents:

#             sentence_text = (
#                 sent.text.strip()
#             )

#             (
#                 decision_type,
#                 confidence
#             ) = classify_decision(
#                 sentence_text
#             )

#             if decision_type:

#                 decisions.append({

#                     "speaker":
#                         item["speaker"],

#                     "decision":
#                         sentence_text,

#                     "decision_type":
#                         decision_type,

#                     "confidence":
#                         confidence
#                 })

#     return decisions











































# # # def extract_decisions(transcript):
# # #     decisions = []

# # #     keywords = [
# # #         "decide", "decided", "finalize", "agreed",
# # #         "we will", "let's", "plan is"
# # #     ]

# # #     for item in transcript:
# # #         text = item["text"].lower()

# # #         if any(k in text for k in keywords):
# # #             decisions.append({
# # #                 "speaker": item["speaker"],
# # #                 "decision": item["text"]
# # #             })

# # #     return decisions
# # import spacy

# # nlp = spacy.load("en_core_web_sm")

# # DECISION_KEYWORDS = {
# #     "finalize",
# #     "decide",
# #     "decided",
# #     "agreed",
# #     "approve",
# #     "approved",
# #     "confirm",
# #     "confirmed",
# #     "plan"
# # }

# # MODAL_DECISION_WORDS = {
# #     "will",
# #     "shall"
# # }


# # def is_decision_sentence(sent):
# #     text = sent.text.lower()

# #     # Rule 1: Important decision keywords
# #     if any(word in text for word in DECISION_KEYWORDS):
# #         return True

# #     # Rule 2: Detect commitment/finalization structure
# #     for token in sent:
# #         if token.lemma_.lower() in MODAL_DECISION_WORDS:
# #             if any(child.dep_ == "xcomp" or child.pos_ == "VERB" for child in token.children):
# #                 return True

# #     # Rule 3: Detect planning intent
# #     if "let's" in text or "plan is" in text:
# #         return True

# #     return False


# # def extract_decisions(transcript):
# #     decisions = []

# #     for item in transcript:
# #         doc = nlp(item["text"])

# #         for sent in doc.sents:
# #             if is_decision_sentence(sent):
# #                 decisions.append({
# #                     "speaker": item["speaker"],
# #                     "decision": sent.text.strip()
# #                 })

# #     return decisions

# # # WHY THIS IS BETTER
# # # Before:
# # # keyword exists → decision

# # # Very weak.

# # # Now:

# # # We analyze:

# # # sentence structure
# # # verbs
# # # modal intent
# # # planning language
# # # commitment semantics

# # # This is:

# # # much more NLP-driven