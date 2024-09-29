from fastapi import APIRouter, HTTPException
from conexion import get_db_connection

router = APIRouter()

@router.post("/crear/")
async def crear_asignacion(Id_asig: int, Id_usuario: int):
    try:
        with get_db_connection() as connection:
            cursor = connection.cursor()
            insert_query = '''
            INSERT INTO public."Proyecto-asig" ("Id_asig", "Id_usuario") 
            VALUES (%s, %s);
            '''
            cursor.execute(insert_query, (Id_asig, Id_usuario))
            connection.commit()
            return {"message": "Asignación creada exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/")
async def obtener_asignaciones():
    try:
        with get_db_connection() as connection:
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM public."Proyecto-asig";')
            result = cursor.fetchall()
            cursor.close()
            return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{Id_asig}")
async def obtener_asignacion(Id_asig: int):
    try:
        with get_db_connection() as connection:
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM public."Proyecto-asig" WHERE "Id_asig" = %s;', (Id_asig,))
            asignacion = cursor.fetchone()
            cursor.close()
            if asignacion is None:
                raise HTTPException(status_code=404, detail="Asignación no encontrada")
            return asignacion
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{Id_asig}")
async def eliminar_asignacion(Id_asig: int):
    try:
        with get_db_connection() as connection:
            cursor = connection.cursor()
            cursor.execute('DELETE FROM public."Proyecto-asig" WHERE "Id_asig" = %s;', (Id_asig,))
            connection.commit()
            cursor.close()
            return {"message": "Asignación eliminada exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))