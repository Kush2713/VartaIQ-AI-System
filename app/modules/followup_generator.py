import re

from app.modules.deduplication import (
    semantic_deduplicate
)

# =====================================
# FILLER PREFIXES
# =====================================

FILLER_PREFIXES = {

    "i will",
    "we will",
    "we should",
    "we need to",
    "please",
    "today",
    "tomorrow",
    "let's",
    "kindly"
}

# =====================================
# IMPERATIVE VERB FIXES
# =====================================

VERB_NORMALIZATION = {

    "finalizing": "Finalize",
    "deploying": "Deploy",
    "implementing": "Implement",
    "testing": "Test",
    "reviewing": "Review",
    "creating": "Create",
    "preparing": "Prepare",
    "updating": "Update",
    "optimizing": "Optimize",
    "fixing": "Fix"
}

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

    # Remove repeated punctuation
    text = re.sub(
        r"([.,!?])\1+",
        r"\1",
        text
    )

    # Remove quotes
    text = text.replace(
        "\"",
        ""
    )

    text = text.strip()

    return text

# =====================================
# REMOVE FILLER PREFIXES
# =====================================

def remove_filler_prefixes(
    text
):

    lowered = text.lower()

    for prefix in (
        FILLER_PREFIXES
    ):

        if lowered.startswith(prefix):

            text = text[
                len(prefix):
            ].strip()

            lowered = text.lower()

    return text

# =====================================
# REMOVE DEADLINE PHRASES
# =====================================

def remove_deadline_phrases(
    text
):

    patterns = [

        r"\bbefore\s+\w+",

        r"\bby\s+\w+",

        r"\btoday\b",

        r"\btomorrow\b"
    ]

    for pattern in patterns:

        text = re.sub(

            pattern,

            "",

            text,

            flags=re.IGNORECASE
        )

    return text.strip()

# =====================================
# NORMALIZE TASK
# =====================================

def normalize_task(task):

    task = clean_text(task)

    # ---------------------------------
    # Strip "Final decision:" prefix
    # ---------------------------------

    if task.lower().startswith("final decision:"):
        task = task[len("final decision:"):].strip()

    # ---------------------------------
    # Remove filler openings
    # ---------------------------------

    task = remove_filler_prefixes(task)

    # ---------------------------------
    # Remove inline deadline phrases
    # so they don't duplicate the
    # deadline appended at the end
    # ---------------------------------

    task = remove_deadline_phrases(task)

    # ---------------------------------
    # Normalize verbs
    # ---------------------------------

    words = task.split()

    if words:

        first_word = words[0].lower()

        if first_word in VERB_NORMALIZATION:

            words[0] = VERB_NORMALIZATION[first_word]

        else:

            words[0] = words[0].capitalize()

    task = " ".join(words)

    # ---------------------------------
    # Final cleanup
    # ---------------------------------

    task = re.sub(r"\s+", " ", task)

    task = task.strip(" .,")

    return task

# =====================================
# FORMAT DEADLINE
# =====================================

def format_deadline(
    deadline
):

    if not deadline:
        return ""

    deadline = clean_text(deadline)

    # Strip leading "before" / "by" so we
    # don't produce "before Before friday"
    # when we append "before {deadline}"
    deadline_lower = deadline.lower()

    for prefix in ("before ", "by "):

        if deadline_lower.startswith(prefix):

            deadline = deadline[len(prefix):].strip()

            break

    # Capitalise first letter
    if deadline:
        deadline = deadline[0].upper() + deadline[1:]

    return deadline

# =====================================
# ACTION FOLLOWUPS
# =====================================

def generate_action_followups(
    action_items
):

    followups = []

    for action in action_items:

        assignee = clean_text(

            action.get(
                "assignee",
                "Team"
            )
        )

        task = normalize_task(

            action.get(
                "task",
                ""
            )
        )

        deadline = format_deadline(

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

        # ---------------------------------
        # Skip weak tasks
        # ---------------------------------

        if len(task.split()) < 3:
            continue

        # ---------------------------------
        # Build sentence
        # ---------------------------------

        # Ensure task doesn't start with
        # a pronoun/filler that makes the
        # "{assignee} should {task}" awkward
        task_lower = task.lower()

        awkward_starts = (
            "we need to",
            "we should",
            "we will",
            "i will",
            "i should",
            "today we",
            "today i",
        )

        for start in awkward_starts:

            if task_lower.startswith(start):

                task = task[len(start):].strip()

                if task:
                    task = (
                        task[0].upper()
                        + task[1:]
                    )

                break

        sentence = (
            f"{assignee} should "
            f"{task}"
        )

        if deadline:

            sentence += (
                f" before {deadline}"
            )

        sentence += "."

        # ---------------------------------
        # Priority enhancement
        # ---------------------------------

        if priority.lower() == "high":

            sentence += (
                " This is a high-priority task."
            )

        followups.append({

            "text":
                clean_text(sentence)
        })

    return followups

# =====================================
# DECISION FOLLOWUPS
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

        if len(
            decision_text.split()
        ) < 4:
            continue

        sentence = (

            "Ensure alignment and execution "
            f"for decision: {decision_text}."
        )

        followups.append({

            "text":
                clean_text(sentence)
        })

    return followups

# =====================================
# RISK FOLLOWUPS
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

        if len(text.split()) < 4:
            continue

        sentence = (

            "Monitor operational risk: "
            f"{text}."
        )

        followups.append({

            "text":
                clean_text(sentence)
        })

    return followups

# =====================================
# MEETING QUALITY FOLLOWUP
# =====================================

def generate_meeting_quality_followup(
    meeting_score
):

    if meeting_score >= 75:

        return {

            "text":
                (
                    "Meeting execution and "
                    "collaboration were highly effective."
                )
        }

    if meeting_score >= 58:

        return {

            "text":
                (
                    "Meeting productivity was good, "
                    "with clear technical discussion "
                    "and execution planning."
                )
        }

    if meeting_score >= 40:

        return {

            "text":
                (
                    "Meeting was reasonably effective. "
                    "Strengthening ownership clarity "
                    "will improve future outcomes."
                )
        }

    return {

        "text":
            (
                "Meeting productivity was low. "
                "Improve collaboration, task clarity, "
                "and execution focus."
            )
    }

# =====================================
# FINAL CLEANUP
# =====================================

def finalize_followups(
    followups
):

    followups = semantic_deduplicate(

        followups,

        "text"
    )

    cleaned = []

    seen = set()

    for item in followups:

        text = clean_text(
            item["text"]
        )

        normalized = (
            text.lower().strip()
        )

        if normalized in seen:
            continue

        seen.add(normalized)

        cleaned.append(text)

    return cleaned

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
    # Action items
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
    # Meeting quality
    # ---------------------------------

    followups.append(

        generate_meeting_quality_followup(
            meeting_score
        )
    )

    # ---------------------------------
    # Final cleanup
    # ---------------------------------

    return finalize_followups(
        followups
    )