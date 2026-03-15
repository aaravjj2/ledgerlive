import { useEffect, useState, useCallback } from 'react'
import { apiGet } from '../services/api'

interface EvidenceBinderItem {
  id: string
  name?: string
  status?: string
  created_at?: string
  updated_at?: string
  [key: string]: unknown
}

function truncateHash(hash: unknown): string {
  if (typeof hash !== 'string' || hash.length === 0) return 'N/A'
  return hash.slice(0, 16) + '...'
}

function getFileTypeLabel(item: EvidenceBinderItem): string {
  if (typeof item.name === 'string') {
    const parts = item.name.split('.')
    if (parts.length > 1) {
      const ext = parts[parts.length - 1]
      if (ext && ext.length <= 5) return ext.toUpperCase()
    }
  }
  const ft = item.file_type
  if (typeof ft === 'string') return ft.toUpperCase().slice(0, 4)
  return 'DOC'
}

function isSealedItem(item: EvidenceBinderItem): boolean {
  return item.status === 'sealed' || item.status === 'active'
}

interface IntegrityRingProps { score: number }

function IntegrityRing({ score }: IntegrityRingProps) {
  const ringClass =
    score >= 90 ? 'border-green-400 bg-green-900/20' :
    score >= 70 ? 'border-yellow-400 bg-yellow-900/20' :
                  'border-red-400 bg-red-900/20'
  const textClass =
    score >= 90 ? 'text-green-400' :
    score >= 70 ? 'text-yellow-400' :
                  'text-red-400'
  return (
    <div className={`w-12 h-12 rounded-full border-4 flex items-center justify-center ${ringClass}`}>
      <span className={`text-xs font-bold ${textClass}`}>&#10003;</span>
    </div>
  )
}

