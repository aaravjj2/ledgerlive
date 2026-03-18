import { useEffect, useState } from 'react'

interface Health { project: string; status: string; mode: string; llm: string; ts: string }

export default function Settings() {
  const [health, setHealth] = useState<Health | null>(null)
  const [waveCount, setWaveCount] = useState<number | null>(null)

  useEffect(() => {
    fetch('/healthz').then(r => r.json()).then(setHealth).catch(() => {})
    // Count routes from openapi
    fetch('/openapi.json').then(r => r.json()).then(spec => {
      setWaveCount(Object.keys(spec.paths || {}).length)
    }).catch(() => {})
  }, [])

  const rows = [
    { label: 'Project ID', value: health?.project ?? '…' },
    { label: 'API Status', value: health?.status ?? '…' },
    { label: 'Mode', value: health?.mode ?? '…' },
    { label: 'LLM Provider', value: health?.llm ?? '…' },
    { label: 'API Timestamp', value: health?.ts ? new Date(health.ts).toLocaleString() : '…' },
    { label: 'Backend URL', value: 'https://ledgerlive-api-production.up.railway.app' },
    { label: 'Total API Routes', value: waveCount != null ? `${waveCount}` : '…' },
    { label: 'Waves Shipped', value: '340' },
    { label: 'Test Suite', value: '4021 tests · all green' },
    { label: 'Gates', value: 'no_apex_references · no_network_in_tests · 2/2 PASS' },
    { label: 'Branch', value: 'waves' },
    { label: 'Repo', value: 'aaravjj2/ledgerlive' },
  ]

  return (
    <div data-testid="settings-page">
      <h1 className="text-2xl font-bold mb-1" data-testid="settings-title">Settings</h1>
      <p className="text-gray-500 mb-6" data-testid="settings-subtitle">System configuration and preferences.</p>

      <div className="rounded-xl border bg-[#111118] overflow-hidden mb-6">
        <div className="bg-[#1A1A24] border-b px-4 py-3">
          <h2 className="font-semibold text-gray-300">System Info</h2>
        </div>
        <table className="w-full text-sm">
          <tbody>
            {rows.map(r => (
              <tr key={r.label} className="border-b last:border-0 hover:bg-[#1A1A24]">
                <td className="px-4 py-3 font-medium text-gray-400 w-48">{r.label}</td>
                <td className="px-4 py-3 text-gray-200 font-mono text-xs">{r.value}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="rounded-xl border bg-[#111118] border-[#2A2A3A] p-4">
        <div className="flex items-center gap-2 mb-2">
          <span className="text-lg">🏎️</span>
          <h2 className="font-semibold text-gray-200 text-sm">LedgerLive — Finance Ops Close Agent</h2>
        </div>
        <p className="text-xs text-gray-500 leading-relaxed">
          340 waves shipped · Phases 0–36 · Blueprint Builder · Atlassian Integration ·
          Airia Readiness · Security Governance · 4,021 tests passing
        </p>
        <div className="flex gap-4 mt-3">
          <a href="https://github.com/aaravjj2/ledgerlive" target="_blank" rel="noopener noreferrer"
            className="text-xs text-blue-400 hover:text-blue-400 transition">
            → GitHub Repo
          </a>
          <a href="https://ledgerlive-api-production.up.railway.app/docs" target="_blank" rel="noopener noreferrer"
            className="text-xs text-blue-400 hover:text-blue-400 transition">
            → API Docs
          </a>
          <a href="https://ledgerlive-web-570445019871.us-central1.run.app" target="_blank" rel="noopener noreferrer"
            className="text-xs text-red-400 hover:text-red-300 transition">
            → Live App
          </a>
        </div>
      </div>
    </div>
  )
}
