/**
 * Heatmap — Account variance / entity health visualization.
 * TradingView-style density view for finance close metrics.
 */
import { useMemo } from 'react'

export interface HeatmapCell {
  id: string
  label: string
  value: number
  min?: number
  max?: number
  status?: 'ok' | 'warning' | 'critical'
}

interface HeatmapProps {
  cells: HeatmapCell[]
  columns?: number
  colorScale?: 'red-green' | 'blue' | 'amber'
  showValues?: boolean
  className?: string
  dataTestId?: string
}

export function Heatmap({
  cells,
  columns = 6,
  colorScale = 'red-green',
  showValues = true,
  className = '',
  dataTestId = 'heatmap',
}: HeatmapProps) {
  const { minVal, maxVal } = useMemo(() => {
    const vals = cells.map((c) => c.value)
    return { minVal: Math.min(...vals, 0), maxVal: Math.max(...vals, 1) }
  }, [cells])

  const getColor = (value: number) => {
    if (colorScale === 'red-green') {
      const t = maxVal === minVal ? 0.5 : (value - minVal) / (maxVal - minVal)
      if (t < 0.33) return 'bg-red-500/80'
      if (t < 0.66) return 'bg-amber-500/80'
      return 'bg-emerald-500/80'
    }
    if (colorScale === 'blue') {
      const t = maxVal === minVal ? 0.5 : (value - minVal) / (maxVal - minVal)
      return `bg-blue-${Math.round(400 + t * 400)}`
    }
    const t = maxVal === minVal ? 0.5 : (value - minVal) / (maxVal - minVal)
    return t > 0.5 ? 'bg-amber-500/80' : 'bg-slate-600/80'
  }

  return (
    <div
      data-testid={dataTestId}
      className={`grid gap-1 ${className}`}
      style={{ gridTemplateColumns: `repeat(${columns}, minmax(0, 1fr))` }}
    >
      {cells.map((cell) => (
        <div
          key={cell.id}
          data-testid={`heatmap-cell-${cell.id}`}
          className={`rounded p-2 text-center transition ${getColor(cell.value)} ${
            cell.status === 'critical' ? 'ring-2 ring-red-400' : ''
          }`}
          title={`${cell.label}: ${cell.value}`}
        >
          <div className="text-xs font-medium truncate text-white/90">{cell.label}</div>
          {showValues && (
            <div className="text-sm font-bold text-white">{cell.value.toLocaleString()}</div>
          )}
        </div>
      ))}
    </div>
  )
}

export default Heatmap
