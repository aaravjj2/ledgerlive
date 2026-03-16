/**
 * Agent Console — Live agent cycles, perceive, and ask.
 * Integrates /api/agent/cycle, /api/agent/cycles, /api/agent/perceive, /api/agent/ask.
 */
import { useEffect, useState, useCallback } from 'react'

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
      const r = await fetch('/api/agent/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: askQuery.trim() }),
      })
      const j = await r.json()
      setAskResponse(j)
    } catch {
      setAskResponse({ response: 'Failed to get response.', intent: 'error' })
    }
    setAskLoading(false)
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
            {askResponse && (
              <div
                data-testid="agent-ask-response"
                className="mt-3 rounded-xl border bg-[#111118] border-[#2A2A3A] p-4 text-gray-300 text-sm leading-relaxed"
              >
                {askResponse.response}
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
