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



# PRODUCTIVE_KEYWORDS = {
#     "complete",
#     "finalize",
#     "deploy",
#     "implement",
#     "design",
#     "integrate",
#     "review",
#     "submit",
#     "approve",
#     "deliver",
#     "prepare",
#     "test",
#     "optimize",
#     "improve",
#     "fix"
# }


# def calculate_productivity(transcript):
#     """
#     Estimates how productive and
#     task-oriented the meeting is.
#     """

#     productive_sentences = 0

#     for item in transcript:

#         text = item["text"].lower()

#         if any(
#             keyword in text
#             for keyword in PRODUCTIVE_KEYWORDS
#         ):
#             productive_sentences += 1

#     if len(transcript) == 0:
#         return 0

#     productivity_ratio = (
#         productive_sentences / len(transcript)
#     )

#     return round(productivity_ratio * 100, 2)


# def calculate_balance_score(
#     speaker_analysis
# ):
#     """
#     Measures participation balance.
#     """

#     percentages = [
#         v["percentage"]
#         for v in speaker_analysis.values()
#     ]

#     if len(percentages) <= 1:
#         return 50

#     imbalance = (
#         max(percentages) - min(percentages)
#     )

#     return max(0, round(100 - imbalance, 2))


# def calculate_relevance_penalty(
#     useless_segments
# ):
#     """
#     Penalizes off-topic discussion.
#     """

#     if not useless_segments:
#         return 0

#     penalty = 0

#     for segment in useless_segments:

#         reason = segment.get("reason", "")

#         relevance_score = segment.get(
#             "relevance_score",
#             1
#         )

#         # Strong penalty for off-topic
#         if reason == "Off-topic discussion":
#             penalty += (
#                 (1 - relevance_score) * 25
#             )

#         # Smaller penalty for fillers
#         else:
#             penalty += 5

#     return min(round(penalty, 2), 50)


# def calculate_score(
#     transcript,
#     summary,
#     action_items,
#     useless_segments,
#     speaker_analysis,
#     decisions
# ):
#     """
#     Context-aware hybrid meeting scoring.
#     """

#     # ---------------------------------
#     # 1. Productivity
#     # ---------------------------------

#     productivity_score = (
#         calculate_productivity(
#             transcript
#         )
#     )

#     # ---------------------------------
#     # 2. Actionability
#     # ---------------------------------

#     action_score = min(
#         len(action_items) * 12,
#         100
#     )

#     # ---------------------------------
#     # 3. Decision Intelligence
#     # ---------------------------------

#     decision_score = min(
#         len(decisions) * 12,
#         100
#     )

#     # ---------------------------------
#     # 4. Conversation Quality
#     # ---------------------------------

#     relevance_penalty = (
#         calculate_relevance_penalty(
#             useless_segments
#         )
#     )

#     conversation_score = max(
#         100 - relevance_penalty,
#         0
#     )

#     # ---------------------------------
#     # 5. Speaker Participation
#     # ---------------------------------

#     balance_score = (
#         calculate_balance_score(
#             speaker_analysis
#         )
#     )

#     # ---------------------------------
#     # Final Weighted Score
#     # ---------------------------------

#     final_score = round(

#         (
#             productivity_score * 0.30 +

#             action_score * 0.20 +

#             decision_score * 0.20 +

#             conversation_score * 0.15 +

#             balance_score * 0.15
#         ),

#         2
#     )

#     # ---------------------------------
#     # Rating
#     # ---------------------------------

#     if final_score >= 85:
#         rating = "Excellent"

#     elif final_score >= 70:
#         rating = "Good"

#     elif final_score >= 50:
#         rating = "Average"

#     else:
#         rating = "Poor"

#     return {

#         "final_score": final_score,

#         "rating": rating,

#         "breakdown": {

#             "productivity_score":
#                 productivity_score,

#             "action_score":
#                 action_score,

#             "decision_score":
#                 decision_score,

#             "conversation_score":
#                 conversation_score,

#             "balance_score":
#                 balance_score,

