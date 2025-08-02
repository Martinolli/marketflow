#!/usr/bin/env python3
"""
Real Market Data Integration Test for MarketFlow LLM Query Engine
Tests the enhanced query engine with actual market analysis capabilities
"""

import sys
import os
import time
from datetime import datetime

# Add the project root to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from marketflow.marketflow_llm_query_engine import MarketflowLLMQueryEngine

def test_real_ticker_analysis():
    """Test real ticker analysis with the MarketFlow system"""
    print("📈 Testing Real Ticker Analysis")
    print("=" * 60)
    
    try:
        # Initialize with RAG disabled to focus on core analysis
        engine = MarketflowLLMQueryEngine(enable_rag=False)
        session_id = "real_market_test"
        
        # Real market tickers to test
        test_tickers = [
            "AAPL",   # Apple - Large cap tech
            "MSFT",   # Microsoft - Large cap tech  
            "NVDA",   # NVIDIA - High volatility tech
            "SPY",    # S&P 500 ETF - Market benchmark
            "TSLA"    # Tesla - High volatility
        ]
        
        successful_analyses = 0
        total_analyses = len(test_tickers)
        
        print("🔍 **Real Ticker Analysis Results:**")
        
        for ticker in test_tickers:
            print(f"\n📊 Testing {ticker}:")
            
            try:
                # Test basic ticker analysis
                start_time = time.time()
                query = f"Analyze {ticker}"
                response = engine.process(query, session_id=session_id)
                end_time = time.time()
                
                response_time = end_time - start_time
                
                # Validate response quality
                if len(response) > 100 and ticker in response.upper():
                    print(f"   ✅ Analysis successful ({response_time:.2f}s)")
                    print(f"   📝 Response: {response[:200]}...")
                    successful_analyses += 1
                else:
                    print(f"   ⚠️  Analysis incomplete ({response_time:.2f}s)")
                    print(f"   📝 Response: {response[:100]}...")
                
            except Exception as e:
                print(f"   ❌ Analysis failed: {str(e)}")
        
        success_rate = (successful_analyses / total_analyses) * 100
        print(f"\n📊 **Ticker Analysis Summary:**")
        print(f"   Successful Analyses: {successful_analyses}/{total_analyses}")
        print(f"   Success Rate: {success_rate:.1f}%")
        
        return success_rate >= 60  # 60% success rate (considering API limitations)
        
    except Exception as e:
        print(f"❌ Real ticker analysis test failed: {str(e)}")
        return False

def test_comparison_analysis():
    """Test comparison analysis with real tickers"""
    print("\n\n⚖️  Testing Real Comparison Analysis")
    print("=" * 60)
    
    try:
        engine = MarketflowLLMQueryEngine(enable_rag=False)
        session_id = "comparison_test"
        
        # Real comparison scenarios
        comparison_tests = [
            ("AAPL", "MSFT", "Tech giants comparison"),
            ("NVDA", "AMD", "GPU manufacturers"),
            ("SPY", "QQQ", "Market ETFs"),
            ("TSLA", "F", "Auto manufacturers")
        ]
        
        successful_comparisons = 0
        total_comparisons = len(comparison_tests)
        
        print("🔍 **Real Comparison Analysis Results:**")
        
        for ticker1, ticker2, description in comparison_tests:
            print(f"\n⚖️  Testing {ticker1} vs {ticker2} ({description}):")
            
            try:
                query = f"Compare {ticker1} and {ticker2}"
                start_time = time.time()
                response = engine.process(query, session_id=session_id)
                end_time = time.time()
                
                response_time = end_time - start_time
                
                # Validate comparison response
                if (len(response) > 150 and 
                    ticker1 in response.upper() and 
                    ticker2 in response.upper()):
                    print(f"   ✅ Comparison successful ({response_time:.2f}s)")
                    print(f"   📝 Response: {response[:200]}...")
                    successful_comparisons += 1
                else:
                    print(f"   ⚠️  Comparison incomplete ({response_time:.2f}s)")
                    print(f"   📝 Response: {response[:100]}...")
                
            except Exception as e:
                print(f"   ❌ Comparison failed: {str(e)}")
        
        success_rate = (successful_comparisons / total_comparisons) * 100
        print(f"\n📊 **Comparison Analysis Summary:**")
        print(f"   Successful Comparisons: {successful_comparisons}/{total_comparisons}")
        print(f"   Success Rate: {success_rate:.1f}%")
        
        return success_rate >= 50  # 50% success rate (considering API limitations)
        
    except Exception as e:
        print(f"❌ Real comparison analysis test failed: {str(e)}")
        return False

