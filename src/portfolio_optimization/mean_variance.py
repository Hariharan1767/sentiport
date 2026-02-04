"""
Mean-Variance Portfolio Optimizer.
"""

import numpy as np
import pandas as pd
from scipy.optimize import minimize
from typing import Dict, Tuple, Optional
import logging

logger = logging.getLogger(__name__)

class MeanVarianceOptimizer:
    """
    Standard Markowitz Mean-Variance Optimization.
    """
    
    def __init__(self, risk_free_rate: float = 0.02):
        self.risk_free_rate = risk_free_rate
        
    def optimize(self, expected_returns: pd.Series, covariance_matrix: pd.DataFrame, 
                 objective: str = 'max_sharpe') -> Dict[str, float]:
        """
        Optimize portfolio weights.
        
        Args:
            expected_returns: Series of expected returns for each asset
            covariance_matrix: Covariance matrix of asset returns
            objective: 'max_sharpe' or 'min_volatility'
            
        Returns:
            Dictionary mapping tickers to optimal weights
        """
        if len(expected_returns) != len(covariance_matrix):
            raise ValueError("Dimensions of returns and covariance do not match")
            
        tickers = expected_returns.index
        n_assets = len(tickers)
        
        # Initial guess (equal weights)
        initial_weights = np.array([1/n_assets] * n_assets)
        
        # Constraints: Weights sum to 1
        constraints = [{'type': 'eq', 'fun': lambda x: np.sum(x) - 1}]
        
        # Bounds: 0 <= weight <= 1 (Long only)
        bounds = tuple((0, 1) for _ in range(n_assets))
        
        # Objective Functions
        def portfolio_volatility(weights, cov_matrix):
            return np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
            
        def portfolio_return(weights, exp_returns):
            return np.sum(weights * exp_returns)
            
        def negative_sharpe_ratio(weights, exp_returns, cov_matrix, rf_rate):
            p_ret = portfolio_return(weights, exp_returns)
            p_vol = portfolio_volatility(weights, cov_matrix)
            return -(p_ret - rf_rate) / p_vol
            
        if objective == 'max_sharpe':
            args = (expected_returns.values, covariance_matrix.values, self.risk_free_rate)
            fun = negative_sharpe_ratio
        elif objective == 'min_volatility':
            args = (covariance_matrix.values,)
            fun = portfolio_volatility
        else:
            raise ValueError("Unknown objective")
            
        # Optimization
        result = minimize(fun, initial_weights, args=args, method='SLSQP', bounds=bounds, constraints=constraints)
        
        if not result.success:
            logger.warning(f"Optimization failed: {result.message}")
            
        weights = result.x
        
        # Clean weights (round small values to 0)
        weights[weights < 1e-4] = 0
        weights = weights / np.sum(weights) # Renormalize
        
        return dict(zip(tickers, weights))

if __name__ == "__main__":
    # Test
    mu = pd.Series([0.1, 0.2, 0.15], index=['A', 'B', 'C'])
    cov = pd.DataFrame([[0.04, 0.01, 0.01], 
                        [0.01, 0.09, 0.02], 
                        [0.01, 0.02, 0.05]], 
                       index=['A', 'B', 'C'], columns=['A', 'B', 'C'])
                       
    opt = MeanVarianceOptimizer()
    w = opt.optimize(mu, cov)
    print("Optimal Weights (Max Sharpe):", w)
