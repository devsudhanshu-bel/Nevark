# WebSocket Service

## 1. Overview

The `websocket_service.py` module implements connection management for WebSocket communication in Nevark AI.

It defines a `ConnectionManager` class that maintains a collection of active WebSocket connections and provides methods for managing communication with connected clients.

The module supports four primary operations:

- `connect()` – Accepts a WebSocket connection and registers it.
- `disconnect()` – Removes a WebSocket connection from the active connection list.
- `send_message()` – Sends a text message to a specific connected client.
- `broadcast()` – Sends a text message to every connection currently registered.

A module-level `manager` instance provides a shared connection manager for other backend components.

## 2. Dependencies

```python
from fastapi import WebSocket
```

| Dependency | Purpose |
|---|---|
| `WebSocket` | Provides the FastAPI WebSocket connection interface |

The module uses FastAPI's WebSocket object to accept connections and exchange text messages.

## 3. ConnectionManager Class

```python
class ConnectionManager:

    def __init__(self):

        self.active_connections = []
```

The `ConnectionManager` class centralizes the management of active WebSocket connections.

It maintains an instance variable:

`active_connections`

This is a Python list containing the WebSocket objects registered through the manager.

Each registered connection represents a client that has successfully connected through the manager's `connect()` method.

### Initial state

When a new `ConnectionManager` object is created:

```python
self.active_connections = []
```

The connection list starts empty.

As clients connect, their WebSocket objects are appended to this list.

## 4. Function: `connect()`

```python
async def connect(self, websocket: WebSocket):

    await websocket.accept()

    self.active_connections.append(websocket)
```

The `connect()` method accepts an incoming WebSocket connection and registers it with the connection manager.

### Processing steps

**Step 1: Accept the connection**

```python
await websocket.accept()
```

FastAPI accepts the incoming WebSocket connection.

This completes the WebSocket handshake and allows communication to begin.

**Step 2: Register the connection**

```python
self.active_connections.append(websocket)
```

After accepting the connection, the WebSocket object is added to `active_connections`.

The manager can now use this connection for direct messaging or broadcasting.

### Result

The connection becomes part of the manager's active connection list.

## 5. Function: `disconnect()`

```python
def disconnect(self, websocket: WebSocket):

    self.active_connections.remove(websocket)
```

The `disconnect()` method removes a WebSocket object from the active connection list.

### Processing steps

1. Receives the WebSocket object to disconnect.
2. Searches for that object in `active_connections`.
3. Removes the matching object from the list.

This prevents a disconnected client from remaining registered after the method is successfully called.

**Important:** The method uses `list.remove()`. If the supplied WebSocket object is not present in the list, Python raises a `ValueError`. The method does not currently handle this exception.

## 6. Function: `send_message()`

```python
async def send_message(
    self,
    message: str,
    websocket: WebSocket
):

    await websocket.send_text(message)
```

The `send_message()` method sends a text message to one specific WebSocket connection.

### Parameters

| Parameter | Type | Description |
|---|---|---|
| `message` | `str` | Text message to send |
| `websocket` | `WebSocket` | Target WebSocket connection |

### Processing

```python
await websocket.send_text(message)
```

The supplied message is sent through the specified WebSocket connection.

Unlike broadcasting, this method targets only the WebSocket object passed to it.

### Example usage

```python
await manager.send_message(
    "Hello from Nevark AI!",
    websocket
)
```

This sends the message to the specified client.

The example illustrates how another backend component could use the shared manager.

## 7. Function: `broadcast()`

```python
async def broadcast(self, message: str):

    for connection in self.active_connections:

        await connection.send_text(message)
```

The `broadcast()` method sends the same text message to every connection currently registered in `active_connections`.

### Processing steps

**Step 1: Iterate through active connections**

```python
for connection in self.active_connections:
```

The method iterates through the connection list.

Each registered WebSocket object is accessed one at a time.

**Step 2: Send the message**

```python
await connection.send_text(message)
```

The supplied message is sent to the current connection.

The operation is awaited before the loop moves to the next connection.

