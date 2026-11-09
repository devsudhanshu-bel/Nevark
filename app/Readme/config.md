# Application Configuration

## 1. Overview

The `config.py` module centralizes the configuration settings used by the Nevark AI Backend.

It manages application metadata, environment variables, external AI service credentials, audio settings, and database configuration.

The module uses `python-dotenv` to load environment variables from a `.env` file and exposes the resulting configuration values as Python module-level variables.

The configuration is organized into five sections:

1. Application settings.
2. Groq configuration.
3. ElevenLabs configuration.
4. Audio configuration.
5. Database configuration.

## 2. Dependencies

```python
import os

from dotenv import load_dotenv
```

| Dependency | Responsibility |
|---|---|
| `os` | Reads environment variables |
| `load_dotenv()` | Loads environment variables from the `.env` file |

## 3. Environment Variable Initialization

```python
load_dotenv()
```

The module calls `load_dotenv()` during initialization.

This loads environment variables from the `.env` file into the process environment, making them accessible through `os.getenv()`.

This allows sensitive configuration values, such as API keys, to be maintained outside the Python source code.

## 4. Application Configuration

```python
APP_NAME = "Nevark AI Backend"

APP_VERSION = "1.0.0"

DEBUG = True
```

These variables define the backend's basic application metadata.

| Variable | Value | Description |
|---|---|---|
| `APP_NAME` | `Nevark AI Backend` | Application name |
| `APP_VERSION` | `1.0.0` | Application version |
| `DEBUG` | `True` | Debug configuration flag |

The `DEBUG` variable is defined as a configuration value. Its actual effect depends on whether other application components consume it.

## 5. Groq Configuration

```python
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

GROQ_MODEL = os.getenv(
    "GROQ_MODEL",
    "llama-3.3-70b-versatile"
)
```

This section configures the Groq integration used for LLM response generation.

### 5.1 API Key

`GROQ_API_KEY` retrieves the Groq API key from the environment.

The key is not hardcoded in the configuration module.

### 5.2 Model Selection

`GROQ_MODEL` retrieves the configured Groq model name.

If the environment variable is not defined, the module uses:

`llama-3.3-70b-versatile`

| Variable | Source | Default |
|---|---|---|
| `GROQ_API_KEY` | Environment variable | No default |
| `GROQ_MODEL` | Environment variable | `llama-3.3-70b-versatile` |

The configured model is used by the LLM integration.

## 6. ElevenLabs Configuration

```python
ELEVENLABS_API_KEY = os.getenv(
    "ELEVENLABS_API_KEY"
)

VOICE_ID = os.getenv("VOICE_ID")

ELEVEN_MODEL = os.getenv(
    "ELEVEN_MODEL",
    "eleven_multilingual_v2"
)
```

This section contains the configuration required for ElevenLabs-based text-to-speech generation.

| Variable | Description | Default |
|---|---|---|
| `ELEVENLABS_API_KEY` | ElevenLabs API credential | No default |
| `VOICE_ID` | Identifier of the configured voice | No default |
| `ELEVEN_MODEL` | ElevenLabs model identifier | `eleven_multilingual_v2` |

The API key and voice ID are loaded from environment variables.

If no model name is supplied, the configuration defaults to `eleven_multilingual_v2`.

These settings support the backend's text-to-speech functionality.

## 7. Audio Configuration

```python
SAMPLE_RATE = int(
    os.getenv("SAMPLE_RATE", 16000)
)

RECORD_SECONDS = int(
    os.getenv("RECORD_SECONDS", 5)
)
```

This section defines the audio-recording configuration.

### 7.1 Sample Rate

`SAMPLE_RATE` determines the configured audio sample rate.

Default:

`16000 Hz`

### 7.2 Recording Duration

`RECORD_SECONDS` defines the configured recording duration.

Default:

`5 seconds`

| Variable | Description | Default |
|---|---|---|
| `SAMPLE_RATE` | Audio sample rate | `16000` |
| `RECORD_SECONDS` | Recording duration in seconds | `5` |

Both values are converted to integers using `int()`.

This means environment variables supplying these settings must contain values that can be converted into valid integers.

## 8. Database Configuration

```python
DATABASE_URL = "sqlite:///./nevark.db"
```

The module defines the database connection URL for the backend.

The configured database is SQLite.

| Property | Value |
|---|---|
| Database engine | SQLite |
| Database file | `nevark.db` |
| Connection URL | `sqlite:///./nevark.db` |
| File location | Relative to the application's working directory |

This configuration identifies the database used by the backend.

**Implementation note:** The supplied `app/database/database.py` also defines its own `DATABASE_URL` with the same value. The database module currently does not import this configuration variable.

## 9. Complete Configuration Reference

| Category | Variable | Default / Source |
|---|---|---|
| Application | `APP_NAME` | `Nevark AI Backend` |
| Application | `APP_VERSION` | `1.0.0` |
| Application | `DEBUG` | `True` |
| Groq | `GROQ_API_KEY` | Environment variable |
| Groq | `GROQ_MODEL` | `llama-3.3-70b-versatile` |
| ElevenLabs | `ELEVENLABS_API_KEY` | Environment variable |
| ElevenLabs | `VOICE_ID` | Environment variable |
| ElevenLabs | `ELEVEN_MODEL` | `eleven_multilingual_v2` |
| Audio | `SAMPLE_RATE` | `16000` |
| Audio | `RECORD_SECONDS` | `5` |
| Database | `DATABASE_URL` | `sqlite:///./nevark.db` |

## 10. Example Environment Configuration

The following illustrates the environment variables expected by this configuration module.

```env
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=llama-3.3-70b-versatile

ELEVENLABS_API_KEY=your_elevenlabs_api_key
VOICE_ID=your_voice_id
ELEVEN_MODEL=eleven_multilingual_v2

SAMPLE_RATE=16000
RECORD_SECONDS=5
```

The database URL and application metadata are currently defined directly in Python rather than loaded from environment variables.

Never commit real API credentials to a public repository.

## 11. Current Implementation Scope

The configuration module currently provides:

- Environment variable loading.
- Application name and version.
- Debug configuration flag.
- Groq API credential configuration.
- Groq model selection.
- ElevenLabs API credential configuration.
- ElevenLabs voice selection.
- ElevenLabs model selection.
- Configurable audio sample rate.
- Configurable recording duration.
- SQLite database URL.

The module does not currently implement:

- Configuration validation.
- Required API-key checks.
- Multiple environment profiles.
- Separate development and production configurations.
- Environment-specific debug behavior.
- Database URL environment overrides.
- Centralized configuration objects or classes.
- Automatic credential rotation.

## 12. Important Implementation Considerations

### 12.1 Missing API credentials

The API keys are retrieved using `os.getenv()` without explicit validation.

If an environment variable is missing, its value will be `None`.

The module does not stop application initialization when a required credential is unavailable.

### 12.2 Configuration duplication

The database URL is defined in both `app/config.py` and `app/database/database.py`.

Although the values currently match, changing one does not automatically update the other.

### 12.3 Debug mode

`DEBUG` is set to `True`, but this module does not itself configure FastAPI debug behavior.

Other application components must consume this value for it to affect runtime behavior.

### 12.4 Relative database path

The SQLite connection URL uses a relative file path.

The actual database location therefore depends on the application's working directory.

## 13. Summary

The `config.py` module provides centralized configuration values for the Nevark AI Backend.

It loads external credentials through environment variables, defines the Groq and ElevenLabs model settings, configures audio recording parameters, and specifies the SQLite database URL.

By separating configuration values from the main application logic, the module provides a single location for managing important backend settings.