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


class ResetPassword(BaseModel):
    phone: str
    new_password: str
    confirm_password: str
