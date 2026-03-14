/**
 * Connectors — Integration management for QBO, Xero, Plaid
 * Hackathon: Airia AI Agents, DigitalOcean Gradient AI
 */
import { useEffect, useState, useCallback } from 'react'

interface Connector {
  connector_id: string
  name: string
  type: string
  status: 'connected' | 'disconnected' | 'error'
  last_sync?: string
  capabilities: string[]
}

export default function Connectors() {
  const [connectors, setConnectors] = useState<Connector[]>([])
  const [loading, setLoading] = useState(true)

  const load = useCallback(async () => {
    setLoading(true)
    try {
      const [qbo, xero, plaid] = await Promise.all([
        fetch('/api/connectors/qbo/status').then(r => r.json()).catch(() => ({ status: 'disconnected' })),
        fetch('/api/connectors/xero/status').then(r => r.json()).catch(() => ({ status: 'disconnected' })),
        fetch('/api/connectors/plaid/status').then(r => r.json()).catch(() => ({ status: 'disconnected' })),
      ])
      setConnectors([
        { connector_id: 'qbo-1', name: 'QuickBooks Online', type: 'accounting', status: qbo.status || 'disconnected', last_sync: qbo.last_sync, capabilities: ['invoices', 'coa', 'payments'] },
        { connector_id: 'xero-1', name: 'Xero', type: 'accounting', status: xero.status || 'disconnected', last_sync: xero.last_sync, capabilities: ['invoices', 'mapping', 'sync'] },
        { connector_id: 'plaid-1', name: 'Plaid', type: 'banking', status: plaid.status || 'disconnected', last_sync: plaid.last_sync, capabilities: ['bank_feeds', 'transactions', 'dedupe'] },
      ])
    } catch {
      setConnectors([
        { connector_id: 'qbo-1', name: 'QuickBooks Online', type: 'accounting', status: 'disconnected', capabilities: ['invoices', 'coa', 'payments'] },
        { connector_id: 'xero-1', name: 'Xero', type: 'accounting', status: 'disconnected', capabilities: ['invoices', 'mapping', 'sync'] },
        { connector_id: 'plaid-1', name: 'Plaid', type: 'banking', status: 'disconnected', capabilities: ['bank_feeds', 'transactions', 'dedupe'] },
      ])
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => { load() }, [load])

  const statusColor = (s: string) => {
    if (s === 'connected') return 'bg-green-100 text-green-800'
    if (s === 'error') return 'bg-red-100 text-red-800'
    return 'bg-gray-100 text-gray-600'
  }

  return (
    <div data-testid="connectors-page">
      <h1 className="text-2xl font-bold mb-1" data-testid="connectors-title">Connectors</h1>
      <p className="text-gray-500 mb-6" data-testid="connectors-subtitle">Manage accounting and banking integrations.</p>

      {loading ? (
        <p className="text-gray-400">Loading…</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {connectors.map(c => (
            <div
              key={c.connector_id}
              data-testid={`connector-card-${c.connector_id}`}
              className="rounded-xl border bg-white shadow-sm p-5 hover:shadow-md transition"
            >
              <div className="flex items-center justify-between mb-3">
                <h3 className="font-semibold text-gray-800">{c.name}</h3>
                <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${statusColor(c.status)}`}>
                  {c.status}
                </span>
              </div>
              <p className="text-xs text-gray-500 mb-2 capitalize">{c.type}</p>
              {c.last_sync && (
                <p className="text-xs text-gray-400 mb-2">Last sync: {new Date(c.last_sync).toLocaleString()}</p>
              )}
              <div className="flex flex-wrap gap-1">
                {c.capabilities.map(cap => (
                  <span key={cap} className="px-1.5 py-0.5 bg-indigo-50 text-indigo-700 rounded text-xs">
                    {cap}
                  </span>
                ))}
              </div>
              <div className="mt-4 flex gap-2">
                <button
                  data-testid={`connector-connect-${c.connector_id}`}
                  className="px-3 py-1.5 text-xs bg-indigo-600 text-white rounded hover:bg-indigo-700"
                >
                  Connect
                </button>
                <button
                  data-testid={`connector-sync-${c.connector_id}`}
                  className="px-3 py-1.5 text-xs bg-gray-200 text-gray-700 rounded hover:bg-gray-300"
                >
                  Sync Now
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
