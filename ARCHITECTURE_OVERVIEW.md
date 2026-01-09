# 🏗️ Arquitectura: Avatar Digital + Face Swap

## Diagrama General

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          FOOOCUS EXTENDED SYSTEM                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                     USER INPUTS                                      │  │
│  ├──────────────────────────────────────────────────────────────────────┤  │
│  │  • prompts.txt (uno por línea)                                      │  │
│  │  • face_model.jpg (cara del modelo)                                 │  │
│  │  • target_images/ (imágenes para procesar)                          │  │
│  │  • Configuración (steps, CFG, sampler)                              │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                 ↓                                            │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │              MODULES/BATCH_PROCESSOR.PY                              │  │
│  ├──────────────────────────────────────────────────────────────────────┤  │
│  │  • Lee prompts desde TXT                                            │  │
│  │  • Crea tareas AsyncTask                                           │  │
│  │  • Configura IP-Adapter (image prompt)                             │  │
│  │  • Configuración guardada en JSON                                  │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│           ↓                                        ↓                         │
│  ┌────────────────────┐                  ┌────────────────────┐            │
│  │ GENERACIÓN         │                  │ FACE SWAP TARGETS  │            │
│  │ get_generation..() │                  │ get_face_swap..()  │            │
│  └────────────────────┘                  └────────────────────┘            │
│           ↓                                        ↓                         │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │     MODULES/FACE_PROCESSOR.PY                                        │  │
│  ├──────────────────────────────────────────────────────────────────────┤  │
│  │  FACEDETECTOR:                                                      │  │
│  │  • InsightFace lazy-loading                                         │  │
│  │  • detect_faces() → detecta caras                                   │  │
│  │  • swap_faces() → reemplaza caras                                   │  │
│  │                                                                      │  │
│  │  FACESWAPPOSTPROCESSOR:                                            │  │
│  │  • Aplica face swap a imágenes generadas                           │  │
│  │  • Batch processing de target_images/                              │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│           ↓                                        ↓                         │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │              FOOOCUS CORE (webui.py + async_worker.py)              │  │
│  ├──────────────────────────────────────────────────────────────────────┤  │
│  │  • Recibe tareas (AsyncTask)                                        │  │
│  │  • Carga modelos (base + refiner)                                   │  │
│  │  • Aplica IP-Adapter (si use_image_prompt=True)                     │  │
│  │  • Diffusion sampling                                              │  │
│  │  • VAE decode                                                      │  │
│  │  • Salida: imágenes generadas                                      │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│           ↓                                        ↓                         │
│  ┌────────────────────┐                  ┌────────────────────┐            │
│  │ FACE SWAP          │                  │ BATCH RESULTS      │            │
│  │ POST-GENERATION    │                  │ COMPILACIÓN        │            │
│  └────────────────────┘                  └────────────────────┘            │
│           ↓                                        ↓                         │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                  OUTPUT: batch_outputs/                              │  │
│  ├──────────────────────────────────────────────────────────────────────┤  │
│  │  batch_001_generated.png                                            │  │
│  │  batch_001_generated_faceswapped.png                                │  │
│  │  batch_002_generated.png                                            │  │
│  │  batch_002_generated_faceswapped.png                                │  │
│  │  ...                                                                │  │
│  │  batch_config.json (configuración usada)                            │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                  OUTPUT: target_images/faceswapped/                  │  │
│  ├──────────────────────────────────────────────────────────────────────┤  │
│  │  faceswapped_foto1.jpg (cara detectada y reemplazada)               │  │
│  │  faceswapped_foto2.jpg                                              │  │
│  │  ...                                                                │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Flujo de Ejecución: Feature 2 (Prompts → Imágenes + Face Swap)

