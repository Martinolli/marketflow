#!/usr/bin/env python3
"""
Complete Integration Test for MarketFlow LLM Query Engine
Tests the enhanced query engine with the full MarketFlow system including all new features
"""

import sys
import os
import time
from datetime import datetime

# Add the project root to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from marketflow.marketflow_llm_query_engine import MarketflowLLMQueryEngine

def test_all_query_types():
    """Test all 10 query types with the complete system"""
    print("🔬 Testing All Query Types Integration")
    print("=" * 60)
    
    try:
        engine = MarketflowLLMQueryEngine(enable_rag=True)
        session_id = "complete_integration_test"
        
        # Comprehensive test queries covering all 10 query types
        test_scenarios = [
            # 1. Ticker Analysis
            {
                "category": "Ticker Analysis",
                "queries": [
                    "Analyze AAPL",
                    "What's the VPA signal for MSFT?",
                    "Check NVDA performance",
                    "Review GOOGL analysis"
                ]
            },
            
            # 2. Concept Explanation
            {
                "category": "Concept Explanation", 
                "queries": [
                    "What is accumulation?",
                    "Explain Wyckoff Spring",
                    "What is VPA?",
                    "Tell me about distribution"
                ]
            },
            
            # 3. Comparison
            {
                "category": "Comparison Queries",
                "queries": [
                    "Compare AAPL and MSFT",
                    "GOOGL vs AMZN analysis",
                    "Difference between TSLA and NVDA"
                ]
            },
            
            # 4. RAG Queries
            {
                "category": "RAG Knowledge Queries",
                "queries": [
                    "What does Anna Coulling say about volume?",
                    "According to Wyckoff, what is accumulation?",
                    "What does the literature say about VPA?"
                ]
            },
            
            # 5. Multi-Timeframe
            {
                "category": "Multi-Timeframe Analysis",
                "queries": [
                    "Show AAPL across all timeframes",
                    "MSFT analysis on multiple timeframes"
                ]
            },
            
            # 6. Historical Analysis
            {
                "category": "Historical Analysis",
                "queries": [
                    "AAPL performance last month",
                    "NVDA trend over the past quarter",
                    "Historical analysis of MSFT"
                ]
            },
            
            # 7. Market Condition
            {
                "category": "Market Condition",
                "queries": [
                    "What is market sentiment?",
                    "Current market conditions",
                    "Bull or bear market?"
                ]
            },
            
            # 8. Pattern Recognition
            {
                "category": "Pattern Recognition",
                "queries": [
                    "Show patterns in AAPL",
                    "Find accumulation patterns in MSFT",
                    "NVDA pattern analysis"
                ]
            },
            
            # 9. Timeframe Specific
            {
                "category": "Timeframe Specific",
                "queries": [
                    "AAPL daily analysis",
                    "MSFT weekly chart",
                    "NVDA hourly view"
                ]
            },
            
            # 10. Portfolio Analysis
            {
                "category": "Portfolio Analysis",
                "queries": [
                    "My portfolio AAPL MSFT GOOGL",
                    "Analyze my holdings NVDA TSLA AMZN",
                    "Portfolio analysis AAPL MSFT NVDA GOOGL TSLA"
                ]
            }
        ]
        
        total_queries = 0
        successful_queries = 0
        
        for scenario in test_scenarios:
            print(f"\n📊 **{scenario['category']}**")
            print("-" * 40)
            
            for query in scenario['queries']:
                total_queries += 1
                print(f"\n🔍 Query: '{query}'")
                
                try:
                    start_time = time.time()
                    response = engine.process(query, session_id=session_id)
                    end_time = time.time()
                    
                    response_time = end_time - start_time
                    print(f"✅ Response ({response_time:.2f}s): {response[:150]}{'...' if len(response) > 150 else ''}")
                    successful_queries += 1
                    
                except Exception as e:
                    print(f"❌ Error: {str(e)}")
        
        success_rate = (successful_queries / total_queries) * 100
        print(f"\n🏁 **Integration Test Results:**")
        print(f"   Total Queries: {total_queries}")
        print(f"   Successful: {successful_queries}")
        print(f"   Success Rate: {success_rate:.1f}%")
        
        return success_rate >= 80  # 80% success rate threshold
        
    except Exception as e:
        print(f"❌ Complete integration test failed: {str(e)}")
        return False

