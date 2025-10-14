"""
Controlador de Autenticación para la API de Pokémon.
Maneja el login, registro y generación de tokens JWT.
Usa correo electrónico para autenticación.
Sistema de Access Token + Refresh Token para mayor seguridad.
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token, 
    create_refresh_token,
    jwt_required, 
    get_jwt_identity,
    get_jwt
)
from datetime import timedelta
from Models.Usuario import Usuario
from Config.DataBase import db
from Utils.decorators import profesor_required, get_current_user
import re

auth_blueprint = Blueprint('auth', __name__)

# Set para almacenar tokens revocados (en producción usar Redis)
revoked_tokens = set()

def validar_token_revocado(jti):
    """Verifica si un token ha sido revocado."""
    return jti in revoked_tokens

def validar_email(email):
    """Valida el formato de un correo electrónico."""
    patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(patron, email) is not None

@auth_blueprint.route('/register', methods=['POST'])
@jwt_required()
@profesor_required()
def register():
    """
    Endpoint para registrar un nuevo usuario (SOLO PROFESOR).
    El profesor puede crear cuentas para nuevos trainers o profesores.
    
    Body JSON:
    {
        "email": "nuevo@usuario.com",
        "nombre": "Juan Pérez",
        "password": "contraseña123",
        "rol": "trainer"  // o "profesor"
    }
    """
    profesor = get_current_user()
    
    if not request.is_json:
        return jsonify({"error": "Content-Type debe ser application/json"}), 400
    
    email = request.json.get('email', '').strip().lower()
    nombre = request.json.get('nombre', '').strip()
    password = request.json.get('password', '')
    rol = request.json.get('rol', 'trainer').lower()
    
    # Validaciones
    if not email or not nombre or not password:
        return jsonify({"error": "Email, nombre y contraseña son requeridos"}), 400
    
    if not validar_email(email):
        return jsonify({"error": "Formato de email inválido"}), 400
    
    if rol not in ['profesor', 'trainer']:
        return jsonify({"error": "Rol debe ser 'profesor' o 'trainer'"}), 400
    
    if len(password) < 6:
        return jsonify({"error": "La contraseña debe tener al menos 6 caracteres"}), 400
    
    # Verificar si el email ya existe
    if Usuario.query.filter_by(email=email).first():
        return jsonify({"error": "Este email ya está registrado"}), 409
    
    try:
        # Crear nuevo usuario
        nuevo_usuario = Usuario(
            email=email,
            nombre=nombre,
            rol=rol
        )
        nuevo_usuario.set_password(password)
        
        db.session.add(nuevo_usuario)
        db.session.commit()
        
        return jsonify({
            "message": f"Usuario registrado exitosamente por el profesor {profesor.nombre}",
            "profesor": profesor.nombre,
            "usuario_creado": nuevo_usuario.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error al registrar usuario: {str(e)}"}), 500

@auth_blueprint.route('/login', methods=['POST'])
def login():
    """
    Endpoint para iniciar sesión y obtener tokens JWT.
    
    Body JSON:
    {
        "email": "profesor@universidad.edu",
        "password": "contraseña123"
    }
    
    Retorna:
    {
        "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",  (Expira en 30 min)
        "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...", (Expira en 7 días)
        "token_type": "Bearer",
        "expires_in": 1800,
        "usuario": { ... }
    }
    """
    if not request.is_json:
        return jsonify({"error": "Content-Type debe ser application/json"}), 400
    
    email = request.json.get('email', '').strip().lower()
    password = request.json.get('password', '')
    
    if not email or not password:
        return jsonify({"error": "Email y contraseña son requeridos"}), 400
    
    # Buscar usuario por email
    usuario = Usuario.query.filter_by(email=email).first()
    
    if not usuario or not usuario.check_password(password):
        return jsonify({"error": "Email o contraseña incorrectos"}), 401
    
    if not usuario.activo:
        return jsonify({"error": "Tu cuenta ha sido desactivada"}), 403
    
    # Crear claims adicionales para ambos tokens
    additional_claims = {
        "rol": usuario.rol,
        "nombre": usuario.nombre
    }
    
    # Crear Access Token (corta duración - 30 minutos)
    access_token = create_access_token(
        identity=email,
        additional_claims=additional_claims
    )
    
    # Crear Refresh Token (larga duración - 7 días)
    refresh_token = create_refresh_token(
        identity=email,
        additional_claims=additional_claims
    )
    
    return jsonify({
        "message": "Login exitoso",
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "Bearer",
        "expires_in": 1800,  # 30 minutos en segundos
        "usuario": usuario.to_dict()
    }), 200

@auth_blueprint.route('/me', methods=['GET'])
@jwt_required()
def get_current_user_info():
    """
    Obtiene información del usuario autenticado actual.
    """
    email = get_jwt_identity()
    usuario = Usuario.query.filter_by(email=email).first()
    
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404
    
    return jsonify({
        "usuario": usuario.to_dict()
    }), 200

@auth_blueprint.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """
    Endpoint para refrescar el access token usando el refresh token.
    El refresh token debe enviarse en el header Authorization.
    
    Headers:
        Authorization: Bearer {refresh_token}
    
    Retorna:
    {
        "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
        "token_type": "Bearer",
        "expires_in": 1800
    }
    """
    # Obtener el email del refresh token
    email = get_jwt_identity()
    
    # Buscar usuario para obtener datos actualizados
    usuario = Usuario.query.filter_by(email=email).first()
    
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404
    
    if not usuario.activo:
        return jsonify({"error": "Tu cuenta ha sido desactivada"}), 403
    
    # Crear claims con información actualizada del usuario
    additional_claims = {
        "rol": usuario.rol,
        "nombre": usuario.nombre
    }
    
    # Generar nuevo access token
    new_access_token = create_access_token(
        identity=email,
        additional_claims=additional_claims
    )
    
    return jsonify({
        "message": "Token refrescado exitosamente",
        "access_token": new_access_token,
        "token_type": "Bearer",
        "expires_in": 1800  # 30 minutos
    }), 200

@auth_blueprint.route('/logout', methods=['POST'])
@jwt_required(verify_type=False)  # Acepta tanto access como refresh token
def logout():
    """
    Endpoint para cerrar sesión.
    Revoca el token actual (access o refresh).
    
    Headers:
        Authorization: Bearer {token}
    
    Retorna:
    {
        "message": "Logout exitoso"
    }
    """
    jti = get_jwt()["jti"]  # JWT ID único del token
    token_type = get_jwt()["type"]  # "access" o "refresh"
    email = get_jwt_identity()
    
    # Agregar token a la lista de revocados
    revoked_tokens.add(jti)
    
    return jsonify({
        "message": f"Logout exitoso",
        "token_revocado": token_type,
        "email": email,
        "info": "Token revocado. Elimina ambos tokens (access y refresh) del cliente."
    }), 200
