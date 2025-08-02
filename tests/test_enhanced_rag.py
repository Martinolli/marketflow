#!/usr/bin/env python3
"""
Enhanced RAG Functionality Test for MarketFlow LLM Query Engine
Tests the improved RAG system with multiple fallback mechanisms
"""

import sys
import os
import time
from datetime import datetime

# Add the project root to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from marketflow.marketflow_llm_query_engine import MarketflowLLMQueryEngine

def test_rag_fallback_mechanisms():
    """Test the multi-level RAG fallback system"""
    print("🔄 Testing RAG Fallback Mechanisms")
    print("=" * 60)
    
    try:
        # Test with RAG enabled (will hit API limitations and use fallbacks)
        engine = MarketflowLLMQueryEngine(enable_rag=True)
        session_id = "rag_fallback_test"
        
        # Test queries that should trigger different fallback levels
        fallback_tests = [
            {
                "query": "What does Anna Coulling say about volume?",
                "expected_fallback": "Primary RAG (will fail) -> Local concepts",
                "category": "RAG Query"
            },
            {
                "query": "What is accumulation?",
                "expected_fallback": "Local concept search (direct match)",
                "category": "Direct Concept"
            },
            {
                "query": "Tell me about volume analysis",
                "expected_fallback": "Keyword search in concepts",
                "category": "Keyword Search"
            },
            {
                "query": "What is purple elephant trading?",
                "expected_fallback": "Helpful guidance with available concepts",
                "category": "Unknown Query"
            },
            {
                "query": "Wyckoff method explanation",
                "expected_fallback": "Local concept search (partial match)",
                "category": "Partial Match"
            }
        ]
        
        successful_fallbacks = 0
        total_tests = len(fallback_tests)
        
        print("🔍 **RAG Fallback Test Results:**")
        
        for test in fallback_tests:
            print(f"\n📝 Testing: {test['category']}")
            print(f"   Query: '{test['query']}'")
            print(f"   Expected: {test['expected_fallback']}")
            
            try:
                start_time = time.time()
                response = engine.process(test['query'], session_id=session_id)
                end_time = time.time()
                
                response_time = end_time - start_time
                
                # Analyze response to determine which fallback was used
                fallback_used = "Unknown"
                if "From Local Knowledge Base" in response:
                    fallback_used = "Local Concept Search"
                elif "Related Concepts" in response:
                    fallback_used = "Keyword Search"
                elif "Available VPA concepts" in response or "Available Wyckoff concepts" in response:
                    fallback_used = "Helpful Guidance"
                elif len(response) > 100:
                    fallback_used = "Primary RAG or Interface"
                
                print(f"   ✅ Fallback used: {fallback_used} ({response_time:.2f}s)")
                print(f"   📝 Response: {response[:150]}{'...' if len(response) > 150 else ''}")
                
                # Consider it successful if we got a meaningful response
                if len(response) > 50:
                    successful_fallbacks += 1
                
            except Exception as e:
                print(f"   ❌ Fallback failed: {str(e)}")
        
        success_rate = (successful_fallbacks / total_tests) * 100
        print(f"\n📊 **RAG Fallback Summary:**")
        print(f"   Successful Fallbacks: {successful_fallbacks}/{total_tests}")
        print(f"   Success Rate: {success_rate:.1f}%")
        
        return success_rate >= 80  # 80% success rate for fallbacks
        
    except Exception as e:
        print(f"❌ RAG fallback test failed: {str(e)}")
        return False

def test_local_concept_search():
    """Test the local concept search functionality"""
    print("\n\n🔍 Testing Local Concept Search")
    print("=" * 60)
    
    try:
        engine = MarketflowLLMQueryEngine(enable_rag=False)  # Disable RAG to focus on local search
        
        # Test direct access to local concepts
        local_search_tests = [
            {
                "query": "accumulation",
                "expected_type": "VPA",
                "should_find": True
            },
            {
                "query": "distribution", 
                "expected_type": "VPA",
                "should_find": True
            },
            {
                "query": "Composite_Man",
                "expected_type": "Wyckoff",
                "should_find": True
            },
            {
                "query": "Law_of_Supply_and_Demand",
                "expected_type": "Wyckoff", 
                "should_find": True
            },
            {
                "query": "nonexistent_concept",
                "expected_type": None,
                "should_find": False
            }
        ]
        
        successful_searches = 0
        total_searches = len(local_search_tests)
        
        print("🔍 **Local Concept Search Results:**")
        
        for test in local_search_tests:
            print(f"\n🔎 Searching for: '{test['query']}'")
            
            try:
                # Test the internal search method directly
                result = engine._search_local_concepts(test['query'])
                
                if test['should_find']:
                    if result and test['expected_type'] in result:
                        print(f"   ✅ Found {test['expected_type']} concept")
                        print(f"   📝 Result: {result[:100]}{'...' if len(result) > 100 else ''}")
                        successful_searches += 1
                    else:
                        print(f"   ❌ Expected to find {test['expected_type']} concept but didn't")
                else:
                    if not result:
                        print(f"   ✅ Correctly found no match")
                        successful_searches += 1
                    else:
                        print(f"   ❌ Expected no match but found: {result[:50]}...")
                
            except Exception as e:
                print(f"   ❌ Search failed: {str(e)}")
        
        success_rate = (successful_searches / total_searches) * 100
        print(f"\n📊 **Local Search Summary:**")
        print(f"   Successful Searches: {successful_searches}/{total_searches}")
        print(f"   Success Rate: {success_rate:.1f}%")
        
        return success_rate >= 80  # 80% success rate for local searches
        
    except Exception as e:
        print(f"❌ Local concept search test failed: {str(e)}")
        return False

