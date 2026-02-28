# Task: Orchestrate pipeline + background processing

## Status

ready

## Goal

Wire together menu UI + audio recording + transcription + improvement + clipboard in a safe pipeline that keeps the menu bar responsive.

## Acceptance criteria

- Start Recording triggers audio capture without blocking the menu UI.
- Stop Recording triggers processing:
  - transcribe
  - improve
  - copy to clipboard
- While processing, new recording requests are ignored (MVP constraint).
- Menu bar state transitions are correct (idle -> recording -> processing -> idle).
- Terminal logs show key lifecycle events without logging transcriptions when `privacy.log_transcriptions: false`.

## Dependencies

- Task 03 (menu bar controller)
- Task 04 (audio capture)
- Task 06 (whisper integration)
- Task 07 (ollama improvement)
- Task 08 (clipboard)
- Task 02 (config loading)

---

## Implementation Guide

### Complete Pipeline Flow

```
┌─────────────────────────────────────────────────────────────┐
│                   Full Processing Pipeline                   │
└─────────────────────────────────────────────────────────────┘

[User clicks "Start Recording"]
         │
         ▼
┌─────────────────────┐
│  IDLE → RECORDING   │
└──────────┬──────────┘
           │
           ▼
    ┌──────────────┐
    │ Start Audio  │ ← audio_handler.start_recording()
    │  Capture     │
    └──────┬───────┘
           │
    [User speaks or silence detected]
           │
           ▼
[User clicks "Stop" OR auto-stop]
           │
           ▼
┌─────────────────────────┐
│ RECORDING → PROCESSING  │
└──────────┬──────────────┘
           │
           ▼
    ┌──────────────────┐
    │ Background Thread│ ← daemon=True
    │    Started       │
    └──────┬───────────┘
           │
           ├─> 1. Stop Audio
           │   └─> audio_handler.stop_recording()
           │   └─> Returns: numpy array
           │
           ├─> 2. Transcribe
           │   └─> transcriber.transcribe(audio)
           │   └─> Returns: raw text
           │
           ├─> 3. Improve
           │   └─> improver.improve_text(text)
           │   └─> Returns: improved text
           │
           ├─> 4. Copy
           │   └─> clipboard.copy_to_clipboard(text)
           │   └─> Show success notification
           │
           └─> 5. Complete
               └─> Set state: PROCESSING → IDLE
```

### Pseudocode: Pipeline Orchestration

```
class SpeakTypeApp:

    start_recording():
        - check state == IDLE
        - set_state(RECORDING)
        - audio_handler.start_recording()
        - show notification "Recording started"

    stop_recording():
        - check state == RECORDING
        - set_state(PROCESSING)
        - create background thread:
            * target = _process_audio
            * daemon = True
        - start thread
        - return immediately (UI stays responsive)

    _process_audio() [runs in background thread]:
        try:
            # Step 1: Stop audio
            audio = audio_handler.stop_recording()
            if audio is None:
                show_error("No audio captured")
                return

            # Step 2: Transcribe
            transcription = transcriber.transcribe(audio)
            if not transcription:
                show_error("Transcription failed")
                return

            # Step 3: Improve
            improved = improver.improve_text(transcription)

            # Step 4: Copy to clipboard
            success = clipboard.copy_to_clipboard(improved)
            if success:
                last_result = improved
                show_success(improved)
            else:
                show_error("Failed to copy")

        except Exception as e:
            show_error(str(e))

        finally:
            # Always return to idle
            set_state(IDLE)
```

### Threading Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Thread Architecture                     │
└─────────────────────────────────────────────────────────────┘

Main Thread (rumps):
├─> Menu bar UI
├─> Event handling
├─> State updates
└─> User interactions
    │
    └─> Spawns ──────────────┐
                             │
                             ▼
                    Background Thread (daemon):
                    ├─> Audio processing
                    ├─> Whisper transcription
                    ├─> Ollama improvement
                    └─> Clipboard operations
                        │
                        └─> Calls back to main thread
                            for state updates

Key Points:
- Main thread never blocks
- Background thread is daemon (dies with app)
- State updates are thread-safe
- Only one processing thread at a time (MVP)
```

### State Machine

```
States: IDLE, RECORDING, PROCESSING

Transitions:

IDLE ──[Start Recording]──> RECORDING
                              │
                              │
IDLE <──[Pipeline Complete]── PROCESSING
                              ▲
                              │
                              │
RECORDING ──[Stop/Silence]──> PROCESSING

Rules:
- Start only allowed from IDLE
- Stop only allowed from RECORDING
- New recording blocked during PROCESSING
- Quit allowed from any state
```

### Concurrency Control

```
MVP Constraint: Single-task pipeline

if state == PROCESSING:
    - ignore "Start Recording" clicks
    - show message "Processing in progress"
    - wait for current pipeline to complete

Why:
- Simpler implementation
- Avoids race conditions
- Prevents resource conflicts
- Sufficient for MVP use case
```

### Error Handling in Pipeline

```
Each step has error handling:

1. Audio capture fails:
   → Show error "No audio captured"
   → Return to IDLE
   → Don't proceed to transcription

2. Transcription fails:
   → Show error "Transcription failed"
   → Return to IDLE
   → Don't proceed to improvement

3. Improvement fails:
   → Use raw transcription (fallback)
   → Show warning "Using raw transcription"
   → Proceed to clipboard

4. Clipboard fails:
   → Show error "Failed to copy"
   → Return to IDLE
   → Text is lost (user must retry)

All errors:
   → Log to terminal
   → Show user notification
   → Return to IDLE state
   → Never crash the app
```

### Privacy Considerations

```
After each pipeline run:

1. Clear audio buffer
   - if privacy.clear_audio_buffer == true
   - audio_handler clears internal buffers

2. Don't log transcriptions
   - if privacy.log_transcriptions == false
   - only log "Transcribed X seconds"
   - never log actual text content

3. Optional clipboard clear
   - if privacy.clear_clipboard_after == true
   - clear after user pastes or timeout
```

### Testing Checklist

- [ ] Start → Record → Stop → Process → Copy works end-to-end
- [ ] Menu bar stays responsive during processing
- [ ] State transitions are correct
- [ ] New recording blocked during processing
- [ ] Background thread completes successfully
- [ ] Errors don't crash the app
- [ ] Privacy settings are respected
- [ ] Terminal logs show pipeline progress
- [ ] Notifications appear at each step
- [ ] Multiple recording cycles work

### Performance Expectations

**Total Pipeline Time:**

- Audio capture: Real-time (user-controlled)
- Stop audio: ~100ms
- Transcription: 0.5-1.5s (base model)
- Improvement: 0.5-2s (llama3.2:3b)
- Clipboard: <10ms
- **Total processing: 1-4 seconds**

### Notes

- Background thread keeps UI responsive
- daemon=True ensures thread dies with app
- Only one processing thread at a time (MVP)
- State machine prevents invalid transitions
- All errors are caught and handled gracefully
- Privacy settings applied after each run
