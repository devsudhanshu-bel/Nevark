from fastapi import APIRouter
from pydantic import BaseModel

from app.services.chat_service import process_chat

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


class ChatRequest(BaseModel):
    message: str


@router.post("/")
async def chat(request: ChatRequest):

    response = await process_chat(
        request.message
    )

    return {
        "success": True,
        "response": response
    }