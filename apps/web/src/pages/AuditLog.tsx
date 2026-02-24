import { useEffect, useState } from 'react'

interface AuditEvent { trace_id: string; action: string; entity_type: string; entity_id: string; ts: string; detail?: Record<string, unknown> }

export default function AuditLog() {
  const [events, setEvents] = useState<AuditEvent[]>([])
  const [loading, setLoading] = useState(true)

  const load = () => {
    setLoading(true)
    fetch('/api/audit').then(r => r.json()).then(d => { setEvents((d.events || []).slice().reverse()); setLoading(false) }).catch(() => setLoading(false))
  }

  useEffect(() => { load() }, [])

  return (
    <div data-testid="page-audit">
      <div className="flex items-center justify-between mb-2">
        <h1 className="text-2xl font-bold" data-testid="audit-title">Audit Log</h1>
        <button onClick={load} className="text-sm px-3 py-1 rounded-lg bg-indigo-600 text-white hover:bg-indigo-700">↻ Refresh</button>
      </div>
      <p className="text-gray-500 mb-6" data-testid="audit-subtitle">Immutable audit trail of all system actions.</p>

      {loading ? <p className="text-gray-400">Loading…</p> : (
        <div className="rounded-xl border bg-white shadow-sm overflow-hidden">
          <table className="w-full text-sm">
            <thead className="bg-gray-50 border-b">
              <tr>
                <th className="text-left px-4 py-3 font-semibold text-gray-600">Timestamp</th>
                <th className="text-left px-4 py-3 font-semibold text-gray-600">Action</th>
                <th className="text-left px-4 py-3 font-semibold text-gray-600">Entity Type</th>
                <th className="text-left px-4 py-3 font-semibold text-gray-600">Entity ID</th>
                <th className="text-left px-4 py-3 font-semibold text-gray-600">Trace ID</th>
              </tr>
            </thead>
            <tbody>
              {events.length === 0 && (
                <tr><td colSpan={5} className="text-center py-8 text-gray-400">No audit events yet. Perform an action to generate entries.</td></tr>
              )}
              {events.map((e, i) => (
                <tr key={e.trace_id + i} className="border-b hover:bg-gray-50 font-mono text-xs">
                  <td className="px-4 py-2 text-gray-500">{e.ts ? new Date(e.ts).toLocaleTimeString() : '—'}</td>
                  <td className="px-4 py-2 font-semibold text-indigo-700">{e.action}</td>
                  <td className="px-4 py-2 text-gray-600">{e.entity_type}</td>
                  <td className="px-4 py-2 text-gray-500">{e.entity_id.slice(0, 12)}…</td>
                  <td className="px-4 py-2 text-gray-400">{e.trace_id.slice(0, 8)}…</td>
                </tr>
              ))}
            </tbody>
          </table>
          <div className="px-4 py-2 text-xs text-gray-400 bg-gray-50">{events.length} event(s) in log</div>
        </div>
      )}
    </div>
  )
}
