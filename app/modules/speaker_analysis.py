import spacy

from collections import defaultdict

from app.modules.context_engine import (
    calculate_context_relevance
)

nlp = spacy.load(
    "en_core_web_sm"
)

# =====================================
# CONFIGURATION
# =====================================

MIN_RELEVANCE_THRESHOLD = 0.30

DOMINANT_THRESHOLD = 35

PASSIVE_THRESHOLD = 10

# Adjusted to match realistic effectiveness score range.
# The formula produces scores roughly in 20-70 range for
# typical meeting participants, so thresholds are calibrated
# accordingly rather than using absolute 75/45 cutoffs.
HIGH_ENGAGEMENT_SCORE = 55

MEDIUM_ENGAGEMENT_SCORE = 30


# =====================================
# PRODUCTIVE VERBS
# =====================================

PRODUCTIVE_VERBS = {

    "complete",
    "deploy",
    "implement",
    "design",
    "review",
    "optimize",
    "improve",
    "finalize",
    "prepare",
    "integrate",
    "test",
    "create",
    "fix",
    "analyze",
    "document"
}


# =====================================
# STRATEGIC TERMS
# =====================================

STRATEGIC_TERMS = {

    "deploy",
    "architecture",
    "optimize",
    "release",
    "integration",
    "priority",
    "decision",
    "deadline",
    "risk",
    "scaling",
    "latency",
    "performance",
    "client",
    "api",
    "security",
    "authentication"
}


# =====================================
# DECISION TERMS
# =====================================

DECISION_TERMS = {

    "decided",
    "finalized",
    "approved",
    "confirmed",
    "agreed",
    "officially",
    "decision"
}


# =====================================
# COLLABORATION TERMS
# =====================================

COLLABORATION_TERMS = {

    "we",
    "team",
    "together",
    "collaborate",
    "support",
    "coordinate",
    "help"
}


# =====================================
# PRODUCTIVE SENTENCE
# =====================================

def is_productive_sentence(
    sentence
):

    doc = nlp(sentence)

    for token in doc:

        if (
            token.lemma_.lower()
            in PRODUCTIVE_VERBS
        ):
            return True

    return False


# =====================================
# DECISION SENTENCE
# =====================================

def is_decision_sentence(
    sentence
):

    lowered = sentence.lower()

    for term in DECISION_TERMS:

        if term in lowered:
            return True

    return False


# =====================================
# STRATEGIC SENTENCE
# =====================================

def is_strategic_sentence(
    sentence
):

    lowered = sentence.lower()

    for term in STRATEGIC_TERMS:

        if term in lowered:
            return True

    return False


# =====================================
# COLLABORATION SENTENCE
# =====================================

def is_collaboration_sentence(
    sentence
):

    lowered = sentence.lower()

    for term in COLLABORATION_TERMS:

        if term in lowered:
            return True

    return False


# =====================================
# ENGAGEMENT LEVEL
# =====================================

def determine_engagement_level(
    score
):

    if score >= (
        HIGH_ENGAGEMENT_SCORE
    ):
        return "High"

    if score >= (
        MEDIUM_ENGAGEMENT_SCORE
    ):
        return "Medium"

    return "Low"


# =====================================
# MAIN ANALYSIS
# =====================================

