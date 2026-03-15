/**
 * Connectors — Integration marketplace for accounting, banking, CRM, storage, communication
 * Hackathon: Airia AI Agents, DigitalOcean Gradient AI
 */
import { useEffect, useState, useCallback } from 'react'

interface Connector {
  connector_id: string
  name: string
  type: string
  status: 'connected' | 'disconnected' | 'error' | 'coming_soon'
  last_sync?: string
  capabilities: string[]
  description: string
  monogram: string
  monogramColor: string
  category: string
}

const STATIC_CONNECTORS: Omit<Connector, 'status' | 'last_sync'>[] = [
  {
    connector_id: 'qbo-1',
    name: 'QuickBooks Online',
    type: 'accounting',
    capabilities: ['invoices', 'coa', 'payments'],
    description: 'Sync invoices, chart of accounts and payment data',
    monogram: 'QB',
    monogramColor: 'bg-green-700',
    category: 'Accounting',
  },
  {
    connector_id: 'xero-1',
    name: 'Xero',
    type: 'accounting',
    capabilities: ['invoices', 'mapping', 'sync'],
    description: 'Cloud accounting with invoice sync and GL mapping',
    monogram: 'XE',
    monogramColor: 'bg-blue-700',
    category: 'Accounting',
  },
  {
    connector_id: 'netsuite-1',
    name: 'NetSuite',
    type: 'accounting',
    capabilities: ['erp', 'financials', 'reporting'],
    description: 'Full ERP financial consolidation and reporting',
    monogram: 'NS',
    monogramColor: 'bg-orange-700',
    category: 'Accounting',
  },
  {
    connector_id: 'sap-1',
    name: 'SAP',
    type: 'accounting',
    capabilities: ['s4hana', 'fiori', 'consolidation'],
    description: 'SAP S/4HANA integration for enterprise finance',
    monogram: 'SA',
    monogramColor: 'bg-blue-900',
    category: 'Accounting',
  },
  {
    connector_id: 'plaid-1',
    name: 'Plaid',
    type: 'banking',
    capabilities: ['bank_feeds', 'transactions', 'dedupe'],
    description: 'Bank feeds, transactions and deduplication',
    monogram: 'PL',
    monogramColor: 'bg-indigo-700',
    category: 'Banking',
  },
  {
    connector_id: 'stripe-1',
    name: 'Stripe',
    type: 'banking',
    capabilities: ['payments', 'subscriptions', 'billing'],
    description: 'Payment processing and subscription billing sync',
    monogram: 'ST',
    monogramColor: 'bg-violet-700',
    category: 'Banking',
  },
  {
    connector_id: 'salesforce-1',
    name: 'Salesforce',
    type: 'crm',
    capabilities: ['revenue_data', 'pipeline', 'forecasting'],
    description: 'Pull revenue pipeline and forecast data for close',
    monogram: 'SF',
    monogramColor: 'bg-sky-700',
    category: 'CRM',
  },
  {
    connector_id: 'hubspot-1',
    name: 'HubSpot',
    type: 'crm',
    capabilities: ['deals', 'contacts', 'revenue'],
    description: 'Deal pipeline and revenue recognition data',
    monogram: 'HS',
    monogramColor: 'bg-rose-700',
    category: 'CRM',
  },
  {
    connector_id: 'gdrive-1',
    name: 'Google Drive',
    type: 'storage',
    capabilities: ['file_sync', 'sharing', 'versioning'],
    description: 'Store and share board pack documents and reports',
    monogram: 'GD',
    monogramColor: 'bg-yellow-700',
    category: 'Storage',
  },
  {
    connector_id: 'sharepoint-1',
    name: 'SharePoint',
    type: 'storage',
    capabilities: ['document_management', 'collaboration'],
    description: 'Enterprise document management and collaboration',
    monogram: 'SP',
    monogramColor: 'bg-teal-700',
    category: 'Storage',
  },
  {
    connector_id: 'coupa-1',
    name: 'Coupa',
    type: 'storage',
    capabilities: ['procurement', 'invoices', 'spend'],
    description: 'Procurement and spend management integration',
    monogram: 'CO',
    monogramColor: 'bg-red-800',
    category: 'Storage',
  },
  {
    connector_id: 'slack-1',
    name: 'Slack',
    type: 'communication',
    capabilities: ['notifications', 'alerts', 'workflows'],
    description: 'Close cycle alerts and workflow notifications',
    monogram: 'SL',
    monogramColor: 'bg-purple-700',
    category: 'Communication',
  },
]

