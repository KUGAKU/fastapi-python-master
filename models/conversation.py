import uuid
from sqlalchemy import UUID, Column, DateTime, String, func
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy.orm import relationship
from settings import Base


class Conversations(Base):
    __tablename__ = "conversations"

    conversation_id = Column(
        String,
        default=lambda: str(uuid.uuid4()),
        unique=True,
        nullable=False,
        primary_key=True,
    )
    conversation_title = Column(String, nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now())

    messages = relationship("Messages", back_populates="conversation")

    def __repr__(self):
        return "<Conversations('conversation_id={}, conversation_title={}, created_at={}, updated_at={}')>".format(
            self.conversation_id,
            self.conversation_title,
            self.created_at,
            self.updated_at,
        )
