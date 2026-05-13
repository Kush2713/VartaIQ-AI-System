from app.modules.topic_detection import (
    detect_meeting_topics
)

from app.modules.context_engine import (
    generate_meeting_embedding
)


# =====================================
# BUILD SHARED AI CONTEXT
# =====================================

def build_ai_context(
    transcript
):
    """
    Generates shared semantic meeting context
    used across the entire AI pipeline.
    """

    # ---------------------------------
    # Detect meeting topics
    # ---------------------------------

    topic_data = detect_meeting_topics(
        transcript
    )

    # ---------------------------------
    # Generate semantic embedding
    # ---------------------------------

    meeting_embedding = (
        generate_meeting_embedding(
            transcript
        )
    )

    # ---------------------------------
    # Shared context object
    # ---------------------------------

    context = {

        "topics":
            topic_data.get(
                "topics",
                []
            ),

        "meeting_embedding":
            meeting_embedding
    }

    return context