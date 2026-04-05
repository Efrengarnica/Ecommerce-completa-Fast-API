from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_session
from repository.producto import ProductoRepository
from services.producto import ProductoService

from repository.user import UserRepository
from services.user import UserService

from repository.cart import CartRepository
from services.cart import CartService

from services.auth import AuthService

# Estás funciones me ayudan a inyectar la sesión en el endpont por medio de dependecias.


# Dependencias para conseguir la session en Producto
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


# Dependencias para conseguir la session de un Cart 
async def get_cart_repository(
    session: AsyncSession = Depends(get_session),
) -> CartRepository:
    return CartRepository(session)

async def get_cart_service(
    repository: CartRepository = Depends(get_cart_repository),
) -> CartService:
    return CartService(repository)


# Dependecias para conseguir la session de un Usuario
async def get_user_repository(
    session: AsyncSession = Depends(get_session),
) -> UserRepository:
    return UserRepository(session)

async def get_user_service(
    repository: UserRepository = Depends(get_user_repository),
    cart_service: CartService = Depends(get_cart_service)
) -> UserService:
    return UserService(repository, cart_service)


# Dependencias para conseguir la session de un Auth.
async def get_auth_service(
        user_service:UserService = Depends(get_user_service)
) -> AuthService:
    return AuthService(user_service)