import { useEffect, useState } from 'react'
import { API_BASE } from '../services/api'

interface Review { review_id: string; review_type?: string; subject?: string; assignee?: string; priority?: string; status?: string; due_date?: string }

export default function ReviewQueue() {
  const [items, setItems] = useState<Review[]>([])
  const [loading, setLoading] = useState(true)
  const [acting, setActing] = useState<string | null>(null)

  const load = () => {
    setLoading(true)
    fetch(`${API_BASE}/api/reviews`).then(r => r.json()).then(d => { setItems(d.items || []); setLoading(false) }).catch(() => setLoading(false))
  }

  useEffect(() => { load() }, [])

  const decide = async (id: string, decision: string) => {
    setActing(id)
    await fetch(`${API_BASE}/api/reviews/${id}/decide`, { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ decision }) })
    setActing(null)
    load()
  }

  const priColor = (p?: string) => {
    if (p === 'high' || p === 'critical') return 'bg-red-100 text-red-700'
    if (p === 'medium') return 'bg-yellow-100 text-yellow-700'
    return 'bg-blue-100 text-blue-700'
  }

  return (
    <div data-testid="review-page">
      <div className="flex items-center justify-between mb-2">
        <h1 className="text-2xl font-bold" data-testid="review-title">Review Queue</h1>
        <span className="text-sm text-gray-500">{items.filter(i => i.status === 'pending').length} pending</span>
      </div>
      <p className="text-gray-500 mb-6" data-testid="review-subtitle">Human-in-the-loop review and approval workflow.</p>

      {loading ? <p className="text-gray-400">Loading…</p> : (
        <div className="space-y-3">
          {items.length === 0 && <p className="text-gray-400 py-8 text-center">Review queue is empty.</p>}
          {items.map(rv => (
            <div key={rv.review_id} className="rounded-xl border bg-white shadow-sm p-4 flex items-start gap-4">
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-1">
                  <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${priColor(rv.priority)}`}>{rv.priority || 'normal'}</span>
                  <span className="text-xs text-gray-500 uppercase">{rv.review_type || 'review'}</span>
                </div>
                <p className="text-sm font-medium text-gray-800">{rv.subject || rv.review_id.slice(0,8)}</p>
                <p className="text-xs text-gray-500 mt-1">Assigned to: <span className="text-indigo-600">{rv.assignee || '—'}</span> · Due: {rv.due_date || '—'}</p>
              </div>
              <div className="flex flex-col items-end gap-2">
                <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${rv.status === 'pending' ? 'bg-yellow-100 text-yellow-700' : 'bg-green-100 text-green-700'}`}>{rv.status}</span>
                {rv.status === 'pending' && (
                  <div className="flex gap-1">
                    <button onClick={() => decide(rv.review_id, 'approved')} disabled={acting === rv.review_id}
                      className="text-xs px-2 py-1 rounded bg-green-600 text-white hover:bg-green-700 disabled:opacity-50">✓ Approve</button>
                    <button onClick={() => decide(rv.review_id, 'rejected')} disabled={acting === rv.review_id}
                      className="text-xs px-2 py-1 rounded bg-red-500 text-white hover:bg-red-600 disabled:opacity-50">✗ Reject</button>
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
