from fastapi import Request, status
from fastapi.responses import JSONResponse
from exceptions.s3_exceptions import InvalidImageTypeException, S3UploadException, S3ImageDeleteError, S3ImageNotFound

async def invalid_image_type_exception(request: Request, exc: InvalidImageTypeException):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "estado":"error",
            "mensaje":exc.mensaje
        }
    )

async def s3_upload_exception(request: Request, exc: S3UploadException):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "estado":"error",
            "mensaje":exc.mensaje
        }
    )


async def s3_image_delete_error(request: Request, exc: S3ImageDeleteError):
        return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "estado":"error",
            "mensaje":exc.mensaje
        }
    )
    
    
async def s3_image_not_found(request: Request, exc: S3ImageNotFound):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "estado":"error",
            "mensaje":exc.mensaje
        }
    )