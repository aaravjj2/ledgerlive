"""Gemini Live API integration for LedgerLive voice assistant.

Provides real-time audio-in/audio-out conversation with tool calling
for finance operations.
"""
from __future__ import annotations

import asyncio
import base64
import json
import os
from typing import Any, AsyncGenerator

# Conditional import — works in DEMO mode without google-genai installed
try:
    from google import genai
    from google.genai import types
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash-live")
GOOGLE_CLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT", "")

SYSTEM_PROMPT = """You are LedgerBot, an expert finance operations assistant with full access
to this company's reconciliation data, exception queue, and audit trail.

Your personality: precise, proactive, never alarming. You speak in clear,
conversational language. When discussing numbers, always state the currency and
round to two decimal places.

Capabilities:
- Query reconciliation status and match rates
- Review and triage exceptions by severity
- Look up specific transactions by ID or description
- Approve or reject exceptions (with human confirmation)
- Generate audit trail summaries
- Explain anomalies with root cause analysis

Rules:
- Always ask for human confirmation before modifying any record
- Never fabricate financial data — if unsure, say so
- Flag anomalies proactively when reviewing data
- Provide reasoning for every recommendation
"""

# Tool definitions for Gemini function calling
LEDGER_TOOLS = [
    {
        "name": "get_exceptions",
        "description": "Get all open exceptions in the triage queue, optionally filtered by severity",
        "parameters": {
            "type": "object",
            "properties": {
                "severity": {"type": "string", "enum": ["critical", "high", "medium", "low"], "description": "Filter by severity level"},
                "limit": {"type": "integer", "description": "Max number of exceptions to return", "default": 10}
            }
        }
    },
    {
        "name": "get_reconciliation_status",
        "description": "Get the current reconciliation run status including match rates and outstanding items",
        "parameters": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "get_transaction",
        "description": "Look up a specific transaction by ID",
        "parameters": {
            "type": "object",
            "properties": {
                "transaction_id": {"type": "string", "description": "The transaction ID to look up"}
            },
            "required": ["transaction_id"]
        }
    },
    {
        "name": "approve_exception",
        "description": "Approve an exception after human confirmation",
        "parameters": {
            "type": "object",
            "properties": {
                "exception_id": {"type": "string", "description": "The exception ID to approve"},
                "reason": {"type": "string", "description": "Reason for approval"}
            },
            "required": ["exception_id"]
        }
    },
    {
        "name": "reject_exception",
        "description": "Reject an exception after human confirmation",
        "parameters": {
            "type": "object",
            "properties": {
                "exception_id": {"type": "string", "description": "The exception ID to reject"},
                "reason": {"type": "string", "description": "Reason for rejection"}
            },
            "required": ["exception_id"]
        }
    },
    {
        "name": "get_audit_log",
        "description": "Get recent audit trail entries",
        "parameters": {
            "type": "object",
            "properties": {
                "limit": {"type": "integer", "description": "Max entries to return", "default": 20}
            }
        }
    },
    {
        "name": "get_close_period_status",
        "description": "Get the current close period status and progress",
        "parameters": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "get_dashboard_summary",
        "description": "Get a high-level summary of all finance metrics: documents processed, reconciliation progress, open exceptions, and SLA status",
        "parameters": {
            "type": "object",
            "properties": {}
        }
    }
]


