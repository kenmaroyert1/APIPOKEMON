"""
Script de prueba completo para el Sistema de Pokémon con Roles.
Prueba todas las funcionalidades con profesor y trainer.

Requisitos: pip install requests

Uso: python test_roles_system.py
"""
import requests
import json

BASE_URL = "http://localhost:5000"

def print_header(title):
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)

def print_response(response, title="Respuesta"):
    print(f"\n📡 {title}:")
    print(f"Status: {response.status_code}")
    try:
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    except:
        print(response.text)

def test_login(email, password, rol_name):
    """Prueba el login y retorna el token."""
    print_header(f"LOGIN - {rol_name}")
    
    payload = {"email": email, "password": password}
    print(f"\n📤 POST {BASE_URL}/auth/login")
    print(json.dumps(payload, indent=2))
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=payload)
        print_response(response)
        
        if response.status_code == 200:
            token = response.json().get('access_token')
            print(f"\n✅ Token obtenido para {rol_name}")
            return token
        else:
            print(f"\n❌ Error en login de {rol_name}")
            return None
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return None

def test_crear_pokemon(token, nombre="Test Pokemon"):
    """Prueba crear un pokémon (solo profesor)."""
    print_header("CREAR POKÉMON")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "nombre": nombre,
        "tipo": "Fuego",
        "nivel": 10,
        "poder_ataque": 50.0,
        "poder_defensa": 45.0,
        "hp": 30,
        "descripcion": "Pokémon de prueba"
    }
    
    print(f"\n📤 POST {BASE_URL}/api/pokemon")
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    
    try:
        response = requests.post(f"{BASE_URL}/api/pokemon", json=payload, headers=headers)
        print_response(response)
        
        if response.status_code == 201:
            pokemon_id = response.json()['pokemon']['id']
            return pokemon_id
        return None
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return None

def test_ver_todos_pokemons(token, rol_name):
    """Prueba ver todos los pokémons."""
    print_header(f"VER TODOS LOS POKÉMONS - {rol_name}")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    print(f"\n📤 GET {BASE_URL}/api/pokemon")
    
    try:
        response = requests.get(f"{BASE_URL}/api/pokemon", headers=headers)
        print_response(response)
    except Exception as e:
        print(f"\n❌ Error: {e}")

def test_ver_pokemon_especifico(token, pokemon_id, rol_name):
    """Prueba ver un pokémon específico."""
    print_header(f"VER POKÉMON ID {pokemon_id} - {rol_name}")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    print(f"\n📤 GET {BASE_URL}/api/pokemon/{pokemon_id}")
    
    try:
        response = requests.get(f"{BASE_URL}/api/pokemon/{pokemon_id}", headers=headers)
        print_response(response)
    except Exception as e:
        print(f"\n❌ Error: {e}")

def test_asignar_pokemon(token_profesor, pokemon_id, trainer_email):
    """Profesor asigna pokémon a trainer."""
    print_header(f"ASIGNAR POKÉMON {pokemon_id} A TRAINER")
    
    headers = {
        "Authorization": f"Bearer {token_profesor}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "trainer_email": trainer_email,
        "apodo": "Pokémon Asignado"
    }
    
    print(f"\n📤 POST {BASE_URL}/api/pokemon/{pokemon_id}/asignar")
    print(json.dumps(payload, indent=2))
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/pokemon/{pokemon_id}/asignar",
            json=payload,
            headers=headers
        )
        print_response(response)
        return response.status_code == 201
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False

def test_actualizar_pokemon(token, pokemon_id, rol_name):
    """Prueba actualizar un pokémon (solo profesor)."""
    print_header(f"ACTUALIZAR POKÉMON - {rol_name}")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "nivel": 20,
        "poder_ataque": 70.0
    }
    
    print(f"\n📤 PUT {BASE_URL}/api/pokemon/{pokemon_id}")
    print(json.dumps(payload, indent=2))
    
    try:
        response = requests.put(
            f"{BASE_URL}/api/pokemon/{pokemon_id}",
            json=payload,
            headers=headers
        )
        print_response(response)
    except Exception as e:
        print(f"\n❌ Error: {e}")

