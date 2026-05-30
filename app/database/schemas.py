from pydantic import BaseModel
from datetime import datetime


class ConversationBase(BaseModel):

    user_message: str

    ai_response: str


class ConversationCreate(ConversationBase):

    pass


class ConversationResponse(ConversationBase):

    id: int

    timestamp: datetime

    class Config:

        from_attributes = True
