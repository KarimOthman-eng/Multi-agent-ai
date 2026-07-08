import json
from functools import lru_cache
from typing import Literal
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage 
from langchain_community.tools import DuckDuckGoSearchResults
from langgraph.graph import END
import re
from app.state import State, get_llm

search_engine = DuckDuckGoSearchResults(num_results=5, output_format="json")

@tool
def search_web(query: str) -> str:
    """Search the web for recent or source-backed information. Pass a concise search query."""
    clean_query = query.strip()
    if not clean_query:
        return "No search query provided."
    return search_engine.invoke(clean_query)

import chromadb
from langchain_core.tools import tool

client = chromadb.PersistentClient(path="./agent_memory")
collection = client.get_or_create_collection(name="my_knowledge_base")

@tool
def search_agent_memory(query: str) -> str:
    """
    Use this tool to search the agent's long-term memory or vector database 
    whenever the user asks about past files, contracts, user preferences, 
    or historical data that is not in the immediate chat history.
    """
    results = collection.query(
        query_texts=[query],
        n_results=1  
    )
    
    if results and results['documents'] and results['documents'][0]:
        return f"Found this relevant context in memory: {results['documents'][0][0]}"
    
    return "No relevant information found in memory."

tools = [search_web, search_agent_memory]
tools_by_name = {tool.name: tool for tool in tools}

@lru_cache(maxsize=1)
def get_llm_with_tools():
    return get_llm().bind_tools(tools)


def tool_node(state: dict):
    last_message = state["messages"][-1]
    content = str(last_message.content) 
    
    match = re.search(r'<call_tool name=".*?">(.*?)</call_tool>', content, re.DOTALL)
    
    result = []
    if match:
        query = match.group(1).strip()

        try:
            observation = search_web.invoke({"query": query}) 
        except Exception as e:
            observation = f"Search Error: {str(e)}"
        result.append(HumanMessage(content=f"Search Results:\n{observation}"))
        
    return {"messages": result}

def tool_router(state: State) -> Literal["tool_node", "__end__"]:
    last_message = state["messages"][-1]
    content = str(last_message.content)
    
    if re.search(r'<call_tool name=".*?">', content, re.DOTALL):
        return "tool_node"
        
    return END

