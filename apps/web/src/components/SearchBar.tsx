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
      <div className="flex items-center bg-indigo-600 rounded-lg px-3">
        <svg className="w-4 h-4 text-indigo-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
        </svg>
        <input
          ref={inputRef}
          type="text"
          value={query}
          onChange={(e) => { setQuery(e.target.value); setIsOpen(true) }}
          onFocus={() => setIsOpen(true)}
          placeholder="Search... (press /)"
          className="bg-transparent px-2 py-2 text-sm text-white placeholder-indigo-300 focus:outline-none w-48 lg:w-64"
          data-testid="search-input"
        />
        <kbd className="hidden sm:inline text-xs text-indigo-300 bg-indigo-800 px-1.5 py-0.5 rounded">/</kbd>
      </div>
      {isOpen && results.length > 0 && (
        <div className="absolute top-full left-0 right-0 mt-1 bg-white rounded-lg shadow-lg border z-50 max-h-64 overflow-y-auto" data-testid="search-results">
          {results.map(r => (
            <a
              key={r.id}
              href={r.url}
              className="flex items-center gap-3 px-4 py-3 hover:bg-gray-50 border-b last:border-0"
              onClick={() => { setIsOpen(false); setQuery('') }}
            >
              <span className={`text-xs font-medium px-2 py-0.5 rounded ${
                r.type === 'exception' ? 'bg-red-100 text-red-700' :
                r.type === 'transaction' ? 'bg-blue-100 text-blue-700' :
                'bg-green-100 text-green-700'
              }`}>
                {r.type}
              </span>
              <div>
                <p className="text-sm font-medium text-gray-900">{r.title}</p>
                <p className="text-xs text-gray-500">{r.subtitle}</p>
              </div>
            </a>
          ))}
        </div>
      )}
    </div>
  )
}
