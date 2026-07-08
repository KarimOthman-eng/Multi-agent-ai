# Agent Lograph Groq

A small LangGraph command-line assistant that routes each user message to either a helper agent or a research agent. The research path can call a DuckDuckGo search tool, then returns to the model so the user gets a normal assistant answer instead of raw tool output.

## Setup

1. Install dependencies:

   ```powershell
   uv sync
   ```

2. Add your Groq key to `.env`:

   ```text
   GROQ_API_KEY=your_key_here
   ```

3. Run the chat loop:

   ```powershell
   uv run python main.py
   ```

Type `exit` or `quit` to leave the chat.

## Flow

```text
user message -> classify_intent -> router -> helper or researcher
researcher -> search_web tool -> researcher -> final answer
```

Runtime code lives in `app/`, and agent node functions live in `agents/`.
"# multi-agent-ai" 
