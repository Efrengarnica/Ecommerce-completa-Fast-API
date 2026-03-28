from fastapi import Request, status
from fastapi.responses import JSONResponse
from exceptions.ejemplo_exceptions import EjemploException

async def ejemplo_handler(request: Request, exc: EjemploException):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"estado":"error", "mensaje":exc.message}
    )