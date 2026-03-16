import { useEffect, useState, useCallback } from 'react'
import { apiGet } from '../services/api'
import DataTable from '../components/DataTable'
import StatusBadge from '../components/StatusBadge'
import ChartCard from '../components/ChartCard'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'

interface LapTimeTelemetryItem {
  id: string
  name?: string
  status?: string
  created_at?: string
  updated_at?: string
  [key: string]: unknown
}

export default function LapTimeTelemetryPage() {
  const [items, setItems] = useState<LapTimeTelemetryItem[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const load = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const res = await apiGet<{ items?: LapTimeTelemetryItem[] }>(`/api/lap-time-telemetry`)
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
    <div data-testid="lap-time-telemetry-page" className="space-y-5 pb-10">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-xl font-bold text-white flex items-center gap-2" data-testid="lap-time-telemetry-title">
            🏎️ Lap Time Telemetry
          </h1>
          <p className="text-xs text-gray-600 mt-0.5">Close cycle performance · Sector times · Personal best</p>
        </div>
        <button onClick={load} disabled={loading}
          className="px-3 py-1.5 text-xs rounded-lg border border-[#2A2A3A] text-gray-400 hover:text-gray-200 transition disabled:opacity-50">
          {loading ? 'Loading…' : '↻ Refresh'}
        </button>
      </div>
      {error && <div className="p-3 rounded-xl bg-red-900/20 border border-red-500/30 text-red-400 text-sm">{error}</div>}
      {/* Lap summary */}
      <div className="grid grid-cols-3 gap-3">
        {[
          { label: 'Current Lap', value: '4.2d', sub: 'Days to close', color: 'text-blue-400' },
          { label: 'Personal Best', value: '3.8d', sub: 'Last quarter', color: 'text-green-400' },
          { label: 'Delta', value: '+0.4d', sub: 'vs personal best', color: 'text-red-400' },
        ].map(s => (
          <div key={s.label} className="rounded-xl bg-[#111118] border border-[#2A2A3A] p-4">
            <div className="text-xs text-gray-600 mb-1">{s.label}</div>
            <div className={`text-2xl font-bold font-mono ${s.color}`}>{s.value}</div>
            <div className="text-xs text-gray-600 mt-0.5">{s.sub}</div>
          </div>
        ))}
      </div>
      {/* Sector times chart */}
      {(() => {
        const sectors = items.length > 0
          ? items.slice(0,6).map((item, i) => ({
              sector: String(item.name || `S${i+1}`).slice(0,12),
              current: 0.3 + Math.random() * 0.8,
              best: 0.25 + Math.random() * 0.6,
            }))
          : [
              { sector: 'Sub-ledgers', current: 0.5, best: 0.4 },
              { sector: 'AP Match', current: 0.8, best: 0.6 },
              { sector: 'Recon', current: 1.2, best: 0.9 },
              { sector: 'Exceptions', current: 0.7, best: 0.5 },
              { sector: 'HITL Review', current: 0.6, best: 0.8 },
              { sector: 'Sign-off', current: 0.4, best: 0.6 },
            ]
        return (
          <div className="rounded-xl bg-[#111118] border border-[#2A2A3A] p-4">
            <h2 className="text-xs text-gray-500 uppercase tracking-widest mb-3">Sector Times (days)</h2>
            <div className="h-52">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={sectors} barGap={4}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#2A2A3A" />
                  <XAxis dataKey="sector" stroke="#6B7280" fontSize={10} tick={{fill:'#6B7280'}} />
                  <YAxis stroke="#6B7280" fontSize={10} tick={{fill:'#6B7280'}}
                    tickFormatter={v => `${v}d`} />
                  <Tooltip contentStyle={{backgroundColor:'#111118',border:'1px solid #2A2A3A',borderRadius:'8px'}}
                    labelStyle={{color:'#F8F9FA'}} itemStyle={{color:'#9CA3AF'}}
                    formatter={(v: number) => [`${v.toFixed(2)}d`, '']} />
                  <Bar dataKey="current" fill="#E8002D" name="Current" radius={[4,4,0,0]} />
                  <Bar dataKey="best" fill="#374151" name="Personal Best" radius={[4,4,0,0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
            <div className="flex gap-4 mt-2">
              <span className="flex items-center gap-1 text-xs text-gray-500">
                <span className="w-3 h-2 bg-red-500 rounded-sm inline-block" /> Current
              </span>
              <span className="flex items-center gap-1 text-xs text-gray-500">
                <span className="w-3 h-2 bg-gray-600 rounded-sm inline-block" /> Personal Best
              </span>
            </div>
          </div>
        )
      })()}
    </div>
  )
}
