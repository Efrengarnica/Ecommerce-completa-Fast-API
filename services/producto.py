from fastapi import UploadFile
from repository.producto import ProductoRepository
from models.producto import Producto
from schemas.producto import ProductoCreate
from infrastructure.s3_storage import upload_product_image


class ProductoService:
    def __init__(self, repository: ProductoRepository):
        self.repository = repository


    async def get_all_products(self) -> list[Producto]:
        return await self.repository.get_all_products()
    

    async def get_product_by_id(self, id:int) -> Producto:
        return await self.repository.get_product_by_id(id)
    
    
    async def create_product(self, producto_create: ProductoCreate, file: UploadFile) -> Producto:
        #Delego la verificación y el lanzado de excepciones a otros scripts.
        image_url = upload_product_image(file)

        producto_dict = producto_create.model_dump()
        producto_dict["ubicacion_imagen"] = image_url

        producto = Producto(**producto_dict)
        return await self.repository.create_product(producto)