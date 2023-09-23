from abc import ABC, abstractmethod
from typing import Optional

from models.conversation import Conversations
from models.message_type import MessageType, MessageTypeEnum
from models.messages import Messages

from settings import Session


class AbstractChatRepository(ABC):
    @abstractmethod
    def upsert_conversation_message(
        self,
        conversation_id: str,
        message: str,
        message_type: MessageTypeEnum,
        message_token_count: int,
        consumed_token_count: int,
    ):
        raise NotImplementedError()


class ChatRepository(AbstractChatRepository):
    def upsert_conversation_message(
        self,
        conversation_id: str,
        message: str,
        message_type_enum: MessageTypeEnum,
        message_token_count: int,
        consumed_token_count: int,
    ):
        session = Session()
        try:
            messages = Messages()
            message_type = (
                session.query(MessageType)
                .filter_by(message_type_id=message_type_enum.value)
                .first()
            )
            if message_type is None:
                raise ValueError("Invalid message type")

            conversation = (
                session.query(Conversations)
                .filter_by(conversation_id=conversation_id)
                .first()
            )

            if conversation is None:  # 新しい会話データの作成
                conversations = Conversations()
                conversations.conversation_id = conversation_id
                messages.conversation_id = conversation_id
                messages.message_content = message
                messages.message_type_id = message_type.message_type_id
                messages.message_token_count = message_token_count
                messages.consumed_token_count = consumed_token_count
                session.add(conversations)
                session.add(messages)
            else:  # 既存の会話データの更新
                messages.conversation_id = conversation_id
                messages.message_content = message
                messages.message_type_id = message_type.message_type_id
                messages.message_token_count = message_token_count
                messages.consumed_token_count = consumed_token_count
                session.add(messages)

            session.commit()
        except Exception as e:
            print(e)
            session.rollback()
            raise
        finally:
            session.close()
        return
