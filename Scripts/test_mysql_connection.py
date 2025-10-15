import mysql.connector
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

try:
    print("Intentando conectar a la base de datos...")
    connection = mysql.connector.connect(
        host=os.getenv('DBHOST'),
        user=os.getenv('DBUSERNAME'),
        password=os.getenv('DBPASSWORD'),
        port=os.getenv('DBPORT'),
        database=os.getenv('DBNAME')
    )

    if connection.is_connected():
        print("¡Conexión exitosa!")
        db_info = connection.get_server_info()
        print(f"Información del servidor MySQL: {db_info}")

        cursor = connection.cursor()
        cursor.execute("SELECT DATABASE();")
        record = cursor.fetchone()
        print(f"Conectado a la base de datos: {record}")

        cursor.close()
        connection.close()
        print("Conexión cerrada correctamente.")

except mysql.connector.Error as err:
    print(f"Error al conectar a la base de datos: {err}")