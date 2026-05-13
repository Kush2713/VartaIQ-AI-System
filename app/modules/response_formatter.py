import re


# =====================================
# TEXT CLEANING
# =====================================

def clean_text(text):

    if not text:
        return ""

    text = str(text)

    # Remove extra spaces
    text = re.sub(
        r"\s+",
        " ",
        text
    )

    # Fix punctuation spacing
    text = re.sub(
        r"\s+([.,!?])",
        r"\1",
        text
    )

    # Remove repeated punctuation
    text = re.sub(
        r"([!?.,])\1+",
        r"\1",
        text
    )

    text = text.strip()

    # Capitalize first letter
    if len(text) > 1:

        text = (
            text[0].upper()
            + text[1:]
        )

    return text


# =====================================
# SUMMARY
# =====================================

def format_summary(summary):

    return clean_text(summary)


# =====================================
# TOPICS
# =====================================

def format_topics(topics):

    formatted = []

    for topic in topics:

        formatted.append({

            "topic":
                clean_text(
                    topic.get(
                        "topic",
                        ""
                    )
                ),

            "relevance_score":
                round(
                    topic.get(
                        "relevance_score",
                        0
                    ),
                    2
                )
        })

    return formatted


# =====================================
# ACTION ITEMS
# =====================================

def format_action_items(
    action_items
):

    formatted = []

    for action in action_items:

        formatted.append({

            "speaker":
                clean_text(
                    action.get(
                        "speaker",
                        ""
                    )
                ),

            "assignee":
                clean_text(
                    action.get(
                        "assignee",
                        ""
                    )
                ),

            "task":
                clean_text(
                    action.get(
                        "task",
                        ""
                    )
                ),

            "deadline":
                clean_text(
                    action.get(
                        "deadline",
                        ""
                    )
                ),

            "priority":
                clean_text(
                    action.get(
                        "priority",
                        "Normal"
                    )
                ),

            "confidence":
                round(
                    action.get(
                        "confidence",
                        0
                    ),
                    2
                )
        })

    return formatted


# =====================================
# DECISIONS
# =====================================

def format_decisions(
    decisions
):

    formatted = []

    for decision in decisions:

        formatted.append({

            "speaker":
                clean_text(
                    decision.get(
                        "speaker",
                        ""
                    )
                ),

            "decision":
                clean_text(
                    decision.get(
                        "decision",
                        ""
                    )
                ),

            "decision_confidence":
                round(
                    decision.get(
                        "decision_confidence",
                        0
                    ),
                    2
                )
        })

    return formatted


# =====================================
# USELESS TALK
# =====================================

def format_useless_talk(
    useless_talk
):

    segments = useless_talk.get(
        "useless_segments",
        []
    )

    formatted_segments = []

    for segment in segments:

        formatted_segments.append({

            "speaker":
                clean_text(
                    segment.get(
                        "speaker",
                        ""
                    )
                ),

            "text":
                clean_text(
                    segment.get(
                        "text",
                        ""
                    )
                ),

            "reason":
                clean_text(
                    segment.get(
                        "reason",
                        ""
                    )
                ),

            "relevance_score":
                round(
                    segment.get(
                        "relevance_score",
                        0
                    ),
                    2
                )
        })

    return {

        "useless_segments":
            formatted_segments
    }


# =====================================
# SPEAKER ANALYSIS
# =====================================

def format_speaker_analysis(
    speaker_analysis
):

    formatted = {}

    for speaker, data in (
        speaker_analysis.items()
    ):

        formatted[
            clean_text(speaker)
        ] = {

            "word_count":
                data.get(
                    "word_count",
                    0
                ),

            "participation_percentage":
                round(
                    data.get(
                        "participation_percentage",
                        0
                    ),
                    2
                ),

            "relevance_ratio":
                round(
                    data.get(
                        "relevance_ratio",
                        0
                    ),
                    2
                ),

            "productivity_ratio":
                round(
                    data.get(
                        "productivity_ratio",
                        0
                    ),
                    2
                ),

            "average_relevance":
                round(
                    data.get(
                        "average_relevance",
                        0
                    ),
                    2
                ),

            "effectiveness_score":
                round(
                    data.get(
                        "effectiveness_score",
                        0
                    ),
                    2
                ),

            "engagement_level":
                clean_text(
                    data.get(
                        "engagement_level",
                        "Unknown"
                    )
                ),

            "dominant_speaker":
                data.get(
                    "dominant_speaker",
                    False
                ),

            "passive_participant":
                data.get(
                    "passive_participant",
                    False
                )
        }

    return formatted


# =====================================
# SENTIMENT ANALYSIS
# =====================================

def format_sentiment_analysis(
    sentiment_analysis
):

    formatted_sentiments = []

    sentiments = sentiment_analysis.get(
        "conversation_sentiments",
        []
    )

    for item in sentiments:

        formatted_sentiments.append({

            "speaker":
                clean_text(
                    item.get(
                        "speaker",
                        ""
                    )
                ),

            "text":
                clean_text(
                    item.get(
                        "text",
                        ""
                    )
                ),

            "sentiment":
                clean_text(
                    item.get(
                        "sentiment",
                        ""
                    )
                ),

            "confidence":
                round(
                    item.get(
                        "confidence",
                        0
                    ),
                    2
                ),

            "relevance_score":
                round(
                    item.get(
                        "relevance_score",
                        0
                    ),
                    2
                )
        })

    return {

        "overall_sentiment":
            clean_text(
                sentiment_analysis.get(
                    "overall_sentiment",
                    "Unknown"
                )
            ),

        "overall_score":
            round(
                sentiment_analysis.get(
                    "overall_score",
                    0
                ),
                2
            ),
            
        "operational_risk_level":
            clean_text(
                sentiment_analysis.get(
                    "operational_risk_level",
                    "Unknown"
                )
            ),

        "risk_count":
            sentiment_analysis.get(
                "risk_count",
                0
            ),

        "conflict_count":
            sentiment_analysis.get(
                "conflict_count",
                0
            ),

        "risks":
            sentiment_analysis.get(
                "risks",
                []
            ),

        "conflicts":
            sentiment_analysis.get(
                "conflicts",
                []
            ),

        "conversation_sentiments":
            formatted_sentiments
    }


# =====================================
# SCORE FORMATTER
# =====================================

def format_score(score):

    breakdown = score.get(
        "breakdown",
        {}
    )

    return {

        "final_score":
            round(
                score.get(
                    "final_score",
                    0
                ),
                2
            ),

        "rating":
            clean_text(
                score.get(
                    "rating",
                    "Unknown"
                )
            ),

        "breakdown": {

            "productivity_score":
                round(
                    breakdown.get(
                        "productivity_score",
                        0
                    ),
                    2
                ),

            "relevance_score":
                round(
                    breakdown.get(
                        "relevance_score",
                        0
                    ),
                    2
                ),

            "balance_score":
                round(
                    breakdown.get(
                        "balance_score",
                        0
                    ),
                    2
                ),

            "action_score":
                round(
                    breakdown.get(
                        "action_score",
                        0
                    ),
                    2
                ),

            "decision_score":
                round(
                    breakdown.get(
                        "decision_score",
                        0
                    ),
                    2
                ),

            "conversation_score":
                round(
                    breakdown.get(
                        "conversation_score",
                        0
                    ),
                    2
                )
        }
    }


# =====================================
# FOLLOWUPS
# =====================================

def format_followups(
    followups
):

    return [
        clean_text(item)
        for item in followups
    ]


# =====================================
# AI INSIGHTS
# =====================================

def format_ai_insights(
    insights
):

    return [
        clean_text(insight)
        for insight in insights
    ]