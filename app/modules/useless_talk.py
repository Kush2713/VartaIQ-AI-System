import spacy

from app.modules.context_engine import (
    calculate_context_relevance
)

from app.modules.deduplication import (
    semantic_deduplicate
)

from app.config.ai_config import (
    USELESS_RELEVANCE_THRESHOLD
)

nlp = spacy.load("en_core_web_sm")


# =====================================
# META MEETING TERMS
# =====================================

META_MEETING_TERMS = {

    "meeting",
    "discussion",
    "agenda",
    "timeline",
    "deadline",
    "progress",
    "requirement",
    "update",
    "planning",
    "review"
}


# =====================================
# IMPORTANT CONTEXT TERMS
# =====================================

IMPORTANT_CONTEXT_TERMS = {

    "risk",
    "latency",
    "performance",
    "deployment",
    "client",
    "release",
    "bug",
    "issue",
    "optimization",
    "api",
    "failure",
    "security",
    "authentication",
    "database",
    "backend",
    "frontend",
    "analytics",
    "testing",
    "integration"
}


# =====================================
# FILLER EXPRESSIONS
# =====================================

FILLER_EXPRESSIONS = {

    "umm",
    "uh",
    "hmm",
    "yeah",
    "okay",
    "cool",
    "nice",
    "right",
    "alright"
}


# =====================================
# CHECK FILLER
# =====================================

def is_filler_sentence(sentence):

    cleaned = sentence.lower().strip()

    words = cleaned.split()

    if len(words) <= 3:

        filler_count = sum(

            1 for word in words

            if word in FILLER_EXPRESSIONS
        )

        if filler_count >= 1:
            return True

    return False


# =====================================
# CHECK META DISCUSSION
# =====================================

def is_meta_meeting_sentence(sentence):

    lowered = sentence.lower()

    for word in META_MEETING_TERMS:

        if word in lowered:
            return True

    return False


# =====================================
# IMPORTANT CONTEXT
# =====================================

def is_important_context_sentence(
    sentence
):

    lowered = sentence.lower()

    for term in IMPORTANT_CONTEXT_TERMS:

        if term in lowered:
            return True

    return False


# =====================================
# MAIN DETECTION
# =====================================

def detect_useless_talk(
    transcript,
    context
):

    useless_segments = []

    meeting_embedding = context[
        "meeting_embedding"
    ]

    for item in transcript:

        doc = nlp(item["text"])

        for sent in doc.sents:

            sentence_text = (
                sent.text.strip()
            )

            if len(sentence_text) < 2:
                continue

            # ---------------------------------
            # Filler
            # ---------------------------------

            if is_filler_sentence(
                sentence_text
            ):

                useless_segments.append({

                    "speaker":
                        item["speaker"],

                    "text":
                        sentence_text,

                    "reason":
                        "Filler conversation",

                    "relevance_score":
                        0.0
                })

                continue

            # ---------------------------------
            # Meta discussion
            # ---------------------------------

            if is_meta_meeting_sentence(
                sentence_text
            ):
                continue

            # ---------------------------------
            # IMPORTANT BUSINESS CONTEXT
            # NEVER MARK USELESS
            # ---------------------------------

            if is_important_context_sentence(
                sentence_text
            ):
                continue

            # ---------------------------------
            # Semantic relevance
            # ---------------------------------

            relevance_score = (
                calculate_context_relevance(

                    sentence_text,

                    meeting_embedding
                )
            )

            # ---------------------------------
            # Off-topic
            # ---------------------------------

            if relevance_score < (
                USELESS_RELEVANCE_THRESHOLD
            ):

                useless_segments.append({

                    "speaker":
                        item["speaker"],

                    "text":
                        sentence_text,

                    "reason":
                        "Off-topic discussion",

                    "relevance_score":
                        round(
                            relevance_score,
                            2
                        )
                })

    # =====================================
    # DEDUPLICATION
    # =====================================

    useless_segments = semantic_deduplicate(

        useless_segments,

        "text"
    )

    return {

        "useless_segments":
            useless_segments
    }



































































# # def detect_useless_talk(data):
# #     useless = []

# #     for item in data:
# #         words = item["text"].split()
# #         filler_count = sum(1 for w in words if w.lower() in ["umm", "uh", "okay", "yeah"])

# #         if len(words) <= 2 or (filler_count / len(words)) > 0.4:
# #             useless.append(item)

# #     return useless

# import spacy

# nlp = spacy.load("en_core_web_sm")

# FILLER_WORDS = {
#     "umm",
#     "uh",
#     "yeah",
#     "okay",
#     "hmm",
#     "like"
# }

# IMPORTANT_VERBS = {
#     "deploy",
#     "complete",
#     "finalize",
#     "approve",
#     "design",
#     "integrate",
#     "test",
#     "review",
#     "submit",
#     "prepare"
# }


# def is_meaningful(sent):
#     """
#     Determines whether sentence contains meaningful intent.
#     """

#     for token in sent:

#         # meaningful action verbs
#         if token.lemma_.lower() in IMPORTANT_VERBS:
#             return True

#         # proper nouns often indicate entities/tasks
#         if token.pos_ in {"PROPN", "NOUN"}:
#             return True

#     return False


# def detect_useless_talk(data):
#     useless = []

#     for item in data:

#         doc = nlp(item["text"])

#         for sent in doc.sents:

#             words = [token.text.lower() for token in sent if not token.is_punct]

#             if not words:
#                 continue

#             filler_count = sum(
#                 1 for word in words if word in FILLER_WORDS
#             )

#             filler_ratio = filler_count / len(words)

#             meaningful = is_meaningful(sent)

#             # useless if mostly filler + no meaningful intent
#             if filler_ratio > 0.4 and not meaningful:

#                 useless.append({
#                     "speaker": item["speaker"],
#                     "text": sent.text.strip()
#                 })

#     return useless

# # CURRENT PROBLEMS
# # - False Positives

# # Example:

# # "Okay approved"

# # Important confirmation.

# # Could be marked useless.

# # - No semantic understanding

# # Example:

# # "Yeah let's deploy today"

# # Actually important.

# # But filler exists.

# # - Short sentence ≠ useless

# # Example:

# # "Deployment confirmed"

# # Very important.

# # But short.