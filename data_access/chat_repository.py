from abc import ABC, abstractmethod

from models.conversation import Conversations
from models.message_type import MessageType, MessageTypeEnum
from models.messages import Messages

from settings import Session


class AbstractChatRepository(ABC):
    @abstractmethod
    def create_conversation_message(
        self, message: str, message_type: MessageTypeEnum
    ) -> str:
        raise NotImplementedError()

    def update_conversation_message(
        self, message: str, conversation_id: str, message_type: MessageTypeEnum
    ) -> str:
        raise NotImplementedError()


class ChatRepository(AbstractChatRepository):
    def create_conversation_message(
        self, message: str, message_type: MessageTypeEnum
    ) -> str:
        session = Session()
        conversation_id = ""
        try:
            conversations = Conversations()
            messages = Messages()
            message_type = (
                session.query(MessageType)
                .filter_by(message_type_id=message_type.value)
                .first()
            )

            session.add(conversations)
            session.flush()

            conversation_id = conversations.conversation_id
            messages.conversation_id = conversation_id
            messages.message_content = message
            messages.message_type_id = message_type.message_type_id
            session.add(messages)

            session.commit()
        except Exception as e:
            print(e)
            session.rollback()
            raise
        finally:
            session.close()
        return conversation_id

    def update_conversation_message(
        self, message: str, conversation_id: str, message_type: MessageTypeEnum
    ) -> str:
        session = Session()
        try:
            messages = Messages()
            message_type = (
                session.query(MessageType)
                .filter_by(message_type_id=message_type.value)
                .first()
            )

            messages.conversation_id = conversation_id
            messages.message_content = message
            messages.message_type_id = message_type.message_type_id
            session.add(messages)

            session.commit()

        except Exception as e:
            print(e)
            session.rollback()
            raise
        finally:
            session.close()
        return conversation_id
