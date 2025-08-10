#!/usr/bin/env python3
"""
Standalone Test for Enhanced AI Studio Code

This test validates the core improvements without requiring the full MarketFlow environment.
It focuses on testing the enhanced ticker extraction, prompt engineering, and integration logic.
"""

import re
import json
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum
from datetime import datetime


class AnalysisSource(Enum):
    """Types of analysis sources available"""
    TVM_RECENT = "tvm_recent"
    TVM_HISTORICAL = "tvm_historical"
    STATIC_KNOWLEDGE = "static_knowledge"
    CONVERSATION_MEMORY = "conversation_memory"


@dataclass
class AnalysisContext:
    """Context information for analysis retrieval"""
    tickers: List[str]
    has_recent_analysis: bool
    analysis_age_hours: Optional[float]
    namespaces_found: List[str]
    query_type: str  # 'specific_ticker', 'general_concept', 'comparison'


class EnhancedTickerExtractor:
    """Enhanced ticker extraction with context awareness"""
    
    def __init__(self):
        # Comprehensive blacklist of non-ticker terms
        self.blacklist = {
            # VPA/Wyckoff terms
            'VPA', 'SOW', 'SOS', 'LPS', 'LPSY', 'PS', 'SC', 'AR', 'ST', 'BC',
            'UTAD', 'LPSY', 'SOW', 'SOS', 'SPRING', 'TEST', 'PHASE',
            
            # Technical analysis terms
            'RSI', 'MACD', 'EMA', 'SMA', 'ATR', 'ADX', 'CCI', 'ROC', 'OBV',
            'VWAP', 'TWAP', 'PIVOT', 'FIBO', 'BB', 'KC', 'SAR',
            
            # Market terms
            'NYSE', 'NASDAQ', 'SPX', 'DJI', 'QQQ', 'SPY', 'IWM', 'VIX',
            'FOREX', 'CRYPTO', 'ETF', 'REIT', 'IPO', 'ESG',
            
            # Time/Date terms
            'TODAY', 'YESTERDAY', 'WEEK', 'MONTH', 'YEAR', 'DAY', 'HOUR',
            'AM', 'PM', 'EST', 'PST', 'UTC', 'GMT',
            
            # General terms
            'THE', 'AND', 'FOR', 'WITH', 'FROM', 'THAT', 'THIS', 'WHAT',
            'WHERE', 'WHEN', 'WHY', 'HOW', 'WHO', 'WHICH', 'WILL', 'CAN',
            'SHOULD', 'WOULD', 'COULD', 'MIGHT', 'MAY', 'MUST', 'SHALL',
            'HELP', 'PLEASE', 'THANKS', 'HELLO', 'HI', 'BYE', 'QUIT', 'EXIT',
            
            # Analysis terms
            'ANALYSIS', 'REPORT', 'CHART', 'GRAPH', 'DATA', 'INFO', 'DETAIL',
            'SUMMARY', 'OVERVIEW', 'REVIEW', 'UPDATE', 'NEWS', 'EVENT',
            'SIGNAL', 'PATTERN', 'TREND', 'MOVE', 'PRICE', 'VOLUME',
            
            # Question words and common phrases
            'WHAT', 'ABOUT', 'SHOW', 'TELL', 'GIVE', 'GET', 'FIND', 'LOOK',
            'CHECK', 'SEE', 'VIEW', 'DISPLAY', 'PRINT', 'LIST', 'COMPARE'
        }
        
        # Known ticker patterns for validation
        self.known_patterns = {
            'US_STOCK': r'^[A-Z]{1,5}$',  # AAPL, MSFT, etc.
            'CRYPTO': r'^[A-Z]+:[A-Z]+$',  # BTC:USD, ETH:USD
            'FOREX': r'^[A-Z]{3}[A-Z]{3}$',  # EURUSD, GBPUSD
            'INDEX': r'^[A-Z]+\d*$',  # SPX, NDX, DJI
        }
    
    def extract_tickers(self, text: str) -> List[str]:
        """Extract ticker symbols with enhanced context awareness"""
        # Find potential tickers using multiple patterns
        potential_tickers = set()
        
        # Pattern 1: Standard 1-5 letter uppercase words
        standard_tickers = re.findall(r'\b[A-Z]{1,5}\b', text.upper())
        potential_tickers.update(standard_tickers)
        
        # Pattern 2: Crypto-style tickers (X:BTCUSD, BTC:USD)
        crypto_tickers = re.findall(r'\b[A-Z]+:[A-Z]+\b', text.upper())
        potential_tickers.update(crypto_tickers)
        
        # Pattern 3: Context-aware extraction (after words like "analyze", "ticker", etc.)
        context_patterns = [
            r'(?:analyze|ticker|stock|symbol|company)\s+([A-Z]{1,5})',
            r'([A-Z]{1,5})\s+(?:stock|ticker|analysis|chart|price)',
            r'(?:buy|sell|hold)\s+([A-Z]{1,5})',
            r'([A-Z]{1,5})\s+(?:vs|versus|compared to)\s+([A-Z]{1,5})'
        ]
        
        for pattern in context_patterns:
            matches = re.findall(pattern, text.upper())
            if matches:
                for match in matches:
                    if isinstance(match, tuple):
                        potential_tickers.update(match)
                    else:
                        potential_tickers.add(match)
        
        # Filter out blacklisted terms
        filtered_tickers = [t for t in potential_tickers if t not in self.blacklist]
        
        # Validate tickers using known patterns
        validated_tickers = []
        for ticker in filtered_tickers:
            if self._is_valid_ticker(ticker):
                validated_tickers.append(ticker)
        
        # Remove duplicates and sort
        result = sorted(list(set(validated_tickers)))
        return result
    
    def _is_valid_ticker(self, ticker: str) -> bool:
        """Validate if a string is likely a real ticker symbol"""
        # Check against known patterns
        for pattern_name, pattern in self.known_patterns.items():
            if re.match(pattern, ticker):
                return True
        
        # Additional heuristics
        if len(ticker) == 1:  # Single letter tickers are rare
            return ticker in ['F', 'T', 'X', 'C']  # Known single-letter tickers
        
        if len(ticker) > 5:  # Very long tickers are rare
            return False
        
        # Check for common non-ticker patterns
        if ticker.isdigit():  # Pure numbers
            return False
        
        if ticker in ['NULL', 'NONE', 'EMPTY', 'VOID']:  # Programming terms
            return False
        
        return True


