import webrtcvad

class VADEngine:
    """Wrapper for WebRTC Voice Activity Detection."""
    def __init__(self, aggressiveness=3):
        # Aggressiveness: 0 is least aggressive (more noise), 3 is most aggressive (cuts out noise)
        self.vad = webrtcvad.Vad(aggressiveness)
        
    def is_speech(self, frame: bytes, sample_rate: int = 16000) -> bool:
        """
        Determines if an audio frame contains human speech.
        Frame must be 10ms, 20ms, or 30ms of audio.
        For 16000Hz, 16-bit audio:
        10ms = 160 samples = 320 bytes
        20ms = 320 samples = 640 bytes
        30ms = 480 samples = 960 bytes
        """
        try:
            return self.vad.is_speech(frame, sample_rate)
        except Exception:
            return False
