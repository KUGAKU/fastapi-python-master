from abc import ABC, abstractmethod
from typing import Optional
from fastapi.responses import StreamingResponse

from injector import inject

from business_logic.chat_service import AbstractChatService


class AbstractChatController(ABC):
    @abstractmethod
    def startChat(self, chat_message: str, conversation_id: Optional[str]):
        raise NotImplementedError()


class ChatController(AbstractChatController):
    @inject
    def __init__(self, chat_service: AbstractChatService) -> None:
        if not isinstance(chat_service, AbstractChatService):
            raise TypeError("chat_service must be an instance of AbstractChatService")
        self.chat_service = chat_service

    def startChat(self, chat_message: str, conversation_id: Optional[str]):
        return StreamingResponse(
            content=self.chat_service.get_chat_data(chat_message, conversation_id),
            media_type="text/event-stream",
        )
