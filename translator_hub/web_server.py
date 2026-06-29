from __future__ import annotations

import json
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from .manifest import build_manifest
from .registry import TOOL_CALLS


WEB_ROOT = Path(__file__).resolve().parent / "web"


def _read_json(handler: BaseHTTPRequestHandler) -> dict[str, Any]:
    content_length = int(handler.headers.get("Content-Length", "0"))
    if content_length <= 0:
        return {}
    raw = handler.rfile.read(content_length)
    if not raw:
        return {}
    return json.loads(raw.decode("utf-8"))


def _send_json(handler: BaseHTTPRequestHandler, payload: dict[str, Any], status: int = HTTPStatus.OK) -> None:
    raw = json.dumps(payload, indent=2, ensure_ascii=False).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Content-Length", str(len(raw)))
    handler.send_header("Cache-Control", "no-store")
    handler.end_headers()
    handler.wfile.write(raw)


def _send_html(handler: BaseHTTPRequestHandler, html: str) -> None:
    raw = html.encode("utf-8")
    handler.send_response(HTTPStatus.OK)
    handler.send_header("Content-Type", "text/html; charset=utf-8")
    handler.send_header("Content-Length", str(len(raw)))
    handler.send_header("Cache-Control", "no-store")
    handler.end_headers()
    handler.wfile.write(raw)


def _send_not_found(handler: BaseHTTPRequestHandler) -> None:
    payload = {"error": "Not found"}
    _send_json(handler, payload, status=HTTPStatus.NOT_FOUND)


class TranslatorHubHandler(BaseHTTPRequestHandler):
    server_version = "TranslatorHubHTTP/0.1"

    def log_message(self, format: str, *args: Any) -> None:  # noqa: A003
        return

    def do_GET(self) -> None:  # noqa: N802
        path = urlparse(self.path).path
        if path in {"/", "/index.html"}:
            _send_html(self, (WEB_ROOT / "index.html").read_text(encoding="utf-8"))
            return
        if path == "/api/health":
            _send_json(self, {"ok": True, "service": "translator-hub"})
            return
        if path == "/api/manifest":
            _send_json(self, build_manifest())
            return
        if path == "/api/examples":
            _send_json(
                self,
                {
                    "examples": [
                        "I don’t understand this.",
                        "Your builder went to the top of the list on principle.",
                        "I need this translated before it causes a misunderstanding.",
                    ]
                },
            )
            return
        _send_not_found(self)

    def do_POST(self) -> None:  # noqa: N802
        path = urlparse(self.path).path
        try:
            data = _read_json(self)
        except json.JSONDecodeError:
            _send_json(self, {"error": "Invalid JSON body."}, status=HTTPStatus.BAD_REQUEST)
            return

        route_map = {
            "/api/interpret": "interpret_message",
            "/api/normalize": "normalize_human_input",
            "/api/rewrite": "rewrite_for_audience",
            "/api/route": "route_to_model",
            "/api/split": "split_intents",
        }
        if path not in route_map:
            _send_not_found(self)
            return

        tool_name = route_map[path]
        try:
            result = TOOL_CALLS[tool_name](**data)
        except TypeError as exc:
            _send_json(self, {"error": f"Bad request: {exc}"}, status=HTTPStatus.BAD_REQUEST)
            return
        _send_json(self, result)


def serve_web(host: str = "127.0.0.1", port: int = 8787) -> ThreadingHTTPServer:
    server = ThreadingHTTPServer((host, port), TranslatorHubHandler)
    return server

