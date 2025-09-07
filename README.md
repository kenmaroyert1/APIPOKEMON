# API Pokémon

Una API RESTful construida con Flask para gestionar información de Pokémon. Esta API permite realizar operaciones CRUD (Crear, Leer, Actualizar y Eliminar) sobre una base de datos de Pokémon.

## 🚀 Características

- Arquitectura en capas (Controladores, Servicios, Repositorios, Modelos)
- Operaciones CRUD completas
- Base de datos SQLite
- Validación de datos
- Pruebas unitarias
- Documentación de endpoints

## 📋 Requisitos Previos

- Python 3.x
- pip (gestor de paquetes de Python)

## 🔧 Dependencias Principales

- Flask
- Flask-SQLAlchemy
- SQLAlchemy
- python-dotenv
- pytest
- pytest-flask

## ⚙️ Instalación

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/kenmaroyert1/APIPOKEMON.git
   cd APIPOKEMON
   ```

2. Crear y activar un entorno virtual:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. Instalar las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Ejecutar la Aplicación

```bash
python app.py
```

La aplicación se ejecutará en `http://localhost:5000`

## 🛣️ Endpoints Disponibles

### Página de Bienvenida
- `GET /`
  - Retorna información general sobre la API y sus endpoints disponibles

### Operaciones con Pokémon
- `GET /api/pokemon`
  - Obtiene la lista de todos los pokémon
- `GET /api/pokemon/<id>`
  - Obtiene un pokémon específico por ID
- `POST /api/pokemon`
  - Crea un nuevo pokémon
- `PUT /api/pokemon/<id>`
  - Actualiza un pokémon existente
- `DELETE /api/pokemon/<id>`
  - Elimina un pokémon

## 📦 Estructura del Proyecto

```
APIPOKEMON/
├── app.py                  # Punto de entrada de la aplicación
├── requirements.txt        # Dependencias del proyecto
├── pokemon.db             # Base de datos SQLite
│
├── Config/                # Configuración de la aplicación
│   └── DataBase.py       # Configuración de la base de datos
│
├── Controllers/           # Controladores de la API
│   └── PokemonController.py
│
├── Models/               # Modelos de datos
│   └── Pokemon.py
│
├── Repositories/         # Capa de acceso a datos
│   └── PokemonRepositories.py
│
├── Services/            # Lógica de negocio
│   └── PokemonService.py
│
└── Test/               # Pruebas unitarias
    └── TestDataBase.py
```

## 📝 Formato de Datos

### Crear/Actualizar Pokémon
```json
{
    "nombre": "string (requerido)",
    "tipo": "string (requerido)",
    "nivel": "integer (requerido, positivo)",
    "poder_ataque": "float (requerido)",
    "poder_defensa": "float (requerido)",
    "hp": "integer (requerido, positivo)",
    "descripcion": "string (opcional)"
}
```

## 🧪 Ejecutar Pruebas

```bash
pytest
```

## 👥 Autor

- **Kenma Royert** - [kenmaroyert1](https://github.com/kenmaroyert1)

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - mira el archivo `LICENSE` para más detalles.
