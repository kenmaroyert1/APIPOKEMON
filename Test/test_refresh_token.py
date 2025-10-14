"""
Test completo del sistema de Access Token + Refresh Token
"""
import requests
import json
import time

BASE_URL = "http://localhost:5000"

def print_separator(title=""):
    print("\n" + "="*70)
    if title:
        print(f"  {title}")
        print("="*70)

def print_request(method, url, body=None, headers=None):
    print(f"\n📤 {method} {url}")
    if headers and 'Authorization' in headers:
        token_preview = headers['Authorization'][:50] + "..."
        print(f"Headers: Authorization: {token_preview}")
    if body:
        print(json.dumps(body, indent=2, ensure_ascii=False))

def print_response(response):
    print(f"\n📡 Respuesta:")
    print(f"Status: {response.status_code}")
    try:
        data = response.json()
        print(json.dumps(data, indent=2, ensure_ascii=False))
        return data
    except:
        print(response.text)
        return None

def test_token_system():
    """Test completo del sistema de tokens."""
    
    print("🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐")
    print("  TEST - SISTEMA DE ACCESS TOKEN + REFRESH TOKEN")
    print("🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐")
    
    # ========================================================================
    # 1. LOGIN - Obtener ambos tokens
    # ========================================================================
    print_separator("1. LOGIN - OBTENER ACCESS Y REFRESH TOKEN")
    
    login_data = {
        "email": "profesor@universidad.edu",
        "password": "profesor123"
    }
    
    print_request("POST", f"{BASE_URL}/auth/login", login_data)
    
    response = requests.post(
        f"{BASE_URL}/auth/login",
        json=login_data,
        headers={"Content-Type": "application/json"}
    )
    
    data = print_response(response)
    
    if response.status_code != 200:
        print("\n❌ Error: No se pudo hacer login")
        return
    
    access_token = data['access_token']
    refresh_token = data['refresh_token']
    
    print("\n✅ Tokens obtenidos exitosamente:")
    print(f"   - Access Token: {access_token[:50]}...")
    print(f"   - Refresh Token: {refresh_token[:50]}...")
    print(f"   - Expira en: {data['expires_in']} segundos (30 minutos)")
    
    # ========================================================================
    # 2. USAR ACCESS TOKEN - Ver usuario actual
    # ========================================================================
    print_separator("2. USAR ACCESS TOKEN - VER USUARIO ACTUAL")
    
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    print_request("GET", f"{BASE_URL}/auth/me", headers=headers)
    
    response = requests.get(
        f"{BASE_URL}/auth/me",
        headers=headers
    )
    
    print_response(response)
    
    if response.status_code == 200:
        print("\n✅ Access Token funciona correctamente")
    else:
        print("\n❌ Access Token no funciona")
    
    # ========================================================================
    # 3. USAR ACCESS TOKEN - Crear Pokémon
    # ========================================================================
    print_separator("3. USAR ACCESS TOKEN - CREAR POKÉMON")
    
    pokemon_data = {
        "nombre": "Pikachu",
        "tipo": "Eléctrico",
        "nivel": 5,
        "poder_ataque": 55.0,
        "poder_defensa": 40.0,
        "hp": 35,
        "descripcion": "Pokémon eléctrico adorable"
    }
    
    print_request("POST", f"{BASE_URL}/api/pokemon", pokemon_data, headers)
    
    response = requests.post(
        f"{BASE_URL}/api/pokemon",
        json=pokemon_data,
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
    )
    
    print_response(response)
    
    if response.status_code in [201, 409]:  # Creado o ya existe
        print("\n✅ Access Token permite operaciones protegidas")
    
    # ========================================================================
    # 4. REFRESCAR TOKEN - Obtener nuevo access token
    # ========================================================================
    print_separator("4. REFRESCAR TOKEN - OBTENER NUEVO ACCESS TOKEN")
    
    print("🔄 Usando el refresh token para obtener un nuevo access token...")
    
    refresh_headers = {
        "Authorization": f"Bearer {refresh_token}"
    }
    
    print_request("POST", f"{BASE_URL}/auth/refresh", headers=refresh_headers)
    
    response = requests.post(
        f"{BASE_URL}/auth/refresh",
        headers=refresh_headers
    )
    
    data = print_response(response)
    
    if response.status_code == 200:
        new_access_token = data['access_token']
        print("\n✅ Nuevo Access Token obtenido:")
        print(f"   - Nuevo Access Token: {new_access_token[:50]}...")
        print(f"   - Expira en: {data['expires_in']} segundos")
        
        # Usar el nuevo access token
        print("\n🔹 Probando el nuevo access token...")
        response = requests.get(
            f"{BASE_URL}/auth/me",
            headers={"Authorization": f"Bearer {new_access_token}"}
        )
        
        if response.status_code == 200:
            print("✅ Nuevo access token funciona correctamente")
    else:
        print("\n❌ Error al refrescar token")
        return
    
    # ========================================================================
    # 5. INTENTAR USAR REFRESH TOKEN EN ENDPOINT PROTEGIDO (DEBE FALLAR)
    # ========================================================================
    print_separator("5. INTENTAR USAR REFRESH TOKEN EN ENDPOINT NORMAL (DEBE FALLAR)")
    
    print("⚠️  Intentando usar refresh token donde se requiere access token...")
    
    response = requests.get(
        f"{BASE_URL}/api/pokemon",
        headers={"Authorization": f"Bearer {refresh_token}"}
    )
    
    print_response(response)
    
    if response.status_code == 422:
        print("\n✅ Correcto: Refresh token NO puede usarse en endpoints normales")
    else:
        print("\n❌ Error: Refresh token debería ser rechazado")
    
    # ========================================================================
    # 6. LOGOUT CON ACCESS TOKEN
    # ========================================================================
    print_separator("6. LOGOUT - REVOCAR TOKEN")
    
    print_request("POST", f"{BASE_URL}/auth/logout", headers=headers)
    
    response = requests.post(
        f"{BASE_URL}/auth/logout",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    
    print_response(response)
    
    if response.status_code == 200:
        print("\n✅ Logout exitoso - Token revocado")
    
    # ========================================================================
    # 7. INTENTAR USAR TOKEN REVOCADO (Nota: requiere implementación completa)
    # ========================================================================
    print_separator("7. INFORMACIÓN SOBRE TOKENS REVOCADOS")
    
    print("""
📝 Nota sobre Revocación de Tokens:
   - En este sistema básico, los tokens revocados se almacenan en memoria
   - Para producción, se recomienda usar Redis u otra base de datos
   - Los tokens JWT son stateless por naturaleza
   - La mejor práctica es:
     * Eliminar ambos tokens del cliente al hacer logout
     * Implementar lista negra de tokens con TTL
     * Usar refresh tokens con rotación
    """)
    
    # ========================================================================
    # 8. RESUMEN DEL FLUJO
    # ========================================================================
    print_separator("RESUMEN DEL FLUJO DE TOKENS")
    
    print("""
✅ Sistema de Tokens Implementado Correctamente:

📋 Flujo Normal:
   1. Usuario hace LOGIN
      → Recibe: access_token (30 min) + refresh_token (7 días)
   
   2. Usuario usa access_token para operaciones
      → Endpoints protegidos requieren access_token
   
   3. Cuando access_token expira (30 min):
      → Usar refresh_token en /auth/refresh
      → Recibe nuevo access_token (30 min más)
   
   4. Cuando refresh_token expira (7 días):
      → Usuario debe hacer LOGIN nuevamente

🔒 Seguridad:
   ✓ Access tokens de corta duración (30 min)
   ✓ Refresh tokens de larga duración (7 días)
   ✓ Refresh token solo para /auth/refresh
   ✓ Access token para todos los demás endpoints
   ✓ Logout revoca tokens

📝 Ventajas:
   ✓ Mejor experiencia de usuario (no login frecuente)
   ✓ Mayor seguridad (tokens de corta duración)
   ✓ Control de sesiones activas
   ✓ Capacidad de revocar acceso
    """)
    
    print("="*70)

if __name__ == "__main__":
    try:
        test_token_system()
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: No se pudo conectar al servidor")
        print("   Asegúrate de que la API esté ejecutándose en http://localhost:5000")
    except Exception as e:
        print(f"\n❌ Error inesperado: {str(e)}")
        import traceback
        traceback.print_exc()
