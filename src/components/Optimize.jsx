import { useState, useRef, useEffect } from 'react'
import { Plus, X, Sliders, PieChart, CheckCircle } from 'lucide-react'
import { Chart, registerables } from 'chart.js'
import axios from 'axios'

Chart.register(...registerables)

const API = axios.create({ baseURL: 'http://localhost:5000/api' })

const METHODS = [
  { id: 'mean_variance', label: 'Mean-Variance' },
  { id: 'sentiment', label: 'Sentiment-Enhanced' },
]

const PALETTE = ['#10b981', '#3b82f6', '#f59e0b', '#8b5cf6', '#ef4444', '#ec4899', '#14b8a6', '#f97316']

export default function Optimize() {
  const [tickers, setTickers] = useState(['AAPL', 'MSFT', 'GOOGL'])
  const [tickerInput, setTickerInput] = useState('')
  const [method, setMethod] = useState('mean_variance')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const pieRef = useRef(null)
  const pieChart = useRef(null)

  const addTicker = () => {
    const t = tickerInput.trim().toUpperCase()
    if (t && !tickers.includes(t) && tickers.length < 8) {
      setTickers(prev => [...prev, t])
      setTickerInput('')
    }
  }

  const removeTicker = (t) => setTickers(prev => prev.filter(x => x !== t))

  const optimize = async () => {
    if (tickers.length < 2) { setError('Add at least 2 tickers'); return }
    setLoading(true)
    setError(null)
    setResult(null)
    try {
      const res = await API.post('/optimize', { tickers, method })
      setResult(res.data)
    } catch (e) {
      setError(e.response?.data?.error || 'Optimization failed. Is the API running?')
    } finally {
      setLoading(false)
    }
  }

  // Pie chart
  useEffect(() => {
    if (!result?.allocation || !pieRef.current) return
    if (pieChart.current) pieChart.current.destroy()

    const labels = Object.keys(result.allocation)
    const values = Object.values(result.allocation).map(v => (v * 100).toFixed(1))

    pieChart.current = new Chart(pieRef.current, {
      type: 'doughnut',
      data: {
        labels,
        datasets: [{
          data: values,
          backgroundColor: PALETTE.slice(0, labels.length),
          borderColor: '#111827',
          borderWidth: 2,
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'right',
            labels: { color: '#9ca3af', padding: 12 }
          },
          tooltip: {
            callbacks: { label: ctx => `${ctx.label}: ${ctx.parsed}%` }
          }
        }
      }
    })
  }, [result])

  return (
    <div className="max-w-5xl mx-auto px-4 py-8 space-y-6">
      <div>
        <h1 className="text-2xl font-bold">Portfolio Optimizer</h1>
        <p className="text-gray-400 text-sm mt-1">Sentiment-aware Markowitz portfolio optimization</p>
      </div>

      <div className="grid md:grid-cols-2 gap-6">
        {/* Config panel */}
        <div className="bg-gray-800/60 border border-gray-700 rounded-xl p-5 space-y-5">
          <h2 className="font-semibold flex items-center gap-2">
            <Sliders className="w-4 h-4 text-emerald-400" /> Configuration
          </h2>

          {/* Ticker input */}
          <div>
            <label className="block text-xs text-gray-400 mb-2 uppercase tracking-wide">Tickers</label>
            <div className="flex gap-2">
              <input
                id="optimize-ticker-input"
                type="text"
                value={tickerInput}
                onChange={e => setTickerInput(e.target.value.toUpperCase())}
                onKeyDown={e => { if (e.key === 'Enter') addTicker() }}
                placeholder="Add ticker…"
                className="flex-1 bg-gray-900 border border-gray-600 rounded-lg px-3 py-2 text-sm text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-emerald-500"
              />
              <button
                id="optimize-add-ticker-btn"
                onClick={addTicker}
                className="px-3 py-2 bg-gray-700 hover:bg-gray-600 rounded-lg transition text-gray-300"
              >
                <Plus className="w-4 h-4" />
              </button>
            </div>

            <div className="flex flex-wrap gap-2 mt-3">
              {tickers.map(t => (
                <span key={t} className="flex items-center gap-1.5 bg-gray-700 text-gray-200 text-xs px-3 py-1 rounded-full">
                  {t}
                  <button onClick={() => removeTicker(t)} className="text-gray-500 hover:text-red-400 transition">
                    <X className="w-3 h-3" />
                  </button>
                </span>
              ))}
            </div>
          </div>

          {/* Method */}
          <div>
            <label className="block text-xs text-gray-400 mb-2 uppercase tracking-wide">Optimization Method</label>
            <div className="flex gap-2">
              {METHODS.map(m => (
                <button
                  key={m.id}
                  id={`method-${m.id}`}
                  onClick={() => setMethod(m.id)}
                  className={`flex-1 py-2 rounded-lg text-sm font-medium transition ${method === m.id ? 'bg-emerald-600 text-white' : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
                    }`}
                >
                  {m.label}
                </button>
              ))}
            </div>
          </div>

          <button
            id="optimize-run-btn"
            onClick={optimize}
            disabled={loading}
            className="w-full py-3 bg-emerald-600 hover:bg-emerald-500 disabled:opacity-50 text-white font-medium rounded-xl transition"
          >
            {loading ? 'Optimizing…' : 'Run Optimization'}
          </button>

          {error && (
            <p className="text-red-400 text-xs">⚠️ {error}</p>
          )}
        </div>

        {/* Result panel */}
        <div className="bg-gray-800/60 border border-gray-700 rounded-xl p-5 space-y-4">
          <h2 className="font-semibold flex items-center gap-2">
            <PieChart className="w-4 h-4 text-emerald-400" /> Allocation
          </h2>

          {!result && !loading && (
            <div className="flex items-center justify-center h-48 text-gray-500 text-sm">
              Run optimization to see results
            </div>
          )}

          {loading && (
            <div className="flex items-center justify-center h-48 text-gray-400">
              <PieChart className="w-5 h-5 animate-spin mr-2" /> Computing…
            </div>
          )}

          {result && (
            <>
              <div className="h-52">
                <canvas ref={pieRef} />
              </div>

              {/* Metrics */}
              <div className="grid grid-cols-3 gap-3 mt-4">
                {[
                  { label: 'Exp. Return', value: `${((result.metrics?.expected_return ?? 0) * 100).toFixed(2)}%`, color: 'text-emerald-400' },
                  { label: 'Risk (Vol)', value: `${((result.metrics?.risk ?? 0) * 100).toFixed(2)}%`, color: 'text-red-400' },
                  { label: 'Sharpe', value: (result.metrics?.sharpe_ratio ?? 0).toFixed(3), color: 'text-blue-400' },
                ].map(m => (
                  <div key={m.label} className="bg-gray-900/50 rounded-xl p-3 text-center">
                    <div className={`text-lg font-bold ${m.color}`}>{m.value}</div>
                    <div className="text-xs text-gray-500">{m.label}</div>
                  </div>
                ))}
              </div>

              <div className="space-y-2 mt-2">
                {Object.entries(result.allocation).map(([t, w]) => (
                  <div key={t} className="flex items-center gap-3">
                    <span className="w-14 text-xs font-bold text-gray-300">{t}</span>
                    <div className="flex-1 bg-gray-700 rounded-full h-2">
                      <div
                        className="bg-emerald-500 h-2 rounded-full transition-all"
                        style={{ width: `${(w * 100).toFixed(1)}%` }}
                      />
                    </div>
                    <span className="text-xs text-gray-400 w-12 text-right">{(w * 100).toFixed(1)}%</span>
                  </div>
                ))}
              </div>

              <div className="flex items-center gap-2 mt-3 text-xs text-emerald-400">
                <CheckCircle className="w-4 h-4" /> Method: {result.method}
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  )
}
