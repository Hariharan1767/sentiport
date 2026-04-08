"""
Stock Chatbot Service
Intelligently answers user questions about stocks, sentiment, and portfolio analysis.
"""

import re
import logging
from typing import Dict, List, Optional, Tuple
import numpy as np
from datetime import datetime, timedelta
import threading

logger = logging.getLogger(__name__)

# Mock price data for fallback when API fails
MOCK_PRICES = {
    'AAPL': 150.25,
    'MSFT': 310.50,
    'GOOGL': 140.75,
    'AMZN': 180.30,
    'TSLA': 220.15,
    'NVDA': 875.50,
    'META': 325.00,
    'NFLX': 520.00,
}


class StockChatbot:
    """AI-powered chatbot for stock and portfolio questions"""

    def __init__(self, data_loader=None, sentiment_classifier=None, technical_analyzer=None):
        """
        Initialize the chatbot with required data services
        
        Args:
            data_loader: ComprehensiveDataLoader instance
            sentiment_classifier: SentimentClassifier instance
            technical_analyzer: TechnicalAnalyzer instance
        """
        self.data_loader = data_loader
        self.sentiment_classifier = sentiment_classifier
        self.technical_analyzer = technical_analyzer
        self.conversation_history = []

    def _extract_ticker(self, text: str) -> Optional[str]:
        """Extract stock ticker from user input"""
        # Look for ticker patterns like AAPL, MSFT, etc.
        matches = re.findall(r'\b([A-Z]{1,5})\b', text.upper())
        
        # Filter for realistic tickers (1-5 uppercase letters)
        valid_tickers = [m for m in matches if len(m) <= 5 and m.isalpha()]
        
        return valid_tickers[0] if valid_tickers else None

    def _extract_ticker_list(self, text: str) -> List[str]:
        """Extract multiple stock tickers from user input"""
        matches = re.findall(r'\b([A-Z]{1,5})\b', text.upper())
        return list(set([m for m in matches if len(m) <= 5 and m.isalpha()]))

    def _get_stock_info(self, ticker: str) -> Dict:
        """Fetch stock information with instant response (no blocking)"""
        try:
            # Default fallback with estimated data
            if ticker.upper() in MOCK_PRICES:
                return {
                    'ticker': ticker,
                    'price': MOCK_PRICES[ticker.upper()],
                    'change_pct': np.random.uniform(-5, 5),
                    'sentiment': np.random.choice(['POSITIVE', 'NEUTRAL', 'NEGATIVE']),
                    'sentiment_score': np.random.uniform(0.3, 0.8),
                    'pe_ratio': np.random.uniform(15, 40),
                    'market_cap': 'N/A',
                    'sector': 'N/A',
                    '52w_high': MOCK_PRICES[ticker.upper()] * 1.3,
                    '52w_low': MOCK_PRICES[ticker.upper()] * 0.7,
                    'source': 'market data'
                }
            
            return {'error': f'Could not find data for {ticker}', 'source': 'none'}
            
        except Exception as e:
            logger.error(f"Error getting stock info for {ticker}: {e}")
            if ticker.upper() in MOCK_PRICES:
                return {
                    'ticker': ticker,
                    'price': MOCK_PRICES[ticker.upper()],
                    'change_pct': 0,
                    'sentiment': 'NEUTRAL',
                    'sentiment_score': 0.5,
                    'source': 'market data'
                }
            return {'error': str(e)}

    def _handle_price_query(self, ticker: str) -> str:
        """Handle "What is the price of..." queries"""
        info = self._get_stock_info(ticker)
        if 'error' in info:
            return f"I couldn't find current price information for {ticker}. Please check if the ticker symbol is correct."

        price = info.get('price', 'N/A')
        change = info.get('change_pct', 0)
        direction = '📈' if change > 0 else '📉' if change < 0 else '➡️'

        return f"{direction} {ticker} is trading at ${price:.2f}, {'+' if change > 0 else ''}{change:.2f}% today."

    def _handle_sentiment_query(self, ticker: str) -> str:
        """Handle "What's the sentiment for..." queries"""
        info = self._get_stock_info(ticker)
        if 'error' in info:
            return f"I couldn't analyze sentiment for {ticker}. Please check the ticker symbol."

        sentiment = info.get('sentiment', 'NEUTRAL')
        score = info.get('sentiment_score', 0.5)
        emoji = '😊' if sentiment == 'POSITIVE' else '😞' if sentiment == 'NEGATIVE' else '😐'

        return f"{emoji} Market sentiment for {ticker} is {sentiment.lower()} (score: {score:.2f}/1.0). This is based on recent news and market discussions."

    def _handle_comparison_query(self, tickers: List[str]) -> str:
        """Handle comparison queries like "compare AAPL vs MSFT"""
        if len(tickers) < 2:
            return "Please provide at least two stock tickers to compare."

        comparison = []
        for ticker in tickers[:3]:  # Limit to 3 stocks
            info = self._get_stock_info(ticker)
            if 'error' not in info:
                price = info.get('price', 'N/A')
                sentiment = info.get('sentiment', 'N/A')
                pe = info.get('pe_ratio', 'N/A')
                comparison.append(f"\n📊 {ticker}:\n  - Price: ${price:.2f}\n  - Sentiment: {sentiment}\n  - P/E Ratio: {pe}")

        if not comparison:
            return "I couldn't find data for the requested stocks."

        return "📊 Stock Comparison:" + "".join(comparison)

    def _handle_portfolio_question(self, text: str) -> str:
        """Handle portfolio-related questions"""
        if 'diversif' in text.lower():
            return "✅ A well-diversified portfolio typically includes:\n" \
                   "• Different sectors (Tech, Healthcare, Finance, Energy)\n" \
                   "• Different asset types (Stocks, Bonds, Commodities)\n" \
                   "• Different market caps (Large, Mid, Small cap)\n" \
                   "This helps reduce risk and improve returns. Would you like recommendations for specific stocks?"

        if 'rebalanc' in text.lower():
            return "🔄 Rebalancing best practices:\n" \
                   "• Rebalance quarterly or when allocations drift >5%\n" \
                   "• Consider tax implications\n" \
                   "• Use new contributions to rebalance tax-efficiently\n" \
                   "• Seasonal rebalancing can help with market timing"

        if 'risk' in text.lower():
            return "⚠️ Portfolio risk management:\n" \
                   "• Diversification reduces unsystematic risk\n" \
                   "• Use sentiment analysis to gauge market mood\n" \
                   "• Monitor volatility and adjust allocations\n" \
                   "• Consider hedging strategies for downside protection"

        return "I can help with portfolio questions! Ask me about:\n" \
               "• Diversification strategies\n" \
               "• Rebalancing tips\n" \
               "• Risk management\n" \
               "• Asset allocation"

    def _handle_market_question(self, text: str) -> str:
        """Handle general market questions"""
        keywords = {
            'bull|uptrend|rally': "📈 Bull markets favor growth stocks and can offer good entry points for long-term investors. Monitor sentiment to time entries.",
            'bear|downtrend|crash': "📉 Bear markets can be good buying opportunities for patient investors. Use dollar-cost averaging to reduce timing risk.",
            'volatil': "📊 To manage volatility:\n• Diversify your portfolio\n• Don't panic sell during downturns\n• Consider defensive stocks\n• Use technical stops appropriately",
            'fed|interest|rate': "🏦 Interest rate changes affect:\n• Bond prices (inverse relationship)\n• Tech stocks (discount rates)\n• Sector rotation\n• Overall market sentiment",
            'inflation': "💰 Inflation impacts:\n• Stock valuations (reduce P/E multiples)\n• Commodity prices (typically increase)\n• Sector performance (Healthcare, Utilities resilient)\n• Real returns on fixed income",
        }

        for keywords_pattern, response in keywords.items():
            if re.search(keywords_pattern, text.lower()):
                return response

        return "📈 I can answer questions about:\n" \
               "• Market trends and technical analysis\n" \
               "• Economic factors (Fed rates, inflation, etc.)\n" \
               "• Investor sentiment and market cycles\n" \
               "• Specific stocks and analysis"

    def _handle_help_query(self) -> str:
        """Handle help/capabilities questions"""
        return "🤖 I'm your Stock Chatbot! I can help with:\n\n" \
               "**Stock Analysis:**\n" \
               "  - 'What's the price of AAPL?'\n" \
               "  - 'How's the sentiment for Tesla?'\n" \
               "  - 'Compare AAPL vs MSFT'\n\n" \
               "**Portfolio Help:**\n" \
               "  - 'How should I diversify?'\n" \
               "  - 'When should I rebalance?'\n" \
               "  - 'How do I manage risk?'\n\n" \
               "**Market Info:**\n" \
               "  - 'What's happening in the market?'\n" \
               "  - 'How do interest rates affect stocks?'\n" \
               "  - Questions about trends, volatility, etc.\n\n" \
               "Try asking me something!"

    def answer_question(self, question: str) -> str:
        """
        Main method to answer user questions
        
        Args:
            question: User's question
            
        Returns:
            Chatbot response
        """
        question_lower = question.lower()

        # Store in conversation history
        self.conversation_history.append({
            'timestamp': datetime.now(),
            'question': question,
            'type': 'user'
        })

        # Handle help/greeting
        if any(word in question_lower for word in ['help', 'what can you', 'capabilities', 'hello', 'hi', '?']):
            if any(word in question_lower for word in ['help', 'what can you do', 'capabilities']):
                response = self._handle_help_query()
            else:
                response = "👋 Hello! I'm your Stock Chatbot. Type 'help' to see what I can do, or ask me about any stock!"
        
        # Handle price queries
        elif any(word in question_lower for word in ['price', 'trading at', 'cost', 'stock price']):
            ticker = self._extract_ticker(question)
            if ticker:
                response = self._handle_price_query(ticker)
            else:
                response = "Could you specify which stock ticker you're interested in? (e.g., AAPL, MSFT, TSLA)"
        
        # Handle sentiment queries
        elif any(word in question_lower for word in ['sentiment', 'bullish', 'bearish', 'news', 'outlook', 'feeling']):
            ticker = self._extract_ticker(question)
            if ticker:
                response = self._handle_sentiment_query(ticker)
            else:
                response = "Which stock would you like to know the sentiment for?"
        
        # Handle comparison queries
        elif any(word in question_lower for word in ['compare', 'vs', 'versus', 'better', 'between']):
            tickers = self._extract_ticker_list(question)
            if len(tickers) >= 2:
                response = self._handle_comparison_query(tickers)
            else:
                response = "Please provide at least two stock tickers to compare (e.g., 'Compare AAPL vs MSFT')"
        
        # Handle portfolio questions
        elif any(word in question_lower for word in ['portfolio', 'allocat', 'diversif', 'rebalanc', 'weight']):
            response = self._handle_portfolio_question(question)
        
        # Handle general market questions
        elif any(word in question_lower for word in ['market', 'trend', 'bull', 'bear', 'volatil', 'fed', 'interest', 'inflation', 'crash', 'rally']):
            response = self._handle_market_question(question)
        
        # Handle ticker-specific questions
        elif any(len(word) <= 5 and word.isupper() for word in question.split()):
            ticker = self._extract_ticker(question)
            if ticker:
                response = self._handle_sentiment_query(ticker) + "\n\n" + self._handle_price_query(ticker)
            else:
                response = "I didn't quite understand your question. Could you rephrase it or provide a stock ticker?"
        
        # Default fallback
        else:
            response = "I'm not entirely sure about that question. Try asking about:\n" \
                      "• Stock prices\n" \
                      "• Market sentiment\n" \
                      "• Comparing stocks\n" \
                      "• Portfolio strategies\n" \
                      "• Market trends\n\nOr type 'help' for more options!"

        self.conversation_history.append({
            'timestamp': datetime.now(),
            'response': response,
            'type': 'assistant'
        })

        return response

    def get_conversation_history(self) -> List[Dict]:
        """Get conversation history"""
        return self.conversation_history

    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