```
START
  ↓
run_batch_processing.py
  ├─ setup_interactive()
  │   ├─ Pregunta prompts_file
  │   ├─ Pregunta face_model_image
  │   ├─ Pregunta steps, cfg_scale, sampler
  │   ├─ Validar archivos
  │   └─ Crear batch_processor.BatchProcessor
  │
  ├─ generate_images()
  │   ├─ processor.read_prompts()
  │   │   └─ Retorna: ["prompt1", "prompt2", ...]
  │   │
  │   ├─ processor.get_generation_tasks()
  │   │   └─ Para cada prompt:
  │   │       ├─ Crear AsyncTask
  │   │       ├─ Setear enable_face_swap = True
  │   │       ├─ Setear use_image_prompt = True
  │   │       ├─ Setear face_swap_image = face_model.jpg
  │   │       └─ Agregar a lista de tareas
  │   │
  │   ├─ Enviar tareas a async_worker (Fooocus)
  │   │
  │   └─ async_worker.worker() para cada tarea:
  │       ├─ Cargar modelos
  │       ├─ Encode prompts (CLIP)
  │       ├─ Crear latentes iniciales
  │       ├─ Diffusion loop (base model)
  │       ├─ Refiner stage (opcional)
  │       ├─ VAE decode → imagen
  │       ├─ Salvar en batch_outputs/batch_NNN_generated.png
  │       │
  │       └─ Si enable_face_swap:
  │           ├─ FaceSwapPostProcessor
  │           ├─ Detectar caras en imagen generada
  │           ├─ Swap con face_model.jpg
  │           └─ Salvar batch_outputs/batch_NNN_generated_faceswapped.png
  │
  ├─ process_targets_faceswap()
  │   └─ Para cada imagen en target_images/:
  │       ├─ FaceDetector.detect_faces()
  │       ├─ FaceDetector.swap_faces()
  │       └─ Salvar en target_images/faceswapped/
  │
  ├─ summary()
  │   └─ Mostrar resultados y próximos pasos
  │
  └─ END
```

---

## Integración con async_worker.py (Futura)

```python
# En modules/async_worker.py

async def process_task(task: AsyncTask):
    """Procesa una tarea de generación/face swap"""

    # 1. GENERACIÓN (ya existe)
    generated_image = generate_image(task)

    # 2. FACE SWAP (NUEVO)
    if task.enable_face_swap:
        from modules.face_processor import FaceSwapPostProcessor

        swapper = FaceSwapPostProcessor(task.face_swap_image)
        swapper.process_generated_image(
            generated_image_path,
            output_path
        )

    return output_image
```

---

## Dependencias entre Módulos

```
run_batch_processing.py
    ├─→ modules/batch_processor.py
    │   ├─→ modules/config.py (config paths)
    │   └─→ modules/util.py (file utilities)
    │
    └─→ modules/face_processor.py
        ├─→ insightface (externo)
        ├─→ cv2/PIL (image processing)
        └─→ onnxruntime (externo)

async_worker.py (modificación futura)
    └─→ modules/face_processor.py
        (para post-processing de imágenes)

webui.py (integración futura)
    ├─→ modules/batch_processor.py
    └─→ modules/face_processor.py
```

---

## Flujo de Datos: BatchProcessorConfig

```
BatchProcessorConfig
    ├─ Rutas:
    │   ├─ prompts_file: "prompts.txt"
    │   ├─ face_model_image: "face_model.jpg"
    │   ├─ target_images_folder: "target_images"
    │   └─ batch_output_folder: "batch_outputs"
    │
    ├─ Face Swap:
    │   ├─ enable_face_swap: bool
    │   └─ face_swap_strength: float [0.0, 1.0]
    │
    ├─ Image Prompt (IP-Adapter):
    │   ├─ use_image_prompt: bool
    │   └─ image_prompt_strength: float [0.0, 1.0]
    │
    └─ Generación:
        ├─ aspect_ratio: str
        ├─ steps: int
        ├─ cfg_scale: float
        ├─ sampler: str
        ├─ scheduler: str
        └─ seed: int

    → Convertido a AsyncTask para async_worker
    → Guardado en batch_config.json para reproducibilidad
```

---

## Transformación de Datos: Prompt → Imagen + Face Swap

```
prompts.txt
    ↓
[
    "a girl in office, professional, 8k",
    "a girl on beach, sunset, 8k",
    ...
]
    ↓
BatchProcessor.get_generation_tasks()
    ↓
[
    AsyncTask(prompt="a girl in office...", enable_face_swap=True, ...),
    AsyncTask(prompt="a girl on beach...", enable_face_swap=True, ...),
    ...
]
    ↓
async_worker.worker() itera cada tarea
    ↓
default_pipeline.process_diffusion()
    ├─ CLIP encode prompt
    ├─ Latent initialization
    ├─ Diffusion steps
    ├─ VAE decode
    └─ Imagen generada
    ↓
FaceSwapPostProcessor.process_generated_image()
    ├─ FaceDetector.detect_faces() en imagen generada
    ├─ FaceDetector.swap_faces() con face_model.jpg
    └─ FaceSwapPostProcessor.save_result()
    ↓
batch_outputs/batch_001_generated_faceswapped.png
```

---

## Arquitectura de InsightFace Integration

