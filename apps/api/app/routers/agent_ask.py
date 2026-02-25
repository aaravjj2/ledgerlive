"""Agent Ask Router — Ask Race Engineer conversational panel.

Deterministic intent parsing in DEMO mode. Supports 6+ query types
with citations to dossiers and evidence IDs.

PROJECT_ID: LEDGERLIVE
"""
from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(tags=["Agent Ask"])


class AskRequest(BaseModel):
    question: str


@router.post("/api/agent/ask")
async def ask_agent(req: AskRequest):
    """Ask the Race Engineer a question. Deterministic in DEMO mode."""
    from app.services.cfo_scenario import ask_race_engineer
    return ask_race_engineer(req.question)


@router.get("/api/agent/ask/intents")
async def list_intents():
    """List supported intents for the Ask Race Engineer panel."""
    from app.services.cfo_scenario import ENGINEER_RESPONSES
    return {
        "intents": [
            {"id": k, "intent": v["intent"], "sample_question": _SAMPLES.get(k, "")}
            for k, v in ENGINEER_RESPONSES.items()
        ],
        "model": "deterministic-intent-v1",
        "total": len(ENGINEER_RESPONSES),
    }


_SAMPLES = {
    "blocking": "What's blocking the close?",
    "cost_cap": "What is our cost cap runway?",
    "highest_risk": "Which vendor is highest risk?",
    "approve_next": "What should we approve next?",
    "exception_why": "Show me why this exception was flagged",
    "court_pack": "Generate the court pack",
}
