from fastapi import Request, status
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException

#Recuerda que es async ya que esta función puede ser llamada muchas veces.
async def custom_404_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"status": "error", "message": str(exc.detail)}
    )