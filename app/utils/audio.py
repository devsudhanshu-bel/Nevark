import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav

SAMPLE_RATE = 16000


def record_audio(

    duration: int = 5,

    output_file: str = "temp.wav"
):

    print("🎤 Recording Audio...")

    audio = sd.rec(

        int(duration * SAMPLE_RATE),

        samplerate=SAMPLE_RATE,

        channels=1,

        dtype="float32"
    )

    sd.wait()

    wav.write(

        output_file,

        SAMPLE_RATE,

        (audio * 32767).astype(np.int16)
    )

    print("✅ Recording Complete")

    return output_file

