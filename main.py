from fastapi import FastAPI, status, Request
from fastapi.responses import JSONResponse


#rutas
from api.ejemplo_router import router as ejemplo_router


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


""" Que pasa cuando a mi app llegan rutas que no están, bueno la app
lanza una excepción y un mensaje que llevara uvicorn de regreso
Si la app tiene un exception handler entonces la app no lanza la excepcion 
la maneja y lanza solo el mensaje.
 """

@app.exception_handler(status.HTTP_404_NOT_FOUND)
async def custom_404_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"estado":"error", "mensaje":"Ruta no encontrada"}
    )