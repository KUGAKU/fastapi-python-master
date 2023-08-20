from abc import ABC, abstractmethod

from models.conversation import Conversations
from models.messages import Messages

from settings import Session


class AbstractChatRepository(ABC):
    @abstractmethod
    def create_conversation_message(self, message: str) -> str:
        raise NotImplementedError()

    def update_conversation_message(self, message: str, conversation_id: str) -> str:
        raise NotImplementedError()


class ChatRepository(AbstractChatRepository):
    def create_conversation_message(self, message: str) -> str:
        session = Session()
        conversation_id = ""
        try:
            conversations = Conversations()
            messages = Messages()

            session.add(conversations)
            session.flush()

            conversation_id = conversations.conversation_id
            messages.conversation_id = conversation_id
            messages.message_content = message
            session.add(messages)

            session.commit()
        except Exception as e:
            print(e)
            session.rollback()
            raise
        finally:
            session.close()
        return conversation_id

    def update_conversation_message(self, message: str, conversation_id: str) -> str:
        session = Session()
        try:
            messages = Messages()

            messages.conversation_id = conversation_id
            messages.message_content = message
            session.add(messages)

            session.commit()

        except Exception as e:
            print(e)
            session.rollback()
            raise
        finally:
            session.close()
        return conversation_id
