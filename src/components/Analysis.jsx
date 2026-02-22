import { useState, useRef, useEffect } from 'react'
import { Search, BarChart2, AlertTriangle, TrendingUp } from 'lucide-react'
import { Chart, registerables } from 'chart.js'
import axios from 'axios'

Chart.register(...registerables)

const API = axios.create({ baseURL: 'http://localhost:5000/api' })

const TABS = [
  { id: 'fundamental', label: 'Fundamental', icon: BarChart2 },
  { id: 'technical', label: 'Technical', icon: TrendingUp },
  { id: 'risk', label: 'Risk', icon: AlertTriangle },
]

function ScoreGauge({ score, label }) {
  const color = score >= 70 ? '#10b981' : score >= 45 ? '#f59e0b' : '#ef4444'
  return (
    <div className="flex flex-col items-center gap-2">
      <svg width="90" height="90" viewBox="0 0 90 90">
        <circle cx="45" cy="45" r="36" fill="none" stroke="#1f2937" strokeWidth="8" />
        <circle
          cx="45" cy="45" r="36"
          fill="none"
          stroke={color}
          strokeWidth="8"
          strokeDasharray={`${(score / 100) * 226} 226`}
          strokeLinecap="round"
          transform="rotate(-90 45 45)"
        />
        <text x="45" y="50" textAnchor="middle" fill={color} fontSize="16" fontWeight="bold">{score}</text>
      </svg>
      <span className="text-xs text-gray-400">{label}</span>
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
    setData(null)
    try {
      const res = await API.get(`/analysis/${t}`)
      setData(res.data)
    } catch (e) {
      setError(e.response?.data?.error || 'Analysis failed. Is the API running?')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { analyze(ticker) }, [ticker])

  // Render bar chart when data + tab changes
  useEffect(() => {
    if (!data || !barRef.current) return
    if (barChart.current) barChart.current.destroy()

    let labels = [], values = [], bgColors = []

    if (activeTab === 'fundamental' && data.fundamental?.sub_scores) {
      labels = ['Health', 'Valuation', 'Growth']
      values = [
        data.fundamental.sub_scores.health,
        data.fundamental.sub_scores.valuation,
        data.fundamental.sub_scores.growth,
      ]
    } else if (activeTab === 'technical' && data.technical) {
      labels = ['Technical Score']
      values = [data.technical.score]
    } else if (activeTab === 'risk' && data.risk) {
      labels = ['Risk Score']
      values = [data.risk.score]
    }

    bgColors = values.map(v =>
      v >= 70 ? 'rgba(16,185,129,0.7)' : v >= 45 ? 'rgba(245,158,11,0.7)' : 'rgba(239,68,68,0.7)'
    )

    if (!labels.length) return

    barChart.current = new Chart(barRef.current, {
      type: 'bar',
      data: {
        labels,
        datasets: [{ data: values, backgroundColor: bgColors, borderRadius: 6, borderSkipped: false }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: {
          y: { min: 0, max: 100, ticks: { color: '#9ca3af' }, grid: { color: '#1f2937' } },
          x: { ticks: { color: '#9ca3af' }, grid: { display: false } }
        }
      }
    })
  }, [data, activeTab])

  const tabData = data?.[activeTab]

  return (
    <div className="max-w-5xl mx-auto px-4 py-8 space-y-6">
      <div>
        <h1 className="text-2xl font-bold">Stock Analysis</h1>
        <p className="text-gray-400 text-sm mt-1">9-factor deep analysis powered by sentiment + fundamentals</p>
      </div>

      {/* Search */}
      <div className="flex gap-3">
        <div className="flex-1 relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-500" />
          <input
            id="analysis-ticker-input"
            type="text"
            value={input}
            onChange={e => setInput(e.target.value.toUpperCase())}
            onKeyDown={e => { if (e.key === 'Enter') setTicker(input) }}
            placeholder="e.g. AAPL, TSLA"
            className="w-full bg-gray-800 border border-gray-700 rounded-xl pl-9 pr-4 py-2.5 text-sm text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-emerald-500"
          />
        </div>
        <button
          id="analysis-submit-btn"
          onClick={() => setTicker(input)}
          className="px-5 py-2.5 bg-emerald-600 hover:bg-emerald-500 text-white text-sm font-medium rounded-xl transition"
        >
          Analyze
        </button>
      </div>

      {error && (
        <div className="bg-red-900/20 border border-red-700 text-red-300 rounded-xl p-4 text-sm">⚠️ {error}</div>
      )}

      {loading && (
        <div className="flex items-center justify-center py-24 text-gray-400">
          <BarChart2 className="w-5 h-5 animate-pulse mr-2" /> Analysing {ticker}…
        </div>
      )}

      {data && !loading && (
        <>
          {/* Overview gauges */}
          <div className="bg-gray-800/60 border border-gray-700 rounded-xl p-6">
            <div className="flex items-center justify-between mb-4">
              <h2 className="font-semibold">{ticker} Overview</h2>
              <span className={`text-xs font-bold px-3 py-1 rounded-full ${data.recommendation === 'BUY' ? 'bg-emerald-500/20 text-emerald-400' :
                  data.recommendation === 'SELL' ? 'bg-red-500/20 text-red-400' :
                    'bg-gray-700 text-gray-400'
                }`}>
                {data.recommendation ?? 'HOLD'}
              </span>
            </div>
            <div className="flex gap-8 justify-center flex-wrap">
              <ScoreGauge score={data.fundamental?.score ?? 0} label="Fundamental" />
              <ScoreGauge score={data.technical?.score ?? 0} label="Technical" />
              <ScoreGauge score={data.risk?.score ?? 0} label="Risk" />
              <ScoreGauge score={data.sentiment?.score ?? 0} label="Sentiment" />
            </div>
          </div>

          {/* Tabs */}
          <div className="bg-gray-800/60 border border-gray-700 rounded-xl overflow-hidden">
            <div className="flex border-b border-gray-700">
              {TABS.map(({ id, label, icon: Icon }) => (
                <button
                  key={id}
                  id={`tab-${id}`}
                  onClick={() => setActiveTab(id)}
                  className={`flex-1 flex items-center justify-center gap-2 py-3 text-sm font-medium transition ${activeTab === id ? 'bg-gray-700/50 text-white border-b-2 border-emerald-400' : 'text-gray-400 hover:text-white'
                    }`}
                >
                  <Icon className="w-4 h-4" />{label}
                </button>
              ))}
            </div>

            <div className="p-5 grid md:grid-cols-2 gap-6">
              {/* Bar chart */}
              <div className="h-52">
                <canvas ref={barRef} />
              </div>

              {/* Details */}
              <div className="space-y-2">
                <h3 className="text-sm font-semibold text-gray-300 mb-3">Key Signals</h3>
                {(tabData?.details || []).map((d, i) => (
                  <p key={i} className="text-xs text-gray-400 flex items-start gap-2">
                    <span className="text-emerald-400 mt-0.5">›</span>{d}
                  </p>
                ))}
                {(!tabData?.details?.length) && (
                  <p className="text-xs text-gray-500">No details available for this tab.</p>
                )}

                {activeTab === 'technical' && tabData?.signal && (
                  <div className={`mt-3 inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-bold ${tabData.signal === 'BUY' ? 'bg-emerald-500/20 text-emerald-400' :
                      tabData.signal === 'SELL' ? 'bg-red-500/20 text-red-400' : 'bg-gray-700 text-gray-300'
                    }`}>
                    Signal: {tabData.signal}
                  </div>
                )}
                {activeTab === 'risk' && tabData?.risk_level && (
                  <div className={`mt-3 inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-bold ${tabData.risk_level === 'LOW' ? 'bg-emerald-500/20 text-emerald-400' :
                      tabData.risk_level === 'HIGH' ? 'bg-red-500/20 text-red-400' : 'bg-yellow-500/20 text-yellow-400'
                    }`}>
                    Risk Level: {tabData.risk_level}
                  </div>
                )}
              </div>
            </div>
          </div>
        </>
      )}
    </div>
  )
}
