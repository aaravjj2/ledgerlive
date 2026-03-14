# LedgerLive — Multi-Hackathon Master Plan & Task List
> Project: LedgerLive (Finance Ops Close Agent)
> Repo: https://github.com/aaravjj2/ledgerlive
> Last Updated: March 13, 2026

---

## HACKATHON OVERVIEW & DEADLINES

| # | Hackathon | Prize Pool | Deadline | Priority |
|---|-----------|-----------|----------|----------|
| 1 | Gemini Live Agent Challenge | $80,000 | Mar 16 @ 5pm PDT | ⚡ URGENT |
| 2 | DigitalOcean Gradient AI | $20,000 | Mar 18 @ 5pm EDT | 🔥 HIGH |
| 3 | Airia AI Agents | $7,000 | Mar 19 @ 11:45pm EDT | 🔥 HIGH |
| 4 | GitLab AI Hackathon | $65,000 | Mar 25 @ 2pm EDT | 📅 PLANNED |

**Total prize potential: $172,000**

---

## STRATEGIC NARRATIVE (READ THIS FIRST)

LedgerLive is a finance ops close agent. The core workflow — ingest documents → OCR/extract → reconcile → triage exceptions → HITL review → generate audit binder — is a genuinely strong story for ALL FOUR hackathons. Here is how to frame it for each:

- **Gemini**: "Talk to your ledger in real-time." Voice-enabled finance assistant using Gemini Live API. A CFO can speak questions and the agent responds, explains anomalies, and awaits approval — all via audio.
- **DigitalOcean**: "Production-grade AI finance ops, cloud-native." Deploy the full stack on DigitalOcean Gradient AI with GPU-backed OCR and model inference, managed Postgres, and App Platform deployment.
- **Airia**: "The enterprise multi-agent close team." A network of specialized agents (Ingestion, Reconciliation, Exception, HITL Coordinator) built and published on Airia's platform, orchestrated across 2+ enterprise systems.
- **GitLab**: "AI-accelerated finance DevOps — compliance, audit, and release pipelines, automated." A GitLab Duo Agent that monitors merge requests for financial configuration changes, runs compliance checks, and auto-generates audit artifacts. This also qualifies for the Anthropic bonus ($13,500) by routing through Claude.

---

## CROSS-CUTTING FOUNDATION TASKS
> These apply to ALL hackathons. Do these first, in order.

### REPO & LEGAL

- [ ] FOUND-001: Add MIT LICENSE file to root of repo (required by DigitalOcean and GitLab; good hygiene for all)
- [ ] FOUND-002: Ensure LICENSE is visible in the GitHub "About" section (set it in repo settings)
- [ ] FOUND-003: Add open-source license badge to README header
- [ ] FOUND-004: Verify .gitignore excludes all API keys, .env files, and secrets
- [ ] FOUND-005: Create a `.env.example` file listing all required environment variables with placeholder values
- [ ] FOUND-006: Add a CONTRIBUTING.md with basic contribution guidelines
- [ ] FOUND-007: Add a CODE_OF_CONDUCT.md (standard Contributor Covenant)
- [ ] FOUND-008: Tag the current state of the repo as `v0.1.0-pre-hackathon` before making any changes
- [ ] FOUND-009: Create a `hackathons/` directory to hold per-hackathon submission assets
- [ ] FOUND-010: Create `hackathons/gemini/`, `hackathons/digitalocean/`, `hackathons/airia/`, `hackathons/gitlab/` subdirectories

### README OVERHAUL

- [ ] README-001: Rewrite README.md with a compelling hero section — project name, one-line description, and what problem it solves
- [ ] README-002: Add a live demo GIF or screenshot carousel to README (at minimum 3 screenshots already exist in repo — reference them properly)
- [ ] README-003: Add a clear "Architecture" section with a Mermaid diagram in the README
- [ ] README-004: Write a "Quick Start" section that works on a clean machine (test it)
- [ ] README-005: Add a "Features" section listing all current capabilities with checkboxes
- [ ] README-006: Add a "Tech Stack" table (FastAPI, React, Vite, Tailwind, SQLite/Postgres, etc.)
- [ ] README-007: Add badges: build status, license, Python version, Node version
- [ ] README-008: Add a "Hackathon Submissions" section linking to each Devpost page
- [ ] README-009: Add a "Roadmap" section showing planned features
- [ ] README-010: Fix any broken links or references in the existing README

### CODE QUALITY BASELINE

- [ ] CODE-001: Run `black` formatter on all Python files and commit
- [ ] CODE-002: Run `isort` on all Python imports
- [ ] CODE-003: Run `eslint` on all TypeScript/React files and fix errors
- [ ] CODE-004: Add `pre-commit` config with black, isort, eslint hooks
- [ ] CODE-005: Remove any hardcoded localhost URLs — make them env-var-driven
- [ ] CODE-006: Add docstrings to all FastAPI route handlers
- [ ] CODE-007: Add type hints to all Python functions missing them
- [ ] CODE-008: Write a `Dockerfile` for the FastAPI backend
- [ ] CODE-009: Write a `Dockerfile` for the React frontend
- [ ] CODE-010: Write a `docker-compose.yml` that brings up the full stack locally
- [ ] CODE-011: Add health check endpoint `GET /health` returning `{"status": "ok", "version": "x.y.z"}`
- [ ] CODE-012: Add structured logging with `structlog` or `loguru` to the Python backend
- [ ] CODE-013: Replace SQLite connection strings with environment variable–driven config so it's swappable for Postgres
- [ ] CODE-014: Add Alembic for database migrations
- [ ] CODE-015: Write at least 10 meaningful unit tests for reconciliation logic
- [ ] CODE-016: Write at least 5 integration tests for FastAPI endpoints
- [ ] CODE-017: Add a `Makefile` target `make test` that runs all tests
- [ ] CODE-018: Add a `Makefile` target `make lint` that runs all linters
- [ ] CODE-019: Add a `Makefile` target `make docker-up` that starts the full stack
- [ ] CODE-020: Add a `Makefile` target `make demo` that seeds sample data and opens the browser