### Example usage

```python
await manager.broadcast(
    "Nevark AI is now online!"
)
```

Every connection registered with the manager receives the message, provided each send operation succeeds.

### Important behavior

The broadcast implementation sends messages sequentially rather than concurrently.

It also does not currently handle individual connection failures. If sending to one connection raises an exception, the broadcast operation can stop before reaching the remaining connections.

## 8. Shared Connection Manager Instance

```python
manager = ConnectionManager()
```

The module creates a single `ConnectionManager` instance named `manager`.

Other backend modules can import this instance instead of creating separate connection managers.

For example:

```python
from app.services.websocket_service import manager
```

This allows different components importing the same module instance to access the shared active connection list.

The shared manager provides a centralized location for WebSocket connection registration and messaging.

## 9. Complete Connection Lifecycle

The intended connection lifecycle is:

```text
          CLIENT CONNECTS
                 |
                 v
          connect(websocket)
                 |
                 v
          Accept WebSocket
                 |
                 v
       Register Active Connection
                 |
                 v
          ACTIVE CONNECTION
                 |
          +------+------+
          |             |
          v             v
     send_message()  broadcast()
          |             |
          v             v
      One Client    All Registered
                     Connections
                 |
                 v
        disconnect(websocket)
                 |
                 v
       Remove Active Connection
```

This represents the operations exposed by the `ConnectionManager` class. The class itself does not implement a complete receive-message loop.

## 10. Relationship with the WebSocket API Route

The WebSocket route is defined in:

`app/api/routes/websocket.py`

The supplied route implementation:

1. Accepts an incoming WebSocket connection.
2. Receives text messages in a loop.
3. Prints received messages.
4. Creates a simple acknowledgement response.
5. Sends the response back to the connected client.
6. Handles `WebSocketDisconnect`.

The route currently implements its own connection handling directly.

It does not import or use the shared `ConnectionManager` instance from this service.

Therefore, the existence of `websocket_service.py` does not mean that the current WebSocket route automatically uses centralized connection registration or broadcasting.

The service provides reusable connection-management functionality that can be integrated into the route separately.

## 11. Current Implementation Scope

The module currently provides:

- Centralized WebSocket connection management.
- Active connection storage using a Python list.
- WebSocket connection acceptance.
- Connection registration.
- Connection removal.
- Direct text messaging.
- Message broadcasting.
- A shared manager instance.

The module does not currently implement:

- Client authentication.
- User-specific connection tracking.
- Connection identifiers.
- Room or channel management.
- Message history.
- JSON message serialization.
- Automatic disconnection detection.
- Automatic removal of failed connections.
- Concurrent broadcast execution.
- Connection synchronization or locking.
- Reconnection management.
- Persistent connection storage.

## 12. Important Implementation Considerations

### 12.1 In-memory connection storage

Active connections are stored in a Python list.

This means the connection registry exists only within the running application process.

It is not shared automatically between multiple application workers or separate server instances.

### 12.2 Disconnected connection handling

The `disconnect()` method removes a connection only when it is explicitly called.

The class does not independently monitor connection status or remove disconnected clients automatically.

### 12.3 Broadcast failure handling

The broadcast loop does not contain an individual exception handler for each connection.

A failed send can interrupt the remaining broadcast operations.

### 12.4 Sequential broadcasting

Each message is awaited before the next connection is processed.

Consequently, broadcast duration can increase as the number of active connections grows.

### 12.5 No connection locking

The active connection list is modified directly.

The implementation does not include synchronization mechanisms for coordinating simultaneous connection changes and broadcasts.

## 13. Summary

The `websocket_service.py` module provides a reusable connection-management layer for WebSocket communication in Nevark AI.

Its `ConnectionManager` class maintains active WebSocket connections and exposes methods for accepting connections, removing connections, sending individual messages, and broadcasting messages.

A shared module-level `manager` instance allows backend components to reuse the same connection registry.

Although the service provides centralized connection-management functionality, the currently supplied WebSocket route implements its own connection handling and does not yet use this manager.