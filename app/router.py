from app.state import State


def route_by_intent(state: State) -> dict[str, str]:
    intent = state.get("intent", "help")
    if intent == "research":
        return {"route": "research"}
    return {"route": "help"}
