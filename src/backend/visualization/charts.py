"""
Visualization module.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Optional, List
import logging
from pathlib import Path

# Configure plotting style
try:
    plt.style.use('seaborn-v0_8-whitegrid')
except:
    plt.style.use('ggplot')
    
sns.set_palette("husl")
logger = logging.getLogger(__name__)

class ChartGenerator:
    """
    Generates static charts and plots.
    """
    
    def __init__(self, output_dir: str = 'results/figures'):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def save_plot(self, fig, filename: str):
        """Save plot to file"""
        path = self.output_dir / filename
        fig.savefig(path, dpi=300, bbox_inches='tight')
        logger.info(f"Saved plot to {path}")
        plt.close(fig)

    def plot_cumulative_returns(self, backtest_results: pd.DataFrame, 
                              benchmark_col: Optional[str] = None):
        """
        Plot cumulative returns of strategies.
        """
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Calculate cumulative returns from portfolio values
        # Assume input are portfolio values (price series)
        returns = backtest_results.pct_change().fillna(0)
        cum_ret = (1 + returns).cumprod()
        
        cum_ret.plot(ax=ax, linewidth=2)
        
        ax.set_title("Cumulative Portfolio Returns", fontsize=14, fontweight='bold')
        ax.set_ylabel("Growth ($1 Invested)", fontsize=12)
        ax.set_xlabel("Date", fontsize=12)
        ax.legend(title="Strategy")
        ax.grid(True, alpha=0.3)
        
        self.save_plot(fig, 'cumulative_returns.png')
        
    def plot_drawdown(self, backtest_results: pd.DataFrame):
        """
        Plot drawdowns.
        """
        fig, ax = plt.subplots(figsize=(12, 6))
        
        returns = backtest_results.pct_change().fillna(0)
        cum_ret = (1 + returns).cumprod()
        peak = cum_ret.cummax()
        drawdown = (cum_ret - peak) / peak
        
        drawdown.plot(ax=ax, linewidth=1.5, alpha=0.8)
        
        ax.fill_between(drawdown.index, 0, -1, color='gray', alpha=0.1) # Highlight unexpected deep drawdown? Or just formatting
        
        ax.set_title("Portfolio Drawdown", fontsize=14, fontweight='bold')
        ax.set_ylabel("Drawdown %", fontsize=12)
        ax.axhline(0, color='black', linewidth=0.5)
        
        self.save_plot(fig, 'drawdowns.png')
        
    def plot_sentiment_time_series(self, sentiment_df: pd.DataFrame, ticker: str):
        """
        Plot sentiment scores over time for a stock.
        """
        # sentiment_df expected to have Date/Ticker index or columns, ideally filtered for ticker
        # Or pivot table with tickers as columns
        
        data = sentiment_df[ticker] if ticker in sentiment_df.columns else None
        
        if data is None:
            return
            
        fig, ax = plt.subplots(figsize=(12, 4))
        
        # Rolling average
        ma = data.rolling(window=7).mean()
        
        ax.bar(data.index, data, label='Daily Sentiment', alpha=0.3, color='gray')
        ax.plot(ma.index, ma, label='7-Day MA', color='blue', linewidth=2)
        
        ax.set_title(f"News Sentiment: {ticker}", fontsize=14)
        ax.set_ylabel("Sentiment Score", fontsize=12)
        ax.legend()
        ax.axhline(0, color='black', linestyle='--')
        
        self.save_plot(fig, f'sentiment_{ticker}.png')
        
    def plot_sentiment_vs_price(self, stock_df: pd.DataFrame, sentiment_df: pd.DataFrame, ticker: str):
        """
        Plot Price vs Sentiment on dual axis.
        """
        stock_data = stock_df[stock_df['Ticker'] == ticker].set_index('Date')['Close']
        
        # Need sentiment with date index for this ticker
        # Assuming sentiment_df is pivoted or we filter
        # Let's assume passed sentiment_df is pivoted (index=Date, columns=Tickers)
        sent_data = sentiment_df[ticker]
        
        # Align
        common_idx = stock_data.index.intersection(sent_data.index)
        stock_data = stock_data.loc[common_idx]
        sent_ma = sent_data.loc[common_idx].rolling(10).mean()
        
        fig, ax1 = plt.subplots(figsize=(12, 6))
        
        # Plot Price
        color = 'tab:blue'
        ax1.set_xlabel('Date')
        ax1.set_ylabel('Stock Price', color=color)
        ax1.plot(stock_data.index, stock_data, color=color, linewidth=2, label='Price')
        ax1.tick_params(axis='y', labelcolor=color)
        
        # Plot Sentiment
        ax2 = ax1.twinx() 
        color = 'tab:orange'
        ax2.set_ylabel('Sentiment (10d MA)', color=color)
        ax2.plot(sent_ma.index, sent_ma, color=color, linestyle='--', linewidth=1.5, label='Sentiment')
        ax2.tick_params(axis='y', labelcolor=color)
        
        plt.title(f"{ticker}: Price vs Sentiment", fontsize=14)
        fig.tight_layout()
        
        self.save_plot(fig, f'price_vs_sentiment_{ticker}.png')

if __name__ == "__main__":
    # Test
    dates = pd.date_range('2023-01-01', periods=100)
    results = pd.DataFrame({
        'Strategy A': 100 * (1 + np.random.normal(0.001, 0.01, 100)).cumprod(),
        'Strategy B': 100 * (1 + np.random.normal(0.0005, 0.01, 100)).cumprod()
    }, index=dates)
    
    gen = ChartGenerator()
    gen.plot_cumulative_returns(results)
    gen.plot_drawdown(results)
