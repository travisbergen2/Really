"""Prompt templates for Translator Hub."""

PROMPTS = {
    "translate_to_plain_english": {
        "description": "Rewrite dense or technical language into clear plain English without losing meaning.",
        "arguments": ["text"],
        "template": "Rewrite the following into plain English while preserving meaning:\n\n{text}",
    },
    "translate_to_technical": {
        "description": "Rewrite content in a more technical register while preserving intent.",
        "arguments": ["text"],
        "template": "Rewrite the following in a technical register while preserving meaning:\n\n{text}",
    },
    "route_and_rewrite": {
        "description": "Interpret a messy message, route it to a suitable model, and rewrite it for the target audience.",
        "arguments": ["text", "target_audience", "task_type"],
        "template": "Interpret, route, and rewrite this message:\n\n{text}",
    },
}
