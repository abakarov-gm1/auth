import random
from fastapi import FastAPI
import requests
from models.pydentic.user_model import User

app = FastAPI()


# еще есть регистрация её отдельно вынесу в фйал как и авторизацию


@app.get("/")
def main():
    return {"message": "Hello World"}


@app.post("/send-sms")
def send_sms(user: User):
    # otp_record = db.session.query(OTPCode).filter_by(phone=phone).first()
    otp_record = ''
    if not otp_record:
        return False, "Неверный номер телефона"

    code = random.randint(1000, 9999)
    requests.post("отправить смс к номеру", user.phone)


@app.post("/auth")
def auth(user_data: User):
    pass
    # elif user_data.sms is not None and user_data.phone:
    #     pass


def validate_otp(phone, input_otp):
    # otp_record = db.session.query(OTPCode).filter_by(phone=phone).first()
    otp_record = ''
    if not otp_record:
        return False, "Неверный номер телефона"

    if otp_record.otp != input_otp:
        return False, "Неверный код OTP"

    if otp_record.expires_at < datetime.utcnow():
        return False, "Код OTP истек"

    return True, "OTP успешно подтвержден"


# d = requests.get("https://smspilot.ru/api.php?balance=rur&apikey=VJE190N841KGED5V624GD9EOFOB7XG89D819V56O1Y6B29P6I59792X991OGYY49")
# print(d.text)











