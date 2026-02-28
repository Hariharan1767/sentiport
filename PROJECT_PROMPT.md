# SentiPort: Comprehensive Project Prompt

## 🎯 Project Overview

**SentiPort** is a sophisticated, production-ready financial analysis and portfolio optimization system that combines sentiment analysis from financial news with quantitative financial metrics to deliver intelligent investment recommendations and portfolio optimization strategies.

This is a **full-stack application** consisting of:
- **Backend**: Python-based data processing, ML models, and API services
- **Frontend**: React-based interactive dashboard with real-time visualizations
- **Research Module**: Streamlit-based deep learning prediction system
- **Deployment**: Docker containerization for cloud deployment

---

## 🏗️ Architecture Overview

### Technology Stack

**Backend (Python)**:
- Flask >= 3.0.0 - REST API server
- scikit-learn 1.3.2 - ML models (Sentiment Classification, Ensemble Learning)
- pandas 2.1.3 - Data manipulation and time-series analysis
- numpy 1.24.3 - Numerical computations
- NLTK 3.8.1 - Natural language processing
- yfinance 0.2.32 - Stock price data collection
- CVXPY 1.3.2 - Portfolio optimization (convex optimization)
- Plotly 5.17.0 - Interactive charts
- Streamlit 1.29.0 - Research dashboard

**Frontend (JavaScript/React)**:
- React 18.2.0 - UI framework
- Vite 5.0.8 - Build tool and dev server
- TailwindCSS 3.3.6 - Styling
- Chart.js 4.4.1 + react-chartjs-2 - Data visualization
- Axios 1.6.2 - HTTP client
- Framer Motion 10.16.4 - Animations

**Deployment**:
- Docker - Container orchestration
- Docker Compose - Multi-container coordination
- Nginx - Reverse proxy and static content serving
- Gunicorn 21.2.0 - Production WSGI server

---

## 📋 Core Modules & Components

### 1. Data Collection Layer (`src/backend/data_collection/`)

**Purpose**: Collect and consolidate financial data from multiple sources

**Key Components**:
- `stock_data.py` - Downloads historical OHLCV (Open, High, Low, Close, Volume) data using yfinance
- `sentiment_data.py` - Retrieves financial news headlines and metadata
- `comprehensive_data.py` - Unified interface to fetch and cache all required data

**Data Sources**:
- Yahoo Finance/yfinance: Historical stock prices, volume, technical indicators (SMA, RSI, MACD)
- Alpha Vantage: Time-series stock data, technical indicators
- Finnhub: Real-time company news, sentiment metadata
- External News APIs: Financial headlines and sentiment labels

**Configuration** (from `config/config.yaml`):
```yaml
tickers: [AAPL, GOOGL, AMZN, MSFT, TSLA, META, NVDA, JPM]
start_date: "2019-01-01"
end_date: "2024-12-31"
data_source: "yahoo_finance"
interval: "1d" (daily data)
```

---

### 2. Preprocessing & Feature Engineering (`src/backend/preprocessing/`)

**Purpose**: Clean raw text and engineer quantitative/qualitative features

**Key Components**:
- `text_cleaner.py` - Text preprocessing pipeline:
  - Lowercase conversion
  - URL/email removal
  - Special character removal
  - Stop word removal (NLTK)
  - Lemmatization
  - Min word length filtering (3 chars)
  - Number removal

- `feature_engineering.py` - Creates features for ML models:
  - **Quantitative Features**:
    - Lagged returns (1, 3, 5, 10-day windows)
    - Moving averages (SMA 7, 14, 30, 50 days)
    - RSI (Relative Strength Index)
    - MACD (Moving Average Convergence Divergence)
    - Volatility (rolling standard deviation)
    - Volume moving average
  
  - **Qualitative Features**:
    - Daily mean sentiment score
    - 7-day rolling sentiment index
    - Sentiment volatility
    - News volume per day