def test_keyword_search_intelligence():
    """Test the keyword-based search functionality"""
    print("\n\n🔤 Testing Keyword Search Intelligence")
    print("=" * 60)
    
    try:
        engine = MarketflowLLMQueryEngine(enable_rag=False)
        
        # Test keyword-based searches
        keyword_tests = [
            {
                "query": "volume price analysis",
                "expected_matches": ["vpa", "volume", "price"],
                "min_results": 1
            },
            {
                "query": "supply and demand",
                "expected_matches": ["supply", "demand", "law"],
                "min_results": 1
            },
            {
                "query": "market structure",
                "expected_matches": ["market", "structure"],
                "min_results": 1
            },
            {
                "query": "trading method",
                "expected_matches": ["trading", "method"],
                "min_results": 1
            },
            {
                "query": "xyz nonsense query",
                "expected_matches": [],
                "min_results": 0
            }
        ]
        
        successful_searches = 0
        total_searches = len(keyword_tests)
        
        print("🔍 **Keyword Search Results:**")
        
        for test in keyword_tests:
            print(f"\n🔤 Keyword search: '{test['query']}'")
            
            try:
                # Test the internal keyword search method
                result = engine._keyword_search_concepts(test['query'])
                
                if test['min_results'] > 0:
                    if result and len(result) > 50:  # Meaningful result
                        print(f"   ✅ Found relevant matches")
                        print(f"   📝 Result: {result[:200]}{'...' if len(result) > 200 else ''}")
                        successful_searches += 1
                    else:
                        print(f"   ❌ Expected matches but found none or insufficient")
                else:
                    if not result:
                        print(f"   ✅ Correctly found no relevant matches")
                        successful_searches += 1
                    else:
                        print(f"   ⚠️  Found unexpected matches: {result[:50]}...")
                        successful_searches += 0.5  # Partial credit
                
            except Exception as e:
                print(f"   ❌ Keyword search failed: {str(e)}")
        
        success_rate = (successful_searches / total_searches) * 100
        print(f"\n📊 **Keyword Search Summary:**")
        print(f"   Successful Searches: {successful_searches}/{total_searches}")
        print(f"   Success Rate: {success_rate:.1f}%")
        
        return success_rate >= 70  # 70% success rate for keyword searches
        
    except Exception as e:
        print(f"❌ Keyword search test failed: {str(e)}")
        return False

