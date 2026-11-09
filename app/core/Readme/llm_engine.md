# LLM Engine

## 1. Overview

The `llm_engine.py` module provides the Large Language Model (LLM) integration layer for Nevark AI.

It uses the Groq API to generate responses from a configured language model. The module combines a predefined system prompt, optional conversation history, and the latest user message before submitting a chat-completion request.

The generated response is extracted, logged, and returned to the calling component.

If an exception occurs during processing, the module logs the error and returns a predefined fallback message instead of allowing the exception to propagate.

## 2. Dependencies

The module imports the following libraries and application components:

```python
import os

from groq import Groq
from dotenv import load_dotenv

from app.utils.prompts import SYSTEM_PROMPT
from app.utils.logger import logger
```

| Dependency | Purpose |
|---|---|
| `os` | Reads environment variables |
| `Groq` | Creates the Groq API client |
| `load_dotenv` | Loads environment variables from a `.env` file |
| `SYSTEM_PROMPT` | Supplies the system-level instructions for the LLM |
| `logger` | Records successful responses and errors |

The system prompt and logger are imported from the backend's utility modules rather than being defined inside this file.

## 3. Environment Configuration

```python
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

GROQ_MODEL = os.getenv(
    "GROQ_MODEL",
    "llama-3.3-70b-versatile"
)
```

The module loads environment variables and retrieves the configuration required for Groq integration.

### Environment variables

| Variable | Purpose | Default |
|---|---|---|
| `GROQ_API_KEY` | Authentication key used by the Groq client | No default |
| `GROQ_MODEL` | Specifies the language model used for generation | `llama-3.3-70b-versatile` |

### GROQ_API_KEY

The API key is retrieved using:

```python
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
```

This keeps the API credential outside the source code.

### GROQ_MODEL

The selected model is retrieved using:

```python
GROQ_MODEL = os.getenv(
    "GROQ_MODEL",
    "llama-3.3-70b-versatile"
)
```

If `GROQ_MODEL` is defined in the environment, that value is used. Otherwise, the module defaults to `llama-3.3-70b-versatile`.

This allows the model selection to be changed through environment configuration without modifying the request logic.

## 4. Groq Client Initialization

```python
client = Groq(
    api_key=GROQ_API_KEY
)
```

The Groq client is initialized using the configured API key.

The client is created at module level, meaning it is initialized when the module is imported and reused by subsequent calls to `ask_llm()`.

The module does not initialize a new Groq client for every user request.

**Configuration note:** The source does not explicitly validate whether `GROQ_API_KEY` exists before initializing the client.

## 5. Core Function: `ask_llm()`

```python
def ask_llm(
    user_input: str,
    conversation_history: list = None
):
```

The `ask_llm()` function is responsible for sending user input and conversation context to the configured Groq model.

It accepts two parameters.

| Parameter | Type | Description |
|---|---|---|
| `user_input` | `str` | The latest message submitted by the user |
| `conversation_history` | `list` | Optional list of previous conversation messages |

If no conversation history is supplied, the function starts with the system prompt and the current user message.

## 6. Message Construction

The function first creates a messages list containing the system prompt.

### Step 1: Initialize the system message

```python
messages = [
    {
        "role": "system",
        "content": SYSTEM_PROMPT
    }
]
```

The system message establishes the instructions and behavioral context provided to the language model.

The actual content of these instructions is defined in:

`app/utils/prompts.py`

The message uses the `system` role, distinguishing it from user and assistant conversation messages.

### Step 2: Add conversation history

```python
if conversation_history:
    messages.extend(conversation_history)
```

If conversation history is provided and is truthy, the previous messages are appended to the messages list.

This allows the LLM to receive earlier conversation context when generating a response.

The history is appended without modification.

The expected structure is a list of message dictionaries compatible with the chat-completion message format.

For example:

```python
conversation_history = [
    {
        "role": "user",
        "content": "Hello!"
    },
    {
        "role": "assistant",
        "content": "Hey! How can I help?"
    }
]
```

The example illustrates the expected message structure; the actual history supplied depends on the calling component.

### Step 3: Append the current user message

```python
messages.append(
    {
        "role": "user",
        "content": user_input
    }
)
```

The latest user input is appended after the system prompt and any supplied conversation history.

The final message structure follows this order:

1. System prompt.
2. Previous conversation messages, if provided.
3. Current user message.

This ensures that the model receives the latest request along with the available conversation context.

## 7. Groq Chat Completion Request

