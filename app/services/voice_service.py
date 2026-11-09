import tempfile
import os

from fastapi.responses import FileResponse

from app.core.whisper_engine import (
    transcribe_audio
)

from app.services.chat_service import (
    process_chat
)

from app.core.tts_engine import (
    generate_audio
)


async def process_voice(audio_file):

    temp_path = None

    try:

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".wav"
        ) as temp:

            content = await audio_file.read()

            temp.write(content)

            temp_path = temp.name

        transcript = transcribe_audio(
            temp_path
        )

        response = await process_chat(
            transcript
        )

        audio_path = generate_audio(
            response
        )

        return FileResponse(
            path=audio_path,
            media_type="audio/mpeg",
            filename="response.mp3"
        )

    except Exception as e:

        print(
            "❌ VOICE SERVICE ERROR:",
            e
        )

        return {
            "success": False,
            "error": str(e)
        }

    finally:

        if (
            temp_path and
            os.path.exists(temp_path)
        ):
            os.remove(temp_path)