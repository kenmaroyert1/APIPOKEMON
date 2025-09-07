from flask import Flask, jsonify
from Config.DataBase import init_db
from Controllers.PokemonController import pokemon_blueprint

app = Flask(__name__)

# Inicializar la base de datos
init_db(app)

# Ruta de bienvenida
@app.route('/')
def welcome():
    return jsonify({
        "mensaje": "¡Bienvenido a la API de Pokémon!",
        "versión": "1.0",
        "rutas_disponibles": {
            "GET /": "Página de bienvenida",
            "GET /api/pokemon": "Obtener todos los pokémons",
            "GET /api/pokemon/<id>": "Obtener un pokémon específico",
            "POST /api/pokemon": "Crear un nuevo pokémon",
            "PUT /api/pokemon/<id>": "Actualizar un pokémon existente",
            "DELETE /api/pokemon/<id>": "Eliminar un pokémon"
        },
        "formato_json": {
            "crear_actualizar": {
                "nombre": "string (requerido)",
                "tipo": "string (requerido)",
                "nivel": "integer (requerido, positivo)",
                "poder_ataque": "float (requerido)",
                "poder_defensa": "float (requerido)",
                "hp": "integer (requerido, positivo)",
                "descripcion": "string (opcional)"
            }
        }
    }), 200

# Registrar los blueprints
app.register_blueprint(pokemon_blueprint, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True)