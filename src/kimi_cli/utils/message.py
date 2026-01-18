from __future__ import annotations

from kosong.message import Message, TextPart


def message_stringify(message: Message) -> str:
    parts: list[str] = []
    for part in message.content:
        if isinstance(part, TextPart):
            parts.append(part.text)
        else:
            parts.append(f"[{part.type}]")
    return "".join(parts)
