# Speak-Type

A privacy-first, local-only speech-to-text application that converts speech to improved text and copies it to clipboard. All processing happens on your machine - no data ever leaves your device.

## Features

- **Privacy First**: All data processing happens locally
- **Offline Capable**: No external API dependencies
- **Lightweight**: Minimal resource usage when idle
- **Simple**: Single menu-bar control surface
- **Fast**: Optimized for quick transcription and improvement

## Quick Start

### Prerequisites

1. **Install Ollama**

   ```bash
   brew install ollama
   ollama serve
   ollama pull llama3.2:3b
   ```

2. **Install PortAudio (required for PyAudio on macOS)**

   ```bash
   brew install portaudio
   ```

3. **Install Python dependencies**

   ```bash
   pip install pyaudio numpy openai-whisper requests pyperclip rumps pyyaml
   ```

4. **Grant microphone permissions** (macOS System Preferences → Security & Privacy → Privacy)

### Usage

```bash
python main.py
```

The app will appear in your menu bar. Click the menu icon to start recording, speak naturally, then click stop. The improved text will be copied to your clipboard.

## How It Works

1. Click "Start Recording" from the menu bar
2. Speak into your microphone
3. Click "Stop Recording"
4. Audio is transcribed using Whisper
5. Text is improved using local LLM (Ollama)
6. Improved text is automatically copied to clipboard
7. Paste with Cmd+V wherever you need it
8. Use "Copy Last" to re-copy the previous result

## Tech Stack

- **Core**: Python 3.10+
- **Speech Recognition**: OpenAI Whisper (Python)
- **Text Improvement**: Ollama with local LLM
- **Audio**: PyAudio + numpy
- **UI**: rumps (macOS menu bar)
- **Clipboard**: pyperclip
- **Configuration**: PyYAML

## Configuration

Edit `config.yaml` to customize:

- Whisper model selection
- LLM model and settings
- Audio parameters
- Privacy options

## Privacy

✅ All processing happens locally  
✅ No external API calls  
✅ Audio buffers cleared after processing  
✅ No transcription logging by default

## Development

See `docs/architecture.md` for detailed technical documentation.

## License

See LICENSE file for details.
