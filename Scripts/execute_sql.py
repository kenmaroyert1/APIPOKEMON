import mysql.connector
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Leer el archivo SQL
sql_file_path = 'Scripts/create_pokemon_table.sql'
with open(sql_file_path, 'r') as file:
    sql_script = file.read()

try:
    print("Conectando a la base de datos...")
    connection = mysql.connector.connect(
        host=os.getenv('DBHOST'),
        user=os.getenv('DBUSERNAME'),
        password=os.getenv('DBPASSWORD'),
        port=os.getenv('DBPORT'),
        database=os.getenv('DBNAME')
    )

    if connection.is_connected():
        print("¡Conexión exitosa!")
        cursor = connection.cursor()

        # Ejecutar el script SQL
        for statement in sql_script.split(';'):
            if statement.strip():
                cursor.execute(statement)

        connection.commit()
        print("Script SQL ejecutado correctamente.")

        cursor.close()
        connection.close()
        print("Conexión cerrada correctamente.")

except mysql.connector.Error as err:
    print(f"Error al ejecutar el script SQL: {err}")