PERSONA_SCHEMA = {
    "type": "object",
    "required": ["name", "vector"],
    "properties": {
        "name": {"type": "string"},
        "vector": {"type": "array", "items": {"type": "number"}},
        "description": {"type": "string"}
    }
}
