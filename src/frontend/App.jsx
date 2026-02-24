import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
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

  // Error tracking
  useEffect(() => {
    window.onerror = (msg, url, line) => {
      console.log(`[UI ERROR] ${msg} at ${line}`);
      alert(`UI Error: ${msg}`);
    };
  }, []);

  return (
    <div className="min-h-screen bg-background text-white font-epilogue selection:bg-primary/30 selection:text-primary">
      {/* RAW DEBUG PANEL - FOR TROUBLESHOOTING */}
      <div style={{ position: 'fixed', bottom: 10, left: 10, zIndex: 9999, background: 'red', color: 'white', padding: '10px', fontSize: '12px' }}>
        DEBUG: {currentPage} |
        <button onClick={() => setCurrentPage('dashboard')} style={{ margin: '0 5px', color: 'black' }}>DASH</button>
        <button onClick={() => setCurrentPage('analysis')} style={{ margin: '0 5px', color: 'black' }}>ANLY</button>
        <button onClick={() => setCurrentPage('optimize')} style={{ margin: '0 5px', color: 'black' }}>OPT</button>
      </div>

      {/* Background radial glows */}
      <div className="fixed inset-0 pointer-events-none z-0 overflow-hidden">
        <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-primary/10 rounded-full blur-[120px]" />
        <div className="absolute bottom-[10%] right-[-5%] w-[30%] h-[30%] bg-accent/10 rounded-full blur-[120px]" />
      </div>

      <div className="relative z-10">
        <Navigation currentPage={currentPage} onNavigate={setCurrentPage} />

        <main className="pt-24 pb-12">
          <AnimatePresence mode="wait">
            <motion.div
              key={currentPage}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              transition={{ duration: 0.3, ease: 'easeOut' }}
            >
              <PageComponent />
            </motion.div>
          </AnimatePresence>
        </main>
      </div>

      <footer className="relative z-10 py-8 border-t border-white/5 text-center">
        <p className="text-gray-500 text-sm">
          &copy; {new Date().getFullYear()} SentiPort • Advanced Portfolio Intelligence
        </p>
      </footer>
    </div>
  )
}
