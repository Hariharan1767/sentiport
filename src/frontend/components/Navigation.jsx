import { TrendingUp } from 'lucide-react'
import { motion } from 'framer-motion'

const NAV_LINKS = [
  { id: 'dashboard', label: 'Dashboard' },
  { id: 'analysis', label: 'Analysis' },
  { id: 'optimize', label: 'Optimize' },
  { id: 'settings', label: 'Settings' },
]

export default function Navigation({ currentPage, onNavigate }) {
  return (
    <nav className="fixed top-0 left-0 right-0 z-50 transition-all duration-300">
      <div className="absolute inset-0 bg-background/60 backdrop-blur-md border-b border-white/5" />
      <div className="relative max-w-7xl mx-auto px-6 lg:px-12">
        <div className="flex items-center justify-between h-20">
          {/* Brand */}
          <div
            className="flex items-center gap-3 cursor-pointer group"
            onClick={() => onNavigate('dashboard')}
          >
            <div className="p-2 bg-primary/10 rounded-xl group-hover:bg-primary/20 transition-all duration-300">
              <TrendingUp className="w-6 h-6 text-primary" />
            </div>
            <span className="text-xl font-bold tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-white to-white/60">
              SentiPort
            </span>
          </div>

          {/* Links */}
          <div className="hidden md:flex items-center gap-2">
            {NAV_LINKS.map(({ id, label }) => (
              <button
                key={id}
                id={`nav-${id}`}
                onClick={() => onNavigate(id)}
                className="relative px-5 py-2.5 text-sm font-semibold transition-all duration-300 group"
              >
                <span className={`relative z-10 ${currentPage === id ? 'text-primary' : 'text-gray-400 group-hover:text-white'
                  }`}>
                  {label}
                </span>
                {currentPage === id && (
                  <motion.div
                    layoutId="nav-bg"
                    className="absolute inset-0 bg-primary/10 rounded-xl border border-primary/20"
                    transition={{ type: 'spring', bounce: 0.2, duration: 0.6 }}
                  />
                )}
              </button>
            ))}
          </div>

          {/* Mobile Menu Button - Placeholder for mobile refinement if needed */}
          <div className="md:hidden">
            <button className="p-2 text-gray-400 hover:text-white">
              <span className="sr-only">Menu</span>
              <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16m-7 6h7" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </nav>
  )
}
