from injector import Module
from business_logic.chat_service import AbstractChatService, ChatService

from data_access.chat_repository import AbstractChatRepository, ChatRepository
from data_source.openai_data_source import AbstractOpenaiDataSource, OpenaiDataSource


class ChatDi(Module):
    def configure(self, binder):
        binder.bind(AbstractChatRepository, to=ChatRepository)
        binder.bind(AbstractChatService, to=ChatService)
        binder.bind(AbstractOpenaiDataSource, to=OpenaiDataSource)