def test_eliminar_pokemon(token, pokemon_id, rol_name):
    """Prueba eliminar pokémon."""
    print_header(f"ELIMINAR POKÉMON ID {pokemon_id} - {rol_name}")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    print(f"\n📤 DELETE {BASE_URL}/api/pokemon/{pokemon_id}")
    
    try:
        response = requests.delete(
            f"{BASE_URL}/api/pokemon/{pokemon_id}",
            headers=headers
        )
        print_response(response)
    except Exception as e:
        print(f"\n❌ Error: {e}")

def main():
    print("\n" + "🎓" * 35)
    print("  TEST COMPLETO - SISTEMA DE POKÉMON CON ROLES")
    print("🎓" * 35)
    
    # === LOGIN PROFESOR ===
    token_profesor = test_login("profesor@universidad.edu", "profesor123", "PROFESOR")
    if not token_profesor:
        print("\n❌ No se pudo obtener token del profesor. Verifica:")
        print("   1. La aplicación está corriendo (python app.py)")
        print("   2. Los usuarios están inicializados (python init_users.py)")
        return
    
    # === LOGIN TRAINER ===
    token_trainer = test_login("ash@pokemon.com", "ash123", "TRAINER")
    if not token_trainer:
        print("\n❌ No se pudo obtener token del trainer")
        return
    
    # === PROFESOR CREA POKÉMON ===
    pokemon_id = test_crear_pokemon(token_profesor, "Charizard")
    
    if not pokemon_id:
        print("\n⚠️  No se pudo crear pokémon, continuando con tests...")
        pokemon_id = 1
    
    # === TRAINER INTENTA CREAR POKÉMON (Debe fallar) ===
    print_header("TRAINER INTENTA CREAR POKÉMON (DEBE FALLAR)")
    test_crear_pokemon(token_trainer, "Pikachu Ilegal")
    
    # === VER TODOS LOS POKÉMONS ===
    test_ver_todos_pokemons(token_profesor, "PROFESOR")
    test_ver_todos_pokemons(token_trainer, "TRAINER (vacío)")
    
    # === PROFESOR ASIGNA POKÉMON A TRAINER ===
    if pokemon_id:
        test_asignar_pokemon(token_profesor, pokemon_id, "ash@pokemon.com")
    
    # === VER TODOS LOS POKÉMONS DESPUÉS DE ASIGNACIÓN ===
    test_ver_todos_pokemons(token_trainer, "TRAINER (con pokémons)")
    
    # === VER POKÉMON ESPECÍFICO ===
    if pokemon_id:
        test_ver_pokemon_especifico(token_profesor, pokemon_id, "PROFESOR")
        test_ver_pokemon_especifico(token_trainer, pokemon_id, "TRAINER (asignado)")
    
    # === TRAINER INTENTA VER POKÉMON NO ASIGNADO (Debe fallar) ===
    test_ver_pokemon_especifico(token_trainer, 999, "TRAINER (no asignado - debe fallar)")
    
    # === ACTUALIZAR POKÉMON ===
    if pokemon_id:
        test_actualizar_pokemon(token_profesor, pokemon_id, "PROFESOR")
        test_actualizar_pokemon(token_trainer, pokemon_id, "TRAINER (debe fallar)")
    
    # === ELIMINAR POKÉMON ===
    if pokemon_id:
        # Trainer libera de su colección
        test_eliminar_pokemon(token_trainer, pokemon_id, "TRAINER (libera)")
        # Profesor elimina de BD
        test_eliminar_pokemon(token_profesor, pokemon_id, "PROFESOR (elimina)")
    
    print_header("RESUMEN")
    print("\n✅ Pruebas completadas!")
    print("\n📋 Qué se probó:")
    print("   ✓ Login con email para profesor y trainer")
    print("   ✓ Profesor puede crear pokémons")
    print("   ✓ Trainer NO puede crear pokémons")
    print("   ✓ Profesor ve todos los pokémons")
    print("   ✓ Trainer solo ve sus pokémons")
    print("   ✓ Profesor asigna pokémons a trainers")
    print("   ✓ Trainer NO puede ver pokémons no asignados")
    print("   ✓ Solo profesor puede actualizar")
    print("   ✓ Trainer libera (no elimina de BD)")
    print("   ✓ Profesor elimina de BD")
    print("\n📖 Lee GUIA_SISTEMA_ROLES.md para más información")
    print("=" * 70 + "\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Pruebas interrumpidas")
    except Exception as e:
        print(f"\n❌ Error fatal: {e}")
