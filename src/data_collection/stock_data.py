"""
Stock price data collection module.

This module handles downloading historical stock price data from Yahoo Finance,
data validation, and feature engineering for technical analysis.
"""

import logging
import pandas as pd
import numpy as np
import yfinance as yf
from typing import List, Dict, Tuple, Optional
from datetime import datetime, timedelta
from pathlib import Path
import warnings

warnings.filterwarnings('ignore')

logger = logging.getLogger(__name__)


class StockDataCollector:
    """
    Download and process historical stock price data.
    
    This class handles:
    - Downloading data from Yahoo Finance
    - Data quality validation
    - Missing data handling
    - Technical feature calculation (returns, volatility)
    
    Attributes:
        tickers (List[str]): List of stock tickers to download
        start_date (str): Start date in YYYY-MM-DD format
        end_date (str): End date in YYYY-MM-DD format
        data (Dict[str, pd.DataFrame]): Downloaded price data by ticker
    """
    
    def __init__(
        self,
        tickers: List[str],
        start_date: str,
        end_date: str,
        interval: str = "1d"
    ):
        """
        Initialize StockDataCollector.
        
        Args:
            tickers: List of stock ticker symbols (e.g., ['AAPL', 'GOOGL'])
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            interval: Data interval ('1d' for daily, '1h' for hourly, etc.)
            
        Raises:
            ValueError: If date range is invalid
        """
        self.tickers = tickers
        self.start_date = start_date
        self.end_date = end_date
        self.interval = interval
        self.data = {}
        
        # Validate dates
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        
        if start >= end:
            raise ValueError(
                f"start_date ({start_date}) must be before end_date ({end_date})"
            )
        
        logger.info(
            f"Initialized StockDataCollector for {len(tickers)} tickers, "
            f"period: {start_date} to {end_date}"
        )
    
    def download(self, progress: bool = True) -> Dict[str, pd.DataFrame]:
        """
        Download stock price data from Yahoo Finance.
        
        Args:
            progress: Whether to show download progress
            
        Returns:
            Dictionary with ticker as key and DataFrame as value
            
        Raises:
            Exception: If download fails for all tickers
        """
        logger.info(f"Starting download for {len(self.tickers)} tickers...")
        
        successful = 0
        failed_tickers = []
        
        for ticker in self.tickers:
            try:
                logger.debug(f"Downloading {ticker}...")
                
                data = yf.download(
                    ticker,
                    start=self.start_date,
                    end=self.end_date,
                    interval=self.interval,
                    progress=False
                )
                
                if data.empty:
                    logger.warning(f"No data downloaded for {ticker}")
                    failed_tickers.append(ticker)
                    continue
                
                # Ensure proper column names
                data.columns = ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
                data['Ticker'] = ticker
                
                self.data[ticker] = data
                successful += 1
                logger.info(f"✓ Downloaded {ticker} ({len(data)} records)")
                
            except Exception as e:
                logger.error(f"Failed to download {ticker}: {str(e)}")
                failed_tickers.append(ticker)
        
        if successful == 0:
            raise Exception(
                f"Failed to download data for all tickers. "
                f"Check internet connection and ticker symbols."
            )
        
        logger.info(
            f"Download complete: {successful}/{len(self.tickers)} successful"
        )
        
        if failed_tickers:
            logger.warning(f"Failed tickers: {failed_tickers}")
        
        return self.data
    
    def calculate_returns(self) -> None:
        """
        Calculate daily returns for all tickers.
        
        Adds 'Daily_Return' column to each DataFrame.
        """
        for ticker, df in self.data.items():
            df['Daily_Return'] = df['Adj Close'].pct_change()
            logger.debug(f"Calculated returns for {ticker}")
    
    def calculate_volatility(self, window: int = 21) -> None:
        """
        Calculate rolling volatility.
        
        Args:
            window: Rolling window size in days (default: 21 trading days = 1 month)
        """
        for ticker, df in self.data.items():
            df[f'Volatility_{window}d'] = (
                df['Daily_Return'].rolling(window=window).std() * np.sqrt(252)
            )  # Annualize volatility
            logger.debug(
                f"Calculated {window}-day rolling volatility for {ticker}"
            )
    
    def handle_missing_data(self, method: str = "forward_fill") -> None:
        """
        Handle missing values in data.
        
        Args:
            method: Handling method ('forward_fill', 'backward_fill', 'interpolate')
        """
        for ticker, df in self.data.items():
            original_missing = df.isna().sum().sum()
            
            if method == "forward_fill":
                df.fillna(method='ffill', inplace=True)
            elif method == "backward_fill":
                df.fillna(method='bfill', inplace=True)
            elif method == "interpolate":
                df.interpolate(method='linear', inplace=True)
            
            df.fillna(method='bfill', inplace=True)  # Fill any remaining
            
            new_missing = df.isna().sum().sum()
            if original_missing > 0:
                logger.info(
                    f"{ticker}: Fixed {original_missing} missing values "
                    f"({original_missing-new_missing} resolved)"
                )
    
    def validate_data(self) -> Dict[str, Dict]:
        """
        Validate data quality for all tickers.
        
        Returns:
            Dictionary with validation metrics for each ticker
        """
        validation_report = {}
        
        for ticker, df in self.data.items():
            report = {
                'total_records': len(df),
                'missing_values': df.isna().sum().to_dict(),
                'price_range': {
                    'min': df['Close'].min(),
                    'max': df['Close'].max(),
                },
                'volume_stats': {
                    'mean': df['Volume'].mean(),
                    'median': df['Volume'].median(),
                    'std': df['Volume'].std(),
                },
                'return_stats': {
                    'mean': df['Daily_Return'].mean(),
                    'std': df['Daily_Return'].std(),
                    'min': df['Daily_Return'].min(),
                    'max': df['Daily_Return'].max(),
                    'skewness': df['Daily_Return'].skew(),
                    'kurtosis': df['Daily_Return'].kurtosis(),
                },
                'duplicates': df.index.duplicated().sum(),
            }
            
            validation_report[ticker] = report
            
            # Log warnings for data quality issues
            if report['duplicates'] > 0:
                logger.warning(
                    f"{ticker}: Found {report['duplicates']} duplicate records"
                )
            
            total_missing = sum(report['missing_values'].values())
            if total_missing > 0:
                logger.warning(
                    f"{ticker}: {total_missing} missing values found"
                )
        
        logger.info("Data validation complete")
        return validation_report
    
    def combine_data(self, on: str = "Date") -> pd.DataFrame:
        """
        Combine data from all tickers into a single DataFrame.
        
        Args:
            on: Column to merge on ('Date' or 'Ticker')
            
        Returns:
            Combined DataFrame with all tickers
        """
        if not self.data:
            raise ValueError("No data to combine. Run download() first.")
        
        combined_dfs = []
        for ticker, df in self.data.items():
            df_copy = df.copy()
            df_copy.reset_index(inplace=True)
            df_copy['Ticker'] = ticker
            combined_dfs.append(df_copy)
        
        combined = pd.concat(combined_dfs, ignore_index=True)
        combined['Date'] = pd.to_datetime(combined['Date'])
        combined = combined.sort_values(['Ticker', 'Date'])
        
        logger.info(f"Combined data shape: {combined.shape}")
        return combined
    
    def save_to_csv(self, output_path: str) -> None:
        """
        Save combined data to CSV file.
        
        Args:
            output_path: Path to output CSV file
        """
        combined = self.combine_data()
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        combined.to_csv(output_path, index=False)
        logger.info(f"Data saved to {output_path}")
    
    def get_summary_statistics(self) -> pd.DataFrame:
        """
        Get summary statistics for all tickers.
        
        Returns:
            DataFrame with summary statistics
        """
        summary_data = []
        
        for ticker, df in self.data.items():
            summary = {
                'Ticker': ticker,
                'Records': len(df),
                'Start_Date': df.index.min(),
                'End_Date': df.index.max(),
                'Avg_Close': df['Close'].mean(),
                'Avg_Volume': df['Volume'].mean(),
                'Avg_Return': df['Daily_Return'].mean(),
                'Volatility': df['Daily_Return'].std(),
                'Sharpe_Ratio': (df['Daily_Return'].mean() / df['Daily_Return'].std() * np.sqrt(252))
                if df['Daily_Return'].std() > 0 else 0,
            }
            summary_data.append(summary)
        
        return pd.DataFrame(summary_data)
    
    def __len__(self) -> int:
        """Return number of tickers with data."""
        return len(self.data)
    
    def __repr__(self) -> str:
        """String representation."""
        return (
            f"StockDataCollector("
            f"tickers={len(self.tickers)}, "
            f"downloaded={len(self.data)}, "
            f"period={self.start_date} to {self.end_date}"
            f")"
        )


# Example usage
if __name__ == "__main__":
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Create collector
    collector = StockDataCollector(
        tickers=['AAPL', 'GOOGL', 'AMZN'],
        start_date='2023-01-01',
        end_date='2024-12-31'
    )
    
    # Download data
    collector.download()
    
    # Calculate features
    collector.calculate_returns()
    collector.calculate_volatility(window=21)
    
    # Handle missing data
    collector.handle_missing_data(method='forward_fill')
    
    # Validate data
    validation = collector.validate_data()
    
    # Get summary
    summary = collector.get_summary_statistics()
    print("\n" + "="*60)
    print("STOCK DATA SUMMARY")
    print("="*60)
    print(summary)
    
    # Save combined data
    collector.save_to_csv('data/raw/stock_prices.csv')
    
    print(f"\n{collector}")
