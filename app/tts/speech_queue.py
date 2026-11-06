import threading
import queue
from app.tts.piper_engine import PiperEngine
from app.tts.audio_player import AudioPlayer

class SpeechQueue:
    """Manages sequential audio synthesis and playback in the background."""
    def __init__(self):
        self.q = queue.Queue()
        self.piper = PiperEngine()
        self.player = AudioPlayer()
        
        self.worker_thread = threading.Thread(target=self._worker, daemon=True)
        self.worker_thread.start()
        
    def speak(self, text: str):
        """Adds a sentence to the TTS queue to be spoken aloud."""
        if text and text.strip():
            self.q.put(text.strip())
            
    def wait_until_done(self):
        """Blocks until all queued speech is finished."""
        self.q.join()
            
    def _worker(self):
        while True:
            text = self.q.get()
            if text is None:
                break # Exit signal
            
            # Synthesize text to audio
            audio_data = self.piper.synthesize(text)
            
            # Play audio blockingly
            self.player.play(audio_data)
            
            self.q.task_done()
