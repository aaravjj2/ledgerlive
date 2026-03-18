import httpx
import os
import logging

logger = logging.getLogger(__name__)

AIRIA_ENDPOINT = os.getenv("AIRIA_ENDPOINT")
AIRIA_API_KEY = os.getenv("AIRIA_API_KEY")


async def call_airia_agent(message: str) -> dict:
    if not AIRIA_ENDPOINT or not AIRIA_API_KEY:
        logger.error("Airia not configured: missing AIRIA_ENDPOINT or AIRIA_API_KEY")
        return {
            "response": "Airia agent not configured",
            "success": False,
            "model": "airia-ledgerlive-close-orchestrator"
        }

    try:
        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(
                AIRIA_ENDPOINT,
                headers={
                    "Content-Type": "application/json",
                    "X-API-Key": AIRIA_API_KEY
                },
                json={"input": message}
            )
            response.raise_for_status()
            data = response.json()

            # Extract response from Airia output format
            body = data.get("Body", data)
            ai_response = (
                body.get("response") or
                body.get("summary") or
                body.get("Value") or
                str(body)
            )

            return {
                "response": ai_response,
                "success": True,
                "session_id": body.get("session_id", ""),
                "latency_ms": body.get("latency_ms", 0),
                "model": "airia-ledgerlive-close-orchestrator"
            }
    except httpx.HTTPStatusError as e:
        logger.error(f"Airia API error: {e.response.status_code} {e.response.text}")
        return {"response": f"Agent error: {e.response.status_code}", "success": False}
    except Exception as e:
        logger.error(f"Airia call failed: {e}")
        return {"response": f"Agent unavailable: {str(e)}", "success": False}
