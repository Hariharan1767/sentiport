#!/usr/bin/env python
"""
System test script to verify Sentiport deployment
"""

import sys
import os
import requests
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

def test_imports():
    """Test that all required modules can be imported"""
    print("Testing imports...")
    try:
        import pandas
        print("✓ pandas")
        import numpy
        print("✓ numpy")
        import sklearn
        print("✓ scikit-learn")
        import nltk
        print("✓ nltk")
        import flask
        print("✓ flask")
        import yfinance
        print("✓ yfinance")
        from src.data_collection.comprehensive_data import ComprehensiveDataLoader
        print("✓ ComprehensiveDataLoader")
        from src.sentiment_analysis.classifier import SentimentClassifier
        print("✓ SentimentClassifier")
        return True
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        return False


def test_api_endpoints():
    """Test API endpoints"""
    print("\nTesting API endpoints...")
    base_url = "http://localhost:5000"
    
    try:
        # Test health endpoint
        response = requests.get(f"{base_url}/api/health", timeout=5)
        if response.status_code == 200:
            print(f"✓ Health check: {response.json()}")
        else:
            print(f"✗ Health check failed: {response.status_code}")
            return False
        
        # Test status endpoint
        response = requests.get(f"{base_url}/api/status", timeout=5)
        if response.status_code == 200:
            print(f"✓ Status check: {response.json()['status']}")
        else:
            print(f"✗ Status check failed: {response.status_code}")
            return False
        
        return True
    except requests.exceptions.ConnectionError:
        print("✗ Could not connect to API server at http://localhost:5000")
        print("  Make sure the server is running: python api_server.py")
        return False
    except Exception as e:
        print(f"✗ API test failed: {e}")
        return False


def test_data_fetching():
    """Test data fetching capabilities"""
    print("\nTesting data fetching...")
    try:
        from src.data_collection.comprehensive_data import ComprehensiveDataLoader
        loader = ComprehensiveDataLoader()
        
        # Test price data fetching
        print("  Fetching price data for AAPL...")
        data = loader.fetch_price_data("AAPL", period="1mo")
        if data is not None and not data.empty:
            print(f"  ✓ Price data retrieved: {len(data)} records")
            return True
        else:
            print("  ✗ No price data retrieved")
            return False
    except Exception as e:
        print(f"✗ Data fetching failed: {e}")
        return False


def main():
    """Run all tests"""
    print("=" * 50)
    print("Sentiport Deployment Test Suite")
    print("=" * 50)
    print()
    
    tests = [
        ("Module Imports", test_imports),
        ("Data Fetching", test_data_fetching),
        ("API Endpoints", test_api_endpoints),
    ]
    
    results = {}
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"\n✗ {test_name} encountered an error: {e}")
            results[test_name] = False
    
    # Summary
    print("\n" + "=" * 50)
    print("Test Summary")
    print("=" * 50)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    print()
    print(f"Total: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n✓ All tests passed! Deployment is ready.")
        return 0
    else:
        print(f"\n✗ {total - passed} test(s) failed. Please review the errors above.")
        return 1


if __name__ == '__main__':
    sys.exit(main())
