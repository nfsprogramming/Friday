# F.R.I.D.A.Y - Roadmap

## Build Phases (v0.1 to v3.0)

This roadmap follows a strict rule: **Do NOT touch the UI until the terminal brain (v0.1–v0.3) works perfectly.** Every version must be usable and testable.

### PHASE 0: Environment & Project Init (Week 1)
*   **Goal:** Solid foundation before coding.
*   **Steps:**
    *   Install `uv`, initialize project (`uv init FRIDAY`), add dependencies.
    *   Install Ollama, pull `qwen2.5:7b-instruct-q4_K_M`, verify inference speed.
    *   Create folder structure.
    *   Setup `config.yaml`, `.env`, and logging.
    *   Write core documentation (VISION, ARCHITECTURE, etc.).
    *   Init git repo.

### PHASE 1: Terminal Brain (v0.1 - v1.0)

*   **v0.1: Local Chat Assistant (Weeks 1-2)**
    *   *Focus:* Terminal only. Async Ollama client with streaming. Basic prompt manager and CLI chat interface.

*   **v0.2: Voice Assistant (Weeks 2-3)**
    *   *Focus:* Full voice loop. `faster-whisper` (STT) -> LLM Stream -> Sentence Buffer -> `Piper TTS`. Push-to-talk first, streaming TTS implemented for <1.5s latency. Start with whisper-tiny for MVP (lowest latency/RAM). Upgrade path: tiny → base → small → medium.

*   **v0.3: Wake Word + Memory System (Weeks 3-4)**
    *   *Focus:* Persistence & Ambient listening. CPU-only `OpenWakeWord`. SQLite schema and ChromaDB setup. Context manager injects memories into prompts.

*   **v0.4: Tool Framework + Permission System (Weeks 4-5)**
    *   *Focus:* Actions & Safety. Custom plugin-like tool registry. SAFE/WARNING/DANGEROUS execution tags. Intent parser for fast-path command execution.

*   **v0.5: File Manager (Weeks 5-6)**
    *   *Focus:* Local file operations. Create, move, search. Smart cleanup tools. Safe execution with confirmation.

*   **v0.6: Desktop Automation (Weeks 6-7)**
    *   *Focus:* System control. App launching (PyAutoGUI/pywinauto), window management, system settings, keyboard/mouse macros.

*   **v0.7: Browser Automation (Weeks 7-8)**
    *   *Focus:* Web interaction. Playwright driver for navigation, DuckDuckGo search, scraping, and screenshotting.

*   **v0.8: Scheduling & Reminders (Weeks 8-9)**
    *   *Focus:* Background tasks. APScheduler integration for time/date tasks. Desktop notifications.

*   **v0.9: Vision System (Weeks 9-10)**
    *   *Focus:* Seeing the screen. Fast screencap (`mss`), text extraction (`EasyOCR`), and screen Q&A (`moondream2`). Memory management for VRAM constraints.

*   **v1.0: Desktop UI + Production Release (Weeks 10-12)**
    *   *Focus:* The Iron Man HUD. Tauri v2 + React desktop overlay connecting to the FastAPI WebSocket backend. Installer packaging.

### PHASE 2: Expansion (v1.1 - v1.4, Months 3-4)
*   **v1.1:** Android Companion (Flutter App).
*   **v1.2:** Knowledge Base (PDF ingestion, local docs).
*   **v1.3:** Local RAG (ChromaDB document retrieval).
*   **v1.4:** Workflow Engine (Multi-step tasks and automation chains).

### PHASE 3+: Ecosystem (v2.0 - v3.0, Month 5+)
*   **v2.0:** Full Plugin System (SDK, dynamic loading).
*   **v2.1:** Multi-Agent Framework (Specialized agents for coding, research, vision, coordinated together).
*   **v2.2:** Advanced Context Awareness (Workspace & project context).
*   **v2.3:** Learning System (Behavioral adaptation).
*   **v3.0:** AI Operating Companion (Cross-device, autonomous workflows).
