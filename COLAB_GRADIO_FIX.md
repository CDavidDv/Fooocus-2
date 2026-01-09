# 🔧 Solucionar Problema de Gradio en Colab

## El Problema

Ves este error cuando ejecutas en Colab:

```
Version mismatch for gradio: Installed version 3.41.2 does not meet requirement gradio==4.44.1
Installing requirements
...
ModuleNotFoundError: No module named 'modules.gradio_hijack'
```

**Causa:** Gradio 3.41.2 está instalado pero Fooocus necesita 4.44.1, causando conflictos de importación.

---

## ✅ Solución (Elige UNA)

### Opción 1: Reinstalar desde Cero (RECOMENDADO)

```python
# Celda 1: Limpiar completamente
!pip uninstall gradio -y
!pip cache purge
!pip install --force-reinstall gradio==4.44.1
!pip install insightface onnxruntime-gpu

# Celda 2: Clonar repositorio actualizado
!git clone https://github.com/tu-usuario/Fooocus.git
%cd Fooocus

# Celda 3: Ejecutar
!python fooocus_colab_optimized.py
```

**Tiempo:** ~5 min la primera vez | ~30s siguientes veces

---

### Opción 2: Usar Comando Directo (RÁPIDA)

Si ya tienes Fooocus clonado:

```python
# Celda 1: Limpiar Gradio
!pip uninstall gradio -y
!pip install --force-reinstall gradio==4.44.1

# Celda 2: Ejecutar Fooocus directamente
!python entry_with_update.py --preset default --share --listen --always-high-vram
```

---

### Opción 3: Actualizar Repositorio Existente

Si ya tienes Fooocus pero con archivos viejos:

```python
%cd Fooocus

# Actualizar código desde GitHub
!git pull

# Limpiar Gradio
!pip uninstall gradio -y
!pip install --force-reinstall gradio==4.44.1

# Ejecutar con script mejorado
!python fooocus_colab_optimized.py
```

---

## 📊 ¿Qué hace cada paso?

| Paso | Propósito |
|------|-----------|
| `pip uninstall gradio -y` | Elimina Gradio 3.41.2 completamente |
| `pip cache purge` | Limpia caché de pip para evitar conflictos |
| `pip install --force-reinstall gradio==4.44.1` | Instala versión nueva, limpia |
| `git pull` | Obtiene script mejorado de fooocus_colab_optimized.py |

---

## ⚠️ Si Aún Tienes Errores

### Error: "Gradio installation failed"

```python
# Intenta con versión alternativa
!pip install --no-cache-dir --force-reinstall gradio==4.44.0
```

### Error: "ModuleNotFoundError: torch"

```python
# Reinstala PyTorch
!pip install torch==2.1.0 torchvision==0.16.0 torchaudio==2.1.0
```

### Error: "Still seeing old Gradio"

```python
# Reinicia el kernel de Colab
# Runtime → Restart runtime
# Luego ejecuta nuevamente
```

---

## ✨ Verificación Rápida

Para confirmar que Gradio está correctamente instalado:

```python
import gradio as gr
print(f"Gradio version: {gr.__version__}")
# Debería mostrar: Gradio version: 4.44.1
```

---

## 🚀 Una Vez Resuelto

Verás este output limpio:

```
[COLAB] Detectado entorno Google Colab
[COLAB] Montando Google Drive...
[COLAB] Instalando PyTorch y dependencias...
[COLAB] Limpiando Gradio viejo (3.41.2)...
[COLAB] Instalando Gradio 4.44.1 (nuevo, más rápido)...
[COLAB] ✓ Gradio 4.44.1 instalado exitosamente
[COLAB] Iniciando Fooocus...
Running on local URL:  http://127.0.0.1:7865
Running on public URL: https://xxxxx.gradio.live  ← ¡URL PÚBLICA LISTA!
```

**Esperado:** El link público aparece en 30-60 segundos ✓

---

## 💡 Tips Útiles

- **Una vez resuelto:** Gradio no se reinstala cada vez, sigue siendo 4.44.1
- **Google Drive:** Guarda modelos en Drive para reutilizarlos (ver COLAB_SIMPLE.md)
- **Máximo rendimiento:** Usa Colab Pro con A100 GPU para 3-5s por imagen

---

**¿Necesitas ayuda?** Revisa la salida completa del error y copia/pega la línea que dice "ModuleNotFoundError" o similar.
