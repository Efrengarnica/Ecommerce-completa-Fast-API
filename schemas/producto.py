from pydantic import BaseModel, Field, ValidationError
from models.producto import Producto
from typing import Optional
from fastapi import Form
from fastapi.exceptions import RequestValidationError


# Ayuda a dar el formato a la respuesta final.
class ProductoResponse(BaseModel):
    id: int
    nombre: str
    descripcion: str
    precio: float
    link_imagen: str

    model_config = {
        "from_attributes": True
    }


# Funcion para transformar un producto a un producto response.
def producto_to_response(producto: Producto) -> ProductoResponse:
    return ProductoResponse(
        id=producto.id,
        nombre=producto.nombre,
        descripcion=producto.descripcion,
        precio=producto.precio,
        link_imagen=producto.ubicacion_imagen
    )


# Sirve para ocuparse para la validación de entrada y con form me ayuda a lanzar un RequestValidationError y manejar todas
# las validaciones de entrada de manera global.
class ProductoCreate(BaseModel):
    nombre: str = Field(min_length=7, max_length=100)
    descripcion: str = Field(min_length=20, max_length=1000)
    precio: float = Field(gt=0)
    model_config = {
        "extra": "forbid"
    }

    # AQUÍ VA EL MÉTODO:
    @classmethod
    def as_form(
        cls,
        nombre: str = Form(...),
        descripcion: str = Form(...),
        precio: float = Form(...)
    ):
        try:
            # Este método crea una instancia de la clase usando los datos del formulario
            return cls(nombre=nombre, descripcion=descripcion, precio=precio)
        except ValidationError as e:
            raise RequestValidationError(e.errors())

    model_config = {
        "extra": "forbid"
    }


# Ayuda a dar formato al producto que regresamos cuando eliminamos un producto.
class ProductoEliminadoResponse(BaseModel):
    nombre: str
    descripcion:str
    precio: float
    mensaje: str = "Producto eliminado exitosamente"

    model_config = {
    "from_attributes": True
    }


class ProductoCreatePut(BaseModel):
    id: int
    nombre: Optional[str] = Field(
        default=None,
        min_length=7,
        max_length=100
    )
    descripcion: Optional[str] = Field(
        default=None,
        min_length=20,
        max_length=1000
    )
    precio: Optional[float] = Field(
        default=None,
        gt=0
    )

    model_config = {
        "extra": "forbid"
    }

    @classmethod
    def as_form(
        cls,
        id: int = Form(...),
        nombre: Optional[str] = Form(None),
        descripcion: Optional[str] = Form(None),
        precio: Optional[float] = Form(None)
    ):
        try:
            # Creamos la instancia. Pydantic validará solo los campos que vengan con datos
            return cls(id=id, nombre=nombre, descripcion=descripcion, precio=precio)
        except ValidationError as e:
            # Nuevamente, lanzamos el error con la "munición" de Pydantic
            raise RequestValidationError(e.errors())

    