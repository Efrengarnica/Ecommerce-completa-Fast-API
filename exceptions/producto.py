#Aquí van todas las excepciones relacionadas con los productos.

class ProductoNoEncontrado(Exception):
    def __init__(self, id:int):
        self.mensaje = f"Producto con id:{id} no existe en la base de datos."
        super().__init__(self.mensaje)


class ProductoYaExistente(Exception):
    def __init__(self, nombre:str):
        self.mensaje = f"El nombre: {nombre} ya está registrado en la Base de Datos."
        super().__init__(self.mensaje)
        

class ProductoNoEncontradoNombre(Exception):
    def __init__(self, nombre:str):
        self.mensaje = f"Producto con nombre:{nombre} no existe en la base de datos."
        super().__init__(self.mensaje)

class ErrorAlBorrarArchivosBasura(Exception):
    def __init__(self):
        self.mensaje = "Hubo un error al querer borrar los registros basura de la BD."
        super().__init__(self.mensaje)