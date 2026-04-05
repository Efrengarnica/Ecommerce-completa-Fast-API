from fastapi import APIRouter,Depends, Form, Response
from typing import Annotated
from services.auth import AuthService
from dependencies.dependencies import get_auth_service

router = APIRouter(prefix="/authentication", tags=["Authtentication"])

# Incio de sesión.
@router.post("/")
async def log_in(
    response: Response,
    email: Annotated[str, Form(...)],
    password: Annotated[str, Form(...)],
    service: AuthService = Depends(get_auth_service)
):

    token = await service.log_in(email, password)
    
    # Configuramos la Cookie segura
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=False,  # Cambiar a True en producción (HTTPS)
        samesite="lax",
        max_age=1800   # 30 minutos de vida
    )
    
    return {"message": "Has iniciado sesión correctamente"}