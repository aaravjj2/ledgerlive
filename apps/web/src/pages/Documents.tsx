import { useEffect, useState } from 'react'

interface Doc { doc_id: string; doc_name?: string; filename?: string; doc_type?: string; status?: string; file_size?: number; uploaded_by?: string }

export default function Documents() {
  const [docs, setDocs] = useState<Doc[]>([])
  const [loading, setLoading] = useState(true)

  const load = () => {
    setLoading(true)
    fetch('/api/documents').then(r => r.json()).then(d => { setDocs(d.items || []); setLoading(false) }).catch(() => setLoading(false))
  }

  useEffect(() => { load() }, [])

  const statusColor = (s?: string) => {
    if (s === 'completed' || s === 'processed') return 'bg-green-100 text-green-700'
    if (s === 'pending') return 'bg-yellow-100 text-yellow-700'
    if (s === 'error') return 'bg-red-100 text-red-700'
    return 'bg-gray-100 text-gray-600'
  }

  return (
    <div data-testid="page-documents">
      <div className="flex items-center justify-between mb-2">
        <h1 className="text-2xl font-bold" data-testid="documents-title">Documents</h1>
        <button onClick={load} className="text-sm px-3 py-1 rounded-lg bg-indigo-600 text-white hover:bg-indigo-700">↻ Refresh</button>
      </div>
      <p className="text-gray-500 mb-6" data-testid="documents-subtitle">Upload and manage invoices, receipts, and financial documents.</p>

      {loading ? <p className="text-gray-400">Loading…</p> : (
        <div className="rounded-xl border bg-white shadow-sm overflow-hidden">
          <table className="w-full text-sm">
            <thead className="bg-gray-50 border-b">
              <tr>
                <th className="text-left px-4 py-3 font-semibold text-gray-600">Document</th>
                <th className="text-left px-4 py-3 font-semibold text-gray-600">Type</th>
                <th className="text-left px-4 py-3 font-semibold text-gray-600">Size</th>
                <th className="text-left px-4 py-3 font-semibold text-gray-600">Uploaded By</th>
                <th className="text-left px-4 py-3 font-semibold text-gray-600">Status</th>
              </tr>
            </thead>
            <tbody>
              {docs.length === 0 && (
                <tr><td colSpan={5} className="text-center py-8 text-gray-400">No documents yet.</td></tr>
              )}
              {docs.map(d => (
                <tr key={d.doc_id} className="border-b hover:bg-gray-50">
                  <td className="px-4 py-3 font-medium text-gray-800">{d.doc_name || d.filename || d.doc_id.slice(0,8)}</td>
                  <td className="px-4 py-3 text-gray-600 capitalize">{d.doc_type || '—'}</td>
                  <td className="px-4 py-3 text-gray-600">{d.file_size ? `${(d.file_size/1024).toFixed(1)} KB` : '—'}</td>
                  <td className="px-4 py-3 text-gray-600">{d.uploaded_by || '—'}</td>
                  <td className="px-4 py-3">
                    <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${statusColor(d.status)}`}>{d.status || 'unknown'}</span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          <div className="px-4 py-2 text-xs text-gray-400 bg-gray-50">{docs.length} document(s) total</div>
        </div>
      )}
    </div>
  )
}