```
FaceDetector (Lazy Loading)
    │
    ├─ _lazy_load()
    │   ├─ import insightface
    │   ├─ FaceAnalysis (GPU/CPU)
    │   ├─ get_model('inswapper_128.onnx')
    │   └─ Almacenado en self.detector, self.face_swapper
    │
    ├─ detect_faces(image_path)
    │   ├─ cv2.imread()
    │   ├─ self.detector.get(img) → [Face, Face, ...]
    │   └─ Retorna: [{'bbox': [x1,y1,x2,y2], 'face_data': ...}, ...]
    │
    └─ swap_faces(target_img_path, source_img_path, indices)
        ├─ cv2.imread(target), cv2.imread(source)
        ├─ detect_faces() en ambas
        ├─ self.face_swapper.get(target, face1, face2, paste_back=True)
        └─ Retorna: imagen procesada (numpy array)

FaceSwapPostProcessor
    │
    ├─ __init__(face_model_image: str)
    │   └─ self.detector = FaceDetector()
    │
    ├─ process_generated_image(img_path) → bool
    │   └─ Aplica face swap a imagen individual
    │
    └─ process_batch(images_folder, output_folder)
        └─ Itera carpeta, aplica swap a cada imagen
```

---

## Memoria y Performance

```
MEMORIA (por imagen):
    Generación SDXL:
        ├─ Base Model (UNet): 3-4 GB
        ├─ CLIP encoders: 1-2 GB
        ├─ VAE: 0.5-1 GB
        └─ Latentes/tensores: 1-2 GB
        └─ TOTAL: ~6-9 GB en pico

    Face Swap:
        ├─ InsightFace model: ~200 MB
        ├─ Buffers: ~500 MB
        └─ TOTAL: ~700 MB

    TOTAL PEAK VRAM: 6.7-9.7 GB


TIME (por imagen):
    Generación SDXL:
        ├─ Model loading: 2-5s
        ├─ CLIP encoding: 1-2s
        ├─ Diffusion (20 steps): 20-30s
        ├─ VAE decode: 3-5s
        └─ TOTAL: 26-42s

    Face Swap:
        ├─ Face detection: 0.2-0.5s
        ├─ Face swap: 5-10s
        └─ TOTAL: 5.2-10.5s

    PER IMAGEN (con face swap): 31-52s
    BATCH 10 IMÁGENES: ~5-8 minutos
```

---

## Comparativa: Antes (Manual) vs Después (Automatizado)

```
┌─────────────────────────────────────────────────────────────────┐
│                    ANTES (Manual)                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│ User → Fooocus UI → Click Generate → Esperar → Descargar       │
│  ↓                                                              │
│ Photoshop/Software Face Swap → Manual Face Swap → Guardar      │
│  ↓                                                              │
│ Repetir 10 veces...                                            │
│                                                                  │
│ ⏱️ TIEMPO: ~5 min/imagen × 10 = 50 minutos                     │
│ 😞 TEDIOSA: Mucho click y espera                               │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                 DESPUÉS (Automatizado)                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│ Crear prompts.txt + face_model.jpg                             │
│  ↓                                                              │
│ python run_batch_processing.py                                 │
│  ├─ Crea tareas (automático)                                   │
│  ├─ Genera imágenes (paralelo con Fooocus)                     │
│  ├─ Face swap (automático post-gen)                            │
│  ├─ Detecta caras en targets (automático)                      │
│  └─ Procesa face swap targets (automático)                     │
│  ↓                                                              │
│ batch_outputs/ + target_images/faceswapped/ (¡Listo!)         │
│                                                                  │
│ ⏱️ TIEMPO: ~2 min config + 5-10 min generación = 7-12 min      │
│ 😊 AUTOMÁTICA: Setup y a esperar                               │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

MEJORA: 75-80% más rápido, 100% automatizado
```

---

## Punto de Extensión Futuro: Plugin System

```
plugins/
├── batch_processing_plugin.py
│   └── BatchProcessingPlugin
│       ├── get_ui_components()
│       ├── on_generate()
│       ├── on_image_generated()
│       └── register_plugin()
│
├── face_swap_plugin.py
│   └── FaceSwapPlugin
│       └── ...
│
└── __init__.py
    └── register_all_plugins()

webui.py
    ├─ Carga plugins automáticamente
    ├─ Injeta UI components
    ├─ Registra event hooks
    └─ Permite extensiones sin tocar core
```

---

## Conclusión: Arquitectura Limpia y Extensible

✅ **Separación de responsabilidades:**
- Batch processor: Orquestación de tareas
- Face processor: Detección y swap
- Fooocus core: Generación de imágenes
- CLI: Interfaz de usuario

✅ **Extensible:**
- Fácil agregar nuevos modos (batch segmentation, estilo transfer, etc.)
- Plugin system para futuras extensiones
- Configuración JSON para reproducibilidad

✅ **Performante:**
- Lazy loading de modelos
- Batch processing eficiente
- GPU/CPU automático

✅ **User-Friendly:**
- CLI interactivo
- Documentación clara
- Ejemplos listos para copiar-pegar
