#La idea es aprender que existen otras maneras de recibir datos, no solo por JSON.
#Se pueden recibir por medio de un form y no hay necesidad, para datos sencillos, de usar un DTO para verificarlos.
#En un form también se pueden recibir archivos, files.
#Se aprenderá a recibir un archivo y explorar las caracteristicas que tiene el archivo.
#Se aprenderá a subir el archivo en tu disco, no es recomendado para eso hay otros servicios.
#Se aprenderá a recuperar tu archivo y regresarlo.
from fastapi import APIRouter, status, Form, UploadFile, Query
from fastapi.responses import JSONResponse, FileResponse
from typing import Annotated
import uuid
import os

router = APIRouter(prefix="/upload", tags=["Subir archivos"])


# Recuperar datos de un form.
""" @router.post("/")
async def subir(negocio_id:Annotated[int, Form()]):
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"estado":"ok", 
                 "mensaje": f"Método post | negocio_id={negocio_id}"}
    )  """


#Recuperar datos, esos datos también pueden ser files.
#Si no le pasas alguno te marca error y si le pasas algo diferente tambien
""" @router.post("/")
async def subir(negocio_id:Annotated[int, Form()], file:UploadFile):
    return JSONResponse(
        #print(file) para ver lo que tiene el file.
        status_code=status.HTTP_201_CREATED,
        content={"estado":"OK", 
                 "mensaje":f"Método post | negocio_id={negocio_id}",
                 "filename":file.filename,
                 "size":file.size,
                 "mimetype":file.content_type
                 }
    ) """


#Recibirlo solo si tiene el formato correcto.
""" @router.post("/")
async def subir(negocio_id: Annotated[int, Form()], file:UploadFile):
    extension="0"
    if file.content_type=="image/png":
        extension="png"
    if file.content_type=="image/jpg":
        extension="jpg"
    if extension=="0":
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content = {
                "estado":"error",
                "mensaje":f"Ocurrió un error inesperado"
            }
        )
    else:
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={"estado":"OK", 
                    "mensaje":f"Método post | negocio_id={negocio_id}",
                    "filename":file.filename,
                    "size":file.size,
                    "mimetype":file.content_type
                    }
                ) """


#Ahora hay que subirlo al disco.
#Recomendacion, siempre cambia el nombre del file para que tu tengas el control.
@router.post("/")
async def subir(negocio_id:Annotated[int, Form()], file:UploadFile):
    extension="0"
    if file.content_type=="image/png":
        extension="png"
    if file.content_type=="image/jpeg":
        extension="jpg"
    if extension=="0":
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content = {
                "estado":"error",
                "mensaje":f"Ocurrió un error inesperado"
            }
        )
    else:
        nombre = f"{uuid.uuid4()}.{extension}"
        file_location= os.path.join("uploads", nombre)
        #Aqui habría que manejar la exception si falla algo.
        with open(file_location, "wb") as buffer:
            buffer.write(await file.read())
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={"estado":"OK", 
                    "mensaje":f"Método post | negocio_id={negocio_id}",
                    "filename":file.filename,
                    "size":file.size,
                    "mimetype":file.content_type,
                    "nombre": nombre
                    }
            )


#Ahora la idea es que podamos devolver la imagen, esto no es recomendable ya que se supone que la imagen deberia no estar en tu servidor.
#Aqui vamos a ver otra manera de recibir informacion, ya aprendimos a recibirla por medio de JSON, de Form, por medio de /ID ahora lo vamos
#a recibir por medio de ?8990(query string)
@router.get("/file")
async def dar_imagen(id:str = Query(..., description="Nombre del archivo")):
   if not os.path.exists(f"uploads/{id}"):
       return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"estado":"error", 
                    "mensaje":f"Ocurrió un error inesperado."
                    }
            )
   return FileResponse(f"uploads/{id}")