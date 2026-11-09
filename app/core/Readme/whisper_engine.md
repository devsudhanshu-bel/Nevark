# Whisper Speech-to-Text Engine

## 1. Overview

The `whisper_engine.py` module provides speech-to-text (STT) functionality for Nevark AI using Faster-Whisper.

It loads the Whisper `small` model and uses it to convert audio files into text transcripts.

The module exposes one primary function:

- `transcribe_audio()` – Accepts an audio file path, performs speech recognition, combines the recognized segments into a single text string, and returns the transcript.

The model is configured to run locally on the CPU using INT8 computation.

## 2. Dependencies

```python
from faster_whisper import WhisperModel
```

The module uses:

| Dependency | Purpose |
|---|---|
| `faster-whisper` | Provides optimized Whisper-based speech recognition |
| `WhisperModel` | Loads the selected speech-recognition model and performs transcription |

No external speech-to-text API is called directly by this module.

## 3. Whisper Model Initialization

```python
print("🔄 Loading Whisper Model...")

model = WhisperModel(
    "small",
    device="cpu",
    compute_type="int8"
)

print("✅ Whisper Model Loaded")
```

The Whisper model is initialized when the module is imported.

### Model configuration

| Parameter | Value | Purpose |
|---|---|---|
| Model size | `small` | Selects the Whisper small model |
| Device | `cpu` | Runs inference on the CPU |
| Compute type | `int8` | Uses 8-bit integer computation |

### Model loading process

1. A loading message is printed.
2. `WhisperModel` initializes the `small` model.
3. The model is configured for CPU execution.
4. INT8 computation is selected.
5. A confirmation message is printed after successful initialization.

The model instance is stored in the module-level variable `model` and reused by subsequent calls to `transcribe_audio()`.

This avoids explicitly loading a new model for every transcription request.

**Important:** Because initialization occurs at module level, a model-loading failure can prevent the module from importing successfully.

## 4. Core Function: `transcribe_audio()`

```python
def transcribe_audio(audio_path: str):
```

The `transcribe_audio()` function accepts the path of an audio file and converts its spoken content into text.

### Input parameter

| Parameter | Type | Description |
|---|---|---|
| `audio_path` | `str` | Path to the audio file that needs to be transcribed |

### Return values

| Return value | Meaning |
|---|---|
| `str` | Successfully generated transcript |
| `""` | Transcription failed due to a caught exception |

## 5. Transcription Process

### Step 1: Submit audio for transcription

```python
segments, info = model.transcribe(
    audio_path,
    beam_size=1,
    vad_filter=True,
    language="en"
)
```

The audio file is passed to the loaded Whisper model through `model.transcribe()`.

The function returns two values:

- `segments`: An iterable containing the recognized speech segments.
- `info`: Transcription metadata returned by Faster-Whisper.

### Transcription parameters

| Parameter | Value | Purpose |
|---|---|---|
| `audio_path` | Supplied file path | Identifies the audio input |
| `beam_size` | `1` | Uses a beam-search size of one |
| `vad_filter` | `True` | Enables voice activity detection filtering |
| `language` | `"en"` | Specifies English as the transcription language |

### Beam size

```python
beam_size=1
```

Controls the beam-search size used during decoding.

The implementation uses a value of one.

### Voice Activity Detection

```python
vad_filter=True
```

Enables voice activity detection filtering.

This allows the transcription process to filter out portions identified as non-speech before transcription.

### Language configuration

```python
language="en"
```

Specifies English as the language for transcription.

The implementation does not automatically detect and select other languages through this parameter.

## 6. Combining Transcription Segments

```python
text = " ".join(
    [segment.text for segment in segments]
).strip()
```

Faster-Whisper returns recognized speech as multiple segments.

The function extracts the `.text` value from each segment and combines the results into one string.

The operations are:

1. Iterate through the returned segments.
2. Extract the text from each segment.
3. Collect the extracted text into a list.
4. Join the segments using spaces.
5. Remove leading and trailing whitespace using `.strip()`.

For example, if the model returns:

```text
Segment 1: Hello
Segment 2: Nevark
Segment 3: How are you?
```

The combined transcript becomes:

```text
Hello Nevark How are you?
```

The example is illustrative; actual segment boundaries and transcription results depend on the audio input.

## 7. Returning the Transcript

