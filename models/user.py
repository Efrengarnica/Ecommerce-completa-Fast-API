from sqlmodel import SQLModel, Field
from typing import Optional
from schemas.enums import UserRole

class User(SQLModel, table=True):
    id:Optional[int] = Field(default=None, primary_key=True)
    imagen: Optional[str]
    nombre: str
    correo:str = Field(index=True, unique=True)
    contrasena:str
    numero: str
    rol: UserRole =Field(default=UserRole.CUSTOMER)# El default solo sirve para cuando creas instancias en python no para 
    #la base de datos.