export default function EvidenceBinderPage() {
  const [items, setItems] = useState<EvidenceBinderItem[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [generating, setGenerating] = useState(false)
  const [binderReady, setBinderReady] = useState(false)

  const load = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const res = await apiGet<{ items?: EvidenceBinderItem[] }>(`/api/evidence-binder`)
      setItems(res?.items ?? [])
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Failed to load')
      setItems([])
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => { load() }, [load])

  const generateBinder = async () => {
    setGenerating(true)
    try {
      await fetch('/api/evidence-binder', { method: 'POST' })
      setBinderReady(true)
      await load()
    } catch {
      // silent
    }
    setGenerating(false)
  }

  const sealedItems = items.filter(isSealedItem)
  const integrityScore =
    items.length > 0 ? Math.round((sealedItems.length / items.length) * 100) : 0

  const scoreTextClass =
    integrityScore >= 90 ? 'text-green-400' :
    integrityScore >= 70 ? 'text-yellow-400' :
                           'text-red-400'

  const barClass =
    integrityScore >= 90 ? 'bg-green-400' :
    integrityScore >= 70 ? 'bg-yellow-400' :
                           'bg-red-400'

  const chainStatus =
    integrityScore >= 90 ? 'VERIFIED' :
    integrityScore >= 70 ? 'PARTIAL' :
                           'INCOMPLETE'

  return (
    <div data-testid="evidence-binder-page" className="min-h-screen bg-[#0A0A0F] pb-16">

      {/* ── Page Header ── */}
      <div className="border-b border-[#2A2A3A] bg-[#111118] px-6 py-5">
        <div className="flex items-start justify-between gap-4 flex-wrap">
          <div>
            <div className="flex items-center gap-3 mb-1">
              <div className="w-8 h-8 rounded bg-[#1A1A24] border border-[#2A2A3A] flex items-center justify-center shrink-0">
                <svg
                  className="w-4 h-4 text-[#00D2FF]"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                  aria-hidden="true"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                  />
                </svg>
              </div>
              <h1
                className="text-3xl font-bold tracking-tight text-[#F8F9FA]"
                data-testid="evidence-binder-title"
              >
                Evidence Binder
              </h1>
            </div>
            <p className="text-[#9CA3AF] text-sm ml-11">
              Cryptographic evidence chain &middot; SHA-256 sealed
            </p>
          </div>

          {/* Integrity Score */}
          <div className="flex items-center gap-4">
            <div className="text-right">
              <div className="text-[10px] font-semibold text-[#9CA3AF] uppercase tracking-widest mb-0.5">
                Integrity Score
              </div>
              <div className={`text-3xl font-bold font-mono ${scoreTextClass}`}>
                {integrityScore}%
              </div>
            </div>
            <IntegrityRing score={integrityScore} />
          </div>
        </div>
      </div>

      <div className="px-6 pt-6 space-y-6">

        {/* ── Seal Progress + Actions ── */}
        <div className="rounded-xl border border-[#2A2A3A] bg-[#111118] p-5">
          <div className="flex items-center justify-between mb-4 flex-wrap gap-3">
            <div>
              <div className="flex items-center gap-2 mb-0.5">
                <span className="text-[#F8F9FA] font-semibold text-sm">
                  {sealedItems.length}/{items.length} items sealed
                </span>
                {binderReady && (
                  <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-green-900/40 text-green-400 border border-green-800 uppercase tracking-wider">
                    Binder Ready
                  </span>
                )}
              </div>
              <div className="text-[11px] text-[#9CA3AF] font-mono">
                Chain integrity: {chainStatus}
              </div>
            </div>

            <div className="flex items-center gap-3 flex-wrap">
              <button
                onClick={load}
                disabled={loading}
                className="px-3 py-2 bg-[#1A1A24] border border-[#2A2A3A] text-[#F8F9FA] rounded-lg text-sm font-medium hover:bg-[#2A2A3A] disabled:opacity-50 transition-colors"
              >
                {loading ? 'Loading\u2026' : '\u21BB Refresh'}
              </button>

              <button
                onClick={generateBinder}
                disabled={generating || loading}
                className="px-5 py-2 bg-[#00D2FF]/10 border border-[#00D2FF]/30 text-[#00D2FF] rounded-lg text-sm font-semibold hover:bg-[#00D2FF]/20 disabled:opacity-50 transition-colors"
              >
                {generating ? 'Generating\u2026' : 'Generate Binder'}
              </button>

              {binderReady && (
                <button className="px-5 py-2 bg-green-900/30 border border-green-800 text-green-400 rounded-lg text-sm font-semibold hover:bg-green-900/50 transition-colors">
                  &#8595; Download .pdf
                </button>
              )}
            </div>
          </div>

          {/* Progress bar — width is dynamic, inline style required */}
          <div className="w-full bg-[#1A1A24] rounded-full h-2 overflow-hidden">
            <div
              className={`h-full rounded-full transition-all duration-700 ${barClass}`}
              style={{ width: `${integrityScore}%` }}
            />
          </div>
        </div>

        {/* ── Error state ── */}
        {error && (
          <div className="p-4 bg-red-900/20 border border-red-800 rounded-lg text-red-400 text-sm font-mono">
            {error}
          </div>
        )}

        {/* ── Evidence Records ── */}
        <div className="rounded-xl border border-[#2A2A3A] bg-[#111118] overflow-hidden">
          <div className="px-5 py-3 border-b border-[#2A2A3A] flex items-center justify-between">
            <span className="text-xs font-semibold text-[#9CA3AF] uppercase tracking-widest">
              Evidence Records
            </span>
            <span className="text-xs text-[#9CA3AF] font-mono">{items.length} items</span>
          </div>

          {loading ? (
            <div className="py-16 text-center">
              <div className="w-6 h-6 border-2 border-[#00D2FF] border-t-transparent rounded-full animate-spin mx-auto mb-3" />
              <p className="text-[#9CA3AF] text-sm">Loading evidence chain\u2026</p>
            </div>
          ) : items.length === 0 ? (
            <div className="py-16 text-center">
              <p className="text-[#9CA3AF] text-sm">No evidence records found.</p>
            </div>
          ) : (
            <div className="divide-y divide-[#2A2A3A]">
              {items.map(item => {
                const sealed = isSealedItem(item)
                const hash = item.sha256 ?? item.hash ?? item.checksum
                const sealedAt = item.sealed_at ?? item.updated_at ?? item.created_at
                const fileType = getFileTypeLabel(item)

                return (
                  <div
                    key={item.id}
                    className="flex items-center gap-4 px-5 py-4 hover:bg-[#1A1A24] transition-colors group"
                  >
                    {/* File type indicator */}
                    <div className="w-10 h-10 rounded-lg bg-[#1A1A24] border border-[#2A2A3A] flex items-center justify-center shrink-0 group-hover:border-[#3A3A4A] transition-colors">
                      <span className="text-[9px] font-bold text-[#00D2FF] font-mono leading-none">
                        {fileType}
                      </span>
                    </div>

                    {/* Main content */}
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2 mb-1 flex-wrap">
                        <span className="text-sm font-medium text-[#F8F9FA] truncate">
                          {item.name ?? `Record ${item.id.slice(0, 8)}`}
                        </span>
                        {sealed ? (
                          <span className="shrink-0 text-[10px] font-bold px-2 py-0.5 rounded bg-green-900/40 text-green-400 uppercase tracking-wider border border-green-800">
                            SEALED
                          </span>
                        ) : (
                          <span className="shrink-0 text-[10px] font-bold px-2 py-0.5 rounded bg-[#2A2A3A] text-[#9CA3AF] uppercase tracking-wider">
                            {item.status ?? 'PENDING'}
                          </span>
                        )}
                      </div>

                      <div className="flex items-center gap-1.5">
                        <span className="text-[10px] text-[#9CA3AF] font-mono">SHA-256:</span>
                        <span className="text-[11px] font-mono text-[#00D2FF]/70 tracking-wider">
                          {truncateHash(hash)}
                        </span>
                      </div>
                    </div>

                    {/* Sealed-at timestamp */}
                    <div className="text-right shrink-0 min-w-[80px]">
                      {sealedAt ? (
                        <div>
                          <div className="text-[10px] text-[#9CA3AF] font-mono mb-0.5">
                            Sealed at
                          </div>
                          <div className="text-[11px] font-mono text-[#F8F9FA]">
                            {new Date(String(sealedAt)).toLocaleTimeString([], {
                              hour: '2-digit',
                              minute: '2-digit',
                            })}
                          </div>
                          <div className="text-[10px] font-mono text-[#9CA3AF]">
                            {new Date(String(sealedAt)).toLocaleDateString()}
                          </div>
                        </div>
                      ) : (
                        <span className="text-[10px] font-mono text-[#9CA3AF]">&mdash;</span>
                      )}
                    </div>
                  </div>
                )
              })}
            </div>
          )}
        </div>

      </div>
    </div>
  )
}
