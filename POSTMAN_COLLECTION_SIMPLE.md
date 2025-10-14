# 📮 Colección Postman - API Pokémon

## 🎯 Configuración Inicial

### Variables de Entorno
```
base_url = http://localhost:5000
access_token = (se actualiza automáticamente)
refresh_token = (se actualiza automáticamente)
```

### Script Global para Login (Tests tab)
```javascript
if (pm.response.code === 200) {
    var jsonData = pm.response.json();
    pm.environment.set("access_token", jsonData.access_token);
    pm.environment.set("refresh_token", jsonData.refresh_token);
}
```

---

## 📁 AUTH

### 1. Login Profesor
```
POST {{base_url}}/auth/login
Content-Type: application/json
```
**Body**:
```json
{
  "email": "profesor@universidad.edu",
  "password": "profesor123"
}
```

---

### 2. Login Trainer
```
POST {{base_url}}/auth/login
Content-Type: application/json
```
**Body**:
```json
{
  "email": "ash@pokemon.com",
  "password": "ash123"
}
```

---

### 3. Refresh Token
```
POST {{base_url}}/auth/refresh
Authorization: Bearer {{refresh_token}}
```

---

### 4. Get Me
```
GET {{base_url}}/auth/me
Authorization: Bearer {{access_token}}
```

---

### 5. Logout
```
POST {{base_url}}/auth/logout
Authorization: Bearer {{access_token}}
```

---

## 📁 PROFESOR

### 1. Registrar Usuario
```
POST {{base_url}}/auth/register
Authorization: Bearer {{access_token}}
Content-Type: application/json
```
**Body**:
```json
{
  "email": "nuevo@usuario.com",
  "password": "pass123",
  "nombre": "Nuevo Usuario",
  "rol": "trainer"
}
```

---

### 2. Crear Pokémon
```
POST {{base_url}}/api/pokemon
Authorization: Bearer {{access_token}}
Content-Type: application/json
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
  "descripcion": "Pokémon tipo fuego"
}
```

---

### 3. Ver Todos los Pokémon
```
GET {{base_url}}/api/pokemon
Authorization: Bearer {{access_token}}
```

---

### 4. Ver Pokémon por ID
```
GET {{base_url}}/api/pokemon/1
Authorization: Bearer {{access_token}}
```

---

### 5. Actualizar Pokémon
```
PUT {{base_url}}/api/pokemon/1
Authorization: Bearer {{access_token}}
Content-Type: application/json
```
**Body**:
```json
{
  "nivel": 50,
  "poder_ataque": 130.0,
  "hp": 300
}
```

---

### 6. Eliminar Pokémon
```
DELETE {{base_url}}/api/pokemon/1
Authorization: Bearer {{access_token}}
```

---

### 7. Asignar Pokémon a Trainer
```
POST {{base_url}}/api/pokemon/1/asignar
Authorization: Bearer {{access_token}}
Content-Type: application/json
```
**Body**:
```json
{
  "trainer_email": "ash@pokemon.com",
  "apodo": "Mi Pokémon"
}
```

---

## 📁 TRAINER

### 1. Ver Mis Pokémon
```
GET {{base_url}}/api/pokemon
Authorization: Bearer {{access_token}}
```
**Nota**: Solo verá sus pokémon asignados

---

### 2. Ver Mi Pokémon por ID
```
GET {{base_url}}/api/pokemon/1
Authorization: Bearer {{access_token}}
```
**Nota**: Solo si le fue asignado

---

### 3. Liberar Pokémon
```
DELETE {{base_url}}/api/pokemon/1
Authorization: Bearer {{access_token}}
```
**Nota**: Lo libera de su colección, no lo elimina de la BD

---

## 🚀 Flujo de Prueba Rápido

### 1️⃣ Como Profesor
```
1. Login Profesor
2. Crear Pokémon
3. Registrar Nuevo Trainer
4. Asignar Pokémon a Trainer
5. Ver Todos los Pokémon
```

### 2️⃣ Como Trainer
```
1. Login Trainer
2. Ver Mis Pokémon
3. Ver Mi Pokémon por ID
4. Liberar Pokémon
```

---

## 📋 Usuarios de Prueba

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

---

## ⚡ Respuestas Rápidas

### Login Exitoso (200)
```json
{
  "access_token": "...",
  "refresh_token": "...",
  "expires_in": 1800,
  "usuario": {...}
}
```

### Error 401 - Token Inválido
```json
{
  "msg": "Missing Authorization Header"
}
```

### Error 403 - Sin Permisos
```json
{
  "error": "Acceso denegado",
  "mensaje": "Solo los profesores tienen acceso..."
}
```

### Error 404 - No Encontrado
```json
{
  "error": "Pokémon no encontrado"
}
```

---

## 🎨 Estructura de Carpetas en Postman

```
📦 API Pokémon
 ┣ 📁 AUTH
 ┃ ┣ Login Profesor
 ┃ ┣ Login Trainer
 ┃ ┣ Refresh Token
 ┃ ┣ Get Me
 ┃ ┗ Logout
 ┣ 📁 PROFESOR
 ┃ ┣ Registrar Usuario
 ┃ ┣ Crear Pokémon
 ┃ ┣ Ver Todos los Pokémon
 ┃ ┣ Ver Pokémon por ID
 ┃ ┣ Actualizar Pokémon
 ┃ ┣ Eliminar Pokémon
 ┃ ┗ Asignar Pokémon a Trainer
 ┗ 📁 TRAINER
   ┣ Ver Mis Pokémon
   ┣ Ver Mi Pokémon por ID
   ┗ Liberar Pokémon
```

---

## 💡 Tips Postman

### Auto-guardar Tokens
En el tab "Tests" del endpoint Login:
```javascript
if (pm.response.code === 200) {
    var data = pm.response.json();
    pm.environment.set("access_token", data.access_token);
    pm.environment.set("refresh_token", data.refresh_token);
}
```

### Auto-refresh Token
En el tab "Pre-request Script" (opcional):
```javascript
// Verificar si el token está por expirar y refrescarlo
const tokenExpiry = pm.environment.get("token_expiry");
if (Date.now() > tokenExpiry - 300000) { // 5 min antes
    pm.sendRequest({
        url: pm.environment.get("base_url") + "/auth/refresh",
        method: "POST",
        header: {
            "Authorization": "Bearer " + pm.environment.get("refresh_token")
        }
    }, (err, res) => {
        if (!err && res.code === 200) {
            const data = res.json();
            pm.environment.set("access_token", data.access_token);
            pm.environment.set("token_expiry", Date.now() + 1800000);
        }
    });
}
```

---

**✅ Listo para importar a Postman!**
