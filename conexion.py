import os
import psycopg2
from psycopg2 import Error
from contextlib import contextmanager
from fastapi import HTTPException

@contextmanager
def get_db_connection():
    connection = None
    try:
        connection = psycopg2.connect(
            dbname=os.getenv('DB_NAME'),
            host=os.getenv('DB_HOST'),
            password=os.getenv('DB_PASSWORD'),
            port=os.getenv('DB_PORT'),
            user=os.getenv('DB_USER')
        )
        yield connection
    except Error as error:
        print("Error al conectar a la base de datos:", error)
        raise HTTPException(status_code=500, detail="Error de conexión a la base de datos")
    finally:
        if connection:
            connection.close()

