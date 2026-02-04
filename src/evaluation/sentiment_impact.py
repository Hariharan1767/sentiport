"""
Sentiment Impact Analysis module.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

class SentimentImpactAnalyzer:
    """
    Analyzes the relationship between sentiment and market movements.
    """
    
    def calculate_correlations(self, stock_df: pd.DataFrame, sentiment_df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate correlation between Sentiment and Future Returns.
        """
        # Ensure proper indices
        # Expecting stock_df with Date, Ticker, Return_1d
        # Expecting sentiment_df with Date, Ticker, Daily_Sentiment
        
        merged = pd.merge(stock_df, sentiment_df, on=['Date', 'Ticker'], how='inner')
        
        results = []
        for ticker in merged['Ticker'].unique():
            df = merged[merged['Ticker'] == ticker]
            
            # Correlation with T+1 return
            corr_1d = df['Daily_Sentiment'].corr(df['Return_1d'].shift(-1))
            corr_5d = df['Daily_Sentiment'].corr(df['Return_1d'].rolling(5).sum().shift(-5))
            
            # Correlation with Volatility
            if 'Vol_21' in df.columns:
                corr_vol = df['Daily_Sentiment'].abs().corr(df['Vol_21'])
            else:
                corr_vol = np.nan
                
            results.append({
                'Ticker': ticker,
                'Corr_NextDay_Return': corr_1d,
                'Corr_NextWeek_Return': corr_5d,
                'Corr_SentimentAbs_Vol': corr_vol
            })
            
        return pd.DataFrame(results).set_index('Ticker')

    def event_study(self, stock_df: pd.DataFrame, sentiment_df: pd.DataFrame, 
                   threshold_quantile: float = 0.05, window: int = 5) -> Dict:
        """
        Analyze returns following extreme sentiment events.
        """
        merged = pd.merge(stock_df, sentiment_df, on=['Date', 'Ticker'], how='inner')
        
        # Define events
        # Top 5% positive sentiment
        pos_thresh = merged['Daily_Sentiment'].quantile(1 - threshold_quantile)
        neg_thresh = merged['Daily_Sentiment'].quantile(threshold_quantile)
        
        pos_events = merged[merged['Daily_Sentiment'] > pos_thresh]
        neg_events = merged[merged['Daily_Sentiment'] < neg_thresh]
        
        # Calculate post-event returns
        def get_post_event_return(events, full_df):
            cum_rets = []
            for idx, row in events.iterrows():
                # Find the window after this date for this ticker
                # This approach assumes indices align or we lookup by date, which is slow for huge data
                # Faster: Use integer indexing if sorted
                
                # Simplified: Filter by ticker and date > event data
                subset = full_df[(full_df['Ticker'] == row['Ticker']) & 
                               (full_df['Date'] > row['Date'])].head(window)
                
                if len(subset) == window:
                    cum_ret = (1 + subset['Return_1d']).cumprod().iloc[-1] - 1
                    cum_rets.append(cum_ret)
            return np.mean(cum_rets) if cum_rets else 0.0

        avg_ret_pos = get_post_event_return(pos_events, merged)
        avg_ret_neg = get_post_event_return(neg_events, merged)
        
        # Compare to baseline (random sample)
        baseline_ret = merged['Return_1d'].rolling(window).apply(lambda x: np.prod(1+x)-1).mean()
        
        return {
            'Positive_Event_Return': avg_ret_pos,
            'Negative_Event_Return': avg_ret_neg,
            'Baseline_Return': baseline_ret,
            'Sentiment_Spread': avg_ret_pos - avg_ret_neg
        }

if __name__ == "__main__":
    # Test
    # Generate data
    dates = pd.date_range('2023-01-01', periods=100)
    data = pd.DataFrame({
        'Date': np.tile(dates, 2),
        'Ticker': np.repeat(['A', 'B'], 100),
        'Return_1d': np.random.normal(0, 0.01, 200),
        'Vol_21': 0.02
    })
    sent = pd.DataFrame({
        'Date': np.tile(dates, 2),
        'Ticker': np.repeat(['A', 'B'], 100),
        'Daily_Sentiment': np.random.normal(0, 1, 200)
    })
    
    analyzer = SentimentImpactAnalyzer()
    print("Correlations:\n", analyzer.calculate_correlations(data, sent))
    print("\nEvent Study:\n", analyzer.event_study(data, sent))
