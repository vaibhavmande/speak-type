#!/usr/bin/env python3
"""
SpeakType - Voice-to-Text Transcription and Improvement Tool

This is the main entry point for the SpeakType application.
It creates a menu bar app that allows users to record audio,
transcribe it using Whisper, improve the text using Ollama LLM,
and copy the result to the clipboard.

LEARNING NOTE: This file demonstrates:
- Creating a macOS menu bar app using rumps
- Orchestrating multiple components
- Handling user interactions
- Managing application state
"""

# TODO: Import the rumps library for creating macOS menu bar apps
# Install with: pip install rumps
# import rumps

# TODO: Import our custom modules (we'll create these next)
# from audio_handler import AudioHandler
# from transcription import WhisperTranscriber
# from text_improver import TextImprover
# from clipboard_manager import ClipboardManager
from config import load_config


class SpeakTypeApp:
    """
    Main application class that manages the menu bar interface
    and coordinates between different components.
    
    LEARNING NOTE: This class shows how to:
    - Create a menu bar app with multiple menu items
    - Handle different application states (IDLE, RECORDING, PROCESSING)
    - Coordinate between different components
    """
    
    def __init__(self, config):
        """
        Initialize the app with configuration and create all components.
        
        Args:
            config: Configuration object with settings for all components

        TODO: Implement this method to:
        1. Create a rumps.App instance with menu bar icon (🎤)
        2. Initialize all components (audio_handler, transcriber, improver, clipboard)
        3. Set up menu items: Start Recording, Stop Recording, Copy Last, Quit
        4. Set initial state to IDLE
        5. Store config and components as instance variables
        """
        print("SpeakTypeApp initialized with config:", config)
    
    def start_recording(self, sender):
        """
        Start audio recording when user clicks "Start Recording" menu item.
        
        Args:
            sender: The menu item that triggered this action
            
        TODO: Implement this method to:
        1. Call audio_handler.start_recording()
        2. Update UI to show recording state (change menu item text/color)
        3. Update internal state to RECORDING
        4. Print a message to confirm recording started
        """
        pass
    
    def stop_recording(self, sender):
        """
        Stop recording and start processing pipeline.
        
        Args:
            sender: The menu item that triggered this action
            
        TODO: Implement this method to:
        1. Call audio_handler.stop_recording() to get audio data
        2. Update UI to show processing state
        3. Start processing pipeline in background thread:
           - Transcribe audio using Whisper
           - Improve text using Ollama LLM
           - Copy to clipboard
        4. Update state to PROCESSING during pipeline
        5. Return to IDLE state when done
        """
        pass
    
    def copy_last(self, sender):
        """
        Copy the last processed result to clipboard.
        
        Args:
            sender: The menu item that triggered this action
            
        TODO: Implement this method to:
        1. Get the last processed text from storage
        2. Use clipboard_manager to copy it
        3. Show a notification to confirm copy
        """
        pass
    
    def quit_app(self, sender):
        """
        Clean up resources and quit the application.
        
        Args:
            sender: The menu item that triggered this action
            
        TODO: Implement this method to:
        1. Clean up any resources (close audio streams, unload models)
        2. Save any necessary state
        3. Terminate the application
        """
        pass


def main():
    """
    Main entry point for the application.
    
    LEARNING NOTE: This function demonstrates:
    - Loading configuration from a file
    - Creating and running the main application
    - Basic error handling
    
    TODO: Implement this function to:
    1. Load configuration from config.yaml (use load_config function)
    2. Create a SpeakTypeApp instance with the config
    3. Run the menu bar app (this will keep it running until user quits)
    4. Add basic error handling for config loading
    """
    config = load_config()
    app = SpeakTypeApp(config)
    # somehow call rumps.run() from here and somehow that .run is inside SpeakTypeApp class
    pass


# This is the standard Python pattern for making a file executable
# When this file is run directly (not imported), __name__ will be "__main__"
if __name__ == "__main__":
    # TODO: Call the main() function to start the application
    main()
