from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import File

from app.services.voice_service import (
    process_voice
)

router = APIRouter(
    prefix="/voice",
    tags=["Voice"]
)

@router.post("/")
async def voice_chat(
    audio: UploadFile = File(...)
):

    return await process_voice(
        audio
    )