/**
 * Compliance Dashboard — SOC2, ISO, eDiscovery, GDPR, Key Management.
 * Waves 101-110 frontend.
 */
import { useEffect, useState, useCallback } from 'react'
import { apiGet } from '../services/api'

interface ComplianceItem {
  id: string
  type: string
  status: string
  last_audit: string
  evidence_count: number
}

export default function Compliance() {
  const [items, setItems] = useState<ComplianceItem[]>([])
  const [loading, setLoading] = useState(true)

  const load = useCallback(async () => {
    setLoading(true)
    try {
      const d = await apiGet<{ items?: ComplianceItem[] }>('/api/soc2-evidence')
      setItems(d?.items ?? [])
    } catch {
      setItems([])
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => { load() }, [load])

  const statusColor = (s: string) => {
    if (s === 'pass' || s === 'compliant') return 'bg-green-900/40 text-green-400'
    if (s === 'pending') return 'bg-yellow-900/40 text-yellow-400'
    return 'bg-red-900/40 text-red-400'
  }

  return (
    <div data-testid="compliance-page">
      <h1 className="text-2xl font-bold mb-1" data-testid="compliance-title">Compliance</h1>
      <p className="text-gray-500 mb-6">SOC2, ISO, eDiscovery, GDPR, Key Management.</p>

      {loading ? (
        <p className="text-gray-400">Loading…</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {items.length === 0 && (
            <div className="col-span-full text-center py-12 text-gray-400">No compliance items. Run demo seed.</div>
          )}
          {items.map(item => (
            <div key={item.id} className="rounded-xl border bg-[#111118] p-4" data-testid="compliance-card">
              <div className="flex justify-between items-start mb-2">
                <span className="font-semibold text-gray-200">{item.type}</span>
                <span className={`px-2 py-0.5 rounded text-xs ${statusColor(item.status)}`}>{item.status}</span>
              </div>
              <div className="text-sm text-gray-500">
                Last audit: {item.last_audit || '—'}<br />
                Evidence: {item.evidence_count ?? 0}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
