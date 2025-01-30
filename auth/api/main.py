import os
import uuid
from typing import List
from starlette.responses import HTMLResponse, JSONResponse
from fastapi import FastAPI, Request, HTTPException, WebSocket, WebSocketDisconnect
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


# html = """
# <!DOCTYPE html>
# <html>
#     <head>
#         <title>Chat</title>
#     </head>
#     <body>
#         <h1>WebSocket Chat</h1>
#         <form action="" onsubmit="sendMessage(event)">
#             <input type="file" id="messageText" autocomplete="off"/>
#             <button>Send</button>
#         </form>
#
#         <ul id='messages'>
#         </ul>
#         <script>
#             // Ждем, пока страница полностью загрузится
#
#             var token = localStorage.getItem('token');
#
#             var ws = new WebSocket("ws://localhost:8000/ws/1/" + token);
#
#             ws.onmessage = function(event) {
#                 var messages = document.getElementById('messages');
#                 var message = document.createElement('li');
#                 var content = document.createTextNode(event.data);
#                 message.appendChild(content);
#                 messages.appendChild(message);
#             };
#
#
#             // Функция отправки сообщений
#             function sendMessage(event) {
#                var input = document.getElementById("messageText")
#                 ws.send(input.value)
#                 input.value = ''
#                 event.preventDefault()
#             }
#
#
#         </script>
#     </body>
# </html>
# """


# html = '''
# <!DOCTYPE html>
# <html>
#     <head>
#         <title>Chat</title>
#     </head>
#     <body>
#         <h1>WebSocket Chat</h1>
#
#         <form action="" onsubmit="sendMessage(event)">
#             <input type="file" id="messageFile" autocomplete="off"/>
#             <button>Send</button>
#         </form>
#
#         <form action="" onsubmit="sendMessageText(event)">
#             <input type="text" id="messageText" autocomplete="off"/>
#             <button>Send</button>
#         </form>
#
#         <ul id="messages"></ul>
#
#         <script>
#             // Получаем токен
#             var token = localStorage.getItem("token");
#
#             // Открываем WebSocket-соединение
#             var ws = new WebSocket("ws://localhost:8000/ws/1/" + token);
#
#             ws.onmessage = function(event) {
#                 var messages = document.getElementById("messages");
#                 var message = document.createElement("li");
#
#                 // Если сервер отправляет бинарные данные (например, изображение)
#                 if (event.data instanceof Blob) {
#                     var blobUrl = URL.createObjectURL(event.data); // Создаём URL для бинарных данных
#                     var img = document.createElement("img");
#                     img.src = blobUrl;
#                     img.style.maxWidth = "300px"; // Задаём ограничение размера изображения
#                     message.appendChild(img);
#                 } else {
#                     // Если сервер отправляет текстовые данные
#                     var content = document.createTextNode(event.data);
#                     message.appendChild(content);
#                 }
#
#                 messages.appendChild(message);
#             };
#
#             function sendMessageText(event) {
#                  var input = document.getElementById("messageText")
#                  ws.send(input.value)
#                  input.value = ''
#                  event.preventDefault()
#             }
#
#             // Функция отправки файлов через WebSocket
#             function sendMessage(event) {
#                 event.preventDefault();
#
#                 var input = document.getElementById("messageFile");
#                 var file = input.files[0]; // Получаем первый файл из инпута
#                 console.log(file)
#                 if (file) {
#                     var reader = new FileReader();
#
#                     reader.onload = function() {
#                         ws.send(reader.result); // Отправляем бинарные данные файла
#                 };
#
#                     reader.readAsArrayBuffer(file); // Читаем файл как бинарные данные
#                 } else {
#                     alert("Выберите файл для отправки.");
#                 }
#
#                 input.value = ""; // Сбрасываем поле выбора файла
#             }
#         </script>
#     </body>
# </html>
#
# '''
#
#
# @app.get("/q")
# def get():
#     return HTMLResponse(html)
#
#
# class ConnectionManager:
#
#     def __init__(self):
#         self.active_connections: List[WebSocket] = list()
#
#     async def connect(self, websocket: WebSocket):
#         await websocket.accept()
#         self.active_connections.append(websocket)
#
#     def disconnect(self, websocket: WebSocket):
#         self.active_connections.remove(websocket)
#
#     async def send_message(self, message: str, websocket: WebSocket):
#         await websocket.send_text(message)
#
#     async def broadcast(self, message: str):
#         for connection in self.active_connections:
#             try:
#                 await connection.send_text(message)
#             except WebSocketDisconnect:
#                 self.active_connections.remove(connection)
#         # for connection in self.active_connections:
#         #     await connection.send_text(message)
#
#     async def broadcast_file(self, file_url: str):
#         for connection in self.active_connections:
#             await connection.send_text(f"FILE: {file_url}")
#
#
# manager = ConnectionManager()
#
#
# @app.websocket("/ws/{chat_id}/{token}")
# async def websocket_endpoint(websocket: WebSocket, chat_id: int, token: str):
#
#     await manager.connect(websocket)
#     decode_data = dict(decode_access_token(token))
#
#     while True:
#         data = await websocket.receive_text()
#         print(data, "sssssssssss")
#
#         #    data = await websocket.receive_bytes()
#         # await websocket.send_bytes(data)
#         # if data.get("text"):
#         #     # data = await websocket.receive_text()
#         #     # create_message(data, decode_data.get("user_id"), chat_id)
#         #     # message = get_last_message()
#         #     # await manager.broadcast(f"{message.user.name}: {message.text}")
#         #
#         #     await manager.broadcast(f"{data.get('text')}")
#         #
#
#     # try:
#
#         # тут надо отдельно обрабатывать медиа файлы это в конце сделаю
#         # messages = get_all_messages(chat_id)
#         #
#         # for message in messages:
#         #     await websocket.send_text(f"{message.user.name}:  {message.text}")
#
#     # while True:
#     #     data = await websocket.receive()
#     #     print(data, "sssssssssss")
#     #
#     #     #    data = await websocket.receive_bytes()
#     #     # await websocket.send_bytes(data)
#     #     if data.get("text"):
#     #         # data = await websocket.receive_text()
#     #         # create_message(data, decode_data.get("user_id"), chat_id)
#     #         # message = get_last_message()
#     #         # await manager.broadcast(f"{message.user.name}: {message.text}")
#     #         new_data = dict(data)
#     #         await manager.broadcast(f"{data.get('text')}")
#
#     # except WebSocketDisconnect:
#     #     manager.disconnect(websocket)
#     #     await manager.broadcast(f"User disconnected from chat {chat_id}")















