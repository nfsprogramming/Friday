# F.R.I.D.A.Y - Technology Stack

## Core Technologies

These choices are finalized. They are selected based on the specific hardware constraints (RTX 4050, 6GB VRAM) and the goal of a 100% local, low-latency assistant.

### AI Models
*   **LLM:** Qwen2.5-7B-Instruct Q4_K_M (via Ollama)
    *   *Why:* Best tool-calling and coding at 7B. Fits within the ~5.5GB VRAM budget. Llama 3.2 is weaker at instructions; Gemma 2 lacks function calling.
*   **Speech-to-Text (STT):** faster-whisper
    *   *Why:* Start with `whisper-tiny` for MVP (lowest latency/RAM), upgrade to `medium`. CTranslate2 backend is 4x faster than original Whisper.
*   **Text-to-Speech (TTS):** Piper TTS (en_US-ryan-high)
    *   *Why:* Fastest local TTS (<100ms latency). The 'Ryan' voice closely matches a composed assistant tone.
*   **Vision:** moondream2 (1.8B) via Ollama — primary. LLaVA-1.5-7B-Q4 available as a quality upgrade swap only. Cannot run simultaneously with Qwen2.5-7B on 6GB VRAM — must unload LLM before loading vision model.
    *   *Why:* Fast natural language screen Q&A. moondream2 is extremely lightweight.
*   **Embeddings:** Sentence Transformers (`all-MiniLM-L6-v2`)
    *   *Why:* Powers ChromaDB semantic search. Fast, lightweight, and runs entirely on the CPU.
*   **Wake Word:** OpenWakeWord
    *   *Why:* Runs on CPU with <1% usage. Highly accurate and allows training a custom "Hey Friday" model.

### Backend & Infrastructure
*   **Language & Framework:** Python 3.11 + FastAPI
    *   *Why:* Native async/WebSocket support. Best AI ecosystem. Configuration via YAML and `.env`.
*   **Memory / Database:** SQLite + ChromaDB
    *   *Why:* SQLite for structured data (facts, preferences, tasks, logs). ChromaDB for semantic memory search. Both are embedded and require zero extra infrastructure.
*   **Scheduler:** APScheduler
    *   *Why:* Handles reminders, recurring tasks, background jobs. Runs embedded in Python without a separate process.

### Automation
*   **Desktop Automation:** PyAutoGUI -> pywinauto
    *   *Why:* PyAutoGUI for the MVP (mouse/keyboard/windows). Upgrade path to pywinauto for robust Windows API control. `psutil` used for system metrics.
*   **Browser Automation:** Playwright
    *   *Why:* Modern, stable, fast. Supports Chromium, Firefox, and Edge. Superior to Selenium for this use case.
*   **Vision/OCR Tasks:** OpenCV + EasyOCR
    *   *Why:* OpenCV for preprocessing and object detection. EasyOCR for pure text extraction (faster than using the LLM for simple OCR).

### Clients
*   **Desktop UI:** Tauri v2 + React
    *   *Why:* Familiar tech stack. Native OS access. Rust sidecar for tasks like running Piper. No Electron bloat.
*   **Mobile:** Flutter
    *   *Why:* Reuses existing setup (from SpotiFLAC). Single codebase that connects via the same WebSockets as the desktop client.

### Framework Rules
*   **Tool Calling:** Custom JSON tool calling (Ollama format) + Custom Permission Layer.
    *   *Why:* Directly interacts with Qwen2.5 tool schemas. Explicit risk levels (SAFE/WARNING/DANGEROUS). **NO LangChain or LlamaIndex.** Abstractions add latency and hide operations.

### Future
*   **Plugin Architecture:** Custom Python Plugin System (Targeting v2.0+)
    *   *Why:* To allow dynamic loading, hot reloading, and permission isolation for future community features.
