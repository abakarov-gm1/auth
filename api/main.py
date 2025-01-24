from typing import List

import requests
from pydantic import BaseModel
from starlette.responses import HTMLResponse, JSONResponse
from fastapi import FastAPI, Request, HTTPException, WebSocket, WebSocketDisconnect

from services.chat_service import add_users_to_chat_service, get_users_from_chat_service
from services.message_service import create_message, get_last_message, get_all_messages
from services.user_service import create_user, get_user_service
from routes import auth, auth_telegram, users, chat_router

app = FastAPI()

app.include_router(auth, prefix="/auth")
app.include_router(users, prefix="/api")
app.include_router(auth_telegram, prefix="/telegram")
app.include_router(chat_router, prefix="/chat")


@app.get("/")
def main():
    return HTMLResponse(content=open("index.html").read(), status_code=200)


@app.get("/test")
async def auth_callback(request: Request):
    """Обработка данных из Telegram."""
    data = dict(request.query_params)
    return data


html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/ws/1");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@app.get("/q")
async def get():
    return HTMLResponse(html)


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


manager = ConnectionManager()


@app.websocket("/ws/{chat_id}")
async def websocket_endpoint(websocket: WebSocket, chat_id: int):
    await manager.connect(websocket)
    # i_am_user = get_user_service(1)
    # users_ = get_users_from_chat_service(chat_id)

    # if i_am_user in users_:
    #     # тут если не будет возвращаем ошибку
    #     pass


    # chat = get_chat_service(chat_id)

    try:
        messages = get_all_messages(chat_id)
        for message in messages:
            await websocket.send_text(f"{message.user.name}:  {message.text}")

        while True:
            data = await websocket.receive_text()
            create_message(data, 3, chat_id)
            message = get_last_message()
            await manager.broadcast(f"{message.user.name}: {message.text}")

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"User disconnected from chat {chat_id}")


@app.get("/ggg")
def ggg():
    return get_last_message()


@app.post("/add-user-in-chat")
def ggg():
    add_users_to_chat_service(1, 4)
    return "ok"


@app.get("/users-from-chat")
def ggg():
    return get_users_from_chat_service(1)








