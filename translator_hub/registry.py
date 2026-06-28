from __future__ import annotations

from .tools.interpret import interpret_message, normalize_human_input, split_intents
from .tools.memory import create_memory_entry, list_memory_entries, search_memory
from .tools.persona import create_persona_pack, list_persona_packs, validate_persona_pack
from .tools.rewrite import rewrite_for_audience
from .tools.routing import route_to_model

TOOL_CALLS = {
    "interpret_message": interpret_message,
    "split_intents": split_intents,
    "normalize_human_input": normalize_human_input,
    "rewrite_for_audience": rewrite_for_audience,
    "route_to_model": route_to_model,
    "create_memory_entry": create_memory_entry,
    "search_memory": search_memory,
    "list_memory_entries": list_memory_entries,
    "create_persona_pack": create_persona_pack,
    "list_persona_packs": list_persona_packs,
    "validate_persona_pack": validate_persona_pack,
}
