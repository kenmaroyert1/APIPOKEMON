CREATE TABLE IF NOT EXISTS pokemon (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    tipo VARCHAR(50) NOT NULL,
    nivel INT NOT NULL,
    poder_ataque FLOAT NOT NULL,
    poder_defensa FLOAT NOT NULL,
    hp INT NOT NULL,
    descripcion TEXT
);