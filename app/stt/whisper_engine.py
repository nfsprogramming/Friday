import whisper
import os
from app.core.logger import logger

class WhisperEngine:
    """Wraps OpenAI Whisper for Speech-to-Text transcription."""
    def __init__(self, model_name="base"):
        logger.info(f"[Whisper] Loading '{model_name}' model... This might take a moment.")
        # Load the model on CPU by default to save VRAM for Ollama
        self.model = whisper.load_model(model_name)
        logger.info("[Whisper] Model loaded successfully.")
        
    def transcribe(self, audio_path: str) -> str:
        """Transcribes a saved .wav file to text."""
        if not os.path.exists(audio_path):
            logger.error(f"[Whisper] Audio file not found: {audio_path}")
            return ""
            
        logger.info("[Whisper] Transcribing audio...")
        try:
            # fp16=False to avoid warnings on CPU
            result = self.model.transcribe(audio_path, fp16=False)
            text = result["text"].strip()
            logger.info(f"[Whisper] Transcribed: '{text}'")
            return text
        except Exception as e:
            logger.error(f"[Whisper] Transcription failed: {e}")
            return ""
