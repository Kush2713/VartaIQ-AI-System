from sqlalchemy import (

    Column,

    Integer,

    String,

    JSON,

    DateTime
)

from sqlalchemy.sql import (
    func
)

from app.db.database import Base


class MeetingAnalysis(Base):

    __tablename__ = "meeting_analysis"

    # =====================================
    # PRIMARY ID
    # =====================================

    id = Column(

        Integer,

        primary_key=True,

        index=True
    )

    # =====================================
    # MEETING METADATA
    # =====================================

    meeting_title = Column(
        String,
        default="Untitled Meeting"
    )

    participant_count = Column(
        Integer,
        default=0
    )

    transcript_length = Column(
        Integer,
        default=0
    )

    # =====================================
    # CORE AI OUTPUTS
    # =====================================

    summary = Column(String)

    topics = Column(JSON)

    transcript = Column(JSON)

    # =====================================
    # NLP / AI MODULE OUTPUTS
    # =====================================

    action_items = Column(JSON)

    decisions = Column(JSON)

    useless_talk = Column(JSON)

    speaker_analysis = Column(JSON)

    score = Column(JSON)

    ai_insights = Column(JSON)

    # =====================================
    # NEW ADVANCED AI FEATURES
    # =====================================

    sentiment_analysis = Column(JSON)

    conflicts = Column(JSON)

    risks = Column(JSON)

    followups = Column(JSON)

    # =====================================
    # TIMESTAMPS
    # =====================================

    created_at = Column(

        DateTime(timezone=True),

        server_default=func.now()
    )

    updated_at = Column(

        DateTime(timezone=True),

        server_default=func.now(),

        onupdate=func.now()
    )