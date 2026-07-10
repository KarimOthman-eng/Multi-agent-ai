import os
from functools import lru_cache

from dotenv import load_dotenv
from typing import Annotated, Literal
from typing_extensions import NotRequired, TypedDict
from langchain_groq import ChatGroq
from langgraph.graph.message import add_messages
from pydantic import BaseModel, Field
from langchain_core.messages import AnyMessage

GROQ_MODEL = "llama-3.1-8b-instant"


@lru_cache(maxsize=1)
def get_llm() -> ChatGroq:
    load_dotenv()
    if not os.getenv("GROQ_API_KEY"):
        raise RuntimeError("Missing GROQ_API_KEY. Add it to .env or set it in the environment.")
    return ChatGroq(model=GROQ_MODEL, temperature=0)


class ClassificationIntent(BaseModel):
    intent: Literal["research", "help"] = Field(
        ...,
        description="The intent of the user, either 'research' or 'help'.",
    )


class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    intent: NotRequired[Literal["research", "help"]]
    route: NotRequired[Literal["research", "help"]]
     


