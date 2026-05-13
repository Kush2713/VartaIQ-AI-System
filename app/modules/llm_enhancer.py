from app.services.model_manager import (
    get_llm_model
)


# =====================================
# LOAD CENTRALIZED LLM
# =====================================

generator = get_llm_model()


# =====================================
# SUMMARY REFINEMENT
# =====================================

def refine_summary(summary):

    prompt = f"""

    Improve this meeting summary professionally.
    Keep it concise, clean, and business-oriented.

    Summary:
    {summary}

    """

    result = generator(

        prompt,

        max_length=180,

        do_sample=False
    )

    return result[0][
        "generated_text"
    ]


# =====================================
# PRODUCTIVITY INSIGHTS
# =====================================

def generate_productivity_insights(
    score
):

    insights = []

    final_score = score.get(
        "final_score",
        0
    )

    breakdown = score.get(
        "breakdown",
        {}
    )

    productivity_score = breakdown.get(
        "productivity_score",
        0
    )

    action_score = breakdown.get(
        "action_score",
        0
    )

    decision_score = breakdown.get(
        "decision_score",
        0
    )

    if final_score >= 85:

        insights.append(

            "Meeting demonstrated strong execution, "
            "high collaboration quality, and clear "
            "decision-making."
        )

    elif final_score >= 70:

        insights.append(

            "Meeting was productive overall, "
            "but execution clarity can still improve."
        )

    else:

        insights.append(

            "Meeting effectiveness was limited due "
            "to unclear alignment, weak actionability, "
            "or low discussion focus."
        )

    if productivity_score < 50:

        insights.append(

            "Discussion lacked strong task-oriented "
            "execution focus."
        )

    if action_score < 50:

        insights.append(

            "Few actionable commitments were "
            "identified during the meeting."
        )

    if decision_score < 50:

        insights.append(

            "Meeting discussions lacked strong "
            "decision finalization."
        )

    return insights


# =====================================
# SPEAKER INSIGHTS
# =====================================

def generate_speaker_insights(
    speaker_analysis
):

    insights = []

    dominant_speakers = []

    passive_members = []

    for speaker, data in (
        speaker_analysis.items()
    ):

        if data.get(
            "dominant_speaker"
        ):

            dominant_speakers.append(
                speaker
            )

        if data.get(
            "passive_participant"
        ):

            passive_members.append(
                speaker
            )

    if dominant_speakers:

        insights.append(

            f"High participation dominance detected "
            f"from: {', '.join(dominant_speakers)}."
        )

    if passive_members:

        insights.append(

            f"Low engagement observed from: "
            f"{', '.join(passive_members)}."
        )

    return insights


# =====================================
# RISK INSIGHTS
# =====================================

def generate_risk_insights(
    sentiment_analysis
):

    insights = []

    risk_count = sentiment_analysis.get(
        "risk_count",
        0
    )

    conflict_count = sentiment_analysis.get(
        "conflict_count",
        0
    )

    if risk_count > 0:

        insights.append(

            f"{risk_count} operational or technical "
            f"risk discussions were detected."
        )

    if conflict_count > 0:

        insights.append(

            f"{conflict_count} conflict or disagreement "
            f"signals were identified."
        )

    return insights


# =====================================
# TOPIC INSIGHTS
# =====================================

def generate_topic_insights(
    topics
):

    insights = []

    if not topics:
        return insights

    top_topics = [

        topic["topic"]

        for topic in topics[:3]
    ]

    insights.append(

        f"Primary meeting focus areas included: "
        f"{', '.join(top_topics)}."
    )

    return insights


# =====================================
# MAIN AI INSIGHTS GENERATOR
# =====================================

def generate_meeting_insights(

    summary,

    score,

    speaker_analysis,

    sentiment_analysis,

    topics
):

    insights = []

    insights.extend(

        generate_productivity_insights(
            score
        )
    )

    insights.extend(

        generate_speaker_insights(
            speaker_analysis
        )
    )

    insights.extend(

        generate_risk_insights(
            sentiment_analysis
        )
    )

    insights.extend(

        generate_topic_insights(
            topics
        )
    )

    unique = []

    seen = set()

    for insight in insights:

        normalized = (
            insight.lower().strip()
        )

        if normalized in seen:
            continue

        seen.add(normalized)

        unique.append(insight)

    return unique[:12]