# F.R.I.D.A.Y - Architecture

## Full System Architecture

F.R.I.D.A.Y is structured into three main layers: Client, Backend Core, and Memory. It operates entirely locally, utilizing a FastAPI backend communicating with clients via WebSockets.

### Layer Diagram

```
CLIENT LAYER
  Tauri/React (Desktop UI) <---> Flutter Mobile (Android Companion)
         |                              |
         |                              |
         +------------------------------+
                       | WebSocket (ws://localhost:8000)
                       v
BACKEND CORE (FastAPI)
  [Wake Word Detector (OpenWakeWord)] --> [Audio Input (microphone)]
                                                 |
                                                 v
                                          [faster-whisper (STT)]
                                                 | text
                                                 v
                                          [INTENT ROUTER (rule + LLM)]
                                                 |
         +---------------------------------------+---------------------------------------+
         |                                       |                                       |
         v                                       v                                       v
[DIRECT CMD (fast path, no LLM)]      [LLM+TOOLS (Qwen2.5-7B/Ollama)]       [VISION (moondream2)]
         |                                       |                                       |
         +---------------------------------------+---------------------------------------+
                                                 |
                                                 v
                                          [TOOL MANAGER]
                                                 |
     +----------+----------+----------+----------+----------+
     v          v          v          v          v          v
[SYS MON]  [FILES MGMT] [WEB SRCH] [GAMES]  [STEAM]    [MEMORY]
                                                 |
                                                 v
                                          [PIPER TTS]
                                                 | audio
                                                 v
                                             🔊 Speaker

MEMORY LAYER
  SQLite (facts/prefs/tasks/history)  <--->  ChromaDB (semantic search/RAG knowledge)
```

### Voice Pipeline & Streaming TTS Latency Trick

To achieve the JARVIS latency target (<1.5s), the architecture relies on Streaming TTS.
Instead of waiting for the LLM (Qwen2.5-7B) to finish generating a complete response, F.R.I.D.A.Y buffers tokens as they arrive. When a sentence boundary (like a period, exclamation mark, or comma) is detected, that chunk is immediately sent to the Piper TTS queue to be spoken. 

This means F.R.I.D.A.Y begins speaking while the LLM is still generating the rest of the response, cutting perceived latency by 40–60%.

### Technology Stack Decisions

- **LLM**: Qwen2.5-7B-Instruct Q4_K_M via Ollama (Best tool calling at 7B, fits in 5.5GB VRAM constraint).
- **STT**: faster-whisper (Fastest local STT, start tiny, upgrade to medium).
- **TTS**: Piper TTS (en_US-ryan-high) (Fast, low latency, composed voice).
- **Backend**: Python 3.11 + FastAPI (Async WebSocket support).
- **Memory DB**: SQLite + ChromaDB (Structured facts vs Semantic search).
- **Embeddings**: Sentence Transformers - all-MiniLM-L6-v2 (Fast, CPU-based).
- **Wake Word**: OpenWakeWord (Lightweight, CPU-based).
- **Desktop UI**: Tauri v2 + React (Native OS access, low overhead).
- **Mobile**: Flutter (Cross-platform companion).
- **Desktop Automation**: PyAutoGUI -> pywinauto (Progressive enhancement for control).
- **Browser Automation**: Playwright (Modern, fast).
- **Vision**: OpenCV + EasyOCR + moondream2 (Task-split approach for efficiency).
- **Scheduler**: APScheduler (Embedded Python scheduling).
- **Tool System**: Custom JSON tool calling (Ollama format) with strict Permission layer.
