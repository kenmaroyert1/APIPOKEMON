# 🔐 Sistema de Access Token + Refresh Token

## 📋 Descripción General

El sistema ahora implementa un mecanismo de **doble token** para mayor seguridad y mejor experiencia de usuario:

- **Access Token**: Token de corta duración (30 minutos) para acceder a endpoints protegidos
- **Refresh Token**: Token de larga duración (7 días) para obtener nuevos access tokens

---

## 🎯 ¿Por Qué Usar Este Sistema?

### ❌ **Problema con un solo token:**
- Token de larga duración = mayor riesgo si es robado
- Token de corta duración = usuario debe hacer login frecuentemente

### ✅ **Solución con doble token:**
- **Access Token corto**: Minimiza riesgo si es comprometido
- **Refresh Token largo**: Evita logins frecuentes
- **Mejor balance**: Seguridad + Experiencia de usuario

---

## 🔄 Flujo Completo

```
┌─────────────┐
│   Cliente   │
└──────┬──────┘
       │
       │ 1. POST /auth/login
       │    {email, password}
       ▼
┌─────────────────────┐
│      Servidor       │
│  Valida credenciales│
└──────┬──────────────┘
       │
       │ 2. Retorna:
       │    - access_token (30 min)
       │    - refresh_token (7 días)
       ▼
┌─────────────┐
│   Cliente   │
│ Guarda ambos│
│   tokens    │
└──────┬──────┘
       │
       │ 3. Usa access_token
       │    en cada request
       ▼
┌─────────────────────┐
│  Endpoints          │
│  Protegidos         │
│  /api/pokemon, etc  │
└─────────────────────┘
       
       ⏰ [30 minutos después]
       
┌─────────────┐
│   Cliente   │
│ access_token│
│  expirado   │
└──────┬──────┘
       │
       │ 4. POST /auth/refresh
       │    con refresh_token
       ▼
┌─────────────────────┐
│      Servidor       │
│ Valida refresh_token│
└──────┬──────────────┘
       │
       │ 5. Retorna:
       │    - nuevo access_token (30 min)
       ▼
┌─────────────┐
│   Cliente   │
│ Actualiza   │
│access_token │
└─────────────┘
```

---

## 📡 Endpoints

### 1. Login - Obtener Tokens

```http
POST /auth/login
Content-Type: application/json

{
  "email": "profesor@universidad.edu",
  "password": "profesor123"
}
```

**Respuesta (200)**:
```json
{
  "message": "Login exitoso",
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "Bearer",
  "expires_in": 1800,
  "usuario": {
    "id": 1,
    "email": "profesor@universidad.edu",
    "nombre": "Profesor Oak",
    "rol": "profesor",
    "activo": true,
    "fecha_registro": "2025-10-14T16:25:52"
  }
}
```

### 2. Refresh - Obtener Nuevo Access Token

```http
POST /auth/refresh
Authorization: Bearer {refresh_token}
```

**Respuesta (200)**:
```json
{
  "message": "Token refrescado exitosamente",
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "Bearer",
  "expires_in": 1800
}
```

**Errores**:
```json
// Refresh token inválido o expirado (401)
{
  "msg": "Token has expired"
}

// Usuario no encontrado (404)
{
  "error": "Usuario no encontrado"
}

// Cuenta desactivada (403)
{
  "error": "Tu cuenta ha sido desactivada"
}
```

### 3. Logout - Revocar Token

```http
POST /auth/logout
Authorization: Bearer {access_token o refresh_token}
```

**Respuesta (200)**:
```json
{
  "message": "Logout exitoso",
  "token_revocado": "access",
  "email": "profesor@universidad.edu",
  "info": "Token revocado. Elimina ambos tokens (access y refresh) del cliente."
}
```

---

## 💻 Ejemplos de Uso

### PowerShell - Flujo Completo

```powershell
# 1. LOGIN - Obtener ambos tokens
$loginBody = @{
    email = "profesor@universidad.edu"
    password = "profesor123"
} | ConvertTo-Json

$loginResponse = Invoke-RestMethod -Uri "http://localhost:5000/auth/login" `
  -Method Post `
  -Body $loginBody `
  -ContentType "application/json"

# Guardar tokens
$accessToken = $loginResponse.access_token
$refreshToken = $loginResponse.refresh_token

