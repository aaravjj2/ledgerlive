import Nav from './components/Nav'
import VoiceAssistant from './components/VoiceAssistant'
import { routeElements } from './routes'

export default function App() {
  return (
    <div className="min-h-screen flex flex-col" data-testid="app-root">
      <Nav />
      <main className="flex-1 p-6" data-testid="main-content">
        {routeElements}
      </main>
      <footer className="text-center text-xs text-gray-400 py-2" data-testid="footer">
        LedgerLive — Finance Ops Close Agent
      </footer>
      <VoiceAssistant />
    </div>
  )
}
