import { useEffect, useState } from 'react'

interface Exc { exception_id: string; exception_type?: string; severity?: string; description?: string; account_id?: string; status?: string; amount_delta?: number }

export default function Exceptions() {
  const [items, setItems] = useState<Exc[]>([])
  const [loading, setLoading] = useState(true)
  const [acting, setActing] = useState<string | null>(null)

  const load = () => {
    setLoading(true)
    fetch('/api/exceptions').then(r => r.json()).then(d => { setItems(d.items || []); setLoading(false) }).catch(() => setLoading(false))
  }

  useEffect(() => { load() }, [])

  const resolve = async (id: string) => {
    setActing(id)
    await fetch(`/api/exceptions/${id}/resolve`, { method: 'POST', headers: { 'content-type': 'application/json' }, body: '{}' })
    setActing(null)
    load()
  }

  const sevColor = (s?: string) => {
    if (s === 'high' || s === 'critical') return 'bg-red-100 text-red-700'
    if (s === 'medium') return 'bg-yellow-100 text-yellow-700'
    return 'bg-blue-100 text-blue-700'
  }

  const statusColor = (s?: string) => {
    if (s === 'resolved') return 'bg-green-100 text-green-700'
    if (s === 'open') return 'bg-red-100 text-red-700'
    return 'bg-gray-100 text-gray-600'
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
            <div key={ex.exception_id} className="rounded-xl border bg-white shadow-sm p-4 flex items-start gap-4">
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-1">
                  <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${sevColor(ex.severity)}`}>{ex.severity || 'low'}</span>
                  <span className="text-xs text-gray-500 uppercase">{ex.exception_type || 'variance'}</span>
                  {ex.account_id && <span className="text-xs text-indigo-600 font-mono">{ex.account_id}</span>}
                </div>
                <p className="text-sm text-gray-800">{ex.description || 'Reconciliation exception'}</p>
                {ex.amount_delta != null && (
                  <p className="text-xs text-gray-500 mt-1">Δ Amount: <span className="font-semibold text-red-600">${ex.amount_delta.toLocaleString()}</span></p>
                )}
              </div>
              <div className="flex flex-col items-end gap-2">
                <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${statusColor(ex.status)}`}>{ex.status}</span>
                {ex.status === 'open' && (
                  <button onClick={() => resolve(ex.exception_id)} disabled={acting === ex.exception_id}
                    className="text-xs px-3 py-1 rounded-lg bg-indigo-600 text-white hover:bg-indigo-700 disabled:opacity-50">
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
