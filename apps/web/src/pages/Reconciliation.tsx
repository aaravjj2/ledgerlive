import { useEffect, useState } from 'react'

interface Recon { recon_id: string; recon_name?: string; account_id?: string; status?: string; matched_count?: number; unmatched_count?: number; total_amount?: number }

export default function Reconciliation() {
  const [recons, setRecons] = useState<Recon[]>([])
  const [loading, setLoading] = useState(true)
  const [acting, setActing] = useState<string | null>(null)

  const load = () => {
    setLoading(true)
    fetch('/api/reconciliations').then(r => r.json()).then(d => { setRecons(d.items || []); setLoading(false) }).catch(() => setLoading(false))
  }

  useEffect(() => { load() }, [])

  const approve = async (id: string) => {
    setActing(id)
    await fetch(`/api/reconciliations/${id}/approve`, { method: 'POST', headers: { 'content-type': 'application/json' }, body: '{}' })
    setActing(null)
    load()
  }

  const statusColor = (s?: string) => {
    if (s === 'approved') return 'bg-green-900/40 text-green-400'
    if (s === 'open') return 'bg-yellow-900/40 text-yellow-400'
    if (s === 'rejected') return 'bg-red-900/40 text-red-400'
    return 'bg-[#1A1A24] text-gray-400'
  }

  return (
    <div data-testid="reconciliation-page">
      <div className="flex items-center justify-between mb-2">
        <h1 className="text-2xl font-bold" data-testid="reconciliation-title">Reconciliation</h1>
        <button onClick={load} className="text-sm px-3 py-1 rounded-lg bg-red-600 text-white hover:bg-red-700">↻ Refresh</button>
      </div>
      <p className="text-gray-500 mb-6" data-testid="reconciliation-subtitle">Match and reconcile financial records.</p>

      {loading ? <p className="text-gray-400">Loading…</p> : (
        <div className="rounded-xl border bg-[#111118] overflow-hidden">
          <table className="w-full text-sm">
            <thead className="bg-[#1A1A24] border-b">
              <tr>
                <th className="text-left px-4 py-3 font-semibold text-gray-400">Name</th>
                <th className="text-left px-4 py-3 font-semibold text-gray-400">Account</th>
                <th className="text-right px-4 py-3 font-semibold text-gray-400">Matched</th>
                <th className="text-right px-4 py-3 font-semibold text-gray-400">Unmatched</th>
                <th className="text-right px-4 py-3 font-semibold text-gray-400">Total ($)</th>
                <th className="text-left px-4 py-3 font-semibold text-gray-400">Status</th>
                <th className="px-4 py-3"></th>
              </tr>
            </thead>
            <tbody>
              {recons.length === 0 && (
                <tr><td colSpan={7} className="text-center py-8 text-gray-400">No reconciliations yet.</td></tr>
              )}
              {recons.map(r => (
                <tr key={r.recon_id} className="border-b hover:bg-[#1A1A24]">
                  <td className="px-4 py-3 font-medium text-gray-200">{r.recon_name || r.recon_id.slice(0,8)}</td>
                  <td className="px-4 py-3 text-gray-400">{r.account_id || '—'}</td>
                  <td className="px-4 py-3 text-right text-green-400 font-medium">{r.matched_count ?? '—'}</td>
                  <td className="px-4 py-3 text-right text-red-600 font-medium">{r.unmatched_count ?? '—'}</td>
                  <td className="px-4 py-3 text-right text-gray-300">{r.total_amount ? r.total_amount.toLocaleString() : '—'}</td>
                  <td className="px-4 py-3">
                    <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${statusColor(r.status)}`}>{r.status || 'unknown'}</span>
                  </td>
                  <td className="px-4 py-3">
                    {r.status === 'open' && (
                      <button onClick={() => approve(r.recon_id)} disabled={acting === r.recon_id}
                        className="text-xs px-2 py-1 rounded bg-green-600 text-white hover:bg-green-700 disabled:opacity-50">
                        {acting === r.recon_id ? '…' : 'Approve'}
                      </button>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          <div className="px-4 py-2 text-xs text-gray-400 bg-[#1A1A24]">{recons.length} reconciliation(s)</div>
        </div>
      )}
    </div>
  )
}
