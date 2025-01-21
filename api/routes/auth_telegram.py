from fastapi import APIRouter
from fastapi import Request
from controllers.auth_telegram.authenticate_telegram import authenticate


from services.user_service import update_status

router = APIRouter()


@router.get("/authentication")
def register(requests: Request):
    data = dict(requests.query_params)
    data_test = {
        "phone": "79280679861",
        "region": "russian",
        "password": "1122",
        "id": "1690141834",
        "first_name": "АГМ",
        "username": "abakarov_1",
        "auth_date": "1737408354",
        "hash": "8b86836a9d7f323c67c94f56550210e6cde51ad03c8f32c10b8aae0f8904eba7"
    }
    return authenticate(data_test)


@router.get("/phone-verify")
def phone_verify(requests: Request):
    data = dict(requests.query_params)
    status = update_status(data["phone"])
    if status:
        return "ваш номер успешно верифицирован !"
    return "ошибка: номер не верифицирован !"




