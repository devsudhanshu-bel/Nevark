# Speech Service

## 1. Overview

The `speech_service.py` module provides the service layer for speech processing in Nevark AI.

It connects the speech-to-text (STT) and text-to-speech (TTS) engines and exposes two asynchronous functions:

- `process_speech()` – Accepts an audio file path, transcribes the audio using Faster-Whisper, and returns the recognized text.
- `speak_text()` – Accepts text, invokes the ElevenLabs-based speech engine, and returns an execution status.

The module acts as an intermediary between API routes and the underlying speech-processing engines.

## 2. Dependencies

```python
from app.core.whisper_engine import transcribe_audio
from app.core.tts_engine import speak
```

| Dependency | Responsibility |
|---|---|
| `transcribe_audio()` | Converts audio files into text using Faster-Whisper |
| `speak()` | Converts text into speech and plays the generated audio locally |

The module delegates actual speech recognition and speech generation to the core engine components.

## 3. Function: `process_speech()`

```python
async def process_speech(audio_path: str):
```

This function handles incoming audio transcription.

It accepts an audio file path, passes it to the Whisper engine, and returns the resulting transcript.

### Input parameter

| Parameter | Type | Description |
|---|---|---|
| `audio_path` | `str` | Path to the audio file that needs transcription |

### Step 1: Transcribe the audio

```python
text = transcribe_audio(audio_path)
```

The audio file path is passed to `transcribe_audio()` from:

`app/core/whisper_engine.py`

The Whisper engine:

1. Loads the configured Faster-Whisper model.
2. Processes the audio file.
3. Extracts recognized speech segments.
4. Combines the segments into a single text string.
5. Returns the transcript.

The resulting text is stored in the `text` variable.

### Step 2: Return the transcription result

```python
return {
    "success": True,
    "text": text
}
```

After the transcription function returns successfully, the service returns a dictionary containing:

| Field | Type | Description |
|---|---|---|
| `success` | `bool` | Indicates that the service operation completed without raising an exception |
| `text` | `str` | Transcribed text returned by the Whisper engine |

Example response:

```json
{
    "success": true,
    "text": "Hello Nevark, how are you?"
}
```

### Step 3: Handle transcription errors

```python
except Exception as e:

    print("❌ SPEECH SERVICE ERROR:", e)

    return {
        "success": False,
        "error": str(e)
    }
```

If an exception occurs during transcription or response construction:

1. The exception is caught.
2. An error message is printed.
3. The service returns `success: False`.
4. The exception message is included in the `error` field.

**Important:** The underlying `transcribe_audio()` function already catches exceptions and returns an empty string. Therefore, errors handled inside that function will normally appear here as a successful service response with an empty `text` value, rather than reaching this service-level exception handler.

## 4. Function: `speak_text()`

```python
async def speak_text(text: str):
```

This function handles text-to-speech playback.

It accepts text, passes it to the core TTS engine, and returns an execution-status dictionary.

### Input parameter

| Parameter | Type | Description |
|---|---|---|
| `text` | `str` | Text that should be converted into speech |

### Step 1: Invoke the speech engine

```python
speak(text)
```

The supplied text is passed to `speak()` from:

`app/core/tts_engine.py`

The underlying TTS engine:

1. Checks whether the input text is empty.
2. Sends the text to ElevenLabs.
3. Generates MP3 audio.
4. Saves the generated audio to a temporary file.
5. Plays the audio locally using `playsound`.
6. Attempts to remove the temporary file.

The service does not directly handle audio generation or playback. Those responsibilities belong to the core TTS engine.

### Step 2: Return the execution status

```python
return {
    "success": True
}
```

If `speak()` returns without raising an exception, the service returns:

```json
{
    "success": true
}
```

No audio file path or generated audio data is included in this response.

### Step 3: Handle TTS errors

```python
except Exception as e:

    print("❌ TTS SERVICE ERROR:", e)

    return {
        "success": False,
        "error": str(e)
    }
```

If an exception propagates from the speech engine:

1. The exception is caught.
2. An error message is printed.
3. The service returns `success: False`.
4. The exception message is included in the response.

**Important:** The underlying `speak()` function catches its own exceptions and prints them without re-raising. Consequently, failures handled inside `speak()` will not reach this service-level exception handler. In those cases, `speak_text()` can return `success: True` even though audio generation or playback failed.

## 5. Function Comparison

| Feature | `process_speech()` | `speak_text()` |
|---|---|---|
| Processing direction | Speech-to-text | Text-to-speech |
| Input | Audio file path | Text |
| Core engine | Faster-Whisper | ElevenLabs |
| Main operation | Audio transcription | Audio generation and playback |
| Output | Transcribed text | Execution status |
| Error response | Error dictionary when an exception propagates | Error dictionary when an exception propagates |

## 6. Complete Speech Processing Flow

### Speech-to-text flow

1. A calling component supplies an audio file path.
2. `process_speech()` receives the path.
3. `transcribe_audio()` processes the audio using Faster-Whisper.
4. Recognized speech is returned as text.
5. The service constructs a response dictionary.
6. The transcript is returned to the caller.

### Text-to-speech flow

1. A calling component supplies text.
2. `speak_text()` receives the text.
3. `speak()` sends the text to ElevenLabs.
4. The generated MP3 is saved temporarily.
5. The audio is played locally.
6. The TTS engine attempts to remove the temporary file.
7. The service returns an execution-status dictionary.

## 7. Integration with the Speech API

The speech service provides functionality that can be used by API routes.

The existing speech route imports the Whisper engine directly:

```python
from app.core.whisper_engine import transcribe_audio
```

It does not currently import `process_speech()` or `speak_text()` from this service.

Therefore, although this module provides service-level speech processing functions, the supplied `speech.py` route does not currently delegate to them.

The actual route-to-service integration must be verified against the other route and service files.

## 8. Current Implementation Scope

The module currently provides:

- Service-level speech-to-text processing.
- Service-level text-to-speech playback.
- Integration with Faster-Whisper.
- Integration with the ElevenLabs playback engine.
- Structured success responses.
- Structured exception responses.
- Basic terminal error logging.

The module does not currently implement:

- Audio-file upload handling.
- Audio-format conversion.
- Direct audio-file generation and hosting.
- Streaming speech recognition.
- Streaming speech synthesis.
- Conversation-history integration.
- Automatic speech-to-chat orchestration.
- Background audio-processing tasks.
- Dedicated logging through the shared application logger.

## 9. Important Implementation Considerations

### 9.1 Asynchronous function declarations

Both functions use `async def`, but the underlying engine calls are synchronous and are not awaited.

Consequently, the operations may block the executing thread while transcription, API communication, or playback takes place.

### 9.2 Error propagation

Both core engine functions catch their own exceptions.

This means the service-level exception handlers cannot reliably detect every underlying engine failure.

### 9.3 Local playback dependency

`speak_text()` ultimately uses `playsound`, meaning the TTS operation is designed around local audio playback rather than returning an audio stream to a remote client.

### 9.4 Empty transcription

If Whisper returns an empty string after handling an internal error, `process_speech()` still returns `success: True` because no exception propagates to the service.

## 10. Summary

The `speech_service.py` module provides a service-level interface for Nevark AI's speech capabilities.

It connects Faster-Whisper for audio transcription and ElevenLabs for text-to-speech playback.

`process_speech()` converts an audio file into recognized text, while `speak_text()` sends supplied text to the speech engine for local playback.

The module separates speech-processing orchestration from the underlying engine implementations, providing reusable functions for other backend components.