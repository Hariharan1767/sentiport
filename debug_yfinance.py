
import yfinance as yf
import pandas as pd

def debug_ticker(ticker_symbol):
    print(f"--- Debugging {ticker_symbol} ---")
    ticker = yf.Ticker(ticker_symbol)
    
    print("\n1. Info:")
    info = ticker.info
    print(f"Type of info: {type(info)}")
    print(f"Company: {info.get('longName', 'N/A')}")
    print(f"Current Price: {info.get('currentPrice', 'N/A')}")
    
    print("\n2. History (Technicals):")
    hist = ticker.history(period="1y")
    print(f"Columns: {hist.columns}")
    print(f"Is MultiIndex: {isinstance(hist.columns, pd.MultiIndex)}")
    print(f"Head:\n{hist.head(2)}")
    
    print("\n3. Download (Technicals):")
    df = yf.download(ticker_symbol, period="1y", progress=False)
    print(f"Columns: {df.columns}")
    print(f"Is MultiIndex: {isinstance(df.columns, pd.MultiIndex)}")
    print(f"Head:\n{df.head(2)}")

    print("\n4. Financials:")
    print(f"Cashflow empty? {ticker.cashflow.empty}")
    if not ticker.cashflow.empty:
        print(f"Cashflow index:\n{ticker.cashflow.index[:5]}")

if __name__ == "__main__":
    debug_ticker("AAPL")
