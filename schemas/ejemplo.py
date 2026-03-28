#Aquí deberan de ir mis modelos relacionados con mi router ejemplo.
#La idea es darle a fastapi un formato que deberá de verificar con lo que le llegue en el body.
from pydantic import BaseModel, model_validator, field_validator, StrictInt
from typing import Any
#Recuerda que esto esta relacionado con Router
class EjemploDto(BaseModel):
    id:StrictInt
    nombre:str
    boleano: bool

     #La idea ahora es entender como personalizar el msj de error que nos arroja
    # fastapi cuando esta mal la info y no corresponde al dto.
    #La idea es que se lance una exception aquí, tambien debes de agregar en tu manejador de excepciones algo que
    # atrape la excepcion y que ejecute la funcion con el mensaje personalizado.
    """ 
    Se supone que es mejor con lo de abajo
    
    @model_validator(mode="after")
    def validator_nombre(self):
        if len(self.nombre.strip())<2:
            raise ValueError("nombre", "El campo nombre debe de tener al menos 2 caracteres")
        return self
    
    @model_validator(mode="after")
    def validar_id(self):
        if self.id <=0:
            raise ValueError("id", "El id debe de ser mayor que cero")
        return self """
    @field_validator("nombre")
    @classmethod
    def validator_nombre(cls, v: str) -> str:
        if not v or len(v.strip()) < 2:
            # Pydantic V2 guarda estos argumentos en ctx["error"]
            raise ValueError("nombre", "El campo nombre debe de tener al menos 2 caracteres")
        return v
    
    @field_validator("id")
    @classmethod
    def validar_id(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("id", "El id debe de ser mayor que cero")
        return v