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

            azure_chat_openai = chatModelFactory.create_instance(handle_token)
            human_message_token_count = azure_chat_openai.get_num_tokens(chat_message)
            token_count_including_special_token = (
                azure_chat_openai.get_num_tokens_from_messages(history.messages)
            )

            self.chat_repository.upsert_conversation_message(
                current_conversation_id,
                chat_message,
                MessageTypeEnum.HUMAN,
                human_message_token_count,
                token_count_including_special_token,
            )

            azure_chat_openai(history.messages)

            for token in messageBufferManager.get_buffer():
                chatSSEData = ChatSSEData(chat_content=token, conversation_id=None)
                yield ServerSentEventMaker.create_sse_packet(
                    ChatSSEEvent.PROGRESSION, chatSSEData
                )
            message = messageBufferManager.get_joined_buffer()

            ai_message_token_count = azure_chat_openai.get_num_tokens(message)
            history.add_ai_message(message)

            token_count_including_special_token = (
                azure_chat_openai.get_num_tokens_from_messages(history.messages)
            )

            self.chat_repository.upsert_conversation_message(
                current_conversation_id,
                message,
                MessageTypeEnum.ARTIFICIAL_INTELLIGENCE,
                ai_message_token_count,
                token_count_including_special_token,
            )

            chatSSEData = ChatSSEData(
                chat_content="", conversation_id=current_conversation_id
            )  # todo: fix this
            yield ServerSentEventMaker.create_sse_packet(
                ChatSSEEvent.COMPLETE, chatSSEData
            )
        except Exception as e:
            raise
