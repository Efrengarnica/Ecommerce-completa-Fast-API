from fastapi import UploadFile
from config.aws import s3_client, S3_BUCKET_NAME
import uuid

class InvalidImageTypeException(Exception):
    pass

class S3UploadException(Exception):
    pass

def upload_product_image(file: UploadFile) -> str:
    if file.content_type == "image/png":
        extension = "png"
    elif file.content_type in ("image/jpeg", "image/jpg"):
        extension = "jpg"
    else:
        #La tengo que crear aparte y decidir que mensaje va a mostrar.
        raise InvalidImageTypeException("Formato de imagen no permitido")

    nombre = f"{uuid.uuid4()}.{extension}"

    try:
        s3_client.upload_fileobj(
            file.file,
            S3_BUCKET_NAME,
            f"archivos/{nombre}",
            ExtraArgs={"ContentType": file.content_type},
        )
    except Exception as e:
        #La tengo que crear de igual manera y saber que hacer.
        raise S3UploadException(f"No se pudo subir la imagen: {str(e)}")

    return f"http://localhost:8000/{S3_BUCKET_NAME}/archivos/{nombre}"