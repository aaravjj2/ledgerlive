/**
 * TickerBar — Bloomberg-style real-time ticker strip.
 * Displays live metrics: close progress, SLA countdown, exception counts.
 * Hackathon: Multimodal UX, professional finance aesthetic.
 */
import { useEffect, useState } from 'react'

export interface TickerItem {
  id: string
  label: string
  value: string | number
  change?: number
  trend?: 'up' | 'down' | 'flat'
  pulse?: boolean
}

interface TickerBarProps {
  items: TickerItem[]
  speed?: number
  className?: string
  dataTestId?: string
}

export function TickerBar({ items, speed = 30, className = '', dataTestId = 'ticker-bar' }: TickerBarProps) {
  const [mounted, setMounted] = useState(false)
  useEffect(() => setMounted(true), [])

  if (items.length === 0) return null

  const trendColor = (t?: 'up' | 'down' | 'flat') => {
    if (t === 'up') return 'text-emerald-400'
    if (t === 'down') return 'text-red-400'
    return 'text-gray-400'
  }

  return (
    <div
      data-testid={dataTestId}
      className={`overflow-hidden bg-[#0A0A0F] border-y border-[#2A2A3A] ${className}`}
    >
      <div
        className="flex gap-8 py-2 animate-ticker whitespace-nowrap"
        style={{
          animation: mounted ? `ticker ${speed}s linear infinite` : 'none',
          width: 'max-content',
        }}
      >
        {[...items, ...items].map((item, i) => (
          <div key={`${item.id}-${i}`} className="flex items-center gap-2 px-4">
            <span className="text-slate-500 text-xs font-medium uppercase">{item.label}</span>
            <span className={`font-mono text-sm font-semibold ${trendColor(item.trend)}`}>
              {item.value}
            </span>
            {item.change != null && (
              <span className={`text-xs ${item.trend === 'up' ? 'text-emerald-400' : item.trend === 'down' ? 'text-red-400' : 'text-slate-500'}`}>
                {item.change > 0 ? '+' : ''}{item.change}%
              </span>
            )}
            {item.pulse && (
              <span className="w-2 h-2 rounded-full bg-amber-400 animate-pulse" />
            )}
          </div>
        ))}
      </div>
      <style>{`
        @keyframes ticker {
          0% { transform: translateX(0); }
          100% { transform: translateX(-50%); }
        }
      `}</style>
    </div>
  )
}

export default TickerBar
