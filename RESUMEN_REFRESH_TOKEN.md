# 🎉 SISTEMA DE ACCESS + REFRESH TOKEN IMPLEMENTADO

## ✅ RESUMEN DE CAMBIOS

Se ha actualizado el sistema de autenticación para incluir **Access Tokens** y **Refresh Tokens**, mejorando significativamente la seguridad y experiencia de usuario.

---

## 📋 ¿Qué Cambió?

### ANTES (Sistema Simple):
```json
POST /auth/login
→ Retorna: {
    "access_token": "..."
}
```
- ❌ Un solo token
- ❌ Si expira, usuario debe hacer login nuevamente
- ❌ Tokens de larga duración = mayor riesgo

### AHORA (Sistema Dual Token):
```json
POST /auth/login
→ Retorna: {
    "access_token": "...",      // 30 minutos
    "refresh_token": "...",     // 7 días
    "expires_in": 1800
}
```
- ✅ Dos tokens con diferentes propósitos
- ✅ Access token corto = mayor seguridad
- ✅ Refresh token largo = mejor UX
- ✅ Renovación automática sin re-login

---

## 🔐 Cómo Funciona

### 1️⃣ **Login Inicial**
```
Usuario → POST /auth/login {email, password}
         ↓
Servidor → Valida credenciales
         ↓
Cliente ← Recibe:
          • access_token (30 min)
          • refresh_token (7 días)
```

### 2️⃣ **Uso Normal** (0-30 minutos)
```
Cliente → GET /api/pokemon
          Authorization: Bearer {access_token}
         ↓
Servidor → Valida access_token
         ↓
Cliente ← Respuesta con datos
```

### 3️⃣ **Token Expirado** (después de 30 min)
```
Cliente → GET /api/pokemon
          Authorization: Bearer {access_token_expirado}
         ↓
Servidor → 401 Unauthorized
         ↓
Cliente → POST /auth/refresh
          Authorization: Bearer {refresh_token}
         ↓
Servidor → Valida refresh_token
         ↓
Cliente ← Nuevo access_token (30 min más)
         ↓
Cliente → Reintenta GET /api/pokemon
          Authorization: Bearer {nuevo_access_token}
         ↓
Servidor → OK ✅
```

### 4️⃣ **Logout**
```
Cliente → POST /auth/logout
          Authorization: Bearer {access_token}
         ↓
Servidor → Revoca token
         ↓
Cliente → Elimina ambos tokens
```

---

## 📂 Archivos Modificados

### 1. **Controllers/AuthController.py**
```python
# NUEVAS IMPORTACIONES
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,  # ← NUEVO
    get_jwt,               # ← NUEVO
    jwt_required
)

# NUEVO: Sistema de revocación
revoked_tokens = set()

# MODIFICADO: Login retorna ambos tokens
@auth_blueprint.route('/login', methods=['POST'])
def login():
    # ...
    access_token = create_access_token(identity=email, ...)
    refresh_token = create_refresh_token(identity=email, ...)  # ← NUEVO
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,  # ← NUEVO
        "expires_in": 1800               # ← NUEVO
    }

# NUEVO ENDPOINT: Refrescar token
@auth_blueprint.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    email = get_jwt_identity()
    new_access_token = create_access_token(identity=email, ...)
    return {"access_token": new_access_token}

# MODIFICADO: Logout revoca tokens
@auth_blueprint.route('/logout', methods=['POST'])
@jwt_required(verify_type=False)  # ← MODIFICADO: acepta ambos tipos
def logout():
    jti = get_jwt()["jti"]
    revoked_tokens.add(jti)  # ← NUEVO: revoca token
    return {"message": "Logout exitoso"}
```

