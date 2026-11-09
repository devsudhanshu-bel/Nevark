# WebSocket Chat Route

## 1. Overview

The `websocket.py` module implements a basic WebSocket endpoint for real-time, two-way communication between a client and the Nevark AI backend.

Unlike a traditional HTTP endpoint, which handles individual requests and responses, this WebSocket endpoint maintains an active connection and continuously listens for incoming messages.

The current implementation acts as a simple message echo handler. It receives text from the client and responds with a message confirming that Nevark AI received it.

## 2. Source Code

The module uses three FastAPI components:

- `APIRouter`: Registers the WebSocket route.
- `WebSocket`: Represents the active WebSocket connection.
- `WebSocketDisconnect`: Handles client disconnection events.

## 3. Route Configuration

```python
router = APIRouter()
```

Creates an API router for registering the WebSocket endpoint.

Unlike the other route modules, this router does not define a prefix or tags.

### WebSocket endpoint

| Property | Value |
|---|---|
| Protocol | WebSocket |
| Path | `/ws/chat` |
| Handler | `websocket_chat` |
| Input | Text messages |
| Output | Text messages |

The endpoint is registered using:

```python
@router.websocket("/ws/chat")
```

Clients connect to this route using the WebSocket protocol.

## 4. Connection Lifecycle

### Step 1: Accept the connection

```python
await websocket.accept()
print("✅ WebSocket Connected")
```

The backend accepts the incoming WebSocket connection.

After acceptance, the client and server can exchange messages through the established connection.

### Step 2: Listen for incoming messages

```python
while True:
    data = await websocket.receive_text()
```

The endpoint enters an infinite loop and waits for incoming text messages.

- `receive_text()` waits asynchronously for a message.
- The received message is stored in `data`.
- The loop allows the connection to handle multiple messages without requiring a new connection for each message.

### Step 3: Process the received message

```python
print("📩 Message:", data)

response = f"Nevark AI received: {data}"
```

The received message is printed in the backend terminal.

A response string is then created by adding the received message to the prefix:

`Nevark AI received:`

**Important:** This implementation does not invoke the Nevark AI agent engine, an LLM, or the chat service. It currently generates a simple confirmation response.

### Step 4: Send the response

```python
await websocket.send_text(response)
```

The generated response is sent back to the connected client as a text message.

The loop then continues waiting for the next incoming message.

### Step 5: Handle disconnection

```python
except WebSocketDisconnect:
    print("❌ WebSocket Disconnected")
```

When the client disconnects, FastAPI raises `WebSocketDisconnect`.

The exception is caught, and a disconnection message is printed in the backend terminal.

This prevents the normal client-disconnection event from appearing as an unhandled exception.

## 5. Message Flow

The current WebSocket communication follows this sequence:

1. Client connects to `/ws/chat`.
2. Backend accepts the connection.
3. Client sends a text message.
4. Backend receives and prints the message.
5. Backend constructs a confirmation response.
6. Backend sends the response to the client.
7. The connection remains active for additional messages.
8. When the client disconnects, the backend handles the disconnection.

### Example

**Client sends:**

```text
Hello Nevark!
```

**Backend receives:**

```text
Hello Nevark!
```

**Backend responds:**

```text
Nevark AI received: Hello Nevark!
```

## 6. Integration with the API Router

The WebSocket router is imported and registered in:

`app/api/router.py`

```python
from app.api.routes.websocket import router as websocket_router

api_router.include_router(websocket_router)
```

This makes the WebSocket endpoint available through the application's main API router.

The final connection URL depends on the host, port, and any application-level route prefix configured by the main FastAPI application.

For a local server running on port `8000` without an additional prefix, the connection URL is:

```text
ws://localhost:8000/ws/chat
```

## 7. Current Implementation Scope

The current implementation provides:

- WebSocket connection acceptance.
- Persistent connection handling through a message loop.
- Asynchronous text-message reception.
- Text-message responses.
- Basic terminal logging.
- Client-disconnection handling.

The following functionality is not implemented in this module:

- Integration with the Nevark AI agent engine.
- LLM-based response generation.
- Conversation memory or message persistence.
- User authentication or authorization.
- Structured JSON message handling.
- Streaming AI responses.
- Explicit handling of other WebSocket errors.

These capabilities would require additional implementation or delegation to other backend services.

## 8. Summary

The `websocket.py` module provides the real-time communication entry point for Nevark AI.

It maintains a WebSocket connection, receives client messages, and sends confirmation responses. At its current stage, it functions as a basic echo-style communication endpoint rather than a complete AI conversation handler.

Its primary purpose is to establish and manage the WebSocket communication layer that can later be connected to the Nevark AI conversation-processing pipeline.