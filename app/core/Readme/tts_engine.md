# Text-to-Speech (TTS) Engine

## 1. Overview

The `tts_engine.py` module provides text-to-speech functionality for Nevark AI using the ElevenLabs API.

It converts text into MP3 audio using a configured ElevenLabs voice and model.

The module exposes two main functions:

- `speak()` – Generates speech, saves it temporarily, plays it through the local audio playback system, and removes the temporary file.
- `generate_audio()` – Generates speech and saves the resulting MP3 file inside the `generated_audio/` directory, returning its file path.

Both functions use the same ElevenLabs text-to-speech configuration but serve different purposes: immediate playback and persistent audio-file generation.

## 2. Dependencies

```python
import os
import uuid
import time

from dotenv import load_dotenv

from elevenlabs.client import ElevenLabs
from elevenlabs import save

from playsound import playsound
```

| Dependency | Purpose |
|---|---|
| `os` | Reads environment variables, creates directories, checks file existence, and removes files |
| `uuid` | Generates unique identifiers for audio filenames |
| `time` | Introduces a short delay after audio playback |
| `dotenv` | Loads environment variables from the `.env` file |
| `ElevenLabs` | Initializes the ElevenLabs API client |
| `save` | Saves generated audio data to an MP3 file |
| `playsound` | Plays generated audio through the local playback system |

## 3. Environment Configuration

```python
load_dotenv()

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
VOICE_ID = os.getenv("VOICE_ID")
ELEVEN_MODEL = os.getenv("ELEVEN_MODEL")
```

The module loads its configuration from environment variables.

| Variable | Purpose |
|---|---|
| `ELEVENLABS_API_KEY` | Authenticates requests to ElevenLabs |
| `VOICE_ID` | Identifies the voice used for speech generation |
| `ELEVEN_MODEL` | Specifies the ElevenLabs model used for text-to-speech |

This keeps API credentials and voice configuration outside the source code.

## 4. ElevenLabs Client Initialization

```python
client = ElevenLabs(
    api_key=ELEVENLABS_API_KEY
)
```

The ElevenLabs client is initialized using the configured API key.

The client is created at module level and reused by both audio-generation functions.

This avoids creating a separate client instance every time `speak()` or `generate_audio()` is called.

## 5. Audio Output Format

Both functions use the following output format:

```python
output_format="mp3_44100_128"
```

This configures the generated audio as:

| Property | Value |
|---|---|
| Format | MP3 |
| Sample rate | 44,100 Hz |
| Bitrate | 128 kbps |

The generated audio is saved with the `.mp3` extension.

## 6. Function: `speak()`

```python
def speak(text: str):
```

The `speak()` function generates speech from the supplied text and plays the resulting audio locally.

It is intended for immediate voice output rather than retaining generated audio files.

### Input parameter

| Parameter | Type | Description |
|---|---|---|
| `text` | `str` | Text that should be converted into speech |

### Step 1: Validate the input

```python
if not text:
    return
```

If the supplied text is empty or otherwise evaluates to `False`, the function exits immediately.

No API request or audio generation takes place.

### Step 2: Generate speech through ElevenLabs

```python
audio = client.text_to_speech.convert(
    voice_id=VOICE_ID,
    model_id=ELEVEN_MODEL,
    text=text,
    output_format="mp3_44100_128"
)
```

The text is submitted to the ElevenLabs text-to-speech conversion API.

The request includes:

- Configured voice ID.
- Configured ElevenLabs model.
- Input text.
- MP3 output format.

The returned audio data is stored in the `audio` variable.

### Step 3: Generate a unique filename

```python
filename = f"nevark_{uuid.uuid4().hex}.mp3"
```

The module uses `uuid.uuid4().hex` to generate a unique identifier.

This identifier is included in the filename to reduce the possibility of filename collisions.

Example filename:

```text
nevark_a1b2c3d4e5f678901234567890abcdef.mp3
```

The filename above is illustrative.

### Step 4: Save generated audio

```python
save(audio, filename)
```

The generated audio data is saved to the specified MP3 file.

The file is created using the generated filename in the current working directory.

### Step 5: Play generated audio

```python
playsound(filename)
```

The `playsound` library plays the saved MP3 file through the local audio playback system.

This operation is used for immediate speech output.

### Step 6: Introduce a short delay

```python
time.sleep(0.3)
```

The function waits for 0.3 seconds after the playback call returns.

This is a fixed delay; it is not calculated from the audio duration.

### Step 7: Remove the temporary audio file

```python
if os.path.exists(filename):
    os.remove(filename)
```

After playback, the function checks whether the generated file exists.

If it does, the file is deleted.

This prevents temporary playback files from accumulating in the working directory during normal successful execution.

### Step 8: Handle errors

```python
except Exception as e:
    print("❌ TTS ERROR:", e)
```

If an exception occurs during speech generation, saving, playback, or file removal, the function prints an error message.

The exception is caught rather than propagated to the caller.

The function does not return a success indicator or error object.

## 7. Function: `generate_audio()`

```python
def generate_audio(text: str):
```

The `generate_audio()` function converts text into speech and saves the generated MP3 file inside the `generated_audio/` directory.

Unlike `speak()`, this function does not play the audio.

Instead, it returns the generated file path so that another component can use the saved audio.

### Input parameter

| Parameter | Type | Description |
|---|---|---|
| `text` | `str` | Text that should be converted into an audio file |

### Return values

| Return value | Meaning |
|---|---|
| File path (`str`) | Successfully generated audio file location |
| `None` | Empty input or an exception occurred |

### Step 1: Validate the input

```python
if not text:
    return None
```

