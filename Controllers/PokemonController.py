"""
Controlador de Pokémon con control de acceso basado en roles.

Reglas de negocio:
- PROFESOR: Puede ver todos los pokémons, crear, actualizar y eliminar cualquiera
- TRAINER: Solo puede ver y eliminar sus pokémons capturados, no puede crear ni actualizar
"""
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from Services.PokemonService import PokemonService
from Models.Usuario import Usuario
from Models.PokemonCapturado import PokemonCapturado
from Models.Pokemon import Pokemon
from Config.DataBase import db
from Utils.decorators import profesor_required, get_current_user

pokemon_blueprint = Blueprint('pokemon', __name__)
pokemon_service = PokemonService()

# ============================================================================
# CREAR POKÉMON (Solo Profesor)
# ============================================================================

@pokemon_blueprint.route('/pokemon', methods=['POST'])
@jwt_required()
@profesor_required()
def create_pokemon():
    """Crear un nuevo pokémon (SOLO PROFESOR)."""
    try:
        usuario = get_current_user()
        pokemon_data = request.get_json()
        pokemon = pokemon_service.create_pokemon(pokemon_data)
        
        return jsonify({
            'message': f'Pokémon creado exitosamente por el profesor {usuario.nombre}',
            'pokemon': pokemon
        }), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============================================================================
# OBTENER TODOS LOS POKÉMONS
# ============================================================================

@pokemon_blueprint.route('/pokemon', methods=['GET'])
@jwt_required()
def get_all_pokemons():
    """Obtener pokémons según el rol del usuario."""
    try:
        usuario = get_current_user()
        
        if not usuario:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        
        if usuario.rol == 'profesor':
            # El profesor ve todos los pokémons
            pokemons = pokemon_service.get_all_pokemons()
            return jsonify({
                'rol': 'profesor',
                'total': len(pokemons),
                'pokemons': pokemons
            }), 200
        
        elif usuario.rol == 'trainer':
            # El trainer solo ve sus pokémons capturados
            capturas = PokemonCapturado.query.filter_by(usuario_id=usuario.id).all()
            pokemons_capturados = [captura.to_dict() for captura in capturas]
            
            return jsonify({
                'rol': 'trainer',
                'entrenador': usuario.nombre,
                'total_capturados': len(pokemons_capturados),
                'pokemons_capturados': pokemons_capturados
            }), 200
        
        else:
            return jsonify({'error': 'Rol de usuario no válido'}), 403
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============================================================================
# OBTENER UN POKÉMON ESPECÍFICO
# ============================================================================

@pokemon_blueprint.route('/pokemon/<int:pokemon_id>', methods=['GET'])
@jwt_required()
def get_pokemon(pokemon_id):
    """Obtener un pokémon específico según el rol."""
    try:
        usuario = get_current_user()
        
        if not usuario:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        
        pokemon = pokemon_service.get_pokemon_by_id(pokemon_id)
        
        if not pokemon:
            return jsonify({'error': 'Pokémon no encontrado'}), 404
        
        if usuario.rol == 'profesor':
            # El profesor puede ver cualquier pokémon
            return jsonify({
                'rol': 'profesor',
                'pokemon': pokemon
            }), 200
        
        elif usuario.rol == 'trainer':
            # Verificar si el trainer ha capturado este pokémon
            captura = PokemonCapturado.query.filter_by(
                usuario_id=usuario.id,
                pokemon_id=pokemon_id
            ).first()
            
            if not captura:
                return jsonify({
                    'error': 'No has capturado este Pokémon',
                    'mensaje': f'El Pokémon con ID {pokemon_id} no está en tu colección'
                }), 403
            
            return jsonify({
                'rol': 'trainer',
                'pokemon': captura.to_dict()
            }), 200
        
        else:
            return jsonify({'error': 'Rol de usuario no válido'}), 403
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============================================================================
# ACTUALIZAR POKÉMON (Solo Profesor)
# ============================================================================

