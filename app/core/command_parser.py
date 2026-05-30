import re


def detect_command(user_input: str):

    user_input = user_input.lower()

    words = re.findall(
        r"\b\w+\b",
        user_input
    )

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

    for command, keywords in commands.items():

        for keyword in keywords:

            if keyword in words:

                return command

    return None