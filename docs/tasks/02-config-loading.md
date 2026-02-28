# Task: Config loading (YAML) + defaults

## Status

ready

## Goal

Implement `config.yaml` loading with defaults and basic validation so all components can read settings consistently.

## Acceptance criteria

- `config.yaml` exists with keys described in `docs/architecture.md` (menu/whisper/ollama/audio/privacy).
- App loads config at startup and merges with sensible defaults when values are missing.
- Invalid config values produce a clear, user-actionable error message.
- Config object is passed into components instead of using scattered globals.

## Dependencies

- Task 01 (project skeleton)

---

## Implementation Guide

### Configuration File Structure

#### `config.yaml` Example

```yaml
# Menu bar configuration
menu:
  show_copy_last: true # Show "Copy Last Result" menu option
  show_notifications: true # Show visual notifications for events

# Whisper speech recognition settings
whisper:
  model: "base" # Options: tiny, base, small, medium, large
  language: "en" # Language code or null for auto-detect

# Ollama LLM settings
ollama:
  host: "http://localhost:11434" # Ollama API endpoint
  model: "llama3.2:3b" # Model to use for text improvement
  timeout: 10 # Request timeout in seconds

# Audio recording settings
audio:
  sample_rate: 16000 # Hz (required by Whisper)
  channels: 1 # Mono audio
  silence_threshold: 0.01 # RMS amplitude threshold for silence
  silence_duration: 2.0 # Seconds of silence before auto-stop
  max_recording_duration: 60 # Maximum recording length in seconds

# Privacy and security settings
privacy:
  clear_clipboard_after: false # Clear clipboard after use
  clear_audio_buffer: true # Clear audio buffer after processing
  log_transcriptions: false # Never log transcriptions (privacy)
```

### Pseudocode: `config.py`

```
class Config:
    initialize(config_dict):
        - store configuration dictionary

    get(key_path, default):
        - split key_path by dots (e.g., "whisper.model" → ["whisper", "model"])
        - traverse nested dictionary
        - return value or default if not found

    validate():
        - check whisper.model in ['tiny', 'base', 'small', 'medium', 'large']
        - check audio.sample_rate == 16000 (Whisper requirement)
        - check audio.channels == 1 (mono)
        - check audio.silence_threshold in range [0.0, 1.0]
        - check audio.silence_duration >= 0
        - check audio.max_recording_duration > 0
        - check ollama.timeout > 0
        - raise ConfigError with clear message if invalid

get_default_config():
    - return dictionary with all default values:
        * menu: show_copy_last=true, show_notifications=true
        * whisper: model='base', language='en'
        * ollama: host='localhost:11434', model='llama3.2:3b', timeout=10
        * audio: sample_rate=16000, channels=1, thresholds, durations
        * privacy: clear flags, log_transcriptions=false

merge_configs(defaults, user):
    - deep merge user config into defaults
    - user values override defaults
    - preserve nested structure

load_config(path):
    - get default config
    - if config.yaml exists:
        * read and parse YAML
        * merge with defaults
    - else:
        * use defaults only
    - validate merged config
    - return Config object
    - raise ConfigError if validation fails
```

### Configuration Loading Flow

```
┌─────────────────────────────────────────────────────────┐
│                   Application Startup                    │
└───────────────────────┬─────────────────────────────────┘
                        │
                        ▼
            ┌───────────────────────┐
            │  load_config() called │
            └───────────┬───────────┘
                        │
                        ▼
            ┌───────────────────────┐
            │ Get default config    │
            └───────────┬───────────┘
                        │
                        ▼
            ┌───────────────────────┐
            │ config.yaml exists?   │
            └───────┬───────────────┘
                    │
        ┌───────────┴───────────┐
        │                       │
       NO                      YES
        │                       │
        ▼                       ▼
┌───────────────┐   ┌──────────────────────┐
│ Use defaults  │   │ Load YAML file       │
└───────┬───────┘   └──────────┬───────────┘
        │                      │
        │                      ▼
        │           ┌──────────────────────┐
        │           │ Parse YAML           │
        │           └──────────┬───────────┘
        │                      │
        │                      ▼
        │           ┌──────────────────────┐
        │           │ Merge with defaults  │
        │           └──────────┬───────────┘
        │                      │
        └──────────┬───────────┘
                   │
                   ▼
        ┌──────────────────────┐
        │ Validate config      │
        └──────────┬───────────┘
                   │
        ┌──────────┴──────────┐
        │                     │
    Valid                 Invalid
        │                     │
        ▼                     ▼
┌───────────────┐   ┌─────────────────────┐
│ Return Config │   │ Raise ConfigError   │
│ object        │   │ with clear message  │
└───────────────┘   └─────────────────────┘
```

### Validation Rules

| Setting                        | Type   | Valid Range                      | Default |
| ------------------------------ | ------ | -------------------------------- | ------- |
| `whisper.model`                | string | tiny, base, small, medium, large | base    |
| `whisper.language`             | string | ISO 639-1 code or null           | en      |
| `audio.sample_rate`            | int    | Must be 16000                    | 16000   |
| `audio.channels`               | int    | Must be 1                        | 1       |
| `audio.silence_threshold`      | float  | 0.0 - 1.0                        | 0.01    |
| `audio.silence_duration`       | float  | >= 0.0                           | 2.0     |
| `audio.max_recording_duration` | int    | > 0                              | 60      |
| `ollama.timeout`               | int    | > 0                              | 10      |
| `menu.show_notifications`      | bool   | true/false                       | true    |
| `privacy.log_transcriptions`   | bool   | true/false                       | false   |

### Testing Checklist

- [ ] Config loads successfully with valid YAML
- [ ] Missing config.yaml uses defaults
- [ ] Invalid YAML produces clear error message
- [ ] Invalid model name raises ConfigError
- [ ] Invalid sample_rate raises ConfigError
- [ ] Out-of-range values raise ConfigError
- [ ] Partial config merges with defaults correctly
- [ ] Dot notation access works (e.g., 'whisper.model')
- [ ] Config object can be passed to components

### Notes

- Config file is optional - app works with defaults
- Validation happens at startup to fail fast
- Error messages guide users to fix issues
- Deep merge preserves nested structure
- No global state - config passed explicitly
