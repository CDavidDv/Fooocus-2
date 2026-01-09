"""
Batch Processor: Procesa múltiples prompts desde un archivo TXT
y aplica face swap automáticamente.

Uso:
    - Crear un archivo 'prompts.txt' con un prompt por línea
    - Subir imagen de cara (modelo digital) como 'face_model.jpg'
    - El sistema genera imágenes y las procesa con face swap
"""

import os
import json
from typing import List, Tuple, Optional
from PIL import Image
import numpy as np


class BatchProcessorConfig:
    """Configuración para el procesamiento en lote"""

    def __init__(self):
        # Rutas
        self.prompts_file = "prompts.txt"
        self.face_model_image = "face_model.jpg"  # Imagen de cara a inyectar
        self.target_images_folder = "target_images"  # Carpeta con imágenes donde detectar caras
        self.batch_output_folder = "batch_outputs"

        # Configuración de Face Swap
        self.enable_face_swap = True
        self.face_swap_strength = 1.0  # 0.0-1.0

        # Configuración de Image Prompt (IP-Adapter)
        self.use_image_prompt = True
        self.image_prompt_strength = 0.5  # Control de cuánto influye la imagen

        # Configuración de generación
        self.aspect_ratio = "1152*896"
        self.steps = 20
        self.cfg_scale = 4.0
        self.sampler = "dpmpp_2m_sde_gpu"
        self.seed = -1  # -1 para aleatorio


class BatchProcessor:
    """
    Procesa prompts en lote y aplica face swap.

    Características:
    1. Lee prompts desde archivo TXT
    2. Genera imágenes usando cada prompt
    3. Aplica face swap automáticamente (inyecta cara del modelo)
    4. Detecta caras en imágenes targets y las reemplaza
    5. Guarda todo en batch_outputs/
    """

    def __init__(self, config: Optional[BatchProcessorConfig] = None):
        self.config = config or BatchProcessorConfig()
        self._create_directories()
        self._validate_files()

    def _create_directories(self):
        """Crea directorios necesarios"""
        os.makedirs(self.config.batch_output_folder, exist_ok=True)
        os.makedirs(self.config.target_images_folder, exist_ok=True)

    def _validate_files(self):
        """Valida que existan los archivos necesarios"""
        if not os.path.exists(self.config.prompts_file):
            print(f"[BATCH] ⚠️ No encontrado: {self.config.prompts_file}")
            print(f"[BATCH] Crear archivo con un prompt por línea")
            self._create_example_prompts_file()

        if not os.path.exists(self.config.face_model_image):
            print(f"[BATCH] ⚠️ No encontrado: {self.config.face_model_image}")
            print(f"[BATCH] Subir imagen de cara del modelo digital")

    def _create_example_prompts_file(self):
        """Crea archivo de ejemplo de prompts"""
        example_prompts = """# Ejemplos de prompts para batch processing
# Cada línea es un prompt separado
a beautiful girl, professional portrait, studio lighting, 8k, masterpiece
a girl in a cyberpunk city, neon lights, detailed, 8k
a girl in a forest, fantasy style, magical atmosphere, 8k
a girl in a beach, sunset, summer vibes, 8k
a girl in office, professional wear, natural lighting, 8k
"""
        with open(self.config.prompts_file, 'w', encoding='utf-8') as f:
            f.write(example_prompts)
        print(f"[BATCH] ✓ Creado: {self.config.prompts_file}")

    def read_prompts(self) -> List[str]:
        """Lee prompts desde archivo TXT"""
        if not os.path.exists(self.config.prompts_file):
            return []

        prompts = []
        with open(self.config.prompts_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                # Ignorar comentarios y líneas vacías
                if line and not line.startswith('#'):
                    prompts.append(line)

        print(f"[BATCH] ✓ Leídos {len(prompts)} prompts")
        return prompts

    def get_generation_tasks(self) -> List[dict]:
        """
        Convierte prompts en tareas de generación

        Retorna lista de dicts con parámetros para async_worker.AsyncTask
        """
        prompts = self.read_prompts()
        if not prompts:
            return []

        # Verificar que existe imagen de cara
        if self.config.enable_face_swap and not os.path.exists(self.config.face_model_image):
            print("[BATCH] ⚠️ Face swap habilitado pero no encontrada imagen de cara")

        tasks = []
        for idx, prompt in enumerate(prompts, 1):
            task = {
                'task_id': f"batch_{idx:03d}",
                'prompt': prompt,
                'prompt_negative': '',
                'aspect_ratio': self.config.aspect_ratio,
                'image_number': 1,
                'steps': self.config.steps,
                'cfg_scale': self.config.cfg_scale,
                'sampler_name': self.config.sampler,
                'scheduler_name': 'karras',
                'seed': self.config.seed,

                # Face Swap
                'enable_face_swap': self.config.enable_face_swap,
                'face_swap_image': self.config.face_model_image if self.config.enable_face_swap else None,

                # Image Prompt (IP-Adapter)
                'use_image_prompt': self.config.use_image_prompt,
                'image_prompt_path': self.config.face_model_image if self.config.use_image_prompt else None,
                'image_prompt_strength': self.config.image_prompt_strength,

                # Metadata
                'save_metadata': True,
                'output_format': 'png',
            }
            tasks.append(task)

        print(f"[BATCH] ✓ {len(tasks)} tareas de generación creadas")
        return tasks

    def get_face_swap_tasks(self) -> List[dict]:
        """
        Genera tareas para detectar caras en imágenes y hacer face swap

        Procesa todas las imágenes en target_images_folder
        """
        if not os.path.exists(self.config.target_images_folder):
            print(f"[BATCH] ⚠️ Carpeta no encontrada: {self.config.target_images_folder}")
            return []

        if not os.path.exists(self.config.face_model_image):
            print(f"[BATCH] ⚠️ Imagen de cara no encontrada: {self.config.face_model_image}")
            return []

        tasks = []
        image_files = [f for f in os.listdir(self.config.target_images_folder)
                      if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))]

        for idx, image_file in enumerate(image_files, 1):
            task = {
                'task_id': f"faceswap_{idx:03d}",
                'target_image_path': os.path.join(self.config.target_images_folder, image_file),
                'face_model_image': self.config.face_model_image,
                'face_swap_strength': self.config.face_swap_strength,
                'save_output': True,
                'output_prefix': f"faceswapped_{os.path.splitext(image_file)[0]}",
            }
            tasks.append(task)

        print(f"[BATCH] ✓ {len(tasks)} tareas de face swap creadas")
        return tasks

    def save_config_file(self, output_path: Optional[str] = None):
        """Guarda la configuración actual en un JSON"""
        if output_path is None:
            output_path = os.path.join(self.config.batch_output_folder, "batch_config.json")

        config_dict = {
            'prompts_file': self.config.prompts_file,
            'face_model_image': self.config.face_model_image,
            'target_images_folder': self.config.target_images_folder,
            'batch_output_folder': self.config.batch_output_folder,
            'enable_face_swap': self.config.enable_face_swap,
            'face_swap_strength': self.config.face_swap_strength,
            'use_image_prompt': self.config.use_image_prompt,
            'image_prompt_strength': self.config.image_prompt_strength,
            'aspect_ratio': self.config.aspect_ratio,
            'steps': self.config.steps,
            'cfg_scale': self.config.cfg_scale,
            'sampler': self.config.sampler,
            'seed': self.config.seed,
        }

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(config_dict, f, indent=4, ensure_ascii=False)

        print(f"[BATCH] ✓ Config guardada en: {output_path}")


