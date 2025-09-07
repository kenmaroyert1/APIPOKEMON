from Config.DataBase import db

class Pokemon(db.Model):
    __tablename__ = 'pokemon'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    nivel = db.Column(db.Integer, nullable=False)
    poder_ataque = db.Column(db.Float, nullable=False)
    poder_defensa = db.Column(db.Float, nullable=False)
    hp = db.Column(db.Integer, nullable=False)
    descripcion = db.Column(db.Text)
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'tipo': self.tipo,
            'nivel': self.nivel,
            'poder_ataque': self.poder_ataque,
            'poder_defensa': self.poder_defensa,
            'hp': self.hp,
            'descripcion': self.descripcion
        }