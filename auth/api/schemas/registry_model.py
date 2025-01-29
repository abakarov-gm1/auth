from pydantic import BaseModel


class RegistryModel(BaseModel):
    phone: str
    name: str
    password: str
    region: str

