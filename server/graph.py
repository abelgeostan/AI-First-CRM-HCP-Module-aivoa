from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

from schemas import AgentState
from llm import classify_intent
from services import (
    log_interaction,
    edit_interaction,
    search_interactions,
    list_logs,
    delete_interaction,
    build_suggestions,
)


# --------------------------------------------------
# Intent Detection
# --------------------------------------------------

def detect_intent(state: AgentState):

    message = state["messages"][-1].content
    normalized = message.lower()

    if state["current_log_id"] is not None and (
        "follow up action" in normalized
        or "follow-up action" in normalized
        or "add follow up" in normalized
        or "add follow-up" in normalized
        or "followup action" in normalized
    ):
        return {
            "intent": "EDIT"
        }

    intent = classify_intent(message)

    return {
        "intent": intent.intent
    }


# --------------------------------------------------
# Router
# --------------------------------------------------

def router(state: AgentState):

    return state["intent"]


# --------------------------------------------------
# Log
# --------------------------------------------------

def log_node(state: AgentState):

    result = log_interaction(
        state["messages"][-1].content
    )

    return result


# --------------------------------------------------
# Edit
# --------------------------------------------------

def edit_node(state: AgentState):

    if state["current_log_id"] is None:

        return {
            "reply": "Please provide a log id."
        }

    result = edit_interaction(
        state["current_log_id"],
        state["messages"][-1].content,
    )

    return result


# --------------------------------------------------
# Search
# --------------------------------------------------

def search_node(state: AgentState):

    return search_interactions(
        state["messages"][-1].content
    )


# --------------------------------------------------
# Delete
# --------------------------------------------------

def delete_node(state: AgentState):

    return list_logs()


# --------------------------------------------------
# Confirm Delete
# --------------------------------------------------

def confirm_delete_node(state: AgentState):

    message = state["messages"][-1].content

    try:

        log_id = int(message.split()[-1])

    except:

        return {
            "reply": "Invalid log id."
        }

    return delete_interaction(log_id)


# --------------------------------------------------
# Unknown
# --------------------------------------------------

def unknown_node(state: AgentState):

    return {
        "reply":
            "I can only help with logging, editing, searching and deleting HCP interactions."
    }


# --------------------------------------------------
# Suggestions
# --------------------------------------------------

def suggestion_node(state: AgentState):

    suggestions = build_suggestions(
        state["form_state"]
    )

    return {
        "ai_suggestions": suggestions
    }


# --------------------------------------------------
# Build Graph
# --------------------------------------------------

builder = StateGraph(AgentState)

builder.add_node("intent", detect_intent)

builder.add_node("LOG", log_node)

builder.add_node("EDIT", edit_node)

builder.add_node("SEARCH", search_node)

builder.add_node("DELETE", delete_node)

builder.add_node("CONFIRM_DELETE", confirm_delete_node)

builder.add_node("UNKNOWN", unknown_node)

builder.add_node("SUGGESTIONS", suggestion_node)

builder.set_entry_point("intent")


builder.add_conditional_edges(
    "intent",
    router,
    {
        "LOG": "LOG",
        "EDIT": "EDIT",
        "SEARCH": "SEARCH",
        "DELETE": "DELETE",
        "CONFIRM_DELETE": "CONFIRM_DELETE",
        "UNKNOWN": "UNKNOWN",
    }
)


builder.add_edge("LOG", "SUGGESTIONS")

builder.add_edge("EDIT", "SUGGESTIONS")

builder.add_edge("SEARCH", END)

builder.add_edge("DELETE", END)

builder.add_edge("CONFIRM_DELETE", END)

builder.add_edge("UNKNOWN", END)

builder.add_edge("SUGGESTIONS", END)


memory = MemorySaver()

graph = builder.compile(
    checkpointer=memory
)