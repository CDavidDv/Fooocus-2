# Integración de Batch Processing en webui.py

Este archivo muestra cómo integrar las 3 características en la UI de Fooocus.

---

## Opción 1: Nueva Pestaña en webui.py (Recomendado)

Agregar en `webui.py` después de las otras pestañas:

```python
# ============= BATCH PROCESSING TAB =============
with gr.Tab("Batch Processing"):
    with gr.Column():
        gr.Markdown("### 🎨 Procesa múltiples prompts y aplica face swap automático")

        with gr.Row():
            batch_enabled = gr.Checkbox(
                label="Habilitar Batch Processing",
                value=False,
                info="Procesar múltiples prompts desde archivo"
            )
            batch_generate_btn = gr.Button("Procesar Batch", variant="primary")

        gr.Markdown("#### 📝 Prompts")
        batch_prompts_file = gr.File(
            label="Archivo de prompts (TXT)",
            file_types=["text"],
            type="filepath"
        )
        batch_prompts_preview = gr.Textbox(
            label="Vista previa de prompts",
            lines=5,
            interactive=False
        )

        gr.Markdown("#### 😊 Imagen de Cara (Modelo Digital)")
        batch_face_image = gr.Image(
            label="Cara del modelo para inyectar",
            type="filepath"
        )

        with gr.Row():
            batch_enable_face_swap = gr.Checkbox(
                label="Habilitar Face Swap",
                value=True
            )
            batch_face_swap_strength = gr.Slider(
                label="Fuerza Face Swap",
                minimum=0.0,
                maximum=1.0,
                step=0.1,
                value=1.0
            )

        with gr.Row():
            batch_use_ip_adapter = gr.Checkbox(
                label="Usar Image Prompt (IP-Adapter)",
                value=True,
                info="Usar cara como referencia visual"
            )
            batch_ip_strength = gr.Slider(
                label="Fuerza Image Prompt",
                minimum=0.0,
                maximum=1.0,
                step=0.1,
                value=0.5,
                visible=True
            )

        gr.Markdown("#### 📁 Imágenes Target (Para Face Swap)")
        batch_target_folder = gr.Textbox(
            label="Carpeta con imágenes (target_images/)",
            value="target_images",
            info="Inyectar cara en imágenes existentes"
        )

        batch_output_folder = gr.Textbox(
            label="Carpeta de salida",
            value="batch_outputs",
            info="Donde guardar los resultados"
        )

        gr.Markdown("#### ⚙️ Configuración de Generación")
        with gr.Row():
            batch_steps = gr.Slider(
                label="Pasos",
                minimum=15,
                maximum=40,
                step=1,
                value=20
            )
            batch_cfg = gr.Slider(
                label="CFG Scale",
                minimum=2.0,
                maximum=10.0,
                step=0.5,
                value=4.0
            )

        batch_progress = gr.Textbox(
            label="Progreso",
            interactive=False,
            lines=5
        )

        batch_output_gallery = gr.Gallery(
            label="Resultados",
            columns=2,
            rows=2
        )


# ============= EVENT HANDLERS =============
def on_batch_generate_clicked(
    prompts_file,
    face_image,
    enable_face_swap,
    use_ip_adapter,
    steps,
    cfg_scale,
    face_swap_strength,
    ip_adapter_strength,
    target_folder,
    output_folder
):
    """Handler para generar batch"""
    from modules.batch_processor import BatchProcessor, BatchProcessorConfig
    from modules.face_processor import FaceSwapPostProcessor

    try:
        # Crear configuración
        config = BatchProcessorConfig()
        config.enable_face_swap = enable_face_swap
        config.use_image_prompt = use_ip_adapter
        config.face_swap_strength = face_swap_strength
        config.image_prompt_strength = ip_adapter_strength
        config.steps = int(steps)
        config.cfg_scale = cfg_scale
        config.batch_output_folder = output_folder
        config.target_images_folder = target_folder

        # Guardar archivos subidos
        if prompts_file:
            import shutil
            shutil.copy(prompts_file, config.prompts_file)

        if face_image:
            import shutil
            shutil.copy(face_image, config.face_model_image)

        # Crear processor
        processor = BatchProcessor(config)

        # Obtener tareas
        tasks = processor.get_generation_tasks()

        progress_text = f"✓ {len(tasks)} tareas preparadas\n"
        progress_text += f"Salida: {output_folder}\n"
        progress_text += f"Face Swap: {'HABILITADO' if enable_face_swap else 'DESHABILITADO'}\n"
        progress_text += f"Image Prompt: {'HABILITADO' if use_ip_adapter else 'DESHABILITADO'}\n"
        progress_text += "\nLas tareas se enviarán a la cola de generación..."

        return progress_text, [], ""

    except Exception as e:
        return f"❌ Error: {str(e)}", [], ""


# Conectar eventos
batch_generate_btn.click(
    fn=on_batch_generate_clicked,
    inputs=[
        batch_prompts_file,
        batch_face_image,
        batch_enable_face_swap,
        batch_use_ip_adapter,
        batch_steps,
        batch_cfg,
        batch_face_swap_strength,
        batch_ip_strength,
        batch_target_folder,
        batch_output_folder
    ],
    outputs=[
        batch_progress,
        batch_output_gallery,
        batch_prompts_preview
    ]
)

# Actualizar preview de prompts
def update_prompts_preview(prompts_file):
    if not prompts_file:
        return ""
    try:
        with open(prompts_file, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f.readlines() if line.strip() and not line.startswith('#')]
        return "\n".join(lines[:10])  # Mostrar primeros 10
    except:
        return "Error leyendo archivo"

batch_prompts_file.change(
    fn=update_prompts_preview,
    inputs=[batch_prompts_file],
    outputs=[batch_prompts_preview]
)
```

