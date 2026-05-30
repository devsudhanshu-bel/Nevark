
from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import File

from app.core.whisper_engine import transcribe_audio

import tempfile

router = APIRouter(
    prefix="/speech",
    tags=["Speech"]
)


@router.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".wav"
    ) as temp_audio:

        content = await file.read()

        temp_audio.write(content)

        temp_path = temp_audio.name

    text = transcribe_audio(temp_path)

    return {
        "success": True,
        "text": text
    }

