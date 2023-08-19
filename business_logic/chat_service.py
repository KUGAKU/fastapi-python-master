from abc import ABC, abstractmethod
import json
from typing import Any, Generator
from injector import inject
from data_access.chat_repository import AbstractChatRepository
from data_source.openai_data_source import AbstractOpenaiDataSource
from models.chat_completion_chunk import ChatCompletionChunk


class AbstractChatService(ABC):
    @abstractmethod
    def get_chat_data(self, chatMessage: str) -> Generator[str, Any, None]:
        raise NotImplementedError()


class ChatService(AbstractChatService):
    @inject
    def __init__(
        self,
        chat_repository: AbstractChatRepository,
        openai_data_source: AbstractOpenaiDataSource,
    ) -> None:
        if not isinstance(chat_repository, AbstractChatRepository):
            raise TypeError(
                "chat_repository must be an instance of AbstractChatRepository"
            )
        if not isinstance(openai_data_source, AbstractOpenaiDataSource):
            raise TypeError(
                "openai_data_source must be an instance of AbstractOpenaiDataSource"
            )
        self.chat_repository = chat_repository
        self.openai_data_source = openai_data_source

    def create_sse_packet(self, message: str) -> str:
        """Convert a given message into SSE packet format."""
        data = json.dumps({"message": message}, ensure_ascii=False)
        return f"event: message\ndata: {data}\n\n"

    def extract_event_content(self, event: ChatCompletionChunk) -> str:
        """Extract the content from a given event."""
        return event.choices[0].delta.get("content", "")

    def get_chat_data(self, chatMessage: str):
        response = self.openai_data_source.get_chat_stream_content(chatMessage)
        for event in response:
            event_content = self.extract_event_content(event)
            if event_content:
                yield self.create_sse_packet(event_content)
        yield self.create_sse_packet("done")
