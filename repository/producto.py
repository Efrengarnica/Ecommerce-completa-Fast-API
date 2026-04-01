from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy import delete
from models.producto import Producto
from datetime import datetime, timezone


class ProductoRepository:


    # Me permite tener una sesión en mi ProductoRepository.
    def __init__(self, session: AsyncSession):
        self.session = session


    # Consigue el producto por medio de su nombre, descartando los productos eliminados que aún están en la BD.
    async def get_product_by_name(self, nombre:str) -> Producto | None:
        statement = select(Producto).where(
            Producto.nombre == nombre,
            Producto.deleted_at == None  # Solo trae los que NO tienen fecha de borrado
        )
        result = await self.session.execute(statement)
        return result.scalars().first()


    # Función para traer todos los productos en una lista, descartando los ya eliminados que están en la BD.
    async def get_all_products(self) -> list[Producto] | None:
        identificador = select(Producto).where(Producto.deleted_at == None)  # Nos sirve para abajo pero no es una consulta.
        tabla = await self.session.execute(identificador) #Vamos a la tabla.
        productos = tabla.scalars().all()  #Quitamos cosas extras y lo convertimos a una lista.
        return productos
    

    # Trae el producto siempre y cuando no este marcado como eliminado.
    async def get_product_by_id(self, id:int) -> Producto | None:
        stmt = select(Producto).where(Producto.id == id, Producto.deleted_at == None)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
        
    

    # El rollback solo es cuando se modifica algo de la BD no cuando se hacen lecturas.
    async def create_product(self, producto: Producto) -> Producto:
        self.session.add(producto) #Le dice que eso se guardará
        try: 
            await self.session.commit()  #Realiza la operacion
            await self.session.refresh(producto) #Le da el id al producto que retornamos a pesar que no tenia.
            return producto
        
        except IntegrityError:
            await self.session.rollback()
            raise
    
  
    # Me ayuda a marcar el producto como eliminado.
    async def soft_delete(self, producto: Producto) -> None:
        producto.deleted_at = datetime.now(timezone.utc)
        self.session.add(producto)
        try:
            await self.session.commit()
            await self.session.refresh(producto)
        except:
            await self.session.rollback()
            raise


    # Me ayuda a eliminar el producto de manera definitiva.
    async def hard_delete(self, producto: Producto) -> None:
        await self.session.delete(producto)
        try:
            await self.session.commit()
        except:
            await self.session.rollback()
            raise

    
    # Me ayuda a limpiar los registros basura.
    async def purge_deleted_products(self) -> int:
        try:
            statement = (
                delete(Producto)
                .where(Producto.deleted_at.is_not(None))
                .execution_options(synchronize_session="fetch")
            )

            result = await self.session.execute(statement)
            
            await self.session.commit()

            return result.rowcount
        
        except Exception as e:
            await self.session.rollback()
            raise e 