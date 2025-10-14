from flask_sqlalchemy import SQLAlchemy
import os
import logging
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

db = SQLAlchemy()

# URI de SQLite como fallback
SQLITE_URI = 'sqlite:///pokemon_local.db'

def get_database_url():
    """
    Intenta construir la URL de MySQL y verificar la conexión.
    Si falla, retorna la URL de SQLite local.
    """
    username = os.getenv('DBUSERNAME')
    password = os.getenv('DBPASSWORD')
    host = os.getenv('DBHOST')
    port = os.getenv('DBPORT')
    database = os.getenv('DBNAME')
    
    # Si todas las variables de MySQL están configuradas, intentar usar MySQL
    if all([username, password, host, port, database]):
        mysql_uri = f"mysql+mysqlconnector://{username}:{password}@{host}:{port}/{database}"
        
        try:
            # Probar la conexión a MySQL con timeout
            test_engine = create_engine(
                mysql_uri, 
                echo=False,
                connect_args={
                    'connect_timeout': 5,  # Timeout de 5 segundos
                    'connection_timeout': 5
                }
            )
            conn = test_engine.connect()
            conn.close()
            test_engine.dispose()
            logger.info('✓ Conexión a MySQL exitosa.')
            return mysql_uri
        except Exception as e:
            # Capturar cualquier tipo de error de conexión
            logger.warning(f'⚠ No se pudo conectar a MySQL: {type(e).__name__}')
            logger.warning(f'  Detalle: {str(e)[:100]}')
            logger.warning('→ Usando SQLite local como fallback.')
    else:
        logger.warning('⚠ Variables de entorno de MySQL no configuradas completamente.')
        logger.warning('→ Usando SQLite local.')
    
    # Fallback a SQLite
    return SQLITE_URI

def init_db(app):
    """
    Inicializa la base de datos con Flask-SQLAlchemy.
    Intenta usar MySQL, si falla usa SQLite local.
    """
    database_url = get_database_url()
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    
    with app.app_context():
        try:
            db.create_all()
            logger.info(f'✓ Base de datos inicializada correctamente: {database_url.split("://")[0]}')
        except Exception as e:
            logger.error(f'✗ Error al inicializar la base de datos: {str(e)}')
            raise

def get_db_session():
    """
    Retorna una nueva sesión de base de datos para ser utilizada en los servicios o controladores.
    Esta función es útil si necesitas trabajar con sesiones directas de SQLAlchemy.
    """
    return db.session