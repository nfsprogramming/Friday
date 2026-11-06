from piper.voice import PiperVoice
from app.tts.voice_manager import VoiceManager
from app.core.logger import logger
import numpy as np

class PiperEngine:
    """Handles Text-to-Speech synthesis using Piper."""
    def __init__(self):
        logger.info("[TTS] Initializing Voice Engine...")
        self.manager = VoiceManager()
        model_path = self.manager.get_voice_path()
        self.voice = PiperVoice.load(model_path)
        logger.info("[TTS] Voice Engine loaded.")

    def synthesize(self, text: str) -> np.ndarray:
        """Synthesizes text into a numpy audio array (16kHz, 16-bit mono PCM)."""
        if not text.strip():
            return np.array([], dtype=np.int16)
            
        audio_arrays = []
        # synthesize() returns an iterable of AudioChunk objects
        for chunk in self.voice.synthesize(text):
            audio_arrays.append(chunk.audio_int16_array)
            
        if not audio_arrays:
            return np.array([], dtype=np.int16)
            
        return np.concatenate(audio_arrays)
