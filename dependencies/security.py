from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError, ExpiredSignatureError
import os



admin_token = os.getenv("ADMIN_TOKEN")


# Instanciamos el esquema de seguridad
security = HTTPBearer()


async def validate_auth(credentials: HTTPAuthorizationCredentials = Depends(security)):

    token = credentials.credentials
    if token != admin_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o no proporcionado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token


# Me ayuda a poder obtener el id del usuario y comprobar que el token es válido y que la fecha de expiración sea válida
async def get_current_user_id(request: Request):
    token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(status_code=401, detail="No hay sesión activa")
    
    try:
        payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")])
        user_id = payload.get("sub")
        return user_id

    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="La sesión ha expirado")
        
    except JWTError:
        raise HTTPException(status_code=401, detail="Error de autenticación")