### DEMO & VIDEO ASSETS

- [ ] DEMO-001: Create a `demo/` directory with sample financial documents (PDFs, CSVs) for judges to use
- [ ] DEMO-002: Write a `demo/seed.py` script that populates the database with realistic sample data (at least 50 transactions, 5 documents, 3 reconciliation runs, 2 exceptions)
- [ ] DEMO-003: Record a 5-minute "master" walkthrough video covering all features end-to-end
- [ ] DEMO-004: Cut a 4-minute version for Airia (enterprise multi-agent framing)
- [ ] DEMO-005: Cut a 3-minute version for DigitalOcean (cloud infra + GPU framing)
- [ ] DEMO-006: Cut a 4-minute version for Gemini (voice/multimodal framing)
- [ ] DEMO-007: Cut a 3-minute version for GitLab (DevOps/compliance framing)
- [ ] DEMO-008: Upload all videos to YouTube (unlisted) and save URLs in `hackathons/video-links.md`
- [ ] DEMO-009: Create a demo script / narration guide for each video
- [ ] DEMO-010: Add captions/subtitles to each demo video for accessibility

### ARCHITECTURE DIAGRAMS

- [ ] ARCH-001: Draw the full system architecture diagram (PNG + source file, Miro/Excalidraw)
- [ ] ARCH-002: Draw the agent workflow diagram showing each agent stage and data flow
- [ ] ARCH-003: Draw the HITL decision flow diagram
- [ ] ARCH-004: Draw a Gemini-specific architecture diagram (frontend → Gemini Live API → FastAPI → DB)
- [ ] ARCH-005: Draw a DigitalOcean-specific architecture diagram (App Platform → Gradient AI → Managed Postgres)
- [ ] ARCH-006: Draw an Airia-specific multi-agent architecture diagram
- [ ] ARCH-007: Draw a GitLab-specific architecture diagram (GitLab event → Duo Agent → LedgerLive API → audit trail)
- [ ] ARCH-008: Save all diagrams as both PNG and SVG in `docs/architecture/`
- [ ] ARCH-009: Embed all diagrams in their respective hackathon subdirectories under `hackathons/`
- [ ] ARCH-010: Add Mermaid source for each diagram inline in the README

---

## HACKATHON 1: GEMINI LIVE AGENT CHALLENGE
> Deadline: March 16, 2026 @ 5pm PDT — 3 DAYS FROM NOW
> Prize: $80,000 | Track: Live Agents 🗣️
> Mandatory: Gemini Live API or ADK, Google Cloud hosting

### PHASE 1: GOOGLE CLOUD SETUP (Day 1 Morning)

- [ ] GEM-001: Create a new Google Cloud project named `ledgerlive-gemini`
- [ ] GEM-002: Enable the following APIs: Vertex AI, Cloud Run, Cloud Build, Cloud SQL, Secret Manager, Artifact Registry
- [ ] GEM-003: Set up a service account with appropriate IAM roles for Cloud Run and Vertex AI
- [ ] GEM-004: Install and authenticate `gcloud` CLI locally
- [ ] GEM-005: Set up Artifact Registry repository for Docker images (`us-central1-docker.pkg.dev/ledgerlive-gemini/ledgerlive`)
- [ ] GEM-006: Enable billing and confirm free-tier / credit coverage for the project
- [ ] GEM-007: Create a Cloud SQL Postgres instance (`ledgerlive-db`) or use SQLite on Cloud Run for simplicity
- [ ] GEM-008: Store all secrets (DB password, Gemini API key) in Secret Manager
- [ ] GEM-009: Create a `cloudbuild.yaml` for CI/CD pipeline to Cloud Run
- [ ] GEM-010: Add a `PROJECT_ID` and `REGION` to `.env.example`

### PHASE 2: GEMINI LIVE API INTEGRATION (Day 1 Afternoon)

- [ ] GEM-011: Install Google GenAI SDK: `pip install google-genai`
- [ ] GEM-012: Create `apps/api/app/services/gemini_live.py` — wrapper module for Gemini Live API
- [ ] GEM-013: Implement WebSocket endpoint `WS /ws/voice` in FastAPI for real-time audio streaming
- [ ] GEM-014: Implement audio-in / text-out flow: receive base64-encoded PCM audio chunks, send to Gemini Live, return transcript
- [ ] GEM-015: Implement audio-in / audio-out flow: receive PCM audio, get audio response from Gemini, stream back to client
- [ ] GEM-016: Write a system prompt for the LedgerLive finance assistant persona: "You are LedgerBot, an expert finance operations assistant with full access to this company's reconciliation data, exception queue, and audit trail. Answer questions conversationally, flag anomalies proactively, and always ask for human confirmation before modifying any record."
- [ ] GEM-017: Implement tool calling: define Gemini tools for `get_exceptions()`, `get_reconciliation_status()`, `get_transaction(id)`, `approve_exception(id)`, `reject_exception(id)`, `get_audit_log()`
- [ ] GEM-018: Wire tool calls to actual FastAPI service layer — when Gemini calls a tool, execute the real DB query and return results
- [ ] GEM-019: Implement interruption handling — if user speaks mid-response, cut off the current audio stream and start a new response
- [ ] GEM-020: Add session management so each WebSocket connection has its own conversation history
- [ ] GEM-021: Implement graceful error handling — if Gemini times out or returns an error, speak a fallback message to the user
- [ ] GEM-022: Add rate limiting to the WebSocket endpoint (max 10 concurrent sessions)
- [ ] GEM-023: Test the voice flow end-to-end with a mock audio file

### PHASE 3: FRONTEND VOICE UI (Day 2 Morning)

