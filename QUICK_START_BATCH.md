# 🚀 Quick Start: Avatar Digital + Face Swap

Para impaciantes: 3 características en 5 minutos

---

## ✅ Característica 1: Checkpoints Automáticos

### Google Colab (IDEAL)

```python
!git clone https://github.com/tu-usuario/Fooocus.git
%cd Fooocus
!python fooocus_colab_optimized.py
```

**Que pasa automáticamente:**
- ✅ Instala PyTorch
- ✅ Descarga Juggernaut XL, Realistic, Anime
- ✅ Monta Google Drive
- ✅ Inicia Fooocus

**Primera vez:** ~10 min | **Siguientes:** <1 min

### Local (Windows/Linux)

```bash
python entry_with_update.py --preset colab
```

Descarga: Juggernaut + Realistic + Anime automáticamente

---

## ✅ Característica 2: Prompts TXT → Imágenes + Face Swap

### 3 pasos:

**1. Crear `prompts.txt`:**
```
a girl in office, professional, 8k
a girl on beach, sunset, 8k
a girl in cyberpunk city, neon, 8k
```

**2. Subir `face_model.jpg`:**
- Foto clara de la cara (512-2048 px)
- Frontal o 3/4
- Buena iluminación

**3. Ejecutar:**
```bash
python run_batch_processing.py
```

Interactivo - te pregunta todo:
```
📝 Archivo de prompts [prompts.txt]: (Enter)
😊 Imagen de cara [face_model.jpg]: (Enter)
⚙️ Pasos [20]: (Enter)
...
✅ LISTO
```

**Resultado en `batch_outputs/`:**
```
batch_001_generated.png          ← Imagen generada
batch_001_generated_faceswapped.png  ← Con cara inyectada
batch_002_generated.png
batch_002_generated_faceswapped.png
...
```

---

## ✅ Característica 3: Detectar Cara y Reemplazarla

### Para imágenes existentes:

**1. Crear carpeta `target_images/`:**
```
target_images/
├── foto1.jpg
├── foto2.jpg
├── foto3.jpg
```

**2. Ejecutar batch processing:**
```bash
python run_batch_processing.py
```

El script automáticamente también procesa `target_images/`

**Resultado en `target_images/faceswapped/`:**
```
faceswapped_foto1.jpg  ← Cara reemplazada
faceswapped_foto2.jpg
faceswapped_foto3.jpg
```

---

## ⚡ Equivalencia Simplificada

### Antes (Manual)
```
Imagen → Fooocus → Descargar → Photoshop → Face Swap → Guardareperir 10 veces = 1 hora
```

### Ahora (Automático)
```
prompts.txt + face_model.jpg → Script → ¡LISTO! 10 imágenes = 5 minutos
```

---

## 📝 Archivo `prompts.txt` - Ejemplos

### Avatar en diferentes poses
```
a beautiful woman, standing, professional outfit, 8k
a beautiful woman, sitting at desk, business casual, 8k
a beautiful woman, dancing, dynamic pose, 8k
a beautiful woman, laying down, relaxed, 8k
```

### Avatar en diferentes situaciones
```
a woman in a coffee shop, warm lighting, cozy, 8k
a woman in an office, professional setting, 8k
a woman at the beach, sunset, summer vibes, 8k
a woman in a cyberpunk city, neon lights, 8k
a woman in a fantasy forest, magical, ethereal, 8k
```

### Avatar con diferentes outfits
```
a woman in a red dress, elegant, 8k
a woman in a business suit, professional, 8k
a woman in casual clothes, relaxed, 8k
a woman in formal wear, glamorous, 8k
```

---

## 🎮 Configuración Rápida por Caso de Uso

### Realista (Mejor Calidad)
```bash
python run_batch_processing.py
# Pasos: 25
# CFG: 5.0
# Image Prompt: 0.6
# Tiempo: ~40s/imagen
```

### Variedad (Diferentes Poses)
```bash
python run_batch_processing.py
# Pasos: 20
# CFG: 4.0
# Image Prompt: 0.4
# Sampler: dpmpp_3m_sde_gpu
# Tiempo: ~30s/imagen
```

### Rápido (Colab Free)
```bash
python run_batch_processing.py
# Pasos: 15
# CFG: 3.5
# Resolución: 896x896
# Tiempo: ~20s/imagen
```

---

## 🔧 Instalación de Dependencias

Para face swap automático:
```bash
pip install insightface onnxruntime-gpu
```

O para CPU:
```bash
pip install insightface onnxruntime
```

---

## 📊 Rendimiento

| Plataforma | Tiempo/imagen | Batch 10 |
|-----------|--------------|---------|
| Colab T4 | 30-40s | 5-7 min |
| RTX 3060 | 15-20s | 2.5-3.5 min |
| RTX 4090 | 5-8s | 50-80s |

---

## 🆘 Si Algo No Funciona

### "No encuentro prompts.txt"
```bash
python run_batch_processing.py
# Se crea automáticamente con ejemplos
```

### "Face swap no funciona"
```bash
# Instalar InsightFace
pip install insightface onnxruntime-gpu
```

### "GPU sin memoria"
```bash
python entry_with_update.py --preset colab --always-low-vram
```

---

## 💡 Tips Pro

1. **Consistencia de cara:** Usa `image_prompt_strength = 0.5-0.6`
2. **Variedad de pose:** Varía los prompts dramáticamente
3. **Mejor calidad:** Aumenta `steps` a 25-30
4. **Más rápido:** Reduce `steps` a 15-18
5. **Múltiples caras:** Cambia `face_model.jpg` y re-ejecuta

---

## 📁 Estructura de Carpetas

```
Fooocus/
├── prompts.txt                    ← TUS PROMPTS
├── face_model.jpg                 ← CARA DEL MODELO
├── target_images/                 ← IMÁGENES PARA PROCESAR
│   ├── foto1.jpg
│   └── ...
├── batch_outputs/                 ← RESULTADOS
│   ├── batch_001_generated.png
│   ├── batch_001_generated_faceswapped.png
│   └── ...
├── run_batch_processing.py        ← EJECUTA ESTO
└── presets/colab.json             ← CONFIG (ya incluido)
```

---

¡Listo! Ahora solo crea los archivos y ejecuta. 🎉

**Next step:** `python run_batch_processing.py`
