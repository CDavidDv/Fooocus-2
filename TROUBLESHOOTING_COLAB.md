# 🆘 Troubleshooting: Google Colab

Problemas comunes en Google Colab y cómo solucionarlos.

---

## ❌ Error 1: "Load preset failed"

### Síntomas:
```
Load preset [/content/Fooocus-2/presets/colab.json] failed
```

### Causa:
El preset `colab.json` no existe o hay problema al leerlo.

### Solución:
✅ **YA CORREGIDO** - Ahora usamos `--preset default` que siempre existe.

**En Colab, simplemente ejecuta:**
```python
!git clone https://github.com/tu-usuario/Fooocus.git
%cd Fooocus
!python fooocus_colab_optimized.py
```

Si aún ves este error, usa directamente:
```python
!python entry_with_update.py --preset default
```

---

## ❌ Error 2: "Exception in thread Thread-3 (worker)"

### Síntomas:
```
Exception in thread Thread-3 (worker):
Traceback (most recent call last):
  ...
  File "/content/Fooocus-2/modules/default_pipeline.py", line 263, in refresh_everything
    final_expansion = FooocusExpansion()
```

### Causa:
Problema al cargar el modelo FooocusExpansion. Generalmente timeout en descarga o ruta incorrecta.

### Solución:

**Opción 1: Reintentar**
```python
# Simplemente re-ejecuta en una nueva celda
!python entry_with_update.py --preset default
```

**Opción 2: Con timeout más largo**
```python
import os
os.environ['HF_HUB_DOWNLOAD_TIMEOUT'] = '600'  # 10 minutos

!python entry_with_update.py --preset default
```

**Opción 3: Sin LoRAs (más rápido)**
```python
# Editar config antes de correr
# O usar flags
!python entry_with_update.py --preset default --disable-xformers
```

---

## ❌ Error 3: "CUDA out of memory"

### Síntomas:
```
RuntimeError: CUDA out of memory. Tried to allocate X.XX GiB
```

### Causa:
GPU T4 de Colab se quedó sin memoria (solo 16 GB).

### Soluciones:

**Opción 1: Usar low-VRAM mode**
```python
!python entry_with_update.py --preset default --always-low-vram
```

**Opción 2: Reducir tamaño de imagen**
```
En Fooocus UI:
  Aspect Ratio: 896*896 (en lugar de 1152*896)
  Image Number: 1 (generar una a la vez)
```

**Opción 3: Upgrade a Colab Pro (A100)**
```
Si tienes Colab Pro, selecciona GPU "A100" que tiene 40 GB VRAM
```

---

## ❌ Error 4: "Connection refused" o "Cannot access localhost"

### Síntomas:
```
Error: Cannot access http://127.0.0.1:7865
```

### Causa:
Gradio no está siendo expuesto correctamente en Colab.

### Solución:

El script ya usa `--share` que debería crear un enlace público. Si aún no funciona:

```python
# En Colab, después de que Fooocus inicie, busca la salida:
# "To create a public link, set `share=True`"

# Debería mostrar algo como:
# Running on public URL: https://xxxxx.gradio.live

# Copia ese link en el navegador
```

---

## ✅ Soluciones Rápidas (Copy-Paste)

### Opción A: Setup limpio (recomendado)
```python
# Celda 1: Instalar dependencias
!pip install --upgrade git+https://github.com/lllyasviel/Fooocus.git
!pip install insightface onnxruntime-gpu

# Celda 2: Clonar y correr
!git clone https://github.com/tu-usuario/Fooocus.git
%cd Fooocus
!python fooocus_colab_optimized.py
```

### Opción B: Preset default sin custom launcher
```python
!git clone https://github.com/tu-usuario/Fooocus.git
%cd Fooocus
!python entry_with_update.py --preset default --listen
```

### Opción C: Minimalist (solo para batch processing)
```python
!git clone https://github.com/tu-usuario/Fooocus.git
%cd Fooocus

# Instalar solo lo necesario
!pip install -q insightface onnxruntime-gpu torch torchvision

# Crear prompt file
with open('prompts.txt', 'w') as f:
    f.write('a beautiful girl, professional portrait, 8k\n')
    f.write('a beautiful girl on beach, sunset, 8k\n')

# Subir face_model.jpg manualmente desde Files

# Ejecutar batch processor
!python run_batch_processing.py
```

---

## 📊 Requisitos Mínimos Colab

| Componente | Requerido |
|-----------|----------|
| GPU | T4 (free) o mejor |
| VRAM | 16 GB (T4) o 40 GB (A100) |
| RAM | ~8 GB |
| Disco | 30+ GB en Drive |
| Internet | Conexión estable |

---

## ⏱️ Tiempos Típicos Colab

| Fase | Tiempo | Notas |
|------|--------|-------|
| Instalación | 5-10 min | Primera vez |
| Descarga modelos | 10-15 min | ~6-7 GB |
| Generación imagen | 30-40s | T4 GPU |
| Face Swap | 5-10s | Por imagen |

---

## 🔥 Problemas Avanzados

### Problema: "RuntimeError: CPUAllocator"

**Causa:** Swap de disco insuficiente

**Solución:**
```python
# Liberar memoria
import gc
gc.collect()

# O reiniciar runtime
```

### Problema: Desconexión por timeout (después de 1 hora)

**Causa:** Colab desconecta si no hay actividad

**Solución:**
```python
# Agregar clicks automáticos en la UI
# O ejecutar batch processing (no necesita UI)
!python run_batch_processing.py
```

### Problema: "ModuleNotFoundError: No module named 'insightface'"

**Causa:** Dependencia no instalada

**Solución:**
```python
!pip install -q insightface onnxruntime-gpu
```

---

## ✨ Tips Pro Colab

1. **Montar Google Drive para persistencia:**
   ```python
   from google.colab import drive
   drive.mount('/content/drive')
   ```

2. **Ver archivos de salida:**
   ```python
   !ls -lah batch_outputs/
   !ls -lah target_images/faceswapped/
   ```

3. **Descargar resultados:**
   ```python
   from google.colab import files
   files.download('batch_outputs/batch_001_generated_faceswapped.png')
   ```

4. **Guardar modelos en Drive:**
   ```python
   # Después de descargar modelos:
   !cp -r models/ /content/drive/MyDrive/fooocus_models/

   # Próxima vez, copiar desde Drive:
   !cp -r /content/drive/MyDrive/fooocus_models/ models/
   ```

5. **Usar GPU A100 (más rápido):**
   - Colab Pro: Runtime → Change runtime type → GPU (A100)
   - Reduce tiempo a 8-10s por imagen

---

## 📞 Checklist Antes de Reportar Bug

- [ ] Limpié RAM y caché (`gc.collect()`)
- [ ] Reinicié el runtime
- [ ] Usé `--preset default` (no colab)
- [ ] Intenté con `--always-low-vram`
- [ ] Verifiqué conexión a internet
- [ ] Tengo 30+ GB disponibles en Drive

---

## 🎯 Flujo Recomendado Para Colab

```python
# 1. Instalar (una sola vez)
!pip install -q insightface onnxruntime-gpu
!git clone https://github.com/tu-usuario/Fooocus.git
%cd Fooocus

# 2. Ejecutar (cada vez que uses)
!python fooocus_colab_optimized.py

# O para batch processing (no requiere UI)
!python run_batch_processing.py
```

---

¿Aún tienes problemas? Intenta reproducir el error exacto y comparalo con las secciones de arriba.

**Si nada funciona:**
1. Reinicia el runtime (Runtime → Restart runtime)
2. Ejecuta en una nueva sesión
3. Intenta con preset "default" simplemente
