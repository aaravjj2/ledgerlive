/**
 * Watchlist — Tracked accounts, entities, exceptions.
 * Bloomberg-style watchlist with add/remove and quick actions.
 */
import { useState } from 'react'

export interface WatchlistItem {
  id: string
  name: string
  type: 'account' | 'entity' | 'exception' | 'metric'
  value?: string | number
  status?: string
  alert?: boolean
}

interface WatchlistProps {
  items: WatchlistItem[]
  onRemove?: (id: string) => void
  onSelect?: (id: string) => void
  maxItems?: number
  className?: string
  dataTestId?: string
}

export function Watchlist({
  items,
  onRemove,
  onSelect,
  maxItems = 20,
  className = '',
  dataTestId = 'watchlist',
}: WatchlistProps) {
  const [expanded, setExpanded] = useState(true)

  const typeIcon = (t: WatchlistItem['type']) => {
    if (t === 'account') return '📊'
    if (t === 'entity') return '🏢'
    if (t === 'exception') return '⚠️'
    return '📈'
  }

  return (
    <div
      data-testid={dataTestId}
      className={`rounded-lg border border-[#2A2A3A] bg-[#0A0A0F]/50 overflow-hidden ${className}`}
    >
      <button
        onClick={() => setExpanded((e) => !e)}
        className="w-full px-4 py-2 flex items-center justify-between bg-[#111118]/50 hover:bg-[#111118] text-left"
      >
        <span className="font-semibold text-slate-200">Watchlist</span>
        <span className="text-slate-500 text-sm">{items.length} items</span>
      </button>
      {expanded && (
        <div className="max-h-64 overflow-y-auto">
          {items.slice(0, maxItems).map((item) => (
            <div
              key={item.id}
              data-testid={`watchlist-item-${item.id}`}
              className={`flex items-center justify-between px-4 py-2 border-b border-slate-800 last:border-0 hover:bg-[#111118]/30 ${
                item.alert ? 'bg-amber-900/20' : ''
              }`}
            >
              <button
                onClick={() => onSelect?.(item.id)}
                className="flex-1 flex items-center gap-2 text-left min-w-0"
              >
                <span>{typeIcon(item.type)}</span>
                <span className="truncate text-slate-200">{item.name}</span>
                {item.value != null && (
                  <span className="text-slate-500 text-sm font-mono ml-auto">{item.value}</span>
                )}
              </button>
              {onRemove && (
                <button
                  onClick={(e) => { e.stopPropagation(); onRemove(item.id) }}
                  className="text-slate-500 hover:text-red-400 p-1"
                  aria-label="Remove"
                >
                  ×
                </button>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default Watchlist