**Configuration** (from `config/config.yaml`):
```yaml
preprocessing:
  lowercase: true
  remove_urls: true
  lemmatization: true
  min_word_length: 3

vectorizer:
  type: "tfidf"
  max_features: 5000
  ngram_range: [1, 2]
  min_df: 2
  max_df: 0.95
```

---

### 3. Sentiment Analysis (`src/backend/sentiment_analysis/`)

**Purpose**: Classify financial news sentiment and aggregate daily sentiment scores

**Key Components**:

#### `classifier.py` - Sentiment Classification
- **Supported Models**:
  - Logistic Regression (default) - Fast, interpretable, suitable for initial experiments
  - Naive Bayes - Probabilistic, good baseline
  - Linear SVM - Powerful, good for high-dimensional text data
  
- **Pipeline**:
  1. TF-IDF Vectorization (up to 5000 features, 1-2 character n-grams)
  2. Feature scaling and normalization
  3. Binary classification: Positive (1) / Negative (0) sentiment
  
- **Training Configuration**:
  - Train/Test split: 80/20
  - Cross-validation: 5-fold stratified
  - Optional GridSearchCV for hyperparameter tuning
  - Metrics: Accuracy, Precision, Recall, F1-Score

- **Methods**:
  ```python
  train(texts, labels)           # Train classifier on labeled data
  predict(texts)                 # Predict sentiment for new texts
  predict_proba(texts)           # Get probability scores
  evaluate(texts, labels)        # Get classification metrics
  save(path)                     # Persist model to disk
  load(path)                     # Load trained model
  ```

#### `aggregator.py` - Sentiment Aggregation
- Aggregates individual news sentiment into daily portfolio sentiment scores
- Aggregation methods:
  - Mean sentiment
  - Weighted mean (by relevance/authority)
  - Median sentiment
