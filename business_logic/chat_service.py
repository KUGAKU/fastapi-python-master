from abc import ABC, abstractmethod
import json
from typing import Any, Generator

from injector import inject

from data_access.chat_repository import AbstractChatRepository
from data_source.openai_data_source import AbstractOpenaiDataSource


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

    def get_chat_data(self, chatMessage: str):
        response = self.openai_data_source.get_chat_stream_content(chatMessage)

        for event in response:
            if "content" in event["choices"][0]["delta"]:
                event_text = event["choices"][0]["delta"]["content"]
                data = json.dumps({"message": event_text}, ensure_ascii=False)
                packet = "event: %s\n" % "message"
                packet += "data: %s\n" % data
                packet += "\n"
                yield packet
        data = json.dumps({"message": "done"}, ensure_ascii=False)
        packet = "event: %s\n" % "message"
        packet += "data: %s\n" % data
        packet += "\n"
        yield packet
