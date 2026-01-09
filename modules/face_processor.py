"""
Face Processor: Detección de caras y reemplazo automático

Características:
1. Detectar caras en imágenes usando InsightFace
2. Hacer face swap (reemplazar cara detectada con otra imagen)
3. Integración con async_worker para aplicar face swap post-generación
"""

import os
import cv2
import numpy as np
from typing import List, Tuple, Optional
from PIL import Image


class FaceDetector:
    """Detecta caras en imágenes usando InsightFace"""

    def __init__(self):
        self.detector = None
        self.face_swapper = None
        self._lazy_load()

    def _lazy_load(self):
        """Carga InsightFace de forma perezosa"""
        try:
            import insightface
            # Detector
            self.detector = insightface.app.FaceAnalysis(providers=['CUDAExecutionProvider', 'CPUExecutionProvider'])
            self.detector.prepare(ctx_id=0, det_size=(640, 640))

            # Face Swapper
            from insightface.model_zoo import get_model
            self.face_swapper = get_model('inswapper_128.onnx', providers=['CUDAExecutionProvider', 'CPUExecutionProvider'])

            print("[FACE] ✓ InsightFace cargado exitosamente")
        except ImportError:
            print("[FACE] ⚠️ InsightFace no instalado. Instalar con:")
            print("       pip install insightface onnxruntime-gpu")
            self.detector = None
            self.face_swapper = None

    def is_available(self) -> bool:
        """Verifica si InsightFace está disponible"""
        return self.detector is not None and self.face_swapper is not None

    def detect_faces(self, image_path: str) -> List[dict]:
        """
        Detecta caras en una imagen

        Args:
            image_path: Ruta a la imagen

        Returns:
            Lista de detectores encontrados con bounding box y landmarks
        """
        if not self.is_available():
            print("[FACE] ⚠️ Face detection no disponible")
            return []

        try:
            img = cv2.imread(image_path)
            if img is None:
                print(f"[FACE] ✗ No se pudo cargar imagen: {image_path}")
                return []

            faces = self.detector.get(img)
            print(f"[FACE] ✓ Detectadas {len(faces)} caras en {os.path.basename(image_path)}")

            return [
                {
                    'face_data': face,
                    'bbox': face.bbox,  # [x1, y1, x2, y2]
                    'landmarks': face.landmark_2d_106 if hasattr(face, 'landmark_2d_106') else None,
                    'confidence': face.det_score
                }
                for face in faces
            ]
        except Exception as e:
            print(f"[FACE] ✗ Error detectando caras: {e}")
            return []

    def swap_faces(self,
                   target_image_path: str,
                   source_image_path: str,
                   target_face_idx: int = 0,
                   source_face_idx: int = 0) -> Optional[np.ndarray]:
        """
        Hace face swap (reemplaza cara en target_image con cara de source_image)

        Args:
            target_image_path: Imagen donde cambiar la cara
            source_image_path: Imagen de donde sacar la cara
            target_face_idx: Índice de cara en target (si hay múltiples)
            source_face_idx: Índice de cara en source (si hay múltiples)

        Returns:
            Imagen procesada (numpy array) o None si falló
        """
        if not self.is_available():
            print("[FACE] ⚠️ Face swap no disponible")
            return None

        try:
            # Cargar imágenes
            target_img = cv2.imread(target_image_path)
            source_img = cv2.imread(source_image_path)

            if target_img is None or source_img is None:
                print("[FACE] ✗ No se pudieron cargar imágenes")
                return None

            # Detectar caras
            target_faces = self.detector.get(target_img)
            source_faces = self.detector.get(source_img)

            if not target_faces:
                print("[FACE] ⚠️ No se encontró cara en imagen target")
                return None

            if not source_faces:
                print("[FACE] ⚠️ No se encontró cara en imagen source")
                return None

            # Validar índices
            if target_face_idx >= len(target_faces):
                target_face_idx = 0
            if source_face_idx >= len(source_faces):
                source_face_idx = 0

            # Hacer swap
            result = self.face_swapper.get(target_img, target_faces[target_face_idx], source_faces[source_face_idx], paste_back=True)

            print(f"[FACE] ✓ Face swap completado")
            return result

        except Exception as e:
            print(f"[FACE] ✗ Error en face swap: {e}")
            return None

    def save_result(self, image_array: np.ndarray, output_path: str):
        """Guarda imagen procesada"""
        try:
            cv2.imwrite(output_path, image_array)
            print(f"[FACE] ✓ Guardado en: {output_path}")
        except Exception as e:
            print(f"[FACE] ✗ Error guardando imagen: {e}")


class FaceSwapPostProcessor:
    """
    Post-procesador que aplica face swap automático a imágenes generadas

    Se usa después de generar imágenes para inyectar caras del modelo
    """

    def __init__(self, face_model_image: str):
        """
        Args:
            face_model_image: Ruta a imagen de cara del modelo digital
        """
        self.face_model_image = face_model_image
        self.detector = FaceDetector()

    def process_generated_image(self,
                               generated_image_path: str,
                               output_path: Optional[str] = None) -> bool:
        """
        Aplica face swap a imagen generada

        Args:
            generated_image_path: Imagen recién generada
            output_path: Donde guardar resultado (default: overwrite)

        Returns:
            True si éxito, False si falló
        """
        if output_path is None:
            # Crear nombre de salida con sufijo
            base, ext = os.path.splitext(generated_image_path)
            output_path = f"{base}_faceswapped{ext}"

        result = self.detector.swap_faces(
            target_image_path=generated_image_path,
            source_image_path=self.face_model_image,
            target_face_idx=0,
            source_face_idx=0
        )

        if result is not None:
            self.detector.save_result(result, output_path)
            return True
        return False

    def process_batch(self, images_folder: str, output_folder: str):
        """
        Procesa múltiples imágenes en una carpeta

        Args:
            images_folder: Carpeta con imágenes a procesar
            output_folder: Carpeta de salida
        """
        os.makedirs(output_folder, exist_ok=True)

        image_files = [f for f in os.listdir(images_folder)
                      if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))]

        print(f"[FACE] Procesando {len(image_files)} imágenes...")

        success_count = 0
        for image_file in image_files:
            image_path = os.path.join(images_folder, image_file)
            output_path = os.path.join(output_folder, f"faceswapped_{image_file}")

            if self.process_generated_image(image_path, output_path):
                success_count += 1

        print(f"[FACE] ✓ {success_count}/{len(image_files)} imágenes procesadas")


# Test function
def test_face_processor():
    """Test del módulo"""
    print("[TEST] Iniciando test de Face Processor...")

    # Crear processor
    processor = FaceDetector()

    if not processor.is_available():
        print("[TEST] ⚠️ InsightFace no disponible, test saltado")
        return

    # Test de detección (requiere imagen real)
    test_image = "test_image.jpg"
    if os.path.exists(test_image):
        faces = processor.detect_faces(test_image)
        print(f"[TEST] Detectadas {len(faces)} caras")

    print("[TEST] Test completado")


if __name__ == "__main__":
    test_face_processor()
