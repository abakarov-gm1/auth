from fastapi import APIRouter

from models.pydentic.registry_model import RegistryModel
from use_cases.auth.registry import registry_cases

router = APIRouter()


@router.post("/registry")
def registry(data: RegistryModel):
    return registry_cases(data)
