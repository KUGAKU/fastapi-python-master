from injector import Module
from business_logic.chat_service import AbstractChatService, ChatService

from data_access.chat_repository import AbstractChatRepository, ChatRepository


class ChatDi(Module):
    def configure(self, binder):
        binder.bind(AbstractChatRepository, to=ChatRepository)
        binder.bind(AbstractChatService, to=ChatService)
