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

  const chartData = metrics.map(m => ({ name: m.name, value: m.value, target: m.target }))

  return (
    <div data-testid="close-scorecard-page">
      <h1 className="text-2xl font-bold mb-1" data-testid="scorecard-title">Close Scorecard</h1>
      <p className="text-gray-500 mb-6">Close KPI scorecard and metrics.</p>

      {loading ? (
        <p className="text-gray-400">Loading…</p>
      ) : (
        <>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
            {metrics.slice(0, 4).map(m => (
              <div key={m.metric_id} className="rounded-xl border bg-[#111118] p-4" data-testid="scorecard-metric">
                <div className="text-sm text-gray-500 mb-1">{m.name}</div>
                <div className="text-2xl font-bold text-red-400">{m.value}{m.unit}</div>
                <div className="text-xs text-gray-400">Target: {m.target}{m.unit}</div>
                <span className={`inline-block mt-2 px-2 py-0.5 rounded text-xs ${
                  m.status === 'on_track' ? 'bg-green-900/40 text-green-400' :
                  m.status === 'at_risk' ? 'bg-yellow-900/40 text-yellow-400' : 'bg-red-900/40 text-red-400'
                }`}>
                  {m.status}
                </span>
              </div>
            ))}
          </div>

          {chartData.length > 0 && (
            <div className="rounded-xl border bg-[#111118] p-4 h-64">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={chartData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="value" fill="#4f46e5" name="Actual" />
                  <Bar dataKey="target" fill="#94a3b8" name="Target" />
                </BarChart>
              </ResponsiveContainer>
            </div>
          )}
        </>
      )}
    </div>
  )
}
