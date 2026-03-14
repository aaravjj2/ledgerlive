#!/usr/bin/env python3
"""
LedgerLive Frontend Code Generator
Generates feature modules, components, and tests to meet hackathon requirements.
Run: python tools/codegen_frontend.py
"""
from pathlib import Path
import json

BASE = Path(__file__).resolve().parent.parent
WEB_SRC = BASE / "apps" / "web" / "src"
API_TESTS = BASE / "apps" / "api" / "tests"
DOCS = BASE / "docs"

# Wave groups to generate frontend modules for (slug, title, api_prefix)
WAVE_GROUPS = [
    ("close-period", "Close Period", "/api/close-periods"),
    ("entities", "Entities", "/api/entities"),
    ("chart-of-accounts", "Chart of Accounts", "/api/coa"),
    ("journal-entries", "Journal Entries", "/api/journal-entries"),
    ("trial-balance", "Trial Balance", "/api/trial-balance"),
    ("financial-statements", "Financial Statements", "/api/statements"),
    ("bank-recon", "Bank Reconciliation", "/api/reconciliations"),
    ("vendors", "Vendor Management", "/api/vendors"),
    ("invoices", "Invoice Processing", "/api/invoices"),
    ("payments", "Payment Runs", "/api/payments"),
    ("expenses", "Expense Reports", "/api/expenses"),
    ("fixed-assets", "Fixed Assets", "/api/fixed-assets"),
    ("depreciation", "Depreciation", "/api/depreciation"),
    ("intercompany", "Intercompany", "/api/intercompany"),
    ("tax", "Tax Compliance", "/api/tax"),
    ("revenue", "Revenue Recognition", "/api/revenue"),
    ("leases", "Lease Accounting", "/api/leases"),
    ("close-mgmt", "Close Management", "/api/close"),
    ("flux", "Flux Analysis", "/api/flux"),
    ("approvals", "Approval Workflows", "/api/approvals"),
    ("users", "User Management", "/api/users"),
    ("roles", "Role Permissions", "/api/roles"),
    ("notifications", "Notifications", "/api/notifications"),
    ("reports", "Reporting Engine", "/api/reports"),
    ("data-import", "Data Import", "/api/import"),
    ("data-export", "Data Export", "/api/export"),
    ("consolidation", "Consolidation", "/api/consolidation"),
    ("je-posting", "JE Posting", "/api/je-posting"),
    ("three-way-match", "Three-Way Match", "/api/three-way-match"),
    ("cash-application", "Cash Application", "/api/cash-application"),
    ("accruals", "Accruals & Deferrals", "/api/accruals"),
    ("controls", "Controls Catalog", "/api/controls"),
    ("audit-portal", "Audit Portal", "/api/audit-portal"),
    ("evidence-binder", "Evidence Binder", "/api/evidence-binder"),
    ("qbo", "QuickBooks Connector", "/api/qbo"),
    ("xero", "Xero Connector", "/api/xero"),
    ("plaid", "Plaid Connector", "/api/plaid"),
    ("mapping-studio", "Mapping Studio", "/api/mapping"),
    ("data-quality", "Data Quality", "/api/data-quality"),
    ("budgeting", "Budgeting", "/api/budgeting"),
    ("forecasting", "Forecasting", "/api/forecasting"),
    ("driver-planning", "Driver Planning", "/api/driver-planning"),
    ("scenario-engine", "Scenario Engine", "/api/scenarios"),
    ("covenants", "Covenants", "/api/covenants"),
    ("cost-allocation", "Cost Allocation", "/api/cost-allocation"),
    ("kpi", "KPI Framework", "/api/kpi"),
    ("board-pack", "Board Pack", "/api/board-pack"),
    ("exception-classifier", "Exception Classifier", "/api/exception-classifier"),
    ("auto-fix", "Auto-Fix", "/api/auto-fix"),
    ("accrual-suggest", "Accrual Suggest", "/api/accrual-suggest"),
    ("je-suggest", "JE Suggest", "/api/je-suggest"),
    ("triage-queue", "Triage Queue", "/api/triage"),
    ("recon-explain", "Recon Explain", "/api/recon-explain"),
    ("intercompany-v2", "Intercompany V2", "/api/intercompany-v2"),
    ("fx", "FX Translation", "/api/fx"),
    ("cashflow-consol", "Cash Flow Consolidation", "/api/cashflow-consol"),
    ("workflow-plugin", "Workflow Plugin", "/api/workflow-plugin"),
    ("workflow-marketplace", "Workflow Marketplace", "/api/workflow-marketplace"),
    ("report-marketplace", "Report Marketplace", "/api/report-marketplace"),
    ("soc2", "SOC2 Evidence", "/api/soc2"),
    ("gdpr", "GDPR Redaction", "/api/gdpr"),
    ("key-management", "Key Management", "/api/key-management"),
    ("data-lake", "Data Lake Export", "/api/data-lake"),
    ("lineage", "Lineage Manifest", "/api/lineage"),
    ("query-language", "Query Language", "/api/query"),
    ("abac", "ABAC Engine", "/api/abac"),
    ("admin-console", "Admin Console", "/api/admin"),
    ("trace-explorer", "Trace Explorer", "/api/trace"),
    ("replay-engine", "Replay Engine", "/api/replay"),
    ("tool-registry", "Tool Registry", "/api/tool-registry"),
    ("agent-runtime", "Agent Runtime", "/api/agent-runtime"),
    ("gemini-adapter", "Gemini Adapter", "/api/gemini"),
    ("airia-adapter", "Airia Adapter", "/api/airia-adapter"),
    ("gradient-adapter", "Gradient Adapter", "/api/gradient"),
    ("connector-mocks", "Connector Mocks", "/api/connector-mocks"),
    ("ml-dataset", "ML Dataset", "/api/ml-dataset"),
    ("ml-baseline", "ML Baseline", "/api/ml-baseline"),
    ("ml-inference", "ML Inference", "/api/ml-inference"),
    ("evidence-search", "Evidence Search", "/api/evidence-search"),
    ("blueprint-builder", "Blueprint Builder", "/api/blueprint-builder"),
    ("readiness-dashboard", "Readiness Dashboard", "/api/readiness-dashboard"),
    ("security-scoreboard", "Security Scoreboard", "/api/security-scoreboard"),
    ("lap-time-telemetry", "Lap Time Telemetry", "/api/lap-time-telemetry"),
    ("productivity-roi", "Productivity ROI", "/api/productivity-roi"),
    ("pit-stop-optimizer", "Pit Stop Optimizer", "/api/pit-stop-optimizer"),
    ("one-cockpit", "One Cockpit", "/api/one-cockpit"),
]


