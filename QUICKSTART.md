# Sentiport - Quick Start Guide

## ⚡ Fast Track Deployment

### Option 1: Local Development (2 minutes)
```bash
# Activate environment
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # macOS/Linux

# Start API
python api_server.py

# In another terminal:
npm run dev
```
**Access**: http://localhost:5173

---

### Option 2: Docker (Windows) - 5 minutes
```bash
deploy.bat
```
**Access**: http://localhost

---

### Option 3: Docker (Linux/macOS) - 5 minutes
```bash
chmod +x deploy.sh
./deploy.sh
```
**Access**: http://localhost

---

## 🎯 What You Get

### Backend API (http://localhost:5000)
- `GET  /api/health` - System health
- `POST /api/stocks/data` - Stock price history
- `POST /api/stocks/news` - News sentiment
- `POST /api/analysis/comprehensive` - Multi-factor analysis
- `POST /api/portfolio/optimize` - Portfolio optimization
- `POST /api/portfolio/backtest` - Backtesting
- `POST /api/predict/investment` - Buy/Sell recommendation

### Frontend Features
- 📊 Real-time stock analysis dashboard
- 📈 Technical & fundamental analysis
- 💭 Sentiment analysis from news
- 🎯 Portfolio optimization engine
- 📉 Performance backtesting
- ⚙️ Settings & customization

---

## 📋 Pre-requisites

- **Docker + Docker Compose** (for Option 2/3)
- **Node.js 16+** (for Option 1)
- **Python 3.8+** (for Option 1)
- **4GB RAM** minimum
- **Internet connection** (for stock data)

---

## ✅ Verify Installation

```bash
# API Health Check
curl http://localhost:5000/api/health

# Should return:
# {"status": "healthy", "timestamp": "...", "version": "1.0.0"}
```

---

## 🚨 Troubleshooting

**Port 5000 already in use?**
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# macOS/Linux
lsof -i :5000
kill -9 <PID>
```

**Port 80 already in use?**
```bash
# Change port in docker-compose.yml:
# ports:
#   - "8080:80"
# Then access at http://localhost:8080
```

**API not responding?**
```bash
docker-compose logs -f api
# or
docker-compose logs -f
```

---

## 📚 Full Documentation

See [DEPLOYMENT.md](DEPLOYMENT.md) for:
- Detailed setup instructions
- Cloud deployment (AWS, GCP, Azure)
- Kubernetes deployment
- Production configuration
- Advanced troubleshooting

See [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) for:
- Complete feature overview
- Project structure
- Technology stack
- API examples

---

## 🎓 API Examples

### Get Stock Data
```bash
curl -X POST http://localhost:5000/api/stocks/data \
  -H "Content-Type: application/json" \
  -d '{"ticker": "AAPL", "period": "1y"}'
```

### Analyze Stock
```bash
curl -X POST http://localhost:5000/api/analysis/comprehensive \
  -H "Content-Type: application/json" \
  -d '{"ticker": "AAPL"}'
```

### Optimize Portfolio
```bash
curl -X POST http://localhost:5000/api/portfolio/optimize \
  -H "Content-Type: application/json" \
  -d '{
    "tickers": ["AAPL", "MSFT", "GOOGL"],
    "target_return": 0.10,
    "method": "sentiment"
  }'
```

### Get Recommendation
```bash
curl -X POST http://localhost:5000/api/predict/investment \
  -H "Content-Type: application/json" \
  -d '{"ticker": "AAPL"}'
```

---

## 🛑 Stop Services

**Docker:**
```bash
docker-compose down
```

**Local:**
```bash
# Press Ctrl+C in terminals running:
# - python api_server.py
# - npm run dev
```

---

## 📞 Need Help?

1. Check [DEPLOYMENT.md](DEPLOYMENT.md) for detailed guides
2. Review API logs: `docker-compose logs api`
3. Verify health: `curl http://localhost:5000/api/health`
4. Check requirements: Python 3.8+, Node 16+, Docker

---

**Version**: 1.0.0  
**Status**: ✅ Ready to Deploy  
**Last Updated**: February 2024
