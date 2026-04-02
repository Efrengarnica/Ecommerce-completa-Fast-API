from fastapi import UploadFile
from repository.producto import ProductoRepository
from models.producto import Producto
from schemas.producto import ProductoCreate, ProductoCreatePut
from infrastructure.s3_storage import upload_product_image
from exceptions.producto import ProductoNoEncontrado, ProductoYaExistente, ProductoNoEncontradoNombre, ErrorAlBorrarArchivosBasura
from infrastructure.s3_storage import delete_image_from_s3, delete_all_trash_s3
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
    

    # Método para modificar un producto.
    async def modified_product(self, producto_create: ProductoCreatePut, file: UploadFile = None) -> Producto:
        busqueda = await self.repository.get_product_by_id(producto_create.id)
        if not busqueda:
            raise ProductoNoEncontrado(producto_create.id)
    
        if file:
            imagen_vieja=busqueda.ubicacion_imagen
            image_url = await run_in_threadpool(upload_product_image, file)
        else:
            image_url = busqueda.ubicacion_imagen

        datos_nuevos = producto_create.model_dump(exclude_none=True)

        for campo, valor in datos_nuevos.items():
            setattr(busqueda, campo, valor)

        busqueda.ubicacion_imagen = image_url

        try:
            #Ocupo create, es una mala práctica pero para que entienda que al modificar un objeto hace que 
            # cuando haga commit ese objeto sigue siendo el mismo y por ende la BD no se queja y apesar de que 
            # le pase el parámetro id y nombre iguales no lo toma como una creacion nueva y no lanza la excepcion
            # ya que detecta que es el mismo objeto el que esta ingresando.
            producto_a_regresar = await self.repository.create_product(busqueda)
            if file:
                try:
                    await run_in_threadpool(delete_image_from_s3, imagen_vieja)
                except Exception:
                    print("Error al borrar la imagen vieja del bucket.")
                    return producto_a_regresar
            return producto_a_regresar

        except IntegrityError:
            if file:
                try:
                    await run_in_threadpool(delete_image_from_s3, image_url)
                except Exception:
                    print("Error al borrar la imagen nueva del bucket.")

            raise ProductoYaExistente(producto_create.nombre)


    # Elimina los registros basura solo si pasa la autenticación del token.
    async def purge_deleted_products(self) -> int:
        try:
            return await self.repository.purge_deleted_products()
        except Exception as e:
            raise ErrorAlBorrarArchivosBasura()
        

    # Elimina los elementos huérfanos del bucket.    
    async def clean_bucket_s3(self)-> int:
        #Crear una funcion que implemenete que para cada elemento del bucket revisar que el elemento este en la BD,
        #si no esta entonces se elimina, esa funcion debera de manejar las excepciones ella misama.

        lista_registros_imagenes = await self.repository.obtener_la_fila_ubicacion_imagen()

        elementos_eliminados = await run_in_threadpool(delete_all_trash_s3, lista_registros_imagenes)

        return elementos_eliminados