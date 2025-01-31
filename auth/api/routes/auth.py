from fastapi import APIRouter, Form, UploadFile, File
from controllers.auth.login import login_case
from controllers.auth.registry import registry_cases
from controllers.auth.veryfy_phone import send_sms, veryfi_phone_cases
from schemas.auth_model import Login, Verify, Refresh
from schemas.auth_model import SendSms
from controllers.auth.refresh_token import refresh
from typing import Optional
from schemas.auth_model import ResetPassword
from controllers.auth.reset_password import reset_passwd

router = APIRouter()


@router.post("/registry")
def registry(
    phone: Optional[str] = Form(None),
    name: Optional[str] = Form(None),
    password: Optional[str] = Form(None),
    region: Optional[str] = Form(None),
    photo: Optional[UploadFile] = File(None)
):
    return registry_cases(phone=phone, name=name, password=password, region=region, photo=photo)


@router.post("/login")
def login(data: Login):
    return login_case(data)


@router.post('/send-sms')
def send(data: SendSms):
    send_sms(data.phone)
    return {"message": "код успешно отправлен"}


@router.post('/veryfi-phone')
def veryfi_phone(data: Verify):
    return veryfi_phone_cases(data)


@router.post("/refresh-token")
def refresh_token(data: Refresh):
    return refresh(data)


@router.post("/reset-password")
def reset_password(data: ResetPassword):
    return reset_passwd(data)
