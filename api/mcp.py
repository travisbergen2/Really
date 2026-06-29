def handler(_request):
    # For now, just expose a simple MCP manifest
    manifest = {
        "name": "rpcs1-hub",
        "version": "0.1.0",
        "tools": ["interpret_message", "route_to_model"]
    }
    return manifest
