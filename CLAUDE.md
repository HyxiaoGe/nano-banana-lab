# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Nano Banana Lab** is a learning project exploring Google Gemini 3 Pro Image (Nano Banana Pro) capabilities for AI image generation. It provides both an interactive Streamlit web UI and standalone experiment scripts demonstrating various image generation techniques.

**Core Features:**
- Text-to-image generation with multiple resolution options (1K, 2K, 4K)
- Multi-turn chat-based iterative image refinement
- Batch image generation with progress tracking and cost estimation
- Image blending and style transfer
- Search-grounded generation with real-time data integration
- Complete bilingual support (English and Chinese)
- **Trial Mode** - Shared quota system for users without API keys (NEW)
- **GitHub OAuth** - User authentication with data isolation (NEW)
- **AI Prompt Library** - AI-powered prompt generation with favorites and cloud sync (NEW)

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Streamlit Web UI (app.py)                │
├─────────────────────────────────────────────────────────────┤
│   components/           │           i18n/                   │
│   ├── sidebar.py        │           ├── en.json             │
│   ├── basic_generation  │           └── zh.json             │
│   ├── chat_generation   │                                   │
│   ├── batch_generation  ├───────────────────────────────────┤
│   ├── style_transfer    │        utils/async_helper.py      │
│   ├── search_generation │                                   │
│   ├── templates.py      │                                   │
│   └── history.py        │                                   │
├─────────────────────────────────────────────────────────────┤
│                    services/ (Business Logic)               │
│   ├── generator.py       - Core image generation            │
│   ├── chat_session.py    - Multi-turn conversations         │
│   ├── cost_estimator.py  - Cost calculation                 │
│   ├── image_storage.py   - Local storage                    │
│   ├── r2_storage.py      - Cloudflare R2 cloud storage      │
│   ├── persistence.py     - Browser cookie persistence       │
│   ├── generation_state.py- State & progress tracking        │
│   ├── history_sync.py    - Cross-tab synchronization        │
│   └── health_check.py    - API health monitoring            │
├─────────────────────────────────────────────────────────────┤
│              Google GenAI SDK (gemini-3-pro-image-preview)  │
└─────────────────────────────────────────────────────────────┘
```

## Directory Structure

```
nano-banana-lab/
├── app.py                 # Main Streamlit entry point
├── config.py              # Client initialization & timing instrumentation
├── requirements.txt       # Python dependencies
├── .env.example           # Environment variable template
├── components/            # UI component modules
│   ├── sidebar.py         # Settings, API key, language selection
│   ├── basic_generation.py
│   ├── chat_generation.py
│   ├── batch_generation.py
│   ├── style_transfer.py
│   ├── search_generation.py
│   ├── templates.py
│   └── history.py
├── services/              # Backend service layer
│   ├── generator.py       # ImageGenerator with retry logic
│   ├── chat_session.py    # ChatSession for multi-turn
│   ├── cost_estimator.py
│   ├── image_storage.py
│   ├── r2_storage.py
│   ├── persistence.py
│   ├── generation_state.py
│   ├── history_sync.py
│   ├── health_check.py
│   ├── auth.py            # GitHub OAuth authentication
│   ├── trial_quota.py     # Trial mode quota management
│   ├── prompt_generator.py # AI-powered prompt generation
│   └── prompt_storage.py  # Prompt library storage
├── i18n/                  # Internationalization
│   ├── __init__.py        # Translator class
│   ├── en.json            # English translations
│   └── zh.json            # Chinese translations
├── experiments/           # Standalone experiment scripts
│   ├── 01_basic.py
│   ├── 02_thinking.py
│   ├── 03_search.py
│   ├── 04_4k.py
│   ├── 05_multilang.py
│   └── 06_blend.py
├── scripts/               # Utility scripts
│   ├── init_prompts.py    # Initialize prompt library with AI
│   ├── test_prompts.py    # Test prompt generation
│   └── preview_prompts.py # Preview prompt templates
├── utils/
│   └── async_helper.py    # Async/event loop management
├── outputs/               # Generated images directory
├── .streamlit/
│   └── config.toml        # Streamlit theme and server settings
├── Dockerfile
├── docker-compose.yml
├── Procfile
├── railway.json
└── render.yaml
```

## Quick Reference Commands

```bash
# Development server
streamlit run app.py

