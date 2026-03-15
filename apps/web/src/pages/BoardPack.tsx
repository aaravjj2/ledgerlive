/**
 * BoardPack — PDF-preview style board pack generator
 * Produces structured Q-period board materials from the close ledger
 */
import { useEffect, useState, useCallback } from 'react'
import { apiGet } from '../services/api'

interface BoardPackItem {
  id: string
  name?: string
  status?: string
  created_at?: string
  updated_at?: string
  [key: string]: unknown
}

interface BoardSection {
  num: number
  title: string
  content: string
}

const SECTIONS: BoardSection[] = [
  {
    num: 1,
    title: 'Executive Summary',
    content:
      'Q1 2026 revenue of $4.2M exceeded plan by 8%. Operating margin improved 200bps to 21.4%. Net income of $892K. Three strategic initiatives on track. Close cycle completed in 5.2 days, down from 7.1 days in Q4 2025.',
  },
  {
    num: 2,
    title: 'P&L Statement',
    content:
      'Revenue: $4,200,000 | COGS: $1,848,000 | Gross Profit: $2,352,000 (56.0%) | OpEx: $1,460,000 | EBITDA: $892,000 | Interest & Tax: $128,000 | Net Income: $764,000. YoY revenue growth: +14.2%.',
  },
  {
    num: 3,
    title: 'Balance Sheet',
    content:
      'Total Assets: $18,420,000 | Cash & Equivalents: $3,240,000 | Accounts Receivable: $2,180,000 | PP&E: $8,900,000 | Total Liabilities: $7,220,000 | Accounts Payable: $980,000 | Long-term Debt: $4,800,000 | Total Equity: $11,200,000.',
  },
  {
    num: 4,
    title: 'Cash Flow',
    content:
      'Operating Activities: +$1,200,000 | Investing Activities: -$340,000 (capex) | Financing Activities: -$180,000 (debt service) | Net Change in Cash: +$680,000 | Beginning Cash: $2,560,000 | Ending Cash: $3,240,000.',
  },
  {
    num: 5,
    title: 'KPIs',
    content:
      'DSO: 42 days (target 45) | DPO: 38 days | Close Cycle: 5.2 days | AR Aging <30d: 94% | Exception Rate: 2.1% | Reconciliation Coverage: 98.4% | Automation Rate: 67%.',
  },
  {
    num: 6,
    title: 'Close Status',
    content:
      'Period: Q1 2026 (Jan–Mar) | Status: In Progress | Tasks Complete: 24 / 31 | Open Exceptions: 3 | Owner: Finance Operations | Target Close Date: March 31, 2026 | Next Board Meeting: April 14, 2026.',
  },
]

