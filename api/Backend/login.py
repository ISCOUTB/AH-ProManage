from fastapi import APIRouter, HTTPException, Depends
from api.conexion import get_db_connection
from pydantic import BaseModel
import psycopg2

router = APIRouter()



class LoginRequest(BaseModel):
    email: str
    contraseña: str


@router.post("/login")
async def login(request: LoginRequest):
    try:
        with get_db_connection() as connection:
            cursor = connection.cursor()
            
            query = '''
            SELECT "Id_usuario", "Contraseña" FROM public."Usuario" 
            WHERE "Email" = %s;
            '''
            cursor.execute(query, (request.email,))
            user = cursor.fetchone()

            if user is None:
                raise HTTPException(status_code=404, detail="Usuario no encontrado")
            
            user_id, stored_password = user

            
            if request.contraseña != stored_password:
                raise HTTPException(status_code=401, detail="Contraseña incorrecta")
            
            cursor.close()
            return {"message": "Login exitoso", "user_id": user_id}

    except psycopg2.Error as error:
        raise HTTPException(status_code=500, detail="Error en la base de datos: " + str(error))