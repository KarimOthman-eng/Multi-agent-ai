from langchain_core.messages import AnyMessage

from app.state import State, get_llm


def helper(state: State) -> dict[str, list[AnyMessage]]:
    response = get_llm().invoke(state["messages"])
    return {"messages": [response]}
