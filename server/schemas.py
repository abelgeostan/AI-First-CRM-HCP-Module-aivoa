from typing import Literal, Optional, Union

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from pydantic import BaseModel, Field, field_validator
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

    attendees: Optional[Union[list[str], str]] = Field(default_factory=list)

    topics_discussed: Optional[Union[str, list[str]]] = None

    materials_shared: Optional[Union[list[str], str]] = Field(default_factory=list)

    samples_distributed: Optional[Union[list[str], str]] = Field(default_factory=list)

    sentiment: Optional[str] = None

    outcomes: Optional[str] = None

    follow_up_actions: Optional[str] = None

    @field_validator("attendees", "materials_shared", "samples_distributed", mode="before")
    @classmethod
    def normalize_list_fields(cls, value):
        if value is None:
            return []
        if isinstance(value, str):
            return [value]
        if isinstance(value, list):
            return [str(item) for item in value if item is not None]
        return [str(value)]

    @field_validator("topics_discussed", mode="before")
    @classmethod
    def normalize_topics(cls, value):
        if value is None:
            return None
        if isinstance(value, list):
            return ", ".join(str(item) for item in value if item is not None)
        if isinstance(value, str):
            return value
        return str(value)


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

