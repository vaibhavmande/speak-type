# Task: Project skeleton + module interfaces

## Status

ready

## Goal

Create the initial Python project layout that matches the architecture and defines minimal interfaces between components (menu app, audio, transcription, improver, clipboard, config).

## Acceptance criteria

- A top-level `main.py` exists and can be executed (even if it only prints startup/shutdown messages).
- Stub modules exist for:
  - `audio_handler.py`
  - `transcription.py`
  - `text_improver.py`
  - `clipboard_manager.py`
  - `config.py` (or equivalent)
- Each module exposes a minimal public API (function/class signatures) that the orchestrator can call.
- Imports are clean and the app starts without crashing.

## Dependencies

None

---

## Implementation Guide

### Project Structure

```
speak-type/
├── main.py                 # Entry point, orchestrates all components
├── audio_handler.py        # Microphone recording & silence detection
├── transcription.py        # Whisper integration
├── text_improver.py        # Ollama LLM calls
├── clipboard_manager.py    # Clipboard functionality
├── config.py               # Configuration loading and validation
├── config.yaml             # User configuration (created in Task 02)
├── requirements.txt        # Python dependencies (created in Task 12)
├── README.md               # Setup & usage instructions (created in Task 12)
├── models/                 # Whisper models stored here (auto-downloaded)
├── tests/                  # Unit tests (created in Task 11)
│   ├── __init__.py
│   ├── test_config.py
│   ├── test_silence_detection.py
│   └── test_text_improver.py
└── docs/
    └── architecture.md
```

### Component Interaction Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                         main.py                             │
│                   (SpeakTypeApp - rumps)                    │
│                                                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐     │
│  │  Start   │  │   Stop   │  │   Copy   │  │   Quit   │     │
│  │Recording │  │Recording │  │   Last   │  │          │     │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘     │
└───────┼─────────────┼─────────────┼─────────────┼───────────┘
        │             │             │             │
        ▼             ▼             ▼             ▼
┌───────────┐  ┌──────────────────────────┐  ┌──────────┐
│  Audio    │  │    Processing Pipeline   │  │ Cleanup  │
│  Handler  │  │                          │  │ Shutdown │
└─────┬─────┘  │  1. Stop Audio           │  └──────────┘
      │        │  2. Transcribe (Whisper) │
      │        │  3. Improve (Ollama)     │
      │        │  4. Copy (Clipboard)     │
      │        └──────────────────────────┘
      │
      ▼
┌─────────────────────────────────────────┐
│         Component Dependencies           │
├─────────────────────────────────────────┤
│  config.py         → All components     │
│  audio_handler.py  → transcription.py   │
│  transcription.py  → text_improver.py   │
│  text_improver.py  → clipboard_manager  │
└─────────────────────────────────────────┘
```

### Module Interfaces (Pseudocode)

#### `main.py`

```
class SpeakTypeApp(rumps.App):
    initialize(config):
        - create menu bar icon (🎤)
        - initialize all components (audio, transcriber, improver, clipboard)
        - set up menu items (Start, Stop, Copy Last, Quit)
        - set initial state to IDLE

    start_recording():
        - trigger audio capture
        - update UI to recording state

    stop_recording():
        - trigger processing pipeline in background thread
        - update UI to processing state

    copy_last():
        - copy last result to clipboard

    quit_app():
        - cleanup resources
        - exit application

main():
    - load configuration
    - create SpeakTypeApp instance
    - run menu bar app
```

#### `config.py`

```
class Config:
    get(key_path, default):
        - parse dot-notation key (e.g., "whisper.model")
        - return value or default

load_config(path):
    - read YAML file
    - merge with defaults
    - validate values
    - return Config object
```

#### `audio_handler.py`

```
class AudioHandler:
    start_recording():
        - open audio stream (16kHz, mono)
        - start capturing to buffer

    stop_recording():
        - stop stream
        - return audio as numpy array

    get_audio_level():
        - calculate RMS of recent audio
        - return amplitude (0.0-1.0)
```

#### `transcription.py`

```
class WhisperTranscriber:
    load_model():
        - load Whisper model into memory

    transcribe(audio):
        - send audio to Whisper
        - return transcribed text

    unload_model():
        - free model memory
```

#### `text_improver.py`

```
class TextImprover:
    improve_text(text):
        - build prompt for LLM
        - call Ollama API
        - return improved text or fallback to original
```

#### `clipboard_manager.py`

```
class ClipboardManager:
    copy_to_clipboard(text):
        - copy text using pyperclip
        - return success/failure

    notify_user(title, message):
        - show macOS notification
```

### Implementation Steps

1. Create directory structure
2. Create stub files for each module
3. Define class signatures and method stubs
4. Add TODO comments for future tasks
5. Test that app starts without errors

### Testing Checklist

- [ ] All modules import without errors
- [ ] `main.py` executes and shows menu bar icon
- [ ] Stub methods print expected messages
- [ ] No circular dependencies
- [ ] Directory structure matches architecture

### Notes

- Keep stub implementations simple - just print statements and return None/empty values
- Focus on defining clean interfaces that other tasks will implement
- Ensure all modules accept a `config` parameter for future configuration
- Use type hints for better code documentation
- Add docstrings to all public methods
