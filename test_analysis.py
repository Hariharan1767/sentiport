"""
Quick test script to verify the 9-factor analysis system works.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.prediction.orchestrator import StockAnalysisOrchestrator

def test_analysis():
    print("=" * 60)
    print("Testing SentiPort 9-Factor Analysis System")
    print("=" * 60)
    
    orchestrator = StockAnalysisOrchestrator()
    
    # Test with AAPL
    print("\n📊 Analyzing AAPL...")
    result = orchestrator.analyze_stock("AAPL")
    
    if 'error' in result:
        print(f"❌ Error: {result['error']}")
        return False
    
    print(f"\n✅ Company: {result['company_name']}")
    print(f"✅ Sector: {result['sector']}")
    print(f"✅ Current Price: ${result['current_price']}")
    
    print(f"\n📊 Analysis Results:")
    for factor_name, factor_result in result['analysis'].items():
        score = factor_result['score']
        max_score = factor_result['max_score']
        percentage = (score / max_score * 100) if max_score > 0 else 0
        print(f"  {factor_name.title()}: {score:.1f}/{max_score} ({percentage:.0f}%)")
    
    prediction = result['prediction']
    print(f"\n🎯 Decision: {prediction['decision']}")
    print(f"🎯 Confidence: {prediction['confidence_score']:.1%}")
    
    print("\n" + "=" * 60)
    print("✅ All components working correctly!")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    try:
        success = test_analysis()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
