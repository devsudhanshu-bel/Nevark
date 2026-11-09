# Memory Service

## 1. Overview

The `memory_service.py` module implements the database-backed conversation-history retrieval layer for Nevark AI.

It retrieves recent conversation records from the SQLite database using SQLAlchemy and converts them into a role-based message structure that can be supplied to the LLM engine.

The module exposes two primary functions:

- `fetch_recent_conversations()` – Retrieves the most recent conversation records from the database.
- `build_conversation_history()` – Converts the retrieved records into alternating user and assistant messages.

This module provides the short-term conversation context used by the chat service when generating AI responses.

## 2. Dependencies

```python
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.database.models import Conversation
```

| Dependency | Purpose |
|---|---|
| `Session` | Provides SQLAlchemy session typing |
| `SessionLocal` | Creates database sessions |
| `Conversation` | Represents the conversation table and its ORM records |

The module uses the existing database configuration rather than creating a separate database connection.

## 3. Function: `fetch_recent_conversations()`

```python
def fetch_recent_conversations(
    limit: int = 10
):
```

This function retrieves the most recent conversation records from the SQLite database.

### Input parameter

| Parameter | Type | Default | Description |
|---|---|---|---|
| `limit` | `int` | `10` | Maximum number of conversation records to retrieve |

### Step 1: Create a database session

```python
db: Session = SessionLocal()
```

A new SQLAlchemy session is created using the shared session factory defined in:

`app/database/database.py`

This session is used to query the `conversations` table.

### Step 2: Query conversation records

```python
conversations = (
    db.query(Conversation)
    .order_by(
        Conversation.id.desc()
    )
    .limit(limit)
    .all()
)
```

The function constructs a SQLAlchemy query against the `Conversation` model.

The query performs three operations:

**A. Retrieve conversation records**

```python
db.query(Conversation)
```

Selects records from the `Conversation` table.

**B. Sort by descending ID**

```python
.order_by(
    Conversation.id.desc()
)
```

Sorts the records by their primary key in descending order.

This places records with higher IDs before records with lower IDs.

**C. Apply the retrieval limit**

```python
.limit(limit)
```

Restricts the number of records returned according to the supplied limit.

**D. Execute the query**

```python
.all()
```

Executes the query and returns the matching ORM objects as a Python list.

### Step 3: Close the database session

```python
db.close()
```

After retrieving the records, the database session is closed.

### Step 4: Return the conversations

```python
return conversations
```

The retrieved conversation objects are returned to the calling function.

### Error handling

```python
except Exception as e:

    print(
        "❌ MEMORY SERVICE ERROR:",
        e
    )

    return []
```

If an exception occurs during session creation or database querying, the error is printed and an empty list is returned.

**Implementation consideration:** The session is closed explicitly after a successful query. If an exception occurs before `db.close()` executes, this function does not guarantee session cleanup.

## 4. Function: `build_conversation_history()`

```python
def build_conversation_history(
    limit: int = 10
):
```

This function transforms database conversation records into a message structure compatible with the LLM chat-completion interface.

It retrieves recent conversations using `fetch_recent_conversations()` and converts each record into two messages:

- A user message.
- An assistant response.

### Step 1: Fetch recent conversations

```python
conversations = fetch_recent_conversations(
    limit
)
```

The function calls `fetch_recent_conversations()` with the supplied limit.

By default, it retrieves the latest ten conversation records.

### Step 2: Initialize conversation history

```python
history = []
```

An empty list is created to store the formatted conversation messages.

### Step 3: Restore chronological order

```python
for convo in reversed(conversations):
```

The database query retrieves conversations in descending ID order.

For example:

```text
Database query result:

Conversation 10
Conversation 9
Conversation 8
```

Using `reversed()` changes the iteration order to:

```text
Conversation 8
Conversation 9
Conversation 10
```

This restores chronological order among the retrieved records.

The oldest selected conversation is processed first, followed by the newest.

### Step 4: Append the user message

```python
history.append({
    "role": "user",
    "content": convo.user_message
})
```

The user's original message is converted into a dictionary containing:

- `role`: `"user"`
- `content`: The stored user message.

### Step 5: Append the assistant response

```python
history.append({
    "role": "assistant",
    "content": convo.ai_response
})
```

The corresponding AI response is converted into another dictionary containing:

- `role`: `"assistant"`
- `content`: The stored AI response.

Both messages are appended consecutively.

### Step 6: Return formatted history

```python
return history
```

The completed message list is returned to the calling component.

For ten conversation records, the function produces twenty message dictionaries.

