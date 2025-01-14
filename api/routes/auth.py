from fastapi import APIRouter

from controllers.auth.login import login_case
from controllers.auth.registry import registry_cases
from controllers.auth.veryfy_phone import send_sms, veryfi_phone_cases
from schemas.auth_model import Login, Verify, Refresh
from schemas.registry_model import RegistryModel
from schemas.auth_model import SendSms
from controllers.auth.refresh_token import refresh


router = APIRouter()


@router.post("/registry")
def registry(data: RegistryModel):
    return registry_cases(data)


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

