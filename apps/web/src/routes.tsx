/**
 * Central route configuration - lazy loads generated feature pages.
 * Add new routes here when new features are generated.
 */
import { lazy, Suspense } from 'react'
import { Routes, Route } from 'react-router-dom'
import Nav from './components/Nav'
import Dashboard from './pages/Dashboard'
import Documents from './pages/Documents'
import Reconciliation from './pages/Reconciliation'
import Exceptions from './pages/Exceptions'
import ReviewQueue from './pages/ReviewQueue'
import AuditLog from './pages/AuditLog'
import Settings from './pages/Settings'
import RaceControl from './pages/RaceControl'
import AiriaReadiness from './pages/AiriaReadiness'
import CFOCockpit from './pages/CFOCockpit'
import AgentConsole from './pages/AgentConsole'
import BloombergTerminal from './pages/BloombergTerminal'
import Connectors from './pages/Connectors'
import CloseCalendar from './pages/CloseCalendar'
import Treasury from './pages/Treasury'
import Compliance from './pages/Compliance'
import OCRPipeline from './pages/OCRPipeline'
import CloseScorecard from './pages/CloseScorecard'
import LiveVoiceAgent from './pages/LiveVoiceAgent'
import MultimodalStoryteller from './pages/MultimodalStoryteller'
import UINavigator from './pages/UINavigator'
import GradientAIDashboard from './pages/GradientAIDashboard'
import AiriaEverywhereHub from './pages/AiriaEverywhereHub'
import MultiAgentOrchestrator from './pages/MultiAgentOrchestrator'
import HackathonShowcase from './pages/HackathonShowcase'
import NotFound from './pages/NotFound'

const Loading = () => <div className="p-6 text-gray-500" data-testid="route-loading">Loading…</div>

const Lazy = (C: React.LazyExoticComponent<React.ComponentType<unknown>>) => (
  <Suspense fallback={<Loading />}><C /></Suspense>
)

