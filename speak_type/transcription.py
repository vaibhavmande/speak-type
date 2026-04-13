"""
Speech-to-text transcription using OpenAI Whisper.

This module handles loading Whisper models and transcribing audio data.
It provides a clean interface for converting speech to text.
"""

import whisper
import traceback
from pathlib import Path


class WhisperTranscriber:

    def __init__(self, config):
        self.config = config.config
        self.whisper_config = config.get_whisper_config()
        self.model = None
        self.model_loaded = False
        self.models_dir = Path("models")
        self.models_dir.mkdir(exist_ok=True)

    def load_model(self):
        if self.model_loaded:
            return True

        try:
            model_name = self.whisper_config.get("model", "base")
            model_device = self.whisper_config.get("device", "cpu")

            self.model = whisper.load_model(model_name, device=model_device)
            self.model_loaded = True
            return True

        except Exception as e:
            print(f"Failed to load model: {e}")
            traceback.print_exc()
            return False

    def transcribe(self, audio_data, language):
        if not self.model_loaded:
            if not self.load_model():
                return None

        if audio_data is None or len(audio_data) == 0:
            print("No audio data provided for transcription")
            return None

        try:
            result = self.model.transcribe(audio_data, language=language, fp16=False)
            transcribed_text = result.get("text", "").strip()
            return transcribed_text if transcribed_text else None

        except Exception as e:
            print(f"Error during transcription: {e}")
            traceback.print_exc()
            return None

    def unload_model(self):
        if self.model_loaded:
            del self.model
            self.model = None
            self.model_loaded = False
            import gc

            gc.collect()
