import openwakeword
from openwakeword.model import Model
from app.core.logger import logger
import numpy as np

class WakeWordDetector:
    def __init__(self, threshold=0.5):
        logger.info("[WakeWord] Downloading/Loading 'hey_jarvis' model...")
        openwakeword.utils.download_models()
        # We use hey_jarvis as the default highly-accurate model
        self.oww_model = Model(wakeword_models=["hey_jarvis"], inference_framework="onnx")
        self.threshold = threshold
        logger.info("[WakeWord] Ready.")

    def detect(self, audio_chunk: np.ndarray) -> bool:
        """Processes 16-bit 16kHz audio chunk. Returns True if wake word detected."""
        prediction = self.oww_model.predict(audio_chunk)
        # prediction is a dict like {"hey_jarvis_v0.1": 0.95}
        for key, score in prediction.items():
            if score >= self.threshold:
                return True
        return False

    def reset(self):
        """Clears the internal audio buffer to prevent stale wake word detection."""
        self.oww_model.reset()
