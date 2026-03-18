import { useEffect, useState } from 'react'
import { API_BASE } from '../services/api'

interface Exc { exception_id: string; exception_type?: string; severity?: string; description?: string; account_id?: string; status?: string; amount_delta?: number }

export default function Exceptions() {
  const [items, setItems] = useState<Exc[]>([])
  const [loading, setLoading] = useState(true)
  const [acting, setActing] = useState<string | null>(null)

  const load = () => {
    setLoading(true)
    fetch(`${API_BASE}/api/exceptions`).then(r => r.json()).then(d => { setItems(d.items || []); setLoading(false) }).catch(() => setLoading(false))
  }

  useEffect(() => { load() }, [])

  const resolve = async (id: string) => {
    setActing(id)
    await fetch(`${API_BASE}/api/exceptions/${id}/resolve`, { method: 'POST', headers: { 'content-type': 'application/json' }, body: '{}' })
    setActing(null)
    load()
  }

  const sevColor = (s?: string) => {
    if (s === 'high' || s === 'critical') return 'bg-red-900/40 text-red-400'
    if (s === 'medium') return 'bg-yellow-900/40 text-yellow-400'
    return 'bg-blue-900/40 text-blue-400'
  }

  const statusColor = (s?: string) => {
    if (s === 'resolved') return 'bg-green-900/40 text-green-400'
    if (s === 'open') return 'bg-red-900/40 text-red-400'
    return 'bg-[#1A1A24] text-gray-400'
  }

  const getClassificationBadge = (ex: Exc) => {
    const sev = (ex.severity || '').toLowerCase()
    const isHighRisk = sev === 'high' || sev === 'critical'
    if (isHighRisk) {
      return (
        <span className="px-2 py-0.5 bg-amber-900/40 text-amber-300 border border-amber-500/30 rounded text-xs font-medium">
          ESCALATE
        </span>
      )
    }
    return (
      <span className="px-2 py-0.5 bg-green-900/40 text-green-300 border border-green-500/30 rounded text-xs font-medium">
        AUTO-RESOLVE
      </span>
    )
  }

  return (
    <div data-testid="exceptions-page">
      <div className="flex items-center justify-between mb-2">
        <h1 className="text-2xl font-bold" data-testid="exceptions-title">Exceptions</h1>
        <span className="text-sm text-gray-500">{items.filter(i => i.status === 'open').length} open</span>
      </div>
      <p className="text-gray-500 mb-6" data-testid="exceptions-subtitle">Review and triage reconciliation exceptions.</p>

      {loading ? <p className="text-gray-400">Loading…</p> : (
        <div className="space-y-3">
          {items.length === 0 && <p className="text-gray-400 py-8 text-center">No exceptions. All clear ✅</p>}
          {items.map(ex => (
            <div key={ex.exception_id} className="rounded-xl border bg-[#111118] p-4 flex items-start gap-4">
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-1">
                  <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${sevColor(ex.severity)}`}>{ex.severity || 'low'}</span>
                  <span className="text-xs text-gray-500 uppercase">{ex.exception_type || 'variance'}</span>
                  {getClassificationBadge(ex)}
                  {ex.account_id && <span className="text-xs text-red-400 font-mono">{ex.account_id}</span>}
                </div>
                <p className="text-sm text-gray-200">{ex.description || 'Reconciliation exception'}</p>
                {ex.amount_delta != null && (
                  <p className="text-xs text-gray-500 mt-1">Δ Amount: <span className="font-semibold text-red-600">${ex.amount_delta.toLocaleString()}</span></p>
                )}
              </div>
              <div className="flex flex-col items-end gap-2">
                <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${statusColor(ex.status)}`}>{ex.status}</span>
                {ex.status === 'open' && (
                  <button onClick={() => resolve(ex.exception_id)} disabled={acting === ex.exception_id}
                    className="text-xs px-3 py-1 rounded-lg bg-red-600 text-white hover:bg-red-700 disabled:opacity-50">
                    {acting === ex.exception_id ? '…' : 'Resolve'}
                  </button>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
