import { useState, useEffect, useRef } from 'react'
import axios from 'axios'
import { Send, Trash2, MessageCircle } from 'lucide-react'

const API_BASE_URL = 'http://localhost:5000/api'

export default function Chatbot() {
  const [messages, setMessages] = useState([
    {
      id: 'intro',
      type: 'assistant',
      text: "👋 Hi! I'm your Stock Chatbot. Ask me anything about stocks, sentiment analysis, or portfolio optimization. Type 'help' to see what I can do!",
      timestamp: new Date()
    }
  ])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const messagesEndRef = useRef(null)

  // Auto-scroll to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const handleSendMessage = async (e) => {
    e.preventDefault()
    
    if (!input.trim()) return

    // Add user message to UI
    const userMessage = {
      id: Date.now(),
      type: 'user',
      text: input,
      timestamp: new Date()
    }
    setMessages(prev => [...prev, userMessage])
    setInput('')
    setLoading(true)
    setError(null)

    try {
      const response = await axios.post(`${API_BASE_URL}/chatbot/ask`, {
        question: input
      }, {
        timeout: 15000  // Increased timeout to 15 seconds
      })

      const assistantMessage = {
        id: Date.now() + 1,
        type: 'assistant',
        text: response.data.answer,
        timestamp: new Date(response.data.timestamp)
      }
      
      setMessages(prev => [...prev, assistantMessage])
    } catch (err) {
      const errorMsg = err.response?.data?.error || err.message || 'Failed to get response'
      setError(errorMsg)
      
      const errorMessage = {
        id: Date.now() + 1,
        type: 'assistant',
        text: `❌ Error: ${errorMsg}. Please try again or check your connection.`,
        timestamp: new Date()
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setLoading(false)
    }
  }

  const handleClear = async () => {
    if (!window.confirm('Clear conversation history?')) return

    try {
      await axios.post(`${API_BASE_URL}/chatbot/clear`)
      setMessages([
        {
          id: 'intro',
          type: 'assistant',
          text: "👋 Conversation cleared! Ask me about stocks, sentiment, or portfolio strategies.",
          timestamp: new Date()
        }
      ])
      setError(null)
    } catch (err) {
      setError('Failed to clear history')
    }
  }

  const handleQuickQuestion = async (question) => {
    setInput(question)
    // Trigger send after a brief delay to allow state update
    setTimeout(() => {
      const form = document.querySelector('form[data-chatbot-form]')
      if (form) form.dispatchEvent(new Event('submit', { bubbles: true }))
    }, 0)
  }

  const quickQuestions = [
    "What's the price of AAPL?",
    "How's the sentiment for TSLA?",
    "Compare MSFT vs AAPL",
    "How should I diversify my portfolio?"
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 pt-24 pb-12">
      <div className="max-w-4xl mx-auto px-4">
        {/* Header */}
        <div className="mb-6">
          <div className="flex items-center gap-3 mb-2">
            <MessageCircle className="w-8 h-8 text-primary" />
            <h1 className="text-4xl font-bold text-white">Stock Chatbot</h1>
          </div>
          <p className="text-gray-400">Ask anything about stocks, sentiment, and portfolio strategies</p>
        </div>

        {/* Main Chat Container */}
        <div className="bg-slate-800/50 backdrop-blur-sm border border-white/10 rounded-2xl overflow-hidden shadow-2xl flex flex-col h-[600px]">
          
          {/* Messages Area */}
          <div className="flex-1 overflow-y-auto p-6 space-y-4">
            {messages.map((msg) => (
              <div
                key={msg.id}
                className={`flex ${msg.type === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div
                  className={`max-w-xs lg:max-w-md xl:max-w-lg px-4 py-3 rounded-lg ${
                    msg.type === 'user'
                      ? 'bg-primary text-white rounded-br-none'
                      : 'bg-slate-700/50 text-gray-100 rounded-bl-none border border-white/10'
                  }`}
                >
                  <p className="text-sm break-words whitespace-pre-wrap">{msg.text}</p>
                  <span className="text-xs opacity-60 mt-1 block">
                    {msg.timestamp.toLocaleTimeString()}
                  </span>
                </div>
              </div>
            ))}
            
            {loading && (
              <div className="flex justify-start">
                <div className="bg-slate-700/50 text-gray-100 px-4 py-3 rounded-lg rounded-bl-none border border-white/10">
                  <div className="flex gap-2">
                    <div className="w-2 h-2 bg-primary rounded-full animate-bounce"></div>
                    <div className="w-2 h-2 bg-primary rounded-full animate-bounce delay-100"></div>
                    <div className="w-2 h-2 bg-primary rounded-full animate-bounce delay-200"></div>
                  </div>
                </div>
              </div>
            )}
            
            <div ref={messagesEndRef} />
          </div>

          {/* Error Message */}
          {error && (
            <div className="px-6 py-2 bg-red-900/20 border-t border-red-500/30 text-red-300 text-sm">
              {error}
            </div>
          )}

          {/* Quick Questions (show if not many messages) */}
          {messages.length <= 2 && (
            <div className="px-6 py-4 border-t border-white/10 bg-slate-700/30">
              <p className="text-xs text-gray-400 mb-3">Try asking:</p>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                {quickQuestions.map((q) => (
                  <button
                    key={q}
                    onClick={() => handleQuickQuestion(q)}
                    className="text-left text-sm px-3 py-2 bg-slate-600/50 hover:bg-primary/20 text-gray-300 hover:text-primary rounded transition-colors border border-white/10"
                  >
                    {q}
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* Input Area */}
          <form
            onSubmit={handleSendMessage}
            data-chatbot-form
            className="border-t border-white/10 bg-slate-700/20 p-4 flex gap-2"
          >
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask about stocks, sentiment, portfolio strategies..."
              className="flex-1 bg-slate-600/50 text-white placeholder-gray-400 rounded-lg px-4 py-2 border border-white/10 focus:border-primary focus:outline-none transition-colors"
              disabled={loading}
            />
            
            <button
              type="button"
              onClick={handleClear}
              className="p-2 bg-slate-600/50 hover:bg-red-600/30 text-gray-300 hover:text-red-300 rounded-lg transition-colors border border-white/10"
              title="Clear history"
            >
              <Trash2 className="w-5 h-5" />
            </button>

            <button
              type="submit"
              disabled={loading || !input.trim()}
              className="p-2 bg-primary hover:bg-primary/80 text-white rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <Send className="w-5 h-5" />
            </button>
          </form>
        </div>

        {/* Info Section */}
        <div className="mt-8 grid md:grid-cols-2 gap-6">
          <div className="bg-slate-800/30 border border-white/10 rounded-lg p-6">
            <h3 className="text-lg font-semibold text-primary mb-3">📊 Stock Analysis</h3>
            <ul className="text-sm text-gray-300 space-y-2">
              <li>✓ Current prices & price changes</li>
              <li>✓ Market sentiment analysis</li>
              <li>✓ Stock comparisons</li>
              <li>✓ Technical & fundamental data</li>
            </ul>
          </div>

          <div className="bg-slate-800/30 border border-white/10 rounded-lg p-6">
            <h3 className="text-lg font-semibold text-accent mb-3">💼 Portfolio Help</h3>
            <ul className="text-sm text-gray-300 space-y-2">
              <li>✓ Diversification strategies</li>
              <li>✓ Rebalancing guidance</li>
              <li>✓ Risk management tips</li>
              <li>✓ Asset allocation advice</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  )
}
