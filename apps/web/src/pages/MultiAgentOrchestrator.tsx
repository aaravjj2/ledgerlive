/**
 * Multi-Agent Orchestrator — Airia AI Agents Hackathon (Track 2: Active Agents)
 * Orchestrate intelligence across 2+ systems. HITL, nested agents, document generation.
 */
import { useEffect, useState, useCallback } from 'react'
import { apiGet, API_BASE } from '../services/api'

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

const STATIC_AGENTS = [
  { id: 'ingest',     name: 'Ingest Agent',     system: 'Documents',       icon: '📥', color: 'text-blue-400',   hitl: false },
  { id: 'reconcile',  name: 'Reconcile Agent',  system: 'Reconciliations', icon: '⚖️', color: 'text-[#00D2FF]', hitl: false },
  { id: 'triage',     name: 'Triage Agent',     system: 'Exceptions',      icon: '🔍', color: 'text-yellow-400', hitl: false },
  { id: 'hitl',       name: 'HITL Review',      system: 'Approvals',       icon: '👤', color: 'text-amber-400',  hitl: true  },
  { id: 'close',      name: 'Close Agent',      system: 'Close Period',    icon: '🏁', color: 'text-red-400',    hitl: false },
]

const STATUS_DOT: Record<string, string> = {
  active:    'bg-green-400 animate-pulse',
  completed: 'bg-green-600',
  pending:   'bg-gray-600',
  idle:      'bg-gray-700',
}

function AgentNodeCard({ agent, live }: { agent: typeof STATIC_AGENTS[0], live?: AgentNode }) {
  const status = live?.status ?? 'idle'
  const hitlPending = live?.hitl_pending ?? false
  const dotClass = live?.status === 'active' ? 'bg-green-400 animate-pulse' : (STATUS_DOT[status] ?? 'bg-gray-600')

  return (
    <div className="relative flex items-center gap-3 bg-[#1A1A24] border border-[#2A2A3A] rounded-xl p-3 hover:border-red-600/40 transition-colors">
      <div className={`text-xl w-8 text-center ${agent.color}`}>{agent.icon}</div>
      <div className="flex-1 min-w-0">
        <div className="font-medium text-sm text-gray-100 truncate">{agent.name}</div>
        <div className="text-xs text-gray-500">→ {agent.system}</div>
      </div>
      <div className="flex items-center gap-2">
        {(agent.hitl || hitlPending) && (
          <span className="px-1.5 py-0.5 rounded text-[10px] font-bold bg-amber-900/40 text-amber-400 uppercase tracking-wide">
            {hitlPending ? '⏸ AWAIT' : 'HITL'}
          </span>
        )}
        <div className={`w-2 h-2 rounded-full ${dotClass}`} title={status} />
      </div>
    </div>
  )
}

