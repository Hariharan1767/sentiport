# Sentiport - Windows Deployment Guide

## 🚀 Quick Start (2 Options)

### Option A: Start Everything with One Click
```bash
start_all.bat
```
This will open two windows automatically:
- **Window 1**: API Server on http://localhost:5000
- **Window 2**: Frontend Dev on http://localhost:5173

### Option B: Start Separately
**Terminal 1 - API Server:**
```bash
start_api.bat
```
Access: http://localhost:5000

**Terminal 2 - Frontend (in another terminal):**
```bash
start_frontend.bat
```
Access: http://localhost:5173

---

## ✅ Verify Deployment

### Check API Health
```bash
curl http://localhost:5000/api/health
```

Should return:
```json
{
  "status": "healthy",
  "timestamp": "2024-02-07T10:30:00",
  "version": "1.0.0"
}
```

### Open in Browser
- **Frontend UI**: http://localhost:5173
- **API Server**: http://localhost:5000
- **API Health**: http://localhost:5000/api/health

---

## 📋 Prerequisites Check

Before starting, ensure you have:
- ✅ Python 3.8+ installed
- ✅ Node.js 16+ installed
- ✅ Virtual environment created (`.venv` folder)
- ✅ Dependencies installed

### If Virtual Environment Missing:
```bash
python -m venv .venv
```

### If Dependencies Missing:
```bash
.venv\Scripts\python.exe -m pip install -r requirements.txt
npm install
```

---

## 🎯 Usage

### Accessing the Application

**Frontend** (User Interface):
```
http://localhost:5173
```

Features available:
- 📊 Stock Dashboard
- 📈 Technical & Fundamental Analysis
- 💭 Sentiment Analysis
- 🎯 Portfolio Optimization
- 📉 Backtesting

### API Endpoints

Base URL: `http://localhost:5000/api`

```
GET    /health                    - System health check
GET    /status                    - Component status
POST   /stocks/data               - Get stock price data
POST   /stocks/news               - Analyze news sentiment
POST   /analysis/comprehensive    - Multi-factor stock analysis
POST   /portfolio/optimize        - Optimize portfolio
POST   /portfolio/backtest        - Backtest strategy
POST   /predict/investment        - Get buy/sell recommendation
```

---

## 🛑 Stopping Services

Simply close the terminal windows or press **Ctrl+C** in each.

---

## 🔧 Troubleshooting

### Port Already in Use

**Port 5000 (API):**
```bash
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

**Port 5173 (Frontend):**
```bash
netstat -ano | findstr :5173
taskkill /PID <PID> /F
```

### Python Not Found
Make sure virtual environment is activated:
```bash
.venv\Scripts\activate.bat
python --version
```

### npm Not Found
Install Node.js from: https://nodejs.org/

### Dependencies Missing
```bash
.venv\Scripts\python.exe -m pip install -r requirements.txt
npm install
```

### API Returns Error 500
Check the API window for error messages. Common issues:
- Stock ticker doesn't exist
- Network connection problem
- Missing NLTK data

---

## 📚 Full Documentation

For more details, see:
- [DEPLOYMENT.md](DEPLOYMENT.md) - Comprehensive deployment guide
- [QUICKSTART.md](QUICKSTART.md) - Quick reference
- [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) - Project overview

---

## 💡 Tips

1. **Keep both terminals open** - API and Frontend need to run simultaneously
2. **Monitor the API window** - Shows real-time logs and any errors
3. **Check browser console** - Frontend errors appear in DevTools (F12)
4. **API logs show details** - Watch API terminal for debugging

---

## 🎓 Example API Calls

### Get Stock Data
```bash
curl -X POST http://localhost:5000/api/stocks/data ^
  -H "Content-Type: application/json" ^
  -d "{\"ticker\": \"AAPL\", \"period\": \"1y\"}"
```

### Analyze Stock
```bash
curl -X POST http://localhost:5000/api/analysis/comprehensive ^
  -H "Content-Type: application/json" ^
  -d "{\"ticker\": \"AAPL\"}"
```

### Get Recommendation
```bash
curl -X POST http://localhost:5000/api/predict/investment ^
  -H "Content-Type: application/json" ^
  -d "{\"ticker\": \"AAPL\"}"
```

---

## 📊 System Architecture

```
User Browser (http://localhost:5173)
        ↓
    React Frontend
        ↓ (API calls)
Flask API Server (http://localhost:5000)
        ↓
Python Modules:
  - Sentiment Analysis
  - Technical Analysis
  - Portfolio Optimization
  - Data Collection
        ↓
External APIs:
  - yfinance (stock data)
  - News sources (sentiment)
```

---

**Version**: 1.0.0
**Status**: Ready to Deploy ✅
**Date**: February 2024
