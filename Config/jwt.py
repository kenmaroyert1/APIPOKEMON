"""
Configuración de JWT (JSON Web Tokens) para la API de Pokémon.
Este módulo contiene todas las configuraciones necesarias para la autenticación basada en tokens.
"""
import os
from datetime import timedelta
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Clave secreta para firmar los tokens JWT
# IMPORTANTE: Esta clave debe ser segura y nunca compartirse públicamente
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "default-secret-key-change-in-production")

# Algoritmo de cifrado para JWT
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

# Ubicación donde se buscará el token JWT (en los headers HTTP)
JWT_TOKEN_LOCATION = ["headers"]

# Tiempo de expiración del token de acceso (en minutos)
# 30 minutos por defecto
JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", 30)))

# Tiempo de expiración del refresh token (en días)
# 7 días por defecto
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=int(os.getenv("JWT_REFRESH_TOKEN_EXPIRE_DAYS", 7)))

# Nombre del header HTTP donde se enviará el token
JWT_HEADER_NAME = "Authorization"

# Tipo/prefijo del token en el header (ej: "Bearer <token>")
JWT_HEADER_TYPE = "Bearer"

# Configuración adicional opcional
JWT_ERROR_MESSAGE_KEY = "message"  # Clave para mensajes de error en respuestas JSON

def init_jwt(app):
    """
    Inicializa la configuración de JWT en la aplicación Flask.
    Configura tanto Access Tokens como Refresh Tokens.
    
    Args:
        app: Instancia de la aplicación Flask
    """
    app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY
    app.config['JWT_ALGORITHM'] = JWT_ALGORITHM
    app.config['JWT_TOKEN_LOCATION'] = JWT_TOKEN_LOCATION
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = JWT_ACCESS_TOKEN_EXPIRES
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = JWT_REFRESH_TOKEN_EXPIRES
    app.config['JWT_HEADER_NAME'] = JWT_HEADER_NAME
    app.config['JWT_HEADER_TYPE'] = JWT_HEADER_TYPE
    app.config['JWT_ERROR_MESSAGE_KEY'] = JWT_ERROR_MESSAGE_KEY
    
    # Validar que la clave secreta no sea la default en producción
    if JWT_SECRET_KEY == "default-secret-key-change-in-production":
        print("⚠️  ADVERTENCIA: Usando JWT_SECRET_KEY por defecto. Configura una clave segura en producción.")
    
    print(f"✓ JWT configurado correctamente")
    print(f"  - Access Token: {JWT_ACCESS_TOKEN_EXPIRES}")
    print(f"  - Refresh Token: {JWT_REFRESH_TOKEN_EXPIRES}")

def get_jwt_config():
    """
    Retorna un diccionario con todas las configuraciones de JWT.
    Útil para debugging o información.
    """
    return {
        'JWT_TOKEN_LOCATION': JWT_TOKEN_LOCATION,
        'JWT_ACCESS_TOKEN_EXPIRES': str(JWT_ACCESS_TOKEN_EXPIRES),
        'JWT_HEADER_NAME': JWT_HEADER_NAME,
        'JWT_HEADER_TYPE': JWT_HEADER_TYPE,
        'JWT_SECRET_KEY_CONFIGURED': bool(os.getenv("JWT_SECRET_KEY"))
    }
