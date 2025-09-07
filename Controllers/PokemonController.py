from flask import Blueprint, jsonify, request
from Services.PokemonService import PokemonService

pokemon_blueprint = Blueprint('pokemon', __name__)
pokemon_service = PokemonService()

@pokemon_blueprint.route('/pokemon', methods=['POST'])
def create_pokemon():
    try:
        pokemon_data = request.get_json()
        pokemon = pokemon_service.create_pokemon(pokemon_data)
        return jsonify(pokemon), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@pokemon_blueprint.route('/pokemon', methods=['GET'])
def get_all_pokemons():
    try:
        pokemons = pokemon_service.get_all_pokemons()
        return jsonify(pokemons), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@pokemon_blueprint.route('/pokemon/<int:pokemon_id>', methods=['GET'])
def get_pokemon(pokemon_id):
    try:
        pokemon = pokemon_service.get_pokemon_by_id(pokemon_id)
        if pokemon:
            return jsonify(pokemon), 200
        return jsonify({'error': 'Pokémon no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@pokemon_blueprint.route('/pokemon/<int:pokemon_id>', methods=['PUT'])
def update_pokemon(pokemon_id):
    try:
        pokemon_data = request.get_json()
        pokemon = pokemon_service.update_pokemon(pokemon_id, pokemon_data)
        if pokemon:
            return jsonify(pokemon), 200
        return jsonify({'error': 'Pokémon no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@pokemon_blueprint.route('/pokemon/<int:pokemon_id>', methods=['DELETE'])
def delete_pokemon(pokemon_id):
    try:
        if pokemon_service.delete_pokemon(pokemon_id):
            return jsonify({'message': 'Pokémon eliminado correctamente'}), 200
        return jsonify({'error': 'Pokémon no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500