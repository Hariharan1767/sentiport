import { motion } from 'framer-motion'
import { User, Bell, Shield, Database, Layout, Smartphone } from 'lucide-react'

const SECTIONS = [
  { id: 'profile', icon: User, label: 'Account Profile', desc: 'Manage your primary account details and security.' },
  { id: 'data', icon: Database, label: 'Data Providers', desc: 'Configure AlphaVantage and NewsAPI credentials.' },
  { id: 'ui', icon: Layout, label: 'Interface Settings', desc: 'Toggle glassmorphism intensity and theme colors.' },
  { id: 'mobile', icon: Smartphone, label: 'Device Sync', desc: 'Manage your mobile terminal connections.' },
]

export default function Settings() {
  return (
    <div className="max-w-4xl mx-auto px-6 lg:px-12 space-y-10">
      <div>
        <h1 className="tracking-tight mb-2">Terminal Settings</h1>
        <p className="text-gray-400 font-medium italic">Configure your SentiPort instance for precision analysis.</p>
      </div>

      <div className="grid gap-6">
        {SECTIONS.map((s, i) => (
          <motion.div
            key={s.id}
            initial={{ opacity: 0, x: -10 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: i * 0.1 }}
            className="group bg-card/40 backdrop-blur-xl border border-white/5 rounded-3xl p-8 flex items-center justify-between hover:bg-white/[0.04] hover:border-white/10 transition-all cursor-pointer"
          >
            <div className="flex items-center gap-6">
              <div className="p-4 bg-white/5 rounded-2xl text-gray-400 group-hover:text-primary transition-colors">
                <s.icon className="w-6 h-6" />
              </div>
              <div>
                <h3 className="text-lg font-bold group-hover:text-white transition-colors">{s.label}</h3>
                <p className="text-xs text-gray-500 font-medium">{s.desc}</p>
              </div>
            </div>
            <div className="p-2 border border-white/5 rounded-full group-hover:border-primary/20 group-hover:bg-primary/5 transition-all">
              <svg className="w-5 h-5 text-gray-600 group-hover:text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
              </svg>
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  )
}
