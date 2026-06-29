from translator_hub.memory import PersonaStore

def handler(request):
    body = request.get_json()
    action = body.get("action", "list")
    store = PersonaStore()

    if action == "create":
        # Adapting to existing PersonaStore if it exists, or user's snippet
        persona = {
            "name": body["name"],
            "vector": body["vector"],
            "description": body.get("description", "")
        }
        store.create_persona_pack(persona)
        return {"status": "ok"}
    else:
        return {"personas": store.list_persona_packs()}