- [ ] GEM-024: Install browser audio dependencies: `npm install @mediapipe/tasks-audio` or use Web Audio API
- [ ] GEM-025: Create `apps/web/src/components/VoiceAssistant.tsx` — the main voice interface component
- [ ] GEM-026: Implement `useAudioCapture` hook — captures microphone input as PCM chunks via `getUserMedia` and `AudioContext`
- [ ] GEM-027: Implement `useWebSocket` hook — manages WebSocket connection to `WS /ws/voice` with reconnection logic
- [ ] GEM-028: Implement `useAudioPlayback` hook — queues and plays audio chunks received from the backend
- [ ] GEM-029: Build the voice UI: a floating "LedgerBot" widget with a pulsing microphone button, live waveform visualization, and transcript display
- [ ] GEM-030: Add "push to talk" mode (hold spacebar or hold button) as well as always-on mode
- [ ] GEM-031: Add a live transcript panel that shows what the user said and what LedgerBot responded, with timestamps
- [ ] GEM-032: Add visual "thinking" indicator while waiting for Gemini response
- [ ] GEM-033: Add voice activity detection (VAD) so recording auto-stops when user stops speaking (use WebRTC VAD or simple amplitude threshold)
- [ ] GEM-034: Add a "LedgerBot is speaking" indicator with a stop button to interrupt playback
- [ ] GEM-035: Style the voice widget with a clean, finance-appropriate dark theme — navy/teal color palette
- [ ] GEM-036: Make the voice widget accessible — keyboard-navigable, ARIA labels, screen reader announcements
- [ ] GEM-037: Add a "Suggested Questions" panel with pre-loaded prompts: "What exceptions need my review?", "Summarize today's reconciliation run", "Show me unmatched transactions"
- [ ] GEM-038: Wire voice approval flow — when LedgerBot asks "Should I approve exception #47?", user can say "yes" and the exception is approved live

### PHASE 4: CLOUD RUN DEPLOYMENT (Day 2 Afternoon)

- [ ] GEM-039: Build Docker image for FastAPI backend with Gemini SDK included
- [ ] GEM-040: Push image to Artifact Registry
- [ ] GEM-041: Deploy FastAPI to Cloud Run (`ledgerlive-api`) with min-instances=1, max-instances=10, 2GB memory (WebSocket support requires min-instances=1)
- [ ] GEM-042: Configure Cloud Run to allow WebSocket connections (set `--session-affinity` flag)
- [ ] GEM-043: Deploy React frontend to Cloud Run or Firebase Hosting
- [ ] GEM-044: Set up Cloud Run environment variables via Secret Manager bindings
- [ ] GEM-045: Configure CORS in FastAPI to allow the frontend domain
- [ ] GEM-046: Set up a custom domain or use the auto-generated Cloud Run URL
- [ ] GEM-047: Run a full end-to-end test on the deployed Cloud Run instance
- [ ] GEM-048: Record the proof-of-deployment screen recording (Cloud Console logs + Cloud Run dashboard)
- [ ] GEM-049: Save proof recording to `hackathons/gemini/proof-of-deployment.mp4`

### PHASE 5: GEMINI SUBMISSION ASSETS

- [ ] GEM-050: Write `hackathons/gemini/description.md` — 500-word project description covering: problem, solution, tech used, Gemini Live API usage, Google Cloud services used, target users
- [ ] GEM-051: Write spin-up instructions specifically for judges in `hackathons/gemini/JUDGING.md`
- [ ] GEM-052: Finalize the 4-minute demo video (DEMO-006) showing: voice interaction → exception flagging → voice approval → audit trail update
- [ ] GEM-053: Upload architecture diagram (ARCH-004) to `hackathons/gemini/architecture.png`
- [ ] GEM-054: Create Devpost submission page for Gemini hackathon — fill all fields
- [ ] GEM-055: Submit before March 16 @ 4pm PDT (1 hour buffer)

### GEMINI BONUS POINT TASKS

- [ ] GEM-056: Write a Medium/Dev.to blog post: "How I Built a Voice-Enabled Finance Agent with Gemini Live API" — publish and link with #GeminiLiveAgentChallenge
- [ ] GEM-057: Sign up for a Google Developer Group at gdg.community.dev and get profile link
- [ ] GEM-058: Write infrastructure-as-code using `gcloud` CLI scripts or Terraform for automated Cloud Run deployment — include in repo
- [ ] GEM-059: Add the IaC deploy script to `hackathons/gemini/deploy.sh`

---

## HACKATHON 2: DIGITALOCEAN GRADIENT AI
> Deadline: March 18, 2026 @ 5pm EDT
> Prize: $20,000 ($8K first) + special prizes
> Mandatory: DigitalOcean Gradient AI full-stack features

### PHASE 1: DIGITALOCEAN ACCOUNT & PROJECT SETUP

- [ ] DO-001: Create/log into DigitalOcean account at the hackathon signup link
- [ ] DO-002: Create a new DigitalOcean project named `LedgerLive`
- [ ] DO-003: Familiarize with DigitalOcean Gradient AI documentation — read the getting started guide fully
- [ ] DO-004: Create a Gradient AI workspace
- [ ] DO-005: Note your DigitalOcean API token and store it in `.env` (never commit)
- [ ] DO-006: Install `doctl` (DigitalOcean CLI) and authenticate
- [ ] DO-007: Create a DigitalOcean Container Registry: `registry.digitalocean.com/ledgerlive`
- [ ] DO-008: Create a DigitalOcean Managed PostgreSQL cluster (cheapest tier, 1GB RAM) named `ledgerlive-db`
- [ ] DO-009: Get the Postgres connection string and store it in DigitalOcean environment variables
- [ ] DO-010: Enable DigitalOcean Spaces (object storage) for document storage — create bucket `ledgerlive-docs`

### PHASE 2: GRADIENT AI INTEGRATION

