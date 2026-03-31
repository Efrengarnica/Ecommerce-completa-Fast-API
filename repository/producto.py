from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.producto import Producto


class ProductoRepository:
    def __init__(self, session: AsyncSession):
        self.session = session


    #Función para traer todos los productos en una lista.
    async def get_all_products(self) -> list[Producto]:
        identificador = select(Producto)  # Nos sirve para abajo pero no es una consulta.
        tabla = await self.session.execute(identificador) #Vamos a la tabla.
        productos = tabla.scalars().all()  #Quitamos cosas extras y lo convertimos a una lista.
        return productos
    

    async def get_product_by_id(self, id:int) -> Producto:
        return await self.session.get(Producto, id)
    
    
    async def create_product(self, producto: Producto) -> Producto:
        self.session.add(producto) #Le dice que eso se guardará
        await self.session.commit()  #Realiza la operacion
        await self.session.refresh(producto) #Le da el id al producto que retornamos a pesar que no tenia.
        return producto