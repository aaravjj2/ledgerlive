import { useState, useRef, useCallback, useEffect } from 'react'

interface VoiceMessage {
  id: string
  role: 'user' | 'assistant' | 'system'
  text: string
  timestamp: string
  type: 'text' | 'audio' | 'tool_call'
  toolName?: string
  toolArgs?: Record<string, unknown>
}

interface VoiceState {
  isConnected: boolean
  isRecording: boolean
  isSpeaking: boolean
  isThinking: boolean
  messages: VoiceMessage[]
  error: string | null
}

export type { VoiceMessage, VoiceState }

export function useVoiceAssistant() {
  const [state, setState] = useState<VoiceState>({
    isConnected: false,
    isRecording: false,
    isSpeaking: false,
    isThinking: false,
    messages: [],
    error: null,
  })

  const wsRef = useRef<WebSocket | null>(null)
  const mediaRecorderRef = useRef<MediaRecorder | null>(null)
  const audioContextRef = useRef<AudioContext | null>(null)
  const streamRef = useRef<MediaStream | null>(null)

  const addMessage = useCallback((msg: Omit<VoiceMessage, 'id' | 'timestamp'>) => {
    setState(prev => ({
      ...prev,
      messages: [...prev.messages, {
        ...msg,
        id: crypto.randomUUID(),
        timestamp: new Date().toISOString(),
      }],
    }))
  }, [])

  const connect = useCallback(() => {
    // In production, use VITE_WS_URL pointing directly to the Cloud Run API backend.
    // In development, derive from window.location (Vite proxy handles it).
    const viteWsUrl = (import.meta as { env?: { VITE_WS_URL?: string } }).env?.VITE_WS_URL
    let wsUrl: string
    if (viteWsUrl) {
      wsUrl = `${viteWsUrl.replace(/\/$/, '')}/ws/voice`
    } else {
      const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
      const host = window.location.hostname
      const port = window.location.port || (window.location.protocol === 'https:' ? '443' : '80')
      wsUrl = `${protocol}//${host}:${port}/ws/voice`
    }

    const ws = new WebSocket(wsUrl)

    ws.onopen = () => {
      setState(prev => ({ ...prev, isConnected: true, error: null }))
    }

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data)
        if (data.type === 'text') {
          addMessage({ role: data.role || 'assistant', text: data.text, type: 'text' })
          setState(prev => ({ ...prev, isThinking: false, isSpeaking: false }))
        } else if (data.type === 'tool_call') {
          addMessage({
            role: 'system',
            text: `Calling tool: ${data.name}`,
            type: 'tool_call',
            toolName: data.name,
            toolArgs: data.args,
          })
        } else if (data.type === 'error') {
          setState(prev => ({ ...prev, error: data.message, isThinking: false }))
        }
      } catch {
        setState(prev => ({ ...prev, error: 'Failed to parse server message' }))
      }
    }

    ws.onclose = () => {
      setState(prev => ({ ...prev, isConnected: false }))
    }

    ws.onerror = () => {
      setState(prev => ({
        ...prev,
        error: 'Connection failed. Check if the backend is running.',
      }))
    }

    wsRef.current = ws
  }, [addMessage])

  const disconnect = useCallback(() => {
    wsRef.current?.close()
    wsRef.current = null
    if (streamRef.current) {
      streamRef.current.getTracks().forEach(t => t.stop())
      streamRef.current = null
    }
    setState(prev => ({ ...prev, isConnected: false, isRecording: false }))
  }, [])

  const sendText = useCallback((text: string) => {
    if (!wsRef.current || wsRef.current.readyState !== WebSocket.OPEN) return
    addMessage({ role: 'user', text, type: 'text' })
    setState(prev => ({ ...prev, isThinking: true }))
    wsRef.current.send(JSON.stringify({ type: 'text', text }))
  }, [addMessage])

  const startRecording = useCallback(async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
      streamRef.current = stream
      const audioContext = new AudioContext({ sampleRate: 16000 })
      audioContextRef.current = audioContext

      const source = audioContext.createMediaStreamSource(stream)
      const processor = audioContext.createScriptProcessor(4096, 1, 1)

      processor.onaudioprocess = (e) => {
        if (!wsRef.current || wsRef.current.readyState !== WebSocket.OPEN) return
        const pcmData = e.inputBuffer.getChannelData(0)
        const int16 = new Int16Array(pcmData.length)
        for (let i = 0; i < pcmData.length; i++) {
          int16[i] = Math.max(-32768, Math.min(32767, Math.floor(pcmData[i] * 32768)))
        }
        const b64 = btoa(String.fromCharCode(...new Uint8Array(int16.buffer)))
        wsRef.current.send(JSON.stringify({ type: 'audio', data: b64 }))
      }

      source.connect(processor)
      processor.connect(audioContext.destination)
      setState(prev => ({ ...prev, isRecording: true }))
      addMessage({ role: 'user', text: '[Recording audio...]', type: 'audio' })
    } catch {
      setState(prev => ({ ...prev, error: 'Microphone access denied' }))
    }
  }, [addMessage])

  const stopRecording = useCallback(() => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach(t => t.stop())
      streamRef.current = null
    }
    if (audioContextRef.current) {
      audioContextRef.current.close()
      audioContextRef.current = null
    }
    mediaRecorderRef.current = null
    setState(prev => ({ ...prev, isRecording: false, isThinking: true }))
  }, [])

  const clearMessages = useCallback(() => {
    setState(prev => ({ ...prev, messages: [] }))
  }, [])

  const dismissError = useCallback(() => {
    setState(prev => ({ ...prev, error: null }))
  }, [])

  useEffect(() => {
    return () => {
      disconnect()
    }
  }, [disconnect])

  return {
    ...state,
    connect,
    disconnect,
    sendText,
    startRecording,
    stopRecording,
    clearMessages,
    dismissError,
  }
}
