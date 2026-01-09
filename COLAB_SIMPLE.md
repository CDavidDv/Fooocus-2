# 🚀 Google Colab - Ultra Simple

## Copy-Paste Esto en Colab

### Celda 1: Setup (5-10 minutos, solo primera vez)

```python
# Clonar repositorio
!git clone https://github.com/tu-usuario/Fooocus.git
%cd Fooocus

# Instalar dependencias
!pip install -q -r requirements_versions.txt
!pip install -q insightface onnxruntime-gpu
```

### Celda 2: Ejecutar Fooocus (UI Pública)

```python
!python fooocus_colab_optimized.py
```

**Esto debería mostrar:**
```
[COLAB] Detectado entorno Google Colab
[COLAB] Montando Google Drive...
[COLAB] Instalando PyTorch...
[COLAB] Iniciando Fooocus...
Running on local URL:  http://127.0.0.1:7865
Running on public URL: https://xxxxx.gradio.live  ← COPIA ESTE LINK
```

**¡Abre el link `https://xxxxx.gradio.live` en tu navegador!**

Ese es un enlace público que funciona desde cualquier lugar (computadora, tablet, móvil, otro navegador, etc.).

---

## Si No Funciona

### Error: "Load preset failed"

```python
# Usa esto en lugar de arriba:
!python entry_with_update.py --preset default --listen --share
```

### Error: "CUDA out of memory"

```python
# Usa low-VRAM mode:
!python entry_with_update.py --preset default --always-low-vram --listen --share
```

### Error: "ModuleNotFoundError: insightface"

```python
!pip install -q insightface onnxruntime-gpu
```

### No ves el link de Gradio

```python
# Mira la salida de la celda anterior
# Debería mostrar: "Running on public URL: https://..."
# Si no, espera 30 segundos más
```

---

## ✨ Para Batch Processing (Sin UI)

### Celda 1: Setup
```python
!git clone https://github.com/tu-usuario/Fooocus.git
%cd Fooocus
!pip install -q insightface onnxruntime-gpu torch torchvision
```

### Celda 2: Crear archivos

```python
# Crear prompts.txt
with open('prompts.txt', 'w') as f:
    f.write('a beautiful girl, professional, 8k\n')
    f.write('a beautiful girl on beach, sunset, 8k\n')
    f.write('a beautiful girl in office, professional, 8k\n')

print("✓ prompts.txt creado")
```

### Celda 3: Subir face_model.jpg

```python
from google.colab import files
print("📤 Sube tu archivo face_model.jpg")
uploaded = files.upload()
```

### Celda 4: Batch Process

```python
!python run_batch_processing.py --no-interactive \
  --prompts prompts.txt \
  --face face_model.jpg \
  --output batch_outputs
```

### Celda 5: Descargar resultados

```python
from google.colab import files
import os

# Listar resultados
!ls -lah batch_outputs/

# Descargar una imagen
files.download('batch_outputs/batch_001_generated_faceswapped.png')
```

---

## 📊 Tiempos (Colab T4 gratis)

| Fase | Tiempo |
|------|--------|
| Setup inicial | 5-10 min |
| Descarga modelos | 10-15 min |
| Generación 1 imagen | 30-40s |
| Face Swap 1 imagen | 5-10s |
| **Batch 10 imágenes** | **5-7 min** |

---

## ⚠️ Límites Colab

- **T4 GPU:** 16 GB VRAM (gratis, puede desconectarse)
- **A100 GPU:** 40 GB VRAM (Colab Pro $9.99/mes, más rápido)
- **Tiempo máximo:** 12 horas continuas (después se disconnecta)
- **Almacenamiento:** Guardar en Drive para persistencia

---

## 💡 Pro Tips

### Guardar modelos en Drive (para siguiente vez)

```python
# Después de que descargen:
!cp -r models/ /content/drive/MyDrive/fooocus_models/

# Próxima vez:
!cp -r /content/drive/MyDrive/fooocus_models/ models/
```

### Mantener Drive montado

```python
from google.colab import drive
drive.mount('/content/drive')

# Luego usar:
!python fooocus_colab_optimized.py \
  --external-working-path /content/drive/MyDrive/fooocus_models
```

### Ver salida en tiempo real

```python
# Los comandos con ! muestran salida en tiempo real
# Si se tarda mucho, NO cierre la celda
# Espere a que termine
```

---

## ❓ FAQ

**P: ¿Puedo usar Colab gratis?**
R: Sí, con GPU T4 gratis. Un poco lento pero funciona.

**P: ¿Cuánto tiempo toma generar una imagen?**
R: ~30-40 segundos con T4. ~8-10 segundos con A100.

**P: ¿Se pierden los modelos si me desconecto?**
R: Sí, debes guardarlos en Google Drive para reutilizar.

**P: ¿Puedo generar múltiples imágenes en paralelo?**
R: No, Colab solo tiene 1 GPU. Hace batch processing secuencial.

**P: ¿Es legal usar Colab para esto?**
R: Sí, es permitido. Solo no uses para proyectos comerciales con TOS muy estrictos.

---

## 🚀 ¡Listo!

Copia los comandos de arriba en Colab y ¡a generar avatares!

Si tienes problemas, lee `TROUBLESHOOTING_COLAB.md`

---

**Tiempo total para primera imagen:** ~30 minutos (incluye descargas)

**Próximas imágenes:** Solo 30-40 segundos cada una ⚡
