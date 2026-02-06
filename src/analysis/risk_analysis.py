
class RiskAnalyzer:
    def __init__(self):
        pass

    def analyze_risk(self, data, tech_df):
        """
        Analyzes Risk Factors (Factor 7) and Market Position (Factor 5).
        """
        info = data.get('info', {})
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

        # 2. Debt Control (Company Risk) - Re-evaluating textually for risk module
        debt_to_equity = info.get('debtToEquity', 0)
        if debt_to_equity > 200:
            details.append("High Debt Risk (>200% D/E)")
            score -= 1 
        
        # 3. Recommendation Rating
        rec = info.get('recommendationKey', 'none')
        if rec in ['buy', 'strong_buy']:
            score += 1
            details.append(f"Analyst Consensus: {rec.replace('_', ' ').upper()}")

        return {
            "score": max(0, score), # Clamp to 0
            "max_score": 2, # Rough max
            "details": details
        }
