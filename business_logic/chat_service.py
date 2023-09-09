from abc import ABC, abstractmethod
from typing import Any, Generator, Optional
import uuid
from injector import inject
from data_access.chat_repository import AbstractChatRepository
from data_source.langchain.langchain_chat_model_factory import LangchainChatModelFactory
from data_source.langchain.langchain_memory_factory import LangchainMemoryFactory
from data_source.openai_data_source import AbstractOpenaiDataSource
from data_transfer_object.chat_completion_chunk import ChatCompletionChunk
from models.message_type import MessageTypeEnum
from utils.message_buffer import MessageBufferManager
from langchain.schema import HumanMessage
from utils.server_sent_event_maker import (
    ChatSSEData,
    ChatSSEEvent,
    ServerSentEventMaker,
)


class AbstractChatService(ABC):
    @abstractmethod
    def get_chat_data(
        self, chat_message: str, conversation_id: Optional[str]
    ) -> Generator[str, Any, None]:
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

    def extract_event_content(self, event: ChatCompletionChunk) -> str:
        """Extract the content from a given event."""
        return event.choices[0].delta.get("content", "")

    def is_new_conversation(self, conversation_id: Optional[str]) -> bool:
        return conversation_id is None

    def get_chat_data(self, chat_message: str, conversation_id: Optional[str]):
        try:
            current_conversation_id = (
                str(uuid.uuid4())
                if self.is_new_conversation(conversation_id)
                else conversation_id
            )

            if current_conversation_id is None:
                raise ValueError("current_conversation_id should not be None.")

            messageBufferManager = MessageBufferManager()
            chatModelFactory = LangchainChatModelFactory()
            memoryFactory = LangchainMemoryFactory()
            history = memoryFactory.create_instance(current_conversation_id)
            history.add_user_message(chat_message)

            def handle_token(token: str):
                messageBufferManager.add_to_buffer(token)

            azure_chat_model = chatModelFactory.create_instance(handle_token)
            azure_chat_model(history.messages)

            for token in messageBufferManager.get_buffer():
                chatSSEData = ChatSSEData(chat_content=token, conversation_id=None)
                yield ServerSentEventMaker.create_sse_packet(
                    ChatSSEEvent.PROGRESSION, chatSSEData
                )
            message = messageBufferManager.get_joined_buffer()

            history.add_ai_message(message)

            self.chat_repository.upsert_conversation_message(
                current_conversation_id,
                chat_message,
                MessageTypeEnum.HUMAN,
            )
            self.chat_repository.upsert_conversation_message(
                current_conversation_id,
                message,
                MessageTypeEnum.ARTIFICIAL_INTELLIGENCE,
            )

            chatSSEData = ChatSSEData(
                chat_content="", conversation_id=current_conversation_id
            )  # todo: fix this
            yield ServerSentEventMaker.create_sse_packet(
                ChatSSEEvent.COMPLETE, chatSSEData
            )
        except Exception as e:
            raise
