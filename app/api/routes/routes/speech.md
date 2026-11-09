# Speech API Route

## 1. Overview

The Speech API Route provides an audio transcription endpoint for the Nevark Backend.

It allows clients to upload an audio file through an HTTP POST request. The uploaded audio is read, written to a temporary WAV file, and passed to the backend's Whisper transcription engine.

The transcription result is returned to the client as JSON.

This route acts as the HTTP interface between the client and the speech-processing component. The actual transcription logic is implemented separately in `app/core/whisper_engine.py`.

## 2. Source File Details

| Property | Description |
|---|---|
| Module | Speech API Route |
| File | `app/api/routes/speech.py` |
| Framework | FastAPI |
| HTTP method | POST |
| Route prefix | `/speech` |
| Endpoint | `/transcribe` |
| Input | Uploaded audio file |
| Processing component | `transcribe_audio()` |
| Speech engine | Whisper engine |
| Temporary storage | Python `tempfile` |

## 3. Imports and Dependencies

The module imports:

```python
from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import File

from app.core.whisper_engine import transcribe_audio

import tempfile
```

| Import | Purpose |
|---|---|
| `APIRouter` | Defines the speech API router |
| `UploadFile` | Represents an uploaded file |
| `File` | Declares the file as a required multipart form input |
| `transcribe_audio` | Processes audio and returns transcription text |
| `tempfile` | Creates a temporary file for audio processing |

The route delegates transcription to the Whisper engine rather than implementing speech recognition itself.

## 4. Router Initialization

```python
router = APIRouter(
    prefix="/speech",
    tags=["Speech"]
)
```

The router defines:

- `prefix="/speech"` – Establishes the speech endpoint URL prefix.
- `tags=["Speech"]` – Groups the endpoint under the Speech category in FastAPI documentation.

## 5. Speech Transcription Endpoint

### Route: `POST /transcribe`

```python
@router.post("/transcribe")
async def transcribe(
    file: UploadFile = File(...)
):
```

The endpoint is asynchronous and accepts one required uploaded file.

The combined endpoint path is:

```http
POST /speech/transcribe
```

### Request Parameter

| Parameter | Type | Required | Description |
|---|---|---|---|
| `file` | `UploadFile` | Yes | Audio file uploaded by the client |

`File(...)` declares the file as a required multipart form-data input.

The endpoint uses FastAPI's `UploadFile` interface to access the uploaded file.

## 6. Audio Processing Workflow

### Step 1 — Create a Temporary Audio File

The endpoint creates a temporary file:

```python
with tempfile.NamedTemporaryFile(
    delete=False,
    suffix=".wav"
) as temp_audio:
```

Configuration:

| Parameter | Value | Purpose |
|---|---|---|
| `delete` | `False` | Prevents automatic deletion when the file is closed |
| `suffix` | `.wav` | Gives the temporary file a WAV extension |

The temporary file is used as an intermediate storage location before transcription.

### Step 2 — Read Uploaded Audio

```python
content = await file.read()
```

The uploaded audio is read asynchronously.

The returned content is stored as bytes in the `content` variable.

### Step 3 — Write Audio to Temporary Storage

```python
temp_audio.write(content)
```

The uploaded bytes are written into the temporary file.

This makes the audio available as a filesystem path for the transcription engine.

### Step 4 — Capture Temporary File Path

```python
temp_path = temp_audio.name
```

The temporary file's path is stored in `temp_path`.

This path is passed to the transcription function.

### Step 5 — Invoke Whisper Transcription

```python
text = transcribe_audio(temp_path)
```

The route invokes `transcribe_audio()` from:

```text
app/core/whisper_engine.py
```

The function receives the temporary audio file path and returns the recognized text.

The transcription implementation, model configuration, and supported audio formats must be understood from the Whisper engine source file itself.

### Step 6 — Return Transcription

The endpoint returns:

```python
{
    "success": True,
    "text": text
}
```

The transcription result is placed in the `text` field.

## 7. API Request and Response

### Endpoint Information

| Property | Value |
|---|---|
| Method | `POST` |
| URL | `/speech/transcribe` |
| Content type | `multipart/form-data` |
| Input field | `file` |
| Response | JSON |

### Example Request

The client sends a multipart form-data request containing the audio file under the field name `file`.

Example using cURL:

```bash
curl -X POST "http://localhost:8000/speech/transcribe" \
  -F "file=@recording.wav"
```

### Example Response

```json
{
    "success": true,
    "text": "Hello, how are you today?"
}
```

The transcription text shown is illustrative. The actual value depends on the uploaded audio and Whisper engine output.

## 8. Integration with the Backend

The speech router is registered in the central API router:

```python
api_router.include_router(speech_router)
```

The processing flow is:

```text
Client
  |
  | POST /speech/transcribe
  | multipart/form-data
  v
Speech API Route
  |
  v
UploadFile
  |
  v
Read Audio Bytes
  |
  v
Temporary WAV File
  |
  v
Whisper Engine
  |
  v
transcribe_audio()
  |
  v
Recognized Text
  |
  v
JSON Response
```

This separation allows the API layer to handle file uploads while the Whisper engine handles transcription.

## 9. Important Implementation Notes

- The uploaded file is required.
- The endpoint reads the entire uploaded file into memory before writing it to disk.
- The temporary file is created with a `.wav` suffix.
- The route does not explicitly convert the uploaded audio into WAV format; it writes the uploaded bytes unchanged.
- The transcription engine is called synchronously inside the asynchronous endpoint.
- The route does not explicitly delete the temporary file after transcription.
- No file-size restriction is declared in this route.
- No MIME-type or audio-format validation is implemented here.
- No custom exception handling is implemented around temporary-file creation or transcription.
- No authentication or authorization dependency is declared.

**Important:** A `.wav` filename suffix does not itself convert audio into WAV format. The actual compatibility of uploaded audio formats depends on the transcription engine and the uploaded file contents.

## 10. Error Handling Considerations

The route does not define a custom error response.

Potential failures include:

- Failure while reading the uploaded file.
- Failure while creating the temporary file.
- Failure while writing the uploaded bytes.
- Failure inside `transcribe_audio()`.
- Unsupported or invalid audio content.

Such exceptions are not caught by this route and are therefore left to FastAPI's exception-handling mechanisms or any handling implemented by the underlying transcription engine.

## 11. Conclusion

The Speech API Route provides the audio-upload interface for Nevark's speech-to-text functionality.

It accepts uploaded audio, stores it temporarily, delegates transcription to the Whisper engine, and returns the recognized text in JSON format.

This keeps HTTP file handling separate from the speech-recognition implementation.