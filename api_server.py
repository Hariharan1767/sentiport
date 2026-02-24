"""
Flask API Server for Sentiment-Driven Portfolio Optimization System
Serves as the backend for the React frontend application.
"""

import os
import sys
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import json
import traceback

from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
from dotenv import load_dotenv

# Add src/backend directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src', 'backend'))

# Import all required modules
from data_collection.comprehensive_data import ComprehensiveDataLoader
from sentiment_analysis.classifier import SentimentClassifier
from sentiment_analysis.aggregator import SentimentAggregator
from analysis.fundamental_analysis import FundamentalAnalyzer
from analysis.technical_analysis import TechnicalAnalyzer
from analysis.risk_analysis import RiskAnalyzer
from analysis.qualitative_analysis import QualitativeAnalyzer
from portfolio_optimization.mean_variance import MeanVarianceOptimizer
from portfolio_optimization.sentiment_optimizer import SentimentEnhancedOptimizer
from prediction.orchestrator import StockAnalysisOrchestrator as PredictionOrchestrator
from evaluation.performance_analyzer import PerformanceAnalyzer

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
# Enable CORS for all routes with explicit support for credentials and standard methods
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Initialize core components
data_loader = ComprehensiveDataLoader()
sentiment_classifier = SentimentClassifier()
sentiment_aggregator = SentimentAggregator()
fundamental_analyzer = FundamentalAnalyzer()
technical_analyzer = TechnicalAnalyzer()
risk_analyzer = RiskAnalyzer()
qualitative_analyzer = QualitativeAnalyzer()
mean_variance_optimizer = MeanVarianceOptimizer()
sentiment_optimizer = SentimentEnhancedOptimizer()
prediction_orchestrator = PredictionOrchestrator()
performance_analyzer = PerformanceAnalyzer()

# Cache for storing analysis results (simple in-memory cache)
analysis_cache = {}


# ===========================
# Health & Status Endpoints
# ===========================

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    }), 200


@app.route('/api/status', methods=['GET'])
def status():
    """Get system status"""
    return jsonify({
        'status': 'operational',
        'components': {
            'data_loader': 'ready',
            'sentiment_analysis': 'ready',
            'portfolio_optimization': 'ready',
            'prediction': 'ready'
        },
        'timestamp': datetime.now().isoformat()
    }), 200


# ===========================
# Stock Data Endpoints
# ===========================

