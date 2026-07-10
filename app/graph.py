from langgraph.checkpoint import memory
from langgraph.graph import END, START, StateGraph

from app.state import State
from agents.researcher_agent import researcher
from agents.helper_agent import helper
from app.classifier_intent import classify_intent
from app.router import route_by_intent
from app.tools import tool_node, tool_router
from langgraph.checkpoint.memory import MemorySaver


graph_builder = StateGraph(State)
graph_builder.add_node("classify_intent", classify_intent)
graph_builder.add_node("router", route_by_intent)
graph_builder.add_node("helper", helper)
graph_builder.add_node("researcher", researcher)
graph_builder.add_node("tool_node", tool_node)


graph_builder.add_edge(START, "classify_intent")
graph_builder.add_edge("classify_intent", "router")
graph_builder.add_conditional_edges("router",
    lambda state: state.get("route", "help"),
    {
        "help": "helper",
        "research": "researcher"
    }
)
graph_builder.add_conditional_edges( #this is made , if resercher response is needed tool or not
    "researcher",
    tool_router,
    ["tool_node", END]
)
graph_builder.add_edge("helper", END)

graph_builder.add_edge("tool_node", "researcher")
memory = MemorySaver()


graph = graph_builder.compile(checkpointer=memory)


try:
    png_bytes = graph.get_graph().draw_mermaid_png()
    
    with open("graph_visual.png", "wb") as f:
        f.write(png_bytes)
        
except Exception as e:
    print(graph.get_graph().draw_ascii())
    