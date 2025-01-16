from http.client import HTTPException
from fastapi import FastAPI
from starlette.responses import HTMLResponse, JSONResponse
from fastapi import FastAPI, Request, HTTPException
from routes import auth
from routes import users

app = FastAPI()

app.include_router(auth, prefix="/auth")
app.include_router(users, prefix="/api")


@app.get("/")
def main():
    return HTMLResponse(content=open("index.html").read(), status_code=200)


@app.get("/test")
async def auth_callback(request: Request):
    """Обработка данных из Telegram."""
    data = dict(request.query_params)

    return data
#     # Проверка подписи данных
#     # if not check_telegram_auth(data):
#     #     raise HTTPException(status_code=403, detail="Invalid authentication data")
#
#     # Проверка срока действия (должно быть меньше 24 часов)
#     # auth_date = data.get("auth_date")
#     # if not auth_date or time.time() - int(auth_date) > 86400:
#     #     raise HTTPException(status_code=403, detail="Authentication data expired")
#
#     # Успешная аутентификация
#     return JSONResponse(content={
#         "id": data.get("id"),
#         "first_name": data.get("first_name"),
#         "last_name": data.get("last_name"),
#         "username": data.get("username"),
#         "photo_url": data.get("photo_url"),
#     })

