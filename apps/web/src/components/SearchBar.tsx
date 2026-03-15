import { useState, useRef, useEffect } from 'react'

interface SearchResult {
  type: 'transaction' | 'document' | 'exception'
  id: string
  title: string
  subtitle: string
  url: string
}

export default function SearchBar() {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState<SearchResult[]>([])
  const [isOpen, setIsOpen] = useState(false)
  const inputRef = useRef<HTMLInputElement>(null)

  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if (e.key === '/' && !['INPUT', 'TEXTAREA'].includes((e.target as HTMLElement).tagName)) {
        e.preventDefault()
        inputRef.current?.focus()
        setIsOpen(true)
      }
      if (e.key === 'Escape') {
        setIsOpen(false)
        setQuery('')
      }
    }
    window.addEventListener('keydown', handler)
    return () => window.removeEventListener('keydown', handler)
  }, [])

  useEffect(() => {
    if (query.length < 2) { setResults([]); return }
    // Demo search results
    const demoResults: SearchResult[] = [
      { type: 'transaction', id: 'TXN-001', title: `Transaction matching "${query}"`, subtitle: '$1,500.00 - Acme Corp', url: '/reconciliation' },
      { type: 'exception', id: 'EXC-001', title: `Exception matching "${query}"`, subtitle: 'Critical - Duplicate payment', url: '/exceptions' },
      { type: 'document', id: 'DOC-001', title: `Document matching "${query}"`, subtitle: 'Invoice - Feb 2026', url: '/documents' },
    ]
    setResults(demoResults)
  }, [query])

  return (
    <div className="relative" data-testid="search-bar">
      <div className="flex items-center bg-[#1A1A24] border border-[#2A2A3A] rounded-lg px-3 focus-within:border-[#3A3A4A] transition">
        <svg className="w-3.5 h-3.5 text-gray-600 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
        </svg>
        <input
          ref={inputRef}
          type="text"
          value={query}
          onChange={(e) => { setQuery(e.target.value); setIsOpen(true) }}
          onFocus={() => setIsOpen(true)}
          placeholder="Search… /"
          className="bg-transparent px-2 py-1.5 text-sm text-gray-300 placeholder-gray-700 focus:outline-none w-36 lg:w-48"
          data-testid="search-input"
        />
        <kbd className="hidden sm:inline text-[10px] text-gray-700 bg-[#111118] border border-[#2A2A3A] px-1 py-0.5 rounded font-mono">/</kbd>
      </div>
      {isOpen && results.length > 0 && (
        <div
          className="absolute top-full left-0 right-0 mt-1 bg-[#111118] border border-[#2A2A3A] rounded-xl shadow-2xl z-50 max-h-64 overflow-y-auto"
          data-testid="search-results"
        >
          {results.map(r => (
            <a
              key={r.id}
              href={r.url}
              className="flex items-center gap-3 px-4 py-2.5 hover:bg-[#1A1A24] border-b border-[#1E1E2E] last:border-0 transition"
              onClick={() => { setIsOpen(false); setQuery('') }}
            >
              <span className={`text-[10px] font-medium px-1.5 py-0.5 rounded font-mono ${
                r.type === 'exception'   ? 'bg-red-900/40 text-red-400' :
                r.type === 'transaction' ? 'bg-blue-900/40 text-blue-400' :
                                           'bg-green-900/40 text-green-400'
              }`}>
                {r.type}
              </span>
              <div className="min-w-0">
                <p className="text-sm text-gray-300 truncate">{r.title}</p>
                <p className="text-xs text-gray-600">{r.subtitle}</p>
              </div>
            </a>
          ))}
        </div>
      )}
    </div>
  )
}
