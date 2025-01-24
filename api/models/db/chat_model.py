from models.db.base import Base
from sqlalchemy import Column, BigInteger, String
from sqlalchemy.orm import relationship


class Chat(Base):
    __tablename__ = 'chat'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String)

    users = relationship("User", secondary='chat_users', back_populates="chats")
    messages = relationship("MessageModel", back_populates="chat")

