"""
MarketFlow LLM Query Engine - Enhanced Version
---------------------------------------------
Handles all LLM-driven query processing for MarketFlow with robust architecture.

Features:
- Provider-agnostic LLM interface with OpenAI as default
- Advanced intent recognition with confidence scoring
- RAG integration for knowledge retrieval
- Multi-turn conversation support
- Comprehensive error handling and logging
- Input validation and sanitization
"""

import re
import json
import traceback
from typing import Any, Dict, List, Optional, Tuple, Union
from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime

# MarketFlow imports
from marketflow.marketflow_llm_interface import MarketflowLLMInterface
from marketflow.marketflow_llm_narrative import generate_analysis_narrative
from marketflow.marketflow_logger import get_logger
from marketflow.marketflow_config_manager import create_app_config
from marketflow.enums import QueryIntent, QueryConfidence

# RAG imports
from rag.retriever import chroma_retrieve_top_chunks


@dataclass
class IntentResult:
    """Result of intent parsing"""
    intent: QueryIntent
    confidence: QueryConfidence
    confidence_score: float
    parameters: Dict[str, Any] = field(default_factory=dict)
    alternative_intents: List[Tuple[QueryIntent, float]] = field(default_factory=list)


@dataclass
class QueryContext:
    """Context for multi-turn conversations"""
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    conversation_history: List[Dict[str, Any]] = field(default_factory=list)
    last_ticker: Optional[str] = None
    last_timeframes: Optional[List[str]] = None
    context_window: int = 5  # Number of previous exchanges to keep


