#!/usr/bin/env python3
"""Fix generated pages: substitute api_prefix and title with actual values."""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
WEB_SRC = BASE / "apps" / "web" / "src"
PAGES = WEB_SRC / "pages"
HOOKS = WEB_SRC / "hooks"
MANIFEST = BASE / "tools" / "generated_routes.json"

# Load route manifest to get path->component mapping, then derive slug from path
with open(MANIFEST) as f:
    data = json.load(f)

# Build slug -> (title, api_prefix) from WAVE_GROUPS
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

slug_map = {s[0]: (s[1], s[2]) for s in WAVE_GROUPS}

def pascal(s: str) -> str:
    return "".join(w.capitalize() for w in s.replace("-", " ").replace("_", " ").split())

fixed = 0
for slug, (title, api_prefix) in slug_map.items():
    comp = pascal(slug)
    path = WEB_SRC / f"{comp}.tsx"
    if not path.exists():
        continue
    content = path.read_text(encoding="utf-8")
    if "api_prefix" in content and "${api_prefix}" in content:
        content = content.replace("`${api_prefix}`", f"`{api_prefix}`")
        content = content.replace("{title}", title)
        # Fix the Manage line - it might have {title} and {api_prefix} as literal
        content = content.replace(f"Manage {{title}} via API {{api_prefix}}", f"Manage {title} via API {api_prefix}")
        path.write_text(content, encoding="utf-8")
        fixed += 1

print(f"Fixed {fixed} page files")