@app.route('/api/stock/<ticker>', methods=['GET'])
def get_stock_dashboard_data(ticker):
    """Unified GET endpoint for dashboard stock stats"""
    try:
        ticker = ticker.upper()
        # Fetch price data for metrics
        price_data = data_loader.fetch_price_data(ticker, period='5d')
        if price_data is None or price_data.empty:
            return jsonify({'error': 'No data'}), 404
        
        current_price = float(price_data['Close'].iloc[-1])
        prev_price = float(price_data['Close'].iloc[-2]) if len(price_data) > 1 else current_price
        change_pct = ((current_price - prev_price) / prev_price) * 100 if prev_price != 0 else 0
        
        # Fetch sentiment
        news_df = data_loader.fetch_news(ticker, days=7)
        sent_label = 'NEUTRAL'
        sent_score = 0.5
        if news_df is not None and not news_df.empty:
            texts = (news_df['title'] + " " + news_df['description'].fillna('')).tolist()
            scores = [sentiment_classifier.predict_sentiment(t)['score'] for t in texts[:10]]
            sent_score = float(np.mean(scores))
            sent_label = 'POSITIVE' if sent_score > 0.6 else 'NEGATIVE' if sent_score < 0.4 else 'NEUTRAL'

        # Recommendation
        info = data_loader.fetch_fundamentals(ticker).get('info', {})
        rec = info.get('recommendationKey', 'hold').upper().replace('_', ' ')

        return jsonify({
            'ticker': ticker,
            'price': current_price,
            'change_pct': change_pct,
            'sentiment': {'label': sent_label, 'score': sent_score},
            'recommendation': rec
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stock/<ticker>/history', methods=['GET'])
def get_stock_history(ticker):
    """GET endpoint for chart history"""
    try:
        period = request.args.get('period', '3mo')
        price_data = data_loader.fetch_price_data(ticker.upper(), period=period)
        if price_data is None or price_data.empty:
            return jsonify({'prices': []}), 200
        
        history = []
        for date, row in price_data.iterrows():
            history.append({
                'date': date.strftime('%Y-%m-%d') if hasattr(date, 'strftime') else str(date),
                'close': float(row['Close'])
            })
        return jsonify({'prices': history}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analysis/<ticker>', methods=['GET'])
def get_comprehensive_analysis(ticker):
    """GET endpoint for full security analysis"""
    try:
        ticker = ticker.upper()
        stock_data = data_loader.fetch_price_data(ticker, period='2y')
        fundamentals = data_loader.fetch_fundamentals(ticker)
        
        fund_res = fundamental_analyzer.analyze(fundamentals)
        tech_res = technical_analyzer.analyze(stock_data)
        risk_res = risk_analyzer.analyze(stock_data)
        
        # Simple recommendation engine
        scores = [fund_res['score'], tech_res['score'], risk_res['score']]
        avg = np.mean(scores)
        rec = 'BUY' if avg > 70 else 'SELL' if avg < 40 else 'HOLD'

        return jsonify({
            'ticker': ticker,
            'fundamental': fund_res,
            'technical': tech_res,
            'risk': risk_res,
            'recommendation': rec,
            'sentiment': {'score': 50, 'label': 'NEUTRAL'} # Simplified for speed
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ===========================
# Analysis Endpoints
# ===========================

@app.route('/api/analysis/comprehensive', methods=['POST'])
def comprehensive_analysis():
    """
    Perform comprehensive analysis on a stock
    Request body: {
        "ticker": "AAPL"
    }
    """
    try:
        data = request.get_json()
        ticker = data.get('ticker', '').upper()

        if not ticker:
            return jsonify({'error': 'Ticker is required'}), 400

        logger.info(f"Performing comprehensive analysis for {ticker}")

        # Check cache
        cache_key = f"analysis_{ticker}_{datetime.now().strftime('%Y%m%d')}"
        if cache_key in analysis_cache:
            return jsonify(analysis_cache[cache_key]), 200

        # Fetch data
        stock_data = data_loader.fetch_price_data(ticker, period='2y')
        fundamentals = data_loader.fetch_fundamentals(ticker)
        news_df = data_loader.fetch_news(ticker, days=30)

        results = {
            'ticker': ticker,
            'analysis_date': datetime.now().isoformat(),
            'analyses': {}
        }

        # Fundamental Analysis
        try:
            fund_result = fundamental_analyzer.analyze(fundamentals)
            results['analyses']['fundamental'] = {
                'score': float(fund_result.get('score', 0)),
                'rating': fund_result.get('rating', 'N/A'),
                'details': fund_result
            }
        except Exception as e:
            logger.warning(f"Fundamental analysis failed: {e}")
            results['analyses']['fundamental'] = {'score': 50, 'rating': 'N/A', 'error': str(e)}

        # Technical Analysis
        try:
            tech_result = technical_analyzer.analyze(stock_data)
            results['analyses']['technical'] = {
                'score': float(tech_result.get('score', 0)),
                'signal': tech_result.get('signal', 'NEUTRAL'),
                'details': tech_result
            }
        except Exception as e:
            logger.warning(f"Technical analysis failed: {e}")
            results['analyses']['technical'] = {'score': 50, 'signal': 'NEUTRAL', 'error': str(e)}

        # Risk Analysis
        try:
            risk_result = risk_analyzer.analyze(stock_data)
            results['analyses']['risk'] = {
                'score': float(risk_result.get('score', 0)),
                'risk_level': risk_result.get('risk_level', 'MEDIUM'),
                'details': risk_result
            }
        except Exception as e:
            logger.warning(f"Risk analysis failed: {e}")
            results['analyses']['risk'] = {'score': 50, 'risk_level': 'MEDIUM', 'error': str(e)}

        # Sentiment Analysis
        try:
            if news_df is not None and not news_df.empty:
                sentiments = []
                for idx, article in news_df.iterrows():
                    text = f"{article.get('title', '')} {article.get('description', '')}"
                    sentiment = sentiment_classifier.predict_sentiment(text)
                    sentiments.append(sentiment)
                
                sentiment_scores = [s['score'] for s in sentiments]
                avg_sentiment = float(np.mean(sentiment_scores)) if sentiment_scores else 0.5
            else:
                avg_sentiment = 0.5
            
            results['analyses']['sentiment'] = {
                'score': avg_sentiment * 100,
                'label': 'POSITIVE' if avg_sentiment > 0.6 else 'NEGATIVE' if avg_sentiment < 0.4 else 'NEUTRAL'
            }
        except Exception as e:
            logger.warning(f"Sentiment analysis failed: {e}")
            results['analyses']['sentiment'] = {'score': 50, 'label': 'NEUTRAL', 'error': str(e)}

        # Cache results
        analysis_cache[cache_key] = results

        return jsonify(results), 200

    except Exception as e:
        logger.error(f"Error in comprehensive analysis: {str(e)}\n{traceback.format_exc()}")
        return jsonify({'error': str(e)}), 500


# ===========================
# Portfolio Optimization Endpoints
# ===========================

@app.route('/api/portfolio/optimize', methods=['POST'])
def optimize_portfolio():
    """
    Optimize portfolio using mean-variance or sentiment-enhanced optimization
    Request body: {
        "tickers": ["AAPL", "MSFT", "GOOGL"],
        "target_return": 0.10,
        "method": "sentiment" | "mean_variance",
        "sentiment_weights": {"AAPL": 0.8, ...}  // Optional
    }
    """
    try:
        data = request.get_json()
        tickers = data.get('tickers', [])
        target_return = data.get('target_return', 0.10)
        method = data.get('method', 'mean_variance')
        sentiment_weights = data.get('sentiment_weights', {})

        if not tickers:
            return jsonify({'error': 'Tickers list is required'}), 400

        logger.info(f"Optimizing portfolio for {tickers} using {method} method")

        # Fetch historical data for all tickers
        returns_data = []
        for ticker in tickers:
            try:
                price_data = data_loader.fetch_price_data(ticker, period='1y')
                if price_data is not None and not price_data.empty:
                    returns = price_data['Close'].pct_change().dropna()
                    returns_data.append(returns)
            except Exception as e:
                logger.warning(f"Error fetching data for {ticker}: {e}")

        if not returns_data:
            return jsonify({'error': 'Unable to fetch data for provided tickers'}), 400

        # Create returns DataFrame
        returns_df = pd.concat(returns_data, axis=1)
        returns_df.columns = tickers[:len(returns_data)]

        # Calculate statistics
        mean_returns = returns_df.mean()
        cov_matrix = returns_df.cov()

        # Optimize
        tickers_used = tickers[:len(returns_data)]
        if method == 'sentiment' and sentiment_weights:
            weights, metrics = sentiment_optimizer.optimize(
                mean_returns.values,
                cov_matrix.values,
                sentiment_weights=sentiment_weights,
                tickers=tickers_used
            )
        else:
            weights, metrics = mean_variance_optimizer.optimize(
                mean_returns.values,
                cov_matrix.values,
                target_return=target_return
            )

        # Format response
        allocation = {ticker: float(w) for ticker, w in zip(tickers_used, weights)}
        
        return jsonify({
            'method': method,
            'allocation': allocation,
            'expected_return': float(metrics.get('expected_return', 0)),
            'risk': float(metrics.get('risk', 0)),
            'sharpe_ratio': float(metrics.get('sharpe_ratio', 0)),
            'optimization_date': datetime.now().isoformat()
        }), 200

    except Exception as e:
        logger.error(f"Error optimizing portfolio: {str(e)}\n{traceback.format_exc()}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/portfolio/backtest', methods=['POST'])
def backtest_portfolio():
    """
    Backtest portfolio strategy
    Request body: {
        "tickers": ["AAPL", "MSFT"],
        "weights": [0.6, 0.4],
        "start_date": "2023-01-01",
        "end_date": "2024-01-01"
    }
    """
    try:
        data = request.get_json()
        tickers = data.get('tickers', [])
        weights = data.get('weights', [])
        start_date = data.get('start_date', None)
        end_date = data.get('end_date', None)

        if not tickers or not weights or len(tickers) != len(weights):
            return jsonify({'error': 'Valid tickers and weights are required'}), 400

        logger.info(f"Backtesting portfolio: {dict(zip(tickers, weights))}")

        # Fetch data and compute returns
        portfolio_returns = None
        for ticker, weight in zip(tickers, weights):
            try:
                price_data = data_loader.fetch_price_data(ticker, period='2y')
                if price_data is not None and not price_data.empty:
                    returns = price_data['Close'].pct_change() * weight
                    if portfolio_returns is None:
                        portfolio_returns = returns
                    else:
                        portfolio_returns += returns
            except Exception as e:
                logger.warning(f"Error in backtest for {ticker}: {e}")

        if portfolio_returns is None or portfolio_returns.empty:
            return jsonify({'error': 'Unable to fetch data for backtest'}), 400

        # Calculate performance metrics
        cumulative_returns = (1 + portfolio_returns).cumprod()
        total_return = (cumulative_returns.iloc[-1] - 1) * 100
        annualized_return = (cumulative_returns.iloc[-1] ** (252 / len(portfolio_returns)) - 1) * 100
        annualized_volatility = portfolio_returns.std() * np.sqrt(252) * 100
        sharpe_ratio = (annualized_return / 100) / (annualized_volatility / 100) if annualized_volatility > 0 else 0

        return jsonify({
            'portfolio': dict(zip(tickers, weights)),
            'total_return_percent': float(total_return),
            'annualized_return_percent': float(annualized_return),
            'annualized_volatility_percent': float(annualized_volatility),
            'sharpe_ratio': float(sharpe_ratio),
            'data_points': len(portfolio_returns),
            'backtest_date': datetime.now().isoformat()
        }), 200

    except Exception as e:
        logger.error(f"Error in backtest: {str(e)}\n{traceback.format_exc()}")
        return jsonify({'error': str(e)}), 500


# ===========================
# Prediction Endpoints
# ===========================

@app.route('/api/predict/investment', methods=['POST'])
def predict_investment():
    """
    Predict investment decision based on comprehensive analysis
    Request body: {
        "ticker": "AAPL"
    }
    """
    try:
        data = request.get_json()
        ticker = data.get('ticker', '').upper()

        if not ticker:
            return jsonify({'error': 'Ticker is required'}), 400

        logger.info(f"Predicting investment decision for {ticker}")

        # Perform comprehensive analysis
        stock_data = data_loader.fetch_price_data(ticker, period='2y')
        fundamentals = data_loader.fetch_fundamentals(ticker)
        
        # Get analysis results
        analyses = {}
        
        try:
            fund_result = fundamental_analyzer.analyze(fundamentals)
            analyses['fundamental'] = fund_result.get('score', 50)
        except:
            analyses['fundamental'] = 50

        try:
            tech_result = technical_analyzer.analyze(stock_data)
            analyses['technical'] = tech_result.get('score', 50)
        except:
            analyses['technical'] = 50

        try:
            risk_result = risk_analyzer.analyze(stock_data)
            analyses['risk'] = risk_result.get('score', 50)
        except:
            analyses['risk'] = 50

        # Calculate weighted score
        weights = {
            'fundamental': 0.35,
            'technical': 0.25,
            'risk': 0.25,
            'sentiment': 0.15
        }

        weighted_score = sum(analyses.get(k, 50) * v for k, v in weights.items() if k != 'sentiment')
        final_score = weighted_score / (1 - weights.get('sentiment', 0))

        # Determine recommendation
        if final_score >= 70:
            recommendation = 'BUY'
            confidence = min(final_score / 100, 0.95)
        elif final_score >= 50:
            recommendation = 'HOLD'
            confidence = 0.5
        else:
            recommendation = 'SELL'
            confidence = 1 - (final_score / 100)

        return jsonify({
            'ticker': ticker,
            'recommendation': recommendation,
            'score': float(final_score),
            'confidence': float(confidence),
            'analyses': {k: float(v) for k, v in analyses.items()},
            'prediction_date': datetime.now().isoformat()
        }), 200

    except Exception as e:
        logger.error(f"Error in prediction: {str(e)}\n{traceback.format_exc()}")
        return jsonify({'error': str(e)}), 500


# ===========================
# Error Handlers
# ===========================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal server error: {error}")
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV', 'production') == 'development'
    
    logger.info(f"Starting API server on port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)
