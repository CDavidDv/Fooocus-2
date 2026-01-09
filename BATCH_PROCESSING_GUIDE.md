# Guía Completa: Batch Processing + Face Swap

Este documento explica cómo usar las 3 características implementadas:
1. ✅ Gestión óptima de checkpoints
2. ✅ Generar imágenes desde TXT + Face Swap automático
3. ✅ Detectar y reemplazar caras en imágenes

---

## 1️⃣ CARACTERÍSTICA 1: Gestión Óptima de Checkpoints

### Solución Recomendada: Hugging Face Hub + Preset Colab

**¿Por qué es óptima?**
- ✅ Gratuito sin límites de tamaño
- ✅ Auto-descargar en Colab (~2-3 min por modelo de 8GB)
- ✅ No pesa en GitHub
- ✅ Rápido en Colab con GPU

### Opción A: En Google Colab (RECOMENDADO)

**Paso 1: Usar el notebook optimizado**

```python
# En tu Colab notebook:

!git clone https://github.com/tu-usuario/Fooocus.git
%cd Fooocus

!python fooocus_colab_optimized.py
```

**Qué hace automáticamente:**
- ✓ Instala PyTorch optimizado para Colab
- ✓ Descarga checkpoints (Juggernaut, Realistic, Anime)
- ✓ Monta Google Drive para persistencia
- ✓ Expone UI via gradio.live

**Tiempo de primera ejecución:** ~5-10 minutos
- Instalación de dependencias: ~3 min
- Descarga de checkpoints (3 modelos × 8GB): ~5-7 min total
- Siguiente ejecución: <30 segundos

### Opción B: En Local (Windows/Linux)

**Paso 1: Usar el preset colab**

```bash
# Windows
python entry_with_update.py --preset colab

# Linux
python entry_with_update.py --preset colab --listen
```

**Checkpoints que se descargan automáticamente:**
- `juggernautXL_v9.safetensors` (8.2 GB) - General purpose
- `realisticStockPhoto_v20.safetensors` (7.8 GB) - Fotorrealistico
- `animaPencilXL_v500.safetensors` (7.5 GB) - Anime

### Agregar Más Checkpoints

**Editar `presets/colab.json`:**

```json
"checkpoint_downloads": {
    "juggernautXL_v9.safetensors": "https://huggingface.co/lllyasviel/fav_models/resolve/main/fav/juggernautXL_v9.safetensors",
    "tu_modelo.safetensors": "https://huggingface.co/tu-usuario/tu-modelo/resolve/main/tu_modelo.safetensors"
}
```

**Dónde obtener URLs de Hugging Face:**
1. Ve a https://huggingface.co/tu-usuario/tu-repo
2. Click en archivo `.safetensors`
3. Click en botón ">" (mostrar URL)
4. Copia la URL

---

## 2️⃣ CARACTERÍSTICA 2: Prompts en TXT + Face Swap Automático

### Flujo Completo

```
prompts.txt ───┐
               │
               ├──> Fooocus Generate ──> Imágenes Generadas
               │
face_model.jpg ┤
               │
               └──> Face Swap ──> Imágenes con Cara del Modelo
```

### Paso 1: Crear archivo de prompts

**Crear `prompts.txt` en la carpeta raíz:**

```
# Cada línea es un prompt separado
# Las líneas con # se ignoran

a beautiful girl in a office, professional attire, natural lighting, 8k
a girl on a beach, sunset, summer vibes, detailed, 8k
a girl in a cyberpunk city, neon lights, sci-fi, 8k
a girl in a fantasy forest, magical, ethereal, 8k
a girl in formal wear, elegant, studio lighting, 8k
```

