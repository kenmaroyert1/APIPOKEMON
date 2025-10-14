# 📮 COLECCIÓN POSTMAN/THUNDER CLIENT - Sistema Pokémon

## 🔧 Configurar Variables de Entorno

Crea estas variables en Postman/Thunder Client:

```
base_url = http://127.0.0.1:5000
token_profesor = (se llenará después del login)
token_trainer = (se llenará después del login)
```

---

## 📁 COLECCIÓN DE ENDPOINTS

### 1️⃣ AUTENTICACIÓN

#### 1.1 Login Profesor
```
POST {{base_url}}/auth/login
Content-Type: application/json

{
    "email": "profesor@universidad.edu",
    "password": "profesor123"
}
```

**Acción después:** Guarda el `access_token` en la variable `token_profesor`

---

#### 1.2 Login Trainer
```
POST {{base_url}}/auth/login
Content-Type: application/json

{
    "email": "ash@pokemon.com",
    "password": "ash123"
}
```

**Acción después:** Guarda el `access_token` en la variable `token_trainer`

---

#### 1.3 Registrar Nuevo Usuario
```
POST {{base_url}}/auth/register
Content-Type: application/json

{
    "email": "brock@pokemon.com",
    "nombre": "Brock",
    "password": "brock123",
    "rol": "trainer"
}
```

---

#### 1.4 Info Usuario Actual
```
GET {{base_url}}/auth/me
Authorization: Bearer {{token_profesor}}
```

---

### 2️⃣ POKÉMONS - PROFESOR

#### 2.1 Crear Pokémon
```
POST {{base_url}}/api/pokemon
Authorization: Bearer {{token_profesor}}
Content-Type: application/json

{
    "nombre": "Charizard",
    "tipo": "Fuego/Volador",
    "nivel": 36,
    "poder_ataque": 84.0,
    "poder_defensa": 78.0,
    "hp": 78,
    "descripcion": "Un poderoso Pokémon dragón"
}
```

---

#### 2.2 Ver Todos los Pokémons (Profesor)
```
GET {{base_url}}/api/pokemon
Authorization: Bearer {{token_profesor}}
```

---

#### 2.3 Ver Pokémon Específico (Profesor)
```
GET {{base_url}}/api/pokemon/1
Authorization: Bearer {{token_profesor}}
```

---

#### 2.4 Actualizar Pokémon
```
PUT {{base_url}}/api/pokemon/1
Authorization: Bearer {{token_profesor}}
Content-Type: application/json

{
    "nivel": 40,
    "poder_ataque": 90.0,
    "descripcion": "Charizard más poderoso tras entrenamiento"
}
```

---

#### 2.5 Eliminar Pokémon (de la BD)
```
DELETE {{base_url}}/api/pokemon/1
Authorization: Bearer {{token_profesor}}
```

---

#### 2.6 Asignar Pokémon a Trainer
```
POST {{base_url}}/api/pokemon/1/asignar
Authorization: Bearer {{token_profesor}}
Content-Type: application/json

{
    "trainer_email": "ash@pokemon.com",
    "apodo": "Charizard Feroz"
}
```

---

### 3️⃣ POKÉMONS - TRAINER

#### 3.1 Ver Mis Pokémons (Trainer)
```
GET {{base_url}}/api/pokemon
Authorization: Bearer {{token_trainer}}
```

**Nota:** Solo muestra pokémons asignados al trainer

---

#### 3.2 Ver Pokémon Específico Propio
```
GET {{base_url}}/api/pokemon/1
Authorization: Bearer {{token_trainer}}
```

**Nota:** Solo funciona si el trainer tiene ese pokémon

---

#### 3.3 Ver Pokémon NO Propio (Debe Fallar)
```
GET {{base_url}}/api/pokemon/999
Authorization: Bearer {{token_trainer}}
```

**Respuesta esperada:** 403 - "No has capturado este Pokémon"

---

#### 3.4 Intentar Crear Pokémon (Debe Fallar)
```
POST {{base_url}}/api/pokemon
Authorization: Bearer {{token_trainer}}
Content-Type: application/json

{
    "nombre": "Pikachu Ilegal",
    "tipo": "Eléctrico",
    "nivel": 10,
    "poder_ataque": 50.0,
    "poder_defensa": 40.0,
    "hp": 30
}
```

**Respuesta esperada:** 403 - "Solo los profesores tienen acceso"