class MarketflowLLMQueryEngine:
    """
    Enhanced LLM Query Engine for MarketFlow with robust architecture
    """
    
    def __init__(self, 
                 interface: Optional[MarketflowLLMInterface] = None,
                 enable_rag: bool = True,
                 max_context_length: int = 5):
        """
        Initialize the enhanced query engine
        
        Args:
            interface: Optional MarketflowLLMInterface instance
            enable_rag: Whether to enable RAG functionality
            max_context_length: Maximum conversation context length
        """
        # Initialize logging and configuration
        self.logger = get_logger(module_name="MarketflowLLMQueryEngine")
        self.config_manager = create_app_config(logger=self.logger)
        
        self.logger.info("Initializing Enhanced MarketFlow LLM Query Engine")
        
        try:
            # Initialize core components
            self.interface = interface or MarketflowLLMInterface()
            self.enable_rag = enable_rag
            self.max_context_length = max_context_length
            
            # Initialize conversation contexts (keyed by session_id)
            self.contexts: Dict[str, QueryContext] = {}
            
            # Initialize intent patterns for parsing
            self._initialize_intent_patterns()
            
            # Initialize ticker validation patterns
            self._initialize_ticker_patterns()
            
            self.logger.info("MarketFlow LLM Query Engine initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize query engine: {str(e)}", exc_info=True)
            raise
    
    def _initialize_intent_patterns(self):
        """Initialize regex patterns for intent recognition"""
        self.intent_patterns = {
            QueryIntent.TICKER_ANALYSIS: [
                (r'\b(analyze|analysis|check|examine|look at|review)\s+([A-Z]{1,5})\b', 0.9),
                (r'\b([A-Z]{1,5})\s+(analysis|signal|vpa|wyckoff)', 0.8),
                (r'\bwhat.*signal.*([A-Z]{1,5})', 0.7),
                (r'\bhow.*([A-Z]{1,5}).*performing', 0.6),
            ],
            QueryIntent.CONCEPT_EXPLANATION: [
                (r'\b(what is|explain|define|describe)\s+(.+)', 0.9),
                (r'\btell me about\s+(.+)', 0.8),
                (r'\b(spring|accumulation|distribution|climax|wyckoff|vpa)\b', 0.7),
            ],
            QueryIntent.COMPARISON: [
                (r'\b(compare|vs|versus|against)\b', 0.9),
                (r'\b([A-Z]{1,5})\s+(and|vs|versus)\s+([A-Z]{1,5})', 0.8),
                (r'\bdifference between\s+([A-Z]{1,5})\s+and\s+([A-Z]{1,5})', 0.7),
            ],
            QueryIntent.RAG_QUERY: [
                (r'\b(according to|what does|says about|mentions)\b', 0.8),
                (r'\b(anna coulling|wyckoff|book|source|reference)\b', 0.7),
                (r'\bin the (context|literature|material)', 0.6),
            ],
            QueryIntent.MULTI_TIMEFRAME: [
                (r'\b(all timeframes|multiple timeframes|across.*timeframes)', 0.9),
                (r'\b(daily|weekly|hourly|1h|4h|1d|1w)\b.*\b(daily|weekly|hourly|1h|4h|1d|1w)\b', 0.8),
            ]
        }
    
    def _initialize_ticker_patterns(self):
        """Initialize patterns for ticker validation"""
        # Common ticker patterns (1-5 uppercase letters)
        self.ticker_pattern = re.compile(r'\b[A-Z]{1,5}\b')
        
        # Common false positives to filter out
        self.ticker_blacklist = {
            'VPA', 'LLM', 'API', 'USD', 'EUR', 'GBP', 'JPY', 'CAD', 'AUD',
            'THE', 'AND', 'FOR', 'ARE', 'BUT', 'NOT', 'YOU', 'ALL', 'CAN',
            'HAD', 'HER', 'WAS', 'ONE', 'OUR', 'OUT', 'DAY', 'GET', 'HAS',
            'HIM', 'HOW', 'ITS', 'MAY', 'NEW', 'NOW', 'OLD', 'SEE', 'TWO',
            'WHO', 'BOY', 'DID', 'ITS', 'LET', 'PUT', 'SAY', 'SHE', 'TOO', 'USE'
        }
    
    def validate_input(self, user_input: str) -> Tuple[bool, Optional[str]]:
        """
        Validate and sanitize user input
        
        Args:
            user_input: Raw user input string
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not user_input or not isinstance(user_input, str):
            return False, "Input must be a non-empty string"
        
        # Check length limits
        if len(user_input.strip()) == 0:
            return False, "Input cannot be empty or only whitespace"
        
        if len(user_input) > 1000:
            return False, "Input too long (maximum 1000 characters)"
        
        # Check for potentially malicious content
        suspicious_patterns = [
            r'<script',
            r'javascript:',
            r'eval\(',
            r'exec\(',
        ]
        
        for pattern in suspicious_patterns:
            if re.search(pattern, user_input, re.IGNORECASE):
                return False, "Input contains potentially unsafe content"
        
        return True, None
    
    def extract_tickers(self, text: str) -> List[str]:
        """
        Extract valid ticker symbols from text
        
        Args:
            text: Input text to search for tickers
            
        Returns:
            List of valid ticker symbols
        """
        potential_tickers = self.ticker_pattern.findall(text.upper())
        
        # Filter out blacklisted words and duplicates
        valid_tickers = []
        for ticker in potential_tickers:
            if ticker not in self.ticker_blacklist and ticker not in valid_tickers:
                valid_tickers.append(ticker)
        
        return valid_tickers
    
    def _parse_intent(self, user_input: str) -> IntentResult:
        """
        Enhanced intent parsing with confidence scoring
        
        Args:
            user_input: User's input string
            
        Returns:
            IntentResult with intent, confidence, and parameters
        """
        user_input_lower = user_input.lower()
        intent_scores = {}
        
        # Score each intent based on pattern matching
        for intent, patterns in self.intent_patterns.items():
            max_score = 0.0
            matched_params = {}
            
            for pattern, base_score in patterns:
                match = re.search(pattern, user_input_lower)
                if match:
                    # Adjust score based on match quality
                    score = base_score
                    
                    # Bonus for exact matches
                    if match.group(0) == user_input_lower.strip():
                        score += 0.1
                    
                    # Extract parameters based on intent type
                    if intent == QueryIntent.TICKER_ANALYSIS:
                        tickers = self.extract_tickers(user_input)
                        if tickers:
                            matched_params['tickers'] = tickers
                            matched_params['primary_ticker'] = tickers[0]
                    
                    elif intent == QueryIntent.CONCEPT_EXPLANATION:
                        # Extract concept from the match
                        if len(match.groups()) > 0:
                            concept = match.group(-1).strip()
                            matched_params['concept'] = concept
                    
                    elif intent == QueryIntent.COMPARISON:
                        tickers = self.extract_tickers(user_input)
                        if len(tickers) >= 2:
                            matched_params['tickers'] = tickers[:2]  # Take first two
                    
                    max_score = max(max_score, score)
            
            if max_score > 0:
                intent_scores[intent] = (max_score, matched_params)
        
        # Determine best intent
        if not intent_scores:
            return IntentResult(
                intent=QueryIntent.UNKNOWN,
                confidence=QueryConfidence.LOW,
                confidence_score=0.0,
                parameters={}
            )
        
        # Sort by score and get the best match
        sorted_intents = sorted(intent_scores.items(), key=lambda x: x[1][0], reverse=True)
        best_intent, (best_score, best_params) = sorted_intents[0]
        
        # Determine confidence level
        if best_score >= 0.8:
            confidence = QueryConfidence.HIGH
        elif best_score >= 0.5:
            confidence = QueryConfidence.MEDIUM
        else:
            confidence = QueryConfidence.LOW
        
        # Prepare alternative intents
        alternatives = [(intent, score) for intent, (score, _) in sorted_intents[1:3]]
        
        return IntentResult(
            intent=best_intent,
            confidence=confidence,
            confidence_score=best_score,
            parameters=best_params,
            alternative_intents=alternatives
        )

    def get_or_create_context(self, session_id: str = "default") -> QueryContext:
        """
        Get or create conversation context for a session
        
        Args:
            session_id: Session identifier
            
        Returns:
            QueryContext for the session
        """
        if session_id not in self.contexts:
            self.contexts[session_id] = QueryContext(session_id=session_id)
        
        return self.contexts[session_id]

    def update_context(self, context: QueryContext, user_input: str, response: str, 
                      intent_result: IntentResult):
        """
        Update conversation context with new exchange
        
        Args:
            context: Context to update
            user_input: User's input
            response: System response
            intent_result: Parsed intent result
        """
        # Add to conversation history
        exchange = {
            "timestamp": datetime.now().isoformat(),
            "user_input": user_input,
            "response": response,
            "intent": intent_result.intent.value,
            "confidence": intent_result.confidence_score,
            "parameters": intent_result.parameters
        }
        
        context.conversation_history.append(exchange)
        
        # Maintain context window
        if len(context.conversation_history) > self.max_context_length:
            context.conversation_history = context.conversation_history[-self.max_context_length:]
        
        # Update context state
        if 'primary_ticker' in intent_result.parameters:
            context.last_ticker = intent_result.parameters['primary_ticker']
        
        if 'timeframes' in intent_result.parameters:
            context.last_timeframes = intent_result.parameters['timeframes']


# This is the first part of the enhanced query engine
# The implementation will continue with the main process method and handlers


    def process(self, user_input: str, session_id: str = "default", 
                metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        Main entry point: process a user's query and return a response
        
        Args:
            user_input: User's natural language query
            session_id: Session identifier for conversation context
            metadata: Optional metadata for the query
            
        Returns:
            Response string
        """
        try:
            # Validate input
            is_valid, error_msg = self.validate_input(user_input)
            if not is_valid:
                self.logger.warning(f"Invalid input: {error_msg}")
                return f"Invalid input: {error_msg}"
            
            # Get conversation context
            context = self.get_or_create_context(session_id)
            
            # Parse intent
            intent_result = self._parse_intent(user_input)
            
            self.logger.info(f"Processing query with intent: {intent_result.intent.value} "
                           f"(confidence: {intent_result.confidence.value})")
            
            # Route to appropriate handler
            response = self._route_query(intent_result, user_input, context)
            
            # Update conversation context
            self.update_context(context, user_input, response, intent_result)
            
            return response
            
        except Exception as e:
            error_msg = f"An error occurred while processing your query: {str(e)}"
            self.logger.error(f"Error in process(): {str(e)}", exc_info=True)
            return error_msg
    
    def _route_query(self, intent_result: IntentResult, user_input: str, 
                    context: QueryContext) -> str:
        """
        Route query to appropriate handler based on intent
        
        Args:
            intent_result: Parsed intent result
            user_input: Original user input
            context: Conversation context
            
        Returns:
            Response string
        """
        try:
            if intent_result.intent == QueryIntent.TICKER_ANALYSIS:
                return self.handle_ticker_analysis(intent_result.parameters, context)
            
            elif intent_result.intent == QueryIntent.CONCEPT_EXPLANATION:
                return self.handle_concept_explanation(intent_result.parameters, context)
            
            elif intent_result.intent == QueryIntent.RAG_QUERY:
                return self.handle_rag_query(intent_result.parameters, user_input, context)
            
            elif intent_result.intent == QueryIntent.COMPARISON:
                return self.handle_comparison_query(intent_result.parameters, context)
            
            elif intent_result.intent == QueryIntent.MULTI_TIMEFRAME:
                return self.handle_multi_timeframe_query(intent_result.parameters, context)
            
            elif intent_result.intent == QueryIntent.HISTORICAL_ANALYSIS:
                return self.handle_historical_analysis(intent_result.parameters, context)
            
            else:
                return self._handle_unknown_query(user_input, intent_result, context)
                
        except Exception as e:
            self.logger.error(f"Error in query routing: {str(e)}", exc_info=True)
            return f"I encountered an error while processing your request: {str(e)}"
    
    def handle_ticker_analysis(self, params: Dict[str, Any], 
                              context: QueryContext) -> str:
        """
        Handle ticker analysis queries
        
        Args:
            params: Parsed parameters containing ticker information
            context: Conversation context
            
        Returns:
            Analysis response string
        """
        try:
            # Get ticker from params or context
            ticker = params.get('primary_ticker') or context.last_ticker
            
            if not ticker:
                return ("I need a ticker symbol to perform analysis. "
                       "Please specify a ticker like 'Analyze AAPL' or 'Check MSFT signal'.")
            
            self.logger.info(f"Performing ticker analysis for: {ticker}")
            
            # Get analysis from interface
            analysis_result = self.interface.get_ticker_analysis(ticker)
            
            # Check for errors
            if isinstance(analysis_result, dict) and "error" in analysis_result:
                return f"I couldn't analyze {ticker}: {analysis_result['error']}"
            
            # Generate narrative response
            if isinstance(analysis_result, dict) and "analysis_narrative" in analysis_result:
                response = analysis_result["analysis_narrative"]
            else:
                # Fallback to generating narrative
                response = generate_analysis_narrative(analysis_result)
            
            return response
            
        except Exception as e:
            self.logger.error(f"Error in ticker analysis: {str(e)}", exc_info=True)
            return f"I encountered an error analyzing {params.get('primary_ticker', 'the ticker')}: {str(e)}"
    
    def handle_concept_explanation(self, params: Dict[str, Any], 
                                  context: QueryContext) -> str:
        """
        Handle concept explanation queries
        
        Args:
            params: Parsed parameters containing concept information
            context: Conversation context
            
        Returns:
            Concept explanation string
        """
        try:
            concept = params.get('concept', '').strip()
            
            if not concept:
                return ("Please specify which concept you'd like me to explain. "
                       "For example: 'What is a Wyckoff Spring?' or 'Explain accumulation'.")
            
            self.logger.info(f"Explaining concept: {concept}")
            
            # Try to get explanation from interface
            explanation = self.interface.explain_concept(concept)
            
            # If not found, try RAG search as fallback
            if "not found" in explanation.lower() and self.enable_rag:
                self.logger.info(f"Concept not found in interface, trying RAG search for: {concept}")
                rag_results = self._perform_rag_search(f"explain {concept}", top_k=3)
                
                if rag_results:
                    explanation = f"Based on the knowledge base:\n\n{rag_results}"
                else:
                    explanation = (f"I don't have specific information about '{concept}'. "
                                 f"Could you try rephrasing or asking about a related VPA/Wyckoff concept?")
            
            return explanation
            
        except Exception as e:
            self.logger.error(f"Error in concept explanation: {str(e)}", exc_info=True)
            return f"I encountered an error explaining the concept: {str(e)}"
    
    def handle_rag_query(self, params: Dict[str, Any], user_input: str, 
                        context: QueryContext) -> str:
        """
        Handle RAG-based knowledge queries
        
        Args:
            params: Parsed parameters
            user_input: Original user input for RAG search
            context: Conversation context
            
        Returns:
            RAG-based response string
        """
        try:
            if not self.enable_rag:
                return "Knowledge base search is currently disabled."
            
            self.logger.info(f"Performing RAG query: {user_input}")
            
            # Perform RAG search
            rag_results = self._perform_rag_search(user_input, top_k=5)
            
            if rag_results:
                return f"Based on the knowledge base:\n\n{rag_results}"
            else:
                return ("I couldn't find relevant information in the knowledge base. "
                       "Try rephrasing your question or asking about specific VPA/Wyckoff concepts.")
            
        except Exception as e:
            self.logger.error(f"Error in RAG query: {str(e)}", exc_info=True)
            return f"I encountered an error searching the knowledge base: {str(e)}"
    
    def handle_comparison_query(self, params: Dict[str, Any], 
                               context: QueryContext) -> str:
        """
        Handle ticker comparison queries
        
        Args:
            params: Parsed parameters containing ticker information
            context: Conversation context
            
        Returns:
            Comparison response string
        """
        try:
            tickers = params.get('tickers', [])
            
            if len(tickers) < 2:
                return ("I need at least two ticker symbols to make a comparison. "
                       "For example: 'Compare AAPL and MSFT' or 'AAPL vs GOOGL'.")
            
            ticker1, ticker2 = tickers[0], tickers[1]
            self.logger.info(f"Comparing tickers: {ticker1} vs {ticker2}")
            
            # Get analysis for both tickers
            analysis1 = self.interface.get_ticker_analysis(ticker1)
            analysis2 = self.interface.get_ticker_analysis(ticker2)
            
            # Check for errors
            if isinstance(analysis1, dict) and "error" in analysis1:
                return f"I couldn't analyze {ticker1}: {analysis1['error']}"
            
            if isinstance(analysis2, dict) and "error" in analysis2:
                return f"I couldn't analyze {ticker2}: {analysis2['error']}"
            
            # Generate comparison
            comparison = self._generate_comparison(analysis1, analysis2, ticker1, ticker2)
            
            return comparison
            
        except Exception as e:
            self.logger.error(f"Error in comparison query: {str(e)}", exc_info=True)
            return f"I encountered an error comparing the tickers: {str(e)}"
    
    def handle_multi_timeframe_query(self, params: Dict[str, Any], 
                                    context: QueryContext) -> str:
        """
        Handle multi-timeframe analysis queries
        
        Args:
            params: Parsed parameters
            context: Conversation context
            
        Returns:
            Multi-timeframe analysis response
        """
        try:
            ticker = params.get('primary_ticker') or context.last_ticker
            
            if not ticker:
                return ("I need a ticker symbol for multi-timeframe analysis. "
                       "For example: 'Show AAPL across all timeframes'.")
            
            self.logger.info(f"Performing multi-timeframe analysis for: {ticker}")
            
            # Get full analysis (which includes all timeframes)
            analysis_result = self.interface.get_ticker_analysis(ticker)
            
            if isinstance(analysis_result, dict) and "error" in analysis_result:
                return f"I couldn't analyze {ticker}: {analysis_result['error']}"
            
            # Generate multi-timeframe summary
            response = self._generate_multi_timeframe_summary(analysis_result, ticker)
            
            return response
            
        except Exception as e:
            self.logger.error(f"Error in multi-timeframe query: {str(e)}", exc_info=True)
            return f"I encountered an error with multi-timeframe analysis: {str(e)}"
    
    def handle_historical_analysis(self, params: Dict[str, Any], 
                                  context: QueryContext) -> str:
        """
        Handle historical analysis queries (placeholder for future implementation)
        
        Args:
            params: Parsed parameters
            context: Conversation context
            
        Returns:
            Historical analysis response
        """
        return ("Historical analysis is not yet implemented. "
               "Currently, I can provide current market analysis for tickers.")
    
    def _handle_unknown_query(self, user_input: str, intent_result: IntentResult, 
                             context: QueryContext) -> str:
        """
        Handle queries with unknown or low-confidence intent
        
        Args:
            user_input: Original user input
            intent_result: Intent parsing result
            context: Conversation context
            
        Returns:
            Helpful response string
        """
        # If confidence is very low, try RAG as fallback
        if intent_result.confidence == QueryConfidence.LOW and self.enable_rag:
            try:
                rag_results = self._perform_rag_search(user_input, top_k=3)
                if rag_results:
                    return f"I found this information that might help:\n\n{rag_results}"
            except Exception as e:
                self.logger.error(f"Error in fallback RAG search: {str(e)}")
        
        # Provide helpful guidance
        help_text = """I'm not sure what you're asking for. Here are some things I can help with:

• **Ticker Analysis**: "Analyze AAPL" or "What's the VPA signal for MSFT?"
• **Concept Explanations**: "What is a Wyckoff Spring?" or "Explain accumulation"
• **Comparisons**: "Compare AAPL and GOOGL" or "AAPL vs MSFT"
• **Knowledge Search**: "What does Anna Coulling say about volume?"
• **Multi-timeframe**: "Show AAPL across all timeframes"

Please try rephrasing your question or ask about a specific ticker or concept."""
        
        return help_text


    def _perform_rag_search(self, query: str, top_k: int = 5) -> Optional[str]:
        """
        Perform RAG search using the existing retriever
        
        Args:
            query: Search query
            top_k: Number of results to retrieve
            
        Returns:
            Formatted search results or None
        """
        try:
            # Use the existing RAG retriever
            results = chroma_retrieve_top_chunks(query, top_k=top_k)
            
            if not results:
                return None
            
            # Format results
            formatted_results = []
            for i, result in enumerate(results, 1):
                # Handle different result formats
                if isinstance(result, dict):
                    content = result.get('content', result.get('text', str(result)))
                    source = result.get('source', 'Unknown')
                    formatted_results.append(f"**Source {i}** ({source}):\n{content}")
                else:
                    formatted_results.append(f"**Result {i}**:\n{str(result)}")
            
            return "\n\n".join(formatted_results)
            
        except Exception as e:
            self.logger.error(f"Error in RAG search: {str(e)}", exc_info=True)
            return None
    
    def _generate_comparison(self, analysis1: Dict, analysis2: Dict, 
                           ticker1: str, ticker2: str) -> str:
        """
        Generate comparison between two ticker analyses
        
        Args:
            analysis1: Analysis result for first ticker
            analysis2: Analysis result for second ticker
            ticker1: First ticker symbol
            ticker2: Second ticker symbol
            
        Returns:
            Formatted comparison string
        """
        try:
            comparison = f"**Comparison: {ticker1} vs {ticker2}**\n\n"
            
            # Compare signals
            signal1 = analysis1.get('vpa_signal', {})
            signal2 = analysis2.get('vpa_signal', {})
            
            comparison += f"**VPA Signals:**\n"
            comparison += f"• {ticker1}: {signal1.get('type', 'Unknown')} ({signal1.get('strength', 'Unknown')})\n"
            comparison += f"• {ticker2}: {signal2.get('type', 'Unknown')} ({signal2.get('strength', 'Unknown')})\n\n"
            
            # Compare current prices
            price1 = analysis1.get('current_price')
            price2 = analysis2.get('current_price')
            
            if price1 and price2:
                comparison += f"**Current Prices:**\n"
                comparison += f"• {ticker1}: ${price1:.2f}\n"
                comparison += f"• {ticker2}: ${price2:.2f}\n\n"
            
            # Compare risk assessments
            risk1 = analysis1.get('risk_assessment', {})
            risk2 = analysis2.get('risk_assessment', {})
            
            rr1 = risk1.get('risk_reward_ratio', 0)
            rr2 = risk2.get('risk_reward_ratio', 0)
            
            if rr1 and rr2:
                comparison += f"**Risk/Reward Ratios:**\n"
                comparison += f"• {ticker1}: {rr1:.2f}\n"
                comparison += f"• {ticker2}: {rr2:.2f}\n\n"
            
            # Add recommendation
            if signal1.get('type') == 'BUY' and signal2.get('type') != 'BUY':
                comparison += f"**Recommendation:** {ticker1} shows a stronger bullish signal than {ticker2}."
            elif signal2.get('type') == 'BUY' and signal1.get('type') != 'BUY':
                comparison += f"**Recommendation:** {ticker2} shows a stronger bullish signal than {ticker1}."
            elif rr1 > rr2:
                comparison += f"**Recommendation:** {ticker1} offers a better risk/reward ratio."
            elif rr2 > rr1:
                comparison += f"**Recommendation:** {ticker2} offers a better risk/reward ratio."
            else:
                comparison += "**Recommendation:** Both tickers show similar characteristics. Consider other factors for decision making."
            
            return comparison
            
        except Exception as e:
            self.logger.error(f"Error generating comparison: {str(e)}", exc_info=True)
            return f"I encountered an error while comparing {ticker1} and {ticker2}: {str(e)}"
    
    def _generate_multi_timeframe_summary(self, analysis: Dict, ticker: str) -> str:
        """
        Generate multi-timeframe analysis summary
        
        Args:
            analysis: Full analysis result
            ticker: Ticker symbol
            
        Returns:
            Multi-timeframe summary string
        """
        try:
            summary = f"**Multi-Timeframe Analysis for {ticker}**\n\n"
            
            timeframe_data = analysis.get('timeframe_data', {})
            
            if not timeframe_data:
                return f"No multi-timeframe data available for {ticker}."
            
            # Analyze each timeframe
            for timeframe, data in timeframe_data.items():
                summary += f"**{timeframe.upper()} Timeframe:**\n"
                
                # Trend information
                trend = data.get('trend', {})
                if trend:
                    direction = trend.get('direction', 'Unknown')
                    strength = trend.get('strength', 'Unknown')
                    summary += f"• Trend: {direction} ({strength})\n"
                
                # Wyckoff context
                wyckoff = data.get('wyckoff', {})
                if wyckoff:
                    context = wyckoff.get('context', 'Unknown')
                    phases = wyckoff.get('phases', [])
                    if phases:
                        latest_phase = phases[-1]
                        phase_name = latest_phase.get('phase', 'Unknown')
                        summary += f"• Wyckoff: {context} - Phase {phase_name}\n"
                
                # Support/Resistance
                sr = data.get('support_resistance', {})
                if sr:
                    support = sr.get('support_level')
                    resistance = sr.get('resistance_level')
                    if support and resistance:
                        summary += f"• Support: ${support:.2f}, Resistance: ${resistance:.2f}\n"
                
                summary += "\n"
            
            # Overall assessment
            primary_signal = analysis.get('vpa_signal', {})
            summary += f"**Overall Assessment:**\n"
            summary += f"Primary Signal: {primary_signal.get('type', 'Unknown')} ({primary_signal.get('strength', 'Unknown')})\n"
            
            # Look for timeframe alignment
            bullish_tfs = []
            bearish_tfs = []
            
            for tf, data in timeframe_data.items():
                trend = data.get('trend', {})
                direction = trend.get('direction', '').lower()
                
                if 'up' in direction or 'bull' in direction:
                    bullish_tfs.append(tf)
                elif 'down' in direction or 'bear' in direction:
                    bearish_tfs.append(tf)
            
            if len(bullish_tfs) > len(bearish_tfs):
                summary += f"Multiple timeframes ({', '.join(bullish_tfs)}) show bullish alignment."
            elif len(bearish_tfs) > len(bullish_tfs):
                summary += f"Multiple timeframes ({', '.join(bearish_tfs)}) show bearish alignment."
            else:
                summary += "Mixed signals across timeframes - exercise caution."
            
            return summary
            
        except Exception as e:
            self.logger.error(f"Error generating multi-timeframe summary: {str(e)}", exc_info=True)
            return f"I encountered an error generating the multi-timeframe summary: {str(e)}"
    
    def get_conversation_history(self, session_id: str = "default") -> List[Dict[str, Any]]:
        """
        Get conversation history for a session
        
        Args:
            session_id: Session identifier
            
        Returns:
            List of conversation exchanges
        """
        context = self.contexts.get(session_id)
        if context:
            return context.conversation_history
        return []
    
    def clear_conversation_history(self, session_id: str = "default"):
        """
        Clear conversation history for a session
        
        Args:
            session_id: Session identifier
        """
        if session_id in self.contexts:
            self.contexts[session_id].conversation_history.clear()
            self.logger.info(f"Cleared conversation history for session: {session_id}")
    
    def get_session_stats(self) -> Dict[str, Any]:
        """
        Get statistics about active sessions
        
        Returns:
            Dictionary with session statistics
        """
        stats = {
            "active_sessions": len(self.contexts),
            "total_exchanges": sum(len(ctx.conversation_history) for ctx in self.contexts.values()),
            "sessions": {}
        }
        
        for session_id, context in self.contexts.items():
            stats["sessions"][session_id] = {
                "exchanges": len(context.conversation_history),
                "last_ticker": context.last_ticker,
                "last_timeframes": context.last_timeframes
            }
        
        return stats


