#!/usr/bin/env python3
"""
SpeakType - Voice-to-Text Transcription and Improvement Tool

This is the main entry point for the SpeakType application.
It creates a menu bar app that allows users to record audio,
transcribe it using Whisper, improve the text using Ollama LLM,
and copy the result to the clipboard.
"""

from typing import Literal
from audio_handler import AudioHandler
from transcription import WhisperTranscriber
from text_improver import TextImprover

# from clipboard_manager import ClipboardManager

import traceback
from config import load_config
from app_states import AppStates

import rumps

rumps.debug_mode(True)


class SpeakTypeApp(rumps.App):
    """
    Main application class that manages the menu bar interface
    and coordinates between different components.
    """

    def __init__(self, config):

        self.config = config.config
        self.config_instance = config
        self.app_config = config.get_app_config()
        self.audio_config = config.get_audio_config()

        self.audio_handler = AudioHandler(config)
        self.transcriber = WhisperTranscriber(config)
        self.improver = TextImprover(config)
        # self.clipboard = ClipboardManager(config)

        super(SpeakTypeApp, self).__init__(
            self.app_config.get("idle_icon"), menu=self.app_config.get("menu")
        )
        # menu_items = self.app_config.get("menu")
        # self.menu = [rumps.MenuItem(item) for item in menu_items]
        # self.menu = menu_items

        start_button = self.menu["Start Recording"]
        stop_button = self.menu["Stop Recording"]

        stop_button.set_callback(None)
        start_button.set_callback(None)
        # self.update_app_state(AppStates.IDLE)

        start_button.update(["Start Recording"])
        stop_button.update(["Stop Recording"])

        # print("SpeakTypeApp initialized with config:", self.config)
        return

    def update_app_state(self, state):
        """
        Update the application state and UI.
        IDLE, RECORDING, PROCESSING
        activate/deactivate menu items
        """
        self.state = state
        self.title = self.get_app_metadata().get("title")

        start_button = self.menu.get("Start Recording")
        stop_button = self.menu.get("Stop Recording")

        match self.state:
            case AppStates.IDLE:
                stop_button.set_callback(None)
                start_button.set_callback(self.start_recording)
                pass
            case AppStates.RECORDING:
                start_button.set_callback(None)
                stop_button.set_callback(self.stop_recording)
                pass
            case AppStates.PROCESSING:
                start_button.set_callback(None)
                stop_button.set_callback(None)
                pass
            case _:
                self.update_app_state(AppStates.IDLE)

        print(start_button)
        print(stop_button)

    def get_app_metadata(self):

        match self.state:
            case AppStates.IDLE:
                title = self.app_config.get("idle_icon")
            case AppStates.RECORDING:
                title = self.app_config.get("recording_icon")
            case AppStates.PROCESSING:
                title = self.app_config.get("processing_icon")
            case _:
                title = self.app_config.get("idle_icon")

        return {"title": title}

    @rumps.clicked("Start Recording")
    def start_recording(self, sender):

        print("Starting recording...")
        self.update_app_state(AppStates.RECORDING)
        # self.title = self.get_app_metadata().get("title")
        self.audio_handler.start_recording()

    @rumps.clicked("Stop Recording")
    def stop_recording(self, sender):

        audio_data = self.audio_handler.stop_recording()
        self.update_app_state(AppStates.PROCESSING)
        language = self.audio_config.get("language", "english")
        transcribed = self.transcriber.transcribe(audio_data, language)
        print(f"Transcribed text={transcribed}")
        # for now send a dummy text
        dummy_text = "Their are many benifits of using AI in healthcare. It not only helps in diagnosing diseases but also in providing personalized treatments."

        improved_text = self.improver.improve_text(dummy_text)

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
    try:
        config = load_config("config.yaml")
        app = SpeakTypeApp(config)
        app.run()
    except Exception as e:
        print(f"Failed to start application: {e}")
        traceback.print_exc()
        return


# This is the standard Python pattern for making a file executable
# When this file is run directly (not imported), __name__ will be "__main__"
if __name__ == "__main__":
    main()