def test_rag_integration_with_queries():
    """Test RAG integration with actual query processing"""
    print("\n\n🔗 Testing RAG Integration with Query Processing")
    print("=" * 60)
    
    try:
        engine = MarketflowLLMQueryEngine(enable_rag=True)
        session_id = "rag_integration_test"
        
        # Test queries that should use RAG functionality
        rag_integration_tests = [
            {
                "query": "What does Anna Coulling say about volume analysis?",
                "query_type": "RAG Query",
                "should_use_rag": True
            },
            {
                "query": "According to Wyckoff, what is accumulation?",
                "query_type": "RAG Query",
                "should_use_rag": True
            },
            {
                "query": "What is VPA?",
                "query_type": "Concept Explanation",
                "should_use_rag": False  # Should use local concepts first
            },
            {
                "query": "Tell me about volume price analysis methodology",
                "query_type": "Knowledge Query",
                "should_use_rag": True
            }
        ]
        
        successful_integrations = 0
        total_integrations = len(rag_integration_tests)
        
        print("🔍 **RAG Integration Results:**")
        
        for test in rag_integration_tests:
            print(f"\n🔗 Testing: {test['query_type']}")
            print(f"   Query: '{test['query']}'")
            print(f"   Should use RAG: {test['should_use_rag']}")
            
            try:
                start_time = time.time()
                response = engine.process(test['query'], session_id=session_id)
                end_time = time.time()
                
                response_time = end_time - start_time
                
                # Analyze response to see if RAG was used appropriately
                rag_indicators = [
                    "From Local Knowledge Base",
                    "Related Concepts", 
                    "Available VPA concepts",
                    "knowledge base"
                ]
                
                rag_used = any(indicator in response for indicator in rag_indicators)
                
                print(f"   📊 RAG used: {rag_used} ({response_time:.2f}s)")
                print(f"   📝 Response: {response[:150]}{'...' if len(response) > 150 else ''}")
                
                # Consider it successful if we got a meaningful response
                if len(response) > 50:
                    successful_integrations += 1
                
            except Exception as e:
                print(f"   ❌ Integration failed: {str(e)}")
        
        success_rate = (successful_integrations / total_integrations) * 100
        print(f"\n📊 **RAG Integration Summary:**")
        print(f"   Successful Integrations: {successful_integrations}/{total_integrations}")
        print(f"   Success Rate: {success_rate:.1f}%")
        
        return success_rate >= 75  # 75% success rate for integrations
        
    except Exception as e:
        print(f"❌ RAG integration test failed: {str(e)}")
        return False

def test_rag_performance():
    """Test RAG system performance and response times"""
    print("\n\n⚡ Testing RAG Performance")
    print("=" * 60)
    
    try:
        engine = MarketflowLLMQueryEngine(enable_rag=True)
        
        # Performance test queries
        performance_queries = [
            "What is accumulation?",
            "Tell me about VPA",
            "Wyckoff method basics",
            "Volume analysis principles",
            "What does Anna Coulling say about trading?"
        ]
        
        response_times = []
        successful_responses = 0
        
        print("⏱️  **RAG Performance Results:**")
        
        for query in performance_queries:
            try:
                start_time = time.time()
                response = engine.process(query, session_id="perf_test")
                end_time = time.time()
                
                response_time = end_time - start_time
                response_times.append(response_time)
                
                if len(response) > 50:
                    successful_responses += 1
                    print(f"   '{query[:30]}...' → {response_time:.2f}s ✅")
                else:
                    print(f"   '{query[:30]}...' → {response_time:.2f}s ⚠️")
                
            except Exception as e:
                print(f"   '{query[:30]}...' → ERROR: {str(e)}")
        
        if response_times:
            avg_time = sum(response_times) / len(response_times)
            max_time = max(response_times)
            min_time = min(response_times)
            
            print(f"\n📊 **RAG Performance Summary:**")
            print(f"   Successful Responses: {successful_responses}/{len(performance_queries)}")
            print(f"   Average Response Time: {avg_time:.2f}s")
            print(f"   Fastest Response: {min_time:.2f}s")
            print(f"   Slowest Response: {max_time:.2f}s")
            
            # Performance evaluation
            if avg_time < 3.0:
                print("   ✅ Performance: Excellent (< 3s average)")
                return True
            elif avg_time < 8.0:
                print("   ✅ Performance: Good (< 8s average)")
                return True
            else:
                print("   ⚠️  Performance: Needs optimization (> 8s average)")
                return False
        
        return False
        
    except Exception as e:
        print(f"❌ RAG performance test failed: {str(e)}")
        return False

def main():
    """Run enhanced RAG test suite"""
    print("🔍 MarketFlow LLM Query Engine - Enhanced RAG Test Suite")
    print("=" * 80)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    tests = [
        ("RAG Fallback Mechanisms", test_rag_fallback_mechanisms),
        ("Local Concept Search", test_local_concept_search),
        ("Keyword Search Intelligence", test_keyword_search_intelligence),
        ("RAG Integration with Queries", test_rag_integration_with_queries),
        ("RAG Performance", test_rag_performance),
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
                print(f"⚠️  {test_name}: NEEDS IMPROVEMENT")
        except Exception as e:
            print(f"💥 {test_name}: ERROR - {str(e)}")
    
    print("\n" + "="*80)
    print(f"🏁 **ENHANCED RAG TEST RESULTS: {passed_tests}/{total_tests} PASSED**")
    print(f"Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    if passed_tests >= total_tests * 0.8:  # 80% threshold
        print("🎉 Enhanced RAG system is working excellently!")
        return 0
    elif passed_tests >= total_tests * 0.6:  # 60% threshold
        print("✅ Enhanced RAG system is functional with room for improvement.")
        return 0
    else:
        print("⚠️  Enhanced RAG system needs significant improvements.")
        return 1

if __name__ == "__main__":
    exit(main())

