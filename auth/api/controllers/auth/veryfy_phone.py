import random
import requests

from services.otp_service import opt_create, validate_otp, otp_storage_time
from services.user_service import update_status
from conf import SMS_SERVICE_KEY


def send_sms(phone: str):
    random_code = random.randint(1000, 9999)
    opt_create(phone, random_code)
    requests.post(f"https://smspilot.ru/api.php?send={random_code}&to={phone}&apikey={SMS_SERVICE_KEY}")


def veryfi_phone_cases(data):
    if not validate_otp(data.phone, data.sms_code):
        return {"message": "неверный код"}

    if not otp_storage_time(data.phone, data.sms_code):
        return {"message": "время ожидания смс истекло"}

    if update_status(data.phone):
        return {"message": "ваш номер успешно верифицирован"}

    return {"message": "error"}
