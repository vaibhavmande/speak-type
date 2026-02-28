# Task: Add small unit tests (pure logic)

## Status

ready

## Goal

Add basic tests for the logic that can be tested without microphone/LLM.

## Acceptance criteria

- Tests exist for:
  - silence detection helper(s)
  - config parsing/merging defaults
  - prompt builder for improvement step
- Tests can be run locally with a single command (documented).

## Dependencies

- Task 02 (config loading)
- Task 05 (silence detection)
- Task 07 (ollama improvement) (prompt builder)

---

## Implementation Guide

### Test Structure

```
tests/
├── __init__.py
├── test_config.py              # Config loading and validation
├── test_silence_detection.py   # Silence detection logic
└── test_text_improver.py       # Prompt building
```

### Test Framework

```bash
# Run tests
python -m pytest tests/

# Run with coverage
python -m pytest --cov=. tests/

# Run specific test file
python -m pytest tests/test_config.py
```

### Pseudocode: `test_config.py`

```python
import pytest
from config import Config, load_config, merge_configs, ConfigError

test_dot_notation_access():
    - create Config with nested dict
    - assert config.get('whisper.model') returns correct value
    - assert config.get('missing.key', 'default') returns 'default'

test_config_validation_valid():
    - create Config with valid values
    - call config.validate()
    - assert no exception raised

test_config_validation_invalid_model():
    - create Config with invalid whisper.model
    - assert validate() raises ConfigError
    - assert error message mentions valid models

test_config_validation_invalid_sample_rate():
    - create Config with sample_rate != 16000
    - assert validate() raises ConfigError
    - assert error message mentions 16000 requirement

test_merge_configs():
    - create defaults dict
    - create user dict with partial overrides
    - merged = merge_configs(defaults, user)
    - assert user values override defaults
    - assert missing user values use defaults
    - assert nested dicts are merged correctly

test_load_config_missing_file():
    - delete config.yaml if exists
    - config = load_config()
    - assert config uses defaults
    - assert no exception raised

test_load_config_invalid_yaml():
    - create config.yaml with invalid YAML syntax
    - assert load_config() raises ConfigError
    - assert error message mentions YAML error
```

### Pseudocode: `test_silence_detection.py`

```python
import numpy as np
from audio_handler import calculate_rms, check_silence

test_calculate_rms_zero():
    - audio = np.zeros(1000)
    - rms = calculate_rms(audio)
    - assert rms == 0.0

test_calculate_rms_constant():
    - audio = np.full(1000, 0.5)
    - rms = calculate_rms(audio)
    - assert rms ≈ 0.5

test_calculate_rms_varying():
    - audio = np.array([0.1, -0.2, 0.15, -0.1, 0.05])
    - rms = calculate_rms(audio)
    - expected = sqrt(mean([0.01, 0.04, 0.0225, 0.01, 0.0025]))
    - assert rms ≈ expected

test_silence_detection_below_threshold():
    - threshold = 0.01
    - duration = 2.0
    - audio_level = 0.005  # Below threshold
    - time_elapsed = 2.5   # Above duration
    - assert check_silence(audio_level, threshold, duration, time_elapsed) == True

test_silence_detection_above_threshold():
    - threshold = 0.01
    - audio_level = 0.05  # Above threshold
    - assert check_silence(audio_level, threshold, duration, time_elapsed) == False

test_silence_detection_insufficient_duration():
    - threshold = 0.01
    - duration = 2.0
    - audio_level = 0.005  # Below threshold
    - time_elapsed = 1.0   # Below duration
    - assert check_silence(audio_level, threshold, duration, time_elapsed) == False

test_silence_detection_disabled():
    - duration = 0  # Disabled
    - assert check_silence(any_level, threshold, duration, any_time) == False
```

### Pseudocode: `test_text_improver.py`

```python
from text_improver import TextImprover, build_prompt

test_build_prompt_structure():
    - text = "test input"
    - prompt = build_prompt(text)
    - assert "Fix grammar" in prompt
    - assert "improve clarity" in prompt
    - assert "Keep the original meaning" in prompt
    - assert "Output only" in prompt
    - assert text in prompt

test_build_prompt_preserves_input():
    - text = "the quick brown fox"
    - prompt = build_prompt(text)
    - assert text in prompt
    - assert prompt.endswith(text) or text in prompt.split('\n\n')

test_improve_text_fallback():
    - improver = TextImprover(config)
    - mock Ollama unavailable
    - original = "test text"
    - result = improver.improve_text(original)
    - assert result == original  # Fallback to original

test_improve_text_success():
    - improver = TextImprover(config)
    - mock Ollama response with improved text
    - original = "the quick brown fox jump"
    - result = improver.improve_text(original)
    - assert result != original
    - assert "jumps" in result  # Improved grammar
```

### Test Data Examples

**Valid Config:**

```python
valid_config = {
    'whisper': {'model': 'base', 'language': 'en'},
    'audio': {'sample_rate': 16000, 'channels': 1},
    'ollama': {'host': 'http://localhost:11434', 'timeout': 10}
}
```

**Invalid Config:**

```python
invalid_config = {
    'whisper': {'model': 'invalid'},  # Bad model
    'audio': {'sample_rate': 44100}    # Wrong rate
}
```

**Test Audio Data:**

```python
silent_audio = np.zeros(16000)  # 1 second of silence
noisy_audio = np.random.uniform(-0.5, 0.5, 16000)  # Random noise
quiet_audio = np.random.uniform(-0.005, 0.005, 16000)  # Below threshold
```

### Mocking External Dependencies

```python
# Mock Ollama API
@pytest.fixture
def mock_ollama(monkeypatch):
    def mock_post(*args, **kwargs):
        return MockResponse({
            'response': 'Improved text',
            'done': True
        })
    monkeypatch.setattr('requests.post', mock_post)

# Mock audio device
@pytest.fixture
def mock_sounddevice(monkeypatch):
    def mock_query_devices():
        return [{'name': 'Test Device', 'max_input_channels': 1}]
    monkeypatch.setattr('sounddevice.query_devices', mock_query_devices)
```

### Testing Checklist

**Config Tests:**

- [ ] Dot notation access works
- [ ] Validation catches invalid values
- [ ] Merge preserves defaults and overrides
- [ ] Missing file uses defaults
- [ ] Invalid YAML raises error

**Silence Detection Tests:**

- [ ] RMS calculation is accurate
- [ ] Silence detected when below threshold
- [ ] Silence reset when above threshold
- [ ] Duration requirement enforced
- [ ] Disabled mode works (duration=0)

**Text Improver Tests:**

- [ ] Prompt structure is correct
- [ ] Input text preserved in prompt
- [ ] Fallback works when Ollama unavailable
- [ ] Success case returns improved text

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run all tests
pytest tests/

# Run with verbose output
pytest -v tests/

# Run specific test
pytest tests/test_config.py::test_dot_notation_access

# Run with coverage report
pytest --cov=. --cov-report=html tests/
```

### Notes

- Focus on pure logic (no I/O dependencies)
- Mock external services (Ollama, audio devices)
- Test edge cases and error conditions
- Keep tests fast (<1s total)
- Use fixtures for common setup
- Test one thing per test function
