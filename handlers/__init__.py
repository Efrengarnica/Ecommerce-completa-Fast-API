from fastapi import FastAPI, status
#from exceptions.ejemplo_exceptions import EjemploException
#from handlers.ejemplo_handler import ejemplo_handler, 
# validation_exception_handler
from handlers.generic import custom_404_handler, validation_exception_handler
from fastapi.exceptions import RequestValidationError #Esto es para que si se lanza una excepcion por mal formato yo la tome.
from exceptions.producto import ProductoNoEncontrado, ProductoYaExistente, ProductoNoEncontradoNombre, ErrorAlBorrarArchivosBasura
from handlers.producto import producto_no_encontrado, producto_ya_existente, producto_no_encontrado_nombre, error_al_borrar_archivos_basura
from exceptions.s3_exceptions import InvalidImageTypeException, S3UploadException, S3ImageNotFound, S3ImageDeleteError
from handlers.s3_handler import invalid_image_type_exception, s3_upload_exception, s3_image_not_found, s3_image_delete_error

#Aquí vivirá mi manejador de excepciones, será una función que reciba la app y agregue 
#las excepciones que voy a manejar.

def register_exception_handlers(app:FastAPI):
    #app.add_exception_handler(ValidationError, validation_exception_handler)
    #app.add_exception_handler(EjemploException, ejemplo_handler)
    app.add_exception_handler(status.HTTP_404_NOT_FOUND,custom_404_handler)
    app.add_exception_handler(ProductoNoEncontrado, producto_no_encontrado)
    app.add_exception_handler(ProductoYaExistente, producto_ya_existente)
    app.add_exception_handler(InvalidImageTypeException,invalid_image_type_exception)
    app.add_exception_handler(S3UploadException,s3_upload_exception)
    app.add_exception_handler(S3ImageNotFound,s3_image_not_found)        
    app.add_exception_handler(S3ImageDeleteError,s3_image_delete_error)   
    app.add_exception_handler(ProductoNoEncontradoNombre,producto_no_encontrado_nombre)
    app.add_exception_handler(ErrorAlBorrarArchivosBasura,error_al_borrar_archivos_basura)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    
    

