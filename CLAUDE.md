# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Quick Start Commands

### Running Fooocus

**Windows (via embedded Python):**
```bash
# Default preset (juggernautXL)
run.bat

# Anime preset
run_anime.bat

# Realistic preset
run_realistic.bat
```

**Linux/Mac (native Python 3.10+):**
```bash
# Activate conda environment (if using conda)
conda activate fooocus

# Run with default preset
python entry_with_update.py

# Run with anime preset
python entry_with_update.py --preset anime

# Run with realistic preset
python entry_with_update.py --preset realistic

# Listen on network (open remote port)
python entry_with_update.py --listen

# Specify custom port
python entry_with_update.py --listen --port 8888
```

### Development and Testing

**Running unit tests:**
```bash
# Native Python
python -m unittest tests/

# Windows embedded Python
..\python_embeded\python.exe -m unittest tests/
```

**With Docker:**
See [docker.md](docker.md) for full Docker setup and commands.

## Architecture Overview

Fooocus is a Stable Diffusion XL-based image generator with a Gradio web UI. The system is organized into three main layers:

### 1. **User Interface Layer** (`webui.py`)
- Gradio-based web interface
- Orchestrates user input collection and result display
- Real-time preview streaming during generation
- Manages image input workflows (upscale, variation, inpaint, enhance, image prompt)

### 2. **Task Execution Layer** (`modules/async_worker.py`)
- Asynchronous task queue with `AsyncTask` class
- `worker()` generator function runs image generation in background thread
- Yields progress updates and preview images to UI
- Handles all generation modes: text-to-image, upscaling, inpainting, enhancement, etc.

### 3. **Model Processing Layer**
- `modules/default_pipeline.py` - Core diffusion sampling pipeline with base + refiner stages
- `modules/patch.py` - Patching system for custom model behavior (CFG, ADM guidance, FreeU, etc.)
- `modules/core.py` - Low-level model operations (LoRA loading, ControlNet application)
- `modules/config.py` - Centralized configuration and model path management

### Data Flow

```
User Input (webui) → AsyncTask → worker() → default_pipeline.process_diffusion()
                                               ↓
                                    Base Model Diffusion
                                               ↓
                                    Refiner Model (optional)
                                               ↓
                                    VAE Decode → Post-processing
                                               ↓
                                    Save Image & Update UI
```

## Key Modules and Responsibilities

| Module | Responsibility |
|--------|-----------------|
| `entry_with_update.py` | Update wrapper and entry point |
| `launch.py` | Environment setup, PyTorch init, model downloads |
| `webui.py` | Gradio UI interface and event handling |
| `modules/async_worker.py` | Task queue and generation loop |
| `modules/default_pipeline.py` | Core diffusion process, model orchestration |
| `modules/patch.py` | Model patching for custom sampling behavior |
| `modules/core.py` | Model loading, LoRA/ControlNet application |
| `modules/config.py` | Config loading, path management, defaults |
| `modules/util.py` | Image utilities, prompt parsing, file helpers |
| `modules/meta_parser.py` | Image metadata encoding/decoding |
| `modules/sdxl_styles.py` | Style management and application |
| `modules/inpaint_worker.py` | Inpaint/outpaint mask generation |
| `modules/sample_hijack.py` | Prompt reweighting and CLIP text processing |
| `args_manager.py` | CLI argument parsing |
| `shared.py` | Global app instance reference |

## Configuration

### Configuration File

After first run, edit `config.txt` to customize:
- Model paths (checkpoints, LoRAs, embeddings, VAEs, etc.)
- Default generation parameters (CFG scale, sampler, scheduler)
- Default model and styles
- Output and cache directories

Example:
```json
{
    "path_checkpoints": "D:\\Fooocus\\models\\checkpoints",
    "path_loras": "D:\\Fooocus\\models\\loras",
    "default_model": "juggernautXL_v8Rundiffusion.safetensors",
    "default_cfg_scale": 3.0,
    "default_sampler": "dpmpp_2m",
    "default_scheduler": "karras"
}
```

### Model Presets

Three built-in presets with different default models in `presets/`:
- `default.json` - juggernautXL (general purpose)
- `anime.json` - animaPencilXL (anime style)
- `realistic.json` - realisticStockPhoto (photorealistic)

Models auto-download on first use. Pre-download manually to `models/checkpoints/` to skip download.

## Important Architectural Patterns

### Asynchronous Task Processing
- `AsyncTask` class holds all generation parameters
- `worker()` function is a generator yielding progress and results
- `async_tasks` queue manages task submission
- Progress callbacks through `task.yields` for streaming results to UI

