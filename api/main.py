from fastapi import FastAPI
from routes import login, registry, veryfi_


app = FastAPI()

app.include_router(login, prefix="/auth")
app.include_router(registry, prefix="/auth")
app.include_router(veryfi_, prefix="/auth")


@app.get("/")
def main():
    return {"message": "success"}



