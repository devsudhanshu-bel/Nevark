# Chat Service

## 1. Overview

The `chat_service.py` module implements the central chat-processing workflow for Nevark AI.

It acts as the orchestration layer between the user's message and the different backend components responsible for understanding, processing, generating, and storing a response.

The module integrates:

- Command detection through `command_parser.py`.
- Conversation-history retrieval through `memory_service.py`.
- Semantic memory retrieval through `rag_engine.py`.
- AI response generation through `llm_engine.py`.
- JSON-based conversation storage through `memory_engine.py`.
- Vector-based memory storage through ChromaDB.
- Relational conversation persistence through SQLAlchemy.

The main function, `process_chat()`, coordinates these components and returns the generated response.

## 2. Dependencies

```python
from sqlalchemy.orm import Session

from app.core.llm_engine import ask_llm
from app.core.command_parser import detect_command

from app.core.memory_engine import save_memory

from app.core.rag_engine import (
    retrieve_relevant_memories,
    save_memory_to_vector_db
)

from app.services.memory_service import (
    build_conversation_history
)

from app.database.database import SessionLocal
from app.database.models import Conversation
```

| Dependency | Responsibility |
|---|---|
| `Session` | Provides SQLAlchemy session typing |
| `ask_llm()` | Generates AI responses through Groq |
| `detect_command()` | Identifies predefined user commands |
| `save_memory()` | Saves conversations to JSON memory |
| `retrieve_relevant_memories()` | Retrieves semantically relevant stored documents |
| `save_memory_to_vector_db()` | Stores text in ChromaDB |
| `build_conversation_history()` | Constructs recent conversation history |
| `SessionLocal` | Creates SQLAlchemy database sessions |
| `Conversation` | Represents the conversation database model |

The service coordinates these dependencies rather than implementing their internal functionality itself.

## 3. Core Function: `process_chat()`

```python
async def process_chat(
    user_input: str
):
```

This asynchronous function is the main entry point for processing chat messages.

### Input

| Parameter | Type | Description |
|---|---|---|
| `user_input` | `str` | Message submitted by the user |

### Return value

The function returns a string containing one of the following:

- A predefined response for a recognized command.
- An AI-generated response.
- A fallback error message if an exception occurs.

## 4. Complete Chat Processing Pipeline

### Step 1: Command Detection

```python
command = detect_command(
    user_input
)
```

The user's input is first passed to the command parser.

The parser checks whether the message contains any predefined command keywords.

Currently, the command parser recognizes:

| Command | Keywords |
|---|---|
| `shutdown` | `shutdown`, `exit`, `quit` |
| `greeting` | `hello`, `hi`, `hey` |

The returned command determines whether the service should execute a predefined response or continue through the normal AI processing pipeline.

#### Shutdown command

```python
if command == "shutdown":
    return (
        "Shutting down Nevark AI."
    )
```

If a shutdown keyword is detected, the service immediately returns:

`Shutting down Nevark AI.`

This is a response only. The supplied implementation does not actually shut down the application or its server.

#### Greeting command

```python
if command == "greeting":
    return (
        "Hello, I am Nevark AI. "
        "How can I help you today?"
    )
```

If a greeting keyword is detected, the service immediately returns a predefined greeting.

Neither of these command branches proceeds to conversation-history retrieval, LLM generation, or memory persistence.

### Step 2: Short-Term Memory Retrieval

```python
conversation_history = (
    build_conversation_history(
        limit=10
    )
)
```

If the message does not match a predefined command, the service retrieves recent conversation history.

It calls `build_conversation_history()` from:

`app/services/memory_service.py`

The function is supplied with:

`limit=10`

This requests conversation history using a limit of ten.

The resulting history is stored in `conversation_history` and later supplied to the LLM.

The exact retrieval and formatting implementation is defined in `memory_service.py`.

### Step 3: Memory Detection

```python
memory_keywords = [
    "my",
    "mine",
    "remember",
    "favorite",
    "laptop",
    "dog",
    "name",
    "project",
    "phone",
    "who am i",
    "what do i",
    "which",
    "owned",
    "own"
]
```

The service defines a predefined list of keywords associated with user-related information and memory queries.

These keywords are used to determine whether semantic memory retrieval should be performed.

The list includes:

- Personal references such as `my` and `mine`.
- Memory-related terms such as `remember` and `favorite`.
- Entity references such as `laptop`, `dog`, `name`, `project`, and `phone`.
- Question patterns such as `who am i` and `what do i`.
- Ownership-related terms such as `owned` and `own`.

#### Determine whether RAG should be used

```python
use_rag = any(
    keyword in user_input.lower()
    for keyword in memory_keywords
)
```

The input is converted to lowercase before checking the keyword list.

The `any()` function returns `True` when at least one keyword appears as a substring in the user's input.

For example:

| User input | RAG activation |
|---|---|
| `What is my laptop?` | Yes |
| `Remember my project` | Yes |
| `Who am I?` | Yes |
| `Explain artificial intelligence` | No |

