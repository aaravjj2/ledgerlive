/**
 * InterleavedMediaViewer — Renders Gemini-style interleaved output (text + image + audio + video).
 * Critical for Gemini Live Creative Storyteller track.
 */
import { ReactNode } from 'react'

export type MediaBlockType = 'text' | 'image' | 'audio' | 'video'

export interface MediaBlock {
  id: string
  type: MediaBlockType
  content: string
  url?: string
  mimeType?: string
  caption?: string
}

interface InterleavedMediaViewerProps {
  blocks: MediaBlock[]
  className?: string
  dataTestId?: string
}

export function InterleavedMediaViewer({ blocks, className = '', dataTestId }: InterleavedMediaViewerProps) {
  return (
    <div
      data-testid={dataTestId ?? 'interleaved-media-viewer'}
      className={`space-y-4 ${className}`}
    >
      {blocks.map((block) => (
        <MediaBlockRenderer key={block.id} block={block} />
      ))}
    </div>
  )
}

function MediaBlockRenderer({ block }: { block: MediaBlock }) {
  switch (block.type) {
    case 'text':
      return (
        <div
          data-testid={`media-block-text-${block.id}`}
          className="prose prose-sm dark:prose-invert max-w-none text-gray-700 dark:text-gray-300"
        >
          {block.content}
        </div>
      )
    case 'image':
      return (
        <div data-testid={`media-block-image-${block.id}`} className="rounded-lg overflow-hidden border border-gray-200 dark:border-gray-700">
          {block.url ? (
            <img src={block.url} alt={block.caption ?? ''} className="w-full max-h-96 object-contain" />
          ) : (
            <div className="h-48 bg-gray-100 dark:bg-gray-800 flex items-center justify-center text-gray-500">
              [Generated image placeholder]
            </div>
          )}
          {block.caption && (
            <p className="text-xs text-gray-500 dark:text-gray-400 p-2 bg-gray-50 dark:bg-gray-800">
              {block.caption}
            </p>
          )}
        </div>
      )
    case 'audio':
      return (
        <div data-testid={`media-block-audio-${block.id}`} className="rounded-lg border border-gray-200 dark:border-gray-700 p-4 bg-gray-50 dark:bg-gray-800">
          {block.url ? (
            <audio controls src={block.url} className="w-full" />
          ) : (
            <div className="flex items-center gap-2 text-gray-500">
              <span className="text-2xl">🔊</span>
              <span>Narration: {block.content || 'Audio segment'}</span>
            </div>
          )}
        </div>
      )
    case 'video':
      return (
        <div data-testid={`media-block-video-${block.id}`} className="rounded-lg overflow-hidden border border-gray-200 dark:border-gray-700">
          {block.url ? (
            <video controls src={block.url} className="w-full max-h-96" />
          ) : (
            <div className="h-48 bg-gray-100 dark:bg-gray-800 flex items-center justify-center text-gray-500">
              [Video: {block.content || 'Generated clip'}]
            </div>
          )}
        </div>
      )
    default:
      return null
  }
}
