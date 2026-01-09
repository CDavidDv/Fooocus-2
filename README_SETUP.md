# 🎨 Fooocus: Avatar Digital + Face Swap Setup

> **Nota:** Este es un fork de [Fooocus](https://github.com/lllyasviel/Fooocus) extendido con características de batch processing y face swap automático.

## 📖 Documentación Rápida

- **Principiante:** Lee [`00_START_HERE.md`](00_START_HERE.md) (5 min)
- **Quick Start:** Lee [`QUICK_START_BATCH.md`](QUICK_START_BATCH.md) (5 min)
- **Guía Completa:** Lee [`BATCH_PROCESSING_GUIDE.md`](BATCH_PROCESSING_GUIDE.md) (20 min)
- **Técnica:** Lee [`ARCHITECTURE_OVERVIEW.md`](ARCHITECTURE_OVERVIEW.md) (30 min)

## 🚀 Instalación Rápida

### Opción A: Google Colab (SIN GPU)

```python
!git clone https://github.com/tu-usuario/Fooocus.git
%cd Fooocus
!python fooocus_colab_optimized.py
```

**Automático:**
- ✅ Instala PyTorch
- ✅ Descarga modelos (Juggernaut, Realistic, Anime)
- ✅ Monta Google Drive
- ✅ Inicia Fooocus

### Opción B: Local (Windows/Linux)

```bash
# 1. Clonar
git clone https://github.com/tu-usuario/Fooocus.git
cd Fooocus

# 2. Instalar dependencias
pip install -r requirements_versions.txt
pip install insightface onnxruntime-gpu

# 3. Usar preset Colab (auto-descarga modelos)
python entry_with_update.py --preset default

# O ejecutar batch processing
python run_batch_processing.py
```

## ✨ 3 Características Principales

### 1️⃣ Checkpoints Automáticos
```bash
python entry_with_update.py --preset default
# Auto-descarga: Juggernaut, Realistic, Anime (~25 GB)
```

### 2️⃣ Batch Processing (Prompts → Imágenes + Face Swap)
```bash
# 1. Crear prompts.txt
echo "a girl in office, professional, 8k" > prompts.txt
echo "a girl on beach, sunset, 8k" >> prompts.txt

# 2. Subir face_model.jpg (tu cara)

# 3. Ejecutar
python run_batch_processing.py

# Resultado: batch_outputs/ (10+ imágenes con cara inyectada)
```

### 3️⃣ Detectar Caras y Reemplazarlas
```bash
# 1. Crear carpeta target_images/ con fotos
mkdir target_images
# (subir imágenes con caras)

# 2. Ejecutar script (procesa automáticamente)
python run_batch_processing.py

# Resultado: target_images/faceswapped/
```

## 📦 Requisitos

| Componente | Versión |
|-----------|---------|
| Python | 3.8+ |
| PyTorch | 2.1.0 |
| CUDA (opcional) | 12.1+ |
| GPU VRAM | 4GB mínimo |
| RAM | 8GB mínimo |
| Disco | 30GB+ |

## ⏱️ Tiempo de Ejecución

| GPU | Tiempo/imagen | Batch 10 |
|-----|--------------|---------|
| Colab T4 | 30-40s | 5-7 min |
| RTX 3060 | 15-20s | 2.5-3.5 min |
| RTX 3090 | 8-12s | 80-120s |
| RTX 4090 | 5-8s | 50-80s |

## 📚 Archivos Principales

### Código Nuevo
- `fooocus_colab_optimized.py` - Launcher automático para Colab
- `run_batch_processing.py` - CLI interactivo para batch processing
- `modules/batch_processor.py` - Procesador de prompts desde TXT
- `modules/face_processor.py` - Detección y face swap (InsightFace)
- `presets/colab.json` - Configuración de 3 modelos

### Documentación
- `00_START_HERE.md` - Punto de entrada
- `QUICK_START_BATCH.md` - Quick start 5 minutos
- `BATCH_PROCESSING_GUIDE.md` - Guía completa
- `ARCHITECTURE_OVERVIEW.md` - Diagramas técnicos
- `WEBUI_INTEGRATION_EXAMPLE.md` - Integración en UI
- `CLAUDE.md` - Referencia rápida

## 🎯 Casos de Uso

### Avatar Digital en Diferentes Poses
```
prompts.txt:
  woman standing, professional
  woman sitting, relaxed
  woman dancing, dynamic

Resultado: 3 imágenes, MISMA cara, diferentes poses
```

### Avatar Digital en Diferentes Situaciones
```
prompts.txt:
  woman in office, professional
  woman on beach, summer
  woman in cyberpunk city, neon

Resultado: 3 imágenes, MISMA cara, diferentes contextos
```

### Reemplazar Caras en Imágenes Existentes
```
target_images/:
  foto1.jpg
  foto2.jpg

Resultado: target_images/faceswapped/
  faceswapped_foto1.jpg (cara reemplazada)
  faceswapped_foto2.jpg (cara reemplazada)
```

## 🔧 Configuración Avanzada

Ver `BATCH_PROCESSING_GUIDE.md` para:
- Parámetros de configuración
- IP-Adapter (image prompt) tuning
- Face swap strength control
- Sampler y scheduler options

## 🆘 Problemas Comunes

### "InsightFace not found"
```bash
pip install insightface onnxruntime-gpu
```

### "No faces detected"
- Usar foto frontal (no perfil)
- Mejor iluminación
- Cara más grande en imagen

### "GPU out of memory"
```bash
python entry_with_update.py --preset default --always-low-vram
```

Ver `BATCH_PROCESSING_GUIDE.md` para más troubleshooting.

## 📄 Licencia

Este proyecto extiende [Fooocus](https://github.com/lllyasviel/Fooocus) que está bajo licencia [bajo la licencia original de Fooocus].

Las extensiones (batch processing + face swap) están bajo la misma licencia.

## 🙏 Créditos

- **Fooocus Original:** [lllyasviel/Fooocus](https://github.com/lllyasviel/Fooocus)
- **Face Detection:** [InsightFace](https://github.com/deepinsight/insightface)
- **Extensiones:** Batch Processing + Face Swap Automático

## 📞 Support

1. Lee la documentación:
   - `00_START_HERE.md` - Para empezar
   - `BATCH_PROCESSING_GUIDE.md` - Para problemas

2. Revisa `ARCHITECTURE_OVERVIEW.md` para entender la arquitectura

3. Abre un issue en GitHub si encuentras bugs

---

**¡Disfruta generando avatares digitales!** 🚀
