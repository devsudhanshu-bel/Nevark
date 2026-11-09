import os
import json
from datetime import datetime

MEMORY_DIR = "memory"
MEMORY_FILE = os.path.join(
    MEMORY_DIR,
    "conversations.json"
)


def save_memory(
    user_message: str,
    ai_response: str
):

    os.makedirs(
        MEMORY_DIR,
        exist_ok=True
    )

    memory_data = []

    if os.path.exists(MEMORY_FILE):

        try:

            with open(
                MEMORY_FILE,
                "r",
                encoding="utf-8"
            ) as file:

                memory_data = json.load(file)

        except Exception:

            memory_data = []

    memory_data.append({

        "timestamp": str(datetime.now()),

        "user": user_message,

        "assistant": ai_response
    })

    with open(
        MEMORY_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            memory_data,
            file,
            indent=4,
            ensure_ascii=False
        )


def load_recent_memory(
    limit: int = 10
):

    if not os.path.exists(MEMORY_FILE):

        return []

    try:

        with open(
            MEMORY_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            memory_data = json.load(file)

    except Exception:

        return []

    recent = memory_data[-limit:]

    conversation_history = []

    for item in recent:

        conversation_history.append({

            "role": "user",

            "content": item["user"]
        })

        conversation_history.append({

            "role": "assistant",

            "content": item["assistant"]
        })

    return conversation_history