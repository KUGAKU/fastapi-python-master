from dataclasses import dataclass
from enum import Enum
import json
from typing import Optional


@dataclass
class ChatSSEData:
    def __init__(self, chat_content: str, conversation_id: Optional[str]):
        self.chat_content = chat_content
        self.conversation_id = conversation_id


class ChatSSEDataEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ChatSSEData):
            return obj.__dict__
        return super().default(obj)


class ChatSSEEvent(Enum):
    PROGRESSION = "progression"  # SSEによってチャットメッセージを送信している事を示します。
    COMPLETE = "complete"  # SSEによってチャットメッセージの送信が完了した事を示します。
    ERROR = "error"  # SSEによってチャットメッセージの送信が失敗した事を示します。


class ServerSentEventMaker:
    @classmethod
    def create_sse_packet(
        self, chatSSEEvent: ChatSSEEvent, chatSSEData: ChatSSEData
    ) -> str:
        """Convert a given message into SSE packet format."""
        data = json.dumps(
            chatSSEData,
            cls=ChatSSEDataEncoder,
            ensure_ascii=False,
        )
        return f"event: {chatSSEEvent.value}\ndata: {data}\n\n"
