import os
import pandas as pd
from data_ingestion import AlphaVantageIngestor, FinnhubIngestor
from nlp_processor import SentimentProcessor
from feature_engineering import MultiModalFeatureEngineer
from training_engine import ResearchTrainingEngine

class ResearchPipeline:
    """
    The main orchestrator for the Research-Grade Multi-Modal System.
    """
    def __init__(self, av_key: str = None, fh_key: str = None):
        self.av_ingestor = AlphaVantageIngestor(av_key)
        self.fh_ingestor = FinnhubIngestor(fh_key)
        self.nlp = SentimentProcessor()
        self.engineer = MultiModalFeatureEngineer(window_size=14)
        self.engine = ResearchTrainingEngine(window_size=14)

    def run_experiment(self, ticker: str):
        print(f"=== Starting Research Experiment for {ticker} ===")
        
        # 1. Data Ingestion
        print(f"Fetching data for {ticker}...")
        price_df = self.av_ingestor.fetch_daily_prices(ticker, full=True)
        # Fetch indicators
        rsi_df = self.av_ingestor.fetch_indicator(ticker, "RSI")
        macd_df = self.av_ingestor.fetch_indicator(ticker, "MACD")
        news_df = self.fh_ingestor.fetch_company_news(ticker, days_back=60)
        
        # Merge indicators with price
        price_df = price_df.merge(rsi_df[['RSI']], left_index=True, right_index=True, how='left')
        price_df = price_df.merge(macd_df[['MACD']], left_index=True, right_index=True, how='left')
        
        # 2. NLP Processing
        print("Processing sentiment data...")
        daily_sentiment = self.nlp.process_news_dataframe(news_df)
        full_df = self.nlp.align_sentiment_with_prices(price_df, daily_sentiment)
        
        # 3. Feature Engineering
        print("Engineering features...")
        full_df = self.engineer.engineer_base_features(full_df)
        Xp, Xs, y = self.engineer.prepare_data(full_df)
        
        # 4. Training & Comparison
        print("Running training loop and evaluation...")
        base_met, hyb_met, models = self.engine.train_and_compare(Xp, Xs, y)
        
        print("\n=== EXPERIMENT COMPLETE ===")
        return {
            "baseline": base_met,
            "hybrid": hyb_met,
            "models": models,
            "data": full_df
        }

if __name__ == "__main__":
    # Note: Requires API Keys in .env
    pipeline = ResearchPipeline()
    try:
        results = pipeline.run_experiment("AAPL")
        print("\nResults Summary:")
        print(f"Baseline Accuracy: {results['baseline']['directional_acc']:.2%}")
        print(f"Hybrid Accuracy: {results['hybrid']['directional_acc']:.2%}")
    except Exception as e:
        print(f"Pipeline failed (most likely API keys): {e}")
