from fastapi import Request, status
from fastapi.responses import JSONResponse
from exceptions.producto import ProductoNoEncontrado, ProductoYaExistente, ProductoNoEncontradoNombre, ErrorAlBorrarArchivosBasura

# El request sirve para extraer mas info de la peticion que causo el error, es necesario que lo lleve aunque no se use.

# Producto no encontrado por medio del ID.
async def producto_no_encontrado(request: Request, exc: ProductoNoEncontrado):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "estado":"error",
            "mensaje":exc.mensaje
        }
    )

# Registrar un producto con nombre ya exitente en la base de datos.
async def producto_ya_existente(request: Request, exc: ProductoYaExistente):
    return JSONResponse(
        status_code= status.HTTP_409_CONFLICT,
        content = {
            "estado": "error",
            "mensaje":exc.mensaje
        }
    )

async def producto_no_encontrado_nombre(request: Request, exc: ProductoNoEncontradoNombre):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "estado":"error",
            "mensaje":exc.mensaje
        }
    )


async def error_al_borrar_archivos_basura(request: Request, exc: ErrorAlBorrarArchivosBasura):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "estado":"error",
            "mensaje":exc.mensaje
        }
    )