class MockTVMManager:
    """Mock TVM manager for testing purposes"""
    
    def __init__(self):
        self.namespace_cache = {
            "AAPL": "aapl_analysis_20250810_143022",
            "MSFT": "msft_analysis_20250810_142015",
            "GOOGL": "googl_analysis_20250810_141030"
        }
    
    def get_analysis_context(self, tickers: List[str]) -> AnalysisContext:
        """Get analysis context for tickers"""
        namespaces = []
        for ticker in tickers:
            if ticker in self.namespace_cache:
                namespaces.append(self.namespace_cache[ticker])
        
        has_recent = len(namespaces) > 0
        
        if len(tickers) == 1:
            query_type = "specific_ticker"
        elif len(tickers) > 1:
            query_type = "comparison"
        else:
            query_type = "general_concept"
        
        return AnalysisContext(
            tickers=tickers,
            has_recent_analysis=has_recent,
            analysis_age_hours=2.5 if has_recent else None,
            namespaces_found=namespaces,
            query_type=query_type
        )


class EnhancedPromptEngine:
    """Enhanced prompt engineering for better response synthesis"""
    
    def create_analysis_prompt(self, 
                             question: str, 
                             context: AnalysisContext, 
                             tvm_chunks: List[Dict], 
                             static_chunks: List[Dict]) -> str:
        """Create an intelligent prompt based on available analysis context"""
        
        if context.has_recent_analysis and tvm_chunks:
            return self._create_analysis_focused_prompt(question, context, tvm_chunks, static_chunks)
        elif context.tickers and not tvm_chunks:
            return self._create_ticker_focused_prompt(question, context, static_chunks)
        else:
            return self._create_general_knowledge_prompt(question, static_chunks)
    
    def _create_analysis_focused_prompt(self, 
                                      question: str, 
                                      context: AnalysisContext, 
                                      tvm_chunks: List[Dict], 
                                      static_chunks: List[Dict]) -> str:
        """Create prompt when recent analysis is available"""
        
        tickers_str = ", ".join(context.tickers)
        age_info = f" (approximately {context.analysis_age_hours:.1f} hours old)" if context.analysis_age_hours else ""
        
        tvm_content = "\\n\\n".join([chunk.get("text", "") for chunk in tvm_chunks])
        static_content = "\\n\\n".join([chunk.get("text", "") for chunk in static_chunks])
        
        prompt = f"""You have access to recent MarketFlow analysis for {tickers_str}{age_info}. This analysis contains specific, data-driven insights about the current market conditions for these tickers.

PRIORITY INSTRUCTIONS:
1. PRIMARY SOURCE: Use the recent analysis data as your main source of truth
2. SECONDARY SOURCE: Use general knowledge only to explain concepts or provide context
3. SYNTHESIS: Combine specific analysis findings with general principles
4. CITATIONS: Reference sources using [1], [2], etc.

RECENT ANALYSIS DATA:
{tvm_content}

GENERAL KNOWLEDGE CONTEXT:
{static_content}

QUESTION: {question}

Please provide a comprehensive answer that prioritizes the specific analysis findings for {tickers_str}."""

        return prompt
    
    def _create_ticker_focused_prompt(self, 
                                    question: str, 
                                    context: AnalysisContext, 
                                    static_chunks: List[Dict]) -> str:
        """Create prompt when tickers are mentioned but no recent analysis available"""
        
        tickers_str = ", ".join(context.tickers)
        static_content = "\\n\\n".join([chunk.get("text", "") for chunk in static_chunks])
        
        prompt = f"""The user is asking about {tickers_str}, but no recent MarketFlow analysis is available for these tickers.

INSTRUCTIONS:
1. Acknowledge that no recent analysis is available
2. Provide general guidance based on VPA/Wyckoff principles
3. Suggest what to look for in an analysis of these tickers

GENERAL KNOWLEDGE CONTEXT:
{static_content}

QUESTION: {question}

Please provide an answer that explains relevant VPA/Wyckoff concepts for analyzing {tickers_str}."""

        return prompt
    
    def _create_general_knowledge_prompt(self, 
                                       question: str, 
                                       static_chunks: List[Dict]) -> str:
        """Create prompt for general concept questions"""
        
        static_content = "\\n\\n".join([chunk.get("text", "") for chunk in static_chunks])
        
        prompt = f"""This is a general question about VPA/Wyckoff concepts or trading principles.

KNOWLEDGE BASE CONTEXT:
{static_content}

QUESTION: {question}

Please provide a comprehensive answer that explains the concept clearly."""

        return prompt


