import { useState, useEffect, useRef } from 'react'
import { motion } from 'framer-motion'
import { TrendingUp, TrendingDown, Activity, RefreshCw, BarChart3, Globe } from 'lucide-react'
import { Chart, registerables } from 'chart.js'
import axios from 'axios'

Chart.register(...registerables)

const API = axios.create({ baseURL: `http://${window.location.hostname}:5000/api` })
const WATCHLIST = ['AAPL', 'MSFT', 'GOOGL', 'TSLA', 'AMZN']

function StatCard({ label, value, sub, positive, icon: Icon }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-card/40 backdrop-blur-xl border border-white/5 rounded-2xl p-6 relative overflow-hidden group hover:border-white/10 transition-all duration-300"
    >
      <div className="absolute top-0 right-0 p-4 opacity-5 group-hover:opacity-10 transition-opacity">
        <Icon className="w-16 h-16" />
      </div>
      <div className="relative z-10 flex flex-col gap-1">
        <span className="text-[10px] font-bold text-gray-500 uppercase tracking-[0.2em]">{label}</span>
        <div className="flex items-baseline gap-2">
          <span className={`text-2xl font-bold tracking-tight ${positive === undefined ? 'text-white' : positive ? 'text-primary' : 'text-danger'
            }`}>
            {value}
          </span>
        </div>
        {sub && <span className="text-xs text-gray-500 font-medium">{sub}</span>}
      </div>
    </motion.div>
  )
}

