"""Gemini Live Voice WebSocket endpoint for LedgerLive.

Provides real-time voice interaction with the finance agent.
"""
from __future__ import annotations

import json
import uuid

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from pydantic import BaseModel

from app.airia_adapter import call_airia_agent
from app.services.gemini_live import get_or_create_session, remove_session

router = APIRouter(tags=["gemini-voice"])


class VoiceRequest(BaseModel):
    text: str


@router.post("/api/voice/ask")
async def voice_ask(request: VoiceRequest):
    result = await call_airia_agent(request.text)
    return result


async def execute_tool(tool_name: str, tool_args: dict) -> dict:
    """Execute a LedgerLive tool call from Gemini."""
    # Import services lazily to avoid circular imports
    from app.services.w06_reconciliation import (
        list_reconciliations,
    )
    from app.services.w07_exception import list_exceptions
    from app.services.w01_close_period import list_close_periods
    from app.main import AUDIT_LOG

    if tool_name == "get_exceptions":
        exceptions = list_exceptions()
        severity = tool_args.get("severity")
        limit = tool_args.get("limit", 10)
        if severity:
            exceptions = [e for e in exceptions if e.get("severity") == severity]
        return {"exceptions": exceptions[:limit], "total": len(exceptions)}

    elif tool_name == "get_reconciliation_status":
        recons = list_reconciliations()
        return {"reconciliations": recons, "total": len(recons)}

    elif tool_name == "get_transaction":
        tid = tool_args.get("transaction_id", "")
        return {"transaction_id": tid, "status": "found", "amount": 1500.00, "description": "Sample transaction"}

    elif tool_name == "approve_exception":
        eid = tool_args.get("exception_id", "")
        reason = tool_args.get("reason", "Approved via voice")
        return {"exception_id": eid, "status": "approved", "reason": reason}

    elif tool_name == "reject_exception":
        eid = tool_args.get("exception_id", "")
        reason = tool_args.get("reason", "Rejected via voice")
        return {"exception_id": eid, "status": "rejected", "reason": reason}

    elif tool_name == "get_audit_log":
        limit = tool_args.get("limit", 20)
        return {"events": AUDIT_LOG[-limit:], "total": len(AUDIT_LOG)}

    elif tool_name == "get_close_period_status":
        periods = list_close_periods()
        return {"periods": periods, "total": len(periods)}

    elif tool_name == "get_dashboard_summary":
        recons = list_reconciliations()
        exceptions = list_exceptions()
        return {
            "documents_processed": 12,
            "reconciliation_rate": 94.2,
            "open_exceptions": len([e for e in exceptions if e.get("status") == "open"]),
            "total_exceptions": len(exceptions),
            "sla_status": "on_track"
        }

    return {"error": f"Unknown tool: {tool_name}"}


@router.websocket("/ws/voice")
async def voice_websocket(websocket: WebSocket):
    """WebSocket endpoint for real-time voice interaction with LedgerBot.

    Protocol:
    - Client sends: {"type": "audio", "data": "<base64 PCM>"}
    - Client sends: {"type": "text", "text": "..."}
    - Server responds: {"type": "text", "role": "assistant", "text": "..."}
    - Server responds: {"type": "audio", "data": "<base64 PCM>"}
    - Server responds: {"type": "tool_call", "name": "...", "args": {...}}
    """
    await websocket.accept()
    session_id = str(uuid.uuid4())

    try:
        session = await get_or_create_session(session_id, execute_tool)

        # Send welcome message
        await websocket.send_json({
            "type": "text",
            "role": "assistant",
            "text": "Hello! I'm LedgerBot, your finance operations assistant. How can I help you today?",
            "session_id": session_id,
        })

        while True:
            data = await websocket.receive_text()
            message = json.loads(data)

            if message.get("type") == "audio":
                async for event in session.send_audio(message["data"]):
                    await websocket.send_json(event)

            elif message.get("type") == "text":
                async for event in session.send_text(message.get("text", "")):
                    await websocket.send_json(event)

            elif message.get("type") == "ping":
                await websocket.send_json({"type": "pong"})

    except WebSocketDisconnect:
        remove_session(session_id)
    except Exception as e:
        try:
            await websocket.send_json({
                "type": "error",
                "message": f"LedgerBot encountered an issue: {str(e)}. Please try again."
            })
        except Exception:
            pass
        remove_session(session_id)


@router.get("/api/voice/status")
async def voice_status():
    """Get voice service status and session count."""
    from app.services.gemini_live import _sessions, GENAI_AVAILABLE, GEMINI_API_KEY
    return {
        "service": "gemini-voice",
        "status": "active",
        "genai_available": GENAI_AVAILABLE,
        "api_key_configured": bool(GEMINI_API_KEY),
        "active_sessions": len(_sessions),
        "max_sessions": 10,
    }


@router.get("/api/voice/tools")
async def voice_tools():
    """List available voice assistant tools."""
    from app.services.gemini_live import LEDGER_TOOLS
    return {"tools": LEDGER_TOOLS, "count": len(LEDGER_TOOLS)}
