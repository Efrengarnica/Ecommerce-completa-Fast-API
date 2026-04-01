from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_session
from repository.producto import ProductoRepository
from services.producto import ProductoService

#Estás funciones me ayudan a inyectar la sesión en el endpont por medio de dependecias.

#Aquí menciono que para conseguir un ProductoRepository necesito primero conseguir la session.
async def get_product_repository(
    session: AsyncSession = Depends(get_session),
) -> ProductoRepository:
    return ProductoRepository(session)

#Aquí menciono que si quiero conseguir un ProductoService debo primero de conseguir un ProductoRepository.
async def get_product_service(
    repository: ProductoRepository = Depends(get_product_repository),
) -> ProductoService:
    return ProductoService(repository)