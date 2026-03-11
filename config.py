"""
Configuration management for SpeakType application.

This module handles loading and accessing configuration settings
from YAML files. It provides a clean interface for other components
to access their settings.
"""

import yaml
from pathlib import Path


class Config:
    def __init__(self, config_data):
        if not isinstance(config_data, dict):
            raise ValueError("Invalid config data, config data is not a dictionary")

        self.config = config_data
        print("Config data loaded")

    def get(self, key_path: str, default=None):
        tokens = key_path.split(".")
        first_token = tokens[0]

        if not first_token in self.config:
            return default

        value = self.config[first_token]

        if isinstance(value, dict) and len(tokens) > 1:
            return self.get(".".join(tokens[1:]), value)
        else:
            return value

    def get_whisper_config(self):
        if "whisper" not in self.config:
            raise ValueError("'whisper' key not found in config")

        return self.config["whisper"]

    def get_ollama_config(self):
        if "ollama" not in self.config:
            raise ValueError("'ollama' key not found in config")

        return self.get("ollama")

    def get_app_config(self):
        if "app" not in self.config:
            raise ValueError("'app' key not found in config")

        return self.get("app")


def load_config(config_path="config.yaml"):
    """
    Load configuration from a YAML file.
    Returns config object with loaded settings
    """

    config_file_path = Path(config_path)
    if not config_file_path.exists():
        raise Exception(f"Config file {config_path} not found.")

    with Path(config_path).open() as config_file:
        if config_file is None:
            raise Exception(f"Unable to load config file {config_path}")

        try:
            config_data = yaml.safe_load(config_file)
        except yaml.YAMLError as e:
            raise Exception(f"Error parsing YAML file {config_path}: {e}")
        except Exception as e:
            raise Exception(f"Error reading config file {config_path}: {e}")

        validate_config(config_data)

        return Config(config_data)


def validate_config(config_data):
    """
    Validate important configuration settings.
    Raises ValueError if any validation fails.
    """

    # Validate Whisper model
    valid_whisper_models = ["tiny", "base", "small", "medium", "large"]
    whisper_model = config_data.get("whisper", {}).get("model")
    if whisper_model is None or whisper_model not in valid_whisper_models:
        raise ValueError(
            f"Invalid Whisper model. {whisper_model} is not a valid model. Valid models: ${str(valid_whisper_models)}"
        )

    # Validate audio settings
    audio_config = config_data.get("audio", {})
    if "sample_rate" not in audio_config:
        raise ValueError("Audio sample rate not found in config")

    sample_rate = audio_config.get("sample_rate")
    if sample_rate <= 0:
        raise ValueError("Audio sample rate must be greater than 0")

    # Validate ollama settings
    ollama_config = config_data.get("ollama", {})
    if "host" not in ollama_config:
        raise ValueError("Ollama host not found in config")
    if "model" not in ollama_config:
        raise ValueError("Ollama model not found in config")
    if "prompt_template" not in ollama_config:
        raise ValueError("Ollama prompt_template not found in config")
