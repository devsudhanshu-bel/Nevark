# FastAPI Application Entry Point

## 1. Overview

The `main.py` module serves as the primary entry point for the Nevark AI Backend.

It initializes the FastAPI application and connects the API routing layer, database configuration, and logging system.

Its main responsibilities include:

- Creating database tables using SQLAlchemy metadata.
- Initializing the FastAPI application.
- Configuring Cross-Origin Resource Sharing (CORS).
- Registering the centralized API router.
- Defining the root endpoint.
- Logging application startup and shutdown events.

This module brings together the backend components and prepares the application to serve HTTP and WebSocket requests.

## 2. Dependencies

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router

from app.database.database import engine
from app.database.models import Base

from app.utils.logger import logger
```

| Dependency | Responsibility |
|---|---|
| `FastAPI` | Creates the backend application |
| `CORSMiddleware` | Configures cross-origin request handling |
| `api_router` | Provides the registered API route modules |
| `engine` | Provides SQLAlchemy database connectivity |
| `Base` | Provides ORM metadata for database models |
| `logger` | Records application lifecycle events |

## 3. Database Table Initialization

```python
Base.metadata.create_all(bind=engine)
```

Before the FastAPI application is initialized, the module invokes SQLAlchemy's metadata table-creation operation.

### How it works

- `Base.metadata` contains the table definitions registered through the shared SQLAlchemy declarative base.
- `create_all()` checks the configured database for the tables represented in that metadata.
- `bind=engine` specifies the database engine against which the operation is performed.

The configured database is:

`sqlite:///./nevark.db`

The currently defined `Conversation` model is registered through the shared `Base`.

This allows the application to create the corresponding table when it does not already exist.

**Important:** `create_all()` creates missing tables but does not perform schema migrations or automatically modify existing tables when model definitions change.

## 4. FastAPI Application Initialization

```python
app = FastAPI(
    title="Nevark AI Backend",
    version="1.0.0"
)
```

The module creates the main FastAPI application instance and stores it in `app`.

### Application metadata

| Property | Value |
|---|---|
| Framework | FastAPI |
| Application title | `Nevark AI Backend` |
| Version | `1.0.0` |

The title and version are used as application metadata and are reflected in FastAPI's generated API documentation.

The `app` instance is the object served by the ASGI server.

## 5. CORS Configuration

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

The module registers FastAPI's `CORSMiddleware` to control cross-origin requests.

CORS is important when a frontend application and backend API are running on different origins.

### 5.1 Allowed origins

The configuration permits requests from two development frontend origins:

| Origin | Purpose |
|---|---|
| `http://localhost:5173` | Localhost frontend |
| `http://127.0.0.1:5173` | Loopback-IP frontend |

These origins commonly correspond to a frontend development server running on port `5173`.

### 5.2 Credentials

```python
allow_credentials=True
```

Allows cross-origin requests to include credentials where supported by the browser and request configuration.

### 5.3 Allowed methods

```python
allow_methods=["*"]
```

Allows all HTTP methods through the CORS middleware.

### 5.4 Allowed headers

```python
allow_headers=["*"]
```

Allows all request headers through the CORS middleware.

### CORS configuration summary

| Setting | Configuration |
|---|---|
| Allowed origins | Two local development origins |
| Credentials | Enabled |
| HTTP methods | All |
| Request headers | All |

**Implementation note:** The configured origins are local development addresses. Other frontend origins are not included in this allowlist.

## 6. API Router Registration

```python
app.include_router(api_router)
```

The main application registers the centralized API router.

The router is imported from:

`app/api/router.py`

That module aggregates the individual route modules.

### Registered route modules

| Route module | Responsibility |
|---|---|
| `chat.py` | Text-based AI chat |
| `health.py` | Health endpoint |
| `memory.py` | Memory endpoint |
| `speech.py` | Audio transcription |
| `websocket.py` | WebSocket chat communication |
| `voice.py` | Voice interaction |

The router registration makes these routes part of the main FastAPI application.

The individual endpoint paths and HTTP methods are defined within their respective route modules.

## 7. Root Endpoint

```python
@app.get("/")
async def root():

    return {
        "message": "Nevark AI Backend Running",
        "status": "online"
    }
```

The module defines a root HTTP endpoint.

### Endpoint details

| Property | Value |
|---|---|
| HTTP method | GET |
| Path | `/` |
| Function | `root()` |
| Response format | JSON |

### Response

```json
{
    "message": "Nevark AI Backend Running",
    "status": "online"
}
```

The endpoint provides a simple response indicating that the root route is responding.

