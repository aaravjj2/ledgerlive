import { useState, useEffect, useCallback } from 'react'

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

interface CompatCheck {
  id: string
  name: string
  passed: boolean
  status: string
  reason: string
}

interface CompatReport {
  overall: string
  checks: CompatCheck[]
  bundle_sha256: string
  blueprint_sha256: string
  tools_sha256: string
  report_signature_sha256: string
  pass_count: number
  fail_count: number
}

const API = 'http://127.0.0.1:8090'

// Metadata for the No-Code Preview — maps tool IDs to display properties
const TOOL_NOCODE_META: Record<string, { approval_required: boolean; fail_closed: boolean; evidence_required: boolean; step: number }> = {
  'ledgerlive.ingest':           { approval_required: false, fail_closed: true,  evidence_required: true,  step: 1 },
  'ledgerlive.reconcile':        { approval_required: false, fail_closed: true,  evidence_required: true,  step: 2 },
  'ledgerlive.triage':           { approval_required: false, fail_closed: false, evidence_required: true,  step: 3 },
  'ledgerlive.hitl_review':      { approval_required: true,  fail_closed: true,  evidence_required: true,  step: 4 },
  'ledgerlive.audit_trail':      { approval_required: false, fail_closed: false, evidence_required: true,  step: 5 },
  'ledgerlive.evidence_binder':  { approval_required: true,  fail_closed: true,  evidence_required: true,  step: 6 },
  'ledgerlive.blueprint_builder':{ approval_required: false, fail_closed: false, evidence_required: false, step: 7 },
  'ledgerlive.race_control':     { approval_required: false, fail_closed: false, evidence_required: true,  step: 8 },
}

const IMPORT_WALKTHROUGH_STEPS = [
  { step: 1, title: 'Upload bundle archive', detail: 'In Airia, navigate to Templates → Import. Upload the community_bundle/ directory. Airia validates manifest.json and checksums.txt automatically.', endpoint: 'POST /api/airia/validate-bundle' },
  { step: 2, title: 'Configure trigger', detail: 'Set trigger type: manual, scheduled, or webhook. For demo mode, choose manual. Airia creates a run card for each trigger type.', endpoint: null },
  { step: 3, title: 'Map tool credentials', detail: 'Each tool may need API credentials. In DEMO mode all tools run with deterministic mock responses — no credentials required.', endpoint: 'GET /api/airia/status' },
  { step: 4, title: 'Configure HITL approval chain', detail: 'The ledgerlive.hitl_review step creates an approval gate. Add approver emails. Workflow halts (fail-closed) until all approvers confirm.', endpoint: null },
  { step: 5, title: 'Validate blueprint', detail: 'Click Validate to verify the workflow DAG is acyclic, tool schemas are version-pinned, and fail-closed rules are enabled.', endpoint: 'GET /api/airia/compat_report' },
  { step: 6, title: 'Run first close cycle', detail: 'Click Run Canonical on Race Control, or trigger from Airia. The full close pipeline executes: ingest → reconcile → triage → review → close.', endpoint: 'POST /api/ops/golden-scenario-run' },
  { step: 7, title: 'Export evidence packs', detail: 'After close, export the Telemetry Pack (tool traces) and Court Pack (stewards evidence). Both are deterministic.', endpoint: 'POST /api/ops/export/telemetry-pack' },
]

function buildImportNotesText(): string {
  return IMPORT_WALKTHROUGH_STEPS
    .map(s => `Step ${s.step}: ${s.title}\n  ${s.detail}${s.endpoint ? `\n  Endpoint: ${s.endpoint}` : ''}`)
    .join('\n\n')
}