---

## Opción 2: Panel Lateral (Más Compacto)

Agregar en la UI principal un acordeón o panel lateral:

```python
with gr.Accordion("🎨 Batch Processing", open=False):
    # [Mismo contenido que arriba pero compacto]
    gr.Markdown("### Procesar múltiples prompts")

    batch_mode = gr.Radio(
        choices=["Generación", "Face Swap Target", "Ambos"],
        value="Generación",
        label="Modo"
    )

    batch_prompts = gr.File(label="Prompts (TXT)")
    batch_face = gr.Image(label="Cara del modelo")

    batch_go = gr.Button("Procesar", variant="primary")
```

---

## Opción 3: API REST (Para Integración Externa)

Crear archivo `api_batch_processing.py`:

```python
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import FileResponse
import asyncio
from modules.batch_processor import BatchProcessor, BatchProcessorConfig

app = FastAPI(title="Fooocus Batch API")

@app.post("/batch/generate")
async def batch_generate(
    prompts: UploadFile = File(...),
    face_image: UploadFile = File(...),
    steps: int = 20,
    cfg_scale: float = 4.0,
    enable_face_swap: bool = True
):
    """Generar batch de imágenes"""

    # Guardar archivos subidos
    prompts_path = f"temp_prompts_{prompts.filename}"
    face_path = f"temp_face_{face_image.filename}"

    with open(prompts_path, 'wb') as f:
        f.write(await prompts.read())
    with open(face_path, 'wb') as f:
        f.write(await face_image.read())

    # Crear config
    config = BatchProcessorConfig()
    config.prompts_file = prompts_path
    config.face_model_image = face_path
    config.steps = steps
    config.cfg_scale = cfg_scale
    config.enable_face_swap = enable_face_swap

    # Procesar
    processor = BatchProcessor(config)
    tasks = processor.get_generation_tasks()

    return {
        "status": "ok",
        "tasks_created": len(tasks),
        "output_folder": config.batch_output_folder
    }

@app.post("/batch/faceswap")
async def batch_faceswap(
    images_folder: str = Form(...),
    face_image: UploadFile = File(...)
):
    """Face swap batch"""

    face_path = f"temp_face_{face_image.filename}"
    with open(face_path, 'wb') as f:
        f.write(await face_image.read())

    from modules.face_processor import FaceSwapPostProcessor
    processor = FaceSwapPostProcessor(face_path)
    processor.process_batch(images_folder, f"{images_folder}_faceswapped")

    return {"status": "ok", "output_folder": f"{images_folder}_faceswapped"}
```

