from fastapi import APIRouter
from app.schemas import TranscriptRequest, AnalysisResponse
from app.services.pipeline import run_pipeline

router = APIRouter()

@router.post("/analyze", response_model=AnalysisResponse)
def analyze_meeting(request: TranscriptRequest):
    data = [item.dict() for item in request.transcript]
    return run_pipeline(data)