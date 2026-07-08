from langchain_core.messages import SystemMessage

from app.state import ClassificationIntent, State, get_llm


def classify_intent(state: State) -> dict[str, str]:
    last_message = state["messages"][-1]
    structured_llm = get_llm().with_structured_output(ClassificationIntent)
    result = structured_llm.invoke(
        [
            SystemMessage(
                content=(
                    "Classify the user's message. Use 'research' when the user "
                    "asks for facts, investigation, comparison, or source-backed "
                    "information. Use 'help' for general conversation, coding "
                    "help, drafting, or task assistance."
                )
            ),
            last_message,
        ]
    )
    return {"intent": result.intent}
