/**
 * LedgerLive constants — project identity, hackathon tags, API paths.
 */

export const PROJECT_ID = 'LEDGERLIVE'

export const HACKATHON_TAGS = {
  gemini: '#GeminiLiveAgentChallenge',
  digitalOcean: '#GradientAIHackathon',
  airia: '#AiriaAgents',
} as const

export const API_PATHS = {
  health: '/healthz',
  audit: '/api/audit',
  documents: '/api/documents',
  reconciliations: '/api/reconciliations',
  exceptions: '/api/exceptions',
  reviews: '/api/reviews',
  raceControl: '/api/race-control',
  laneStatus: '/api/lane-status',
  incidentLog: '/api/incident-log',
  liveScoreboard: '/api/live-scoreboard',
  closeCheckpoint: '/api/close-checkpoint',
  rcApproval: '/api/rc-approval',
  raceWeekendStages: '/api/race-weekend/stages',
  cfoCockpit: '/api/cfo/cockpit',
  cfoScenario: '/api/cfo/scenario',
  agentAsk: '/api/agent/ask',
  agentCycle: '/api/agent/cycle',
  goldenScenarioRun: '/api/ops/golden-scenario-run',
  telemetryPack: '/api/ops/export/telemetry-pack',
  courtPack: '/api/ops/export/court-pack',
  mcpTools: '/api/mcp/tools',
  airiaStatus: '/api/airia/status',
  airiaCompat: '/api/airia/compat_report',
} as const