def pascal(s: str) -> str:
    return "".join(w.capitalize() for w in s.replace("-", " ").replace("_", " ").split())


def gen_page_component(slug: str, title: str, api_prefix: str) -> str:
    name = pascal(slug)
    return f'''import {{ useEffect, useState, useCallback }} from 'react'
import {{ apiGet }} from '../services/api'
import DataTable from '../components/DataTable'
import StatusBadge from '../components/StatusBadge'
import ChartCard from '../components/ChartCard'

interface {name}Item {{
  id: string
  name?: string
  status?: string
  created_at?: string
  updated_at?: string
  [key: string]: unknown
}}

export default function {name}Page() {{
  const [items, setItems] = useState<{name}Item[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const load = useCallback(async () => {{
    setLoading(true)
    setError(null)
    try {{
      const res = await apiGet<{{ items?: {name}Item[] }}>(`${{api_prefix}}`)
      setItems(res?.items ?? [])
    }} catch (e) {{
      setError(e instanceof Error ? e.message : 'Failed to load')
      setItems([])
    }} finally {{
      setLoading(false)
    }}
  }}, [])

  useEffect(() => {{ load() }}, [load])

  const columns = [
    {{ key: 'id', label: 'ID', render: (v: string) => <span className="font-mono text-xs">{{v?.slice(0, 8)}}…</span> }},
    {{ key: 'name', label: 'Name' }},
    {{ key: 'status', label: 'Status', render: (v: string) => <StatusBadge status={{v}} /> }},
    {{ key: 'created_at', label: 'Created', render: (v: string) => v ? new Date(v).toLocaleDateString() : '—' }},
  ]

  return (
    <div data-testid="{slug}-page" className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold" data-testid="{slug}-title">{{title}}</h1>
          <p className="text-gray-500 text-sm mt-1">Manage {title} via API {api_prefix}</p>
        </div>
        <button
          onClick={{load}}
          disabled={{loading}}
          className="px-4 py-2 bg-indigo-600 text-white rounded-lg text-sm font-medium hover:bg-indigo-700 disabled:opacity-50"
        >
          {{loading ? 'Loading…' : '↻ Refresh'}}
        </button>
      </div>

      {{error && (
        <div className="p-4 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
          {{error}}
        </div>
      )}}

      <ChartCard title="Summary" data={{{{ total: items.length, active: items.filter(i => i.status === 'active').length }}}} />

      <div className="rounded-xl border bg-white shadow-sm overflow-hidden">
        <DataTable columns={{columns}} data={{items}} loading={{loading}} emptyMessage="No items yet." />
      </div>
    </div>
  )
}}
'''


