# Sentiment-Driven Portfolio Optimization System

A comprehensive Python-based framework that integrates Financial News Sentiment Analysis with Modern Portfolio Theory to build risk-optimized investment portfolios.

## 🚀 Features

- **Sentiment Analysis Pipeline**: 
  - Text preprocessing (cleaning, lemmatization)
  - TF-IDF Vectorization
  - Machine Learning Classification (Logistic Regression, SVM)
  - Daily Sentiment Aggregation
- **Return Prediction**: 
  - Feature Engineering (RSI, Moving Averages, Volatility)
  - Predictive Modeling (Random Forest, Gradient Boosting)
- **Portfolio Optimization**: 
  - Mean-Variance Optimization (Markowitz)
  - **Sentiment-Enhanced Optimization** (Black-Litterman inspired)
- **Evaluation & Visualization**: 
  - Walk-forward Backtesting
  - Performance Metrics (Sharpe, Sortino, Drawdowns)
  - Interactive **Streamlit Dashboard**

## 📂 Project Structure

```
src/
├── data_collection/        # Stock & News data loaders
├── preprocessing/          # Text cleaning & Feature engineering
├── sentiment_analysis/     # Classifier & Aggregator models
├── portfolio_optimization/ # Mean-Variance & Sentiment Optimizers
├── evaluation/             # Backtester & Performance Analyzer
└── visualization/          # Charts & Dashboard
```

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd sentiport
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   *Note: Ensure you have Python 3.8+ installed.*

3. **Download NLTK data** (First run only):
   ```python
   import nltk
   nltk.download('stopwords')
   nltk.download('wordnet')
   ```

## 📊 Usage

### Interactive Dashboard
The easiest way to explore the system is via the dashboard:

```bash
streamlit run src/visualization/dashboard.py
```

Features:
- **Data Explorer**: View historical stock prices.
- **Sentiment Analysis**: Analyze sentiment trends for specific tickers.
- **Backtest**: Run simulations comparing Equal-Weight, Max-Sharpe, and Sentiment-Enhanced strategies.

### Library Usage

```python
from src.sentiment_analysis.aggregator import SentimentAggregator
from src.portfolio_optimization.sentiment_optimizer import SentimentEnhancedOptimizer

# 1. Get Daily Sentiment
aggregator = SentimentAggregator(...)
daily_scores = aggregator.process_headlines(news_df)

# 2. Optimize Portfolio
optimizer = SentimentEnhancedOptimizer()
weights = optimizer.optimize(expected_returns, cov_matrix, sentiment_scores=daily_scores)
```

## 🧪 Verification

To run the end-to-end system verification script:

```bash
python scripts/verify_full_system.py
```

## 📈 Results

The system aims to demonstrate that incorporating sentiment signals can improve risk-adjusted returns (Sharpe Ratio) by dynamically adjusting portfolio weights based on market news tone.

## License

MIT License
