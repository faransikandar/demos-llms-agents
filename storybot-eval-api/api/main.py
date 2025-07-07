from fastapi import FastAPI
from api.router import router
from dotenv import load_dotenv

load_dotenv()  # Load from .env

app = FastAPI(
    title="StoryBot Health - Conversational Evaluation API",
    description="Evaluates user-StoryBot conversations and provides belief insights, metrics, and recommendations.",
    version="0.1.0"
)

app.include_router(router)
