from fastapi import APIRouter, HTTPException
import psycopg2
from conexion import get_db_connection

router = APIRouter()

            
@router.get("/")
async def Tareas():
    try:
        with get_db_connection() as connection:
            cursor = connection.cursor()
            cursor.execute( 'SELECT * FROM public."Tarea";' )
            result = cursor.fetchall()
            cursor.close()
            return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{Id_tarea}")
async def obtener_tarea(Id_tarea: int):
    with get_db_connection() as connection:
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM public."Tarea" WHERE "Id_tarea" = %s;', (Id_tarea,))
        tarea = cursor.fetchone()
        cursor.close()
        if tarea is None:
            raise HTTPException(status_code=404, detail="Tarea no encontrada")
        return tarea


@router.post("/creacion_tarea/")
async def crear_tarea(Nombre, Descripcion,Fecha_inicio,Fecha_final,Id_proyecto,Id_asig_T,Id_estado):
   try:
    with get_db_connection() as connection:
        cursor = connection.cursor()
        insert_query = '''
        INSERT INTO  public."Tarea" ("Nombre", "Descripcion", "Fecha_inicio", "Fecha_final", "Id_proyecto", "Id_asig_T","Id_estado") 
        VALUES (%s, %s, %s, %s, %s, %s,%s) RETURNING "Id_tarea";
        '''
        cursor.execute(insert_query, (Nombre, Descripcion,Fecha_inicio,Fecha_final,Id_proyecto,Id_asig_T,Id_estado))
        connection.commit()
        cursor.close()
        connection.close()
        return True
   except psycopg2.Error as error:
        print("Error al crear la Tarea:", error)
        return False
        



@router.delete("/{Id_tarea}")
async def eliminar_tarea(Id_tarea: int):
    with get_db_connection() as connection:
        cursor = connection.cursor()
        cursor.execute('DELETE FROM public."Tarea" WHERE "Id_tarea" = %s;', (Id_tarea,))
        connection.commit()  
        cursor.close()
        return {"message": "Tarea eliminada"}
