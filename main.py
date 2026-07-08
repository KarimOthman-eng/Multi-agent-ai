from app.graph import graph


def main() -> None:
    config = {"configurable": {"thread_id": "session_1"}}
    while True:
        user_input = input("User: ").strip()
        if user_input.lower() in {"exit", "quit"}:
            break
        if not user_input:
            continue

        response = graph.invoke(
        {"messages": [("user", user_input)]}, 
        config=config 
        )
        intent = response.get("intent", "unknown")
        print(f"Assistant ({intent}): {response['messages'][-1].content} ")


if __name__ == "__main__":
    main()
