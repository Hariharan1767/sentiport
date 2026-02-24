import { useState, useRef, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Search, BarChart2, AlertTriangle, TrendingUp, Info } from 'lucide-react'
import { Chart, registerables } from 'chart.js'
import axios from 'axios'

Chart.register(...registerables)

const API = axios.create({ baseURL: `http://${window.location.hostname}:5000/api` })

const TABS = [
  { id: 'fundamental', label: 'Fundamental', icon: BarChart2, color: '#00ff88' },
  { id: 'technical', label: 'Technical', icon: TrendingUp, color: '#3b82f6' },
  { id: 'risk', label: 'Risk', icon: AlertTriangle, color: '#ef4444' },
]

function ScoreCircle({ score, label, color }) {
  const radius = 40
  const circumference = 2 * Math.PI * radius
  const offset = circumference - (score / 100) * circumference

  return (
    <div className="flex flex-col items-center gap-4 group">
      <div className="relative w-24 h-24">
        <svg className="w-24 h-24 transform -rotate-90">
          <circle cx="48" cy="48" r={radius} stroke="rgba(255,255,255,0.05)" strokeWidth="6" fill="none" />
          <motion.circle
            initial={{ strokeDashoffset: circumference }}
            animate={{ strokeDashoffset: offset }}
            transition={{ duration: 1, ease: 'easeOut' }}
            cx="48" cy="48" r={radius}
            stroke={color}
            strokeWidth="6"
            strokeDasharray={circumference}
            strokeLinecap="round"
            fill="none"
          />
        </svg>
        <div className="absolute inset-0 flex items-center justify-center flex-col">
          <span className="text-xl font-bold font-mono tracking-tighter" style={{ color }}>{Math.round(score)}</span>
        </div>
      </div>
      <span className="text-[10px] font-bold text-gray-400 uppercase tracking-widest group-hover:text-white transition-colors">
        {label}
      </span>
    </div>
  )
}

