from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime


# =====================================
# INPUT SCHEMAS
# =====================================

class TranscriptItem(BaseModel):
    speaker: str
    text: str


class TranscriptRequest(BaseModel):
    transcript: List[TranscriptItem]


# =====================================
# ACTION ITEMS
# =====================================

class ActionItem(BaseModel):

    speaker: str

    assignee: str

    task: str

    deadline: Optional[str] = None

    confidence: float


# =====================================
# DECISIONS
# =====================================

class DecisionItem(BaseModel):

    speaker: str

    decision: str

    decision_type: Optional[str] = None

    category: Optional[str] = None

    consensus: Optional[bool] = None

    confidence: Optional[float] = None


# =====================================
# USELESS TALK
# =====================================

class UselessTalkItem(BaseModel):

    speaker: str

    text: str

    relevance_score: float

    reason: str


# =====================================
# SPEAKER ANALYSIS
# =====================================

class SpeakerStats(BaseModel):

    word_count: int

    participation_percentage: float

    relevance_ratio: float

    productivity_ratio: float

    effectiveness_score: float


# =====================================
# SCORING
# =====================================

class ScoreBreakdown(BaseModel):

    productivity_score: float

    action_score: float

    decision_score: float

    conversation_score: float

    balance_score: float


class ScoreResponse(BaseModel):

    final_score: float

    rating: str

    breakdown: ScoreBreakdown


# =====================================
# FINAL ANALYSIS RESPONSE
# =====================================

class AnalysisResponse(BaseModel):

    summary: str

    topics: list

    action_items: list

    decisions: list

    useless_talk: dict

    speaker_analysis: dict

    sentiment_analysis: dict

    score: dict

    ai_insights: list

    followups: list


# =====================================
# DATABASE RESPONSE SCHEMAS
# =====================================

class SentimentResponse(BaseModel):

    overall_sentiment: str

    overall_score: float

    risk_count: int

    conflict_count: int

    conversation_sentiments: list


class MeetingResponse(BaseModel):

    id: int

    meeting_title: str

    participant_count: int

    transcript_length: int

    summary: str

    topics: list

    transcript: list

    action_items: list

    decisions: list

    useless_talk: dict

    speaker_analysis: dict

    sentiment_analysis: dict

    score: dict

    ai_insights: list

    followups: list

    created_at: datetime

    updated_at: datetime

    class Config:
        from_attributes = True
