/**
 * ResizablePanes — Multi-pane Bloomberg-style layout.
 * Draggable dividers for professional terminal UX.
 */
import { useState, useCallback, ReactNode } from 'react'

interface PaneConfig {
  id: string
  minSize?: number
  maxSize?: number
  defaultSize?: number
}

interface ResizablePanesProps {
  panes: { id: string; content: ReactNode; config?: Partial<PaneConfig> }[]
  direction?: 'row' | 'column'
  className?: string
  dataTestId?: string
}

export function ResizablePanes({
  panes,
  direction = 'row',
  className = '',
  dataTestId = 'resizable-panes',
}: ResizablePanesProps) {
  const [sizes, setSizes] = useState<number[]>(
    panes.map((p) => p.config?.defaultSize ?? 100 / panes.length)
  )
  const [dragging, setDragging] = useState<number | null>(null)

  const handleDrag = useCallback(
    (idx: number, delta: number) => {
      setSizes((prev) => {
        const next = [...prev]
        const total = next.reduce((a, b) => a + b, 0)
        const pct = (delta / total) * 100
        next[idx] = Math.max(5, Math.min(95, next[idx] + pct))
        next[idx + 1] = Math.max(5, Math.min(95, next[idx + 1] - pct))
        return next
      })
    },
    []
  )

  return (
    <div
      data-testid={dataTestId}
      className={`flex ${direction === 'column' ? 'flex-col' : ''} h-full ${className}`}
    >
      {panes.map((pane, i) => (
        <div key={pane.id} className="flex flex-1 min-h-0 min-w-0" style={{ flex: `${sizes[i] ?? 1} 1 0` }}>
          <div className="flex-1 overflow-auto">{pane.content}</div>
          {i < panes.length - 1 && (
            <div
              data-testid={`pane-divider-${i}`}
              className={`w-1 cursor-col-resize bg-slate-600 hover:bg-indigo-500 transition flex-shrink-0 ${
                dragging === i ? 'bg-indigo-500' : ''
              }`}
              onMouseDown={() => setDragging(i)}
              onMouseUp={() => setDragging(null)}
              onMouseLeave={() => setDragging(null)}
            />
          )}
        </div>
      ))}
    </div>
  )
}

export default ResizablePanes
