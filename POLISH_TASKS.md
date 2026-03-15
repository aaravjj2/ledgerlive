# LedgerLive — Polish, Features & Quality Tasks
> Generated: March 15, 2026
> Status: Post dark-mode shell rebuild. 108 pages still have light-mode classes.
> Focus: UI polish, feature depth, test quality, video/artifact quality

---

## PRIORITY TIERS

| Tier | Description | Pages |
|------|-------------|-------|
| P0 — CRITICAL | Judges will definitely click these | CFOCockpit, EvidenceBinder, MultiAgent, RaceControl, CloseCalendar, Bloomberg, Connectors, AuditLog, BoardPack, GradientAI |
| P1 — HIGH | Core workflow pages | BankRecon, Reconciliation, Documents, Exceptions, ReviewQueue, TrialBalance, FinancialStatements, JournalEntries, Consolidation |
| P2 — MEDIUM | Feature pages that show depth | ScenarioEngine, Forecasting, Budgeting, Compliance, Controls, Soc2, EvidenceSearch, TraceExplorer, AgentConsole |
| P3 — SWEEP | All remaining 108 light-mode pages | Bulk automated sweep |

---

## SECTION 1 — BULK LIGHT-MODE SWEEP (108 pages)

### SWEEP-001: Automated class replacement
Replace all instances of these classes across all 108 affected pages:
- `bg-white` → `bg-[#111118]`
- `bg-gray-50` → `bg-[#1A1A24]`  
- `bg-gray-100` → `bg-[#1A1A24]`
- `text-gray-800` → `text-gray-200`
- `text-gray-700` → `text-gray-300`
- `border-gray-200` → `border-[#2A2A3A]`
- `bg-green-100 text-green-700` → `bg-green-900/40 text-green-400`
- `bg-red-100 text-red-700` → `bg-red-900/40 text-red-400`
- `bg-yellow-100 text-yellow-700` → `bg-yellow-900/40 text-yellow-400`
- `bg-blue-100 text-blue-700` → `bg-blue-900/40 text-blue-400`
- `bg-amber-100 text-amber-700` → `bg-amber-900/40 text-amber-400`
- `bg-indigo-100 text-indigo-700` → `bg-blue-900/40 text-blue-400`
- `bg-purple-100 text-purple-700` → `bg-purple-900/40 text-purple-400`
- `bg-indigo-600 text-white hover:bg-indigo-700` → `bg-red-600 text-white hover:bg-red-700`
- `bg-emerald-50 border-emerald-200` → `bg-green-900/20 border-green-500/30`
- `text-emerald-700` → `text-green-400`
- `text-emerald-800` → `text-green-300`
- `shadow-sm` → remove (not needed on dark surfaces)
- `hover:bg-gray-50` → `hover:bg-[#1A1A24]`
- `hover:bg-gray-100` → `hover:bg-[#1A1A24]`

### SWEEP-002: DataTable component dark mode
`apps/web/src/components/DataTable.tsx` — apply dark table styles globally so all pages using DataTable get dark mode automatically

### SWEEP-003: StatusBadge component dark mode  
`apps/web/src/components/StatusBadge.tsx` — replace all light badge variants with dark equivalents

### SWEEP-004: ChartCard component dark mode
`apps/web/src/components/ChartCard.tsx` — dark surface, dark chart backgrounds

### SWEEP-005: EmptyState component consistency
`apps/web/src/components/EmptyState.tsx` — ensure dark background, correct text colors

---

## SECTION 2 — P0 TIER: HIGH-VALUE PAGE REBUILDS

