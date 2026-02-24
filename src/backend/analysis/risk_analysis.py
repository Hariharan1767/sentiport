
class RiskAnalyzer:
    def __init__(self):
        pass

    def analyze_risk(self, data, tech_df=None):
        """
        Analyzes Risk Factors (Factor 7) and Market Position (Factor 5).
        """
        if not data or not isinstance(data, dict):
            return {"score": 1, "max_score": 2, "details": [], "risk_level": "MEDIUM"}

        info = data.get('info', {})
        if not isinstance(info, dict):
            info = {}
        score = 0 # Higher score = Lower Risk (Better)
        details = []
        
        # 1. Beta (Market Risk)
        beta = info.get('beta', 1.0)
        if beta and beta < 1.2 and beta > 0.8:
             score += 1
             details.append("Moderate Volatility (Beta ~1)")
        elif beta and beta < 0.8:
             score += 0.5
             details.append("Low Volatility (Beta < 0.8)")
        else:
             details.append("High Volatility (Beta > 1.2)")

        # 2. Debt Control (Company Risk)
        debt_to_equity = info.get('debtToEquity', 0)
        if debt_to_equity and debt_to_equity > 200:
            details.append("High Debt Risk (>200% D/E)")
            score -= 1 
        
        # 3. Recommendation Rating
        rec = info.get('recommendationKey', 'none')
        if rec in ['buy', 'strong_buy']:
            score += 1
            details.append(f"Analyst Consensus: {rec.replace('_', ' ').upper()}")

        return {
            "score": max(0, score),
            "max_score": 2,
            "details": details
        }

    def analyze(self, stock_df):
        """
        Unified entry point called by api_server.py.
        Accepts a price DataFrame; derives risk from price volatility + static rules.
        Returns normalised 0-100 score.
        """
        try:
            import numpy as np
            import pandas as pd
            details = []
            score_pct = 50  # default medium risk

            if stock_df is not None and not (hasattr(stock_df, 'empty') and stock_df.empty):
                if 'Close' in stock_df.columns:
                    returns = stock_df['Close'].pct_change().dropna()
                    ann_vol = returns.std() * (252 ** 0.5) * 100
                    if ann_vol < 15:
                        score_pct = 75
                        details.append(f"Low annualised volatility ({ann_vol:.1f}%)")
                    elif ann_vol < 30:
                        score_pct = 55
                        details.append(f"Moderate volatility ({ann_vol:.1f}%)")
                    else:
                        score_pct = 30
                        details.append(f"High volatility ({ann_vol:.1f}%)")

            if score_pct >= 65:
                risk_level = 'LOW'
            elif score_pct >= 40:
                risk_level = 'MEDIUM'
            else:
                risk_level = 'HIGH'

            return {
                'score': round(score_pct, 1),
                'risk_level': risk_level,
                'details': details
            }
        except Exception as e:
            return {'score': 50, 'risk_level': 'MEDIUM', 'details': [str(e)]}