- [ ] DO-011: Identify which part of LedgerLive to power with Gradient AI — OCR/document extraction is the best fit (run a vision model on uploaded PDFs)
- [ ] DO-012: Browse available models on DigitalOcean Gradient AI model catalog — identify a suitable vision/OCR model (e.g., a fine-tuned document extraction model)
- [ ] DO-013: Create a Gradient AI inference endpoint for document OCR
- [ ] DO-014: Replace or augment the existing OCR logic in `apps/api/app/services/` with calls to the Gradient AI endpoint
- [ ] DO-015: Implement the Gradient AI API call in a new `apps/api/app/services/gradient_ai.py` module
- [ ] DO-016: Add retry logic and error handling for Gradient AI API calls (exponential backoff, max 3 retries)
- [ ] DO-017: Log Gradient AI inference latency and token usage to the structured logger
- [ ] DO-018: Test Gradient AI OCR on 3 different types of financial documents: invoice, bank statement, GL export
- [ ] DO-019: Compare accuracy of Gradient AI OCR vs previous OCR implementation — document results in `hackathons/digitalocean/gradient-ai-eval.md`
- [ ] DO-020: Add Gradient AI usage metrics to the Settings page in the frontend ("Documents processed via Gradient AI: N")

### PHASE 3: DATABASE MIGRATION TO POSTGRES

- [ ] DO-021: Update SQLAlchemy connection string to use Postgres (DATABASE_URL env var)
- [ ] DO-022: Run Alembic migrations against the DigitalOcean Managed Postgres instance
- [ ] DO-023: Test all CRUD operations against Postgres
- [ ] DO-024: Add a database connection pool (min 2, max 10) using SQLAlchemy
- [ ] DO-025: Write a `scripts/migrate_sqlite_to_postgres.py` script to migrate existing data

### PHASE 4: DIGITALOCEAN APP PLATFORM DEPLOYMENT

- [ ] DO-026: Write `.do/app.yaml` — DigitalOcean App Platform spec file defining the API service, web service, and database attachment
- [ ] DO-027: Configure the backend service in app.yaml: build from Dockerfile, set port 8090, set health check path `/health`
- [ ] DO-028: Configure the frontend service in app.yaml: build from Dockerfile or use static site build output
- [ ] DO-029: Link DigitalOcean Managed Postgres to the App Platform app via app.yaml
- [ ] DO-030: Deploy to App Platform via `doctl apps create --spec .do/app.yaml`
- [ ] DO-031: Set all environment variables in the App Platform dashboard (Gradient AI key, DB URL, etc.)
- [ ] DO-032: Verify the deployed app is accessible at the App Platform URL
- [ ] DO-033: Set up DigitalOcean Spaces for document uploads — update the backend to use Spaces instead of local filesystem
- [ ] DO-034: Implement `apps/api/app/services/spaces.py` — upload/download/delete documents from DigitalOcean Spaces
- [ ] DO-035: Update document ingestion pipeline to store PDFs in Spaces and reference them by URL in the DB

### PHASE 5: SPECIAL PRIZE TARGETING

- [ ] DO-036: **Best AI Agent Persona** — give LedgerBot a name, avatar, and distinct personality in the UI. Add a "Meet LedgerBot" onboarding modal
- [ ] DO-037: Add LedgerBot persona copy: tone is "precise, proactive, never alarming" — write 20 varied response templates
- [ ] DO-038: Add a LedgerBot avatar SVG icon to the frontend (a small robot holding a balance sheet)
- [ ] DO-039: **Best Program for the People** — add a "Small Business Mode" that simplifies the UI and uses plain-English labels instead of accounting jargon. Add a landing page section explaining how LedgerLive helps small business owners who can't afford a CFO
- [ ] DO-040: Write a compelling "impact" section for the Devpost description: "LedgerLive democratizes financial close automation, a process that previously cost $50K+/year in consulting fees"

### PHASE 6: DIGITALOCEAN SUBMISSION ASSETS

- [ ] DO-041: Ensure repo has MIT LICENSE file (FOUND-001) — required for judging
- [ ] DO-042: Write `hackathons/digitalocean/description.md` — detailed description of Gradient AI usage, architecture, and impact
- [ ] DO-043: Write spin-up instructions for judges in `hackathons/digitalocean/JUDGING.md` (must be reproducible from scratch)
- [ ] DO-044: Finalize the 3-minute demo video (DEMO-005) showing Gradient AI inference in action on a real document
- [ ] DO-045: Upload architecture diagram (ARCH-005) to `hackathons/digitalocean/architecture.png`
- [ ] DO-046: Create Devpost submission page for DigitalOcean hackathon
- [ ] DO-047: Add optional live demo URL to Devpost (the deployed App Platform URL)
- [ ] DO-048: Submit before March 18 @ 4pm EDT (1 hour buffer)

---

## HACKATHON 3: AIRIA AI AGENTS
> Deadline: March 19, 2026 @ 11:45pm EDT
> Prize: $7,000 | Track: Active Agents (recommended)
> Mandatory: Must use Airia platform AND publish to Airia Community

### PHASE 1: AIRIA PLATFORM ONBOARDING

- [ ] AIR-001: Sign up for Airia account at airia.com
- [ ] AIR-002: Complete the Airia onboarding — create workspace, verify email
- [ ] AIR-003: Read the Airia documentation fully: agent creation, community publishing, API integration
- [ ] AIR-004: Create an Airia API key and store in `.env`
- [ ] AIR-005: Explore the Airia Community to understand how top agents are structured and described
- [ ] AIR-006: Install Airia SDK or identify the API endpoint structure for custom agent creation
- [ ] AIR-007: Create a test "hello world" agent in Airia to verify your account is working
- [ ] AIR-008: Read the Airia Hackathon resources page for any specific integration patterns required

### PHASE 2: MULTI-AGENT ARCHITECTURE DESIGN

- [ ] AIR-009: Design the 4-agent architecture: IngestionAgent, ReconciliationAgent, ExceptionTriageAgent, HITLCoordinatorAgent
- [ ] AIR-010: Define the message/event contract between agents (JSON schema for inter-agent communication)
- [ ] AIR-011: Document which agent "owns" which data and which triggers which
- [ ] AIR-012: Design the human-in-the-loop moment: ExceptionTriageAgent flags an item → HITLCoordinatorAgent surfaces it to a human → human approves/rejects → result flows back
- [ ] AIR-013: Draw the multi-agent architecture diagram (ARCH-006)
- [ ] AIR-014: Decide the external system integrations — at minimum 2 systems beyond the LedgerLive DB. Options: Google Drive (document source), Slack (HITL notifications), QuickBooks mock API (GL data)

