
from faster_whisper import WhisperModel

print("🔄 Loading Whisper Model...")

model = WhisperModel(
    "small",
    device="cpu",
    compute_type="int8"
)

print("✅ Whisper Model Loaded")


def transcribe_audio(audio_path: str):

    try:

        segments, info = model.transcribe(
            audio_path,
            beam_size=1,
            vad_filter=True,
            language="en"
        )

        text = " ".join(
            [segment.text for segment in segments]
        ).strip()

        return text

    except Exception as e:

        print("❌ Whisper ERROR:", e)

        return ""
