/**
 * Airia Everywhere Hub — Airia AI Agents Hackathon (Track 1)
 * Meet users where they are: browser extension, Slack, Teams, Outlook, chat widgets.
 */
import { useState } from 'react'

interface Channel {
  id: string
  name: string
  icon: string
  connected: boolean
  lastSync: string
  actions: number
}

const CHANNELS: Channel[] = [
  { id: 'browser', name: 'Browser Extension', icon: '🌐', connected: true, lastSync: '2m ago', actions: 47 },
  { id: 'slack', name: 'Slack', icon: '💬', connected: true, lastSync: '1m ago', actions: 23 },
  { id: 'teams', name: 'Microsoft Teams', icon: '💼', connected: false, lastSync: '—', actions: 0 },
  { id: 'outlook', name: 'Outlook', icon: '📧', connected: true, lastSync: '5m ago', actions: 12 },
  { id: 'chat', name: 'Chat Widget', icon: '💭', connected: true, lastSync: 'now', actions: 89 },
  { id: 'sharepoint', name: 'SharePoint', icon: '📁', connected: false, lastSync: '—', actions: 0 },
  { id: 'whatsapp', name: 'WhatsApp', icon: '📱', connected: false, lastSync: '—', actions: 0 },
]

export default function AiriaEverywhereHub() {
  const [channels, setChannels] = useState<Channel[]>(CHANNELS)
  const [selected, setSelected] = useState<string | null>(null)

  const toggleConnection = (id: string) => {
    setChannels(prev => prev.map(c => c.id === id ? { ...c, connected: !c.connected } : c))
  }

  return (
    <div data-testid="airia-everywhere-hub" className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold" data-testid="airia-everywhere-title">Airia Everywhere</h1>
        <p className="text-gray-500 text-sm mt-1">
          Meet users where they are — browser, Slack, Teams, Outlook, chat. No context-switching.
        </p>
      </div>

      <div className="rounded-xl border bg-indigo-50 border-indigo-200 p-4">
        <h3 className="font-semibold text-indigo-800 mb-2">Track 1: Airia Everywhere</h3>
        <p className="text-sm text-indigo-700">
          LedgerLive agents integrate into the platforms people use every day. Ask the CFO assistant from Slack,
          triage exceptions from Outlook, or run close checks from a browser extension — intelligence exactly when needed.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {channels.map(c => (
          <div
            key={c.id}
            data-testid={`airia-channel-${c.id}`}
            onClick={() => setSelected(c.id)}
            className={`rounded-xl border p-4 cursor-pointer transition ${
              selected === c.id ? 'border-indigo-500 bg-indigo-50' : 'border-gray-200 hover:border-indigo-300'
            }`}
          >
            <div className="flex items-center justify-between mb-2">
              <span className="text-2xl">{c.icon}</span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${
                c.connected ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-600'
              }`}>
                {c.connected ? 'Connected' : 'Disconnected'}
              </span>
            </div>
            <div className="font-semibold text-gray-800">{c.name}</div>
            <div className="text-xs text-gray-500 mt-1">
              Last sync: {c.lastSync} · {c.actions} actions
            </div>
            <button
              onClick={e => { e.stopPropagation(); toggleConnection(c.id) }}
              className="mt-3 w-full py-1.5 text-xs rounded bg-indigo-600 text-white hover:bg-indigo-700"
            >
              {c.connected ? 'Disconnect' : 'Connect'}
            </button>
          </div>
        ))}
      </div>

      <div className="rounded-xl border bg-white p-4">
        <h2 className="font-semibold mb-3">Recent Channel Actions</h2>
        <div className="space-y-2 text-sm">
          <div className="flex justify-between py-2 border-b">
            <span>Browser: Asked CFO about Q4 variance</span>
            <span className="text-gray-500">2m ago</span>
          </div>
          <div className="flex justify-between py-2 border-b">
            <span>Slack: /ledgerlive status</span>
            <span className="text-gray-500">5m ago</span>
          </div>
          <div className="flex justify-between py-2 border-b">
            <span>Outlook: Triage exception EX-001</span>
            <span className="text-gray-500">8m ago</span>
          </div>
          <div className="flex justify-between py-2">
            <span>Chat: Run canonical close</span>
            <span className="text-gray-500">12m ago</span>
          </div>
        </div>
      </div>
    </div>
  )
}
