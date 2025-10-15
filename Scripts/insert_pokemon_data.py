import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Config.DataBase import db
from Models.Pokemon import Pokemon
from app import app
import mysql.connector
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Datos de prueba
pokemons = [
    {
        'nombre': 'Pikachu',
        'tipo': 'Eléctrico',
        'nivel': 25,
        'poder_ataque': 55.5,
        'poder_defensa': 40.0,
        'hp': 100,
        'descripcion': 'Ratón eléctrico'
    },
    {
        'nombre': 'Charizard',
        'tipo': 'Fuego/Volador',
        'nivel': 36,
        'poder_ataque': 84.0,
        'poder_defensa': 78.0,
        'hp': 150,
        'descripcion': 'Dragón de fuego'
    },
    {
        'nombre': 'Bulbasaur',
        'tipo': 'Planta/Veneno',
        'nivel': 15,
        'poder_ataque': 49.0,
        'poder_defensa': 49.0,
        'hp': 90,
        'descripcion': 'Pokémon semilla'
    },
    {
        'nombre': 'Squirtle',
        'tipo': 'Agua',
        'nivel': 18,
        'poder_ataque': 48.0,
        'poder_defensa': 65.0,
        'hp': 95,
        'descripcion': 'Tortuga de agua'
    },
    {
        'nombre': 'Mewtwo',
        'tipo': 'Psíquico',
        'nivel': 70,
        'poder_ataque': 110.0,
        'poder_defensa': 90.0,
        'hp': 200,
        'descripcion': 'Pokémon genético'
    },
    {
        'nombre': 'Dragonite',
        'tipo': 'Dragón/Volador',
        'nivel': 55,
        'poder_ataque': 100.0,
        'poder_defensa': 95.0,
        'hp': 180,
        'descripcion': 'Pokémon dragón'
    },
    {
        'nombre': 'Snorlax',
        'tipo': 'Normal',
        'nivel': 45,
        'poder_ataque': 85.0,
        'poder_defensa': 110.0,
        'hp': 250,
        'descripcion': 'Pokémon dormilón'
    },
    {
        'nombre': 'Gengar',
        'tipo': 'Fantasma/Veneno',
        'nivel': 40,
        'poder_ataque': 95.0,
        'poder_defensa': 60.0,
        'hp': 120,
        'descripcion': 'Pokémon sombra'
    },
    {
        'nombre': 'Machamp',
        'tipo': 'Lucha',
        'nivel': 42,
        'poder_ataque': 100.0,
        'poder_defensa': 80.0,
        'hp': 160,
        'descripcion': 'Pokémon superpoderoso'
    },
    {
        'nombre': 'Gyarados',
        'tipo': 'Agua/Volador',
        'nivel': 48,
        'poder_ataque': 92.0,
        'poder_defensa': 79.0,
        'hp': 170,
        'descripcion': 'Pokémon atrocidad'
    },
    {
        'nombre': 'Alakazam',
        'tipo': 'Psíquico',
        'nivel': 45,
        'poder_ataque': 105.0,
        'poder_defensa': 55.0,
        'hp': 130,
        'descripcion': 'Pokémon psíquico'
    },
    {
        'nombre': 'Arcanine',
        'tipo': 'Fuego',
        'nivel': 39,
        'poder_ataque': 90.0,
        'poder_defensa': 80.0,
        'hp': 155,
        'descripcion': 'Pokémon legendario'
    },
    {
        'nombre': 'Lapras',
        'tipo': 'Agua/Hielo',
        'nivel': 44,
        'poder_ataque': 75.0,
        'poder_defensa': 80.0,
        'hp': 190,
        'descripcion': 'Pokémon transporte'
    },
    {
        'nombre': 'Jolteon',
        'tipo': 'Eléctrico',
        'nivel': 35,
        'poder_ataque': 85.0,
        'poder_defensa': 60.0,
        'hp': 120,
        'descripcion': 'Pokémon relámpago'
    },
    {
        'nombre': 'Vaporeon',
        'tipo': 'Agua',
        'nivel': 35,
        'poder_ataque': 80.0,
        'poder_defensa': 65.0,
        'hp': 190,
        'descripcion': 'Pokémon burbuja'
    },
    {
        'nombre': 'Flareon',
        'tipo': 'Fuego',
        'nivel': 35,
        'poder_ataque': 95.0,
        'poder_defensa': 65.0,
        'hp': 120,
        'descripcion': 'Pokémon llama'
    },
    {
        'nombre': 'Rhydon',
        'tipo': 'Tierra/Roca',
        'nivel': 47,
        'poder_ataque': 95.0,
        'poder_defensa': 95.0,
        'hp': 175,
        'descripcion': 'Pokémon taladro'
    },
    {
        'nombre': 'Starmie',
        'tipo': 'Agua/Psíquico',
        'nivel': 38,
        'poder_ataque': 75.0,
        'poder_defensa': 70.0,
        'hp': 120,
        'descripcion': 'Pokémon misterioso'
    },
    {
        'nombre': 'Scyther',
        'tipo': 'Bicho/Volador',
        'nivel': 40,
        'poder_ataque': 90.0,
        'poder_defensa': 75.0,
        'hp': 140,
        'descripcion': 'Pokémon mantis'
    },
    {
        'nombre': 'Tauros',
        'tipo': 'Normal',
        'nivel': 43,
        'poder_ataque': 85.0,
        'poder_defensa': 70.0,
        'hp': 150,
        'descripcion': 'Pokémon toro bravo'
    },
    {
        'nombre': 'Electabuzz',
        'tipo': 'Eléctrico',
        'nivel': 37,
        'poder_ataque': 83.0,
        'poder_defensa': 57.0,
        'hp': 140,
        'descripcion': 'Pokémon eléctrico'
    },
    {
        'nombre': 'Magmar',
        'tipo': 'Fuego',
        'nivel': 38,
        'poder_ataque': 95.0,
        'poder_defensa': 57.0,
        'hp': 140,
        'descripcion': 'Pokémon ardiente'
    },
    {
        'nombre': 'Pinsir',
        'tipo': 'Bicho',
        'nivel': 40,
        'poder_ataque': 85.0,
        'poder_defensa': 100.0,
        'hp': 150,
        'descripcion': 'Pokémon pinza'
    },
    {
        'nombre': 'Zapdos',
        'tipo': 'Eléctrico/Volador',
        'nivel': 50,
        'poder_ataque': 90.0,
        'poder_defensa': 85.0,
        'hp': 200,
        'descripcion': 'Pokémon legendario'
    },
    {
        'nombre': 'Moltres',
        'tipo': 'Fuego/Volador',
        'nivel': 50,
        'poder_ataque': 100.0,
        'poder_defensa': 90.0,
        'hp': 200,
        'descripcion': 'Pokémon legendario'
    },
    {
        'nombre': 'Articuno',
        'tipo': 'Hielo/Volador',
        'nivel': 50,
        'poder_ataque': 85.0,
        'poder_defensa': 100.0,
        'hp': 200,
        'descripcion': 'Pokémon legendario'
    },
    {
        'nombre': 'Ditto',
        'tipo': 'Normal',
        'nivel': 20,
        'poder_ataque': 48.0,
        'poder_defensa': 48.0,
        'hp': 100,
        'descripcion': 'Pokémon transformador'
    },
    {
        'nombre': 'Eevee',
        'tipo': 'Normal',
        'nivel': 20,
        'poder_ataque': 55.0,
        'poder_defensa': 50.0,
        'hp': 110,
        'descripcion': 'Pokémon evolución'
    },
    {
        'nombre': 'Kabutops',
        'tipo': 'Roca/Agua',
        'nivel': 40,
        'poder_ataque': 105.0,
        'poder_defensa': 90.0,
        'hp': 150,
        'descripcion': 'Pokémon fósil'
    },
    {
        'nombre': 'Omastar',
        'tipo': 'Roca/Agua',
        'nivel': 40,
        'poder_ataque': 90.0,
        'poder_defensa': 125.0,
        'hp': 150,
        'descripcion': 'Pokémon fósil'
    }
]

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

        # Insertar datos
        for pokemon in pokemons:
            cursor.execute(
                "INSERT INTO pokemon (nombre, tipo, nivel, poder_ataque, poder_defensa, hp, descripcion) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (pokemon['nombre'], pokemon['tipo'], pokemon['nivel'], pokemon['poder_ataque'], 
                 pokemon['poder_defensa'], pokemon['hp'], pokemon['descripcion'])
            )

        connection.commit()
        print("Datos insertados correctamente.")

        cursor.close()
        connection.close()
        print("Conexión cerrada correctamente.")

except mysql.connector.Error as err:
    print(f"Error al insertar los datos: {err}")