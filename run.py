#!/usr/bin/env python3

"""
SpeakType - Voice-to-Text Transcription and Improvement Tool

This is the main entry point for the SpeakType application.
It creates a menu bar app that allows users to record audio,
transcribe it using Whisper, improve the text using Ollama LLM,
and copy the result to the clipboard.
"""

from speak_type.main import main

if __name__ == "__main__":
    main()
