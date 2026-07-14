from uuid import uuid4

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langchain_core.messages import HumanMessage

from graph import graph
from schemas import ChatRequest, ChatResponse


app = FastAPI(
    title="Life Science CRM Agent",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# Chat Endpoint
# --------------------------------------------------

@app.post(
    "/api/chat",
    response_model=ChatResponse,
)
def chat(request: ChatRequest):

    thread_id = request.thread_id or str(uuid4())

    state = {
        "messages": [
            HumanMessage(content=request.message)
        ],

        "intent": "",

        "reply": "",

        "form_state": {},

        "ai_suggestions": [],

        "current_log_id": request.current_log_id,

        "pending_delete_id": None,
    }

    result = graph.invoke(
        state,
        config={
            "configurable": {
                "thread_id": thread_id
            }
        },
    )

    return ChatResponse(
        reply=result.get("reply", ""),

        form_state=result.get(
            "form_state",
            {},
        ),

        ai_suggestions=result.get(
            "ai_suggestions",
            [],
        ),
    )


# --------------------------------------------------
# Health Check
# --------------------------------------------------

@app.get("/")
def health():

    return {
        "status": "healthy",
        "service": "Life Science CRM Agent",
    }