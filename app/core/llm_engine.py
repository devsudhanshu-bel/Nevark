import os

from groq import Groq
from dotenv import load_dotenv

from app.utils.prompts import SYSTEM_PROMPT
from app.utils.logger import logger

load_dotenv()

# ============================================================
# ENV VARIABLES
# ============================================================

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

GROQ_MODEL = os.getenv(
    "GROQ_MODEL",
    "llama-3.3-70b-versatile"
)

# ============================================================
# GROQ CLIENT
# ============================================================

client = Groq(
    api_key=GROQ_API_KEY
)

# ============================================================
# ASK LLM
# ============================================================

def ask_llm(

    user_input: str,

    conversation_history: list = None
):

    try:

        messages = [

            {
                "role": "system",
                "content": SYSTEM_PROMPT
            }
        ]

        # ====================================================
        # ADD CONVERSATION HISTORY
        # ====================================================

        if conversation_history:

            messages.extend(conversation_history)

        # ====================================================
        # CURRENT USER MESSAGE
        # ====================================================

        messages.append(

            {
                "role": "user",
                "content": user_input
            }
        )

        # ====================================================
        # GROQ REQUEST
        # ====================================================

        completion = client.chat.completions.create(

            model=GROQ_MODEL,

            messages=messages,

            temperature=0.7,

            max_tokens=300,

            top_p=1,

            stream=False
        )

        reply = (

            completion
            .choices[0]
            .message
            .content
        )

        logger.info(
            f"LLM Response Generated Successfully"
        )

        return reply.strip()

    except Exception as e:

        logger.error(
            f"LLM ERROR: {str(e)}"
        )

        return (
            "Sorry, I encountered an issue "
            "while processing your request."
        )
