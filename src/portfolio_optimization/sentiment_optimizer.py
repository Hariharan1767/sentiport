"""
Sentiment-Enhanced Portfolio Optimizer.
"""

import numpy as np
import pandas as pd
from typing import Dict, Optional, Tuple, Union
import logging
from portfolio_optimization.mean_variance import MeanVarianceOptimizer

logger = logging.getLogger(__name__)

class SentimentEnhancedOptimizer(MeanVarianceOptimizer):
    """
    Portfolio optimization incorporating sentiment signals.
    """
    
    def __init__(self, risk_free_rate: float = 0.02, sentiment_sensitivity: float = 0.1):
        super().__init__(risk_free_rate)
        self.sentiment_sensitivity = sentiment_sensitivity
        
    def adjust_expected_returns(
        self,
        expected_returns: Union[np.ndarray, pd.Series],
        sentiment_weights: Dict[str, float],
        tickers: Optional[list] = None
    ) -> np.ndarray:
        """
        Adjust expected returns based on sentiment scores.
        sentiment_weights: dict mapping ticker -> score (0-1 range from api_server)
        """
        if isinstance(expected_returns, pd.Series):
            er = expected_returns.copy()
            for ticker, raw_score in sentiment_weights.items():
                if ticker in er.index:
                    # Convert 0-1 score to -1..+1 adjustment
                    sentiment = (raw_score - 0.5) * 2
                    er[ticker] += self.sentiment_sensitivity * sentiment
            return er
        else:
            er = np.array(expected_returns, dtype=float).copy()
            if tickers:
                for i, ticker in enumerate(tickers):
                    raw_score = sentiment_weights.get(ticker, 0.5)
                    sentiment = (raw_score - 0.5) * 2
                    er[i] += self.sentiment_sensitivity * sentiment
            return er
        
    def optimize(
        self,
        expected_returns: Union[np.ndarray, pd.Series],
        covariance_matrix: Union[np.ndarray, pd.DataFrame],
        sentiment_weights: Optional[Dict] = None,
        objective: str = 'max_sharpe',
        target_return: Optional[float] = None,
        tickers: Optional[list] = None,
    ) -> Tuple[np.ndarray, Dict]:
        """
        Optimize with sentiment adjustment.
        Returns (weights_array, metrics_dict) to match api_server expectations.
        """
        if sentiment_weights:
            logger.info(f"Adjusting returns with sentiment (lambda={self.sentiment_sensitivity})")
            expected_returns = self.adjust_expected_returns(
                expected_returns, sentiment_weights, tickers=tickers
            )
            
        return super().optimize(expected_returns, covariance_matrix, objective=objective)


if __name__ == "__main__":
    mu = pd.Series([0.1, 0.2], index=['AAPL', 'TSLA'])
    cov = pd.DataFrame([[0.04, 0.01], [0.01, 0.09]], index=['AAPL', 'TSLA'], columns=['AAPL', 'TSLA'])
    sent = {'AAPL': 0.8, 'TSLA': 0.3}
    
    baseline_w, baseline_m = MeanVarianceOptimizer().optimize(mu, cov)
    print("Baseline weights:", dict(zip(['AAPL', 'TSLA'], baseline_w)))
    
    opt = SentimentEnhancedOptimizer(sentiment_sensitivity=0.1)
    enhanced_w, enhanced_m = opt.optimize(mu, cov, sentiment_weights=sent, tickers=['AAPL', 'TSLA'])
    print("Enhanced weights:", dict(zip(['AAPL', 'TSLA'], enhanced_w)))
