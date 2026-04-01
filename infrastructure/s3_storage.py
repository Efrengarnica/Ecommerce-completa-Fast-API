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