### P0-001: CFOCockpit.tsx — Executive command center
**Current state:** Basic metric tiles with light backgrounds, basic scenario list
**Target:** World-class CFO dashboard with:
- Full-width hero row: 6 KPI cards with sparklines (revenue, EBITDA, cash, AR aging, close health, variance)
- Each metric card: trend arrow, vs-budget delta, vs-prior-period delta
- Scenario pack comparison: side-by-side 3-column cards with delta highlighting (red/green)
- Story Mode output: styled narrative box with amber accent, bullet highlights as chips
- healthColor function → dark variants (green-900/40, yellow-900/40, red-900/40)
- Add a "CFO Sign-Off" button that posts to /api/cfo/sign-off
- Add period selector: Q1 2026 / Q2 2026 / Full Year toggle
- Mobile: collapses to 2-col KPI grid

### P0-002: EvidenceBinder.tsx — Audit-grade evidence display  
**Current state:** Generic DataTable with no visual identity
**Target:** Looks like a legal evidence management system:
- Header: sealed binder with SHA-256 hash displayed prominently
- Each evidence item: file type icon, tamper-evident hash (truncated + copy button), seal status badge
- "Generate Binder" button → POST /api/ops/export/court-pack → shows loading then hash
- Integrity score meter: X/10 items sealed, progress bar
- Download button that triggers the court pack export
- Timeline view showing when each item was sealed
- Dark: near-black background, monospace font for hashes, green "SEALED" badges

### P0-003: MultiAgentOrchestrator.tsx — Live agent flow visualization
**Current state:** Simple list of agent nodes and run table
**Target:** Visual agent graph with flow animation:
- Left panel: 5 agent nodes stacked vertically with connecting arrows between them
  - Each node: colored icon, name, system, live status dot (pulsing if active)
  - Arrows between nodes: animated dashes when workflow is running
- Right panel: recent workflow runs with expandable details
- Top: "Run Full Close Cycle" button → POST /api/ops/golden-scenario-run
- HITL gate visual: when hitl_pending=true, node shows orange "⏸ AWAITING HUMAN" badge
- Systems touched badges: show logos/icons for Documents, Reconciliations, Exceptions, Approvals
- Live run counter: "3 agents active" badge in header

### P0-004: CloseCalendar.tsx — Visual calendar grid
**Current state:** Plain table of tasks
**Target:** Actual calendar-style layout:
- Top: month/week toggle, current month header "March 2026"
- Calendar grid: 7-column week view with dates
- Tasks appear as colored pills on their due dates
- Status color coding: completed=green, in_progress=blue, blocked=red, pending=gray
- Dependency arrows between connected tasks (simplified, with "→ depends on X" text)
- SLA timer: tasks due within 24h show a countdown
- Click a task → expand detail panel on the right
- Add "Add Task" button
- Mobile: collapses to list view

### P0-005: AuditLog.tsx — Timeline evidence view
**Current state:** Generic light table
**Target:** Security audit timeline:
- Vertical timeline with colored dots (severity-based)
- Each entry: timestamp (monospace), actor, action description, affected entity
- SHA-256 hash displayed for each entry (truncated, with copy button)
- Filter bar: by severity, by actor, by date range
- "Export Audit Pack" button → POST /api/ops/export/court-pack
- Green "VERIFIED" badge when golden binder hash matches
- Auto-refresh every 30s with subtle "Updated X seconds ago" indicator

### P0-006: BoardPack.tsx — PDF-preview style board pack
**Current state:** Unknown (needs to be rebuilt)
**Target:** Simulates a real board pack PDF:
- Cover page style header: company name, period, date prepared, CFO signature line
- Sections listed as "pages": Executive Summary, P&L, Balance Sheet, Cash Flow, KPIs, Close Status
- Each section: expandable accordion with dark-themed data
- "Generate Board Pack" button → calls /api/board-pack/generate
- Download button for PDF export
- "Last generated" timestamp

### P0-007: GradientAIDashboard.tsx — OCR demo showpiece
**Current state:** Unknown
**Target:** Live OCR demonstration page:
- Upload zone: drag-and-drop PDF/image with dashed border
- After upload: show extracted fields in a structured panel
  - Vendor name, invoice number, date, line items, total, tax
