from __future__ import annotations

from typing import Any


def rewrite_for_audience(text: str, style: str = "plain", preserve_precision: bool = True) -> dict[str, Any]:
    stripped = " ".join(text.strip().split())
    if not stripped:
        return {"rewritten_text": "", "tone_notes": ["Empty input received."]}

    if style == "technical":
        rewritten = stripped
        notes = ["Technical register preserved."]
    elif style == "plain":
        rewritten = stripped
        notes = ["Plain-language mode selected."]
    elif style == "socially_gentle":
        rewritten = f"I may be missing something, but {stripped[0].lower() + stripped[1:] if len(stripped) > 1 else stripped}"
        notes = ["Softened to reduce social friction."]
    elif style == "concise":
        rewritten = stripped.split(". ")[0].strip()
        notes = ["Condensed to the shortest useful form."]
    elif style == "detailed":
        rewritten = f"{stripped}\n\nDetails: preserve the key meaning, edge cases, and assumptions."
        notes = ["Expanded for completeness."]
    elif style == "direct":
        rewritten = stripped
        notes = ["Direct mode selected."]
    else:
        rewritten = stripped
        notes = [f"Unknown style '{style}' received; returned original text."]

    if not preserve_precision and style in {"plain", "socially_gentle"}:
        notes.append("Precision may be slightly reduced for readability.")

    return {"rewritten_text": rewritten, "tone_notes": notes}