### PHASE 3: AGENT IMPLEMENTATION IN AIRIA

- [ ] AIR-015: Create `IngestionAgent` in Airia — triggers when a new document is uploaded to Google Drive folder (or webhook), downloads PDF, calls LedgerLive OCR endpoint, stores result
- [ ] AIR-016: Create `ReconciliationAgent` in Airia — triggers after IngestionAgent completes, calls LedgerLive reconciliation API, logs results
- [ ] AIR-017: Create `ExceptionTriageAgent` in Airia — reads reconciliation output, classifies each exception by type and severity (using an LLM prompt), assigns priority score
- [ ] AIR-018: Create `HITLCoordinatorAgent` in Airia — for high-severity exceptions, posts a structured Slack message with approve/reject buttons; listens for Slack interaction callback; routes response back to LedgerLive API
- [ ] AIR-019: Wire all 4 agents into an Airia Flow — define the trigger → chain → human gate → resolution sequence
- [ ] AIR-020: Add error handling to each agent: if any step fails, log to Airia and send a Slack alert
- [ ] AIR-021: Add retry logic to IngestionAgent for flaky document sources
- [ ] AIR-022: Test the full 4-agent flow with the demo dataset (DEMO-002)
- [ ] AIR-023: Add a nested agent architecture: ExceptionTriageAgent spawns sub-agents for different exception types (AmountMismatch sub-agent, MissingDocument sub-agent, DateRangeError sub-agent)
- [ ] AIR-024: Implement dynamic document generation: HITLCoordinatorAgent generates a formatted PDF exception report before sending to human reviewer
- [ ] AIR-025: Add cross-platform workflow: after HITL approval, trigger a Google Sheets update logging the resolution

### PHASE 4: AIRIA COMMUNITY PUBLISHING

- [ ] AIR-026: Navigate to Airia Community → Share Agent
- [ ] AIR-027: Publish `LedgerLive Close Agent` to the Airia Community with a compelling name, description, and tags: finance, reconciliation, multi-agent, HITL, enterprise, accounting
- [ ] AIR-028: Set agent visibility to Public
- [ ] AIR-029: Add a detailed agent description: what it does, how to configure it, what integrations it requires
- [ ] AIR-030: Add usage examples to the Airia Community listing
- [ ] AIR-031: Copy the Community URL and save it to `hackathons/airia/community-url.txt`
- [ ] AIR-032: Verify the community listing is publicly accessible from a logged-out browser

### PHASE 5: AIRIA SUBMISSION ASSETS

- [ ] AIR-033: Write `hackathons/airia/description.md` — emphasize enterprise impact, multi-agent orchestration, HITL decision points, and cross-system integrations
- [ ] AIR-034: Finalize the 4-minute demo video (DEMO-004) showing the full 4-agent flow, HITL Slack notification, and audit trail
- [ ] AIR-035: Upload architecture diagram (ARCH-006) to `hackathons/airia/architecture.png`
- [ ] AIR-036: Create Devpost submission page for Airia hackathon — include Airia Community URL in the submission
- [ ] AIR-037: Fill in all required Devpost fields: agent name, problem statement, solution overview, key features, technologies, target users
- [ ] AIR-038: Submit before March 19 @ 10pm EDT (2 hour buffer)

### AIRIA JUDGING CRITERIA ALIGNMENT

- [ ] AIR-039: **Technological Implementation** — add a `hackathons/airia/tech-notes.md` explaining how Airia tools/triggers/context are used. Be specific about which Airia features are leveraged
- [ ] AIR-040: **Design** — ensure the frontend has a polished UI. Add a "Multi-Agent Status Panel" showing which agent is currently active and what it last did
- [ ] AIR-041: **Potential Impact** — add a "Business Case" section to the Devpost description quantifying impact: time saved, error reduction rate, cost savings vs manual close process
- [ ] AIR-042: **Quality of Idea** — differentiate from competitors: emphasize the nested agent pattern and the dynamic HITL document generation as novel elements

---

## HACKATHON 4: GITLAB AI HACKATHON
> Deadline: March 25, 2026 @ 2pm EDT — Most time available
> Prize: $65,000 ($15K grand) + $13,500 Anthropic bonus + $13,500 Google Cloud bonus
> Mandatory: GitLab Duo Agent Platform, custom agent or flow, public GitLab repo

### PHASE 1: GITLAB DUO AGENT PLATFORM ONBOARDING

- [ ] GL-001: Join the GitLab AI Hackathon Discord at discord.com/invite/gitlab, find #ai-hackathon
- [ ] GL-002: Request access to the GitLab AI Hackathon group at the Google Forms link on the hackathon page
- [ ] GL-003: Read the "GitLab Duo Agent Platform Complete Getting Started Guide" fully
- [ ] GL-004: Complete the interactive demo for creating GitLab custom Agents (Navattic link)
- [ ] GL-005: Complete the interactive demo for creating GitLab Flows (Navattic link)
- [ ] GL-006: Explore the GitLab Duo prompt library for inspiration
- [ ] GL-007: Create a new GitLab repository under the GitLab AI Hackathon group (required for submission)
- [ ] GL-008: Mirror or copy the LedgerLive codebase to this GitLab repository
- [ ] GL-009: Add MIT LICENSE to the GitLab repo (must be detectable in Project Information section)
- [ ] GL-010: Verify the repo is public and visible to judges

### PHASE 2: CONCEPT — THE LEDGERLIVE COMPLIANCE AGENT

The GitLab angle: LedgerLive's financial configuration lives in code (e.g., reconciliation rules, chart of accounts mappings, threshold configs). Any merge request that changes these files has compliance implications. The LedgerLive Compliance Agent monitors GitLab merge requests, automatically runs compliance checks, generates audit evidence, and flags changes that require CFO review — all without leaving GitLab.

