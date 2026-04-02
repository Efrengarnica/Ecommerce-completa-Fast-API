from fastapi import APIRouter, Depends, Form, UploadFile, File, Query, status
from fastapi.responses import JSONResponse
from typing import Annotated, Optional
from dependencies.dependencies import get_product_service
from dependencies.security import validate_auth
from services.producto import ProductoService
from schemas.producto import ProductoResponse, ProductoCreate, producto_to_response, ProductoEliminadoResponse, ProductoCreatePut


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
    file: Annotated[UploadFile, File(...)],
    producto: ProductoCreate = Depends(ProductoCreate.as_form),
    service: ProductoService = Depends(get_product_service)
):
    return producto_to_response(await service.create_product(producto, file))


# Eliminar un producto.
@router.delete("/", response_model=ProductoEliminadoResponse)
async def delete_product_by_name(nombre:str = Query(..., description="Nombre de la imagen"), service:ProductoService = Depends(get_product_service)):
    return await service.delete_product_by_name(nombre)


# Modificar un producto.
@router.put("/", response_model=ProductoResponse)
async def modified_product(
    file: Annotated[Optional[UploadFile], File(...)]=None,
    producto: ProductoCreatePut = Depends(ProductoCreatePut.as_form),
    service:ProductoService=Depends(get_product_service)
):
    producto = await service.modified_product(producto, file)
    return producto_to_response(producto)


# Este enpoint es para realizar la limpieza de la BD de registros basura.
# Debe de llevar un token para que pueda ser ejecutado.
@router.post("/limpieza")
async def clean_database(
    service: ProductoService = Depends(get_product_service),
    _token: str = Depends(validate_auth)
):
    count = await service.purge_deleted_products()
    
    return {
        "status": "success",
        "message": f"Se han eliminado permanentemente {count} productos.",
        "action": "HARD_DELETE_CLEANUP"
    }


#Vamos a hacer el enpoint que limpie cosas del bucket
@router.post("/limpieza/bucket")
async def clean_bucket_s3(
    service:ProductoService=Depends(get_product_service),
    _token:str=Depends(validate_auth)
):
    deleted_elements=await service.clean_bucket_s3()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "status":"success",
            "message":f"Se eliminaron correctamente: {deleted_elements} elementos basura del bucket.",
            "action": "HARD_DELETE_CLEANUP_S3"
        }
    )