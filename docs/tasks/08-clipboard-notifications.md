# Task: Clipboard manager + notifications

## Status

ready

## Goal

Copy the final (improved) text to clipboard and optionally notify the user.

## Acceptance criteria

- `copy_to_clipboard(text)` copies text using `pyperclip`.
- Menu action "Copy Last Result" works and provides feedback if there is no result yet.
- If `privacy.clear_clipboard_after` is enabled:
  - clipboard is cleared after a configurable short delay (or immediate if specified)
  - behavior is documented in config defaults
- Notifications can be toggled with `menu.show_notifications`.

## Dependencies

- Task 03 (menu bar controller)
- Task 02 (config loading)

---

## Implementation Guide

### Pseudocode: `clipboard_manager.py`

```
class ClipboardManager:
    initialize(config):
        - show_notifications = config.get('menu.show_notifications', True)
        - clear_after = config.get('privacy.clear_clipboard_after', False)

    copy_to_clipboard(text) → bool:
        - try:
            * use pyperclip.copy(text)
            * if clear_after enabled:
                - schedule clear after delay
            * return True (success)
        - except Exception:
            * log error
            * return False (failure)

    notify_user(title, subtitle, message):
        - if show_notifications enabled:
            * use rumps.notification(title, subtitle, message)
        - else:
            * skip notification

    clear_clipboard():
        - pyperclip.copy('')
        - log "Clipboard cleared for privacy"
```

### Clipboard Flow

```
┌─────────────────────────────────────────────────────────┐
│              Clipboard & Notification Flow              │
└─────────────────────────────────────────────────────────┘

1. Text Ready
   │
   └─> Improved text from Ollama

2. Copy to Clipboard
   │
   ├─> Use pyperclip.copy(text)
   └─> Clipboard now contains improved text

3. Show Notification
   │
   ├─> Title: "✓ Copied to clipboard!"
   ├─> Subtitle: "Paste with Cmd+V"
   └─> Message: Preview of text (first 50 chars)

4. User Pastes
   │
   ├─> User switches to destination app
   ├─> User presses Cmd+V
   └─> Text appears at cursor

5. Privacy Cleanup (optional)
   │
   └─> Clear clipboard after delay (if enabled)
```

### Notification Types

**Success:**

```
Title: "✓ Copied to clipboard!"
Subtitle: "Paste with Cmd+V"
Message: "The quick brown fox jumps over the lazy..."
```

**Error:**

```
Title: "❌ Error"
Subtitle: "Processing failed"
Message: "Whisper model not loaded"
```

**Info:**

```
Title: "Speak-Type"
Subtitle: "Recording started"
Message: "Speak now. Click 'Stop Recording' when done."
```

**No Result:**

```
Title: "No result"
Subtitle: ""
Message: "No previous result to copy"
```

### Configuration

```yaml
menu:
  show_notifications: true # Show macOS notifications
  show_copy_last: true # Show "Copy Last Result" option

privacy:
  clear_clipboard_after: false # Clear clipboard after use
```

### Privacy Clipboard Clearing

```
if privacy.clear_clipboard_after enabled:
    1. Copy text to clipboard
    2. Wait for user to paste (or timeout)
    3. Clear clipboard
    4. Log "Clipboard cleared"

Note: This is optional and disabled by default
```

### macOS Notification Permissions

**Required:**

- System Preferences → Notifications
- Find "Python" or "Terminal"
- Enable "Allow Notifications"

**Notification Behavior:**

- Appears in top-right corner
- Shows for ~5 seconds
- Stored in Notification Center
- Can be clicked to focus app

### Integration with Menu Bar

```
In main.py:

_show_success(text):
    - clipboard.copy_to_clipboard(text)
    - clipboard.notify_user(
        title="✓ Copied to clipboard!",
        subtitle="Paste with Cmd+V",
        message=text[:50] + "..."
    )

_show_error(message):
    - clipboard.notify_user(
        title="❌ Error",
        subtitle="Processing failed",
        message=message
    )
```

### Testing Checklist

- [ ] Text copies to clipboard successfully
- [ ] Cmd+V pastes copied text
- [ ] Notifications appear when enabled
- [ ] Notifications hidden when disabled
- [ ] "Copy Last Result" works
- [ ] "Copy Last" shows error when no result
- [ ] Clipboard clears if privacy setting enabled
- [ ] Multiple copy operations work
- [ ] Special characters copy correctly

### Error Handling

**Clipboard Errors:**

- pyperclip not installed → Install dependency
- Clipboard access denied → Check permissions
- Copy fails → Return False, show error

**Notification Errors:**

- Notifications disabled → Silently skip
- Permission denied → Log warning, continue

### Notes

- Use `pyperclip` for cross-platform clipboard access
- Use `rumps.notification()` for macOS notifications
- Notifications are optional (configurable)
- Clipboard remains available after paste
- Privacy clearing is opt-in (disabled by default)
- Test with emoji and special characters
