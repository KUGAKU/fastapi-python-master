from abc import ABC, abstractmethod
from typing import Optional
from fastapi.responses import StreamingResponse

from injector import inject

from business_logic.chat_service import AbstractChatService
from schemas.chat import ChatRequest
from utils.server_sent_event_maker import (
    ChatSSEData,
    ChatSSEEvent,
    ServerSentEventMaker,
)


class AbstractChatController(ABC):
    @abstractmethod
    def startChat(self, chat_message: str, conversation_id: str):
        raise NotImplementedError()


class ChatController(AbstractChatController):
    @inject
    def __init__(self, chat_service: AbstractChatService) -> None:
        if not isinstance(chat_service, AbstractChatService):
            raise TypeError("chat_service must be an instance of AbstractChatService")
        self.chat_service = chat_service

    def startChat(self, chat_message: str, conversation_id: str):
        try:
            return StreamingResponse(
                content=self.chat_service.get_chat_data(chat_message, conversation_id),
                media_type="text/event-stream",
            )
        except Exception as e:
            print(e)

            def error(e: Exception):
                error_message = str(e)
                yield ServerSentEventMaker.create_sse_packet(  # todo: fix this
                    ChatSSEEvent.ERROR,
                    ChatSSEData(chat_content=error_message, conversation_id=None),
                )

            return StreamingResponse(
                content=error(e),
                status_code=500,
                media_type="text/event-stream",
            )
