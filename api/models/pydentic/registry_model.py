from pydantic import BaseModel


class RegistryModel(BaseModel):
    name: str
    password: str
    subscription: str

