from __future__ import annotations

from typing import Any

from ..memory import create_memory_entry as _create_memory_entry
from ..memory import list_memory_entries as _list_memory_entries
from ..memory import search_memory as _search_memory


def create_memory_entry(
    content: str,
    source: str = "user",
    tags: list[str] | None = None,
    importance: str = "normal",
    persona_pack_id: str | None = None,
    visibility: str = "private",
) -> dict[str, Any]:
    return _create_memory_entry(
        content=content,
        source=source,
        tags=tags,
        importance=importance,
        persona_pack_id=persona_pack_id,
        visibility=visibility,
    )


def list_memory_entries(limit: int = 20) -> dict[str, Any]:
    return _list_memory_entries(limit=limit)


def search_memory(query: str, limit: int = 10) -> dict[str, Any]:
    return _search_memory(query=query, limit=limit)

