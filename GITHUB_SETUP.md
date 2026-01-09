# 📤 Cómo Publicar en GitHub

## ⚙️ Configuración Inicial (Una sola vez)

### 1️⃣ Crear repositorio en GitHub

1. Ve a https://github.com/new
2. **Repository name:** `Fooocus` (o el nombre que quieras)
3. **Description:** "Fooocus extended with batch processing and face swap"
4. **Visibility:** Public o Private
5. **Initialize repository:** NO (ya tenemos commits locales)
6. Click "Create repository"

### 2️⃣ Configurar Git localmente

**Primera vez (configurar usuario global):**
```bash
git config --global user.name "Tu Nombre"
git config --global user.email "tu-email@example.com"
```

**En la carpeta Fooocus (configurar para este repo):**
```bash
# Ver configuración actual
git config --list

# Ver remote actual
git remote -v
```

### 3️⃣ Conectar con GitHub y hacer push

**Si aún no hay remote configurado:**
```bash
cd D:\carlo\Desktop\Fooocus-main

# Conectar con GitHub (reemplaza tu-usuario y nombre-repo)
git remote add origin https://github.com/tu-usuario/Fooocus.git

# Verificar que se agregó
git remote -v

# Cambiar rama a "main" si es necesario
git branch -M main

# Push inicial (con -u para rastrear)
git push -u origin main
```

**Si ya hay un remote existente:**
```bash
# Ver remote actual
git remote -v

# Cambiar remote (si es incorrecto)
git remote set-url origin https://github.com/tu-usuario/Fooocus.git

# Push
git push -u origin main
```

---

## 🔄 Workflow Diario (Después de configurado)

### Guardar cambios locales

```bash
# Ver qué cambió
git status

# Agregar cambios
git add .

# Hacer commit
git commit -m "Descripción de los cambios"

# Enviar a GitHub
git push
```

### Ejemplo completo

```bash
cd D:\carlo\Desktop\Fooocus-main

# Editar archivos...

# Ver cambios
git status

# Agregar cambios
git add .

# Commit con mensaje descriptivo
git commit -m "fix: Ajustar parámetros de face swap"

# Push a GitHub
git push
```

---

## ✅ Errores Comunes y Soluciones

### Error 1: "fatal: No remote specified"

**Problema:** No hay remote configurado

**Solución:**
```bash
git remote add origin https://github.com/tu-usuario/Fooocus.git
git push -u origin main
```

### Error 2: "fatal: 'origin' does not appear to be a git repository"

**Problema:** Remote incorrecto

**Solución:**
```bash
# Ver remotes actuales
git remote -v

# Cambiar remote
git remote set-url origin https://github.com/tu-usuario/Fooocus.git

# Verificar
git remote -v

# Push
git push -u origin main
```

### Error 3: "error: failed to push some refs to 'origin'"

**Problema:** El repositorio remoto ya tiene commits

**Solución:**
```bash
# Pull primero
git pull origin main --allow-unrelated-histories

# Luego push
git push -u origin main
```

### Error 4: "Authentication failed"

**Problema:** GitHub no reconoce las credenciales

**Soluciones:**

**Opción A: Token de acceso personal (Recomendado)**
1. Ve a https://github.com/settings/tokens
2. Click "Generate new token"
3. Selecciona permisos: `repo`, `gist`, `user`
4. Copia el token
5. En vez de contraseña, usa: `git clone https://[token]@github.com/usuario/repo.git`

**Opción B: SSH (Más seguro)**
```bash
# Generar clave SSH
ssh-keygen -t ed25519 -C "tu-email@example.com"

# Copiar clave pública a GitHub:
# https://github.com/settings/keys
# (Pega el contenido de ~/.ssh/id_ed25519.pub)

# Usar SSH en remotes
git remote set-url origin git@github.com:tu-usuario/Fooocus.git
```

**Opción C: Windows Credential Manager**
1. Windows Start → "Credential Manager"
2. Generic Credentials → Agregar credencial
3. Nombre: `https://github.com`
4. Usuario: tu GitHub username
5. Contraseña: Tu GitHub token o password

