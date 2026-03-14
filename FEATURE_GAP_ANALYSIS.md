# LedgerLive — Frontend Feature Gap Analysis

> **Purpose:** Every API feature present in the backend but NOT implemented in the frontend.
> **Date:** 2026-03-07
> **Total API Routes:** 2040+
> **Frontend Pages:** 10 (Dashboard, Documents, Reconciliation, Exceptions, Review, Audit, Settings, Race Control, Airia, NotFound)
> **Gap:** ~95% of API capabilities have no frontend UI

---

## 1. FULLY IMPLEMENTED (Partial Coverage)

| Feature | API Routes | Frontend | Coverage |
|---------|------------|----------|----------|
| Dashboard | /healthz, /api/documents, /api/reconciliations, /api/exceptions, /api/reviews, /api/audit | Dashboard.tsx | Basic counts only |
| Documents | /api/documents CRUD | Documents.tsx | List only, no upload/delete UI |
| Reconciliations | /api/reconciliations | Reconciliation.tsx | List + approve only |
| Exceptions | /api/exceptions | Exceptions.tsx | List + resolve only |
| Review Queue | /api/reviews | ReviewQueue.tsx | List + decide only |
| Audit Log | /api/audit | AuditLog.tsx | List only |
| Race Control | lane-status, incident-log, live-scoreboard, close-checkpoint, rc-approval, rc-state-machine, security-events, golden-scenario-run, export packs, replay | RaceControl.tsx | **Full** |
| Airia Readiness | /api/airia/*, /api/mcp/* | AiriaReadiness.tsx | **Full** |
| Settings | /healthz, /openapi.json | Settings.tsx | Basic info |

---

## 2. NOT IMPLEMENTED — Core Finance (W01–W30)

| Wave | Slug | API Prefix | Missing Frontend |
|------|------|------------|------------------|
| W01 | close_period | /api/close-periods | Close period CRUD, lock, close actions |
| W02 | entity | /api/entities | Entity hierarchy, multi-entity selector |
| W03 | document_store | /api/documents | Upload multipart, download, delete |
| W04 | ocr_pipeline | /api/ocr-jobs | OCR job list, create, retry, stats |
| W05 | extraction | /api/extractions | Extraction results, field mapping |
| W06 | reconciliation | /api/reconciliations | Detail view, match/unmatch, variance drill |
| W07 | exception | /api/exceptions | Exception detail, AI suggestion, triage |
| W08 | review_queue | /api/reviews | Review detail, context, bulk actions |
| W09 | evidence_binder | /api/evidence-binder | Binder view, sign, verify |
| W10 | eval_harness | /api/eval-harness | Eval runs, metrics |
| W11 | tenant | /api/tenants | Tenant management |
| W12 | auth | /api/auth | Login, SSO, tokens |
| W13 | workflow | /api/workflows | Workflow DAG, run, status |
| W14 | notification | /api/notifications | Notification center |
| W15 | connector | /api/connectors | Connector list, sync, config |
| W16 | vendor_master | /api/vendors | Vendor CRUD, risk |
| W17 | chart_of_accounts | /api/chart-of-accounts | COA tree, mapping |
| W18 | continuous_close | /api/continuous-close | Rolling close status |
| W19 | audit_integrity | /api/audit-integrity | Integrity checks |
| W20 | signed_export | /api/signed-export | Export, sign |
| W21 | report | /api/reports | Report builder, run |
| W22 | search_index | /api/search | Full-text search |
| W23 | compliance_bundle | /api/compliance-bundle | Compliance packs |
| W24 | retention | /api/retention | Retention policies |
| W25 | data_privacy | /api/data-privacy | Privacy controls |
| W26 | performance | /api/performance | Perf metrics |
| W27 | release_bundle | /api/release-bundle | Release artifacts |
| W28 | judge_demo | /api/judge-demo | Demo runner |
| W29 | deploy_config | /api/deploy-config | Deploy settings |
| W30 | hardening | /api/hardening | Hardening status |

---

## 3. NOT IMPLEMENTED — Real Company Close (W31–W60)

| Wave | Slug | Missing Frontend |
|------|------|------------------|
| W31 | close_calendar | Calendar view, dependency graph, SLA timers |
| W32 | consolidation | Entity hierarchy, eliminations, adjustments |
| W33 | je_posting | JE batch list, post, lock, reverse |
| W34 | three_way_match | PO/Receipt/Invoice matching UI |
| W35 | cash_application | AR allocations, partial payments |
| W36 | accruals_deferrals | Schedules, proposals, reversals |
| W37 | controls_catalog | SOX controls, evidence mapping |
| W38 | audit_portal | Auditor queries, export |
| W39 | vendor_master_v2 | Vendor families, risk, watchlists |
| W40 | evidence_binder_v2 | Signed binder, Merkle integrity |
| W41 | connector_framework_v2 | Connector capability, sync schedule |
| W42 | qbo_connector | QuickBooks auth, sync |
| W43 | xero_connector | Xero auth, sync |
| W44 | plaid_connector | Plaid bank feeds |
| W45 | mapping_studio | Transform DSL, mapping UI |
| W46 | data_quality | DQ rules, scorecard |
| W47 | continuous_close_v2 | Rolling exceptions, jobs |
| W48 | perf_suite | Perf runs, budgets |
| W49 | release_bundle_v2 | Proof index, lineage |
| W50 | judge_demo_v2 | 4-min demo runner |
| W51 | budgeting | Budget versions, approval |
| W52 | forecasting | Forecast models, drift |
| W53 | driver_planning | Driver-based planning |
| W54 | scenario_engine | Monte Carlo, scenarios |
| W55 | treasury | Debt schedules, liquidity |
| W56 | covenants | Covenant rules, breach alerts |
| W57 | cost_allocation | Cost centers, allocations |
| W58 | kpi_framework | KPI definitions, formulas |
| W59 | board_pack | Board pack generator |
| W60 | ops_bundle | Ops evidence export |

---

## 4. NOT IMPLEMENTED — Agent & AI (W161–W200)

| Wave | Slug | Missing Frontend |
|------|------|------------------|
| W164 | agent_runtime | Agent session, run, stop |
| W165 | session_sim | Session simulator |
| **W166** | **agent_console** | **Agent Console UI — CRITICAL for hackathons** |
| W167 | close_orchestrator | Orchestrator workflow |
| W177 | gemini_adapter | Gemini integration status |
| W178 | airia_adapter | Airia adapter status |
| W179 | gradient_adapter | Gradient AI status |
| **W181** | **gemini_live_provider** | **Gemini Live — CRITICAL for Gemini hackathon** |
| W186 | gradient_inference | Gradient inference |
| W191 | explanation_graph | Explanation visualization |
| W192 | policy_engine | Policy rules UI |
| W193 | claim_enforcement | Claim enforcement |
| agent_ask | /api/agent/ask | Natural language ask — NO UI |
| agent_loop | /api/agent/cycle | Agent cycle — NO UI |

---

## 5. NOT IMPLEMENTED — CFO & Cockpit

| API | Missing Frontend |
|-----|------------------|
| /api/cfo/cockpit | CFO metrics dashboard |
| /api/cfo/scenario | CFO scenario pack |
| /api/cfo/story-mode | CFO story mode |
| /api/cfo-cockpit | Nuclear CFO cockpit |
| /api/productivity-roi | Productivity ROI |
| /api/one-cockpit | Unified cockpit |
| /api/readiness-dashboard | Readiness dashboard |

---

## 6. NOT IMPLEMENTED — Bloomberg/TradingView Style

| Feature | Status |
|---------|--------|
| Multi-panel terminal layout | NOT IMPLEMENTED |
| Real-time ticker/streaming | NOT IMPLEMENTED |
| Candlestick/OHLC charts | NOT IMPLEMENTED |
| Heatmaps | NOT IMPLEMENTED |
| Watchlists | NOT IMPLEMENTED |
| Keyboard shortcuts | NOT IMPLEMENTED |
| Dark theme terminal | NOT IMPLEMENTED |
| Multi-monitor layout | NOT IMPLEMENTED |

---

## 7. NOT IMPLEMENTED — Compliance & Security (W101–W130)

| Wave | Slug | Missing Frontend |
|------|------|------------------|
| W101 | soc2_evidence | SOC2 evidence automation |
| W102 | iso_mapping | ISO mapping |
| W103 | ediscovery | eDiscovery workflows |
| W104 | gdpr_redaction | GDPR redaction |
| W105 | key_management | Key management |
| W106 | compliance_signing | Compliance signing |
| W121 | abac_engine | ABAC policy engine |
| W122 | sso_scim | SSO/SCIM |
| W123 | admin_console | Policy admin |
| W328 | security_scoreboard | Security scoreboard |
| W332 | security_gov_proof | Security governance |

---

## 8. NOT IMPLEMENTED — Marketplace & Workflow (W91–W100)

| Wave | Slug | Missing Frontend |
|------|------|------------------|
| W91 | workflow_plugin | Workflow plugins |
| W92 | workflow_marketplace | Workflow marketplace |
| W93 | report_marketplace | Report marketplace |
| W94 | mapping_marketplace | Mapping marketplace |
| W95 | template_governance | Template governance |
| W100 | demo_marketplace | Demo marketplace |

---

## 9. NOT IMPLEMENTED — Blueprint Builder & Atlassian (W301–W320)

| Wave | Slug | Missing Frontend |
|------|------|------------------|
| W301 | blueprint_builder_v1 | Blueprint builder |
| W302 | blueprint_graph | Blueprint graph |
| W303 | blueprint_versioning | Versioning |
| W304 | generate_from_intent | Intent → blueprint |
| W305 | blueprint_to_template | Compile to template |
| W306 | template_validator | Template validation |
| W309 | jira_adapter | Jira integration |
| W310 | jira_cards_rc | Jira cards in RC |
| W311 | confluence_adapter | Confluence |
| W312 | confluence_templates | Confluence templates |

---

## 10. IMPLEMENTATION PRIORITY (Hackathon-Aligned)

### Tier 1 — Hackathon Differentiators
1. **Agent Console** (W166) — Airia, Gemini, DigitalOcean
2. **Gemini Live Provider** (W181) — Gemini Live Agent Challenge
3. **CFO Cockpit** — All hackathons
4. **Bloomberg-style Terminal** — Visual impact
5. **TradingView-style Charts** — Data visualization

### Tier 2 — Core Value
6. Close Calendar (W31, W221)
7. OCR Pipeline (W04)
8. Agent Ask/Cycle UI
9. Connector Framework (W41)
10. Evidence Binder (W40)

### Tier 3 — Completeness
11–50. Remaining wave UIs per phase

---

## 11. ROUTE COUNT SUMMARY

| Category | API Routes | Frontend Coverage |
|----------|------------|-------------------|
| Core (W01–W30) | ~150 | ~15% |
| Real Close (W31–W60) | ~300 | 0% |
| E2E/Instrumentation (W61–W70) | ~100 | 0% |
| Exception/Close (W71–W90) | ~200 | 0% |
| Marketplace (W91–W100) | ~100 | 0% |
| Compliance (W101–W120) | ~200 | 0% |
| Identity (W121–W140) | ~200 | 0% |
| Perf/Scale (W141–W160) | ~200 | 0% |
| Agent (W161–W200) | ~400 | 0% |
| RC/Proof (W221–W280) | ~600 | ~5% (Race Control) |
| Builder/Atlassian (W301–W340) | ~400 | 0% |
| **Total** | **~2040+** | **~5%** |
