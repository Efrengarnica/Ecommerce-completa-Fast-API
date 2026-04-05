from fastapi import Request, status
from fastapi.responses import JSONResponse
from exceptions.auth import NotAuthorization

# Producto no encontrado por medio del ID.
async def claves_incorrectas(request: Request, exc: NotAuthorization):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={
            "estado":"error",
            "mensaje":exc.mensaje
        }
    )