def analyze_speakers(
    transcript,
    context
):

    meeting_embedding = context[
        "meeting_embedding"
    ]

    speaker_stats = defaultdict(

        lambda: {

            "word_count": 0,

            "relevant_sentences": 0,

            "productive_sentences": 0,

            "decision_sentences": 0,

            "strategic_sentences": 0,

            "collaboration_sentences": 0,

            "total_sentences": 0,

            "relevance_scores": []
        }
    )

    total_words = 0

    # =================================
    # PROCESS TRANSCRIPT
    # =================================

    for item in transcript:

        speaker = item.get(
            "speaker",
            "Unknown"
        )

        text = item.get(
            "text",
            ""
        ).strip()

        if not text:
            continue

        doc = nlp(text)

        words = [

            token.text

            for token in doc

            if not token.is_punct
        ]

        word_count = len(words)

        total_words += word_count

        speaker_stats[speaker][
            "word_count"
        ] += word_count

        # ---------------------------------
        # Sentence level analysis
        # ---------------------------------

        for sent in doc.sents:

            sentence = (
                sent.text.strip()
            )

            if not sentence:
                continue

            speaker_stats[speaker][
                "total_sentences"
            ] += 1

            # -----------------------------
            # Relevance
            # -----------------------------

            relevance_score = (
                calculate_context_relevance(

                    sentence,

                    meeting_embedding
                )
            )

            speaker_stats[speaker][
                "relevance_scores"
            ].append(
                relevance_score
            )

            if relevance_score >= (
                MIN_RELEVANCE_THRESHOLD
            ):

                speaker_stats[speaker][
                    "relevant_sentences"
                ] += 1

            # -----------------------------
            # Productive
            # -----------------------------

            if is_productive_sentence(
                sentence
            ):

                speaker_stats[speaker][
                    "productive_sentences"
                ] += 1

            # -----------------------------
            # Decision
            # -----------------------------

            if is_decision_sentence(
                sentence
            ):

                speaker_stats[speaker][
                    "decision_sentences"
                ] += 1

            # -----------------------------
            # Strategic contribution
            # -----------------------------

            if is_strategic_sentence(
                sentence
            ):

                speaker_stats[speaker][
                    "strategic_sentences"
                ] += 1

            # -----------------------------
            # Collaboration
            # -----------------------------

            if is_collaboration_sentence(
                sentence
            ):

                speaker_stats[speaker][
                    "collaboration_sentences"
                ] += 1

    # =================================
    # FINAL METRICS
    # =================================

    final_analysis = {}

    for speaker, stats in (
        speaker_stats.items()
    ):

        word_count = stats[
            "word_count"
        ]

        participation = 0

        if total_words > 0:

            participation = (

                word_count
                / total_words

            ) * 100

        total_sentences = max(

            stats["total_sentences"],

            1
        )

        relevance_ratio = (

            stats["relevant_sentences"]
            / total_sentences

        ) * 100

        productivity_ratio = (

            stats["productive_sentences"]
            / total_sentences

        ) * 100

        decision_ratio = (

            stats["decision_sentences"]
            / total_sentences

        ) * 100

        strategic_ratio = (

            stats["strategic_sentences"]
            / total_sentences

        ) * 100

        collaboration_ratio = (

            stats[
                "collaboration_sentences"
            ]
            / total_sentences

        ) * 100

        avg_relevance = 0

        if stats[
            "relevance_scores"
        ]:

            avg_relevance = (

                sum(
                    stats[
                        "relevance_scores"
                    ]
                )

                / len(
                    stats[
                        "relevance_scores"
                    ]
                )
            )

        # =================================
        # NORMALIZED RELEVANCE
        # =================================

        normalized_relevance = min(

            avg_relevance * 200,

            100
        )

        # =================================
        # ENTERPRISE EFFECTIVENESS SCORE
        # =================================

        effectiveness_score = (

            normalized_relevance
            * 0.30

            +

            participation
            * 0.20

            +

            productivity_ratio
            * 0.20

            +

            decision_ratio
            * 0.15

            +

            strategic_ratio
            * 0.10

            +

            collaboration_ratio
            * 0.05
        )

        engagement_level = (
            determine_engagement_level(
                effectiveness_score
            )
        )

        dominant_speaker = (
            participation >=
            DOMINANT_THRESHOLD
        )

        passive_participant = (
            participation <=
            PASSIVE_THRESHOLD
        )

        final_analysis[speaker] = {

            "word_count":
                word_count,

            "participation_percentage":
                round(
                    participation,
                    2
                ),

            "relevance_ratio":
                round(
                    relevance_ratio,
                    2
                ),

            "productivity_ratio":
                round(
                    productivity_ratio,
                    2
                ),

            "decision_ratio":
                round(
                    decision_ratio,
                    2
                ),

            "strategic_ratio":
                round(
                    strategic_ratio,
                    2
                ),

            "collaboration_ratio":
                round(
                    collaboration_ratio,
                    2
                ),

            "average_relevance":
                round(
                    avg_relevance,
                    2
                ),

            "normalized_relevance":
                round(
                    normalized_relevance,
                    2
                ),

            "effectiveness_score":
                round(
                    effectiveness_score,
                    2
                ),

            "engagement_level":
                engagement_level,

            "dominant_speaker":
                dominant_speaker,

            "passive_participant":
                passive_participant
        }

    return final_analysis
