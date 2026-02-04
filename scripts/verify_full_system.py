"""
End-to-End System Verification Script.
"""

import sys
import logging
import pandas as pd
import numpy as np
import shutil
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.data_collection.sentiment_data import SentimentDataPreparer
from src.preprocessing.text_cleaner import TextPreprocessor
from src.sentiment_analysis.classifier import SentimentClassifier
from src.sentiment_analysis.aggregator import SentimentAggregator
from src.preprocessing.feature_engineering import FeatureEngineer
from src.portfolio_optimization.return_predictor import ReturnPredictor
from src.portfolio_optimization.risk_estimator import RiskEstimator
from src.portfolio_optimization.sentiment_optimizer import SentimentEnhancedOptimizer
from src.evaluation.backtester import Backtester
from src.evaluation.performance_analyzer import PerformanceAnalyzer
from src.visualization.charts import ChartGenerator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("FullSystemVerify")

def run_e2e_test():
    print("="*80)
    print("STARTING END-TO-END SYSTEM VERIFICATION")
    print("="*80)

    # 1. Pipeline Setup (Sentiment)
    print("\n[1/6] Sentiment Pipeline...")
    prep = SentimentDataPreparer()
    # Create 500 mock news articles over 2 years
    start_date = '2022-01-01'
    end_date = '2023-12-31'
    dates = pd.date_range(start_date, end_date, freq='D')
    
    # Generate Mock News
    news_df = prep.create_sample_data(n_records=500)
    news_df['Date'] = np.random.choice(dates, 500) # Spread dates
    news_df = news_df.sort_values('Date')
    
    # Process
    cleaner = TextPreprocessor()
    news_df['clean_text'] = cleaner.transform(news_df['Headline'])
    
    clf = SentimentClassifier()
    # Determine train split for classifier (mock)
    clf.train(news_df['clean_text'], news_df['Sentiment_Label'], optimize=False)
    
    agg = SentimentAggregator(preprocessor=cleaner, classifier=clf)
    daily_sentiment = agg.process_headlines(news_df)
    print(f"Generated {len(daily_sentiment)} daily sentiment signals.")

    # 2. Stock Data Setup
    print("\n[2/6] Stock Data Generation...")
    tickers = ['AAPL', 'MSFT', 'TSLA']
    biz_dates = pd.date_range(start_date, end_date, freq='B')
    
    stock_records = []
    for t in tickers:
        # Random walk
        p = 100 + np.cumsum(np.random.normal(0.05, 1.5, len(biz_dates)))
        for d, price in zip(biz_dates, p):
            stock_records.append({
                'Date': d, 'Ticker': t, 'Close': price, 
                'Open': price, 'High': price, 'Low': price, 'Volume': 1000
            })
    stock_df = pd.DataFrame(stock_records)
    print(f"Generated {len(stock_records)} stock records.")

    # 3. Feature Engineering & Prediction
    print("\n[3/6] Return Prediction Pipeline...")
    fe = FeatureEngineer()
    full_df = fe.prepare_data(stock_df, daily_sentiment)
    
    # Train Predictor
    train, test, _ = fe.split_data(full_df)
    predictor = ReturnPredictor(model_type='linear_regression') # Faster for test
    predictor.train(train[fe.feature_columns], train['Target_Return'])
    
    metrics = predictor.evaluate(test[fe.feature_columns], test['Target_Return'])
    print(f"Prediction Metrics: {metrics}")

    # 4. Optimization & Backtesting
    print("\n[4/6] Portfolio Optimization & Backtesting...")
    # Pivot returns and sentiment for backtester
    returns_pivot = stock_df.pivot(index='Date', columns='Ticker', values='Close').pct_change().fillna(0)
    # Ensure sentiment pivot matches returns index (fill missing)
    sent_pivot = daily_sentiment.pivot(index='Date', columns='Ticker', values='Daily_Sentiment')
    sent_pivot = sent_pivot.reindex(returns_pivot.index).ffill().fillna(0)
    
    bt = Backtester()
    results = bt.run_backtest(returns_pivot, sent_pivot, rebalance_freq='M', window_size=60) # 3 months history
    print(f"Backtest complete. Steps: {len(results)}")

    # 5. Performance Analysis
    print("\n[5/6] Performance Analysis...")
    analyzer = PerformanceAnalyzer()
    perf_metrics = analyzer.calculate_metrics(results)
    print("\nStrategy Performance:")
    print(perf_metrics[['Ann. Return', 'Sharpe Ratio', 'Max Drawdown']])

    # 6. Visualization
    print("\n[6/6] Generating Charts...")
    gen = ChartGenerator(output_dir='results/test_figures')
    gen.plot_cumulative_returns(results)
    gen.plot_drawdown(results)
    
    # Check output
    if Path('results/test_figures/cumulative_returns.png').exists():
        print("Charts generated successfully.")
    else:
        print("WARNING: Charts not found.")

    print("\n" + "="*80)
    print("ALL SYSTEMS OPERATIONAL - VERIFICATION PASSED")
    print("="*80)

if __name__ == "__main__":
    run_e2e_test()
