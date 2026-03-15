/**
 * ScreenshotCapture — For UI Navigator track (Gemini Live).
 * Captures viewport or selection for visual QA / close flow automation.
 */
import { useCallback, useRef, useState } from 'react'

interface ScreenshotCaptureProps {
  onCapture?: (dataUrl: string, bounds?: { x: number; y: number; w: number; h: number }) => void
  className?: string
  dataTestId?: string
}

export function ScreenshotCapture({ onCapture, className = '', dataTestId = 'screenshot-capture' }: ScreenshotCaptureProps) {
  const [selecting, setSelecting] = useState(false)
  const [start, setStart] = useState<{ x: number; y: number } | null>(null)
  const [end, setEnd] = useState<{ x: number; y: number } | null>(null)
  const containerRef = useRef<HTMLDivElement>(null)

  const captureFull = useCallback(() => {
    if (typeof window === 'undefined') return
    try {
      // In real implementation: use html2canvas or browser extension API
      // For demo: simulate capture with a placeholder
      const canvas = document.createElement('canvas')
      canvas.width = window.innerWidth
      canvas.height = window.innerHeight
      const ctx = canvas.getContext('2d')
      if (ctx) {
        ctx.fillStyle = '#1a1a2e'
        ctx.fillRect(0, 0, canvas.width, canvas.height)
        ctx.fillStyle = '#eee'
        ctx.font = '16px monospace'
        ctx.fillText('Screenshot placeholder — Gemini multimodal would process this', 20, 40)
      }
      const dataUrl = canvas.toDataURL('image/png')
      onCapture?.(dataUrl)
    } catch {
      onCapture?.('data:image/png;base64,placeholder')
    }
  }, [onCapture])

  const handleMouseDown = (e: React.MouseEvent) => {
    setSelecting(true)
    setStart({ x: e.clientX, y: e.clientY })
    setEnd(null)
  }

  const handleMouseMove = (e: React.MouseEvent) => {
    if (selecting && start) setEnd({ x: e.clientX, y: e.clientY })
  }

  const handleMouseUp = () => {
    if (selecting && start && end) {
      const x = Math.min(start.x, end.x)
      const y = Math.min(start.y, end.y)
      const w = Math.abs(end.x - start.x)
      const h = Math.abs(end.y - start.y)
      if (w > 10 && h > 10) {
        const canvas = document.createElement('canvas')
        canvas.width = w
        canvas.height = h
        const ctx = canvas.getContext('2d')
        if (ctx) {
          ctx.fillStyle = '#2d2d44'
          ctx.fillRect(0, 0, w, h)
          ctx.fillStyle = '#aaa'
          ctx.font = '12px monospace'
          ctx.fillText(`Region ${w}x${h}`, 8, 20)
        }
        onCapture?.(canvas.toDataURL('image/png'), { x, y, w, h })
      }
    }
    setSelecting(false)
    setStart(null)
    setEnd(null)
  }

  const selectionBox = start && end && (
    <div
      className="absolute border-2 border-indigo-500 bg-indigo-500/20 pointer-events-none"
      style={{
        left: Math.min(start.x, end.x),
        top: Math.min(start.y, end.y),
        width: Math.abs(end.x - start.x),
        height: Math.abs(end.y - start.y),
      }}
    />
  )

  return (
    <div
      ref={containerRef}
      data-testid={dataTestId}
      className={`relative rounded-lg border-2 border-dashed border-gray-600 bg-gray-900/50 p-4 ${className}`}
      onMouseDown={handleMouseDown}
      onMouseMove={handleMouseMove}
      onMouseUp={handleMouseUp}
      onMouseLeave={handleMouseUp}
    >
      <div className="flex items-center gap-3 mb-3">
        <button
          onClick={captureFull}
          className="px-3 py-1.5 bg-red-600 text-white rounded text-sm font-medium hover:bg-red-700"
        >
          📷 Capture Full Screen
        </button>
        <span className="text-gray-400 text-xs">
          {selecting ? 'Drag to select region…' : 'Or click and drag to select a region'}
        </span>
      </div>
      <div className="h-32 rounded bg-gray-800/50 flex items-center justify-center text-gray-500 text-sm">
        Gemini multimodal interprets screenshots → executable actions
      </div>
      {selectionBox}
    </div>
  )
}

export default ScreenshotCapture
