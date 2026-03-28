from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from schemas.ejemplo import EjemploDto


#La idea es que ahora aquí se definan todos los endpoints relacionado con ejemplo.
#Primero se define el router.
#Para que mi router este asociado a mi app debo de ir a mi app a decirle que este router estará asociado con ella.
router = APIRouter(prefix="/ejemplo", tags=["Ejemplo"])


@router.get("/")
async def index():
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"De donde me hablas": "De ejemplo"}
    )


#Cuando haces esto fastapi detecta la variable en la ruta y lo puede rescatar.
@router.get("/{id}")
async def show(id:int):
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"estado":"ok", "mensaje":f"Método GET | id={id}"}
    )

#Aquí implementamos nuestra primera verificacion con pydantic
@router.post("/")
async def create(body_ejemplo:EjemploDto):
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"estado":"ok", 
                 "mensaje": f"Método POST | id:{body_ejemplo.id} | nombre:{body_ejemplo.nombre} | boleano:{body_ejemplo.boleano}"}
    )
""" @router.post("/")
async def create():
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"estado":"ok", "mensaje": "Método POST"}
    ) """


@router.put("/{id}")
async def update(id:int):
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"estado":"ok", "mensaje": f"Método PUT | id={id}"}
    )


@router.delete("/{id}")
async def destroy(id:int):
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"estado":"ok", "mensaje": f"Método DELETE | id={id}"}
    )