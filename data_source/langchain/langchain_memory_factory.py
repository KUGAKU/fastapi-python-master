import os
from langchain.memory.chat_message_histories import SQLChatMessageHistory


class LangchainMemoryFactory:
    def __init__(self):
        pass

    def create_instance(self, conversation_id: str):
        return SQLChatMessageHistory(
            session_id=conversation_id,
            connection_string=os.environ.get(
                "DATABASE_CONNECTION_STRING", "sqlite:///db.sqlite3"
            ),
        )
