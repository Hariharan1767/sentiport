"""
Feature engineering module for portfolio optimization.
Combines stock price data with sentiment data and generates predictive features.
"""

import logging
import pandas as pd
import numpy as np
from typing import Tuple, List, Optional

logger = logging.getLogger(__name__)

class FeatureEngineer:
    """
    Generates features for return prediction models.
    """
    
    def __init__(self, use_technical: bool = True, use_sentiment: bool = True):
        self.use_technical = use_technical
        self.use_sentiment = use_sentiment
        self.feature_columns = []
        
    def create_technical_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Generate technical indicators.
        """
        df = df.copy()
        
        # 1. Returns and Lags
        df['Return_1d'] = df.groupby('Ticker')['Close'].pct_change()
        
        for lag in [1, 3, 5, 10]:
            df[f'Return_Lag{lag}'] = df.groupby('Ticker')['Return_1d'].shift(lag)
            
        # 2. Moving Averages
        for window in [5, 10, 20, 50]:
            df[f'SMA_{window}'] = df.groupby('Ticker')['Close'].transform(
                lambda x: x.rolling(window=window).mean()
            )
            df[f'Dist_to_SMA_{window}'] = (df['Close'] / df[f'SMA_{window}']) - 1
            
        # 3. Volatility (Historical)
        for window in [10, 21, 63]:
            df[f'Vol_{window}'] = df.groupby('Ticker')['Return_1d'].transform(
                lambda x: x.rolling(window=window).std()
            )
            
        # 4. RSI (Simple approximation)
        def calculate_rsi(data, window=14):
            delta = data.diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
            rs = gain / loss
            return 100 - (100 / (1 + rs))

        df['RSI_14'] = df.groupby('Ticker')['Close'].transform(lambda x: calculate_rsi(x))
        
        return df

    def create_sentiment_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Generate sentiment-derived features.
        """
        if 'Daily_Sentiment' not in df.columns:
            logger.warning("Daily_Sentiment column missing. Skipping sentiment features.")
            return df
            
        df = df.copy()
        
        # 1. Fill missing sentiment (forward fill then 0)
        df['Daily_Sentiment'] = df.groupby('Ticker')['Daily_Sentiment'].ffill().fillna(0)
        df['Sentiment_Std'] = df.groupby('Ticker')['Sentiment_Std'].ffill().fillna(0)
        
        # 2. Sentiment Lags and Momentum
        for lag in [1, 3, 5]:
            df[f'Sentiment_Lag{lag}'] = df.groupby('Ticker')['Daily_Sentiment'].shift(lag)
            
        df['Sentiment_Momentum_5d'] = df['Daily_Sentiment'] - df.groupby('Ticker')['Daily_Sentiment'].shift(5)
        
        # 3. Interaction Terms (Sentiment * Volatility)
        # Hypothesis: Sentiment matters more when volatility is high? Or low?
        if 'Vol_21' in df.columns:
            df['Sentiment_x_Vol'] = df['Daily_Sentiment'] * df['Vol_21']
            
        return df

    def prepare_data(self, stock_df: pd.DataFrame, 
                    sentiment_df: Optional[pd.DataFrame] = None) -> pd.DataFrame:
        """
        Main pipeline to merge and feature engineer data.
        """
        logger.info("Starting feature engineering...")
        
        # 1. Merge Data
        if sentiment_df is not None:
            # Ensure dates are datetime
            stock_df['Date'] = pd.to_datetime(stock_df['Date'])
            sentiment_df['Date'] = pd.to_datetime(sentiment_df['Date'])
            
            # Merge left (keep all stock days)
            df = pd.merge(stock_df, sentiment_df, on=['Date', 'Ticker'], how='left')
            
            # Fill missing sentiment with 0 (neutral) for days with no news
            df['Daily_Sentiment'] = df['Daily_Sentiment'].fillna(0)
            df['Sentiment_Std'] = df['Sentiment_Std'].fillna(0)
            df['News_Count'] = df['News_Count'].fillna(0)
        else:
            df = stock_df.copy()
            
        # 2. Create Features
        if self.use_technical:
            df = self.create_technical_features(df)
            
        if self.use_sentiment and sentiment_df is not None:
            df = self.create_sentiment_features(df)  
            
        # 3. Create Target (Next Day Return)
        df['Target_Return'] = df.groupby('Ticker')['Return_1d'].shift(-1)
        
        # 4. Cleanup
        # Remove rows with NaN features or target (due to lags/shifts)
        # Need to be modifying feature_columns list to know what to use for training later
        self.feature_columns = [c for c in df.columns if c not in 
                                ['Date', 'Ticker', 'Target_Return', 'Open', 'High', 'Low', 'Close', 'Volume', 'Adj Close']]
        
        initial_len = len(df)
        df = df.dropna()
        logger.info(f"Dropped {initial_len - len(df)} rows due to NaN (lags/rolling windows).")
        
        logger.info(f"Final dataset shape: {df.shape}")
        return df

    def split_data(self, df: pd.DataFrame, train_ratio: float = 0.7, val_ratio: float = 0.15):
        """
        Time-series split of data.
        """
        dates = df['Date'].sort_values().unique()
        n_dates = len(dates)
        
        train_end_idx = int(n_dates * train_ratio)
        val_end_idx = int(n_dates * (train_ratio + val_ratio))
        
        train_date_end = dates[train_end_idx]
        val_date_end = dates[val_end_idx]
        
        train_df = df[df['Date'] <= train_date_end]
        val_df = df[(df['Date'] > train_date_end) & (df['Date'] <= val_date_end)]
        test_df = df[df['Date'] > val_date_end]
        
        return train_df, val_df, test_df

if __name__ == "__main__":
    # Test run
    # Mock stock data
    dates = pd.date_range('2023-01-01', periods=100)
    stock_df = pd.DataFrame({
        'Date': dates,
        'Ticker': 'AAPL',
        'Close': np.random.normal(150, 5, 100),
        'Volume': 1000
    })
    
    # Mock sentiment data (sparse)
    sent_df = pd.DataFrame({
        'Date': dates[::5], # Every 5th day
        'Ticker': 'AAPL',
        'Daily_Sentiment': np.random.uniform(-1, 1, 20),
        'Sentiment_Std': 0.1,
        'News_Count': 1
    })
    
    eng = FeatureEngineer()
    full_df = eng.prepare_data(stock_df, sent_df)
    
    print("Features:", eng.feature_columns)
    print("Data Head:\n", full_df.head())
