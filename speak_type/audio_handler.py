"""
Audio recording and processing for SpeakType application.

This module handles microphone recording, audio format conversion,
and silence detection. It provides clean audio data for transcription.
"""

import pyaudio
import numpy as np
import time


class AudioHandler:
    """
    Handles audio recording and provides audio data for transcription.
    """

    def __init__(self, config):

        self.audio_config = config.get_audio_config()

        self.recording = False
        self.start_time = None
        self.audio_buffer = []
        self.stream = None

        self.format = pyaudio.paInt16
        self.audio = pyaudio.PyAudio()
        self.channels = self.audio_config.get("channels", 1)
        self.sample_rate = self.audio_config.get("sample_rate", 16000)
        self.chunk_size = self.audio_config.get("chunk_size", 1024)

        pass

    def start_recording(self):

        if self.recording:
            return False

        try:
            self.stream = self.audio.open(
                format=self.format,
                channels=self.channels,
                rate=self.sample_rate,
                input=True,
                frames_per_buffer=self.chunk_size,
                stream_callback=self._audio_callback,
            )
            self.stream.start_stream()
            self.recording = True
            self.start_time = time.time()
            self.audio_buffer = []
            print("Recording started")
            return True

        except Exception as e:
            print(f"Error starting recording: {e}")
            return False

    def stop_recording(self):

        if not self.is_recording():
            return None

        try:
            self.stream.stop_stream()
            self.stream.close()
            self.stream = None
            self.recording = False

            if self.audio_buffer:
                audio_data = np.concatenate(self.audio_buffer)
                return audio_data
            else:
                return None

        except Exception as e:
            print(f"Error stopping recording: {e}")
            return None

        finally:
            # self.audio.terminate()
            self.audio_buffer = []
            self.recording = False
            self.stream = None

    def get_audio_level(self):
        """
        Calculate the current audio level (RMS amplitude).
        """
        if not self.is_recording():
            return 0.0

        recent_audio = self.audio_buffer[-1] if self.audio_buffer else np.array([])
        if not recent_audio:
            return 0.0

        rms = np.sqrt(np.mean(recent_audio**2))

        # Normalize to 0.0-1.0 range
        return min(rms * 10, 1.0)

    def _audio_callback(self, in_data, frame_count, time_info, status):
        """
        Callback function called by PyAudio when new audio data is available.
        """
        audio_chunk = np.frombuffer(in_data, dtype=np.int16)
        audio_chunk = audio_chunk.astype(np.float32) / 32768.0
        self.audio_buffer.append(audio_chunk)

        return (None, pyaudio.paContinue)

    def is_recording(self):
        return self.stream is not None and self.recording is True

    def cleanup(self):
        if self.stream is not None:
            try:
                if self.stream.is_active():
                    self.stream.stop_stream()
                self.stream.close()
            except OSError as e:
                print(f"Error closing audio stream: {e}")
            except Exception as e:
                print(f"Error closing audio stream: {e}")
            finally:
                self.stream = None

        if self.audio is not None:
            try:
                self.audio.terminate()
            except Exception as e:
                print(f"Error terminating PyAudio: {e}")
            finally:
                self.audio = None

        self.audio_buffer = []
        self.recording = False