export default function Analysis() {
  const [ticker, setTicker] = useState('AAPL')
  const [input, setInput] = useState('AAPL')
  const [activeTab, setActiveTab] = useState('fundamental')
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const barRef = useRef(null)
  const barChart = useRef(null)

  const analyze = async (t) => {
    setLoading(true)
    setError(null)
    try {
      const res = await API.get(`/analysis/${t}`)
      setData(res.data)
    } catch (e) {
      setError(e.response?.data?.error || 'Database sync failed. Check API status.')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { analyze(ticker) }, [ticker])

  useEffect(() => {
    if (!data || !barRef.current) return
    if (barChart.current) barChart.current.destroy()

    let labels = [], values = [], color = '#00ff88'

    if (activeTab === 'fundamental' && data.fundamental?.sub_scores) {
      labels = ['Health', 'Valuation', 'Growth']
      values = [
        data.fundamental.sub_scores.health,
        data.fundamental.sub_scores.valuation,
        data.fundamental.sub_scores.growth,
      ]
      color = '#00ff88'
    } else if (activeTab === 'technical' && data.technical) {
      labels = ['Indicator Strength']
      values = [data.technical.score]
      color = '#3b82f6'
    } else if (activeTab === 'risk' && data.risk) {
      labels = ['Risk Rating']
      values = [data.risk.score]
      color = '#ef4444'
    }

    if (!labels.length) return

    barChart.current = new Chart(barRef.current, {
      type: 'bar',
      data: {
        labels,
        datasets: [{
          data: values,
          backgroundColor: color + '44',
          borderColor: color,
          borderWidth: 2,
          borderRadius: 8,
          barThickness: 40
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: {
          y: {
            min: 0, max: 100,
            ticks: { color: '#4b5563', font: { size: 10 } },
            grid: { color: 'rgba(255,255,255,0.03)' }
          },
          x: {
            ticks: { color: '#9ca3af', font: { weight: 'bold', size: 10 } },
            grid: { display: false }
          }
        }
      }
    })
  }, [data, activeTab])

  const tabData = data?.[activeTab]

  return (
    <div className="max-w-5xl mx-auto px-6 lg:px-12 space-y-8">
      <div>
        <h1 className="tracking-tight mb-2">Security Analysis</h1>
        <p className="text-gray-400 font-medium italic">Deep intelligence across 9 quantitative factors.</p>
      </div>

      {/* Search Interaction */}
      <div className="flex gap-4 p-2 bg-white/5 border border-white/5 rounded-2xl">
        <div className="flex-1 relative">
          <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-500" />
          <input
            id="analysis-ticker-input"
            type="text"
            value={input}
            onChange={e => setInput(e.target.value.toUpperCase())}
            onKeyDown={e => { if (e.key === 'Enter') setTicker(input) }}
            placeholder="Search Security (e.g. TSLA)"
            className="w-full bg-transparent border-none rounded-xl pl-11 pr-4 py-3 text-sm font-bold placeholder:text-gray-600 focus:ring-0"
          />
        </div>
        <button
          id="analysis-submit-btn"
          onClick={() => setTicker(input)}
          className="px-8 py-3 bg-primary text-black font-bold rounded-xl hover:scale-105 active:scale-95 transition-transform shadow-lg shadow-primary/20"
        >
          ANALYZE
        </button>
      </div>

      {error && (
        <div className="p-4 bg-danger/10 border border-danger/20 text-danger text-sm font-bold rounded-xl animate-pulse">
          ⚠️ {error}
        </div>
      )}

      {loading ? (
        <div className="flex flex-col items-center justify-center py-40 text-gray-500 gap-6">
          <div className="w-16 h-1 w-16 bg-white/5 rounded-full overflow-hidden relative">
            <motion.div
              className="absolute inset-0 bg-primary"
              animate={{ left: ['-100%', '100%'] }}
              transition={{ repeat: Infinity, duration: 1.5, ease: 'easeInOut' }}
            />
          </div>
          <p className="text-xs font-bold tracking-[0.3em] uppercase">Processing Data Stream</p>
        </div>
      ) : data && (
        <div className="space-y-8">
          {/* Overview Section */}
          <motion.div
            initial={{ opacity: 0, scale: 0.98 }}
            animate={{ opacity: 1, scale: 1 }}
            className="bg-card/40 backdrop-blur-xl border border-white/5 rounded-3xl p-10 relative overflow-hidden"
          >
            <div className="absolute top-0 right-0 p-8">
              <span className={`text-xs font-black px-4 py-1.5 rounded-full border ${data.recommendation === 'BUY' ? 'bg-primary/10 text-primary border-primary/20' :
                data.recommendation === 'SELL' ? 'bg-danger/10 text-danger border-danger/20' :
                  'bg-white/5 text-gray-400 border-white/10'
                }`}>
                {data.recommendation ?? 'HOLD'}
              </span>
            </div>

            <div className="flex flex-col lg:flex-row items-center justify-center gap-16">
              <ScoreCircle score={data.fundamental?.score ?? 0} label="Fundamental" color="#00ff88" />
              <ScoreCircle score={data.technical?.score ?? 0} label="Technical" color="#3b82f6" />
              <ScoreCircle score={data.risk?.score ?? 0} label="Risk Profile" color="#ef4444" />
              <ScoreCircle score={data.sentiment?.score ?? 0} label="Market Sentiment" color="#f59e0b" />
            </div>
          </motion.div>

          {/* Detailed Tabs */}
          <div className="bg-card/40 backdrop-blur-xl border border-white/5 rounded-3xl overflow-hidden shadow-2xl shadow-black/40">
            <div className="flex bg-white/5 p-2">
              {TABS.map(({ id, label, icon: Icon, color }) => (
                <button
                  key={id}
                  id={`tab-${id}`}
                  onClick={() => setActiveTab(id)}
                  className={`flex-1 flex items-center justify-center gap-3 py-4 text-xs font-black uppercase tracking-tighter transition-all ${activeTab === id ? 'text-white' : 'text-gray-500 hover:text-gray-300'
                    }`}
                >
                  <Icon className="w-4 h-4" style={{ color: activeTab === id ? color : 'currentColor' }} />
                  {label}
                  {activeTab === id && (
                    <motion.div layoutId="tab-underline" className="absolute bottom-0 h-0.5 bg-primary w-full" />
                  )}
                </button>
              ))}
            </div>

            <div className="p-10 grid lg:grid-cols-2 gap-12 items-center">
              <div className="h-[300px]">
                <canvas ref={barRef} />
              </div>

              <div className="space-y-6">
                <div className="flex items-center gap-3">
                  <Info className="w-5 h-5 text-primary" />
                  <h3 className="text-sm font-black uppercase tracking-widest text-white">Insight Generator</h3>
                </div>

                <div className="space-y-4">
                  {(tabData?.details || []).map((d, i) => (
                    <motion.div
                      key={i}
                      initial={{ opacity: 0, x: 10 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: i * 0.1 }}
                      className="flex items-start gap-4 p-4 bg-white/[0.03] border border-white/5 rounded-2xl"
                    >
                      <div className="w-1.5 h-1.5 rounded-full bg-primary mt-2 shrink-0 shadow-[0_0_8px_rgba(0,255,136,0.6)]" />
                      <p className="text-sm text-gray-300 leading-relaxed font-medium">{d}</p>
                    </motion.div>
                  ))}
                </div>

                {activeTab === 'technical' && tabData?.signal && (
                  <div className={`mt-6 p-4 rounded-2xl border flex items-center justify-between ${tabData.signal === 'BUY' ? 'bg-primary/10 border-primary/20 text-primary' :
                    tabData.signal === 'SELL' ? 'bg-danger/10 border-danger/20 text-danger' :
                      'bg-white/5 border-white/10 text-gray-400'
                    }`}>
                    <span className="text-xs font-black uppercase">Execution Signal</span>
                    <span className="font-black text-lg">{tabData.signal}</span>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