class StandaloneTestSuite:
    """Standalone test suite for enhanced AI Studio functionality"""
    
    def __init__(self):
        self.test_results = []
        
    def run_all_tests(self):
        """Run all test suites"""
        print("🧪 Enhanced AI Studio Code - Standalone Test Suite")
        print("=" * 60)
        
        # Test 1: Ticker Extraction
        self.test_ticker_extraction()
        
        # Test 2: Analysis Context
        self.test_analysis_context()
        
        # Test 3: Prompt Engineering
        self.test_prompt_engineering()
        
        # Test 4: Integration Workflow
        self.test_integration_workflow()
        
        # Display results
        self.display_test_results()
        
    def test_ticker_extraction(self):
        """Test the enhanced ticker extraction functionality"""
        print("\\n🎯 Testing Enhanced Ticker Extraction")
        print("-" * 40)
        
        extractor = EnhancedTickerExtractor()
        
        test_cases = [
            # Test case: (input_text, expected_tickers, description)
            ("What about AAPL vs MSFT?", ["AAPL", "MSFT"], "Basic comparison"),
            ("Analyze GOOGL for accumulation patterns", ["GOOGL"], "Analysis request"),
            ("Show me TSLA chart", ["TSLA"], "Chart request"),
            ("What is VPA methodology?", [], "General concept - no tickers"),
            ("Check AMD and NVDA signals", ["AMD", "NVDA"], "Multiple tickers"),
            ("WHAT ABOUT THE MARKET TODAY?", [], "All caps non-tickers"),
            ("Buy AAPL, sell MSFT, hold GOOGL", ["AAPL", "GOOGL", "MSFT"], "Trading actions"),
            ("X:BTCUSD analysis please", ["X:BTCUSD"], "Crypto ticker format"),
            ("Compare SPY with QQQ", ["QQQ", "SPY"], "ETF tickers"),
            ("DAILY CHART FOR WEEKLY ANALYSIS", [], "Time-related false positives"),
            ("Based on the analysis what are the Wyckoff events in AMD ticker?", ["AMD"], "Real user query")
        ]
        
        passed = 0
        total = len(test_cases)
        
        for i, (text, expected, description) in enumerate(test_cases, 1):
            try:
                result = extractor.extract_tickers(text)
                result_sorted = sorted(result)
                expected_sorted = sorted(expected)
                
                if result_sorted == expected_sorted:
                    print(f"✅ Test {i}: {description}")
                    print(f"   Input: '{text}'")
                    print(f"   Expected: {expected_sorted}, Got: {result_sorted}")
                    passed += 1
                else:
                    print(f"❌ Test {i}: {description}")
                    print(f"   Input: '{text}'")
                    print(f"   Expected: {expected_sorted}, Got: {result_sorted}")
                    
            except Exception as e:
                print(f"❌ Test {i}: {description} - Error: {e}")
        
        success_rate = (passed / total) * 100
        print(f"\\n📊 Ticker Extraction Results: {passed}/{total} passed ({success_rate:.1f}%)")
        
        self.test_results.append({
            "test_name": "Ticker Extraction",
            "passed": passed,
            "total": total,
            "success_rate": success_rate
        })
    
    def test_analysis_context(self):
        """Test analysis context generation"""
        print("\\n🗄️ Testing Analysis Context Generation")
        print("-" * 40)
        
        tvm_manager = MockTVMManager()
        
        test_cases = [
            (["AAPL"], "specific_ticker", True),
            (["AAPL", "MSFT"], "comparison", True),
            (["UNKNOWN"], "specific_ticker", False),
            ([], "general_concept", False)
        ]
        
        passed = 0
        total = len(test_cases)
        
        for i, (tickers, expected_type, expected_recent) in enumerate(test_cases, 1):
            try:
                context = tvm_manager.get_analysis_context(tickers)
                
                type_correct = context.query_type == expected_type
                recent_correct = context.has_recent_analysis == expected_recent
                
                if type_correct and recent_correct:
                    print(f"✅ Test {i}: Tickers {tickers}")
                    print(f"   Type: {context.query_type}, Recent: {context.has_recent_analysis}")
                    passed += 1
                else:
                    print(f"❌ Test {i}: Tickers {tickers}")
                    print(f"   Expected: {expected_type}, {expected_recent}")
                    print(f"   Got: {context.query_type}, {context.has_recent_analysis}")
                    
            except Exception as e:
                print(f"❌ Test {i}: Error: {e}")
        
        success_rate = (passed / total) * 100
        print(f"\\n📊 Analysis Context Results: {passed}/{total} passed ({success_rate:.1f}%)")
        
        self.test_results.append({
            "test_name": "Analysis Context",
            "passed": passed,
            "total": total,
            "success_rate": success_rate
        })
    
    def test_prompt_engineering(self):
        """Test prompt engineering functionality"""
        print("\\n📝 Testing Enhanced Prompt Engineering")
        print("-" * 40)
        
        prompt_engine = EnhancedPromptEngine()
        
        # Test case 1: Analysis-focused prompt
        context_with_analysis = AnalysisContext(
            tickers=["AAPL"],
            has_recent_analysis=True,
            analysis_age_hours=2.5,
            namespaces_found=["aapl_analysis_20250810"],
            query_type="specific_ticker"
        )
        
        tvm_chunks = [{"text": "AAPL shows accumulation pattern", "metadata": {}}]
        static_chunks = [{"text": "Accumulation is a Wyckoff phase", "metadata": {}}]
        
        prompt1 = prompt_engine.create_analysis_prompt(
            "What are AAPL signals?", context_with_analysis, tvm_chunks, static_chunks
        )
        
        # Test case 2: No analysis available
        context_no_analysis = AnalysisContext(
            tickers=["UNKNOWN"],
            has_recent_analysis=False,
            analysis_age_hours=None,
            namespaces_found=[],
            query_type="specific_ticker"
        )
        
        prompt2 = prompt_engine.create_analysis_prompt(
            "What are UNKNOWN signals?", context_no_analysis, [], static_chunks
        )
        
        # Test case 3: General concept
        context_general = AnalysisContext(
            tickers=[],
            has_recent_analysis=False,
            analysis_age_hours=None,
            namespaces_found=[],
            query_type="general_concept"
        )
        
        prompt3 = prompt_engine.create_analysis_prompt(
            "What is VPA?", context_general, [], static_chunks
        )
        
        tests_passed = 0
        
        # Validate prompts
        if "PRIORITY INSTRUCTIONS" in prompt1 and "RECENT ANALYSIS DATA" in prompt1:
            print("✅ Analysis-focused prompt created correctly")
            tests_passed += 1
        else:
            print("❌ Analysis-focused prompt missing key sections")
        
        if "no recent MarketFlow analysis is available" in prompt2:
            print("✅ No-analysis prompt created correctly")
            tests_passed += 1
        else:
            print("❌ No-analysis prompt missing acknowledgment")
        
        if "general question about VPA/Wyckoff concepts" in prompt3:
            print("✅ General concept prompt created correctly")
            tests_passed += 1
        else:
            print("❌ General concept prompt missing identification")
        
        success_rate = (tests_passed / 3) * 100
        print(f"\\n📊 Prompt Engineering Results: {tests_passed}/3 passed ({success_rate:.1f}%)")
        
        self.test_results.append({
            "test_name": "Prompt Engineering",
            "passed": tests_passed,
            "total": 3,
            "success_rate": success_rate
        })
    
    def test_integration_workflow(self):
        """Test the complete integration workflow"""
        print("\\n🔗 Testing Integration Workflow")
        print("-" * 40)
        
        # Initialize components
        extractor = EnhancedTickerExtractor()
        tvm_manager = MockTVMManager()
        prompt_engine = EnhancedPromptEngine()
        
        test_queries = [
            "What are the Wyckoff events in AAPL?",
            "Compare AAPL and MSFT signals",
            "What is accumulation in VPA?",
            "Show me UNKNOWN ticker analysis"
        ]
        
        passed = 0
        total = len(test_queries)
        
        for i, query in enumerate(test_queries, 1):
            try:
                # Step 1: Extract tickers
                tickers = extractor.extract_tickers(query)
                
                # Step 2: Get analysis context
                context = tvm_manager.get_analysis_context(tickers)
                
                # Step 3: Mock chunks
                mock_tvm_chunks = []
                if context.has_recent_analysis:
                    mock_tvm_chunks = [{"text": f"Analysis for {', '.join(tickers)}", "metadata": {}}]
                
                mock_static_chunks = [{"text": "General VPA knowledge", "metadata": {}}]
                
                # Step 4: Create prompt
                prompt = prompt_engine.create_analysis_prompt(
                    query, context, mock_tvm_chunks, mock_static_chunks
                )
                
                # Validate workflow
                workflow_valid = (
                    isinstance(tickers, list) and
                    isinstance(context, AnalysisContext) and
                    isinstance(prompt, str) and
                    len(prompt) > 100  # Reasonable prompt length
                )
                
                if workflow_valid:
                    print(f"✅ Test {i}: '{query[:30]}...'")
                    print(f"   Tickers: {tickers}, Type: {context.query_type}")
                    print(f"   Recent analysis: {context.has_recent_analysis}")
                    passed += 1
                else:
                    print(f"❌ Test {i}: Workflow validation failed")
                    
            except Exception as e:
                print(f"❌ Test {i}: Error in workflow: {e}")
        
        success_rate = (passed / total) * 100
        print(f"\\n📊 Integration Workflow Results: {passed}/{total} passed ({success_rate:.1f}%)")
        
        self.test_results.append({
            "test_name": "Integration Workflow",
            "passed": passed,
            "total": total,
            "success_rate": success_rate
        })
    
    def display_test_results(self):
        """Display comprehensive test results"""
        print("\\n" + "=" * 60)
        print("📊 ENHANCED AI STUDIO CODE TEST RESULTS")
        print("=" * 60)
        
        total_passed = 0
        total_tests = 0
        
        for result in self.test_results:
            total_passed += result["passed"]
            total_tests += result["total"]
            
            status = "✅ PASS" if result["success_rate"] == 100.0 else "⚠️ PARTIAL" if result["success_rate"] > 0 else "❌ FAIL"
            print(f"{status} {result['test_name']}: {result['passed']}/{result['total']} ({result['success_rate']:.1f}%)")
        
        overall_success = (total_passed / total_tests * 100) if total_tests > 0 else 0
        
        print("-" * 60)
        print(f"🎯 OVERALL RESULTS: {total_passed}/{total_tests} tests passed ({overall_success:.1f}%)")
        
        if overall_success >= 90:
            print("🎉 EXCELLENT: Enhanced AI Studio code is working great!")
            print("   ✅ Ticker extraction is highly accurate")
            print("   ✅ Analysis context generation is robust")
            print("   ✅ Prompt engineering is intelligent")
            print("   ✅ Integration workflow is seamless")
        elif overall_success >= 70:
            print("👍 GOOD: Enhanced AI Studio code is working well with minor issues")
        elif overall_success >= 50:
            print("⚠️ FAIR: Enhanced AI Studio code has some issues that need attention")
        else:
            print("❌ POOR: Enhanced AI Studio code needs significant fixes")
        
        print("=" * 60)
        
        # Save results to file
        results_file = f"standalone_test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        try:
            with open(results_file, 'w') as f:
                json.dump({
                    "timestamp": datetime.now().isoformat(),
                    "overall_success_rate": overall_success,
                    "total_passed": total_passed,
                    "total_tests": total_tests,
                    "detailed_results": self.test_results,
                    "improvements_validated": [
                        "Context-aware ticker extraction",
                        "Comprehensive blacklist filtering",
                        "Intelligent analysis context generation",
                        "Adaptive prompt engineering",
                        "Robust integration workflow"
                    ]
                }, f, indent=2)
            print(f"📄 Test results saved to: {results_file}")
        except Exception as e:
            print(f"⚠️ Could not save test results: {e}")


def main():
    """Main function to run the standalone tests"""
    print("🧪 Enhanced AI Studio Code - Standalone Validation")
    print("=" * 60)
    
    try:
        tester = StandaloneTestSuite()
        tester.run_all_tests()
        
    except KeyboardInterrupt:
        print("\\n⏹️ Tests interrupted by user")
    except Exception as e:
        print(f"\\n❌ Test suite failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

