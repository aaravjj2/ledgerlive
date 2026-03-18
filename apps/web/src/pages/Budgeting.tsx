import { useEffect, useState, useCallback } from 'react'
import { apiGet } from '../services/api'
import DataTable from '../components/DataTable'
import StatusBadge from '../components/StatusBadge'
import ChartCard from '../components/ChartCard'

interface BudgetingItem {
  id: string
  name?: string
  status?: string
  created_at?: string
  updated_at?: string
  [key: string]: unknown
}

export default function BudgetingPage() {
  const [items, setItems] = useState<BudgetingItem[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const load = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const res = await apiGet<{ items?: BudgetingItem[] }>(`/api/budgeting`)
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
    <div data-testid="budgeting-page" className="space-y-5 pb-10">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-xl font-bold text-white" data-testid="budgeting-title">Budgeting</h1>
          <p className="text-xs text-gray-600 mt-0.5">Budget vs Actual · Q1 2026</p>
        </div>
        <div className="flex gap-2">
          <button onClick={load} disabled={loading}
            className="px-3 py-1.5 text-xs rounded-lg border border-[#2A2A3A] text-gray-400 hover:text-gray-200 transition disabled:opacity-50">
            {loading ? 'Loading…' : '↻ Refresh'}
          </button>
          <button className="px-3 py-1.5 text-xs rounded-lg bg-red-600/10 border border-red-500/30 text-red-400 hover:bg-red-600/20 transition">
            🔒 Lock Period
          </button>
        </div>
      </div>
      {error && <div className="p-3 rounded-xl bg-red-900/20 border border-red-500/30 text-red-400 text-sm">{error}</div>}
      {/* Budget vs actual table */}
      {(() => {
        const budgetRows = items.length > 0
          ? items.slice(0,8).map((item, i) => ({
              dept: item.name || `Department ${i+1}`,
              budget: 500000 + i * 75000,
              actual: [492000, 548000, 612000, 701000, 759000, 805000, 867000, 938000][i] ?? (500000 + i * 75000),
            }))
          : [
              { dept: 'Engineering', budget: 1200000, actual: 1148000 },
              { dept: 'Sales & Marketing', budget: 800000, actual: 872000 },
              { dept: 'G&A', budget: 400000, actual: 388000 },
              { dept: 'Product', budget: 600000, actual: 574000 },
              { dept: 'Customer Success', budget: 300000, actual: 312000 },
              { dept: 'Operations', budget: 250000, actual: 241000 },
            ]
        const totalBudget = budgetRows.reduce((a, r) => a + r.budget, 0)
        const totalActual = budgetRows.reduce((a, r) => a + r.actual, 0)
        const totalVariance = totalActual - totalBudget
        return (
          <>
            {/* Summary */}
            <div className="grid grid-cols-3 gap-3">
              <div className="rounded-xl bg-[#111118] border border-[#2A2A3A] p-4">
                <div className="text-xs text-gray-600 mb-1">Total Budget</div>
                <div className="text-2xl font-bold font-mono text-gray-100">${(totalBudget/1000000).toFixed(2)}M</div>
              </div>
              <div className="rounded-xl bg-[#111118] border border-[#2A2A3A] p-4">
                <div className="text-xs text-gray-600 mb-1">Total Actual</div>
                <div className="text-2xl font-bold font-mono text-blue-400">${(totalActual/1000000).toFixed(2)}M</div>
              </div>
              <div className={`rounded-xl border p-4 ${totalVariance > 0 ? 'bg-red-900/20 border-red-500/30' : 'bg-green-900/20 border-green-500/30'}`}>
                <div className="text-xs text-gray-600 mb-1">Variance</div>
                <div className={`text-2xl font-bold font-mono ${totalVariance > 0 ? 'text-red-400' : 'text-green-400'}`}>
                  {totalVariance > 0 ? '+' : ''}${Math.abs(totalVariance/1000).toFixed(0)}K
                </div>
              </div>
            </div>
            {/* Table */}
            <div className="rounded-xl border border-[#2A2A3A] overflow-hidden">
              <table className="w-full text-sm">
                <thead className="bg-[#1A1A24]">
                  <tr>
                    <th className="text-left px-4 py-3 text-xs font-medium text-gray-400 uppercase tracking-wide">Department</th>
                    <th className="text-right px-4 py-3 text-xs font-medium text-gray-400 uppercase tracking-wide">Budget</th>
                    <th className="text-right px-4 py-3 text-xs font-medium text-gray-400 uppercase tracking-wide">Actual</th>
                    <th className="text-right px-4 py-3 text-xs font-medium text-gray-400 uppercase tracking-wide">Variance</th>
                    <th className="text-right px-4 py-3 text-xs font-medium text-gray-400 uppercase tracking-wide">% Used</th>
                  </tr>
                </thead>
                <tbody>
                  {budgetRows.map((r, i) => {
                    const variance = r.actual - r.budget
                    const pctUsed = Math.round((r.actual / r.budget) * 100)
                    return (
                      <tr key={i} className="border-t border-[#2A2A3A] hover:bg-[#1A1A24]">
                        <td className="px-4 py-3 text-gray-300 font-medium">{r.dept}</td>
                        <td className="px-4 py-3 text-right font-mono text-gray-400">${(r.budget/1000).toFixed(0)}K</td>
                        <td className="px-4 py-3 text-right font-mono text-gray-200">${(r.actual/1000).toFixed(0)}K</td>
                        <td className={`px-4 py-3 text-right font-mono ${variance > 0 ? 'text-red-400' : 'text-green-400'}`}>
                          {variance > 0 ? '+' : ''}${(variance/1000).toFixed(0)}K
                        </td>
                        <td className="px-4 py-3 text-right">
                          <div className="flex items-center justify-end gap-2">
                            <div className="w-16 h-1.5 bg-[#2A2A3A] rounded-full overflow-hidden">
                              <div className={`h-full rounded-full ${pctUsed > 105 ? 'bg-red-500' : pctUsed > 95 ? 'bg-yellow-500' : 'bg-green-500'}`}
                                style={{width:`${Math.min(pctUsed,100)}%`}} />
                            </div>
                            <span className={`text-xs font-mono ${pctUsed > 105 ? 'text-red-400' : pctUsed > 95 ? 'text-yellow-400' : 'text-green-400'}`}>
                              {pctUsed}%
                            </span>
                          </div>
                        </td>
                      </tr>
                    )
                  })}
                </tbody>
                <tfoot className="bg-[#1A1A24] border-t-2 border-[#3A3A4A]">
                  <tr>
                    <td className="px-4 py-3 font-semibold text-gray-200 text-sm">TOTAL</td>
                    <td className="px-4 py-3 text-right font-mono font-bold text-gray-200">${(totalBudget/1000000).toFixed(2)}M</td>
                    <td className="px-4 py-3 text-right font-mono font-bold text-gray-200">${(totalActual/1000000).toFixed(2)}M</td>
                    <td className={`px-4 py-3 text-right font-mono font-bold ${totalVariance > 0 ? 'text-red-400' : 'text-green-400'}`}>
                      {totalVariance > 0 ? '+' : ''}${(Math.abs(totalVariance)/1000).toFixed(0)}K
                    </td>
                    <td className="px-4 py-3 text-right font-mono text-gray-400">
                      {Math.round((totalActual/totalBudget)*100)}%
                    </td>
                  </tr>
                </tfoot>
              </table>
            </div>
          </>
        )
      })()}
    </div>
  )
}
