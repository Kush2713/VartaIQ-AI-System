import re


# =====================================
# CLEAN TEXT
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

    # Remove duplicate punctuation
    text = re.sub(
        r"([.,!?])\1+",
        r"\1",
        text
    )

    # Remove quote wrapping
    text = text.replace(
        "\"",
        ""
    )

    text = text.strip()

    return text


# =====================================
# SHORTEN TASK
# =====================================

def shorten_task(task):

    task = clean_text(task)

    task = task.replace(
        "we need to",
        ""
    )

    task = task.replace(
        "i will",
        ""
    )

    task = task.replace(
        "we should",
        ""
    )

    task = task.replace(
        "please",
        ""
    )

    task = task.strip()

    # Capitalize properly
    if len(task) > 1:

        task = (
            task[0].upper()
            + task[1:]
        )

    return task


# =====================================
# GENERATE ACTION FOLLOWUPS
# =====================================

def generate_action_followups(
    action_items
):

    followups = []

    for action in action_items:

        assignee = action.get(
            "assignee",
            "Team"
        )

        task = shorten_task(

            action.get(
                "task",
                ""
            )
        )

        deadline = clean_text(

            action.get(
                "deadline",
                ""
            )
        )

        priority = clean_text(

            action.get(
                "priority",
                "Normal"
            )
        )

        if not task:
            continue

        # -----------------------------
        # Deadline Handling
        # -----------------------------

        if deadline:

            sentence = (

                f"{assignee} should complete "
                f"{task} by {deadline}."
            )

        else:

            sentence = (

                f"{assignee} should complete "
                f"{task}."
            )

        # -----------------------------
        # Priority Enhancement
        # -----------------------------

        if priority.lower() == "high":

            sentence += (
                " This task is high priority."
            )

        followups.append(
            clean_text(sentence)
        )

    return followups


# =====================================
# GENERATE DECISION FOLLOWUPS
# =====================================

def generate_decision_followups(
    decisions
):

    followups = []

    for decision in decisions:

        decision_text = clean_text(

            decision.get(
                "decision",
                ""
            )
        )

        if not decision_text:
            continue

        sentence = (

            "Ensure execution alignment for "
            f"decision: {decision_text}."
        )

        followups.append(
            clean_text(sentence)
        )

    return followups


# =====================================
# GENERATE RISK FOLLOWUPS
# =====================================

def generate_risk_followups(
    sentiment_analysis
):

    followups = []

    risks = sentiment_analysis.get(
        "risks",
        []
    )

    for risk in risks:

        text = clean_text(
            risk.get(
                "text",
                ""
            )
        )

        if not text:
            continue

        sentence = (

            "Monitor operational risk: "
            f"{text}."
        )

        followups.append(
            clean_text(sentence)
        )

    return followups


# =====================================
# GENERATE SCORE FOLLOWUP
# =====================================

def generate_score_followup(
    meeting_score
):

    if meeting_score >= 80:

        return (
            "Meeting execution and collaboration "
            "were highly effective."
        )

    if meeting_score >= 60:

        return (
            "Meeting productivity was good, "
            "but execution clarity can improve."
        )

    if meeting_score >= 40:

        return (
            "Meeting effectiveness was moderate. "
            "Reduce distractions and improve "
            "decision clarity."
        )

    return (

        "Meeting productivity was low. "
        "Improve collaboration, reduce "
        "off-topic discussion, and define "
        "clear action ownership."
    )


# =====================================
# DEDUPLICATION
# =====================================

def deduplicate_followups(
    followups
):

    unique = []

    seen = set()

    for item in followups:

        normalized = (
            item.lower().strip()
        )

        if normalized in seen:
            continue

        seen.add(normalized)

        unique.append(item)

    return unique


# =====================================
# MAIN GENERATOR
# =====================================

def generate_followups(

    summary,

    action_items,

    decisions,

    sentiment_analysis,

    meeting_score
):

    followups = []

    # ---------------------------------
    # Action Items
    # ---------------------------------

    followups.extend(

        generate_action_followups(
            action_items
        )
    )

    # ---------------------------------
    # Decisions
    # ---------------------------------

    followups.extend(

        generate_decision_followups(
            decisions
        )
    )

    # ---------------------------------
    # Risks
    # ---------------------------------

    followups.extend(

        generate_risk_followups(
            sentiment_analysis
        )
    )

    # ---------------------------------
    # Overall Meeting Recommendation
    # ---------------------------------

    followups.append(

        generate_score_followup(
            meeting_score
        )
    )

    # ---------------------------------
    # Final Deduplication
    # ---------------------------------

    followups = (
        deduplicate_followups(
            followups
        )
    )

    return followups