Once the messages list is constructed, the module sends the request to Groq.

```python
completion = client.chat.completions.create(
    model=GROQ_MODEL,
    messages=messages,
    temperature=0.7,
    max_tokens=300,
    top_p=1,
    stream=False
)
```

The request uses the Groq chat-completions interface.

### Generation parameters

| Parameter | Value | Purpose |
|---|---|---|
| `model` | `GROQ_MODEL` | Selects the configured language model |
| `messages` | Constructed message list | Provides system instructions and conversation context |
| `temperature` | `0.7` | Controls response-generation randomness |
| `max_tokens` | `300` | Sets the maximum number of generated tokens |
| `top_p` | `1` | Configures nucleus sampling |
| `stream` | `False` | Requests a complete response instead of streamed output |

### Non-streaming response

The setting:

```python
stream=False
```

means that the module waits for the completion request to finish before processing the returned response.

The function does not stream generated tokens to the caller.

## 8. Extracting the LLM Response

```python
reply = (
    completion
    .choices[0]
    .message
    .content
)
```

After the completion request succeeds, the module extracts the generated message content from the first returned choice.

The response is accessed through:

- `completion.choices[0]` – First generated completion choice.
- `.message` – Message associated with that choice.
- `.content` – Generated text content.

The response is then cleaned and returned:

```python
return reply.strip()
```

The `strip()` method removes leading and trailing whitespace from the generated response.

## 9. Logging and Error Handling

The entire message construction and LLM request process is enclosed within a `try-except` block.

### Successful response

```python
logger.info(
    f"LLM Response Generated Successfully"
)
```

When the request and response extraction succeed, the module records a success message through the application's logger.

The generated response is then returned to the calling component.

### Exception handling

```python
except Exception as e:

    logger.error(
        f"LLM ERROR: {str(e)}"
    )

    return (
        "Sorry, I encountered an issue "
        "while processing your request."
    )
```

If an exception occurs during processing:

1. The exception is caught.
2. The error details are recorded in the application logs.
3. A predefined fallback response is returned.

The fallback response is:

```text
Sorry, I encountered an issue while processing your request.
```

This provides a consistent response to the caller when an operation fails.

The function does not re-raise the caught exception.

## 10. Complete Execution Flow

The LLM request follows this sequence:

1. The backend imports `ask_llm()`.
2. Environment variables are loaded.
3. The Groq client is initialized.
4. A calling component supplies the latest user message.
5. The system prompt is added to the messages list.
6. Previous conversation history is appended if available.
7. The current user message is appended.
8. The configured Groq model receives the chat-completion request.
9. The generated response is extracted from the first completion choice.
10. A success message is recorded in the logs.
11. The cleaned response is returned to the caller.

If an exception occurs, the error is logged and the fallback message is returned instead.

## 11. Current Implementation Scope

The module currently provides:

- Groq API client integration.
- Environment-based API key configuration.
- Environment-based model selection.
- System prompt integration.
- Optional conversation-history support.
- Chat-completion request construction.
- Configurable generation parameters.
- Non-streaming response generation.
- Response extraction and whitespace cleanup.
- Success and error logging.
- A fallback response for caught exceptions.

The module does not currently implement:

- Streaming token generation.
- Conversation-history storage or retrieval.
- Automatic retry logic.
- Explicit API-key validation.
- Request timeout configuration in the supplied code.
- Token usage tracking.
- Custom model selection per request.
- Tool calling or function execution.
- Direct integration with a vector database.

These responsibilities are not defined in this module.

## 12. Integration with Other Backend Components

The `ask_llm()` function acts as a reusable language-model interface for other components in the Nevark backend.

A calling service can provide:

- The current user input.
- Previous conversation messages, when available.

The function handles message construction, Groq communication, response extraction, and basic error handling.

The system prompt is sourced from `app/utils/prompts.py`, while logging is delegated to `app/utils/logger.py`.

This separation keeps language-model communication independent of prompt definition and logging implementation.

## 13. Summary

The `llm_engine.py` module serves as the Groq-powered language-model execution layer of Nevark AI.

It constructs a conversation using the system prompt, optional conversation history, and current user input. It then sends the request to the configured Groq model using controlled generation parameters.

After receiving the response, it extracts and returns the generated text. If processing fails, it logs the exception and returns a fallback message.

The module provides the backend with a centralized interface for LLM response generation while keeping model configuration, prompt definition, and logging separated from the calling services.