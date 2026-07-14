from sqlalchemy import or_

from database import InteractionLog, SessionLocal
from llm import (
    extract_interaction,
    extract_updates,
    extract_search_query,
    generate_followups,
)
from schemas import HCPFormState


# --------------------------------------------------
# LOG
# --------------------------------------------------

def log_interaction(message: str):

    extracted = extract_interaction(message)

    db = SessionLocal()

    log = InteractionLog(
        **extracted.model_dump(exclude={"id"})
    )

    db.add(log)
    db.commit()
    db.refresh(log)

    extracted.id = log.id

    db.close()

    return {
        "reply": f"Interaction logged successfully with ID {log.id}.",
        "form_state": extracted.model_dump(),
        "current_log_id": log.id,
    }


# --------------------------------------------------
# EDIT
# --------------------------------------------------

def edit_interaction(
    log_id: int,
    message: str,
):

    updates = extract_updates(message).updates

    db = SessionLocal()

    log = (
        db.query(InteractionLog)
        .filter(
            InteractionLog.id == log_id,
            InteractionLog.is_deleted == False,
        )
        .first()
    )

    if log is None:

        db.close()

        return {
            "reply": "Interaction not found."
        }

    for key, value in updates.items():

        if hasattr(log, key):

            setattr(log, key, value)

    db.commit()
    db.refresh(log)

    form = HCPFormState.model_validate(
        log,
        from_attributes=True,
    )

    db.close()

    return {
        "reply": "Interaction updated successfully.",
        "form_state": form.model_dump(),
        "current_log_id": log.id,
    }


# --------------------------------------------------
# SEARCH
# --------------------------------------------------

def search_interactions(message: str):

    query = extract_search_query(message).query

    db = SessionLocal()

    logs = (
        db.query(InteractionLog)
        .filter(
            InteractionLog.is_deleted == False,
            or_(
                InteractionLog.hcp_name.ilike(f"%{query}%"),
                InteractionLog.topics_discussed.ilike(f"%{query}%"),
            ),
        )
        .all()
    )

    db.close()

    if not logs:
        return {
            "reply": "No interactions found matching your search."
        }

    results = []

    for log in logs:

        results.append({
            "id": log.id,
            "hcp_name": log.hcp_name,
            "interaction_type": log.interaction_type,
            "date": log.date,
            "topics_discussed": log.topics_discussed,
            "sentiment": log.sentiment,
        })

    reply = "\n".join(
        [
            f"ID:{r['id']} | {r['hcp_name']} | {r['interaction_type']} | {r['sentiment']}"
            for r in results
        ]
    )

    return {"reply": reply}


# --------------------------------------------------
# DELETE LIST
# --------------------------------------------------

def list_logs():

    db = SessionLocal()

    logs = (
        db.query(InteractionLog)
        .filter(
            InteractionLog.is_deleted == False
        )
        .all()
    )

    db.close()

    if not logs:
        return {
            "reply": "No logs available to delete."
        }

    lines = []

    for log in logs:
        lines.append(
            f"ID: {log.id}, HCP: {log.hcp_name}, Date: {log.date}"
        )

    return {
        "reply": "Select a log ID to delete.\n\n" + "\n".join(lines)
    }


# --------------------------------------------------
# DELETE
# --------------------------------------------------

def delete_interaction(log_id: int):

    db = SessionLocal()

    log = (
        db.query(InteractionLog)
        .filter(
            InteractionLog.id == log_id
        )
        .first()
    )

    if log is None:

        db.close()

        return {
            "reply": "Interaction not found."
        }

    log.is_deleted = True

    db.commit()

    db.close()

    return {
        "reply": f"Interaction {log_id} deleted successfully."
    }


# --------------------------------------------------
# FOLLOWUPS
# --------------------------------------------------

def build_suggestions(form_state: dict):

    topic = form_state.get("topics_discussed")

    if not topic:

        return []

    return generate_followups(topic)