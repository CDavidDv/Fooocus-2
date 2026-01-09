# 📤 Pasos para Publicar en GitHub

## ✅ Lo que ya está hecho

```
✓ .gitignore creado (evita archivos pesados)
✓ Primer commit hecho (601 archivos)
✓ Repositorio local inicializado
✓ Documentación completa
```

## 🚀 Los 4 Pasos para Publicar

### PASO 1: Crear repositorio en GitHub (2 minutos)

1. Ve a https://github.com/new
2. **Repository name:** `Fooocus`
3. **Description:** "Fooocus extended with batch processing and face swap"
4. **Visibility:** Public (recomendado) o Private
5. **Initialize repository:** NO (deja vacío)
6. Click **"Create repository"**

**Resultado:** Tendrás una URL como:
```
https://github.com/tu-usuario/Fooocus
```

---

### PASO 2: Configurar Git (2 minutos)

**Solo la primera vez en tu PC:**

```bash
git config --global user.name "Tu Nombre Real"
git config --global user.email "tu-email@gmail.com"
```

---

### PASO 3: Conectar con GitHub (1 minuto)

```bash
cd D:\carlo\Desktop\Fooocus-main

# Reemplaza "tu-usuario" con tu usuario de GitHub
git remote add origin https://github.com/tu-usuario/Fooocus.git

# Verificar que se conectó
git remote -v
```

**Salida esperada:**
```
origin  https://github.com/tu-usuario/Fooocus.git (fetch)
origin  https://github.com/tu-usuario/Fooocus.git (push)
```

---

### PASO 4: Hacer Push a GitHub (1 minuto)

```bash
git push -u origin main
```

**Esto:**
- Envía todos los commits a GitHub
- Configura la rama para rastreo automático
- Sube la documentación y código

**Salida esperada:**
```
Enumerating objects: 601, done.
Counting objects: 100% (601/601), done.
...
 * [new branch]      main -> main
Branch 'main' set up to track remote branch 'main' from 'origin'.
```

---

## 🎯 Opción Rápida: Usar Script Automatizado

### Windows (.bat):
```bash
cd D:\carlo\Desktop\Fooocus-main
push_to_github.bat
```

Te preguntará:
1. Remote a usar
2. Mensaje de commit (si hay cambios)
3. Procede con el push automáticamente

### Linux/Mac (.sh):
```bash
cd D:\carlo\Desktop\Fooocus-main
bash push_to_github.sh
```

---

## 📝 Ejemplo Completo (Copy-Paste)

```bash
# 1. Navegar a la carpeta
cd D:\carlo\Desktop\Fooocus-main

# 2. Verificar que todo está en orden
git status
# Debería mostrar "nothing to commit, working tree clean"

# 3. Ver commit previo
git log --oneline -1
# Debería mostrar: feat: Add batch processing + face swap + Colab support

# 4. Configurar global (solo primera vez)
git config --global user.name "Tu Nombre"
git config --global user.email "tu-email@gmail.com"

# 5. Conectar con GitHub
# (Reemplaza "tu-usuario" con tu usuario de GitHub)
git remote add origin https://github.com/tu-usuario/Fooocus.git

# 6. Verificar remote
git remote -v

# 7. Hacer push
git push -u origin main

# 8. Verificar en navegador
# Abre: https://github.com/tu-usuario/Fooocus
# ¡Deberías ver todos los archivos!
```

---

## ✨ Qué Se Va a Subir

### ✅ Se sube (código + docs):
```
✓ fooocus_colab_optimized.py
✓ run_batch_processing.py
✓ modules/batch_processor.py
✓ modules/face_processor.py
✓ presets/colab.json
✓ Toda la documentación (*.md)
✓ Código original de Fooocus
✓ Archivos de configuración
```

### ❌ NO se sube (archivos pesados):
```
✗ models/ (checkpoints, LoRAs, etc. - 25+ GB)
✗ outputs/ (imágenes generadas)
✗ batch_outputs/ (resultados)
✗ target_images/ (imágenes de usuario)
✗ .cache/ (archivos temporales)
✗ __pycache__/ (bytecode compilado)
✗ prompts.txt, face_model.jpg (archivos personales)
✗ config.txt (configuración local)
```

---

## 🔍 Verificación Final

Después de hacer push, verifica en GitHub:

1. **Abre:** https://github.com/tu-usuario/Fooocus
2. **Verifica que ves:**
   - [ ] Rama `main` con 1 commit
   - [ ] Archivos Python (*.py)
   - [ ] Documentación (*.md)
   - [ ] README.md o README_SETUP.md
   - [ ] .gitignore (archivo oculto)

3. **Ver commits:**
   - Click en "1 commit"
   - Deberías ver: "feat: Add batch processing + face swap + Colab support"

4. **Ver archivos:**
   - Deberías ver carpetas: `modules`, `extras`, `css`, etc.
   - Deberías ver archivos: `00_START_HERE.md`, `run_batch_processing.py`, etc.

---

## 🆘 Si Algo Sale Mal

### Problema: "fatal: 'origin' does not appear to be a 'git repository'"

**Solución:**
```bash
# Ver remotes actuales
git remote -v

# Si está vacío, agregar
git remote add origin https://github.com/tu-usuario/Fooocus.git
```

### Problema: "fatal: unable to access 'https://...' Could not resolve host"

**Causa:** Sin conexión a internet
**Solución:** Verifica tu conexión a internet

### Problema: "error: failed to push some refs to 'origin'"

**Causa:** El repositorio remoto tiene cambios
**Solución:**
```bash
git pull origin main --allow-unrelated-histories
git push -u origin main
```

### Problema: "Permission denied (publickey)"

**Causa:** Problemas de SSH (si usas SSH en lugar de HTTPS)
**Solución:** Usa HTTPS en lugar de SSH:
```bash
git remote set-url origin https://github.com/tu-usuario/Fooocus.git
git push -u origin main
```

---

## 📚 Archivos de Referencia

- `GITHUB_SETUP.md` - Guía completa y detallada
- `push_to_github.sh` - Script automático (Linux/Mac)
- `push_to_github.bat` - Script automático (Windows)
- `.gitignore` - Configuración de archivos a ignorar

---

## ✅ Checklist Final

Antes de considerar que está listo:

- [ ] Repositorio creado en GitHub
- [ ] Git configurado globalmente (`git config --global ...`)
- [ ] Remote agregado (`git remote add origin ...`)
- [ ] Push completado (`git push -u origin main`)
- [ ] Verifica en GitHub que los archivos estén presentes
- [ ] README o README_SETUP.md visible en la página principal
- [ ] Documentación clara y accesible

---

## 🎉 ¡Listo!

Una vez completados estos pasos, tu repositorio estará publicado en GitHub.

**Siguiente:**
- Comparte el link: `https://github.com/tu-usuario/Fooocus`
- Usuarios pueden hacer: `git clone https://github.com/tu-usuario/Fooocus.git`
- Siguen las instrucciones en `00_START_HERE.md`

---

**Tiempo total:** ~5 minutos

**Dificultad:** ⭐ Muy fácil (Copy-Paste)

**¡Éxito!** 🚀
