import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq

INTENT_PROMPT = """
You are an intent classifier for a Life Science CRM.

Choose exactly one intent.

LOG
- User is describing a meeting, visit or call.
- User is logging a new interaction.

Examples:
Today I met Dr. Abel...
I had a call with...
Log this meeting...

EDIT
- User wants to change an existing interaction.
- User modifies any field.

Examples:
Change the sentiment to Positive.
Update the interaction type.
Add Dr. Smith.
Remove the attendee.
Correct the doctor's name.
Modify the meeting date.
Change the topic discussed.

SEARCH
Examples:
Search for log with name Smith.

Find all oncology meetings.
Show all logs.

DELETE
Examples:
Delete a log.
Remove interaction.
I want to delete an entry.

CONFIRM_DELETE
Examples:
confirm delete 3
yes delete 5

UNKNOWN
Anything unrelated to HCP interaction logs.

Return only the structured output.
"""


EXTRACTION_PROMPT = """
Extract the HCP interaction.

Leave unknown values as null.
give date as current date if not provided.
date format should be DD/MM/YYYY
the sentiment should be one of the following: Positive, Neutral, Negative, Unknown
the time should be the current time if not provided. 
time format should be HH:MM AM/PM

Never invent information.
"""


EDIT_PROMPT = """
Extract only the fields that should be updated.

Ignore every field that should remain unchanged.

Return a JSON object with one property named updates.

The value of updates must be an object containing only the changed fields.

Examples:
User: change the sentiment to Positive
Output: {"updates": {"sentiment": "Positive"}}

User: update the interaction type to Call and add Dr. Michael Lee
Output: {"updates": {"interaction_type": "Call", "attendees": ["Dr. Michael Lee"]}}
"""


SEARCH_PROMPT = """
Extract only the keyword the user wants to search.

Examples:

Search for Abel
↓

query="Abel"

Show all logs about Oncology
↓

query="Oncology"
"""


FOLLOWUP_PROMPT = """
Generate exactly three short follow-up actions.

Each action should be under one sentence.

Do not number them.
"""

from schemas import (
    EditRequest,
    HCPFormState,
    IntentResponse,
    SearchRequest,
)

load_dotenv()

def classify_intent(message: str):

    return intent_llm.invoke(
        f"""
{INTENT_PROMPT}

User:

{message}
"""
    )


def extract_interaction(message: str):

    return extract_llm.invoke(
        f"""
{EXTRACTION_PROMPT}

{message}
"""
    )


def extract_updates(message: str):

    return edit_llm.invoke(
        f"""
{EDIT_PROMPT}

{message}
"""
    )


def extract_search_query(message: str):

    return search_llm.invoke(
        f"""
{SEARCH_PROMPT}

{message}
"""
    )


def generate_followups(topic: str):

    response = llm.invoke(
        f"""
{FOLLOWUP_PROMPT}

Topic:

{topic}
"""
    )

    return [
        line.strip("-• ")
        for line in response.content.splitlines()
        if line.strip()
    ][:3]

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.2,
    groq_api_key=os.getenv("GROQ_API_KEY"),
)

# ----------------------------------------------------
# Structured LLMs
# ----------------------------------------------------

intent_llm = llm.with_structured_output(IntentResponse)

extract_llm = llm.with_structured_output(HCPFormState)

edit_llm = llm.with_structured_output(EditRequest)

search_llm = llm.with_structured_output(SearchRequest)