### 2. **Config/jwt.py**
```python
# NUEVA CONFIGURACIÓN
JWT_REFRESH_TOKEN_EXPIRES = timedelta(
    days=int(os.getenv("JWT_REFRESH_TOKEN_EXPIRE_DAYS", 7))
)

def init_jwt(app):
    # ...
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = JWT_REFRESH_TOKEN_EXPIRES
    print(f"  - Access Token: {JWT_ACCESS_TOKEN_EXPIRES}")
    print(f"  - Refresh Token: {JWT_REFRESH_TOKEN_EXPIRES}")
```

### 3. **GUIA_ENDPOINTS.md**
- ✅ Actualizado endpoint `/auth/login` con ambos tokens
- ✅ Agregado nuevo endpoint `/auth/refresh`
- ✅ Actualizado endpoint `/auth/logout`
- ✅ Ejemplos PowerShell y cURL actualizados

### 4. **Test/test_refresh_token.py** (NUEVO)
- ✅ Script de prueba completo
- ✅ Valida login con ambos tokens
- ✅ Valida refresh endpoint
- ✅ Valida que refresh token no funcione en otros endpoints

### 5. **GUIA_REFRESH_TOKEN.md** (NUEVO)
- ✅ Documentación completa del sistema
- ✅ Diagramas de flujo
- ✅ Ejemplos de implementación
- ✅ Mejores prácticas

---

## 🆕 Nuevos Endpoints

### POST /auth/refresh

**Propósito**: Obtener un nuevo access token sin hacer login nuevamente

**Request**:
```http
POST /auth/refresh
Authorization: Bearer {refresh_token}
```

**Response** (200):
```json
{
  "message": "Token refrescado exitosamente",
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "Bearer",
  "expires_in": 1800
}
```

**Cuándo usar**:
- Automáticamente cuando access_token expira (401)
- Programáticamente 5 minutos antes de expiración
- Después de 30 minutos de la última renovación

---

## ⏱️ Tiempos de Expiración

| Token | Duración | Propósito |
|-------|----------|-----------|
| **Access Token** | 30 minutos | Acceso a endpoints protegidos |
| **Refresh Token** | 7 días | Renovar access tokens |

### Configuración (.env):
```env
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7
```

---

## 💻 Ejemplos de Uso

### PowerShell Completo

```powershell
# ============================================
# 1. LOGIN - Obtener ambos tokens
# ============================================
$loginBody = @{
    email = "profesor@universidad.edu"
    password = "profesor123"
} | ConvertTo-Json

$login = Invoke-RestMethod -Uri "http://localhost:5000/auth/login" `
  -Method Post `
  -Body $loginBody `
  -ContentType "application/json"

$accessToken = $login.access_token
$refreshToken = $login.refresh_token

Write-Host "✅ Login exitoso" -ForegroundColor Green
Write-Host "   Access Token: $($accessToken.Substring(0, 30))..."
Write-Host "   Refresh Token: $($refreshToken.Substring(0, 30))..."
Write-Host "   Expira en: $($login.expires_in) segundos`n"

# ============================================
# 2. USAR ACCESS TOKEN
# ============================================
$headers = @{
    "Authorization" = "Bearer $accessToken"
}

$pokemons = Invoke-RestMethod -Uri "http://localhost:5000/api/pokemon" `
  -Method Get `
  -Headers $headers

Write-Host "✅ Pokémons obtenidos con access token`n" -ForegroundColor Green

# ============================================
# 3. SIMULAR EXPIRACIÓN Y REFRESH
# ============================================
Write-Host "⏰ Simulando expiración de access token..." -ForegroundColor Yellow
Start-Sleep -Seconds 2

# Refrescar token
$refreshHeaders = @{
    "Authorization" = "Bearer $refreshToken"
}

$refresh = Invoke-RestMethod -Uri "http://localhost:5000/auth/refresh" `
  -Method Post `
  -Headers $refreshHeaders

$accessToken = $refresh.access_token

Write-Host "✅ Token refrescado exitosamente" -ForegroundColor Green
Write-Host "   Nuevo Access Token: $($accessToken.Substring(0, 30))...`n"

