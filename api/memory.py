from translator_hub.memory import MemoryStore

def handler(request):
    body = request.get_json()
    action = body.get("action", "list")
    store = MemoryStore()

    if action == "add":
        entry = body["entry"]
        store.add_entry(entry)
        return {"status": "ok"}
    elif action == "search":
        query = body["query"]
        return {"results": store.search_memory(query)}
    else:
        return {"entries": store.list_memory_entries()}