class GeminiLiveSession:
    """Manages a single Gemini Live API conversation session."""

    def __init__(self, session_id: str, tool_executor: Any = None):
        self.session_id = session_id
        self.tool_executor = tool_executor
        self.history: list[dict] = []
        self._client = None
        self._session = None

    async def initialize(self) -> None:
        """Initialize the Gemini client and live session."""
        if not GENAI_AVAILABLE:
            return
        if GEMINI_API_KEY:
            self._client = genai.Client(api_key=GEMINI_API_KEY)
        elif GOOGLE_CLOUD_PROJECT:
            self._client = genai.Client(project=GOOGLE_CLOUD_PROJECT, location="us-central1")

    async def send_audio(self, audio_base64: str) -> AsyncGenerator[dict, None]:
        """Send audio chunk and yield response events."""
        if not GENAI_AVAILABLE or not self._client:
            # Demo mode — return a simulated response
            yield {
                "type": "transcript",
                "role": "user",
                "text": "[Audio received — demo mode, no Gemini API key configured]"
            }
            yield {
                "type": "text",
                "role": "assistant",
                "text": "I'm LedgerBot, your finance operations assistant. In demo mode, I can show you how I'd help with reconciliation review, exception triage, and audit trail queries. Configure your GEMINI_API_KEY to enable live voice interaction."
            }
            return

        # Real Gemini Live API flow
        config = types.LiveConnectConfig(
            response_modalities=["AUDIO", "TEXT"],
            system_instruction=types.Content(
                parts=[types.Part(text=SYSTEM_PROMPT)]
            ),
            tools=[types.Tool(function_declarations=[
                types.FunctionDeclaration(**tool) for tool in LEDGER_TOOLS
            ])]
        )

        async with self._client.aio.live.connect(
            model=GEMINI_MODEL, config=config
        ) as session:
            audio_bytes = base64.b64decode(audio_base64)
            await session.send(
                input=types.LiveClientRealtimeInput(
                    media_chunks=[types.Blob(data=audio_bytes, mime_type="audio/pcm;rate=16000")]
                )
            )

            async for response in session.receive():
                if response.text:
                    self.history.append({"role": "assistant", "text": response.text})
                    yield {"type": "text", "role": "assistant", "text": response.text}

                if response.data:
                    audio_b64 = base64.b64encode(response.data).decode()
                    yield {"type": "audio", "data": audio_b64}

                if hasattr(response, "tool_call") and response.tool_call:
                    tool_name = response.tool_call.function_calls[0].name
                    tool_args = dict(response.tool_call.function_calls[0].args)
                    yield {"type": "tool_call", "name": tool_name, "args": tool_args}

                    if self.tool_executor:
                        result = await self.tool_executor(tool_name, tool_args)
                        await session.send(
                            input=types.LiveClientToolResponse(
                                function_responses=[types.FunctionResponse(
                                    name=tool_name,
                                    response={"result": json.dumps(result)}
                                )]
                            )
                        )

    async def send_text(self, text: str) -> AsyncGenerator[dict, None]:
        """Send text input and yield response events (for non-voice interaction)."""
        self.history.append({"role": "user", "text": text})

        if not GENAI_AVAILABLE or not self._client:
            # Demo mode responses
            demo_responses = {
                "exceptions": "In demo mode: You have 3 open exceptions — 1 critical (duplicate payment $4,500), 1 high (vendor mismatch), 1 medium (timing difference). The critical one needs your review first.",
                "reconciliation": "Demo reconciliation status: 94.2% match rate across 847 transactions. 49 items matched automatically, 3 exceptions flagged for review.",
                "approve": "I'd need your explicit confirmation to approve. Could you say 'Yes, approve exception #47' to confirm?",
                "default": "I'm LedgerBot in demo mode. I can help with: exception review, reconciliation status, transaction lookups, and audit trail queries. What would you like to know?"
            }
            text_lower = text.lower()
            if "exception" in text_lower:
                response_text = demo_responses["exceptions"]
            elif "reconcil" in text_lower:
                response_text = demo_responses["reconciliation"]
            elif "approve" in text_lower or "yes" in text_lower:
                response_text = demo_responses["approve"]
            else:
                response_text = demo_responses["default"]

            self.history.append({"role": "assistant", "text": response_text})
            yield {"type": "text", "role": "assistant", "text": response_text}
            return

        # Real Gemini interaction would go here
        config = types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            tools=[types.Tool(function_declarations=[
                types.FunctionDeclaration(**tool) for tool in LEDGER_TOOLS
            ])]
        )
        response = await self._client.aio.models.generate_content(
            model="gemini-2.0-flash",
            contents=text,
            config=config
        )
        if response.text:
            self.history.append({"role": "assistant", "text": response.text})
            yield {"type": "text", "role": "assistant", "text": response.text}


# Session manager
_sessions: dict[str, GeminiLiveSession] = {}
MAX_SESSIONS = 10


async def get_or_create_session(session_id: str, tool_executor: Any = None) -> GeminiLiveSession:
    """Get existing session or create new one. Enforces max session limit."""
    if session_id in _sessions:
        return _sessions[session_id]
    if len(_sessions) >= MAX_SESSIONS:
        oldest = next(iter(_sessions))
        del _sessions[oldest]
    session = GeminiLiveSession(session_id, tool_executor)
    await session.initialize()
    _sessions[session_id] = session
    return session


def remove_session(session_id: str) -> None:
    """Remove a session when WebSocket disconnects."""
    _sessions.pop(session_id, None)
