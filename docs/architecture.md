# Local Speech-to-Text Application Architecture

## Overview

A privacy-first, local-only application that converts speech to improved text and copies it to clipboard. All processing happens on your machine - no data ever leaves your device. Can run completely offline. Users launch the process once from the terminal, after which it runs headlessly as a macOS menu-bar utility.

## Design Principles

- **Privacy First**: All data processing happens locally
- **Offline Capable**: No external API dependencies
- **Lightweight**: Minimal resource usage when idle
- **Simple**: Single menu-bar control surface, no complex UI
- **Fast**: Optimized for quick transcription and improvement

## Core Components

### 0. Menu Bar Controller

- **Technology**: [`rumps`](https://github.com/jaredks/rumps) (confirmed choice)
- **Rationale**: Pure Python, simple API, handles all NSStatusBar boilerplate
- **Responsibilities**:
  - Draws menu-bar icon with idle/recording/processing states
  - Exposes dropdown actions (Start/Stop, Copy Last Result, Quit)
  - Shows optional user notifications (visual only)
  - Hosts long-running event loop while main thread handles audio/LLM work
- **Launch**: Started once via `python main.py`; terminal stays open for logs while the UI lives in the menu bar

#### Sample Implementation:

```python
import rumps

class SpeechToTextApp(rumps.App):
    def __init__(self):
        super(SpeechToTextApp, self).__init__("🎤", quit_button=None)
        self.menu = [
            rumps.MenuItem("Start Recording", callback=self.start_recording),
            rumps.MenuItem("Stop Recording", callback=self.stop_recording),
            rumps.separator,
            rumps.MenuItem("Copy Last Result", callback=self.copy_last),
            rumps.MenuItem("Quit", callback=self.quit_app)
        ]
        self.last_result = ""

    def start_recording(self, _):
        self.icon = "🔴"
        self.title = "Recording..."
        # Trigger audio recording in separate thread

    def stop_recording(self, _):
        self.icon = "⏳"
        self.title = "Processing..."
        # Stop recording and start processing

    def copy_last(self, _):
        if self.last_result:
            rumps.notification("Copied", "Last result copied to clipboard")

    def quit_app(self, _):
        self.quit()
```

### 1. Speech Recognition Layer

- **Technology**: whisper.cpp (C++ bindings for OpenAI Whisper)
- **Rationale**:
  - Faster than Python implementation
  - Runs entirely locally
  - No external dependencies
  - Efficient memory usage
- **Model Selection**: Start with `base` or `small` model
  - `base`: ~140MB, faster, good for quick dictation
  - `small`: ~460MB, more accurate, slightly slower
- **Processing**: Chunk-based processing for real-time feel

### 2. Text Improvement Layer

- **Technology**: Ollama with local LLM
- **Recommended Models**:
  - `llama3.2:3b` - Fast, lightweight, good general purpose
  - `qwen2.5:3b` - Excellent at text refinement tasks
- **Purpose**: Fix grammar, improve phrasing, maintain original meaning
- **System Prompt**:

```
Fix grammar, improve clarity and phrasing.
Keep the original meaning intact.
Output only the improved text,
```

### 3. Audio Input Handler

- **Technology**: `sounddevice` + `numpy`
- **Functionality**:
  - Captures microphone input in real-time
  - Buffers audio data for processing
  - Detects silence for auto-stop
  - Clears buffers after processing (privacy)
- **Configuration**:
  - Sample rate: 16kHz (Whisper requirement)
  - Channels: Mono
  - Buffer size: Configurable

### 4. Clipboard Manager

- **Technology**: `pyperclip` for clipboard manipulation
- **Flow**:
  1. Copy improved text to clipboard
  2. Show notification asking user to manually paste with Cmd+V
  3. Text appears at cursor position when user pastes (user keeps destination app focused)
  4. Clipboard remains available for user to reuse as needed

## Tech Stack

```
Core Language:     Python 3.10+
Speech Recognition: whisper.cpp (with Python bindings: whispercpp)
LLM Processing:    Ollama API (localhost:11434)
Audio Capture:     sounddevice + numpy
Clipboard:         pyperclip
Configuration:     YAML (config.yaml) + pyyaml
Menu Bar Shell:    rumps (macOS status bar helper)
HTTP Client:       requests (for Ollama API)
```

**Excluded**: Rich library (removed to speed up development)

## Application Flow

```
1. User launches menu-bar app from terminal (`python main.py`)
   → App initializes, loads models, and creates NSStatusBar icon
   → Terminal stays open for logs only; user interacts via menu bar icon
   → Menu bar tooltip displays "Ready. Click menu to start"

2. User clicks "Start Recording" from menu bar while cursor remains in destination app
   → Menu bar icon turns red and tooltip shows "🎤 Listening... (Click menu to stop)"
   → Start recording audio from microphone

3. User speaks
   → Audio buffered in real-time
   → Optional: Visual indicator (simple text) showing recording in progress

4. User clicks "Stop Recording" from menu OR silence detected (after 2-3 seconds)
   → Stop recording
   → Menu bar icon shows spinner state with tooltip "⏳ Processing..."

5. Audio → Whisper
   → Send audio buffer to whisper.cpp
   → Get raw transcription
   → Display: "📝 Transcribed: [first 50 chars]..."

6. Transcription → Ollama
   → Send transcription to local LLM
   → Get improved text
   → Display via menu bar notification: "✨ Improved: [first 50 chars]..."

7. Copy to clipboard
   → Copy improved text to clipboard
   → Show notification: "✓ Copied to clipboard! Paste with Cmd+V"

8. Cleanup
   → Clear audio buffer
   → Clear temporary data
   → Return to listening state
   → Menu bar icon returns to idle gray state with tooltip "Ready. Click menu to start"

9. User wants to stop the app
   → Press Ctrl+C in terminal OR click "Quit" from menu
   → Display: "Shutting down..." in terminal log and menu bar tooltip
   → Cleanup:
     - Unload Whisper model from memory
     - Close Ollama connection
     - Release audio device
   → Display: "✓ Cleanup complete. Goodbye!" and hide menu bar icon
   → Exit process
```

## Project Structure

```
speech-to-text-local/
├── main.py                 # Entry point, orchestrates all components
├── audio_handler.py        # Microphone recording & silence detection
├── transcription.py        # Whisper integration
├── text_improver.py        # Ollama LLM calls
├── clipboard_manager.py    # Clipboard functionality
├── config.yaml             # User configuration
├── requirements.txt        # Python dependencies
├── install.sh              # Installation script (optional)
├── README.md               # Setup & usage instructions
└── models/                 # Whisper models stored here (auto-downloaded)
```

## Key Implementation Details

### Whisper Integration

```python
# Use whispercpp or direct subprocess calls
# Load model once at startup (keep in memory for speed)
# Example:
from whispercpp import Whisper

whisper = Whisper.from_pretrained("base")
result = whisper.transcribe(audio_array)
```

### Ollama Integration

```python
import requests

def improve_text(transcription):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3.2:3b",
            "prompt": f"Fix grammar and improve: {transcription}",
            "stream": False
        }
    )
    return response.json()['response']
```

### Menu Configuration

```python
# Menu items handled by rumps
menu_items = ["Start Recording", "Stop Recording", "Copy Last Result", "Quit"]
```

### Silence Detection

```python
# Detect silence: if audio level below threshold for N seconds, auto-stop
SILENCE_THRESHOLD = 0.01  # Amplitude threshold
SILENCE_DURATION = 2.0    # Seconds of silence before auto-stop
```

## Configuration File (config.yaml)

```yaml
# Menu configuration (menu bar app controls)
menu:
  show_copy_last: true # Show "Copy Last Result" option
  show_notifications: true # Show visual notifications

# Whisper settings
whisper:
  model: "base" # Options: tiny, base, small, medium, large
  language: "en" # Auto-detect if null

# Ollama settings
ollama:
  host: "http://localhost:11434"
  model: "llama3.2:3b"
  timeout: 10 # Seconds

# Audio settings
audio:
  sample_rate: 16000
  channels: 1
  silence_threshold: 0.01
  silence_duration: 2.0 # Seconds
  max_recording_duration: 60 # Seconds

# Privacy settings
privacy:
  clear_clipboard_after: true
  clear_audio_buffer: true
  log_transcriptions: false # Never log for privacy
```

## Privacy & Security Features

✅ **Local Processing Only**

- Whisper runs locally via whisper.cpp
- Ollama runs locally on localhost:11434
- No external API calls

✅ **Data Cleanup**

- Audio buffers cleared immediately after processing
- No transcription logging (configurable)

✅ **Minimal Permissions**

- Microphone access (required)
- No special accessibility permissions needed
- No network access needed (except localhost for Ollama)

⚠️ **User Responsibilities**

- Ensure Ollama doesn't have telemetry enabled
- Verify no other apps are recording audio
- Grant only necessary system permissions

## Performance Characteristics

### Latency Breakdown

- **Audio Recording**: Real-time (0ms added)
- **Whisper Transcription**: 0.5-1.5 seconds (base model)
- **LLM Improvement**: 0.5-2 seconds (3B model)
- **Total Latency**: 1-4 seconds (acceptable for dictation)

### Resource Usage

- **RAM (Idle)**: ~100MB (Python process only)
- **RAM (Active)**:
  - Whisper base model: ~500MB
  - Llama 3.2 3B: ~2GB
  - Total: ~2.5GB during processing
- **CPU (Idle)**: <1% (menu bar app only)
- **CPU (Active)**: 50-100% (one core, brief bursts)

### Model Storage

- Whisper base: ~140MB disk space
- Whisper small: ~460MB disk space
- Llama 3.2 3B: ~2GB disk space

## Installation Prerequisites

### 1. Install Ollama

```bash
# macOS
brew install ollama

# Start Ollama service
ollama serve

# Pull model
ollama pull llama3.2:3b
```

### 2. Install whisper.cpp

```bash
# Clone repository
git clone https://github.com/ggml-org/whisper.cpp
cd whisper.cpp

# Compile
make

# Download model
bash ./models/download-ggml-model.sh base
```

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt

# requirements.txt contents:
# sounddevice>=0.4.6
# numpy>=1.24.0
# pyperclip>=1.8.2
# requests>=2.31.0
# pyyaml>=6.0.1
# rumps>=0.3.0
# whispercpp>=1.0.0  # Or use subprocess for whisper.cpp binary
```

### 4. Grant System Permissions

**macOS**:

- System Preferences → Security & Privacy → Privacy
  - Microphone: Allow Terminal (or your Python executable)

## Startup & Shutdown

### Startup

```bash
# From project directory
python main.py

# Expected output:
# Loading Whisper model (base)...
# Connecting to Ollama...
# Models loaded successfully.
# Menu bar icon: Ready (gray). Click menu to start recording.
# Quit via menu bar menu or Ctrl+C.
```

### Shutdown Options

1. **Graceful Shutdown**: Click "Quit" from menu
2. **Force Quit**: Press `Ctrl+C` in terminal
3. **Kill Process**: `killall python` (not recommended)

### Cleanup Process

```
1. Stop audio stream
3. Unload Whisper model from memory
4. Close Ollama connection
5. Clear all buffers (audio, text)
6. Release system resources
7. Exit with code 0

## MVP Constraints

- **Terminal-launched**: Users start the process via `python menu_app.py`; packaging into a standalone `.app` is deferred.
- **Single-task pipeline**: Recording requests are ignored while processing/pasting to keep implementation simple.
- **Manual focus discipline**: Users must keep the destination app focused during recording; automatic refocus is out of scope.
```

## Error Handling

### Common Issues

1. **Ollama not running**: Check with `curl http://localhost:11434`
2. **Microphone not accessible**: Verify permissions
3. **Whisper model missing**: Download with provided script

### Graceful Degradation

- If LLM fails: Output raw transcription (skip improvement step)
- If Whisper fails: Show error, allow retry
- If clipboard copy fails: Show error, allow retry

## Future Enhancements (Optional)

- **Global Hotkey Support**: Add `Cmd+Shift+Space` hotkey for quick recording without menu interaction
- **Multi-language support**: Use Whisper's language detection
- **Custom vocabulary**: Fine-tune Whisper for domain-specific terms
- **Noise reduction**: Pre-process audio before Whisper
- **Multiple LLM profiles**: Different improvement styles (formal, casual, technical)
- **Keyboard shortcuts**: Undo last transcription, retry transcription
- **Statistics**: Track usage, accuracy, latency

## Alternative Approaches Considered

### 1. Python Whisper Package (Not Chosen)

- **Pros**: Easier installation
- **Cons**: Slower than whisper.cpp, higher memory usage
- **Decision**: whisper.cpp for performance

### 2. Cloud-based Speech Recognition (Not Chosen)

- **Pros**: Better accuracy, no local models
- **Cons**: Violates privacy requirement, needs internet
- **Decision**: Local-only for privacy

### 3. Skip LLM Improvement (Not Chosen)

- **Pros**: Faster (sub-second latency)
- **Cons**: Raw transcription has errors, no improvement
- **Decision**: LLM improvement adds value despite latency

## Development Roadmap

### Phase 1: Core Functionality

- [ ] Audio recording with menu trigger
- [ ] Whisper integration & transcription
- [ ] Basic clipboard functionality

### Phase 2: Text Improvement

- [ ] Ollama integration
- [ ] Improvement prompt engineering
- [ ] Error handling

### Phase 3: Polish & Reliability

- [ ] Graceful shutdown with cleanup
- [ ] Configuration file support
- [ ] Silence detection
- [ ] Terminal status messages

### Phase 4: Documentation & Testing

- [ ] README with setup instructions
- [ ] Test on different macOS versions
- [ ] Performance optimization

## Success Criteria

✅ **Functional Requirements**

- Menu launches recording
- Transcribes speech accurately (>90%)
- Improves text grammar/phrasing
- Copies improved text to clipboard
- Runs completely offline
- Clean shutdown with memory cleanup

✅ **Non-Functional Requirements**

- Total latency < 5 seconds
- Memory usage < 3GB during processing
- No data leaves machine
- No crashes or memory leaks
- Works on macOS 12+

---

**Document Version**: 1.0  
**Last Updated**: 2026-01-26  
**Author**: System Architecture  
**Status**: Ready for Implementation
