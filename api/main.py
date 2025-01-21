import requests
from starlette.responses import HTMLResponse, JSONResponse
from fastapi import FastAPI, Request, HTTPException

from services.user_service import create_user
from routes import auth, auth_telegram, users

app = FastAPI()

app.include_router(auth, prefix="/auth")
app.include_router(users, prefix="/api")
app.include_router(auth_telegram, prefix="/telegram")


@app.get("/")
def main():
    return HTMLResponse(content=open("index.html").read(), status_code=200)


@app.get("/test")
async def auth_callback(request: Request):
    """Обработка данных из Telegram."""
    data = dict(request.query_params)
    return data


@app.get("/f")
async def auth_callback(request: Request):

    data_test = {
        "phone": "79280679861",
        "region": "russian",
        "password": "1122",
        "id": "1690141834",
        "first_name": "АГМ",
        "username": "abakarov_5",
        "auth_date": "1737408354",
        "hash": "8b86836a9d7f323c67c94f56550210e6cde51ad03c8f32c10b8aae0f8904eba7"
    }

    create_user(name=data_test["first_name"], telegram_id=data_test["id"], telegram_username=data_test["username"])
    return data_test



















@app.post("/teleg")
def post_telegram():
    BOT_TOKEN = "7866999033:AAHIDFptopNsvFBc00DXKvM7dPc0Q_gkL0Y"
    CHAT_ID = "7866999033"
    MESSAGE = "/start"
    URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": MESSAGE
    }
    response = requests.post(URL, data=payload)
    if response.status_code == 200:
        print("Сообщение отправлено успешно!")
    else:
        print(f"Ошибка отправки сообщения: {response.status_code}, {response.text}")

