#Este será la primer tabla que creo con alembic, puede cambiar después.
from sqlmodel import SQLModel, Field

class Producto(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nombre: str
    precio: float
    ubicacion_imagen: str


