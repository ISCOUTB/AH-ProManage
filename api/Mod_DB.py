import psycopg2


pgdatabase = 'railway'
pghost = 'autorack.proxy.rlwy.net'
pgpassword = 'KTONJqnAteMSScvyyolzAhfIrBZIeAIX'
pgport = '52744'
pguser = 'postgres'

try:
   
    connection = psycopg2.connect(
        dbname=pgdatabase,
        user=pguser,
        password=pgpassword,
        host=pghost,
        port=pgport
    )
    print("Conexión establecida")

   
    cursor = connection.cursor()

  
    query = """
     
   
    """
   
    cursor.execute(query)

   
    connection.commit()

  
    cursor.close()
    connection.close()
    print("Modificación completada")

except Exception as e:
    print(f"Error al realizar la consulta: {e}")