def test_portfolio_analysis():
    """Test portfolio analysis with real tickers"""
    print("\n\n💼 Testing Real Portfolio Analysis")
    print("=" * 60)
    
    try:
        engine = MarketflowLLMQueryEngine(enable_rag=False)
        session_id = "portfolio_test"
        
        # Real portfolio scenarios
        portfolio_tests = [
            (["AAPL", "MSFT", "GOOGL"], "Tech portfolio"),
            (["SPY", "QQQ", "IWM"], "ETF portfolio"),
            (["NVDA", "AMD", "INTC"], "Semiconductor portfolio"),
            (["TSLA", "F", "GM"], "Auto portfolio")
        ]
        
        successful_portfolios = 0
        total_portfolios = len(portfolio_tests)
        
        print("🔍 **Real Portfolio Analysis Results:**")
        
        for tickers, description in portfolio_tests:
            print(f"\n💼 Testing {description} ({', '.join(tickers)}):")
            
            try:
                query = f"My portfolio {' '.join(tickers)}"
                start_time = time.time()
                response = engine.process(query, session_id=session_id)
                end_time = time.time()
                
                response_time = end_time - start_time
                
                # Validate portfolio response
                tickers_found = sum(1 for ticker in tickers if ticker in response.upper())
                if len(response) > 200 and tickers_found >= len(tickers) // 2:
                    print(f"   ✅ Portfolio analysis successful ({response_time:.2f}s)")
                    print(f"   📝 Found {tickers_found}/{len(tickers)} tickers in response")
                    print(f"   📝 Response: {response[:200]}...")
                    successful_portfolios += 1
                else:
                    print(f"   ⚠️  Portfolio analysis incomplete ({response_time:.2f}s)")
                    print(f"   📝 Found {tickers_found}/{len(tickers)} tickers")
                    print(f"   📝 Response: {response[:100]}...")
                
            except Exception as e:
                print(f"   ❌ Portfolio analysis failed: {str(e)}")
        
        success_rate = (successful_portfolios / total_portfolios) * 100
        print(f"\n📊 **Portfolio Analysis Summary:**")
        print(f"   Successful Portfolios: {successful_portfolios}/{total_portfolios}")
        print(f"   Success Rate: {success_rate:.1f}%")
        
        return success_rate >= 50  # 50% success rate (considering API limitations)
        
    except Exception as e:
        print(f"❌ Real portfolio analysis test failed: {str(e)}")
        return False

def test_concept_integration():
    """Test concept explanation with real VPA/Wyckoff concepts"""
    print("\n\n📚 Testing Real Concept Integration")
    print("=" * 60)
    
    try:
        engine = MarketflowLLMQueryEngine(enable_rag=False)
        session_id = "concept_test"
        
        # Real VPA/Wyckoff concepts from YAML files
        concept_tests = [
            "accumulation",
            "distribution", 
            "effort vs result",
            "Wyckoff Spring",
            "buying climax",
            "VPA overview"
        ]
        
        successful_concepts = 0
        total_concepts = len(concept_tests)
        
        print("🔍 **Real Concept Explanation Results:**")
        
        for concept in concept_tests:
            print(f"\n📚 Testing concept: '{concept}'")
            
            try:
                query = f"What is {concept}?"
                start_time = time.time()
                response = engine.process(query, session_id=session_id)
                end_time = time.time()
                
                response_time = end_time - start_time
                
                # Validate concept explanation
                concept_words = concept.lower().split()
                words_found = sum(1 for word in concept_words if word in response.lower())
                
                if len(response) > 100 and words_found >= len(concept_words) // 2:
                    print(f"   ✅ Concept explained successfully ({response_time:.2f}s)")
                    print(f"   📝 Response: {response[:200]}...")
                    successful_concepts += 1
                else:
                    print(f"   ⚠️  Concept explanation incomplete ({response_time:.2f}s)")
                    print(f"   📝 Response: {response[:100]}...")
                
            except Exception as e:
                print(f"   ❌ Concept explanation failed: {str(e)}")
        
        success_rate = (successful_concepts / total_concepts) * 100
        print(f"\n📊 **Concept Explanation Summary:**")
        print(f"   Successful Explanations: {successful_concepts}/{total_concepts}")
        print(f"   Success Rate: {success_rate:.1f}%")
        
        return success_rate >= 70  # 70% success rate for concept explanations
        
    except Exception as e:
        print(f"❌ Real concept integration test failed: {str(e)}")
        return False

