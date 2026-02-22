"""
Mean-Variance Portfolio Optimizer.
"""

import numpy as np
import pandas as pd
from scipy.optimize import minimize
from typing import Dict, Tuple, Optional, Union
import logging

logger = logging.getLogger(__name__)

class MeanVarianceOptimizer:
    """
    Standard Markowitz Mean-Variance Optimization.
    
    optimize() returns (weights_array, metrics_dict) to match api_server.py's
    tuple-unpacking: `weights, metrics = optimizer.optimize(...)`
    """
    
    def __init__(self, risk_free_rate: float = 0.02):
        self.risk_free_rate = risk_free_rate
        
    def optimize(
        self,
        expected_returns: Union[np.ndarray, pd.Series],
        covariance_matrix: Union[np.ndarray, pd.DataFrame],
        objective: str = 'max_sharpe',
        target_return: Optional[float] = None,
    ) -> Tuple[np.ndarray, Dict]:
        """
        Optimize portfolio weights.
        
        Args:
            expected_returns: Array/Series of expected returns for each asset
            covariance_matrix: Covariance matrix of asset returns
            objective: 'max_sharpe' or 'min_volatility'
            target_return: Ignored (kept for backward-compat with api_server)
            
        Returns:
            (weights_array, metrics_dict) tuple
        """
        # Accept both numpy arrays and pandas Series/DataFrame
        if isinstance(expected_returns, pd.Series):
            er = expected_returns.values
        else:
            er = np.asarray(expected_returns, dtype=float)

        if isinstance(covariance_matrix, pd.DataFrame):
            cov = covariance_matrix.values
        else:
            cov = np.asarray(covariance_matrix, dtype=float)

        if len(er) != cov.shape[0]:
            raise ValueError("Dimensions of returns and covariance do not match")
            
        n_assets = len(er)
        initial_weights = np.array([1.0 / n_assets] * n_assets)
        constraints = [{'type': 'eq', 'fun': lambda x: np.sum(x) - 1}]
        bounds = tuple((0.0, 1.0) for _ in range(n_assets))
        
        def portfolio_volatility(w):
            return float(np.sqrt(w @ cov @ w))
            
        def portfolio_return(w):
            return float(np.dot(w, er))
            
        def neg_sharpe(w):
            ret = portfolio_return(w)
            vol = portfolio_volatility(w)
            if vol < 1e-10:
                return 0.0
            return -(ret - self.risk_free_rate) / vol

        fun = neg_sharpe if objective != 'min_volatility' else portfolio_volatility
            
        result = minimize(
            fun, initial_weights, method='SLSQP',
            bounds=bounds, constraints=constraints,
            options={'maxiter': 1000, 'ftol': 1e-9}
        )
        
        if not result.success:
            logger.warning(f"Optimization did not converge: {result.message}")
            
        weights = result.x.copy()
        weights[weights < 1e-4] = 0.0
        total = weights.sum()
        if total > 0:
            weights /= total
        
        exp_ret = float(np.dot(weights, er))
        vol = float(np.sqrt(weights @ cov @ weights))
        sharpe = (exp_ret - self.risk_free_rate) / vol if vol > 0 else 0.0
        
        metrics = {
            'expected_return': exp_ret,
            'risk': vol,
            'sharpe_ratio': sharpe,
        }
        
        return weights, metrics


if __name__ == "__main__":
    # Test
    mu = pd.Series([0.1, 0.2, 0.15], index=['A', 'B', 'C'])
    cov = pd.DataFrame([[0.04, 0.01, 0.01], 
                        [0.01, 0.09, 0.02], 
                        [0.01, 0.02, 0.05]], 
                       index=['A', 'B', 'C'], columns=['A', 'B', 'C'])
                       
    opt = MeanVarianceOptimizer()
    w, m = opt.optimize(mu, cov)
    print("Optimal Weights (Max Sharpe):", dict(zip(['A', 'B', 'C'], w)))
    print("Metrics:", m)
