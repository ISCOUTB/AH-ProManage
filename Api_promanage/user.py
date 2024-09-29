from fastapi import APIRouter, HTTPException
import psycopg2
from conexion import get_db_connection


router = APIRouter()

@router.get("/")
async def obtener_usuarios():
    try:
        with get_db_connection() as connection:
            cursor = connection.cursor()
            cursor.execute( 'SELECT * FROM public."Usuario";' )
            result = cursor.fetchall()
            cursor.close()
            return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{Id_usuario}")
async def obtener_usuario(Id_usuario: int):
    with get_db_connection() as connection:
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM public."Usuario" WHERE "Id_usuario" = %s;', (Id_usuario,))
        usuario = cursor.fetchone()
        cursor.close()
        if usuario is None:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return usuario

@router.post("/usuarios/")
async def crear_usuario(Primer_nombre, Segundo_nombre, Primer_apellido, Segundo_apellido, Email, Contraseña):
   try:
    with get_db_connection() as connection:
        cursor = connection.cursor()
        insert_query = '''
        INSERT INTO  public."Usuario" ("Primer_nombre", "Segundo_nombre", "Primer_apellido", "Segundo_apellido", "Email", "Contraseña") 
        VALUES (%s, %s, %s, %s, %s, %s) RETURNING "Id_usuario";
        '''
        cursor.execute(insert_query, (Primer_nombre, Segundo_nombre, Primer_apellido, Segundo_apellido, Email, Contraseña))
        connection.commit()
        cursor.close()
        connection.close()
        return True
   except psycopg2.Error as error:
        print("Error al crear el usuario:", error)
        return False


@router.delete("/{Id_usuario}")
async def eliminar_usuario(Id_usuario: int):
    with get_db_connection() as connection:
        cursor = connection.cursor()
        cursor.execute('DELETE FROM public."Usuario" WHERE "Id_usuario" = %s;', (Id_usuario,))
        connection.commit()  
        cursor.close()
        return {"message": "Usuario eliminado"}

