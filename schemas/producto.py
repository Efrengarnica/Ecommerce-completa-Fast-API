from pydantic import BaseModel
from models.producto import Producto


# Ayuda a dar el formato a la respuesta final.
class ProductoResponse(BaseModel):
    id: int
    nombre: str
    descripcion: str
    precio: float
    link_imagen: str


    #Habilita junto con response_model el que si no le das el formato que quiero arroja una excepcion.
    #Cuando le das un atributo de mas a tu respuesta lo quita automaticamente y cuando le das otro tipo
    #dato como de int a str lanza la excepcion.
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


#Ayuda a agrupar los valores que llegan de un Form.
class ProductoCreate(BaseModel):
    nombre: str
    descripcion: str
    precio: float