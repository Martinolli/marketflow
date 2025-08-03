"""
Enhanced MarketFlow Application Interface - Production Ready

This enhanced version provides a robust and flexible interface that leverages
the full potential of MarketFlow's VPA and Wyckoff analysis capabilities.

Key Enhancements:
- Advanced response processing with multi-format output
- Intelligent query preprocessing and context management
- Enhanced error handling with graceful degradation
- Rich analysis output with visualization support
- Session management with persistent memory
- Performance monitoring and optimization
- Comprehensive logging and debugging
"""

import os
import sys
import json
import time
import logging
import argparse
from typing import Optional, Dict, Any, List
from datetime import datetime
from pathlib import Path

# Add the project root to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from marketflow.marketflow_logger import get_logger
from marketflow.marketflow_config_manager import get_marketflow_config_manager
from marketflow.marketflow_llm_query_engine import MarketflowLLMQueryEngine
from marketflow.enums import QueryIntent, QueryConfidence

# Global configuration
ENHANCED_MODE = True
logger = get_logger(module_name="EnhancedMarketflowApp")

class EnhancedMarketFlowInterface:
    """
    Enhanced interface for MarketFlow with advanced capabilities
    """
    
    def __init__(self, config):
        """Initialize the enhanced interface"""
        self.config = config
        self.logger = get_logger(module_name="EnhancedInterface")
        self.query_engine = None
        self.session_stats = {
            'queries_processed': 0,
            'successful_queries': 0,
            'failed_queries': 0,
            'session_start': datetime.now(),
            'response_times': []
        }
        self.current_context = {
            'ticker': None,
            'timeframes': None,
            'analysis_mode': 'comprehensive',
            'output_format': 'detailed'
        }
        self.conversation_history = []  # Add this line

    def initialize_system(self) -> bool:
        """Initialize the MarketFlow system with enhanced error handling"""
        try:
            self.logger.info("Initializing Enhanced MarketFlow System")
            self.query_engine = MarketflowLLMQueryEngine(config=self.config)
            
            # Validate system components
            validation_results = self._validate_system_components()
            if not validation_results['all_valid']:
                self.logger.warning("Some system components have issues")
                self._display_validation_results(validation_results)
            
            self.logger.info("Enhanced MarketFlow System initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize Enhanced MarketFlow System: {e}")
            self._display_initialization_error(e)
            return False
    
    def _validate_system_components(self) -> Dict[str, Any]:
        """Validate all system components"""
        results = {
            'query_engine': False,
            'memory_manager': False,
            'llm_interface': False,
            'config_manager': False,
            'all_valid': False
        }
        
        try:
            # Test query engine
            if self.query_engine:
                status = self.query_engine.get_configuration_status()
                results['query_engine'] = True
                
            # Test memory manager
            if hasattr(self.query_engine, 'memory') and self.query_engine.memory:
                results['memory_manager'] = True
                
            # Test LLM interface
            if hasattr(self.query_engine, 'interface') and self.query_engine.interface:
                results['llm_interface'] = True
                
            # Test config manager
            if self.config:
                results['config_manager'] = True
                
            results['all_valid'] = all(
                value for key, value in results.items() if key != 'all_valid'
            )
            
        except Exception as e:
            self.logger.error(f"Error during system validation: {e}")
            
        return results
    
    def _display_validation_results(self, results: Dict[str, Any]):
        """Display system validation results"""
        print("\n" + "="*50)
        print("SYSTEM VALIDATION RESULTS")
        print("="*50)
        
        for component, status in results.items():
            if component != 'all_valid':
                icon = "✅" if status else "❌"
                print(f"{icon} {component.replace('_', ' ').title()}: {'OK' if status else 'FAILED'}")
        
        overall_status = "✅ SYSTEM READY" if results['all_valid'] else "⚠️  PARTIAL FUNCTIONALITY"
        print(f"\nOverall Status: {overall_status}")
        print("="*50 + "\n")
    
    def _display_initialization_error(self, error: Exception):
        """Display initialization error with helpful information"""
        print("\n" + "="*60)
        print("❌ INITIALIZATION ERROR")
        print("="*60)
        print(f"Error: {error}")
        print("\nTroubleshooting Steps:")
        print("1. Check your API keys in .env file")
        print("2. Verify internet connection")
        print("3. Ensure all dependencies are installed")
        print("4. Run: python -m pip install -r requirements.txt")
        print("5. Check logs for detailed error information")
        print("="*60 + "\n")
    
    def process_enhanced_query(self, query: str, session_id: str = "default") -> Dict[str, Any]:
        """
        Process query with enhanced capabilities and comprehensive response
        """
        start_time = time.time()
        self.session_stats['queries_processed'] += 1
        
        try:
            # Preprocess query with context
            enhanced_query = self._preprocess_query(query)
            
            # Process with query engine
            response = self.query_engine.process(enhanced_query, session_id=session_id)
            
            # Post-process response for enhanced output
            enhanced_response = self._postprocess_response(query, response)
            
            # Update statistics
            response_time = time.time() - start_time
            self.session_stats['response_times'].append(response_time)
            self.session_stats['successful_queries'] += 1
            
            # Add metadata
            enhanced_response['metadata'] = {
                'response_time': response_time,
                'query_processed': enhanced_query,
                'session_id': session_id,
                'timestamp': datetime.now().isoformat(),
                'context': dict(self.current_context)
            }
            
            return enhanced_response
            
            
        except Exception as e:
            self.session_stats['failed_queries'] += 1
            self.logger.error(f"Error processing enhanced query: {e}")
            
            return {
                'success': False,
                'error': str(e),
                'response': f"I encountered an error processing your query: {e}",
                'suggestions': self._get_error_suggestions(e),
                'metadata': {
                    'response_time': time.time() - start_time,
                    'session_id': session_id,
                    'timestamp': datetime.now().isoformat()
                }
            }
    
    def _preprocess_query(self, query: str) -> str:
        """Preprocess query with context and intelligence"""
        enhanced_query = query.strip()
        
        # Add ticker context if available and not already in query
        if self.current_context['ticker']:
            ticker = self.current_context['ticker']
            if ticker.upper() not in enhanced_query.upper():
                enhanced_query = f"{enhanced_query} for {ticker.upper()}"
        
        # Add analysis mode context
        if self.current_context['analysis_mode'] == 'comprehensive':
            if 'analyze' in enhanced_query.lower() and 'comprehensive' not in enhanced_query.lower():
                enhanced_query = f"Provide comprehensive {enhanced_query}"
        
        # Add timeframe context if specified
        if self.current_context['timeframes']:
            timeframes_str = ', '.join(self.current_context['timeframes'])
            if 'timeframe' not in enhanced_query.lower():
                enhanced_query = f"{enhanced_query} (focus on {timeframes_str} timeframes)"
        
        return enhanced_query
    
    def _postprocess_response(self, original_query: str, response: str) -> Dict[str, Any]:
        """Post-process response for enhanced output"""
        result = {
            'success': True,
            'response': response,
            'original_query': original_query,
            'analysis_type': self._detect_analysis_type(original_query),
            'key_insights': self._extract_key_insights(response),
            'actionable_items': self._extract_actionable_items(response),
            'confidence_level': self._assess_response_confidence(response),
            'related_concepts': self._identify_related_concepts(response)
        }
        
        # Add visualization suggestions if applicable
        if self._should_suggest_visualization(original_query, response):
            result['visualization_suggestions'] = self._get_visualization_suggestions(original_query)
        
        return result
    
    def _detect_analysis_type(self, query: str) -> str:
        """Detect the type of analysis being requested"""
        query_lower = query.lower()
        
        if any(word in query_lower for word in ['compare', 'vs', 'versus']):
            return 'comparison'
        elif any(word in query_lower for word in ['accumulation', 'distribution', 'wyckoff']):
            return 'wyckoff_analysis'
        elif any(word in query_lower for word in ['volume', 'vpa', 'effort', 'result']):
            return 'vpa_analysis'
        elif any(word in query_lower for word in ['pattern', 'signal', 'trend']):
            return 'pattern_analysis'
        elif any(word in query_lower for word in ['what', 'explain', 'define']):
            return 'concept_explanation'
        else:
            return 'general_analysis'
    
    def _extract_key_insights(self, response: str) -> List[str]:
        """Extract key insights from the response"""
        insights = []
        
        # Look for bullet points or numbered lists
        lines = response.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith(('•', '-', '*')) or (line and line[0].isdigit() and '.' in line[:3]):
                insight = line.lstrip('•-*0123456789. ').strip()
                if len(insight) > 10:  # Filter out very short items
                    insights.append(insight)
        
        # If no structured insights found, extract sentences with key terms
        if not insights:
            sentences = response.split('.')
            for sentence in sentences:
                if any(term in sentence.lower() for term in [
                    'signal', 'indicates', 'suggests', 'shows', 'reveals',
                    'accumulation', 'distribution', 'volume', 'price'
                ]):
                    insight = sentence.strip()
                    if len(insight) > 20:
                        insights.append(insight)
        
        return insights[:5]  # Return top 5 insights
    
    def _extract_actionable_items(self, response: str) -> List[str]:
        """Extract actionable items from the response"""
        actionable = []
        
        # Look for action-oriented phrases
        action_patterns = [
            r'should\s+([^.]+)',
            r'consider\s+([^.]+)',
            r'watch\s+for\s+([^.]+)',
            r'monitor\s+([^.]+)',
            r'look\s+for\s+([^.]+)'
        ]
        
        import re
        for pattern in action_patterns:
            matches = re.findall(pattern, response, re.IGNORECASE)
            for match in matches:
                action = match.strip()
                if len(action) > 10:
                    actionable.append(f"Consider {action}")
        
        return actionable[:3]  # Return top 3 actionable items
    
    def _assess_response_confidence(self, response: str) -> str:
        """Assess the confidence level of the response"""
        confidence_indicators = {
            'high': ['clearly', 'definitely', 'strong signal', 'obvious', 'certain'],
            'medium': ['likely', 'suggests', 'indicates', 'appears', 'seems'],
            'low': ['might', 'could', 'possibly', 'uncertain', 'unclear']
        }
        
        response_lower = response.lower()
        
        for level, indicators in confidence_indicators.items():
            if any(indicator in response_lower for indicator in indicators):
                return level
        
        return 'medium'  # Default confidence level
    
    def _identify_related_concepts(self, response: str) -> List[str]:
        """Identify related VPA/Wyckoff concepts mentioned in the response"""
        concepts = []
        
        vpa_concepts = [
            'accumulation', 'distribution', 'effort vs result', 'volume',
            'price action', 'support', 'resistance', 'breakout', 'climax'
        ]
        
        wyckoff_concepts = [
            'composite man', 'cause and effect', 'supply and demand',
            'spring', 'upthrust', 'test', 'markup', 'markdown'
        ]
        
        all_concepts = vpa_concepts + wyckoff_concepts
        response_lower = response.lower()
        
        for concept in all_concepts:
            if concept in response_lower:
                concepts.append(concept.title())
        
        return list(set(concepts))  # Remove duplicates
    
    def _should_suggest_visualization(self, query: str, response: str) -> bool:
        """Determine if visualization suggestions should be provided"""
        viz_keywords = ['chart', 'graph', 'plot', 'analyze', 'pattern', 'trend', 'volume']
        query_lower = query.lower()
        
        return any(keyword in query_lower for keyword in viz_keywords)
    
    def _get_visualization_suggestions(self, query: str) -> List[str]:
        """Get visualization suggestions based on the query"""
        suggestions = []
        query_lower = query.lower()
        
        if 'volume' in query_lower:
            suggestions.append("Volume analysis chart with price overlay")
        
        if any(word in query_lower for word in ['pattern', 'signal', 'trend']):
            suggestions.append("Price action chart with pattern annotations")
        
        if 'compare' in query_lower:
            suggestions.append("Side-by-side comparison charts")
        
        if any(word in query_lower for word in ['accumulation', 'distribution']):
            suggestions.append("Wyckoff phase analysis chart")
        
        if not suggestions:
            suggestions.append("Comprehensive analysis chart with volume and price")
        
        return suggestions
    
    def _get_error_suggestions(self, error: Exception) -> List[str]:
        """Get helpful suggestions based on the error type"""
        error_str = str(error).lower()
        suggestions = []
        
        if 'api' in error_str or 'key' in error_str:
            suggestions.extend([
                "Check your API keys in the .env file",
                "Verify your internet connection",
                "Ensure API quotas are not exceeded"
            ])
        
        if 'ticker' in error_str or 'symbol' in error_str:
            suggestions.extend([
                "Verify the ticker symbol is correct",
                "Try using a different ticker symbol",
                "Check if the market is open"
            ])
        
        if 'timeout' in error_str:
            suggestions.extend([
                "Try again in a moment",
                "Check your internet connection",
                "Consider using a simpler query"
            ])
        
        if not suggestions:
            suggestions.extend([
                "Try rephrasing your query",
                "Check the logs for more details",
                "Restart the application if issues persist"
            ])
        
        return suggestions
    
    def display_enhanced_response(self, result: Dict[str, Any]):
        """Display enhanced response with rich formatting"""
        if not result['success']:
            self._display_error_response(result)
            return
        
        print("\n" + "="*80)
        print("📊 MARKETFLOW ANALYSIS RESPONSE")
        print("="*80)
        
        # Main response
        print(f"\n💬 Response:")
        print("-" * 40)
        print(result['response'])
        
        # Key insights
        if result.get('key_insights'):
            print(f"\n🔍 Key Insights:")
            print("-" * 40)
            for i, insight in enumerate(result['key_insights'], 1):
                print(f"{i}. {insight}")
        
        # Actionable items
        if result.get('actionable_items'):
            print(f"\n🎯 Actionable Items:")
            print("-" * 40)
            for i, item in enumerate(result['actionable_items'], 1):
                print(f"{i}. {item}")
        
        # Related concepts
        if result.get('related_concepts'):
            print(f"\n🔗 Related Concepts:")
            print("-" * 40)
            print(", ".join(result['related_concepts']))
        
        # Visualization suggestions
        if result.get('visualization_suggestions'):
            print(f"\n📈 Visualization Suggestions:")
            print("-" * 40)
            for i, suggestion in enumerate(result['visualization_suggestions'], 1):
                print(f"{i}. {suggestion}")
        
        # Metadata
        metadata = result.get('metadata', {})
        print(f"\n📋 Analysis Details:")
        print("-" * 40)
        print(f"Analysis Type: {result.get('analysis_type', 'Unknown').title()}")
        print(f"Confidence Level: {result.get('confidence_level', 'Medium').title()}")
        print(f"Response Time: {metadata.get('response_time', 0):.2f}s")
        print(f"Timestamp: {metadata.get('timestamp', 'Unknown')}")
        
        print("="*80 + "\n")
    
    def _display_error_response(self, result: Dict[str, Any]):
        """Display error response with helpful information"""
        print("\n" + "="*60)
        print("❌ ERROR PROCESSING QUERY")
        print("="*60)
        print(f"Error: {result.get('error', 'Unknown error')}")
        print(f"Response: {result.get('response', 'No response available')}")
        
        if result.get('suggestions'):
            print(f"\n💡 Suggestions:")
            print("-" * 30)
            for i, suggestion in enumerate(result['suggestions'], 1):
                print(f"{i}. {suggestion}")
        
        print("="*60 + "\n")
    
    def display_session_stats(self):
        """Display session statistics"""
        stats = self.session_stats
        duration = datetime.now() - stats['session_start']
        avg_response_time = sum(stats['response_times']) / len(stats['response_times']) if stats['response_times'] else 0
        
        print("\n" + "="*50)
        print("📊 SESSION STATISTICS")
        print("="*50)
        print(f"Session Duration: {duration}")
        print(f"Queries Processed: {stats['queries_processed']}")
        print(f"Successful Queries: {stats['successful_queries']}")
        print(f"Failed Queries: {stats['failed_queries']}")
        print(f"Success Rate: {(stats['successful_queries']/stats['queries_processed']*100):.1f}%" if stats['queries_processed'] > 0 else "N/A")
        print(f"Average Response Time: {avg_response_time:.2f}s")
        print("="*50 + "\n")
    
    def update_context(self, **kwargs):
        """Update the current context"""
        for key, value in kwargs.items():
            if key in self.current_context:
                self.current_context[key] = value
                self.logger.debug(f"Updated context: {key} = {value}")


