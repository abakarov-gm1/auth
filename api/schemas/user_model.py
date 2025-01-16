from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    phone: str
    sms: str


class UpdateUser(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    balance: Optional[int] = None
    region: Optional[str] = None


class UpdateBalance(BaseModel):
    balance: int


class Subscription(BaseModel):
    subscription: str
