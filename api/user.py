from fastapi import APIRouter, Query, Depends, Form
from typing import Annotated
from services.user import UserService
from schemas.user import UserResponse, UserCreate, UserRemovedResponse
from dependencies.dependencies import get_user_service
from dependencies.security import get_current_user_id

router = APIRouter(prefix="/user", tags=["Usuario"])


# Por lo que entendí no se le debe de estar pidiendo info sensible a cada rato al usuario.
# La idea es que haya un router que pida info del usuario para devolverle un token y guardarlo en una cookie.
# Ese token será usado para la mayoría de los routers pero algunos sí pedirán además del token info del usuario.


# Conseguir User
@router.get("/", response_model = UserResponse)
async def get_user_by_id(
    id:str = Depends(get_current_user_id),
    service:UserService=Depends(get_user_service)
    ):
    return await service.get_user_by_id(int(id))


# Crear un User
@router.post("/",response_model = UserResponse | None)
async def create_user(userCreate:UserCreate, service:UserService=Depends(get_user_service)):
    return await service.create_user(userCreate)


# Eliminar un User
@router.delete("/", response_model= UserRemovedResponse | None)
async def delete_user(
    email:Annotated[str, Form(...)], 
    contrasena:Annotated[str, Form(...)],
    service:UserService=Depends(get_user_service)
):
    return await service.delete_user(email, contrasena)

# Modificar un User

# En los services y repository tengo que el constructor se escribe de manera sync, no afecta para mi app async.