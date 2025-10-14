"""
Script de prueba para la API con JWT.
Puedes ejecutar este script para probar que todo funcione correctamente.

Requisitos:
    pip install requests

Uso:
    python test_jwt_api.py
"""
import requests
import json

# Configuración
BASE_URL = "http://localhost:5000"
AUTH_URL = f"{BASE_URL}/auth"
API_URL = f"{BASE_URL}/api"

def print_section(title):
    """Imprime un separador visual."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)

def print_response(response, title="Respuesta"):
    """Imprime una respuesta HTTP de forma legible."""
    print(f"\n📡 {title}:")
    print(f"Status Code: {response.status_code}")
    try:
        print(f"Body: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except:
        print(f"Body: {response.text}")

def test_login():
    """Prueba el endpoint de login."""
    print_section("1. PROBANDO LOGIN")
    
    payload = {
        "username": "admin",
        "password": "admin123"
    }
    
    print(f"\n📤 POST {AUTH_URL}/login")
    print(f"Body: {json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(f"{AUTH_URL}/login", json=payload)
        print_response(response, "Login Response")
        
        if response.status_code == 200:
            token = response.json().get('access_token')
            print(f"\n✅ Token obtenido exitosamente!")
            print(f"Token (primeros 50 caracteres): {token[:50]}...")
            return token
        else:
            print("\n❌ Error al hacer login")
            return None
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: No se pudo conectar al servidor.")
        print("   Asegúrate de que la aplicación Flask esté ejecutándose (python app.py)")
        return None
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        return None

def test_protected_route(token):
    """Prueba una ruta protegida con el token."""
    print_section("2. PROBANDO RUTA PROTEGIDA")
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    print(f"\n📤 GET {AUTH_URL}/protected")
    print(f"Headers: Authorization: Bearer {token[:30]}...")
    
    try:
        response = requests.get(f"{AUTH_URL}/protected", headers=headers)
        print_response(response, "Protected Route Response")
        
        if response.status_code == 200:
            print("\n✅ Acceso a ruta protegida exitoso!")
        else:
            print("\n❌ Error al acceder a ruta protegida")
    except Exception as e:
        print(f"\n❌ Error: {e}")

def test_get_current_user(token):
    """Obtiene información del usuario actual."""
    print_section("3. OBTENIENDO INFORMACIÓN DEL USUARIO")
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    print(f"\n📤 GET {AUTH_URL}/me")
    
    try:
        response = requests.get(f"{AUTH_URL}/me", headers=headers)
        print_response(response, "Current User Info")
        
        if response.status_code == 200:
            print("\n✅ Información de usuario obtenida!")
        else:
            print("\n❌ Error al obtener información")
    except Exception as e:
        print(f"\n❌ Error: {e}")

def test_create_pokemon(token):
    """Prueba crear un pokémon (si la ruta está protegida)."""
    print_section("4. CREANDO POKÉMON (Con Token)")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    pokemon_data = {
        "nombre": "Pikachu Test",
        "tipo": "Eléctrico",
        "nivel": 25,
        "poder_ataque": 55.0,
        "poder_defensa": 40.0,
        "hp": 35,
        "descripcion": "Pokémon de prueba con JWT"
    }
    
    print(f"\n📤 POST {API_URL}/pokemon")
    print(f"Body: {json.dumps(pokemon_data, indent=2, ensure_ascii=False)}")
    
    try:
        response = requests.post(f"{API_URL}/pokemon", json=pokemon_data, headers=headers)
        print_response(response, "Create Pokemon Response")
        
        if response.status_code == 201:
            print("\n✅ Pokémon creado exitosamente!")
        else:
            print("\n⚠️  Nota: Si la ruta no está protegida, funcionará sin token también")
    except Exception as e:
        print(f"\n❌ Error: {e}")

def test_without_token():
    """Prueba acceder a una ruta protegida sin token."""
    print_section("5. PROBANDO ACCESO SIN TOKEN (Debe Fallar)")
    
    print(f"\n📤 GET {AUTH_URL}/protected (sin token)")
    
    try:
        response = requests.get(f"{AUTH_URL}/protected")
        print_response(response, "Protected Route Without Token")
        
        if response.status_code == 401:
            print("\n✅ Protección funcionando correctamente (401 Unauthorized)")
        else:
            print("\n⚠️  Advertencia: La ruta no está rechazando peticiones sin token")
    except Exception as e:
        print(f"\n❌ Error: {e}")

def main():
    """Función principal que ejecuta todas las pruebas."""
    print("\n" + "🔐" * 35)
    print("  TEST DE API CON JWT - API POKÉMON")
    print("🔐" * 35)
    
    # 1. Login
    token = test_login()
    
    if not token:
        print("\n❌ No se pudo obtener el token. Verifica que:")
        print("   1. La aplicación esté ejecutándose (python app.py)")
        print("   2. El servidor esté en http://localhost:5000")
        print("   3. Las credenciales sean correctas (admin/admin123)")
        return
    
    # 2. Ruta protegida con token
    test_protected_route(token)
    
    # 3. Información del usuario
    test_get_current_user(token)
    
    # 4. Crear pokémon con token
    test_create_pokemon(token)
    
    # 5. Intentar sin token
    test_without_token()
    
    print_section("RESUMEN")
    print("\n✅ Pruebas completadas!")
    print("\n📋 Próximos pasos:")
    print("   1. Revisa los resultados arriba")
    print("   2. Prueba con Postman o Thunder Client")
    print("   3. Lee JWT_SETUP_GUIDE.md para más información")
    print("\n" + "=" * 70 + "\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Pruebas interrumpidas por el usuario.")
    except Exception as e:
        print(f"\n❌ Error fatal: {e}")