- [ ] GL-011: Define the agent's trigger: any MR touching `config/reconciliation_rules.yaml`, `config/accounts.yaml`, or `config/thresholds.yaml`
- [ ] GL-012: Design the agent workflow: MR opened → agent triggered → run compliance check → post structured comment → if high-risk, require human approval → on merge, auto-generate audit artifact
- [ ] GL-013: Define what "compliance check" means: detect changes that widen matching tolerances (risk), changes that modify account mappings, changes that disable exception flags
- [ ] GL-014: Design the audit artifact: a signed markdown file with the diff, the compliance check results, the approver's name, and a timestamp — committed to a `audit-trail/` branch automatically on merge

### PHASE 3: BUILD THE GITLAB DUO AGENT

- [ ] GL-015: Create the `LedgerLive Compliance Checker` custom agent in GitLab Duo Agent Platform
- [ ] GL-016: Define agent context: access to the MR diff, the changed files, the MR author, and the project config
- [ ] GL-017: Define agent tools: `get_mr_diff()`, `parse_config_change()`, `run_compliance_rules()`, `post_mr_comment()`, `request_human_approval()`, `generate_audit_artifact()`, `commit_file_to_branch()`
- [ ] GL-018: Write the compliance rule engine in Python: `tools/compliance/check_rules.py` — takes a config diff and returns a list of findings with severity (LOW/MEDIUM/HIGH/CRITICAL)
- [ ] GL-019: Define at least 10 compliance rules, e.g.: "Increasing a reconciliation tolerance by >10% is HIGH risk", "Disabling any exception flag is CRITICAL", "Changing an account code mapping requires CFO approval"
- [ ] GL-020: Implement `post_mr_comment()` — formats the compliance findings as a structured GitLab MR comment with emoji severity indicators, a summary table, and next steps
- [ ] GL-021: Implement `request_human_approval()` — adds the CFO as a required approver on the MR if any HIGH or CRITICAL finding exists
- [ ] GL-022: Implement `generate_audit_artifact()` — creates a markdown audit record containing: MR URL, author, changed files, compliance findings, approver, timestamp, SHA hash of the config files
- [ ] GL-023: Implement `commit_file_to_branch()` — programmatically commits the audit artifact to `audit-trail/YYYY-MM-DD-MR-{id}.md` on merge
- [ ] GL-024: Wire all tools into a GitLab Flow: trigger → agent invocation → tool chain → human gate (if needed) → post-merge action
- [ ] GL-025: Test the flow with a mock MR changing a threshold config
- [ ] GL-026: Test the "happy path" (low-risk change, no approval needed, audit artifact committed)
- [ ] GL-027: Test the "escalation path" (critical change, CFO added as required approver, blocked until approved)
- [ ] GL-028: Test error handling: what happens if the compliance check fails, if the commit fails, etc.

### PHASE 4: ANTHROPIC BONUS INTEGRATION ($13,500)

- [ ] GL-029: Route the compliance analysis LLM call through Anthropic (Claude) via the GitLab platform
- [ ] GL-030: Write the system prompt for Claude: "You are a financial compliance expert reviewing a configuration change to a finance automation system. Analyze the diff for compliance risks, regulatory implications, and segregation-of-duties concerns."
- [ ] GL-031: Write the user prompt template that includes the full config diff and asks Claude to produce a structured compliance report
- [ ] GL-032: Parse Claude's response and map it to the compliance findings schema
- [ ] GL-033: Add the Anthropic integration to `hackathons/gitlab/anthropic-integration.md` — document exactly how Claude is invoked through GitLab
- [ ] GL-034: In the Devpost submission, explicitly call out the Anthropic integration as a separate section to qualify for the bonus prize

### PHASE 5: GOOGLE CLOUD BONUS INTEGRATION ($13,500)

- [ ] GL-035: Deploy the LedgerLive compliance check runner as a Google Cloud Function (serverless)
- [ ] GL-036: Configure the GitLab webhook to trigger the Cloud Function on MR events
- [ ] GL-037: Use Vertex AI (Gemini) for a secondary compliance analysis pass — compare with Anthropic results
- [ ] GL-038: Store audit artifacts in Google Cloud Storage bucket `ledgerlive-audit-trail`
- [ ] GL-039: Add Cloud Function deployment script to `hackathons/gitlab/deploy-cloud-function.sh`
- [ ] GL-040: In the Devpost submission, explicitly call out the Google Cloud integration as a separate section to qualify for the bonus prize

### PHASE 6: GREEN AGENT PRIZE ($3,000)

- [ ] GL-041: Research what "Green Agents" means in the context of the GitLab hackathon — check the resources tab
- [ ] GL-042: Add energy efficiency tracking to the agent: log token usage per run, estimate CO2 equivalent
- [ ] GL-043: Implement a "minimal inference" mode that uses a smaller/faster model for low-risk changes and reserves the full Claude call for HIGH/CRITICAL changes only
- [ ] GL-044: Document the energy efficiency design in `hackathons/gitlab/green-agent.md`
- [ ] GL-045: Add a badge to the GitLab README: "This agent is carbon-aware — inference is tiered by risk level"

### PHASE 7: GITLAB SUBMISSION ASSETS

- [ ] GL-046: Write the full project description in `hackathons/gitlab/description.md` — cover: the problem (compliance risk in financial config changes), the solution, the agent architecture, Duo Agent Platform usage, Anthropic integration, Google Cloud integration
- [ ] GL-047: Write spin-up instructions for judges in `hackathons/gitlab/JUDGING.md`
- [ ] GL-048: Finalize the 3-minute demo video (DEMO-007) showing: an MR being opened → agent triggered → compliance report posted → CFO approval requested → merge → audit artifact committed
- [ ] GL-049: Upload architecture diagram (ARCH-007) to `hackathons/gitlab/architecture.png`
- [ ] GL-050: Create the Devpost submission page — link to the GitLab AI Hackathon group repo (not the GitHub repo)
- [ ] GL-051: Verify the GitLab repo is in the correct GitLab AI Hackathon group (see the example link on the hackathon page)
- [ ] GL-052: Submit before March 25 @ 1pm EDT (1 hour buffer)