def create_batch_config_ui_fields() -> List[dict]:
    """
    Retorna campos para agregar a webui.py para control de batch processing

    Estos campos aparecerían en una nueva pestaña "Batch Processing"
    """
    return [
        {
            'label': 'Habilitar Batch Processing',
            'component_type': 'checkbox',
            'default': False,
            'key': 'enable_batch_processing',
            'info': 'Procesar múltiples prompts desde archivo'
        },
        {
            'label': 'Archivo de prompts (prompts.txt)',
            'component_type': 'file',
            'key': 'batch_prompts_file',
            'info': 'Archivo TXT con un prompt por línea'
        },
        {
            'label': 'Imagen de cara (modelo digital)',
            'component_type': 'image',
            'key': 'batch_face_model',
            'info': 'Imagen de cara para inyectar en las generaciones'
        },
        {
            'label': 'Habilitar Face Swap',
            'component_type': 'checkbox',
            'default': True,
            'key': 'batch_enable_face_swap',
            'info': 'Inyectar cara del modelo en las imágenes generadas'
        },
        {
            'label': 'Fuerza de Face Swap',
            'component_type': 'slider',
            'minimum': 0.0,
            'maximum': 1.0,
            'step': 0.1,
            'default': 1.0,
            'key': 'batch_face_swap_strength',
        },
        {
            'label': 'Usar Image Prompt (IP-Adapter)',
            'component_type': 'checkbox',
            'default': True,
            'key': 'batch_use_image_prompt',
            'info': 'Usar cara del modelo como referencia visual (IP-Adapter)'
        },
        {
            'label': 'Fuerza Image Prompt',
            'component_type': 'slider',
            'minimum': 0.0,
            'maximum': 1.0,
            'step': 0.1,
            'default': 0.5,
            'key': 'batch_image_prompt_strength',
        },
    ]
