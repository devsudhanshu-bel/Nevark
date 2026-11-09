# Database Schemas

## 1. Overview

The `schemas.py` module defines the Pydantic data schemas used by the Nevark AI backend for conversation data validation and response serialization.

It contains three schemas:

- `ConversationBase` – Defines the common conversation fields.
- `ConversationCreate` – Represents the data required to create a conversation record.
- `ConversationResponse` – Defines the structure of conversation data returned with its database identifier and timestamp.

These schemas separate the structure of application data from the SQLAlchemy database model.

## 2. Dependencies

```python
from pydantic import BaseModel
from datetime import datetime
```

| Dependency | Purpose |
|---|---|
| `BaseModel` | Provides Pydantic's data validation and serialization functionality |
| `datetime` | Defines the timestamp field's data type |

## 3. ConversationBase Schema

```python
class ConversationBase(BaseModel):

    user_message: str

    ai_response: str
```

`ConversationBase` is the parent schema containing the common fields shared by conversation-related schemas.

### Fields

| Field | Type | Description |
|---|---|---|
| `user_message` | `str` | Stores the user's message |
| `ai_response` | `str` | Stores the AI-generated response |

Both fields are required because no default values are defined.

This schema provides a reusable foundation for other conversation schemas.

## 4. ConversationCreate Schema

```python
class ConversationCreate(ConversationBase):

    pass
```

`ConversationCreate` inherits from `ConversationBase`.

It does not introduce any additional fields or validation rules.

The `pass` statement indicates that the class currently uses the parent's implementation without extending it.

### Inherited fields

| Field | Type | Required |
|---|---|---|
| `user_message` | `str` | Yes |
| `ai_response` | `str` | Yes |

### Purpose

This schema represents the conversation data required when creating a new conversation record.

It excludes database-generated fields such as `id` and `timestamp`.

This keeps the creation input separate from the complete conversation record.

## 5. ConversationResponse Schema

```python
class ConversationResponse(ConversationBase):

    id: int

    timestamp: datetime

    class Config:

        from_attributes = True
```

`ConversationResponse` extends `ConversationBase` and adds two additional fields.

### Fields

| Field | Type | Description |
|---|---|---|
| `user_message` | `str` | Original user message inherited from the base schema |
| `ai_response` | `str` | AI response inherited from the base schema |
| `id` | `int` | Database record identifier |
| `timestamp` | `datetime` | Timestamp associated with the conversation |

The resulting response schema represents a complete conversation record.

### Configuration: `from_attributes`

```python
class Config:
    from_attributes = True
```

This configuration enables Pydantic to construct the response model using object attributes rather than requiring a dictionary.

This is useful when working with SQLAlchemy ORM objects.

For example, a SQLAlchemy `Conversation` object exposes attributes such as:

- `conversation.id`
- `conversation.user_message`
- `conversation.ai_response`
- `conversation.timestamp`

Pydantic can read these attributes when constructing a `ConversationResponse`.

This configuration is commonly used with Pydantic v2.

## 6. Schema Inheritance Structure

The three schemas use inheritance to avoid repeating common conversation fields.

```text
ConversationBase
       |
       |
       +----------------------+
       |                      |
       v                      v
ConversationCreate     ConversationResponse
                              |
                              +-- id: int
                              |
                              +-- timestamp: datetime
```

### Schema comparison

| Feature | ConversationBase | ConversationCreate | ConversationResponse |
|---|---|---|---|
| User message | Yes | Inherited | Inherited |
| AI response | Yes | Inherited | Inherited |
| Database ID | No | No | Yes |
| Timestamp | No | No | Yes |
| ORM attribute support | Not configured | Not configured | Enabled |

## 7. Example Data Structures

### 7.1 Conversation creation input

An illustrative creation payload:

```json
{
    "user_message": "Hello Nevark!",
    "ai_response": "Hey! How can I help you?"
}
```

This structure contains the two fields inherited by `ConversationCreate`.

### 7.2 Conversation response

An illustrative response:

```json
{
    "id": 1,
    "user_message": "Hello Nevark!",
    "ai_response": "Hey! How can I help you?",
    "timestamp": "2026-11-09T10:30:00"
}
```

The response includes the database identifier and timestamp in addition to the conversation messages.

These examples illustrate the schema structures; actual values depend on the database record.

## 8. Relationship with SQLAlchemy Models

The schemas correspond to the ORM model defined in:

`app/database/models.py`

The SQLAlchemy `Conversation` model defines the database table, while the Pydantic schemas define how conversation data is represented and validated at the application level.

| SQLAlchemy Model | Pydantic Schema |
|---|---|
| `Conversation.id` | `ConversationResponse.id` |
| `Conversation.user_message` | `ConversationBase.user_message` |
| `Conversation.ai_response` | `ConversationBase.ai_response` |
| `Conversation.timestamp` | `ConversationResponse.timestamp` |

### Key distinction

**SQLAlchemy Model:**
- Defines database table structure.
- Maps Python attributes to database columns.
- Handles ORM-level database representation.

**Pydantic Schema:**
- Defines application data structures.
- Validates incoming data.
- Controls the fields represented in response models.
- Supports serialization of ORM objects through `from_attributes`.

## 9. Current Implementation Scope

The module currently provides:

- Reusable conversation base schema.
- Conversation creation schema.
- Conversation response schema.
- String validation for conversation messages.
- Integer typing for database identifiers.
- Datetime typing for timestamps.
- Schema inheritance.
- ORM attribute-based response construction.

The module does not currently implement:

- Custom field validators.
- Message-length restrictions.
- User identification fields.
- Conversation session identifiers.
- Optional message fields.
- Custom serialization methods.
- Additional business-level validation.
- Database insertion or retrieval operations.

These responsibilities are not defined in the supplied source.

## 10. Summary

The `schemas.py` module provides the Pydantic data structures for conversation handling in Nevark AI.

It uses inheritance to define shared conversation fields through `ConversationBase`, reuses those fields for creation through `ConversationCreate`, and extends them with database metadata through `ConversationResponse`.

Together with `database.py` and `models.py`, it completes the basic database structure:

- `database.py` manages database connectivity and sessions.
- `models.py` defines the SQLAlchemy conversation table.
- `schemas.py` defines the validated application-level representation of conversation data.