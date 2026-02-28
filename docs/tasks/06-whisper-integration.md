# Task: Whisper transcription integration (whisper.cpp via whispercpp)

## Status

ready

## Goal

Integrate local speech recognition using `whispercpp` (or a controlled subprocess wrapper) and transcribe recorded audio.

## Acceptance criteria

- Whisper model loads once at startup (per config: `whisper.model`).
- `transcribe(audio)` returns a transcription string.
- Errors (missing model, missing binary, unsupported input shape) produce a clear message and do not crash the menu UI.
- Transcription respects optional language setting (`whisper.language`) if configured.

## Dependencies

- Task 04 (audio capture)
- Task 02 (config loading)
- Task 01 (project skeleton)

---

## Implementation Guide

### Whisper Model Selection

| Model  | Size  | Speed     | Accuracy | Use Case              |
| ------ | ----- | --------- | -------- | --------------------- |
| tiny   | 75MB  | Very fast | Low      | Testing only          |
| base   | 140MB | Fast      | Good     | **Recommended (MVP)** |
| small  | 460MB | Medium    | Better   | Higher accuracy needs |
| medium | 1.5GB | Slow      | High     | Production quality    |
| large  | 2.9GB | Very slow | Highest  | Maximum accuracy      |

### Pseudocode: `transcription.py`

```
class WhisperTranscriber:
    initialize(config):
        - model_name = config.get('whisper.model', 'base')
        - language = config.get('whisper.language', 'en')
        - model = None

    load_model():
        - check if model file exists in models/ directory
        - if not exists:
            * download model from Whisper repository
        - load model into memory using whispercpp
        - print "Model loaded: {model_name}"

    transcribe(audio_array) → string:
        - validate audio format:
            * check dtype is float32
            * check sample_rate is 16000 Hz
            * check is 1D array (mono)
        - if model not loaded:
            * raise error "Model not loaded"
        - pass audio to Whisper model
        - get transcription result
        - return transcribed text
        - on error:
            * log error
            * return None

    unload_model():
        - free model from memory
        - set model = None
```

### Transcription Flow

```
┌─────────────────────────────────────────────────────┐
│              Whisper Transcription Flow             │
└─────────────────────────────────────────────────────┘

1. Application Startup
   │
   ├─> Check if model exists in models/
   ├─> If missing, download model
   └─> Load model into memory

2. Audio Recording Complete
   │
   ├─> Receive audio array (float32, 16kHz, mono)
   └─> Validate format

3. Transcription
   │
   ├─> Pass audio to Whisper
   ├─> Whisper processes audio
   └─> Return transcribed text

4. Error Handling
   │
   ├─> Model not loaded → Load model
   ├─> Invalid audio format → Return error
   └─> Transcription failed → Return None

5. Shutdown
   │
   └─> Unload model from memory
```

### Model Loading

```yaml
whisper:
  model: "base" # Model size to use
  language: "en" # Language code or null for auto-detect
```

**Model Storage:**

```
models/
├── ggml-base.bin       # Downloaded on first run
└── ggml-small.bin      # Optional
```

### Audio Format Requirements

**Input to Whisper:**

- Format: numpy array, dtype=float32
- Sample rate: 16000 Hz
- Channels: 1 (mono)
- Shape: (N,) where N = samples
- Range: -1.0 to 1.0 (normalized)

**Example:**

```
audio.shape = (80000,)     # 5 seconds at 16kHz
audio.dtype = float32
audio.min() = -0.8
audio.max() = 0.9
```

### Error Handling

**Common Errors:**

1. Model not found → Download automatically
2. Invalid audio format → Validate and convert
3. Transcription timeout → Retry or return None
4. Memory error → Use smaller model

### Testing Checklist

- [ ] Model downloads on first run
- [ ] Model loads successfully
- [ ] Transcription works with valid audio
- [ ] Invalid audio format raises clear error
- [ ] Language setting is respected
- [ ] Model unloads on shutdown
- [ ] Multiple transcriptions work
- [ ] Error messages are user-friendly

### Performance

**Base Model:**

- Load time: 1-2 seconds
- Transcription: ~0.5-1.5 seconds for 5s audio
- Memory: ~500MB

**Optimization:**

- Load model once at startup (not per transcription)
- Keep model in memory during app lifetime
- Unload only on shutdown

### Notes

- Use `whispercpp` Python bindings for whisper.cpp
- Model files stored in `models/` directory
- Base model recommended for MVP (good balance)
- Language auto-detection works but is slower
- Transcription runs on CPU (no GPU needed for base model)
