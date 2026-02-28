# Task: Graceful shutdown + cleanup

## Status

ready

## Goal

Ensure the app shuts down cleanly from both menu "Quit" and terminal `Ctrl+C` with all resources released.

## Acceptance criteria

- Audio stream is stopped and device released on shutdown.
- Whisper resources are released/unloaded (or process exits cleanly without hanging).
- Background threads are joined/cancelled.
- Menu bar icon disappears on quit.
- Shutdown prints a short terminal message sequence (no sensitive data).

## Dependencies

- Task 09 (orchestration)

---

## Implementation Guide

### Shutdown Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    Graceful Shutdown Flow                    │
└─────────────────────────────────────────────────────────────┘

[User clicks "Quit" OR presses Ctrl+C]
         │
         ▼
┌─────────────────────┐
│  Shutdown Initiated │
└──────────┬──────────┘
           │
           ├─> 1. Stop Audio (if recording)
           │   └─> audio_handler.cleanup()
           │       ├─> Stop stream
           │       ├─> Close device
           │       └─> Clear buffers
           │
           ├─> 2. Unload Whisper Model
           │   └─> transcriber.unload_model()
           │       └─> Free memory (~500MB)
           │
           ├─> 3. Close Ollama Connection
           │   └─> improver.cleanup()
           │       └─> Close HTTP session
           │
           ├─> 4. Wait for Background Threads
           │   └─> Join processing thread (if running)
           │       └─> Max wait: 5 seconds
           │
           ├─> 5. Clear Sensitive Data
           │   └─> Clear last_result
           │   └─> Clear audio buffers
           │
           └─> 6. Exit Application
               └─> Remove menu bar icon
               └─> Exit with code 0
```

### Pseudocode: Shutdown Logic

```
class SpeakTypeApp:

    quit_app():
        print("[Shutdown] Initiating graceful shutdown...")

        # 1. Stop audio if recording
        if state == RECORDING:
            print("[Shutdown] Stopping active recording...")
            audio_handler.cleanup()

        # 2. Wait for processing to complete
        if processing_thread and processing_thread.is_alive():
            print("[Shutdown] Waiting for processing to complete...")
            processing_thread.join(timeout=5.0)
            if processing_thread.is_alive():
                print("[Shutdown] Warning: Processing thread still running")

        # 3. Cleanup components
        print("[Shutdown] Cleaning up components...")
        cleanup_all_components()

        # 4. Clear sensitive data
        print("[Shutdown] Clearing sensitive data...")
        last_result = ""

        # 5. Exit
        print("[Shutdown] Shutdown complete. Goodbye!")
        rumps.quit_application()

    cleanup_all_components():
        # Audio
        if audio_handler:
            audio_handler.cleanup()

        # Whisper
        if transcriber:
            transcriber.unload_model()

        # Ollama (if needed)
        if improver:
            improver.cleanup()

        # Clipboard (if needed)
        if clipboard:
            clipboard.cleanup()


class AudioHandler:
    cleanup():
        - stop stream if active
        - close audio device
        - clear audio_buffer
        - clear audio_queue
        - set is_recording = False


class WhisperTranscriber:
    unload_model():
        - free model from memory
        - set model = None
        - log "Whisper model unloaded"


class TextImprover:
    cleanup():
        - close HTTP session (if persistent)
        - log "Ollama connection closed"


class ClipboardManager:
    cleanup():
        - optionally clear clipboard
        - log "Clipboard manager cleaned up"
```

### Signal Handling (Ctrl+C)

```
import signal
import sys

def signal_handler(sig, frame):
    print("\n[Signal] Received interrupt signal")
    # Trigger graceful shutdown
    app.quit_app()
    sys.exit(0)

# Register signal handler
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)
```

### Cleanup Checklist by Component

**Audio Handler:**

- [ ] Stop audio stream
- [ ] Close audio device
- [ ] Clear audio_buffer list
- [ ] Clear audio_queue
- [ ] Set is_recording = False

**Whisper Transcriber:**

- [ ] Unload model from memory
- [ ] Set model = None
- [ ] Free ~500MB RAM

**Text Improver:**

- [ ] Close HTTP session (if any)
- [ ] No persistent state to clean

**Clipboard Manager:**

- [ ] Optionally clear clipboard
- [ ] No persistent state

**Main App:**

- [ ] Join background threads
- [ ] Clear last_result
- [ ] Remove menu bar icon

### Shutdown Scenarios

**Scenario 1: Quit from IDLE**

```
State: IDLE
Action: Click "Quit"
Steps:
  1. Cleanup components
  2. Exit immediately
Time: <1 second
```

**Scenario 2: Quit while RECORDING**

```
State: RECORDING
Action: Click "Quit"
Steps:
  1. Stop audio recording
  2. Cleanup audio handler
  3. Cleanup other components
  4. Exit
Time: ~1 second
```

**Scenario 3: Quit while PROCESSING**

```
State: PROCESSING
Action: Click "Quit"
Steps:
  1. Wait for processing thread (max 5s)
  2. If thread still running, warn and continue
  3. Cleanup components
  4. Exit
Time: 1-5 seconds
```

**Scenario 4: Ctrl+C in Terminal**

```
Action: Press Ctrl+C
Steps:
  1. Signal handler catches SIGINT
  2. Calls quit_app()
  3. Same as normal quit
Time: 1-5 seconds
```

### Terminal Output Example

```
[User presses Ctrl+C]

^C
[Signal] Received interrupt signal
[Shutdown] Initiating graceful shutdown...
[Shutdown] Stopping active recording...
[Audio] Stopping recording...
[Audio] Cleaning up...
[Audio] Cleanup complete
[Shutdown] Cleaning up components...
[Whisper] Unloading model...
[Whisper] Model unloaded
[Ollama] Connection closed
[Shutdown] Clearing sensitive data...
[Shutdown] Shutdown complete. Goodbye!
```

### Testing Checklist

- [ ] Quit from IDLE works
- [ ] Quit while recording stops audio cleanly
- [ ] Quit while processing waits for completion
- [ ] Ctrl+C triggers graceful shutdown
- [ ] All resources are released
- [ ] No memory leaks
- [ ] Menu bar icon disappears
- [ ] Terminal shows shutdown messages
- [ ] No error messages during shutdown
- [ ] App exits with code 0

### Error Handling During Shutdown

```
If cleanup fails:
  - Log error but continue shutdown
  - Don't block exit on cleanup errors
  - Ensure app always exits

Example:
  try:
      audio_handler.cleanup()
  except Exception as e:
      print(f"[Shutdown] Warning: Audio cleanup failed: {e}")
      # Continue anyway
```

### Memory Cleanup

**Before Shutdown:**

- Whisper model: ~500MB
- Ollama (external): ~2GB
- Audio buffers: ~4MB
- Python process: ~100MB
- **Total: ~600MB in Python process**

**After Shutdown:**

- All memory freed
- Process terminated
- Ollama continues running (external service)

### Notes

- Graceful shutdown prevents data loss
- Always cleanup audio resources first
- Wait for background threads (with timeout)
- Clear sensitive data before exit
- Handle Ctrl+C same as menu Quit
- Log all shutdown steps for debugging
- Never block indefinitely during shutdown