# ============================================
# 4. USAR NUEVO ACCESS TOKEN
# ============================================
$headers = @{
    "Authorization" = "Bearer $accessToken"
}

$usuario = Invoke-RestMethod -Uri "http://localhost:5000/auth/me" `
  -Method Get `
  -Headers $headers

Write-Host "✅ Usuario obtenido con nuevo token: $($usuario.usuario.nombre)`n" -ForegroundColor Green

# ============================================
# 5. LOGOUT
# ============================================
Invoke-RestMethod -Uri "http://localhost:5000/auth/logout" `
  -Method Post `
  -Headers $headers

$accessToken = $null
$refreshToken = $null

Write-Host "✅ Logout exitoso - Tokens eliminados`n" -ForegroundColor Green
```

---

## 🧪 Probar el Sistema

### 1. Reiniciar el Servidor

```powershell
# Detener servidor actual (Ctrl+C)
python app.py
```

### 2. Ejecutar Test Automático

```powershell
python Test/test_refresh_token.py
```

**El test validará**:
- ✅ Login retorna access_token y refresh_token
- ✅ Access token funciona en endpoints protegidos
- ✅ Refresh token obtiene nuevo access token
- ✅ Refresh token NO funciona en endpoints normales
- ✅ Logout revoca tokens correctamente

---

## 📊 Comparación: Antes vs Ahora

| Característica | Antes | Ahora |
|----------------|-------|-------|
| **Tokens por login** | 1 | 2 |
| **Duración token acceso** | Variable | 30 min fijo |
| **Renovación sin login** | ❌ No | ✅ Sí (7 días) |
| **Seguridad** | ⚠️ Media | ✅ Alta |
| **UX** | ⚠️ Login frecuente | ✅ Sin logins frecuentes |
| **Revocación** | ⚠️ Difícil | ✅ Implementada |
| **Estándar industria** | ❌ No | ✅ Sí (OAuth 2.0) |

---

## 🔒 Mejores Prácticas Implementadas

### ✅ Seguridad
- Access tokens de corta duración (30 min)
- Refresh tokens de larga duración (7 días)
- Tokens separados por propósito
- Sistema de revocación básico

### ✅ Experiencia de Usuario
- No requiere login frecuente
- Renovación transparente
- Sesiones más largas (hasta 7 días)

### ✅ Arquitectura
- Separación de responsabilidades
- Fácil de escalar
- Compatible con OAuth 2.0
- Preparado para implementar rotación de tokens

---

## 📚 Documentación

### Documentos Creados/Actualizados:

1. **GUIA_REFRESH_TOKEN.md** - Guía completa del sistema
2. **GUIA_ENDPOINTS.md** - Endpoints actualizados
3. **Test/test_refresh_token.py** - Tests automatizados
4. **Controllers/AuthController.py** - Lógica actualizada
5. **Config/jwt.py** - Configuración actualizada

---

## ⚠️ IMPORTANTE - Próximos Pasos

### 1. Reiniciar el Servidor
```powershell
python app.py
```

### 2. Actualizar Clientes
Los clientes (web/móvil) deben:
- Guardar **ambos tokens** en el login
- Usar **access_token** para requests normales
- Usar **refresh_token** solo para `/auth/refresh`
- Implementar renovación automática
- Eliminar ambos tokens en logout

### 3. Probar Cambios
```powershell
python Test/test_refresh_token.py
```

---

## 🚀 Estado del Sistema

✅ **COMPLETADO**:
- Sistema de access + refresh tokens
- Endpoint de refresh
- Logout con revocación
- Documentación completa
- Tests automatizados
- Configuración flexible

⏳ **RECOMENDADO PARA PRODUCCIÓN**:
- Usar Redis para tokens revocados
- Implementar rotación de refresh tokens
- Agregar rate limiting
- Monitoreo de sesiones activas
- Logs de seguridad

---

**✅ Sistema listo para usar - Reinicia el servidor y prueba!** 🎉
