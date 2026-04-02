from fastapi import Request, status
from fastapi.responses import JSONResponse
from exceptions.ejemplo_exceptions import EjemploException
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
# Maneja la excepcion EjemploException
""" async def ejemplo_handler(request: Request, exc: EjemploException):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"estado":"error", "mensaje":exc.message}
    ) """

#Maneja la exception que lanza FastAPI cuando el formato de mis DTO son incorrectos y les da un formato más entendible.
""" async def manejar_errores_validacion(request: Request, exc: RequestValidationError):
    errores_personalizados = []

    for error in exc.errors():
        # Por defecto tomamos el nombre del campo de la ubicación del error
        campo = error["loc"][-1]
        mensaje = error["msg"]

        # 1. Verificamos si es un error manual (ValueError)
        if "ctx" in error and "error" in error["ctx"]:
            exception_original = error["ctx"]["error"]
            
            # Si el error tiene argumentos (la tupla que enviamos)
            if hasattr(exception_original, "args") and len(exception_original.args) == 2:
                # Aquí recuperamos: ("nombre", "El mensaje...")
                campo_desde_dto, mensaje_desde_dto = exception_original.args
                campo = campo_desde_dto
                mensaje = mensaje_desde_dto
            else:
                # Si no es tupla, al menos limpiamos el prefijo "Value error, "
                mensaje = mensaje.replace("Value error, ", "")

        # 2. Traducciones para errores automáticos de Pydantic
        elif "Input should be a valid integer" in mensaje:
            mensaje = f"El campo {campo} debe ser un número entero"
        elif "Field required" in mensaje:
            mensaje = f"El campo {campo} es obligatorio"

        errores_personalizados.append({
            "campo": campo,
            "mensaje": mensaje
        })

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "estado": "error",
            "mensaje": "Errores de validación",
            "errores": errores_personalizados
        },
    )


async def validation_exception_handler(request: Request, exc: ValidationError):
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


 """


#Formatos importantes que me ayudan a entender lo de arriba
""" 
{
    "type": "value_error",
    "loc": ["body", "id"],
    "msg": "Value error, ('id', 'El id debe ser mayor que cero')",
    "input": -5,
    "ctx": {
        "error": ValueError("id", "El id debe ser mayor que cero")
    },
    "url": "https://errors.pydantic.dev/2.6/v/value_error"
}

{
    "loc": ["body", "id"],
    "msg": "Value error, El id debe ser mayor que cero",  <--- ¡Ojo aquí!
    "type": "value_error"
}

 """