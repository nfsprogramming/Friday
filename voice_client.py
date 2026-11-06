import asyncio
import httpx
import os
import sys
import re
import numpy as np
import time
import sounddevice as sd
import soundfile as sf
import logging

# Ensure the app module can be found
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.stt.whisper_engine import WhisperEngine
from app.stt.vad import VADEngine
from app.tts.speech_queue import SpeechQueue
from app.wakeword.detector import WakeWordDetector
from app.wakeword.state_manager import AssistantState
from app.core.logger import logger

# Hide background INFO logs
logger.setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)

class FridayAmbientSystem:
    def __init__(self):
        print("\n--- Initializing F.R.I.D.A.Y. Ambient System ---")
        self.state = AssistantState.IDLE
        self.whisper = WhisperEngine(model_name="base")
        self.speech_q = SpeechQueue()
        # Lowered threshold from 0.5 to 0.15 to make it highly sensitive to your normal speaking volume
        self.wakeword = WakeWordDetector(threshold=0.15)
        self.vad = VADEngine(aggressiveness=3)
        self.sample_rate = 16000
        
        # Audio chunk size for WebRTCVAD (30ms = 480 samples)
        self.vad_chunk_size = int(self.sample_rate * (30 / 1000.0)) 
        
        print("--- System Ready. Say 'Hey Jarvis' to activate. Press Ctrl+C to exit. ---\n")
        print("[State: IDLE] Waiting for wake word...")

    def run(self):
        try:
            with sd.InputStream(samplerate=self.sample_rate, channels=1, dtype='int16') as stream:
                while True:
                    if self.state == AssistantState.IDLE:
                        # Feed 1280 samples for OpenWakeWord detection (80ms)
                        audio_chunk, overflowed = stream.read(1280)
                        
                        if self.wakeword.detect(audio_chunk.flatten()):
                            print("\n[FRIDAY]: Yes Sir?")
                            self.speech_q.speak("Yes Sir?")
                            self.speech_q.wait_until_done()
                            
                            self.state = AssistantState.LISTENING
                            print("[State: LISTENING] Speak your command...")
                            
                            # Flush stream so we don't process leftover audio
                            stream.read(stream.read_available)
                            
                    elif self.state == AssistantState.LISTENING:
                        # VAD Pipeline: Record until 1.5 seconds of silence
                        audio_buffer = []
                        is_recording = False
                        silence_start_time = None
                        
                        while True:
                            audio_chunk, _ = stream.read(self.vad_chunk_size)
                            chunk_data = audio_chunk.flatten()
                            is_speech = self.vad.is_speech(chunk_data.tobytes(), self.sample_rate)
                            
                            if is_speech:
                                if not is_recording:
                                    is_recording = True
                                audio_buffer.append(chunk_data)
                                silence_start_time = None # Reset silence timer
                            else:
                                if is_recording:
                                    audio_buffer.append(chunk_data)
                                    if silence_start_time is None:
                                        silence_start_time = time.time()
                                    elif (time.time() - silence_start_time) > 1.5:
                                        break # 1.5 seconds of silence detected
                                        
                        if len(audio_buffer) > 0:
                            self.state = AssistantState.THINKING
                            print("[State: THINKING] Processing...")
                            
                            # Save temporary audio file for Whisper
                            os.makedirs("data/audio", exist_ok=True)
                            recording = np.concatenate(audio_buffer)
                            sf.write("data/audio/command.wav", recording, self.sample_rate)
                            
                            text = self.whisper.transcribe("data/audio/command.wav")
                            if text and len(text.strip()) > 1:
                                asyncio.run(self.process_chat(text))
                            else:
                                print("\n[Whisper] Could not understand audio.")
                                
                        self.state = AssistantState.IDLE
                        print("\n[State: IDLE] Waiting for 'Hey Jarvis'...")
                        # Flush stream and reset detector to prevent stale state
                        if stream.read_available > 0:
                            stream.read(stream.read_available)
                        self.wakeword.reset()

        except KeyboardInterrupt:
            print("\nExiting FRIDAY...")
            sys.exit(0)

    async def process_chat(self, text: str):
        self.state = AssistantState.SPEAKING
        print(f"\n[You]: {text}")
        print("[FRIDAY]: ", end="", flush=True)
        url = "http://127.0.0.1:8000/api/chat"
        payload = {"session_id": "voice_user_1", "message": text, "stream": True}
        
        try:
            async with httpx.AsyncClient() as client:
                async with client.stream("POST", url, json=payload, timeout=120.0) as response:
                    if response.status_code == 200:
                        sentence_buffer = ""
                        async for chunk in response.aiter_text():
                            print(chunk, end="", flush=True)
                            sentence_buffer += chunk
                            
                            # Stream sentences to TTS queue
                            match = re.search(r'(?<=[.!?])\s+|\n', sentence_buffer)
                            if match:
                                end_idx = match.end()
                                self.speech_q.speak(sentence_buffer[:end_idx])
                                sentence_buffer = sentence_buffer[end_idx:]
                                
                        # Flush remainder
                        if sentence_buffer.strip():
                            self.speech_q.speak(sentence_buffer)
                        print("\n")
                        
                        # Wait for TTS to finish speaking
                        self.speech_q.wait_until_done()
                    else:
                        print(f"\n[API Error]: {response.status_code}")
        except Exception as e:
            print(f"\n[Error] {e}")

if __name__ == "__main__":
    system = FridayAmbientSystem()
    system.run()
