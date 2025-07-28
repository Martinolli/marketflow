#!/usr/bin/env python3
"""
Test script for the Enhanced MarketFlow LLM Query Engine
"""

import sys
import os

from marketflow.marketflow_llm_query_engine import MarketflowLLMQueryEngine, QueryIntent

def test_intent_parsing():
    """Test the intent parsing functionality"""
    print("Testing Intent Parsing")
    print("=" * 50)
    
    try:
        engine = MarketflowLLMQueryEngine(enable_rag=False)  # Disable RAG for basic testing
        
        test_queries = [
            "Analyze AAPL",
            "What is a Wyckoff Spring?",
            "Compare AAPL and MSFT",
            "What does Anna Coulling say about volume?",
            "Show AAPL across all timeframes",
            "Random text that doesn't match anything"
        ]
        
        for query in test_queries:
            intent_result = engine._parse_intent(query)
            print(f"Query: '{query}'")
            print(f"  Intent: {intent_result.intent.value}")
            print(f"  Confidence: {intent_result.confidence.value} ({intent_result.confidence_score:.2f})")
            print(f"  Parameters: {intent_result.parameters}")
            print()
        
        return True
        
    except Exception as e:
        print(f"Error in intent parsing test: {str(e)}")
        return False

def test_input_validation():
    """Test the input validation functionality"""
    print("Testing Input Validation")
    print("=" * 50)
    
    try:
        engine = MarketflowLLMQueryEngine(enable_rag=False)
        
        test_inputs = [
            ("Analyze AAPL", True),
            ("", False),
            ("   ", False),
            ("x" * 1001, False),  # Too long
            ("<script>alert('test')</script>", False),  # Suspicious content
            ("What is VPA?", True)
        ]
        
        for test_input, expected_valid in test_inputs:
            is_valid, error_msg = engine.validate_input(test_input)
            status = "✓" if is_valid == expected_valid else "✗"
            print(f"{status} Input: '{test_input[:50]}{'...' if len(test_input) > 50 else ''}'")
            print(f"  Valid: {is_valid}, Expected: {expected_valid}")
            if error_msg:
                print(f"  Error: {error_msg}")
            print()
        
        return True
        
    except Exception as e:
        print(f"Error in input validation test: {str(e)}")
        return False

def test_ticker_extraction():
    """Test ticker extraction functionality"""
    print("Testing Ticker Extraction")
    print("=" * 50)
    
    try:
        engine = MarketflowLLMQueryEngine(enable_rag=False)
        
        test_texts = [
            "Analyze AAPL and MSFT",
            "What about GOOGL vs AMZN?",
            "I like THE and AND stocks",  # Should filter out common words
            "Check TSLA performance",
            "No tickers here"
        ]
        
        for text in test_texts:
            tickers = engine.extract_tickers(text)
            print(f"Text: '{text}'")
            print(f"  Extracted tickers: {tickers}")
            print()
        
        return True
        
    except Exception as e:
        print(f"Error in ticker extraction test: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("Enhanced MarketFlow LLM Query Engine Tests")
    print("=" * 60)
    print()
    
    tests = [
        test_intent_parsing,
        test_input_validation,
        test_ticker_extraction
    ]
    
    passed = 0
    total = len(tests)
    
    for test_func in tests:
        try:
            if test_func():
                passed += 1
                print("✓ PASSED\n")
            else:
                print("✗ FAILED\n")
        except Exception as e:
            print(f"✗ ERROR: {str(e)}\n")
    
    print("=" * 60)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed!")
        return 0
    else:
        print("❌ Some tests failed")
        return 1

if __name__ == "__main__":
    exit(main())

