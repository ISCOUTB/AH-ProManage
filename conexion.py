import psycopg2
from psycopg2 import Error
from contextlib import contextmanager
from fastapi import  HTTPException

@contextmanager
def get_db_connection():
    connection = None
    try:
        connection = psycopg2.connect(
            dbname='railway',
            host='autorack.proxy.rlwy.net',
            password='KTONJqnAteMSScvyyolzAhfIrBZIeAIX',
            port='52744',
            user='postgres'
        )
        yield connection
    except Error as error:
        print("Error al conectar a la base de datos:", error)
        raise HTTPException(status_code=500, detail="Error de conexión a la base de datos")
    finally:
        if connection:
            connection.close()
