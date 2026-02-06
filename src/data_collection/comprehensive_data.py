import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from src.utils import technical_indicators as ta

class ComprehensiveDataLoader:
    def __init__(self):
        """
        Initializes the data loader.
        """
        pass

    def fetch_fundamentals(self, ticker: str):
        """
        Fetches fundamental data: Income Sheet, Balance Sheet, Cash Flow.
        """
        try:
            stock = yf.Ticker(ticker)
            
            # 1. Company Fundamentals - access info cautiously
            info = getattr(stock, 'info', {})
            if not info or not isinstance(info, dict):
                print(f"Warning: No info found for {ticker}")
                info = {}
            
            earnings_growth = info.get('earningsGrowth')
            revenue_growth = info.get('revenueGrowth')
            margins = {
                'grossMargins': info.get('grossMargins'),
                'operatingMargins': info.get('operatingMargins'),
                'profitMargins': info.get('profitMargins')
            }
            
            # Use getattr for dataframes to avoid 'Failed to get ticker' hard stops if possible
            cash_flow = getattr(stock, 'cashflow', pd.DataFrame())
            income_stmt = getattr(stock, 'income_stmt', pd.DataFrame())
            balance_sheet = getattr(stock, 'balance_sheet', pd.DataFrame())

            debt_to_equity = info.get('debtToEquity')
            
            # 2. Valuation Metrics
            valuation = {
                'forwardPE': info.get('forwardPE'),
                'trailingPE': info.get('trailingPE'),
                'priceToBook': info.get('priceToBook'),
                'pegRatio': info.get('pegRatio'),
                'dividendYield': info.get('dividendYield')
            }

            # 3. Industry & Market Position
            industry_data = {
                'sector': info.get('sector'),
                'industry': info.get('industry'),
                'marketCap': info.get('marketCap'),
                'beta': info.get('beta')
            }

            return {
                'info': info,
                'valuation': valuation,
                'growth': {
                    'earnings_growth': earnings_growth,
                    'revenue_growth': revenue_growth
                },
                'margins': margins,
                'debt': debt_to_equity,
                'industry': industry_data,
                'financials_dfs': {
                    'cash_flow': cash_flow,
                    'income_stmt': income_stmt,
                    'balance_sheet': balance_sheet
                }
            }
        except Exception as e:
            print(f"Error fetching fundamentals for {ticker}: {e}")
            return None

    def fetch_technicals(self, ticker: str, period="1y", interval="1d"):
        """
        Fetches historical price data and calculates technical indicators.
        """
        try:
            # download can return multi-index
            df = yf.download(ticker, period=period, interval=interval, progress=False)
            if df is None or df.empty:
                print(f"Warning: No technical data for {ticker}")
                return None
            
            # Flatten MultiIndex if necessary
            if isinstance(df.columns, pd.MultiIndex):
                # Usually level 0 is price type (Open, Close, etc)
                df.columns = df.columns.get_level_values(0)

            # Ensure necessary columns exist for indicators
            if 'Close' not in df.columns:
                print(f"Warning: 'Close' column missing for {ticker}")
                return df

            # Simple Moving Averages
            df['SMA_50'] = ta.sma(df['Close'], length=50)
            df['SMA_200'] = ta.sma(df['Close'], length=200)
            
            # RSI
            df['RSI'] = ta.rsi(df['Close'], length=14)
            
            # MACD
            macd_df = ta.macd(df['Close'])
            df = pd.concat([df, macd_df], axis=1)
            
            # Bollinger Bands
            bb_df = ta.bbands(df['Close'], length=20)
            df = pd.concat([df, bb_df], axis=1)
            
            # ATR
            if all(col in df.columns for col in ['High', 'Low', 'Close']):
                df['ATR'] = ta.atr(df['High'], df['Low'], df['Close'], length=14)

            return df
        except Exception as e:
            print(f"Error fetching technicals for {ticker}: {e}")
            return None

    def fetch_macro_data(self):
        """
        Fetches macro economic indicators: Treasury Yields, VIX.
        """
        try:
            tickers = ['^TNX', '^VIX', 'GC=F']
            data = yf.download(tickers, period="1y", interval="1d", progress=False)
            
            if isinstance(data.columns, pd.MultiIndex):
                # For multiple tickers, we want the 'Close' prices
                data = data['Close']
                
            return data
        except Exception as e:
            print(f"Error fetching macro data: {e}")
            return None
    
    def get_full_analysis_data(self, ticker: str):
        """
        Aggregates all data for comprehensive 9-factor analysis.
        """
        fundamentals = self.fetch_fundamentals(ticker)
        technicals = self.fetch_technicals(ticker)
        macro = self.fetch_macro_data()
        
        return {
            'fundamentals': fundamentals,
            'technicals': technicals,
            'macro': macro,
            'ticker': ticker
        }

if __name__ == "__main__":
    loader = ComprehensiveDataLoader()
    data = loader.get_full_analysis_data("AAPL")
    if data['fundamentals']:
        print("Fundamentals Info found:", "longName" in data['fundamentals']['info'])
    if data['technicals'] is not None:
        print("Technicals Shape:", data['technicals'].shape)

