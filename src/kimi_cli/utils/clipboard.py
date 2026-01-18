from __future__ import annotations

import pyperclip


def is_clipboard_available() -> bool:
    try:
        pyperclip.paste()
        return True
    except Exception:
        return False
