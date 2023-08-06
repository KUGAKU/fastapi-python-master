from abc import ABC, abstractmethod
import json
import os
from fastapi.responses import StreamingResponse

from injector import inject
import openai


class AbstractChatController(ABC):
    @abstractmethod
    def chat(self):
        raise NotImplementedError()


class ChatController(AbstractChatController):
    @inject
    def __init__(self) -> None:
        pass

    def chat(self):
        response = StreamingResponse(
            content=self.stream_content(), media_type="text/event-stream"
        )
        print("xxx")
        return response

    def stream_content(self):
        openai.api_type = "azure"
        openai.api_base = "https://dev-aoai.openai.azure.com/"
        openai.api_version = "2023-03-15-preview"
        openai.api_key = os.getenv("OPENAI_API_KEY")

        response = openai.ChatCompletion.create(
            engine="gpt-35-turbo",
            messages=[
                {
                    "role": "user",
                    "content": "terraformのソースコードをリファクタリングしたいと考えているんだけど、どういった手順でリファクタリングするのが良いと思う？",
                }
            ],
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
                print(data)
                yield packet
