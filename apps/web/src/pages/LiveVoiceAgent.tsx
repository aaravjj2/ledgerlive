/**
 * LiveVoiceAgent -- Full-page Gemini Voice Agent experience.
 * Provides a three-column layout: suggested questions sidebar,
 * central chat area with voice controls, and a tool-call activity sidebar.
 * Uses the shared useVoiceAssistant hook for WebSocket + audio streaming.
 */
import { useState, useRef, useEffect, useCallback } from 'react'
import { useVoiceAssistant } from '../hooks/useVoiceAssistant'
import type { VoiceMessage } from '../hooks/useVoiceAssistant'
import { VoiceVisualizer } from '../components/VoiceVisualizer'

const SUGGESTED_QUESTIONS = [
  { category: 'Close Status', questions: [
    "What's the current close period status?",
    'How many tasks are remaining in this close?',
    'Show me the close calendar for this month',
  ]},
  { category: 'Reconciliation', questions: [
    "Summarize today's reconciliation run",
    'Show me unmatched transactions',
    'What is the bank recon match rate?',
  ]},
  { category: 'Exceptions', questions: [
    'What exceptions need my review?',
    'Show me high-priority exceptions',
    'How many exceptions were auto-resolved today?',
  ]},
  { category: 'Dashboard', questions: [
    'Give me a dashboard summary',
    'What are the top KPIs right now?',
    'Show revenue variance this quarter',
  ]},
]

function ConnectionBadge({ isConnected }: { isConnected: boolean }) {
  return (
    <div className="flex items-center gap-2">
      <div
        data-testid="connection-indicator"
        className={`w-2.5 h-2.5 rounded-full ${
          isConnected ? 'bg-green-400 shadow-green-400/50' : 'bg-red-400'
        }`}
      />
      <span className={`text-xs font-medium ${isConnected ? 'text-green-400' : 'text-gray-400'}`}>
        {isConnected ? 'Connected' : 'Disconnected'}
      </span>
    </div>
  )
}

function ToolCallCard({ message }: { message: VoiceMessage }) {
  const [isExpanded, setIsExpanded] = useState(false)

  return (
    <div
      data-testid="tool-call-card"
      className="bg-gray-800 border border-yellow-700/50 rounded-lg p-3 text-sm"
    >
      <button
        onClick={() => setIsExpanded(prev => !prev)}
        className="w-full flex items-center justify-between text-left"
        aria-expanded={isExpanded}
      >
        <div className="flex items-center gap-2">
          <span className="w-5 h-5 bg-yellow-600 rounded flex items-center justify-center text-xs text-white font-bold">
            T
          </span>
          <span className="text-yellow-300 font-medium">{message.toolName}</span>
        </div>
        <svg
          className={`w-4 h-4 text-gray-400 transition-transform ${isExpanded ? 'rotate-180' : ''}`}
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
        </svg>
      </button>
      <span className="text-xs text-gray-500 mt-1 block">
        {new Date(message.timestamp).toLocaleTimeString()}
      </span>
      {isExpanded && message.toolArgs && (
        <pre className="mt-2 p-2 bg-gray-900 rounded text-xs text-gray-300 overflow-x-auto">
          {JSON.stringify(message.toolArgs, null, 2)}
        </pre>
      )}
    </div>
  )
}

function MessageBubble({ message }: { message: VoiceMessage }) {
  const isUser = message.role === 'user'
  const isSystem = message.role === 'system'

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}>
      {!isUser && (
        <div className="w-8 h-8 rounded-full bg-teal-700 flex items-center justify-center mr-2 flex-shrink-0 mt-1">
          <span className="text-xs text-white font-bold">LB</span>
        </div>
      )}
      <div
        className={`max-w-[75%] px-4 py-3 rounded-2xl text-sm leading-relaxed ${
          isUser
            ? 'bg-teal-700 text-white rounded-br-md'
            : isSystem
              ? 'bg-yellow-900/40 text-yellow-200 border border-yellow-700/50 rounded-bl-md'
              : 'bg-gray-800 text-gray-200 rounded-bl-md'
        }`}
      >
        {message.type === 'tool_call' && (
          <span className="text-xs text-yellow-400 block mb-1 font-medium">
            Tool Call: {message.toolName}
          </span>
        )}
        {message.type === 'audio' && (
          <span className="text-xs text-teal-300 block mb-1 font-medium">Audio Message</span>
        )}
        <p className="whitespace-pre-wrap">{message.text}</p>
        <span className="text-xs text-gray-500 mt-2 block">
          {new Date(message.timestamp).toLocaleTimeString()}
        </span>
      </div>
      {isUser && (
        <div className="w-8 h-8 rounded-full bg-gray-600 flex items-center justify-center ml-2 flex-shrink-0 mt-1">
          <span className="text-xs text-white font-bold">U</span>
        </div>
      )}
    </div>
  )
}

