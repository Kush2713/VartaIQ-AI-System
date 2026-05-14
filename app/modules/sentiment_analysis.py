import spacy

from app.services.model_manager import (
    get_sentiment_model
)

from app.modules.context_engine import (
    calculate_context_relevance
)

nlp = spacy.load(
    "en_core_web_sm"
)

# =====================================
# LOAD SENTIMENT MODEL (HF API)
# =====================================

sentiment_pipeline = get_sentiment_model()

# =====================================
# CONFIGURATION
# =====================================

MIN_RELEVANCE_SCORE = 0.30

# =====================================
# TECHNICAL RISK TERMS
# =====================================

TECHNICAL_RISK_TERMS = {

    "latency",
    "failure",
    "crash",
    "downtime",
    "memory",
    "cpu",
    "gpu",
    "bug",
    "issue",
    "blocker",
    "delay",
    "deployment failed",
    "risk",
    "timeout",
    "slow",
    "optimization",
    "overload",
    "bottleneck",
    "scaling",
    "performance",
    "memory leak",
    "fallback"
}

# =====================================
# CONFLICT TERMS
# =====================================

CONFLICT_TERMS = {

    "angry",
    "frustrated",
    "upset",
    "blame",
    "argument",
    "conflict",
    "unacceptable",
    "terrible",
    "hate",
    "disappointed",
    "not happy",
    "bad communication"
}

# =====================================
# POSITIVE TERMS
# =====================================

POSITIVE_TERMS = {

    "great",
    "good",
    "excellent",
    "nice",
    "success",
    "completed",
    "improved",
    "working",
    "stable",
    "optimized",
    "resolved",
    "clean"
}

# =====================================
# DETECT OPERATIONAL RISK
# =====================================

def detect_operational_risk(
    text
):

    lowered = text.lower()

    matched_terms = []

    for term in (
        TECHNICAL_RISK_TERMS
    ):

        if term in lowered:

            matched_terms.append(
                term
            )

    return matched_terms


# =====================================
# DETECT CONFLICT
# =====================================

def detect_conflict(text):

    lowered = text.lower()

    matched_terms = []

    for term in (
        CONFLICT_TERMS
    ):

        if term in lowered:

            matched_terms.append(
                term
            )

    return matched_terms


# =====================================
# SENTIMENT NORMALIZATION
# =====================================

def normalize_sentiment(
    label
):

    label = label.lower()

    if "positive" in label:
        return "Positive"

    if "negative" in label:
        return "Negative"

    return "Neutral"


# =====================================
# CALCULATE NUMERIC SCORE
# =====================================

def calculate_sentiment_score(
    sentiment,
    confidence
):

    if sentiment == "Positive":

        return (
            0.5 + (confidence * 0.5)
        )

    if sentiment == "Negative":

        return (
            -0.5 - (confidence * 0.5)
        )

    return 0.0


# =====================================
# MAIN ANALYSIS
# =====================================

def analyze_sentiment(
    transcript,
    context
):

    meeting_embedding = context[
        "meeting_embedding"
    ]

    conversation_sentiments = []

    total_score = 0

    sentiment_count = 0

    risk_count = 0

    conflict_count = 0

    risks = []

    conflicts = []

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

        # -----------------------------
        # Relevance Filtering
        # -----------------------------

        relevance_score = (
            calculate_context_relevance(

                text,

                meeting_embedding
            )
        )

        if relevance_score < (
            MIN_RELEVANCE_SCORE
        ):
            continue

        # -----------------------------
        # Sentiment Model
        # -----------------------------

        try:

            result = sentiment_pipeline(
                text
            )[0]

            sentiment = (
                normalize_sentiment(
                    result["label"]
                )
            )

            confidence = float(
                result["score"]
            )

        except Exception:

            sentiment = "Neutral"

            confidence = 0.5

        # -----------------------------
        # Detect Operational Risks
        # -----------------------------

        detected_risks = (
            detect_operational_risk(
                text
            )
        )

        risk_detected = (
            len(detected_risks) > 0
        )

        if risk_detected:

            risk_count += 1

            risks.append({

                "speaker":
                    speaker,

                "text":
                    text,

                "risk_terms":
                    detected_risks
            })

        # -----------------------------
        # Detect Conflict
        # -----------------------------

        detected_conflicts = (
            detect_conflict(
                text
            )
        )

        conflict_detected = (
            len(detected_conflicts)
            > 0
        )

        if conflict_detected:

            conflict_count += 1

            conflicts.append({

                "speaker":
                    speaker,

                "text":
                    text,

                "conflict_terms":
                    detected_conflicts
            })

        # -----------------------------
        # Technical Risk != Negative
        # -----------------------------

        if (
            risk_detected
            and sentiment == "Negative"
            and not conflict_detected
        ):

            sentiment = "Neutral"

        # -----------------------------
        # Calculate Score
        # -----------------------------

        sentiment_score = (
            calculate_sentiment_score(

                sentiment,

                confidence
            )
        )

        total_score += (
            sentiment_score
        )

        sentiment_count += 1

        # -----------------------------
        # Store Result
        # -----------------------------

        conversation_sentiments.append({

            "speaker":
                speaker,

            "text":
                text,

            "sentiment":
                sentiment,

            "confidence":
                round(
                    confidence,
                    2
                ),

            "relevance_score":
                round(
                    relevance_score,
                    2
                ),

            "risk_detected":
                risk_detected,

            "conflict_detected":
                conflict_detected
        })

    # =================================
    # OVERALL SCORE
    # =================================

    if sentiment_count == 0:

        overall_score = 50

    else:

        normalized = (
            total_score
            / sentiment_count
        )

        overall_score = int(

            ((normalized + 1) / 2)
            * 100
        )

    # =================================
    # OVERALL SENTIMENT
    # =================================

    if overall_score >= 70:

        overall_sentiment = (
            "Positive"
        )

    elif overall_score >= 40:

        overall_sentiment = (
            "Neutral"
        )

    else:

        overall_sentiment = (
            "Negative"
        )

    # =================================
    # OPERATIONAL RISK LEVEL
    # =================================

    if risk_count >= 6:

        operational_risk_level = (
            "High"
        )

    elif risk_count >= 3:

        operational_risk_level = (
            "Medium"
        )

    else:

        operational_risk_level = (
            "Low"
        )

    # =================================
    # FINAL RESPONSE
    # =================================

    return {

        "overall_sentiment":
            overall_sentiment,

        "overall_score":
            overall_score,

        "operational_risk_level":
            operational_risk_level,

        "risk_count":
            risk_count,

        "conflict_count":
            conflict_count,

        "risks":
            risks,

        "conflicts":
            conflicts,

        "conversation_sentiments":
            conversation_sentiments
    }