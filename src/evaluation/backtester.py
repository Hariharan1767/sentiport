"""
Backtesting framework for portfolio strategies.
"""

import pandas as pd
import numpy as np
import logging
from typing import Dict, List, Any, Optional
from tqdm import tqdm

from src.portfolio_optimization.mean_variance import MeanVarianceOptimizer
from src.portfolio_optimization.sentiment_optimizer import SentimentEnhancedOptimizer
from src.portfolio_optimization.risk_estimator import RiskEstimator

logger = logging.getLogger(__name__)

class Backtester:
    """
    Simulates portfolio performance over time using walk-forward optimization.
    """
    
    def __init__(self, initial_capital: float = 100000.0, transaction_cost: float = 0.001):
        self.initial_capital = initial_capital
        self.transaction_cost = transaction_cost
        self.results = {}
        
    def run_backtest(self, 
                     returns_df: pd.DataFrame, 
                     sentiment_df: Optional[pd.DataFrame] = None,
                     rebalance_freq: str = 'M', 
                     window_size: int = 126, # 6 months trading days
                     strategies: List[str] = ['equal_weight', 'max_sharpe', 'sentiment_enhanced']) -> pd.DataFrame:
        """
        Run backtest.
        
        Args:
            returns_df: Pivot table of returns (index=Date, columns=Tickers)
            sentiment_df: Pivot table of sentiment (index=Date, columns=Tickers)
            rebalance_freq: 'M' (Month), 'Q' (Quarter)
            window_size: Training window for estimating covariance/returns
        """
        logger.info("Starting backtest...")
        
        # Resample rebalance dates
        rebalance_dates = returns_df.resample(rebalance_freq).last().index
        
        if window_size >= len(returns_df):
            raise ValueError("Window size larger than dataset history")
            
        start_date = returns_df.index[window_size]
                
        # Align rebalance dates to start after window
        valid_rebalance_dates = [d for d in rebalance_dates if d >= returns_df.index[window_size]]
        
        portfolio_values = {strat: [self.initial_capital] for strat in strategies}
        dates = [returns_df.index[window_size-1]] # Start tracking from end of first window
        
        # Initialize weights
        tickers = returns_df.columns
        n_assets = len(tickers)
        current_weights = {strat: np.zeros(n_assets) for strat in strategies}
        
        optimizers = {
            'max_sharpe': MeanVarianceOptimizer(),
            'sentiment_enhanced': SentimentEnhancedOptimizer(sentiment_sensitivity=0.1)
        }
        
        # Simulation Loop
        # We iterate day by day to track value, but only rebalance on rebalance_dates
        
        sim_data = returns_df.iloc[window_size:]
        
        for date in tqdm(sim_data.index):
            # Check if rebalance day
            # (Simplification: check if date is in rebalance_dates or close to it)
            # Better: Keep track of last rebalance
            
            is_rebalance = False
            # Find closest rebalance date in past/today
            # For simplicity in this mock, let's just rebalance if date matches Month End roughly
            if date in valid_rebalance_dates:
                is_rebalance = True
                
            if is_rebalance:
                # 1. Get History (Window)
                history_mask = (returns_df.index < date) & (returns_df.index >= date - pd.Timedelta(days=window_size*2)) # Approx
                history = returns_df[history_mask].iloc[-window_size:] 
                
                # 2. Estimate Parameters
                estimator = RiskEstimator(history)
                mu = history.mean() * 252 # annualized returns estimate
                cov = estimator.calculate_covariance()
                
                # Sentiment (Use latest available)
                if sentiment_df is not None:
                    # Get average sentiment of last month/week? Or latest?
                    # Let's use EMA of sentiment
                    sent_history = sentiment_df[sentiment_df.index < date].iloc[-20:] # Last month
                    latest_sentiment = sent_history.mean()
                else:
                    latest_sentiment = pd.Series(0, index=tickers)
                
                # 3. Optimize Weights
                for strat in strategies:
                    if strat == 'equal_weight':
                        new_w = np.array([1/n_assets] * n_assets)
                    elif strat == 'max_sharpe':
                        w_dict = optimizers['max_sharpe'].optimize(mu, cov)
                        new_w = np.array([w_dict.get(t, 0) for t in tickers])
                    elif strat == 'sentiment_enhanced':
                        w_dict = optimizers['sentiment_enhanced'].optimize(mu, cov, sentiment_scores=latest_sentiment)
                        new_w = np.array([w_dict.get(t, 0) for t in tickers])
                        
                    # Apply Transaction Costs
                    turnover = np.sum(np.abs(new_w - current_weights[strat]))
                    cost = turnover * self.transaction_cost * portfolio_values[strat][-1]
                    portfolio_values[strat][-1] -= cost
                    
                    current_weights[strat] = new_w
            
            # Update Portfolio Value
            day_return = returns_df.loc[date]
            for strat in strategies:
                port_ret = np.sum(current_weights[strat] * day_return)
                new_val = portfolio_values[strat][-1] * (1 + port_ret)
                portfolio_values[strat].append(new_val)
                
            dates.append(date)
            
        # Compile Results
        results_df = pd.DataFrame(index=dates)
        for strat in strategies:
            # Pad or Trim to match dates
            vals = portfolio_values[strat]
            if len(vals) > len(dates):
                vals = vals[:len(dates)]
            elif len(vals) < len(dates):
                # Should not happen if logic correct
                pass
            results_df[strat] = vals
            
        return results_df

    def calculate_metrics(self, backtest_results: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate performance metrics.
        """
        metrics = []
        for strat in backtest_results.columns:
            prices = backtest_results[strat]
            returns = prices.pct_change().dropna()
            
            total_return = (prices.iloc[-1] / prices.iloc[0]) - 1
            ann_return = returns.mean() * 252
            ann_vol = returns.std() * np.sqrt(252)
            sharpe = ann_return / ann_vol if ann_vol > 0 else 0
            
            # Max Drawdown
            cum_returns = (1 + returns).cumprod()
            peak = cum_returns.cummax()
            drawdown = (cum_returns - peak) / peak
            max_dd = drawdown.min()
            
            metrics.append({
                'Strategy': strat,
                'Total Return': total_return,
                'Ann. Return': ann_return,
                'Ann. Volatility': ann_vol,
                'Sharpe Ratio': sharpe,
                'Max Drawdown': max_dd
            })
            
        return pd.DataFrame(metrics).set_index('Strategy')

if __name__ == "__main__":
    # Test
    dates = pd.date_range('2022-01-01', '2023-12-31', freq='B')
    tickers = ['A', 'B']
    returns = pd.DataFrame(np.random.normal(0, 0.01, (len(dates), 2)), index=dates, columns=tickers)
    sentiment = pd.DataFrame(np.random.normal(0, 1, (len(dates), 2)), index=dates, columns=tickers)
    
    bt = Backtester()
    res = bt.run_backtest(returns, sentiment)
    print(bt.calculate_metrics(res))
