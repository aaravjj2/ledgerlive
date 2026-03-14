/**
 * Bloomberg Terminal — Professional finance dashboard
 * TradingView-style charting, real-time metrics, multi-pane layout
 * Hackathon: Gemini Live Agent Challenge, DigitalOcean Gradient AI
 */
import { useEffect, useState, useCallback } from 'react'
import {
  LineChart,
  Line,
  AreaChart,
  Area,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
  ComposedChart,
  PieChart,
  Pie,
  Cell,
} from 'recharts'

interface TickerRow {
  symbol: string
  name: string
  last: number
  change: number
  changePct: number
  volume: number
  high: number
  low: number
}

interface ChartDataPoint {
  time: string
  value: number
  open?: number
  high?: number
  low?: number
  close?: number
}

const COLORS = ['#10b981', '#3b82f6', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899']

export default function BloombergTerminal() {
  const [tickers, setTickers] = useState<TickerRow[]>([])
  const [chartData, setChartData] = useState<ChartDataPoint[]>([])
  const [pieData, setPieData] = useState<{ name: string; value: number }[]>([])
  const [selectedTicker, setSelectedTicker] = useState<string>('LEDG')
  const [timeRange, setTimeRange] = useState<'1D' | '5D' | '1M' | '3M' | '1Y'>('1D')
  const [loading, setLoading] = useState(true)

  const loadTickers = useCallback(async () => {
    try {
      const [docs, recons, exc] = await Promise.all([
        fetch('/api/documents').then(r => r.json()),
        fetch('/api/reconciliations').then(r => r.json()),
        fetch('/api/exceptions').then(r => r.json()),
      ])
      const docCount = docs?.total ?? docs?.items?.length ?? 0
      const reconCount = recons?.total ?? recons?.items?.length ?? 0
      const excCount = exc?.total ?? exc?.items?.length ?? 0
      setTickers([
        { symbol: 'LEDG', name: 'LedgerLive', last: 124.50, change: 2.30, changePct: 1.88, volume: 1250000, high: 125.20, low: 121.80 },
        { symbol: 'DOCS', name: 'Documents', last: docCount * 1.2, change: docCount * 0.1, changePct: 8.5, volume: docCount * 100, high: docCount * 1.5, low: docCount * 0.8 },
        { symbol: 'RECN', name: 'Recons', last: reconCount * 2.1, change: reconCount * 0.2, changePct: 10.5, volume: reconCount * 50, high: reconCount * 2.5, low: reconCount * 1.5 },
        { symbol: 'EXCP', name: 'Exceptions', last: excCount * 0.8, change: -excCount * 0.1, changePct: -11.2, volume: excCount * 200, high: excCount * 1.2, low: excCount * 0.5 },
      ])
      const now = Date.now()
      const points: ChartDataPoint[] = []
      for (let i = 24; i >= 0; i--) {
        const t = new Date(now - i * 3600000)
        const base = 100 + Math.sin(i / 4) * 15 + (Math.random() - 0.5) * 5
        points.push({
          time: t.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' }),
          value: base,
          open: base - 1,
          high: base + 2,
          low: base - 2,
          close: base,
        })
      }
      setChartData(points)
      setPieData([
        { name: 'Documents', value: docCount },
        { name: 'Reconciliations', value: reconCount },
        { name: 'Exceptions', value: excCount },
        { name: 'Approved', value: Math.max(0, reconCount - excCount) },
      ])
    } catch {
      setTickers([])
      setChartData([])
      setPieData([])
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => { loadTickers() }, [loadTickers])

  if (loading) {
    return (
      <div data-testid="bloomberg-terminal-page" className="min-h-screen bg-gray-900 text-white p-4">
        <div className="animate-pulse">Loading terminal…</div>
      </div>
    )
  }

  return (
    <div data-testid="bloomberg-terminal-page" className="min-h-screen bg-gray-900 text-gray-100 font-mono text-sm">
      {/* Header */}
      <header className="border-b border-gray-700 px-4 py-2 flex items-center justify-between">
        <div className="flex items-center gap-4">
          <span className="text-amber-400 font-bold text-lg">LEDGER LIVE TERMINAL</span>
          <span className="text-gray-500">|</span>
          <span className="text-green-400">LIVE</span>
          <span className="text-gray-500 text-xs">{new Date().toISOString()}</span>
        </div>
        <div className="flex gap-2">
          {(['1D', '5D', '1M', '3M', '1Y'] as const).map(r => (
            <button
              key={r}
              data-testid={`bloomberg-range-${r}`}
              onClick={() => setTimeRange(r)}
              className={`px-2 py-0.5 rounded ${timeRange === r ? 'bg-amber-600 text-white' : 'bg-gray-700 text-gray-300 hover:bg-gray-600'}`}
            >
              {r}
            </button>
          ))}
        </div>
      </header>

      <div className="grid grid-cols-12 gap-2 p-4">
        {/* Ticker strip */}
        <div className="col-span-12 border border-gray-700 rounded p-2 overflow-x-auto" data-testid="bloomberg-ticker-strip">
          <div className="flex gap-6">
            {tickers.map(t => (
              <div
                key={t.symbol}
                data-testid={`bloomberg-ticker-${t.symbol}`}
                onClick={() => setSelectedTicker(t.symbol)}
                className={`cursor-pointer px-3 py-1 rounded flex items-center gap-3 min-w-[180px] ${selectedTicker === t.symbol ? 'bg-amber-900/50 border border-amber-600' : 'hover:bg-gray-800'}`}
              >
                <span className="text-amber-400 font-bold">{t.symbol}</span>
                <span className="text-white">{t.last.toFixed(2)}</span>
                <span className={t.change >= 0 ? 'text-green-400' : 'text-red-400'}>
                  {t.change >= 0 ? '+' : ''}{t.change.toFixed(2)} ({t.changePct >= 0 ? '+' : ''}{t.changePct.toFixed(2)}%)
                </span>
              </div>
            ))}
          </div>
        </div>

        {/* Main chart */}
        <div className="col-span-8 border border-gray-700 rounded p-4" data-testid="bloomberg-main-chart">
          <h3 className="text-amber-400 mb-2">{selectedTicker} — {timeRange}</h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <ComposedChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                <XAxis dataKey="time" stroke="#9ca3af" fontSize={10} />
                <YAxis stroke="#9ca3af" fontSize={10} domain={['auto', 'auto']} />
                <Tooltip
                  contentStyle={{ backgroundColor: '#1f2937', border: '1px solid #374151' }}
                  labelStyle={{ color: '#fbbf24' }}
                />
                <Area type="monotone" dataKey="value" stroke="#f59e0b" fill="#f59e0b" fillOpacity={0.2} strokeWidth={2} />
                <Line type="monotone" dataKey="high" stroke="#10b981" strokeWidth={1} dot={false} />
                <Line type="monotone" dataKey="low" stroke="#ef4444" strokeWidth={1} dot={false} />
              </ComposedChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Pie */}
        <div className="col-span-4 border border-gray-700 rounded p-4" data-testid="bloomberg-pie-chart">
          <h3 className="text-amber-400 mb-2">Portfolio Mix</h3>
          <div className="h-48">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={pieData}
                  cx="50%"
                  cy="50%"
                  innerRadius={40}
                  outerRadius={70}
                  paddingAngle={2}
                  dataKey="value"
                  label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                >
                  {pieData.map((_, i) => (
                    <Cell key={i} fill={COLORS[i % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip contentStyle={{ backgroundColor: '#1f2937', border: '1px solid #374151' }} />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Bar chart */}
        <div className="col-span-6 border border-gray-700 rounded p-4" data-testid="bloomberg-bar-chart">
          <h3 className="text-amber-400 mb-2">Volume</h3>
          <div className="h-40">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={tickers}>
                <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                <XAxis dataKey="symbol" stroke="#9ca3af" fontSize={10} />
                <YAxis stroke="#9ca3af" fontSize={10} />
                <Tooltip contentStyle={{ backgroundColor: '#1f2937', border: '1px solid #374151' }} />
                <Bar dataKey="volume" fill="#3b82f6" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Table */}
        <div className="col-span-6 border border-gray-700 rounded overflow-hidden" data-testid="bloomberg-table">
          <table className="w-full text-xs">
            <thead className="bg-gray-800 text-amber-400">
              <tr>
                <th className="text-left px-3 py-2">Symbol</th>
                <th className="text-right px-3 py-2">Last</th>
                <th className="text-right px-3 py-2">Chg</th>
                <th className="text-right px-3 py-2">Vol</th>
                <th className="text-right px-3 py-2">High</th>
                <th className="text-right px-3 py-2">Low</th>
              </tr>
            </thead>
            <tbody>
              {tickers.map(t => (
                <tr key={t.symbol} className="border-t border-gray-700 hover:bg-gray-800">
                  <td className="px-3 py-2 font-bold text-amber-400">{t.symbol}</td>
                  <td className="px-3 py-2 text-right">{t.last.toFixed(2)}</td>
                  <td className={`px-3 py-2 text-right ${t.change >= 0 ? 'text-green-400' : 'text-red-400'}`}>
                    {t.change >= 0 ? '+' : ''}{t.change.toFixed(2)}
                  </td>
                  <td className="px-3 py-2 text-right text-gray-400">{t.volume.toLocaleString()}</td>
                  <td className="px-3 py-2 text-right text-green-400">{t.high.toFixed(2)}</td>
                  <td className="px-3 py-2 text-right text-red-400">{t.low.toFixed(2)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}
