from sqlalchemy import Column, Integer, String, JSON, DateTime
from datetime import datetime

from app.db.database import Base


class MeetingAnalysis(Base):

    __tablename__ = "meeting_analysis"

    id = Column(Integer, primary_key=True, index=True)

    summary = Column(String)

    action_items = Column(JSON)

    decisions = Column(JSON)

    useless_talk = Column(JSON)

    speaker_analysis = Column(JSON)

    score = Column(JSON)

    transcript = Column(JSON)

    created_at = Column(DateTime, default=datetime.utcnow)