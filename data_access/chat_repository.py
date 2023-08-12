from abc import ABC, abstractmethod

import openai


class AbstractChatRepository(ABC):
    @abstractmethod
    def create_message(self):
        raise NotImplementedError()


class ChatRepository(AbstractChatRepository):
    def create_message(self):
        pass
