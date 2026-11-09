# Voice API Route

## 1. Overview

The Voice API Route provides an HTTP interface for audio-based interactions with the Nevark Backend.

It accepts an uploaded audio file through a POST request and forwards that file to the `process_voice()` function in the service layer.

The service is responsible for processing the uploaded audio and returning the resulting response.

This route keeps the HTTP upload-handling layer separate from the voice-processing implementation.

## 2. Source File Details

| Property | Description |
|---|---|
| Module | Voice API Route |
| File | `app/api/routes/voice.py` |
| Framework | FastAPI |
| HTTP method | POST |
| Route prefix | `/voice` |
| Endpoint | `/` |
| Input | Uploaded audio file |
| Service dependency | `process_voice()` |
| Processing style | Asynchronous |

## 3. Imports and Dependencies

```python
from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import File

from app.services.voice_service import (
    process_voice
)
```

| Import | Purpose |
|---|---|
| `APIRouter` | Defines the voice API router |
| `UploadFile` | Represents the uploaded audio file |
| `File` | Declares the required multipart file input |
| `process_voice` | Handles voice processing in the service layer |

The route does not implement audio processing itself.

## 4. Router Initialization

```python
router = APIRouter(
    prefix="/voice",
    tags=["Voice"]
)
```

The router defines:

- `prefix="/voice"` – Establishes the voice endpoint URL prefix.
- `tags=["Voice"]` – Groups the endpoint under the Voice category in FastAPI documentation.

## 5. Voice Chat Endpoint

### Route: `POST /`

```python
@router.post("/")
async def voice_chat(
    audio: UploadFile = File(...)
):
```

The endpoint is asynchronous and accepts one required uploaded file.

The combined endpoint path is:

```http
POST /voice/
```

### Request Parameter

| Parameter | Type | Required | Description |
|---|---|---|---|
| `audio` | `UploadFile` | Yes | Audio file uploaded by the client |

`File(...)` declares the uploaded audio as a required multipart form-data field.

The parameter name expected by the endpoint is `audio`.

## 6. Voice Processing Workflow

The endpoint delegates processing directly to the voice service:

```python
return await process_voice(
    audio
)
```

The workflow is:

1. A client sends a POST request to `/voice/`.
2. FastAPI receives the uploaded audio.
3. The file is represented as an `UploadFile` object.
4. The route passes the audio object to `process_voice()`.
5. The endpoint awaits the asynchronous service function.
6. The service result is returned directly to the client.

Unlike the Speech API route, this endpoint does not explicitly create a temporary WAV file or call `transcribe_audio()`.

Those operations, if performed, must be verified in `app/services/voice_service.py`.

## 7. API Request and Response

### Endpoint Information

| Property | Value |
|---|---|
| Method | `POST` |
| URL | `/voice/` |
| Content type | `multipart/form-data` |
| Input field | `audio` |
| Processing function | `process_voice()` |
| Response | Service return value |

### Example Request

Using cURL:

```bash
curl -X POST "http://localhost:8000/voice/" \
  -F "audio=@recording.wav"
```

The uploaded file must use the form field name `audio`.

### Response

The endpoint returns the result of:

```python
await process_voice(audio)
```

No response dictionary or response schema is defined directly in this route.

Therefore, the exact response structure depends entirely on the implementation of `process_voice()`.

## 8. Integration with the Backend

The voice router is registered in the central API router:

```python
api_router.include_router(voice_router)
```

The routing architecture is:

```text
Client
  |
  | POST /voice/
  | multipart/form-data
  v
Voice API Route
  |
  v
UploadFile
  |
  v
voice_chat()
  |
  | await process_voice(audio)
  v
Voice Service
  |
  v
Service Result
  |
  v
Client Response
```

This architecture keeps the API route lightweight and delegates business logic to the service layer.

## 9. Difference Between Speech and Voice Routes

Nevark exposes separate endpoints for speech transcription and voice processing.

| Feature | Speech API | Voice API |
|---|---|---|
| Endpoint | `/speech/transcribe` | `/voice/` |
| HTTP method | POST | POST |
| Upload parameter | `file` | `audio` |
| Processing function | `transcribe_audio()` | `process_voice()` |
| Implementation layer | `app/core/whisper_engine.py` | `app/services/voice_service.py` |
| Temporary WAV file | Explicitly created in route | Not created in this route |
| Response | Transcription wrapped in JSON | Service result returned directly |

The Speech API explicitly exposes transcription functionality, while the Voice API delegates the complete operation to a dedicated service.

## 10. Important Implementation Notes

- The uploaded audio field is required.
- The route uses FastAPI's `UploadFile`.
- The endpoint is asynchronous.
- The service function is awaited.
- The route does not explicitly read the uploaded file.
- The route does not perform audio-format conversion.
- No MIME-type or file-size validation is declared.
- No custom exception handling is implemented.
- No authentication or authorization dependency is declared.
- The response structure is determined by the voice service.

## 11. Conclusion

The Voice API Route provides the HTTP entry point for audio-based interactions in Nevark Backend.

It accepts an uploaded audio file and delegates processing to `process_voice()`.

By keeping the route separate from the voice service, the backend maintains a clean separation between HTTP request handling and the actual voice-processing workflow.