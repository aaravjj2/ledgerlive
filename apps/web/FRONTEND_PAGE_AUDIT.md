# Frontend Page Audit

Generated: 2026-03-18 14:59:07 UTC

Status heuristics: WORKING, STATIC_CONTENT, STUB, STUB-WITH-CONTENT.
This table was generated from source inspection (routes + API call signatures), before applying the latest fix patch set.

## Targeted Fixes Applied
- AgentConsole.tsx: switched ask call to /api/voice/ask and added structured Airia response renderer + phase animation.
- Dashboard.tsx: KPI row now derives exception metrics from /api/exceptions and agent cycle count from /api/agent/cycles.
- Settings.tsx: added Airia status badge and updated URLs to Railway/Vercel.
- Exceptions.tsx: added AUTO-RESOLVE / ESCALATE classification badges.
- TraceExplorer.tsx, Forecasting.tsx, Budgeting.tsx: replaced random demo data with deterministic static datasets.

## Full Page Audit Table

 |  PAGE | ROUTED | DATA_CALLS | OLD_GEMINI_WS | STATUS_HEURISTIC
 |  Abac.tsx | NO | /api/abac | NO | STATIC_CONTENT
 |  AccrualSuggest.tsx | NO | /api/accrual-suggest | NO | STATIC_CONTENT
 |  Accruals.tsx | NO | /api/accruals | NO | STATIC_CONTENT
 |  AdminConsole.tsx | NO | /api/admin | NO | STATIC_CONTENT
 |  AgentConsole.tsx | YES | /api/agent/ask,/api/agent/cycle,/api/agent/cycles,/api/agent/perceive | NO | STUB
 |  AgentRuntime.tsx | NO | /api/agent-runtime | NO | STATIC_CONTENT
 |  AiriaAdapter.tsx | NO | /api/airia-adapter | NO | STATIC_CONTENT
 |  AiriaEverywhereHub.tsx | YES | none | NO | STATIC_CONTENT
 |  AiriaReadiness.tsx | YES | /api/airia/compat_report,/api/airia/generate-bundle,/api/airia/status,/api/airia/validate-bundle,/api/airia/verify-bundle,/api/mcp/call,/api/mcp/config,/api/mcp/tools,/api/ops/export/telemetry-pack,/api/ops/golden-scenario-run | NO | WORKING
 |  Approvals.tsx | NO | /api/approvals | NO | STATIC_CONTENT
 |  AuditLog.tsx | YES | /api/audit,/api/audit/export | NO | WORKING
 |  AuditPortal.tsx | NO | /api/audit-portal | NO | STATIC_CONTENT
 |  AutoFix.tsx | NO | /api/auto-fix | NO | STATIC_CONTENT
 |  BankRecon.tsx | NO | /api/reconciliations | NO | STATIC_CONTENT
 |  BloombergTerminal.tsx | YES | /api/documents,/api/exceptions,/api/reconciliations | POSSIBLE | STUB-WITH-CONTENT
 |  BlueprintBuilder.tsx | NO | /api/blueprint-builder | NO | STATIC_CONTENT
 |  BoardPack.tsx | NO | /api/board-pack | NO | STUB
 |  Budgeting.tsx | NO | /api/budgeting | NO | STUB-WITH-CONTENT
 |  CFOCockpit.tsx | YES | /api/cfo/cockpit,/api/cfo/scenario,/api/cfo/signoff,/api/cfo/story-mode | NO | WORKING
 |  CashApplication.tsx | NO | /api/cash-application | NO | STATIC_CONTENT
 |  CashflowConsol.tsx | NO | /api/cashflow-consol | NO | STATIC_CONTENT
 |  ChartOfAccounts.tsx | NO | /api/coa | NO | STATIC_CONTENT
 |  CloseCalendar.tsx | YES | /api/close-calendar | NO | WORKING
 |  CloseMgmt.tsx | NO | /api/close | NO | STATIC_CONTENT
 |  ClosePeriod.tsx | NO | /api/close-periods | NO | STATIC_CONTENT
 |  CloseScorecard.tsx | YES | /api/close-scorecards | NO | STATIC_CONTENT
 |  Compliance.tsx | YES | /api/soc2-evidence | NO | STATIC_CONTENT
 |  ConnectorMocks.tsx | NO | /api/connector-mocks | NO | STATIC_CONTENT
 |  Connectors.tsx | YES | /api/connectors/plaid/status,/api/connectors/qbo/status,/api/connectors/xero/status | NO | STUB
 |  Consolidation.tsx | NO | /api/consolidation | NO | STATIC_CONTENT
 |  Controls.tsx | NO | /api/controls | NO | STATIC_CONTENT
 |  CostAllocation.tsx | NO | /api/cost-allocation | NO | STATIC_CONTENT
 |  Covenants.tsx | NO | /api/covenants | NO | STATIC_CONTENT
 |  Dashboard.tsx | YES | /api/agent/status,/api/audit,/api/documents,/api/exceptions,/api/reconciliations,/api/reviews | NO | WORKING
 |  DataExport.tsx | NO | /api/export | NO | STATIC_CONTENT
 |  DataImport.tsx | NO | /api/import | NO | STATIC_CONTENT
 |  DataLake.tsx | NO | /api/data-lake | NO | STATIC_CONTENT
 |  DataQuality.tsx | NO | /api/data-quality | NO | STATIC_CONTENT
 |  Depreciation.tsx | NO | /api/depreciation | NO | STATIC_CONTENT
 |  Documents.tsx | YES | /api/documents | NO | WORKING
 |  DriverPlanning.tsx | NO | /api/driver-planning | NO | STATIC_CONTENT
 |  Entities.tsx | NO | /api/entities | NO | STATIC_CONTENT
 |  EvidenceBinder.tsx | NO | /api/evidence-binder | NO | WORKING
 |  EvidenceSearch.tsx | NO | /api/evidence-search | NO | STATIC_CONTENT
 |  ExceptionClassifier.tsx | NO | /api/exception-classifier | NO | STATIC_CONTENT
 |  Exceptions.tsx | YES | /api/exceptions,/api/exceptions/ | NO | WORKING
 |  Expenses.tsx | NO | /api/expenses | NO | STATIC_CONTENT
 |  FinancialStatements.tsx | NO | /api/statements | NO | STATIC_CONTENT
 |  FixedAssets.tsx | NO | /api/fixed-assets | NO | STATIC_CONTENT
 |  Flux.tsx | NO | /api/flux | NO | STATIC_CONTENT
 |  Forecasting.tsx | NO | /api/forecasts | NO | STUB-WITH-CONTENT
 |  Fx.tsx | NO | /api/fx | NO | STATIC_CONTENT
 |  Gdpr.tsx | NO | /api/gdpr | NO | STATIC_CONTENT
 |  GeminiAdapter.tsx | NO | /api/gemini | POSSIBLE | STATIC_CONTENT
 |  GradientAIDashboard.tsx | YES | /api/gradient-inference,/api/gradient-training | NO | STATIC_CONTENT
 |  GradientAdapter.tsx | NO | /api/gradient | NO | STATIC_CONTENT
 |  HackathonShowcase.tsx | YES | /api/documents,/api/reconciliations | POSSIBLE | WORKING
 |  Intercompany.tsx | NO | /api/intercompany | NO | STATIC_CONTENT
 |  IntercompanyV2.tsx | NO | /api/intercompany-v2 | NO | STATIC_CONTENT
 |  Invoices.tsx | NO | /api/invoices | NO | STATIC_CONTENT
 |  JePosting.tsx | NO | /api/je-posting | NO | STATIC_CONTENT
 |  JeSuggest.tsx | NO | /api/je-suggest | NO | STATIC_CONTENT
 |  JournalEntries.tsx | NO | /api/journal-entries | NO | STATIC_CONTENT
 |  KeyManagement.tsx | NO | /api/key-management | NO | STATIC_CONTENT
 |  Kpi.tsx | NO | /api/kpis | NO | STUB
 |  LapTimeTelemetry.tsx | NO | /api/lap-time-telemetry | NO | STUB-WITH-CONTENT
 |  Leases.tsx | NO | /api/leases | NO | STATIC_CONTENT
 |  Lineage.tsx | NO | /api/lineage | NO | STATIC_CONTENT
 |  LiveVoiceAgent.tsx | YES | none | POSSIBLE | STUB
 |  MappingStudio.tsx | NO | /api/mapping | NO | STATIC_CONTENT
 |  MlBaseline.tsx | NO | /api/ml-baseline | NO | STATIC_CONTENT
 |  MlDataset.tsx | NO | /api/ml-dataset | NO | STATIC_CONTENT
 |  MlInference.tsx | NO | /api/ml-inference | NO | STATIC_CONTENT
 |  MultiAgentOrchestrator.tsx | YES | /api/close-orchestrator/agents,/api/close-orchestrator/runs,/api/ops/golden-scenario-run | NO | WORKING
 |  MultimodalStoryteller.tsx | YES | /api/ops/export/telemetry-pack | POSSIBLE | STATIC_CONTENT
 |  NotFound.tsx | YES | none | NO | STATIC_CONTENT
 |  Notifications.tsx | NO | /api/notifications | NO | STATIC_CONTENT
 |  OCRPipeline.tsx | YES | /api/ocr-jobs,/api/ocr-jobs/,/api/ocr-jobs/stats | NO | WORKING
 |  OneCockpit.tsx | NO | /api/one-cockpit | NO | STATIC_CONTENT
 |  Payments.tsx | NO | /api/payments | NO | STATIC_CONTENT
 |  PitStopOptimizer.tsx | NO | /api/pit-stop-optimizer | NO | STATIC_CONTENT
 |  Plaid.tsx | NO | /api/plaid | NO | STATIC_CONTENT
 |  ProductivityRoi.tsx | NO | /api/productivity-roi | NO | STATIC_CONTENT
 |  Qbo.tsx | NO | /api/qbo | NO | STATIC_CONTENT
 |  QueryLanguage.tsx | NO | /api/query | NO | STATIC_CONTENT
 |  RaceControl.tsx | YES | /api/close-checkpoint,/api/incident-log,/api/lane-status,/api/live-scoreboard,/api/ops/approval/,/api/ops/checkpoint/,/api/ops/export/court-pack,/api/ops/export/telemetry-pack,/api/ops/golden-scenario-run,/api/ops/incident/,/api/ops/rc-approval/,/api/ops/replay/regenerate-binder,/api/ops/security-event/,/api/ops/security-events,/api/race-weekend/stages,/api/rc-approval,/api/rc-state-machine | NO | WORKING
 |  ReadinessDashboard.tsx | NO | /api/readiness-dashboard | NO | STATIC_CONTENT
 |  ReconExplain.tsx | NO | /api/recon-explain | NO | STATIC_CONTENT
 |  Reconciliation.tsx | YES | /api/reconciliations,/api/reconciliations/ | NO | WORKING
 |  ReplayEngine.tsx | NO | /api/replay | NO | STATIC_CONTENT
 |  ReportMarketplace.tsx | NO | /api/report-marketplace | NO | STATIC_CONTENT
 |  Reports.tsx | NO | /api/reports | NO | STATIC_CONTENT
 |  Revenue.tsx | NO | /api/revenue | NO | STATIC_CONTENT
 |  ReviewQueue.tsx | YES | /api/reviews,/api/reviews/ | NO | WORKING
 |  Roles.tsx | NO | /api/roles | NO | STATIC_CONTENT
 |  ScenarioEngine.tsx | NO | /api/scenarios | NO | STUB
 |  SecurityScoreboard.tsx | NO | /api/security-scoreboard | NO | STATIC_CONTENT
 |  Settings.tsx | YES | none | NO | WORKING
 |  Soc2.tsx | NO | /api/soc2 | NO | STATIC_CONTENT
 |  Tax.tsx | NO | /api/tax | NO | STATIC_CONTENT
 |  ThreeWayMatch.tsx | NO | /api/three-way-match | NO | STATIC_CONTENT
 |  ToolRegistry.tsx | NO | /api/tool-registry | NO | STATIC_CONTENT
 |  TraceExplorer.tsx | NO | /api/trace | NO | STUB-WITH-CONTENT
 |  Treasury.tsx | YES | /api/treasury,/api/treasury/liquidity-ladder | NO | STATIC_CONTENT
 |  TriageQueue.tsx | NO | /api/triage | NO | STATIC_CONTENT
 |  TrialBalance.tsx | NO | /api/trial-balance | NO | STUB
 |  UINavigator.tsx | YES | /api/race-control | POSSIBLE | WORKING
 |  Users.tsx | NO | /api/users | NO | STATIC_CONTENT
 |  Vendors.tsx | NO | /api/vendors | NO | STATIC_CONTENT
 |  WorkflowMarketplace.tsx | NO | /api/workflow-marketplace | NO | STATIC_CONTENT
 |  WorkflowPlugin.tsx | NO | /api/workflow-plugin | NO | STATIC_CONTENT
 |  Xero.tsx | NO | /api/xero | NO | STATIC_CONTENT