#             "relevance_penalty":
#                 relevance_penalty
#         }
#     }























































# # # def calculate_score(summary, action_items, useless, speaker_analysis, decisions):

# # #     useful_score = max(100 - (len(useless) * 5), 0)
# # #     action_score = min(len(action_items) * 20, 100)
# # #     decision_score = min(len(decisions) * 20, 100)

# # #     percentages = [v["percentage"] for v in speaker_analysis.values()]

# # #     balance_score = 100 - (max(percentages) - min(percentages)) if len(percentages) > 1 else 50

# # #     final = int(
# # #         0.3 * useful_score +
# # #         0.25 * action_score +
# # #         0.25 * decision_score +
# # #         0.2 * balance_score
# # #     )

# # #     return {
# # #         "final_score": final,
# # #         "rating": "Excellent" if final > 75 else "Good" if final > 50 else "Poor",
# # #         "breakdown": {
# # #             "useful_score": useful_score,
# # #             "action_score": action_score,
# # #             "decision_score": decision_score,
# # #             "balance_score": balance_score
# # #         }
# # #     }
# # # {
# # #   "final_score": 82,
# # #   "rating": "Excellent"
# # # }
# # PRODUCTIVE_KEYWORDS = {
# #     "complete",
# #     "finalize",
# #     "deploy",
# #     "implement",
# #     "design",
# #     "integrate",
# #     "review",
# #     "submit",
# #     "approve",
# #     "deliver",
# #     "prepare",
# #     "test"
# # }


# # def calculate_productivity(transcript):
# #     """
# #     Estimates how task-oriented and productive
# #     the meeting discussion is.
# #     """

# #     productive_sentences = 0

# #     for item in transcript:

# #         text = item["text"].lower()

# #         if any(keyword in text for keyword in PRODUCTIVE_KEYWORDS):
# #             productive_sentences += 1

# #     if len(transcript) == 0:
# #         return 0

# #     productivity_ratio = productive_sentences / len(transcript)

# #     return round(productivity_ratio * 100, 2)


# # def calculate_balance_score(speaker_analysis):

# #     percentages = [
# #         v["percentage"]
# #         for v in speaker_analysis.values()
# #     ]

# #     if len(percentages) <= 1:
# #         return 50

# #     imbalance = max(percentages) - min(percentages)

# #     return max(0, round(100 - imbalance, 2))


# # def calculate_score(
# #     transcript,
# #     summary,
# #     action_items,
# #     useless,
# #     speaker_analysis,
# #     decisions
# # ):
# #     """
# #     Hybrid meeting quality scoring.
# #     """

# #     # 1. Productivity score
# #     productivity_score = calculate_productivity(transcript)

# #     # 2. Actionability score
# #     action_score = min(len(action_items) * 15, 100)

# #     # 3. Decision score
# #     decision_score = min(len(decisions) * 15, 100)

# #     # 4. Conversational quality
# #     useless_penalty = min(len(useless) * 10, 50)

# #     conversation_score = max(100 - useless_penalty, 0)

# #     # 5. Speaker participation balance
# #     balance_score = calculate_balance_score(
# #         speaker_analysis
# #     )

# #     # Final weighted score
# #     final_score = round(
# #         (
# #             productivity_score * 0.30 +
# #             action_score * 0.20 +
# #             decision_score * 0.20 +
# #             conversation_score * 0.15 +
# #             balance_score * 0.15
# #         ),
# #         2
# #     )

# #     # Rating
# #     if final_score >= 80:
# #         rating = "Excellent"
# #     elif final_score >= 60:
# #         rating = "Good"
# #     elif final_score >= 40:
# #         rating = "Average"
# #     else:
# #         rating = "Poor"

# #     return {
# #         "final_score": final_score,
# #         "rating": rating,
# #         "breakdown": {
# #             "productivity_score": productivity_score,
# #             "action_score": action_score,
# #             "decision_score": decision_score,
# #             "conversation_score": conversation_score,
# #             "balance_score": balance_score
# #         }
# #     }