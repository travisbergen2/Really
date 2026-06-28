from __future__ import annotations

from typing import Any

from ..memory import create_persona_pack as _create_persona_pack
from ..memory import list_persona_packs as _list_persona_packs
from ..memory import validate_persona_pack as _validate_persona_pack


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
    return _create_persona_pack(
        creator_id=creator_id,
        creator_username=creator_username,
        name=name,
        description=description,
        style_profile=style_profile,
        prompt_template=prompt_template,
        memory_rules=memory_rules,
        tags=tags,
        version=version,
    )


def validate_persona_pack(pack: dict[str, Any] | None = None, pack_id: str | None = None) -> dict[str, Any]:
    return _validate_persona_pack(pack=pack, pack_id=pack_id)


def list_persona_packs(limit: int = 20) -> dict[str, Any]:
    return _list_persona_packs(limit=limit)