export default function AiriaReadiness() {
  const [status, setStatus] = useState<BundleStatus | null>(null)
  const [loading, setLoading] = useState(true)
  const [compatReport, setCompatReport] = useState<CompatReport | null>(null)
  const [generateResult, setGenerateResult] = useState<string | null>(null)
  const [validateResult, setValidateResult] = useState<string | null>(null)
  const [verifyResult, setVerifyResult] = useState<string | null>(null)
  const [actionLoading, setActionLoading] = useState(false)
  const [copySuccess, setCopySuccess] = useState(false)

  const fetchStatus = useCallback(() => {
    fetch(`${API}/api/airia/status`)
      .then(r => r.json())
      .then(data => { setStatus(data); setLoading(false) })
      .catch(() => setLoading(false))
  }, [])

  const fetchCompat = useCallback(() => {
    fetch(`${API}/api/airia/compat_report`)
      .then(r => r.json())
      .then(data => setCompatReport(data))
      .catch(() => {/* non-fatal */})
  }, [])

  useEffect(() => {
    fetchStatus()
    fetchCompat()
  }, [fetchStatus, fetchCompat])

  async function handleGenerate() {
    setActionLoading(true)
    setGenerateResult(null)
    try {
      const r = await fetch(`${API}/api/airia/generate-bundle`, { method: 'POST' })
      const data = await r.json()
      setGenerateResult(data.bundle_hash || data.message || JSON.stringify(data))
      fetchStatus()
      fetchCompat()
    } catch (e) {
      setGenerateResult('Error: could not reach API')
    }
    setActionLoading(false)
  }

  function handleCopyImportNotes() {
    const text = buildImportNotesText()
    navigator.clipboard.writeText(text).then(() => {
      setCopySuccess(true)
      setTimeout(() => setCopySuccess(false), 2000)
    }).catch(() => {
      const ta = document.createElement('textarea')
      ta.value = text
      document.body.appendChild(ta)
      ta.select()
      document.execCommand('copy')
      document.body.removeChild(ta)
      setCopySuccess(true)
      setTimeout(() => setCopySuccess(false), 2000)
    })
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
        <div className="flex items-center gap-3 mb-1 flex-wrap">
          <h1 className="text-3xl font-bold text-white">🤖 Airia Readiness</h1>
          <span
            data-testid="airia-validator-badge"
            className={`px-3 py-1 rounded-full text-sm font-bold ${badgeColour(status?.validator_status ?? null)}`}
          >
            {status?.validator_status ?? (loading ? '…' : 'UNKNOWN')}
          </span>
          {compatReport && (
            <span
              data-testid="airia-compat-badge"
              className={`px-3 py-1 rounded-full text-sm font-bold ${badgeColour(compatReport.overall)}`}
              title={`Compat: ${compatReport.overall} (${compatReport.pass_count}/${compatReport.pass_count + compatReport.fail_count} checks)`}
            >
              Compat: {compatReport.overall}
            </span>
          )}
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

      {/* Compat Report Detail */}
      {compatReport && (
        <div className="bg-gray-800 rounded-lg p-4 mb-6">
          <div className="flex items-center gap-3 mb-3">
            <h2 className="text-white font-semibold">Airia Compatibility Report</h2>
            <span className={`px-2 py-0.5 rounded text-xs font-bold ${badgeColour(compatReport.overall)}`}>
              {compatReport.overall}
            </span>
          </div>
          <div className="grid grid-cols-2 gap-1 mb-3">
            {compatReport.checks.map(c => (
              <div key={c.id} className="flex items-center gap-2 text-xs">
                <span className={c.passed ? 'text-green-400' : 'text-red-400'}>{c.passed ? '✓' : '✗'}</span>
                <span className="text-gray-300">{c.name}</span>
              </div>
            ))}
          </div>
          <div className="text-xs font-mono text-gray-400 space-y-1">
            <div>bundle_sha: <span className="text-green-400">{compatReport.bundle_sha256.slice(0, 32)}…</span></div>
            <div>report_sig: <span className="text-blue-400">{compatReport.report_signature_sha256.slice(0, 32)}…</span></div>
          </div>
        </div>
      )}

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

      {/* No-Code Builder Preview */}
      <div data-testid="airia-nocode-preview" className="bg-gray-800 rounded-lg p-4 mb-6">
        <h2 className="text-white font-semibold mb-1">No-Code Builder Preview</h2>
        <p className="text-gray-400 text-xs mb-4">Workflow DAG — each card is a configurable step in the Airia no-code builder</p>
        <div className="flex flex-wrap gap-3">
          {(status?.tools ?? []).map((tool, idx) => {
            const meta = TOOL_NOCODE_META[tool.id] ?? { approval_required: false, fail_closed: false, evidence_required: true, step: idx + 1 }
            return (
              <div
                key={tool.id}
                data-testid="airia-nocode-step-card"
                className="bg-gray-700 border border-gray-600 rounded-lg p-3 min-w-[160px] max-w-[200px] flex-1"
              >
                <div className="text-gray-400 text-xs mb-1">#{meta.step}</div>
                <div className="text-white font-medium text-sm leading-tight mb-1">{tool.name}</div>
                <div className="text-gray-400 font-mono text-xs mb-2 truncate">{tool.id}</div>
                <div className="text-gray-500 text-xs mb-2">{tool.type}</div>
                <div className="flex flex-wrap gap-1">
                  {meta.approval_required && (
                    <span className="text-xs px-1 py-0.5 rounded bg-orange-900 text-orange-300">approval-required</span>
                  )}
                  {meta.fail_closed && (
                    <span className="text-xs px-1 py-0.5 rounded bg-red-900 text-red-300">fail-closed</span>
                  )}
                  {meta.evidence_required && (
                    <span className="text-xs px-1 py-0.5 rounded bg-purple-900 text-purple-300">evidence</span>
                  )}
                </div>
              </div>
            )
          })}
        </div>
      </div>

      {/* Import Walkthrough */}
      <div data-testid="airia-import-walkthrough" className="bg-gray-800 rounded-lg p-4 mb-6">
        <div className="flex items-center justify-between mb-3">
          <h2 className="text-white font-semibold">Import Walkthrough</h2>
          <button
            data-testid="airia-copy-import-notes"
            onClick={handleCopyImportNotes}
            className="px-3 py-1 bg-gray-700 hover:bg-gray-600 text-gray-300 hover:text-white rounded text-xs font-medium transition"
          >
            {copySuccess ? '✓ Copied!' : '📋 Copy import notes'}
          </button>
        </div>
        <ol className="space-y-3">
          {IMPORT_WALKTHROUGH_STEPS.map(s => (
            <li key={s.step} className="flex gap-3">
              <span className="flex-shrink-0 w-6 h-6 bg-indigo-600 rounded-full flex items-center justify-center text-white text-xs font-bold">
                {s.step}
              </span>
              <div className="min-w-0">
                <div className="text-white text-sm font-medium">{s.title}</div>
                <div className="text-gray-400 text-xs mt-0.5">{s.detail}</div>
                {s.endpoint && (
                  <div className="text-indigo-400 font-mono text-xs mt-1">{s.endpoint}</div>
                )}
              </div>
            </li>
          ))}
        </ol>
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
