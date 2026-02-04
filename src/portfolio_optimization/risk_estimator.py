"""
Risk estimation module.
"""

import numpy as np
import pandas as pd
from typing import Optional, Union

class RiskEstimator:
    """
    Estimates risk metrics (volatility, covariance).
    """
    
    def __init__(self, returns_data: pd.DataFrame):
        """
        Args:
            returns_data: DataFrame with Date, Ticker, Return_1d OR pivoted returns (Date index, Ticker cols)
        """
        if 'Ticker' in returns_data.columns:
            self.returns = returns_data.pivot(index='Date', columns='Ticker', values='Return_1d')
        else:
            self.returns = returns_data
            
    def calculate_volatility(self, window: Optional[int] = None, annualized: bool = True) -> pd.Series:
        """
        Calculate volatility for each asset.
        """
        if window:
            vol = self.returns.rolling(window=window).std().iloc[-1]
        else:
            vol = self.returns.std()
            
        if annualized:
            vol = vol * np.sqrt(252)
            
        return vol
        
    def calculate_covariance(self, window: Optional[int] = None, annualized: bool = True) -> pd.DataFrame:
        """
        Calculate covariance matrix.
        """
        if window:
            cov = self.returns.rolling(window=window).cov().iloc[-len(self.returns.columns):]
            # The above rolling cov structure is complex (MultiIndex), simplified:
            # rolling().cov() returns a MultiIndex. We just want the LAST covariance estimate usually.
            
            # Alternative: Get covariance of last 'window' days
            last_returns = self.returns.iloc[-window:]
            cov = last_returns.cov()
        else:
            cov = self.returns.cov()
            
        if annualized:
            cov = cov * 252
            
        return cov
        
    def calculate_correlation(self) -> pd.DataFrame:
        return self.returns.corr()

if __name__ == "__main__":
    # Test
    dates = pd.date_range('2023-01-01', periods=100)
    data = pd.DataFrame({
        'Date': np.repeat(dates, 2),
        'Ticker': np.tile(['AAPL', 'MSFT'], 100),
        'Return_1d': np.random.normal(0, 0.01, 200)
    })
    
    estimator = RiskEstimator(data)
    print("Volatility:\n", estimator.calculate_volatility())
    print("Covariance:\n", estimator.calculate_covariance())
