import { Routes, Route } from 'react-router-dom'
import Nav from './components/Nav'
import Dashboard from './pages/Dashboard'
import Documents from './pages/Documents'
import Reconciliation from './pages/Reconciliation'
import Exceptions from './pages/Exceptions'
import ReviewQueue from './pages/ReviewQueue'
import AuditLog from './pages/AuditLog'
import Settings from './pages/Settings'

export default function App() {
  return (
    <div className="min-h-screen flex flex-col" data-testid="app-root">
      <Nav />
      <main className="flex-1 p-6" data-testid="main-content">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/documents" element={<Documents />} />
          <Route path="/reconciliation" element={<Reconciliation />} />
          <Route path="/exceptions" element={<Exceptions />} />
          <Route path="/review" element={<ReviewQueue />} />
          <Route path="/audit" element={<AuditLog />} />
          <Route path="/settings" element={<Settings />} />
        </Routes>
      </main>
      <footer className="text-center text-xs text-gray-400 py-2" data-testid="footer">
        LedgerLive — Finance Ops Close Agent
      </footer>
    </div>
  )
}
