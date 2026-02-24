
import pandas as pd
import numpy as np

class TechnicalAnalyzer:
    def __init__(self):
        pass

    def analyze_trend(self, df):
        """
        Analyzes Trend & Momentum (Factor 6).
        """
        if df is None or (hasattr(df, 'empty') and df.empty):
            return {"score": 0, "max_score": 3, "details": ["No Technical Data"]}

        score = 0
        details = []
        
        # Latest data point
        latest = df.iloc[-1]
        
        # 1. Trend (SMA 50 vs 200)
        if 'SMA_50' in df.columns and 'SMA_200' in df.columns:
            if latest['SMA_50'] > latest['SMA_200']:
                score += 1
                details.append("Golden Cross / Bullish Trend (SMA50 > SMA200)")
            else:
                details.append("Bearish Trend (SMA50 < SMA200)")

        # 2. RSI
        rsi = latest.get('RSI', 50) if hasattr(latest, 'get') else latest.get('RSI', 50)
        try:
            rsi_val = float(rsi) if rsi is not None else 50
        except (TypeError, ValueError):
            rsi_val = 50
        if rsi_val < 30:
            score += 1
            details.append("Oversold (RSI < 30) - Potential Buy")
        elif rsi_val > 70:
            details.append("Overbought (RSI > 70) - Caution")
        else:
            score += 0.5
            details.append("Neutral RSI")

        # 3. MACD
        macd = latest.get('MACD_12_26_9', 0) if hasattr(latest, 'get') else 0
        macd_signal = latest.get('MACDs_12_26_9', 0) if hasattr(latest, 'get') else 0
        try:
            if float(macd or 0) > float(macd_signal or 0):
                score += 1
                details.append("Bullish MACD Crossover")
        except (TypeError, ValueError):
            pass

        return {
            "score": score,
            "max_score": 3,
            "details": details
        }

    def analyze(self, stock_df):
        """
        Unified entry point called by api_server.py.
        Accepts a price DataFrame and returns a normalised 0-100 score with signal.
        """
        if stock_df is None or (hasattr(stock_df, 'empty') and stock_df.empty):
            return {'score': 50, 'signal': 'NEUTRAL', 'details': []}
        try:
            # Try to compute simple indicators inline if columns are missing
            if 'Close' in stock_df.columns:
                close = stock_df['Close']
                if 'SMA_50' not in stock_df.columns and len(close) >= 50:
                    stock_df = stock_df.copy()
                    stock_df['SMA_50'] = close.rolling(50).mean()
                    stock_df['SMA_200'] = close.rolling(200).mean() if len(close) >= 200 else close.rolling(min(len(close), 50)).mean()
                    delta = close.diff()
                    gain = delta.clip(lower=0).rolling(14).mean()
                    loss = (-delta.clip(upper=0)).rolling(14).mean()
                    rs = gain / loss.replace(0, 1e-10)
                    stock_df['RSI'] = 100 - (100 / (1 + rs))

            result = self.analyze_trend(stock_df)
            raw = result.get('score', 0)
            max_s = result.get('max_score', 3) or 3
            pct = (raw / max_s) * 100

            if pct >= 66:
                signal = 'BUY'
            elif pct >= 33:
                signal = 'NEUTRAL'
            else:
                signal = 'SELL'

            return {
                'score': round(pct, 1),
                'signal': signal,
                'details': result.get('details', [])
            }
        except Exception as e:
            return {'score': 50, 'signal': 'NEUTRAL', 'details': [str(e)]}