It does not perform database checks, LLM connectivity checks, or external service health verification.

## 8. Startup Event

```python
@app.on_event("startup")
async def startup_event():

    logger.info(
        "🚀 Nevark AI Backend Started"
    )
```

The startup event defines an asynchronous function that logs a message when the FastAPI application starts.

### Operation

1. The application startup lifecycle reaches the registered event.
2. `startup_event()` executes.
3. The shared application logger records an INFO-level message.

Log message:

`🚀 Nevark AI Backend Started`

The logger writes to the configured destinations:

- `logs/nevark.log`
- Terminal output

This provides a record of application startup.

## 9. Shutdown Event

```python
@app.on_event("shutdown")
async def shutdown_event():

    logger.info(
        "🛑 Nevark AI Backend Stopped"
    )
```

The shutdown event defines an asynchronous function that logs a message when the FastAPI application shuts down.

### Operation

1. The application enters its shutdown lifecycle.
2. `shutdown_event()` executes.
3. The shared logger records an INFO-level message.

Log message:

`🛑 Nevark AI Backend Stopped`

This provides a record of application shutdown.

The supplied implementation does not perform additional resource cleanup or connection management in this event.

## 10. Complete Application Initialization Flow

The overall initialization sequence in the supplied source is:

```text
             app/main.py
                  |
                  v
       Import Backend Components
                  |
                  v
       Create Database Tables
       Base.metadata.create_all()
                  |
                  v
        Initialize FastAPI App
                  |
                  v
           Configure CORS
                  |
                  v
        Register Central Router
                  |
                  v
           Define Root Route
                  |
                  v
        Register Startup Event
                  |
                  v
        Register Shutdown Event
                  |
                  v
         Application Ready
```

The database table-creation operation appears before the FastAPI application instance is created in this module.

## 11. Backend Architecture Integration

The main application connects the backend's major architectural layers.

```text
                  main.py
                     |
          +----------+----------+
          |          |          |
          v          v          v
       API Layer  Database   Logger
          |          |          |
          v          v          v
      api_router   SQLAlchemy  logger
          |
    +-----+-----+
    |     |     |
    v     v     v
   Chat  Voice WebSocket
    |     |     |
    +-----+-----+
          |
          v
     Service Layer
          |
          v
       Core AI
          |
     +----+----+
     |         |
     v         v
    Groq   Memory/RAG
     |
     v
   Response
```

The diagram illustrates the broader backend relationships established by the modules documented so far. The specific execution flow for each request is implemented in the respective route and service modules.

## 12. Current Implementation Scope

The module currently provides:

- SQLAlchemy table initialization.
- FastAPI application creation.
- Application title and version configuration.
- CORS middleware registration.
- Local frontend origin allowlisting.
- Central API router registration.
- Root endpoint.
- Startup logging.
- Shutdown logging.

The module does not currently implement:

- Authentication middleware.
- Authorization middleware.
- Rate limiting.
- Custom exception handlers.
- Application-wide request validation.
- Database migration management.
- External dependency health checks.
- Background task initialization.
- Explicit resource cleanup during shutdown.
- Production-specific CORS configuration.

These responsibilities are not defined in the supplied source.

## 13. Important Implementation Considerations

### 13.1 Database initialization

`Base.metadata.create_all(bind=engine)` runs when the module is imported.

This means database table initialization occurs during application module loading rather than inside the startup event.

### 13.2 CORS restrictions

Only the two configured local origins are explicitly allowed.

A deployed frontend hosted on another domain would require an appropriate origin to be added.

### 13.3 Deprecated lifecycle event style

The implementation uses `@app.on_event("startup")` and `@app.on_event("shutdown")`.

These decorators are the lifecycle mechanism used in the supplied source. FastAPI also provides the lifespan mechanism for managing application startup and shutdown in newer application designs.

### 13.4 Root endpoint limitations

The root endpoint returns a static online response.

It should not be interpreted as confirmation that Groq, ElevenLabs, SQLite, ChromaDB, or other dependencies are operational.

### 13.5 API router organization

The application imports a single `api_router` rather than registering each endpoint module individually.

This keeps the main application entry point separate from the organization of individual API routes.

## 14. Summary

The `main.py` module is the primary initialization point for the Nevark AI Backend.

It creates the database tables using SQLAlchemy metadata, initializes the FastAPI application, configures CORS for local frontend development, and registers the centralized API router.

It also exposes a root endpoint and records application startup and shutdown events through the shared logging system.

By bringing together routing, database initialization, middleware, and lifecycle logging, this module establishes the runtime foundation for the Nevark AI Backend.