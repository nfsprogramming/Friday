# F.R.I.D.A.Y - Installation Guide

## Prerequisites
- Git
- Python 3.12+ (or UV package manager)
- Ollama
- Flutter (Optional, for Android app)
- Visual Studio Code (Optional, but recommended)

## Phase 0: Environment Setup (Day 2)

This project uses `uv`, an extremely fast Python package and project manager written in Rust.

### 1. Initialize Project & Install Dependencies
Run the following from the root directory. This will resolve and install all dependencies defined in `pyproject.toml` into a local virtual environment (`.venv`).

```bash
uv add fastapi uvicorn faster-whisper piper-tts openwakeword pyaudio psutil duckduckgo-search chromadb sentence-transformers apscheduler playwright easyocr opencv-python mss
```

*(Note: PyAudio may require additional build tools on Windows, or you can install the precompiled wheel using pipx/uv pip if it fails)*

### 2. Local LLM Setup
1. Download and install [Ollama](https://ollama.com).
2. Ensure the Ollama app is running in the background.
3. Open a terminal and pull our primary model (Qwen 2.5 7B, 4-bit quantized):
```bash
ollama pull qwen2.5:7b-instruct-q4_K_M
```

### 3. Verify the Installation
We have provided test scripts to ensure your environment is set up correctly:

**Test 1: FastAPI Backend**
```bash
uv run uvicorn app.main:app --reload
```
Navigate to `http://127.0.0.1:8000`. You should see `{"message": "FRIDAY ONLINE"}`.

**Test 2: Ollama Connection**
```bash
uv run test_ollama.py
```
This script will ping your local Ollama instance and ask "Hello FRIDAY, are you online?". If successful, it prints the response text.
