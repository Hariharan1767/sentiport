
import pandas as pd
import numpy as np

class FundamentalAnalyzer:
    def __init__(self):
        pass

    def analyze_health(self, data):
        """
        Analyzes Financial Health (Factor 1).
        Criteria: Revenue Growth, Margins, Operating Cash Flow, Debt/Equity.
        """
        info = data.get('info', {})
        financials = data.get('financials_dfs', {})
        
        score = 0
        details = []

        # 1. Revenue Growth
        rev_growth = info.get('revenueGrowth', 0)
        if rev_growth and rev_growth > 0.10:
            score += 1
            details.append("Strong Revenue Growth (>10%)")
        elif rev_growth and rev_growth > 0:
            score += 0.5
            details.append("Positive Revenue Growth")
        else:
            details.append("Negative/Stagnant Revenue Growth")

        # 2. Margins
        op_margin = info.get('operatingMargins', 0)
        if op_margin and op_margin > 0.15:
            score += 1
            details.append("Healthy Operating Margins (>15%)")
        
        # 3. Cash Flow
        try:
            cash_flow = financials.get('cash_flow')
            if cash_flow is not None and not cash_flow.empty:
                op_cash = cash_flow.loc['Operating Cash Flow'].iloc[0] if 'Operating Cash Flow' in cash_flow.index else 0
                if op_cash > 0:
                    score += 1
                    details.append("Positive Operating Cash Flow")
        except:
            pass

        # 4. Debt Control
        debt_equity = info.get('debtToEquity', 100)
        if debt_equity and debt_equity < 100: # < 1.0 ratio often represented as 100 in yfinance sometimes, need verification. usually it's percentage. 
            # safe assumption: < 200 (2.0) is okay, < 50 (0.5) is great.
            score += 1
            details.append("Reasonable Debt Levels")
        
        return {
            "score": score,
            "max_score": 4,
            "details": details
        }

    def analyze_valuation(self, data):
        """
        Analyzes Valuation (Factor 2).
        Criteria: P/E, P/B, PEG, Dividend Yield vs Benchmarks (Static for now).
        """
        val = data.get('valuation', {})
        score = 0
        details = []

        # P/E Ratio (General baseline < 25)
        pe = val.get('trailingPE')
        if pe and pe < 20:
            score += 1
            details.append(f"Attractive P/E Ratio ({pe:.2f})")
        elif pe and pe < 30:
            score += 0.5
            details.append(f"Moderate P/E Ratio ({pe:.2f})")
        
        # PEG Ratio (General baseline < 1 is undervalued)
        peg = val.get('pegRatio')
        if peg and peg < 1.2:
            score += 1
            details.append(f"Undervalued per PEG ({peg:.2f})")
        
        # Price to Book
        pb = val.get('priceToBook')
        if pb and pb < 3:
            score += 0.5
            details.append(f"Reasonable P/B Ratio ({pb:.2f})")

        return {
            "score": score,
            "max_score": 2.5,
            "details": details
        }
    def analyze_growth_potential(self, data):
        """
        Analyzes Growth Potential (Factor 4).
        """
        info = data.get('info', {})
        score = 0
        details = []

        # 1. Earnings Growth
        earnings_growth = info.get('earningsGrowth', 0)
        if earnings_growth and earnings_growth > 0.15:
            score += 1
            details.append("High Earnings Growth Potential (>15%)")
        
        # 2. Analyst Growth Estimates
        growth_est = info.get('earningsQuarterlyGrowth', 0)
        if growth_est and growth_est > 0.10:
            score += 1
            details.append("Positive Quarterly Growth Estimates")
        
        return {
            "score": score,
            "max_score": 2,
            "details": details
        }

    def analyze(self, data):
        """
        Unified entry point called by api_server.py.
        Runs all fundamental sub-analyses and returns a normalised 0-100 score.
        """
        if not data or not isinstance(data, dict):
            return {'score': 50, 'rating': 'N/A', 'details': []}

        try:
            health = self.analyze_health(data)
            valuation = self.analyze_valuation(data)
            growth = self.analyze_growth_potential(data)

            # Normalise each sub-score to 0-100
            def to_pct(result):
                max_s = result.get('max_score', 1) or 1
                return (result.get('score', 0) / max_s) * 100

            composite = (to_pct(health) * 0.5 + to_pct(valuation) * 0.3 + to_pct(growth) * 0.2)

            all_details = health.get('details', []) + valuation.get('details', []) + growth.get('details', [])

            if composite >= 70:
                rating = 'STRONG'
            elif composite >= 45:
                rating = 'AVERAGE'
            else:
                rating = 'WEAK'

            return {
                'score': round(composite, 1),
                'rating': rating,
                'details': all_details,
                'sub_scores': {
                    'health': round(to_pct(health), 1),
                    'valuation': round(to_pct(valuation), 1),
                    'growth': round(to_pct(growth), 1),
                }
            }
        except Exception as e:
            return {'score': 50, 'rating': 'N/A', 'details': [str(e)]}
