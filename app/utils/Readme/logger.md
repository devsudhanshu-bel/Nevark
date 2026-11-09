# Logging Utility

## 1. Overview

The `logger.py` module provides centralized logging configuration for the Nevark AI backend.

It uses Python's built-in `logging` module to capture application events and write log messages to two destinations:

- A persistent log file: `logs/nevark.log`
- The terminal through a console stream handler.

The module configures logging at the INFO level and exposes a named logger called `NevarkAI`.

Other backend components can import this shared logger to record informational messages, warnings, errors, and other logging events.

## 2. Dependencies

```python
import logging
import os
```

| Dependency | Purpose |
|---|---|
| `logging` | Provides Python's built-in logging framework |
| `os` | Creates the directory used for log storage |

No external logging package is required.

## 3. Log Directory Initialization

```python
os.makedirs("logs", exist_ok=True)
```

The module creates a directory named `logs` if it does not already exist.

The `exist_ok=True` parameter prevents an error when the directory is already present.

This ensures that the destination directory is available before the file logging handler is configured.

## 4. Log File Configuration

```python
LOG_FILE = "logs/nevark.log"
```

The module defines the destination for persistent application logs.

| Property | Value |
|---|---|
| Directory | `logs/` |
| Filename | `nevark.log` |
| Full relative path | `logs/nevark.log` |
| Format | Plain-text log entries |

The path is relative to the application's current working directory.

## 5. Logging Configuration

```python
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
```

The `logging.basicConfig()` function configures Python's root logging system.

### 5.1 Logging level

```python
level=logging.INFO
```

The minimum logging level is set to `INFO`.

The standard logging levels are:

| Level | Purpose |
|---|---|
| `DEBUG` | Detailed diagnostic information |
| `INFO` | General application events |
| `WARNING` | Potential problems that do not necessarily stop execution |
| `ERROR` | Errors that affect an operation |
| `CRITICAL` | Severe failures |

With the configured INFO threshold, INFO, WARNING, ERROR, and CRITICAL messages are eligible for processing.

DEBUG messages are excluded by this configuration.

### 5.2 Log message format

```python
format="%(asctime)s | %(levelname)s | %(message)s"
```

The module defines a consistent format for every log entry.

| Format field | Description |
|---|---|
| `%(asctime)s` | Timestamp when the log record is created |
| `%(levelname)s` | Logging severity level |
| `%(message)s` | Actual log message |

Example:

```text
2026-11-09 10:30:00,123 | INFO | LLM Response Generated Successfully
```

The timestamp shown is illustrative.

The vertical separators make log entries easier to scan.

## 6. Logging Handlers

The configuration defines two handlers.

### 6.1 FileHandler

```python
logging.FileHandler(LOG_FILE)
```

The file handler writes log messages to:

`logs/nevark.log`

This provides persistent logging so that application events can be inspected after execution.

### 6.2 StreamHandler

```python
logging.StreamHandler()
```

The stream handler sends log messages to the configured console stream, which defaults to standard error.

This allows developers to monitor application events directly in the terminal while the backend is running.

### Dual-output logging

Both handlers are configured together:

```text
             Application Event
                     |
                     v
               Python Logger
                     |
              +------+------+
              |             |
              v             v
          FileHandler   StreamHandler
              |             |
              v             v
       logs/nevark.log   Terminal
```

A qualifying log record is sent to both configured destinations.

## 7. Named Logger Initialization

```python
logger = logging.getLogger("NevarkAI")
```

The module creates a named logger called `NevarkAI`.

This logger can be imported and reused by different backend components.

For example:

```python
from app.utils.logger import logger
```

The imported logger can then record application events.

### Example logging operations

```python
logger.info("Application started")

logger.warning("Unexpected input received")

logger.error("Database operation failed")

logger.critical("Critical application failure")
```

These examples demonstrate the available logging methods.

The resulting records use the configured logging format and handlers when the logging configuration is active.

## 8. Integration with Other Backend Components

The logger is designed to be shared across the application.

For example, the LLM engine imports it:

```python
from app.utils.logger import logger
```

The LLM engine uses it to record successful response generation and errors.

This allows different modules to use a common logging configuration rather than independently defining log destinations and formats.

The shared logger provides consistency across backend components.

## 9. Current Implementation Scope

The module currently provides:

- Automatic creation of the log directory.
- Centralized logging configuration.
- INFO-level logging threshold.
- Timestamped log formatting.
- Severity-level formatting.
- Message formatting.
- Persistent file logging.
- Console logging.
- Named `NevarkAI` logger.

The module does not currently implement:

- Log rotation.
- Maximum log-file size limits.
- Automatic log retention or deletion.
- Separate files for different severity levels.
- JSON-formatted logging.
- Request or session identifiers.
- Structured application metadata.
- Remote log aggregation.
- Custom logging filters.
- Explicit logging configuration validation.

## 10. Important Implementation Considerations

### 10.1 Relative log path

The configured path is:

`logs/nevark.log`

Its location depends on the application's current working directory.

Running the application from a different directory may result in a different log directory being used.

### 10.2 Log persistence

The `FileHandler` writes logs to a local file.

The module does not configure rotation or retention, so the log file can continue growing as the application runs.

### 10.3 Basic configuration behavior

`logging.basicConfig()` configures the root logger when no handlers are already configured, unless options such as `force=True` are used.

The supplied implementation does not use `force=True`.

Therefore, if logging has already been configured elsewhere, this call may not replace the existing root configuration.

### 10.4 Shared logger

The named logger is created at module level and can be imported by other components.

This encourages consistent logging throughout the application.

## 11. Summary

The `logger.py` module provides the centralized logging foundation for Nevark AI.

It creates the log directory, configures Python logging at the INFO level, and directs log messages to both `logs/nevark.log` and the terminal.

By exposing a shared logger named `NevarkAI`, the module allows backend components to record application events using a consistent format and configuration.