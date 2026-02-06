
class QualitativeAnalyzer:
    def __init__(self):
        pass

    def analyze_business_model(self, data):
        """
        Analyzes Business Model & Competitive Advantage (Factor 3).
        Infers 'Moat' from margins and industry.
        """
        info = data.get('info', {})
        score = 0
        details = []

        # 1. Wide Moat Inference (High Gross Margins often indicate pricing power)
        gross_margins = info.get('grossMargins', 0)
        if gross_margins > 0.40:
            score += 1
            details.append("High Gross Margins (Possible Moat)")
        
        # 2. Industry Position
        # This is harder to get free, but we can look at Market Cap as a proxy for leadership
        mkt_cap = info.get('marketCap', 0)
        if mkt_cap > 100_000_000_000: # 100 Billion
            score += 1
            details.append("Large Cap Industry Leader")
        
        # 3. Dividend Payout (Stability)
        payout = info.get('payoutRatio', 0)
        if payout and payout < 0.6 and payout > 0:
            score += 0.5
            details.append("Sustainable Dividend Payout")

        return {
            "score": score,
            "max_score": 2.5,
            "details": details
        }

    def analyze_management(self, data):
        """
        Analyzes Management & Corporate Governance (Factor 4).
        Very hard to quantify freely, using Return on Equity (ROE) as proxy for management efficiency.
        """
        info = data.get('info', {})
        score = 0
        details = []

        # 1. Return on Equity (Management Efficiency)
        roe = info.get('returnOnEquity', 0)
        if roe > 0.15:
            score += 1
            details.append(f"Strong ROE ({roe:.2%}) - Efficient Management")
        elif roe > 0.10:
            score += 0.5
            details.append(f"Decent ROE ({roe:.2%})")

        # 2. Insider Ownership (Held by Insiders)
        held_insiders = info.get('heldPercentInsiders', 0)
        if held_insiders > 0.10:
            score += 1
            details.append("High Insider Ownership (>10%)")
        
        return {
            "score": score,
            "max_score": 2,
            "details": details
        }
