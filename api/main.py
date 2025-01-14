from fastapi import FastAPI
from routes import auth


app = FastAPI()

app.include_router(auth, prefix="/auth")


@app.get("/")
def main():
    return {"message": "success"}



