import sounddevice as sd
import numpy as np
from app.core.logger import logger

class AudioPlayer:
    """Plays raw PCM audio arrays using sounddevice."""
    def __init__(self, sample_rate=16000):
        self.sample_rate = sample_rate

    def play(self, audio_data: np.ndarray):
        """Plays the audio data and blocks until finished."""
        if len(audio_data) == 0:
            return
            
        try:
            sd.play(audio_data, samplerate=self.sample_rate)
            sd.wait() # Block until audio finishes playing
        except Exception as e:
            logger.error(f"[AudioPlayer] Failed to play audio: {e}")
