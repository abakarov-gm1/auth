from pydantic import BaseModel


class SendSms(BaseModel):
    phone: str


class Login(BaseModel):
    phone: str
    sms_code: int

