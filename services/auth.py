from services.user import UserService
from core.security import verify_password, create_access_token
from exceptions.auth import NotAuthorization
from exceptions.user import UsuarioNoEncontrado
from fastapi.concurrency import run_in_threadpool

class AuthService:

    def __init__(self, user_service: UserService):
        self.user_service = user_service

    
    async def log_in(self, email:str, password:str):
        
        try:
            user = await self.user_service.get_user_by_email(email)
        except UsuarioNoEncontrado:
            raise NotAuthorization()
        
        tiene_permisos = await run_in_threadpool(verify_password, password, user.contrasena)
        if not tiene_permisos:
            raise NotAuthorization()
        
        token = create_access_token({"sub": str(user.id)})
    
        return token