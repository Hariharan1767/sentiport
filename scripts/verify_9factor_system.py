"""
Verification Script for 9-Factor Stock Analysis System
Tests all components end-to-end.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.prediction.orchestrator import StockAnalysisOrchestrator

def main():
    print("=" * 60)
    print("9-FACTOR STOCK ANALYSIS SYSTEM - VERIFICATION")
    print("=" * 60)
    
    # Test tickers
    test_tickers = ['AAPL', 'TSLA', 'MSFT']
    
    # Initialize orchestrator
    orchestrator = StockAnalysisOrchestrator()
    
    for ticker in test_tickers:
        print(f"\n{'=' * 60}")
        print(f"Testing: {ticker}")
        print(f"{'=' * 60}\n")
        
        try:
            result = orchestrator.analyze_stock(ticker)
            
            if 'error' in result:
                print(f"❌ Error: {result['error']}")
                continue
            
            # Display results
            print(f"✅ Company: {result['company_name']}")
            print(f"   Sector: {result['sector']}")
            print(f"   Industry: {result['industry']}")
            print(f"   Current Price: ${result['current_price']}")
            print()
            
            # Show decision
            prediction = result['prediction']
            decision_emoji = "🚀" if prediction['decision'] == "INVEST" else "⚠️"
            print(f"{decision_emoji} DECISION: {prediction['decision']}")
            print(f"   Confidence: {prediction['confidence_score']:.1%}")
            print(f"   Weighted Score: {prediction['total_weighted_score']:.2f}/{prediction['max_possible_score']:.2f}")
            print()
            
            # Show factor scores
            print("📊 FACTOR BREAKDOWN:")
            analysis = result['analysis']
            for factor_key, factor_result in analysis.items():
                score = factor_result['score']
                max_score = factor_result['max_score']
                pct = (score / max_score * 100) if max_score > 0 else 0
                print(f"   {factor_key.upper():15} {score:.1f}/{max_score:.1f} ({pct:.0f}%)")
            
            print()
            
        except Exception as e:
            print(f"❌ Error analyzing {ticker}: {str(e)}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("VERIFICATION COMPLETE")
    print("=" * 60)
    print("\n📌 Next Steps:")
    print("   1. Install dependencies: pip install -r requirements.txt")
    print("   2. Run dashboard: streamlit run src/visualization/dashboard.py")
    print("   3. Navigate to '🔍 Deep Analysis (9-Factor)' tab")
    print()

if __name__ == "__main__":
    main()
