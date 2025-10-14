"""
Decoradores personalizados para proteger rutas según roles de usuario.
"""
from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from Models.Usuario import Usuario

def profesor_required():
    """
    Decorador que requiere que el usuario tenga rol de 'profesor'.
    Debe usarse después de @jwt_required().
    """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            email = get_jwt_identity()
            
            usuario = Usuario.query.filter_by(email=email).first()
            
            if not usuario:
                return jsonify({
                    'error': 'Usuario no encontrado',
                    'mensaje': 'Tu sesión ha expirado o el usuario no existe'
                }), 404
            
            if usuario.rol != 'profesor':
                return jsonify({
                    'error': 'Acceso denegado',
                    'mensaje': 'Solo los profesores tienen acceso a esta funcionalidad'
                }), 403
            
            return fn(*args, **kwargs)
        return decorator
    return wrapper

def trainer_or_profesor_required():
    """
    Decorador que requiere que el usuario sea trainer o profesor.
    Debe usarse después de @jwt_required().
    """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            email = get_jwt_identity()
            
            usuario = Usuario.query.filter_by(email=email).first()
            
            if not usuario:
                return jsonify({
                    'error': 'Usuario no encontrado',
                    'mensaje': 'Tu sesión ha expirado o el usuario no existe'
                }), 404
            
            if usuario.rol not in ['profesor', 'trainer']:
                return jsonify({
                    'error': 'Acceso denegado',
                    'mensaje': 'No tienes permisos para acceder a esta funcionalidad'
                }), 403
            
            return fn(*args, **kwargs)
        return decorator
    return wrapper

def get_current_user():
    """
    Obtiene el usuario actual desde el token JWT.
    Retorna el objeto Usuario o None si no existe.
    """
    try:
        verify_jwt_in_request()
        email = get_jwt_identity()
        return Usuario.query.filter_by(email=email).first()
    except:
        return None
