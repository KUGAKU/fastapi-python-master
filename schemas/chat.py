from typing import Optional
from pydantic import BaseModel


# class ChatResponse(BaseModel):
#     chatMessage: str
#     conversation_id: str


class ChatRequest(BaseModel):
    chat_message: str
    conversation_id: Optional[str]
