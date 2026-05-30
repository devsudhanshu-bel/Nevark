from sqlalchemy.orm import Session

from app.core.llm_engine import ask_llm
from app.core.command_parser import detect_command

from app.core.memory_engine import (
    save_memory
)

from app.core.rag_engine import (
    retrieve_relevant_memories,
    save_memory_to_vector_db
)

from app.services.memory_service import (
    build_conversation_history
)

from app.database.database import SessionLocal
from app.database.models import Conversation


async def process_chat(
    user_input: str
):

    try:

        command = detect_command(
            user_input
        )

        if command == "shutdown":

            return (
                "Shutting down Nevark AI."
            )

        if command == "greeting":

            return (
                "Hello, I am Nevark AI. "
                "How can I help you today?"
            )

        # ===================================
        # SHORT TERM MEMORY
        # ===================================

        conversation_history = (

            build_conversation_history(
                limit=10
            )
        )

        # ===================================
        # MEMORY DETECTION
        # ===================================

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

        use_rag = any(

            keyword in user_input.lower()

            for keyword in memory_keywords
        )

        relevant_memories = []

        if use_rag:

            relevant_memories = (

                retrieve_relevant_memories(
                    user_input
                )
            )

        memory_context = ""

        if relevant_memories:

            memory_context = "\n".join(
                relevant_memories
            )

        # ===================================
        # PROMPT BUILDING
        # ===================================

        if memory_context:

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

        else:

            enhanced_prompt = user_input

        # ===================================
        # ASK LLM
        # ===================================

        ai_response = ask_llm(

            user_input=enhanced_prompt,

            conversation_history=
            conversation_history
        )

        # ===================================
        # SAVE JSON MEMORY
        # ===================================

        save_memory(

            user_input,

            ai_response
        )

        # ===================================
        # SAVE VECTOR MEMORY
        # ===================================

        save_memory_to_vector_db(
            user_input
        )

        # ===================================
        # SAVE DATABASE
        # ===================================

        db: Session = SessionLocal()

        conversation = Conversation(

            user_message=user_input,

            ai_response=ai_response
        )

        db.add(conversation)

        db.commit()

        db.close()

        return ai_response

    except Exception as e:

        print(
            "❌ CHAT SERVICE ERROR:",
            e
        )

        return (
            "Sorry, something went "
            "wrong in the AI service."
        )