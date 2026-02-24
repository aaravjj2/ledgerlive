import { useState, useEffect } from 'react'

interface Tool {
  id: string
  name: string
  type: string
}

interface BundleStatus {
  bundle_name: string
  bundle_version: string
  bundle_hash: string
  template_hash: string
  validator_status: string
  missing_files: string[]
  tools: Tool[]
  bundle_path: string
  wave_count: number
  test_count: number
}

const API = 'http://127.0.0.1:8090'

export default function AiriaReadiness() {
  const [status, setStatus] = useState<BundleStatus | null>(null)
  const [loading, setLoading] = useState(true)
  const [generateResult, setGenerateResult] = useState<string | null>(null)
  const [validateResult, setValidateResult] = useState<string | null>(null)
  const [verifyResult, setVerifyResult] = useState<string | null>(null)
  const [actionLoading, setActionLoading] = useState(false)

  useEffect(() => {
    fetch(`${API}/api/airia/status`)
      .then(r => r.json())
      .then(data => { setStatus(data); setLoading(false) })
      .catch(() => setLoading(false))
  }, [])

  async function handleGenerate() {
    setActionLoading(true)
    setGenerateResult(null)
    try {
      const r = await fetch(`${API}/api/airia/generate-bundle`, { method: 'POST' })
      const data = await r.json()
      setGenerateResult(data.bundle_hash || data.message || JSON.stringify(data))
      // Refresh status
      const s = await fetch(`${API}/api/airia/status`).then(r => r.json())
      setStatus(s)
    } catch (e) {
      setGenerateResult('Error: could not reach API')
    }
    setActionLoading(false)
  }

  async function handleValidate() {
    setActionLoading(true)
    setValidateResult(null)
    try {
      const r = await fetch(`${API}/api/airia/validate-bundle`, { method: 'POST' })
      const data = await r.json()
      setValidateResult(data.status || JSON.stringify(data))
    } catch (e) {
      setValidateResult('Error: could not reach API')
    }
    setActionLoading(false)
  }

  async function handleVerify() {
    setActionLoading(true)
    setVerifyResult(null)
    try {
      const r = await fetch(`${API}/api/airia/verify-bundle`, { method: 'POST' })
      const data = await r.json()
      setVerifyResult(data.status || JSON.stringify(data))
    } catch (e) {
      setVerifyResult('Error: could not reach API')
    }
    setActionLoading(false)
  }

  const badgeColour = (val: string | null) => {
    if (val === 'PASS') return 'bg-green-600 text-white'
    if (val === 'FAIL') return 'bg-red-600 text-white'
    return 'bg-gray-600 text-white'
  }

  return (
    <div data-testid="airia-readiness-page" className="p-6 max-w-4xl mx-auto">
      {/* Header */}
      <div className="mb-6">
        <div className="flex items-center gap-3 mb-1">
          <h1 className="text-3xl font-bold text-white">🤖 Airia Readiness</h1>
          <span
            data-testid="airia-validator-badge"
            className={`px-3 py-1 rounded-full text-sm font-bold ${badgeColour(status?.validator_status ?? null)}`}
          >
            {status?.validator_status ?? (loading ? '…' : 'UNKNOWN')}
          </span>
        </div>
        <p className="text-gray-400 text-sm">
          Airia × Williams F1 Hackathon — Community Bundle
        </p>
      </div>

      {/* Bundle Hashes */}
      <div className="bg-gray-800 rounded-lg p-4 mb-6 grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <div className="text-gray-400 text-xs mb-1">Bundle Hash</div>
          <div
            data-testid="airia-bundle-hash"
            className="font-mono text-sm text-green-400 break-all"
          >
            {status?.bundle_hash ?? (loading ? 'loading…' : 'N/A')}
          </div>
        </div>
        <div>
          <div className="text-gray-400 text-xs mb-1">Template Hash</div>
          <div
            data-testid="airia-template-hash"
            className="font-mono text-sm text-blue-400 break-all"
          >
            {status?.template_hash ?? (loading ? 'loading…' : 'N/A')}
          </div>
        </div>
      </div>

      {/* Stats */}
      <div className="bg-gray-800 rounded-lg p-4 mb-6 grid grid-cols-3 gap-4 text-center">
        <div>
          <div className="text-2xl font-bold text-white">{status?.wave_count ?? '—'}</div>
          <div className="text-gray-400 text-xs">Waves</div>
        </div>
        <div>
          <div className="text-2xl font-bold text-white">{status?.test_count ?? '—'}+</div>
          <div className="text-gray-400 text-xs">Tests Passing</div>
        </div>
        <div>
          <div className="text-2xl font-bold text-white">{status?.tools?.length ?? '—'}</div>
          <div className="text-gray-400 text-xs">Airia Tools</div>
        </div>
      </div>

      {/* Tools List */}
      <div className="bg-gray-800 rounded-lg p-4 mb-6">
        <h2 className="text-white font-semibold mb-3">Airia Tool Registry</h2>
        <ul data-testid="airia-tools-list" className="space-y-2">
          {(status?.tools ?? []).map(tool => (
            <li key={tool.id} className="flex items-center gap-3">
              <span className="text-green-400 font-mono text-xs bg-gray-700 px-2 py-0.5 rounded">
                {tool.type}
              </span>
              <span className="text-white text-sm">{tool.name}</span>
              <span className="text-gray-500 text-xs ml-auto font-mono">{tool.id}</span>
            </li>
          ))}
          {!loading && !status?.tools?.length && (
            <li className="text-gray-400 text-sm">No tools loaded</li>
          )}
        </ul>
      </div>

      {/* Bundle Path */}
      <div className="bg-gray-800 rounded-lg p-4 mb-6">
        <div className="text-gray-400 text-xs mb-1">Bundle Path</div>
        <div data-testid="airia-bundle-path" className="font-mono text-sm text-gray-300">
          {status?.bundle_path ?? 'artifacts/airia/community_bundle'}
        </div>
      </div>

      {/* Actions */}
      <div className="flex flex-wrap gap-3 mb-6">
        <button
          data-testid="airia-generate-btn"
          onClick={handleGenerate}
          disabled={actionLoading}
          className="px-4 py-2 bg-blue-600 hover:bg-blue-500 text-white rounded font-medium disabled:opacity-50"
        >
          🏗 Generate Airia Community Bundle
        </button>
        <button
          data-testid="airia-validate-btn"
          onClick={handleValidate}
          disabled={actionLoading}
          className="px-4 py-2 bg-green-700 hover:bg-green-600 text-white rounded font-medium disabled:opacity-50"
        >
          ✓ Validate Bundle
        </button>
        <button
          data-testid="airia-verify-btn"
          onClick={handleVerify}
          disabled={actionLoading}
          className="px-4 py-2 bg-purple-700 hover:bg-purple-600 text-white rounded font-medium disabled:opacity-50"
        >
          🔒 Verify Checksums
        </button>
      </div>

      {/* Action Results */}
      <div className="space-y-2">
        {generateResult !== null && (
          <div className="bg-gray-800 rounded p-3">
            <span className="text-gray-400 text-xs mr-2">Generate:</span>
            <span className="font-mono text-sm text-green-400">{generateResult}</span>
          </div>
        )}
        {validateResult !== null && (
          <div className="bg-gray-800 rounded p-3">
            <span className="text-gray-400 text-xs mr-2">Validate:</span>
            <span
              data-testid="airia-verify-status"
              className={`font-bold text-sm ${validateResult === 'PASS' ? 'text-green-400' : 'text-red-400'}`}
            >
              {validateResult}
            </span>
          </div>
        )}
        {verifyResult !== null && (
          <div className="bg-gray-800 rounded p-3">
            <span className="text-gray-400 text-xs mr-2">Verify Checksums:</span>
            <span className={`font-bold text-sm ${verifyResult === 'PASS' ? 'text-green-400' : 'text-red-400'}`}>
              {verifyResult}
            </span>
          </div>
        )}
      </div>
    </div>
  )
}
