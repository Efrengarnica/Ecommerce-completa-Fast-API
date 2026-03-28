from fastapi import FastAPI, status
from exceptions.ejemplo_exceptions import EjemploException
from handlers.ejemplo_handler import ejemplo_handler
from handlers.generic import custom_404_handler
#Aquí vivirá mi manejador de excepciones, será una función que reciba la app y agregue 
#las excepciones que voy a manejar.


def register_exception_handlers(app:FastAPI):
    app.add_exception_handler(EjemploException, ejemplo_handler)
    app.add_exception_handler(status.HTTP_404_NOT_FOUND,custom_404_handler)