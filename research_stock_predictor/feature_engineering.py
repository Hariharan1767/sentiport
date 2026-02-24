import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from typing import Tuple, List

class MultiModalFeatureEngineer:
    """
    Handles scaling and windowing of price, technical, and sentiment features.
    """
    def __init__(self, window_size: int = 14):
        self.window_size = window_size
        self.price_scaler = MinMaxScaler()
        self.sentiment_scaler = MinMaxScaler()
        # Features to be windowed for LSTM
        self.price_features = ['Close', 'Volume', 'Return', 'SMA_7', 'SMA_14', 'RSI', 'MACD']
        # Sentiment features (could be windowed or treated separately)
        self.sentiment_features = ['daily_sentiment', 'rolling_sentiment_7d', 'sentiment_volatility_7d']

    def engineer_base_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Adds daily return and SMA if not present."""
        df = df.copy()
        df['Return'] = df['Close'].pct_change().fillna(0)
        df['SMA_7'] = df['Close'].rolling(window=7).mean().fillna(method='bfill')
        df['SMA_14'] = df['Close'].rolling(window=14).mean().fillna(method='bfill')
        
        # Ensure RSI and MACD exist (placeholders if API failed)
        if 'RSI' not in df.columns: df['RSI'] = 50.0 
        if 'MACD' not in df.columns: df['MACD'] = 0.0
            
        return df

    def prepare_data(self, df: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Normalizes data and creates temporal windows.
        Returns:
            X_price: (samples, window_size, price_feature_count)
            X_sentiment: (samples, sentiment_feature_count) - or (samples, window_size, sent_feat_count)
            y: (samples, 1) - Target (next day close)
        """
        # 1. Scaling
        df = df.copy()
        df[self.price_features] = self.price_scaler.fit_transform(df[self.price_features])
        df[self.sentiment_features] = self.sentiment_scaler.fit_transform(df[self.sentiment_features])
        
        # 2. Windowing
        X_p, X_s, y = [], [], []
        
        # We want to predict Target Close (shifted by 1)
        df['Target'] = df['Close'].shift(-1)
        # Drop last row since target is unknown
        df_cleaned = df.dropna(subset=['Target'])
        
        values_p = df_cleaned[self.price_features].values
        values_s = df_cleaned[self.sentiment_features].values
        target = df_cleaned['Target'].values
        
        for i in range(self.window_size, len(df_cleaned)):
            X_p.append(values_p[i-self.window_size:i])
            # For Hybrid Model B: we can take the last window's sentiment or a windowed sentiment
            # Research requirement says "Hybrid Model: Dense layer for sentiment features"
            # This implies a static vector for the current window's context
            X_s.append(values_s[i-1]) # Sentiment features for the most recent day in the window
            y.append(target[i-1]) # Predicting the close of day 'i'
            
        return np.array(X_p), np.array(X_s), np.array(y)

if __name__ == "__main__":
    # Test
    engineer = MultiModalFeatureEngineer(window_size=5)
    mock_df = pd.DataFrame({
        'Close': np.random.rand(20),
        'Volume': np.random.rand(20),
        'daily_sentiment': np.random.rand(20),
        'rolling_sentiment_7d': np.random.rand(20),
        'sentiment_volatility_7d': np.random.rand(20)
    })
    mock_df = engineer.engineer_base_features(mock_df)
    Xp, Xs, y = engineer.prepare_data(mock_df)
    print(f"X_price shape: {Xp.shape}")
    print(f"X_sentiment shape: {Xs.shape}")
    print(f"y shape: {y.shape}")
