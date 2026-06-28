from __future__ import annotations

import json
import sys
from typing import Any

from .manifest import build_manifest
from .registry import TOOL_CALLS
from .schema.prompts import PROMPTS
from .schema.resources import RESOURCES
from .schema.tools import TOOLS


def _json_response(message_id: Any, result: Any) -> dict[str, Any]:
    return {"jsonrpc": "2.0", "id": message_id, "result": result}


def _json_error(message_id: Any, code: int, message: str, data: Any | None = None) -> dict[str, Any]:
    payload: dict[str, Any] = {"code": code, "message": message}
    if data is not None:
        payload["data"] = data
    return {"jsonrpc": "2.0", "id": message_id, "error": payload}


def _tool_list() -> list[dict[str, Any]]:
    tools: list[dict[str, Any]] = []
    for name, schema in TOOLS.items():
        tools.append(
            {
                "name": name,
                "description": schema["description"],
                "inputSchema": schema["input_schema"],
            }
        )
    return tools


def _prompt_list() -> list[dict[str, Any]]:
    prompts: list[dict[str, Any]] = []
    for name, schema in PROMPTS.items():
        prompts.append(
            {
                "name": name,
                "description": schema["description"],
                "arguments": [{"name": argument, "required": True} for argument in schema["arguments"]],
            }
        )
    return prompts


def _resource_list() -> list[dict[str, Any]]:
    resources: list[dict[str, Any]] = []
    for resource in RESOURCES:
        resources.append(resource)
    return resources


def _resource_read(uri: str) -> dict[str, Any]:
    for resource in RESOURCES:
        if resource["uri"] == uri:
            return {
                "contents": [
                    {
                        "uri": uri,
                        "mimeType": resource.get("mimeType", "text/plain"),
                        "text": resource.get("text", resource.get("description", "")),
                    }
                ]
            }
    raise KeyError(uri)


def _prompt_get(name: str, arguments: dict[str, Any] | None) -> dict[str, Any]:
    if name not in PROMPTS:
        raise KeyError(name)
    prompt = PROMPTS[name]
    rendered = {
        "name": name,
        "description": prompt["description"],
        "messages": [
            {
                "role": "user",
                "content": {
                    "type": "text",
                    "text": f"{prompt['description']}\nArguments: {json.dumps(arguments or {}, indent=2, ensure_ascii=False)}",
                },
            }
        ],
    }
    return rendered


def handle_request(request: dict[str, Any]) -> dict[str, Any] | None:
    method = request.get("method")
    message_id = request.get("id")
    params = request.get("params") or {}

    if method == "initialize":
        return _json_response(
            message_id,
            {
                "protocolVersion": "2025-06-18",
                "serverInfo": {"name": "translator-hub", "version": "0.1.0"},
                "capabilities": {
                    "tools": {"listChanged": False},
                    "resources": {"listChanged": False, "subscribe": False},
                    "prompts": {"listChanged": False},
                },
            },
        )

    if method == "notifications/initialized":
        return None

    if method == "tools/list":
        return _json_response(message_id, {"tools": _tool_list()})

    if method == "tools/call":
        name = params.get("name")
        arguments = params.get("arguments") or {}
        if name not in TOOL_CALLS:
            return _json_error(message_id, -32601, f"Unknown tool: {name}")
        result = TOOL_CALLS[name](**arguments)
        return _json_response(
            message_id,
            {
                "content": [
                    {
                        "type": "text",
                        "text": json.dumps(result, indent=2, ensure_ascii=False),
                    }
                ],
                "isError": False,
            },
        )

    if method == "prompts/list":
        return _json_response(message_id, {"prompts": _prompt_list()})

    if method == "prompts/get":
        try:
            return _json_response(message_id, _prompt_get(params.get("name"), params.get("arguments")))
        except KeyError as exc:
            return _json_error(message_id, -32602, f"Unknown prompt: {exc.args[0]}")

    if method == "resources/list":
        return _json_response(message_id, {"resources": _resource_list()})

    if method == "resources/read":
        try:
            return _json_response(message_id, _resource_read(params.get("uri")))
        except KeyError as exc:
            return _json_error(message_id, -32602, f"Unknown resource: {exc.args[0]}")

    if method == "ping":
        return _json_response(message_id, {})

    return _json_error(message_id, -32601, f"Unhandled method: {method}")


def _read_message(stream) -> dict[str, Any] | None:
    headers: dict[str, str] = {}
    while True:
        line = stream.readline()
        if not line:
            return None
        line_text = line.decode("utf-8").strip()
        if not line_text:
            break
        if ":" in line_text:
            key, value = line_text.split(":", 1)
            headers[key.lower().strip()] = value.strip()
    length = int(headers.get("content-length", "0"))
    if length <= 0:
        return None
    payload = stream.read(length)
    while len(payload) < length:
        chunk = stream.read(length - len(payload))
        if not chunk:
            break
        payload += chunk
    return json.loads(payload.decode("utf-8"))


def _write_message(stream, payload: dict[str, Any]) -> None:
    raw = json.dumps(payload, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    stream.write(f"Content-Length: {len(raw)}\r\n\r\n".encode("utf-8"))
    stream.write(raw)
    stream.flush()


def serve_stdio() -> None:
    stdin = sys.stdin.buffer
    stdout = sys.stdout.buffer
    while True:
        request = _read_message(stdin)
        if request is None:
            break
        response = handle_request(request)
        if response is not None and request.get("id") is not None:
            _write_message(stdout, response)
