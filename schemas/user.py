from pydantic import BaseModel
from typing import Optional
from schemas.enums import UserRole

class UserResponse(BaseModel):
    id: int
    imagen: Optional[str]
    nombre: str
    correo:str
    numero: str
    rol: UserRole
    model_config = {
        "from_attributes": True
    }

class UserCreate(BaseModel):
    imagen: Optional[str]=None
    nombre: str
    correo:str
    contrasena:str
    numero: str
    rol: UserRole

class UserRemovedResponse(BaseModel):
    correo:str
    mensaje:str="Usuario eliminado correctamente."
    model_config = {
    "from_attributes": True
    }

class UserCreatePut(BaseModel):
    imagen: Optional[str]=None
    nombre: Optional[str]=None
    correo:str
    contrasena:str
    numero: Optional[str]=None
    