"""
Performance analysis module.
"""

import pandas as pd
import numpy as np
import logging
from typing import Dict, List, Optional
from scipy import stats

logger = logging.getLogger(__name__)

class PerformanceAnalyzer:
    """
    Calculates detailed performance metrics and statistical tests.
    """
    
    def __init__(self, risk_free_rate: float = 0.02):
        self.risk_free_rate = risk_free_rate
        
    def calculate_metrics(self, prices_df: pd.DataFrame, benchmark_col: Optional[str] = None) -> pd.DataFrame:
        """
        Calculate comprehensive metrics for all strategies.
        
        Args:
            prices_df: DataFrame of portfolio values over time
            benchmark_col: Name of benchmark column (e.g., 'SPY') for Beta/Alpha
            
        Returns:
            DataFrame of metrics
        """
        returns_df = prices_df.pct_change().dropna()
        metrics = []
        
        benchmark_returns = returns_df[benchmark_col] if benchmark_col and benchmark_col in returns_df.columns else None
        
        for strategy in prices_df.columns:
            series = prices_df[strategy]
            rets = returns_df[strategy]
            
            # 1. Basic Metrics
            total_ret = (series.iloc[-1] / series.iloc[0]) - 1
            ann_ret = rets.mean() * 252
            ann_vol = rets.std() * np.sqrt(252)
            sharpe = (ann_ret - self.risk_free_rate) / ann_vol if ann_vol > 0 else 0
            
            # 2. Drawdown
            cum_ret = (1 + rets).cumprod()
            peak = cum_ret.cummax()
            drawdown = (cum_ret - peak) / peak
            max_dd = drawdown.min()
            
            # 3. Sortino Ratio (Downside volatility)
            downside_rets = rets[rets < 0]
            downside_vol = downside_rets.std() * np.sqrt(252)
            sortino = (ann_ret - self.risk_free_rate) / downside_vol if downside_vol > 0 else 0
            
            # 4. Calmar Ratio
            calmar = ann_ret / abs(max_dd) if max_dd != 0 else 0
            
            # 5. Win Rate (Daily)
            win_rate = (rets > 0).mean()
            
            # 6. Beta & Alpha (if benchmark exists)
            beta = np.nan
            alpha = np.nan
            if benchmark_returns is not None and strategy != benchmark_col:
                # Linear regression
                slope, intercept, _, _, _ = stats.linregress(benchmark_returns, rets)
                beta = slope
                alpha = intercept * 252 # Annualized alpha
                
            metrics.append({
                'Strategy': strategy,
                'Ann. Return': ann_ret,
                'Ann. Volatility': ann_vol,
                'Sharpe Ratio': sharpe,
                'Sortino Ratio': sortino,
                'Max Drawdown': max_dd,
                'Calmar Ratio': calmar,
                'Win Rate': win_rate,
                'Beta': beta,
                'Alpha': alpha
            })
            
        return pd.DataFrame(metrics).set_index('Strategy')

    def t_test(self, returns_df: pd.DataFrame, strat_a: str, strat_b: str) -> Dict[str, float]:
        """
        Perform paired t-test between two strategies' returns.
        H0: Mean difference is zero.
        """
        diff = returns_df[strat_a] - returns_df[strat_b]
        t_stat, p_val = stats.ttest_rel(returns_df[strat_a], returns_df[strat_b])
        
        return {
            't_statistic': t_stat,
            'p_value': p_val,
            'mean_diff': diff.mean() * 252 # Annualized difference
        }

if __name__ == "__main__":
    # Test
    dates = pd.date_range('2023-01-01', periods=252)
    prices = pd.DataFrame({
        'Strategy_A': 100 * (1 + np.random.normal(0.0005, 0.01, 252)).cumprod(),
        'Strategy_B': 100 * (1 + np.random.normal(0.0002, 0.01, 252)).cumprod()
    }, index=dates)
    
    analyzer = PerformanceAnalyzer()
    print("Metrics:\n", analyzer.calculate_metrics(prices))
    print("\nT-Test:\n", analyzer.t_test(prices.pct_change().dropna(), 'Strategy_A', 'Strategy_B'))
