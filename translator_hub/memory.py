from __future__ import annotations

import hashlib
import hmac
import json
import os
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DATA_DIR = Path(os.getenv("TRANSLATOR_HUB_DATA_DIR", ".translator_hub"))
MEMORY_FILE = Path(os.getenv("TRANSLATOR_HUB_MEMORY_FILE", DATA_DIR / "memory.json"))
PERSONA_FILE = Path(os.getenv("TRANSLATOR_HUB_PERSONA_FILE", DATA_DIR / "persona_packs.json"))


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def _load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return default


def _save_json(path: Path, payload: Any) -> None:
    _ensure_parent(path)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def _canonical_json(payload: dict[str, Any]) -> bytes:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def _sign_payload(payload: dict[str, Any], secret: str | None = None) -> str:
    signing_secret = secret or os.getenv("TRANSLATOR_HUB_SIGNING_SECRET", "translator-hub-dev-secret")
    return hmac.new(signing_secret.encode("utf-8"), _canonical_json(payload), hashlib.sha256).hexdigest()


def _memory_state() -> dict[str, list[dict[str, Any]]]:
    state = _load_json(MEMORY_FILE, {"entries": []})
    if "entries" not in state or not isinstance(state["entries"], list):
        state["entries"] = []
    return state


def _persona_state() -> dict[str, list[dict[str, Any]]]:
    state = _load_json(PERSONA_FILE, {"packs": []})
    if "packs" not in state or not isinstance(state["packs"], list):
        state["packs"] = []
    return state


def create_memory_entry(
    content: str,
    source: str = "user",
    tags: list[str] | None = None,
    importance: str = "normal",
    persona_pack_id: str | None = None,
    visibility: str = "private",
) -> dict[str, Any]:
    entry = {
        "memory_id": f"mem_{hashlib.sha1(f'{_utc_now()}:{content}'.encode('utf-8')).hexdigest()[:12]}",
        "content": content.strip(),
        "source": source,
        "tags": tags or [],
        "importance": importance,
        "persona_pack_id": persona_pack_id,
        "visibility": visibility,
        "created_at": _utc_now(),
    }
    state = _memory_state()
    state["entries"].append(entry)
    _save_json(MEMORY_FILE, state)
    return {"memory": entry}


def list_memory_entries(limit: int = 20) -> dict[str, Any]:
    entries = _memory_state()["entries"][-max(limit, 0) :]
    return {"entries": entries, "count": len(entries)}


def search_memory(query: str, limit: int = 10) -> dict[str, Any]:
    needle = query.strip().lower()
    scored: list[tuple[int, dict[str, Any]]] = []
    for entry in _memory_state()["entries"]:
        haystack = " ".join(
            [entry.get("content", ""), " ".join(entry.get("tags", [])), entry.get("source", "")]
        ).lower()
        score = haystack.count(needle) if needle else 0
        if needle and needle in haystack:
            scored.append((score, entry))
    scored.sort(key=lambda item: (-item[0], item[1].get("created_at", "")))
    results = [entry for _, entry in scored[: max(limit, 0)]]
    return {"query": query, "results": results, "count": len(results)}


def create_persona_pack(
    creator_id: str,
    creator_username: str,
    name: str,
    description: str,
    style_profile: dict[str, Any],
    prompt_template: str,
    memory_rules: list[str] | None = None,
    tags: list[str] | None = None,
    version: str = "0.1.0",
) -> dict[str, Any]:
    pack = {
        "pack_id": f"persona_{hashlib.sha1(f'{_utc_now()}:{creator_id}:{name}'.encode('utf-8')).hexdigest()[:12]}",
        "creator_id": creator_id.strip(),
        "creator_username": creator_username.strip(),
        "name": name.strip(),
        "description": description.strip(),
        "version": version,
        "style_profile": style_profile,
        "prompt_template": prompt_template,
        "memory_rules": memory_rules or [],
        "tags": tags or [],
        "created_at": _utc_now(),
    }
    signature = _sign_payload(pack)
    pack["signature"] = signature
    state = _persona_state()
    state["packs"].append(pack)
    _save_json(PERSONA_FILE, state)
    return {"persona_pack": pack, "integrity": {"valid": True, "reason": "Signed at creation."}}


def validate_persona_pack(pack: dict[str, Any] | None = None, pack_id: str | None = None) -> dict[str, Any]:
    candidate = pack
    if candidate is None and pack_id is not None:
        for stored in _persona_state()["packs"]:
            if stored.get("pack_id") == pack_id:
                candidate = stored
                break
    if not candidate:
        return {"valid": False, "reason": "Persona pack not found."}

    signature = candidate.get("signature")
    if not signature:
        return {"valid": False, "reason": "Missing signature."}

    payload = dict(candidate)
    payload.pop("signature", None)
    expected = _sign_payload(payload)
    if not hmac.compare_digest(signature, expected):
        return {"valid": False, "reason": "Signature mismatch or manifest was modified."}

    return {"valid": True, "reason": "Signature verified.", "pack_id": candidate.get("pack_id")}


def list_persona_packs(limit: int = 20) -> dict[str, Any]:
    packs = _persona_state()["packs"][-max(limit, 0) :]
    return {"packs": packs, "count": len(packs)}

