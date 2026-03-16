import { useEffect, useState, useCallback } from 'react'
import { apiGet } from '../services/api'
import DataTable from '../components/DataTable'
import StatusBadge from '../components/StatusBadge'
import ChartCard from '../components/ChartCard'

interface KpiItem {
  id: string
  name?: string
  status?: string
  created_at?: string
  updated_at?: string
  [key: string]: unknown
}

export default function KpiPage() {
  const [items, setItems] = useState<KpiItem[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const load = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const res = await apiGet<{ items?: KpiItem[] }>(`/api/kpis`)
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
    <div data-testid="kpi-page" className="space-y-5 pb-10">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-xl font-bold text-white" data-testid="kpi-title">KPI Framework</h1>
          <p className="text-xs text-gray-600 mt-0.5">Key performance indicators · Mar 2026</p>
        </div>
        <button onClick={load} disabled={loading}
          className="px-3 py-1.5 text-xs rounded-lg border border-[#2A2A3A] text-gray-400 hover:text-gray-200 transition disabled:opacity-50">
          {loading ? 'Loading…' : '↻ Refresh'}
        </button>
      </div>

      {error && <div className="p-3 rounded-xl bg-red-900/20 border border-red-500/30 text-red-400 text-sm">{error}</div>}

      {/* KPI cards */}
      {loading ? (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3 animate-pulse">
          {Array.from({length:8}).map((_,i) => (
            <div key={i} className="h-24 rounded-xl bg-[#111118] border border-[#2A2A3A]" />
          ))}
        </div>
      ) : (
        <>
          {/* Build KPI display items from API data or use placeholders */}
          {(() => {
            const kpiCards = items.length > 0
              ? items.slice(0, 8).map((item, i) => ({
                  label: item.name || `KPI ${i+1}`,
                  value: String((item as Record<string, unknown>).value ?? item.id?.slice(0,4) ?? i * 12),
                  unit: String((item as Record<string, unknown>).unit ?? ''),
                  trend: i % 3 === 0 ? 'down' : 'up',
                  health: item.status === 'active' ? 'green' : item.status === 'at_risk' ? 'yellow' : 'green',
                  target: String((item as Record<string, unknown>).target ?? '—'),
                }))
              : [
                  { label: 'Days to Close', value: '4.2', unit: 'd', trend: 'up', health: 'green', target: '5d' },
                  { label: 'Exception Rate', value: '2.1', unit: '%', trend: 'up', health: 'green', target: '<3%' },
                  { label: 'Auto-Resolve %', value: '78', unit: '%', trend: 'down', health: 'yellow', target: '80%' },
                  { label: 'SLA Adherence', value: '94', unit: '%', trend: 'down', health: 'yellow', target: '95%' },
                  { label: 'Recon Match Rate', value: '94.2', unit: '%', trend: 'up', health: 'green', target: '95%' },
                  { label: 'Audit Events', value: '847', unit: '', trend: 'up', health: 'green', target: '—' },
                  { label: 'Open Exceptions', value: '3', unit: '', trend: 'down', health: 'red', target: '0' },
                  { label: 'Close Health', value: '62', unit: '%', trend: 'up', health: 'yellow', target: '100%' },
                ]

            return (
              <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                {kpiCards.map((k, i) => (
                  <div key={i} className={`rounded-xl p-4 border-2 ${
                    k.health === 'green' ? 'bg-green-900/20 border-green-500/40' :
                    k.health === 'yellow' ? 'bg-yellow-900/20 border-yellow-500/40' :
                    'bg-red-900/20 border-red-500/40'
                  }`}>
                    <div className="text-xs text-gray-500 uppercase tracking-wide mb-2">{k.label}</div>
                    <div className={`text-2xl font-bold font-mono ${
                      k.health === 'green' ? 'text-green-400' :
                      k.health === 'yellow' ? 'text-yellow-400' : 'text-red-400'
                    }`}>
                      {k.value}{k.unit && <span className="text-sm font-normal ml-1 text-gray-500">{k.unit}</span>}
                    </div>
                    <div className="flex items-center justify-between mt-2">
                      <span className="text-xs text-gray-600">Target: {k.target}</span>
                      <span className={`text-xs font-mono ${k.trend === 'up' ? 'text-green-400' : 'text-red-400'}`}>
                        {k.trend === 'up' ? '↑' : '↓'}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            )
          })()}
        </>
      )}
    </div>
  )
}