**Formato:**
- Un prompt por línea
- Ignorar líneas vacías y comentarios (#)
- Máximo 500 caracteres por prompt (recomendado: 50-200)

### Paso 2: Subir imagen de cara del modelo

**Archivo: `face_model.jpg` o `face_model.png`**

Requisitos:
- ✅ Cara clara y bien iluminada
- ✅ Resolución: 512×512 a 2048×2048
- ✅ Formato: JPG, PNG o WEBP
- ✅ Tamaño: <50 MB

**Cómo obtener la imagen:**
1. Tomar una foto frontal o de 3/4 de la cara
2. Asegurar buena iluminación
3. No usar filtros extremos
4. Guardar como `face_model.jpg`

### Paso 3: Ejecutar batch processing

**Opción A: Desde Python (Recomendado)**

```python
from modules.batch_processor import BatchProcessor, BatchProcessorConfig

# Crear configuración
config = BatchProcessorConfig()
config.prompts_file = "prompts.txt"
config.face_model_image = "face_model.jpg"
config.enable_face_swap = True
config.use_image_prompt = True  # Usar cara como referencia visual
config.steps = 20
config.cfg_scale = 4.0

# Crear processor
processor = BatchProcessor(config)

# Obtener tareas
tasks = processor.get_generation_tasks()

# Guardar config (para referencia)
processor.save_config_file()

print(f"Tareas creadas: {len(tasks)}")
for task in tasks:
    print(f"  - {task['task_id']}: {task['prompt'][:60]}...")
```

**Opción B: Desde la UI de Fooocus (cuando se integre)**

> Nueva pestaña "Batch Processing" con interfaz gráfica

### Resultados

Después de ejecutar, encontrarás en `batch_outputs/`:

```
batch_outputs/
├── batch_001_generated.png     ← Imagen generada
├── batch_001_generated_faceswapped.png  ← Con face swap
├── batch_002_generated.png
├── batch_002_generated_faceswapped.png
...
└── batch_config.json           ← Configuración usada
```

---

## 3️⃣ CARACTERÍSTICA 3: Detectar Cara y Reemplazarla

### Para imágenes existentes

**Flujo:**

```
Imagen 1 ──┐
Imagen 2 ──┤  ← Detectar caras
Imagen 3 ──┤
Imagen N ──┘
           │
           ├──> Face Swap ──> Imágenes reemplazadas
           │
        face_model.jpg
```

### Paso 1: Preparar imágenes

**Crear carpeta: `target_images/`**

```
target_images/
├── foto1.jpg
├── foto2.png
├── foto3.jpg
...
```

Requisitos:
- ✅ Caras claras y visibles
- ✅ Buena iluminación
- ✅ Formato: JPG, PNG, WEBP
- ✅ Tamaño: recomendado 1080×1440 o similar

### Paso 2: Ejecutar face swap batch

```python
from modules.face_processor import FaceSwapPostProcessor

# Crear processor
processor = FaceSwapPostProcessor(
    face_model_image="face_model.jpg"
)

# Procesar todas las imágenes
processor.process_batch(
    images_folder="target_images",
    output_folder="target_images_faceswapped"
)
```

### Resultados

En `target_images_faceswapped/`:
```
target_images_faceswapped/
├── faceswapped_foto1.jpg
├── faceswapped_foto2.jpg
├── faceswapped_foto3.jpg
...
```

---

## Uso Avanzado: Integración Personalizada

### Combinar Todo en un Script

```python
#!/usr/bin/env python
"""Script completo: Generar + Face Swap + Batch Process"""

import os
from modules.batch_processor import BatchProcessor, BatchProcessorConfig
from modules.face_processor import FaceSwapPostProcessor

def main():
    # ============= PASO 1: GENERAR IMÁGENES =============
    print("\n" + "="*50)
    print("PASO 1: Generando imágenes desde prompts...")
    print("="*50 + "\n")

    config = BatchProcessorConfig()
    config.prompts_file = "prompts.txt"
    config.face_model_image = "face_model.jpg"
    config.enable_face_swap = True
    config.use_image_prompt = True
    config.steps = 20

    processor = BatchProcessor(config)
    tasks = processor.get_generation_tasks()

    print(f"✓ {len(tasks)} tareas de generación preparadas")
    print(f"  Ejecutar estas tareas en async_worker...")

    # ============= PASO 2: FACE SWAP A GENERADAS =============
    print("\n" + "="*50)
    print("PASO 2: Aplicando face swap a imágenes generadas...")
    print("="*50 + "\n")

    swap_processor = FaceSwapPostProcessor("face_model.jpg")
    swap_processor.process_batch(
        images_folder=config.batch_output_folder,
        output_folder=os.path.join(config.batch_output_folder, "with_face_swap")
    )

    # ============= PASO 3: FACE SWAP A IMÁGENES TARGETS =============
    print("\n" + "="*50)
    print("PASO 3: Reemplazando caras en imágenes target...")
    print("="*50 + "\n")

    swap_processor.process_batch(
        images_folder=config.target_images_folder,
        output_folder=os.path.join(config.target_images_folder, "faceswapped")
    )

    print("\n" + "="*50)
    print("✓ PROCESO COMPLETADO")
    print("="*50)
    print(f"\nResultados en:")
    print(f"  - Generadas: {config.batch_output_folder}")
    print(f"  - Face Swap: {config.batch_output_folder}/with_face_swap")
    print(f"  - Targets: {config.target_images_folder}/faceswapped")

if __name__ == "__main__":
    main()
```

---

## Troubleshooting

### Problema: "InsightFace no encontrado"

```bash
pip install insightface onnxruntime-gpu
```

O para CPU:
```bash
pip install insightface onnxruntime
```

### Problema: Face swap no funciona / cara no detectada

**Causas:**
- Imagen de cara muy pequeña
- Iluminación pobre
- Ángulo extremo (perfil)
- Cara parcialmente oculta

**Soluciones:**
1. Usar imagen de cara más clara y frontal
2. Asegurar buena iluminación en imagen target
3. Aumentar tamaño de la cara en imagen
4. Probar con cara diferente

### Problema: Generación lenta en Colab

```python
# Agregar flags optimizados
python entry_with_update.py --preset colab --always-high-vram --preview-option fast
```

### Problema: GPU sin memoria

```python
# Reducir aspectos:
python entry_with_update.py --preset colab --always-low-vram
```

---

## Configuración Avanzada

### BatchProcessorConfig - Todas las opciones

```python
from modules.batch_processor import BatchProcessorConfig

config = BatchProcessorConfig()

# Rutas
config.prompts_file = "custom_prompts.txt"
config.face_model_image = "my_face.jpg"
config.target_images_folder = "my_images"
config.batch_output_folder = "my_outputs"

# Face Swap
config.enable_face_swap = True
config.face_swap_strength = 1.0  # 0.0-1.0 (1.0 = máximo swap)

# Image Prompt (IP-Adapter)
config.use_image_prompt = True  # Usar cara como ref visual
config.image_prompt_strength = 0.5  # 0.0-1.0

# Generación
config.aspect_ratio = "1152*896"  # Otros: "1024*1024", "896*1152"
config.steps = 20  # 15-25 recomendado
config.cfg_scale = 4.0  # 3.0-7.0
config.sampler = "dpmpp_2m_sde_gpu"  # O "dpmpp_3m_sde_gpu"
config.seed = -1  # -1 = aleatorio
```

### Parámetros para Diferentes Casos

**Avatar Digital Realista:**
```python
config.steps = 25
config.cfg_scale = 5.0
config.image_prompt_strength = 0.6
config.face_swap_strength = 1.0
config.sampler = "dpmpp_2m_sde_gpu"
```

**Variedad de Poses/Situaciones:**
```python
config.steps = 20
config.cfg_scale = 4.0
config.image_prompt_strength = 0.4
config.sampler = "dpmpp_3m_sde_gpu"  # Más iteraciones internas
```

**Rápido (Colab free tier):**
```python
config.steps = 15
config.cfg_scale = 3.5
config.aspect_ratio = "896*896"  # Más pequeño
config.sampler = "dpmpp_2m_sde_gpu"
```

---

## Comparativa: Antes vs Después

### Antes (Manual)
```
1. Escribir prompt en UI
2. Click generar
3. Esperar imagen
4. Descargar imagen
5. Abrir Photoshop/software de face swap
6. Importar imagen de cara
7. Hacer face swap manualmente
8. Guardar
9. Repetir para cada prompt...
```
⏱️ **~5 minutos por imagen**

### Después (Automatizado)
```
1. Crear prompts.txt
2. Subir face_model.jpg
3. python run_batch_processing.py
4. ¡Listo! 10 imágenes + face swap aplicado
```
⏱️ **~30 segundos de configuración + tiempo de generación**

---

## Soporte y Ejemplos

### Generar Avatar en diferentes poses

**prompts.txt:**
```
a beautiful woman, standing, professional outfit, office background, 8k
a beautiful woman, sitting, casual wear, coffee shop, 8k
a beautiful woman, dancing, club lights, colorful, 8k
a beautiful woman, walking, park background, sunny, 8k
a beautiful woman, lying down, bedroom, cozy, 8k
```

Con `image_prompt_strength=0.5`, cada imagen tendrá:
- ✓ Similitud visual con la cara (0.5 de influencia)
- ✓ Variedad de poses/situaciones
- ✓ Cara reemplazada con face swap

### Crear variantes de outfit

**prompts.txt:**
```
a woman in a red dress, professional portrait, studio lighting, 8k
a woman in a blue dress, professional portrait, studio lighting, 8k
a woman in a black dress, professional portrait, studio lighting, 8k
a woman in a business suit, professional portrait, studio lighting, 8k
```

Mantener consistencia de cara mientras cambias ropa.

---

## Performance Esperado

| GPU | 1 imagen | Batch 10 | Batch 50 |
|-----|---------|---------|---------|
| RTX 4090 | 5-8s | 50-80s | 4-7 min |
| RTX 3090 | 8-12s | 80-120s | 6-10 min |
| RTX 3060 12GB | 15-20s | 150-200s | 12-17 min |
| Colab T4 | 30-40s | 5-7 min | 20-30 min |
| Colab A100 | 8-10s | 80-100s | 6-10 min |

---

¡Ahora estás listo para generar tu avatar digital! 🚀
