"""
Wrapper para compatibilidad Image entre Gradio 3.x y 4.x
"""

import sys

try:
    import gradio
    GRADIO_MAJOR = int(gradio.__version__.split('.')[0])
except:
    GRADIO_MAJOR = 3

# Para Gradio 4.x, usar Image nativa para evitar conflictos de MRO
if GRADIO_MAJOR >= 4:
    # Simplemente importar desde gradio
    from gradio.components import Image
    __all__ = ['Image']
else:
    # Para Gradio 3.x, intentar importar la versión personalizada
    try:
        from gradio_hijack import Image
        __all__ = ['Image']
    except (ImportError, TypeError):
        # Fallback a la versión nativa si hay problemas
        from gradio.components import Image
        __all__ = ['Image']