This is a rule-based memory-detection mechanism rather than an AI-based intent classifier.

**Important:** The implementation uses substring matching, not complete-word matching. Therefore, a keyword can also match inside a larger word.

### Step 4: Retrieve Relevant Memories

```python
relevant_memories = []

if use_rag:

    relevant_memories = (
        retrieve_relevant_memories(
            user_input
        )
    )
```

The service initializes an empty list for relevant memories.

If `use_rag` evaluates to `True`, the user's input is passed to `retrieve_relevant_memories()`.

This function is implemented in:

`app/core/rag_engine.py`

The RAG engine:

1. Converts the query into an embedding.
2. Queries the ChromaDB collection.
3. Retrieves relevant stored documents.
4. Returns the matching document strings.

The retrieved documents are assigned to `relevant_memories`.

If RAG is not activated, the list remains empty.

### Step 5: Construct Memory Context

```python
memory_context = ""

if relevant_memories:

    memory_context = "\n".join(
        relevant_memories
    )
```

If relevant memories are available, they are joined into a single string.

A newline character separates each retrieved document.

This produces a consolidated memory context that can be included in the LLM prompt.

If no relevant memories are found, `memory_context` remains an empty string.

### Step 6: Build the Enhanced Prompt

The service constructs the prompt differently depending on whether relevant memories were retrieved.

#### When relevant memories exist

```python
enhanced_prompt = f"""
Relevant User Memories:

{memory_context}

Current User Message:

{user_input}

Use the memories ONLY if they help answer
the user's question.

If the memories are unrelated,
ignore them completely.
"""
```

The prompt contains three main sections:

1. Relevant User Memories.
2. Current User Message.
3. Instructions for using the retrieved memories.

The instructions tell the LLM to use retrieved memories only when they help answer the current question.

If the memories are unrelated, the LLM is instructed to ignore them.

This provides additional context without requiring every retrieved memory to be used in the response.

#### When no relevant memories exist

```python
enhanced_prompt = user_input
```

If no relevant memories are available, the original user input is passed forward without additional memory context.

### Step 7: Generate the AI Response

```python
ai_response = ask_llm(
    user_input=enhanced_prompt,
    conversation_history=conversation_history
)
```

The enhanced prompt and conversation history are passed to `ask_llm()`.

The LLM engine is implemented in:

`app/core/llm_engine.py`

It performs the following operations:

1. Initializes the system message using `SYSTEM_PROMPT`.
2. Adds the supplied conversation history.
3. Appends the current user message.
4. Sends the messages to the configured Groq model.
5. Extracts the generated response.
6. Returns the cleaned response.

The generated text is stored in `ai_response`.

At this stage, the service has both the original user input and the AI-generated response.

### Step 8: Save JSON Conversation Memory

```python
save_memory(
    user_input,
    ai_response
)
```

After generating the response, the service stores the conversation exchange using `save_memory()`.

This function is implemented in:

`app/core/memory_engine.py`

It saves:

- Original user message.
- Generated AI response.
- Current timestamp.

The conversation is stored in:

`memory/conversations.json`

This provides file-based conversation persistence.

### Step 9: Save Vector Memory

```python
save_memory_to_vector_db(
    user_input
)
```

The service also stores the original user message in the ChromaDB vector database.

The function is implemented in:

`app/core/rag_engine.py`

The storage process:

1. Converts the user message into an embedding.
2. Generates a record ID.
3. Stores the embedding in ChromaDB.
4. Stores the original user message as the document.

The configured collection is:

`nevark_memory`

**Important:** This service call stores only `user_input`. It does not pass `ai_response` to the vector database.

This means the vector-memory collection receives the user's messages rather than complete user-assistant exchanges through this particular workflow.

### Step 10: Save Conversation to SQLite

The final persistence operation stores the conversation in the relational database.

#### Create a database session

```python
db: Session = SessionLocal()
```

A SQLAlchemy database session is created using the session factory defined in:

`app/database/database.py`

#### Create the conversation record

```python
conversation = Conversation(
    user_message=user_input,
    ai_response=ai_response
)
```

A new `Conversation` ORM object is created.

It contains:

| Field | Value |
|---|---|
| `user_message` | Original user input |
| `ai_response` | Generated AI response |
| `id` | Database-generated primary key |
| `timestamp` | Model-defined default timestamp |

The identifier and timestamp are supplied through the database model's configuration rather than explicitly in this service.

#### Add the record to the session

```python
db.add(conversation)
```

The conversation object is added to the SQLAlchemy session.

#### Commit the transaction

```python
db.commit()
```

The transaction is committed, persisting the conversation record to the SQLite database.

The configured database file is:

`nevark.db`

#### Close the session

```python
db.close()
```

After committing, the database session is closed.

## 5. Error Handling

The complete workflow is enclosed in a `try-except` block.

```python
except Exception as e:

    print(
        "❌ CHAT SERVICE ERROR:",
        e
    )

    return (
        "Sorry, something went "
        "wrong in the AI service."
    )
```

If an exception occurs during processing:

