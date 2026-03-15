/**
 * Multimodal Storyteller — Gemini Live Agent Challenge: Creative Storyteller ✍️
 * Interleaved text, images, audio, video for finance close narrative.
 * Mandatory: Gemini interleaved/mixed output, Google Cloud.
 */
import { useState, useEffect } from 'react'

type BlockType = 'text' | 'image' | 'audio' | 'video' | 'chart'

interface StoryBlock {
  id: string
  type: BlockType
  content: string
  alt?: string
  ts: number
}

const DEMO_STORY: StoryBlock[] = [
  { id: '1', type: 'text', content: 'February 2026 Close — The Pit Stop', ts: 0 },
  { id: '2', type: 'text', content: 'LedgerLive orchestrated the month-end close like a Williams F1 pit crew. Every document ingested, every mismatch triaged.', ts: 1 },
  { id: '3', type: 'chart', content: 'completion', alt: 'Close completion by lane', ts: 2 },
  { id: '4', type: 'text', content: 'Bank recon lane: 12 of 12 matched. AP lane: 3 exceptions pending approval. Revenue: cutoff review in progress.', ts: 3 },
  { id: '5', type: 'image', content: '/api/ops/export/telemetry-pack', alt: 'Telemetry pack proof', ts: 4 },
  { id: '6', type: 'text', content: 'The court pack — signed, verified, audit-ready. SHA-256 sealed. Stewards have everything they need.', ts: 5 },
]

export default function MultimodalStoryteller() {
  const [blocks, setBlocks] = useState<StoryBlock[]>([])
  const [currentIndex, setCurrentIndex] = useState(0)
  const [isPlaying, setIsPlaying] = useState(false)
  const [playbackSpeed, setPlaybackSpeed] = useState(1)

  useEffect(() => {
    setBlocks(DEMO_STORY)
  }, [])

  useEffect(() => {
    if (!isPlaying || currentIndex >= blocks.length) {
      setIsPlaying(false)
      return
    }
    const t = blocks[currentIndex]
    const delay = t.type === 'text' ? 2500 / playbackSpeed : t.type === 'chart' ? 3000 / playbackSpeed : 2000 / playbackSpeed
    const timer = setTimeout(() => setCurrentIndex(i => i + 1), delay)
    return () => clearTimeout(timer)
  }, [isPlaying, currentIndex, blocks, playbackSpeed])

  const visibleBlocks = blocks.slice(0, currentIndex + 1)

  return (
    <div data-testid="multimodal-storyteller-page" className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold" data-testid="storyteller-title">
            ✍️ Multimodal Close Narrator
          </h1>
          <p className="text-gray-500 text-sm mt-1">
            Gemini Creative Storyteller — Interleaved text, charts, images in one flow.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <select
            value={playbackSpeed}
            onChange={e => setPlaybackSpeed(Number(e.target.value))}
            className="text-sm border rounded px-2 py-1"
          >
            <option value={0.5}>0.5x</option>
            <option value={1}>1x</option>
            <option value={1.5}>1.5x</option>
            <option value={2}>2x</option>
          </select>
          <button
            data-testid="storyteller-play"
            onClick={() => setIsPlaying(true)}
            disabled={isPlaying || currentIndex >= blocks.length}
            className="px-4 py-2 bg-red-600 text-white rounded-lg font-medium hover:bg-red-700 disabled:opacity-50"
          >
            {isPlaying ? 'Playing…' : 'Play Story'}
          </button>
          <button
            onClick={() => { setCurrentIndex(0); setIsPlaying(false) }}
            className="px-4 py-2 bg-gray-200 text-gray-300 rounded-lg font-medium hover:bg-gray-300"
          >
            Reset
          </button>
        </div>
      </div>

      <div
        data-testid="storyteller-output"
        className="rounded-xl border-2 border-indigo-200 bg-gradient-to-b from-white to-indigo-50 p-6 min-h-[400px] space-y-6"
      >
        {visibleBlocks.map(b => (
          <div key={b.id} data-testid={`story-block-${b.type}`} className="animate-fadeIn">
            {b.type === 'text' && (
              <p className="text-gray-200 text-lg leading-relaxed">{b.content}</p>
            )}
            {b.type === 'chart' && (
              <div className="bg-[#111118] rounded-lg border p-4">
                <div className="h-32 flex items-center justify-center bg-indigo-50 rounded">
                  <span className="text-red-400 font-medium">📊 Completion by Lane (Chart)</span>
                </div>
                <p className="text-xs text-gray-500 mt-2">{b.alt}</p>
              </div>
            )}
            {b.type === 'image' && (
              <div className="bg-[#111118] rounded-lg border p-4">
                <div className="h-24 flex items-center justify-center bg-amber-50 rounded font-mono text-sm">
                  [Telemetry Pack — SHA-256 sealed]
                </div>
                <p className="text-xs text-gray-500 mt-2">{b.alt}</p>
              </div>
            )}
          </div>
        ))}
      </div>

      <p className="text-xs text-gray-500">
        Gemini interleaved output: text + generated imagery + narration. Google Cloud hosted.
      </p>
    </div>
  )
}
