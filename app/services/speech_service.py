from app.core.whisper_engine import transcribe_audio
from app.core.tts_engine import speak


async def process_speech(audio_path: str):

    try:

        text = transcribe_audio(audio_path)

        return {
            "success": True,
            "text": text
        }

    except Exception as e:

        print("❌ SPEECH SERVICE ERROR:", e)

        return {
            "success": False,
            "error": str(e)
        }


async def speak_text(text: str):

    try:

        speak(text)

        return {
            "success": True
        }

    except Exception as e:

        print("❌ TTS SERVICE ERROR:", e)

        return {
            "success": False,
            "error": str(e)
        }
