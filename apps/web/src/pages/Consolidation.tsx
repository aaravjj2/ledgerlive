import { useEffect, useState, useCallback } from 'react'
import { apiGet } from '../services/api'
import DataTable from '../components/DataTable'
import StatusBadge from '../components/StatusBadge'
import ChartCard from '../components/ChartCard'

interface ConsolidationItem {
  id: string
  name?: string
  status?: string
  created_at?: string
  updated_at?: string
  [key: string]: unknown
}

export default function ConsolidationPage() {
  const [items, setItems] = useState<ConsolidationItem[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const load = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const res = await apiGet<{ items?: ConsolidationItem[] }>(`/api/consolidation`)
      setItems(res?.items ?? [])
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Failed to load')
      setItems([])
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => { load() }, [load])

  const columns = [
    { key: 'id', label: 'ID', render: (v: string) => <span className="font-mono text-xs">{v?.slice(0, 8)}…</span> },
    { key: 'name', label: 'Name' },
    { key: 'status', label: 'Status', render: (v: string) => <StatusBadge status={v} /> },
    { key: 'created_at', label: 'Created', render: (v: string) => v ? new Date(v).toLocaleDateString() : '—' },
  ]

  return (
    <div data-testid="consolidation-page" className="space-y-5 pb-10">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-xl font-bold text-white" data-testid="consolidation-title">Consolidation</h1>
          <p className="text-xs text-gray-600 mt-0.5">Multi-entity · Intercompany eliminations · FX translation</p>
        </div>
        <button onClick={load} disabled={loading}
          className="px-3 py-1.5 text-xs rounded-lg border border-[#2A2A3A] text-gray-400 hover:text-gray-200 transition disabled:opacity-50">
          {loading ? 'Loading…' : '↻ Refresh'}
        </button>
      </div>
      {error && <div className="p-3 rounded-xl bg-red-900/20 border border-red-500/30 text-red-400 text-sm">{error}</div>}
      {/* Entity grid */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        {[
          { name: 'US Parent', currency: 'USD', revenue: 2840000, status: 'closed' },
          { name: 'EU Subsidiary', currency: 'EUR', revenue: 980000, status: 'in_progress' },
          { name: 'UK Entity', currency: 'GBP', revenue: 380000, status: 'pending' },
          { name: 'APAC Entity', currency: 'SGD', revenue: 240000, status: 'pending' },
        ].concat(items.slice(0,4).map(i => ({
          name: String(i.name || i.id?.slice(0,8)),
          currency: 'USD',
          revenue: 0,
          status: String(i.status || 'pending'),
        }))).slice(0,4).map((e, i) => (
          <div key={i} className="rounded-xl bg-[#111118] border border-[#2A2A3A] p-4">
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs text-gray-600 font-mono">{e.currency}</span>
              <span className={`px-1.5 py-0.5 rounded text-xs border font-mono uppercase ${
                e.status === 'closed' ? 'bg-green-900/40 text-green-400 border-green-500/30' :
                e.status === 'in_progress' ? 'bg-blue-900/40 text-blue-400 border-blue-500/30' :
                'bg-gray-800 text-gray-400 border-gray-600'
              }`}>{e.status === 'in_progress' ? 'WIP' : e.status.slice(0,6).toUpperCase()}</span>
            </div>
            <div className="font-medium text-gray-200 text-sm mb-1">{e.name}</div>
            <div className="text-lg font-bold font-mono text-blue-400">
              ${e.revenue > 0 ? (e.revenue/1000).toFixed(0) : '—'}K
            </div>
          </div>
        ))}
      </div>
      {/* Eliminations */}
      <div className="rounded-xl bg-[#111118] border border-[#2A2A3A] p-4">
        <h2 className="text-xs text-gray-500 uppercase tracking-widest mb-3">Intercompany Eliminations</h2>
        <div className="space-y-2">
          {[
            { desc: 'US → EU intercompany loan interest', amount: -42000, type: 'eliminate' },
            { desc: 'EU → UK management fee', amount: -18500, type: 'eliminate' },
            { desc: 'FX translation adjustment', amount: 12400, type: 'adjust' },
          ].map((e, i) => (
            <div key={i} className="flex items-center justify-between py-2 border-b border-[#2A2A3A] last:border-0">
              <span className="text-xs text-gray-400">{e.desc}</span>
              <span className={`text-xs font-mono font-medium ${e.amount < 0 ? 'text-red-400' : 'text-green-400'}`}>
                {e.amount < 0 ? '-' : '+'}${Math.abs(e.amount/1000).toFixed(1)}K
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
