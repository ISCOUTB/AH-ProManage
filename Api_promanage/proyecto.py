from fastapi import APIRouter, HTTPException
from conexion import get_db_connection
import psycopg2

router = APIRouter()

         
@router.get("/")
async def proyect():
    try:
        with get_db_connection() as connection:
            cursor = connection.cursor()
            cursor.execute( 'SELECT * FROM public."Proyecto";' )
            result = cursor.fetchall()
            cursor.close()
            return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{Id_proyecto}")
async def obtener_proyecto(Id_proyecto: int):
    with get_db_connection() as connection:
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM public."Proyecto" WHERE "Id_proyecto" = %s;', (Id_proyecto,))
        proyecto = cursor.fetchone()
        cursor.close()
        if proyecto is None:
            raise HTTPException(status_code=404, detail="proyecto no encontrado")
        return proyecto


@router.post("/creacion_proyect/")
async def crear_proyecto(Nombre, Descripcion,Fecha_inicio,Fecha_final,Id_asig,Id_estado):
   try:
    with get_db_connection() as connection:
        cursor = connection.cursor()
        insert_query = '''
        INSERT INTO  public."Proyecto" ("Nombre", "Descripcion", "Fecha_inicio", "Fecha_final", "Id_asig","Id_estado") 
        VALUES (%s, %s, %s, %s, %s, %s) RETURNING "Id_proyecto";
        '''
        cursor.execute(insert_query, (Nombre, Descripcion,Fecha_inicio,Fecha_final,Id_asig,Id_estado))
        connection.commit()
        cursor.close()
        connection.close()
        return True
   except psycopg2.Error as error:
        print("Error al crear el proyecto:", error)
        return False
        

@router.delete("/{Id_proyeto}")
async def eliminar_proyecto(Id_proyecto: int):
    with get_db_connection() as connection:
        cursor = connection.cursor()
        cursor.execute('DELETE FROM public."Tarea" WHERE "Id_tarea" = %s;', (Id_proyecto,))
        connection.commit()  
        cursor.close()
        return {"message": "proyecto eliminado"}