@pokemon_blueprint.route('/pokemon/<int:pokemon_id>', methods=['PUT'])
@jwt_required()
@profesor_required()
def update_pokemon(pokemon_id):
    """Actualizar un pokémon existente (SOLO PROFESOR)."""
    try:
        usuario = get_current_user()
        pokemon_data = request.get_json()
        pokemon = pokemon_service.update_pokemon(pokemon_id, pokemon_data)
        
        if pokemon:
            return jsonify({
                'message': f'Pokémon actualizado por el profesor {usuario.nombre}',
                'pokemon': pokemon
            }), 200
        
        return jsonify({'error': 'Pokémon no encontrado'}), 404
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============================================================================
# ELIMINAR POKÉMON
# ============================================================================

@pokemon_blueprint.route('/pokemon/<int:pokemon_id>', methods=['DELETE'])
@jwt_required()
def delete_pokemon(pokemon_id):
    """Eliminar pokémon según el rol."""
    try:
        usuario = get_current_user()
        
        if not usuario:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        
        if usuario.rol == 'profesor':
            # El profesor puede eliminar cualquier pokémon de la BD
            if pokemon_service.delete_pokemon(pokemon_id):
                return jsonify({
                    'message': f'Pokémon eliminado de la base de datos por el profesor {usuario.nombre}'
                }), 200
            return jsonify({'error': 'Pokémon no encontrado'}), 404
        
        elif usuario.rol == 'trainer':
            # El trainer solo puede liberar pokémons de su colección
            captura = PokemonCapturado.query.filter_by(
                usuario_id=usuario.id,
                pokemon_id=pokemon_id
            ).first()
            
            if not captura:
                return jsonify({
                    'error': 'No puedes liberar este Pokémon',
                    'mensaje': 'Este Pokémon no está en tu colección'
                }), 403
            
            # Guardar el nombre del pokémon ANTES de eliminar la captura
            pokemon_nombre = captura.pokemon.nombre
            
            db.session.delete(captura)
            db.session.commit()
            
            return jsonify({
                'message': f'{usuario.nombre} ha liberado el Pokémon de su colección',
                'pokemon_liberado': pokemon_nombre
            }), 200
        
        else:
            return jsonify({'error': 'Rol de usuario no válido'}), 403
            
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# ============================================================================
# ASIGNAR POKÉMON A TRAINER (Solo Profesor)
# ============================================================================

@pokemon_blueprint.route('/pokemon/<int:pokemon_id>/asignar', methods=['POST'])
@jwt_required()
@profesor_required()
def asignar_pokemon_a_trainer(pokemon_id):
    """El profesor asigna un pokémon a un trainer."""
    try:
        usuario_profesor = get_current_user()
        data = request.get_json()
        
        trainer_email = data.get('trainer_email', '').strip().lower()
        apodo = data.get('apodo', '').strip()
        
        if not trainer_email:
            return jsonify({'error': 'Email del entrenador es requerido'}), 400
        
        pokemon = Pokemon.query.get(pokemon_id)
        if not pokemon:
            return jsonify({'error': 'Pokémon no encontrado'}), 404
        
        trainer = Usuario.query.filter_by(email=trainer_email, rol='trainer').first()
        if not trainer:
            return jsonify({'error': 'Entrenador no encontrado'}), 404
        
        captura_existente = PokemonCapturado.query.filter_by(
            usuario_id=trainer.id,
            pokemon_id=pokemon_id
        ).first()
        
        if captura_existente:
            return jsonify({
                'error': 'El entrenador ya tiene este Pokémon'
            }), 409
        
        nueva_captura = PokemonCapturado(
            usuario_id=trainer.id,
            pokemon_id=pokemon_id,
            apodo=apodo if apodo else None
        )
        
        db.session.add(nueva_captura)
        db.session.commit()
        
        return jsonify({
            'message': f'Pokémon asignado exitosamente',
            'profesor': usuario_profesor.nombre,
            'entrenador': trainer.nombre,
            'pokemon': pokemon.nombre,
            'apodo': apodo if apodo else None
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500