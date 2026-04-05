from fastapi import FastAPI, status, Request
from fastapi.responses import JSONResponse
# En escencia esto creo que no se necesita ya que en docker compose cargó las variables al principio.
# pero lo dejo para futuras referencias de que cuando quiero tener un .env en un proyecto fuera de docker debo de usar 
# esto para cargar el .env
from dotenv import load_dotenv
load_dotenv()
#Importo mi funcion que implementa el manejador de excepciones.
from handlers import register_exception_handlers

#rutas
from api.ejemplo_router import router as ejemplo_router
from api.upload import router as upload_router

#rutas de mi aplicación Ecommerce.
from api.producto import router as producto_router
from api.user import router as user_router
from api.cart import router as cart_router
from api.auth import router as auth_router


# La idea es que este .py quede lo más limpio posible.
app = FastAPI()


@app.get("/")
async def root():
    #Los print en produccion son malos, no dejarlos
    #print("Hola consola") Esto aparece en la consola en los logs de tu contenedor.
    
    #JSONResponse me ayuda a dar un mejor formato a lo que entrego.
    #content, status_code, 
    #Se puede poner el número en estatus pero es mejor usar lo que te da fastAPI
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"mensaje": "API funcionando", "estado":"Genial"} 
    )
""" 
def root():
    return {"mensaje": "API funcionando", "estado":"bien"} 

Otras cosas que aprendí, dado que en la definición de nuestro docker compose
le dijimos que cada vez que se levante el contenedor se ejecute un comando 
ese comando hace que también se ponga a trabajar uvicorn entonces no es necesario que
una vez levantado el servicio también se tenga que levantar uvicorn.
"""


#Decirle a la app que agregue la ruta.
app.include_router(ejemplo_router)
app.include_router(upload_router)
#Rutas de mi app
app.include_router(producto_router)
app.include_router(user_router)
app.include_router(cart_router)
app.include_router(auth_router)


""" Que pasa cuando a mi app llegan rutas que no están, bueno la app
lanza una excepción y un mensaje que llevara uvicorn de regreso
Si la app tiene un exception handler entonces la app no lanza la excepcion 
la maneja y lanza solo el mensaje.
 """

""" @app.exception_handler(status.HTTP_404_NOT_FOUND)
async def custom_404_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"estado":"error", "mensaje":"Ruta no encontrada"}
    ) """
#Arriba está una manera de manejar excepciones pero si queremos crecer esta es la manera
#Aqui se implementa el último paso para conectar la app con el manejador.
""" No es necesario manejar todos los errores la idea es que se manejen los reconocidos para ti
asi tu front sabra que hacer y sabra que presentar.
Otra razon es que no se detiene la app pero hay ocasiones que si no se maneja se da más info de la necesaria y alguien que sepa
puede ocupar esa ventana para entrar por medio de lo que diga el error.
 """
register_exception_handlers(app)