# Run specific experiment
python experiments/01_basic.py
python experiments/02_thinking.py
python experiments/03_search.py
python experiments/04_4k.py
python experiments/05_multilang.py
python experiments/06_blend.py

# Initialize prompt library with AI-generated prompts
python scripts/init_prompts.py

# Test prompt generation
python scripts/test_prompts.py

# Docker local development
docker-compose up -d

# Docker build
docker build -t nano-banana-lab .
docker run -p 8501:8501 -e GOOGLE_API_KEY=your_key nano-banana-lab

# Install dependencies
pip install -r requirements.txt
```

## Key Technologies

| Technology | Version | Purpose |
|------------|---------|---------|
| Python | 3.11 | Runtime |
| google-genai | >=1.0.0 | Google Gemini API SDK |
| streamlit | >=1.30.0 | Web UI framework |
| Pillow | >=10.0.0 | Image processing |
| boto3 | >=1.34.0 | Cloudflare R2 storage (S3-compatible) |
| python-dotenv | >=1.0.0 | Environment variable management |
| extra-streamlit-components | >=0.1.60 | Cookie management |
| streamlit-oauth | >=0.1.8 | GitHub OAuth authentication |

**AI Models:**
- `gemini-3-pro-image-preview` - Image generation
- `gemini-2.0-flash` - Health checks and prompt generation

## Environment Variables

Required:
```
GOOGLE_API_KEY              # Google Gemini API key (required)
```

Optional - Cloudflare R2 Storage:
```
R2_ENABLED                  # Enable cloud storage (true/false)
R2_ACCOUNT_ID               # Cloudflare account ID
R2_ACCESS_KEY_ID            # R2 access key
R2_SECRET_ACCESS_KEY        # R2 secret key
R2_BUCKET_NAME              # S3 bucket name (default: nano-banana-images)
R2_PUBLIC_URL               # Public URL for images
```

Optional - GitHub OAuth:
```
GITHUB_CLIENT_ID            # GitHub OAuth app client ID
GITHUB_CLIENT_SECRET        # GitHub OAuth app client secret
GITHUB_REDIRECT_URI         # OAuth callback URL (default: http://localhost:8501)
```

Optional - Trial Mode (for users without API keys):
```
TRIAL_ENABLED               # Enable trial mode (true/false, default: false)
TRIAL_GLOBAL_QUOTA          # Global daily quota pool (default: 50)
TRIAL_QUOTA_MODE            # Configuration mode: "auto" or "manual" (default: "manual")
TRIAL_COOLDOWN_SECONDS      # Seconds between generations (default: 3)
# Manual quota limits per mode (when TRIAL_QUOTA_MODE=manual)
TRIAL_BASIC_1K_LIMIT        # Daily limit for basic 1K/2K (default: 30)
TRIAL_BASIC_4K_LIMIT        # Daily limit for basic 4K (default: 5)
TRIAL_CHAT_LIMIT            # Daily limit for chat (default: 20)
TRIAL_BATCH_1K_LIMIT        # Daily limit for batch 1K/2K (default: 15)
TRIAL_BATCH_4K_LIMIT        # Daily limit for batch 4K (default: 3)
TRIAL_SEARCH_LIMIT          # Daily limit for search (default: 15)
TRIAL_BLEND_LIMIT           # Daily limit for blend/style (default: 10)
```

Optional - Defaults:
```
DEFAULT_LANGUAGE            # en or zh (default: en)
DEFAULT_RESOLUTION          # 1K, 2K, or 4K (default: 1K)
DEFAULT_ASPECT_RATIO        # 1:1, 16:9, 9:16, 4:3, 3:4 (default: 16:9)
DEFAULT_SAFETY_LEVEL        # strict, moderate, relaxed, none (default: moderate)
```

## Code Conventions

### Naming Conventions
- **Classes:** PascalCase (`ImageGenerator`, `ChatSession`, `PersistenceService`)
- **Functions:** snake_case (`render_sidebar()`, `generate_image()`, `get_storage()`)
- **Constants:** UPPER_SNAKE_CASE (`MAX_RETRIES`, `OUTPUT_DIR`, `MODEL_ID`)
- **Session state keys:** Prefixed by feature (`gen_state_`, `nbl_`, `chat_`)

### Patterns Used

**1. Service Layer Pattern**
Services in `services/` contain business logic separated from UI. Global singleton instances accessed via getter functions:
```python
from services import get_persistence, get_storage, get_history_sync
```

**2. Component Module Pattern**
UI components in `components/` follow this structure:
```python
def render_component_name(translator, settings):
    """Render the component UI."""
    # UI code using Streamlit
