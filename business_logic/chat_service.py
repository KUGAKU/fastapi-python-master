from abc import ABC, abstractmethod
from typing import Any, Generator, Optional
from injector import inject
from data_access.chat_repository import AbstractChatRepository
from data_source.langchain.langchain_chat_model_factory import LangchainChatModelFactory
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

    def is_existing_conversation(self, conversation_id: Optional[str]) -> bool:
        if conversation_id == None:
            return False
        return True

    def get_chat_data(self, chat_message: str, conversation_id: Optional[str]):
        try:
            messageBufferManager = MessageBufferManager()

            def handle_token(token: str):
                messageBufferManager.add_to_buffer(token)

            factory = LangchainChatModelFactory()
            azure_chat_model = factory.create_instance(handle_token)
            azure_chat_model(
                [
                    HumanMessage(
                        content=chat_message,
                    )
                ]
            )
            for token in messageBufferManager.get_buffer():
                chatSSEData = ChatSSEData(chat_content=token, conversation_id=None)
                yield ServerSentEventMaker.create_sse_packet(
                    ChatSSEEvent.PROGRESSION, chatSSEData
                )
            message = messageBufferManager.get_joined_buffer()

            # response = self.openai_data_source.get_chat_stream_chunk_content(
            #     chat_message
            # )
            # for event in response:
            #     event_content = self.extract_event_content(event)
            #     if event_content:
            #         messageBufferManager.add_to_buffer(event_content)
            #         chatSSEData = ChatSSEData(
            #             chat_content=event_content, conversation_id=None
            #         )
            #         yield ServerSentEventMaker.create_sse_packet(
            #             ChatSSEEvent.PROGRESSION, chatSSEData
            #         )

            # message = messageBufferManager.get_joined_buffer()

            # 既存の会話か新しい会話かによってIDが変わる為、最終的に選択されるID
            resolved_conversation_id = None
            # 既存の会話
            if self.is_existing_conversation(conversation_id):
                self.chat_repository.update_conversation_message(
                    chat_message,
                    conversation_id,
                    MessageTypeEnum.HUMAN,
                )
                self.chat_repository.update_conversation_message(
                    message,
                    conversation_id,
                    MessageTypeEnum.ARTIFICIAL_INTELLIGENCE,  # todo: fix this
                )
                resolved_conversation_id = conversation_id
            else:
                # 新しい会話
                new_conversation_id = self.chat_repository.create_conversation_message(
                    chat_message, MessageTypeEnum.HUMAN
                )
                self.chat_repository.update_conversation_message(
                    message,
                    new_conversation_id,
                    MessageTypeEnum.ARTIFICIAL_INTELLIGENCE,
                )
                resolved_conversation_id = new_conversation_id

            chatSSEData = ChatSSEData(
                chat_content="", conversation_id=resolved_conversation_id
            )  # todo: fix this
            yield ServerSentEventMaker.create_sse_packet(
                ChatSSEEvent.COMPLETE, chatSSEData
            )
        except Exception as e:
            raise
