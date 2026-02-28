# Task: Audio capture (sounddevice + numpy)

## Status

ready

## Goal

Implement microphone recording start/stop and buffer audio at 16kHz mono for Whisper.

## Acceptance criteria

- Start recording begins capturing audio frames from the selected input device.
- Stop recording returns a single contiguous `numpy` array (or bytes) representing the recording.
- Sample rate is 16kHz and channels is 1 (or safely downmixed to mono).
- Recording respects `max_recording_duration` from config.
- Audio device resources are released after stop.

## Dependencies

- Task 01 (project skeleton)
- Task 02 (config loading)

---

## Detailed Implementation Guide

### Audio Requirements

**Whisper Requirements:**

- Sample rate: **16000 Hz** (16 kHz)
- Channels: **1** (mono)
- Format: **float32** numpy array
- Range: **-1.0 to 1.0** (normalized)

**Configuration Parameters:**

```yaml
audio:
  sample_rate: 16000 # Required by Whisper
  channels: 1 # Mono
  max_recording_duration: 60 # Maximum seconds
```

### Pseudocode: `audio_handler.py`

```
class AudioHandler:
    initialize(config):
        - get sample_rate (16000 Hz)
        - get channels (1 = mono)
        - get max_duration (60 seconds)
        - create empty audio_queue
        - create empty audio_buffer
        - check audio device availability

    _audio_callback(indata, frames, time_info, status):
        - called by sounddevice for each audio block
        - if recording:
            * copy audio data to queue (non-blocking)

    start_recording():
        - check not already recording
        - clear previous buffers
        - set is_recording = true
        - create InputStream:
            * sample_rate: 16000 Hz
            * channels: 1 (mono)
            * dtype: float32
            * callback: _audio_callback
        - start stream

    stop_recording() → numpy array:
        - check is recording
        - set is_recording = false
        - stop and close stream
        - drain queue into buffer
        - concatenate all chunks into single array
        - if stereo, convert to mono (average channels)
        - flatten to 1D array
        - clear buffer if privacy.clear_audio_buffer enabled
        - return audio array (float32, 16kHz, mono)

    get_audio_level() → float:
        - get most recent audio chunk
        - calculate RMS (root mean square)
        - return amplitude (0.0-1.0)

    get_recording_duration() → float:
        - return elapsed time since start

    is_max_duration_reached() → bool:
        - check if duration >= max_duration

    cleanup():
        - stop stream if active
        - clear all buffers
        - release resources
```

### Audio Processing Flow

```
┌─────────────────────────────────────────────────────────┐
│                  Audio Capture Flow                      │
└─────────────────────────────────────────────────────────┘

1. start_recording()
   │
   ├─> Clear previous buffers
   ├─> Create InputStream (16kHz, mono, float32)
   ├─> Register callback function
   └─> Start stream

2. Audio Callback (runs continuously)
   │
   ├─> Receive audio block from microphone
   ├─> Check status for errors
   └─> Push block to queue (non-blocking)

3. Queue Processing (background)
   │
   └─> Blocks accumulate in queue

4. stop_recording()
   │
   ├─> Stop stream
   ├─> Drain queue into buffer
   ├─> Concatenate all blocks
   ├─> Convert to mono if needed
   ├─> Flatten to 1D array
   └─> Return numpy array (float32, 16kHz, mono)

5. cleanup() [on shutdown]
   │
   ├─> Stop stream if active
   ├─> Clear all buffers
   └─> Release resources
```

### Audio Data Format

**Input (from microphone):**

- Shape: (1024, 1) per callback - (frames, channels)
- Dtype: float32
- Range: -1.0 to 1.0

**Output (to Whisper):**

- Shape: (N,) - 1D array, N samples
- Dtype: float32
- Range: -1.0 to 1.0
- Sample rate: 16000 Hz
- Example: 5 seconds = 80,000 samples (5 × 16000)

### Common Issues & Solutions

**Issue:** `PortAudioError: No input device found`

- **Solution:** Check microphone is connected and enabled
- Verify permissions: System Preferences → Security & Privacy → Microphone

**Issue:** Audio is too quiet or silent

- **Solution:** Check microphone input level in System Preferences → Sound
- Verify correct input device is selected

**Issue:** `PortAudioError: Invalid sample rate`

- **Solution:** Some devices don't support 16kHz
- Use `sd.query_devices()` to check supported rates
- Resample if necessary (though 16kHz is standard)

**Issue:** Recording stops unexpectedly

- **Solution:** Check for buffer overruns
- Increase `blocksize` parameter if needed
- Ensure callback doesn't block

**Issue:** Memory usage grows during recording

- **Solution:** Implement max duration check
- Clear buffers after processing
- Use queue to limit buffer size

### Testing Checklist

- [ ] Audio device is detected and listed
- [ ] Recording starts without errors
- [ ] Audio is captured at 16kHz sample rate
- [ ] Output is mono (1 channel)
- [ ] Output dtype is float32
- [ ] Output range is -1.0 to 1.0
- [ ] Recording stops cleanly
- [ ] Buffers are cleared after stop
- [ ] Max duration is respected
- [ ] Multiple start/stop cycles work
- [ ] No memory leaks during long recordings
- [ ] Stream resources are released

### Performance Considerations

**Memory Usage:**

```python
# 1 minute of audio at 16kHz mono float32:
samples = 60 * 16000 = 960,000
bytes = 960,000 * 4 (float32) = 3.84 MB
```

**Latency:**

- Callback latency: ~20-50ms (depends on blocksize)
- Start latency: ~100-200ms (stream initialization)
- Stop latency: ~50-100ms (queue draining)

**CPU Usage:**

- Idle: <1% (callback only)
- Recording: 1-3% (queue management)

### Notes

- Always use `callback` mode for real-time recording
- Queue prevents blocking in audio callback
- Clear buffers for privacy after processing
- Handle stereo→mono conversion gracefully
- Validate sample rate matches Whisper requirements
- Release resources in cleanup() method
