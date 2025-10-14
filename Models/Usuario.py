"""
Modelo de Usuario para el sistema de autenticación.
Soporta roles de Profesor y Entrenador (Trainer).
"""
from Config.DataBase import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    nombre = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.String(20), nullable=False)  # 'profesor' o 'trainer'
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    activo = db.Column(db.Boolean, default=True)
    
    # Relación con pokémons capturados (solo para trainers)
    pokemons_capturados = db.relationship('PokemonCapturado', backref='entrenador', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hashea y guarda la contraseña."""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verifica si la contraseña es correcta."""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """Convierte el usuario a diccionario (sin contraseña)."""
        return {
            'id': self.id,
            'email': self.email,
            'nombre': self.nombre,
            'rol': self.rol,
            'fecha_registro': self.fecha_registro.isoformat() if self.fecha_registro else None,
            'activo': self.activo
        }
    
    def __repr__(self):
        return f'<Usuario {self.email} - {self.rol}>'
