"""
Sentiment dataset preparation module.

This module handles loading, cleaning, and preparing financial news data
with sentiment labels for training sentiment analysis models.
"""

import logging
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
from pathlib import Path
from datetime import datetime

logger = logging.getLogger(__name__)


class SentimentDataPreparer:
    """
    Prepare and validate financial news sentiment dataset.
    
    This class handles:
    - Loading news datasets (CSV format)
    - Data cleaning and validation
    - Sentiment label processing
    - Stock ticker mapping
    - News aggregation by date and stock
    
    Attributes:
        data (pd.DataFrame): Raw news data
        processed_data (pd.DataFrame): Processed and validated data
    """
    
    def __init__(self, data_path: Optional[str] = None):
        """
        Initialize SentimentDataPreparer.
        
        Args:
            data_path: Path to news dataset CSV file (optional for now)
        """
        self.data = None
        self.processed_data = None
        self.data_path = data_path
        
        if data_path:
            self.load_data(data_path)
        
        logger.info("Initialized SentimentDataPreparer")
    
    def load_data(self, data_path: str) -> pd.DataFrame:
        """
        Load sentiment dataset from CSV file.
        
        Args:
            data_path: Path to CSV file
            
        Returns:
            Loaded DataFrame
            
        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If CSV format is invalid
        """
        path = Path(data_path)
        if not path.exists():
            raise FileNotFoundError(f"Data file not found: {data_path}")
        
        try:
            self.data = pd.read_csv(data_path, low_memory=False)
            logger.info(
                f"Loaded {len(self.data)} records from {data_path}, "
                f"columns: {list(self.data.columns)}"
            )
            return self.data
        except Exception as e:
            raise ValueError(f"Failed to load CSV: {str(e)}")
    
    def create_sample_data(self, n_records: int = 1000) -> pd.DataFrame:
        """
        Create sample sentiment data for demonstration.
        
        This is useful when actual news dataset is not available.
        
        Args:
            n_records: Number of sample records to generate
            
        Returns:
            Sample DataFrame
        """
        np.random.seed(42)
        
        tickers = ['AAPL', 'GOOGL', 'AMZN', 'MSFT', 'TSLA', 'META', 'NVDA', 'JPM']
        sentiments = [-1, 0, 1]  # Negative, Neutral, Positive
        
        dates = pd.date_range(start='2019-01-01', end='2024-12-31', freq='D')
        
        sample_headlines = {
            'negative': [
                'Market downturn affects tech stocks',
                'Company reports disappointing earnings',
                'Stock falls on negative outlook',
                'Regulatory concerns weigh on sector',
                'Production delays impact company',
                'Layoffs announced at tech firm',
                'Competitor gains market share',
            ],
            'neutral': [
                'Company releases quarterly report',
                'New product announcement made',
                'Management changes at firm',
                'Partnership agreement signed',
                'Stock split approved',
                'Dividend payment scheduled',
                'Conference to be held next month',
            ],
            'positive': [
                'Strong quarterly earnings surprise',
                'Company raises guidance for year',
                'Stock hits all-time high',
                'Analyst upgrades rating',
                'New product receives praise',
                'Market share gains reported',
                'Revenue growth exceeds expectations',
            ]
        }
        
        records = []
        for _ in range(n_records):
            sentiment = np.random.choice(sentiments)
            ticker = np.random.choice(tickers)
            date = np.random.choice(dates)
            
            if sentiment == -1:
                headline = np.random.choice(sample_headlines['negative'])
            elif sentiment == 0:
                headline = np.random.choice(sample_headlines['neutral'])
            else:
                headline = np.random.choice(sample_headlines['positive'])
            
            records.append({
                'Date': date,
                'Ticker': ticker,
                'Headline': headline,
                'Sentiment_Label': sentiment,
                'Source': 'Reuters'
            })
        
        self.data = pd.DataFrame(records)
        self.data['Date'] = pd.to_datetime(self.data['Date'])
        self.data = self.data.sort_values(['Ticker', 'Date']).reset_index(drop=True)
        
        logger.info(
            f"Created sample sentiment dataset with {len(self.data)} records"
        )
        return self.data
    
    def validate_columns(self, required_columns: List[str]) -> bool:
        """
        Validate that required columns exist.
        
        Args:
            required_columns: List of required column names
            
        Returns:
            True if all columns present, False otherwise
        """
        if self.data is None:
            logger.error("No data loaded")
            return False
        
        missing = set(required_columns) - set(self.data.columns)
        if missing:
            logger.warning(f"Missing columns: {missing}")
            return False
        
        logger.info("All required columns present")
        return True
    
    def clean_data(self) -> None:
        """
        Clean sentiment data.
        
        Removes:
        - Duplicate entries
        - Missing values in critical columns
        - Invalid dates
        """
        original_len = len(self.data)
        
        # Remove duplicates
        self.data = self.data.drop_duplicates(
            subset=['Date', 'Ticker', 'Headline'],
            keep='first'
        )
        duplicates_removed = original_len - len(self.data)
        
        # Convert Date column to datetime
        if 'Date' in self.data.columns:
            self.data['Date'] = pd.to_datetime(self.data['Date'], errors='coerce')
            invalid_dates = self.data['Date'].isna().sum()
            self.data = self.data[self.data['Date'].notna()]
            if invalid_dates > 0:
                logger.warning(f"Removed {invalid_dates} records with invalid dates")
        
        # Handle missing values
        critical_columns = ['Date', 'Ticker', 'Headline']
        for col in critical_columns:
            if col in self.data.columns:
                missing = self.data[col].isna().sum()
                if missing > 0:
                    self.data = self.data[self.data[col].notna()]
                    logger.warning(f"Removed {missing} records with missing {col}")
        
        # Clean text data
        if 'Headline' in self.data.columns:
            self.data['Headline'] = self.data['Headline'].str.strip()
            self.data = self.data[self.data['Headline'].str.len() > 0]
        
        # Reset index
        self.data = self.data.reset_index(drop=True)
        
        logger.info(
            f"Data cleaning complete. Removed {duplicates_removed + invalid_dates} records. "
            f"Remaining: {len(self.data)}"
        )
    
    def validate_sentiment_labels(self) -> Dict[str, int]:
        """
        Validate and report sentiment label distribution.
        
        Returns:
            Dictionary with label counts
        """
        if 'Sentiment_Label' not in self.data.columns:
            logger.warning("Sentiment_Label column not found")
            return {}
        
        label_counts = self.data['Sentiment_Label'].value_counts().to_dict()
        
        logger.info("Sentiment label distribution:")
        for label, count in sorted(label_counts.items()):
            percentage = 100 * count / len(self.data)
            logger.info(f"  Label {label}: {count} ({percentage:.1f}%)")
        
        return label_counts
    
    def map_tickers(self) -> Dict[str, int]:
        """
        Get ticker distribution in dataset.
        
        Returns:
            Dictionary with ticker counts
        """
        if 'Ticker' not in self.data.columns:
            logger.warning("Ticker column not found")
            return {}
        
        ticker_counts = self.data['Ticker'].value_counts().to_dict()
        
        logger.info("Ticker distribution:")
        for ticker, count in sorted(ticker_counts.items()):
            percentage = 100 * count / len(self.data)
            logger.info(f"  {ticker}: {count} articles ({percentage:.1f}%)")
        
        return ticker_counts
    
    def aggregate_by_date_ticker(self, sentiment_col: str = 'Sentiment_Label') -> pd.DataFrame:
        """
        Aggregate news to daily sentiment by stock.
        
        Args:
            sentiment_col: Column containing sentiment values
            
        Returns:
            Aggregated DataFrame with columns:
            - Date
            - Ticker
            - Sentiment_Score (mean sentiment)
            - News_Count (number of articles)
            - Sentiment_Std (sentiment volatility)
        """
        aggregated = self.data.groupby(['Date', 'Ticker']).agg({
            sentiment_col: ['mean', 'std', 'count'],
        }).reset_index()
        
        # Flatten column names
        aggregated.columns = ['Date', 'Ticker', 'Sentiment_Score', 'Sentiment_Std', 'News_Count']
        
        # Handle cases with single article (std = NaN)
        aggregated['Sentiment_Std'] = aggregated['Sentiment_Std'].fillna(0)
        
        logger.info(
            f"Aggregated to {len(aggregated)} date-ticker combinations"
        )
        
        return aggregated
    
    def generate_quality_report(self) -> Dict:
        """
        Generate comprehensive data quality report.
        
        Returns:
            Dictionary with quality metrics
        """
        if self.data is None or self.data.empty:
            return {}
        
        report = {
            'total_articles': len(self.data),
            'date_range': {
                'start': str(self.data['Date'].min()),
                'end': str(self.data['Date'].max()),
                'span_days': (self.data['Date'].max() - self.data['Date'].min()).days,
            },
            'unique_tickers': self.data['Ticker'].nunique(),
            'tickers': self.data['Ticker'].unique().tolist(),
            'missing_data': {
                col: self.data[col].isna().sum()
                for col in self.data.columns
            },
            'sentiment_distribution': self.data['Sentiment_Label'].value_counts().to_dict(),
            'articles_per_ticker': self.data['Ticker'].value_counts().to_dict(),
            'articles_per_day': {
                'mean': self.data.groupby('Date').size().mean(),
                'median': self.data.groupby('Date').size().median(),
                'max': self.data.groupby('Date').size().max(),
            },
        }
        
        return report
    
    def save_processed_data(self, output_path: str) -> None:
        """
        Save processed data to CSV.
        
        Args:
            output_path: Path to output CSV file
        """
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        self.data.to_csv(output_path, index=False)
        logger.info(f"Processed data saved to {output_path}")
    
    def process_pipeline(self) -> pd.DataFrame:
        """
        Execute full processing pipeline.
        
        Performs:
        1. Data cleaning
        2. Validation
        3. Report generation
        
        Returns:
            Processed DataFrame
        """
        if self.data is None:
            logger.error("No data loaded. Call load_data() or create_sample_data() first.")
            return None
        
        logger.info("Starting sentiment data processing pipeline...")
        
        self.clean_data()
        self.validate_sentiment_labels()
        self.map_tickers()
        report = self.generate_quality_report()
        
        logger.info("\n" + "="*60)
        logger.info("DATA QUALITY REPORT")
        logger.info("="*60)
        logger.info(f"Total articles: {report['total_articles']}")
        logger.info(f"Date range: {report['date_range']['start']} to {report['date_range']['end']}")
        logger.info(f"Unique tickers: {report['unique_tickers']}")
        logger.info(f"Articles per day (avg): {report['articles_per_day']['mean']:.1f}")
        
        self.processed_data = self.data.copy()
        return self.processed_data
    
    def __len__(self) -> int:
        """Return number of records."""
        return len(self.data) if self.data is not None else 0
    
    def __repr__(self) -> str:
        """String representation."""
        return (
            f"SentimentDataPreparer("
            f"records={len(self.data) if self.data is not None else 0}"
            f")"
        )


# Example usage
if __name__ == "__main__":
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Create preparer and generate sample data
    preparer = SentimentDataPreparer()
    preparer.create_sample_data(n_records=1000)
    
    # Process data
    processed = preparer.process_pipeline()
    
    # Save processed data
    preparer.save_processed_data('data/raw/sentiment_news.csv')
    
    # Generate aggregated sentiment
    aggregated = preparer.aggregate_by_date_ticker()
    aggregated.to_csv('data/processed/daily_sentiment_sample.csv', index=False)
    
    print(f"\n{preparer}")
    print(f"Processed shape: {processed.shape}")
    print(f"Aggregated shape: {aggregated.shape}")
