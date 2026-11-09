from fastapi import APIRouter

from app.api.routes.chat import router as chat_router
from app.api.routes.health import router as health_router
from app.api.routes.memory import router as memory_router
from app.api.routes.speech import router as speech_router
from app.api.routes.websocket import router as websocket_router
from app.api.routes.voice import router as voice_router

api_router = APIRouter()

api_router.include_router(chat_router)
api_router.include_router(health_router)
api_router.include_router(memory_router)
api_router.include_router(speech_router)
api_router.include_router(websocket_router)
api_router.include_router(voice_router)