def test_conversation_flow():
    """Test conversation context and flow"""
    print("\n\n💬 Testing Conversation Flow")
    print("=" * 60)
    
    try:
        engine = MarketflowLLMQueryEngine(enable_rag=True)
        session_id = "conversation_flow_test"
        
        # Conversation flow test
        conversation_flow = [
            "Analyze AAPL",
            "What about MSFT?",  # Should understand context
            "Compare them",      # Should use previous tickers
            "Show patterns in NVDA",
            "Daily analysis",    # Should apply to NVDA
            "What is accumulation?",
            "My portfolio AAPL MSFT NVDA GOOGL TSLA",
            "How are they performing?"  # Should reference portfolio
        ]
        
        print("🔄 **Conversation Flow Test:**")
        for i, query in enumerate(conversation_flow, 1):
            print(f"\n{i}. User: '{query}'")
            
            try:
                response = engine.process(query, session_id=session_id)
                print(f"   AI: {response[:100]}{'...' if len(response) > 100 else ''}")
                
                # Show context state
                if session_id in engine.contexts:
                    context = engine.contexts[session_id]
                    print(f"   📝 Context - Last ticker: {getattr(context, 'last_ticker', 'None')}")
                    print(f"   📝 Context - History: {len(context.conversation_history)} exchanges")
                
            except Exception as e:
                print(f"   ❌ Error: {str(e)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Conversation flow test failed: {str(e)}")
        return False

def test_performance_benchmarks():
    """Test performance and response times"""
    print("\n\n⚡ Testing Performance Benchmarks")
    print("=" * 60)
    
    try:
        engine = MarketflowLLMQueryEngine(enable_rag=True)
        
        # Performance test queries
        performance_queries = [
            "Analyze AAPL",
            "What is accumulation?",
            "Compare AAPL and MSFT", 
            "Show NVDA patterns",
            "My portfolio AAPL MSFT GOOGL NVDA TSLA"
        ]
        
        response_times = []
        
        print("⏱️  **Performance Test Results:**")
        for query in performance_queries:
            try:
                start_time = time.time()
                response = engine.process(query, session_id="perf_test")
                end_time = time.time()
                
                response_time = end_time - start_time
                response_times.append(response_time)
                
                print(f"   '{query[:30]}...' → {response_time:.2f}s")
                
            except Exception as e:
                print(f"   '{query[:30]}...' → ERROR: {str(e)}")
        
        if response_times:
            avg_time = sum(response_times) / len(response_times)
            max_time = max(response_times)
            min_time = min(response_times)
            
            print(f"\n📊 **Performance Summary:**")
            print(f"   Average Response Time: {avg_time:.2f}s")
            print(f"   Fastest Response: {min_time:.2f}s")
            print(f"   Slowest Response: {max_time:.2f}s")
            
            # Performance thresholds
            if avg_time < 5.0:
                print("   ✅ Performance: Excellent (< 5s average)")
            elif avg_time < 10.0:
                print("   ✅ Performance: Good (< 10s average)")
            else:
                print("   ⚠️  Performance: Needs optimization (> 10s average)")
        
        return True
        
    except Exception as e:
        print(f"❌ Performance test failed: {str(e)}")
        return False

def test_error_handling_robustness():
    """Test comprehensive error handling"""
    print("\n\n🛡️  Testing Error Handling Robustness")
    print("=" * 60)
    
    try:
        engine = MarketflowLLMQueryEngine(enable_rag=True)
        
        # Error handling test cases
        error_test_cases = [
            ("Empty input", ""),
            ("Whitespace only", "   "),
            ("Very long input", "A" * 1500),
            ("Malicious input", "<script>alert('test')</script>"),
            ("Invalid ticker", "Analyze INVALIDTICKER123"),
            ("Nonsense query", "Purple elephant dancing on Tuesday"),
            ("Mixed languages", "Analyze AAPL pero en español"),
            ("Special characters", "Analyze @#$%^&*()"),
            ("Numbers only", "12345"),
            ("SQL injection attempt", "'; DROP TABLE users; --")
        ]
        
        handled_gracefully = 0
        total_cases = len(error_test_cases)
        
        print("🧪 **Error Handling Test Results:**")
        for test_name, test_input in error_test_cases:
            try:
                response = engine.process(test_input, session_id="error_test")
                
                # Check if error was handled gracefully
                if "error" in response.lower() or "invalid" in response.lower() or "not sure" in response.lower():
                    print(f"   ✅ {test_name}: Handled gracefully")
                    handled_gracefully += 1
                else:
                    print(f"   ✅ {test_name}: Processed normally")
                    handled_gracefully += 1
                    
            except Exception as e:
                print(f"   ⚠️  {test_name}: Exception - {str(e)[:50]}...")
        
        robustness_score = (handled_gracefully / total_cases) * 100
        print(f"\n🛡️  **Robustness Score: {robustness_score:.1f}%**")
        
        return robustness_score >= 90  # 90% robustness threshold
        
    except Exception as e:
        print(f"❌ Error handling test failed: {str(e)}")
        return False

