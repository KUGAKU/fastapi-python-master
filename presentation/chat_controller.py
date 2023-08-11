from abc import ABC, abstractmethod
from fastapi.responses import StreamingResponse

from injector import inject

from business_logic.chat_service import AbstractChatService


class AbstractChatController(ABC):
    @abstractmethod
    def start(self, chatMessage: str):
        raise NotImplementedError()


class ChatController(AbstractChatController):
    @inject
    def __init__(self, chat_service: AbstractChatService) -> None:
        if not isinstance(chat_service, AbstractChatService):
            raise TypeError("chat_service must be an instance of AbstractChatService")
        self.chat_service = chat_service

    def start(self, chatMessage: str):
        return StreamingResponse(
            content=self.chat_service.get_chat_data(chatMessage),
            media_type="text/event-stream",
        )
