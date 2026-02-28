# Task: Packaging basics (requirements + README)

## Status

ready

## Goal

Create the minimum documentation and dependency pins needed to run the MVP on macOS.

## Acceptance criteria

- `requirements.txt` exists with the key dependencies from the architecture.
- `README.md` explains:
  - prerequisites (Ollama, whisper.cpp or whispercpp)
  - microphone permissions on macOS
  - how to run (`python main.py`)
  - expected behavior + troubleshooting tips
- Notes emphasize privacy-first behavior and local-only processing.

## Dependencies

- Task 09 (orchestration)

---

## Implementation Guide

### `requirements.txt`

```
# Core dependencies
sounddevice>=0.4.6      # Audio capture
numpy>=1.24.0           # Audio processing
pyperclip>=1.8.2        # Clipboard operations
requests>=2.31.0        # Ollama API calls
pyyaml>=6.0.1           # Config file parsing
rumps>=0.3.0            # macOS menu bar (macOS only)

# Whisper integration
whispercpp>=1.0.0       # Python bindings for whisper.cpp

# Testing (optional)
pytest>=7.4.0
pytest-cov>=4.1.0
```

### `README.md` Structure

````markdown
# Speak-Type

Local, privacy-first speech-to-text application for macOS. Converts speech to improved text and copies it to your clipboard. All processing happens on your machine - no data ever leaves your device.

## Features

- 🎤 **Local Speech Recognition** - Uses Whisper (runs on your machine)
- ✨ **AI Text Improvement** - Grammar and clarity fixes via local Ollama
- 🔒 **Privacy First** - All processing happens locally, no cloud services
- 📋 **Clipboard Integration** - Improved text copied automatically
- 🖥️ **Menu Bar App** - Simple, unobtrusive interface
- ⚡ **Fast** - 1-4 second processing time
- 🌐 **Offline Capable** - Works without internet connection

## Prerequisites

### 1. macOS

- macOS 12.0 or later
- Python 3.10+

### 2. Ollama

```bash
# Install Ollama
brew install ollama

# Start Ollama service
ollama serve

# Pull recommended model
ollama pull llama3.2:3b
```
````

### 3. Whisper.cpp (or whispercpp)

```bash
# Option A: Install via pip (recommended)
pip install whispercpp

# Option B: Build from source
git clone https://github.com/ggml-org/whisper.cpp
cd whisper.cpp
make
bash ./models/download-ggml-model.sh base
```

## Installation

```bash
# Clone repository
git clone https://github.com/yourusername/speak-type.git
cd speak-type

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Grant microphone permissions
# System Preferences → Security & Privacy → Privacy → Microphone
# Enable for Terminal or Python
```

## Usage

```bash
# Start the application
python main.py

# Look for 🎤 icon in menu bar
# Click "Start Recording" to begin
# Speak your text
# Click "Stop Recording" or wait for silence
# Improved text is copied to clipboard
# Paste with Cmd+V
```

## Configuration

Edit `config.yaml` to customize settings:

```yaml
whisper:
  model: "base" # tiny, base, small, medium, large
  language: "en" # Language code or null for auto-detect

ollama:
  model: "llama3.2:3b" # LLM model for text improvement
  timeout: 10 # Request timeout in seconds

audio:
  silence_threshold: 0.01 # RMS threshold for silence detection
  silence_duration: 2.0 # Seconds of silence before auto-stop
  max_recording_duration: 60

privacy:
  clear_audio_buffer: true # Clear audio after processing
  log_transcriptions: false # Never log transcribed text
  clear_clipboard_after: false # Optional clipboard clearing
```

## Menu Bar Controls

- **Start Recording** - Begin capturing audio
- **Stop Recording** - Stop and process audio
- **Copy Last Result** - Re-copy previous result
- **Quit** - Exit application

## Troubleshooting

### Microphone not working

```bash
# Check permissions
# System Preferences → Security & Privacy → Microphone
# Enable for Terminal/Python

# Test audio device
python -c "import sounddevice; print(sounddevice.query_devices())"
```

### Ollama not responding

```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Start Ollama if needed
ollama serve

# Verify model is downloaded
ollama list
```

### Whisper model not found

```bash
# Models are downloaded automatically on first run
# Or download manually:
whispercpp download base
```

### Menu bar icon doesn't appear

```bash
# Reset Terminal permissions
tccutil reset All

# Restart Terminal and try again
```

## Privacy & Security

✅ **All processing is local**

- Whisper runs on your machine
- Ollama runs on localhost
- No external API calls
- No data sent to cloud services

✅ **Data cleanup**

- Audio buffers cleared after processing
- Transcriptions not logged (configurable)
- No persistent storage of recordings

✅ **Minimal permissions**

- Only requires microphone access
- No network access needed (except localhost)

## Performance

**Processing Time:**

- Transcription (base model): 0.5-1.5 seconds
- Text improvement (llama3.2:3b): 0.5-2 seconds
- **Total: 1-4 seconds**

**Resource Usage:**

- RAM (idle): ~100MB
- RAM (active): ~2.5GB (Whisper + Ollama)
- CPU (idle): <1%
- CPU (active): 50-100% (brief bursts)

**Storage:**

- Whisper base model: ~140MB
- Ollama llama3.2:3b: ~2GB

## Development

```bash
# Run tests
pytest tests/

# Run with coverage
pytest --cov=. tests/

# Format code
black *.py

# Type checking
mypy *.py
```

## Architecture

See [docs/architecture.md](docs/architecture.md) for detailed architecture documentation.

## License

MIT License - See LICENSE file

## Contributing

Contributions welcome! Please read CONTRIBUTING.md first.

## Acknowledgments

- [Whisper](https://github.com/openai/whisper) by OpenAI
- [whisper.cpp](https://github.com/ggml-org/whisper.cpp) by Georgi Gerganov
- [Ollama](https://ollama.ai/) for local LLM inference
- [rumps](https://github.com/jaredks/rumps) for macOS menu bar

````

### Installation Script (Optional)

```bash
#!/bin/bash
# install.sh - Quick setup script

set -e

echo "🚀 Installing Speak-Type..."

# Check Python version
python3 --version | grep -q "3.1[0-9]" || {
    echo "❌ Python 3.10+ required"
    exit 1
}

# Create venv
echo "📦 Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Check Ollama
echo "🔍 Checking Ollama..."
if ! command -v ollama &> /dev/null; then
    echo "⚠️  Ollama not found. Install with: brew install ollama"
else
    echo "✅ Ollama found"
fi

# Create default config
if [ ! -f config.yaml ]; then
    echo "⚙️  Creating default config..."
    python -c "from config import create_default_config; create_default_config()"
fi

echo "✅ Installation complete!"
echo "Run: python main.py"
````

### Testing Checklist

- [ ] requirements.txt includes all dependencies
- [ ] README has clear installation instructions
- [ ] Prerequisites are documented
- [ ] Configuration examples are provided
- [ ] Troubleshooting section covers common issues
- [ ] Privacy features are highlighted
- [ ] Performance expectations are documented

### Notes

- README should be beginner-friendly
- Include troubleshooting for common issues
- Emphasize privacy-first approach
- Provide performance expectations
- Link to architecture documentation
- Keep installation steps simple and clear
