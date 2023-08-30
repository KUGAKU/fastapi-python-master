from abc import ABC, abstractmethod
import os
from typing import Generator
import openai
from data_transfer_object.chat_completion_chunk import ChatCompletionChunk


class AbstractOpenaiDataSource(ABC):
    @abstractmethod
    def get_chat_stream_chunk_content(
        self, chatMessage: str
    ) -> Generator[ChatCompletionChunk, None, None]:
        raise NotImplementedError()


class OpenaiDataSource(AbstractOpenaiDataSource):
    def get_chat_stream_chunk_content(self, chatMessage: str):
        openai.api_type = os.getenv("AZURE_OPENAI_API_TYPE")
        openai.api_base = os.getenv("AZURE_OPENAI_API_BASE")
        openai.api_version = os.getenv("AZURE_OPENAI_API_VERSION")
        openai.api_key = os.getenv("AZURE_OPENAI_API_KEY")

        response = openai.ChatCompletion.create(
            engine=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
            messages=[{"role": "user", "content": chatMessage}],
            temperature=0.7,
            max_tokens=800,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stream=True,
        )
        return response