const ClosePeriod = lazy(() => import('./pages/ClosePeriod').then(m => ({ default: m.default })))
const Entities = lazy(() => import('./pages/Entities').then(m => ({ default: m.default })))
const ChartOfAccounts = lazy(() => import('./pages/ChartOfAccounts').then(m => ({ default: m.default })))
const JournalEntries = lazy(() => import('./pages/JournalEntries').then(m => ({ default: m.default })))
const TrialBalance = lazy(() => import('./pages/TrialBalance').then(m => ({ default: m.default })))
const FinancialStatements = lazy(() => import('./pages/FinancialStatements').then(m => ({ default: m.default })))
const BankRecon = lazy(() => import('./pages/BankRecon').then(m => ({ default: m.default })))
const Vendors = lazy(() => import('./pages/Vendors').then(m => ({ default: m.default })))
const Invoices = lazy(() => import('./pages/Invoices').then(m => ({ default: m.default })))
const Payments = lazy(() => import('./pages/Payments').then(m => ({ default: m.default })))
const Expenses = lazy(() => import('./pages/Expenses').then(m => ({ default: m.default })))
const FixedAssets = lazy(() => import('./pages/FixedAssets').then(m => ({ default: m.default })))
const Depreciation = lazy(() => import('./pages/Depreciation').then(m => ({ default: m.default })))
const Intercompany = lazy(() => import('./pages/Intercompany').then(m => ({ default: m.default })))
const Tax = lazy(() => import('./pages/Tax').then(m => ({ default: m.default })))
const Revenue = lazy(() => import('./pages/Revenue').then(m => ({ default: m.default })))
const Leases = lazy(() => import('./pages/Leases').then(m => ({ default: m.default })))
const CloseMgmt = lazy(() => import('./pages/CloseMgmt').then(m => ({ default: m.default })))
const Flux = lazy(() => import('./pages/Flux').then(m => ({ default: m.default })))
const Approvals = lazy(() => import('./pages/Approvals').then(m => ({ default: m.default })))
const Users = lazy(() => import('./pages/Users').then(m => ({ default: m.default })))
const Roles = lazy(() => import('./pages/Roles').then(m => ({ default: m.default })))
const Notifications = lazy(() => import('./pages/Notifications').then(m => ({ default: m.default })))
const Reports = lazy(() => import('./pages/Reports').then(m => ({ default: m.default })))
const DataImport = lazy(() => import('./pages/DataImport').then(m => ({ default: m.default })))
const DataExport = lazy(() => import('./pages/DataExport').then(m => ({ default: m.default })))
const Consolidation = lazy(() => import('./pages/Consolidation').then(m => ({ default: m.default })))
const JePosting = lazy(() => import('./pages/JePosting').then(m => ({ default: m.default })))
const ThreeWayMatch = lazy(() => import('./pages/ThreeWayMatch').then(m => ({ default: m.default })))
const CashApplication = lazy(() => import('./pages/CashApplication').then(m => ({ default: m.default })))
const Accruals = lazy(() => import('./pages/Accruals').then(m => ({ default: m.default })))
const Controls = lazy(() => import('./pages/Controls').then(m => ({ default: m.default })))
const AuditPortal = lazy(() => import('./pages/AuditPortal').then(m => ({ default: m.default })))
const EvidenceBinder = lazy(() => import('./pages/EvidenceBinder').then(m => ({ default: m.default })))
const Qbo = lazy(() => import('./pages/Qbo').then(m => ({ default: m.default })))
const Xero = lazy(() => import('./pages/Xero').then(m => ({ default: m.default })))
const Plaid = lazy(() => import('./pages/Plaid').then(m => ({ default: m.default })))
const MappingStudio = lazy(() => import('./pages/MappingStudio').then(m => ({ default: m.default })))
const DataQuality = lazy(() => import('./pages/DataQuality').then(m => ({ default: m.default })))
const Budgeting = lazy(() => import('./pages/Budgeting').then(m => ({ default: m.default })))
const Forecasting = lazy(() => import('./pages/Forecasting').then(m => ({ default: m.default })))
const DriverPlanning = lazy(() => import('./pages/DriverPlanning').then(m => ({ default: m.default })))
const ScenarioEngine = lazy(() => import('./pages/ScenarioEngine').then(m => ({ default: m.default })))
const Covenants = lazy(() => import('./pages/Covenants').then(m => ({ default: m.default })))
const CostAllocation = lazy(() => import('./pages/CostAllocation').then(m => ({ default: m.default })))
const Kpi = lazy(() => import('./pages/Kpi').then(m => ({ default: m.default })))
const BoardPack = lazy(() => import('./pages/BoardPack').then(m => ({ default: m.default })))
const ExceptionClassifier = lazy(() => import('./pages/ExceptionClassifier').then(m => ({ default: m.default })))
const AutoFix = lazy(() => import('./pages/AutoFix').then(m => ({ default: m.default })))
const AccrualSuggest = lazy(() => import('./pages/AccrualSuggest').then(m => ({ default: m.default })))
const JeSuggest = lazy(() => import('./pages/JeSuggest').then(m => ({ default: m.default })))
const TriageQueue = lazy(() => import('./pages/TriageQueue').then(m => ({ default: m.default })))
const ReconExplain = lazy(() => import('./pages/ReconExplain').then(m => ({ default: m.default })))
const IntercompanyV2 = lazy(() => import('./pages/IntercompanyV2').then(m => ({ default: m.default })))
const Fx = lazy(() => import('./pages/Fx').then(m => ({ default: m.default })))
const CashflowConsol = lazy(() => import('./pages/CashflowConsol').then(m => ({ default: m.default })))
const WorkflowPlugin = lazy(() => import('./pages/WorkflowPlugin').then(m => ({ default: m.default })))
const WorkflowMarketplace = lazy(() => import('./pages/WorkflowMarketplace').then(m => ({ default: m.default })))
const ReportMarketplace = lazy(() => import('./pages/ReportMarketplace').then(m => ({ default: m.default })))
const Soc2 = lazy(() => import('./pages/Soc2').then(m => ({ default: m.default })))
const Gdpr = lazy(() => import('./pages/Gdpr').then(m => ({ default: m.default })))
const KeyManagement = lazy(() => import('./pages/KeyManagement').then(m => ({ default: m.default })))
const DataLake = lazy(() => import('./pages/DataLake').then(m => ({ default: m.default })))
const Lineage = lazy(() => import('./pages/Lineage').then(m => ({ default: m.default })))
const QueryLanguage = lazy(() => import('./pages/QueryLanguage').then(m => ({ default: m.default })))
const Abac = lazy(() => import('./pages/Abac').then(m => ({ default: m.default })))
const AdminConsole = lazy(() => import('./pages/AdminConsole').then(m => ({ default: m.default })))
const TraceExplorer = lazy(() => import('./pages/TraceExplorer').then(m => ({ default: m.default })))
const ReplayEngine = lazy(() => import('./pages/ReplayEngine').then(m => ({ default: m.default })))
const ToolRegistry = lazy(() => import('./pages/ToolRegistry').then(m => ({ default: m.default })))
const AgentRuntime = lazy(() => import('./pages/AgentRuntime').then(m => ({ default: m.default })))
const GeminiAdapter = lazy(() => import('./pages/GeminiAdapter').then(m => ({ default: m.default })))
const AiriaAdapter = lazy(() => import('./pages/AiriaAdapter').then(m => ({ default: m.default })))
const GradientAdapter = lazy(() => import('./pages/GradientAdapter').then(m => ({ default: m.default })))
const ConnectorMocks = lazy(() => import('./pages/ConnectorMocks').then(m => ({ default: m.default })))
const MlDataset = lazy(() => import('./pages/MlDataset').then(m => ({ default: m.default })))
const MlBaseline = lazy(() => import('./pages/MlBaseline').then(m => ({ default: m.default })))
const MlInference = lazy(() => import('./pages/MlInference').then(m => ({ default: m.default })))
const EvidenceSearch = lazy(() => import('./pages/EvidenceSearch').then(m => ({ default: m.default })))
const BlueprintBuilder = lazy(() => import('./pages/BlueprintBuilder').then(m => ({ default: m.default })))
const ReadinessDashboard = lazy(() => import('./pages/ReadinessDashboard').then(m => ({ default: m.default })))
const SecurityScoreboard = lazy(() => import('./pages/SecurityScoreboard').then(m => ({ default: m.default })))
const LapTimeTelemetry = lazy(() => import('./pages/LapTimeTelemetry').then(m => ({ default: m.default })))
const ProductivityRoi = lazy(() => import('./pages/ProductivityRoi').then(m => ({ default: m.default })))
const PitStopOptimizer = lazy(() => import('./pages/PitStopOptimizer').then(m => ({ default: m.default })))
const OneCockpit = lazy(() => import('./pages/OneCockpit').then(m => ({ default: m.default })))