export default function Dashboard() {
  const [stocks, setStocks] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [selected, setSelected] = useState('AAPL')
  const chartRef = useRef(null)
  const chartInstance = useRef(null)

  useEffect(() => {
    const fetchAll = async () => {
      setLoading(true)
      try {
        const results = await Promise.allSettled(WATCHLIST.map(t => API.get(`/stock/${t}`)))
        const data = results.map((r, i) => ({
          ticker: WATCHLIST[i],
          ...(r.status === 'fulfilled' ? r.value.data : { error: true })
        }))
        setStocks(data)
      } catch (e) {
        setError('Connection failed. Please check if the API server is active.')
      } finally {
        setLoading(false)
      }
    }
    fetchAll()
  }, [])

  useEffect(() => {
    const fetchChart = async () => {
      try {
        const res = await API.get(`/stock/${selected}/history?period=3mo`)
        const history = res.data?.prices || []
        if (history.length) renderChart(history.map(p => p.date), history.map(p => p.close))
      } catch { }
    }
    fetchChart()
  }, [selected])

  function renderChart(labels, prices) {
    const ctx = chartRef.current
    if (!ctx) return
    if (chartInstance.current) chartInstance.current.destroy()

    const gradient = ctx.getContext('2d').createLinearGradient(0, 0, 0, 400)
    gradient.addColorStop(0, 'rgba(0, 255, 136, 0.15)')
    gradient.addColorStop(1, 'rgba(0, 255, 136, 0)')

    chartInstance.current = new Chart(ctx, {
      type: 'line',
      data: {
        labels,
        datasets: [{
          data: prices,
          borderColor: '#00ff88',
          borderWidth: 2.5,
          pointRadius: 0,
          pointHoverRadius: 6,
          pointHoverBackgroundColor: '#00ff88',
          pointHoverBorderColor: '#040715',
          pointHoverBorderWidth: 2,
          tension: 0.4,
          fill: true,
          backgroundColor: gradient,
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        interaction: { intersect: false, mode: 'index' },
        scales: {
          x: {
            ticks: { color: '#4b5563', maxTicksLimit: 8, font: { size: 10 } },
            grid: { display: false }
          },
          y: {
            ticks: { color: '#4b5563', font: { size: 10 }, callback: v => '$' + v.toLocaleString() },
            grid: { color: 'rgba(255,255,255,0.03)' }
          }
        }
      }
    })
  }

  const selectedStock = stocks.find(s => s.ticker === selected)

  return (
    <div className="max-w-7xl mx-auto px-6 lg:px-12 space-y-10">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-4">
        <div>
          <h1 className="tracking-tight mb-2">Market Overview</h1>
          <p className="text-gray-400 font-medium">Real-time intelligence and sentiment tracking.</p>
        </div>
        <button
          onClick={() => window.location.reload()}
          className="flex items-center gap-2 px-5 py-2.5 bg-white/5 hover:bg-white/10 border border-white/5 rounded-xl transition-all font-semibold text-sm"
        >
          <RefreshCw className="w-4 h-4" /> Refresh Data
        </button>
      </div>

      {error && (
        <div className="bg-danger/10 border border-danger/20 text-danger rounded-2xl p-4 text-sm font-medium">
          {error}
        </div>
      )}

      {/* Stats Grid */}
      {selectedStock && !selectedStock.error && (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          <StatCard icon={Globe} label="Current Price" value={`$${selectedStock.price?.toLocaleString() ?? '—'}`} />
          <StatCard
            icon={TrendingUp}
            label="24h Performance"
            value={`${selectedStock.change_pct > 0 ? '+' : ''}${selectedStock.change_pct?.toFixed(2)}%`}
            positive={selectedStock.change_pct > 0}
          />
          <StatCard
            icon={Activity}
            label="Sentiment Index"
            value={selectedStock.sentiment?.label ?? 'Neutral'}
            sub={`Score: ${selectedStock.sentiment?.score?.toFixed(2) ?? '0.50'}`}
            positive={selectedStock.sentiment?.label === 'POSITIVE'}
          />
          <StatCard icon={BarChart3} label="Consensus" value={selectedStock.recommendation ?? 'HOLD'} />
        </div>
      )}

      <div className="grid lg:grid-cols-3 gap-8">
        {/* Chart Card */}
        <div className="lg:col-span-2 bg-card/40 backdrop-blur-xl border border-white/5 rounded-3xl p-8">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between mb-8 gap-4">
            <h2 className="text-xl font-bold flex items-center gap-2">
              <span className="text-primary">{selected}</span>
              <span className="text-gray-500 font-medium text-sm">Performance History</span>
            </h2>
            <div className="flex p-1 bg-white/5 rounded-xl border border-white/5">
              {WATCHLIST.map(t => (
                <button
                  key={t}
                  onClick={() => setSelected(t)}
                  className={`px-4 py-1.5 rounded-lg text-xs font-bold transition-all ${t === selected ? 'bg-primary text-black shadow-lg shadow-primary/20' : 'text-gray-400 hover:text-white'
                    }`}
                >
                  {t}
                </button>
              ))}
            </div>
          </div>
          <div className="h-[380px] w-full">
            <canvas ref={chartRef} />
          </div>
        </div>

        {/* Watchlist Card */}
        <div className="bg-card/40 backdrop-blur-xl border border-white/5 rounded-3xl overflow-hidden flex flex-col">
          <div className="p-8 border-b border-white/5">
            <h2 className="text-xl font-bold underline decoration-primary/30 underline-offset-8">Watchlist</h2>
          </div>
          <div className="flex-1 overflow-auto">
            {loading ? (
              <div className="flex flex-col items-center justify-center h-full py-20 text-gray-500 gap-4">
                <Activity className="w-8 h-8 animate-pulse text-primary/40" />
                <p className="text-sm font-bold tracking-widest uppercase">Syncing Engine</p>
              </div>
            ) : (
              <table className="w-full text-left">
                <tbody>
                  {stocks.map(s => (
                    <tr
                      key={s.ticker}
                      onClick={() => setSelected(s.ticker)}
                      className={`group border-b border-white/5 cursor-pointer transition-all ${s.ticker === selected ? 'bg-white/5' : 'hover:bg-white/[0.02]'
                        }`}
                    >
                      <td className="px-8 py-5">
                        <div className="flex flex-col">
                          <span className="font-bold text-lg group-hover:text-primary transition-colors">{s.ticker}</span>
                          <span className="text-[10px] text-gray-500 font-bold uppercase tracking-wider">Technology</span>
                        </div>
                      </td>
                      <td className="px-8 py-5 text-right">
                        <div className="flex flex-col items-end">
                          <span className="font-bold">{s.error ? '—' : `$${s.price?.toLocaleString()}`}</span>
                          <div className={`flex items-center gap-1 text-xs font-bold ${s.change_pct > 0 ? 'text-primary' : s.change_pct < 0 ? 'text-danger' : 'text-gray-500'
                            }`}>
                            {s.change_pct > 0 ? <TrendingUp className="w-3 h-3" /> : <TrendingDown className="w-3 h-3" />}
                            {Math.abs(s.change_pct || 0).toFixed(2)}%
                          </div>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
