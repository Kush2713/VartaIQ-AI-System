from fastapi import FastAPI
from app.routes import router

from app.db.database import engine
from app.db.models import Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Meeting Analyzer")

app.include_router(router)