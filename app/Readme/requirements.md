# Backend Dependencies

## 1. Overview

The `requirements.txt` file defines the external Python dependencies required by the Nevark AI Backend.

It provides a centralized list of packages used for:

- FastAPI application development.
- ASGI server execution.
- Environment configuration.
- LLM integration.
- Speech recognition and synthesis.
- Audio recording and processing.
- Relational database management.
- WebSocket communication.
- Vector database storage.
- Text embedding generation.

These dependencies can be installed together using Python's package installer, `pip`.

## 2. Dependency Installation

Run the following command from the backend project directory:

```bash
pip install -r requirements.txt
```

This installs the packages listed in the requirements file into the active Python environment.

It is recommended to use a virtual environment to isolate the backend dependencies.

## 3. Complete Dependency List

| Package | Purpose in Nevark AI |
|---|---|
| `fastapi` | Backend API framework |
| `uvicorn` | ASGI server for running the FastAPI application |
| `python-dotenv` | Loads environment variables from `.env` |
| `groq` | Connects to Groq for LLM response generation |
| `faster-whisper` | Speech-to-text processing |
| `elevenlabs` | Text-to-speech generation |
| `playsound==1.2.2` | Plays generated audio locally |
| `sounddevice` | Captures microphone audio |
| `scipy` | Writes audio recordings into WAV files |
| `numpy` | Audio sample processing and numerical operations |
| `sqlalchemy` | ORM and relational database operations |
| `python-multipart` | Handles multipart form-data uploads |
| `websockets` | WebSocket communication support |
| `chromadb` | Vector database for semantic memory |
| `sentence-transformers` | Generates text embeddings |

## 4. Dependency Categories

### 4.1 Backend Framework and Server

**Packages:**
- `fastapi`
- `uvicorn`

FastAPI provides the HTTP and WebSocket application framework.

Uvicorn provides the ASGI server used to run the application.

Together, they form the backend's API execution layer.

### 4.2 Environment and Configuration

**Package:**
- `python-dotenv`

Used to load environment variables from the `.env` file.

This supports configuration of external service credentials and model settings without hardcoding those values into application logic.

### 4.3 LLM Integration

**Package:**
- `groq`

Provides the client library used by the LLM engine to communicate with Groq's chat-completion API.

### 4.4 Speech Recognition

**Package:**
- `faster-whisper`

Provides speech-to-text functionality.

The backend uses it to transcribe uploaded or recorded audio into text.

### 4.5 Text-to-Speech

**Packages:**
- `elevenlabs`
- `playsound==1.2.2`

ElevenLabs generates speech audio from text.

`playsound` plays generated MP3 files locally through the TTS engine.

The version of `playsound` is explicitly pinned to `1.2.2`.

### 4.6 Audio Recording and Processing

**Packages:**
- `sounddevice`
- `scipy`
- `numpy`

These libraries support local audio capture and processing.

| Package | Responsibility |
|---|---|
| `sounddevice` | Microphone recording |
| `scipy` | WAV file writing |
| `numpy` | Audio sample scaling and conversion |

The audio utility uses these packages to capture mono audio and save it as a WAV file.

### 4.7 Database Management

**Package:**
- `sqlalchemy`

SQLAlchemy provides the ORM layer for the SQLite database.

It supports:

- Database engine initialization.
- Session management.
- ORM model definitions.
- Database queries.
- Conversation persistence.

### 4.8 File Upload Handling

**Package:**
- `python-multipart`

Provides multipart form-data parsing support for FastAPI endpoints that receive uploaded files.

It is required by the speech and voice upload routes.

### 4.9 WebSocket Communication

**Package:**
- `websockets`

Provides WebSocket protocol support for asynchronous communication.

The backend includes WebSocket routes and a connection-management service.

### 4.10 Vector Database and Embeddings

**Packages:**
- `chromadb`
- `sentence-transformers`

These packages provide the foundation for Nevark's semantic memory system.

| Package | Responsibility |
|---|---|
| `chromadb` | Stores and retrieves vectorized documents |
| `sentence-transformers` | Converts text into numerical embeddings |

The backend uses the `all-MiniLM-L6-v2` embedding model through Sentence Transformers and stores the resulting vectors in ChromaDB.

## 5. Dependency-to-Module Mapping

The following table connects the dependencies to the source modules documented in the backend.

| Package | Backend module |
|---|---|
| FastAPI | `app/main.py`, `app/api/routes/` |
| Uvicorn | Application server execution |
| python-dotenv | `app/config.py`, `app/core/llm_engine.py` |
| Groq | `app/core/llm_engine.py` |
| Faster-Whisper | `app/core/whisper_engine.py` |
| ElevenLabs | `app/core/tts_engine.py` |
| playsound | `app/core/tts_engine.py` |
| sounddevice | `app/utils/audio.py` |
| SciPy | `app/utils/audio.py` |
| NumPy | `app/utils/audio.py`, `app/core/embeddings.py` |
| SQLAlchemy | `app/database/`, `app/services/` |
| python-multipart | `app/api/routes/speech.py`, `app/api/routes/voice.py` |
| websockets | WebSocket communication support |
| ChromaDB | `app/core/rag_engine.py` |
| Sentence Transformers | `app/core/embeddings.py` |

## 6. Installation Considerations

### 6.1 Python environment

Install dependencies inside the intended Python environment to avoid conflicts with globally installed packages.

### 6.2 Audio dependencies

`sounddevice` and `playsound` depend on the host system's audio capabilities.

Microphone recording and local playback require a compatible audio environment.

### 6.3 Faster-Whisper

Faster-Whisper uses additional model resources for speech recognition.

The backend's Whisper implementation configures the `small` model with CPU execution and `int8` computation.

### 6.4 Sentence Transformers

Sentence Transformers downloads or loads the configured embedding model:

`all-MiniLM-L6-v2`

The model must be available in the execution environment before embedding generation can succeed.

### 6.5 Version management

Only `playsound` has an explicit version pin in the supplied requirements file.

The other dependencies do not specify version constraints.

This means installations may resolve to different package versions over time.

## 7. Current Implementation Scope

The requirements file currently declares dependencies for:

- API development and serving.
- Environment variable management.
- LLM integration.
- Speech recognition.
- Speech synthesis.
- Local audio playback.
- Microphone recording.
- Numerical audio processing.
- Relational database access.
- Multipart uploads.
- WebSocket communication.
- Vector storage.
- Semantic embedding generation.

It does not currently define:

- Exact versions for most packages.
- Platform-specific dependency groups.
- Development-only dependencies.
- Separate production requirements.
- Optional dependency groups.
- A complete dependency lockfile.

## 8. Summary

The `requirements.txt` file defines the external Python libraries needed to run the Nevark AI Backend.

It covers the complete technology foundation of the backend, including FastAPI, Groq, Faster-Whisper, ElevenLabs, SQLAlchemy, ChromaDB, Sentence Transformers, and audio-processing libraries.

Together, these dependencies support Nevark's API layer, conversational AI, speech processing, persistent memory, and real-time communication capabilities.