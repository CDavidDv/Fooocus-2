# 🚩 Guía de Flags: Cómo Ejecutar Fooocus

## 🎯 Lo Más Importante: `--share`

### ¿Qué es `--share`?

Crea un **enlace público temporal** que funciona desde **cualquier lugar del mundo**.

```bash
python entry_with_update.py --preset default --share
```

**Salida esperada:**
```
Running on local URL:  http://127.0.0.1:7865
Running on public URL: https://xxxxx.gradio.live

To create a public link, set `share=True` in `launch()`.
```

**Abre:** `https://xxxxx.gradio.live` en el navegador

**Características:**
- ✅ Acceso desde cualquier lugar (móvil, otra PC, tablet, etc.)
- ✅ No requiere configuración de red
- ✅ Enlace temporal (se genera cada sesión)
- ✅ Funciona en Colab, Local, Docker, etc.
- ⚠️ Enlace público (cualquiera con el link puede acceder)

---

## 📋 Flags Comunes

### Para Colab (RECOMENDADO)

```bash
python fooocus_colab_optimized.py
# Equivalente a:
# python entry_with_update.py --preset default --share --listen --always-high-vram
```

**Qué hace:**
- ✅ Detecta Colab automáticamente
- ✅ Usa `--preset default` (Juggernaut)
- ✅ Usa `--share` (UI pública)
- ✅ Usa `--always-high-vram` (máximo rendimiento Colab)

---

### Para Local (Con Acceso Público)

```bash
python entry_with_update.py --preset default --share
```

**Flags:**
- `--preset default` → Usar modelo Juggernaut
- `--share` → Crear enlace público gradio.live

---

### Para Local (Solo Acceso Local)

```bash
python entry_with_update.py --preset default
```

**Sin `--share`:**
- Solo accesible en `http://localhost:7865`
- Solo desde tu computadora

---

## 📊 Tabla de Flags Útiles

| Flag | Ejemplo | Para Qué |
|------|---------|---------|
| `--preset` | `--preset default` | Cambiar modelo (default, anime, realistic) |
| `--share` | `--share` | Crear enlace público gradio.live |
| `--listen` | `--listen` | Escuchar en toda la red (0.0.0.0) |
| `--port` | `--port 8888` | Cambiar puerto (default: 7865) |
| `--always-high-vram` | `--always-high-vram` | Máximo VRAM (Colab, GPU buena) |
| `--always-low-vram` | `--always-low-vram` | Mínimo VRAM (GPU débil, sin VRAM) |
| `--disable-xformers` | `--disable-xformers` | Desactivar optimizaciones (si hay problemas) |
| `--preview-option` | `--preview-option fast` | Tipo de preview (none, auto, fast, taesd) |
| `--disable-offload-from-vram` | `--disable-offload-from-vram` | Mantener modelos en GPU |

---

## 💡 Combinaciones Útiles

### Máxima Velocidad (GPU alta)

```bash
python entry_with_update.py \
  --preset default \
  --share \
  --always-high-vram \
  --disable-offload-from-vram
```

**Ideal para:** RTX 4090, RTX 3090, GPU de 16GB+

---

### GPU Débil o Sin VRAM

```bash
python entry_with_update.py \
  --preset default \
  --share \
  --always-low-vram \
  --preview-option fast
```

**Ideal para:** RTX 2060, GTX 1660, GPU 6GB

---

### Colab (Optimizado)

```bash
python fooocus_colab_optimized.py
```

**O manual:**
```bash
python entry_with_update.py \
  --preset default \
  --share \
  --listen \
  --always-high-vram
```

---

### Desarrollo Local (sin compartir)

```bash
python entry_with_update.py --preset default
```

**Solo en localhost**

---

## 🔐 Consideraciones de Seguridad

### ⚠️ Con `--share` (Público)

```
https://xxxxx.gradio.live ← PÚBLICO
↓
✅ Cualquiera con el link puede:
   - Generar imágenes
   - Hacer upscale
   - Cambiar parámetros
❌ Pero NO puede:
   - Acceder a tu disco
   - Ver tus archivos
   - Hacer cambios permanentes
```

**Recomendaciones:**
- ✅ Seguro para compartir con amigos
- ✅ Seguro para presentaciones
- ⚠️ No compartir públicamente en redes
- ⚠️ Requiere credenciales en producción (agregar `auth.json`)

### ✅ Sin `--share` (Local)

```
http://127.0.0.1:7865 ← PRIVADO
↓
Solo accesible desde tu PC
```

---

## 🎓 Ejemplos Reales

### Ejemplo 1: Compartir con amigos en Colab

```python
# En Colab
!git clone https://github.com/tu-usuario/Fooocus.git
%cd Fooocus
!python fooocus_colab_optimized.py

# Ver output:
# Running on public URL: https://xxxxx.gradio.live

# Copiar y compartir:
# "Aquí está el link: https://xxxxx.gradio.live"
# (Tus amigos abren el link sin necesidad de Colab)
```

---

### Ejemplo 2: Generar localmente sin compartir

```bash
# Tu PC
python entry_with_update.py --preset default

# Abrir: http://localhost:7865
# Solo tú puedes acceder
```

---

### Ejemplo 3: Servidor local en la red

```bash
# En tu servidor
python entry_with_update.py \
  --preset default \
  --listen \
  --port 8080

# Otros en la red usan:
# http://192.168.1.100:8080
```

---

## ❓ FAQ

**P: ¿Puedo cambiar la URL del enlace público?**
R: No, Gradio genera URLs aleatorias para seguridad.

**P: ¿Cuánto tiempo dura el enlace público?**
R: Mientras el proceso siga ejecutándose. Se regenera cada inicio.

**P: ¿Puedo usar `--share` + `--listen`?**
R: Sí, `--share` ya incluye `--listen` automáticamente.

**P: ¿Cómo agrego autenticación al enlace público?**
R: Crear archivo `auth.json`:
```json
[
  {"user": "usuario", "pass": "contraseña"}
]
```

**P: ¿Funciona `--share` en Docker/VPS?**
R: Sí, funciona en cualquier lugar.

**P: ¿Hay límite de enlaces públicos simultáneos?**
R: Uno por proceso. Puedes correr múltiples instancias en puertos diferentes.

---

## 🚀 Resumen Rápido

| Caso | Comando |
|------|---------|
| **Colab (fácil)** | `!python fooocus_colab_optimized.py` |
| **Local + compartir** | `python entry_with_update.py --preset default --share` |
| **Local privado** | `python entry_with_update.py --preset default` |
| **GPU débil** | `python entry_with_update.py --preset default --always-low-vram` |
| **Máximo rendimiento** | `python entry_with_update.py --preset default --always-high-vram` |

---

**Ahora sabes cómo ejecutar Fooocus en cualquier contexto!** 🎉
