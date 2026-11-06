# F.R.I.D.A.Y - Project Structure

## Repository Layout

```
FRIDAY/
│
├── README.md  ·  LICENSE  ·  .gitignore  ·  pyproject.toml  ·  config.yaml  ·  .env
│
├── docs/                        # VISION.md · ARCHITECTURE.md · FEATURES.md · ROADMAP.md · API.md · SECURITY.md
│
├── app/
│   ├── main.py                  # FastAPI app entry + WebSocket hub
│   │
│   ├── core/                    # Brain of FRIDAY
│   │   ├── assistant.py         # Top-level orchestration loop
│   │   ├── orchestrator.py      # Routes between direct cmd / LLM / vision paths
│   │   ├── session_manager.py   # Active conversation state
│   │   ├── context_manager.py   # Memory injection into prompts
│   │   ├── intent_parser.py     # Regex + keyword fast-path routing
│   │   └── task_planner.py      # Multi-step task decomposition (v0.4+)
│   │
│   ├── llm/                     # Local AI model communication
│   │   ├── ollama_client.py     # Async Ollama client + streaming
│   │   ├── prompt_manager.py    # System prompts + FRIDAY personality
│   │   ├── model_router.py      # Switch models dynamically (chat vs vision)
│   │   └── response_generator.py# Streaming token handler + sentence chunker
│   │
│   ├── voice/                   # Speech recognition and synthesis
│   │   ├── wakeword.py          # OpenWakeWord listener (CPU, always-on)
│   │   ├── whisper_stt.py       # faster-whisper wrapper (tiny → medium)
│   │   ├── piper_tts.py         # Piper wrapper + streaming sentence queue
│   │   ├── microphone.py        # PyAudio capture
│   │   └── audio_manager.py     # VAD, mode switching (wake/listen/speak)
│   │
│   ├── memory/                  # Long-term and short-term memory
│   │   ├── memory_manager.py    # Unified memory interface
│   │   ├── conversation_memory.py# Active session + history
│   │   ├── knowledge_memory.py  # ChromaDB semantic store
│   │   ├── preference_memory.py # SQLite user prefs + facts
│   │   └── embeddings.py        # Sentence Transformers (all-MiniLM-L6)
│   │
│   ├── tools/                   # Tool registration and execution
│   │   ├── tool_manager.py      # Tool registry + discovery
│   │   ├── registry.py          # All tools registered here
│   │   ├── permissions.py       # SAFE / WARNING / DANGEROUS risk levels
│   │   └── executor.py          # Executes tools + approval flow
│   │
│   ├── automation/              # Desktop and browser control
│   │   ├── desktop/
│   │   │   ├── app_control.py   # open/close/restart apps (PyAutoGUI → pywinauto)
│   │   │   ├── keyboard.py      # Typing, shortcuts, macros
│   │   │   ├── mouse.py         # Click, drag, scroll
│   │   │   ├── window_manager.py# Switch, minimize, maximize windows
│   │   │   └── system_control.py# Volume, brightness, shutdown, sleep
│   │   └── browser/
│   │       ├── browser_control.py# Tab management, navigation
│   │       ├── web_search.py    # DuckDuckGo + Playwright search
│   │       ├── scraper.py       # Data extraction
│   │       └── playwright_driver.py# Playwright browser instance
│   │
│   ├── vision/                  # OCR and screen understanding
│   │   ├── screenshot.py        # mss screen capture
│   │   ├── ocr.py               # EasyOCR text extraction
│   │   ├── image_analysis.py    # OpenCV processing
│   │   └── screen_understanding.py# moondream2 natural language Q&A
│   │
│   ├── scheduler/               # Reminders and automation scheduling
│   │   ├── reminders.py         # Time/date-based + recurring reminders
│   │   ├── jobs.py              # Background jobs
│   │   └── task_scheduler.py    # APScheduler wrapper
│   │
│   ├── notifications/
│   │   ├── desktop_notifications.py
│   │   └── mobile_notifications.py
│   │
│   ├── plugins/                 # Plugin framework (v2.0+)
│   │   ├── plugin_manager.py
│   │   ├── plugin_loader.py     # Dynamic loading + hot reload
│   │   └── sdk/                 # Plugin developer kit
│   │
│   ├── api/                     # Android + future web interface
│   │   ├── server.py
│   │   ├── routes/
│   │   └── middleware/
│   │
│   └── utils/
│       ├── logger.py            # app · error · actions · security logs
│       ├── config.py            # YAML + .env loader
│       ├── helpers.py
│       └── constants.py
│
├── data/
│   ├── database/friday.db       # SQLite
│   ├── memories/                # conversations · preferences · knowledge
│   ├── embeddings/              # ChromaDB vector store
│   ├── cache/
│   └── backups/
│
├── models/
│   ├── whisper/                 # faster-whisper model files
│   ├── piper/                   # en_US-ryan-high.onnx + config
│   └── wakeword/                # OpenWakeWord model files
│
├── logs/                        # app.log · errors.log · actions.log · security.log
├── tests/                       # test_memory · test_voice · test_tools · test_llm · test_automation
│
├── frontend/                    # Tauri v2 + React desktop overlay (build in Phase 5)
│   ├── src-tauri/
│   └── src/
│       ├── components/
│       │   ├── HUD.tsx         # Iron Man-style HUD
│       │   ├── VoiceWave.tsx
│       │   └── SystemPanel.tsx
│       └── hooks/useWebSocket.ts
│
├── android/                     # Flutter companion app
│   ├── lib/
│   │   ├── services/ws_service.dart
│   │   └── screens/chat_screen.dart
│   └── pubspec.yaml
│
├── plugins_store/               # calendar · email · notes · custom plugins
│
└── future/                      # Experimental — don't touch until v1.0 is done
    ├── agents/                  # coding · research · vision · automation agents
    ├── rag/                     # PDF ingestion + local knowledge base
    └── cloud_sync/              # Future multi-device (PostgreSQL)
```
