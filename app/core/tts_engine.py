
import os
import uuid
import time

from dotenv import load_dotenv

from elevenlabs.client import ElevenLabs
from elevenlabs import save

from playsound import playsound

load_dotenv()

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
VOICE_ID = os.getenv("VOICE_ID")
ELEVEN_MODEL = os.getenv("ELEVEN_MODEL")

client = ElevenLabs(
    api_key=ELEVENLABS_API_KEY
)


def speak(text: str):

    if not text:
        return

    try:

        audio = client.text_to_speech.convert(

            voice_id=VOICE_ID,

            model_id=ELEVEN_MODEL,

            text=text,

            output_format="mp3_44100_128"
        )

        filename = f"nevark_{uuid.uuid4().hex}.mp3"

        save(audio, filename)

        playsound(filename)

        time.sleep(0.3)

        if os.path.exists(filename):
            os.remove(filename)

    except Exception as e:

        print("❌ TTS ERROR:", e)

def generate_audio(text: str):

    if not text:
        return None

    try:

        audio = client.text_to_speech.convert(

            voice_id=VOICE_ID,

            model_id=ELEVEN_MODEL,

            text=text,

            output_format="mp3_44100_128"
        )

        os.makedirs(
            "generated_audio",
            exist_ok=True
        )

        filename = (
            f"generated_audio/"
            f"{uuid.uuid4().hex}.mp3"
        )

        save(audio, filename)

        return filename

    except Exception as e:

        print(
            "❌ AUDIO GENERATION ERROR:",
            e
        )

        return None