---

## DEVPOST SUBMISSION QUALITY TASKS
> For ALL four hackathons — these make the difference between placing and winning

- [ ] SUB-001: Write a compelling one-liner for each submission that judges see first — test it on someone who has never heard of LedgerLive
- [ ] SUB-002: For each Devpost submission, write the "Problem Statement" in 2-3 sentences — make the pain visceral ("Finance teams spend 40+ hours per quarter on manual close reconciliation, during which errors cost companies an average of $300K")
- [ ] SUB-003: For each submission, write the "Solution Overview" in 3-4 sentences — focus on what changed because of the AI agent, not the features list
- [ ] SUB-004: For each submission, write the "Technologies Used" section — list every API, framework, platform, and tool (judges want depth here)
- [ ] SUB-005: For each submission, write the "Target Users" section — be specific (e.g., "Controller at a Series B SaaS company, managing 3-5 direct reports in accounting")
- [ ] SUB-006: Upload at least 3 screenshots per Devpost submission (dashboard, exception view, audit log)
- [ ] SUB-007: Upload the architecture diagram as an image to each Devpost submission
- [ ] SUB-008: Add the GitHub (or GitLab) repo URL to each Devpost submission
- [ ] SUB-009: Fill in the "What challenges did you face?" field honestly — judges respect authenticity
- [ ] SUB-010: Fill in the "What did you learn?" field — shows intellectual growth
- [ ] SUB-011: Fill in the "What's next for LedgerLive?" field — shows ambition and market thinking
- [ ] SUB-012: Proofread every Devpost submission for typos and grammatical errors
- [ ] SUB-013: Have someone else read each submission before final submit — outside perspective is invaluable
- [ ] SUB-014: Ensure each video starts with the problem statement (30 seconds max), not with setup or code
- [ ] SUB-015: Each video must show the software actually working — no slideshows, no mockups, no "coming soon" screens
- [ ] SUB-016: Add a watermark or title card to each video with the project name and hackathon name
- [ ] SUB-017: Speak clearly and slowly in the demo videos — judges watch many videos and appreciate clear narration
- [ ] SUB-018: End each demo video with a clear "call to action" or "next steps" to show vision

---

## FRONTEND & UX IMPROVEMENTS
> Applies across all hackathons — better UI = better scores on Design criteria

- [ ] UX-001: Add a proper loading skeleton to the Dashboard while data loads (no more blank states)
- [ ] UX-002: Add empty state illustrations for each section (no transactions, no exceptions, etc.) with a clear call to action
- [ ] UX-003: Add a global notification/toast system for success, error, and info messages
- [ ] UX-004: Add a confirmation modal for all destructive or approval actions
- [ ] UX-005: Add keyboard shortcuts: `R` for refresh, `A` for approve (when in exception review), `Esc` to close modals
- [ ] UX-006: Add a global search bar that searches across transactions, documents, and exceptions
- [ ] UX-007: Add a dark mode toggle and persist preference in localStorage
- [ ] UX-008: Make the dashboard responsive for mobile (currently broken per test-10 screenshot)
- [ ] UX-009: Add a "Recent Activity" feed to the dashboard showing the last 10 agent actions
- [ ] UX-010: Add visual diff highlighting to the reconciliation view — show matched/unmatched transactions side by side with color coding
- [ ] UX-011: Add a progress indicator to the document ingestion pipeline (upload → OCR → extraction → stored)
- [ ] UX-012: Add pagination to all list views (transactions, exceptions, audit log) — currently missing
- [ ] UX-013: Add sortable and filterable columns to the transactions table
- [ ] UX-014: Add a date range picker to filter all views by time period
- [ ] UX-015: Add export buttons (CSV, PDF) to the exceptions view and audit log
- [ ] UX-016: Improve the Race Control page — add a real-time refresh mechanism (polling or WebSocket)
- [ ] UX-017: Add a "Help & Docs" section with 5 guided walkthroughs
- [ ] UX-018: Add an onboarding flow for new users: 4-step wizard connecting their first document source
- [ ] UX-019: Add a "System Status" indicator in the header showing agent health (running / idle / error)
- [ ] UX-020: Add breadcrumb navigation to all deep-linked pages
- [ ] UX-021: Improve the 404 page — make it branded and add a "go home" button (the existing 404 fix looks basic)
- [ ] UX-022: Add an accessibility audit using `axe-core` and fix all critical issues
- [ ] UX-023: Add a "Multi-Agent Dashboard" page showing all 4 agents' status, last run time, and last action
- [ ] UX-024: Add a timeline/Gantt view of a close cycle showing which agents ran when
- [ ] UX-025: Add a financial summary widget to the dashboard: total docs processed, reconciliation rate (%), open exceptions, SLA status

---

## BACKEND & API IMPROVEMENTS

- [ ] API-001: Add JWT-based authentication to all FastAPI routes
- [ ] API-002: Add a `/api/v1/` prefix to all routes for proper versioning
- [ ] API-003: Add response pagination to all list endpoints (offset, limit, total)
- [ ] API-004: Add filtering query parameters to transactions endpoint (`?status=unmatched&date_from=2026-01-01`)
- [ ] API-005: Add a `POST /api/v1/documents/upload` endpoint that accepts multipart file uploads
- [ ] API-006: Add a `GET /api/v1/reconciliation/runs` endpoint listing all reconciliation run history
- [ ] API-007: Add a `POST /api/v1/reconciliation/trigger` endpoint to manually trigger a reconciliation run
- [ ] API-008: Add a `GET /api/v1/audit-log/export` endpoint that returns a signed PDF audit binder
- [ ] API-009: Add a `GET /api/v1/metrics` endpoint with Prometheus-format metrics for agent runs, latency, error rates
- [ ] API-010: Add rate limiting using `slowapi` — 100 requests/minute per IP
- [ ] API-011: Add request/response logging middleware that logs method, path, status code, and latency
- [ ] API-012: Add an `X-Request-ID` header to all responses for tracing
- [ ] API-013: Add OpenAPI documentation enhancements — add example request/response bodies to all endpoints
- [ ] API-014: Add a `WebSocket /ws/agent-events` endpoint that streams real-time agent status updates to the frontend
- [ ] API-015: Implement background tasks using FastAPI's `BackgroundTasks` for long-running reconciliation runs
- [ ] API-016: Add a task queue using Redis + Celery (or simply asyncio) for the document ingestion pipeline
- [ ] API-017: Add a `GET /api/v1/health/deep` endpoint that checks DB connectivity, external API connectivity, and disk space
- [ ] API-018: Implement proper HTTP exception handlers with structured error responses (`{"error": "...", "code": "...", "trace_id": "..."}`)
- [ ] API-019: Add CORS configuration that restricts origins in production
- [ ] API-020: Add request body validation using Pydantic v2 models for all POST/PUT endpoints

