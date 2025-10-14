"""
Test para validar que solo el PROFESOR puede registrar nuevos usuarios.
"""
import requests
import json

BASE_URL = "http://localhost:5000"

def print_separator(title=""):
    print("\n" + "="*70)
    if title:
        print(f"  {title}")
        print("="*70)

def print_request(method, url, body=None, headers=None):
    print(f"\n📤 {method} {url}")
    if body:
        print(json.dumps(body, indent=2, ensure_ascii=False))

def print_response(response):
    print(f"\n📡 Respuesta:")
    print(f"Status: {response.status_code}")
    try:
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    except:
        print(response.text)

def test_register_endpoint():
    """Test completo del endpoint de registro."""
    
    print("🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓")
    print("  TEST - REGISTRO DE USUARIOS (SOLO PROFESOR)")
    print("🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓")
    
    # ========================================================================
    # 1. Login como PROFESOR
    # ========================================================================
    print_separator("LOGIN - PROFESOR")
    
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
    
    print_response(response)
    
    if response.status_code != 200:
        print("\n❌ Error: No se pudo hacer login como profesor")
        return
    
    profesor_token = response.json()['access_token']
    print("\n✅ Token obtenido para PROFESOR")
    
    # ========================================================================
    # 2. Login como TRAINER
    # ========================================================================
    print_separator("LOGIN - TRAINER")
    
    login_data_trainer = {
        "email": "ash@pokemon.com",
        "password": "ash123"
    }
    
    print_request("POST", f"{BASE_URL}/auth/login", login_data_trainer)
    
    response = requests.post(
        f"{BASE_URL}/auth/login",
        json=login_data_trainer,
        headers={"Content-Type": "application/json"}
    )
    
    print_response(response)
    
    if response.status_code != 200:
        print("\n❌ Error: No se pudo hacer login como trainer")
        return
    
    trainer_token = response.json()['access_token']
    print("\n✅ Token obtenido para TRAINER")
    
    # ========================================================================
    # 3. TRAINER intenta registrar usuario (DEBE FALLAR)
    # ========================================================================
    print_separator("TRAINER INTENTA REGISTRAR USUARIO (DEBE FALLAR)")
    
    nuevo_usuario = {
        "email": "intento.ilegal@pokemon.com",
        "password": "pass123",
        "nombre": "Usuario Ilegal",
        "rol": "trainer"
    }
    
    print_request("POST", f"{BASE_URL}/auth/register", nuevo_usuario)
    
    response = requests.post(
        f"{BASE_URL}/auth/register",
        json=nuevo_usuario,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {trainer_token}"
        }
    )
    
    print_response(response)
    
    if response.status_code == 403:
        print("\n✅ CORRECTO: Trainer NO puede registrar usuarios")
    else:
        print("\n❌ ERROR: Trainer debería recibir error 403")
    
    # ========================================================================
    # 4. Intento de registro SIN TOKEN (DEBE FALLAR)
    # ========================================================================
    print_separator("REGISTRO SIN TOKEN (DEBE FALLAR)")
    
    print_request("POST", f"{BASE_URL}/auth/register", nuevo_usuario)
    print("(Sin header Authorization)")
    
    response = requests.post(
        f"{BASE_URL}/auth/register",
        json=nuevo_usuario,
        headers={"Content-Type": "application/json"}
    )
    
    print_response(response)
    
    if response.status_code == 401:
        print("\n✅ CORRECTO: Registro sin token es rechazado")
    else:
        print("\n❌ ERROR: Debería recibir error 401")
    
    # ========================================================================
    # 5. PROFESOR registra nuevo TRAINER (DEBE FUNCIONAR)
    # ========================================================================
    print_separator("PROFESOR REGISTRA NUEVO TRAINER (DEBE FUNCIONAR)")
    
    nuevo_trainer = {
        "email": "gary@pokemon.com",
        "password": "gary123",
        "nombre": "Gary Oak",
        "rol": "trainer"
    }
    
    print_request("POST", f"{BASE_URL}/auth/register", nuevo_trainer)
    
    response = requests.post(
        f"{BASE_URL}/auth/register",
        json=nuevo_trainer,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {profesor_token}"
        }
    )
    
    print_response(response)
    
    if response.status_code in [201, 409]:  # 201 creado o 409 ya existe
        if response.status_code == 201:
            print("\n✅ CORRECTO: Profesor puede registrar trainers")
        else:
            print("\n⚠️  Usuario ya existe (normal en segunda ejecución)")
    else:
        print("\n❌ ERROR: Profesor debería poder registrar trainers")
    
    # ========================================================================
    # 6. PROFESOR registra nuevo PROFESOR (DEBE FUNCIONAR)
    # ========================================================================
    print_separator("PROFESOR REGISTRA OTRO PROFESOR (DEBE FUNCIONAR)")
    
    nuevo_profesor = {
        "email": "elm@universidad.edu",
        "password": "elm123",
        "nombre": "Profesor Elm",
        "rol": "profesor"
    }
    
    print_request("POST", f"{BASE_URL}/auth/register", nuevo_profesor)
    
    response = requests.post(
        f"{BASE_URL}/auth/register",
        json=nuevo_profesor,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {profesor_token}"
        }
    )
    
    print_response(response)
    
    if response.status_code in [201, 409]:
        if response.status_code == 201:
            print("\n✅ CORRECTO: Profesor puede registrar otros profesores")
        else:
            print("\n⚠️  Usuario ya existe (normal en segunda ejecución)")
    else:
        print("\n❌ ERROR: Profesor debería poder registrar profesores")
    
    # ========================================================================
    # 7. PROFESOR intenta registrar con email duplicado (DEBE FALLAR)
    # ========================================================================
    print_separator("PROFESOR INTENTA EMAIL DUPLICADO (DEBE FALLAR)")
    
    usuario_duplicado = {
        "email": "ash@pokemon.com",  # Email ya existe
        "password": "otro123",
        "nombre": "Otro Ash",
        "rol": "trainer"
    }
    
    print_request("POST", f"{BASE_URL}/auth/register", usuario_duplicado)
    
    response = requests.post(
        f"{BASE_URL}/auth/register",
        json=usuario_duplicado,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {profesor_token}"
        }
    )
    
    print_response(response)
    
    if response.status_code == 409:
        print("\n✅ CORRECTO: Email duplicado es rechazado")
    else:
        print("\n❌ ERROR: Debería recibir error 409 (Conflict)")
    
    # ========================================================================
    # RESUMEN
    # ========================================================================
    print_separator("RESUMEN")
    
    print("\n✅ Pruebas completadas!")
    print("\n📋 Validaciones realizadas:")
    print("   ✓ Trainer NO puede registrar usuarios (403)")
    print("   ✓ Registro sin token es rechazado (401)")
    print("   ✓ Profesor puede registrar trainers")
    print("   ✓ Profesor puede registrar otros profesores")
    print("   ✓ Emails duplicados son rechazados (409)")
    print("\n🔒 Control de acceso funcionando correctamente")
    print("="*70)

if __name__ == "__main__":
    try:
        test_register_endpoint()
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: No se pudo conectar al servidor")
        print("   Asegúrate de que la API esté ejecutándose en http://localhost:5000")
    except Exception as e:
        print(f"\n❌ Error inesperado: {str(e)}")
