# Command Parser

## 1. Overview

The `command_parser.py` module implements a lightweight command-detection mechanism for Nevark AI.

Its purpose is to inspect user input, identify predefined command keywords, and return the corresponding command category.

The parser currently recognizes two command categories:

- `shutdown` – Detects commands such as shutdown, exit, and quit.
- `greeting` – Detects greetings such as hello, hi, and hey.

If no recognized keyword is found, the function returns `None`.

## 2. Dependencies

The module uses Python's built-in `re` library.

```python
import re
```

The regular expression library is used to extract individual words from the user's input.

No external packages are required by this module.

## 3. Core Function: `detect_command()`

```python
def detect_command(user_input: str):
```

The function accepts a string containing the user's input and attempts to identify whether it matches one of the predefined command categories.

**Input:**

| Parameter | Type | Description |
|---|---|---|
| `user_input` | `str` | Text provided by the user |

**Return values:**

| Return value | Meaning |
|---|---|
| `"shutdown"` | A shutdown-related keyword was detected |
| `"greeting"` | A greeting keyword was detected |
| `None` | No recognized command was found |

## 4. Command Detection Process

### Step 1: Normalize user input

```python
user_input = user_input.lower()
```

Converts the entire input string into lowercase.

This makes command detection case-insensitive.

For example:

- `HELLO` becomes `hello`.
- `Shutdown` becomes `shutdown`.
- `QUIT` becomes `quit`.

### Step 2: Extract individual words

```python
words = re.findall(
    r"\b\w+\b",
    user_input
)
```

The regular expression extracts individual word sequences from the input.

The pattern uses:

- `\b` – Word boundary.
- `\w+` – One or more word characters, including letters, digits, and underscores.
- `\b` – Ending word boundary.

For example:

**Input:**

```text
Hey Nevark, can you help me?
```

**Extracted words:**

```python
["hey", "nevark", "can", "you", "help", "me"]
```

This allows the parser to compare individual words instead of searching through the complete sentence as one string.

### Step 3: Define supported commands

```python
commands = {
    "shutdown": [
        "shutdown",
        "exit",
        "quit"
    ],

    "greeting": [
        "hello",
        "hi",
        "hey"
    ]
}
```

The `commands` dictionary stores the supported command categories and their associated keywords.

| Command category | Recognized keywords |
|---|---|
| `shutdown` | `shutdown`, `exit`, `quit` |
| `greeting` | `hello`, `hi`, `hey` |

This dictionary provides a simple structure for managing the command keywords.

### Step 4: Match extracted words against commands

```python
for command, keywords in commands.items():

    for keyword in keywords:

        if keyword in words:

            return command
```

The parser iterates through each command category and its associated keywords.

For every keyword, it checks whether that keyword exists in the extracted `words` list.

When a match is found, the corresponding command category is returned immediately.

For example:

- If `exit` is found, the function returns `"shutdown"`.
- If `hello` is found, the function returns `"greeting"`.

The function returns the first matching category based on the dictionary's iteration order.

### Step 5: Handle unmatched input

```python
return None
```

If none of the predefined keywords are found, the function returns `None`.

This indicates that the input does not match any command currently supported by the parser.

## 5. Execution Examples

### Example 1: Shutdown command

**Input:**

```python
detect_command("Please shutdown the system")
```

**Output:**

```python
"shutdown"
```

Reason: The word `shutdown` matches a predefined shutdown keyword.

### Example 2: Greeting command

**Input:**

```python
detect_command("Hey Nevark!")
```

**Output:**

```python
"greeting"
```

Reason: The extracted word `hey` matches the greeting category.

### Example 3: Case-insensitive detection

**Input:**

```python
detect_command("HELLO THERE")
```

**Output:**

```python
"greeting"
```

Reason: The input is converted to lowercase before keyword matching.

### Example 4: No recognized command

**Input:**

```python
detect_command("What is artificial intelligence?")
```

**Output:**

```python
None
```

Reason: None of the extracted words match the supported command keywords.

## 6. Important Implementation Details

### Word-based matching

The parser checks whether a complete extracted word matches a keyword.

For example, `hi` is detected as a command when it appears as an individual word, but it is not detected inside a larger word such as `history`.

### First-match behavior

The function immediately returns when it encounters the first matching keyword.

If an input contains keywords from multiple categories, the returned category depends on the order in which the categories are defined in the dictionary.

Currently, `shutdown` is checked before `greeting`.

### Fixed command vocabulary

The parser uses a statically defined dictionary.

It does not currently support:

- Dynamic command registration.
- Context-aware command detection.
- Natural-language intent classification.
- Semantic similarity matching.
- AI-based command interpretation.

## 7. Integration Considerations

The function can be used by other backend components to identify simple commands before deciding how to process user input.

For example, a component calling `detect_command()` could inspect the returned category and implement the corresponding behavior.

However, this module itself only identifies and returns the command category. It does not shut down the application, generate greeting responses, or execute any other action.

## 8. Summary

The `command_parser.py` module provides a simple rule-based command detection layer for Nevark AI.

It normalizes user input, extracts individual words using regular expressions, and compares them against a predefined command dictionary.

Its current functionality is limited to detecting greetings and shutdown-related commands, returning `None` for unmatched input.

The module provides a lightweight foundation for command recognition without requiring an LLM or external NLP dependency.