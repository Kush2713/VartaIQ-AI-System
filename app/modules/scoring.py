# def calculate_score(summary, action_items, useless, speaker_analysis, decisions):

#     useful_score = max(100 - (len(useless) * 5), 0)
#     action_score = min(len(action_items) * 20, 100)
#     decision_score = min(len(decisions) * 20, 100)

#     percentages = [v["percentage"] for v in speaker_analysis.values()]

#     balance_score = 100 - (max(percentages) - min(percentages)) if len(percentages) > 1 else 50

#     final = int(
#         0.3 * useful_score +
#         0.25 * action_score +
#         0.25 * decision_score +
#         0.2 * balance_score
#     )

#     return {
#         "final_score": final,
#         "rating": "Excellent" if final > 75 else "Good" if final > 50 else "Poor",
#         "breakdown": {
#             "useful_score": useful_score,
#             "action_score": action_score,
#             "decision_score": decision_score,
#             "balance_score": balance_score
#         }
#     }
# {
#   "final_score": 82,
#   "rating": "Excellent"
# }
PRODUCTIVE_KEYWORDS = {
    "complete",
    "finalize",
    "deploy",
    "implement",
    "design",
    "integrate",
    "review",
    "submit",
    "approve",
    "deliver",
    "prepare",
    "test"
}


def calculate_productivity(transcript):
    """
    Estimates how task-oriented and productive
    the meeting discussion is.
    """

    productive_sentences = 0

    for item in transcript:

        text = item["text"].lower()

        if any(keyword in text for keyword in PRODUCTIVE_KEYWORDS):
            productive_sentences += 1

    if len(transcript) == 0:
        return 0

    productivity_ratio = productive_sentences / len(transcript)

    return round(productivity_ratio * 100, 2)


def calculate_balance_score(speaker_analysis):

    percentages = [
        v["percentage"]
        for v in speaker_analysis.values()
    ]

    if len(percentages) <= 1:
        return 50

    imbalance = max(percentages) - min(percentages)

    return max(0, round(100 - imbalance, 2))


def calculate_score(
    transcript,
    summary,
    action_items,
    useless,
    speaker_analysis,
    decisions
):
    """
    Hybrid meeting quality scoring.
    """

    # 1. Productivity score
    productivity_score = calculate_productivity(transcript)

    # 2. Actionability score
    action_score = min(len(action_items) * 15, 100)

    # 3. Decision score
    decision_score = min(len(decisions) * 15, 100)

    # 4. Conversational quality
    useless_penalty = min(len(useless) * 10, 50)

    conversation_score = max(100 - useless_penalty, 0)

    # 5. Speaker participation balance
    balance_score = calculate_balance_score(
        speaker_analysis
    )

    # Final weighted score
    final_score = round(
        (
            productivity_score * 0.30 +
            action_score * 0.20 +
            decision_score * 0.20 +
            conversation_score * 0.15 +
            balance_score * 0.15
        ),
        2
    )

    # Rating
    if final_score >= 80:
        rating = "Excellent"
    elif final_score >= 60:
        rating = "Good"
    elif final_score >= 40:
        rating = "Average"
    else:
        rating = "Poor"

    return {
        "final_score": final_score,
        "rating": rating,
        "breakdown": {
            "productivity_score": productivity_score,
            "action_score": action_score,
            "decision_score": decision_score,
            "conversation_score": conversation_score,
            "balance_score": balance_score
        }
    }