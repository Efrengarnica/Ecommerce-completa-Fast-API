class InvalidImageTypeException(Exception):
    def __init__(self, tipo:str):
        self.tipo = tipo
        self.mensaje = f"No está permitido el formato:{tipo} para una imagen."
        super().__init__(self.mensaje)

class S3UploadException(Exception):
    def __init__(self, nombre_file:str):
        self.nombre_file = nombre_file
        self.mensaje = f"El archivo llamado: {nombre_file} no fue posible guardarlo."
        super().__init__(self.mensaje)

class S3ImageNotFound(Exception):
    def __init__(self, file_name:str):
        self.file_name=file_name
        self.mensaje = f"El archivo {file_name} no fue posible localizarlo para su eliminación, intente de nuevo."
        super().__init__(self.mensaje)

class S3ImageDeleteError(Exception):
    def __init__(self, file_name:str):
        self.file_name=file_name
        self.mensaje = f"El archivo {file_name} no fue posible eliminarlo, intenta de nuevo."
        super().__init__(self.mensaje)