# In enhanced_appv1.py

def setup_enhanced_logging(config) -> logging.Logger:
    """Set up enhanced logging configuration"""
    log_dir = os.path.dirname(config.LOG_FILE_PATH)
    os.makedirs(log_dir, exist_ok=True)

    # Create enhanced log format
    log_format = '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'

    logging.basicConfig(
        level=getattr(logging, config.LOG_LEVEL.upper(), logging.INFO),
        format=log_format,
        # Specify encoding for all handlers to prevent crashes
        handlers=[
            logging.FileHandler(config.LOG_FILE_PATH, encoding='utf-8'),
            logging.StreamHandler(sys.stdout) # StreamHandler will use python's default, best to fix at source
        ]
    )
    # A more forceful way for the console is to reconfigure the stream
    # This is often needed for Windows environments
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

    return logging.getLogger("enhanced_marketflow_app")


def parse_enhanced_args() -> argparse.Namespace:
    """Parse command line arguments with enhanced options"""
    parser = argparse.ArgumentParser(
        description="Enhanced MarketFlow Analysis System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python enhanced_app.py --query "Analyze AAPL"
  python enhanced_app.py --ticker MSFT --analysis-mode comprehensive
  python enhanced_app.py --interactive --output-format detailed
  python enhanced_app.py --batch-file queries.txt
        """
    )
    
    # Basic options
    parser.add_argument("--model", help="LLM model to use")
    parser.add_argument("--provider", choices=['openai', 'ollama'], help="LLM provider")
    parser.add_argument("--query", help="Process a single query and exit")
    parser.add_argument("--ticker", help="Ticker symbol for analysis")
    parser.add_argument("--config", help="Path to configuration file")
    
    # Enhanced options
    parser.add_argument("--interactive", action="store_true", help="Run in interactive mode")
    parser.add_argument("--analysis-mode", choices=['basic', 'comprehensive', 'detailed'], 
                       default='comprehensive', help="Analysis depth mode")
    parser.add_argument("--output-format", choices=['simple', 'detailed', 'json'], 
                       default='detailed', help="Output format")
    parser.add_argument("--timeframes", nargs='+', help="Specific timeframes to analyze")
    parser.add_argument("--batch-file", help="Process queries from a file")
    parser.add_argument("--export-results", help="Export results to file")
    
    # System options
    parser.add_argument("--list-models", action="store_true", help="List available models")
    parser.add_argument("--validate-config", action="store_true", help="Validate configuration")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    parser.add_argument("--performance-mode", action="store_true", help="Enable performance monitoring")
    
    return parser.parse_args()


def process_batch_queries(interface: EnhancedMarketFlowInterface, batch_file: str, export_file: Optional[str] = None):
    """Process queries from a batch file"""
    try:
        with open(batch_file, 'r') as f:
            queries = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        
        results = []
        print(f"\n📁 Processing {len(queries)} queries from {batch_file}")
        print("="*60)
        
        for i, query in enumerate(queries, 1):
            print(f"\n[{i}/{len(queries)}] Processing: {query[:50]}...")
            result = interface.process_enhanced_query(query, session_id=f"batch_{i}")
            results.append({
                'query': query,
                'result': result,
                'index': i
            })
            
            if result['success']:
                print(f"✅ Success ({result['metadata']['response_time']:.2f}s)")
            else:
                print(f"❌ Failed: {result.get('error', 'Unknown error')}")
        
        # Export results if requested
        if export_file:
            with open(export_file, 'w') as f:
                json.dump(results, f, indent=2, default=str)
            print(f"\n📄 Results exported to {export_file}")
        
        # Display summary
        successful = sum(1 for r in results if r['result']['success'])
        print(f"\n📊 Batch Summary: {successful}/{len(queries)} successful")
        
    except Exception as e:
        print(f"❌ Error processing batch file: {e}")


def save_chat_history(history, filename):
    """Save chat history to a file"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(history, f, indent=2, default=str)

def load_chat_history(filename):
    """Load chat history from a file"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def enhanced_interactive_mode(interface: EnhancedMarketFlowInterface):
    """Run enhanced interactive mode with chat-like features"""
    print("\n" + "="*80)
    print("🚀 ENHANCED MARKETFLOW CHAT MODE")
    print("="*80)
    
    # Display system status
    interface._display_validation_results(interface._validate_system_components())
    
    print("Chat Commands:")
    print("  /analyze <ticker>     - Comprehensive analysis")
    print("  /compare <t1> <t2>    - Compare two tickers")
    print("  /pattern <ticker>     - Pattern analysis")
    print("  /explain <concept>    - Concept explanation")
    print("  /context              - Show current context")
    print("  /stats                - Show session statistics")
    print("  /mode <basic|comprehensive|detailed> - Set analysis mode")
    print("  /format <simple|detailed|json> - Set output format")
    print("  /ticker <symbol>      - Set default ticker")
    print("  /timeframes <list>    - Set default timeframes")
    print("  /clear                - Clear conversation history")
    print("  /history              - Show conversation history")
    print("  /save <filename>      - Save conversation history")
    print("  /load <filename>      - Load conversation history")
    print("  /exit or /quit        - Exit application")
    print("="*80 + "\n")
    
    session_id = f"chat_{int(time.time())}"
    conversation_history = []

    while True:
        try:
            # Create dynamic prompt
            context_info = []
            if interface.current_context['ticker']:
                context_info.append(f"📊{interface.current_context['ticker']}")
            if interface.current_context['analysis_mode'] != 'comprehensive':
                context_info.append(f"⚙️{interface.current_context['analysis_mode']}")
            
            context_str = f"[{' '.join(context_info)}] " if context_info else ""
            prompt = f"{context_str}You: "
            
            user_input = input(prompt).strip()
            
        except (KeyboardInterrupt, EOFError):
            print("\n👋 Exiting Enhanced MarketFlow Chat...")
            break
        
        if not user_input:
            continue
            
        if user_input.lower() in ('/exit', '/quit'):
            print("👋 Goodbye!")
            break
        
        # Handle chat commands
        if user_input.startswith('/'):
            command = user_input[1:].split()[0].lower()
            args = user_input.split()[1:]
            
            if command == 'context':
                print(f"\n📋 Current Context:")
                for key, value in interface.current_context.items():
                    print(f"  {key}: {value}")
            elif command == 'stats':
                interface.display_session_stats()
            elif command == 'mode' and args:
                mode = args[0]
                if mode in ['basic', 'comprehensive', 'detailed']:
                    interface.update_context(analysis_mode=mode)
                    print(f"✅ Analysis mode set to: {mode}")
                else:
                    print("❌ Invalid mode. Use: basic, comprehensive, or detailed")
            elif command == 'format' and args:
                fmt = args[0]
                if fmt in ['simple', 'detailed', 'json']:
                    interface.update_context(output_format=fmt)
                    print(f"✅ Output format set to: {fmt}")
                else:
                    print("❌ Invalid format. Use: simple, detailed, or json")
            elif command == 'ticker' and args:
                ticker = args[0].upper()
                interface.update_context(ticker=ticker)
                print(f"✅ Default ticker set to: {ticker}")
            elif command == 'timeframes' and args:
                interface.update_context(timeframes=args)
                print(f"✅ Default timeframes set to: {', '.join(args)}")
            elif command == 'clear':
                conversation_history.clear()
                print("🧹 Conversation history cleared")
            elif command == 'history':
                print("\n📜 Conversation History:")
                for i, exchange in enumerate(conversation_history, 1):
                    print(f"{i}. You: {exchange['user'][:50]}...")
                    print(f"   AI: {exchange['ai'][:50]}...")
                    print()
            elif command == 'save' and args:
                filename = args[0]
                save_chat_history(conversation_history, filename)
                print(f"💾 Conversation history saved to {filename}")
            elif command == 'load' and args:
                filename = args[0]
                loaded_history = load_chat_history(filename)
                conversation_history.extend(loaded_history)
                print(f"📂 Conversation history loaded from {filename}")
            else:
                print("❌ Unknown command or missing arguments")
            continue
        
        # Process regular queries
        print(f"\n🔄 Processing query...")
        result = interface.process_enhanced_query(user_input, session_id=session_id)
        
        # Display results based on output format
        if interface.current_context['output_format'] == 'json':
            print(json.dumps(result, indent=2, default=str))
        elif interface.current_context['output_format'] == 'simple':
            if result['success']:
                print(f"\nAI: {result['response']}")
            else:
                print(f"\n❌ AI: {result.get('error', 'Unknown error')}")
        else:  # detailed
            print("\nAI:")
            interface.display_enhanced_response(result)
        
        # Add to conversation history
        conversation_history.append({
            'user': user_input,
            'ai': result['response'] if result['success'] else result.get('error', 'Unknown error'),
            'timestamp': datetime.now().isoformat()
        })

    # Save conversation history on exit
    if conversation_history:
        default_filename = f"chat_history_{session_id}.json"
        save_option = input(f"Do you want to save this conversation? (y/n) [default: {default_filename}]: ")
        if save_option.lower() != 'n':
            filename = input(f"Enter filename to save (or press Enter for default): ") or default_filename
            save_chat_history(conversation_history, filename)
            print(f"💾 Conversation history saved to {filename}")

def main() -> int:
    """Enhanced main function"""
    args = parse_enhanced_args()
    
    try:
        # Initialize configuration
        config = get_marketflow_config_manager(config_file=args.config)
        
        if args.debug:
            config.set_config_value('log_level', 'DEBUG')
        
        # Setup enhanced logging
        logger = setup_enhanced_logging(config)
        logger.info("Starting Enhanced MarketFlow Application")
        
        # Apply command-line overrides
        if args.provider:
            config.set_config_value('llm_provider', args.provider.lower())
        if args.model:
            config.set_llm_model(args.model)
        
        # Handle system commands
        if args.validate_config:
            validation_results = config.validate_configuration()
            print("\n=== Configuration Validation ===")
            for component, is_valid in validation_results.items():
                status = "✅" if is_valid else "❌"
                print(f"{status} {component}: {'Valid' if is_valid else 'Invalid'}")
            return 0 if all(validation_results.values()) else 1
        
        if args.list_models:
            print(f"\n📋 Available Models for {config.LLM_PROVIDER}:")
            models = config.get_available_models()
            for model in models:
                current = " (current)" if model == config.get_llm_model() else ""
                print(f"  • {model}{current}")
            return 0
        
        # Initialize enhanced interface
        interface = EnhancedMarketFlowInterface(config)
        
        # Update context from command line args
        if args.ticker:
            interface.update_context(ticker=args.ticker.upper())
        if args.analysis_mode:
            interface.update_context(analysis_mode=args.analysis_mode)
        if args.output_format:
            interface.update_context(output_format=args.output_format)
        if args.timeframes:
            interface.update_context(timeframes=args.timeframes)
        
        # Initialize system
        if not interface.initialize_system():
            return 1
        
        # Handle different execution modes
        if args.batch_file:
            process_batch_queries(interface, args.batch_file, args.export_results)
        elif args.query:
            result = interface.process_enhanced_query(args.query)
            if args.output_format == 'json':
                print(json.dumps(result, indent=2, default=str))
            else:
                interface.display_enhanced_response(result)
        else:
            enhanced_interactive_mode(interface)
        
        # Display final statistics
        if args.performance_mode:
            interface.display_session_stats()
        
        return 0
        
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        if args.debug:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())

