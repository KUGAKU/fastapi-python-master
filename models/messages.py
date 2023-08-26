import uuid
from sqlalchemy import UUID, Column, DateTime, ForeignKey, String, func
from sqlalchemy.orm import relationship
from settings import Base


class Messages(Base):
    __tablename__ = "messages"

    message_id = Column(
        String,
        default=lambda: str(uuid.uuid4()),
        unique=True,
        nullable=False,
        primary_key=True,
    )
    message_content = Column(String)
    conversation_id = Column(String, ForeignKey("conversations.conversation_id"))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now())

    conversation = relationship("Conversations", back_populates="messages")

    def __repr__(self):
        return "<Messages('message_id={}, message_content={}, conversation_id={}, created_at={}, updated_at={}')>".format(
            self.message_id,
            self.message_content,
            self.conversation_id,
            self.created_at,
            self.updated_at,
        )