---

#### 3.5 Intentar Actualizar (Debe Fallar)
```
PUT {{base_url}}/api/pokemon/1
Authorization: Bearer {{token_trainer}}
Content-Type: application/json

{
    "nivel": 50
}
```

**Respuesta esperada:** 403 - "Solo los profesores tienen acceso"

---

#### 3.6 Liberar Pokémon (de su colección)
```
DELETE {{base_url}}/api/pokemon/1
Authorization: Bearer {{token_trainer}}
```

**Nota:** NO elimina de la BD, solo de la colección del trainer

---

### 4️⃣ OTROS

#### 4.1 Página de Bienvenida
```
GET {{base_url}}/
```

---

#### 4.2 Logout
```
POST {{base_url}}/auth/logout
Authorization: Bearer {{token_profesor}}
```

---

## 🎯 FLUJO COMPLETO DE PRUEBA

### Escenario 1: Profesor asigna pokémon a trainer

1. **Login Profesor** (1.1)
2. **Crear Pokémon** (2.1) → Guarda el ID del pokémon creado
3. **Login Trainer** (1.2)
4. **Trainer ve sus pokémons** (3.1) → Debe estar vacío
5. **Profesor asigna pokémon** (2.6) → Usa email del trainer
6. **Trainer ve sus pokémons** (3.1) → Ahora debe aparecer el pokémon

---

### Escenario 2: Verificar restricciones de Trainer

1. **Login Trainer** (1.2)
2. **Intentar crear pokémon** (3.4) → Debe fallar (403)
3. **Intentar actualizar** (3.5) → Debe fallar (403)
4. **Intentar ver pokémon no asignado** (3.3) → Debe fallar (403)
5. **Ver pokémon asignado** (3.2) → Debe funcionar (200)
6. **Liberar pokémon** (3.6) → Debe funcionar (200)

---

### Escenario 3: Permisos de Profesor

1. **Login Profesor** (1.1)
2. **Crear pokémon** (2.1) → ✅ Funciona
3. **Ver todos** (2.2) → ✅ Ve todos los pokémons
4. **Ver específico** (2.3) → ✅ Ve cualquiera
5. **Actualizar** (2.4) → ✅ Funciona
6. **Eliminar** (2.5) → ✅ Elimina de la BD

---

## 💾 GUARDAR RESPUESTAS

### Thunder Client
1. Crea una nueva Colección: "Sistema Pokémon con Roles"
2. Crea las carpetas: "Auth", "Profesor", "Trainer"
3. Guarda cada request en su carpeta correspondiente
4. Configura las variables de entorno

### Postman
1. Importa como colección
2. Configura el environment con:
   - `base_url`: http://127.0.0.1:5000
   - `token_profesor`: (vacío inicialmente)
   - `token_trainer`: (vacío inicialmente)
3. Usa "Tests" para auto-guardar tokens:

```javascript
// En Login Profesor
pm.environment.set("token_profesor", pm.response.json().access_token);

// En Login Trainer
pm.environment.set("token_trainer", pm.response.json().access_token);
```

---

## 🔥 TIPS

1. **Siempre haz login primero** para obtener el token
2. **Los tokens expiran en 1 hora** (configurable en .env)
3. **Guarda los IDs** de pokémons creados para pruebas posteriores
4. **Usa variables** para evitar copiar/pegar tokens manualmente
5. **Revisa los status codes:**
   - 200/201: ✅ Éxito
   - 403: 🚫 Sin permisos
   - 404: ❓ No encontrado
   - 401: 🔒 No autenticado

---

## 📖 REFERENCIA RÁPIDA

| Método | Endpoint | Profesor | Trainer |
|--------|----------|----------|---------|
| POST | /auth/login | ✅ | ✅ |
| POST | /auth/register | ✅ | ✅ |
| GET | /auth/me | ✅ | ✅ |
| GET | /api/pokemon | ✅ Todos | ✅ Solo suyos |
| GET | /api/pokemon/:id | ✅ Cualquiera | ✅ Solo suyos |
| POST | /api/pokemon | ✅ | ❌ |
| PUT | /api/pokemon/:id | ✅ | ❌ |
| DELETE | /api/pokemon/:id | ✅ Elimina BD | ✅ Libera colección |
| POST | /api/pokemon/:id/asignar | ✅ | ❌ |

---

¡Listo para probar! 🚀
