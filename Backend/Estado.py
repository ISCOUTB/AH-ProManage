from fastapi import APIRouter, HTTPException
from conexion import get_db_connection

router = APIRouter()

@router.get("/")
async def obtener_estados():
    try:
        with get_db_connection() as connection:
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM public."Estado";')
            result = cursor.fetchall()
            cursor.close()
            return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{id_estado}")
async def obtener_estado_id(id_estado: int):
    try:
        with get_db_connection() as connection:
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM public."Estado" WHERE "Id_estado" = %s;', (id_estado,))
            estado = cursor.fetchone()
            cursor.close()
            if estado is None:
                raise HTTPException(status_code=404, detail="Estado no encontrado")
            return estado
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


        
