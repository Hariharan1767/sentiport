import { useState, useRef, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { PieChart, Settings2, Play, Download, Trash2, Plus, Info, RefreshCw } from 'lucide-react'
import { Chart, registerables } from 'chart.js'
import axios from 'axios'

Chart.register(...registerables)

const API = axios.create({ baseURL: `http://${window.location.hostname}:5000/api` })
const DEFAULT_TICKERS = ['AAPL', 'MSFT', 'GOOGL']

export default function Optimize() {
  const [tickers, setTickers] = useState(DEFAULT_TICKERS)
  const [input, setInput] = useState('')
  const [method, setMethod] = useState('mean_variance')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)

  const pieRef = useRef(null)
  const pieChart = useRef(null)

  const addTicker = () => {
    if (input && !tickers.includes(input)) {
      setTickers([...tickers, input.toUpperCase()])
      setInput('')
    }
  }

  const removeTicker = (t) => setTickers(tickers.filter(x => x !== t))

  const optimize = async () => {
    if (tickers.length < 2) {
      setError('Select at least 2 securities for optimization.')
      return
    }
    setLoading(true)
    setError(null)
    setResult(null)
    try {
      const res = await API.post('/portfolio/optimize', { tickers, method })
      setResult(res.data)
    } catch (e) {
      setError(e.response?.data?.error || 'Optimization engine failed. Verify ticker availability.')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    if (!result || !pieRef.current) return
    if (pieChart.current) pieChart.current.destroy()

    const labels = Object.keys(result.allocation)
    const values = Object.values(result.allocation)

    pieChart.current = new Chart(pieRef.current, {
      type: 'doughnut',
      data: {
        labels,
        datasets: [{
          data: values,
          backgroundColor: [
            '#00ff88', '#3b82f6', '#ef4444', '#f59e0b', '#8b5cf6', '#ec4899'
          ],
          borderColor: 'rgba(4, 7, 21, 0.8)',
          borderWidth: 4,
          hoverOffset: 15
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        cutout: '75%',
        plugins: {
          legend: {
            position: 'bottom',
            labels: { color: '#9ca3af', font: { weight: 'bold', size: 11 }, padding: 20, usePointStyle: true }
          }
        },
        animation: { animateRotate: true, animateScale: true }
      }
    })
  }, [result])

  return (
    <div className="max-w-6xl mx-auto px-6 lg:px-12 space-y-10">
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-6">
        <div>
          <h1 className="tracking-tight mb-2">Modern Portfolio Optimizer</h1>
          <p className="text-gray-400 font-medium">Mathematically optimized allocations based on Risk/Reward efficient frontier.</p>
        </div>
        <div className="flex p-1 bg-white/5 border border-white/5 rounded-2xl">
          <button
            onClick={() => setMethod('mean_variance')}
            className={`px-6 py-2.5 rounded-xl text-xs font-black transition-all ${method === 'mean_variance' ? 'bg-primary text-black' : 'text-gray-500 hover:text-white'
              }`}
          >
            MEAN-VARIANCE
          </button>
          <button
            onClick={() => setMethod('sentiment_enhanced')}
            className={`px-6 py-2.5 rounded-xl text-xs font-black transition-all ${method === 'sentiment_enhanced' ? 'bg-primary text-black' : 'text-gray-500 hover:text-white'
              }`}
          >
            SENTIMENT-ENHANCED
          </button>
        </div>
      </div>

      <div className="grid lg:grid-cols-12 gap-10">
        {/* Selector Panel */}
        <div className="lg:col-span-4 space-y-8">
          <section className="bg-card/40 backdrop-blur-xl border border-white/5 rounded-3xl p-8 space-y-6">
            <div className="flex items-center gap-3">
              <Settings2 className="w-5 h-5 text-primary" />
              <h2 className="text-sm font-black uppercase tracking-widest">Asset Universe</h2>
            </div>

            <div className="flex gap-2">
              <input
                type="text"
                value={input}
                onChange={e => setInput(e.target.value.toUpperCase())}
                onKeyDown={e => { if (e.key === 'Enter') addTicker() }}
                placeholder="Ticker"
                className="flex-1 bg-white/5 border-white/10 text-sm font-bold"
              />
              <button onClick={addTicker} className="p-3 bg-white/5 rounded-xl hover:bg-white/10 transition-colors">
                <Plus className="w-5 h-5 text-primary" />
              </button>
            </div>

            <div className="flex flex-wrap gap-2">
              <AnimatePresence>
                {tickers.map(t => (
                  <motion.div
                    key={t}
                    initial={{ opacity: 0, scale: 0.8 }}
                    animate={{ opacity: 1, scale: 1 }}
                    exit={{ opacity: 0, scale: 0.8 }}
                    className="flex items-center gap-2 bg-primary/10 border border-primary/20 rounded-lg pl-3 pr-1 py-1"
                  >
                    <span className="text-[10px] font-black text-primary">{t}</span>
                    <button onClick={() => removeTicker(t)} className="p-1 hover:text-danger">
                      <Trash2 className="w-3.5 h-3.5" />
                    </button>
                  </motion.div>
                ))}
              </AnimatePresence>
            </div>

            <button
              onClick={optimize}
              disabled={loading}
              className="w-full py-4 bg-primary text-black font-black uppercase tracking-[0.2em] rounded-2xl hover:scale-[1.02] active:scale-[0.98] transition-all flex items-center justify-center gap-3 disabled:opacity-50"
            >
              {loading ? <RefreshCw className="w-5 h-5 animate-spin" /> : <Play className="w-5 h-5 fill-current" />}
              Run Optimizer
            </button>
          </section>

          {error && (
            <div className="p-4 bg-danger/10 border border-danger/20 text-danger text-xs font-black rounded-2xl">
              ERROR: {error}
            </div>
          )}
        </div>

        {/* Results Panel */}
        <div className="lg:col-span-8 bg-card/40 backdrop-blur-xl border border-white/5 rounded-3xl overflow-hidden min-h-[500px] flex flex-col items-center justify-center p-10 relative">
          <AnimatePresence mode="wait">
            {!result && !loading ? (
              <motion.div
                key="empty"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="text-center space-y-4"
              >
                <div className="w-20 h-20 bg-white/5 rounded-full flex items-center justify-center mx-auto mb-6">
                  <Settings2 className="w-10 h-10 text-gray-700" />
                </div>
                <h3 className="text-xl font-bold text-gray-500">Configure Universe</h3>
                <p className="text-xs text-gray-600 font-medium max-w-[200px]">Add securities and select an optimization method to generate results.</p>
              </motion.div>
            ) : loading ? (
              <motion.div key="loading" initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="flex flex-col items-center gap-6">
                <div className="relative w-20 h-20">
                  <div className="absolute inset-0 border-4 border-primary/10 rounded-full" />
                  <div className="absolute inset-0 border-4 border-primary border-t-white rounded-full animate-spin" />
                </div>
                <p className="text-xs font-black uppercase tracking-[0.2em] text-primary/60">Solving Frontiers</p>
              </motion.div>
            ) : (
              <motion.div
                key="result"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="w-full grid md:grid-cols-2 gap-12 items-center"
              >
                <div className="h-[350px] relative">
                  <canvas ref={pieRef} />
                  <div className="absolute inset-0 flex items-center justify-center flex-col pointer-events-none">
                    <span className="text-xs font-black text-gray-500 uppercase">Sharpe</span>
                    <span className="text-3xl font-black text-white">{result.sharpe_ratio?.toFixed(2)}</span>
                  </div>
                </div>

                <div className="space-y-6">
                  <div className="flex items-center gap-3 mb-4">
                    <Info className="w-5 h-5 text-primary" />
                    <h3 className="text-sm font-black uppercase tracking-widest underline decoration-primary/30 underline-offset-4">Allocation Details</h3>
                  </div>

                  <div className="space-y-3">
                    {Object.entries(result.allocation).map(([t, w], i) => (
                      <div key={t} className="flex items-center justify-between p-4 bg-white/[0.03] border border-white/5 rounded-2xl hover:border-white/10 transition-colors">
                        <span className="font-black text-sm">{t}</span>
                        <span className="font-mono text-primary font-bold">{(w * 100).toFixed(1)}%</span>
                      </div>
                    ))}
                  </div>

                  <button className="flex items-center gap-2 text-[10px] font-black uppercase tracking-widest text-primary hover:text-white transition-colors pt-4">
                    <Download className="w-4 h-4" /> Download Report PDF
                  </button>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </div>
    </div>
  )
}
