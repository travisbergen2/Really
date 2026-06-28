from __future__ import annotations

import argparse
import json
from typing import Any

from .manifest import build_manifest
from .mcp_transport import serve_stdio
from .registry import TOOL_CALLS


def dispatch_tool(tool_name: str, **kwargs: Any) -> dict[str, Any]:
    if tool_name not in TOOL_CALLS:
        raise KeyError(f"Unknown tool: {tool_name}")
    return TOOL_CALLS[tool_name](**kwargs)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Translator Hub manifest and tool demo.")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("manifest", help="Print the MCP manifest as JSON.")
    sub.add_parser("serve", help="Run the Translator Hub MCP stdio server.")

    p_interpret = sub.add_parser("interpret", help="Interpret a user message.")
    p_interpret.add_argument("message")
    p_interpret.add_argument("--context", default=None)
    p_interpret.add_argument("--target-audience", default="plain")
    p_interpret.add_argument("--no-inference", action="store_true")

    p_normalize = sub.add_parser("normalize", help="Normalize compressed human input.")
    p_normalize.add_argument("text")

    p_rewrite = sub.add_parser("rewrite", help="Rewrite text for an audience.")
    p_rewrite.add_argument("text")
    p_rewrite.add_argument("--style", default="plain")

    p_split = sub.add_parser("split", help="Split mixed thoughts into intents.")
    p_split.add_argument("message")
    p_split.add_argument("--context", default=None)

    p_route = sub.add_parser("route", help="Route a task to the best model family.")
    p_route.add_argument("task_type")
    p_route.add_argument("--objective", default=None)
    p_route.add_argument("--target-audience", default="plain")
    p_route.add_argument("--latency-priority", default="balanced")
    p_route.add_argument("--cost-priority", default="balanced")
    p_route.add_argument("--allow-multi-model", action="store_true")

    p_memory = sub.add_parser("memory", help="Create or inspect local translation memory.")
    memory_sub = p_memory.add_subparsers(dest="memory_command", required=True)
    p_memory_add = memory_sub.add_parser("add", help="Add a memory entry.")
    p_memory_add.add_argument("content")
    p_memory_add.add_argument("--source", default="user")
    p_memory_add.add_argument("--tag", action="append", default=[])
    p_memory_add.add_argument("--importance", default="normal")
    p_memory_add.add_argument("--persona-pack-id", default=None)
    p_memory_add.add_argument("--visibility", default="private")
    p_memory_list = memory_sub.add_parser("list", help="List memory entries.")
    p_memory_list.add_argument("--limit", type=int, default=20)
    p_memory_search = memory_sub.add_parser("search", help="Search memory entries.")
    p_memory_search.add_argument("query")
    p_memory_search.add_argument("--limit", type=int, default=10)

    p_persona = sub.add_parser("persona", help="Create or inspect persona packs.")
    persona_sub = p_persona.add_subparsers(dest="persona_command", required=True)
    p_persona_add = persona_sub.add_parser("create", help="Create a persona pack.")
    p_persona_add.add_argument("creator_id")
    p_persona_add.add_argument("creator_username")
    p_persona_add.add_argument("name")
    p_persona_add.add_argument("description")
    p_persona_add.add_argument("style_profile")
    p_persona_add.add_argument("prompt_template")
    p_persona_add.add_argument("--memory-rule", action="append", default=[])
    p_persona_add.add_argument("--tag", action="append", default=[])
    p_persona_add.add_argument("--version", default="0.1.0")
    p_persona_list = persona_sub.add_parser("list", help="List persona packs.")
    p_persona_list.add_argument("--limit", type=int, default=20)
    p_persona_validate = persona_sub.add_parser("validate", help="Validate a persona pack.")
    p_persona_validate.add_argument("--pack-id", default=None)
    p_persona_validate.add_argument("--pack-json", default=None)

    args = parser.parse_args(argv)

    if args.command == "manifest":
        print(json.dumps(build_manifest(), indent=2))
        return 0

    if args.command == "serve":
        serve_stdio()
        return 0

    if args.command == "interpret":
        result = dispatch_tool(
            "interpret_message",
            message=args.message,
            context=args.context,
            target_audience=args.target_audience,
            allow_inference=not args.no_inference,
        )
    elif args.command == "normalize":
        result = dispatch_tool("normalize_human_input", text=args.text)
    elif args.command == "rewrite":
        result = dispatch_tool("rewrite_for_audience", text=args.text, style=args.style)
    elif args.command == "split":
        result = dispatch_tool("split_intents", message=args.message, context=args.context)
    elif args.command == "route":
        result = dispatch_tool(
            "route_to_model",
            task_type=args.task_type,
            objective=args.objective,
            target_audience=args.target_audience,
            latency_priority=args.latency_priority,
            cost_priority=args.cost_priority,
            allow_multi_model=args.allow_multi_model,
        )
    elif args.command == "memory":
        if args.memory_command == "add":
            result = dispatch_tool(
                "create_memory_entry",
                content=args.content,
                source=args.source,
                tags=args.tag,
                importance=args.importance,
                persona_pack_id=args.persona_pack_id,
                visibility=args.visibility,
            )
        elif args.memory_command == "list":
            result = dispatch_tool("list_memory_entries", limit=args.limit)
        elif args.memory_command == "search":
            result = dispatch_tool("search_memory", query=args.query, limit=args.limit)
        else:
            raise AssertionError(f"Unhandled memory command: {args.memory_command}")
    elif args.command == "persona":
        if args.persona_command == "create":
            try:
                style_profile = json.loads(args.style_profile)
            except json.JSONDecodeError as exc:
                raise SystemExit(f"style_profile must be valid JSON: {exc}") from exc
            result = dispatch_tool(
                "create_persona_pack",
                creator_id=args.creator_id,
                creator_username=args.creator_username,
                name=args.name,
                description=args.description,
                style_profile=style_profile,
                prompt_template=args.prompt_template,
                memory_rules=args.memory_rule,
                tags=args.tag,
                version=args.version,
            )
        elif args.persona_command == "list":
            result = dispatch_tool("list_persona_packs", limit=args.limit)
        elif args.persona_command == "validate":
            pack = json.loads(args.pack_json) if args.pack_json else None
            result = dispatch_tool("validate_persona_pack", pack=pack, pack_id=args.pack_id)
        else:
            raise AssertionError(f"Unhandled persona command: {args.persona_command}")
    else:
        raise AssertionError(f"Unhandled command: {args.command}")

    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