Write-Host "✅ Login exitoso"
Write-Host "Access Token expira en: $($loginResponse.expires_in) segundos"

# 2. USAR ACCESS TOKEN - Crear pokémon
$headers = @{
    "Authorization" = "Bearer $accessToken"
    "Content-Type" = "application/json"
}

$pokemonData = @{
    nombre = "Pikachu"
    tipo = "Eléctrico"
    nivel = 5
    poder_ataque = 55.0
    poder_defensa = 40.0
    hp = 35
    descripcion = "Pokémon eléctrico"
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "http://localhost:5000/api/pokemon" `
  -Method Post `
  -Headers $headers `
  -Body $pokemonData

Write-Host "✅ Pokémon creado con access token"

# 3. SIMULAR EXPIRACIÓN - Refrescar token
Start-Sleep -Seconds 5  # En producción sería después de 30 minutos

$refreshHeaders = @{
    "Authorization" = "Bearer $refreshToken"
}

$refreshResponse = Invoke-RestMethod -Uri "http://localhost:5000/auth/refresh" `
  -Method Post `
  -Headers $refreshHeaders

# Actualizar access token
$accessToken = $refreshResponse.access_token

Write-Host "✅ Access token refrescado"

# 4. LOGOUT - Revocar tokens
$logoutHeaders = @{
    "Authorization" = "Bearer $accessToken"
}

Invoke-RestMethod -Uri "http://localhost:5000/auth/logout" `
  -Method Post `
  -Headers $logoutHeaders

Write-Host "✅ Logout exitoso - Tokens revocados"
```

### cURL - Ejemplos

```bash
# 1. LOGIN
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "profesor@universidad.edu",
    "password": "profesor123"
  }'

# Respuesta incluye access_token y refresh_token
# Guardar ambos tokens

# 2. USAR ACCESS TOKEN
curl -X GET http://localhost:5000/api/pokemon \
  -H "Authorization: Bearer {access_token}"

# 3. REFRESCAR TOKEN (cuando access_token expire)
curl -X POST http://localhost:5000/auth/refresh \
  -H "Authorization: Bearer {refresh_token}"

# 4. LOGOUT
curl -X POST http://localhost:5000/auth/logout \
  -H "Authorization: Bearer {access_token}"
```

### JavaScript/Fetch - Ejemplo Cliente Web

```javascript
class AuthService {
  constructor() {
    this.accessToken = null;
    this.refreshToken = null;
  }

  // 1. Login
  async login(email, password) {
    const response = await fetch('http://localhost:5000/auth/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email, password }),
    });

    const data = await response.json();
    
    if (response.ok) {
      this.accessToken = data.access_token;
      this.refreshToken = data.refresh_token;
      
      // Guardar en localStorage
      localStorage.setItem('access_token', this.accessToken);
      localStorage.setItem('refresh_token', this.refreshToken);
      
      // Programar refresh automático antes de expiración
      this.scheduleTokenRefresh(data.expires_in);
      
      return data.usuario;
    }
    
    throw new Error(data.error);
  }

  // 2. Refrescar token
  async refreshAccessToken() {
    const response = await fetch('http://localhost:5000/auth/refresh', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${this.refreshToken}`,
      },
    });

    const data = await response.json();
    
    if (response.ok) {
      this.accessToken = data.access_token;
      localStorage.setItem('access_token', this.accessToken);
      
      // Reprogramar próximo refresh
      this.scheduleTokenRefresh(data.expires_in);
      
      return true;
    }
    
    // Si el refresh token también expiró, hacer logout
    await this.logout();
    return false;
  }

  // 3. Programar refresh automático
  scheduleTokenRefresh(expiresIn) {
    // Refrescar 5 minutos antes de que expire
    const refreshTime = (expiresIn - 300) * 1000;
    
    setTimeout(() => {
      this.refreshAccessToken();
    }, refreshTime);
  }

  // 4. Hacer request con token
  async fetchWithAuth(url, options = {}) {
    const headers = {
      ...options.headers,
      'Authorization': `Bearer ${this.accessToken}`,
    };

    let response = await fetch(url, { ...options, headers });

    // Si el token expiró, intentar refrescar
    if (response.status === 401) {
      const refreshed = await this.refreshAccessToken();
      
      if (refreshed) {
        // Reintentar con nuevo token
        headers.Authorization = `Bearer ${this.accessToken}`;
        response = await fetch(url, { ...options, headers });
      }
    }

    return response;
  }

  // 5. Logout
  async logout() {
    await fetch('http://localhost:5000/auth/logout', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${this.accessToken}`,
      },
    });

    // Limpiar tokens
    this.accessToken = null;
    this.refreshToken = null;
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  }
}

// Uso:
const auth = new AuthService();

// Login
await auth.login('profesor@universidad.edu', 'profesor123');

// Hacer requests
const response = await auth.fetchWithAuth('http://localhost:5000/api/pokemon');
const pokemons = await response.json();
```

---

## ⏱️ Tiempos de Expiración

| Token | Duración | Variable de Entorno |
|-------|----------|---------------------|
| Access Token | 30 minutos | `JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30` |
| Refresh Token | 7 días | `JWT_REFRESH_TOKEN_EXPIRE_DAYS=7` |

### Configuración en `.env`:

```env
JWT_SECRET_KEY=tu-clave-secreta-super-segura
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7
```

---

## 🔒 Mejores Prácticas

### ✅ **DO - Hacer:**

1. **Guardar ambos tokens de forma segura**
   - En clientes web: `httpOnly` cookies o localStorage
   - En móviles: Keychain (iOS) o Keystore (Android)

2. **Refrescar automáticamente**
   - Programar refresh 5 minutos antes de expiración
   - Manejar errores de refresh gracefully

3. **Limpiar tokens al hacer logout**
   - Eliminar ambos tokens del cliente
   - Llamar al endpoint `/auth/logout`

4. **Manejar errores 401**
   - Intentar refresh automático
   - Si falla, redirigir a login

### ❌ **DON'T - No hacer:**

1. **No usar refresh token en endpoints normales**
   - Refresh token SOLO para `/auth/refresh`
   - Access token para todos los demás

2. **No exponer tokens en URLs**
   - Siempre usar header `Authorization`
   - Nunca query parameters

3. **No guardar tokens en lugares inseguros**
   - Evitar localStorage sin cifrado
   - No logs ni console.log con tokens

---

## 🧪 Probar el Sistema

```powershell
# Ejecutar test completo
python Test/test_refresh_token.py
```

El test validará:
- ✅ Login retorna ambos tokens
- ✅ Access token funciona en endpoints protegidos
- ✅ Refresh token obtiene nuevo access token
- ✅ Refresh token NO funciona en endpoints normales
- ✅ Logout revoca tokens

---

## 📊 Comparación: Antes vs Ahora

| Aspecto | Antes (Single Token) | Ahora (Dual Token) |
|---------|---------------------|-------------------|
| **Seguridad** | ⚠️ Token largo = riesgo | ✅ Token corto = seguro |
| **Experiencia** | ❌ Login frecuente | ✅ Sin logins frecuentes |
| **Revocación** | ⚠️ Difícil revocar | ✅ Fácil revocar |
| **Flexibilidad** | ❌ Un solo timeout | ✅ Dos timeouts |
| **Estándar** | ⚠️ Básico | ✅ Industria estándar |

---

## 🚀 Endpoints Actualizados

Todos los endpoints protegidos ahora usan **solo access token**:

```
✅ /api/pokemon (GET, POST) - Usa access_token
✅ /api/pokemon/:id (GET, PUT, DELETE) - Usa access_token
✅ /api/pokemon/:id/asignar (POST) - Usa access_token
✅ /auth/register (POST) - Usa access_token
✅ /auth/me (GET) - Usa access_token
✅ /auth/logout (POST) - Usa access_token

🔄 /auth/refresh (POST) - Usa refresh_token (SOLO este)
🔓 /auth/login (POST) - Sin token
```

---

## ⚠️ Importante

**Después de implementar estos cambios:**

1. **Reiniciar el servidor**
```powershell
python app.py
```

2. **Actualizar clientes**
   - Modificar lógica para guardar ambos tokens
   - Implementar refresh automático
   - Manejar expiración correctamente

3. **Probar sistema completo**
```powershell
python Test/test_refresh_token.py
```

---

**✅ Sistema de tokens implementado y funcionando**
