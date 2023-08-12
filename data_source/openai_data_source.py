from abc import ABC, abstractmethod
import os
from typing import Any, Generator

import openai


class AbstractOpenaiDataSource(ABC):
    @abstractmethod
    def get_chat_stream_content(
        self, chatMessage: str
    ) -> Generator[Any | list | dict, None, None] | Any | list | dict:
        raise NotImplementedError()


class OpenaiDataSource(AbstractOpenaiDataSource):
    def get_chat_stream_content(self, chatMessage: str):
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
        return response
