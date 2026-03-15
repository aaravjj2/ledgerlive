import { useEffect, useState } from 'react'

interface Health { project: string; status: string; mode: string; llm: string; ts: string }
interface Counts { docs: number; recons: number; exceptions: number; reviews: number; audits: number }

export default function Dashboard() {
  const [health, setHealth] = useState<Health | null>(null)
  const [counts, setCounts] = useState<Counts>({ docs: 0, recons: 0, exceptions: 0, reviews: 0, audits: 0 })

  useEffect(() => {
    fetch('/healthz').then(r => r.json()).then(setHealth).catch(() => {})
    Promise.all([
      fetch('/api/documents').then(r => r.json()),
      fetch('/api/reconciliations').then(r => r.json()),
      fetch('/api/exceptions').then(r => r.json()),
      fetch('/api/reviews').then(r => r.json()),
      fetch('/api/audit').then(r => r.json()),
    ]).then(([d, rc, ex, rv, au]) => setCounts({
      docs: d.total || 0,
      recons: rc.total || 0,
      exceptions: ex.total || 0,
      reviews: rv.total || 0,
      audits: au.total || 0,
    })).catch(() => {})
  }, [])

  const tiles = [
    { label: 'Documents', count: counts.docs, color: 'bg-blue-100 text-blue-800', icon: '📄' },
    { label: 'Reconciliations', count: counts.recons, color: 'bg-green-100 text-green-800', icon: '⚖️' },
    { label: 'Exceptions', count: counts.exceptions, color: 'bg-red-100 text-red-800', icon: '⚠️' },
    { label: 'Pending Reviews', count: counts.reviews, color: 'bg-yellow-100 text-yellow-800', icon: '🔍' },
    { label: 'Audit Events', count: counts.audits, color: 'bg-purple-100 text-purple-800', icon: '📋' },
  ]

  return (
    <div data-testid="dashboard-page">
      <h1 className="text-2xl font-bold mb-1" data-testid="dashboard-title">Dashboard</h1>
      <p className="text-gray-500 mb-6" data-testid="dashboard-subtitle">Finance close overview and key metrics.</p>

      {health && (
        <div className="mb-6 flex gap-3 flex-wrap">
          <span className="inline-flex items-center gap-1 px-3 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800">
            ✅ API {health.status.toUpperCase()}
          </span>
          <span className="inline-flex items-center gap-1 px-3 py-1 rounded-full text-xs font-medium bg-indigo-100 text-indigo-800">
            🏦 {health.project}
          </span>
          <span className="inline-flex items-center gap-1 px-3 py-1 rounded-full text-xs font-medium bg-gray-100 text-gray-700">
            ⚙️ Mode: {health.mode}
          </span>
          <span className="inline-flex items-center gap-1 px-3 py-1 rounded-full text-xs font-medium bg-gray-100 text-gray-700">
            🤖 LLM: {health.llm}
          </span>
        </div>
      )}

      <div className="grid grid-cols-2 md:grid-cols-5 gap-4 mb-8">
        {tiles.map(t => (
          <div key={t.label} className={`rounded-xl p-5 shadow-sm border ${t.color} flex flex-col items-center`}>
            <div className="text-3xl mb-1">{t.icon}</div>
            <div className="text-3xl font-bold">{t.count}</div>
            <div className="text-xs font-medium mt-1 text-center">{t.label}</div>
          </div>
        ))}
      </div>

      <div className="rounded-xl border bg-white shadow-sm p-5">
        <h2 className="font-semibold text-gray-700 mb-3">Close Period Status — Feb 2026</h2>
        <div className="flex items-center gap-3">
          <div className="flex-1 h-4 rounded-full bg-gray-100 overflow-hidden">
            <div className="h-full bg-indigo-600 rounded-full" style={{ width: `${counts.exceptions > 0 ? 62 : 100}%` }} />
          </div>
          <span className="text-sm font-medium text-gray-600">{counts.exceptions > 0 ? '62% complete — exceptions pending' : '100% — All clear ✅'}</span>
        </div>
      </div>
    </div>
  )
}
