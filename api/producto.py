from fastapi import APIRouter, Depends, Form, UploadFile, File
from typing import Annotated
from dependencies.dependencies import get_product_service
from services.producto import ProductoService
from schemas.producto import ProductoResponse, ProductoCreate, producto_to_response


router = APIRouter(prefix="/producto", tags=["Producto"])


#Al parecer aquí no es obligatorio pasar el status_code ya que si todo sale bien te arroja el 200 de manera automática.
#Solamente tendríamos que estar atentos a manejarlos explicitamente cuando hayan excepciones.

# Traer todos los productos existentes.
@router.get("/", response_model=list[ProductoResponse])
async def get_all_products(service: ProductoService = Depends(get_product_service)):
    return [producto_to_response(producto) for producto in await service.get_all_products()]


#La idea es no hacerlo asi, aquí el mismo bucket dará el link para acceder a la foto pero la idea es que el bucket solo
#lo ocupemos para eliminar o subir cosas no para obtenerlas, ahi tendríamos que usar un cdn.

# Traer solo un producto.
@router.get("/{id}", response_model=ProductoResponse)
async def get_product_by_id(id:int, service: ProductoService = Depends(get_product_service)):
    return producto_to_response(await service.get_product_by_id(id))


# Publicar un producto.
@router.post("/", response_model=ProductoResponse)
async def create_product(
    nombre: Annotated[str, Form()],
    descripcion: Annotated[str, Form()],
    precio: Annotated[float, Form()],
    file: Annotated[UploadFile, File(...)],
    service: ProductoService = Depends(get_product_service),
):
    producto_create = ProductoCreate(
        nombre=nombre,
        descripcion=descripcion,
        precio=precio
    )
    return producto_to_response(await service.create_product(producto_create, file))

#Eliminar un producto.