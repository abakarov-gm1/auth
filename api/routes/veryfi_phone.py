from fastapi import APIRouter

from use_cases.auth.registry import send_sms

from models.pydentic.auth_model import Verify, SendSms
from use_cases.auth.veryfy_phone import veryfi_phone_cases

router = APIRouter()


@router.post('/send-sms')
def send(data: SendSms):
    send_sms(data.phone)
    return {"message": "код успешно отправлен"}


@router.post('/veryfi-phone')
def veryfi_phone(data: Verify):
    return veryfi_phone_cases(data)