### Model Management
- **Lazy Loading**: Models loaded on-demand, not at startup
- **Two-Stage Pipeline**: Base model + optional Refiner model
- **LoRA Composition**: LoRAs applied at runtime (not model merged)
- **Automatic VAE Selection**: VAE choice depends on denoise strength and task

### Patching System (modules/patch.py)
Critical for Fooocus's advanced features without forking models:
- Custom CFG computation with negative ADM guidance
- Attention mechanism customization
- Sampler hijacking for advanced scheduling
- FreeU enhancements for quality
- Self-Attention Guidance (SAG) for texture preservation

**Key Pattern**: Global `patch_settings` dictionary applied per process for thread-safe customization.

### Image Enhancement Pipeline
- Mask-based selective region refinement (via GroundingDINO + SAM)
- Multiple enhancement tabs allow iterative refinement
- Separate enhancement generation separate from base generation

### VAE and Memory Optimization
- **Tiled VAE**: Encodes/decodes large images in tiles to reduce peak VRAM
- **VAE Approximation**: Fast VAE preview during generation (faster but lower quality)
- **Cond Caching**: Caches CLIP embeddings for repeated prompts
- **Model Offloading**: Automatic GPU/CPU swapping based on VRAM availability

## Command-Line Flags

Key flags for `entry_with_update.py`:

**Network & Server:**
- `--listen [IP]` - Listen on network interface (default localhost)
- `--port PORT` - Specify port (default 7860)
- `--share` - Create gradio.live endpoint
- `--multi-user` - Allow concurrent users

**GPU & Memory:**
- `--gpu-device-id DEVICE_ID` - Select GPU device
- `--always-gpu` - Force GPU only (no CPU fallback)
- `--always-high-vram` - Maximum VRAM usage, minimum RAM
- `--always-normal-vram` - Balanced mode
- `--always-low-vram` - Minimum VRAM footprint
- `--disable-async-cuda-allocation` - Disable PyTorch async memory allocation
- `--vae-in-cpu` - Keep VAE on CPU

**Model & Precision:**
- `--preset {default,anime,realistic}` - Model preset
- `--all-in-fp16` - Use float16 everywhere
- `--all-in-fp32` - Use float32 everywhere (slower, more compatible)
- `--unet-in-fp8-e4m3fn` - Use 8-bit quantization for UNet
- `--clip-in-fp16` - Use float16 for CLIP

**Advanced:**
- `--debug-mode` - Enable debug logging
- `--disable-offload-from-vram` - Keep models in VRAM between generations
- `--always-download-new-model` - Auto-download missing models on preset change
- `--preview-option {none,auto,fast,taesd}` - Preview generation method
- `--language LANGUAGE` - UI language (load from `language/[language].json`)

See `python entry_with_update.py --help` for complete list.

## Extension Points

### Adding Styles
Edit `presets/default.json` or create custom JSON with style definitions.

### Adding ControlNets
- Place model files in `models/controlnet/`
- Modify `modules/flags.py` to add new ControlNet type
- Update `webui.py` to add UI controls

### Adding Samplers/Schedulers
- Modify sampler enum in `modules/flags.py`
- Update `modules/default_pipeline.py` if using new library

### Language/Localization
- Create JSON file in `language/` directory with UI string translations
- Run with `--language [filename]` flag

## Understanding the Generation Process

### Text-to-Image Flow
1. **Prompt Expansion**: Offline GPT-2 prompt expansion (Fooocus V2 style)
2. **Prompt Parsing**: Extract inline LoRAs, expand wildcards
3. **CLIP Encoding**: Tokenize and encode with CLIP text encoders
4. **Latent Init**: Random noise at target resolution
5. **Diffusion Loop**: Iterative denoising with base model, preview generation
6. **Refiner Switch**: Switch to refiner model at specified step (if enabled)
7. **VAE Decode**: Convert latent to image
8. **Post-process**: Upscaling, enhancement, metadata saving

### Image Upscale/Variation
- Encodes input image to latent
- Applies denoise amount (0.0 = no change, 1.0 = full regeneration)
- Low denoise creates subtle variations
- High denoise creates strong variations

### Inpaint/Outpaint
- Generates mask based on user brush or automatic segmentation
- Masks latent during diffusion (masked regions regenerated, unmasked preserved)
- Supports outpainting by extending canvas

### Image Prompt (IP-Adapter)
- Encodes reference image with CLIP-Vision encoder
- Applies IP-Adapter to condition generation on image semantics
- Allows "image style transfer" conceptually