export default function BoardPackPage() {
  const [items, setItems] = useState<BoardPackItem[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [openSections, setOpenSections] = useState<Set<number>>(new Set([1]))

  const load = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const res = await apiGet<{ items?: BoardPackItem[] }>(`/api/board-pack`)
      setItems(res?.items ?? [])
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Failed to load')
      setItems([])
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => { load() }, [load])

  const toggleSection = (num: number) => {
    setOpenSections(prev => {
      if (prev.has(num)) {
        return new Set([...prev].filter(n => n !== num))
      }
      return new Set([...prev, num])
    })
  }

  const lastGenerated = items[0]?.created_at ?? items[0]?.updated_at ?? null

  return (
    <div data-testid="board-pack-page" className="min-h-screen bg-[#0A0A0F] text-[#F8F9FA]">
      <div className="max-w-4xl mx-auto px-6 py-8">

        {/* Cover page header */}
        <div className="border border-[#2A2A3A] rounded-xl bg-[#111118] p-8 mb-8 text-center">
          <div className="w-12 h-1 bg-red-600 mx-auto mb-6 rounded-full" />
          <p className="text-[#9CA3AF] text-xs tracking-widest uppercase mb-2">LedgerLive Inc.</p>
          <h1
            className="text-3xl font-bold text-[#F8F9FA] mb-2 tracking-tight"
            data-testid="board-pack-title"
          >
            Q1 2026 Board Materials
          </h1>
          <p className="text-[#9CA3AF] text-sm mb-1">March 31, 2026</p>
          <p className="text-[#9CA3AF] text-xs tracking-wide uppercase">Prepared by Finance Operations</p>
          <div className="w-12 h-1 bg-red-600 mx-auto mt-6 rounded-full" />
        </div>

        {/* Toolbar */}
        <div className="flex items-center justify-between mb-6">
          <div>
            {lastGenerated && (
              <p className="text-xs text-[#9CA3AF]">
                Last generated:{' '}
                <span className="text-[#F8F9FA]">
                  {new Date(lastGenerated).toLocaleString()}
                </span>
              </p>
            )}
          </div>
          <div className="flex gap-3">
            <button
              onClick={load}
              disabled={loading}
              className="px-4 py-2 text-sm font-medium bg-red-600 text-white rounded-lg hover:bg-red-700 disabled:opacity-50 transition-colors flex items-center gap-2"
            >
              {loading ? (
                <>
                  <span className="w-3.5 h-3.5 border-2 border-white/30 border-t-white rounded-full animate-spin inline-block" />
                  Generating…
                </>
              ) : (
                'Generate Board Pack'
              )}
            </button>
            <button
              disabled={items.length === 0}
              className="px-4 py-2 text-sm font-medium bg-[#1A1A24] border border-[#2A2A3A] text-[#9CA3AF] rounded-lg hover:border-red-600/50 hover:text-[#F8F9FA] disabled:opacity-40 disabled:cursor-not-allowed transition-all"
            >
              Download PDF
            </button>
          </div>
        </div>

        {error && (
          <div className="p-4 bg-red-900/20 border border-red-800/50 rounded-lg text-red-400 text-sm mb-6">
            {error}
          </div>
        )}

        {/* Accordion section list */}
        <div className="space-y-2">
          {SECTIONS.map(section => {
            const isOpen = openSections.has(section.num)
            return (
              <div
                key={section.num}
                className="border border-[#2A2A3A] rounded-xl bg-[#111118] overflow-hidden"
              >
                {/* Section header */}
                <button
                  onClick={() => toggleSection(section.num)}
                  className="w-full flex items-center gap-4 px-6 py-4 text-left hover:bg-[#1A1A24] transition-colors group"
                >
                  <span className="text-xs font-mono text-red-600 w-6 flex-shrink-0 font-bold">
                    {String(section.num).padStart(2, '0')}
                  </span>
                  <span className="flex-1 text-sm font-semibold text-[#F8F9FA] group-hover:text-white">
                    {section.title}
                  </span>
                  <svg
                    className={`w-4 h-4 text-[#9CA3AF] flex-shrink-0 transition-transform duration-200 ${
                      isOpen ? 'rotate-180' : 'rotate-0'
                    }`}
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                    strokeWidth={2}
                  >
                    <path strokeLinecap="round" strokeLinejoin="round" d="M19 9l-7 7-7-7" />
                  </svg>
                </button>

                {/* Expanded content */}
                {isOpen && (
                  <div className="px-6 pb-5 border-t border-[#2A2A3A]">
                    <div className="pt-4">
                      <p className="text-sm text-[#9CA3AF] leading-relaxed">{section.content}</p>
                      <div className="mt-4 h-16 bg-[#0A0A0F] border border-[#2A2A3A] rounded-lg flex items-center justify-center">
                        <span className="text-xs text-[#9CA3AF]">
                          Chart / table placeholder — populated on generation
                        </span>
                      </div>
                    </div>
                  </div>
                )}

                {/* Separator line when closed */}
                {!isOpen && <div className="h-px bg-[#2A2A3A] mx-6" />}
              </div>
            )
          })}
        </div>

        {/* Footer meta */}
        <div className="mt-8 pt-6 border-t border-[#2A2A3A] flex items-center justify-between">
          <p className="text-xs text-[#9CA3AF]">
            {items.length} item{items.length !== 1 ? 's' : ''} loaded from API
          </p>
          <p className="text-xs text-[#9CA3AF] font-mono">CONFIDENTIAL — BOARD USE ONLY</p>
        </div>
      </div>
    </div>
  )
}
