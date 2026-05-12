# from pydantic import BaseModel
# from typing import List, Dict

# class TranscriptItem(BaseModel):
#     speaker: str
#     text: str

# class TranscriptRequest(BaseModel):
#     transcript: List[TranscriptItem]

# class AnalysisResponse(BaseModel):
#     summary: str
#     action_items: List[Dict]
#     decisions: List[Dict]
#     useless_talk: List[Dict]
#     speaker_analysis: Dict
#     score: Dict

from pydantic import BaseModel
from typing import List, Dict, Any


# =========================
# INPUT SCHEMAS
# =========================

class TranscriptItem(BaseModel):
    speaker: str
    text: str


class TranscriptRequest(BaseModel):
    transcript: List[TranscriptItem]


# =========================
# OUTPUT SCHEMAS
# =========================

class ActionItem(BaseModel):
    speaker: str
    task: str


class DecisionItem(BaseModel):
    speaker: str
    decision: str


class UselessTalkItem(BaseModel):
    speaker: str
    text: str


class SpeakerStats(BaseModel):
    word_count: int
    percentage: float


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


class AnalysisResponse(BaseModel):

    summary: str

    action_items: List[ActionItem]

    decisions: List[DecisionItem]

    useless_talk: List[UselessTalkItem]

    speaker_analysis: Dict[str, SpeakerStats]

    score: ScoreResponse