Uso con curl:
```bash
curl -X POST "http://localhost:8000/batch/generate" \
  -F "prompts=@prompts.txt" \
  -F "face_image=@face_model.jpg" \
  -F "steps=20"
```

---

## Opción 4: Plugin/Extension System

Crear archivo `plugins/batch_processing_plugin.py`:

```python
"""Plugin de Batch Processing para Fooocus"""

class BatchProcessingPlugin:
    """Plugin que agrega Batch Processing a Fooocus"""

    def __init__(self):
        self.name = "Batch Processing"
        self.version = "1.0.0"
        self.description = "Procesa múltiples prompts y aplica face swap"

    def get_ui_components(self):
        """Retorna componentes para la UI"""
        return {
            'tab_name': 'Batch Processing',
            'components': [
                # Lista de componentes UI
            ]
        }

    def on_generate(self, batch_config):
        """Hook ejecutado al generar"""
        from modules.batch_processor import BatchProcessor
        processor = BatchProcessor(batch_config)
        return processor.get_generation_tasks()

    def on_image_generated(self, image_path, task_config):
        """Hook ejecutado después de generar imagen"""
        if task_config.get('enable_face_swap'):
            from modules.face_processor import FaceSwapPostProcessor
            processor = FaceSwapPostProcessor(task_config['face_model_image'])
            processor.process_generated_image(image_path)

# Registrar plugin
def register_plugin():
    return BatchProcessingPlugin()
```

---

## Flujo de Integración Recomendado

```
Usuario
    ↓
Selecciona Tab "Batch Processing"
    ↓
Sube prompts.txt y face_model.jpg
    ↓
Click "Procesar"
    ↓
Crea tareas en async_worker
    ↓
async_worker.worker() itera tareas
    ↓
Por cada tarea:
    - Genera imagen
    - Si enable_face_swap: aplica FaceSwapPostProcessor
    - Guarda en batch_outputs/
    ↓
UI actualiza galería
    ↓
Usuario descarga resultados
```

---

## Variables de Configuración Global

Agregar en `config.py`:

```python
# Batch Processing
batch_processing_enabled = True
batch_default_output_folder = 'batch_outputs'
batch_default_target_folder = 'target_images'
batch_auto_faceswap = True
batch_preserve_originals = True
```

---

## Testing de Integración

```python
# test_batch_webui_integration.py

import gradio as gr
from modules.batch_processor import BatchProcessor, BatchProcessorConfig

def test_batch_ui():
    """Test de componentes UI de batch"""

    with gr.Blocks() as demo:
        gr.Markdown("### Test Batch Processing UI")

        # Agregar componentes aquí
        prompts_file = gr.File(label="Prompts")
        face_image = gr.Image(label="Cara")
        btn = gr.Button("Test")
        output = gr.Textbox()

        def test_fn(prompts, face):
            config = BatchProcessorConfig()
            processor = BatchProcessor(config)
            tasks = processor.get_generation_tasks()
            return f"✓ {len(tasks)} tareas"

        btn.click(test_fn, [prompts_file, face_image], output)

    demo.launch()

if __name__ == "__main__":
    test_batch_ui()
```

---

## Recomendación Final

**Mejor opción para Fooocus:** Opción 1 (Nueva Pestaña)

**Razones:**
- ✅ Consistente con UI actual (basada en tabs)
- ✅ Fácil de mantener
- ✅ Accesible para usuarios
- ✅ No requiere cambios profundos en arquitectura
- ✅ Puedes agregar más tabs en el futuro

**Pasos para implementar:**
1. Copiar código de la Opción 1 a `webui.py`
2. Importar `BatchProcessor` y `FaceSwapPostProcessor`
3. Conectar eventos (`click`, `change`, etc.)
4. Probar y ajustar UI
