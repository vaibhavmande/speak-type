# Task: Silence detection + auto-stop

## Status

ready

## Goal

Detect sustained silence and automatically stop recording after `silence_duration` seconds below `silence_threshold`.

## Acceptance criteria

- Silence detection works reliably on the buffered audio stream.
- When silence is detected for the configured duration, recording auto-stops.
- Auto-stop is disabled or configurable if the user sets `silence_duration: 0`.
- Logic is testable (pure function) independent of `sounddevice`.

## Dependencies

- Task 04 (audio capture)
- Task 02 (config loading)

---

## Implementation Guide

### Silence Detection Algorithm

```
Silence Detection Flow:

1. Get current audio level (RMS)
2. Compare to silence_threshold
3. If below threshold:
   - increment silence_counter
   - if silence_counter >= silence_duration:
     * trigger auto-stop
4. If above threshold:
   - reset silence_counter to 0
```

### Pseudocode: Silence Detection

```
class SilenceDetector:
    initialize(threshold, duration):
        - silence_threshold = threshold (e.g., 0.01)
        - silence_duration = duration (e.g., 2.0 seconds)
        - silence_start_time = None

    check_silence(audio_level, current_time) → bool:
        - if audio_level < silence_threshold:
            * if silence_start_time is None:
                - silence_start_time = current_time
            * elapsed = current_time - silence_start_time
            * if elapsed >= silence_duration:
                - return True (silence detected)
        - else:
            * silence_start_time = None (reset)
        - return False

    calculate_rms(audio_chunk) → float:
        - square all samples
        - calculate mean of squares
        - return square root of mean
        - result is amplitude 0.0-1.0
```

### Integration with AudioHandler

```
In audio_handler.py:

while recording:
    - get current audio level via get_audio_level()
    - check if silence detected
    - if silence detected for silence_duration:
        * auto-stop recording
        * trigger processing pipeline
```

### RMS Calculation Diagram

```
Audio Chunk: [0.1, -0.2, 0.15, -0.1, 0.05]
                    ↓
            Square each value
                    ↓
         [0.01, 0.04, 0.0225, 0.01, 0.0025]
                    ↓
            Calculate mean
                    ↓
              0.0210 (mean)
                    ↓
            Square root
                    ↓
              0.145 (RMS)
```

### Configuration

```yaml
audio:
  silence_threshold: 0.01 # RMS amplitude threshold
  silence_duration: 2.0 # Seconds of silence before auto-stop
```

**Tuning Guidelines:**

- Lower threshold (0.005): More sensitive, stops on quiet speech
- Higher threshold (0.02): Less sensitive, requires louder silence
- Shorter duration (1.0s): Faster auto-stop, may cut off pauses
- Longer duration (3.0s): Slower auto-stop, more forgiving

### Testing Checklist

- [ ] Silence detected when audio below threshold
- [ ] Silence timer resets when audio above threshold
- [ ] Auto-stop triggers after silence_duration
- [ ] RMS calculation is accurate
- [ ] Configurable threshold and duration work
- [ ] Silence detection can be disabled (duration=0)
- [ ] Works with varying audio levels

### Notes

- RMS (Root Mean Square) measures audio amplitude
- Threshold of 0.01 works well for most microphones
- Silence detection is optional (set duration to 0 to disable)
- Check silence in main recording loop or background thread
- Clear silence state when recording stops
