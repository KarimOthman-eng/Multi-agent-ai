from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# --- 1. Import YOUR existing LangGraph structure ---
# This imports the compiled graph from your app/graph.py file
from app.graph import graph as my_agent_graph

# --- 2. Setup the FastAPI Server ---
app = FastAPI(title="My Custom LangGraph Server")

# Define the input format
class ChatInput(BaseModel):
    message: str
    thread_id: str = "default_session" # Added thread_id for memory if you use it

# --- 3. Create the Endpoint ---
@app.post("/chat")
def chat_endpoint(input_data: ChatInput):
    try:
        # Setup configuration for memory tracking (if your graph uses a checkpointer)
        config = {"configurable": {"thread_id": input_data.thread_id}}
        
        # Invoke YOUR existing agent graph
        result = my_agent_graph.invoke(
            {"messages": [("user", input_data.message)]},
            config=config
        )
        
        # Extract the final response from your agent
        last_message = result["messages"][-1].content
        return {"reply": last_message}
        
    except Exception as e:
        # If your agent crashes, the server will tell you exactly why
        raise HTTPException(status_code=500, detail=str(e))