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
   ollama pull llama3.2:latest
   ```

2. **Install PortAudio (required for PyAudio on macOS)**

   ```bash
   brew install portaudio
   ```

3. **Install Python dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Grant microphone permissions** (macOS System Preferences → Security & Privacy → Privacy)

### Usage

```bash
python run.py
```

The app will appear in your menu bar. Click the menu icon to start recording, speak naturally, then click stop. The improved text will be copied to your clipboard.

## Project Structure

```
speak-type/
├── speak_type/          # Main package directory
│   ├── __init__.py
│   ├── main.py          # Application entry point
│   ├── audio_handler.py # Audio recording
│   ├── transcription.py # Whisper integration
│   ├── text_improver.py # Ollama LLM integration
│   ├── clipboard_manager.py
│   ├── config.py        # Configuration management
│   └── app_states.py    # Application state management
├── run.py               # Launch script
├── config.yaml          # Configuration file
├── docs/                # Documentation
├── tests/               # Test files
└── README.md
```

## How It Works

1. Click "Start Recording" from the menu bar (icon changes to ⏺️)
2. Speak into your microphone
3. Click "Stop Recording"
4. App enters processing mode (icon changes to ⏳)
5. Audio is transcribed using Whisper
6. Text is improved using local LLM (Ollama)
7. Improved text is automatically copied to clipboard
8. You'll receive a notification with a preview of the text
9. Paste with Cmd+V wherever you need it
10. Use "Copy Last" to re-copy the previous result

## Tech Stack

- **Core**: Python 3.12+
- **Speech Recognition**: OpenAI Whisper (openai-whisper>=20231117)
- **Text Improvement**: Ollama with local LLM (llama3.2:latest)
- **Audio**: PyAudio + numpy
- **UI**: rumps (macOS menu bar)
- **Clipboard**: pyperclip
- **Configuration**: PyYAML

## Configuration

Edit `config.yaml` to customize:

- **Whisper**: Model selection (tiny, base, small, medium, large), language, device (cpu/cuda)
- **Ollama**: Host URL, model name, custom prompt template
- **Audio**: Sample rate, channels, silence detection, chunk size
- **App**: Menu icons, notification settings
- **Clipboard**: Notification preferences

See `config.yaml` for all available options and defaults.

## Privacy

✅ All processing happens locally  
✅ No external cloud API calls (only local Ollama server)  
✅ Audio buffers cleared after processing  
✅ No transcription logging by default  
✅ No data leaves your machine

## Troubleshooting

### Ollama Connection Issues

Ensure Ollama is running:

```bash
ollama serve
```

Verify the model is downloaded:

```bash
ollama list
```

### Microphone Not Working

- Grant microphone permissions in System Preferences → Security & Privacy → Privacy → Microphone
- Ensure Python/Terminal has microphone access

### PyAudio Installation Fails

Make sure PortAudio is installed:

```bash
brew install portaudio
```

### No Notifications Appearing

Check notification permissions for Python/Terminal in System Preferences → Notifications

## Development

See `docs/architecture.md` for detailed technical documentation.

## License

See LICENSE file for details.
