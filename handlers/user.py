from fastapi import Request, status
from fastapi.responses import JSONResponse
from exceptions.user import UsuarioNoEncontrado

async def usuario_no_encontrado(request: Request, exc: UsuarioNoEncontrado):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "estado":"error",
            "mensaje":exc.mensaje
        }
    )
