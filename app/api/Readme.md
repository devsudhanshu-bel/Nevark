# API Router

## 1. Overview

The API Router acts as the central routing aggregator for the Nevark Backend.

Instead of defining every API endpoint inside a single file, the backend separates endpoints into individual route modules based on their functionality.

This file imports the routers from those modules and registers them with a single FastAPI `APIRouter` instance named `api_router`.

This approach keeps the API architecture modular and makes it easier to maintain and extend.

## 2. Source File Details

| Property | Description |
|---|---|
| Module | API Router |
| File | `app/api/router.py` |
| Framework | FastAPI |
| Main component | `APIRouter` |
| Main object | `api_router` |
| Responsibility | Aggregate individual API route modules |

## 3. Import Dependencies

The module imports `APIRouter` from FastAPI:

```python
from fastapi import APIRouter
```

It then imports six individual route modules:

| Router | Source module | Responsibility indicated by module |
|---|---|---|
| `chat_router` | `app.api.routes.chat` | Chat endpoints |
| `health_router` | `app.api.routes.health` | Health endpoints |
| `memory_router` | `app.api.routes.memory` | Memory endpoints |
| `speech_router` | `app.api.routes.speech` | Speech endpoints |
| `websocket_router` | `app.api.routes.websocket` | WebSocket endpoints |
| `voice_router` | `app.api.routes.voice` | Voice endpoints |

Each router is imported from its corresponding module using an alias.

For example:

```python
from app.api.routes.chat import router as chat_router
```

The alias makes the purpose of each imported router clear within the aggregator.

## 4. Central Router Initialization

The module creates the central API router:

```python
api_router = APIRouter()
```

This object serves as the common container for the individual route modules.

The imported routers are registered with this instance.

## 5. Registering Individual Routers

The module uses FastAPI's `include_router()` method to register each route module:

```python
api_router.include_router(chat_router)
api_router.include_router(health_router)
api_router.include_router(memory_router)
api_router.include_router(speech_router)
api_router.include_router(websocket_router)
api_router.include_router(voice_router)
```

### Registered Router Sequence

The routers are included in the following order:

1. Chat
2. Health
3. Memory
4. Speech
5. WebSocket
6. Voice

Each included router contributes its registered routes to the central `api_router`.

This allows the main FastAPI application to mount the combined router instead of importing every individual route module separately.

## 6. API Routing Architecture

The routing structure can be represented as:

```text
app/
└── api/
    ├── router.py
    │
    └── routes/
        ├── chat.py
        ├── health.py
        ├── memory.py
        ├── speech.py
        ├── voice.py
        └── websocket.py
```

### Logical Routing Flow

```text
                 FastAPI Application
                         |
                         v
                    api_router
                         |
       +-----------------+-----------------+
       |        |        |        |        |
       v        v        v        v        v
      Chat    Health   Memory   Speech  WebSocket
                                     
                         |
                         v
                       Voice
```

All six route modules are registered with the same central router.

## 7. Integration with the Main Application

The intended integration pattern is to import `api_router` into the FastAPI application and register it using `include_router()`.

For example:

```python
from fastapi import FastAPI
from app.api.router import api_router

app = FastAPI()

app.include_router(api_router)
```

This example illustrates the integration pattern; the exact mounting configuration must be confirmed from `app/main.py`.

The main application may also configure a shared API prefix or other router-level settings.

## 8. Important Implementation Notes

- This file does not define individual API endpoint functions.
- Endpoint implementation belongs to the respective route modules.
- No API prefix is specified in this file.
- No tags, dependencies, or response configuration are supplied to `include_router()` here.
- The module does not implement authentication, request validation, or business logic itself.
- WebSocket routing is included alongside the HTTP-related route modules through the same aggregation mechanism.

## 9. Extending the API

To add a new route module:

1. Create a new Python file inside `app/api/routes/`.
2. Define an `APIRouter` instance in that file.
3. Implement the required endpoints.
4. Import its router into `app/api/router.py`.
5. Register it using `api_router.include_router()`.

For example, a future notification route could be registered as:

```python
from app.api.routes.notifications import (
    router as notifications_router
)

api_router.include_router(
    notifications_router
)
```

This allows new API functionality to be introduced without placing all endpoint implementations inside the central router.

## 10. Conclusion

The API Router provides a centralized entry point for the Nevark Backend's route modules.

By separating chat, health, memory, speech, WebSocket, and voice endpoints into independent modules, the backend maintains a modular routing structure.

Its primary responsibility is to aggregate these routers so that the main FastAPI application can expose them through a single API router.