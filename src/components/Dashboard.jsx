import { useState, useEffect, useRef } from 'react'
import { TrendingUp, TrendingDown, Activity, RefreshCw } from 'lucide-react'
import { Chart, registerables } from 'chart.js'
import axios from 'axios'

Chart.register(...registerables)

const API = axios.create({ baseURL: 'http://localhost:5000/api' })

const WATCHLIST = ['AAPL', 'MSFT', 'GOOGL', 'TSLA', 'AMZN']

function StatCard({ label, value, sub, positive }) {
  return (
    <div className="bg-gray-800/60 border border-gray-700 rounded-xl p-5 flex flex-col gap-1">
      <span className="text-xs text-gray-400 uppercase tracking-wider">{label}</span>
      <span className={`text-2xl font-bold ${positive === undefined ? 'text-white' : positive ? 'text-emerald-400' : 'text-red-400'}`}>
        {value}
      </span>
      {sub && <span className="text-xs text-gray-500">{sub}</span>}
    </div>
  )
}

export default function Dashboard() {
  const [stocks, setStocks] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [selected, setSelected] = useState('AAPL')
  const chartRef = useRef(null)
  const chartInstance = useRef(null)

  // Fetch watchlist
  useEffect(() => {
    const fetchAll = async () => {
      setLoading(true)
      setError(null)
      try {
        const results = await Promise.allSettled(
          WATCHLIST.map(t => API.get(`/stock/${t}`))
        )
        const data = results
          .map((r, i) => ({
            ticker: WATCHLIST[i],
            ...(r.status === 'fulfilled' ? r.value.data : { error: true })
          }))
        setStocks(data)
      } catch (e) {
        setError('Could not reach API server. Is it running on port 5000?')
      } finally {
        setLoading(false)
      }
    }
    fetchAll()
  }, [])

  // Fetch price history for chart
  useEffect(() => {
    const fetchChart = async () => {
      try {
        const res = await API.get(`/stock/${selected}/history?period=3mo`)
        const history = res.data?.prices || []
        if (!history.length) return
        const labels = history.map(p => p.date)
        const prices = history.map(p => p.close)
        renderChart(labels, prices)
      } catch {
        // silently fail – chart stays blank
      }
    }
    fetchChart()
  }, [selected])

  function renderChart(labels, prices) {
    const ctx = chartRef.current
    if (!ctx) return
    if (chartInstance.current) chartInstance.current.destroy()

    chartInstance.current = new Chart(ctx, {
      type: 'line',
      data: {
        labels,
        datasets: [{
          label: selected,
          data: prices,
          borderColor: '#10b981',
          backgroundColor: 'rgba(16,185,129,0.08)',
          borderWidth: 2,
          pointRadius: 0,
          tension: 0.3,
          fill: true,
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: {
          x: {
            ticks: { color: '#6b7280', maxTicksLimit: 6 },
            grid: { color: '#1f2937' }
          },
          y: {
            ticks: { color: '#6b7280', callback: v => '$' + v.toFixed(0) },
            grid: { color: '#1f2937' }
          }
        }
      }
    })
  }

  const selectedStock = stocks.find(s => s.ticker === selected)

  return (
    <div className="max-w-7xl mx-auto px-4 py-8 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">Market Dashboard</h1>
          <p className="text-gray-400 text-sm mt-1">Live sentiment-powered stock overview</p>
        </div>
        <button
          onClick={() => window.location.reload()}
          className="flex items-center gap-2 text-sm text-gray-400 hover:text-white px-3 py-2 rounded-lg hover:bg-gray-800 transition"
        >
          <RefreshCw className="w-4 h-4" /> Refresh
        </button>
      </div>

      {error && (
        <div className="bg-red-900/20 border border-red-700 text-red-300 rounded-xl p-4 text-sm">
          ⚠️ {error}
        </div>
      )}

      {/* Stats */}
      {selectedStock && !selectedStock.error && (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <StatCard label="Price" value={`$${selectedStock.price?.toFixed(2) ?? 'N/A'}`} />
          <StatCard
            label="Change"
            value={`${selectedStock.change_pct > 0 ? '+' : ''}${selectedStock.change_pct?.toFixed(2) ?? '0'}%`}
            positive={selectedStock.change_pct > 0}
          />
          <StatCard
            label="Sentiment"
            value={selectedStock.sentiment?.label ?? 'N/A'}
            sub={`Score: ${selectedStock.sentiment?.score?.toFixed(2) ?? '—'}`}
            positive={selectedStock.sentiment?.label === 'POSITIVE'}
          />
          <StatCard label="Analysts" value={selectedStock.recommendation ?? 'N/A'} />
        </div>
      )}

      {/* Chart */}
      <div className="bg-gray-800/60 border border-gray-700 rounded-xl p-5">
        <div className="flex items-center justify-between mb-4">
          <h2 className="font-semibold text-gray-100">{selected} — 3 Month Price</h2>
          <div className="flex gap-2">
            {WATCHLIST.map(t => (
              <button
                key={t}
                onClick={() => setSelected(t)}
                className={`px-3 py-1 rounded-lg text-xs font-medium transition ${t === selected ? 'bg-emerald-500/20 text-emerald-400' : 'text-gray-400 hover:text-white hover:bg-gray-700'
                  }`}
              >
                {t}
              </button>
            ))}
          </div>
        </div>
        <div className="h-56">
          <canvas ref={chartRef} />
        </div>
      </div>

      {/* Watchlist table */}
      <div className="bg-gray-800/60 border border-gray-700 rounded-xl overflow-hidden">
        <div className="px-5 py-4 border-b border-gray-700">
          <h2 className="font-semibold text-gray-100">Watchlist</h2>
        </div>
        {loading ? (
          <div className="flex items-center justify-center py-12 text-gray-500">
            <Activity className="w-5 h-5 animate-pulse mr-2" /> Loading…
          </div>
        ) : (
          <table className="w-full text-sm">
            <thead>
              <tr className="text-gray-500 text-xs uppercase border-b border-gray-700">
                <th className="px-5 py-3 text-left">Ticker</th>
                <th className="px-5 py-3 text-right">Price</th>
                <th className="px-5 py-3 text-right">Change</th>
                <th className="px-5 py-3 text-right">Sentiment</th>
              </tr>
            </thead>
            <tbody>
              {stocks.map(s => (
                <tr
                  key={s.ticker}
                  onClick={() => setSelected(s.ticker)}
                  className={`border-b border-gray-700/50 cursor-pointer transition ${s.ticker === selected ? 'bg-emerald-500/5' : 'hover:bg-gray-700/30'
                    }`}
                >
                  <td className="px-5 py-3 font-bold text-white">{s.ticker}</td>
                  <td className="px-5 py-3 text-right text-gray-300">
                    {s.error ? '—' : `$${s.price?.toFixed(2)}`}
                  </td>
                  <td className={`px-5 py-3 text-right font-medium ${s.change_pct > 0 ? 'text-emerald-400' : s.change_pct < 0 ? 'text-red-400' : 'text-gray-400'
                    }`}>
                    {s.error ? '—' : (
                      <span className="flex items-center justify-end gap-1">
                        {s.change_pct > 0 ? <TrendingUp className="w-3 h-3" /> : <TrendingDown className="w-3 h-3" />}
                        {s.change_pct?.toFixed(2)}%
                      </span>
                    )}
                  </td>
                  <td className={`px-5 py-3 text-right ${s.sentiment?.label === 'POSITIVE' ? 'text-emerald-400' :
                      s.sentiment?.label === 'NEGATIVE' ? 'text-red-400' : 'text-gray-400'
                    }`}>
                    {s.sentiment?.label ?? '—'}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  )
}
