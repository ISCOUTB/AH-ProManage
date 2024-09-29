from fastapi import APIRouter, HTTPException
from conexion import get_db_connection

router = APIRouter()


@router.post("/Crear/")
async def crear_asignacion(Id_asig_T: int, Id_usuario: int):
    try:
        with get_db_connection() as connection:
            cursor = connection.cursor()
            insert_query = '''
            INSERT INTO public."Tarea-asig" ("Id_asig_T", "Id_usuario") 
            VALUES (%s, %s);
            '''
            cursor.execute(insert_query, (Id_asig_T, Id_usuario))
            connection.commit()
            return {"message": "Asignación creada exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/")
async def obtener_asignaciones():
    try:
        with get_db_connection() as connection:
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM public."Tarea-asig";')
            result = cursor.fetchall()
            cursor.close()
            return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{Id_asig_T}")
async def obtener_asignacion(Id_asig_T: int):
    try:
        with get_db_connection() as connection:
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM public."Tarea-asig" WHERE "Id_asig_T" = %s;', (Id_asig_T,))
            asignacion = cursor.fetchone()
            cursor.close()
            if asignacion is None:
                raise HTTPException(status_code=404, detail="Asignación no encontrada")
            return asignacion
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{Id_asig_T}")
async def eliminar_asignacion(Id_asig_T: int):
    try:
        with get_db_connection() as connection:
            cursor = connection.cursor()
            cursor.execute('DELETE FROM public."Tarea-asig" WHERE "Id_asig_T" = %s;', (Id_asig_T,))
            connection.commit()
            cursor.close()
            return {"message": "Asignación eliminada exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


