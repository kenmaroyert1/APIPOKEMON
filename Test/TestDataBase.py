import pytest
from app import app
import json

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_create_20_pokemons(client):
    pokemons = [
        {"nombre": "Pikachu", "tipo": "Eléctrico", "nivel": 25, "poder_ataque": 55.5, "poder_defensa": 40.0, "hp": 100, "descripcion": "Ratón eléctrico"},
        {"nombre": "Charizard", "tipo": "Fuego/Volador", "nivel": 36, "poder_ataque": 84.0, "poder_defensa": 78.0, "hp": 150, "descripcion": "Dragón de fuego"},
        {"nombre": "Bulbasaur", "tipo": "Planta/Veneno", "nivel": 15, "poder_ataque": 49.0, "poder_defensa": 49.0, "hp": 90, "descripcion": "Pokémon semilla"},
        {"nombre": "Squirtle", "tipo": "Agua", "nivel": 18, "poder_ataque": 48.0, "poder_defensa": 65.0, "hp": 95, "descripcion": "Tortuga de agua"},
        {"nombre": "Mewtwo", "tipo": "Psíquico", "nivel": 70, "poder_ataque": 110.0, "poder_defensa": 90.0, "hp": 200, "descripcion": "Pokémon genético"},
        {"nombre": "Dragonite", "tipo": "Dragón/Volador", "nivel": 55, "poder_ataque": 100.0, "poder_defensa": 95.0, "hp": 180, "descripcion": "Pokémon dragón"},
        {"nombre": "Snorlax", "tipo": "Normal", "nivel": 45, "poder_ataque": 85.0, "poder_defensa": 110.0, "hp": 250, "descripcion": "Pokémon dormilón"},
        {"nombre": "Gengar", "tipo": "Fantasma/Veneno", "nivel": 40, "poder_ataque": 95.0, "poder_defensa": 60.0, "hp": 120, "descripcion": "Pokémon sombra"},
        {"nombre": "Machamp", "tipo": "Lucha", "nivel": 42, "poder_ataque": 100.0, "poder_defensa": 80.0, "hp": 160, "descripcion": "Pokémon superpoderoso"},
        {"nombre": "Gyarados", "tipo": "Agua/Volador", "nivel": 48, "poder_ataque": 92.0, "poder_defensa": 79.0, "hp": 170, "descripcion": "Pokémon atrocidad"},
        {"nombre": "Alakazam", "tipo": "Psíquico", "nivel": 45, "poder_ataque": 105.0, "poder_defensa": 55.0, "hp": 130, "descripcion": "Pokémon psíquico"},
        {"nombre": "Arcanine", "tipo": "Fuego", "nivel": 39, "poder_ataque": 90.0, "poder_defensa": 80.0, "hp": 155, "descripcion": "Pokémon legendario"},
        {"nombre": "Lapras", "tipo": "Agua/Hielo", "nivel": 44, "poder_ataque": 75.0, "poder_defensa": 80.0, "hp": 190, "descripcion": "Pokémon transporte"},
        {"nombre": "Jolteon", "tipo": "Eléctrico", "nivel": 35, "poder_ataque": 85.0, "poder_defensa": 60.0, "hp": 120, "descripcion": "Pokémon relámpago"},
        {"nombre": "Vaporeon", "tipo": "Agua", "nivel": 35, "poder_ataque": 80.0, "poder_defensa": 65.0, "hp": 190, "descripcion": "Pokémon burbuja"},
        {"nombre": "Flareon", "tipo": "Fuego", "nivel": 35, "poder_ataque": 95.0, "poder_defensa": 65.0, "hp": 120, "descripcion": "Pokémon llama"},
        {"nombre": "Rhydon", "tipo": "Tierra/Roca", "nivel": 47, "poder_ataque": 95.0, "poder_defensa": 95.0, "hp": 175, "descripcion": "Pokémon taladro"},
        {"nombre": "Starmie", "tipo": "Agua/Psíquico", "nivel": 38, "poder_ataque": 75.0, "poder_defensa": 70.0, "hp": 120, "descripcion": "Pokémon misterioso"},
        {"nombre": "Scyther", "tipo": "Bicho/Volador", "nivel": 40, "poder_ataque": 90.0, "poder_defensa": 75.0, "hp": 140, "descripcion": "Pokémon mantis"},
        {"nombre": "Tauros", "tipo": "Normal", "nivel": 43, "poder_ataque": 85.0, "poder_defensa": 70.0, "hp": 150, "descripcion": "Pokémon toro bravo"}
    ]
    
    successful_creations = 0
    failed_creations = []
    
    for pokemon in pokemons:
        response = client.post('/api/pokemon', 
                             data=json.dumps(pokemon),
                             content_type='application/json')
        if response.status_code == 201:
            successful_creations += 1
        else:
            failed_creations.append({
                "pokemon": pokemon["nombre"],
                "error": response.get_json()
            })
    
    assert successful_creations == 20, f"Se esperaban crear 20 pokémons, pero se crearon {successful_creations}. Errores: {failed_creations}"
    
    # Verificar que se pueden obtener todos los pokémons
    response = client.get('/api/pokemon')
    assert response.status_code == 200
    pokemons_in_db = response.get_json()
    assert len(pokemons_in_db) == 20, f"Se esperaban encontrar 20 pokémons, pero se encontraron {len(pokemons_in_db)}"
from mysql.connector import Error
import os
from dotenv import load_dotenv

def probar_conexion():
    """Prueba la conexión a la base de datos MySQL"""
    try:
        # Cargar variables de entorno
        load_dotenv()
        
        # Intentar establecer la conexión
        print("Intentando conectar a la base de datos...")
        connection = mysql.connector.connect(
            host=os.getenv('DBHOST'),
            user=os.getenv('DBUSER'),
            password=os.getenv('DBPASSWORD'),
            port=os.getenv('DBPORT'),
            database=os.getenv('DBDATABASE_NAME')
        )
        
        if connection.is_connected():
            print("¡Conexión exitosa!")
            
            # Obtener información del servidor
            db_info = connection.server_info
            print(f"Información del servidor MySQL: {db_info}")
            
            # Crear un cursor y ejecutar una consulta simple
            cursor = connection.cursor()
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            print("Consulta de prueba ejecutada correctamente")
            
            cursor.close()
            connection.close()
            print("Conexión cerrada correctamente")
            return True
            
    except Error as e:
        print(f"Error al conectar a la base de datos: {str(e)}")
        return False

if __name__ == "__main__":
    probar_conexion()