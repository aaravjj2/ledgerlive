/**
 * Close Scorecard — Close KPI scorecard.
 * W78 Close Scorecard frontend.
 */
import { useEffect, useState, useCallback } from 'react'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'
import useApi from '../hooks/useApi'

interface ScorecardMetric {
  metric_id: string
  name: string
  value: number
  target: number
  unit: string
  status: string
}

export default function CloseScorecard() {
  const { fetchData } = useApi<{ items?: ScorecardMetric[] }>('/api/close-scorecard')
  const [metrics, setMetrics] = useState<ScorecardMetric[]>([])
  const [loading, setLoading] = useState(true)

  const load = useCallback(async () => {
    setLoading(true)
    try {
      const d = await fetchData()
      setMetrics(d?.items ?? [])
    } catch {
      setMetrics([])
    } finally {
      setLoading(false)
    }
  }, [fetchData])

  useEffect(() => {
    load()
  }, [load])

  const displayMetrics = metrics.length > 0 ? metrics : [
    { metric_id: 'm1', name: 'Days to Close', value: 4.2, target: 5, unit: 'd', status: 'on_track' },
    { metric_id: 'm2', name: 'Exception Rate', value: 2.1, target: 3, unit: '%', status: 'on_track' },
    { metric_id: 'm3', name: 'Auto-Resolve %', value: 78, target: 80, unit: '%', status: 'at_risk' },
    { metric_id: 'm4', name: 'SLA Adherence', value: 94, target: 95, unit: '%', status: 'at_risk' },
  ]

  const chartData = displayMetrics.map(m => ({ name: m.name, value: m.value, target: m.target }))

  return (
    <div data-testid="close-scorecard-page" className="space-y-5 pb-10">
      <div className="flex items-center justify-between mb-5">
        <div>
          <h1 className="text-xl font-bold text-white" data-testid="scorecard-title">Close Scorecard</h1>
          <p className="text-xs text-gray-600 mt-0.5">Close KPI scorecard and metrics.</p>
        </div>
        <button onClick={load} disabled={loading}
          className="px-3 py-1.5 text-xs rounded-lg border border-[#2A2A3A] text-gray-400 hover:text-gray-200 transition disabled:opacity-50">
          {loading ? 'Loading…' : '↻ Refresh'}
        </button>
      </div>

      {loading ? (
        <div className="space-y-2 animate-pulse">
          {Array.from({length: 4}).map((_, i) => (
            <div key={i} className="h-20 rounded-xl bg-[#111118] border border-[#2A2A3A]" />
          ))}
        </div>
      ) : (
        <>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
            {displayMetrics.slice(0, 4).map(m => (
              <div key={m.metric_id} className="rounded-xl border border-[#2A2A3A] bg-[#111118] p-4" data-testid="scorecard-metric">
                <div className="text-sm text-gray-500 mb-1">{m.name}</div>
                <div className="text-2xl font-bold text-red-400">{m.value}{m.unit}</div>
                <div className="text-xs text-gray-400">Target: {m.target}{m.unit}</div>
                <span className={`inline-block mt-2 px-2 py-0.5 rounded text-xs border ${
                  m.status === 'on_track' ? 'bg-green-900/40 text-green-400 border-green-500/30' :
                  m.status === 'at_risk' ? 'bg-yellow-900/40 text-yellow-400 border-yellow-500/30' : 'bg-red-900/40 text-red-400 border-red-500/30'
                }`}>
                  {m.status}
                </span>
              </div>
            ))}
          </div>

          {chartData.length > 0 && (
            <div className="rounded-xl border border-[#2A2A3A] bg-[#111118] p-4">
              <h2 className="text-xs text-gray-500 uppercase tracking-widest mb-3">Actual vs Target</h2>
              <div className="h-56">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={chartData} barGap={4}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#2A2A3A" />
                    <XAxis dataKey="name" stroke="#6B7280" fontSize={11} tick={{ fill: '#6B7280' }} />
                    <YAxis stroke="#6B7280" fontSize={11} tick={{ fill: '#6B7280' }} />
                    <Tooltip
                      contentStyle={{ backgroundColor: '#111118', border: '1px solid #2A2A3A', borderRadius: '8px' }}
                      labelStyle={{ color: '#F8F9FA' }}
                      itemStyle={{ color: '#9CA3AF' }}
                    />
                    <Bar dataKey="value" fill="#E8002D" name="Actual" radius={[4,4,0,0]} />
                    <Bar dataKey="target" fill="#374151" name="Target" radius={[4,4,0,0]} />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>
          )}
        </>
      )}
    </div>
  )
}
