import os

from dotenv import load_dotenv

load_dotenv()

# ============================================================
# APP
# ============================================================

APP_NAME = "Nevark AI Backend"

APP_VERSION = "1.0.0"

DEBUG = True

# ============================================================
# GROQ
# ============================================================

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

GROQ_MODEL = os.getenv(
    "GROQ_MODEL",
    "llama-3.3-70b-versatile"
)

# ============================================================
# ELEVENLABS
# ============================================================

ELEVENLABS_API_KEY = os.getenv(
    "ELEVENLABS_API_KEY"
)

VOICE_ID = os.getenv("VOICE_ID")

ELEVEN_MODEL = os.getenv(
    "ELEVEN_MODEL",
    "eleven_multilingual_v2"
)

# ============================================================
# AUDIO
# ============================================================

SAMPLE_RATE = int(
    os.getenv("SAMPLE_RATE", 16000)
)

RECORD_SECONDS = int(
    os.getenv("RECORD_SECONDS", 5)
)

# ============================================================
# DATABASE
# ============================================================

DATABASE_URL = "sqlite:///./nevark.db"