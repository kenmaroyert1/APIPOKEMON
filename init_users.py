"""
Script para inicializar usuarios de prueba en la base de datos.
Crea un profesor y un entrenador de ejemplo.

Ejecutar: python init_users.py
"""
from app import app
from Config.DataBase import db
from Models.Usuario import Usuario

def init_usuarios_prueba():
    """Crea usuarios de prueba si no existen."""
    with app.app_context():
        print("=" * 60)
        print("🔧 INICIALIZANDO USUARIOS DE PRUEBA")
        print("=" * 60)
        
        # Crear tablas si no existen
        db.create_all()
        print("\n✓ Tablas de base de datos verificadas\n")
        
        # Usuario 1: Profesor
        profesor_email = "profesor@universidad.edu"
        if not Usuario.query.filter_by(email=profesor_email).first():
            profesor = Usuario(
                email=profesor_email,
                nombre="Profesor Oak",
                rol="profesor"
            )
            profesor.set_password("profesor123")
            db.session.add(profesor)
            print(f"✓ Profesor creado: {profesor_email} / profesor123")
        else:
            print(f"⚠  Profesor ya existe: {profesor_email}")
        
        # Usuario 2: Entrenador 1
        trainer1_email = "ash@pokemon.com"
        if not Usuario.query.filter_by(email=trainer1_email).first():
            trainer1 = Usuario(
                email=trainer1_email,
                nombre="Ash Ketchum",
                rol="trainer"
            )
            trainer1.set_password("ash123")
            db.session.add(trainer1)
            print(f"✓ Entrenador creado: {trainer1_email} / ash123")
        else:
            print(f"⚠  Entrenador ya existe: {trainer1_email}")
        
        # Usuario 3: Entrenador 2
        trainer2_email = "misty@pokemon.com"
        if not Usuario.query.filter_by(email=trainer2_email).first():
            trainer2 = Usuario(
                email=trainer2_email,
                nombre="Misty",
                rol="trainer"
            )
            trainer2.set_password("misty123")
            db.session.add(trainer2)
            print(f"✓ Entrenador creado: {trainer2_email} / misty123")
        else:
            print(f"⚠  Entrenador ya existe: {trainer2_email}")
        
        # Guardar cambios
        try:
            db.session.commit()
            print("\n" + "=" * 60)
            print("✅ USUARIOS INICIALIZADOS CORRECTAMENTE")
            print("=" * 60)
            print("\n📋 CREDENCIALES DE ACCESO:")
            print("-" * 60)
            print("PROFESOR:")
            print(f"  Email: {profesor_email}")
            print("  Password: profesor123")
            print("  Permisos: TODOS (crear, ver, actualizar, eliminar)")
            print()
            print("ENTRENADOR 1:")
            print(f"  Email: {trainer1_email}")
            print("  Password: ash123")
            print("  Permisos: Ver y liberar solo sus pokémons")
            print()
            print("ENTRENADOR 2:")
            print(f"  Email: {trainer2_email}")
            print("  Password: misty123")
            print("  Permisos: Ver y liberar solo sus pokémons")
            print("=" * 60)
            print("\n💡 Usa estos usuarios para probar la API")
            print("   Endpoint de login: POST http://localhost:5000/auth/login")
            print()
            
        except Exception as e:
            db.session.rollback()
            print(f"\n❌ Error al guardar usuarios: {e}")
            raise

if __name__ == "__main__":
    init_usuarios_prueba()
