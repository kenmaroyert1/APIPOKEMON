# 📚 Guía Completa de Endpoints - API Pokémon

## 🎯 Información General

- **URL Base**: `http://localhost:5000`
- **Autenticación**: JWT Bearer Token
- **Content-Type**: `application/json`

---

## 📋 Tabla de Contenidos

1. [Autenticación](#autenticación)
   - [Registro de Usuario](#1-registro-de-usuario)
   - [Login](#2-login)
   - [Obtener Usuario Actual](#3-obtener-usuario-actual)
   - [Logout](#4-logout)

2. [Pokémon](#pokémon)
   - [Crear Pokémon](#1-crear-pokémon-solo-profesor)
   - [Listar Todos los Pokémons](#2-listar-todos-los-pokémons)
   - [Obtener Pokémon por ID](#3-obtener-pokémon-por-id)
   - [Actualizar Pokémon](#4-actualizar-pokémon-solo-profesor)
   - [Eliminar/Liberar Pokémon](#5-eliminarliberar-pokémon)
   - [Asignar Pokémon a Trainer](#6-asignar-pokémon-a-trainer-solo-profesor)

---

## 🔐 Autenticación

### 1. Registro de Usuario (Solo Profesor)

Crear una nueva cuenta de usuario. **Solo el profesor puede registrar nuevos usuarios**.

**Endpoint**: `POST /auth/register`

**Permisos**: 🎓 Solo Profesor

**Headers**:
```
Content-Type: application/json
Authorization: Bearer {token_profesor}
```

**Body**:
```json
{
  "email": "nuevo@usuario.com",
  "password": "contraseña123",
  "nombre": "Nombre del Usuario",
  "rol": "trainer"
}
```

**Campos**:
- `email` (requerido): Email único del usuario
- `password` (requerido): Contraseña (mínimo 6 caracteres)
- `nombre` (requerido): Nombre completo del usuario
- `rol` (requerido): `"profesor"` o `"trainer"`

**Respuesta Exitosa** (201):
```json
{
  "message": "Usuario registrado exitosamente por el profesor Profesor Oak",
  "profesor": "Profesor Oak",
  "usuario_creado": {
    "id": 4,
    "email": "nuevo@usuario.com",
    "nombre": "Nombre del Usuario",
    "rol": "trainer",
    "activo": true,
    "fecha_registro": "2025-10-14T16:30:00"
  }
}
```

**Errores Comunes**:
```json
// Sin autenticación de profesor (401/403)
{
  "error": "Acceso denegado",
  "mensaje": "Solo los profesores tienen acceso a esta funcionalidad"
}

// Email ya existe (409)
{
  "error": "Este email ya está registrado"
}

// Email inválido (400)
{
  "error": "Email inválido"
}

// Contraseña muy corta (400)
{
  "error": "La contraseña debe tener al menos 6 caracteres"
}
```

**Ejemplo cURL**:
```bash
curl -X POST http://localhost:5000/auth/register \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer {token_profesor}" \
  -d '{
    "email": "nuevo@usuario.com",
    "password": "contraseña123",
    "nombre": "Nombre del Usuario",
    "rol": "trainer"
  }'
```

**Ejemplo PowerShell**:
```powershell
$headers = @{
    "Authorization" = "Bearer $token"
    "Content-Type" = "application/json"
}

$body = @{
    email = "nuevo@usuario.com"
    password = "contraseña123"
    nombre = "Nombre del Usuario"
    rol = "trainer"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5000/auth/register" `
  -Method Post `
  -Headers $headers `
  -Body $body
```

---

### 2. Login

Iniciar sesión y obtener token JWT.

**Endpoint**: `POST /auth/login`

**Headers**:
```
Content-Type: application/json
```

**Body**:
```json
{
  "email": "profesor@universidad.edu",
  "password": "profesor123"
}
```

**Respuesta Exitosa** (200):
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

**Tokens retornados**:
- `access_token`: Usar en todos los endpoints protegidos (expira en 30 minutos)
- `refresh_token`: Usar solo en `/auth/refresh` para obtener nuevo access token (expira en 7 días)
- `expires_in`: Tiempo en segundos hasta que expire el access_token (1800 = 30 minutos)
```

**Errores Comunes**:
```json
// Credenciales incorrectas (401)
{
  "error": "Credenciales inválidas"
}

// Usuario inactivo (403)
{
  "error": "Usuario inactivo"
}
```

**Usuarios de Prueba**:
```
PROFESOR:
  Email: profesor@universidad.edu
  Password: profesor123

TRAINER 1:
  Email: ash@pokemon.com
  Password: ash123

TRAINER 2:
  Email: misty@pokemon.com
  Password: misty123
```

**Ejemplo cURL**:
```bash
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "profesor@universidad.edu",
    "password": "profesor123"
  }'
```

**Ejemplo PowerShell**:
```powershell
$body = @{
    email = "profesor@universidad.edu"
    password = "profesor123"
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "http://localhost:5000/auth/login" `
  -Method Post `
  -Body $body `
  -ContentType "application/json"

# Guardar el token para usarlo después
$token = $response.access_token
```

---

### 3. Refrescar Token

Obtener un nuevo access token usando el refresh token.

**Endpoint**: `POST /auth/refresh`

**Headers**:
```
Authorization: Bearer {refresh_token}
```

**Respuesta Exitosa** (200):
```json
{
  "message": "Token refrescado exitosamente",
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "Bearer",
  "expires_in": 1800
}
```

**Errores Comunes**:
```json
// Token expirado (401)
{
  "msg": "Token has expired"
}

// Token inválido (422)
{
  "msg": "Only refresh tokens are allowed"
}
```

**Ejemplo cURL**:
```bash
curl -X POST http://localhost:5000/auth/refresh \
  -H "Authorization: Bearer {refresh_token}"
```

**Ejemplo PowerShell**:
```powershell
$refreshHeaders = @{
    "Authorization" = "Bearer $refreshToken"
}

$response = Invoke-RestMethod -Uri "http://localhost:5000/auth/refresh" `
  -Method Post `
  -Headers $refreshHeaders

# Actualizar access token
$accessToken = $response.access_token
```

**Cuándo usar**:
- Cuando tu access token expira (cada 30 minutos)
- Para evitar que el usuario tenga que hacer login nuevamente
- El refresh token es válido por 7 días

---

### 4. Obtener Usuario Actual

Obtener información del usuario autenticado.

**Endpoint**: `GET /auth/me`

**Headers**:
```
Authorization: Bearer {tu_token_jwt}
```

**Respuesta Exitosa** (200):
```json
{
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

**Ejemplo cURL**:
```bash
curl -X GET http://localhost:5000/auth/me \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

**Ejemplo PowerShell**:
```powershell
$headers = @{
    "Authorization" = "Bearer $token"
}

Invoke-RestMethod -Uri "http://localhost:5000/auth/me" `
  -Method Get `
  -Headers $headers
```

---

### 5. Logout

Cerrar sesión y revocar token.

**Endpoint**: `POST /auth/logout`

**Headers**:
```
Authorization: Bearer {access_token o refresh_token}
```

**Respuesta Exitosa** (200):
```json
{
  "message": "Logout exitoso",
  "token_revocado": "access",
  "email": "profesor@universidad.edu",
  "info": "Token revocado. Elimina ambos tokens (access y refresh) del cliente."
}
```

**Recomendación**:
Después del logout, el cliente debe:
1. Eliminar el access_token
2. Eliminar el refresh_token
3. Redirigir al login si es necesario

**Ejemplo cURL**:
```bash
curl -X POST http://localhost:5000/auth/logout \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

**Ejemplo PowerShell**:
```powershell
$headers = @{
    "Authorization" = "Bearer $accessToken"
}

Invoke-RestMethod -Uri "http://localhost:5000/auth/logout" `
  -Method Post `
  -Headers $headers

# Limpiar tokens
$accessToken = $null
$refreshToken = $null
```

---

## 🎮 Pokémon

### 1. Crear Pokémon (Solo Profesor)

Crear un nuevo Pokémon en la base de datos.

**Endpoint**: `POST /api/pokemon`

**Permisos**: 🎓 Solo Profesor

**Headers**:
```
Content-Type: application/json
Authorization: Bearer {token_profesor}
```

**Body**:
```json
{
  "nombre": "Charizard",
  "tipo": "Fuego",
  "nivel": 36,
  "poder_ataque": 84.5,
  "poder_defensa": 78.0,
  "hp": 266,
  "descripcion": "Pokémon tipo fuego y volador, evolución final de Charmander"
}
```

**Campos**:
- `nombre` (requerido): Nombre del Pokémon
- `tipo` (requerido): Tipo del Pokémon (Fuego, Agua, Planta, etc.)
- `nivel` (requerido): Nivel del Pokémon (1-100)
- `poder_ataque` (requerido): Poder de ataque
- `poder_defensa` (requerido): Poder de defensa
- `hp` (requerido): Puntos de salud
- `descripcion` (opcional): Descripción del Pokémon

**Respuesta Exitosa** (201):
```json
{
  "message": "Pokémon creado exitosamente por el profesor Profesor Oak",
  "pokemon": {
    "id": 1,
    "nombre": "Charizard",
    "tipo": "Fuego",
    "nivel": 36,
    "poder_ataque": 84.5,
    "poder_defensa": 78.0,
    "hp": 266,
    "descripcion": "Pokémon tipo fuego y volador, evolución final de Charmander"
  }
}
```

**Errores**:
```json
// Trainer intenta crear (403)
{
  "error": "Acceso denegado",
  "mensaje": "Solo los profesores tienen acceso a esta funcionalidad"
}

// Sin token (401)
{
  "msg": "Missing Authorization Header"
}
```

**Ejemplo cURL**:
```bash
curl -X POST http://localhost:5000/api/pokemon \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer {token_profesor}" \
  -d '{
    "nombre": "Charizard",
    "tipo": "Fuego",
    "nivel": 36,
    "poder_ataque": 84.5,
    "poder_defensa": 78.0,
    "hp": 266,
    "descripcion": "Pokémon tipo fuego y volador"
  }'
```

**Ejemplo PowerShell**:
```powershell
$headers = @{
    "Authorization" = "Bearer $token"
    "Content-Type" = "application/json"
}

$body = @{
    nombre = "Charizard"
    tipo = "Fuego"
    nivel = 36
    poder_ataque = 84.5
    poder_defensa = 78.0
    hp = 266
    descripcion = "Pokémon tipo fuego y volador"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5000/api/pokemon" `
  -Method Post `
  -Headers $headers `
  -Body $body
```

---

### 2. Listar Todos los Pokémons

Obtener lista de Pokémons según el rol del usuario.

**Endpoint**: `GET /api/pokemon`

**Permisos**: 🎓 Profesor (ve todos) | 👤 Trainer (ve solo los suyos)

**Headers**:
```
Authorization: Bearer {tu_token}
```

**Respuesta para Profesor** (200):
```json
{
  "rol": "profesor",
  "total": 3,
  "pokemons": [
    {
      "id": 1,
      "nombre": "Charizard",
      "tipo": "Fuego",
      "nivel": 36,
      "poder_ataque": 84.5,
      "poder_defensa": 78.0,
      "hp": 266,
      "descripcion": "Pokémon tipo fuego y volador"
    },
    {
      "id": 2,
      "nombre": "Blastoise",
      "tipo": "Agua",
      "nivel": 36,
      "poder_ataque": 83.0,
      "poder_defensa": 100.0,
      "hp": 268,
      "descripcion": "Pokémon tipo agua"
    }
  ]
}
```

**Respuesta para Trainer** (200):
```json
{
  "rol": "trainer",
  "entrenador": "Ash Ketchum",
  "total_capturados": 2,
  "pokemons_capturados": [
    {
      "id": 1,
      "pokemon": {
        "id": 1,
        "nombre": "Charizard",
        "tipo": "Fuego",
        "nivel": 36,
        "poder_ataque": 84.5,
        "poder_defensa": 78.0,
        "hp": 266,
        "descripcion": "Pokémon tipo fuego y volador"
      },
      "apodo": "Mi Charizard",
      "fecha_captura": "2025-10-14T16:30:00"
    }
  ]
}
```

**Ejemplo cURL**:
```bash
# Como Profesor
curl -X GET http://localhost:5000/api/pokemon \
  -H "Authorization: Bearer {token_profesor}"

# Como Trainer
curl -X GET http://localhost:5000/api/pokemon \
  -H "Authorization: Bearer {token_trainer}"
```

**Ejemplo PowerShell**:
```powershell
$headers = @{
    "Authorization" = "Bearer $token"
}

Invoke-RestMethod -Uri "http://localhost:5000/api/pokemon" `
  -Method Get `
  -Headers $headers
```

---

### 3. Obtener Pokémon por ID

Obtener información de un Pokémon específico.

**Endpoint**: `GET /api/pokemon/{id}`

**Permisos**: 
- 🎓 Profesor: Puede ver cualquier Pokémon
- 👤 Trainer: Solo puede ver Pokémons asignados a él

**Headers**:
```
Authorization: Bearer {tu_token}
```

**Respuesta para Profesor** (200):
```json
{
  "rol": "profesor",
  "pokemon": {
    "id": 1,
    "nombre": "Charizard",
    "tipo": "Fuego",
    "nivel": 36,
    "poder_ataque": 84.5,
    "poder_defensa": 78.0,
    "hp": 266,
    "descripcion": "Pokémon tipo fuego y volador"
  }
}
```

**Respuesta para Trainer (Pokémon asignado)** (200):
```json
{
  "rol": "trainer",
  "pokemon": {
    "id": 1,
    "pokemon": {
      "id": 1,
      "nombre": "Charizard",
      "tipo": "Fuego",
      "nivel": 36,
      "poder_ataque": 84.5,
      "poder_defensa": 78.0,
      "hp": 266,
      "descripcion": "Pokémon tipo fuego y volador"
    },
    "apodo": "Mi Charizard",
    "fecha_captura": "2025-10-14T16:30:00"
  }
}
```

**Errores**:
```json
// Pokémon no existe (404)
{
  "error": "Pokémon no encontrado"
}

// Trainer intenta ver Pokémon no asignado (404)
{
  "error": "No has atrapado este Pokémon",
  "mensaje": "Este Pokémon no está en tu colección"
}
```

**Ejemplo cURL**:
```bash
curl -X GET http://localhost:5000/api/pokemon/1 \
  -H "Authorization: Bearer {tu_token}"
```

**Ejemplo PowerShell**:
```powershell
$headers = @{
    "Authorization" = "Bearer $token"
}

Invoke-RestMethod -Uri "http://localhost:5000/api/pokemon/1" `
  -Method Get `
  -Headers $headers
```

---

### 4. Actualizar Pokémon (Solo Profesor)

Actualizar información de un Pokémon existente.

**Endpoint**: `PUT /api/pokemon/{id}`

**Permisos**: 🎓 Solo Profesor

**Headers**:
```
Content-Type: application/json
Authorization: Bearer {token_profesor}
```

**Body** (todos los campos opcionales):
```json
{
  "nombre": "Charizard Mega X",
  "tipo": "Fuego/Dragón",
  "nivel": 50,
  "poder_ataque": 130.0,
  "poder_defensa": 111.0,
  "hp": 300,
  "descripcion": "Mega evolución de Charizard"
}
```

**Respuesta Exitosa** (200):
```json
{
  "message": "Pokémon actualizado por el profesor Profesor Oak",
  "pokemon": {
    "id": 1,
    "nombre": "Charizard Mega X",
    "tipo": "Fuego/Dragón",
    "nivel": 50,
    "poder_ataque": 130.0,
    "poder_defensa": 111.0,
    "hp": 300,
    "descripcion": "Mega evolución de Charizard"
  }
}
```

**Errores**:
```json
// Trainer intenta actualizar (403)
{
  "error": "Acceso denegado",
  "mensaje": "Solo los profesores tienen acceso a esta funcionalidad"
}

// Pokémon no existe (404)
{
  "error": "Pokémon no encontrado"
}
```

**Ejemplo cURL**:
```bash
curl -X PUT http://localhost:5000/api/pokemon/1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer {token_profesor}" \
  -d '{
    "nivel": 50,
    "poder_ataque": 130.0,
    "hp": 300
  }'
```

**Ejemplo PowerShell**:
```powershell
$headers = @{
    "Authorization" = "Bearer $token"
    "Content-Type" = "application/json"
}

$body = @{
    nivel = 50
    poder_ataque = 130.0
    hp = 300
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5000/api/pokemon/1" `
  -Method Put `
  -Headers $headers `
  -Body $body
```

---

### 5. Eliminar/Liberar Pokémon

Eliminar o liberar un Pokémon según el rol.

**Endpoint**: `DELETE /api/pokemon/{id}`

**Permisos**: 
- 🎓 Profesor: Elimina el Pokémon de la base de datos (permanente)
- 👤 Trainer: Libera el Pokémon de su colección (no lo elimina de la BD)

**Headers**:
```
Authorization: Bearer {tu_token}
```

**Respuesta Profesor** (200):
```json
{
  "message": "Pokémon eliminado de la base de datos por el profesor Profesor Oak"
}
```

**Respuesta Trainer** (200):
```json
{
  "message": "Ash Ketchum ha liberado el Pokémon de su colección",
  "pokemon_liberado": "Charizard"
}
```

**Errores**:
```json
// Pokémon no existe (404)
{
  "error": "Pokémon no encontrado"
}

// Trainer intenta liberar Pokémon no asignado (403)
{
  "error": "No puedes liberar este Pokémon",
  "mensaje": "Este Pokémon no está en tu colección"
}
```

**Ejemplo cURL**:
```bash
# Profesor elimina
curl -X DELETE http://localhost:5000/api/pokemon/1 \
  -H "Authorization: Bearer {token_profesor}"

# Trainer libera
curl -X DELETE http://localhost:5000/api/pokemon/1 \
  -H "Authorization: Bearer {token_trainer}"
```

**Ejemplo PowerShell**:
```powershell
$headers = @{
    "Authorization" = "Bearer $token"
}

Invoke-RestMethod -Uri "http://localhost:5000/api/pokemon/1" `
  -Method Delete `
  -Headers $headers
```

---

### 6. Asignar Pokémon a Trainer (Solo Profesor)

El profesor asigna un Pokémon a un entrenador.

**Endpoint**: `POST /api/pokemon/{id}/asignar`

**Permisos**: 🎓 Solo Profesor

**Headers**:
```
Content-Type: application/json
Authorization: Bearer {token_profesor}
```

**Body**:
```json
{
  "trainer_email": "ash@pokemon.com",
  "apodo": "Mi primer Pokémon"
}
```

**Campos**:
- `trainer_email` (requerido): Email del entrenador
- `apodo` (opcional): Apodo personalizado para el Pokémon

**Respuesta Exitosa** (201):
```json
{
  "message": "Pokémon asignado exitosamente",
  "profesor": "Profesor Oak",
  "entrenador": "Ash Ketchum",
  "pokemon": "Charizard",
  "apodo": "Mi primer Pokémon"
}
```

**Errores**:
```json
// Pokémon no existe (404)
{
  "error": "Pokémon no encontrado"
}

// Entrenador no existe (404)
{
  "error": "Entrenador no encontrado"
}

// Entrenador ya tiene el Pokémon (409)
{
  "error": "El entrenador ya tiene este Pokémon"
}

// Trainer intenta asignar (403)
{
  "error": "Acceso denegado",
  "mensaje": "Solo los profesores tienen acceso a esta funcionalidad"
}
```

**Ejemplo cURL**:
```bash
curl -X POST http://localhost:5000/api/pokemon/1/asignar \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer {token_profesor}" \
  -d '{
    "trainer_email": "ash@pokemon.com",
    "apodo": "Mi primer Pokémon"
  }'
```

**Ejemplo PowerShell**:
```powershell
$headers = @{
    "Authorization" = "Bearer $token"
    "Content-Type" = "application/json"
}

$body = @{
    trainer_email = "ash@pokemon.com"
    apodo = "Mi primer Pokémon"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5000/api/pokemon/1/asignar" `
  -Method Post `
  -Headers $headers `
  -Body $body
```

---

## 🔄 Flujo de Trabajo Completo

### Escenario 1: Profesor registra un trainer, crea y asigna Pokémon

```bash
# 1. Login como profesor
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "profesor@universidad.edu", "password": "profesor123"}'

# Guardar el token de la respuesta

# 2. Registrar un nuevo trainer
curl -X POST http://localhost:5000/auth/register \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer {token}" \
  -d '{
    "email": "nuevo.trainer@pokemon.com",
    "password": "pass123",
    "nombre": "Gary Oak",
    "rol": "trainer"
  }'

# 3. Crear un Pokémon
curl -X POST http://localhost:5000/api/pokemon \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer {token}" \
  -d '{
    "nombre": "Pikachu",
    "tipo": "Eléctrico",
    "nivel": 5,
    "poder_ataque": 55.0,
    "poder_defensa": 40.0,
    "hp": 35,
    "descripcion": "Pokémon eléctrico"
  }'

# 4. Asignar a un trainer
curl -X POST http://localhost:5000/api/pokemon/1/asignar \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer {token}" \
  -d '{
    "trainer_email": "ash@pokemon.com",
    "apodo": "Pika"
  }'
```

### Escenario 2: Profesor crea cuenta para otro profesor

```bash
# 1. Login como profesor
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "profesor@universidad.edu", "password": "profesor123"}'

# 2. Registrar un nuevo profesor
curl -X POST http://localhost:5000/auth/register \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer {token}" \
  -d '{
    "email": "profesor2@universidad.edu",
    "password": "prof456",
    "nombre": "Profesor Elm",
    "rol": "profesor"
  }'
```

### Escenario 3: Trainer ve y libera sus Pokémons

```bash
# 1. Login como trainer
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "ash@pokemon.com", "password": "ash123"}'

# 2. Ver mis Pokémons
curl -X GET http://localhost:5000/api/pokemon \
  -H "Authorization: Bearer {token}"

# 3. Ver un Pokémon específico
curl -X GET http://localhost:5000/api/pokemon/1 \
  -H "Authorization: Bearer {token}"

# 4. Liberar un Pokémon
curl -X DELETE http://localhost:5000/api/pokemon/1 \
  -H "Authorization: Bearer {token}"
```

---

## 📝 Notas Importantes

### Expiración de Tokens
- **Access Token**: Expira en 30 minutos
- **Refresh Token**: Expira en 7 días

### Headers Requeridos
Todos los endpoints protegidos requieren:
```
Authorization: Bearer {tu_token_jwt}
```

### Formato de Respuestas
Todas las respuestas son en formato JSON:
```json
{
  "key": "value"
}
```

### Códigos de Estado HTTP

| Código | Significado |
|--------|-------------|
| 200 | OK - Operación exitosa |
| 201 | Created - Recurso creado |
| 400 | Bad Request - Datos inválidos |
| 401 | Unauthorized - Token inválido o faltante |
| 403 | Forbidden - Sin permisos |
| 404 | Not Found - Recurso no encontrado |
| 409 | Conflict - Conflicto (ej: email duplicado) |
| 500 | Internal Server Error - Error del servidor |

---

## 🛠️ Testing con Postman

### Importar Colección

1. Abre Postman
2. Click en "Import"
3. Pega esta colección base:

```json
{
  "info": {
    "name": "API Pokémon",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "variable": [
    {
      "key": "base_url",
      "value": "http://localhost:5000"
    },
    {
      "key": "token",
      "value": ""
    }
  ]
}
```

### Configurar Variables de Entorno

1. Crear un environment "Pokemon API"
2. Agregar variables:
   - `base_url`: `http://localhost:5000`
   - `token`: (se actualizará automáticamente al hacer login)

### Script Post-Request para Login

En el endpoint de login, agrega este script en "Tests":
```javascript
if (pm.response.code === 200) {
    var jsonData = pm.response.json();
    pm.environment.set("token", jsonData.access_token);
}
```

---

## 🐛 Troubleshooting

### Error: "Missing Authorization Header"
**Solución**: Asegúrate de incluir el header:
```
Authorization: Bearer {tu_token}
```

### Error: "Token has expired"
**Solución**: Vuelve a hacer login para obtener un nuevo token.

### Error: "Acceso denegado"
**Solución**: Verifica que tu rol de usuario tenga permisos para ese endpoint.

### Error: "Usuario no encontrado"
**Solución**: Ejecuta `python init_users.py` para crear los usuarios de prueba.

---

## 📞 Soporte

Para más información, consulta:
- `GUIA_SISTEMA_ROLES.md` - Detalles del sistema de roles
- `INICIO_RAPIDO.md` - Guía de inicio rápido
- `README.md` - Información general del proyecto

---

**¡Happy Coding! 🚀**