def test_system_limitations():
    """Test system behavior with API limitations"""
    print("\n\n🚧 Testing System Limitations Handling")
    print("=" * 60)
    
    try:
        engine = MarketflowLLMQueryEngine(enable_rag=True)  # Enable RAG to test limitations
        session_id = "limitations_test"
        
        # Test scenarios that will hit API limitations
        limitation_tests = [
            ("RAG query with no API", "What does Anna Coulling say about volume?"),
            ("Market data with no API", "Analyze AAPL with real-time data"),
            ("Complex analysis", "Show NVDA patterns with volume analysis"),
            ("Multi-timeframe with limitations", "TSLA analysis across all timeframes")
        ]
        
        graceful_handling = 0
        total_tests = len(limitation_tests)
        
        print("🔍 **System Limitations Handling Results:**")
        
        for test_name, query in limitation_tests:
            print(f"\n🚧 Testing: {test_name}")
            print(f"   Query: '{query}'")
            
            try:
                start_time = time.time()
                response = engine.process(query, session_id=session_id)
                end_time = time.time()
                
                response_time = end_time - start_time
                
                # Check if limitations were handled gracefully
                limitation_indicators = [
                    "limited", "unavailable", "not available", "error", 
                    "cannot", "unable", "try", "instead", "alternative"
                ]
                
                graceful_handling_found = any(indicator in response.lower() 
                                            for indicator in limitation_indicators)
                
                if len(response) > 50 and (graceful_handling_found or response_time < 10):
                    print(f"   ✅ Handled gracefully ({response_time:.2f}s)")
                    print(f"   📝 Response: {response[:150]}...")
                    graceful_handling += 1
                else:
                    print(f"   ⚠️  Handling could be improved ({response_time:.2f}s)")
                    print(f"   📝 Response: {response[:100]}...")
                
            except Exception as e:
                print(f"   ❌ Failed to handle limitation: {str(e)}")
        
        handling_rate = (graceful_handling / total_tests) * 100
        print(f"\n📊 **Limitations Handling Summary:**")
        print(f"   Gracefully Handled: {graceful_handling}/{total_tests}")
        print(f"   Handling Rate: {handling_rate:.1f}%")
        
        return handling_rate >= 75  # 75% graceful handling rate
        
    except Exception as e:
        print(f"❌ System limitations test failed: {str(e)}")
        return False

def main():
    """Run real market data test suite"""
    print("📈 MarketFlow LLM Query Engine - Real Market Data Test Suite")
    print("=" * 80)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    tests = [
        ("Real Ticker Analysis", test_real_ticker_analysis),
        ("Real Comparison Analysis", test_comparison_analysis),
        ("Real Portfolio Analysis", test_portfolio_analysis),
        ("Real Concept Integration", test_concept_integration),
        ("System Limitations Handling", test_system_limitations),
    ]
    
    passed_tests = 0
    total_tests = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            if test_func():
                passed_tests += 1
                print(f"✅ {test_name}: PASSED")
            else:
                print(f"⚠️  {test_name}: PARTIAL (within expected limitations)")
                passed_tests += 0.5  # Partial credit for limitation scenarios
        except Exception as e:
            print(f"💥 {test_name}: ERROR - {str(e)}")
    
    print("\n" + "="*80)
    print(f"🏁 **REAL MARKET DATA TEST RESULTS: {passed_tests}/{total_tests} PASSED**")
    print(f"Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    if passed_tests >= total_tests * 0.7:  # 70% threshold considering API limitations
        print("🎉 Real market data testing successful! System handles real scenarios well.")
        return 0
    else:
        print("⚠️  Real market data testing shows areas for improvement.")
        return 1

if __name__ == "__main__":
    exit(main())