- Handles missing data via:
  - Forward fill (use previous day's sentiment)
  - Zero fill (neutral sentiment)
  - Last value carry-forward

- **Output**: Daily sentiment scores per ticker (range: [-1, 1] or [0, 1])

---

### 4. Financial Analysis (`src/backend/analysis/`)

**Purpose**: Perform comprehensive financial analysis across 9 factors

#### `fundamental_analysis.py`
Analyzes company fundamentals:
- P/E Ratio (Price-to-Earnings): Valuation metric
- EPS Growth: Earnings per share trend
- ROE (Return on Equity): Profitability
- Debt-to-Equity Ratio: Leverage analysis
- Operating Margin: Operational efficiency
- Free Cash Flow: Cash generation ability
- Book Value: Asset backing per share

#### `valuation_analysis.py` (Embedded in Fundamental)
- P/E Ratio comparison to industry average
- Price-to-Book ratio
- Price-to-Sales ratio
- PEG Ratio (P/E to growth ratio)

#### `growth_analysis.py` (Embedded)
- Revenue CAGR (5-year)
- EPS growth rate
- Earnings momentum
- Forward guidance estimates

#### `technical_analysis.py`
Technical indicators and price patterns:
- **Trend Indicators**:
  - Moving Averages (SMA 50, 200)
  - MACD (momentum)
  - ADX (trend strength)
  
- **Oscillators**:
  - RSI (overbought/oversold)
  - Stochastic Oscillator
  - Bollinger Bands
  
- **Volume Analysis**:
  - Volume moving average
  - On-Balance Volume (OBV)
  - Volume Rate of Change

#### `risk_analysis.py`
Risk metrics and stress testing:
- Beta (market risk)
- Standard Deviation (volatility)
- Sharpe Ratio (risk-adjusted return)
- Sortino Ratio (downside risk-adjusted return)
- Value at Risk (VaR) - 95th percentile
- Maximum Drawdown
- Correlation analysis (with market and sectors)

#### `qualitative_analysis.py`
Qualitative factors:
- Management quality assessment
- Competitive advantage/moat strength
- Industry trends and market position
- ESG (Environmental, Social, Governance) scores
- Business model quality

---

### 5. Portfolio Optimization (`src/backend/portfolio_optimization/`)

**Purpose**: Generate optimal portfolio weights using modern portfolio theory and sentiment signals

#### `mean_variance.py` - Mean-Variance Optimizer (Markowitz)
- **Objective**: Maximize Sharpe Ratio (risk-adjusted return)
- **Constraints**:
  - Portfolio weights sum to 1
  - Long-only constraints (no shorting, optional)
  - Min/max weight per asset
  - Sector concentration limits
  
- **Algorithm**: 
  - Quadratic programming with CVXPY
  - Efficient Frontier generation
  - Minimum variance portfolio
  - Maximum Sharpe Ratio portfolio
  
- **Inputs**:
  - Expected returns vector
  - Covariance matrix (from historical returns)
  
- **Outputs**:
  - Optimal weights for each asset
  - Expected portfolio return
  - Portfolio volatility (standard deviation)
  - Sharpe Ratio

#### `sentiment_optimizer.py` - Sentiment-Enhanced Optimizer
- **Enhancement Strategy**: Black-Litterman inspired approach
  - Incorporates sentiment signals as "market views"
  - Sentiment directly influences expected returns
  - More aggressive on high-sentiment assets (positive outlook)
  - Less allocation to negative sentiment assets
  
- **Logic**:
  ```
  Adjusted_Expected_Return = Historical_Return + (Sentiment_Signal × Adjustment_Factor)
  Sentiment_Signal: -1 (very negative) to +1 (very positive)
  Adjustment_Factor: Tunable parameter (e.g., 0.02 = 2% max adjustment)
  ```

#### `return_predictor.py`
Predicts expected returns using:
- Historical returns (mean)
- Growth metrics from fundamental analysis
- Sentiment trends
- Technical momentum signals

#### `risk_estimator.py`
Estimates portfolio risk:
- Returns covariance matrix calculation
- Asset correlation analysis
- Portfolio volatility computation
- Stress scenario analysis

---

### 6. Evaluation & Backtesting (`src/backend/evaluation/`)

**Purpose**: Validate strategy performance against historical data

#### `backtester.py` - Walk-Forward Backtesting
- **Methodology**:
  - Split historical period into overlapping windows
  - Training period: 2 years, test period: 6 months (sliding window)
  - Rebalance quarterly to maintain target weights
  
- **Strategies Compared**:
  1. **Equal-Weight Baseline**: 1/n allocation to all assets
  2. **Mean-Variance Optimal**: Markowitz optimization
  3. **Sentiment-Enhanced**: Mean-Variance + sentiment signals
  
- **Metrics Calculated**:
  - Cumulative return
  - Annual return
  - Annual volatility
  - Sharpe Ratio
  - Sortino Ratio
  - Maximum Drawdown
  - Win rate (% months with positive returns)
  - Average Monthly Return

#### `performance_analyzer.py`
Analyzes and compares strategy results:
- Statistical significance testing
- Performance attribution (return contribution from each factor)
- Stress testing under market downturns
- Comparison tables and rankings

#### `sentiment_impact.py`
Isolates sentiment's contribution:
- Difference between sentiment-enhanced and mean-variance returns
- Correlation between sentiment signals and actual returns
- Sentiment regime analysis (high/medium/low news volume periods)

---

### 7. Prediction & Orchestration (`src/backend/prediction/`)

**Purpose**: Coordinate analysis and provide investment recommendations

#### `orchestrator.py` - Stock Analysis Orchestrator
Runs end-to-end analysis pipeline:
1. Fetch comprehensive data
2. Engineer features
3. Analyze fundamental, technical, qualitative factors
4. Aggregate results into 9-factor scorecard
5. Generate investment decision

#### `stock_predictor.py` - Investment Decision Engine
- **9-Factor Scorecard** (All normalized to 0-100 scale):
  1. **Fundamental Score** (weight: 2.0)
     - Health of earnings, cash flow, profitability
  2. **Valuation Score** (weight: 1.5)
     - Current price attractiveness
  3. **Growth Score** (weight: 1.5)
     - Future growth potential
  4. **Technical Score** (weight: 1.0)
     - Price chart patterns and momentum
  5. **Risk Score** (weight: 1.5)
     - Volatility, beta, downside protection
  6. **Business Score** (weight: 1.0)
     - Competitive advantage and moat
  7. **Management Score** (weight: 1.0)
     - Leadership quality and governance
  8. **Sentiment Score** (weight: 1.0)
     - News sentiment and market perception
  9. **Macro Score** (weight: 0.5)
     - Industry and sector trends

- **Decision Logic** (Weighted Ensemble):
  ```
  Total Score = Σ(Factor_Score × Weight)
  Confidence = Total Score / Maximum Possible Score
  
  IF Confidence >= 0.60: "INVEST" (Strong Buy)
  ELSE: "WAIT/AVOID" (Hold/Sell)
  ```

- **Output**:
  ```json
  {
    "ticker": "AAPL",
    "decision": "INVEST",
    "confidence_score": 0.78,
    "total_weighted_score": 234.5,
    "rating": "Strong Buy",
    "factor_scores": {
      "fundamental": 85,
      "valuation": 72,
      "growth": 88,
      "technical": 65,
      "risk": 78,
      "business": 90,
      "management": 85,
      "sentiment": 75,
      "macro": 70
    },
    "score_breakdown": { ... },
    "recommendation_reasons": [ ... ]
  }
  ```

---

### 8. Visualization (`src/backend/visualization/`)

**Purpose**: Present insights via interactive dashboards

#### `dashboard.py` - Streamlit Dashboard (Research Grade)
Interactive application with multiple pages:

1. **Data Explorer**:
   - Historical stock price charts
   - Volume analysis
   - Date range selection
   - Multi-ticker comparison

2. **Sentiment Analysis**:
   - Daily sentiment time-series
   - Sentiment heatmaps by ticker
   - News headline viewer
   - Sentiment distribution statistics

3. **Backtest Results**:
   - Performance comparison charts (3 strategies)
   - Cumulative return plots
   - Drawdown analysis
   - Monthly return heatmaps
   - Period-by-period statistics

4. **Portfolio Optimization**:
   - Efficient frontier visualization
   - Optimal portfolio weights pie chart
   - Risk-return scatter plot
   - Sensitivity analysis
   - Rebalancing recommendations

5. **Model Performance**:
   - Sentiment classifier metrics
   - Confusion matrix
   - Feature importance
   - Model comparison

#### `charts.py` - Chart Generation
Utilities for creating:
- Time-series line charts (prices, sentiment)
- Bar charts (comparisons)
- Pie charts (portfolio allocation)
- Scatter plots (risk-return)
- Heatmaps (correlations, returns)

#### `analysis_ui.py` - Web-Based UI
React-based dashboard with components for:
- Stock research interface
- Portfolio builder
- Backtesting setup and results
- Risk analysis tools
- Comparative analysis

---

### 9. API Endpoints (`api_server.py`)

**Purpose**: Expose functionality via REST API for frontend consumption

#### Health & Status
- `GET /api/health` - System health check

#### Data Endpoints
- `GET /api/data/stock-prices/<ticker>` - Historical OHLCV data
- `GET /api/data/sentiment/<ticker>` - Daily sentiment scores
- `GET /api/data/comprehensive/<ticker>` - All combined data

#### Analysis Endpoints
- `POST /api/analysis/sentiment` - Classify sentiment for texts
- `POST /api/analysis/comprehensive` - Run full analysis on ticker
- `GET /api/analysis/<ticker>` - Retrieve cached analysis results
- `POST /api/analysis/compare` - Compare multiple tickers

#### Portfolio Optimization
- `POST /api/optimize/mean-variance` - Optimize portfolio (Markowitz)
- `POST /api/optimize/sentiment-enhanced` - Optimize with sentiment
- `GET /api/efficient-frontier` - Efficient frontier data

#### Backtesting
- `POST /api/backtest/run` - Run backtest
- `GET /api/backtest/results/<test_id>` - Retrieve results
- `POST /api/backtest/compare` - Compare strategy results

#### Predictions & Recommendations
- `GET /api/predict/<ticker>` - Get investment recommendation
- `POST /api/predict/portfolio` - Score entire portfolio
- `GET /api/watchlist/score` - Score watchlist

---

## 🔄 Data Flow Architecture

### End-to-End Analysis Pipeline

```
1. DATA INGESTION
   ├── Fetch stock prices (Yahoo Finance)
   ├── Fetch financial news (Finnhub/Alpha Vantage)
   └── Cache results (local CSV)

2. RAW DATA STORAGE
   ├── data/raw/stock_prices.csv
   ├── data/raw/sentiment_news.csv
   └── data/raw/technical_indicators.csv

3. PREPROCESSING
   ├── Text cleaning (remove URLs, lemmatize, etc.)
   ├── Feature engineering (lagged returns, moving averages)
   ├── Normalization (MinMaxScaler to [0,1])
   └── Handle missing data (forward fill, interpolation)

4. SENTIMENT ANALYSIS
   ├── TF-IDF vectorization of news text
   ├── ML classification (Logistic Regression)
   └── Probability → [-1, 1] sentiment score

5. SENTIMENT AGGREGATION
   ├── Group news by day/ticker
   ├── Compute mean/median sentiment
   └── Generate daily_sentiment.csv

6. FINANCIAL ANALYSIS (Parallel)
   ├── Fundamental Analysis
   │  ├── P/E, EPS Growth, ROE, Debt-to-Equity
   │  └── FCF, Operating Margin, Book Value
   │
   ├── Technical Analysis
   │  ├── Moving Averages, RSI, MACD, ADX
   │  └── Volume indicators
   │
   ├── Risk Analysis
   │  ├── Beta, Volatility, Sharpe Ratio
   │  ├── VaR, Maximum Drawdown
   │  └── Correlation matrix
   │
   ├── Qualitative Analysis
   │  ├── Management quality
   │  ├── Competitive moat
   │  └── Industry trends
   │
   └── Growth Analysis
      ├── Revenue CAGR
      ├── EPS growth
      └── Earnings momentum

7. PREDICTOR (Stock Predictor)
   ├── Aggregate 9 factor scores
   ├── Apply weighted ensemble
   ├── Generate confidence score
   └── Decision: INVEST vs WAIT/AVOID

8. PORTFOLIO OPTIMIZATION
   ├── Mean-Variance Optimizer
   │  ├── Input: Expected returns, covariance
   │  ├── Maximize Sharpe Ratio
   │  └── Output: Optimal weights
   │
   └── Sentiment-Enhanced Optimizer
      ├── Adjust returns by sentiment signals
      ├── Optimize adjusted returns
      └── Output: Sentiment-aware weights

9. EVALUATION (Backtesting)
   ├── Walk-forward test (2yr train, 6mo test)
   ├── Compare 3 strategies
   ├── Calculate metrics (Sharpe, Sortino, Drawdown)
   └── Generate performance report

10. VISUALIZATION
    ├── Charts: prices, sentiment, allocations
    ├── Tables: metrics, comparisons
    ├── Dashboards: research (Streamlit), web (React)
    └── Export: PDF reports, CSV results
```

---

## 📊 Configuration Deep Dive (`config/config.yaml`)

### Key Configuration Sections

#### 1. Data Collection
```yaml
data_collection:
  tickers: [AAPL, GOOGL, AMZN, MSFT, TSLA, META, NVDA, JPM]
  start_date: "2019-01-01"
  end_date: "2024-12-31"
  data_source: "yahoo_finance"
  interval: "1d"  # Daily
  stock_prices_path: "data/raw/stock_prices.csv"
  sentiment_path: "data/raw/sentiment_news.csv"
```

#### 2. Sentiment Analysis
```yaml
sentiment_analysis:
  preprocessing:
    lowercase: true
    remove_urls: true
    remove_stopwords: true
    lemmatization: true
  
  vectorizer:
    type: "tfidf"
    max_features: 5000
    ngram_range: [1, 2]
  
  model:
    type: "logistic_regression"
    hyperparameters:
      C: 1.0
      max_iter: 1000
  
  training:
    test_size: 0.2
    cv_folds: 5
    stratified: true
```

#### 3. Portfolio Optimization
```yaml
portfolio_optimization:
  method: "mean_variance"  # or "sentiment_enhanced"
  constraints:
    min_weight: 0.0
    max_weight: 0.25  # 25% max per asset
    sector_limits: [0.4, 0.4, 0.2]  # Sector concentration caps
  
  rebalance_frequency: "quarterly"
  risk_free_rate: 0.04  # 4% annual
```

#### 4. Backtesting
```yaml
backtesting:
  train_period: 730  # 2 years in days
  test_period: 180   # 6 months in days
  step: 30           # Monthly rebalancing
  
  strategies:
    - equal_weight
    - mean_variance
    - sentiment_enhanced
  
  metrics:
    - cumulative_return
    - annual_return
    - sharpe_ratio
    - sortino_ratio
    - max_drawdown
```

---

## 🔄 Workflow Examples

### Example 1: Single Stock Analysis

```python
from src.backend.prediction.orchestrator import StockAnalysisOrchestrator

# Initialize orchestrator
orchestrator = StockAnalysisOrchestrator()

# Analyze single stock
result = orchestrator.analyze_stock('AAPL')

# Access recommendation
print(result['decision'])          # "INVEST"
print(result['confidence_score'])  # 0.78
print(result['factor_scores'])     # 9 scores breakdown
print(result['reasons'])           # Bullet points
```

**Output Structure**:
```json
{
  "ticker": "AAPL",
  "decision": "INVEST",
  "confidence_score": 0.78,
  "rating": "Strong Buy",
  "factor_scores": {
    "fundamental": 85,
    "valuation": 72,
    "growth": 88,
    "technical": 65,
    "risk": 78,
    "business": 90,
    "management": 85,
    "sentiment": 75,
    "macro": 70
  },
  "recommendation_reasons": [
    "Strong earnings growth (25% YoY)",
    "Positive sentiment trend (+15% vs 1mo ago)",
    "Technical momentum above 200-day MA"
  ]
}
```

---

### Example 2: Portfolio Optimization

```python
from src.backend.portfolio_optimization.sentiment_optimizer import SentimentEnhancedOptimizer
import pandas as pd

# Prepare inputs
tickers = ['AAPL', 'GOOGL', 'AMZN', 'MSFT']
historical_returns = ...  # DataFrame, shape (252, 4)
sentiment_scores = ...    # DataFrame, shape (252, 4) with values in [-1, 1]

# Initialize optimizer
optimizer = SentimentEnhancedOptimizer()

# Optimize
weights = optimizer.optimize(
    expected_returns=historical_returns.mean(),
    cov_matrix=historical_returns.cov(),
    sentiment_scores=sentiment_scores.mean(),
    adjustment_factor=0.02  # 2% max sentiment adjustment
)

print(weights)  # [0.15, 0.35, 0.25, 0.25] for [AAPL, GOOGL, AMZN, MSFT]
```

---

### Example 3: Backtesting Strategy

```python
from src.backend.evaluation.backtester import Backtester

backtester = Backtester(
    tickers=['AAPL', 'GOOGL', 'AMZN', 'MSFT'],
    start_date='2019-01-01',
    end_date='2023-12-31',
    train_period=730,  # 2 years
    test_period=180    # 6 months
)

results = backtester.run_walk_forward(
    strategies=['equal_weight', 'mean_variance', 'sentiment_enhanced']
)

# results[strategy_name] = {
#   'cumulative_return': 0.45,
#   'annual_return': 0.08,
#   'sharpe_ratio': 1.23,
#   'sortino_ratio': 1.87,
#   'max_drawdown': -0.18,
#   'portfolio_values': time-series,
#   'returns': daily returns
# }

print(results['sentiment_enhanced']['sharpe_ratio'])  # 1.23
```

---

## 📈 Key Research Questions

The project addresses these hypotheses:

1. **Does Sentiment Improve Returns?**
   - Benchmark: Mean-Variance portfolio
   - Test: Sentiment-Enhanced portfolio
   - Metric: Sharpe Ratio improvement

2. **What's the Optimal Sentiment Adjustment?**
   - Vary adjustment_factor from 0.01 to 0.05
   - Measure impact on risk-adjusted returns
   - Find sweet spot (not too aggressive, not too conservative)

3. **In What Market Conditions is Sentiment Most Valuable?**
   - High news volume periods (earnings season)
   - Market stress periods (drawdowns)
   - Stable periods (sideways markets)

4. **How Do Factor Scores Correlate with Returns?**
   - Analyze causality vs coincidence
   - Identify leading vs lagging indicators

---

## 🚀 Deployment Architecture

### Development (Local)

```
Frontend (Vite)          Backend (Flask)          Research (Streamlit)
localhost:5173    <-->   localhost:5000    <-->   localhost:8501
   React                 Python API              Dashboard
   Components            REST endpoints          Interactive
```

**Run Commands**:
```bash
# Backend
python api_server.py

# Frontend
npm run dev

# Research Dashboard
streamlit run research_stock_predictor/app/main.py
```

### Production (Docker)

```
External User
    |
    v
Nginx (Reverse Proxy, port 80/443)
    |
    +---> Flask Backend (port 5000, Gunicorn)
    |
    +---> React Frontend (port 5173, static files)
    |
    +---> Streamlit Dashboard (port 8501, optional)

All containerized in Docker with Docker Compose orchestration
```

**Dockerfile**:
- Multi-stage build (reduce image size)
- Base: Python 3.9+ with Node.js
- Stage 1: Build React frontend (npm build)
- Stage 2: Install Python dependencies
- Stage 3: Runtime container with Gunicorn + Nginx

**docker-compose.yml**:
- Service: backend (Flask + Gunicorn)
- Service: frontend (Nginx serving React)
- Service: research (Streamlit)
- Service: proxy (Nginx reverse proxy)
- Volume: `data/` for persistence

---

## 🧪 Testing & Validation

### Test Modules (`tests/`)

1. **test_analysis.py**
   - Unit tests for each analyzer class
   - Integration tests for orchestrator
   - Mock data for reproducibility

2. **test_deployment.py**
   - API endpoint tests
   - Response validation
   - Error handling tests

3. **Verification Scripts** (`scripts/`)
   - `verify_full_system.py` - End-to-end validation
   - `verify_9factor_system.py` - 9-factor calculation verification

---

## 📝 Key File Locations & Purposes

| File | Purpose |
|------|---------|
| `api_server.py` | Main Flask API server (539 lines) |
| `src/backend/prediction/orchestrator.py` | Pipeline orchestrator |
| `src/backend/prediction/stock_predictor.py` | 9-factor decision engine |
| `src/backend/sentiment_analysis/classifier.py` | ML sentiment classifier |
| `src/backend/sentiment_analysis/aggregator.py` | Daily sentiment aggregation |
| `src/backend/portfolio_optimization/sentiment_optimizer.py` | Sentiment-enhanced portfolio optimization |
| `src/backend/evaluation/backtester.py` | Walk-forward backtesting |
| `src/backend/visualization/dashboard.py` | Streamlit dashboard |
| `src/frontend/App.jsx` | React main application |
| `config/config.yaml` | Central configuration (375 lines) |
| `research_stock_predictor/app/main.py` | Streamlit research dashboard |

---

## 🎓 Educational Value

This project demonstrates:

1. **Software Architecture**:
   - Modular design with clear separation of concerns
   - Pipeline pattern for data processing
   - MVC-style separation (backend services, API layer, frontend UI)

2. **Machine Learning in Finance**:
   - Sentiment analysis pipeline (NLP)
   - Ensemble learning (9-factor weighted system)
   - Financial metrics and indicators

3. **Modern Portfolio Theory**:
   - Markowitz mean-variance optimization
   - Sharpe ratio maximization
   - Efficient frontier concepts

4. **Web Technology Stack**:
   - Python backend (Flask, scikit-learn, pandas)
   - JavaScript frontend (React, Vite, TailwindCSS)
   - Containerization (Docker)

5. **Financial Domain Knowledge**:
   - Technical analysis (RSI, MACD, moving averages)
   - Fundamental analysis (P/E, ROE, FCF)
   - Risk metrics (Sharpe ratio, Sortino ratio, max drawdown)
   - Portfolio optimization and rebalancing

---

## 🔐 Security Considerations

1. **API Keys**: Store in `.env` file (not committed)
2. **CORS**: Configured in Flask for frontend communication
3. **Data Validation**: Input validation on all endpoints
4. **Error Handling**: Try-catch blocks prevent crashes and info leaks
5. **Frontend**: No sensitive data in local storage (only UI state)

---

## 🎯 Future Enhancements

1. **Real-Time Predictions**:
   - WebSocket integration for live sentiment feed
   - Streaming price updates

2. **Advanced NLP**:
   - BERT/Transformer-based sentiment classification
   - Multi-language support
   - Entity extraction (extract stock mentions from news)

3. **Deep Learning**:
   - LSTM/GRU models for time-series prediction
   - Attention mechanisms for feature importance
   - Reinforcement learning for dynamic portfolio allocation

4. **Advanced Optimization**:
   - Risk parity allocation
   - Hierarchical risk parity
   - Genetic algorithms for hyperparameter tuning

5. **Scalability**:
   - Redis caching for faster data retrieval
   - Celery task queues for async processing
   - Distributed backtesting across multiple machines

6. **Risk Management**:
   - Options hedging strategies
   - CVaR (Conditional Value at Risk) optimization
   - Stress testing under extreme scenarios

---

## 📞 Quick Reference: Key Classes & Methods

### Core Classes

```python
# Sentiment Analysis
SentimentClassifier(model_type='logistic_regression')
  .train(texts, labels)
  .predict(texts) -> [0 or 1]
  .predict_proba(texts) -> [0->1]

SentimentAggregator()
  .process_headlines(news_df) -> daily_scores

# Analysis
FundamentalAnalyzer().analyze(ticker) -> scores
TechnicalAnalyzer().analyze(ticker) -> scores
RiskAnalyzer().analyze(ticker) -> scores
QualitativeAnalyzer().analyze(ticker) -> scores

# Portfolio Optimization
MeanVarianceOptimizer().optimize(returns, cov)
SentimentEnhancedOptimizer().optimize(returns, cov, sentiment)

# Backtesting
Backtester(...).run_walk_forward(strategies)

# Prediction
StockAnalysisOrchestrator().analyze_stock(ticker)
StockPredictor().predict_invest_decision(scores)
```

---

## 📚 Documentation Files

- `README.md` - Project overview and quick start
- `DEPLOY.md` - Deployment instructions
- `research_stock_predictor/RESEARCH_PAPER.md` - Research methodology
- `config/config.yaml` - Configuration reference (375 lines)

---

**End of Comprehensive Project Prompt**

This document provides a complete understanding of SentiPort's architecture, components, data flow, configuration, and deployment model. It serves as the master reference for understanding, extending, and deploying the system.
