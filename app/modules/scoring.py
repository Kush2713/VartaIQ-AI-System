# =====================================
# CONTEXTUAL MEETING SCORING
# =====================================


# =====================================
# PRODUCTIVITY SCORE
# =====================================

def calculate_productivity_score(
    speaker_analysis
):
    """
    Uses semantic productivity ratios
    from speaker intelligence.
    """

    if not speaker_analysis:
        return 0

    total = 0

    for speaker_data in (
        speaker_analysis.values()
    ):

        total += speaker_data[
            "productivity_ratio"
        ]

    return round(
        total / len(speaker_analysis),
        2
    )


# =====================================
# RELEVANCE SCORE
# =====================================

def calculate_relevance_score(
    speaker_analysis
):
    """
    Average contextual relevance.
    """

    if not speaker_analysis:
        return 0

    total = 0

    for speaker_data in (
        speaker_analysis.values()
    ):

        total += speaker_data[
            "average_relevance"
        ]

    return round(
        (total / len(speaker_analysis)) * 100,
        2
    )


# =====================================
# PARTICIPATION BALANCE
# =====================================

def calculate_balance_score(
    speaker_analysis
):

    if not speaker_analysis:
        return 0

    participation_values = [

        speaker_data[
            "participation_percentage"
        ]

        for speaker_data in (
            speaker_analysis.values()
        )
    ]

    imbalance = (
        max(participation_values)
        -
        min(participation_values)
    )

    balance_score = max(
        0,
        100 - imbalance
    )

    return round(balance_score, 2)


# =====================================
# ACTIONABILITY SCORE
# =====================================

def calculate_action_score(
    action_items
):

    if not action_items:
        return 0

    total_confidence = 0

    for action in action_items:

        total_confidence += (
            action.get(
                "confidence",
                0.5
            ) * 100
        )

    score = (
        total_confidence
        /
        len(action_items)
    )

    return round(score, 2)


# =====================================
# DECISION SCORE
# =====================================

def calculate_decision_score(
    decisions
):

    if not decisions:
        return 0

    total_confidence = 0

    for decision in decisions:

        total_confidence += (
            decision.get(
                "decision_confidence",
                0.5
            ) * 100
        )

    score = (
        total_confidence
        /
        len(decisions)
    )

    return round(score, 2)


# =====================================
# CONVERSATION QUALITY
# =====================================

def calculate_conversation_score(
    useless_talk,
    transcript
):

    if not transcript:
        return 0

    useless_segments = useless_talk.get(
        "useless_segments",
        []
    )

    useless_ratio = (
        len(useless_segments)
        /
        len(transcript)
    )

    penalty = useless_ratio * 100

    conversation_score = max(
        0,
        100 - penalty
    )

    return round(
        conversation_score,
        2
    )


# =====================================
# FINAL MEETING SCORE
# =====================================

def calculate_score(

    transcript,

    summary,

    action_items,

    useless_talk,

    speaker_analysis,

    decisions
):

    # ---------------------------------
    # Core metrics
    # ---------------------------------

    productivity_score = (
        calculate_productivity_score(
            speaker_analysis
        )
    )

    relevance_score = (
        calculate_relevance_score(
            speaker_analysis
        )
    )

    balance_score = (
        calculate_balance_score(
            speaker_analysis
        )
    )

    action_score = (
        calculate_action_score(
            action_items
        )
    )

    decision_score = (
        calculate_decision_score(
            decisions
        )
    )

    conversation_score = (
        calculate_conversation_score(

            useless_talk,

            transcript
        )
    )

    # ---------------------------------
    # Weighted final score
    # ---------------------------------

    final_score = round(

        (
            productivity_score * 0.15 +

            relevance_score * 0.15 +

            balance_score * 0.15 +

            action_score * 0.25 +

            decision_score * 0.20 +

            conversation_score * 0.10
        ),

        2
    )

    # ---------------------------------
    # Final rating
    # Thresholds calibrated to realistic
    # score distributions from the formula
    # ---------------------------------

    if final_score >= 75:

        rating = "Excellent"

    elif final_score >= 58:

        rating = "Good"

    elif final_score >= 40:

        rating = "Average"

    else:

        rating = "Poor"

    # ---------------------------------
    # Final output
    # ---------------------------------

    return {

        "final_score":
            final_score,

        "rating":
            rating,

        "breakdown": {

            "productivity_score":
                productivity_score,

            "relevance_score":
                relevance_score,

            "balance_score":
                balance_score,

            "action_score":
                action_score,

            "decision_score":
                decision_score,

            "conversation_score":
                conversation_score
        }
    }