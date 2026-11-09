# Backend Server Launcher

## 1. Overview

The `run.py` module provides the execution entry point for starting the Nevark AI Backend.

It uses Uvicorn, an ASGI server, to launch the FastAPI application defined in `app/main.py`.

The module configures:

- Application import path.
- Server host.
- Server port.
- Automatic reload behavior.

This provides a simple way to start the backend without manually specifying the Uvicorn command every time.

## 2. Dependency

```python
import uvicorn
```

| Dependency | Purpose |
|---|---|
| `uvicorn` | Runs the FastAPI application as an ASGI server |

Uvicorn handles incoming HTTP and WebSocket connections and forwards them to the FastAPI application.

## 3. Main Execution Guard

```python
if __name__ == "__main__":
```

This condition checks whether `run.py` is being executed directly as the main Python script.

When executed directly, the code inside this block runs.

For example:

```bash
python run.py
```

Importing `run.py` from another Python module does not automatically execute the server-launching block.

## 4. Uvicorn Server Initialization

```python
uvicorn.run(
    "app.main:app",
    host="0.0.0.0",
    port=8000,
    reload=True
)
```

The `uvicorn.run()` function starts the ASGI server using the supplied configuration.

### 4.1 Application Import Path

```python
"app.main:app"
```

This identifies the FastAPI application that Uvicorn should load.

It follows the format:

`module_path:application_variable`

In this configuration:

- `app.main` refers to the Python module `app/main.py`.
- `app` refers to the FastAPI application instance defined inside that module.

Uvicorn imports the module and retrieves its `app` object.

### 4.2 Host Configuration

```python
host="0.0.0.0"
```

The server binds to all available network interfaces on the host machine.

This allows the backend to accept connections through interfaces other than just the local loopback address, subject to network and firewall configuration.

### 4.3 Port Configuration

```python
port=8000
```

The backend listens on port `8000`.

The local development address is:

`http://localhost:8000`

The FastAPI application documentation is normally available at:

`http://localhost:8000/docs`

### 4.4 Automatic Reload

```python
reload=True
```

Enables Uvicorn's automatic reload functionality.

During development, Uvicorn monitors application files and restarts the server when relevant source changes are detected.

This helps developers test code changes without manually restarting the backend after every modification.

**Important:** Automatic reload is intended for development. It should generally be disabled in production deployments.

## 5. Configuration Summary

| Parameter | Value | Responsibility |
|---|---|---|
| Application | `app.main:app` | Identifies the FastAPI instance |
| Host | `0.0.0.0` | Binds to all available network interfaces |
| Port | `8000` | Defines the server listening port |
| Reload | `True` | Enables automatic development reload |

## 6. How to Run Nevark Backend

### Step 1: Navigate to the backend directory

```bash
cd nevark_backend
```

### Step 2: Activate the Python virtual environment

If using a virtual environment, activate it before installing or running the application.

Windows:

```bash
venv\Scripts\activate
```

Linux or macOS:

```bash
source venv/bin/activate
```

### Step 3: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure environment variables

Create or update the `.env` file in the backend root directory.

The backend configuration expects environment variables such as:

```env
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=llama-3.3-70b-versatile

ELEVENLABS_API_KEY=your_elevenlabs_api_key
VOICE_ID=your_voice_id
ELEVEN_MODEL=eleven_multilingual_v2

SAMPLE_RATE=16000
RECORD_SECONDS=5
```

### Step 5: Start the backend

```bash
python run.py
```

This executes the Uvicorn server configuration defined in `run.py`.

## 7. Application Startup Flow

The execution sequence is:

```text
       python run.py
             |
             v
       Import Uvicorn
             |
             v
     Execute Main Guard
             |
             v
       uvicorn.run()
             |
             v
      Load app.main:app
             |
             v
       Execute main.py
             |
       +-----+------+
       |            |
       v            v
  Create Tables  Configure App
       |            |
       |        Configure CORS
       |            |
       |        Register Routes
       |            |
       +-----+------+
             |
             v
       Start ASGI Server
             |
             v
      Listen on Port 8000
```

The diagram describes the relationship between the launcher and the FastAPI application initialization code.

## 8. Backend Access Points

With the configured host and port, the backend exposes these local development addresses:

| Resource | Address |
|---|---|
| Backend root | `http://localhost:8000/` |
| API documentation | `http://localhost:8000/docs` |
| Alternative API documentation | `http://localhost:8000/redoc` |
| Health endpoint | `http://localhost:8000/health/` |
| Chat endpoint | `http://localhost:8000/chat/` |
| Voice endpoint | `http://localhost:8000/voice/` |
| Speech endpoint | `http://localhost:8000/speech/transcribe` |
| WebSocket endpoint | `ws://localhost:8000/ws/chat` |

The endpoint paths are based on the route definitions documented in the backend API modules.

## 9. Current Implementation Scope

The module currently provides:

- Uvicorn server initialization.
- FastAPI application loading.
- Configurable server host through source-code editing.
- Configurable server port through source-code editing.
- Automatic development reload.
- Direct Python execution support.

The module does not currently implement:

- Production deployment configuration.
- HTTPS certificate management.
- Custom worker configuration.
- Reverse-proxy configuration.
- Environment-based port selection.
- Process supervision.
- Container orchestration.
- Deployment health monitoring.

These responsibilities are not defined in the supplied source.

## 10. Important Implementation Considerations

### 10.1 Network accessibility

The `0.0.0.0` host binding allows the server to listen on available network interfaces.

Actual accessibility from another machine depends on firewall rules, network configuration, and deployment environment.

### 10.2 Development reload

`reload=True` is useful during development because source changes trigger server restarts.

For production deployment, use an appropriate server configuration without development reload.

### 10.3 Environment configuration

The launcher does not explicitly load `.env` itself.

Environment loading is handled elsewhere in the application, including the configuration and LLM engine modules.

### 10.4 Single application import target

The launcher references `app.main:app`.

This keeps the server-launching script independent of the internal implementation of the FastAPI application.

## 11. Summary

The `run.py` module provides the startup mechanism for the Nevark AI Backend.

It uses Uvicorn to load the FastAPI application from `app.main:app`, binds the server to `0.0.0.0`, listens on port `8000`, and enables automatic reload during development.

Together with `app/main.py`, it provides the complete application-launching foundation for local backend execution.