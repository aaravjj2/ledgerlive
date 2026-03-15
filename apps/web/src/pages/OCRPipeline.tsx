/**
 * OCR Pipeline — Document OCR jobs, stats, retry.
 * W04 OCR Pipeline frontend.
 */
import { useEffect, useState, useCallback } from 'react'
import { apiGet, apiPost } from '../services/api'

interface OCRJob {
  ocr_id: string
  doc_id: string
  status: string
  pages_processed: number
  confidence_avg: number
  created_at?: string
}

export default function OCRPipeline() {
  const [jobs, setJobs] = useState<OCRJob[]>([])
  const [stats, setStats] = useState<{ total: number; completed: number; pending: number } | null>(null)
  const [loading, setLoading] = useState(true)
  const [acting, setActing] = useState<string | null>(null)

  const load = useCallback(async () => {
    setLoading(true)
    try {
      const [j, s] = await Promise.all([
        apiGet<{ items?: OCRJob[] }>('/api/ocr-jobs'),
        apiGet<{ total: number; completed: number; pending: number }>('/api/ocr-jobs/stats').catch(() => null),
      ])
      setJobs(j?.items ?? [])
      setStats(s)
    } catch {
      setJobs([])
      setStats(null)
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => { load() }, [load])

  const retry = async (id: string) => {
    setActing(id)
    try {
      await apiPost(`/api/ocr-jobs/${id}/retry`, {})
      await load()
    } finally {
      setActing(null)
    }
  }

  const statusColor = (s: string) => {
    if (s === 'completed') return 'bg-green-900/40 text-green-400'
    if (s === 'pending' || s === 'processing') return 'bg-yellow-900/40 text-yellow-400'
    return 'bg-red-900/40 text-red-400'
  }

  return (
    <div data-testid="ocr-pipeline-page">
      <h1 className="text-2xl font-bold mb-1" data-testid="ocr-title">OCR Pipeline</h1>
      <p className="text-gray-500 mb-6">Document OCR jobs, stats, retry.</p>

      {stats && (
        <div className="grid grid-cols-3 gap-4 mb-6">
          <div className="rounded-lg border bg-[#111118] p-4">
            <div className="text-2xl font-bold text-red-400">{stats.total}</div>
            <div className="text-sm text-gray-500">Total Jobs</div>
          </div>
          <div className="rounded-lg border bg-[#111118] p-4">
            <div className="text-2xl font-bold text-green-600">{stats.completed}</div>
            <div className="text-sm text-gray-500">Completed</div>
          </div>
          <div className="rounded-lg border bg-[#111118] p-4">
            <div className="text-2xl font-bold text-yellow-600">{stats.pending}</div>
            <div className="text-sm text-gray-500">Pending</div>
          </div>
        </div>
      )}

      {loading ? (
        <p className="text-gray-400">Loading…</p>
      ) : (
        <div className="rounded-xl border bg-[#111118] overflow-hidden">
          <table className="w-full text-sm">
            <thead className="bg-[#1A1A24]">
              <tr>
                <th className="text-left px-4 py-3">OCR ID</th>
                <th className="text-left px-4 py-3">Doc ID</th>
                <th className="text-left px-4 py-3">Status</th>
                <th className="text-right px-4 py-3">Pages</th>
                <th className="text-right px-4 py-3">Confidence</th>
                <th className="px-4 py-3"></th>
              </tr>
            </thead>
            <tbody>
              {jobs.map(j => (
                <tr key={j.ocr_id} className="border-b hover:bg-[#1A1A24]">
                  <td className="px-4 py-3 font-mono text-xs">{j.ocr_id.slice(0, 8)}…</td>
                  <td className="px-4 py-3 font-mono text-xs">{j.doc_id?.slice(0, 8) || '—'}…</td>
                  <td className="px-4 py-3">
                    <span className={`px-2 py-0.5 rounded text-xs ${statusColor(j.status)}`}>{j.status}</span>
                  </td>
                  <td className="px-4 py-3 text-right">{j.pages_processed ?? '—'}</td>
                  <td className="px-4 py-3 text-right">{j.confidence_avg != null ? `${(j.confidence_avg * 100).toFixed(1)}%` : '—'}</td>
                  <td className="px-4 py-3">
                    {j.status === 'failed' && (
                      <button
                        onClick={() => retry(j.ocr_id)}
                        disabled={acting === j.ocr_id}
                        className="text-xs px-2 py-1 rounded bg-red-600 text-white hover:bg-red-700 disabled:opacity-50"
                      >
                        {acting === j.ocr_id ? '…' : 'Retry'}
                      </button>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}
