#Este será la primer tabla que creo con alembic, puede cambiar después.
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
from sqlalchemy import Column, DateTime

class Producto(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nombre: str = Field(index=True, unique=True) #Index para busquedas por nombre rápidas y unique para pedir unicidad en el nombre
    descripcion: str
    precio: float
    ubicacion_imagen: str
    deleted_at: Optional[datetime] = Field(  #Será None o datetime y me servirá para marcar filas ya eliminadas.
        default=None,
        sa_column=Column(DateTime(timezone=True), nullable=True)
    )

#Verificar como importaste los models en tu antiguo proyecto.  X
#Verificar el nombre que le psuisite a tus migraciones en tu antiguo proyecto.   X
#En tus DTOS definir que validaciones haras y que excepciones vas a lanzar      
#Ver como usaste tu inyeccion de dependencias en tu antiguo proyecto y ver como las usa el profe.  X
#En el proyecto anterior se ocupo JSONResponse?  X
#Se tiene que contemplar una posible excepcion cuando se consulta a una BD?, dos manera usar if y levantar una excepcion que la manejaras
# atrapar la excepcion y jugar con lo que te arroja
#Diferencia entre HTTPException y lo que se lanza en DTO, además ver si es mejor usar HTTPException o una personalizada
# En un post es mejor regresar una generic interface o el objeto mismo que se creo X