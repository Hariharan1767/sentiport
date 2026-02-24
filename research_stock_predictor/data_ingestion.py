import os
import requests
import pandas as pd
import time
from datetime import datetime, timedelta
from typing import Optional, List, Dict
from dotenv import load_dotenv

load_dotenv()

class AlphaVantageIngestor:
    """
    Handles data ingestion from Alpha Vantage for historical prices and technical indicators.
    """
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("ALPHA_VANTAGE_API_KEY")
        self.base_url = "https://www.alphavantage.co/query"
        if not self.api_key:
            print("Warning: Alpha Vantage API Key not found.")

    def _fetch(self, params: Dict) -> Dict:
        params["apikey"] = self.api_key
        response = requests.get(self.base_url, params=params)
        data = response.json()
        
        if "Note" in data:
            print(f"API Rate Limit Hit: {data['Note']}")
            time.sleep(60) # Simple backoff
            return self._fetch(params)
            
        if "Error Message" in data:
            raise ValueError(f"Alpha Vantage Error: {data['Error Message']}")
            
        return data

    def fetch_daily_prices(self, ticker: str, full: bool = False) -> pd.DataFrame:
        """Fetch daily OHLCV data."""
        params = {
            "function": "TIME_SERIES_DAILY",
            "symbol": ticker,
            "outputsize": "full" if full else "compact"
        }
        data = self._fetch(params)
        time_series = data.get("Time Series (Daily)", {})
        df = pd.DataFrame.from_dict(time_series, orient="index").astype(float)
        df.index = pd.to_datetime(df.index)
        df.sort_index(inplace=True)
        # Rename columns to standard format
        df.columns = [c.split(". ")[1].capitalize() for c in df.columns]
        return df

    def fetch_indicator(self, ticker: str, function: str, interval: str = "daily", time_period: int = 14) -> pd.DataFrame:
        """Fetch technical indicators like RSI, SMA, EMA, MACD."""
        params = {
            "function": function,
            "symbol": ticker,
            "interval": interval,
            "time_period": time_period,
            "series_type": "close"
        }
        data = self._fetch(params)
        key = list(data.keys())[1] # Usually 'Technical Analysis: RSI' etc.
        df = pd.DataFrame.from_dict(data[key], orient="index").astype(float)
        df.index = pd.to_datetime(df.index)
        df.sort_index(inplace=True)
        return df

class FinnhubIngestor:
    """
    Handles data ingestion from Finnhub for news and sentiment.
    """
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("FINNHUB_API_KEY")
        self.base_url = "https://finnhub.io/api/v1"
        if not self.api_key:
            print("Warning: Finnhub API Key not found.")

    def fetch_company_news(self, ticker: str, days_back: int = 30) -> pd.DataFrame:
        """Fetch news articles for a specific ticker."""
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')
        
        url = f"{self.base_url}/company-news"
        params = {
            "symbol": ticker,
            "from": start_date,
            "to": end_date,
            "token": self.api_key
        }
        response = requests.get(url, params=params)
        data = response.json()
        
        if not isinstance(data, list):
            print(f"Finnhub Error: {data}")
            return pd.DataFrame()
            
        df = pd.DataFrame(data)
        if not df.empty:
            df['datetime'] = pd.to_datetime(df['datetime'], unit='s')
            df.sort_values('datetime', inplace=True)
        return df

    def fetch_news_sentiment(self, ticker: str) -> Dict:
        """Fetch sentiment statistics for a specific ticker."""
        url = f"{self.base_url}/news-sentiment"
        params = {
            "symbol": ticker,
            "token": self.api_key
        }
        response = requests.get(url, params=params)
        return response.json()

if __name__ == "__main__":
    # Quick test if keys are present
    av = AlphaVantageIngestor()
    fh = FinnhubIngestor()
    print("Ingestors initialized.")
