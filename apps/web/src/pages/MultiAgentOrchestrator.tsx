/**
 * Multi-Agent Orchestrator — Airia AI Agents Hackathon (Track 2: Active Agents)
 * Orchestrate intelligence across 2+ systems. HITL, nested agents, document generation.
 */
import { useEffect, useState, useCallback } from 'react'
import { apiGet } from '../services/api'

interface AgentNode {
  agent_id: string
  name: string
  status: string
  system: string
  hitl_pending: boolean
}

interface WorkflowRun {
  run_id: string
  agents_invoked: number
  systems_touched: string[]
  hitl_count: number
  status: string
  started_at: string
}

export default function MultiAgentOrchestrator() {
  const [agents, setAgents] = useState<AgentNode[]>([])
  const [runs, setRuns] = useState<WorkflowRun[]>([])
  const [loading, setLoading] = useState(true)

  const load = useCallback(async () => {
    setLoading(true)
    try {
      const [a, r] = await Promise.all([
        apiGet<{ items?: AgentNode[] }>('/api/close-orchestrator/agents').catch(() => ({ items: [] })),
        apiGet<{ items?: WorkflowRun[] }>('/api/close-orchestrator/runs').catch(() => ({ items: [] })),
      ])
      setAgents(a?.items ?? [])
      setRuns(r?.items ?? [])
    } catch {
      setAgents([])
      setRuns([])
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => { load() }, [load])

  return (
    <div data-testid="multi-agent-orchestrator" className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold" data-testid="orchestrator-title">Multi-Agent Orchestrator</h1>
          <p className="text-gray-500 text-sm mt-1">
            Active Agents — Orchestrate intelligence across 2+ systems. HITL, nested agents, document generation.
          </p>
        </div>
        <button
          onClick={load}
          disabled={loading}
          className="px-4 py-2 bg-indigo-600 text-white rounded-lg text-sm font-medium hover:bg-indigo-700 disabled:opacity-50"
        >
          {loading ? 'Loading…' : '↻ Refresh'}
        </button>
      </div>

      <div className="rounded-xl border bg-emerald-50 border-emerald-200 p-4">
        <h3 className="font-semibold text-emerald-800 mb-2">Track 2: Active Agents</h3>
        <p className="text-sm text-emerald-700">
          LedgerLive close orchestrator runs multi-agent workflows: ingest → reconcile → triage → HITL review → close.
          Agents touch documents, reconciliations, exceptions, approvals — 2+ systems. Human-in-the-loop gates ensure fail-closed safety.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="rounded-xl border bg-white p-4">
          <h2 className="font-semibold mb-3">Agent Nodes</h2>
          {agents.length === 0 ? (
            <div className="space-y-2">
              {[
                { id: 'ingest', name: 'Ingest Agent', system: 'Documents', hitl: false },
                { id: 'reconcile', name: 'Reconcile Agent', system: 'Reconciliations', hitl: false },
                { id: 'triage', name: 'Triage Agent', system: 'Exceptions', hitl: false },
                { id: 'hitl', name: 'HITL Review', system: 'Approvals', hitl: true },
                { id: 'close', name: 'Close Agent', system: 'Close Period', hitl: false },
              ].map(a => (
                <div key={a.id} className="flex items-center justify-between py-2 border-b last:border-0">
                  <div>
                    <span className="font-medium">{a.name}</span>
                    <span className="text-xs text-gray-500 ml-2">→ {a.system}</span>
                  </div>
                  {a.hitl && <span className="px-2 py-0.5 rounded text-xs bg-amber-100 text-amber-700">HITL</span>}
                </div>
              ))}
            </div>
          ) : (
            <div className="space-y-2">
              {agents.map(a => (
                <div key={a.agent_id} className="flex items-center justify-between py-2 border-b last:border-0">
                  <div>
                    <span className="font-medium">{a.name}</span>
                    <span className="text-xs text-gray-500 ml-2">→ {a.system}</span>
                  </div>
                  {a.hitl_pending && <span className="px-2 py-0.5 rounded text-xs bg-amber-100 text-amber-700">HITL Pending</span>}
                  <span className={`px-2 py-0.5 rounded text-xs ${a.status === 'active' ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-600'}`}>
                    {a.status}
                  </span>
                </div>
              ))}
            </div>
          )}
        </div>

        <div className="rounded-xl border bg-white p-4">
          <h2 className="font-semibold mb-3">Workflow Runs</h2>
          {runs.length === 0 ? (
            <p className="text-gray-500 text-sm">No runs yet. Trigger via Race Control.</p>
          ) : (
            <div className="space-y-2">
              {runs.slice(0, 8).map(r => (
                <div key={r.run_id} className="flex items-center justify-between py-2 border-b last:border-0 text-sm">
                  <span className="font-mono text-xs">{r.run_id.slice(0, 8)}…</span>
                  <span>{r.agents_invoked} agents</span>
                  <span>{r.systems_touched?.join(', ') || '—'}</span>
                  <span className={r.hitl_count > 0 ? 'text-amber-600' : ''}>{r.hitl_count} HITL</span>
                  <span className={`px-2 py-0.5 rounded text-xs ${r.status === 'completed' ? 'bg-green-100 text-green-700' : 'bg-yellow-100 text-yellow-700'}`}>
                    {r.status}
                  </span>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