## Memory and Performance Considerations

**VRAM Requirements:**
- Minimum 4GB for base SDXL (with system swap)
- 6-8GB recommended for comfortable performance
- 12GB+ for running refiner without slowdown

**Performance Tips:**
1. Use `--always-high-vram` on high-VRAM systems for maximum speed
2. Use tiled VAE for large image dimensions
3. Disable preview generation (`--preview-option none`) to save time
4. Use `--unet-in-fp8-e4m3fn` to reduce VRAM with minimal quality loss
5. Keep VAE on GPU for faster encoding/decoding

**Model Selection:**
- juggernautXL is fastest while maintaining quality
- Smaller models (e.g., RealisticStockPhoto) may be faster on limited VRAM
- LoRAs add minimal overhead

## Testing and Debugging

**Enable Debug Mode:**
```bash
python entry_with_update.py --debug-mode
```

This enables:
- Verbose logging to console
- "Debug Mode" panel in UI with wildcard options
- Detailed error messages

**Common Issues:**
- **RuntimeError: CPUAllocator** - Enable Windows Virtual Swap (see readme.md)
- **MetadataIncompleteBuffer or PytorchStreamReader** - Model files corrupted, redownload
- **Slow generation** - Check GPU driver version (Nvidia 531+ has been reported slower; try 531)
- **CUDA out of memory** - Use `--always-low-vram` or reduce image resolution

## Batch Processing & Avatar Digital Features

This codebase has been extended with three key features for avatar digital generation:

### Feature 1: Optimal Checkpoint Management

**Solution:** Hugging Face Hub + Colab Preset (Recommended)

Files:
- `presets/colab.json` - Preset with Juggernaut, Realistic, Anime models
- `fooocus_colab_optimized.py` - Google Colab launcher

Auto-downloads 3 models (8GB each) in ~5-7 minutes. No GitHub bloat, all in HF Hub.

```bash
# Local: python entry_with_update.py --preset colab
# Colab: python fooocus_colab_optimized.py
```

### Feature 2: Batch Prompts TXT → Images + Face Swap

Files:
- `modules/batch_processor.py` - Reads prompts from TXT, generates batch tasks
- `modules/face_processor.py` - Face detection and swapping (InsightFace-based)
- `run_batch_processing.py` - Interactive CLI for batch processing

Workflow:
1. Create `prompts.txt` (one prompt per line)
2. Upload `face_model.jpg` (face to inject)
3. Run `python run_batch_processing.py`
4. Get images with face swap applied in `batch_outputs/`

### Feature 3: Face Detection and Replacement in Existing Images

Process images in `target_images/` folder:
1. Automatically detects faces using InsightFace
2. Replaces with `face_model.jpg` face
3. Saves results in `target_images/faceswapped/`

Also handled automatically by `run_batch_processing.py`

### Configuration

`BatchProcessorConfig` class in `modules/batch_processor.py`:
- `prompts_file` - Path to TXT with prompts
- `face_model_image` - Path to face image
- `enable_face_swap` - Apply face swap post-generation
- `use_image_prompt` - Use face as IP-Adapter reference
- `image_prompt_strength` - 0.0-1.0 influence of face reference
- `face_swap_strength` - 0.0-1.0 intensity of face replacement
- `steps`, `cfg_scale`, `sampler` - Generation parameters

### Quick Start

```bash
# 1. Create prompts.txt
echo "a girl in office, professional, 8k" > prompts.txt
echo "a girl on beach, sunset, 8k" >> prompts.txt

# 2. Upload face_model.jpg

# 3. Run interactive batch processor
python run_batch_processing.py
```

### Documentation Files

- `QUICK_START_BATCH.md` - 5-minute quick reference
- `BATCH_PROCESSING_GUIDE.md` - Comprehensive guide with examples
- `WEBUI_INTEGRATION_EXAMPLE.md` - How to integrate UI components

### InsightFace Installation

For face detection and swap:
```bash
pip install insightface onnxruntime-gpu
```

Or CPU-only:
```bash
pip install insightface onnxruntime
```

---

## Project Status

**Limited Long-Term Support (LTS) with Bug Fixes Only**
- Built on Stable Diffusion XL architecture
- No planned migration to newer model architectures (e.g., Flux)
- Future updates focus on bug fixes and community-driven improvements
- Consider [WebUI Forge](https://github.com/lllyasviel/stable-diffusion-webui-forge) or [ComfyUI](https://github.com/comfyanonymous/ComfyUI) for cutting-edge model support