## 5. Example Transformation

Assume the database contains these three conversation records:

| ID | User message | AI response |
|---:|---|---|
| 1 | Hello Nevark | Hello! How can I help? |
| 2 | What is Python? | Python is a programming language. |
| 3 | Explain APIs | APIs allow software systems to communicate. |

The database query initially retrieves:

```text
ID 3
ID 2
ID 1
```

After applying `reversed()`, the service processes:

```text
ID 1
ID 2
ID 3
```

The resulting conversation history is:

```python
[
    {
        "role": "user",
        "content": "Hello Nevark"
    },
    {
        "role": "assistant",
        "content": "Hello! How can I help?"
    },
    {
        "role": "user",
        "content": "What is Python?"
    },
    {
        "role": "assistant",
        "content": "Python is a programming language."
    },
    {
        "role": "user",
        "content": "Explain APIs"
    },
    {
        "role": "assistant",
        "content": "APIs allow software systems to communicate."
    }
]
```

This preserves the chronological order of the selected conversation exchanges.

## 6. Integration with Chat Service

The memory service is imported by:

`app/services/chat_service.py`

```python
from app.services.memory_service import (
    build_conversation_history
)
```

The chat service calls:

```python
conversation_history = build_conversation_history(
    limit=10
)
```

The returned history is passed to the LLM engine:

```python
ai_response = ask_llm(
    user_input=enhanced_prompt,
    conversation_history=conversation_history
)
```

The LLM engine then combines:

1. System prompt.
2. Retrieved conversation history.
3. Current user message.

This allows the language model to receive recent conversation context when generating its response.

## 7. Short-Term Memory Architecture

The service implements a database-backed approach to retrieving recent conversational context.

Its processing sequence is:

1. Query the `conversations` table.
2. Sort records by descending ID.
3. Retrieve the requested number of records.
4. Reverse the result to restore chronological order.
5. Extract the user message from each record.
6. Extract the corresponding assistant response.
7. Construct role-based message dictionaries.
8. Return the formatted conversation history.

## 8. Relationship with Other Memory Components

Nevark currently has multiple memory mechanisms.

| Component | Storage | Main responsibility |
|---|---|---|
| `memory_service.py` | SQLite | Retrieves recent conversation history |
| `memory_engine.py` | JSON | Saves and loads conversation exchanges |
| `rag_engine.py` | ChromaDB | Stores and retrieves text using vector similarity |

Their roles are different:

- `memory_service.py` retrieves recent conversation records and prepares LLM context.
- `memory_engine.py` maintains JSON-based conversation persistence.
- `rag_engine.py` provides semantic retrieval from vector-stored documents.

The chat service coordinates these components.

## 9. Current Implementation Scope

The module currently provides:

- SQLAlchemy-based conversation retrieval.
- Configurable retrieval limits.
- Descending database-ID ordering.
- Chronological restoration using `reversed()`.
- Extraction of user and assistant messages.
- Role-based message formatting.
- Database-session closure after successful retrieval.
- Basic exception handling.

The module does not currently implement:

- User-specific conversation filtering.
- Conversation-session filtering.
- Semantic memory retrieval.
- Conversation summarization.
- Token-based context management.
- Automatic history expiration.
- Pagination.
- Explicit database-session cleanup through a `finally` block.

## 10. Important Implementation Considerations

### 10.1 Retrieval is based on database ID

The query uses `Conversation.id.desc()` rather than explicitly sorting by timestamp.

Therefore, the chronological ordering assumes that higher conversation IDs correspond to later inserted records.

### 10.2 Limit applies to exchanges

The `limit` parameter controls the number of database records retrieved, not the number of individual messages.

Each record produces two messages in the returned history.

### 10.3 No user-level isolation

The query retrieves recent records from the entire `Conversation` table.

There is no user ID or session filter in the supplied implementation.

### 10.4 No token-budget management

The service limits history by record count rather than by token count.

The returned messages are not summarized or truncated based on the LLM's context window.

### 10.5 Synchronous database access

Both functions are synchronous and use standard SQLAlchemy session operations.

They are not implemented using asynchronous database sessions.

## 11. Summary

The `memory_service.py` module provides the short-term conversation-history retrieval layer for Nevark AI.

It fetches recent conversation records from SQLite, restores their chronological order, and converts them into alternating user and assistant messages.

The resulting history is supplied to the LLM engine through the chat service, allowing Nevark to generate responses with access to recent conversational context.

Together with the JSON and ChromaDB memory components, this module completes the database-backed short-term conversation retrieval mechanism.