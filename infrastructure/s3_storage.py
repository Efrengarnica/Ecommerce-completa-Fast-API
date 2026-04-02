from fastapi import UploadFile
from config.aws import s3_client, S3_BUCKET_NAME
import uuid
from exceptions.s3_exceptions import InvalidImageTypeException, S3UploadException, S3ImageDeleteError, S3ImageNotFound

# Subir archivos a S3.
def upload_product_image(file: UploadFile) -> str:
    if file.content_type == "image/png":
        extension = "png"
    elif file.content_type in ("image/jpeg", "image/jpg"):
        extension = "jpg"
    else:
        raise InvalidImageTypeException(file.content_type)

    nombre = f"{uuid.uuid4()}.{extension}"

    try:
        s3_client.upload_fileobj(
            file.file,
            S3_BUCKET_NAME,
            f"archivos/{nombre}",
            ExtraArgs={"ContentType": file.content_type},
        )
    except Exception as e:
        raise S3UploadException(file.filename)

    return f"http://localhost:8000/{S3_BUCKET_NAME}/archivos/{nombre}"


# Borrar archivos de S3.
def delete_image_from_s3(link:str) -> None:
    file_name = ""
    if "/archivos/" in link:
        file_name = link.split("/archivos/")[-1]
    try:    
        s3_client.head_object(Bucket=S3_BUCKET_NAME, Key=f"archivos/{file_name}")
    except s3_client.exceptions.ClientError as e:
        raise S3ImageNotFound(file_name)
    try:
        s3_client.delete_object(Bucket=S3_BUCKET_NAME, Key=f"archivos/{file_name}")
    except Exception as e:
        raise S3ImageDeleteError(file_name)
    

# Me ayuda a obtener, en una lista, todos los elementos que existen en mi S3.
def listar_objetos_bucket(prefix: str = "archivos/") -> list[str]:
    keys = [] # Se guarda el nombre de los archivos.
    paginator = s3_client.get_paginator("list_objects_v2") # Se necesita para usar paginate y poder leer de 1,000 en 1,000 archivos

    #Si tiene mas de 1,000 archivos para a la otra iteracion.
    for page in paginator.paginate(Bucket=S3_BUCKET_NAME, Prefix=prefix):
        for obj in page.get("Contents", []):
            keys.append(obj["Key"])  # Ejemplo: "archivos/foto.jpg"

    return keys


# Me ayuda a eliminar todos los elementos huérfanos de mi bucket.
def delete_all_trash_s3(lista_registros_imagenes: list[str]) -> int:
 
    contador = 0

    registros_bd = set(lista_registros_imagenes)

    lista_imagenes_bucket = listar_objetos_bucket(prefix="archivos/")

    for key_bucket in lista_imagenes_bucket:
        ubicacion_imagen=f"http://localhost:8000/bucket-s3-imitacion/{key_bucket}"
        if ubicacion_imagen not in registros_bd:
            try:
                s3_client.delete_object(Bucket=S3_BUCKET_NAME, Key=key_bucket)
                contador += 1
            except Exception as e:
               print(f"Falla al eliminar el archivo: {key_bucket}")

    return contador