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


#Necesario para comunicacion con AWS
import boto3
#Necesario para leer las variables de entorno
from dotenv import load_dotenv
load_dotenv()
import os


router = APIRouter(prefix="/upload", tags=["Subir archivos"])


#Creación del client, con métodos me permitirá comunicarme con mi bucket
s3_client = boto3.client(
    "s3", #Que voy a buscar
    region_name=os.getenv("AWS_REGION"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    endpoint_url=os.getenv("AWS_SECRET_ACCESS_URL") #Usado para local
)
S3_BUCKET_NAME=os.getenv("S3_BUCKET_NAME")
#Comandos usados con s3_client: "head_object" "delete_object" "upload_fileobj"


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
""" @router.post("/")
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
            ) """


#Ahora la idea es que podamos devolver la imagen, esto no es recomendable ya que se supone que la imagen deberia no estar en tu servidor.
#Aqui vamos a ver otra manera de recibir informacion, ya aprendimos a recibirla por medio de JSON, de Form, por medio de /ID ahora lo vamos
#a recibir por medio de ?8990(query string)
""" @router.get("/file")
async def dar_imagen(id:str = Query(..., description="Nombre del archivo")):
   if not os.path.exists(f"uploads/{id}"):
       return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"estado":"error", 
                    "mensaje":f"Ocurrió un error inesperado."
                    }
            )
   return FileResponse(f"uploads/{id}") """


#Ya por último vamos a implementar la subida de un archivo a una simulación de un servicio de AWS, usaremos localstack.
#También aprenderemos a pedir un archivo de nuestro servicio de localstack.
#Pasos:
# Crear un bucket S3, en localsatck
# Crear un client, con las credenciales en env, para AWS con boto3.
# Implementas el método para subir.
# Implementas el método para eliminar.

#Necesitamos el comando: docker exec -it localstack bash o 
# docker exec -it localstack awslocal s3 ls -> te todos los buckets creados
# docker exec -it localstack awslocal s3 mb s3://nombre-del-bucket
# docker exec -it localstack awslocal s3 rb s3://nombre-del-bucket (--force) -> Para eliminar el bucket y force si tiene archivos
# Nombrar el bucket y recordarlo en el .env

#NO PUDE HACER QUE EL CONTENEDOR PRESENTE PERSINTENCIA, parece ser que necesito unas buenas varibles para crear un buen contenedor que mapee y haga persistencia.


#Primero hay subir la imagen.
@router.post("/")
async def subir(negocio_id:Annotated[int, Form()], file:UploadFile):
    #Verifico que sea el formato correcto.
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
        #Aqui subo el doc.
        try:
            s3_client.upload_fileobj(
                file.file,
                S3_BUCKET_NAME,
                f"archivos/{nombre}",
                ExtraArgs={"ContentType": file.content_type}
            )
        except Exception as e:
            return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"estado":"error", 
                    "mensaje":f"Ocurrió un error inesperado | detalle={str(e)}"}
            )
        #Cuando implementas en un bucket privado no sirve una url de estás ya que necesitas permiso para que
        #la petición al bucket te conteste, dice que los bucket ahora por defecto vienen privados y debes de implementar 
        #un servicio de aws llamado cdn que podria comunicarse con el bucket el y solo el puede pedir cosas 
        #entonces tu le regresas al cliente un link armado. lo principal es el liknk del cdn y lo otro viene de la base de datos
        #es algo que armamos con el nombre y la carpeta en donde estará en el bucket es decir una ruta relativa.
        file_url=f"http://localhost:8000/{S3_BUCKET_NAME}/archivos/{nombre}"
        #retornamos una respuesta
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={"estado":"OK", 
                    "mensaje":f"Método post | negocio_id={negocio_id}",
                    "filename":file.filename,
                    "size":file.size,
                    "mimetype":file.content_type,
                    "nombre": nombre,
                    "url":file_url
                    }
            )
#Segundo, vamos a eliminar lo que se guardo en en el bucket.  "head_object" "delete_object" "upload_fileobj"
@router.delete("/file")
async def eliminar_foto_bucket(file_name :str = Query(..., description="Nombre del archivo a eliminar")):
    #preguntamos si existe el recurso en el bucket.
    try:    
        #Saber si existe.
        s3_client.head_object(Bucket=S3_BUCKET_NAME, Key=f"archivos/{file_name}")
    except s3_client.exceptions.ClientError as e:
        if e.response["Error"]["Code"]=="404":
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"estado":"error","mensaje":f"Ocurrió un error inesperado, el archivo no existe"}
            )
        else:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"estado":"error", "mensaje":f"Ocurrió un error inesperado al irlo a buscar"}
            )
    #borrar el archivo
    try:
        s3_client.delete_object(Bucket=S3_BUCKET_NAME, Key=f"archivos/{file_name}")
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"estado":"error","mensaje":f"Ocurrió un error inesperado al borrar el archivo", "info":str(e)}
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"estado":"ok", "mensaje":f"Se borra el archivo exitosamente"}
    )#eliminar_foto_bucket


"""
#entrar al contenedor
docker exec -it localstack bash

#crear bucket
docker exec -it localstack awslocal s3 mb s3://curso-udemy

#listar bucket
docker exec -it localstack awslocal s3 ls

# Listar objetos en el bucket "mi-bucket"
docker exec -it localstack awslocal s3 ls s3://curso-udemy/

# Listar recursivamente (todos los archivos y subcarpetas)
docker exec -it localstack awslocal s3 ls s3://curso-udemy/ --recursive

#borrar bucket
docker exec -it localstack awslocal s3 rb s3://curso-udemy2 --force """