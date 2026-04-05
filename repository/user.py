from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.user import User
from schemas.user import UserCreate

class UserRepository:


    def __init__(self, session: AsyncSession):
        self.session = session


    # Conseguir User por id
    async def get_user_by_id(self, id:int):
        consulta = select(User).where(User.id == id)
        usuario = await self.session.execute(consulta)
        return usuario.scalars().first()


    # Conseguir User por email
    async def get_user_by_email(self, email:str) -> User | None:
        consulta = select(User).where(User.correo == email)
        usuario = await self.session.execute(consulta)
        return usuario.scalars().first()
    

    # Registrar un User
    async def create_user(self, user: User) -> User:
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user
    

    # Eliminar un User
    async def delete_user(self, user:User) -> User:
        await self.session.delete(user)
        await self.session.commit()
        return user
    

    # Modificar un User.
    async def modified_user(self, user:User) -> User:
        pass