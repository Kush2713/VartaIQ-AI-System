# =====================================
# SUMMARY REFINEMENT
# No LLM needed — BART already produces
# clean summaries. We just polish here.
# =====================================

def refine_summary(summary):

    if not summary:
        return summary

    summary = summary.strip()

    # Strip any model prefix artifacts
    for prefix in ("summary:", "result:", "output:"):
        if summary.lower().startswith(prefix):
            summary = summary[len(prefix):].strip()

    # Capitalize first letter
    if summary:
        summary = summary[0].upper() + summary[1:]

    return summary


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

    action_score = breakdown.get(
        "action_score",
        0
    )

    decision_score = breakdown.get(
        "decision_score",
        0
    )

    # ---------------------------------
    # Overall meeting quality insight
    # ---------------------------------

    if final_score >= 80:

        insights.append(

            "Meeting demonstrated strong execution, "
            "high collaboration quality, and clear "
            "decision-making."
        )

    elif final_score >= 60:

        insights.append(

            "Meeting was productive with clear "
            "task ownership and actionable outcomes."
        )

    elif final_score >= 45:

        insights.append(

            "Meeting covered key topics with "
            "reasonable task clarity. Some areas "
            "can be improved for better alignment."
        )

    else:

        insights.append(

            "Meeting had limited structure. "
            "Improving task ownership and reducing "
            "off-topic segments would help."
        )

    # ---------------------------------
    # Action item quality
    # ---------------------------------

    if action_score >= 80:

        insights.append(

            "Strong actionable commitments were "
            "identified with clear ownership."
        )

    elif action_score < 40:

        insights.append(

            "Consider assigning clearer task "
            "ownership in future meetings."
        )

    # ---------------------------------
    # Decision quality
    # ---------------------------------

    if decision_score >= 70:

        insights.append(

            "Decisions were well-defined and "
            "confirmed during the meeting."
        )

    return insights


# =====================================
# SPEAKER INSIGHTS
# =====================================

def generate_speaker_insights(
    speaker_analysis
):

    insights = []

    high_performers = []

    good_performers = []

    low_performers = []

    passive_members = []

    for speaker, data in (
        speaker_analysis.items()
    ):

        effectiveness = data.get(
            "effectiveness_score",
            0
        )

        engagement = data.get(
            "engagement_level",
            "Low"
        )

        is_passive = data.get(
            "passive_participant",
            False
        )

        if is_passive:

            passive_members.append(
                speaker
            )

        elif engagement == "High" or effectiveness >= 55:

            high_performers.append(
                speaker
            )

        elif engagement == "Medium" or effectiveness >= 35:

            good_performers.append(
                speaker
            )

        else:

            low_performers.append(
                speaker
            )

    if high_performers:

        insights.append(

            f"{', '.join(high_performers)} showed "
            f"strong engagement and task-oriented "
            f"contributions."
        )

    if good_performers:

        insights.append(

            f"{', '.join(good_performers)} contributed "
            f"meaningfully to the discussion."
        )

    if low_performers:

        insights.append(

            f"{', '.join(low_performers)} had limited "
            f"participation. Encouraging more "
            f"structured input could help."
        )

    if passive_members:

        insights.append(

            f"{', '.join(passive_members)} had minimal "
            f"speaking time in this meeting."
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