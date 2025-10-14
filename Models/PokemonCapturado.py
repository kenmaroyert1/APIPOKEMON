"""
Modelo de relación entre Entrenadores y Pokémons capturados.
Un entrenador puede tener muchos pokémons capturados.
"""
from Config.DataBase import db
from datetime import datetime

class PokemonCapturado(db.Model):
    __tablename__ = 'pokemon_capturado'
    
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    pokemon_id = db.Column(db.Integer, db.ForeignKey('pokemon.id'), nullable=False)
    fecha_captura = db.Column(db.DateTime, default=datetime.utcnow)
    apodo = db.Column(db.String(100))  # Opcional: apodo personalizado
    
    # Relación con Pokemon
    pokemon = db.relationship('Pokemon', backref='capturas', lazy=True)
    
    def to_dict(self):
        """Convierte la captura a diccionario con información del pokémon."""
        pokemon_dict = self.pokemon.to_dict()
        return {
            'id': self.id,
            'pokemon': pokemon_dict,
            'apodo': self.apodo,
            'fecha_captura': self.fecha_captura.isoformat() if self.fecha_captura else None
        }
    
    def __repr__(self):
        return f'<PokemonCapturado usuario_id={self.usuario_id} pokemon_id={self.pokemon_id}>'
