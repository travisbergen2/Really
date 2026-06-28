"""Tool schemas for the first Translator Hub tool set."""

TOOLS = {
    "interpret_message": {
        "description": "Convert raw user text into structured intent and likely meaning.",
        "input_schema": {
            "type": "object",
            "properties": {
                "message": {"type": "string"},
                "context": {"type": ["string", "null"]},
                "target_audience": {
                    "type": "string",
                    "enum": ["technical", "plain", "social", "concise", "detailed"],
                },
                "allow_inference": {"type": "boolean"},
            },
            "required": ["message"],
        },
    },
    "split_intents": {
        "description": "Split a mixed or fragmented message into discrete intents.",
        "input_schema": {
            "type": "object",
            "properties": {
                "message": {"type": "string"},
                "context": {"type": ["string", "null"]},
            },
            "required": ["message"],
        },
    },
    "normalize_human_input": {
        "description": "Clean and structure compressed human input without changing meaning.",
        "input_schema": {
            "type": "object",
            "properties": {
                "text": {"type": "string"},
                "preserve_tone": {"type": "boolean"},
                "preserve_uncertainty": {"type": "boolean"},
            },
            "required": ["text"],
        },
    },
    "rewrite_for_audience": {
        "description": "Rewrite text for a chosen audience or tone.",
        "input_schema": {
            "type": "object",
            "properties": {
                "text": {"type": "string"},
                "style": {
                    "type": "string",
                    "enum": [
                        "technical",
                        "plain",
                        "socially_gentle",
                        "concise",
                        "detailed",
                        "direct",
                    ],
                },
                "preserve_precision": {"type": "boolean"},
            },
            "required": ["text", "style"],
        },
    },
    "route_to_model": {
        "description": "Choose the most suitable model family for a task and audience.",
        "input_schema": {
            "type": "object",
            "properties": {
                "task_type": {"type": "string"},
                "objective": {"type": ["string", "null"]},
                "target_audience": {"type": "string"},
                "latency_priority": {"type": "string", "enum": ["low", "balanced", "high"]},
                "cost_priority": {"type": "string", "enum": ["low", "balanced", "high"]},
                "allow_multi_model": {"type": "boolean"},
            },
            "required": ["task_type"],
        },
    },
    "create_memory_entry": {
        "description": "Store an observation or user preference in the translation memory layer.",
        "input_schema": {
            "type": "object",
            "properties": {
                "content": {"type": "string"},
                "source": {"type": "string"},
                "tags": {"type": "array", "items": {"type": "string"}},
                "importance": {"type": "string"},
                "persona_pack_id": {"type": ["string", "null"]},
                "visibility": {"type": "string"},
            },
            "required": ["content"],
        },
    },
    "search_memory": {
        "description": "Search the local translation memory for matching observations.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string"},
                "limit": {"type": "integer"},
            },
            "required": ["query"],
        },
    },
    "list_memory_entries": {
        "description": "List recent memory entries.",
        "input_schema": {
            "type": "object",
            "properties": {
                "limit": {"type": "integer"},
            },
        },
    },
    "create_persona_pack": {
        "description": "Create and sign a persona pack for marketplace-style reuse.",
        "input_schema": {
            "type": "object",
            "properties": {
                "creator_id": {"type": "string"},
                "creator_username": {"type": "string"},
                "name": {"type": "string"},
                "description": {"type": "string"},
                "style_profile": {"type": "object"},
                "prompt_template": {"type": "string"},
                "memory_rules": {"type": "array", "items": {"type": "string"}},
                "tags": {"type": "array", "items": {"type": "string"}},
                "version": {"type": "string"},
            },
            "required": [
                "creator_id",
                "creator_username",
                "name",
                "description",
                "style_profile",
                "prompt_template",
            ],
        },
    },
    "list_persona_packs": {
        "description": "List persona packs stored in the local registry.",
        "input_schema": {
            "type": "object",
            "properties": {
                "limit": {"type": "integer"},
            },
        },
    },
    "validate_persona_pack": {
        "description": "Validate a persona pack signature before use.",
        "input_schema": {
            "type": "object",
            "properties": {
                "pack": {"type": ["object", "null"]},
                "pack_id": {"type": ["string", "null"]},
            },
        },
    },
}
