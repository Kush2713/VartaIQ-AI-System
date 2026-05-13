from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from app.schemas import (

    TranscriptRequest,

    AnalysisResponse,

    MeetingResponse
)

from app.services.pipeline import (
    run_pipeline
)

from app.db.database import (
    SessionLocal
)

from app.db.models import (
    MeetingAnalysis
)

router = APIRouter()


# =====================================
# DATABASE DEPENDENCY
# =====================================

def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


# =====================================
# ANALYZE MEETING
# =====================================

@router.post(
    "/analyze",
    response_model=dict
)
def analyze_meeting(

    request: TranscriptRequest,

    db: Session = Depends(get_db)
):

    # ---------------------------------
    # Convert Pydantic -> dict
    # ---------------------------------

    data = [

        item.dict()

        for item in request.transcript
    ]

    # ---------------------------------
    # Run AI Pipeline
    # ---------------------------------

    result = run_pipeline(data)

    # ---------------------------------
    # Save Meeting Analysis
    # ---------------------------------

    meeting = MeetingAnalysis(

        # ---------------------------------
        # Meeting Metadata
        # ---------------------------------

        meeting_title=(

            f"Meeting with "

            f"{len(set([x['speaker'] for x in data]))} participants"
        ),

        participant_count=len(
            set([x["speaker"] for x in data])
        ),

        transcript_length=len(data),

        # ---------------------------------
        # AI Outputs
        # ---------------------------------

        summary=result["summary"],

        topics=result["topics"],

        transcript=data,

        action_items=result[
            "action_items"
        ],

        decisions=result[
            "decisions"
        ],

        useless_talk=result[
            "useless_talk"
        ],

        speaker_analysis=result[
            "speaker_analysis"
        ],
        
        sentiment_analysis=result[
            "sentiment_analysis"
        ],

        score=result["score"],
        
        followups=result[
            "followups"
        ],

        ai_insights=result[
            "ai_insights"
        ]
    )

    db.add(meeting)

    db.commit()

    db.refresh(meeting)

    # ---------------------------------
    # Final Response
    # ---------------------------------

    return {

        "meeting_id":
            meeting.id,

        "analysis":
            result
    }


# =====================================
# GET SINGLE MEETING
# =====================================

@router.get(

    "/meetings/{meeting_id}",

    response_model=MeetingResponse
)
def get_meeting(

    meeting_id: int,

    db: Session = Depends(get_db)
):

    meeting = db.query(
        MeetingAnalysis
    ).filter(
        MeetingAnalysis.id == meeting_id
    ).first()

    if not meeting:

        raise HTTPException(

            status_code=404,

            detail="Meeting not found"
        )

    return meeting


# =====================================
# GET ALL MEETINGS
# =====================================

@router.get(

    "/meetings",

    response_model=list[MeetingResponse]
)
def get_all_meetings(

    db: Session = Depends(get_db)
):

    meetings = db.query(
        MeetingAnalysis
    ).all()

    return meetings













































# # from fastapi import APIRouter
# # from app.schemas import TranscriptRequest, AnalysisResponse
# # from app.services.pipeline import run_pipeline

# # router = APIRouter()

# # @router.post("/analyze", response_model=AnalysisResponse)
# # def analyze_meeting(request: TranscriptRequest):
# #     data = [item.dict() for item in request.transcript]
# #     return run_pipeline(data)

# from fastapi import APIRouter
# from sqlalchemy.orm import Session

# from app.schemas import TranscriptRequest
# from app.services.pipeline import run_pipeline

# from app.db.database import SessionLocal
# from app.db.models import MeetingAnalysis

# router = APIRouter()


# @router.post("/analyze")
# def analyze_meeting(request: TranscriptRequest):

#     data = [item.dict() for item in request.transcript]

#     result = run_pipeline(data)

#     db: Session = SessionLocal()

#     meeting = MeetingAnalysis(
#         summary=result["summary"],
#         action_items=result["action_items"],
#         decisions=result["decisions"],
#         useless_talk=result["useless_talk"],
#         speaker_analysis=result["speaker_analysis"],
#         score=result["score"],
#         transcript=data
#     )

#     db.add(meeting)

#     db.commit()

#     db.refresh(meeting)

#     db.close()

#     return {
#         "meeting_id": meeting.id,
#         "analysis": result
#     }
    
# @router.get("/meetings/{meeting_id}")
# def get_meeting(meeting_id: int):

#     db: Session = SessionLocal()

#     meeting = db.query(MeetingAnalysis).filter(
#         MeetingAnalysis.id == meeting_id
#     ).first()

#     db.close()

#     if not meeting:
#         return {"error": "Meeting not found"}

#     return meeting

# @router.get("/meetings")
# def get_all_meetings():

#     db: Session = SessionLocal()

#     meetings = db.query(MeetingAnalysis).all()

#     db.close()

#     return meetings