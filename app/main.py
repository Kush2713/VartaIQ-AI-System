from fastapi import FastAPI
from app.routes import router

app = FastAPI(title="AI Meeting Analyzer")

app.include_router(router)