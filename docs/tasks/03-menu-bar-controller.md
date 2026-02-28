# Task: Menu bar controller (rumps)

## Status

ready

## Goal

Build the macOS menu-bar UI using `rumps` with clear states and menu actions.

## Acceptance criteria

- Menu bar icon shows at least 3 states:
  - idle (ready)
  - recording
  - processing
- Menu includes actions:
  - Start Recording
  - Stop Recording
  - Copy Last Result
  - Quit
- Start/Stop actions call into the backend pipeline (even if backend is stubbed initially).
- Quit performs graceful shutdown.

## Dependencies

- Task 01 (project skeleton)

---

## Detailed Implementation Guide

### Menu Bar States

The application has three primary visual states:

| State          | Icon         | Title           | Tooltip                 | Menu Actions Available           |
| -------------- | ------------ | --------------- | ----------------------- | -------------------------------- |
| **Idle**       | 🎤 (gray)    | ""              | "Ready. Click to start" | Start Recording, Copy Last, Quit |
| **Recording**  | 🔴 (red)     | "Recording..."  | "Click to stop"         | Stop Recording, Quit             |
| **Processing** | ⏳ (spinner) | "Processing..." | "Please wait"           | Quit (all others disabled)       |

### State Transition Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     Application States                       │
└─────────────────────────────────────────────────────────────┘

                    ┌──────────────┐
                    │   STARTUP    │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
          ┌────────▶│     IDLE     │◀────────┐
          │         │   🎤 Ready   │         │
          │         └──────┬───────┘         │
          │                │                 │
          │    [Start Recording clicked]     │
          │                │                 │
          │                ▼                 │
          │         ┌──────────────┐         │
          │         │  RECORDING   │         │
          │         │ 🔴 Listening │         │
          │         └──────┬───────┘         │
          │                │                 │
          │    [Stop clicked OR silence]     │
          │                │                 │
          │                ▼                 │
          │         ┌──────────────┐         │
          │         │  PROCESSING  │         │
          │         │ ⏳ Working... │         │
          │         └──────┬───────┘         │
          │                │                 │
          │    [Pipeline complete]           │
          │                │                 │
          └────────────────┴─────────────────┘

                    [Quit clicked]
                           │
                           ▼
                    ┌──────────────┐
                    │   SHUTDOWN   │
                    └──────────────┘
```

### Pseudocode: `main.py`

```
enum AppState:
    IDLE
    RECORDING
    PROCESSING

class SpeakTypeApp(rumps.App):
    """Main menu bar application controller."""

    initialize(config):
        - create menu bar icon (🎤)
        - initialize components (audio, transcriber, improver, clipboard)
        - create menu items (Start, Stop, Copy Last, Quit)
        - set state to IDLE

    set_state(new_state):
        - update icon and title based on state:
            * IDLE: 🎤, enable Start/Copy, disable Stop
            * RECORDING: 🔴 "Recording...", enable Stop, disable Start/Copy
            * PROCESSING: ⏳ "Processing...", disable all except Quit

    start_recording():
        - check state is IDLE
        - set state to RECORDING
        - call audio_handler.start_recording()
        - show notification "Recording started"

    stop_recording():
        - check state is RECORDING
        - set state to PROCESSING
        - start background thread for _process_audio()

    _process_audio() [background thread]:
        - stop audio and get buffer
        - transcribe audio → text
        - improve text via LLM
        - copy to clipboard
        - show success/error notification
        - set state back to IDLE

    copy_last():
        - if last_result exists:
            * copy to clipboard
            * show notification
        - else:
            * show "No result" message

    quit_app():
        - cleanup resources (Task 10)
        - exit application

main():
    - load configuration
    - create SpeakTypeApp
    - run menu bar app
```

### Menu Interaction Patterns

#### Pattern 1: Normal Recording Flow

```
User Action          →  State Change     →  UI Update
─────────────────────────────────────────────────────────
Click "Start"        →  IDLE → RECORDING →  Icon: 🔴
                                             Title: "Recording..."
                                             Notification shown

User speaks          →  (no state change) →  (audio buffering)

Click "Stop"         →  RECORDING →       →  Icon: ⏳
                        PROCESSING           Title: "Processing..."
                                             All menu items disabled

Processing complete  →  PROCESSING →      →  Icon: 🎤
                        IDLE                 Title: ""
                                             Success notification
```

#### Pattern 2: Copy Last Result

```
User Action          →  Condition         →  Result
─────────────────────────────────────────────────────────
Click "Copy Last"    →  Has last_result   →  Copy to clipboard
                                             Show notification

Click "Copy Last"    →  No last_result    →  Show "No result" message
```

#### Pattern 3: Quit During Recording

```
User Action          →  State             →  Cleanup
─────────────────────────────────────────────────────────
Click "Quit"         →  RECORDING         →  Stop audio capture
                                             Release resources
                                             Exit app
```

### Threading Considerations

- `rumps` runs on main thread (macOS NSRunLoop requirement)
- Audio processing (Whisper + Ollama) takes 1-4 seconds
- Use background thread (daemon=True) to keep menu bar responsive
- State updates via set_state() are thread-safe for rumps

### Testing Checklist

- [ ] Menu bar icon appears in macOS menu bar
- [ ] Icon changes correctly: 🎤 → 🔴 → ⏳ → 🎤
- [ ] Title updates match state transitions
- [ ] "Start Recording" only enabled when IDLE
- [ ] "Stop Recording" only enabled when RECORDING
- [ ] "Copy Last" disabled during PROCESSING
- [ ] Notifications appear (if enabled in config)
- [ ] "Copy Last" shows error when no result exists
- [ ] Quit works from any state
- [ ] Menu remains responsive during processing

### Common Issues & Solutions

**Issue:** Menu bar icon doesn't appear

- **Solution:** Check Terminal permissions for menu bar access
- Run: `tccutil reset All` and restart Terminal

**Issue:** Menu freezes during processing

- **Solution:** Ensure processing happens in background thread
- Verify `daemon=True` on processing thread

**Issue:** State transitions don't update UI

- **Solution:** Always use `set_state()` method
- Never modify `self.state` directly

**Issue:** Notifications don't appear

- **Solution:** Check System Preferences → Notifications
- Ensure Python/Terminal has notification permissions

### Notes

- `rumps` requires macOS 10.10+
- Menu bar app must run on main thread
- Use `daemon=True` for background threads
- State machine prevents invalid transitions
- Notifications are optional (configurable)
- Menu items can be dynamically enabled/disabled
