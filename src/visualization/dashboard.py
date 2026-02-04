"""
Interactive Dashboard using Streamlit.
"""

import streamlit as st
import pandas as pd
import numpy as np
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.data_collection.stock_data import StockDataCollector # Mock or real
from src.data_collection.sentiment_data import SentimentDataPreparer
from src.visualization.charts import ChartGenerator
from src.evaluation.backtester import Backtester

# Page Config
st.set_page_config(
    page_title="SentiPort: Sentiment Portfolio Optimizer",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Sentiment-Driven Portfolio Optimization")
st.markdown("""
This dashboard demonstrates the impact of **News Sentiment** on portfolio performance.
""")

# Sidebar
st.sidebar.header("Configuration")
selected_stocks = st.sidebar.multiselect(
    "Select Stocks",
    ['AAPL', 'GOOGL', 'AMZN', 'MSFT', 'TSLA', 'META', 'NVDA', 'JPM'],
    default=['AAPL', 'MSFT', 'TSLA']
)

date_range = st.sidebar.date_input(
    "Date Range",
    [pd.to_datetime('2023-01-01'), pd.to_datetime('2023-12-31')]
)

# Tabs
tab1, tab2, tab3 = st.tabs(["Data Explorer", "Sentiment Analysis", "Backtesting"])

@st.cache_data
def load_mock_data(tickers, start, end):
    # Mock data generator for demo purposes if real data missing
    dates = pd.date_range(start, end, freq='B')
    
    # Prices
    price_data = []
    for t in tickers:
        prices = 100 + np.cumsum(np.random.normal(0, 1, len(dates)))
        for d, p in zip(dates, prices):
            price_data.append({'Date': d, 'Ticker': t, 'Close': p})
    prices_df = pd.DataFrame(price_data)
    
    # Sentiment
    sent_data = []
    for t in tickers:
        # Random sentiment with some pattern
        regime = np.random.randint(-1, 2, len(dates) // 10)
        regime = np.repeat(regime, 10)
        if len(regime) < len(dates):
            regime = np.pad(regime, (0, len(dates)-len(regime)))
        noise = np.random.normal(0, 0.5, len(dates))
        s = np.clip(regime + noise, -1, 1)
        
        for d, score in zip(dates, s):
            sent_data.append({'Date': d, 'Ticker': t, 'Daily_Sentiment': score})
    sent_df = pd.DataFrame(sent_data)
    
    return prices_df, sent_df

prices_df, sent_df = load_mock_data(selected_stocks, date_range[0], date_range[1])

with tab1:
    st.subheader("Stock Price History")
    
    # Pivot for plotting
    pivot_prices = prices_df.pivot(index='Date', columns='Ticker', values='Close')
    st.line_chart(pivot_prices)
    
    st.subheader("Raw Data")
    st.dataframe(prices_df.head())

with tab2:
    st.subheader("Sentiment Trends")
    
    pivot_sent = sent_df.pivot(index='Date', columns='Ticker', values='Daily_Sentiment')
    
    # Smooth
    ma_window = st.slider("Moving Average Window", 1, 30, 7)
    smoothed_sent = pivot_sent.rolling(ma_window).mean()
    
    st.line_chart(smoothed_sent)
    
    st.subheader("Sentiment Distribution")
    selected_ticker = st.selectbox("Select Ticker", selected_stocks)
    st.bar_chart(sent_df[sent_df['Ticker'] == selected_ticker]['Daily_Sentiment'].value_counts(bins=10).sort_index())

with tab3:
    st.subheader("Strategy Backtest")
    
    st.info("Running backtest comparison between Equal Weight, Max Sharpe, and Sentiment Enhanced strategies.")
    
    if st.button("Run Backtest"):
        with st.spinner("Simulating..."):
            # Prepare data
            returns_df = pivot_prices.pct_change().dropna()
            sentiment_pivot = pivot_sent.loc[returns_df.index]
            
            # Run Backtest
            bt = Backtester(initial_capital=100000)
            try:
                # Use small window for mock data demo
                results = bt.run_backtest(returns_df, sentiment_pivot, window_size=20)
                
                # Metrics
                metrics = bt.calculate_metrics(results)
                
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown("### Cumulative Returns")
                    st.line_chart(results)
                    
                    st.markdown("### Drawdown")
                    # Manual calc for chart
                    cum_ret = results.pct_change().fillna(0).add(1).cumprod()
                    dd = (cum_ret - cum_ret.cummax()) / cum_ret.cummax()
                    st.area_chart(dd)
                    
                with col2:
                    st.markdown("### Performance Metrics")
                    st.dataframe(metrics.style.format("{:.2f}"))
                    
            except Exception as e:
                st.error(f"Backtest failed: {str(e)}")
                st.write("Ensure date range is long enough for training window.")

st.sidebar.markdown("---")
st.sidebar.caption("Project SentiPort · 2026")