#
#
# @app.get("/ggg")
# def ggg():
#     return get_last_message()
#
#
# @app.post("/add-user-in-chat")
# def ggg():
#     add_users_to_chat_service(1, 4)
#     return "ok"
#
#
# @app.get("/users-from-chat")
# def ggg():
#     return get_users_from_chat_service(1)



























































# html = '''
# <!DOCTYPE html>
# <html>
#     <head>
#         <title>Chat</title>
#     </head>
#     <body>
#         <h1>WebSocket Chat</h1>
#
#         <form action="" onsubmit="sendMessage(event)">
#             <input type="file" id="messageFile" autocomplete="off"/>
#             <button>Send</button>
#         </form>
#
#         <form action="" onsubmit="sendMessageText(event)">
#             <input type="text" id="messageText" autocomplete="off"/>
#             <button>Send</button>
#         </form>
#
#         <ul id="messages"></ul>
#
#         <script>
#             // Получаем токен
#             var token = localStorage.getItem("token");
#             var ws;
#
#             function openWebSocket() {
#
#                 var ws = new WebSocket("ws://localhost:8000/ws/1/" + token);
#
#
#                 ws.onopen = function() {
#                     console.log("WebSocket соединение открыто.");
#                 };
#
#                 ws.onmessage = function(event) {
#                     var messages = document.getElementById("messages");
#                     var message = document.createElement("li");
#
#                     // Если сервер отправляет бинарные данные (например, изображение)
#                     if (event.data instanceof Blob) {
#                         var blobUrl = URL.createObjectURL(event.data); // Создаём URL для бинарных данных
#                         var img = document.createElement("img");
#                         img.src = blobUrl;
#                         img.style.maxWidth = "300px"; // Задаём ограничение размера изображения
#                         message.appendChild(img);
#                     } else {
#                         // Если сервер отправляет текстовые данные
#                         var content = document.createTextNode(event.data);
#                         message.appendChild(content);
#                     }
#
#                     messages.appendChild(message);
#                 };
#
#                 ws.onerror = function(error) {
#                     console.error("Ошибка WebSocket: ", error);
#                 };
#
#                 ws.onclose = function(event) {
#                     console.log("WebSocket соединение закрыто. Попытка переподключения...");
#                     setTimeout(openWebSocket, 2000);  // Попытка переподключиться через 3 секунды
#                 };
#
#                 return ws;
#             }
#
#             var ws = openWebSocket()
#
#             //ws.onclose = function(event) {
#             //    console.log("WebSocket соединение закрыто. Попытка переподключения...");
#             //    setTimeout(openWebSocket, 2000);  // Попытка переподключиться через 3 секунды
#             //};
#
#
#             // Открываем WebSocket-соединение
#             function sendMessageText(event) {
#                  var input = document.getElementById("messageText")
#                  if (ws.readyState === WebSocket.OPEN) {
#                      ws.send(input.value);
#                      input.value = '';
#                      event.preventDefault()
#                  }else {
#                      console.error("WebSocket соединение не открыто.");
#                  }
#
#                  //ws.send(input.value)
#                  //input.value = ''
#                  //event.preventDefault()
#             }
#
#             // Функция отправки файлов через WebSocket
#             function sendMessage(event) {
#                 event.preventDefault();
#
#                 var input = document.getElementById("messageFile");
#                 var file = input.files[0]; // Получаем первый файл из инпута
#                 console.log(file)
#
#                 if (file && ws.readyState === WebSocket.OPEN) {
#                     var reader = new FileReader();
#
#                 reader.onload = function () {
#                     if (file.type.startsWith("image/")) {
#                         console.log("Отправка изображения...");
#                     } else if (file.type.startsWith("video/")) {
#                         console.log("Отправка видео...");
#                     } else {
#                         console.log("Отправка другого файла...");
#                     }
#                     ws.send(reader.result);
#                 };
#
#                 reader.readAsArrayBuffer(file);
#                 } else if (!file) {
#                     alert("Выберите файл для отправки.");
#                 } else {
#                     console.error("WebSocket соединение не открыто.");
#                 }
#
#                 input.value = "";
#             }
#         </script>
#     </body>
# </html>
#
# '''


@app.get("/q")
async def get():
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
    await manager.connect(websocket)

    decode_data = dict(decode_access_token(token))

    try:

        messages = get_all_messages(chat_id)
        for message in messages:
            if message.photo is not None:
                file_path = message.photo
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
                    create_message(text=None, user_id=decode_data.get("user_id"), chat_id=chat_id, photo=file_path)
                    await manager.broadcast_file(data['bytes'])

                    # await websocket.send_text(file_path)

            except Exception as e:
                print(e, ".../disconnected")
                manager.disconnect(websocket)
                return

    except WebSocketDisconnect as e:
        print(f"Client disconnected with code: {e.code}, reason: {e.reason}")
        manager.disconnect(websocket)








