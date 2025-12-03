# orchestrator.py
import json
import logging
from typing import Dict, Any, List
from config import settings
from memory import memory_repo
from runner import manager, make_user_event
from router import detect_role, role_references
from agents.schemas import (
    QAResult, QCResult, RegulatoryResult, PVResult,
    MarketAccessResult, SearchResult, RootReport
)

log = logging.getLogger("orchestrator")

def parse_json(payload: str) -> Dict[str, Any]:
    try:
        return json.loads(payload)
    except json.JSONDecodeError:
        return {}

async def orchestrator(query: str) -> str:
    ql = query.lower()

    # Memory commands
    if ql.startswith("remember:"):
        _, fact = query.split(":", 1)
        memory_repo.remember_fact("General", fact.strip())
        return json.dumps({"status": "ok", "message": f"Remembered: {fact.strip()}"}, indent=2)

    if ql.startswith("recall:"):
        facts = memory_repo.recall_all()
        report = RootReport(
            overview="Recalled memory across roles.",
            key_findings=["Memory snapshot"],
            sections={"MemoryContext": facts},
            references=[],
            next_steps=["Review and curate memory as needed."]
        )
        return report.model_dump_json(indent=2)

    # 🔑 NEW: detect if the query is JSON payload
    structured_payload = parse_json(query)
    if structured_payload:
        # If JSON was parsed successfully, skip role detection and send directly to Report agent
        formatted = manager.runner("Report").run(
            user_id=settings.user_id,
            session_id=settings.session_id,
            new_message=make_user_event(json.dumps({
                "payload": structured_payload,
                "references": structured_payload.get("references", [])
            }))
        )
        return manager.consume_output(formatted)

    # Otherwise, continue with role-based routing
    role = detect_role(query)
    payload: Dict[str, Any] = {}
    references: List[str] = role_references(role)
    memory_context = memory_repo.recall_all()
    if memory_context:
        payload["MemoryContext"] = memory_context

    try:
        if role == "QA":
            raw = manager.runner("QA").run(
                user_id=settings.user_id,
                session_id=settings.session_id,
                new_message=make_user_event(query)
            )
            qa = QAResult.model_validate(parse_json(manager.consume_output(raw)))
            payload["QA"] = qa.model_dump()
            references.extend(qa.references)
        elif role == "QC":
            raw = manager.runner("QC").run(
                user_id=settings.user_id,
                session_id=settings.session_id,
                new_message=make_user_event(query)
            )
            qc = QCResult.model_validate(parse_json(manager.consume_output(raw)))
            payload["QC"] = qc.model_dump()
            references.extend(qc.references)
        elif role == "Regulatory":
            raw = manager.runner("Regulatory").run(
                user_id=settings.user_id,
                session_id=settings.session_id,
                new_message=make_user_event(query)
            )
            reg = RegulatoryResult.model_validate(parse_json(manager.consume_output(raw)))
            payload["Regulatory"] = reg.model_dump()
            references.extend(reg.references)
        elif role == "PV":
            raw = manager.runner("PV").run(
                user_id=settings.user_id,
                session_id=settings.session_id,
                new_message=make_user_event(query)
            )
            pv = PVResult.model_validate(parse_json(manager.consume_output(raw)))
            payload["PV"] = pv.model_dump()
            references.extend(pv.references)
        elif role == "MarketAccess":
            raw = manager.runner("MarketAccess").run(
                user_id=settings.user_id,
                session_id=settings.session_id,
                new_message=make_user_event(query)
            )
            ma = MarketAccessResult.model_validate(parse_json(manager.consume_output(raw)))
            payload["MarketAccess"] = ma.model_dump()
            references.extend(ma.references)
        else:
            raw = manager.runner("Search").run(
                user_id=settings.user_id,
                session_id=settings.session_id,
                new_message=make_user_event(query)
            )
            srch = SearchResult.model_validate(parse_json(manager.consume_output(raw)))
            payload["Search"] = srch.model_dump()
    except Exception as e:
        log.exception("Agent execution error: %s", e)
        payload["Error"] = f"Agent failed: {e}"

    # Final formatting via report agent
    formatted = manager.runner("Report").run(
        user_id=settings.user_id,
        session_id=settings.session_id,
        new_message=make_user_event(json.dumps({
            "payload": payload,
            "references": list(set(references))
        }))
    )
    return manager.consume_output(formatted)