const COMING_SOON_IDS = new Set(['sap-1', 'coupa-1', 'netsuite-1'])

const CATEGORIES = ['All', 'Accounting', 'Banking', 'CRM', 'Storage', 'Communication'] as const
type Category = typeof CATEGORIES[number]

export default function Connectors() {
  const [connectors, setConnectors] = useState<Connector[]>([])
  const [loading, setLoading] = useState(true)
  const [activeCategory, setActiveCategory] = useState<Category>('All')
  const [search, setSearch] = useState('')

  const load = useCallback(async () => {
    setLoading(true)
    try {
      const [qbo, xero, plaid] = await Promise.all([
        fetch('/api/connectors/qbo/status').then(r => r.json()).catch(() => ({ status: 'disconnected' })),
        fetch('/api/connectors/xero/status').then(r => r.json()).catch(() => ({ status: 'disconnected' })),
        fetch('/api/connectors/plaid/status').then(r => r.json()).catch(() => ({ status: 'disconnected' })),
      ])
      const apiStatuses: Record<string, { status: Connector['status']; last_sync?: string }> = {
        'qbo-1': { status: (qbo.status as Connector['status']) || 'disconnected', last_sync: qbo.last_sync },
        'xero-1': { status: (xero.status as Connector['status']) || 'disconnected', last_sync: xero.last_sync },
        'plaid-1': { status: (plaid.status as Connector['status']) || 'disconnected', last_sync: plaid.last_sync },
      }
      setConnectors(
        STATIC_CONNECTORS.map(c => ({
          ...c,
          status: COMING_SOON_IDS.has(c.connector_id)
            ? 'coming_soon'
            : (apiStatuses[c.connector_id]?.status ?? 'disconnected'),
          last_sync: apiStatuses[c.connector_id]?.last_sync,
        }))
      )
    } catch {
      setConnectors(
        STATIC_CONNECTORS.map(c => ({
          ...c,
          status: COMING_SOON_IDS.has(c.connector_id) ? 'coming_soon' : ('disconnected' as const),
        }))
      )
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => { load() }, [load])

  const filtered = connectors.filter(c => {
    const matchesCategory = activeCategory === 'All' || c.category === activeCategory
    const q = search.toLowerCase()
    const matchesSearch =
      c.name.toLowerCase().includes(q) ||
      c.description.toLowerCase().includes(q) ||
      c.category.toLowerCase().includes(q)
    return matchesCategory && matchesSearch
  })

  const statusBadge = (s: Connector['status']) => {
    if (s === 'connected')
      return { cls: 'bg-green-900/40 text-green-300 border border-green-800/50', label: 'Connected' }
    if (s === 'coming_soon')
      return { cls: 'bg-[#1A1A24] text-[#9CA3AF] border border-[#2A2A3A]', label: 'Coming Soon' }
    return { cls: 'bg-blue-900/40 text-blue-300 border border-blue-800/50', label: 'Available' }
  }

  return (
    <div data-testid="connectors-page" className="min-h-screen bg-[#0A0A0F] text-[#F8F9FA]">
      <div className="max-w-7xl mx-auto px-6 py-8">
        <h1 className="text-2xl font-bold mb-1" data-testid="connectors-title">
          Connectors
        </h1>
        <p className="text-[#9CA3AF] mb-8" data-testid="connectors-subtitle">
          Manage accounting and banking integrations.
        </p>

        {/* Search + category tabs */}
        <div className="flex flex-col sm:flex-row gap-4 mb-8">
          <input
            type="text"
            placeholder="Search integrations..."
            value={search}
            onChange={e => setSearch(e.target.value)}
            className="w-full sm:w-72 px-4 py-2 bg-[#1A1A24] border border-[#2A2A3A] rounded-lg text-[#F8F9FA] placeholder-[#9CA3AF] text-sm focus:outline-none focus:border-red-600/50 transition-colors"
          />
          <div className="flex gap-2 flex-wrap">
            {CATEGORIES.map(cat => (
              <button
                key={cat}
                onClick={() => setActiveCategory(cat)}
                className={`px-4 py-1.5 rounded-full text-sm font-medium transition-all ${
                  activeCategory === cat
                    ? 'bg-red-600 text-white'
                    : 'bg-[#1A1A24] text-[#9CA3AF] border border-[#2A2A3A] hover:border-red-600/50 hover:text-[#F8F9FA]'
                }`}
              >
                {cat}
              </button>
            ))}
          </div>
        </div>

        {loading ? (
          <p className="text-[#9CA3AF]">Loading…</p>
        ) : filtered.length === 0 ? (
          <p className="text-[#9CA3AF] text-sm">No integrations match your search.</p>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {filtered.map(c => {
              const badge = statusBadge(c.status)
              const isConnected = c.status === 'connected'
              const isComingSoon = c.status === 'coming_soon'
              const syncTime = c.last_sync
                ? Math.floor((Date.now() - new Date(c.last_sync).getTime()) / 60000)
                : null

              return (
                <div
                  key={c.connector_id}
                  data-testid={`connector-card-${c.connector_id}`}
                  className="rounded-xl border bg-[#111118] border-[#2A2A3A] p-5 hover:border-red-600/50 transition-all duration-200 flex flex-col"
                >
                  {/* Card header */}
                  <div className="flex items-start justify-between mb-4">
                    <div className="flex items-center gap-3">
                      <div
                        className={`w-10 h-10 rounded-full ${c.monogramColor} flex items-center justify-center text-white text-sm font-bold flex-shrink-0`}
                      >
                        {c.monogram}
                      </div>
                      <div>
                        <h3 className="font-semibold text-[#F8F9FA] text-sm leading-tight">{c.name}</h3>
                        <p className="text-xs text-[#9CA3AF] mt-0.5">{c.category}</p>
                      </div>
                    </div>
                    <span className={`px-2 py-0.5 rounded-full text-xs font-medium whitespace-nowrap ${badge.cls}`}>
                      {badge.label}
                    </span>
                  </div>

                  {/* Description */}
                  <p className="text-xs text-[#9CA3AF] mb-3 flex-1">{c.description}</p>

                  {/* Last synced */}
                  {isConnected && syncTime !== null && (
                    <p className="text-xs text-green-400 mb-3 flex items-center gap-1.5">
                      <span className="w-1.5 h-1.5 rounded-full bg-green-400 inline-block flex-shrink-0" />
                      Last synced: {syncTime} min ago
                    </p>
                  )}

                  {/* Capabilities */}
                  <div className="flex flex-wrap gap-1 mb-4">
                    {c.capabilities.map(cap => (
                      <span
                        key={cap}
                        className="px-1.5 py-0.5 bg-[#1A1A24] text-[#9CA3AF] border border-[#2A2A3A] rounded text-xs"
                      >
                        {cap}
                      </span>
                    ))}
                  </div>

                  {/* Actions */}
                  <div className="flex gap-2 mt-auto">
                    {isConnected ? (
                      <>
                        <div className="flex items-center gap-1.5 text-xs text-green-400 flex-1">
                          <svg className="w-3.5 h-3.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                            <path
                              fillRule="evenodd"
                              d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                              clipRule="evenodd"
                            />
                          </svg>
                          Connected
                        </div>
                        <button
                          data-testid={`connector-connect-${c.connector_id}`}
                          className="px-3 py-1.5 text-xs bg-[#1A1A24] border border-[#2A2A3A] text-[#9CA3AF] rounded hover:border-red-600/50 hover:text-red-400 transition-all"
                        >
                          Disconnect
                        </button>
                      </>
                    ) : (
                      <button
                        data-testid={`connector-connect-${c.connector_id}`}
                        disabled={isComingSoon}
                        className={`px-3 py-1.5 text-xs rounded transition-colors ${
                          isComingSoon
                            ? 'bg-[#1A1A24] text-[#9CA3AF] border border-[#2A2A3A] cursor-not-allowed'
                            : 'bg-red-600 text-white hover:bg-red-700'
                        }`}
                      >
                        {isComingSoon ? 'Coming Soon' : 'Connect'}
                      </button>
                    )}
                    <button
                      data-testid={`connector-sync-${c.connector_id}`}
                      disabled={isComingSoon}
                      className={`px-3 py-1.5 text-xs rounded transition-all ${
                        isComingSoon
                          ? 'bg-[#1A1A24] border border-[#2A2A3A] text-[#9CA3AF] cursor-not-allowed opacity-40'
                          : 'bg-[#1A1A24] border border-[#2A2A3A] text-[#9CA3AF] hover:border-red-600/50 hover:text-[#F8F9FA]'
                      }`}
                    >
                      Sync Now
                    </button>
                  </div>
                </div>
              )
            })}
          </div>
        )}
      </div>
    </div>
  )
}
