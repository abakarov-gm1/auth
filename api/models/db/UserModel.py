from database import Base
from sqlalchemy import Column, Integer, String


class User(Base):

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=True)
    password = Column(String, nullable=False)
    balance = Column(Integer, nullable=False, default=0)
    subscription = Column(String, nullable=False)
    