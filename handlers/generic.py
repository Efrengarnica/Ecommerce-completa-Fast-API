from fastapi import Request, status
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException
from fastapi.exceptions import RequestValidationError


# Recuerda que es async ya que esta función puede ser llamada muchas veces.
async def custom_404_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"status": "error", "message": str(exc.detail)}
    )


# Me sirve para manejar los RequestValidationError.
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errores = []
    for err in exc.errors():
        campo = ".".join(str(x) for x in err["loc"] if x != "body")
        errores.append({
            "campo": campo,
            "mensaje": err["msg"]
        })

    return JSONResponse(
        status_code=422,
        content={
            "ok": False,
            "mensaje": "Hay errores en los datos enviados.",
            "errores": errores
        }
    )