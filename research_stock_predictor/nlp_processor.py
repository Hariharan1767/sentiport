import pandas as pd
import numpy as np
from textblob import TextBlob
from typing import List, Dict

class SentimentProcessor:
    """
    Processes news articles to generate daily sentiment signals.
    """
    def __init__(self):
        pass

    def compute_sentiment(self, text: str) -> float:
        """Simple sentiment scoring using TextBlob."""
        if not text or not isinstance(text, str):
            return 0.0
        return TextBlob(text).sentiment.polarity

    def process_news_dataframe(self, news_df: pd.DataFrame) -> pd.DataFrame:
        """
        Takes a news DataFrame (from Finnhub) and aggregates daily sentiment.
        Expected columns: 'headline', 'summary', 'datetime'.
        """
        if news_df.empty:
            return pd.DataFrame(columns=['date', 'daily_sentiment', 'sentiment_count'])

        # Combine headline and summary for richer sentiment analysis
        news_df['text'] = news_df['headline'].fillna('') + " " + news_df['summary'].fillna('')
        
        # Compute sentiment polarity for each article
        news_df['sentiment'] = news_df['text'].apply(self.compute_sentiment)
        
        # Extract date from datetime
        news_df['date'] = pd.to_datetime(news_df['datetime']).dt.date
        
        # Aggregate by day
        daily_sentiment = news_df.groupby('date').agg(
            daily_sentiment=('sentiment', 'mean'),
            sentiment_count=('sentiment', 'count')
        ).reset_index()
        
        return daily_sentiment

    def align_sentiment_with_prices(self, price_df: pd.DataFrame, sentiment_df: pd.DataFrame) -> pd.DataFrame:
        """
        Aligns the daily sentiment signals with the stock price timeline.
        Fills missing sentiment days with 0 (neutral) and computes rolling averages.
        """
        # Ensure indices/columns are datetime
        price_df.index = pd.to_datetime(price_df.index).date
        sentiment_df['date'] = pd.to_datetime(sentiment_df['date']).dt.date
        sentiment_df.set_index('date', inplace=True)
        
        # Reindex sentiment to match price dates
        merged_df = price_df.copy()
        merged_df = merged_df.merge(sentiment_df, left_index=True, right_index=True, how='left')
        
        # Fill missing sentiment with neutral (0)
        merged_df['daily_sentiment'] = merged_df['daily_sentiment'].fillna(0)
        merged_df['sentiment_count'] = merged_df['sentiment_count'].fillna(0)
        
        # Compute Rolling Sentiment Index (7-day window)
        merged_df['rolling_sentiment_7d'] = merged_df['daily_sentiment'].rolling(window=7, min_periods=1).mean()
        
        # Compute Rolling Sentiment Volatility
        merged_df['sentiment_volatility_7d'] = merged_df['daily_sentiment'].rolling(window=7, min_periods=1).std().fillna(0)
        
        return merged_df

if __name__ == "__main__":
    # Mock data for testing
    processor = SentimentProcessor()
    mock_news = pd.DataFrame([
        {'headline': 'Great earnings!', 'summary': 'Company did well', 'datetime': '2024-01-01'},
        {'headline': 'Market crash', 'summary': 'Bad news everywhere', 'datetime': '2024-01-01'},
        {'headline': 'Growth remains steady', 'summary': 'Stable outlook', 'datetime': '2024-01-02'}
    ])
    daily = processor.process_news_dataframe(mock_news)
    print("Daily Sentiment:")
    print(daily)
