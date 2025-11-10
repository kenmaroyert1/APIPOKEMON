# Instrucciones para usar el Dashboard HTML

## ✅ Completado

He creado el archivo `static/dashboard.html` con las siguientes funcionalidades:

### 📋 Funcionalidades implementadas

#### Login (Inicio de sesión)
- Formulario de login con email y contraseña
- Botones de ejemplo para autocompletar credenciales de Profesor o Trainer
- Autenticación JWT con la API `/auth/login`
- Almacenamiento de tokens en localStorage

#### Panel Profesor
El profesor puede:
- ✅ Ver **todos** los pokémons en la base de datos
- ✅ Crear nuevos pokémons (formulario con validaciones)
- ✅ Editar pokémons existentes (carga datos en el formulario)
- ✅ Eliminar pokémons de la base de datos
- ✅ Ver detalles de un pokémon específico
- ✅ Asignar pokémons a trainers (prompt para email del trainer y apodo opcional)

#### Panel Trainer
El trainer puede:
- ✅ Ver **solo** los pokémons que le fueron asignados
- ✅ Liberar pokémons de su colección (eliminar captura)
- Ver fecha de captura y apodo de cada pokémon

---

## 🔑 Credenciales de acceso

### Usuarios ya creados en la BD (ejecutaste `python .\init_users.py`):

**PROFESOR:**
- Email: `profesor@universidad.edu`
- Password: `profesor123`
- Permisos: TODOS (crear, ver, actualizar, eliminar, asignar)

**TRAINER 1:**
- Email: `ash@pokemon.com`
- Password: `ash123`
- Permisos: Ver y liberar solo sus pokémons

**TRAINER 2:**
- Email: `misty@pokemon.com`
- Password: `misty123`
- Permisos: Ver y liberar solo sus pokémons

---

## 🚀 Cómo usar el Dashboard

### Opción 1: Arrancar el servidor Flask (recomendado)

1. **Asegúrate de que MySQL esté corriendo** y accesible con las credenciales del archivo `.env`

2. **Arranca el servidor Flask** (desde PowerShell en la carpeta del proyecto):
   ```powershell
   python .\app.py
   ```
   
   Deberías ver:
   ```
   ✓ JWT configurado correctamente
   ✓ Conexión a MySQL exitosa
   * Running on http://127.0.0.1:5000
   ```

3. **Abre el dashboard en tu navegador**:
   ```powershell
   Start-Process "http://127.0.0.1:5000/static/dashboard.html"
   ```
   
   O abre manualmente: http://127.0.0.1:5000/static/dashboard.html

4. **Inicia sesión**:
   - Haz clic en "Ejemplo Profesor" o "Ejemplo Trainer" para autocompletar
   - O escribe manualmente el email y password
   - Haz clic en "Entrar"

5. **Usa las funcionalidades según tu rol**:
   - **Profesor**: verás todos los pokémons y botones para crear, editar, eliminar y asignar
   - **Trainer**: verás solo tus pokémons capturados y botón para liberar

---

## 🔧 Solución a problemas comunes

### Problema 1: El servidor Flask falla al iniciar (error MySQL)

**Síntoma**: Ves errores de conexión MySQL o `KeyboardInterrupt` al arrancar `python .\app.py`

**Causas posibles**:
- MySQL no está corriendo
- Credenciales incorrectas en `.env`
- Puerto MySQL bloqueado o conexión SSL fallando

**Soluciones**:

#### A) Verifica MySQL
```powershell
# Verifica que MySQL esté corriendo (Windows)
Get-Service -Name MySQL* | Select-Object Status, DisplayName
```

#### B) Revisa el archivo `.env`
Abre `.env` y verifica las credenciales:
```
DB_HOST=localhost
DB_PORT=3306
DB_USER=tu_usuario
DB_PASSWORD=tu_password
DB_NAME=nombre_bd
```

#### C) Desactiva el auto-reload de Flask (solución rápida)
Edita `app.py` y cambia la última línea:
```python
if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)  # ← Añade use_reloader=False
```

Esto evita el restart automático que puede causar problemas de reconexión.

#### D) Usa SQLite en lugar de MySQL (para desarrollo rápido)
Si quieres probar el dashboard sin configurar MySQL:

1. Edita `Config/DataBase.py` y cambia la función `get_database_url()`:
   ```python
   def get_database_url():
       """Devuelve la URL de conexión a la base de datos."""
       # Temporalmente usa SQLite
       return "sqlite:///pokemon.db"
   ```

2. Ejecuta de nuevo:
   ```powershell
   python .\init_users.py
   python .\app.py
   ```

3. Los datos se guardarán en `pokemon.db` en la carpeta del proyecto.

---

### Problema 2: El HTML no se conecta a la API (CORS, fetch failed)

**Síntoma**: Ves errores en la consola del navegador tipo "Failed to fetch" o "CORS policy"

**Solución**:
- Asegúrate de que el servidor Flask esté corriendo (`python .\app.py`)
- Usa la URL correcta: `http://127.0.0.1:5000/static/dashboard.html` (no `file://`)
- Si abres el HTML como archivo local (`file://`), las llamadas a `/auth` y `/api` fallarán. Debes usar el servidor Flask.

---

### Problema 3: Login falla (credenciales incorrectas)

**Síntoma**: Al hacer login aparece "Email o contraseña incorrectos"

**Solución**:
1. Verifica que ejecutaste `python .\init_users.py` para crear los usuarios
2. Usa exactamente las credenciales listadas arriba (case-sensitive)
3. Si olvidaste la contraseña, vuelve a ejecutar `python .\init_users.py` (no duplica usuarios)

---

## 📁 Archivos creados/modificados

- ✅ **`static/dashboard.html`** — Interfaz HTML/JS completa con login y paneles
- ✅ **`INSTRUCCIONES_DASHBOARD.md`** — Este archivo con instrucciones

---

## 🧪 Próximos pasos opcionales

1. **Añadir más pokémons a la BD** (como profesor):
   - Login como profesor
   - Haz clic en "Crear Pokémon"
   - Rellena el formulario y guarda

2. **Asignar pokémons a trainers** (como profesor):
   - Login como profesor
   - Haz clic en "Asignar" junto a un pokémon
   - Escribe el email del trainer: `ash@pokemon.com` o `misty@pokemon.com`
   - Opcional: añade un apodo

3. **Ver y liberar pokémons** (como trainer):
   - Login como trainer (`ash@pokemon.com` / `ash123`)
   - Verás los pokémons asignados
   - Haz clic en "Liberar" para eliminar de tu colección

4. **Hacer commit de los cambios** en la rama `feature1`:
   ```powershell
   git add static/dashboard.html INSTRUCCIONES_DASHBOARD.md
   git commit -m "Añadir dashboard HTML con login y paneles para profesor/trainer"
   git push origin feature1
   ```

---

## 🎯 Resumen

- ✅ Dashboard HTML creado con todas las funcionalidades solicitadas
- ✅ Login separado para profesor y trainer
- ✅ Panel profesor: ver todos, crear, editar, eliminar, asignar
- ✅ Panel trainer: ver solo los suyos, liberar
- ✅ Usuarios de prueba creados en la BD
- ✅ Integración completa con la API Flask existente

**Para empezar ahora mismo**:
```powershell
# 1. Arranca el servidor (asegúrate de que MySQL esté corriendo)
python .\app.py

# 2. En otra terminal, abre el dashboard
Start-Process "http://127.0.0.1:5000/static/dashboard.html"

# 3. Haz clic en "Ejemplo Profesor" y luego "Entrar"
```

¡Listo para usar! 🚀
