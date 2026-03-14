import { useState, useRef, useEffect } from 'react'
import { useVoiceAssistant } from '../hooks/useVoiceAssistant'

const SUGGESTED_QUESTIONS = [
  'What exceptions need my review?',
  "Summarize today's reconciliation run",
  'Show me unmatched transactions',
  "What's the current close period status?",
  'Give me a dashboard summary',
]

function MicIcon({ className }: { className?: string }) {
  return (
    <svg className={className ?? 'w-6 h-6'} fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path
        strokeLinecap="round"
        strokeLinejoin="round"
        strokeWidth={2}
        d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z"
      />
    </svg>
  )
}

function CloseIcon({ className }: { className?: string }) {
  return (
    <svg className={className ?? 'w-5 h-5'} fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
    </svg>
  )
}

function SendIcon({ className }: { className?: string }) {
  return (
    <svg className={className ?? 'w-5 h-5'} fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
    </svg>
  )
}

function ThinkingIndicator() {
  return (
    <div className="flex justify-start">
      <div className="bg-gray-800 px-3 py-2 rounded-lg">
        <div className="flex gap-1" data-testid="thinking-indicator">
          <span
            className="w-2 h-2 bg-teal-400 rounded-full animate-bounce"
            style={{ animationDelay: '0ms' }}
          />
          <span
            className="w-2 h-2 bg-teal-400 rounded-full animate-bounce"
            style={{ animationDelay: '150ms' }}
          />
          <span
            className="w-2 h-2 bg-teal-400 rounded-full animate-bounce"
            style={{ animationDelay: '300ms' }}
          />
        </div>
      </div>
    </div>
  )
}

export default function VoiceAssistant() {
  const {
    isConnected,
    isRecording,
    isThinking,
    messages,
    error,
    connect,
    disconnect,
    sendText,
    startRecording,
    stopRecording,
  } = useVoiceAssistant()

  const [isOpen, setIsOpen] = useState(false)
  const [textInput, setTextInput] = useState('')
  const messagesEndRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const handleSend = () => {
    if (!textInput.trim()) return
    sendText(textInput.trim())
    setTextInput('')
  }

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  if (!isOpen) {
    return (
      <button
        onClick={() => setIsOpen(true)}
        data-testid="voice-assistant-trigger"
        className="fixed bottom-6 right-6 z-50 w-14 h-14 rounded-full bg-teal-600 hover:bg-teal-700 text-white shadow-lg flex items-center justify-center transition-all hover:scale-110"
        aria-label="Open LedgerBot voice assistant"
      >
        <MicIcon />
      </button>
    )
  }

  return (
    <div
      data-testid="voice-assistant-panel"
      className="fixed bottom-6 right-6 z-50 w-96 h-[600px] bg-gray-900 rounded-2xl shadow-2xl border border-gray-700 flex flex-col overflow-hidden"
    >
      {/* Header */}
      <div className="flex items-center justify-between px-4 py-3 bg-gray-800 border-b border-gray-700">
        <div className="flex items-center gap-2">
          <div
            className={`w-2 h-2 rounded-full ${isConnected ? 'bg-green-400' : 'bg-red-400'}`}
          />
          <span className="text-white font-semibold text-sm">LedgerBot</span>
          <span className="text-gray-400 text-xs">
            {isConnected ? 'Connected' : 'Disconnected'}
          </span>
        </div>
        <div className="flex items-center gap-2">
          {!isConnected ? (
            <button
              onClick={connect}
              data-testid="voice-connect-btn"
              className="text-xs px-2 py-1 bg-teal-600 hover:bg-teal-700 text-white rounded"
            >
              Connect
            </button>
          ) : (
            <button
              onClick={disconnect}
              className="text-xs px-2 py-1 bg-gray-600 hover:bg-gray-500 text-white rounded"
            >
              Disconnect
            </button>
          )}
          <button
            onClick={() => setIsOpen(false)}
            className="text-gray-400 hover:text-white"
            aria-label="Close voice assistant"
          >
            <CloseIcon />
          </button>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-3" data-testid="voice-messages">
        {messages.length === 0 && (
          <div className="text-center text-gray-500 mt-8">
            <p className="text-lg mb-2">Hi, I am LedgerBot</p>
            <p className="text-sm">Your AI finance operations assistant</p>
            <div className="mt-4 space-y-2">
              {SUGGESTED_QUESTIONS.map((q, i) => (
                <button
                  key={i}
                  onClick={() => {
                    if (isConnected) sendText(q)
                  }}
                  className="block w-full text-left text-xs px-3 py-2 bg-gray-800 hover:bg-gray-700 rounded-lg text-gray-300 transition-colors"
                  data-testid={`suggested-q-${i}`}
                >
                  {q}
                </button>
              ))}
            </div>
          </div>
        )}
        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-[80%] px-3 py-2 rounded-lg text-sm ${
                msg.role === 'user'
                  ? 'bg-teal-700 text-white'
                  : msg.role === 'system'
                    ? 'bg-yellow-900/50 text-yellow-200 border border-yellow-700'
                    : 'bg-gray-800 text-gray-200'
              }`}
            >
              {msg.type === 'tool_call' && (
                <span className="text-xs text-yellow-400 block mb-1">
                  Tool: {msg.toolName}
                </span>
              )}
              <p className="whitespace-pre-wrap">{msg.text}</p>
              <span className="text-xs text-gray-500 mt-1 block">
                {new Date(msg.timestamp).toLocaleTimeString()}
              </span>
            </div>
          </div>
        ))}
        {isThinking && <ThinkingIndicator />}
        <div ref={messagesEndRef} />
      </div>

      {/* Error */}
      {error && (
        <div className="px-4 py-2 bg-red-900/50 border-t border-red-700 text-red-300 text-xs">
          {error}
        </div>
      )}

      {/* Input */}
      <div className="px-4 py-3 bg-gray-800 border-t border-gray-700">
        <div className="flex items-center gap-2">
          <button
            onClick={isRecording ? stopRecording : startRecording}
            disabled={!isConnected}
            data-testid="voice-record-btn"
            className={`w-10 h-10 rounded-full flex items-center justify-center transition-all ${
              isRecording
                ? 'bg-red-600 hover:bg-red-700 animate-pulse'
                : isConnected
                  ? 'bg-teal-600 hover:bg-teal-700'
                  : 'bg-gray-600 cursor-not-allowed'
            }`}
            aria-label={isRecording ? 'Stop recording' : 'Start recording'}
          >
            <MicIcon className="w-5 h-5 text-white" />
          </button>
          <input
            type="text"
            value={textInput}
            onChange={(e) => setTextInput(e.target.value)}
            onKeyDown={handleKeyDown}
            disabled={!isConnected}
            placeholder={isConnected ? 'Type a message...' : 'Connect to start'}
            data-testid="voice-text-input"
            className="flex-1 bg-gray-700 text-white text-sm rounded-lg px-3 py-2 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-teal-500 disabled:opacity-50"
          />
          <button
            onClick={handleSend}
            disabled={!isConnected || !textInput.trim()}
            data-testid="voice-send-btn"
            className="w-10 h-10 rounded-full bg-teal-600 hover:bg-teal-700 disabled:bg-gray-600 disabled:cursor-not-allowed flex items-center justify-center transition-all"
            aria-label="Send message"
          >
            <SendIcon className="w-5 h-5 text-white" />
          </button>
        </div>
      </div>
    </div>
  )
}
