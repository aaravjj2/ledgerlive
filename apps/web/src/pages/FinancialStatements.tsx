import { useEffect, useState, useCallback } from 'react'
import { apiGet } from '../services/api'
import DataTable from '../components/DataTable'
import StatusBadge from '../components/StatusBadge'
import ChartCard from '../components/ChartCard'

interface FinancialStatementsItem {
  id: string
  name?: string
  status?: string
  created_at?: string
  updated_at?: string
  [key: string]: unknown
}

export default function FinancialStatementsPage() {
  const [items, setItems] = useState<FinancialStatementsItem[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [activeTab, setActiveTab] = useState<'pl'|'bs'|'cf'>('pl')

  const load = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const res = await apiGet<{ items?: FinancialStatementsItem[] }>(`/api/statements`)
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
    <div data-testid="financial-statements-page" className="space-y-5 pb-10">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-xl font-bold text-white" data-testid="financial-statements-title">Financial Statements</h1>
          <p className="text-xs text-gray-600 mt-0.5">Period: Q1 2026 · All figures in USD thousands</p>
        </div>
        <div className="flex gap-2">
          <button onClick={load} disabled={loading}
            className="px-3 py-1.5 text-xs rounded-lg border border-[#2A2A3A] text-gray-400 hover:text-gray-200 transition disabled:opacity-50">
            {loading ? 'Loading…' : '↻ Refresh'}
          </button>
          <button className="px-3 py-1.5 text-xs rounded-lg bg-red-600/10 border border-red-500/30 text-red-400 hover:bg-red-600/20 transition">
            ↓ Export PDF
          </button>
        </div>
      </div>
      {error && <div className="p-3 rounded-xl bg-red-900/20 border border-red-500/30 text-red-400 text-sm">{error}</div>}
      {/* Tab switcher */}
      <div className="flex gap-1 p-1 bg-[#111118] rounded-xl border border-[#2A2A3A] w-fit">
        {[{id:'pl',label:'P&L'},{id:'bs',label:'Balance Sheet'},{id:'cf',label:'Cash Flow'}].map(t => (
          <button key={t.id} onClick={() => setActiveTab(t.id as 'pl'|'bs'|'cf')}
            className={`px-4 py-1.5 text-xs rounded-lg font-medium transition ${
              activeTab === t.id ? 'bg-red-600 text-white' : 'text-gray-400 hover:text-gray-200'
            }`}>{t.label}</button>
        ))}
      </div>
      {/* Statement table */}
      <div className="rounded-xl border border-[#2A2A3A] overflow-hidden">
        <table className="w-full text-sm">
          <thead className="bg-[#1A1A24]">
            <tr>
              <th className="text-left px-4 py-3 text-xs font-medium text-gray-400 uppercase tracking-wide w-1/2">
                {activeTab === 'pl' ? 'Income Statement' : activeTab === 'bs' ? 'Balance Sheet' : 'Cash Flow Statement'}
              </th>
              <th className="text-right px-4 py-3 text-xs font-medium text-gray-400 uppercase tracking-wide">Q1 2026</th>
              <th className="text-right px-4 py-3 text-xs font-medium text-gray-400 uppercase tracking-wide">Q1 2025</th>
              <th className="text-right px-4 py-3 text-xs font-medium text-gray-400 uppercase tracking-wide">Δ%</th>
            </tr>
          </thead>
          <tbody>
            {(activeTab === 'pl' ? [
              { label: 'Revenue', q1: 4200, q0: 3800, bold: false, section: true },
              { label: '  Product Revenue', q1: 3150, q0: 2850, bold: false },
              { label: '  Services Revenue', q1: 1050, q0: 950, bold: false },
              { label: 'Cost of Revenue', q1: 2436, q0: 2242, bold: false, section: true },
              { label: 'Gross Profit', q1: 1764, q0: 1558, bold: true },
              { label: 'Operating Expenses', q1: 1240, q0: 1180, bold: false, section: true },
              { label: '  R&D', q1: 520, q0: 490, bold: false },
              { label: '  S&M', q1: 480, q0: 460, bold: false },
              { label: '  G&A', q1: 240, q0: 230, bold: false },
              { label: 'Operating Income', q1: 524, q0: 378, bold: true },
              { label: 'Net Income', q1: 412, q0: 298, bold: true },
            ] : activeTab === 'bs' ? [
              { label: 'ASSETS', q1: null, q0: null, bold: false, section: true },
              { label: '  Cash & Equivalents', q1: 2840, q0: 2320, bold: false },
              { label: '  Accounts Receivable', q1: 1428, q0: 1280, bold: false },
              { label: '  Total Assets', q1: 8420, q0: 7640, bold: true },
              { label: 'LIABILITIES', q1: null, q0: null, bold: false, section: true },
              { label: '  Accounts Payable', q1: 964, q0: 880, bold: false },
              { label: '  Total Liabilities', q1: 3180, q0: 2940, bold: true },
              { label: "SHAREHOLDERS' EQUITY", q1: null, q0: null, bold: false, section: true },
              { label: '  Total Equity', q1: 5240, q0: 4700, bold: true },
            ] : [
              { label: 'Operating Activities', q1: null, q0: null, bold: false, section: true },
              { label: '  Net Income', q1: 412, q0: 298, bold: false },
              { label: '  Depreciation & Amort.', q1: 84, q0: 78, bold: false },
              { label: '  Changes in Working Capital', q1: -120, q0: -95, bold: false },
              { label: 'Net Cash from Operations', q1: 376, q0: 281, bold: true },
              { label: 'Investing Activities', q1: null, q0: null, bold: false, section: true },
              { label: '  CapEx', q1: -180, q0: -145, bold: false },
              { label: 'Net Cash from Investing', q1: -180, q0: -145, bold: true },
              { label: 'Net Change in Cash', q1: 196, q0: 136, bold: true },
            ]).map((row, i) => (
              <tr key={i} className={`border-t border-[#2A2A3A] ${row.section ? 'bg-[#1A1A24]' : 'hover:bg-[#1A1A24]'}`}>
                <td className={`px-4 py-2.5 ${row.bold ? 'font-semibold text-gray-100' : row.section ? 'text-gray-500 text-xs uppercase tracking-wide' : 'text-gray-400'}`}>
                  {row.label}
                </td>
                <td className={`px-4 py-2.5 text-right font-mono ${row.bold ? 'font-semibold text-gray-100' : 'text-gray-300'} ${row.q1 !== null && row.q1 < 0 ? 'text-red-400' : ''}`}>
                  {row.q1 !== null ? (row.q1 < 0 ? `(${Math.abs(row.q1).toLocaleString()})` : row.q1.toLocaleString()) : ''}
                </td>
                <td className={`px-4 py-2.5 text-right font-mono text-gray-500 ${row.q0 !== null && row.q0 < 0 ? 'text-red-600' : ''}`}>
                  {row.q0 !== null ? (row.q0 < 0 ? `(${Math.abs(row.q0).toLocaleString()})` : row.q0.toLocaleString()) : ''}
                </td>
                <td className="px-4 py-2.5 text-right font-mono text-xs">
                  {row.q1 !== null && row.q0 !== null && row.q0 !== 0 ? (() => {
                    const delta = ((row.q1 - row.q0) / Math.abs(row.q0)) * 100
                    return <span className={delta > 0 ? 'text-green-400' : 'text-red-400'}>{delta > 0 ? '+' : ''}{delta.toFixed(1)}%</span>
                  })() : null}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