---

## TESTING & QUALITY ASSURANCE

- [ ] TEST-001: Achieve 80% code coverage on Python backend
- [ ] TEST-002: Write unit tests for all reconciliation matching algorithms
- [ ] TEST-003: Write unit tests for all exception classification logic
- [ ] TEST-004: Write unit tests for the audit trail generation
- [ ] TEST-005: Write integration tests for the document upload → OCR → extraction pipeline
- [ ] TEST-006: Write integration tests for the reconciliation trigger → exception creation flow
- [ ] TEST-007: Write integration tests for the HITL approval flow
- [ ] TEST-008: Write end-to-end Playwright tests for the happy-path close cycle
- [ ] TEST-009: Write Playwright tests for the exception review and approval flow
- [ ] TEST-010: Write Playwright tests for the audit log view
- [ ] TEST-011: Set up GitHub Actions CI that runs all tests on every push
- [ ] TEST-012: Add a code coverage badge to the README
- [ ] TEST-013: Set up GitHub Actions to run the linters on every PR
- [ ] TEST-014: Add a security scan using `bandit` for the Python backend
- [ ] TEST-015: Add a dependency vulnerability scan using `pip-audit` in CI

---

## DOCUMENTATION

- [ ] DOC-001: Write a full API reference in `docs/api-reference.md` — one section per endpoint
- [ ] DOC-002: Write a "How It Works" deep-dive in `docs/how-it-works.md` explaining the reconciliation algorithm
- [ ] DOC-003: Write a "Agent Architecture" guide in `docs/agent-architecture.md`
- [ ] DOC-004: Write a "Deployment Guide" in `docs/deployment.md` covering: local, Docker, Cloud Run, DigitalOcean App Platform
- [ ] DOC-005: Write a "Configuration Reference" in `docs/configuration.md` listing all environment variables and their meaning
- [ ] DOC-006: Write a "Security Guide" in `docs/security.md` covering: auth, secrets management, audit trail tamper-evidence
- [ ] DOC-007: Write a "FAQ" in `docs/faq.md` with 10 questions/answers a judge might ask
- [ ] DOC-008: Add inline comments to all complex reconciliation logic functions
- [ ] DOC-009: Write a glossary of finance terms used in the app in `docs/glossary.md`
- [ ] DOC-010: Write a "Why LedgerLive?" one-pager in `hackathons/one-pager.md` that can be used as a pitch document

---

## FINAL SUBMISSION CHECKLIST

### Gemini (March 16)
- [ ] FINAL-GEM-001: Gemini Live API integrated and working on deployed app
- [ ] FINAL-GEM-002: Backend deployed to Cloud Run with proof screenshot
- [ ] FINAL-GEM-003: Architecture diagram uploaded to Devpost
- [ ] FINAL-GEM-004: 4-minute demo video uploaded to YouTube
- [ ] FINAL-GEM-005: Devpost submission fully filled and submitted

### DigitalOcean (March 18)
- [ ] FINAL-DO-001: Gradient AI inference endpoint integrated and working
- [ ] FINAL-DO-002: App deployed to DigitalOcean App Platform
- [ ] FINAL-DO-003: Open-source LICENSE file present and detectable
- [ ] FINAL-DO-004: 3-minute demo video uploaded
- [ ] FINAL-DO-005: Devpost submission fully filled and submitted

### Airia (March 19)
- [ ] FINAL-AIR-001: All 4 agents created and working in Airia
- [ ] FINAL-AIR-002: Agent published to Airia Community (Public)
- [ ] FINAL-AIR-003: Airia Community URL saved and included in Devpost submission
- [ ] FINAL-AIR-004: 4-minute demo video uploaded
- [ ] FINAL-AIR-005: Devpost submission fully filled and submitted

### GitLab (March 25)
- [ ] FINAL-GL-001: GitLab Duo Agent created and published in Hackathon group
- [ ] FINAL-GL-002: Anthropic integration working and documented
- [ ] FINAL-GL-003: Google Cloud integration working and documented
- [ ] FINAL-GL-004: GitLab repo is public with MIT LICENSE detectable
- [ ] FINAL-GL-005: 3-minute demo video uploaded
- [ ] FINAL-GL-006: Devpost submission fully filled and submitted

---

## TASK COUNT SUMMARY

| Category | Tasks |
|----------|-------|
| Cross-cutting Foundation | 50 |
| Gemini Hackathon | 59 |
| DigitalOcean Hackathon | 48 |
| Airia Hackathon | 42 |
| GitLab Hackathon | 52 |
| Devpost Submission Quality | 18 |
| Frontend & UX | 25 |
| Backend & API | 20 |
| Testing & QA | 15 |
| Documentation | 10 |
| Final Checklists | 20 |
| **TOTAL** | **409 unique tasks** |

> Note: This list is intentionally exhaustive. Not every task is required to win — but every task here directly improves your chances. Prioritize ruthlessly based on deadline order. The tasks marked in each hackathon's Phase 1 are always the highest priority to unblock everything else.

---

*Generated March 13, 2026 — LedgerLive Multi-Hackathon Strategy*
