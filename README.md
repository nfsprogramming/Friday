# F.R.I.D.A.Y.

> *"Fully Responsive Intelligent Digital Assistant for You"*  
> A Tony Stark-inspired AI voice assistant and FastMCP server featuring real-time multimodal voice interaction, tool-augmented reasoning, local wake-word detection, and an interactive 3D WebGL visualization.

---

## Overview

FRIDAY is a modular, multi-layer AI assistant architecture designed for real-time responsiveness and agentic tool invocation:

| Component | Entry Point | Description |
|-----------|------------|-------------|
| **FastMCP Server** | `uv run friday` (`mcp_server.py`) | An SSE-based [FastMCP](https://github.com/jlowin/fastmcp) server running on port `8000` that exposes tools for web browsing, live news summaries, system diagnostics, screen capture, and SQLite memory. |
| **LiveKit Voice Agent** | `uv run friday_voice` (`livekit_agent.py`) | A real-time [LiveKit Agents](https://github.com/livekit/agents) pipeline combining Sarvam STT / Whisper, Gemini 2.5 Flash / GPT-4o, and OpenAI TTS / Sarvam with live MCP tool calling. |
| **Particle Orb UI** | `cd frontend && npm run dev` | A high-performance Three.js WebGL visualization that responds dynamically to speech states (`idle`, `listening`, `thinking`, `speaking`) and audio frequencies. |
| **Ambient Voice Client** | `python voice_client.py` | Standalone offline/local ambient listener with OpenWakeWord detection ("Hey Jarvis"), WebRTC VAD, faster-whisper transcription, and Piper neural TTS. |
| **FastAPI REST Backend** | `python scripts/run_api.py` | REST API and WebSocket gateway providing desktop automation (PyAutoGUI, pywinauto, OpenCV/EasyOCR), file indexing (ChromaDB), and system telemetry. |

---

## Implemented Features

- **FastMCP Tool Ecosystem**:
  - `search_web`: Live internet queries via DuckDuckGo.
  - `get_world_news` & `get_world_finance_news`: Global news headlines and financial briefs.
  - `open_world_monitor`: Automated browser launch of live visualization dashboards.
  - `remember_fact` & `search_memory`: Permanent SQLite memory storage (`data/friday.db`).
  - `add_task`, `list_open_tasks`, `mark_task_done`: Integrated task schedule management.
  - `get_current_time` & `get_system_info`: Real-time host hardware telemetry (CPU, RAM, platform).
  - `capture_screen` & system actions: Desktop screen inspection and volume/power controls.
- **Multimodal Voice Pipeline**:
  - LiveKit Agents architecture supporting room-based WebRTC audio streaming.
  - Pluggable STT: Sarvam Saaras v3 (`sarvam`), local faster-whisper (`whisper`), or Deepgram.
  - Pluggable LLM: Google Gemini 2.5 Flash (`gemini`) or OpenAI GPT-4o (`openai`).
  - Pluggable TTS: OpenAI TTS (`nova` voice) or Sarvam (`rahul` voice, Indian English).
  - Automatic dynamic MCP tool injection into the voice agent session at startup.
- **Interactive Three.js Orb Visualizer**:
  - Procedural 3D particle sphere with dynamic proximity-based connection lines and travelling electron pulses during thinking states.
  - AudioAnalyser integration tracking real-time frequency data from WebRTC audio tracks.
  - Built-in settings overlay for runtime parameters.
- **Desktop & System Automation Engine**:
  - Window management, mouse and keyboard automation via `app/desktop/`.
  - Desktop vision using OpenCV and EasyOCR for screen OCR and template detection.
  - Semantic file search and indexing powered by ChromaDB vector store.
  - System hardware sensors monitoring CPU, GPU, RAM, Disk, Battery, and Network metrics.

---

## Architecture Flow

```
                      ┌──────────────────────────────────────────────┐
                      │              User Audio / Mic                │
                      └──────────────────────┬───────────────────────┘
                                             │ WebRTC / Direct Mic
                                             ▼
                      ┌──────────────────────────────────────────────┐
                      │    LiveKit Voice Agent / Ambient Client      │
                      │  - STT: Sarvam Saaras v3 / Whisper           │
                      │  - VAD: Silero / WebRTC VAD                  │
                      └──────────────────────┬───────────────────────┘
                                             │
                                             ▼
                      ┌──────────────────────────────────────────────┐
                      │         Reasoning Core (Gemini / GPT)         │
                      └──────────────┬────────────────────────▲──────┘
                                     │                        │
               Tool Execution Request│                        │ Tool Results
                                     ▼                        │
                      ┌───────────────────────────────────────┴──────┐
                      │       FastMCP Server (SSE :8000)             │
                      │  ├─ Web Search & Global News Briefings       │
                      │  ├─ Persistent SQLite Memory & Tasks         │
                      │  ├─ Playwright Browser & Desktop Vision      │
                      │  └─ Hardware & System Diagnostics            │
                      └──────────────────────────────────────────────┘
                                             │
                                             ▼ Spoken Reply
                      ┌──────────────────────────────────────────────┐
                      │         TTS: OpenAI (nova) / Sarvam          │
                      │                      │                       │
                      │                      ▼                       │
                      │     LiveKit Room / Local Audio Player        │
                      └──────────────────────┬───────────────────────┘
                                             │
                                             ▼ Audio Frequency Data
                      ┌──────────────────────────────────────────────┐
                      │   Three.js Particle Orb (Frontend WebGL)     │
                      └──────────────────────────────────────────────┘
```

---

## Tech Stack

| Domain | Technology |
|--------|------------|
| **MCP Framework** | [FastMCP](https://github.com/jlowin/fastmcp) |
| **Real-Time Voice** | [LiveKit Agents](https://github.com/livekit/agents), `livekit-client` |
| **Cloud Models** | Google Gemini (`livekit-plugins-google`), OpenAI (`livekit-plugins-openai`), Sarvam AI |
| **Local Speech & Audio** | `faster-whisper`, `piper-tts`, `openwakeword`, `webrtcvad`, `sounddevice` |
| **Web UI & 3D Engine** | TypeScript, [Vite](https://vite.dev), [Three.js](https://threejs.org) |
| **Backend & Automation** | FastAPI, Uvicorn, Playwright, OpenCV, EasyOCR, PyAutoGUI, psutil |
| **Storage & Embeddings** | SQLite, ChromaDB, SQLAlchemy |
| **Package Management** | [uv](https://github.com/astral-sh/uv), npm |

---

## Prerequisites

- **Python**: Version `3.11` or `3.12`
- **uv**: Fast Python package manager (`pip install uv` or official standalone installer)
- **Node.js**: Version `18+` or `20+` and `npm`
- **LiveKit Cloud**: A free account at [LiveKit Cloud](https://cloud.livekit.io) with Project URL, API Key, and Secret (for voice agent mode)
- **API Keys**: Google Gemini API key and/or OpenAI, Sarvam AI API keys

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/nfsprogramming/Friday.git
cd Friday
```

### 2. Install Python Dependencies

```bash
uv sync
```

This synchronizes the virtual environment with all required dependencies from `pyproject.toml` and `uv.lock`.

### 3. Install Frontend Dependencies

```bash
cd frontend
npm install
cd ..
```

---

## Configuration

Copy `.env.example` to `.env` and provide your credentials:

```bash
cp .env.example .env
```

| Variable | Required | Description |
|----------|:--------:|-------------|
| `LIVEKIT_URL` | Yes | LiveKit Cloud WebSocket URL (`wss://...`) |
| `LIVEKIT_API_KEY` | Yes | LiveKit API Key |
| `LIVEKIT_API_SECRET` | Yes | LiveKit API Secret |
| `GOOGLE_API_KEY` | Yes | Google AI Studio key for Gemini 2.5 Flash |
| `SARVAM_API_KEY` | Optional | Sarvam AI key for Saaras v3 Indian-English STT/TTS |
| `OPENAI_API_KEY` | Optional | OpenAI key for TTS (`nova` voice) or GPT-4o LLM |
| `DEEPGRAM_API_KEY` | Optional | Deepgram key for alternative STT |
| `GROQ_API_KEY` | Optional | Groq key for low-latency inference |

### Switching Providers

In `livekit_agent.py`, configure your active providers:

```python
STT_PROVIDER = "sarvam"   # "sarvam" | "whisper"
LLM_PROVIDER = "gemini"   # "gemini" | "openai"
TTS_PROVIDER = "openai"   # "openai" | "sarvam"
```

---

## Usage

### 1. FastMCP Server

Start the FastMCP tool server:

```bash
uv run friday
```

The FastMCP server listens over Server-Sent Events (SSE) at `http://127.0.0.1:8000/sse`.

### 2. LiveKit Voice Agent

In a separate terminal, launch the LiveKit voice agent:

```bash
uv run friday_voice
```

Connect using either the [LiveKit Agents Playground](https://agents-playground.livekit.io) or the included Three.js frontend.

### 3. Frontend Orb Interface

Start the local Vite dev server:

```bash
cd frontend
npm run dev
```

Or build and serve static distribution assets via the utility server:

```bash
cd frontend && npm run build
python scripts/run_ui.py
```

### 4. Standalone Ambient Voice Mode

To run the local wake-word listener on your workstation microphone:

```bash
python voice_client.py
```

Say **"Hey Jarvis"** to wake the assistant, give your spoken command, and receive local Whisper transcription and Piper speech synthesis.

---

## Project Structure

```
FRIDAY/
├── mcp_server.py             # CLI entry point: FastMCP server ('uv run friday')
├── livekit_agent.py          # CLI entry point: LiveKit Voice Agent ('uv run friday_voice')
├── voice_client.py           # Standalone local wake-word + Whisper + Piper loop
├── pyproject.toml            # Python packaging & tool dependencies (PEP 621)
├── uv.lock                   # Deterministic lockfile for Python dependencies
├── requirements.txt          # Frozen pip dependencies
├── .env.example              # Template environment variables
├── .gitignore                # Git ignore specifications
├── LICENSE                   # MIT License
├── app/                      # FastAPI core backend & automation services
│   ├── main.py               # FastAPI application entry point
│   ├── api/                  # Chat & memory routing endpoints
│   ├── core/                 # Logger, database engine, shared configuration
│   ├── desktop/              # Window, mouse, keyboard & OCR screen automation
│   ├── files/                # Document indexing, duplicates & semantic search
│   ├── llm/                  # Prompt templates, session manager & RAG helpers
│   ├── monitoring/           # Hardware telemetry (CPU, RAM, GPU, Battery, Disk)
│   ├── stt/                  # Microphone input, VAD & faster-whisper engine
│   ├── tools/                # Internal tool registry and execution handlers
│   ├── tts/                  # Piper TTS engine & speech queue manager
│   └── wakeword/             # OpenWakeWord detector & state machine
├── friday/                   # Dedicated FastMCP package
│   ├── config.py             # Settings and environment loader
│   ├── memory.py             # SQLite database manager for facts and tasks
│   ├── prompts/              # System prompt templates
│   ├── resources/            # FastMCP resource endpoints (friday://info)
│   └── tools/                # Registered tool modules (web, system, memory, etc.)
├── frontend/                 # Reactive Three.js WebGL particle interface
│   ├── index.html            # Single-page application entry point
│   ├── package.json          # Vite & Three.js package configuration
│   ├── package-lock.json     # Node lockfile
│   ├── src/
│   │   ├── main.ts           # State machine, LiveKit WebRTC client & audio bridge
│   │   ├── orb.ts            # Three.js 3D particle orb & electron animations
│   │   ├── settings.ts       # UI settings panel
│   │   └── style.css         # Dark theme styling
│   ├── tsconfig.json         # TypeScript configuration
│   └── vite.config.ts        # Vite build configuration
├── scripts/                  # Helper launcher scripts
│   ├── run_api.py            # Starts FastAPI backend on port 8000
│   └── run_ui.py             # Serves frontend & LiveKit token endpoint on port 8080
├── models/                   # Local model configurations (Piper TTS JSON configs)
├── data/                     # Local databases, audio cache, runtime storage (gitignored)
└── docs/                     # Extended architectural documentation
    ├── ARCHITECTURE.md       # High-level architecture overview
    ├── blueprint.html        # Interactive visual system blueprint
    ├── FEATURES.md           # Feature breakdown
    ├── INSTALLATION.md       # Step-by-step setup guide
    ├── PROJECT_STRUCTURE.md  # Detailed module catalog
    ├── ROADMAP.md            # Future milestones
    ├── TECH_STACK.md         # Technology decisions and benchmarks
    └── VISION.md             # Project background and design principles
```

---

## Build

### Python Wheel & Source Distribution

Build the Python package using `uv`:

```bash
uv build
```

Artifacts are produced in `dist/`:
- `dist/friday_tony_stark_demo-0.1.0-py3-none-any.whl`
- `dist/friday_tony_stark_demo-0.1.0.tar.gz`

### Frontend Production Bundle

Build the compiled Three.js client using Vite:

```bash
cd frontend
npm run build
```

Compiled static assets are placed in `frontend/dist/`.

---

## Releases & Downloads

Pre-built application packages, wheel distributions, and compiled web assets are published on the [GitHub Releases](https://github.com/nfsprogramming/Friday/releases) page. Each release includes a verified `checksums.txt` containing SHA-256 signatures for all distributed archives.

---

## Testing & Validation

To verify the installation and module integrity:

```bash
# Verify Python package imports and syntax
python -c "import friday; import app; print('Core modules successfully imported.')"

# Verify TypeScript compilation and frontend build
cd frontend && npm run build && cd ..

# Verify Python package packaging
uv build
```

---

## Limitations

- **Platform-Specific Automation**: Desktop automation components (window management, mouse, keyboard) are tailored for Windows environments; macOS and Linux hosts may require alternative X11/Wayland backends.
- **API Credentials Required**: Real-time cloud voice functionality depends on valid credentials for LiveKit Cloud and corresponding model providers (Google Gemini, OpenAI, or Sarvam AI).
- **Local Audio Hardware**: The standalone ambient client (`voice_client.py`) requires an active default microphone and speaker configured via PyAudio/SoundDevice.

---

## Contributing

Contributions, bug reports, and suggestions are welcome.
1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/new-tool`).
3. Commit your changes (`git commit -m "Add new tool"`).
4. Push to the branch (`git push origin feature/new-tool`).
5. Open a Pull Request.

---

## License

This project is licensed under the [MIT License](LICENSE).