export default function LiveVoiceAgent() {
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
    clearMessages,
    dismissError,
  } = useVoiceAssistant()

  const [textInput, setTextInput] = useState('')
  const [sidebarTab, setSidebarTab] = useState<'tools' | 'history'>('tools')
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const toolCallMessages = messages.filter(m => m.type === 'tool_call')
  const conversationMessages = messages.filter(m => m.type !== 'tool_call')

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const handleSend = useCallback(() => {
    if (!textInput.trim()) return
    sendText(textInput.trim())
    setTextInput('')
  }, [textInput, sendText])

  const handleKeyDown = useCallback(
    (e: React.KeyboardEvent) => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault()
        handleSend()
      }
    },
    [handleSend],
  )

  const handleSuggestedQuestion = useCallback(
    (question: string) => {
      if (isConnected) {
        sendText(question)
      }
    },
    [isConnected, sendText],
  )

  return (
    <div data-testid="live-voice-agent-page" className="flex flex-col h-[calc(100vh-8rem)]">
      {/* Top Bar */}
      <div className="flex items-center justify-between mb-4 flex-shrink-0">
        <div>
          <h1 className="text-2xl font-bold text-white" data-testid="live-voice-title">
            Live Voice Agent
          </h1>
          <p className="text-gray-400 text-sm mt-1">
            Gemini-powered real-time voice assistant for finance operations
          </p>
        </div>
        <div className="flex items-center gap-4">
          <ConnectionBadge isConnected={isConnected} />
          {!isConnected ? (
            <button
              data-testid="voice-connect"
              onClick={connect}
              className="px-5 py-2 bg-teal-600 text-white rounded-lg font-medium hover:bg-teal-700 transition-colors"
            >
              Connect
            </button>
          ) : (
            <button
              data-testid="voice-disconnect"
              onClick={disconnect}
              className="px-5 py-2 bg-red-600 text-white rounded-lg font-medium hover:bg-red-700 transition-colors"
            >
              Disconnect
            </button>
          )}
        </div>
      </div>

      {/* Error Banner */}
      {error && (
        <div
          data-testid="voice-error-banner"
          className="mb-4 flex items-center justify-between px-4 py-2 bg-red-900/50 border border-red-700 rounded-lg text-red-300 text-sm flex-shrink-0"
        >
          <span>{error}</span>
          <button
            onClick={dismissError}
            className="text-red-400 hover:text-red-200 ml-4"
            aria-label="Dismiss error"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      )}

      {/* Three-Column Layout */}
      <div className="flex-1 flex gap-4 min-h-0">
        {/* Left Sidebar -- Suggested Questions */}
        <aside
          data-testid="suggested-questions-sidebar"
          className="w-64 flex-shrink-0 bg-gray-900 border border-gray-700 rounded-xl p-4 overflow-y-auto hidden lg:block"
        >
          <h2 className="text-sm font-semibold text-gray-300 mb-3 uppercase tracking-wide">
            Suggested Questions
          </h2>
          <div className="space-y-4">
            {SUGGESTED_QUESTIONS.map((group) => (
              <div key={group.category}>
                <h3 className="text-xs font-medium text-gray-500 mb-2">{group.category}</h3>
                <div className="space-y-1.5">
                  {group.questions.map((q, i) => (
                    <button
                      key={i}
                      onClick={() => handleSuggestedQuestion(q)}
                      disabled={!isConnected}
                      data-testid={`suggested-${group.category.toLowerCase().replace(/\s+/g, '-')}-${i}`}
                      className="w-full text-left text-xs px-3 py-2 bg-gray-800 hover:bg-gray-700 disabled:opacity-40 disabled:cursor-not-allowed rounded-lg text-gray-300 transition-colors leading-relaxed"
                    >
                      {q}
                    </button>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </aside>

        {/* Center -- Chat Area */}
        <div className="flex-1 flex flex-col bg-gray-900 border border-gray-700 rounded-xl overflow-hidden min-w-0">
          {/* Chat Messages */}
          <div
            className="flex-1 overflow-y-auto p-4 space-y-4"
            data-testid="voice-chat-messages"
          >
            {conversationMessages.length === 0 && !isThinking && (
              <div className="flex flex-col items-center justify-center h-full text-gray-500">
                <div className="w-16 h-16 rounded-full bg-teal-900/50 flex items-center justify-center mb-4">
                  <svg className="w-8 h-8 text-teal-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z"
                    />
                  </svg>
                </div>
                <p className="text-lg font-medium mb-1">LedgerBot Voice Agent</p>
                <p className="text-sm text-gray-400">
                  {isConnected
                    ? 'Start speaking or type a message below'
                    : 'Click Connect to start a conversation'}
                </p>
              </div>
            )}
            {conversationMessages.map((msg) => (
              <MessageBubble key={msg.id} message={msg} />
            ))}
            {isThinking && (
              <div className="flex justify-start">
                <div className="w-8 h-8 rounded-full bg-teal-700 flex items-center justify-center mr-2 flex-shrink-0">
                  <span className="text-xs text-white font-bold">LB</span>
                </div>
                <div className="bg-gray-800 px-4 py-3 rounded-2xl rounded-bl-md">
                  <div className="flex gap-1.5" data-testid="thinking-indicator">
                    <span className="w-2 h-2 bg-teal-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                    <span className="w-2 h-2 bg-teal-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                    <span className="w-2 h-2 bg-teal-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Voice Visualizer */}
          {isRecording && (
            <div className="px-4 py-2 border-t border-gray-800 bg-gray-900/80">
              <VoiceVisualizer
                active={isRecording}
                level={0.6}
                barCount={24}
                dataTestId="live-voice-visualizer"
                className="h-8"
              />
              <p className="text-center text-xs text-teal-400 mt-1">Listening...</p>
            </div>
          )}

          {/* Input Area */}
          <div className="px-4 py-3 bg-gray-800 border-t border-gray-700">
            <div className="flex items-center gap-3">
              {/* Record Button */}
              <button
                onClick={isRecording ? stopRecording : startRecording}
                disabled={!isConnected}
                data-testid="voice-record-btn"
                className={`w-12 h-12 rounded-full flex items-center justify-center transition-all flex-shrink-0 ${
                  isRecording
                    ? 'bg-red-600 hover:bg-red-700 animate-pulse ring-4 ring-red-600/30'
                    : isConnected
                      ? 'bg-teal-600 hover:bg-teal-700'
                      : 'bg-gray-600 cursor-not-allowed'
                }`}
                aria-label={isRecording ? 'Stop recording' : 'Start recording'}
              >
                {isRecording ? (
                  <svg className="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 24 24">
                    <rect x="6" y="6" width="12" height="12" rx="2" />
                  </svg>
                ) : (
                  <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z"
                    />
                  </svg>
                )}
              </button>

              {/* Text Input */}
              <input
                type="text"
                value={textInput}
                onChange={(e) => setTextInput(e.target.value)}
                onKeyDown={handleKeyDown}
                disabled={!isConnected}
                placeholder={isConnected ? 'Type a message or press the mic to speak...' : 'Connect to start'}
                data-testid="voice-text-input"
                className="flex-1 bg-gray-700 text-white text-sm rounded-lg px-4 py-3 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-teal-500 disabled:opacity-50"
              />

              {/* Send Button */}
              <button
                onClick={handleSend}
                disabled={!isConnected || !textInput.trim()}
                data-testid="voice-send-btn"
                className="w-12 h-12 rounded-full bg-teal-600 hover:bg-teal-700 disabled:bg-gray-600 disabled:cursor-not-allowed flex items-center justify-center transition-all flex-shrink-0"
                aria-label="Send message"
              >
                <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                </svg>
              </button>

              {/* Clear Button */}
              {messages.length > 0 && (
                <button
                  onClick={clearMessages}
                  data-testid="voice-clear-btn"
                  className="w-10 h-10 rounded-full bg-gray-700 hover:bg-gray-600 flex items-center justify-center transition-all flex-shrink-0"
                  aria-label="Clear conversation"
                >
                  <svg className="w-4 h-4 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                  </svg>
                </button>
              )}
            </div>
          </div>
        </div>

        {/* Right Sidebar -- Tool Calls & Activity */}
        <aside
          data-testid="tool-calls-sidebar"
          className="w-72 flex-shrink-0 bg-gray-900 border border-gray-700 rounded-xl overflow-hidden hidden xl:flex flex-col"
        >
          {/* Sidebar Tabs */}
          <div className="flex border-b border-gray-700">
            <button
              onClick={() => setSidebarTab('tools')}
              className={`flex-1 px-4 py-3 text-xs font-medium transition-colors ${
                sidebarTab === 'tools'
                  ? 'text-teal-400 border-b-2 border-teal-400 bg-gray-800/50'
                  : 'text-gray-400 hover:text-gray-300'
              }`}
              data-testid="sidebar-tab-tools"
            >
              Tool Calls ({toolCallMessages.length})
            </button>
            <button
              onClick={() => setSidebarTab('history')}
              className={`flex-1 px-4 py-3 text-xs font-medium transition-colors ${
                sidebarTab === 'history'
                  ? 'text-teal-400 border-b-2 border-teal-400 bg-gray-800/50'
                  : 'text-gray-400 hover:text-gray-300'
              }`}
              data-testid="sidebar-tab-history"
            >
              Activity ({messages.length})
            </button>
          </div>

          {/* Sidebar Content */}
          <div className="flex-1 overflow-y-auto p-3 space-y-3">
            {sidebarTab === 'tools' && (
              <>
                {toolCallMessages.length === 0 ? (
                  <div className="text-center text-gray-400 text-xs mt-8 px-4">
                    <p>Tool calls from the agent will appear here as they execute.</p>
                  </div>
                ) : (
                  toolCallMessages.map((msg) => (
                    <ToolCallCard key={msg.id} message={msg} />
                  ))
                )}
              </>
            )}
            {sidebarTab === 'history' && (
              <>
                {messages.length === 0 ? (
                  <div className="text-center text-gray-400 text-xs mt-8 px-4">
                    <p>Conversation activity will appear here.</p>
                  </div>
                ) : (
                  messages.map((msg) => (
                    <div
                      key={msg.id}
                      className="flex items-start gap-2 text-xs"
                      data-testid="activity-entry"
                    >
                      <div
                        className={`w-1.5 h-1.5 rounded-full mt-1.5 flex-shrink-0 ${
                          msg.role === 'user'
                            ? 'bg-teal-400'
                            : msg.role === 'system'
                              ? 'bg-yellow-400'
                              : 'bg-gray-400'
                        }`}
                      />
                      <div className="min-w-0">
                        <span className="text-gray-500 font-medium">
                          {msg.role === 'user' ? 'You' : msg.role === 'system' ? 'System' : 'LedgerBot'}
                        </span>
                        <p className="text-gray-400 truncate">{msg.text}</p>
                        <span className="text-gray-400">
                          {new Date(msg.timestamp).toLocaleTimeString()}
                        </span>
                      </div>
                    </div>
                  ))
                )}
              </>
            )}
          </div>

          {/* Sidebar Footer */}
          <div className="p-3 border-t border-gray-700 bg-gray-800/50">
            <div className="flex items-center justify-between text-xs text-gray-500">
              <span>Gemini Live API</span>
              <span>w181</span>
            </div>
          </div>
        </aside>
      </div>
    </div>
  )
}
