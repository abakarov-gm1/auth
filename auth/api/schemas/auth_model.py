from pydantic import BaseModel


class SendSms(BaseModel):
    phone: str


class Verify(BaseModel):
    phone: str
    sms_code: int


class Login(BaseModel):
    phone: str
    password: str


class Refresh(BaseModel):
    user_id: int
    access_token: str
    refresh_token: str


