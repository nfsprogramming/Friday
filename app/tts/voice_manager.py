import os
import requests
from app.core.logger import logger

class VoiceManager:
    """Manages Piper TTS voice models."""
    def __init__(self, voices_dir="data/voices"):
        self.voices_dir = voices_dir
        os.makedirs(self.voices_dir, exist_ok=True)
        
        # We will use the 'lessac' voice (Professional Female) from your blueprint
        self.default_voice = "en_US-lessac-medium"
        self.base_url = f"https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/medium/{self.default_voice}"

    def get_voice_path(self, voice_name=None) -> str:
        """Returns the local path to the voice model, downloading it if necessary."""
        name = voice_name or self.default_voice
        onnx_path = os.path.join(self.voices_dir, f"{name}.onnx")
        json_path = os.path.join(self.voices_dir, f"{name}.onnx.json")

        if not os.path.exists(onnx_path) or not os.path.exists(json_path):
            logger.info(f"[TTS] Downloading voice model '{name}'...")
            self._download_file(f"{self.base_url}.onnx", onnx_path)
            self._download_file(f"{self.base_url}.onnx.json", json_path)
            logger.info("[TTS] Voice model downloaded successfully.")

        return onnx_path

    def _download_file(self, url: str, dest_path: str):
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(dest_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
