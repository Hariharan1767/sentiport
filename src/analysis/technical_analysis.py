
import pandas as pd
import numpy as np

class TechnicalAnalyzer:
    def __init__(self):
        pass

    def analyze_trend(self, df):
        """
        Analyzes Trend & Momentum (Factor 6).
        """
        if df is None or df.empty:
            return {"score": 0, "details": ["No Technical Data"]}

        score = 0
        details = []
        
        # Latest data point
        latest = df.iloc[-1]
        
        # 1. Trend (SMA 50 vs 200)
        if 'SMA_50' in latest and 'SMA_200' in latest:
            if latest['SMA_50'] > latest['SMA_200']:
                score += 1
                details.append("Golden Cross / Bullish Trend (SMA50 > SMA200)")
            else:
                details.append("Bearish Trend (SMA50 < SMA200)")

        # 2. RSI
        rsi = latest.get('RSI', 50)
        if rsi < 30:
            score += 1
            details.append("Oversold (RSI < 30) - Potential Buy")
        elif rsi > 70:
            details.append("Overbought (RSI > 70) - Caution")
        else:
            score += 0.5
            details.append("Neutral RSI")

        # 3. MACD
        macd = latest.get('MACD_12_26_9', 0)
        macd_signal = latest.get('MACDs_12_26_9', 0)
        if macd > macd_signal:
            score += 1
            details.append("Bullish MACD Crossover")

        return {
            "score": score,
            "max_score": 3,
            "details": details
        }
