from typing import Literal, Optional

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from pydantic import BaseModel, Field
from typing_extensions import Annotated, TypedDict


# --------------------------------------------------
# HCP Interaction Form
# --------------------------------------------------

class HCPFormState(BaseModel):
    id: Optional[int] = None

    hcp_name: Optional[str] = None

    interaction_type: str = "Meeting"

    date: Optional[str] = None

    time: Optional[str] = None

    attendees: list[str] = Field(default_factory=list)

    topics_discussed: Optional[str] = None

    materials_shared: list[str] = Field(default_factory=list)

    samples_distributed: list[str] = Field(default_factory=list)

    sentiment: Optional[str] = None

    outcomes: Optional[str] = None

    follow_up_actions: Optional[str] = None


# --------------------------------------------------
# API Models
# --------------------------------------------------

class ChatRequest(BaseModel):
    message: str

    thread_id: str

    current_log_id: Optional[int] = None


class ChatResponse(BaseModel):
    reply: str

    form_state: dict = Field(default_factory=dict)

    ai_suggestions: list[str] = Field(default_factory=list)


# --------------------------------------------------
# Intent Classification
# --------------------------------------------------

class IntentResponse(BaseModel):
    intent: Literal[
        "LOG",
        "EDIT",
        "SEARCH",
        "DELETE",
        "CONFIRM_DELETE",
        "UNKNOWN",
    ]


# --------------------------------------------------
# Edit Extraction
# --------------------------------------------------

class EditRequest(BaseModel):
    updates: dict


# --------------------------------------------------
# Search Extraction
# --------------------------------------------------

class SearchRequest(BaseModel):
    query: str


# --------------------------------------------------
# LangGraph State
# --------------------------------------------------

class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

    intent: str

    reply: str

    form_state: dict

    ai_suggestions: list[str]

    current_log_id: Optional[int]

    pending_delete_id: Optional[int]

