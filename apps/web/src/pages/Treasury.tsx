/**
 * Treasury Dashboard — Debt schedules, interest projection, liquidity ladder.
 * W55 Treasury 2.0 frontend.
 */
import { useEffect, useState, useCallback } from 'react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'
import { apiGet } from '../services/api'

interface DebtSchedule {
  schedule_id: string
  entity_id: string
  principal: number
  rate_pct: number
  maturity_date: string
  next_payment: number
  status: string
}

interface LiquidityLadder {
  bucket: string
  amount: number
  currency: string
  as_of: string
}

export default function Treasury() {
  const [schedules, setSchedules] = useState<DebtSchedule[]>([])
  const [ladder, setLadder] = useState<LiquidityLadder[]>([])
  const [loading, setLoading] = useState(true)

  const load = useCallback(async () => {
    setLoading(true)
    try {
      const [t, l] = await Promise.all([
        apiGet<{ items?: DebtSchedule[] }>('/api/treasury').catch(() => ({ items: [] })),
        apiGet<{ items?: LiquidityLadder[] }>('/api/treasury/liquidity-ladder').catch(() => ({ items: [] })),
      ])
      setSchedules(t?.items ?? [])
      setLadder(l?.items ?? [])
    } catch {
      setSchedules([])
      setLadder([])
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => { load() }, [load])

  const chartData = ladder.map((l, i) => ({ name: l.bucket, amount: l.amount, index: i }))

  return (
    <div data-testid="treasury-page">
      <h1 className="text-2xl font-bold mb-1" data-testid="treasury-title">Treasury</h1>
      <p className="text-gray-500 mb-6">Debt schedules, interest projection, liquidity ladder.</p>

      {loading ? (
        <p className="text-gray-400">Loading…</p>
      ) : (
        <>
          <section className="mb-6" data-testid="treasury-debt-section">
            <h2 className="text-lg font-semibold mb-3">Debt Schedules</h2>
            <div className="rounded-xl border bg-[#111118] overflow-hidden">
              <table className="w-full text-sm">
                <thead className="bg-[#1A1A24]">
                  <tr>
                    <th className="text-left px-4 py-3">Entity</th>
                    <th className="text-right px-4 py-3">Principal</th>
                    <th className="text-right px-4 py-3">Rate %</th>
                    <th className="text-left px-4 py-3">Maturity</th>
                    <th className="text-right px-4 py-3">Next Payment</th>
                    <th className="text-left px-4 py-3">Status</th>
                  </tr>
                </thead>
                <tbody>
                  {schedules.map(s => (
                    <tr key={s.schedule_id} className="border-b hover:bg-[#1A1A24]">
                      <td className="px-4 py-3 font-mono">{s.entity_id}</td>
                      <td className="px-4 py-3 text-right">${(s.principal || 0).toLocaleString()}</td>
                      <td className="px-4 py-3 text-right">{s.rate_pct}%</td>
                      <td className="px-4 py-3">{s.maturity_date || '—'}</td>
                      <td className="px-4 py-3 text-right">${(s.next_payment || 0).toLocaleString()}</td>
                      <td className="px-4 py-3">
                        <span className={`px-2 py-0.5 rounded text-xs ${s.status === 'current' ? 'bg-green-900/40 text-green-400' : 'bg-[#1A1A24]'}`}>
                          {s.status}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </section>

          <section className="mb-6" data-testid="treasury-ladder-section">
            <h2 className="text-lg font-semibold mb-3">Liquidity Ladder</h2>
            <div className="rounded-xl border bg-[#111118] p-4 h-64">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={chartData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip />
                  <Line type="monotone" dataKey="amount" stroke="#4f46e5" strokeWidth={2} />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </section>
        </>
      )}
    </div>
  )
}
