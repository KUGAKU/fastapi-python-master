from dataclasses import dataclass
from enum import Enum
import json
from typing import Union


@dataclass
class ProgressionSSEData:
    def __init__(self, chat_content: str, conversation_id: str):
        self.chat_content = chat_content
        self.conversation_id = conversation_id


@dataclass
class CompleteSSEData:
    def __init__(self):
        self.message = "done"


@dataclass
class ErrorSSEData:
    def __init__(self, ex: Exception):
        self.error = str(ex)


class SSEDataEncoder(json.JSONEncoder):
    def default(self, obj):
        if (
            isinstance(obj, ProgressionSSEData)
            or isinstance(obj, CompleteSSEData)
            or isinstance(obj, ErrorSSEData)
        ):
            return obj.__dict__
        return super().default(obj)


class SSEEvent(Enum):
    PROGRESSION = "progression"  # SSEによってチャットメッセージを送信している事を示します。
    COMPLETE = "complete"  # SSEによってチャットメッセージの送信が完了した事を示します。
    ERROR = "error"  # SSEによってチャットメッセージの送信が失敗した事を示します。


class ServerSentEventMaker:
    @classmethod
    def create_sse_packet(
        self,
        sse_event: SSEEvent,
        sse_data: Union[ProgressionSSEData, CompleteSSEData, ErrorSSEData],
    ) -> str:
        """Convert a given message into SSE packet format."""
        if sse_event == SSEEvent.PROGRESSION and not isinstance(
            sse_data, ProgressionSSEData
        ):
            raise ValueError("sse_data must be an instance of ProgressionSSEData")
        if sse_event == SSEEvent.COMPLETE and not isinstance(sse_data, CompleteSSEData):
            raise ValueError("sse_data must be an instance of CompleteSSEData")
        if sse_event == SSEEvent.ERROR and not isinstance(sse_data, ErrorSSEData):
            raise ValueError("sse_data must be an instance of ErrorSSEData")
        data = json.dumps(
            sse_data,
            cls=SSEDataEncoder,
            ensure_ascii=False,
        )
        return f"event: {sse_event.value}\ndata: {data}\n\n"