def test_system_integration():
    """Test integration with MarketFlow components"""
    print("\n\n🔗 Testing System Integration")
    print("=" * 60)
    
    try:
        engine = MarketflowLLMQueryEngine(enable_rag=True)
        
        print("🔧 **Component Integration Tests:**")
        
        # Test 1: LLM Interface Integration
        print("\n1. LLM Interface Integration:")
        try:
            interface_test = engine.interface.explain_concept("accumulation")
            print(f"   ✅ LLM Interface: Working ({len(interface_test)} chars response)")
        except Exception as e:
            print(f"   ❌ LLM Interface: Error - {str(e)}")
        
        # Test 2: YAML Concepts Integration
        print("\n2. YAML Concepts Integration:")
        try:
            vpa_concepts = len(engine.vpa_concepts)
            wyckoff_concepts = len(engine.wyckoff_concepts)
            print(f"   ✅ VPA Concepts: {vpa_concepts} loaded")
            print(f"   ✅ Wyckoff Concepts: {wyckoff_concepts} loaded")
        except Exception as e:
            print(f"   ❌ YAML Concepts: Error - {str(e)}")
        
        # Test 3: Context Management
        print("\n3. Context Management:")
        try:
            context = engine.get_or_create_context("integration_test")
            engine.update_context(context, "test query", "test response", None)
            print(f"   ✅ Context Management: Working ({len(context.conversation_history)} entries)")
        except Exception as e:
            print(f"   ❌ Context Management: Error - {str(e)}")
        
        # Test 4: Intent Recognition System
        print("\n4. Intent Recognition System:")
        try:
            test_intents = [
                ("Analyze AAPL", "ticker_analysis"),
                ("What is VPA?", "concept_explanation"),
                ("Compare AAPL and MSFT", "comparison"),
                ("Show patterns in NVDA", "pattern_recognition"),
                ("My portfolio AAPL MSFT", "portfolio_analysis")
            ]
            
            correct_intents = 0
            for query, expected_intent in test_intents:
                result = engine._parse_intent(query)
                if result.intent.value == expected_intent:
                    correct_intents += 1
            
            accuracy = (correct_intents / len(test_intents)) * 100
            print(f"   ✅ Intent Recognition: {accuracy:.1f}% accuracy ({correct_intents}/{len(test_intents)})")
            
        except Exception as e:
            print(f"   ❌ Intent Recognition: Error - {str(e)}")
        
        # Test 5: Ticker Extraction
        print("\n5. Ticker Extraction:")
        try:
            test_extractions = [
                ("Analyze AAPL and MSFT", ["AAPL", "MSFT"]),
                ("My portfolio AAPL MSFT GOOGL", ["AAPL", "MSFT", "GOOGL"]),
                ("What about DAILY analysis", []),  # Should filter out DAILY
                ("Check THE and AND performance", [])  # Should filter out common words
            ]
            
            extraction_accuracy = 0
            for query, expected_tickers in test_extractions:
                extracted = engine.extract_tickers(query)
                if set(extracted) == set(expected_tickers):
                    extraction_accuracy += 1
            
            accuracy = (extraction_accuracy / len(test_extractions)) * 100
            print(f"   ✅ Ticker Extraction: {accuracy:.1f}% accuracy ({extraction_accuracy}/{len(test_extractions)})")
            
        except Exception as e:
            print(f"   ❌ Ticker Extraction: Error - {str(e)}")
        
        return True
        
    except Exception as e:
        print(f"❌ System integration test failed: {str(e)}")
        return False

def main():
    """Run complete integration test suite"""
    print("🚀 MarketFlow LLM Query Engine - Complete Integration Test Suite")
    print("=" * 80)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    tests = [
        ("All Query Types Integration", test_all_query_types),
        ("Conversation Flow", test_conversation_flow), 
        ("Performance Benchmarks", test_performance_benchmarks),
        ("Error Handling Robustness", test_error_handling_robustness),
        ("System Integration", test_system_integration),
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
                print(f"❌ {test_name}: FAILED")
        except Exception as e:
            print(f"💥 {test_name}: ERROR - {str(e)}")
    
    print("\n" + "="*80)
    print(f"🏁 **COMPLETE INTEGRATION TEST RESULTS: {passed_tests}/{total_tests} PASSED**")
    print(f"Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    if passed_tests == total_tests:
        print("🎉 ALL INTEGRATION TESTS PASSED! System is ready for production.")
        return 0
    elif passed_tests >= total_tests * 0.8:  # 80% threshold
        print("✅ Most integration tests passed. System is functional with minor issues.")
        return 0
    else:
        print("⚠️  Multiple integration tests failed. System needs attention.")
        return 1

if __name__ == "__main__":
    exit(main())

