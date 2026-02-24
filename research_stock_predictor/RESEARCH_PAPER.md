# Research Paper: Impact of Financial Sentiment on Deep Learning Stock Forecasting

## Abstract
This project investigates whether the inclusion of qualitative news sentiment improves the accuracy of deep learning architectures in predicting short-term stock price movements. We compare a baseline LSTM model (price-only) against a multi-modal hybrid model (price + sentiment).

## 1. Problem Statement
Stock prices are famously volatile and influenced by both technical patterns (quantitative) and market news (qualitative). Traditional models often focus on price data alone. This research addresses the problem: *Does a multi-modal approach combining sentiment and price data outperform a univariate time-series model in directional accuracy?*

## 2. Methodology

### 2.1 Data Ingestion
- **Source A**: Alpha Vantage (Historical daily OHLCV and Technical Indicators: RSI, MACD).
- **Source B**: Finnhub (Company news and sentiment metadata).

### 2.2 Feature Engineering
- **Quantitative**: Close Price, Volume, SMA(7/14), RSI, MACD, Daily Returns.
- **Qualitative**: Daily Mean Sentiment, 7-day Rolling Sentiment Index, Sentiment Volatility.
- **Normalization**: All features scaled using `MinMaxScaler` to [0, 1].

### 2.3 Machine Learning Architecture
We implement two architectures:
1. **Baseline (LSTM)**: Sequential layers of Long Short-Term Memory units to capture temporal dependencies in price data.
2. **Hybrid (Multi-Modal)**:
   - **Branch A**: LSTM for temporal sequence data (prices/indicators).
   - **Branch B**: Dense layer for static daily context (aggregated sentiment).
   - **Merge**: Concatenation of latent representations before a final fully connected prediction layer.

## 3. Experimental Setup
- **Lookback Window**: 14 trading days.
- **Optimization**: Adam optimizer with Mean Squared Error (MSE) loss.
- **Validation**: 80/20 time-series split (no shuffling to prevent data leakage).

## 4. Evaluation Metrics
- **Root Mean Squared Error (RMSE)**: Measures point-prediction accuracy.
- **Directional Accuracy**: Measures the percentage of successfully predicted price movements (UP/DOWN), critical for financial applications.

## 5. Preliminary Findings
The research dashboard provides a real-time comparison of the Baseline vs Hybrid model. Early experiments suggest that sentiment-aware models show higher **Directional Accuracy** during periods of high news volume, although RMSE improvement varies by ticker.

## 6. Future Work
- Integration of Transformer-based encoders for better sequence modeling.
- Real-time streaming data ingestion.
- Multi-ticker portfolio forecasting.