### Error 5: ".gitignore no funciona"

**Problema:** Archivos que deberían ignorarse aparecen en cambios

**Solución:**
```bash
# Limpiar cache de git
git rm -r --cached .

# Re-agregar archivos (respetando .gitignore)
git add .

# Commit
git commit -m "fix: Actualizar gitignore"

# Push
git push
```

---

## 📊 Verificar Status

### Ver estado actual
```bash
git status
```

**Salida normal:**
```
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
```

### Ver commits
```bash
git log --oneline -10
```

### Ver remotes configurados
```bash
git remote -v
```

**Salida esperada:**
```
origin  https://github.com/tu-usuario/Fooocus.git (fetch)
origin  https://github.com/tu-usuario/Fooocus.git (push)
```

---

## 🎯 Checklist: Antes de hacer push

- [ ] `.gitignore` está configurado (no subir modelos/outputs)
- [ ] Los commits tienen mensajes descriptivos
- [ ] No hay archivos personales (prompts.txt, face_model.jpg, etc.)
- [ ] Verificaste `git status` antes de push
- [ ] El repositorio en GitHub está creado
- [ ] El remote está configurado correctamente (`git remote -v`)

---

## 📝 Buenas Prácticas

### Mensajes de Commit Efectivos

❌ **Malo:**
```
git commit -m "fix"
git commit -m "update"
git commit -m "cambios"
```

✅ **Bueno:**
```bash
git commit -m "feat: Agregar batch processing de prompts TXT"
git commit -m "fix: Corregir detección de caras en InsightFace"
git commit -m "docs: Actualizar guía de batch processing"
```

### Estructura de mensaje
```
[tipo]: [descripción corta]

[Descripción larga opcional - qué cambió y por qué]
```

**Tipos comunes:**
- `feat:` - Nueva característica
- `fix:` - Corrección de bug
- `docs:` - Cambios en documentación
- `refactor:` - Refactorización de código
- `test:` - Agregar/actualizar tests
- `perf:` - Mejoras de performance

### Ejemplos completos

```bash
git commit -m "feat: Agregar CLI interactivo para batch processing

- Leer prompts desde archivo TXT
- Configuración interactiva de parámetros
- Guardar configuración en JSON para reproducibilidad"

git commit -m "fix: Corregir detección de múltiples caras

- Asegurar que se detecta la primera cara en imágenes
- Mejorar manejo de errores si no hay caras
- Agregar logging informativo"

git commit -m "docs: Actualizar QUICK_START_BATCH.md

- Agregar ejemplos de casos de uso
- Mejorar formato y claridad
- Agregar tiempo estimado de ejecución"
```

---

## 🚀 Resumen Rápido

**Primera vez:**
```bash
# 1. Crear repositorio en GitHub

# 2. Configurar local
git config --global user.name "Tu Nombre"
git config --global user.email "tu-email@example.com"

# 3. Conectar y push
git remote add origin https://github.com/tu-usuario/Fooocus.git
git push -u origin main
```

**Cambios posteriores:**
```bash
# Edit files...
git add .
git commit -m "feat: Descripción de cambios"
git push
```

---

## ❓ FAQ

**P: ¿Qué archivos se van a subir?**
R: Los definidos en `.gitignore` NO se suben. Los modelos, outputs, y archivos temporales NO se suben.

**P: ¿Cómo cambio el nombre del repositorio?**
R: En GitHub: Settings → Repository name

**P: ¿Puedo hacer push sin conectar remote primero?**
R: No, primero debes configurar el remote con `git remote add origin ...`

**P: ¿Se pueden cambiar los commits ya hecho?**
R: Sí, pero requiere `git rebase` o `git amend`. Mejor evitar si ya hizo push.

**P: ¿Cómo borro un archivo subido?**
R:
```bash
git rm --cached archivo.txt
git commit -m "remove: Borrar archivo"
git push
```

---

¡Ahora estás listo para publicar en GitHub! 🚀
