import random
from fastapi import FastAPI
import requests
from services.db_service.UserService import create_user, update_status, get_user
from models.db.base import Base
from models.pydentic.auth_model import SendSms, Login, Verify
from services.db_service.otp_service import opt_create, otp_storage_time, validate_otp
from models.pydentic.registry_model import RegistryModel
from passlib.context import CryptContext

app = FastAPI()


APP_KEY = ""
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def send_sms(phone: str):
    random_code = random.randint(1000, 9999)
    opt_create(phone, random_code)
    requests.post(f"https://smspilot.ru/api.php?send={random_code}&to={phone}&apikey={APP_KEY}")


@app.post('/send-sms')
def send(data: SendSms):
    send_sms(data.phone)
    return {"message": "код успешно отправлен"}


@app.post('/veryfi-phone')
def veryfi_phone(data: Verify):
    if not validate_otp(data.phone, data.sms_code):
        return {"message": "неверный код"}

    if not otp_storage_time(data.phone, data.sms_code):
        return {"message": "время ожидания смс истекло"}

    if update_status(data.phone):
        return {"message": "ваш номер успешно верифицирован"}
    else:
        return {"message": "error"}


@app.get("/")
def main():
    print(Base.metadata.tables.keys())
    return {"message": "Hello World"}


@app.post("/registry")
def registry(data: RegistryModel):
    if get_user(data.phone):
        return {"message": "номер уже зарегестрирован !"}
    password = hash_password(data.password)
    create_user(data.phone, data.name, password, data.region)
    send_sms(data.phone)
    return {"message": "success"}


@app.post("/login")
def login(data: Login):
    user = get_user(data.phone)
    if not user:
        return {"message": "неверный номер телефона или пароль"}





