from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.database.models import Conversation


def fetch_recent_conversations(
    limit: int = 10
):

    try:

        db: Session = SessionLocal()

        conversations = (

            db.query(Conversation)

            .order_by(
                Conversation.id.desc()
            )

            .limit(limit)

            .all()
        )

        db.close()

        return conversations

    except Exception as e:

        print(
            "❌ MEMORY SERVICE ERROR:",
            e
        )

        return []


def build_conversation_history(
    limit: int = 10
):

    conversations = fetch_recent_conversations(
        limit
    )

    history = []

    for convo in reversed(conversations):

        history.append({

            "role": "user",

            "content": convo.user_message
        })

        history.append({

            "role": "assistant",

            "content": convo.ai_response
        })

    return history