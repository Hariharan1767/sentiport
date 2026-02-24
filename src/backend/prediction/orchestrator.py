
from data_collection.comprehensive_data import ComprehensiveDataLoader
from analysis.fundamental_analysis import FundamentalAnalyzer
from analysis.technical_analysis import TechnicalAnalyzer
from analysis.risk_analysis import RiskAnalyzer
from analysis.qualitative_analysis import QualitativeAnalyzer
from prediction.stock_predictor import StockPredictor

class StockAnalysisOrchestrator:
    """
    Coordinates the entire 9-factor analysis pipeline.
    """
    def __init__(self):
        self.data_loader = ComprehensiveDataLoader()
        self.fundamental_analyzer = FundamentalAnalyzer()
        self.technical_analyzer = TechnicalAnalyzer()
        self.risk_analyzer = RiskAnalyzer()
        self.qualitative_analyzer = QualitativeAnalyzer()
        self.predictor = StockPredictor()
        
    def analyze_stock(self, ticker: str):
        """
        Performs comprehensive 9-factor analysis on a stock.
        Returns a structured result with all factor scores and decision.
        """
        print(f"📊 Analyzing {ticker}...")
        
        # 1. Data Collection
        data = self.data_loader.get_full_analysis_data(ticker)
        
        if not data or not data['fundamentals']:
            return {
                "error": f"Unable to fetch data for {ticker}",
                "ticker": ticker
            }
        
        fundamentals = data['fundamentals']
        technicals = data['technicals']
        
        # 2. Run all analyzers
        health_result = self.fundamental_analyzer.analyze_health(fundamentals)
        valuation_result = self.fundamental_analyzer.analyze_valuation(fundamentals)
        growth_result = self.fundamental_analyzer.analyze_growth_potential(fundamentals)
        
        technical_result = self.technical_analyzer.analyze_trend(technicals)
        risk_result = self.risk_analyzer.analyze_risk(fundamentals, technicals)
        
        business_result = self.qualitative_analyzer.analyze_business_model(fundamentals)
        management_result = self.qualitative_analyzer.analyze_management(fundamentals)
        
        # 3. Aggregate results
        analysis_results = {
            'fundamental': health_result,
            'valuation': valuation_result,
            'growth': growth_result,
            'technical': technical_result,
            'risk': risk_result,
            'business': business_result,
            'management': management_result
        }
        
        # 4. Get prediction
        prediction = self.predictor.predict_invest_decision(analysis_results)
        
        # 5. Return comprehensive report
        return {
            'ticker': ticker,
            'company_name': fundamentals['info'].get('longName', ticker),
            'sector': fundamentals['info'].get('sector', 'N/A'),
            'industry': fundamentals['info'].get('industry', 'N/A'),
            'current_price': fundamentals['info'].get('currentPrice', 'N/A'),
            'market_cap': fundamentals['info'].get('marketCap', 'N/A'),
            
            'analysis': analysis_results,
            'prediction': prediction,
            
            # Factor descriptions
            'factor_descriptions': self._get_factor_descriptions()
        }
    
    def _get_factor_descriptions(self):
        """
        Returns detailed descriptions for each of the 9 factors.
        """
        return {
            'fundamental': {
                'name': '1️⃣ Company Fundamentals',
                'description': 'Evaluates the financial health through revenue growth, profit margins, cash flow, and debt levels.'
            },
            'valuation': {
                'name': '2️⃣ Valuation Metrics',
                'description': 'Assesses if the stock is fairly priced using P/E, P/B, PEG ratios, and dividend yield.'
            },
            'business': {
                'name': '3️⃣ Business Model & Moat',
                'description': 'Examines competitive advantages like brand strength, market position, and pricing power.'
            },
            'management': {
                'name': '4️⃣ Management Quality',
                'description': 'Analyzes management efficiency through ROE and insider ownership levels.'
            },
            'industry': {
                'name': '5️⃣ Industry Position',
                'description': 'Considers sector trends, market share, and competitive landscape (integrated into Risk).'
            },
            'technical': {
                'name': '6️⃣ Technical Analysis',
                'description': 'Studies price trends, momentum indicators (RSI, MACD), and timing signals.'
            },
            'risk': {
                'name': '7️⃣ Risk Factors',
                'description': 'Evaluates market volatility (Beta), debt risk, and analyst recommendations.'
            },
            'macro': {
                'name': '8️⃣ Macro Factors',
                'description': 'Tracks economic indicators like interest rates and market sentiment (VIX).'
            },
            'growth': {
                'name': '9️⃣ Growth Potential',
                'description': 'Projects future earnings growth and long-term sustainability.'
            }
        }
