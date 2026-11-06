# F.R.I.D.A.Y - Features

## Core Capabilities

F.R.I.D.A.Y offers a comprehensive suite of local AI capabilities, developed incrementally:

1. **Local Chat Assistant**
   - Asynchronous, streaming responses via Ollama.
   - Conversation history and context management.

2. **Voice Pipeline**
   - Speech-to-Text via `faster-whisper`.
   - Text-to-Speech via `Piper TTS` with sentence-streaming queue for ultra-low latency.
   - Always-on wake word detection via `OpenWakeWord` running efficiently on CPU.

3. **Memory System**
   - **Short-term/Active**: Conversation context.
   - **Long-term**: SQLite for facts/preferences and ChromaDB with Sentence Transformers for semantic search and retrieval.

4. **Tool Framework & Safety**
   - Custom JSON tool calling via Ollama native function calling.
   - Strict Permission System: Actions are tagged as SAFE (auto-execute), WARNING (prompt confirmation), or DANGEROUS (explicit approval required).
   - Fast-path regex execution for top commands to skip the LLM entirely.

5. **Local File Management**
   - Create, move, duplicate, and search files locally.
   - Smart storage analysis and cleanup recommendations.

6. **Desktop Automation**
   - Control apps, switch windows, manage volume/brightness.
   - Keyboard and mouse macros.
   - Direct game launching (Steam, specific exes).

7. **Browser Automation**
   - `Playwright`-powered web control.
   - Search via DuckDuckGo, form filling, and page summaries.

8. **Scheduling & Reminders**
   - Background jobs via `APScheduler`.
   - Time/date recurring reminders with desktop notifications.

9. **Vision System**
   - Screen capture (`mss`), OCR (`EasyOCR`), and Image Analysis (`OpenCV`).
   - Natural language screen understanding powered by `moondream2` via Ollama.

10. **Custom UI**
    - Desktop overlay using Tauri v2 + React with an Iron Man-style HUD aesthetic.
    - Live system metrics, voice waveform, and chat log panel.
