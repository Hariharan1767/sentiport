import { useState } from 'react'
import Navigation from './components/Navigation'
import Dashboard from './components/Dashboard'
import Analysis from './components/Analysis'
import Optimize from './components/Optimize'
import Settings from './components/Settings'

const PAGES = {
  dashboard: Dashboard,
  analysis: Analysis,
  optimize: Optimize,
  settings: Settings,
}

export default function App() {
  const [currentPage, setCurrentPage] = useState('dashboard')

  const PageComponent = PAGES[currentPage] || Dashboard

  return (
    <div className="min-h-screen bg-gray-950 text-white font-sans">
      <Navigation currentPage={currentPage} onNavigate={setCurrentPage} />
      <main className="pt-16">
        <PageComponent />
      </main>
    </div>
  )
}
