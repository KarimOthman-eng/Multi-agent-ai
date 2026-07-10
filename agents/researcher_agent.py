from langchain_core.messages import AnyMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from app.state import State
from app.tools import get_llm_with_tools


xml_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are an expert research assistant. If the user asks for up-to-date information or news, "
        "you MUST call the search tool by outputting exactly this XML format:\n"
        "<call_tool name=\"search_web\">YOUR_QUERY_HERE</call_tool>\n"
        "Do not output anything else when you call the tool. If you don't need to search, just answer normally."
    ),
    MessagesPlaceholder(variable_name="messages"),
])

researcher_chain = xml_prompt | get_llm_with_tools()

def researcher(state: State):
    response = researcher_chain.invoke({"messages": state["messages"]})
    return {"messages": [response]}