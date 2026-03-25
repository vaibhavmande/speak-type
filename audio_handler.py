"""
Audio recording and processing for SpeakType application.

This module handles microphone recording, audio format conversion,
and silence detection. It provides clean audio data for transcription.

LEARNING NOTE: This file demonstrates:
- Working with audio streams using PyAudio
- Audio format specifications (sample rate, channels, etc.)
- Buffer management for real-time audio
- Silence detection using RMS calculation
"""

import pyaudio
import numpy as np
import time

# TODO: Import threading for background audio processing
# import threading


class AudioHandler:
    """
    Handles audio recording and provides audio data for transcription.

    LEARNING NOTE: This class shows how to:
    - Manage audio streams and buffers
    - Handle different audio formats
    - Implement silence detection
    - Work with real-time audio data
    """

    def __init__(self, config):
        """
        Initialize the audio handler with configuration.

        Args:
            config: Configuration object with audio settings

        TODO: Implement this method to:
        1. Store config as instance variable
        2. Extract audio settings (sample_rate, channels, etc.)
        3. Initialize audio stream variables to None
        4. Create an empty buffer for storing audio data
        5. Set initial state (not recording)
        """
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
        """
        Start recording audio from the microphone.

        Returns:
            True if recording started successfully, False otherwise

        LEARNING NOTE: This method demonstrates:
        - Opening audio streams with specific parameters
        - Setting up audio format (16kHz, mono, 16-bit)
        - Starting background audio capture

        TODO: Implement this method to:
        1. Check if already recording (return False if so)
        2. Create PyAudio instance
        3. Open audio stream with settings from config:
           - Format: paInt16 (16-bit audio)
           - Channels: 1 (mono)
           - Rate: 16000 Hz (from config)
           - Input: True (recording)
           - Stream callback: function to handle audio chunks
        4. Start the stream
        5. Clear the audio buffer
        6. Record start time
        7. Return True on success, False on failure
        """

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
        """
        Stop recording and return the captured audio data.

        Returns:
            numpy array containing the recorded audio, or None if error
        """
        if not self.is_recording():
            return None

        try:
            self.stream.stop_stream()
            self.stream.close()
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

        Args:
            in_data: Raw audio data bytes
            frame_count: Number of audio frames
            time_info: Timing information
            status: Stream status flags

        Returns:
            Tuple of (output_data, continue_flag)
        """
        audio_chunk = np.frombuffer(in_data, dtype=np.int16)
        audio_chunk = audio_chunk.astype(np.float32) / 32768.0
        self.audio_buffer.append(audio_chunk)

        return (None, pyaudio.paContinue)

    def is_recording(self):
        """
        Check if currently recording audio.
        """
        return self.stream is not None and self.recording is True

    def get_recording_duration(self):
        """
        Get the current recording duration in seconds.
        """

        if not self.is_recording():
            return 0.0
        return time.time() - self.start_time

    def cleanup(self):
        """
        Clean up audio resources.
        """
        if self.stream is not None:
            try:
                if self.stream.is_active():
                    self.stream.stop_stream()
                self.stream.close()
            except:
                raise Exception("Error closing audio stream")

        if self.audio is not None:
            self.audio.terminate()

        self.audio_buffer = []
        self.recording = False
