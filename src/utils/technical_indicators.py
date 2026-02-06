
import pandas as pd
import numpy as np

def sma(series, length):
    return series.rolling(window=length).mean()

def rsi(series, length=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=length).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=length).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def macd(series, fast=12, slow=26, signal=9):
    ema_fast = series.ewm(span=fast, adjust=False).mean()
    ema_slow = series.ewm(span=slow, adjust=False).mean()
    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    histogram = macd_line - signal_line
    return pd.DataFrame({
        f'MACD_{fast}_{slow}_{signal}': macd_line,
        f'MACDs_{fast}_{slow}_{signal}': signal_line,
        f'MACDh_{fast}_{slow}_{signal}': histogram
    })

def bbands(series, length=20, std=2):
    ma = series.rolling(window=length).mean()
    sd = series.rolling(window=length).std()
    upper = ma + (std * sd)
    lower = ma - (std * sd)
    return pd.DataFrame({
        f'BBU_{length}_{std}.0': upper,
        f'BBM_{length}_{std}.0': ma,
        f'BBL_{length}_{std}.0': lower
    })

def atr(high, low, close, length=14):
    tr1 = high - low
    tr2 = abs(high - close.shift())
    tr3 = abs(low - close.shift())
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    return tr.rolling(window=length).mean()
