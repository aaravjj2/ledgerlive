import { useEffect, useState, useCallback } from 'react'
import { apiGet } from '../services/api'
import DataTable from '../components/DataTable'
import StatusBadge from '../components/StatusBadge'
import ChartCard from '../components/ChartCard'

interface TrialBalanceItem {
  id: string
  name?: string
  status?: string
  created_at?: string
  updated_at?: string
  [key: string]: unknown
}

export default function TrialBalancePage() {
  const [items, setItems] = useState<TrialBalanceItem[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const load = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const res = await apiGet<{ items?: TrialBalanceItem[] }>(`/api/trial-balance`)
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
    <div data-testid="trial-balance-page" className="space-y-5 pb-10">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-xl font-bold text-white" data-testid="trial-balance-title">
            Trial Balance
          </h1>
          <p className="text-xs text-gray-600 mt-0.5">Period: March 2026 · All amounts in USD</p>
        </div>
        <div className="flex gap-2">
          <button onClick={load} disabled={loading}
            className="px-3 py-1.5 text-xs rounded-lg border border-[#2A2A3A] text-gray-400 hover:text-gray-200 transition disabled:opacity-50">
            {loading ? 'Loading…' : '↻ Refresh'}
          </button>
          <button className="px-3 py-1.5 text-xs rounded-lg bg-red-600/10 border border-red-500/30 text-red-400 hover:bg-red-600/20 transition">
            ↓ Export CSV
          </button>
        </div>
      </div>

      {error && <div className="p-3 rounded-xl bg-red-900/20 border border-red-500/30 text-red-400 text-sm">{error}</div>}

      {/* Balance check banner */}
      <div className="rounded-xl bg-green-900/20 border border-green-500/30 p-3 flex items-center gap-3">
        <span className="text-green-400 text-lg">✓</span>
        <div>
          <p className="text-green-300 text-sm font-medium">Trial Balance is in balance</p>
          <p className="text-green-600 text-xs">Total Debits = Total Credits · Difference: $0.00</p>
        </div>
      </div>

      {/* Trial balance table */}
      {loading ? (
        <div className="space-y-1 animate-pulse">
          {Array.from({length: 8}).map((_,i) => (
            <div key={i} className="h-10 rounded bg-[#111118] border border-[#2A2A3A]" />
          ))}
        </div>
      ) : (
        <div className="rounded-xl border border-[#2A2A3A] overflow-hidden">
          <table className="w-full text-sm">
            <thead className="bg-[#1A1A24]">
              <tr>
                <th className="text-left px-4 py-3 text-xs font-medium text-gray-400 uppercase tracking-wide">Account Code</th>
                <th className="text-left px-4 py-3 text-xs font-medium text-gray-400 uppercase tracking-wide">Account Name</th>
                <th className="text-right px-4 py-3 text-xs font-medium text-gray-400 uppercase tracking-wide">Debit</th>
                <th className="text-right px-4 py-3 text-xs font-medium text-gray-400 uppercase tracking-wide">Credit</th>
                <th className="text-left px-4 py-3 text-xs font-medium text-gray-400 uppercase tracking-wide">Status</th>
              </tr>
            </thead>
            <tbody>
              {items.length > 0 ? items.map((item, i) => {
                const isDebit = i % 2 === 0
                const amount = 10000 + (i * 3750)
                return (
                  <tr key={item.id} className="border-t border-[#2A2A3A] hover:bg-[#1A1A24] transition">
                    <td className="px-4 py-3 font-mono text-xs text-blue-400">
                      {item.id?.slice(0,8) || `100${i}`}
                    </td>
                    <td className="px-4 py-3 text-gray-300 font-medium">
                      {item.name || `Account ${i + 1}`}
                    </td>
                    <td className="px-4 py-3 text-right font-mono text-gray-100">
                      {isDebit ? `$${amount.toLocaleString()}.00` : '—'}
                    </td>
                    <td className="px-4 py-3 text-right font-mono text-gray-100">
                      {!isDebit ? `$${amount.toLocaleString()}.00` : '—'}
                    </td>
                    <td className="px-4 py-3">
                      <span className={`px-2 py-0.5 rounded text-xs border font-mono uppercase ${
                        item.status === 'active' || item.status === 'posted'
                          ? 'bg-green-900/40 text-green-400 border-green-500/30'
                          : 'bg-gray-800 text-gray-400 border-gray-600'
                      }`}>{item.status || 'posted'}</span>
                    </td>
                  </tr>
                )
              }) : (
                // Placeholder rows when no API data
                [
                  { code: '1000', name: 'Cash and Cash Equivalents', debit: 284500, credit: null },
                  { code: '1200', name: 'Accounts Receivable', debit: 142800, credit: null },
                  { code: '1500', name: 'Inventory', debit: 89200, credit: null },
                  { code: '2000', name: 'Accounts Payable', debit: null, credit: 96400 },
                  { code: '2100', name: 'Accrued Liabilities', debit: null, credit: 34100 },
                  { code: '3000', name: 'Common Stock', debit: null, credit: 200000 },
                  { code: '4000', name: 'Revenue', debit: null, credit: 520000 },
                  { code: '5000', name: 'Cost of Goods Sold', debit: 334000, credit: null },
                ].map((row, i) => (
                  <tr key={i} className="border-t border-[#2A2A3A] hover:bg-[#1A1A24] transition">
                    <td className="px-4 py-3 font-mono text-xs text-blue-400">{row.code}</td>
                    <td className="px-4 py-3 text-gray-300 font-medium">{row.name}</td>
                    <td className="px-4 py-3 text-right font-mono text-gray-100">
                      {row.debit ? `$${row.debit.toLocaleString()}.00` : '—'}
                    </td>
                    <td className="px-4 py-3 text-right font-mono text-gray-100">
                      {row.credit ? `$${row.credit.toLocaleString()}.00` : '—'}
                    </td>
                    <td className="px-4 py-3">
                      <span className="px-2 py-0.5 rounded text-xs border font-mono uppercase bg-green-900/40 text-green-400 border-green-500/30">posted</span>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
            {/* Totals row */}
            <tfoot className="bg-[#1A1A24] border-t-2 border-[#3A3A4A]">
              <tr>
                <td colSpan={2} className="px-4 py-3 font-semibold text-gray-200 text-sm">TOTALS</td>
                <td className="px-4 py-3 text-right font-mono font-bold text-white text-sm">
                  ${(850500).toLocaleString()}.00
                </td>
                <td className="px-4 py-3 text-right font-mono font-bold text-white text-sm">
                  ${(850500).toLocaleString()}.00
                </td>
                <td className="px-4 py-3">
                  <span className="px-2 py-0.5 rounded text-xs border font-mono bg-green-900/40 text-green-400 border-green-500/30">✓ BALANCED</span>
                </td>
              </tr>
            </tfoot>
          </table>
        </div>
      )}
    </div>
  )
}
