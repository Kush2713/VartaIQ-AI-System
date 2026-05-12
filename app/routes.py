# from fastapi import APIRouter
# from app.schemas import TranscriptRequest, AnalysisResponse
# from app.services.pipeline import run_pipeline

# router = APIRouter()

# @router.post("/analyze", response_model=AnalysisResponse)
# def analyze_meeting(request: TranscriptRequest):
#     data = [item.dict() for item in request.transcript]
#     return run_pipeline(data)

from fastapi import APIRouter
from sqlalchemy.orm import Session

from app.schemas import TranscriptRequest
from app.services.pipeline import run_pipeline

from app.db.database import SessionLocal
from app.db.models import MeetingAnalysis

router = APIRouter()


@router.post("/analyze")
def analyze_meeting(request: TranscriptRequest):

    data = [item.dict() for item in request.transcript]

    result = run_pipeline(data)

    db: Session = SessionLocal()

    meeting = MeetingAnalysis(
        summary=result["summary"],
        action_items=result["action_items"],
        decisions=result["decisions"],
        useless_talk=result["useless_talk"],
        speaker_analysis=result["speaker_analysis"],
        score=result["score"],
        transcript=data
    )

    db.add(meeting)

    db.commit()

    db.refresh(meeting)

    db.close()

    return {
        "meeting_id": meeting.id,
        "analysis": result
    }
    
@router.get("/meetings/{meeting_id}")
def get_meeting(meeting_id: int):

    db: Session = SessionLocal()

    meeting = db.query(MeetingAnalysis).filter(
        MeetingAnalysis.id == meeting_id
    ).first()

    db.close()

    if not meeting:
        return {"error": "Meeting not found"}

    return meeting

@router.get("/meetings")
def get_all_meetings():

    db: Session = SessionLocal()

    meetings = db.query(MeetingAnalysis).all()

    db.close()

    return meetings