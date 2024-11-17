from fastapi import APIRouter, HTTPException
from .repositorio import EstadoRepo
from .esquema import EstadoEsquema
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/estados/")
async def listar_estados():
    repo = EstadoRepo()
    try:
        estados = repo.obtener_estados()
        return estados
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/estados/{id_estado}")
async def obtener_estado(id_estado: int):
    repo = EstadoRepo()
    try:
        estado = repo.obtener_estado_id(id_estado)
        return estado
    except ValueError:
        raise HTTPException(status_code=404, detail="Estado no encontrado")
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/estados/")
async def crear_estado(estado: EstadoEsquema):
    repo = EstadoRepo()
    try:
        nuevo_estado = repo.crear_estado(estado)
        return JSONResponse(content=nuevo_estado.dict(), status_code=201)
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/estados/{id_estado}")
async def eliminar_estado(id_estado: int):
    repo = EstadoRepo()
    try:
        mensaje = repo.eliminar_estado(id_estado)
        return {"message": mensaje}
    except ValueError:
        raise HTTPException(status_code=404, detail="Estado no encontrado")
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
