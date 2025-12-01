# Nano Banana Lab 🍌

[![English](https://img.shields.io/badge/lang-English-blue.svg)](README.md)
[![中文](https://img.shields.io/badge/lang-中文-red.svg)](README.zh-CN.md)

A learning project exploring Google Gemini 3 Pro Image (Nano Banana Pro) capabilities for AI image generation.

## Features & Experiments

| # | Experiment | File | Description | Status |
|---|------------|------|-------------|--------|
| 01 | Basic Generation | `experiments/01_basic.py` | Text-to-image generation with customizable aspect ratio | ✅ |
| 02 | Thinking Process | `experiments/02_thinking.py` | Visualize model's reasoning before image generation | ✅ |
| 03 | Search Grounding | `experiments/03_search.py` | Integrate real-time Google Search data into images | ✅ |
| 04 | 4K Generation | `experiments/04_4k.py` | Ultra-high resolution image generation (up to 4096x4096) | ✅ |
| 05 | Multilingual | `experiments/05_multilang.py` | Multi-turn chat for cross-language image translation | ✅ |
| 06 | Image Blending | `experiments/06_blend.py` | Combine multiple images with style transfer | ✅ |

## Streamlit Web UI

A full-featured web interface for interactive image generation.

```bash
streamlit run app.py
```

**Features:**
- 🌐 **Internationalization (i18n)** - English and Chinese support
- 🔑 **API Key Management** - Use environment variable or input your own key in UI
- 🎨 **Multiple Generation Modes:**
  - Basic Generation - Simple text-to-image
  - Chat & Refine - Iterative image improvement through conversation
  - Batch Generation - Generate multiple variations with progress tracking
  - Style Transfer - Apply artistic styles between images
  - Search Grounding - Generate images with real-time search data
  - Templates - Start with curated prompt templates
- 📊 **Cost Estimation** - See estimated costs before batch generation
- 📦 **ZIP Download** - Download all batch images in one file
- 📜 **History** - View and download previously generated images

## Quick Start

### 1. Environment Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure API Key

```bash
cp .env.example .env
# Edit .env and add your API Key
# Get it from: https://aistudio.google.com/app/apikey
```

### 3. Run Experiments

```bash
python experiments/01_basic.py
# Generated images are saved in outputs/ directory
```

## Function Details

### 01_basic.py - Basic Image Generation
```python
generate_basic_image(prompt, aspect_ratio="16:9")
```
- Generate images from text prompts
- Supports various aspect ratios: `16:9`, `1:1`, `9:16`, etc.

### 02_thinking.py - Thinking Process Visualization
```python
generate_with_thinking(prompt, aspect_ratio="16:9")
```
- Enable model's thinking feature with `ThinkingConfig(include_thoughts=True)`
- Display model's reasoning process before image generation

### 03_search.py - Search Grounding
```python
generate_with_search(prompt, aspect_ratio="16:9")
```
- Integrate real-time Google Search data using `tools=[{"google_search": {}}]`
- Generate images with up-to-date information (weather, news, etc.)

### 04_4k.py - 4K Ultra HD Generation
```python
generate_4k_image(prompt, resolution="4K", aspect_ratio="16:9")
```
- Support multiple resolutions: `1K`, `2K`, `4K`
- 4K generates 4096x4096 images

### 05_multilang.py - Multilingual Capabilities
```python
generate_multilingual_image(prompt, aspect_ratio="16:9", filename="05_multilang.png")
chat_and_translate()
```
- Multi-turn conversation mode for image translation
- Maintain visual consistency across languages

### 06_blend.py - Advanced Image Blending
```python
blend_images(prompt, image_paths, aspect_ratio="16:9")
demo_style_transfer()
```
- Blend up to 14 images (Pro model)
- Style transfer capabilities

## Output Gallery

### 01 - Basic Generation
![Basic Generation](outputs/01_basic.png)
*A cute corgi wearing sunglasses on a beach at sunset - photorealistic style*

### 02 - Thinking Process
![Thinking Process](outputs/02_thinking.png)
*Viral-worthy image generated with visible AI reasoning process*

### 03 - Search Grounding
![Search Grounding](outputs/03_search.png)
*Real-time weather forecast visualization*

### 04 - 4K Ultra HD
![4K Generation](outputs/04_4K.png)
*Four seasons of an oak tree - 4096x4096 ultra-high resolution*

### 05 - Multilingual
| English | Chinese |
|---------|---------|
| ![English](outputs/05_multilang_en.png) | ![Chinese](outputs/05_multilang_zh.png) |

### 06 - Image Blending
| Base Photo | Style Reference | Blended Result |
|------------|-----------------|----------------|
| ![Base](outputs/06_base_photo.png) | ![Style](outputs/06_style_ref.png) | ![Blend](outputs/06_blend.png) |

## Project Structure

```
nano-banana-lab/
├── app.py              # Streamlit Web UI entry point
├── config.py           # Client initialization & timing
├── components/         # UI components
├── services/           # Backend services
├── i18n/               # Internationalization
├── experiments/        # Experiment scripts
├── outputs/            # Generated images
├── Dockerfile          # Docker configuration
└── docker-compose.yml  # Docker Compose config
```

## Pricing Reference

| Resolution | Price per Image | Notes |
|------------|-----------------|-------|
| 1K / 2K | $0.134 | Standard quality |
| 4K | $0.24 | Print-quality |
| Batch API | -50% | Use for bulk generation |

## References

- [Official Documentation](https://ai.google.dev/gemini-api/docs)
- [Google AI Studio](https://aistudio.google.com)
- [Pricing Page](https://ai.google.dev/pricing)
