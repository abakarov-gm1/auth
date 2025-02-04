import os
import uuid
from typing import List
from starlette.responses import HTMLResponse, JSONResponse
from fastapi import FastAPI, Request, HTTPException, WebSocket, WebSocketDisconnect, Header
from fastapi.staticfiles import StaticFiles

from controllers.auth.refresh_token import decode_access_token
from services.message_service import create_message, get_last_message, get_all_messages
from routes import auth, auth_telegram, users, chat_router
from fastapi.middleware.cors import CORSMiddleware
from conf import UPLOAD_DIR


app = FastAPI()

origins = [
    "",
    "",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешаем запросы с этих доменов
    allow_credentials=True,
    allow_methods=["*"],  # Разрешаем все HTTP-методы
    allow_headers=["*"],  # Разрешаем все заголовки
)

app.include_router(auth, prefix="/auth")
app.include_router(users, prefix="/api")
app.include_router(auth_telegram, prefix="/telegram")
app.include_router(chat_router, prefix="/chat")
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")


@app.get("/")
def main():
    return HTMLResponse(content=open("index.html").read(), status_code=200)


@app.get("/test")
async def auth_callback(request: Request):
    data = dict(request.query_params)
    return data


@app.get("/q")
# async def get(token: str = Header(None)):
# async def get(token: str):
async def get():

    # if token is None:
    #     return {"message": "please add your token"}
    #
    # decode_token = dict(decode_access_token(token))
    #
    # if decode_token.get("error"):
    #     return {"message: token is invalid"}

    return HTMLResponse(content=open("chat.html").read(), status_code=200)


class ConnectionManager:

    def __init__(self):
        self.active_connections: List[WebSocket] = list()

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

    async def broadcast_file(self, file):
        for connection in self.active_connections:
            await connection.send_bytes(file)


manager = ConnectionManager()


@app.websocket("/ws/{chat_id}/{token}")
async def websocket_endpoint(websocket: WebSocket, chat_id: int, token: str):
    decode_data = dict(decode_access_token(token))

    if decode_data.get("error"):
        return  # Прерываем выполнение, клиент не будет добавлен в manager

    await manager.connect(websocket)

    try:

        messages = get_all_messages(chat_id)
        for message in messages:
            if message.file is not None:
                file_path = message.file
                try:
                    with open(file_path, "rb") as file:
                        file_bytes = file.read()
                        await websocket.send_bytes(file_bytes)
                except FileNotFoundError:
                    await websocket.send_text(f"Ошибка: файл {file_path} не найден")
            else:
                await websocket.send_text(f"{message.user.name}:  {message.text}")

        while True:
            try:

                data = await websocket.receive()

                if data.get("text"):
                    create_message(data.get("text"), decode_data.get("user_id"), chat_id)
                    message = get_last_message()
                    await manager.broadcast(f"{message.user.name}: {message.text}")

                if data.get("bytes"):
                    file_name = f"{uuid.uuid4().hex}.bin"
                    file_path = os.path.join(UPLOAD_DIR, file_name)
                    with open(file_path, "wb") as file:
                        file.write(data['bytes'])
                    create_message(text=None, user_id=decode_data.get("user_id"), chat_id=chat_id, file=file_path)
                    await manager.broadcast_file(data['bytes'])

            except Exception as e:
                print(e, ".../disconnected")
                manager.disconnect(websocket)
                return

    except WebSocketDisconnect as e:
        print(f"Client disconnected with code: {e.code}, reason: {e.reason}")
        manager.disconnect(websocket)

    except Exception as e:
        print(e, "message.user => not found")
        manager.disconnect(websocket)



