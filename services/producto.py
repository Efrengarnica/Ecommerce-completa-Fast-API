from fastapi import UploadFile
from repository.producto import ProductoRepository
from models.producto import Producto
from schemas.producto import ProductoCreate
from infrastructure.s3_storage import upload_product_image
from exceptions.producto import ProductoNoEncontrado, ProductoYaExistente, ProductoNoEncontradoNombre, ErrorAlBorrarArchivosBasura
from infrastructure.s3_storage import delete_image_from_s3
from sqlalchemy.exc import IntegrityError
from fastapi.concurrency import run_in_threadpool


class ProductoService:


    # Permite que mi ProductoService lleve consigo un repository.
    def __init__(self, repository: ProductoRepository):
        self.repository = repository


    # Obtiene todos los productos.
    async def get_all_products(self) -> list[Producto]:
        return await self.repository.get_all_products()
    

    # Obtiene el producto por medio del ID.
    async def get_product_by_id(self, id:int) -> Producto:
        producto = await self.repository.get_product_by_id(id)
        if producto is None:
            raise ProductoNoEncontrado(id)
        return producto
    
    
    # En este método se permite cierto margen de error, es decir habrá imagenes huerfanas y debemos de crear 
    # otro método que cada cierto tiempo limpie el bucket.
    async def create_product(self, producto_create: ProductoCreate, file: UploadFile) -> Producto:

        producto_existente = await self.repository.get_product_by_name(producto_create.nombre)

        if producto_existente:
            raise ProductoYaExistente(producto_create.nombre)
        
        image_url = await run_in_threadpool(upload_product_image, file)
        try:
            producto_dict = producto_create.model_dump()
            producto_dict["ubicacion_imagen"] = image_url
            producto = Producto(**producto_dict)
            return await self.repository.create_product(producto)
           
        except IntegrityError as e:
            try:
                await run_in_threadpool(delete_image_from_s3, image_url)
            except Exception as s3_err:
                print(f"Error limpiando S3: {s3_err}")
            raise ProductoYaExistente(producto_create.nombre)


    # Notar que el método permite que se queden registros en la BD ya eliminados, estos serán limpiados con otro método.
    async def delete_product_by_name(self, name: str) -> Producto:
        
        producto = await self.repository.get_product_by_name(name)
        if producto is None:
            raise ProductoNoEncontradoNombre(name)

        await self.repository.soft_delete(producto)
        
        await run_in_threadpool(delete_image_from_s3, producto.ubicacion_imagen)

        await self.repository.hard_delete(producto)
        
        return producto
    

    # Elimina los registros basura solo si pasa la autenticación del token.
    async def purge_deleted_products(self) -> int:
        try:
            return await self.repository.purge_deleted_products()
        except Exception as e:
            raise ErrorAlBorrarArchivosBasura()
        
    #To Do:

    # Método para editar

    # Método para limpiar las imagenes huerfanas del bucket.

    # Recoger las excepciones que lanzarán nuestros models create