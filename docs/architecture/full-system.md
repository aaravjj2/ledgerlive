# LedgerLive — Full System Architecture

```mermaid
graph TB
    subgraph "Frontend Layer"
        WEB["React 18 SPA<br/>Vite + Tailwind CSS"]
        VOICE["Voice Assistant UI<br/>WebSocket + Web Audio API"]
    end

    subgraph "API Layer"
        API["FastAPI Backend<br/>Python 3.12 | Port 8090"]
        WS["WebSocket Server<br/>/ws/voice | /ws/agent-events"]
        AUDIT["Audit Event Spine<br/>Append-only log"]
    end

    subgraph "AI/ML Layer"
        GEMINI["Gemini Live API<br/>Voice + Tool Calling"]
        GRADIENT["Gradient AI<br/>Document OCR"]
        AIRIA["Airia Platform<br/>Agent Orchestration"]
        COMPLIANCE["Compliance Engine<br/>10 Rules | Tiered Inference"]
    end

    subgraph "Data Layer"
        DB[("SQLite / PostgreSQL")]
        SPACES["DigitalOcean Spaces<br/>Document Storage"]
    end

    subgraph "Deployment"
        CR["Google Cloud Run"]
        DO["DigitalOcean App Platform"]
        DOCKER["Docker Compose"]
    end

    WEB --> API
    VOICE --> WS
    WS --> GEMINI
    API --> DB
    API --> GRADIENT
    API --> AIRIA
    API --> SPACES
    API --> AUDIT
    COMPLIANCE --> API
    API --> CR
    API --> DO
    API --> DOCKER
```

## Component Details

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Frontend | React 18 + Vite + Tailwind | SPA dashboard with 113+ pages |
| Voice UI | Web Audio API + WebSocket | Real-time audio capture/playback |
| Backend API | FastAPI (340+ wave routers) | Business logic + API endpoints |
| Gemini Live | Google GenAI SDK | Voice interaction + tool calling |
| Gradient AI | DigitalOcean API | GPU-backed document OCR |
| Airia | MCP Tools + Webhooks | Multi-agent orchestration |
| Compliance | Regex + Claude/Gemini | GitLab MR compliance checking |
| Database | SQLite (dev) / PostgreSQL (prod) | Transaction/document storage |
| Spaces | S3-compatible object storage | Document file storage |
