from pydantic import BaseModel
from typing import List, Dict

class TranscriptItem(BaseModel):
    speaker: str
    text: str

class TranscriptRequest(BaseModel):
    transcript: List[TranscriptItem]

class AnalysisResponse(BaseModel):
    summary: str
    action_items: List[Dict]
    decisions: List[Dict]
    useless_talk: List[Dict]
    speaker_analysis: Dict
    score: Dict