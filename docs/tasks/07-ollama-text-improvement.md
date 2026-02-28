# Task: Ollama text improvement (localhost)

## Status

ready

## Goal

Call local Ollama (`/api/generate`) to improve transcription using the system prompt described in the architecture.

## Acceptance criteria

- `improve_text(transcription)` returns improved text when Ollama is running.
- Uses config keys:
  - `ollama.host`
  - `ollama.model`
  - `ollama.timeout`
- If Ollama is unavailable/timeouts/error:
  - falls back to returning the raw transcription
  - surfaces a user-visible notification or menu title update indicating fallback
- Prompt is deterministic and outputs only improved text.

## Dependencies

- Task 02 (config loading)
- Task 01 (project skeleton)

---

## Implementation Guide

### Pseudocode: `text_improver.py`

```
class TextImprover:
    initialize(config):
        - host = config.get('ollama.host', 'http://localhost:11434')
        - model = config.get('ollama.model', 'llama3.2:3b')
        - timeout = config.get('ollama.timeout', 10)

    improve_text(transcription) → string:
        - build_prompt(transcription)
        - try:
            * call Ollama API at /api/generate
            * send: {model, prompt, stream: false}
            * wait for response (max timeout seconds)
            * extract improved text from response
            * return improved text
        - except (timeout, connection error, API error):
            * log warning "Ollama unavailable, using raw transcription"
            * show notification "Text improvement unavailable"
            * return original transcription (fallback)

    build_prompt(text) → string:
        - system_instruction = "Fix grammar, improve clarity and phrasing."
        - system_instruction += "Keep the original meaning intact."
        - system_instruction += "Output only the improved text."
        - return system_instruction + "\n\n" + text

    check_ollama_available() → bool:
        - try:
            * GET request to http://localhost:11434/api/tags
            * return True if status 200
        - except:
            * return False
```

### Text Improvement Flow

```
┌─────────────────────────────────────────────────────────┐
│              Ollama Text Improvement Flow               │
└─────────────────────────────────────────────────────────┘

1. Receive Transcription
   │
   └─> Raw text from Whisper

2. Build Prompt
   │
   ├─> Add system instructions
   ├─> Add transcription text
   └─> Format for Ollama

3. Call Ollama API
   │
   ├─> POST to /api/generate
   ├─> Send model + prompt
   └─> Wait for response (max 10s)

4. Handle Response
   │
   ├─> Success → Extract improved text
   └─> Error → Fallback to original

5. Return Result
   │
   └─> Improved text or original (if failed)
```

### Ollama API Request

```json
POST http://localhost:11434/api/generate

{
  "model": "llama3.2:3b",
  "prompt": "Fix grammar, improve clarity and phrasing.\nKeep the original meaning intact.\nOutput only the improved text.\n\nthe quick brown fox jump over lazy dog",
  "stream": false
}
```

**Response:**

```json
{
  "model": "llama3.2:3b",
  "response": "The quick brown fox jumps over the lazy dog.",
  "done": true
}
```

### System Prompt Design

**Effective Prompt:**

```
Fix grammar, improve clarity and phrasing.
Keep the original meaning intact.
Output only the improved text.
```

**Why This Works:**

- Clear, specific instructions
- Emphasizes preserving meaning
- Requests clean output (no explanations)
- Short and efficient

### Fallback Strategy

```
if Ollama unavailable:
    1. Log warning message
    2. Show user notification
    3. Return original transcription
    4. Continue pipeline (don't crash)

Reasons for fallback:
- Ollama not running
- Network timeout
- Model not loaded
- API error
```

### Configuration

```yaml
ollama:
  host: "http://localhost:11434" # Ollama API endpoint
  model: "llama3.2:3b" # Model to use
  timeout: 10 # Request timeout (seconds)
```

**Recommended Models:**

- `llama3.2:3b` - Fast, good quality (recommended)
- `qwen2.5:3b` - Excellent at text refinement
- `llama3.2:1b` - Faster, lower quality

### Error Handling

**Common Errors:**

1. Ollama not running → Fallback to original
2. Model not found → Download model or fallback
3. Timeout → Fallback to original
4. Invalid response → Fallback to original

**User-Friendly Messages:**

- "Text improvement unavailable - using transcription as-is"
- "Ollama not running - check if service is started"

### Testing Checklist

- [ ] Ollama connection works when service running
- [ ] Text improvement produces better output
- [ ] Fallback works when Ollama unavailable
- [ ] Timeout is respected
- [ ] User notification shown on fallback
- [ ] Original meaning preserved in improvements
- [ ] Prompt produces clean output (no extra text)
- [ ] Multiple improvements work in sequence

### Performance

**llama3.2:3b:**

- Response time: 0.5-2 seconds
- Memory: ~2GB
- Quality: Good for most use cases

**Optimization:**

- Use `stream: false` for simpler parsing
- Set reasonable timeout (10s)
- Keep prompt concise
- Fallback gracefully on errors

### Notes

- Ollama must be running before app starts
- Model downloads automatically on first use
- Fallback ensures app never crashes
- System prompt is critical for quality
- Test with various transcription errors
