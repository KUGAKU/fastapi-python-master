from abc import ABC, abstractmethod
import json
import os
from fastapi.responses import StreamingResponse

from injector import inject
import openai


class AbstractChatController(ABC):
    @abstractmethod
    def chat(self, chatMessage: str):
        raise NotImplementedError()


class ChatController(AbstractChatController):
    @inject
    def __init__(self) -> None:
        pass

    def chat(self, chatMessage: str):
        response = StreamingResponse(
            content=self.stream_content(chatMessage), media_type="text/event-stream"
        )
        return response

    def stream_content(self, chatMessage: str):
        openai.api_type = "azure"
        openai.api_base = "https://dev-aoai.openai.azure.com/"
        openai.api_version = "2023-03-15-preview"
        openai.api_key = os.getenv("OPENAI_API_KEY")

        response = openai.ChatCompletion.create(
            engine="gpt-35-turbo",
            messages=[{"role": "user", "content": chatMessage}],
            temperature=0.7,
            max_tokens=800,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stream=True,
        )

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
