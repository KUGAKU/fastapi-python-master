import uuid
from sqlalchemy import UUID, Column, DateTime, ForeignKey, Integer, String, func
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
    conversation = relationship("Conversations", back_populates="messages")

    message_type_id = Column(Integer, ForeignKey("message_type.message_type_id"))
    message_type = relationship("MessageType", backref="messages")

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now())

    def __repr__(self):
        return "<Messages('message_id={}, message_content={}, conversation_id={}, message_type_id={}, message_type={}, created_at={}, updated_at={}')>".format(
            self.message_id,
            self.message_content,
            self.conversation_id,
            self.message_type_id,
            self.message_type,
            self.created_at,
            self.updated_at,
        )
