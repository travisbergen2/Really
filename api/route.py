from translator_hub.router import route_to_model
from translator_hub.config import HubConfig

def handler(request):
    body = request.get_json()
    text = body.get("text", "")
    # Using the existing route_to_model function from the repo
    # Note: The existing function signature is different from the user's snippet
    # We'll adapt it or the caller.
    result = route_to_model(task_type="interpretation", objective=text)
    return {"model": result["primary_model"], "output": f"Routed to {result['primary_model']} for: {text}"}
