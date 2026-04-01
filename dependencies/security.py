from fastapi import Depends, HTTPException, status, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
load_dotenv()
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