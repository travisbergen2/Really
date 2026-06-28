from __future__ import annotations

import re
from typing import Any

_AMBIGUITY_MARKERS = (
    "maybe",
    "might",
    "probably",
    "i think",
    "i guess",
    "not sure",
    "kind of",
    "sort of",
    "roughly",
    "around",
    "approximately",
)


def _clean_whitespace(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = [re.sub(r"\s+", " ", line).strip() for line in text.split("\n")]
    return "\n".join(line for line in lines if line)


def _split_fragments(text: str) -> list[str]:
    candidates = re.split(r"[\n;]+", text)
    fragments: list[str] = []
    for candidate in candidates:
        candidate = candidate.strip()
        if not candidate:
            continue
        if len(candidate) > 120 and " also " in candidate.lower():
            fragments.extend(part.strip() for part in re.split(r"\balso\b", candidate, flags=re.I) if part.strip())
        else:
            fragments.append(candidate)
    return fragments


def split_intents(message: str, context: str | None = None) -> dict[str, Any]:
    cleaned = _clean_whitespace(message)
    fragments = _split_fragments(cleaned)
    if not fragments:
        fragments = [cleaned]

    intents = []
    for idx, fragment in enumerate(fragments, start=1):
        priority = "medium"
        lowered = fragment.lower()
        if any(word in lowered for word in ("must", "urgent", "priority", "top", "first")):
            priority = "high"
        elif any(word in lowered for word in ("later", "maybe", "optional")):
            priority = "low"

        intents.append(
            {
                "id": f"intent_{idx}",
                "summary": fragment,
                "priority": priority,
                "confidence": 0.78 if len(fragment) > 18 else 0.58,
            }
        )

    return {"intents": intents, "context_used": bool(context)}


def normalize_human_input(text: str, preserve_tone: bool = True, preserve_uncertainty: bool = True) -> dict[str, Any]:
    cleaned = _clean_whitespace(text)
    fragments = _split_fragments(cleaned)
    clean_prompt = "\n".join(f"- {fragment}" for fragment in fragments)

    assumptions: list[str] = []
    clarifying_questions: list[str] = []

    if not fragments:
        assumptions.append("Input may be incomplete or empty.")
        clarifying_questions.append("What would you like me to help with?")

    lowered = cleaned.lower()
    if any(marker in lowered for marker in _AMBIGUITY_MARKERS):
        assumptions.append("User is expressing uncertainty or approximation.")
        clarifying_questions.append("Should I preserve the uncertainty or turn it into a concrete request?")

    if preserve_tone:
        assumptions.append("Preserve the user's original tone where possible.")
    if preserve_uncertainty:
        assumptions.append("Do not overstate confidence when the user used hedging language.")

    return {
        "clean_prompt": clean_prompt.strip(),
        "assumptions": assumptions,
        "clarifying_questions": clarifying_questions,
    }


def interpret_message(
    message: str,
    context: str | None = None,
    target_audience: str = "plain",
    allow_inference: bool = True,
) -> dict[str, Any]:
    normalized = normalize_human_input(message)
    fragments = normalized["clean_prompt"].split("\n") if normalized["clean_prompt"] else []
    first_fragment = fragments[0][2:] if fragments and fragments[0].startswith("- ") else (fragments[0] if fragments else "")
    lowered = message.lower()

    if "on principle" in lowered or "principle" in lowered:
        implied_meaning = "The user is making a value-based or normative request, not a purely procedural one."
    elif any(word in lowered for word in ("build", "create", "make", "develop")):
        implied_meaning = "The user wants a concrete build or implementation plan."
    elif any(word in lowered for word in ("fix", "repair", "debug", "resolve")):
        implied_meaning = "The user wants a correction or repair rather than a new concept."
    elif "translate" in lowered or "translation layer" in lowered:
        implied_meaning = "The user wants a communication bridge that preserves meaning while changing register."
    else:
        implied_meaning = "The user likely wants a useful action-oriented response, but the exact task should be inferred carefully."

    ambiguities = []
    if any(marker in lowered for marker in _AMBIGUITY_MARKERS):
        ambiguities.append("Hedged or uncertain language present.")
    if "..." in message or len(fragments) > 1:
        ambiguities.append("Fragmented or multi-thought input detected.")
    if "principle" in lowered:
        ambiguities.append("Normative intent may be present beyond literal wording.")

    if not allow_inference:
        suggested_next_step = "Ask one clarifying question before acting."
        confidence = 0.45
    else:
        suggested_next_step = "Proceed with the inferred meaning, then surface uncertainties if needed."
        confidence = 0.84 if not ambiguities else 0.68

    literal_summary = first_fragment or _clean_whitespace(message)
    if target_audience == "technical":
        literal_summary = literal_summary
    elif target_audience == "social":
        literal_summary = literal_summary.replace("must", "would prefer")
    elif target_audience == "concise":
        literal_summary = literal_summary[:120]

    return {
        "literal_summary": literal_summary,
        "implied_meaning": implied_meaning,
        "ambiguities": ambiguities,
        "confidence": round(confidence, 2),
        "suggested_next_step": suggested_next_step,
        "clean_prompt": normalized["clean_prompt"],
        "assumptions": normalized["assumptions"],
        "clarifying_questions": normalized["clarifying_questions"],
    }
