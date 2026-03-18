/**
 * Agent Console — Live agent cycles, perceive, and ask.
 * Integrates /api/agent/cycle, /api/agent/cycles, /api/agent/perceive, /api/agent/ask.
 */
import { useEffect, useState, useCallback } from 'react'
import { API_BASE } from '../services/api'

interface AgentCycle {
  cycle_id: string
  status: string
  perceived_count?: number
  decided_count?: number
  acted_count?: number
  created_at?: string
}

interface PerceiveState {
  open_exceptions: number
  pending_reviews: number
  blocked_lanes: number
  overall_health: string
}

interface AskResponse {
  response: string
  success?: boolean
  model?: string
  low_risk_count?: number
  high_risk_count?: number
  journal_entries?: unknown[]
  agent_summary?: string
  latency_ms?: number
  intent?: string
  trace_id?: string
}

export default function AgentConsole() {
  const [cycles, setCycles] = useState<AgentCycle[]>([])
  const [perceive, setPerceive] = useState<PerceiveState | null>(null)
  const [askQuery, setAskQuery] = useState('')
  const [askResponse, setAskResponse] = useState<AskResponse | null>(null)
  const [loading, setLoading] = useState(true)
  const [cycleLoading, setCycleLoading] = useState(false)
  const [askLoading, setAskLoading] = useState(false)
  const [currentPhase, setCurrentPhase] = useState(0)

  const load = useCallback(() => {
    Promise.all([
      fetch('/api/agent/cycles').then(r => r.json()),
      fetch('/api/agent/perceive').then(r => r.json()),
    ]).then(([cyc, perc]) => {
      setCycles(cyc.cycles || cyc.items || [])
      setPerceive(perc)
      setLoading(false)
    }).catch(() => setLoading(false))
  }, [])

  useEffect(() => { load() }, [load])

  useEffect(() => {
    if (!askLoading) {
      setCurrentPhase(0)
      return
    }
    const phases = 3
    const interval = setInterval(() => {
      setCurrentPhase(prev => (prev + 1) % phases)
    }, 1500)
    return () => clearInterval(interval)
  }, [askLoading])

  const runCycle = async () => {
    setCycleLoading(true)
    try {
      await fetch('/api/agent/cycle', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: '{}' })
      load()
    } catch {
      /* ignore */
    }
    setCycleLoading(false)
  }

  const submitAsk = async () => {
    if (!askQuery.trim()) return
    setAskLoading(true)
    setAskResponse(null)
    try {
      const r = await fetch(`${API_BASE}/api/voice/ask`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: askQuery.trim() }),
      })
      const j = await r.json()
      setAskResponse(j)
    } catch {
      setAskResponse({ response: 'Failed to get response.', intent: 'error' })
    }
    setAskLoading(false)
  }

  const renderAgentResponse = (data: AskResponse | null) => {
    if (!data) return null
    return (
      <div className="space-y-3">
        <p className="text-white text-sm">{data.response || data.agent_summary}</p>

        <div className="flex gap-2 text-xs">
          <span className="px-2 py-1 bg-blue-900/40 text-blue-300 rounded">Perceive</span>
          <span className="px-2 py-1 bg-purple-900/40 text-purple-300 rounded">Decide</span>
          <span className="px-2 py-1 bg-green-900/40 text-green-300 rounded">Act</span>
        </div>

        {(data.low_risk_count || 0) > 0 && (
          <div className="p-2 bg-green-900/20 border border-green-500/30 rounded text-xs">
            <span className="text-green-400 font-medium">Auto-resolved: </span>
            <span className="text-gray-300">{data.low_risk_count} exception(s) - journal entries posted</span>
          </div>
        )}

        {(data.high_risk_count || 0) > 0 && (
          <div className="p-2 bg-amber-900/20 border border-amber-500/30 rounded text-xs">
            <span className="text-amber-400 font-medium">Escalated: </span>
            <span className="text-gray-300">{data.high_risk_count} exception(s) - awaiting CFO approval</span>
          </div>
        )}

        {data.latency_ms && (
          <p className="text-gray-500 text-xs">
            Agent cycle: {(data.latency_ms / 1000).toFixed(1)}s · {data.model}
          </p>
        )}
      </div>
    )
  }

  const healthColor = (h?: string) => {
    if (h === 'green') return 'bg-green-900/40 text-green-300'
    if (h === 'yellow') return 'bg-yellow-900/40 text-yellow-300'
    if (h === 'red') return 'bg-red-900/40 text-red-400'
    return 'bg-[#1A1A24] text-gray-200'
  }

  return (
    <div data-testid="agent-console-page" className="pb-10">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold" data-testid="agent-console-title">Agent Console</h1>
          <p className="text-gray-500 text-sm mt-1">Run agent cycles, perceive state, and ask the race engineer.</p>
        </div>
        <button
          data-testid="agent-run-cycle"
          onClick={runCycle}
          disabled={cycleLoading}
          className="px-4 py-2 bg-red-600 text-white rounded-lg text-sm font-medium hover:bg-red-700 disabled:opacity-50"
        >
          {cycleLoading ? 'Running…' : '▶ Run Cycle'}
        </button>
      </div>

      {loading ? (
        <p className="text-gray-400">Loading…</p>
      ) : (
        <>
          <div className="flex items-center gap-2 mb-4 p-3 bg-purple-900/20 border border-purple-500/30 rounded-lg">
            <div className="w-2 h-2 bg-purple-400 rounded-full animate-pulse"></div>
            <span className="text-purple-300 text-sm font-medium">LedgerLive Close Orchestrator</span>
            <span className="text-gray-500 text-xs">•</span>
            <span className="text-gray-400 text-xs">Powered by Airia · GPT 4.1 · Active Agent</span>
          </div>

          {/* Perceive State */}
          {perceive && (
            <section className="mb-6" data-testid="agent-perceive-section">
              <h2 className="text-lg font-semibold mb-3">Perceived State</h2>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div className="rounded-xl border border-[#2A2A3A] bg-[#111118] p-4">
                  <div className="text-xs text-gray-500">Open Exceptions</div>
                  <div className="text-2xl font-bold font-mono text-red-400">{perceive.open_exceptions ?? 0}</div>
                </div>
                <div className="rounded-xl border border-[#2A2A3A] bg-[#111118] p-4">
                  <div className="text-xs text-gray-500">Pending Reviews</div>
                  <div className="text-2xl font-bold font-mono text-yellow-400">{perceive.pending_reviews ?? 0}</div>
                </div>
                <div className="rounded-xl border border-[#2A2A3A] bg-[#111118] p-4">
                  <div className="text-xs text-gray-500">Blocked Lanes</div>
                  <div className="text-2xl font-bold font-mono text-orange-400">{perceive.blocked_lanes ?? 0}</div>
                </div>
                <div className="rounded-xl border border-[#2A2A3A] bg-[#111118] p-4">
                  <div className="text-xs text-gray-500">Overall Health</div>
                  <span className={`inline-block px-2 py-0.5 rounded text-sm font-bold ${healthColor(perceive.overall_health)}`}>
                    {perceive.overall_health || '—'}
                  </span>
                </div>
              </div>
            </section>
          )}

          {/* Ask Race Engineer */}
          <section className="mb-6" data-testid="agent-ask-section">
            <h2 className="text-lg font-semibold mb-3">Ask Race Engineer</h2>
            <div className="flex gap-2">
              <input
                data-testid="agent-ask-input"
                type="text"
                value={askQuery}
                onChange={e => setAskQuery(e.target.value)}
                onKeyDown={e => e.key === 'Enter' && submitAsk()}
                placeholder="e.g. What's blocking the close?"
                className="flex-1 px-4 py-2 bg-[#1A1A24] border border-[#2A2A3A] rounded-lg text-gray-100 placeholder-gray-600 focus:outline-none focus:ring-1 focus:ring-red-500/50 text-sm"
              />
              <button
                data-testid="agent-ask-submit"
                onClick={submitAsk}
                disabled={askLoading}
                className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 disabled:opacity-50"
              >
                {askLoading ? '…' : 'Ask'}
              </button>
            </div>
            {!askResponse && (
              <div className="flex flex-wrap gap-2 mt-2">
                {["What's blocking the close?", "How many exceptions are open?", "Run a cycle summary", "What's the overall health?"].map(q => (
                  <button key={q} onClick={() => { setAskQuery(q); }}
                    className="px-3 py-1 text-xs rounded-lg border border-[#2A2A3A] text-gray-500 hover:text-gray-300 hover:border-[#3A3A4A] transition">
                    {q}
                  </button>
                ))}
              </div>
            )}
            {askLoading && (
              <div className="space-y-2 p-3 mt-3 rounded-xl border bg-[#111118] border-[#2A2A3A]">
                {['Perceiving exceptions...', 'Deciding risk levels...', 'Acting on low-risk items...'].map((phase, i) => (
                  <div key={phase} className={`text-xs flex items-center gap-2 transition-opacity duration-500 ${i === currentPhase ? 'text-purple-300 opacity-100' : 'text-gray-600 opacity-40'}`}>
                    <div className={`w-1.5 h-1.5 rounded-full ${i === currentPhase ? 'bg-purple-400 animate-pulse' : 'bg-gray-600'}`}></div>
                    {phase}
                  </div>
                ))}
              </div>
            )}
            {askResponse && (
              <div
                data-testid="agent-ask-response"
                className="mt-3 rounded-xl border bg-[#111118] border-[#2A2A3A] p-4 text-gray-300 text-sm leading-relaxed"
              >
                {renderAgentResponse(askResponse)}
              </div>
            )}
          </section>

          {/* Cycle History */}
          <section data-testid="agent-cycles-section">
            <h2 className="text-lg font-semibold mb-3">Cycle History</h2>
            <div className="rounded-xl border bg-[#111118] overflow-hidden">
              <table className="w-full text-sm">
                <thead className="bg-[#1A1A24]">
                  <tr>
                    <th className="text-left px-4 py-2 font-semibold text-gray-400">Cycle ID</th>
                    <th className="text-left px-4 py-2 font-semibold text-gray-400">Status</th>
                    <th className="text-right px-4 py-2 font-semibold text-gray-400">Perceived</th>
                    <th className="text-right px-4 py-2 font-semibold text-gray-400">Decided</th>
                    <th className="text-right px-4 py-2 font-semibold text-gray-400">Acted</th>
                  </tr>
                </thead>
                <tbody>
                  {cycles.length === 0 && (
                    <tr><td colSpan={5} className="text-center py-8 text-gray-400">No cycles yet.</td></tr>
                  )}
                  {cycles.map(c => (
                    <tr key={c.cycle_id} className="border-t hover:bg-[#1A1A24]">
                      <td className="px-4 py-2 font-mono text-xs">{c.cycle_id?.slice(0, 8)}…</td>
                      <td className="px-4 py-2">{c.status}</td>
                      <td className="px-4 py-2 text-right">{c.perceived_count ?? '—'}</td>
                      <td className="px-4 py-2 text-right">{c.decided_count ?? '—'}</td>
                      <td className="px-4 py-2 text-right">{c.acted_count ?? '—'}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </section>
        </>
      )}
    </div>
  )
}