1. The exception is caught.
2. An error message is printed to the terminal.
3. A predefined fallback response is returned.

The fallback message is:

`Sorry, something went wrong in the AI service.`

This prevents exceptions from propagating directly to the calling route.

However, the service does not implement an explicit rollback or guaranteed cleanup for the manually created SQLAlchemy session if an exception occurs during database operations.

## 6. Complete Architecture and Data Flow

The normal chat-processing workflow connects multiple backend components.

```text
                USER MESSAGE
                      |
                      v
              process_chat()
                      |
                      v
              Command Parser
                      |
             +--------+--------+
             |                 |
          Greeting/         Normal
          Shutdown          Message
             |                 |
             v                 v
        Fixed Response   Conversation History
                               |
                               v
                       Memory Detection
                               |
                         +-----+-----+
                         |           |
                       RAG Yes     RAG No
                         |           |
                         v           |
                  ChromaDB Search   |
                         |           |
                         v           |
                  Memory Context     |
                         |           |
                         +-----+-----+
                               |
                               v
                         Prompt Building
                               |
                               v
                           Groq LLM
                               |
                               v
                         AI Response
                               |
                +--------------+--------------+
                |              |              |
                v              v              v
             JSON Memory   Vector Memory   SQLite DB
                |              |              |
                v              v              v
          conversations.json ChromaDB      nevark.db
                |              |              |
                +--------------+--------------+
                               |
                               v
                         Return Response
```

The diagram represents the normal non-command execution path. Greeting and shutdown commands return early and bypass the subsequent processing and storage operations.

## 7. Memory Architecture

The chat service coordinates three different memory mechanisms.

| Memory mechanism | Component | Stored information | Retrieval approach |
|---|---|---|---|
| Short-term conversation history | `memory_service.py` | Recent conversation context | `build_conversation_history(limit=10)` |
| JSON memory | `memory_engine.py` | User message, AI response, timestamp | Recent exchanges |
| Vector memory | `rag_engine.py` | User message and embedding | Semantic vector retrieval |
| Relational persistence | SQLAlchemy | User message and AI response | Database operations |

These mechanisms serve different purposes.

### Short-term memory

Provides recent conversation history to the LLM.

### JSON memory

Stores complete user-assistant exchanges in a local JSON file.

### Vector memory

Stores user messages as embeddings to support semantic retrieval.

### Relational database

Stores conversation exchanges as structured records in SQLite.

The service coordinates these operations but does not implement their underlying storage mechanisms itself.

## 8. Current Implementation Scope

The module currently provides:

- Centralized chat orchestration.
- Rule-based command detection.
- Predefined greeting and shutdown responses.
- Recent conversation-history retrieval.
- Keyword-based RAG activation.
- Semantic memory retrieval.
- Memory-context construction.
- Enhanced prompt generation.
- Groq-powered AI response generation.
- JSON conversation persistence.
- ChromaDB vector-memory persistence.
- SQLite conversation persistence.
- Basic exception handling and fallback responses.

## 9. Important Implementation Considerations

### 9.1 Command responses bypass persistence

Greeting and shutdown commands return immediately.

They do not pass through the normal LLM generation or memory-storage workflow.

Consequently, these responses are not saved through the three persistence operations in this service.

### 9.2 Keyword-based RAG activation

RAG activation depends on the predefined `memory_keywords` list.

Questions that require memory but do not contain one of these keywords will not trigger semantic retrieval.

Similarly, substring matching can activate RAG for unintended keyword matches.

### 9.3 Only user messages enter vector memory

The service calls:

```python
save_memory_to_vector_db(user_input)
```

The generated AI response is not included in this vector-storage operation.

### 9.4 Multiple persistence mechanisms

The service saves the same normal conversation through three different mechanisms:

- JSON file.
- ChromaDB.
- SQLite.

These operations occur sequentially rather than as one shared transaction.

If a later persistence operation fails, earlier operations may already have succeeded.

### 9.5 Database session cleanup

The database session is explicitly closed after a successful commit.

However, if an exception occurs before `db.close()` executes, this function does not guarantee that the session is closed.

A `try-finally` pattern or the existing `get_db()` dependency can provide more reliable lifecycle management.

### 9.6 Asynchronous function with synchronous operations

Although `process_chat()` is declared using `async def`, the supplied implementation calls synchronous operations, including:

- `ask_llm()`
- `retrieve_relevant_memories()`
- `save_memory_to_vector_db()`
- `save_memory()`
- SQLAlchemy session operations.

These operations are not awaited and may block the executing thread while they run.

## 10. Summary

The `chat_service.py` module serves as the central orchestration layer for Nevark AI's text-based conversation workflow.

It receives user input, checks predefined commands, retrieves conversation history, determines whether semantic memory retrieval is required, constructs an enhanced prompt, and generates a response through Groq.

After generating the response, it persists the conversation through JSON memory, ChromaDB vector storage, and SQLite.

By connecting the core AI engine, memory components, and database layer, `chat_service.py` brings together the primary components required for Nevark's conversational processing pipeline.