- Confidence scores as progress bars (94.2% = near-full green bar)
- Raw extracted text in a monospace panel
- Side-by-side: original document preview | extracted data
- Provider badge: "Powered by DigitalOcean Gradient AI"
- Fallback indicator: "Using local OCR fallback" if Gradient AI not configured

### P0-008: Connectors.tsx — Integration marketplace
**Current state:** Unknown
**Target:** Visual connector cards grid:
- 3-column grid of integration cards
- Each card: logo placeholder, name, description, status (Connected/Available/Coming Soon)
- Cards for: QuickBooks, Xero, Plaid, Slack, Google Drive, SharePoint, Salesforce, NetSuite, SAP
- "Connect" button on available cards (doesn't need to work, just render)
- Connected cards: green "✓ Connected" badge, "Last synced: X minutes ago"
- Search/filter bar at top
- Category tabs: Accounting | Banking | CRM | Storage | Communication

### P0-009: Bloomberg Terminal fixes
**Current state:** Already mostly dark (bg-gray-900) but uses amber branding
**Target:** Keep the amber terminal aesthetic (it's intentional for Bloomberg), but fix:
- bg-gray-900 → bg-[#0A0A0F] (deeper black)
- bg-gray-800 → bg-[#111118]
- bg-gray-700 → bg-[#1A1A24]  
- border-gray-700 → border-[#2A2A3A]
- Add a live clock in the header that ticks every second
- Add keyboard shortcut: type ticker symbols directly
- Add a news feed panel below the charts (mock financial headlines)

### P0-010: HackathonShowcase.tsx — Competition landing page
**Current state:** Unknown
**Target:** A stunning showcase page that judges may land on:
- Hero: "LedgerLive — AI Finance Close Agent" with animated ticker
- 4 hackathon cards: Gemini ($80K), DigitalOcean ($20K), Airia ($7K), GitLab ($65K)
- Each card: prize amount, track, key tech used, live URL badge
- Feature highlights: Voice Agent, Multi-Agent, Gradient AI OCR, GitLab Compliance
- Architecture diagram embedded (the Mermaid from README rendered visually)
- Live stats from the API: X documents processed, X reconciliations, X tests passing
- "Open Live Demo" button

---

## SECTION 3 — P1 TIER: CORE WORKFLOW PAGES

### P1-001: BankRecon.tsx — Bank reconciliation detail view
- Two-column layout: bank statement transactions | GL entries
- Match lines visually connecting matched pairs
- Unmatched items highlighted in red
- Match rate progress bar at top
- "Auto-match" button

### P1-002: TrialBalance.tsx — Accounting trial balance
- Debit/credit columns with proper accounting formatting
- Totals row with verification (debits = credits indicator)
- Account code hierarchy (indent sub-accounts)
- Export to CSV button

### P1-003: FinancialStatements.tsx — P&L, Balance Sheet, Cash Flow
- Tab switcher: P&L | Balance Sheet | Cash Flow
- Period comparison: Current | Prior Period | Budget
- Variance column with color coding
- Numbers formatted as accounting (negatives in parentheses)

### P1-004: JournalEntries.tsx — Journal entry ledger
- Debit/credit display
- Entry status (posted/draft/reversed)
- Click to expand full JE detail
- Post button for draft entries

### P1-005: Consolidation.tsx — Multi-entity consolidation
- Entity tree on left
- Elimination entries panel
- FX adjustment summary
- Consolidated total column

### P1-006: AuditPortal.tsx — External auditor view
- Read-only styled differently from internal views
- "Auditor Mode" banner at top
- Evidence request list
- Download selected evidence button

### P1-007: Controls.tsx — SOX controls matrix
- Control ID, description, frequency, owner, last tested, result
- Risk rating column
- Test result: Effective / Deficient / N/T
- Deficient controls highlighted in red

### P1-008: Approvals.tsx — Approval workflow
- Cards with approve/reject (same dark style as ReviewQueue)
- Approval chain visualization: level 1 → level 2 → level 3
- Time in queue indicator

### P1-009: Invoices.tsx / Payments.tsx / Vendors.tsx / Expenses.tsx
- All: dark table treatment
- Invoices: aging buckets (Current, 30, 60, 90+ days)
- Payments: cleared/outstanding badges
- Vendors: spend by vendor bar chart
- Expenses: category breakdown

---

## SECTION 4 — P2 TIER: FEATURE DEPTH PAGES

### P2-001: ScenarioEngine.tsx
- Three scenario columns: Base | Upside | Downside
- Delta highlighting between scenarios
- Assumption inputs that recalculate metrics

### P2-002: Forecasting.tsx
- Line chart: actuals vs forecast vs budget
- Rolling 12-month view
- Confidence interval bands

### P2-003: Budgeting.tsx
- Budget vs actual table with variance %
- Drill-down by department/cost center
- Lock period button

### P2-004: Compliance.tsx
- Compliance checklist with checkboxes
- Regulatory framework selector: SOX | IFRS | GAAP | GDPR
- Evidence attachment slots

### P2-005: TraceExplorer.tsx
- Waterfall trace view (like Jaeger/Zipkin)
- Each tool call: name, duration bar, status
- Expandable payload viewer

### P2-006: AgentConsole.tsx
- Terminal-style output for agent runs
- Green text on near-black (Matrix aesthetic)
- Timestamps, log levels, tool calls

### P2-007: SecurityScoreboard.tsx
- Security score gauge (0-100)
- Vulnerability list with severity
- Last scan timestamp

### P2-008: ReadinessDashboard.tsx
- Close readiness checklist (all items must be green to proceed)
- Blocking items in red with "Fix Now" buttons
- Overall readiness percentage

### P2-009: LapTimeTelemetry.tsx
- F1-style lap delta chart
- Each close task as a "sector time"
- Personal best vs current performance

### P2-010: PitStopOptimizer.tsx
- Optimization recommendations list
- Time savings estimate per recommendation
- "Apply" button per recommendation

---

## SECTION 5 — COMPONENT UPGRADES

### COMP-001: Nav.tsx sidebar — add icons
Replace emoji section headers with proper inline SVG icons for each section.
Use simple geometric shapes if lucide-react not available.

### COMP-002: LoadingSkeleton.tsx — page-specific variants
Add variants: `table`, `cards`, `timeline`, `chart` 
Usage: `<LoadingSkeleton variant="table" rows={5} />`

### COMP-003: DataTable.tsx — full dark mode + features
- Sortable columns (click header to sort)
- Column resizing
- Row selection checkboxes
- Bulk action bar appears when rows selected
- Pagination controls

### COMP-004: SearchBar.tsx — global search
- Search across all pages (not just current)
- Results dropdown with page type icons
- Keyboard navigation (↑↓ to navigate, Enter to go)
- Recent searches

### COMP-005: Toast.tsx — notification system
- 4 variants: success (green), error (red), warning (yellow), info (blue)
- Auto-dismiss after 4 seconds
- Progress bar showing time remaining
- Stack up to 3 toasts

### COMP-006: TickerBar.tsx — live metrics strip
Used in Bloomberg and CFO Cockpit.
- Scrolling horizontal ticker of KPIs
- Alternating colors for readability
- Pause on hover

### COMP-007: Sparkline.tsx — mini trend charts
Used in KPI cards on Dashboard and CFO Cockpit.
- 7-point line chart
- No axes, just the trend line
- Color matches the KPI (green if up, red if down)

### COMP-008: HITLGate.tsx — human approval gate
Used in ReviewQueue and MultiAgent.
- Full-screen overlay option
- Shows: what needs approval, why, risk level
- Large approve/reject buttons
- Countdown timer (SLA)

---

## SECTION 6 — TEST QUALITY

### TEST-001: Expand E2E test coverage to 150+ tests
Current: 4,269 passing (unit/integration). Add E2E scenarios:
- Full close cycle happy path (seed → reconcile → exception → approve → audit)
- Voice API text mode all 5 question types
- Race Control golden scenario → verify all sections populate
- Evidence binder generation → verify SHA hash present
- CFO sign-off flow
- Board pack generation

### TEST-002: Visual regression tests
Use Playwright screenshot comparison:
- Take baseline screenshots of all 10 P0 pages
- Save as `tests/visual/baselines/`
- Future runs compare against baselines
- Threshold: 0.1% pixel difference allowed

### TEST-003: API contract tests
For every endpoint used by the frontend, verify:
- Returns 200 with correct content-type
- Response has `items` array OR `total` field (not both empty)
- No 500 errors on seed data
- Auth headers not required (for demo mode)

### TEST-004: Accessibility tests
Using axe-core in Playwright:
- Each P0 page: 0 critical a11y violations
- Color contrast: all text meets WCAG AA (4.5:1 ratio)
- All buttons have accessible labels
- All images have alt text

### TEST-005: Mobile responsive tests
Playwright viewport: 375x812 (iPhone 14)
- Sidebar collapses to hamburger
- All tables reflow or scroll horizontally
- Voice button is tappable (min 44px)
- No horizontal overflow on any page

### TEST-006: Performance tests
Using Playwright with Chrome DevTools:
- Dashboard LCP (Largest Contentful Paint) < 2.5s
- No layout shift after data loads (CLS < 0.1)
- All lazy-loaded pages load < 1s after initial bundle

---

## SECTION 7 — VIDEO & ARTIFACT QUALITY

### VID-001: Master demo video (5 minutes)
Script outline:
- 0:00-0:20 Hook: "Finance teams waste 40+ hours per close. LedgerLive closes your books like an F1 pit crew."
- 0:20-0:50 Dashboard: Show live KPIs, agent status badge, close cycle progress
- 0:50-1:30 Race Control: Run golden scenario, show lanes populating, incidents appearing
- 1:30-2:10 Voice Agent: Speak "What exceptions need my review?" — LedgerBot responds
- 2:10-2:45 Exception → Review → Approve → Audit trail (full HITL flow in 35 seconds)
- 2:45-3:15 Evidence Binder: Show SHA-256 sealed artifacts, court pack export
- 3:15-3:45 CFO Cockpit: Metrics, story mode narrative
- 3:45-4:20 Multi-Agent: Show 4 agents orchestrating, HITL gate
- 4:20-4:40 Architecture: API docs, Mermaid diagram
- 4:40-5:00 Close: repo link, live URL, prize tracks

### VID-002: Per-hackathon cut videos
- Gemini (4 min): Focus on voice agent, Gemini Live API, Cloud Run proof
- DigitalOcean (3 min): Focus on Gradient AI OCR, App Platform, Spaces storage
- Airia (4 min): Focus on multi-agent flow, community bundle, HITL
- GitLab (3 min): Focus on compliance agent, MR comment, audit artifact, Anthropic integration

### VID-003: Screenshot audit — replace all old screenshots
Current screenshots in artifacts/demo/ are from before the dark mode rebuild.
Retake all 10 core page screenshots with the new dark UI.
Add 5 additional: mobile view, voice agent active state, race control seeded, exceptions with filter bar, evidence binder sealed.

### VID-004: Architecture diagram — production quality
Current: Mermaid in README (text-only renders)
Target: A proper visual PNG diagram with:
- Dark background matching the app
- Color-coded service boxes (frontend=blue, backend=green, AI=purple, infra=gray)
- Arrows with labels
- All 4 hackathon integrations shown
- Save to docs/architecture/ledgerlive-architecture.png

### VID-005: GIF for README
Record a 15-second GIF showing:
- Dashboard loading with live data
- Sidebar navigation
- Race Control with lanes
Upload as assets/demo.gif, reference in README

---

## SECTION 8 — DEVPOST SUBMISSION QUALITY

### SUB-001: Gemini submission description
500 words covering: voice agent, Gemini Live API integration, WebSocket architecture,
Cloud Run deployment proof, finance use case, target users (CFOs, controllers)

### SUB-002: DigitalOcean submission description
400 words covering: Gradient AI OCR, DigitalOcean Spaces, App Platform deployment,
"Best AI Agent Persona" angle (LedgerBot), "Best Program for the People" angle

### SUB-003: Airia submission description
400 words covering: 4-agent architecture, community bundle URL, HITL gates,
Active Agents track, enterprise impact quantification

### SUB-004: GitLab submission description
600 words covering: compliance checker agent, Duo Agent Platform, Anthropic bonus,
Google Cloud bonus, CI/CD pipeline, audit artifact generation

---

## SECTION 9 — REAL INTEGRATIONS (MOCK DATA QUALITY)

### INT-001: QuickBooks mock data
Create tools/mocks/quickbooks_data.json with realistic:
- 50 GL transactions (debits, credits, account codes)
- 20 vendor records
- 10 open invoices
- Chart of accounts (GAAP standard)

### INT-002: Bank statement mock data
Create tools/mocks/bank_statement_march2026.json:
- 30 bank transactions with descriptions, amounts, dates
- 5 of them intentionally unmatched to GL (for exception demo)

### INT-003: Demo seed richness
Enhance POST /api/demo/seed to create:
- 10 documents (not just 5)
- 3 reconciliation runs with realistic match rates (94%, 87%, 99%)
- 5 exceptions (2 CRITICAL, 1 HIGH, 2 MEDIUM — all with realistic descriptions)
- Full audit trail (20+ events with timestamps spread across the day)
- CFO metrics snapshot

### INT-004: Slack notification simulation
When an exception is approved via ReviewQueue, show a "Notification sent to Slack" toast.
Backend: log the notification to audit trail as "SLACK_NOTIFICATION_SENT"

---

## SECTION 10 — REMAINING PAGES (FULL LIST)

The following pages need at minimum the dark-mode sweep (Section 1) applied.
Pages marked [REBUILD] also need meaningful content, not just color changes.

**AI/Agent pages:**
- [ ] AgentConsole.tsx [REBUILD — terminal aesthetic]
- [ ] AgentRuntime.tsx
- [ ] AiriaAdapter.tsx
- [ ] AiriaEverywhereHub.tsx [REBUILD — hub with 4 integration cards]
- [ ] AiriaReadiness.tsx
- [ ] AutoFix.tsx
- [ ] BlueprintBuilder.tsx [REBUILD — visual workflow builder]
- [ ] ExceptionClassifier.tsx
- [ ] GeminiAdapter.tsx
- [ ] GradientAdapter.tsx
- [ ] MlBaseline.tsx
- [ ] MlDataset.tsx
- [ ] MlInference.tsx
- [ ] MultimodalStoryteller.tsx
- [ ] ReadinessDashboard.tsx [REBUILD]
- [ ] ReplayEngine.tsx
- [ ] ToolRegistry.tsx
- [ ] TraceExplorer.tsx [REBUILD — waterfall trace]
- [ ] UINavigator.tsx

**Finance core pages:**
- [ ] Abac.tsx
- [ ] AccrualSuggest.tsx
- [ ] Accruals.tsx [REBUILD]
- [ ] Approvals.tsx [REBUILD]
- [ ] BankRecon.tsx [REBUILD — two-column matching view]
- [ ] Budgeting.tsx [REBUILD]
- [ ] CashApplication.tsx
- [ ] CashflowConsol.tsx
- [ ] ChartOfAccounts.tsx
- [ ] CloseMgmt.tsx
- [ ] ClosePeriod.tsx
- [ ] CloseScorecard.tsx [REBUILD — scorecard with grades]
- [ ] Compliance.tsx [REBUILD]
- [ ] Consolidation.tsx [REBUILD]
- [ ] Controls.tsx [REBUILD]
- [ ] CostAllocation.tsx
- [ ] Covenants.tsx
- [ ] Depreciation.tsx
- [ ] DriverPlanning.tsx
- [ ] Entities.tsx
- [ ] Expenses.tsx
- [ ] FinancialStatements.tsx [REBUILD]
- [ ] FixedAssets.tsx
- [ ] Flux.tsx
- [ ] Forecasting.tsx [REBUILD]
- [ ] Fx.tsx
- [ ] Intercompany.tsx
- [ ] IntercompanyV2.tsx
- [ ] Invoices.tsx
- [ ] JePosting.tsx
- [ ] JeSuggest.tsx
- [ ] JournalEntries.tsx [REBUILD]
- [ ] Kpi.tsx [REBUILD — KPI dashboard]
- [ ] LapTimeTelemetry.tsx [REBUILD — F1 telemetry]
- [ ] Leases.tsx
- [ ] Lineage.tsx [REBUILD — data lineage graph]
- [ ] MappingStudio.tsx
- [ ] Payments.tsx
- [ ] PitStopOptimizer.tsx [REBUILD]
- [ ] Plaid.tsx
- [ ] ProductivityRoi.tsx
- [ ] Qbo.tsx [REBUILD — QuickBooks integration status]
- [ ] QueryLanguage.tsx [REBUILD — SQL-style query UI]
- [ ] ReconExplain.tsx
- [ ] Reports.tsx
- [ ] Revenue.tsx
- [ ] Roles.tsx
- [ ] ScenarioEngine.tsx [REBUILD]
- [ ] SecurityScoreboard.tsx [REBUILD]
- [ ] Settings.tsx
- [ ] Soc2.tsx [REBUILD — SOC 2 compliance matrix]
- [ ] Tax.tsx
- [ ] ThreeWayMatch.tsx [REBUILD]
- [ ] TriageQueue.tsx
- [ ] TrialBalance.tsx [REBUILD]
- [ ] Users.tsx
- [ ] Vendors.tsx
- [ ] WorkflowMarketplace.tsx [REBUILD — marketplace grid]
- [ ] WorkflowPlugin.tsx
- [ ] Xero.tsx

**Data/Admin pages:**
- [ ] AdminConsole.tsx [REBUILD — system admin panel]
- [ ] ConnectorMocks.tsx
- [ ] DataExport.tsx
- [ ] DataImport.tsx
- [ ] DataLake.tsx
- [ ] DataQuality.tsx
- [ ] EvidenceSearch.tsx [REBUILD — search with filters]
- [ ] Gdpr.tsx
- [ ] KeyManagement.tsx
- [ ] Notifications.tsx
- [ ] OneCockpit.tsx
- [ ] ReportMarketplace.tsx [REBUILD — report template marketplace]

---

## TASK SUMMARY

| Section | Tasks | Est. Impact |
|---------|-------|-------------|
| Bulk sweep (108 pages) | 5 | 🟡 Medium — removes white flashes |
| P0 rebuilds (10 pages) | 10 | 🔴 Critical — judge impressions |
| P1 core workflow (9 pages) | 9 | 🟠 High — product completeness |
| P2 feature depth (10 pages) | 10 | 🟡 Medium — depth signal |
| Component upgrades (8) | 8 | 🟠 High — reused everywhere |
| Test quality (6 areas) | 6 | 🟠 High — hackathon credibility |
| Video & artifacts (5) | 5 | 🔴 Critical — submission quality |
| Devpost descriptions (4) | 4 | 🔴 Critical — judging |
| Real integrations (4) | 4 | 🟡 Medium — demo richness |
| Remaining page rebuilds (40+) | 40 | 🟢 Low-Medium per page |
| **TOTAL** | **101** | |

---
*LedgerLive Polish Tasks — March 15, 2026*