export default function MultiAgentOrchestrator() {
  const [agents, setAgents] = useState<AgentNode[]>([])
  const [runs, setRuns] = useState<WorkflowRun[]>([])
  const [loading, setLoading] = useState(true)
  const [running, setRunning] = useState(false)

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

  const runFullCycle = async () => {
    setRunning(true)
    try {
      await fetch(`${API_BASE}/api/ops/golden-scenario-run`, { method: 'POST' })
      await load()
    } finally {
      setRunning(false)
    }
  }

  const activeCount = agents.filter(a => a.status === 'active').length

  return (
    <div data-testid="multi-agent-orchestrator" className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between flex-wrap gap-3">
        <div>
          <h1 className="text-2xl font-bold" data-testid="orchestrator-title">Multi-Agent Orchestrator</h1>
          <p className="text-gray-500 text-sm mt-1">
            Active Agents — Orchestrate intelligence across 2+ systems. HITL, nested agents, document generation.
          </p>
        </div>
        <div className="flex items-center gap-2">
          {activeCount > 0 && (
            <span className="px-3 py-1 bg-green-900/40 text-green-400 rounded-full text-sm font-medium animate-pulse">
              ● {activeCount} agent{activeCount > 1 ? 's' : ''} active
            </span>
          )}
          <button
            onClick={runFullCycle}
            disabled={running || loading}
            className="px-4 py-2 bg-red-600 text-white rounded-lg text-sm font-medium hover:bg-red-700 disabled:opacity-50 transition-colors"
          >
            {running ? '⟳ Running…' : '▶ Run Full Close Cycle'}
          </button>
          <button
            onClick={load}
            disabled={loading}
            className="px-3 py-2 bg-[#1A1A24] border border-[#2A2A3A] text-gray-300 rounded-lg text-sm hover:bg-[#2A2A3A] disabled:opacity-50 transition-colors"
          >
            {loading ? '…' : '↻'}
          </button>
        </div>
      </div>

      {/* Hackathon track banner */}
      <div className="rounded-xl border bg-green-900/20 border-green-500/30 p-4">
        <h3 className="font-semibold text-green-300 mb-1">🏆 Track 2: Active Agents</h3>
        <p className="text-sm text-green-400">
          LedgerLive close orchestrator runs 5-agent workflows: ingest → reconcile → triage → HITL review → close.
          Agents touch 5+ systems. Human-in-the-loop gates ensure fail-closed safety with full audit trail.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Agent Flow */}
        <div className="rounded-xl border border-[#2A2A3A] bg-[#111118] p-4">
          <h2 className="font-semibold mb-4 text-gray-200">Agent Pipeline</h2>
          <div className="space-y-1">
            {STATIC_AGENTS.map((agentDef, idx) => {
              const live = agents.find(a => a.agent_id === agentDef.id || a.name?.toLowerCase().includes(agentDef.id))
              return (
                <div key={agentDef.id}>
                  <AgentNodeCard agent={agentDef} live={live} />
                  {idx < STATIC_AGENTS.length - 1 && (
                    <div className="flex justify-center py-0.5">
                      <div className="w-0.5 h-4 bg-[#2A2A3A]" />
                    </div>
                  )}
                </div>
              )
            })}
          </div>

          {/* Systems touched legend */}
          <div className="mt-4 pt-4 border-t border-[#2A2A3A]">
            <p className="text-xs text-gray-500 mb-2">Systems touched:</p>
            <div className="flex flex-wrap gap-1.5">
              {['Documents', 'Reconciliations', 'Exceptions', 'Approvals', 'Close Period'].map(s => (
                <span key={s} className="px-2 py-0.5 bg-[#1A1A24] text-gray-400 text-xs rounded border border-[#2A2A3A]">
                  {s}
                </span>
              ))}
            </div>
          </div>
        </div>

        {/* Workflow Runs */}
        <div className="rounded-xl border border-[#2A2A3A] bg-[#111118] p-4">
          <h2 className="font-semibold mb-4 text-gray-200">Workflow Runs</h2>
          {runs.length === 0 ? (
            <div className="flex flex-col items-center justify-center py-10 text-center">
              <div className="text-4xl mb-3">🤖</div>
              <p className="text-gray-500 text-sm">No runs yet.</p>
              <p className="text-gray-400 text-xs mt-1">Click "Run Full Close Cycle" to trigger a workflow.</p>
            </div>
          ) : (
            <div className="space-y-2">
              {runs.slice(0, 8).map(r => (
                <div
                  key={r.run_id}
                  className="flex items-center gap-2 py-2 border-b border-[#2A2A3A] last:border-0 text-sm"
                >
                  <span className="font-mono text-xs text-[#00D2FF] w-20 shrink-0">
                    {r.run_id.slice(0, 8)}…
                  </span>
                  <span className="text-gray-400 text-xs shrink-0">{r.agents_invoked}A</span>
                  <div className="flex flex-wrap gap-1 flex-1 min-w-0">
                    {(r.systems_touched ?? []).slice(0, 3).map(s => (
                      <span key={s} className="px-1 py-0.5 bg-[#1A1A24] text-gray-500 text-[10px] rounded truncate">
                        {s}
                      </span>
                    ))}
                  </div>
                  {r.hitl_count > 0 && (
                    <span className="text-amber-400 text-xs shrink-0">{r.hitl_count} HITL</span>
                  )}
                  <span className={`px-2 py-0.5 rounded text-xs shrink-0 ${
                    r.status === 'completed' ? 'bg-green-900/40 text-green-400' : 'bg-yellow-900/40 text-yellow-400'
                  }`}>
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
