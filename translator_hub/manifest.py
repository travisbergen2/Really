from __future__ import annotations

from typing import Any

from .schema.prompts import PROMPTS
from .schema.resources import RESOURCES
from .schema.tools import TOOLS


def build_manifest() -> dict[str, Any]:
    return {
        "name": "translator-hub",
        "version": "0.1.0",
        "description": "AI-human translation layer with routing, memory, and persona pack support.",
        "tools": TOOLS,
        "prompts": PROMPTS,
        "resources": RESOURCES,
    }