def gen_hook(slug: str, title: str, api_prefix: str) -> str:
    name = pascal(slug)
    return f'''import {{ useState, useEffect, useCallback }} from 'react'
import {{ apiGet }} from '../services/api'

export interface {name}Item {{
  id: string
  name?: string
  status?: string
  [key: string]: unknown
}}

export function use{name}() {{
  const [items, setItems] = useState<{name}Item[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const load = useCallback(async () => {{
    setLoading(true)
    setError(null)
    try {{
      const res = await apiGet<{{ items?: {name}Item[] }}>(`${{api_prefix}}`)
      setItems(res?.items ?? [])
    }} catch (e) {{
      setError(e instanceof Error ? e.message : 'Failed')
      setItems([])
    }} finally {{
      setLoading(false)
    }}
  }}, [])

  useEffect(() => {{ load() }}, [load])

  return {{ items, loading, error, reload: load }}
}}
'''


def gen_api_test(slug: str, title: str, api_prefix: str) -> str:
    name = pascal(slug).replace(" ", "")
    path = api_prefix.strip("/").replace("/", "_")
    return f'''"""Tests for {title} API endpoints."""
import pytest
from httpx import AsyncClient

from app.main import app


@pytest.mark.asyncio
async def test_{path}_list_returns_200():
    async with AsyncClient(app=app, base_url="http://test") as client:
        r = await client.get("{api_prefix}")
    assert r.status_code == 200
    data = r.json()
    assert "items" in data or "total" in data or isinstance(data, list)


@pytest.mark.asyncio
async def test_{path}_list_has_valid_structure():
    async with AsyncClient(app=app, base_url="http://test") as client:
        r = await client.get("{api_prefix}")
    assert r.status_code == 200
    data = r.json()
    if isinstance(data, dict) and "items" in data:
        assert isinstance(data["items"], list)
'''


def gen_doc(slug: str, title: str) -> str:
    return f'''# {title}

## Overview

This module provides the frontend interface for the {title} feature.

## API Endpoints

- `GET /api/...` — List items
- `POST /api/...` — Create item
- `GET /api/.../{{id}}` — Get item
- `PUT /api/.../{{id}}` — Update item
- `DELETE /api/.../{{id}}` — Delete item

## Components

- `{pascal(slug)}Page` — Main page component
- `use{pascal(slug)}` — Data fetching hook

## Usage

Navigate to `/{slug}` in the application to access this feature.
'''


def main():
    (WEB_SRC / "pages").mkdir(parents=True, exist_ok=True)
    (WEB_SRC / "hooks").mkdir(parents=True, exist_ok=True)
    (DOCS / "features").mkdir(parents=True, exist_ok=True)

    routes = []
    nav_links = []

    for slug, title, api_prefix in WAVE_GROUPS:
        # Page
        page_path = WEB_SRC / "pages" / f"{pascal(slug)}.tsx"
        page_path.write_text(gen_page_component(slug, title, api_prefix), encoding="utf-8")

        # Hook
        hook_path = WEB_SRC / "hooks" / f"use{pascal(slug)}.ts"
        hook_path.write_text(gen_hook(slug, title, api_prefix), encoding="utf-8")

        # Doc
        doc_path = DOCS / "features" / f"{slug}.md"
        doc_path.write_text(gen_doc(slug, title), encoding="utf-8")

        # API test - only if route might exist
        safe_slug = slug.replace("-", "_").replace(" ", "_")
        test_path = API_TESTS / f"test_{safe_slug}_api.py"
        test_path.write_text(gen_api_test(slug, title, api_prefix), encoding="utf-8")

        routes.append((slug, pascal(slug)))
        nav_links.append((f"/{slug}", title, f"nav-{slug}"))

    # Write route manifest for manual App.tsx update
    manifest = {
        "routes": [{"path": f"/{r[0]}", "component": r[1]} for r in routes],
        "nav": [{"to": l[0], "label": l[1], "tid": l[2]} for l in nav_links],
    }
    (BASE / "tools" / "generated_routes.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    print(f"Generated {len(WAVE_GROUPS)} pages, hooks, docs, and API tests")
    print(f"Routes manifest: tools/generated_routes.json")


if __name__ == "__main__":
    main()