export const routeElements = (
  <Routes>
    <Route path="/" element={<Dashboard />} />
    <Route path="/documents" element={<Documents />} />
    <Route path="/reconciliation" element={<Reconciliation />} />
    <Route path="/exceptions" element={<Exceptions />} />
    <Route path="/review" element={<ReviewQueue />} />
    <Route path="/audit" element={<AuditLog />} />
    <Route path="/settings" element={<Settings />} />
    <Route path="/race-control" element={<RaceControl />} />
    <Route path="/airia" element={<AiriaReadiness />} />
    <Route path="/cfo-cockpit" element={<CFOCockpit />} />
    <Route path="/agent-console" element={<AgentConsole />} />
    <Route path="/bloomberg" element={<BloombergTerminal />} />
    <Route path="/connectors" element={<Connectors />} />
    <Route path="/close-calendar" element={<CloseCalendar />} />
    <Route path="/treasury" element={<Treasury />} />
    <Route path="/compliance" element={<Compliance />} />
    <Route path="/ocr" element={<OCRPipeline />} />
    <Route path="/close-scorecard" element={<CloseScorecard />} />
    <Route path="/showcase" element={<HackathonShowcase />} />
    <Route path="/live-voice" element={<LiveVoiceAgent />} />
    <Route path="/storyteller" element={<MultimodalStoryteller />} />
    <Route path="/ui-navigator" element={<UINavigator />} />
    <Route path="/gradient-ai" element={<GradientAIDashboard />} />
    <Route path="/airia-everywhere" element={<AiriaEverywhereHub />} />
    <Route path="/multi-agent" element={<MultiAgentOrchestrator />} />
    <Route path="/close-period" element={Lazy(ClosePeriod)} />
    <Route path="/entities" element={Lazy(Entities)} />
    <Route path="/chart-of-accounts" element={Lazy(ChartOfAccounts)} />
    <Route path="/journal-entries" element={Lazy(JournalEntries)} />
    <Route path="/trial-balance" element={Lazy(TrialBalance)} />
    <Route path="/financial-statements" element={Lazy(FinancialStatements)} />
    <Route path="/bank-recon" element={Lazy(BankRecon)} />
    <Route path="/vendors" element={Lazy(Vendors)} />
    <Route path="/invoices" element={Lazy(Invoices)} />
    <Route path="/payments" element={Lazy(Payments)} />
    <Route path="/expenses" element={Lazy(Expenses)} />
    <Route path="/fixed-assets" element={Lazy(FixedAssets)} />
    <Route path="/depreciation" element={Lazy(Depreciation)} />
    <Route path="/intercompany" element={Lazy(Intercompany)} />
    <Route path="/tax" element={Lazy(Tax)} />
    <Route path="/revenue" element={Lazy(Revenue)} />
    <Route path="/leases" element={Lazy(Leases)} />
    <Route path="/close-mgmt" element={Lazy(CloseMgmt)} />
    <Route path="/flux" element={Lazy(Flux)} />
    <Route path="/approvals" element={Lazy(Approvals)} />
    <Route path="/users" element={Lazy(Users)} />
    <Route path="/roles" element={Lazy(Roles)} />
    <Route path="/notifications" element={Lazy(Notifications)} />
    <Route path="/reports" element={Lazy(Reports)} />
    <Route path="/data-import" element={Lazy(DataImport)} />
    <Route path="/data-export" element={Lazy(DataExport)} />
    <Route path="/consolidation" element={Lazy(Consolidation)} />
    <Route path="/je-posting" element={Lazy(JePosting)} />
    <Route path="/three-way-match" element={Lazy(ThreeWayMatch)} />
    <Route path="/cash-application" element={Lazy(CashApplication)} />
    <Route path="/accruals" element={Lazy(Accruals)} />
    <Route path="/controls" element={Lazy(Controls)} />
    <Route path="/audit-portal" element={Lazy(AuditPortal)} />
    <Route path="/evidence-binder" element={Lazy(EvidenceBinder)} />
    <Route path="/qbo" element={Lazy(Qbo)} />
    <Route path="/xero" element={Lazy(Xero)} />
    <Route path="/plaid" element={Lazy(Plaid)} />
    <Route path="/mapping-studio" element={Lazy(MappingStudio)} />
    <Route path="/data-quality" element={Lazy(DataQuality)} />
    <Route path="/budgeting" element={Lazy(Budgeting)} />
    <Route path="/forecasting" element={Lazy(Forecasting)} />
    <Route path="/driver-planning" element={Lazy(DriverPlanning)} />
    <Route path="/scenario-engine" element={Lazy(ScenarioEngine)} />
    <Route path="/covenants" element={Lazy(Covenants)} />
    <Route path="/cost-allocation" element={Lazy(CostAllocation)} />
    <Route path="/kpi" element={Lazy(Kpi)} />
    <Route path="/board-pack" element={Lazy(BoardPack)} />
    <Route path="/exception-classifier" element={Lazy(ExceptionClassifier)} />
    <Route path="/auto-fix" element={Lazy(AutoFix)} />
    <Route path="/accrual-suggest" element={Lazy(AccrualSuggest)} />
    <Route path="/je-suggest" element={Lazy(JeSuggest)} />
    <Route path="/triage-queue" element={Lazy(TriageQueue)} />
    <Route path="/recon-explain" element={Lazy(ReconExplain)} />
    <Route path="/intercompany-v2" element={Lazy(IntercompanyV2)} />
    <Route path="/fx" element={Lazy(Fx)} />
    <Route path="/cashflow-consol" element={Lazy(CashflowConsol)} />
    <Route path="/workflow-plugin" element={Lazy(WorkflowPlugin)} />
    <Route path="/workflow-marketplace" element={Lazy(WorkflowMarketplace)} />
    <Route path="/report-marketplace" element={Lazy(ReportMarketplace)} />
    <Route path="/soc2" element={Lazy(Soc2)} />
    <Route path="/gdpr" element={Lazy(Gdpr)} />
    <Route path="/key-management" element={Lazy(KeyManagement)} />
    <Route path="/data-lake" element={Lazy(DataLake)} />
    <Route path="/lineage" element={Lazy(Lineage)} />
    <Route path="/query-language" element={Lazy(QueryLanguage)} />
    <Route path="/abac" element={Lazy(Abac)} />
    <Route path="/admin-console" element={Lazy(AdminConsole)} />
    <Route path="/trace-explorer" element={Lazy(TraceExplorer)} />
    <Route path="/replay-engine" element={Lazy(ReplayEngine)} />
    <Route path="/tool-registry" element={Lazy(ToolRegistry)} />
    <Route path="/agent-runtime" element={Lazy(AgentRuntime)} />
    <Route path="/gemini-adapter" element={Lazy(GeminiAdapter)} />
    <Route path="/airia-adapter" element={Lazy(AiriaAdapter)} />
    <Route path="/gradient-adapter" element={Lazy(GradientAdapter)} />
    <Route path="/connector-mocks" element={Lazy(ConnectorMocks)} />
    <Route path="/ml-dataset" element={Lazy(MlDataset)} />
    <Route path="/ml-baseline" element={Lazy(MlBaseline)} />
    <Route path="/ml-inference" element={Lazy(MlInference)} />
    <Route path="/evidence-search" element={Lazy(EvidenceSearch)} />
    <Route path="/blueprint-builder" element={Lazy(BlueprintBuilder)} />
    <Route path="/readiness-dashboard" element={Lazy(ReadinessDashboard)} />
    <Route path="/security-scoreboard" element={Lazy(SecurityScoreboard)} />
    <Route path="/lap-time-telemetry" element={Lazy(LapTimeTelemetry)} />
    <Route path="/productivity-roi" element={Lazy(ProductivityRoi)} />
    <Route path="/pit-stop-optimizer" element={Lazy(PitStopOptimizer)} />
    <Route path="/one-cockpit" element={Lazy(OneCockpit)} />
    <Route path="*" element={<NotFound />} />
  </Routes>
)
