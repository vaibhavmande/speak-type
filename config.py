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
import yaml

# TODO: Import pathlib for working with file paths
from pathlib import Path

class Config:
    """
    Configuration class that provides access to settings using dot-notation.
    
    LEARNING NOTE: This class shows how to:
    - Store nested configuration data
    - Provide a clean API for accessing settings
    - Handle default values gracefully
    """
    
    def __init__(self, config_data):
        """
        Initialize the Config object with configuration data.
        
        Args:
            config_data: Dictionary containing all configuration settings
            
        TODO: Implement this method to:
        1. Store config_data as an instance variable
        2. Validate that it's a dictionary
        3. Print a message showing config was loaded successfully
        """
        pass
    
    def get(self, key_path, default=None):
        """
        Get a configuration value using dot-notation.
        
        Args:
            key_path: String like "whisper.model" or "ollama.host"
            default: Value to return if key is not found
            
        Returns:
            The configuration value or default
            
        LEARNING NOTE: This method demonstrates:
        - Parsing dot-notation strings
        - Navigating nested dictionaries
        - Providing fallback values
        
        TODO: Implement this method to:
        1. Split key_path by dots (e.g., "whisper.model" -> ["whisper", "model"])
        2. Navigate through the nested config dictionary
        3. Return the value if found, or default if not found
        4. Handle cases where intermediate keys don't exist
        """
        pass
    
    def get_whisper_config(self):
        """
        Get Whisper-specific configuration.
        
        Returns:
            Dictionary with whisper settings (model, language, etc.)
            
        TODO: Implement this method to:
        1. Use self.get() to retrieve whisper configuration
        2. Return a dictionary with keys like 'model', 'language'
        3. Provide sensible defaults if settings are missing
        """
        pass
    
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
    
    Args:
        config_path: Path to the YAML configuration file
        
    Returns:
        Config object with loaded settings
        
    LEARNING NOTE: This function demonstrates:
    - Reading files safely
    - Parsing YAML data
    - Merging with default values
    - Error handling for missing files
    
    TODO: Implement this function to:
    1. Define default configuration (create a dictionary with sensible defaults)
    2. Check if config file exists using pathlib
    3. If file exists, read and parse YAML content
    4. Merge user config with defaults (user values override defaults)
    5. Validate important settings (e.g., whisper model should be valid)
    6. Return a Config object with the merged configuration
    7. Handle errors gracefully (file not found, invalid YAML, etc.)
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
        raise ValueError(f"Invalid Whisper model. ${whisper_model} is not a valid model. Valid models: ${str(valid_whisper_models)}")



    # # Validate audio settings
    # audio_config = config_data.get("audio", {})
    # sample_rate = audio_config.get("sample_rate", 16000)
    # if not isinstance(sample_rate, int) or sample_rate <= 0:
    #     print(f"Warning: Invalid sample rate '{sample_rate}'. Using 16000 instead.")
    #     config_data["audio"]["sample_rate"] = 16000
    
    # channels = audio_config.get("channels", 1)
    # if channels not in [1, 2]:
    #     print(f"Warning: Invalid channels '{channels}'. Using 1 (mono) instead.")
    #     config_data["audio"]["channels"] = 1

"""
Next steps:
Merging Default config with user config is a lot of work and introduces errors.
Instead assume user has a config.yaml file with their settings.
Update README to include correct config structure
If a value is found missing from config, throw error and ask to check config settings from README
"""