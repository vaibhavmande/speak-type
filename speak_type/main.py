#!/usr/bin/env python3

from .audio_handler import AudioHandler
from .transcription import WhisperTranscriber
from .text_improver import TextImprover
from .clipboard_manager import ClipboardManager

import traceback
import threading
from .config import load_config
from .app_states import AppStates, get_app_metadata

import rumps


class SpeakTypeApp(rumps.App):

    def __init__(self, config):
        self.config = config.config
        self.config_instance = config
        self.app_config = config.get_app_config()
        self.audio_config = config.get_audio_config()
        self.state = AppStates.IDLE
        self.last_text = None

        self.audio_handler = AudioHandler(config)
        self.transcriber = WhisperTranscriber(config)
        self.improver = TextImprover(config)
        self.clipboard_manager = ClipboardManager(config)

        super(SpeakTypeApp, self).__init__(
            self.app_config.get("idle_icon"), menu=self.app_config.get("menu")
        )

        self.update_app_state(AppStates.IDLE)
        rumps.events.before_quit.register(self.quit_app)

        print("SpeakTypeApp initialized with config:", self.config)

    def start_recording(self, sender):
        self.update_app_state(AppStates.RECORDING)

        def start_audio():
            self.audio_handler.start_recording()

        thread = threading.Thread(target=start_audio)
        thread.daemon = True
        thread.start()

    def stop_recording(self, sender):
        self.update_app_state(AppStates.PROCESSING)

        def process_audio():
            audio_data = self.audio_handler.stop_recording()
            language = self.audio_config.get("language", "english")
            transcribed = self.transcriber.transcribe(audio_data, language)

            try:
                improved_text = self.improver.improve_text(transcribed)
            except Exception as e:
                print(f"Error improving text: {e}")
                self.update_app_state(AppStates.IDLE)
                improved_text = transcribed

            self.clipboard_manager.copy_to_clipboard(improved_text)
            self.last_text = improved_text
            print("Improvement completed. Text is ready to be pasted")

            preview_length = 30
            preview_text = improved_text[:preview_length]
            if len(improved_text) > preview_length:
                preview_text += "..."

            rumps.notification(
                title="Text Ready to Paste",
                subtitle="Copied to clipboard",
                message=preview_text,
                sound=False,
            )

            self.update_app_state(AppStates.IDLE)

        thread = threading.Thread(target=process_audio)
        thread.daemon = True
        thread.start()

    def copy_last(self, sender):
        if self.last_text:
            self.clipboard_manager.copy_to_clipboard(self.last_text)
        else:
            print("No text to copy")

    def update_app_state(self, state):
        self.state = state
        self.title = get_app_metadata(self.state, self.app_config).get("title")

        start_button = self.menu.get("Start Recording")
        stop_button = self.menu.get("Stop Recording")

        match self.state:
            case AppStates.IDLE:
                stop_button.set_callback(None)
                start_button.set_callback(self.start_recording)
            case AppStates.RECORDING:
                start_button.set_callback(None)
                stop_button.set_callback(self.stop_recording)
            case AppStates.PROCESSING:
                start_button.set_callback(None)
                stop_button.set_callback(None)
            case _:
                self.update_app_state(AppStates.IDLE)

    def quit_app(self):
        self.transcriber.unload_model()
        self.audio_handler.cleanup()


def main():
    try:
        config = load_config("config.yaml")
        app = SpeakTypeApp(config)
        app.run()
    except Exception as e:
        app.update_app_state(AppStates.IDLE)
        print(f"Failed to start application: {e}")
        traceback.print_exc()
        return


if __name__ == "__main__":
    main()
