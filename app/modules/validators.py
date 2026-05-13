from app.config.ai_config import (

    ACTION_CONFIDENCE_THRESHOLD,

    DECISION_CONFIDENCE_THRESHOLD,

    TOPIC_RELEVANCE_THRESHOLD,

    USELESS_VALIDATION_THRESHOLD
)


# =====================================
# VALIDATE ACTION ITEMS
# =====================================

def validate_action_items(actions):

    validated = []

    for action in actions:

        confidence = action.get(
            "confidence",
            0
        )

        # Remove weak actions
        if confidence < (
            ACTION_CONFIDENCE_THRESHOLD
        ):
            continue

        task = action.get(
            "task",
            ""
        ).strip()

        # Remove extremely short tasks
        if len(task.split()) < 3:
            continue

        validated.append(action)

    return validated


# =====================================
# VALIDATE DECISIONS
# =====================================

def validate_decisions(decisions):

    validated = []

    for decision in decisions:

        confidence = decision.get(
            "decision_confidence",
            0
        )

        if confidence < (
            DECISION_CONFIDENCE_THRESHOLD
        ):
            continue

        decision_text = decision.get(
            "decision",
            ""
        ).strip()

        # Very short decisions are weak
        if len(
            decision_text.split()
        ) < 4:
            continue

        validated.append(decision)

    return validated


# =====================================
# VALIDATE TOPICS
# =====================================

def validate_topics(topics):

    validated = []

    GENERIC_TOPICS = {

        "issue",
        "problem",
        "meeting",
        "discussion",
        "update",
        "task",
        "conversation",
        "work"
    }

    for topic in topics:

        score = topic.get(
            "relevance_score",
            0
        )

        if score < (
            TOPIC_RELEVANCE_THRESHOLD
        ):
            continue

        topic_text = topic.get(
            "topic",
            ""
        ).strip().lower()

        # Remove empty topic
        if not topic_text:
            continue

        # Remove generic weak topics
        if topic_text in GENERIC_TOPICS:
            continue

        # Remove extremely short topics
        if len(topic_text.split()) == 1:

            if len(topic_text) <= 3:
                continue

        validated.append(topic)

    return validated


# =====================================
# VALIDATE USELESS TALK
# =====================================

def validate_useless_talk(
    useless_talk
):

    validated_segments = []

    segments = useless_talk.get(
        "useless_segments",
        []
    )

    for segment in segments:

        relevance = segment.get(
            "relevance_score",
            0
        )

        text = segment.get(
            "text",
            ""
        ).strip()

        # Ignore empty
        if not text:
            continue

        # Ignore borderline relevance
        if relevance > (
            USELESS_VALIDATION_THRESHOLD
        ):
            continue

        validated_segments.append(
            segment
        )

    return {

        "useless_segments":
            validated_segments
    }