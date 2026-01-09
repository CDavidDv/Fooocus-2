"""
Optimized Fooocus launcher for Google Colab
Auto-downloads checkpoints and optimizes for Colab environment
"""

import os
import subprocess
import sys

# Detectar si estamos en Colab
IS_COLAB = 'google.colab' in sys.modules

if IS_COLAB:
    print("[COLAB] Detectado entorno Google Colab")
    from google.colab import files

    # Instalar PyTorch optimizado para Colab
    print("[COLAB] Instalando PyTorch y dependencias...")
    subprocess.run([
        sys.executable, "-m", "pip", "install",
        "torch==2.1.0", "torchvision==0.16.0", "torchaudio==2.1.0",
        "xformers==0.0.23",
        "-q"
    ], check=True)

    # Usar más VRAM en Colab
    os.environ['PYTORCH_CUDA_ALLOC_CONF'] = 'max_split_size_mb=512'
    os.environ['CUDA_VISIBLE_DEVICES'] = '0'

def setup_colab_environment():
    """Configura el entorno específico de Colab"""
    if not IS_COLAB:
        return

    print("[COLAB] Montando Google Drive...")
    from google.colab import drive
    drive.mount('/content/drive')

    # Crear directorios en Drive para persistencia
    models_dir = '/content/drive/MyDrive/fooocus_models'
    outputs_dir = '/content/drive/MyDrive/fooocus_outputs'

    os.makedirs(models_dir, exist_ok=True)
    os.makedirs(outputs_dir, exist_ok=True)

    print(f"[COLAB] Modelos guardados en: {models_dir}")
    print(f"[COLAB] Salidas guardadas en: {outputs_dir}")

    return models_dir, outputs_dir

def main():
    # Setup Colab si es necesario
    if IS_COLAB:
        models_dir, outputs_dir = setup_colab_environment()

        # Comando para ejecutar Fooocus con preset colab
        cmd = [
            sys.executable,
            "entry_with_update.py",
            "--preset", "colab",  # Usar el preset que creamos
            "--listen",           # Escuchar en la red
            "--share",            # Crear enlace gradio.live
            "--always-high-vram", # Máximo VRAM (Colab tiene mucho)
        ]

        # Agregar rutas personalizadas si se desea
        # cmd.extend([
        #     "--external-working-path", models_dir,
        #     "--output-path", outputs_dir
        # ])
    else:
        # Ejecución normal en local
        cmd = [
            sys.executable,
            "entry_with_update.py",
            "--preset", "colab"
        ]

    print(f"[INFO] Ejecutando: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)

if __name__ == "__main__":
    main()
