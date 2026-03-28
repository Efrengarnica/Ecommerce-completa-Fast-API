from fastapi import FastAPI, status
from exceptions.ejemplo_exceptions import EjemploException
from handlers.ejemplo_handler import ejemplo_handler, manejar_errores_validacion
from handlers.generic import custom_404_handler
from fastapi.exceptions import RequestValidationError #Esto es para que si se lanza una excepcion por mal formato yo la tome.
#Aquí vivirá mi manejador de excepciones, será una función que reciba la app y agregue 
#las excepciones que voy a manejar.



def register_exception_handlers(app:FastAPI):
    app.add_exception_handler(EjemploException, ejemplo_handler)
    app.add_exception_handler(status.HTTP_404_NOT_FOUND,custom_404_handler)
    #Maneja excepciones de validación.
    app.add_exception_handler(RequestValidationError, manejar_errores_validacion)


