#Aquí deberan de ir mis modelos relacionados con mi router ejemplo.
#La idea es darle a fastapi un formato que deberá de verificar con lo que le llegue en el body.
from pydantic import BaseModel

#Recuerda que esto esta relacionado con Router
class EjemploDto(BaseModel):
    id:int
    nombre:str
    boleano:bool