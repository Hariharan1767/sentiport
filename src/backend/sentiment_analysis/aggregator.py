"""
Sentiment aggregation module.
"""

import logging
import pandas as pd
import numpy as np
from typing import Optional, List, Dict
from pathlib import Path

from preprocessing.text_cleaner import TextPreprocessor
from sentiment_analysis.classifier import SentimentClassifier

logger = logging.getLogger(__name__)

class SentimentAggregator:
    """
    Aggregates news sentiment into daily signals for stocks.
    """
    
    def __init__(self, 
                 preprocessor: Optional[TextPreprocessor] = None,
                 classifier: Optional[SentimentClassifier] = None):
        """
        Initialize aggregator.
        
        Args:
            preprocessor: Initialized text preprocessor
            classifier: Trained sentiment classifier
        """
        self.preprocessor = preprocessor
        self.classifier = classifier
        
    def load_models(self, preprocessor_path: str, classifier_path: str):
        """Load preprocessor and classifier from disk."""
        self.preprocessor = TextPreprocessor.load(preprocessor_path)
        
        self.classifier = SentimentClassifier()
        self.classifier.load_model(classifier_path)
        
        logger.info("Models loaded successfully")
        
    def process_headlines(self, df: pd.DataFrame, 
                         text_col: str = 'Headline',
                         date_col: str = 'Date',
                         ticker_col: str = 'Ticker') -> pd.DataFrame:
        """
        Process new headlines and generate daily sentiments.
        
        Args:
            df: DataFrame containing news
            text_col: Name of column with text
            date_col: Name of column with dates
            ticker_col: Name of column withtickers
            
        Returns:
            DataFrame with daily aggregated sentiment
        """
        if self.preprocessor is None or self.classifier is None:
            raise RuntimeError("Models not initialized. Call load_models() first.")
            
        logger.info(f"Processing {len(df)} headlines...")
        
        # 1. Preprocess Text
        logger.info("Cleaning text...")
        clean_text = self.preprocessor.transform(df[text_col])
        
        # 2. Predict Sentiment
        logger.info("Predicting sentiment...")
        sentiment_scores = self.classifier.predict(clean_text)
        
        # Add scores to dataframe (copy to avoid warning)
        working_df = df.copy()
        working_df['Predicted_Sentiment'] = sentiment_scores
        
        # 3. Aggregate Daily
        logger.info("Aggregating daily scores...")
        daily_sentiment = working_df.groupby([date_col, ticker_col]).agg(
            Daily_Sentiment=('Predicted_Sentiment', 'mean'),
            Sentiment_Std=('Predicted_Sentiment', 'std'),
            News_Count=('Predicted_Sentiment', 'count'),
            Positive_Ratio=('Predicted_Sentiment', lambda x: (x > 0).mean()),
            Negative_Ratio=('Predicted_Sentiment', lambda x: (x < 0).mean())
        ).reset_index()
        
        # Fill NaNs in std (for single observations)
        daily_sentiment['Sentiment_Std'] = daily_sentiment['Sentiment_Std'].fillna(0)
        
        logger.info(f"Generated {len(daily_sentiment)} daily signals")
        return daily_sentiment

if __name__ == "__main__":
    # Test run
    from data_collection.sentiment_data import SentimentDataPreparer
    
    # 1. Setup Data
    print("Generating data...")
    prep = SentimentDataPreparer()
    df = prep.create_sample_data(100)
    
    # 2. Setup Models
    print("Training temp models...")
    cleaner = TextPreprocessor()
    df['clean'] = cleaner.transform(df['Headline'])
    
    clf = SentimentClassifier()
    clf.train(df['clean'], df['Sentiment_Label'], optimize=False)
    
    # 3. Aggregate
    print("Aggregating...")
    agg = SentimentAggregator(preprocessor=cleaner, classifier=clf)
    result = agg.process_headlines(df)
    
    print("\nResult:")
    print(result.head())
