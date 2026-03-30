from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator
#Necesario para leer las variables de entorno
from dotenv import load_dotenv
load_dotenv()
import os


data_base_url = os.getenv("DATABASE_URL")


#El engine es necesario para abrir una conexion con la base de datos.
engine = create_async_engine(
    data_base_url, #La locación de la bd.
    echo=False,    #Evitar que por cada consulta haya logs.
    future=True,  #Que se use el estilo de código más moderno.
    pool_size=10,   #Deja lista 10 conexiones, por default, en la BD para mayor velocidad.
    max_overflow=20 #Permite crear más si es que las 10 por default ya están ocupadas.
)


# Generador de sesiones para FastAPI.
# Usar sessionmaker asegura que siempre crees sesiones con la misma configuración.
async_session_factory = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False#Evita que haya consultas en segundo plano.
)


# Permite que se inyecte una sesion y cuando esta termine se cierre.
async def get_session() -> AsyncGenerator[AsyncSession, None]: 
    async with async_session_factory() as session:
        yield session