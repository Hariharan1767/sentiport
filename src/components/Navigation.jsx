import { TrendingUp } from 'lucide-react'

const NAV_LINKS = [
  { id: 'dashboard', label: 'Dashboard' },
  { id: 'analysis', label: 'Analysis' },
  { id: 'optimize', label: 'Optimize' },
  { id: 'settings', label: 'Settings' },
]

export default function Navigation({ currentPage, onNavigate }) {
  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-gray-900/80 backdrop-blur border-b border-gray-800">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Brand */}
          <div className="flex items-center gap-2">
            <TrendingUp className="w-7 h-7 text-emerald-400" />
            <span className="text-lg font-bold tracking-tight">SentiPort</span>
          </div>

          {/* Links */}
          <div className="flex items-center gap-1">
            {NAV_LINKS.map(({ id, label }) => (
              <button
                key={id}
                id={`nav-${id}`}
                onClick={() => onNavigate(id)}
                className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${currentPage === id
                    ? 'bg-emerald-500/20 text-emerald-400'
                    : 'text-gray-400 hover:text-white hover:bg-gray-800'
                  }`}
              >
                {label}
              </button>
            ))}
          </div>
        </div>
      </div>
    </nav>
  )
}
