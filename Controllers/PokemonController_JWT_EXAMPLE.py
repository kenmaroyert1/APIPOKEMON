"""
EJEMPLO: PokemonController con rutas protegidas por JWT

Este archivo muestra cómo proteger las rutas de tu API con JWT.
Puedes copiar estos ejemplos a tu PokemonController.py cuando estés listo.

IMPORTANTE: Descomenta las líneas de @jwt_required() cuando quieras activar la protección.
"""
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from Services.PokemonService import PokemonService

pokemon_blueprint = Blueprint('pokemon', __name__)
pokemon_service = PokemonService()

# ============================================================================
# RUTAS PÚBLICAS (No requieren autenticación)
# ============================================================================

@pokemon_blueprint.route('/pokemon', methods=['GET'])
def get_all_pokemons():
    """
    Obtener todos los pokémons (Público).
    Cualquiera puede ver la lista de pokémons.
    """
    try:
        pokemons = pokemon_service.get_all_pokemons()
        return jsonify(pokemons), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@pokemon_blueprint.route('/pokemon/<int:pokemon_id>', methods=['GET'])
def get_pokemon(pokemon_id):
    """
    Obtener un pokémon específico (Público).
    Cualquiera puede ver los detalles de un pokémon.
    """
    try:
        pokemon = pokemon_service.get_pokemon_by_id(pokemon_id)
        if pokemon:
            return jsonify(pokemon), 200
        return jsonify({'error': 'Pokémon no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============================================================================
# RUTAS PROTEGIDAS (Requieren autenticación JWT)
# ============================================================================

@pokemon_blueprint.route('/pokemon', methods=['POST'])
@jwt_required()  # ← Solo usuarios autenticados pueden crear pokémons
def create_pokemon():
    """
    Crear un nuevo pokémon (Protegido).
    Requiere token JWT en el header: Authorization: Bearer <token>
    """
    try:
        # Obtener el usuario autenticado actual
        current_user = get_jwt_identity()
        
        pokemon_data = request.get_json()
        pokemon = pokemon_service.create_pokemon(pokemon_data)
        
        return jsonify({
            'message': f'Pokémon creado por {current_user}',
            'pokemon': pokemon
        }), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@pokemon_blueprint.route('/pokemon/<int:pokemon_id>', methods=['PUT'])
@jwt_required()  # ← Solo usuarios autenticados pueden actualizar pokémons
def update_pokemon(pokemon_id):
    """
    Actualizar un pokémon existente (Protegido).
    Requiere token JWT.
    """
    try:
        current_user = get_jwt_identity()
        
        pokemon_data = request.get_json()
        pokemon = pokemon_service.update_pokemon(pokemon_id, pokemon_data)
        
        if pokemon:
            return jsonify({
                'message': f'Pokémon actualizado por {current_user}',
                'pokemon': pokemon
            }), 200
        return jsonify({'error': 'Pokémon no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@pokemon_blueprint.route('/pokemon/<int:pokemon_id>', methods=['DELETE'])
@jwt_required()  # ← Solo usuarios autenticados pueden eliminar pokémons
def delete_pokemon(pokemon_id):
    """
    Eliminar un pokémon (Protegido).
    Requiere token JWT.
    """
    try:
        current_user = get_jwt_identity()
        
        if pokemon_service.delete_pokemon(pokemon_id):
            return jsonify({
                'message': f'Pokémon eliminado por {current_user}'
            }), 200
        return jsonify({'error': 'Pokémon no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============================================================================
# RUTA ADICIONAL: Pokémons del usuario autenticado
# ============================================================================

@pokemon_blueprint.route('/pokemon/my-pokemons', methods=['GET'])
@jwt_required()
def get_my_pokemons():
    """
    Obtener pokémons del usuario autenticado (Ejemplo).
    Esta es una ruta de ejemplo que podrías implementar.
    """
    try:
        current_user = get_jwt_identity()
        # Aquí podrías filtrar pokémons por creador si guardas esa info
        pokemons = pokemon_service.get_all_pokemons()
        
        return jsonify({
            'user': current_user,
            'total_pokemons': len(pokemons),
            'pokemons': pokemons
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
