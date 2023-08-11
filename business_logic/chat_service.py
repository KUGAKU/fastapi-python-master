from abc import ABC, abstractmethod
import json
from typing import Any, Generator

from injector import inject

from data_access.chat_repository import AbstractChatRepository


class AbstractChatService(ABC):
    @abstractmethod
    def get_chat_data(self, chatMessage: str) -> Generator[str, Any, None]:
        raise NotImplementedError()


class ChatService(AbstractChatService):
    @inject
    def __init__(self, chat_repository: AbstractChatRepository) -> None:
        if not isinstance(chat_repository, AbstractChatRepository):
            raise TypeError(
                "chat_repository must be an instance of AbstractChatRepository"
            )
        self.chat_repository = chat_repository

    def get_chat_data(self, chatMessage: str):
        response = self.chat_repository.get_chat_stream_content(chatMessage)

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