```

**3. State Management**
Uses Streamlit session state with initialization pattern:
```python
def init_session_state():
    if "key" not in st.session_state:
        st.session_state.key = default_value
```

**4. Error Handling with Retry**
Network operations use retry logic with exponential backoff:
- Max attempts: 3
- Backoff delays: [2s, 4s, 8s]
- Retryable errors: Connection issues, timeout, 502/503/504 errors

**5. Internationalization**
All user-facing text uses the Translator class:
```python
from i18n import Translator
t = Translator(language="en")
text = t.get("sidebar.api_key.title")
```

### Important Files

| File | Purpose |
|------|---------|
| `app.py` | Main entry point, session initialization, routing |
| `config.py` | GenAI client setup, model ID, timing utilities |
| `services/generator.py` | Core `ImageGenerator` class with retry logic |
| `services/chat_session.py` | `ChatSession` for multi-turn conversations |
| `services/persistence.py` | Browser cookie-based persistence |
| `services/r2_storage.py` | Cloudflare R2 cloud storage integration |
| `services/auth.py` | GitHub OAuth authentication service |
| `services/trial_quota.py` | Trial mode quota tracking and enforcement |
| `services/prompt_generator.py` | AI-powered prompt generation using Gemini |
| `services/prompt_storage.py` | Prompt library storage with R2 sync |
| `components/sidebar.py` | Settings panel, API key management |

## API Configuration

**Image Generation Settings:**
- Aspect Ratios: `1:1`, `16:9`, `9:16`, `4:3`, `3:4`
- Resolutions: `1K`, `2K`, `4K`
- Safety Levels: `strict`, `moderate`, `relaxed`, `none`

**Safety Settings Mapping:**
```python
SAFETY_LEVELS = {
    "strict": "BLOCK_LOW_AND_ABOVE",
    "moderate": "BLOCK_MEDIUM_AND_ABOVE",
    "relaxed": "BLOCK_ONLY_HIGH",
    "none": "BLOCK_NONE"
}
```

## Testing

No automated test framework is configured. Testing is done via:

1. **Experiment scripts** (`experiments/01-06`) - Standalone API tests
2. **Manual UI testing** - Run Streamlit app and test features
3. **Health check endpoint** - `/_stcore/health` for container health

## Deployment

**Supported Platforms:**
- Streamlit Cloud (direct GitHub integration)
- Railway (`railway.json`)
- Render (`render.yaml`)
- Docker (any container platform)
- Google Cloud Run
- Hugging Face Spaces

**Startup command pattern:**
```bash
streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

**Docker health check:**
```
curl --fail http://localhost:8501/_stcore/health
```

## Authentication & User Isolation

**GitHub OAuth Flow:**
- Implemented via `services/auth.py` using `streamlit-oauth`
- User data stored with unique folder IDs (hash of GitHub user ID)
- R2 storage paths: `{user_folder_id}/images/` and `{user_folder_id}/prompts/`
- Session management via Streamlit session state

**Trial Mode:**
- When `TRIAL_ENABLED=true` and no API key provided, users get shared quota
- Quota tracked via `services/trial_quota.py` with Cloudflare KV storage
- Daily reset, per-mode limits, and global quota pool
- Cooldown enforcement between generations

