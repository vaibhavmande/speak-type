"""
Speech-to-text transcription using OpenAI Whisper.

This module handles loading Whisper models and transcribing audio data.
It provides a clean interface for converting speech to text.

LEARNING NOTE: This file demonstrates:
- Using OpenAI Whisper for speech recognition
- Model loading and management
- Audio transcription with different models
- Memory management for ML models
"""

from numba.cuda import fp16
import whisper
import traceback

# TODO: Import numpy for audio data handling
# import numpy as np

from pathlib import Path


class WhisperTranscriber:
    """
    Handles speech-to-text transcription using OpenAI Whisper models.

    LEARNING NOTE: This class shows how to:
    - Load and manage ML models
    - Process audio data for transcription
    - Handle different model sizes and languages
    - Clean up resources properly
    """

    def __init__(self, config):
        """
        Initialize the transcriber with configuration.

        Args:
            config: Configuration object with whisper settings

        TODO: Implement this method to:
        1. Store config as instance variable
        2. Extract whisper settings (model, language, device)
        3. Initialize model variable to None
        4. Set model_loaded flag to False
        5. Create models directory path if it doesn't exist
        """
        self.config = config.config
        self.whisper_config = config.get_whisper_config()
        self.model = None
        self.model_loaded = False
        self.models_dir = Path("models")
        self.models_dir.mkdir(exist_ok=True)
        pass

    def load_model(self):
        """
        Load the Whisper model into memory.
        """

        if self.model_loaded:
            return True

        try:
            # get name and device
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
        """
        Transcribe audio data to text.

        Args:
            audio_data: numpy array containing audio samples

        Returns:
            Transcribed text string, or None if error

        LEARNING NOTE: This method demonstrates:
        - Using ML models for inference
        - Audio data preprocessing
        - Language detection and specification
        - Error handling for transcription

        TODO: Implement this method to:
        1. Check if model is loaded (load it if not)
        2. Get transcription settings from config (language, etc.)
        3. Use model.transcribe() to convert audio to text
        4. Extract the text result
        5. Return the transcribed text
        6. Handle errors gracefully (return None)
        """

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

    def transcribe_file(self, audio_file_path):
        """
        Transcribe audio from a file path.

        Args:
            audio_file_path: Path to audio file

        Returns:
            Transcribed text string, or None if error

        LEARNING NOTE: This method demonstrates:
        - File-based audio processing
        - Path validation
        - Different input formats for transcription

        TODO: Implement this method to:
        1. Check if file exists and is readable
        2. Check if model is loaded (load it if not)
        3. Use model.transcribe() with file path
        4. Return the transcribed text
        5. Handle file errors gracefully
        """
        pass

    def get_supported_languages(self):
        """
        Get list of supported languages for transcription.

        Returns:
            List of language codes (e.g., ['en', 'es', 'fr'])

        LEARNING NOTE: This method demonstrates:
        - Accessing model metadata
        - Providing user-friendly information

        TODO: Implement this method to:
        1. Check if model is loaded (load it if not)
        2. Access model's supported languages
        3. Return list of language codes
        """
        pass

    def unload_model(self):
        """
        Unload the model from memory to free resources.

        LEARNING NOTE: This method demonstrates:
        - Memory management for ML models
        - Resource cleanup
        - State management

        TODO: Implement this method to:
        1. Check if model is loaded
        2. Delete the model instance
        3. Set model_loaded flag to False
        4. Force garbage collection to free memory
        """
        if self.model_loaded:
            del self.model
            self.model = None
            self.model_loaded = False
            import gc

            gc.collect()

    def get_model_info(self):
        """
        Get information about the currently loaded model.

        Returns:
            Dictionary with model information

        TODO: Implement this method to:
        1. Check if model is loaded
        2. Return dictionary with model info:
           - model_name: Name of the model
           - is_loaded: Whether model is loaded
           - device: CPU or GPU
        3. Return empty dict if no model loaded
        """
        pass

    def is_model_loaded(self):
        """
        Check if a model is currently loaded.

        Returns:
            True if model is loaded, False otherwise

        TODO: Implement this method to:
        1. Return the current model_loaded flag
        """
        pass
