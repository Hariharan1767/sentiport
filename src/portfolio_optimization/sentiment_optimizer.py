"""
Sentiment-Enhanced Portfolio Optimizer.
"""

import pandas as pd
import numpy as np
from typing import Dict, Optional
import logging
from src.portfolio_optimization.mean_variance import MeanVarianceOptimizer

logger = logging.getLogger(__name__)

class SentimentEnhancedOptimizer(MeanVarianceOptimizer):
    """
    Portfolio optimization incorporating sentiment signals.
    """
    
    def __init__(self, risk_free_rate: float = 0.02, sentiment_sensitivity: float = 0.1):
        """
        Args:
            risk_free_rate: Annualized risk-free rate
            sentiment_sensitivity: Lambda parameter (how much sentiment affects returns)
        """
        super().__init__(risk_free_rate)
        self.sentiment_sensitivity = sentiment_sensitivity
        
    def adjust_expected_returns(self, expected_returns: pd.Series, 
                                sentiment_scores: pd.Series) -> pd.Series:
        """
        Adjust expected returns based on sentiment.
        Formula: E[r]_adj = E[r] * (1 + sensitivity * sentiment)
        OR: E[r]_adj = E[r] + (sensitivity * sentiment * vol) <- More Black-Litterman
        
        Using simple adjustment for now:
        If sentiment is positive, increase expected return.
        """
        # Align series
        common = expected_returns.index.intersection(sentiment_scores.index)
        if len(common) < len(expected_returns):
            logger.warning(f"Sentiment missing for some assets. Adjusted only overlapping: {common}")
            
        er_adj = expected_returns.copy()
        
        # Assumption: Sentiment is in [-1, 1]
        # Adjustment: Add (Sensitivity * Sentiment) to annualized return? 
        # Or multiplicative?
        # Let's use additive adjustment: Return += (Sensitivity * Sentiment)
        # E.g. if sentiment is 0.5 and sensitivity is 0.1, add 5% to return estimate.
        
        for ticker in common:
            sentiment = sentiment_scores[ticker]
            er_adj[ticker] += (self.sentiment_sensitivity * sentiment)
            
        return er_adj
        
    def optimize(self, expected_returns: pd.Series, covariance_matrix: pd.DataFrame,
                 sentiment_scores: Optional[pd.Series] = None,
                 objective: str = 'max_sharpe') -> Dict[str, float]:
        """
        Optimize with sentiment adjustment.
        """
        if sentiment_scores is not None:
            logger.info(f"Adjusting returns with sentiment (lambda={self.sentiment_sensitivity})")
            expected_returns = self.adjust_expected_returns(expected_returns, sentiment_scores)
            
        return super().optimize(expected_returns, covariance_matrix, objective)

if __name__ == "__main__":
    # Test
    mu = pd.Series([0.1, 0.2], index=['AAPL', 'TSLA'])
    cov = pd.DataFrame([[0.04, 0.01], [0.01, 0.09]], index=['AAPL', 'TSLA'], columns=['AAPL', 'TSLA'])
    sent = pd.Series([0.5, -0.2], index=['AAPL', 'TSLA'])
    
    # Baseline
    print("Baseline:", MeanVarianceOptimizer().optimize(mu, cov))
    
    # Enhanced
    opt = SentimentEnhancedOptimizer(sentiment_sensitivity=0.1)
    print("Enhanced:", opt.optimize(mu, cov, sentiment_scores=sent))
    # Expect AAPL weight to increase (positive sentiment)
