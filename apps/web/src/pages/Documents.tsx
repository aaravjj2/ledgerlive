import { useEffect, useState } from 'react'
import { API_BASE } from '../services/api'

interface Doc { doc_id: string; doc_name?: string; filename?: string; doc_type?: string; status?: string; file_size?: number; uploaded_by?: string }

export default function Documents() {
  const [docs, setDocs] = useState<Doc[]>([])
  const [loading, setLoading] = useState(true)

  const load = () => {
    setLoading(true)
    fetch(`${API_BASE}/api/documents`).then(r => r.json()).then(d => { setDocs(d.items || []); setLoading(false) }).catch(() => setLoading(false))
  }

  useEffect(() => { load() }, [])

  const statusColor = (s?: string) => {
    if (s === 'completed' || s === 'processed') return 'bg-green-900/40 text-green-400'
    if (s === 'pending') return 'bg-yellow-900/40 text-yellow-400'
    if (s === 'error') return 'bg-red-900/40 text-red-400'
    return 'bg-[#1A1A24] text-gray-400'
  }

  return (
    <div data-testid="documents-page">
      <div className="flex items-center justify-between mb-2">
        <h1 className="text-2xl font-bold" data-testid="documents-title">Documents</h1>
        <button onClick={load} className="text-sm px-3 py-1 rounded-lg bg-red-600 text-white hover:bg-red-700">↻ Refresh</button>
      </div>
      <p className="text-gray-500 mb-6" data-testid="documents-subtitle">Upload and manage invoices, receipts, and financial documents.</p>

      {loading ? <p className="text-gray-400">Loading…</p> : (
        <div className="rounded-xl border bg-[#111118] overflow-hidden">
          <table className="w-full text-sm">
            <thead className="bg-[#1A1A24] border-b">
              <tr>
                <th className="text-left px-4 py-3 font-semibold text-gray-400">Document</th>
                <th className="text-left px-4 py-3 font-semibold text-gray-400">Type</th>
                <th className="text-left px-4 py-3 font-semibold text-gray-400">Size</th>
                <th className="text-left px-4 py-3 font-semibold text-gray-400">Uploaded By</th>
                <th className="text-left px-4 py-3 font-semibold text-gray-400">Status</th>
              </tr>
            </thead>
            <tbody>
              {docs.length === 0 && (
                <tr><td colSpan={5} className="text-center py-8 text-gray-400">No documents yet.</td></tr>
              )}
              {docs.map(d => (
                <tr key={d.doc_id} className="border-b hover:bg-[#1A1A24]">
                  <td className="px-4 py-3 font-medium text-gray-200">{d.doc_name || d.filename || d.doc_id.slice(0,8)}</td>
                  <td className="px-4 py-3 text-gray-400 capitalize">{d.doc_type || '—'}</td>
                  <td className="px-4 py-3 text-gray-400">{d.file_size ? `${(d.file_size/1024).toFixed(1)} KB` : '—'}</td>
                  <td className="px-4 py-3 text-gray-400">{d.uploaded_by || '—'}</td>
                  <td className="px-4 py-3">
                    <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${statusColor(d.status)}`}>{d.status || 'unknown'}</span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          <div className="px-4 py-2 text-xs text-gray-400 bg-[#1A1A24]">{docs.length} document(s) total</div>
        </div>
      )}
    </div>
  )
}