**Data Isolation:**
- Authenticated users: Data stored in user-specific folders in R2
- Trial users: Shared quota, no persistent data
- API key users: Local storage or user-specific R2 folders

## Common Tasks

### Adding a New UI Component
1. Create new file in `components/`
2. Implement `render_component_name(translator, settings)` function
3. Export from `components/__init__.py`
4. Add mode option in `app.py`
5. Add translations in `i18n/en.json` and `i18n/zh.json`
6. If trial mode is supported, add quota checks via `check_and_show_quota_warning()`

### Adding New Translations
1. Add keys to both `i18n/en.json` and `i18n/zh.json`
2. Use dot-notation for nested keys: `"section.subsection.key"`
3. Use `{placeholder}` for format strings

### Modifying Image Generation
Core generation logic is in `services/generator.py`:
- `generate()` - Basic text-to-image
- `blend_images()` - Multi-image blending
- `generate_with_search()` - Search-grounded generation

### Adding New Service
1. Create file in `services/`
2. Implement service class with singleton getter
3. Export from `services/__init__.py`
4. Initialize in `app.py` if needed at startup

### Working with Prompts
Scripts for prompt library management:
- `scripts/init_prompts.py` - Bulk generate prompts using AI
- `scripts/test_prompts.py` - Test prompt generation and storage
- `scripts/preview_prompts.py` - Preview existing prompt templates

## Error Handling

The codebase has comprehensive error handling for API calls:

**Retryable errors (automatic retry):**
- Connection errors
- Timeout errors
- HTTP 502/503/504 (server overloaded)
- Network-related exceptions

**Non-retryable errors (immediate failure):**
- Invalid API key (401)
- Quota exceeded (429)
- Safety content blocked
- Invalid request parameters

**Friendly error messages** are displayed via i18n system - see `get_friendly_error_message()` in `services/generator.py`. Error types are classified and mapped to `errors.api.*` keys in i18n files.

## Security Notes

- API keys are obfuscated in browser cookies (base64 + reversal) but not encrypted
- Use environment variables for production deployments
- XSRF protection is enabled in Streamlit config
- `.env` files are excluded from git via `.gitignore`
- R2 credentials should never be committed

## Performance Considerations

- Images are cached in Streamlit session state
- Metadata is cached in history sync service
- boto3 connection pooling for R2 storage
- Date-based folder organization for efficient file lookup
- Lazy loading of translations

## UI/UX Features

### History Management
- **Pagination**: Configurable items per page (4/8/12/16)
- **Search**: Filter by prompt text
- **Mode Filter**: Filter by generation mode (basic, chat, batch, etc.)
- **Image Preview**: Click 🔍 to open full-size preview with details
- **Sorting**: Sort by date (newest/oldest first)
- **Date Filtering**: Filter images by date range
- **Grid Layout**: Toggle between compact and spacious views
- **Data Source**: Switch between local and R2 storage

### Chat Mode
- **Clear Confirmation**: Prevents accidental chat deletion
- **Export Chat**: Download conversation as JSON
- **Message Count**: Shows current conversation length
- **Empty State**: Helpful guidance for new users

### Prompt Library (Templates)
- **AI Generation**: Generate prompts with Gemini Flash
- **Categories**: Organize by portrait, landscape, food, abstract, etc.
- **Favorites**: Star/unstar prompts for quick access
- **Search**: Filter prompts by keywords
- **Cloud Sync**: Optional R2 sync for authenticated users
- **Use Button**: One-click copy to generation modes

### Trial Mode UI
- **Quota Display**: Real-time quota usage tracking
- **Per-Mode Limits**: Show remaining quota for each generation mode
- **Cooldown Timer**: Visual countdown between generations
- **Warning Dialogs**: Prevent usage when quota exhausted

### Empty States
All modes show helpful guidance when no content exists:
- Tips for better prompts in Basic Generation
- Quick start instructions in Chat mode
- Navigation hints in History
- Prompt library introduction in Templates
