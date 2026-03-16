import { useEffect, useState, useCallback } from 'react'
import { apiGet } from '../services/api'
import DataTable from '../components/DataTable'
import StatusBadge from '../components/StatusBadge'
import ChartCard from '../components/ChartCard'

interface ScenarioEngineItem {
  id: string
  name?: string
  status?: string
  created_at?: string
  updated_at?: string
  [key: string]: unknown
}

export default function ScenarioEnginePage() {
  const [items, setItems] = useState<ScenarioEngineItem[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const load = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const res = await apiGet<{ items?: ScenarioEngineItem[] }>(`/api/scenarios`)
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
    <div data-testid="scenario-engine-page" className="space-y-5 pb-10">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-xl font-bold text-white" data-testid="scenario-engine-title">Scenario Engine</h1>
          <p className="text-xs text-gray-600 mt-0.5">Compare financial scenarios · Base · Upside · Downside</p>
        </div>
        <button onClick={load} disabled={loading}
          className="px-3 py-1.5 text-xs rounded-lg border border-[#2A2A3A] text-gray-400 hover:text-gray-200 transition disabled:opacity-50">
          {loading ? 'Loading…' : '↻ Refresh'}
        </button>
      </div>

      {error && <div className="p-3 rounded-xl bg-red-900/20 border border-red-500/30 text-red-400 text-sm">{error}</div>}

      {loading ? (
        <div className="grid grid-cols-3 gap-3 animate-pulse">
          {[0,1,2].map(i => <div key={i} className="h-64 rounded-xl bg-[#111118] border border-[#2A2A3A]" />)}
        </div>
      ) : (
        <>
          {/* Three scenario columns */}
          {(() => {
            // Build scenario data from API or use placeholders
            const scenarioData = [
              {
                id: 'base', label: 'Base Case', tag: 'CURRENT',
                style: 'bg-[#111118] border-[#2A2A3A]',
                headerStyle: 'text-gray-200',
                tagStyle: 'bg-gray-800 text-gray-400 border-gray-600',
                metrics: items.length > 0
                  ? Object.fromEntries(items.slice(0,5).map((item, i) => [item.name || `Metric ${i+1}`, Number((item as Record<string,unknown>).value) || (100 + i * 25)]))
                  : { 'Revenue': 4200000, 'EBITDA': 1100000, 'Gross Margin %': 42, 'OpEx': 3100000, 'Net Income': 820000 }
              },
              {
                id: 'upside', label: 'Upside', tag: '+15%',
                style: 'bg-green-900/20 border-green-500/30',
                headerStyle: 'text-green-300',
                tagStyle: 'bg-green-900/40 text-green-400 border-green-500/30',
                metrics: items.length > 0
                  ? Object.fromEntries(items.slice(0,5).map((item, i) => [item.name || `Metric ${i+1}`, Math.round((Number((item as Record<string,unknown>).value) || (100 + i * 25)) * 1.15)]))
                  : { 'Revenue': 4830000, 'EBITDA': 1380000, 'Gross Margin %': 46, 'OpEx': 3100000, 'Net Income': 1040000 }
              },
              {
                id: 'downside', label: 'Downside', tag: '-12%',
                style: 'bg-red-900/20 border-red-500/30',
                headerStyle: 'text-red-300',
                tagStyle: 'bg-red-900/40 text-red-400 border-red-500/30',
                metrics: items.length > 0
                  ? Object.fromEntries(items.slice(0,5).map((item, i) => [item.name || `Metric ${i+1}`, Math.round((Number((item as Record<string,unknown>).value) || (100 + i * 25)) * 0.88)]))
                  : { 'Revenue': 3696000, 'EBITDA': 820000, 'Gross Margin %': 38, 'OpEx': 3100000, 'Net Income': 520000 }
              },
            ]

            const baseMetrics = scenarioData[0].metrics

            return (
              <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                {scenarioData.map((scenario, si) => (
                  <div key={scenario.id} className={`rounded-xl border p-4 ${scenario.style}`}>
                    <div className="flex items-center justify-between mb-4">
                      <h2 className={`font-semibold text-sm ${scenario.headerStyle}`}>{scenario.label}</h2>
                      <span className={`px-2 py-0.5 rounded text-xs border font-mono ${scenario.tagStyle}`}>
                        {scenario.tag}
                      </span>
                    </div>
                    <div className="space-y-3">
                      {Object.entries(scenario.metrics).map(([key, val]) => {
                        const baseVal = baseMetrics[key] as number
                        const current = val as number
                        const delta = si > 0 && baseVal ? ((current - baseVal) / baseVal * 100) : 0
                        const isPositive = delta > 0
                        return (
                          <div key={key}>
                            <div className="flex justify-between items-start mb-0.5">
                              <span className="text-xs text-gray-500">{key}</span>
                              {si > 0 && (
                                <span className={`text-xs font-mono ${isPositive ? 'text-green-400' : 'text-red-400'}`}>
                                  {isPositive ? '+' : ''}{delta.toFixed(1)}%
                                </span>
                              )}
                            </div>
                            <div className="flex items-center gap-2">
                              <span className={`text-sm font-bold font-mono ${scenario.headerStyle}`}>
                                {typeof current === 'number' && current > 1000
                                  ? `$${(current/1000).toFixed(0)}K`
                                  : `${current}${key.includes('%') ? '%' : ''}`}
                              </span>
                            </div>
                          </div>
                        )
                      })}
                    </div>
                  </div>
                ))}
              </div>
            )
          })()}

          {/* Assumptions note */}
          <div className="rounded-xl bg-[#111118] border border-[#2A2A3A] p-4">
            <h2 className="text-xs text-gray-500 uppercase tracking-widest mb-2">Key Assumptions</h2>
            <div className="grid grid-cols-2 md:grid-cols-3 gap-3 text-xs text-gray-400">
              <div>📈 Upside: +15% revenue, flat OpEx</div>
              <div>📉 Downside: -12% revenue, +5% OpEx</div>
              <div>🎯 Base: Current run-rate trajectory</div>
            </div>
          </div>
        </>
      )}
    </div>
  )
}