If the input text is empty or otherwise evaluates to `False`, the function returns `None`.

### Step 2: Generate speech

```python
audio = client.text_to_speech.convert(
    voice_id=VOICE_ID,
    model_id=ELEVEN_MODEL,
    text=text,
    output_format="mp3_44100_128"
)
```

The function sends the supplied text to the same ElevenLabs text-to-speech endpoint used by `speak()`.

It uses the configured voice, model, and MP3 output format.

### Step 3: Create the output directory

```python
os.makedirs(
    "generated_audio",
    exist_ok=True
)
```

The module creates the `generated_audio/` directory if it does not already exist.

The `exist_ok=True` parameter prevents an error when the directory is already present.

### Step 4: Generate the output filename

```python
filename = (
    f"generated_audio/"
    f"{uuid.uuid4().hex}.mp3"
)
```

A unique UUID is generated for the output file.

Unlike `speak()`, the filename is created inside the `generated_audio/` directory.

Example:

```text
generated_audio/a1b2c3d4e5f678901234567890abcdef.mp3
```

### Step 5: Save the generated audio

```python
save(audio, filename)
```

The generated audio data is saved to the specified path.

### Step 6: Return the file path

```python
return filename
```

After successful generation and saving, the function returns the relative path of the generated MP3 file.

The file is not deleted by this function.

This allows another backend component to access the generated audio later.

### Step 7: Handle errors

```python
except Exception as e:
    print(
        "❌ AUDIO GENERATION ERROR:",
        e
    )

    return None
```

If an exception occurs during generation, directory creation, or saving:

1. An error message is printed.
2. The exception is caught.
3. The function returns `None`.

## 8. Difference Between `speak()` and `generate_audio()`

Both functions use ElevenLabs to generate speech, but their output-handling behavior is different.

| Feature | `speak()` | `generate_audio()` |
|---|---|---|
| Text-to-speech provider | ElevenLabs | ElevenLabs |
| Input | Text | Text |
| Output format | MP3 | MP3 |
| Audio playback | Yes | No |
| Output directory | Current working directory | `generated_audio/` |
| Filename | UUID-based | UUID-based |
| File cleanup | Attempts to delete temporary file | Retains generated file |
| Return value | No explicit return value | File path or `None` |
| Main purpose | Immediate local speech playback | Audio-file generation |

The distinction is important:

- `speak()` is designed for speaking a response immediately.
- `generate_audio()` is designed to create an audio asset that another component can access.

## 9. Complete Execution Flow

### Immediate playback flow

1. A component calls `speak(text)`.
2. The function checks whether the text is empty.
3. ElevenLabs generates the speech audio.
4. A UUID-based temporary filename is created.
5. The audio is saved as an MP3 file.
6. `playsound()` plays the generated file.
7. The function waits for 0.3 seconds.
8. The temporary file is removed if it still exists.

### Persistent audio-generation flow

1. A component calls `generate_audio(text)`.
2. The function checks whether the text is empty.
3. ElevenLabs generates the speech audio.
4. The `generated_audio/` directory is created if necessary.
5. A UUID-based MP3 filename is generated.
6. The audio is saved to that location.
7. The relative file path is returned to the caller.

## 10. Integration Considerations

The module provides two different interfaces for other backend components.

A component that needs immediate local playback can call:

```python
speak("Hello! How can I help you?")
```

A component that needs a generated audio file can call:

```python
audio_path = generate_audio(
    "Hello! How can I help you?"
)
```

The second function can be used by another component that needs to serve, transfer, or otherwise process the generated MP3 file.

These are illustrative calls based on the functions exposed by this module.

The module itself does not define an HTTP download endpoint, upload the audio to cloud storage, or manage audio-file access permissions.

## 11. Current Implementation Scope

The module currently provides:

- ElevenLabs API integration.
- Environment-based API and voice configuration.
- Text-to-speech conversion.
- MP3 audio generation at the configured output format.
- UUID-based audio filenames.
- Local audio playback through `playsound`.
- Temporary audio-file cleanup in `speak()`.
- Persistent generated audio files in `generated_audio/`.
- File-path return from `generate_audio()`.
- Basic exception handling for both functions.

The module does not currently implement:

- Streaming audio playback.
- Audio generation progress reporting.
- Explicit retry logic.
- Custom voice or model selection per function call.
- Audio-duration-based cleanup.
- Automatic cleanup of retained generated files.
- Audio metadata management.
- Cloud-based audio hosting.
- Explicit validation of API configuration before client initialization.

## 12. Important Implementation Considerations

### 12.1 Local playback dependency

`speak()` uses `playsound`, which requires a compatible local audio playback environment.

This means the function is intended for an environment where audio playback is available. It is not simply an API response generator.

### 12.2 Temporary file cleanup

The temporary file is removed after successful playback and the fixed delay.

If an exception occurs before the cleanup section is reached, the temporary file may remain on disk.

### 12.3 Generated audio retention

`generate_audio()` deliberately does not remove the generated file.

The caller is responsible for deciding how long the generated audio should be retained and when it should be deleted.

### 12.4 Blocking operations

The functions are synchronous. The supplied implementation does not use asynchronous ElevenLabs calls or background tasks.

## 13. Summary

The `tts_engine.py` module provides the text-to-speech layer of Nevark AI through ElevenLabs.

It supports two output modes: immediate local playback through `speak()` and MP3 file generation through `generate_audio()`.

Both functions share the same configured ElevenLabs client, voice, model, and output format, while handling the generated audio differently depending on the intended use.

This module provides the audio-generation foundation for voice-enabled interactions in the Nevark backend.