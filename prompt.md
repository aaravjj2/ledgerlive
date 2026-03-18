You are working on a hackathon project called LedgerLive. The repo is already cloned and the FastAPI backend is at apps/api/app/. The live deployment is on Google Cloud Run.

## CREDENTIALS YOU HAVE
- AIRIA_API_KEY: ak-MTQxMTc3NDE2NHwxNzczODA1MTE0MDAwfHRpLVZtbHlaMmx1YVdFZ1ZHVmphQzFQY0dWdUlGSmxaMmx6ZEhKaGRHbHZiaTFCYVhKcFlTQkdjbVZsfDF8Mzg0MzA3MzU2NyAg
- AIRIA_ENDPOINT: https://api.airia.ai/v2/PipelineExecution/030f43a3-5f34-4351-a659-094408f3e250
- GCP Project: gen-lang-client-0432346640
- Live API URL: https://ledgerlive-api-production.up.railway.app
- Live Web URL: https://web-omega-silk-71.vercel.app

## TASK 1 — CREATE AIRIA ADAPTER
Create file apps/api/app/airia_adapter.py with this exact content:
```python
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
```

## TASK 2 — WIRE AIRIA INTO MAIN.PY
Open apps/api/app/main.py. Find the route that handles POST /api/voice/ask. It currently calls Gemini. Replace the entire handler body so it calls call_airia_agent() from airia_adapter.py instead. The request body field is called "text" (FastAPI Pydantic model). The handler should look like:
```python
from .airia_adapter import call_airia_agent

@app.post("/api/voice/ask")
async def voice_ask(request: VoiceRequest):
    result = await call_airia_agent(request.text)
    return result
```

If the Pydantic model uses a different field name than "text", find what field name the model actually uses and use that. Do not change the route path or the Pydantic model — only replace the handler body.

## TASK 3 — UPDATE ENV FILES
Add to .env (local, not committed):
AIRIA_ENDPOINT=<the endpoint provided>
AIRIA_API_KEY=<the key provided>

Add to .env.example (committed to repo):
AIRIA_ENDPOINT=https://api.airia.ai/v1/PROJECT_ID/PIPELINE_ID/execute
AIRIA_API_KEY=your_airia_api_key_here

Verify .env is in .gitignore. If it is not, add it.

## TASK 4 — LOCAL VERIFICATION
Run these checks in order and report the result of each:

