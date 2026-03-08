"""
Configuration management for SpeakType application.

This module handles loading and accessing configuration settings
from YAML files. It provides a clean interface for other components
to access their settings.

LEARNING NOTE: This file demonstrates:
- Working with YAML files
- Creating configuration classes
- Using dot-notation for nested settings
- Input validation and error handling
"""

# TODO: Import the yaml library for parsing YAML files
# Install with: pip install PyYAML
from multiprocessing import Value
import yaml

# TODO: Import pathlib for working with file paths
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
            return self.get(".".join(token[1:]), value)
        else:
            return value

    def get_whisper_config(self):
        if "whisper" in self.config:
            whisper_config = self.config.whisper
            return whisper_config

        raise ValueError("'whisper' key not found in config")

    def get_ollama_config(self):
        """
        Get Ollama-specific configuration.

        Returns:
            Dictionary with ollama settings (host, model, prompt, etc.)

        TODO: Implement this method to:
        1. Use self.get() to retrieve ollama configuration
        2. Return a dictionary with keys like 'host', 'model', 'prompt_template'
        3. Provide sensible defaults if settings are missing
        """
        pass


def load_config(config_path="config.yaml"):
    """
    Load configuration from a YAML file.
    Returns config object with loaded settings
    """

    config_file = open_file(config_path)
    if config_file is None:
        print(f"Config file {config_path} not found. Using default configuration.")
        return None

    try:
        config_data = yaml.safe_load(config_file)
        config_data_dict = yaml.to_dict(config_data)
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file {config_path}: {e}")
        return None
    except Exception as e:
        print(f"Error reading config file {config_path}: {e}")
        return None

    validate_config(config_data_dict)

    return Config(config_data_dict)


def validate_config(config_data):
    """
    Validate important configuration settings.
    Raises ValueError if any validation fails.
    """

    # Validate Whisper model
    valid_whisper_models = ["tiny", "base", "small", "medium", "large"]
    whisper_model = config_data.get("whisper", {}).get("model")
    if whisper_model not in valid_whisper_models:
        raise ValueError(
            f"Invalid Whisper model. ${whisper_model} is not a valid model. Valid models: ${str(valid_whisper_models)}"
        )

    # Validate audio settings
    sample_rate = config_data.get("audio", {}).get("sample_rate")
    if sample_rate is None:
        raise ValueError("Audio sample rate not found in config")

    if sample_rate <= 0:
        raise ValueError("Audio sample rate must be greater than 0")
