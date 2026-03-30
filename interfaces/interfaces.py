from pydantic import BaseModel

#Este será una estructura que me permitirá darle formato a mis respuestas.
class GenericInterface(BaseModel):
    estado: str
    mensaje:str