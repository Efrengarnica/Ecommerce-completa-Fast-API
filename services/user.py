from repository.user import UserRepository
from services.cart import CartService
from models.user import User
from schemas.enums import UserRole
from schemas.user import UserCreate
from core.security import get_password_hash, verify_password
from fastapi.concurrency import run_in_threadpool
from exceptions.user import UsuarioNoEncontrado

class UserService:


    def __init__(self, repository: UserRepository, cart_service: CartService):
        self.repository = repository
        self.cart_service = cart_service


    # Obtener User por id
    async def get_user_by_id(self, id:int):
        usuario = await self.repository.get_user_by_id(id)
        if not usuario:
            raise UsuarioNoEncontrado
        return usuario


    # Conseguir User por email
    async def get_user_by_email(self, email:str) -> User | None:

        usuario = await self.repository.get_user_by_email(email)
        if not usuario:
            raise UsuarioNoEncontrado
        return usuario
    

    # Registrar a un User
    async def create_user(self, userCreate: UserCreate) -> User:

        contrasena_segura = await run_in_threadpool(get_password_hash, userCreate.contrasena)

        data=userCreate.model_dump()
        data["contrasena"]=contrasena_segura

        usuario = User(**data)

        user_db = await self.repository.create_user(usuario)
    
        if user_db.rol == UserRole.CUSTOMER:
            await self.cart_service.create_cart_for_user(user_db.id)

        return user_db
    
    # Eliminar un User
    # La idea es que si el user desaparece el id que tiene un carrito de user quedará huerfano, ent tambien hay 
    # que implementar algo para limpiar las cosas.

    #Preguntar que es mejor, eliminar el user y que pasa con los carritos de ese id?, se limpiaran.
    #Crear Excepciones.
    #Hacerlo a preuba de errores
    async def delete_user(self, email:str, contrasena:str):
        # Primero verificar que exista el usuario en bd.
        # Verificar que la contraseña que me dio es la misma que esta en la bd.
        # Eliminar usuario 

        usuario = await self.get_user_by_email(email)
        if not usuario:
            pass
        
        password_user = usuario.contrasena
       
        tiene_permisos= await run_in_threadpool(verify_password, contrasena, password_user)

        if not tiene_permisos:
            pass

        return await self.repository.delete_user(usuario)