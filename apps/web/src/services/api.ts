/**
 * LedgerLive API client — typed fetch wrappers for all backend endpoints.
 * PROJECT_ID: LEDGERLIVE
 */

// In development, Vite proxies /api to localhost:8090.
// In production, VITE_API_URL should point to the deployed API.
const API_BASE = (import.meta as { env?: { VITE_API_URL?: string } }).env?.VITE_API_URL || 'https://ledgerlive-api-production.up.railway.app'
const BASE = API_BASE.replace(/\/$/, '')

// Export for use in pages that use raw fetch() instead of typed wrappers
export { API_BASE }

export interface ApiResponse<T> {
  items?: T[]
  total?: number
  [key: string]: unknown
}

export async function apiGet<T>(path: string): Promise<T> {
  const r = await fetch(`${BASE}${path}`)
  if (!r.ok) throw new Error(`API ${r.status}: ${path}`)
  return r.json()
}

export async function apiPost<T>(path: string, body?: unknown): Promise<T> {
  const r = await fetch(`${BASE}${path}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: body ? JSON.stringify(body) : undefined,
  })
  if (!r.ok) throw new Error(`API ${r.status}: ${path}`)
  return r.json()
}

export async function apiDelete(path: string): Promise<void> {
  const r = await fetch(`${BASE}${path}`, { method: 'DELETE' })
  if (!r.ok) throw new Error(`API ${r.status}: ${path}`)
}

// ── Health ─────────────────────────────────────────────────────────────
export async function getHealth() {
  return apiGet<{ project: string; status: string; mode: string; llm: string; ts: string }>('/healthz')
}

// ── Documents ───────────────────────────────────────────────────────────
export async function getDocuments() {
  return apiGet<ApiResponse<{ doc_id: string; doc_name?: string; filename?: string; doc_type?: string; status?: string }>>('/api/documents')
}

// ── Reconciliations ─────────────────────────────────────────────────────
export async function getReconciliations() {
  return apiGet<ApiResponse<{ recon_id: string; recon_name?: string; status?: string; matched_count?: number; unmatched_count?: number }>>('/api/reconciliations')
}

export async function approveReconciliation(id: string) {
  return apiPost(`/api/reconciliations/${id}/approve`, {})
}

// ── Exceptions ──────────────────────────────────────────────────────────
export async function getExceptions() {
  return apiGet<ApiResponse<{ exception_id: string; severity?: string; status?: string; description?: string }>>('/api/exceptions')
}

export async function resolveException(id: string) {
  return apiPost(`/api/exceptions/${id}/resolve`, {})
}

// ── CFO Cockpit ─────────────────────────────────────────────────────────
export async function getCfoCockpit() {
  return apiGet<{ metrics: Record<string, number>; lanes: unknown[] }>('/api/cfo/cockpit')
}

export async function getCfoScenario() {
  return apiGet<{ scenario_id: string; pack: unknown }>('/api/cfo/scenario')
}

// ── Agent ───────────────────────────────────────────────────────────────
export async function agentAsk(query: string) {
  return apiPost<{ answer: string; trace_id?: string }>('/api/agent/ask', { query })
}

export async function agentCycle() {
  return apiPost<{ cycle_id: string; status: string }>('/api/agent/cycle', {})
}

export async function getAgentCycles() {
  return apiGet<ApiResponse<{ cycle_id: string; status: string; ts: string }>>('/api/agent/cycles')
}

// ── Race Control ────────────────────────────────────────────────────────
export async function getLaneStatus() {
  return apiGet<ApiResponse<{ lane_id: string; lane_name: string; completion_pct: number; blocked_count: number }>>('/api/lane-status')
}

export async function getIncidentLog() {
  return apiGet<ApiResponse<{ incident_id: string; incident_title: string; severity: string; status: string }>>('/api/incident-log')
}

export async function runGoldenScenario() {
  return apiPost<{ status: string }>('/api/ops/golden-scenario-run', {})
}

// ── Race Weekend ────────────────────────────────────────────────────────
export async function getRaceWeekendStages() {
  return apiGet<{ stages: unknown[]; safety_car_active: boolean; lap_count: number }>('/api/race-weekend/stages')
}

// ── OCR ────────────────────────────────────────────────────────────────
export async function getOcrJobs() {
  return apiGet<ApiResponse<{ ocr_id: string; status?: string; doc_id?: string }>>('/api/ocr-jobs')
}

export async function getOcrStats() {
  return apiGet<{ total: number; completed: number; pending: number }>('/api/ocr-jobs/stats')
}

// ── Close Period ───────────────────────────────────────────────────────
export async function getClosePeriods() {
  return apiGet<ApiResponse<{ period_id: string; period_name?: string; status?: string }>>('/api/close-periods')
}

// ── Connectors ──────────────────────────────────────────────────────────
export async function getConnectors() {
  return apiGet<ApiResponse<{ connector_id: string; connector_type?: string; status?: string }>>('/api/connectors')
}