Check 1 — start the API locally:
cd apps/api
pip install httpx --break-system-packages
source venv/bin/activate (or python -m venv venv && source venv/bin/activate if venv doesn't exist)
export AIRIA_ENDPOINT=<endpoint>
export AIRIA_API_KEY=<key>
uvicorn app.main:app --reload --port 8090 &
sleep 5

Check 2 — test the Airia integration:
curl -s -X POST http://localhost:8090/api/voice/ask \
  -H "Content-Type: application/json" \
  -d '{"text": "What exceptions are open and which can be auto-resolved to close the books this month?"}' | jq '.'

Expected: JSON response with a "response" field containing text about exceptions. If it returns {"response": "Airia agent not configured"} then the env vars are not being picked up — debug and fix.

Check 3 — test the exceptions endpoint still works:
curl -s https://ledgerlive-api-production.up.railway.app/api/exceptions | jq '.items | length'
Expected: 3

Check 4 — run existing tests to make sure nothing is broken:
cd apps/api
pytest tests/ -x -q --tb=short 2>&1 | tail -20

## TASK 5 — UPDATE CLOUD RUN
Deploy the updated API to Cloud Run with the Airia env vars:

gcloud run services update ledgerlive-api \
  --region us-central1 \
  --set-env-vars \
    AIRIA_ENDPOINT="<endpoint>",\
    AIRIA_API_KEY="<key>" \
  --project gen-lang-client-0432346640

Wait for deployment then verify:
curl -s -X POST https://ledgerlive-api-production.up.railway.app/api/voice/ask \
  -H "Content-Type: application/json" \
  -d '{"text": "What exceptions are open this month?"}' | jq '.'

Expected: same Airia response as local. If this fails, check Cloud Run logs:
gcloud logs read --project gen-lang-client-0432346640 --limit 50

## TASK 6 — GIT COMMIT AND PUSH
git add apps/api/app/airia_adapter.py
git add apps/api/app/main.py  
git add .env.example
git status
git commit -m "feat: integrate Airia Close Orchestrator agent

- Add airia_adapter.py: async HTTP client for Airia API
- Wire /api/voice/ask endpoint to Airia agent
- Replace Gemini Live with Airia LedgerLive Close Orchestrator
- Agent runs Perceive→Decide→Act loop with GPT 4.1
- HITL escalation for high-risk exceptions via Airia approval workflow
- Update .env.example with AIRIA_ENDPOINT and AIRIA_API_KEY vars

Airia agent: LedgerLive Close Orchestrator (Active Agents track)
Hackathon: Airia AI Agents Hackathon - devpost.com/airia-hackathon"
git push origin main

## TASK 7 — RECORD DEMO VIDEO WITH PLAYWRIGHT
Install playwright if not present:
pip install playwright --break-system-packages
playwright install chromium

Create and run this script as record_demo.py:
```python
import asyncio
from playwright.async_api import async_playwright
import time

async def record_demo():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            slow_mo=800,
            args=["--window-size=1440,900"]
        )
        context = await browser.new_context(
            viewport={"width": 1440, "height": 900},
            record_video_dir="./demo_video/",
            record_video_size={"width": 1440, "height": 900}
        )
        page = await context.new_page()
        
        BASE = "https://web-omega-silk-71.vercel.app"
        
        # Scene 1: Dashboard (8 seconds)
        print("Scene 1: Dashboard")
        await page.goto(BASE)
        await page.wait_for_load_state("networkidle")
        await asyncio.sleep(8)
        
        # Scene 2: Exceptions page (6 seconds)
        print("Scene 2: Exceptions")
        await page.goto(f"{BASE}/exceptions")
        await page.wait_for_load_state("networkidle")
        await asyncio.sleep(6)
        
        # Scene 3: Agent Console - navigate there
        print("Scene 3: Agent Console")
        await page.goto(f"{BASE}/agent-console")
        await page.wait_for_load_state("networkidle")
        await asyncio.sleep(3)
        
        # Type the demo message slowly
        input_selectors = [
            "textarea",
            "input[type='text']",
            "[placeholder*='message']",
            "[placeholder*='Message']",
            "[placeholder*='ask']",
            "[placeholder*='type']",
            ".agent-input",
            "#agent-input"
        ]
        
        input_el = None
        for selector in input_selectors:
            try:
                input_el = await page.wait_for_selector(selector, timeout=3000)
                if input_el:
                    break
            except:
                continue
        
        if input_el:
            await input_el.click()
            await asyncio.sleep(1)
            await input_el.type(
                "What exceptions are open and which can be auto-resolved to close the books this month?",
                delay=40
            )
            await asyncio.sleep(2)
            
            # Submit - try multiple methods
            try:
                await page.keyboard.press("Enter")
            except:
                pass
            
            # Try send button
            send_selectors = ["button[type='submit']", "button:has-text('Send')", ".send-button", "#send-btn"]
            for sel in send_selectors:
                try:
                    btn = await page.query_selector(sel)
                    if btn:
                        await btn.click()
                        break
                except:
                    continue
            
            print("Waiting for Airia agent response...")
            await asyncio.sleep(12)
        else:
            print("Could not find input - showing page for 10 seconds")
            await asyncio.sleep(10)
        
        # Scene 4: Show Readiness Dashboard
        print("Scene 4: Readiness Dashboard")
        await page.goto(f"{BASE}/readiness")
        await page.wait_for_load_state("networkidle")
        await asyncio.sleep(6)
        
        # Scene 5: Show Trace Explorer
        print("Scene 5: Trace Explorer")
        await page.goto(f"{BASE}/trace-explorer")
        await page.wait_for_load_state("networkidle")
        await asyncio.sleep(5)
        
        # Scene 6: Back to dashboard final shot
        print("Scene 6: Final dashboard shot")
        await page.goto(BASE)
        await page.wait_for_load_state("networkidle")
        await asyncio.sleep(4)
        
        await context.close()
        await browser.close()
        print("Video recorded to ./demo_video/")

asyncio.run(record_demo())
```

Run it:
python record_demo.py

The video will be saved in ./demo_video/ as a .webm file. Convert it to mp4:
ffmpeg -i demo_video/*.webm -c:v libx264 -preset slow -crf 22 demo_video/LEDGERLIVE_DEMO.mp4

If ffmpeg is not installed:
apt-get install -y ffmpeg 2>/dev/null || brew install ffmpeg

Copy the final video to the artifacts directory:
cp demo_video/LEDGERLIVE_DEMO.mp4 artifacts/demo/LEDGERLIVE_DEMO_AIRIA.mp4

## TASK 8 — UPDATE SUBMISSION DOCS
Update the following files to reflect the Airia integration:

1. README.md — find the line that says "Gemini Live" in the badges and key features section. Add a new badge:
[![Airia](https://img.shields.io/badge/Airia-Close_Orchestrator-6B46C1.svg)](https://airia.com)
And add to Key Features:
"- **Airia Close Orchestrator** — Multi-step Active Agent with GPT 4.1, HITL approval, and live API integration"

2. Create a new file AIRIA_INTEGRATION.md with this content:
Airia Integration — LedgerLive Close Orchestrator
Agent Details

Platform: Airia AI Agents
Track: Active Agents
Model: GPT 4.1
Hackathon: Airia AI Agents Hackathon

Agent Flow
Input → [FetchExceptions + FetchKPIs] → CloseOrchestrator (GPT 4.1) → RiskRouter → [HighRisk: CFOReviewGate HITL] [LowRisk: PostJournalEntry] → Output
What the Agent Does

PERCEIVE: Fetches live exceptions from /api/exceptions and readiness from /api/readiness
DECIDE: GPT 4.1 classifies each exception as LOW_RISK or HIGH_RISK
ACT: Posts journal entries for LOW_RISK items automatically
HITL: HIGH_RISK items trigger Human Approval — CFO approves/denies via email

API Integration
The LedgerLive FastAPI backend (/api/voice/ask) calls the Airia agent via airia_adapter.py.
The Airia agent calls back into the LedgerLive API to fetch data and post actions.
Live Systems Connected

LedgerLive FastAPI: https://ledgerlive-api-production.up.railway.app
LedgerLive Web: https://web-omega-silk-71.vercel.app
Airia Agent: [COMMUNITY URL]


3. Update DEVPOST_PROJECT_STORY.md — replace every mention of "Gemini Live" with "Airia Close Orchestrator" in the first 3 paragraphs. Add this sentence to the opening: "We built LedgerLive as an Active Agent on the Airia platform, connecting GPT 4.1 to a live financial close API with human-in-the-loop approval for high-risk exceptions."

## TASK 9 — FINAL GIT PUSH
git add .
git commit -m "docs: update submission materials for Airia hackathon integration

- Add AIRIA_INTEGRATION.md with full agent architecture
- Update README with Airia badge and feature entry
- Update DEVPOST_PROJECT_STORY for Airia submission
- Add demo video artifacts/demo/LEDGERLIVE_DEMO_AIRIA.mp4"
git push origin main

## TASK 10 — FINAL VERIFICATION CHECKLIST
Run each of these and report pass/fail:

[ ] curl https://ledgerlive-api-production.up.railway.app/api/exceptions returns 200 with 3 items
[ ] curl -X POST https://ledgerlive-api-production.up.railway.app/api/voice/ask -H "Content-Type: application/json" -d '{"text":"test"}' returns 200 with a "response" field
[ ] curl https://web-omega-silk-71.vercel.app returns 200 (frontend loads)
[ ] git log --oneline -3 shows the two new commits
[ ] demo_video/LEDGERLIVE_DEMO_AIRIA.mp4 exists and is larger than 1MB
[ ] AIRIA_INTEGRATION.md exists in repo root
[ ] .env is NOT tracked by git (git status should not show .env)

Report the result of every check. If anything fails, fix it before finishing.

## IMPORTANT NOTES FOR THE AGENT
- The repo uses Python 3.12
- Always use --break-system-packages with pip if outside a venv
- If you cannot find the /api/voice/ask route in main.py, search for "voice" or "ask" or "gemini" in all files under apps/api/app/ to find the right file
- If the frontend URLs for the demo video return 404 pages, try these alternate routes: /dashboard, /agent-console, /race-control, /airia — use whichever ones actually load
- Do not modify any test files
- Do not change the Pydantic models, only the route handler bodies
- The .env file must never be committed — check this explicitly