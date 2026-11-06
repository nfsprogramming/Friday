import sounddevice as sd
import soundfile as sf
import numpy as np
import time
import os
from app.stt.vad import VADEngine
from app.core.logger import logger

class MicrophoneManager:
    """Manages audio recording with Voice Activity Detection (VAD)."""
    def __init__(self, sample_rate=16000, channels=1):
        self.sample_rate = sample_rate
        self.channels = channels
        self.vad = VADEngine(aggressiveness=3)
        self.audio_dir = "data/audio"
        os.makedirs(self.audio_dir, exist_ok=True)
        
    def listen_and_record(self, output_filename="temp.wav", silence_duration=1.5) -> str:
        """
        Listens to the microphone continuously. 
        Starts recording when speech is detected.
        Stops recording after `silence_duration` seconds of silence.
        """
        logger.info("[Mic] Listening... (Speak now)")
        
        # WebRTCVAD requires 10, 20, or 30ms frames.
        # 30ms at 16000Hz = 480 samples
        frame_duration_ms = 30
        chunk_size = int(self.sample_rate * (frame_duration_ms / 1000.0))
        
        audio_buffer = []
        is_recording = False
        silence_start_time = None
        
        try:
            with sd.InputStream(samplerate=self.sample_rate, channels=self.channels, dtype='int16') as stream:
                while True:
                    # Read a 30ms chunk
                    audio_chunk, overflowed = stream.read(chunk_size)
                    
                    if overflowed:
                        logger.warning("[Mic] Audio buffer overflowed.")
                        
                    # Flatten and convert to bytes for VAD
                    chunk_data = audio_chunk.flatten()
                    chunk_bytes = chunk_data.tobytes()
                    
                    # Check for speech
                    is_speech = self.vad.is_speech(chunk_bytes, self.sample_rate)
                    
                    if is_speech:
                        if not is_recording:
                            logger.info("[Mic] Speech detected. Recording started...")
                            is_recording = True
                        
                        audio_buffer.append(chunk_data)
                        silence_start_time = None # Reset silence timer
                        
                    else:
                        if is_recording:
                            # We are recording, but heard silence. Append it (natural pauses).
                            audio_buffer.append(chunk_data)
                            
                            # Start or check silence timer
                            if silence_start_time is None:
                                silence_start_time = time.time()
                            elif (time.time() - silence_start_time) > silence_duration:
                                logger.info(f"[Mic] {silence_duration}s of silence. Recording stopped.")
                                break
        except Exception as e:
            logger.error(f"[Mic] Microphone error: {e}")
            return None
            
        # If we exited the loop and have audio, save it
        if len(audio_buffer) > 0:
            output_path = os.path.join(self.audio_dir, output_filename)
            # Concatenate all chunks into a single numpy array
            recording = np.concatenate(audio_buffer)
            sf.write(output_path, recording, self.sample_rate)
            return output_path
            
        return None
