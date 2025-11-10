from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from Config.DataBase import init_db
from Config.jwt import init_jwt
from Controllers.PokemonController import pokemon_blueprint
from Controllers.AuthController import auth_blueprint

app = Flask(__name__)

# Inicializar JWT
init_jwt(app)
jwt = JWTManager(app)

# Inicializar la base de datos
init_db(app)










# Ruta de bienvenida
@app.route('/')
def welcome():
    return jsonify({
        "mensaje": "¡Bienvenido a la API de Pokémon con Sistema de Roles! 🎓",
        "versión": "2.0",
        "rutas_disponibles": {
            "GET /": "Página de bienvenida",
            # Rutas de Autenticación
            "POST /auth/register": "Registrar nuevo usuario",
            "POST /auth/login": "Iniciar sesión con email (obtener token JWT)",
            "GET /auth/me": "Información del usuario actual",
            "POST /auth/logout": "Cerrar sesión",
            # Rutas de Pokémon
            "GET /api/pokemon": "Obtener pokémons (según rol)",
            "GET /api/pokemon/<id>": "Obtener un pokémon específico",
            "POST /api/pokemon": "Crear pokémon (SOLO PROFESOR)",
            "PUT /api/pokemon/<id>": "Actualizar pokémon (SOLO PROFESOR)",
            "DELETE /api/pokemon/<id>": "Eliminar pokémon (según rol)",
            "POST /api/pokemon/<id>/asignar": "Asignar pokémon a trainer (SOLO PROFESOR)"
        },
        "roles": {
            "profesor": {
                "permisos": [
                    "Ver TODOS los pokémons",
                    "Crear pokémons",
                    "Actualizar pokémons",
                    "Eliminar pokémons",
                    "Asignar pokémons a trainers"
                ],
                "email_ejemplo": "profesor@universidad.edu",
                "password_ejemplo": "profesor123"
            },
            "trainer": {
                "permisos": [
                    "Ver SOLO sus pokémons capturados",
                    "Ver detalles de pokémons que posee",
                    "Liberar pokémons de su colección"
                ],
                "restricciones": [
                    "NO puede crear pokémons",
                    "NO puede actualizar pokémons",
                    "NO puede ver pokémons que no ha capturado"
                ],
                "email_ejemplo": "ash@pokemon.com",
                "password_ejemplo": "ash123"
            }
        },
        "autenticacion": {
            "login": {
                "endpoint": "/auth/login",
                "metodo": "POST",
                "body_ejemplo": {
                    "email": "profesor@universidad.edu",
                    "password": "profesor123"
                }
            },
            "register": {
                "endpoint": "/auth/register",
                "metodo": "POST",
                "body_ejemplo": {
                    "email": "nuevo@example.com",
                    "nombre": "Tu Nombre",
                    "password": "contraseña123",
                    "rol": "trainer"
                }
            },
            "uso_token": {
                "header": "Authorization",
                "formato": "Bearer <tu_token_aqui>"
            }
        },
        "formato_json": {
            "crear_actualizar_pokemon": {
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
app.register_blueprint(auth_blueprint, url_prefix='/auth')
app.register_blueprint(pokemon_blueprint, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)