```python
return text
```

After combining the recognized segments, the function returns the final transcript as a Python string.

The returned text can then be passed to other backend components for further processing.

The `info` metadata returned by `model.transcribe()` is not used or returned by this implementation.

## 8. Error Handling

```python
except Exception as e:

    print("❌ Whisper ERROR:", e)

    return ""
```

The transcription operation is wrapped in a `try-except` block.

If an exception occurs during transcription or segment processing:

1. The exception is caught.
2. An error message is printed.
3. An empty string is returned.

This allows the calling component to receive a string result even when transcription fails.

The module does not currently distinguish between different transcription failure types.

## 9. Complete Execution Flow

The speech-to-text pipeline follows this sequence:

1. Another backend component imports `transcribe_audio()`.
2. The module initializes the Faster-Whisper `small` model if it has not already been initialized.
3. The caller supplies an audio file path.
4. The audio is passed to `model.transcribe()`.
5. Transcription runs using CPU execution and INT8 computation.
6. Voice activity detection filtering is enabled.
7. Recognized speech segments are returned.
8. Segment text is extracted and combined.
9. Leading and trailing whitespace is removed.
10. The final transcript is returned.

If an exception occurs during transcription, the function logs the error to the terminal and returns an empty string.

## 10. Integration with the Speech API

The module can be used by the speech route located at:

`app/api/routes/speech.py`

That route imports:

```python
from app.core.whisper_engine import transcribe_audio
```

The speech endpoint reads an uploaded audio file, writes its contents to a temporary file, and passes the temporary file path to `transcribe_audio()`.

The transcription result is then returned by the route in its response.

The integration flow is:

1. Client uploads an audio file.
2. Speech API receives the upload.
3. Uploaded bytes are written to a temporary file.
4. The temporary file path is passed to `transcribe_audio()`.
5. Faster-Whisper generates the transcript.
6. The speech route returns the resulting text.

**Important:** The speech route assigns a `.wav` suffix to its temporary file, but the route does not convert the uploaded audio into WAV format. The actual audio bytes are written unchanged.

## 11. Current Implementation Scope

The module currently provides:

- Faster-Whisper integration.
- Local Whisper model initialization.
- Small-model configuration.
- CPU-based inference.
- INT8 computation.
- English-language transcription configuration.
- Voice activity detection filtering.
- Segment-based transcript extraction.
- Text concatenation.
- Whitespace cleanup.
- Basic exception handling.
- Empty-string fallback on transcription errors.

The module does not currently implement:

- GPU-based inference.
- Automatic language selection.
- Multilingual configuration through the supplied function.
- Speaker identification.
- Speaker diarization.
- Translation into another language.
- Timestamp formatting in the returned transcript.
- Confidence-score extraction.
- Streaming transcription.
- Audio-file conversion.
- Custom model selection per request.

## 12. Important Implementation Considerations

### 12.1 Model loading overhead

The model is loaded during module import rather than inside `transcribe_audio()`.

This avoids explicitly reloading it for every transcription request, but model initialization contributes to application startup time.

### 12.2 CPU execution

The model is configured with `device="cpu"`.

Therefore, this implementation does not use the laptop or server GPU for inference.

### 12.3 English-only configuration

The transcription request explicitly specifies `language="en"`.

The function is therefore configured for English transcription rather than dynamically selecting the input language.

### 12.4 Synchronous transcription

The function is synchronous.

If it is called directly from an asynchronous API endpoint, the transcription operation can occupy the executing thread while inference runs.

### 12.5 Error visibility

Transcription exceptions are printed to the terminal, and the caller receives an empty string.

The function does not return structured error details or use the application's shared logger.

## 13. Summary

The `whisper_engine.py` module provides the speech-to-text functionality for Nevark AI through Faster-Whisper.

It loads the Whisper `small` model with CPU-based INT8 computation and uses English transcription with voice activity detection filtering.

The `transcribe_audio()` function accepts an audio file path, extracts recognized speech segments, combines them into a single transcript, and returns the resulting text.

Together with `tts_engine.py`, it provides the speech-processing foundation for Nevark's voice interaction capabilities:

- `whisper_engine.py` converts speech into text.
- `tts_engine.py` converts text into speech.

These modules provide the STT and TTS capabilities independently, allowing other backend components to coordinate voice-based interactions.