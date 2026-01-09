#!/usr/bin/env python3
"""
Script completo para:
1. Leer prompts desde TXT
2. Generar imágenes
3. Aplicar face swap automático
4. Procesar imágenes target

Uso:
    python run_batch_processing.py
"""

import os
import sys
import asyncio
from pathlib import Path
from typing import Optional

# Agregar módulos a path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modules.batch_processor import BatchProcessor, BatchProcessorConfig
from modules.face_processor import FaceSwapPostProcessor


class BatchProcessingPipeline:
    """Pipeline completo de batch processing"""

    def __init__(self, interactive: bool = True):
        self.interactive = interactive
        self.config = BatchProcessorConfig()

    def setup_interactive(self):
        """Configuración interactiva"""
        print("\n" + "="*60)
        print("BATCH PROCESSING PARA AVATAR DIGITAL")
        print("="*60)

        # Preguntar sobre archivos
        prompts_file = input("\n📝 Archivo de prompts [prompts.txt]: ").strip()
        if prompts_file:
            self.config.prompts_file = prompts_file

        face_model = input("\n😊 Imagen de cara del modelo [face_model.jpg]: ").strip()
        if face_model:
            self.config.face_model_image = face_model

        # Validar que existan
        if not os.path.exists(self.config.prompts_file):
            print(f"\n⚠️  No encontrado: {self.config.prompts_file}")
            print("   Creando archivo de ejemplo...")
            processor = BatchProcessor(self.config)
            processor._create_example_prompts_file()

        if not os.path.exists(self.config.face_model_image):
            print(f"\n⚠️  No encontrado: {self.config.face_model_image}")
            print("   Por favor, sube la imagen de cara del modelo")
            response = input("   ¿Continuar sin face swap? (s/n): ").strip().lower()
            if response != 's':
                sys.exit(1)
            self.config.enable_face_swap = False

        # Opciones de generación
        print("\n⚙️  OPCIONES DE GENERACIÓN:")
        steps = input("   Pasos de difusión [20]: ").strip()
        if steps:
            self.config.steps = int(steps)

        cfg_scale = input("   CFG Scale [4.0]: ").strip()
        if cfg_scale:
            self.config.cfg_scale = float(cfg_scale)

        use_ip_adapter = input("\n   Usar Image Prompt (IP-Adapter)? [s/n]: ").strip().lower()
        self.config.use_image_prompt = use_ip_adapter != 'n'

        if self.config.use_image_prompt:
            ip_strength = input("   Fuerza Image Prompt [0.5]: ").strip()
            if ip_strength:
                self.config.image_prompt_strength = float(ip_strength)

        face_swap_enabled = input("\n   Aplicar Face Swap? [s/n]: ").strip().lower()
        self.config.enable_face_swap = face_swap_enabled != 'n'

    def generate_images(self) -> int:
        """
        Genera imágenes desde prompts

        Retorna número de tareas creadas
        """
        print("\n" + "="*60)
        print("PASO 1: PREPARANDO TAREAS DE GENERACIÓN")
        print("="*60 + "\n")

        processor = BatchProcessor(self.config)
        tasks = processor.get_generation_tasks()

        if not tasks:
            print("❌ No se encontraron prompts")
            return 0

        print(f"✓ {len(tasks)} tareas preparadas:\n")
        for i, task in enumerate(tasks, 1):
            print(f"  {i}. {task['prompt'][:70]}")

        print(f"\n📊 Configuración:")
        print(f"   - Pasos: {self.config.steps}")
        print(f"   - CFG Scale: {self.config.cfg_scale}")
        print(f"   - Image Prompt: {self.config.use_image_prompt}")
        print(f"   - Face Swap: {self.config.enable_face_swap}")

        # Guardar configuración
        processor.save_config_file()

        return len(tasks)

    def process_targets_faceswap(self) -> bool:
        """
        Procesa imágenes target con face swap

        Retorna True si hay imágenes procesadas
        """
        if not os.path.exists(self.config.target_images_folder):
            print(f"\n⚠️  Carpeta no encontrada: {self.config.target_images_folder}")
            return False

        image_files = [f for f in os.listdir(self.config.target_images_folder)
                      if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))]

        if not image_files:
            print(f"\n⚠️  No hay imágenes en: {self.config.target_images_folder}")
            return False

        print("\n" + "="*60)
        print("PASO 2: FACE SWAP EN IMÁGENES TARGET")
        print("="*60 + "\n")

        print(f"Encontradas {len(image_files)} imágenes:\n")
        for i, img_file in enumerate(image_files, 1):
            print(f"  {i}. {img_file}")

        processor = FaceSwapPostProcessor(self.config.face_model_image)
        target_output = os.path.join(self.config.target_images_folder, "faceswapped")

        processor.process_batch(
            images_folder=self.config.target_images_folder,
            output_folder=target_output
        )

        return True

    def summary(self, num_generation_tasks: int):
        """Imprime resumen final"""
        print("\n" + "="*60)
        print("✅ CONFIGURACIÓN COMPLETADA")
        print("="*60 + "\n")

        print("📋 RESUMEN:")
        print(f"  • Prompts para generar: {num_generation_tasks}")
        print(f"  • Salida: {self.config.batch_output_folder}")
        print(f"  • Face Swap: {'HABILITADO' if self.config.enable_face_swap else 'DESHABILITADO'}")
        print(f"  • Image Prompt: {'HABILITADO' if self.config.use_image_prompt else 'DESHABILITADO'}")

        print("\n📖 PRÓXIMOS PASOS:")
        print("  1. Las tareas de generación se ejecutarán en Fooocus")
        print("  2. Las imágenes se guardarán en batch_outputs/")
        print("  3. Face swap se aplicará automáticamente (si está habilitado)")
        print("  4. Verifica resultados en batch_outputs/")

        print("\n💡 CONSEJOS:")
        print("  • Mantén Fooocus ejecutándose en otra ventana")
        print("  • Aumenta steps (20-25) para mejor calidad")
        print("  • Ajusta image_prompt_strength (0.3-0.7) para variar pose")
        print("  • Usa diferentes samplers para variar resultados")

        print("\n" + "="*60)

    def run(self):
        """Ejecuta el pipeline completo"""
        try:
            if self.interactive:
                self.setup_interactive()

            # Generar imágenes
            num_tasks = self.generate_images()

            if num_tasks == 0:
                print("❌ No se pudieron crear tareas")
                return False

            # Procesar targets
            self.process_targets_faceswap()

            # Resumen
            self.summary(num_tasks)

            return True

        except KeyboardInterrupt:
            print("\n\n⏹️  Cancelado por usuario")
            return False
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()
            return False


def main():
    """Punto de entrada"""
    import argparse

    parser = argparse.ArgumentParser(
        description='Batch Processing para Avatar Digital en Fooocus'
    )
    parser.add_argument('--no-interactive', action='store_true',
                       help='Usar configuración por defecto (no interactivo)')
    parser.add_argument('--prompts', default='prompts.txt',
                       help='Archivo de prompts')
    parser.add_argument('--face', default='face_model.jpg',
                       help='Imagen de cara del modelo')
    parser.add_argument('--output', default='batch_outputs',
                       help='Carpeta de salida')

    args = parser.parse_args()

    # Crear pipeline
    pipeline = BatchProcessingPipeline(interactive=not args.no_interactive)

    # Configuración manual
    if args.no_interactive:
        pipeline.config.prompts_file = args.prompts
        pipeline.config.face_model_image = args.face
        pipeline.config.batch_output_folder = args.output

    # Ejecutar
    success = pipeline.run()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
