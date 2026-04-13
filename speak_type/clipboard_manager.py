import pyperclip
from rumps import notification


class ClipboardManager:

    def __init__(self, config):
        self.config = config.config
        self.clipboard_config = config.get_clipboard_config()
        self.last_copied = None
        self.message_bell = False
        self.show_notifications = self.clipboard_config.get("show_notifications", False)
        self.notification_title = self.clipboard_config.get(
            "notification_title", "SpeakType"
        )

    def copy_to_clipboard(self, text):
        if text is None or not text.strip():
            print("Cannot copy empty or None text to clipboard")
            return False

        try:
            pyperclip.copy(text)
            self.last_copied = text

            if self.show_notifications:
                self.notify_success()

            return True

        except pyperclip.PyperclipException as e:
            print(f"Clipboard error: {e}")
        except Exception as e:
            print(f"Unexpected error copying to clipboard: {e}")
        finally:
            self.notify_error()
            return False

    def notify_user(self, title, message):
        if not self.show_notifications:
            return

        title = self.notification_title
        message = message

        try:
            notification(
                title=title,
                subtitle=message,
                message=message,
                sound=self.message_bell,
            )
        except Exception as e:
            print(f"🔔 {title}: {message}")
            print(f"Notification error: {e}")

    def notify_success(self, message="Text copied to clipboard!"):
        self.notify_user(self.notification_title, f"✅ {message}")

    def notify_error(self, message="Failed to copy to clipboard"):
        self.notify_user(self.notification_title, f"❌ {message}")

    def notify_info(self, message):
        try:
            notification(title=self.notification_title, message=message)
        except Exception as e:
            print(f"🔔 {self.notification_title}: {message}")
            print(f"Notification error: {e}")

    def clear_clipboard(self):
        try:
            pyperclip.copy("")
            return True
        except Exception as e:
            print(f"Error clearing clipboard: {e}")
            return False