# CLI Interface for testing and demonstration
def main():
    """CLI interface for testing the enhanced query engine"""
    print("MarketFlow Enhanced LLM Query Engine")
    print("=====================================")
    print("Type 'quit' to exit, 'help' for commands, 'clear' to clear history")
    print()
    
    try:
        engine = MarketflowLLMQueryEngine(enable_rag=True)
        session_id = "cli_session"
        
        while True:
            try:
                user_input = input("\nUser: ").strip()
                
                if user_input.lower() in {'quit', 'exit', 'q'}:
                    print("Goodbye!")
                    break
                
                elif user_input.lower() == 'clear':
                    engine.clear_conversation_history(session_id)
                    print("Conversation history cleared.")
                    continue
                
                elif user_input.lower() == 'help':
                    print("""
Available commands:
• quit/exit/q - Exit the program
• clear - Clear conversation history
• help - Show this help message

Example queries:
• "Analyze AAPL"
• "What is a Wyckoff Spring?"
• "Compare AAPL and MSFT"
• "What does Anna Coulling say about volume?"
• "Show AAPL across all timeframes"
                    """)
                    continue
                
                elif user_input.lower() == 'stats':
                    stats = engine.get_session_stats()
                    print(f"Session Statistics: {json.dumps(stats, indent=2)}")
                    continue
                
                if not user_input:
                    continue
                
                # Process the query
                print("\nAI: ", end="", flush=True)
                response = engine.process(user_input, session_id)
                print(response)
                
            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                break
            except Exception as e:
                print(f"\nError: {str(e)}")
                print("Please try again or type 'quit' to exit.")
    
    except Exception as e:
        print(f"Failed to initialize query engine: {str(e)}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())

