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
    "integration",
    "agreed",
    "decision",
    "finalized",
    "confirmed",
    "officially",
    "must",
    "clustering",
    "semantic",
    "pipeline",
    "architecture",
    "infrastructure"
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
# GREETING / CLOSING PHRASES
# These are socially normal in meetings
# and should never be flagged as useless
# =====================================

GREETING_PHRASES = {

    "good morning",
    "good afternoon",
    "good evening",
    "hello everyone",
    "hi everyone",
    "hi team",
    "hello team",
    "welcome everyone",
    "thanks everyone",
    "thank you everyone",
    "great job",
    "well done",
    "excellent",
    "sounds good",
    "perfect",
    "that's great",
    "good work"
}


# =====================================
# CHECK GREETING / CLOSING
# =====================================

def is_greeting_or_closing(sentence):

    lowered = sentence.lower().strip()

    for phrase in GREETING_PHRASES:

        if lowered.startswith(phrase):
            return True

    return False




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
            # Greeting / closing — always keep
            # ---------------------------------

            if is_greeting_or_closing(
                sentence_text
            ):
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