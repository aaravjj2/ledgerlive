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
