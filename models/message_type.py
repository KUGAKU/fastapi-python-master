from enum import Enum
from sqlalchemy import Column, DateTime, Integer, String, func
from settings import Base


class MessageType(Base):
    __tablename__ = "message_type"

    message_type_id = Column(Integer, primary_key=True)
    message_type_name = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now())

    def __repr__(self):
        return "<MessageType('message_type_id={}, message_type_name={}, created_at={}, updated_at={}')>".format(
            self.message_type_id,
            self.message_type_name,
            self.created_at,
            self.updated_at,
        )


class MessageTypeEnum(Enum):
    HUMAN = 1
    ARTIFICIAL_INTELLIGENCE = 2
