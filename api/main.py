import random
from fastapi import FastAPI
import requests
from services.db_service.UserService import create_user, update_status
from models.db.base import Base
from models.pydentic.auth_model import SendSms, Login
from services.db_service.opt_service import opt_create, otp_storage_time, validate_otp
from models.pydentic.registry_model import RegistryModel

app = FastAPI()


# еще есть регистрация её отдельно вынесу в фйал как и авторизацию
APP_KEY = "VJE190N841KGED5V624GD9EOFOB7XG89D819V56O1Y6B29P6I59792X991OGYY49"


@app.post('/send-sms')
def send_sms(data: SendSms):
    random_code = random.randint(1000, 9999)
    opt_create(data.phone, random_code)
    requests.post(f"https://smspilot.ru/api.php?send={random_code}&to={data.phone}&apikey={APP_KEY}")
    return {"message": "код успешно отправлен"}


@app.post('/veryfi-phone')
def veryfi_phone(data: Login):
    if not validate_otp(data.phone, data.sms_code):
        return {"message": "неверный код или номер телефона"}

    if not otp_storage_time(data.phone, data.sms_code):
        return {"message": "время ожидания смс истекло"}

    update_status(data.phone)
    return {"message": "вы успешно авторизованны"}


@app.get("/")
def main():
    print(Base.metadata.tables.keys())
    return {"message": "Hello World"}


@app.post("/registry")
def registry(data: RegistryModel):
    passwd = "test"
    create_user(data.name, passwd, data.subscription)
    return {"message": "success"}














