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
import yaml
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
            
            # Load concepts from YAML files for enhanced explanations
            self._load_concepts()
            
            self.logger.info("MarketFlow LLM Query Engine initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize query engine: {str(e)}", exc_info=True)
            raise
    
    def _initialize_intent_patterns(self):
        """Initialize regex patterns for intent recognition"""
        self.intent_patterns = {
            QueryIntent.TICKER_ANALYSIS: [
                (r'\b(analyze|analysis|check|examine|look at|review)\s+([a-z]{1,5})\b', 0.9),
                (r'\b([a-z]{1,5})\s+(analysis|signal|vpa|wyckoff)', 0.8),
                (r'\bwhat.*signal.*([a-z]{1,5})', 0.7),
                (r'\bhow.*([a-z]{1,5}).*performing', 0.6),
                (r'\b(analyze|analysis|check|examine)\b.*\b[a-z]{1,5}\b', 0.7),  # More flexible
            ],
            QueryIntent.CONCEPT_EXPLANATION: [
                (r'\b(what is|explain|define|describe)\s+(.+)', 0.9),
                (r'\btell me about\s+(.+)', 0.8),
                (r'\b(spring|accumulation|distribution|climax|wyckoff|vpa)\b', 0.7),
                (r'\bwhat.*\b(spring|accumulation|distribution|climax|wyckoff|vpa)\b', 0.8),
            ],
            QueryIntent.COMPARISON: [
                (r'\b(compare|vs|versus|against)\b', 0.9),
                (r'\b([a-z]{1,5})\s+(and|vs|versus)\s+([a-z]{1,5})', 0.8),
                (r'\bdifference between\s+([a-z]{1,5})\s+and\s+([a-z]{1,5})', 0.7),
            ],
            QueryIntent.RAG_QUERY: [
                (r'\b(according to|what does|says about|mentions)\b', 0.8),
                (r'\b(anna coulling|wyckoff|book|source|reference)\b', 0.7),
                (r'\bin the (context|literature|material)', 0.6),
            ],
            QueryIntent.MULTI_TIMEFRAME: [
                (r'\b(all timeframes|multiple timeframes|across.*timeframes)', 0.9),
                (r'\b(daily|weekly|hourly|1h|4h|1d|1w)\b.*\b(daily|weekly|hourly|1h|4h|1d|1w)\b', 0.8),
            ],
            QueryIntent.HISTORICAL_ANALYSIS: [
                (r'\b(last|past|previous)\s+(week|month|quarter|year)', 0.9),
                (r'\b(historical|history|trend|performance)\b', 0.8),
                (r'\b(since|from|over the)\s+(last|past)', 0.7),
                (r'\b(ytd|year to date|monthly|quarterly)\b', 0.7),
            ],
            QueryIntent.MARKET_CONDITION: [
                (r'\b(market|markets)\s+(condition|sentiment|state|status)', 0.9),
                (r'\b(current|overall|general)\s+(market|sentiment)', 0.8),
                (r'\b(bull|bear)\s+(market|trend)', 0.8),
                (r'\b(market|economic)\s+(outlook|environment)', 0.7),
            ],
            QueryIntent.PATTERN_RECOGNITION: [
                (r'\b(pattern|patterns)\b', 0.8),
                (r'\b(show|find|identify).*\b(pattern|formation)', 0.8),
                (r'\b(head and shoulders|double top|double bottom|triangle)', 0.9),
                (r'\b(accumulation|distribution)\s+(pattern|zone)', 0.8),
            ],
            QueryIntent.TIMEFRAME_SPECIFIC: [
                (r'\b(daily|weekly|hourly|1h|4h|1d|1w|5m|15m|30m)\s+(analysis|chart|view)', 0.9),
                (r'\bon\s+(daily|weekly|hourly|1h|4h|1d|1w|5m|15m|30m)', 0.8),
                (r'\b(short term|long term|intraday)', 0.7),
            ],
            QueryIntent.PORTFOLIO_ANALYSIS: [
                (r'\b(portfolio|watchlist|holdings)', 0.9),
                (r'\b(my|our)\s+(stocks|positions|investments)', 0.8),
                (r'\b(diversification|allocation|risk)', 0.7),
            ]
        }
    
    def _initialize_ticker_patterns(self):
        """Initialize patterns for ticker validation"""
        # Context-aware ticker patterns
        self.ticker_pattern = re.compile(r'\b[A-Z]{1,5}\b')
        
        # Specific ticker context patterns (higher confidence)
        self.ticker_context_patterns = [
            r'\b(analyze|analysis|check|examine|look at|review)\s+([A-Z]{1,5})\b',
            r'\b([A-Z]{1,5})\s+(stock|ticker|symbol|analysis|signal|price)',
            r'\b([A-Z]{1,5})\s+(vs|versus|and)\s+([A-Z]{1,5})\b',  # AAPL vs MSFT
            r'\b([A-Z]{1,5})\s+vs\s+([A-Z]{1,5})\b',  # AAPL vs MSFT
            r'\bcompare\s+([A-Z]{1,5})\s+(and|with|to|vs|versus)\s+([A-Z]{1,5})\b',  # compare AAPL and MSFT
            r'\$([A-Z]{1,5})\b',  # $AAPL format
            r'\b([A-Z]{1,5}):\w+',  # AAPL:NASDAQ format
        ]
        
        # Comprehensive blacklist of common false positives
        self.ticker_blacklist = {
            # Common English words
            'THE', 'AND', 'FOR', 'ARE', 'BUT', 'NOT', 'YOU', 'ALL', 'CAN',
            'HAD', 'HER', 'WAS', 'ONE', 'OUR', 'OUT', 'DAY', 'GET', 'HAS',
            'HIM', 'HOW', 'ITS', 'MAY', 'NEW', 'NOW', 'OLD', 'SEE', 'TWO',
            'WHO', 'BOY', 'DID', 'LET', 'PUT', 'SAY', 'SHE', 'TOO', 'USE',
            'WHAT', 'WHEN', 'WHERE', 'WHICH', 'WHILE', 'WITH', 'WOULD',
            'COULD', 'SHOULD', 'WILL', 'WELL', 'VERY', 'MUCH', 'SUCH',
            'EACH', 'SOME', 'MANY', 'MOST', 'MORE', 'LESS', 'THAN', 'THEN',
            'THEM', 'THEY', 'THEIR', 'THERE', 'HERE', 'NEAR', 'FAR', 'AWAY',
            'BACK', 'COME', 'CAME', 'TAKE', 'MAKE', 'GIVE', 'TELL', 'KNOW',
            'THINK', 'FEEL', 'LOOK', 'SEEM', 'TURN', 'KEEP', 'FIND', 'CALL',
            'WORK', 'PART', 'PLACE', 'RIGHT', 'GREAT', 'SMALL', 'LARGE',
            'GOOD', 'BEST', 'BETTER', 'FIRST', 'LAST', 'NEXT', 'LONG', 'LITTLE',
            'OWN', 'OTHER', 'ANOTHER', 'SAME', 'DIFFERENT', 'EVERY', 'EACH',
            'BOTH', 'FEW', 'SEVERAL', 'ABOUT', 'ABOVE', 'AFTER', 'AGAIN',
            'AGAINST', 'ALONG', 'AMONG', 'AROUND', 'BEFORE', 'BEHIND',
            'BELOW', 'BESIDE', 'BETWEEN', 'BEYOND', 'DURING', 'EXCEPT',
            'INSIDE', 'INSTEAD', 'OUTSIDE', 'THROUGH', 'THROUGHOUT', 'UNDER',
            'UNTIL', 'WITHOUT', 'WITHIN',
            
            # Technical/Finance terms that aren't tickers
            'VPA', 'LLM', 'API', 'SQL', 'HTML', 'CSS', 'JSON', 'XML', 'HTTP',
            'HTTPS', 'FTP', 'SSH', 'TCP', 'UDP', 'DNS', 'URL', 'URI', 'UUID',
            'AI', 'ML', 'NLP', 'GPU', 'CPU', 'RAM', 'SSD', 'HDD', 'USB',
            'PDF', 'DOC', 'XLS', 'PPT', 'ZIP', 'RAR', 'TAR', 'GZ',
            
            # Currency codes (these are valid but not stock tickers)
            'USD', 'EUR', 'GBP', 'JPY', 'CAD', 'AUD', 'CHF', 'CNY', 'INR',
            'KRW', 'BRL', 'MXN', 'RUB', 'ZAR', 'SEK', 'NOK', 'DKK', 'PLN',
            
            # Common abbreviations
            'CEO', 'CFO', 'CTO', 'COO', 'VP', 'SVP', 'EVP', 'MD', 'GM',
            'HR', 'IT', 'PR', 'QA', 'RD', 'BD', 'PM', 'AM', 'FM',
            'USA', 'UK', 'EU', 'US', 'CA', 'AU', 'DE', 'FR', 'IT', 'ES',
            'BR', 'IN', 'CN', 'JP', 'KR', 'MX', 'RU', 'ZA',
            
            # Time/Date related
            'AM', 'PM', 'EST', 'PST', 'GMT', 'UTC', 'CST', 'MST',
            'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN',
            'JAN', 'FEB', 'MAR', 'APR', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC',
            
            # Question words and common query terms
            'WHY', 'WHEN', 'WHERE', 'WHAT', 'HOW', 'WHICH', 'WHOSE',
            'EXPLAIN', 'TELL', 'SHOW', 'GIVE', 'HELP', 'PLEASE',
            'THANKS', 'THANK', 'HELLO', 'HI', 'BYE', 'GOODBYE',
            
            # Common prepositions and conjunctions (uppercase)
            'OF', 'TO', 'IN', 'ON', 'AT', 'BY', 'FROM', 'UP', 'DOWN',
            'OVER', 'UNDER', 'INTO', 'ONTO', 'UPON', 'ACROSS', 'THROUGH',
            'DURING', 'BEFORE', 'AFTER', 'ABOVE', 'BELOW', 'BETWEEN',
            'AMONG', 'AROUND', 'NEAR', 'BESIDE', 'BEHIND', 'BEYOND',
            'WITHIN', 'WITHOUT', 'EXCEPT', 'BESIDES', 'DESPITE', 'DURING',
            'SINCE', 'UNTIL', 'UNLESS', 'ALTHOUGH', 'BECAUSE', 'HOWEVER',
            'THEREFORE', 'MOREOVER', 'FURTHERMORE', 'NEVERTHELESS',
            
            # Market/Finance terms that aren't tickers
            'BULL', 'BEAR', 'LONG', 'SHORT', 'CALL', 'PUT', 'BID', 'ASK',
            'HIGH', 'LOW', 'OPEN', 'CLOSE', 'VOLUME', 'PRICE', 'TREND',
            'SIGNAL', 'BUY', 'SELL', 'HOLD', 'STOP', 'LIMIT', 'MARKET',
            'ORDER', 'TRADE', 'STOCK', 'SHARE', 'BOND', 'FUND', 'ETF',
            
            # Analysis and chart terms
            'CHART', 'GRAPH', 'DATA', 'INFO', 'ANALYSIS', 'ANALYZE',
            'DAILY', 'WEEKLY', 'HOURLY', 'MONTHLY', 'YEARLY', 'TIMEFRAME',
            'PATTERN', 'PATTERNS', 'FORMATION', 'FORMATIONS',
            
            # Personal and possessive terms
            'MY', 'YOUR', 'HIS', 'HER', 'OUR', 'THEIR', 'MINE', 'YOURS',
            'PORTFOLIO', 'WATCHLIST', 'HOLDINGS', 'POSITIONS',
            
            # Action and query terms
            'SHOW', 'FIND', 'SEARCH', 'LOOK', 'CHECK', 'EXAMINE', 'REVIEW',
            'COMPARE', 'VERSUS', 'AGAINST', 'BETWEEN', 'DIFFERENCE',
            'INDEX', 'SECTOR', 'INDUSTRY', 'GROWTH', 'VALUE', 'INCOME',
            'RISK', 'RETURN', 'YIELD', 'RATE', 'RATIO', 'MARGIN',
            'PROFIT', 'LOSS', 'GAIN', 'COST', 'FEE', 'TAX', 'DEBT',
            'CASH', 'ASSET', 'LIABILITY', 'EQUITY', 'CAPITAL', 'REVENUE',
            'SALES', 'INCOME', 'EXPENSE', 'BUDGET', 'FORECAST', 'TARGET',
            'GOAL', 'PLAN', 'STRATEGY', 'ANALYSIS', 'REPORT', 'DATA',
            'INFO', 'NEWS', 'UPDATE', 'ALERT', 'WARNING', 'ERROR',
            
            # Wyckoff/VPA specific terms
            'WYCKOFF', 'SPRING', 'UTAD', 'CLIMAX', 'PHASE', 'EVENT',
            'ACCUMULATION', 'DISTRIBUTION', 'MARKUP', 'MARKDOWN',
            'SUPPORT', 'RESISTANCE', 'BREAKOUT', 'BREAKDOWN', 'TEST',
            'EFFORT', 'RESULT', 'SUPPLY', 'DEMAND', 'ABSORPTION',
            'SELLING', 'BUYING', 'AUTOMATIC', 'RALLY', 'REACTION',
            'SECONDARY', 'LAST', 'POINT', 'SIGN', 'STRENGTH', 'WEAKNESS',
            'JUMP', 'ACROSS', 'CREEK', 'ICE', 'CAUSE', 'EFFECT', 'SMART',
            'MONEY', 'COMPOSITE', 'OPERATOR', 'PROFESSIONAL', 'PUBLIC',
            'HERD', 'CROWD', 'SENTIMENT', 'PSYCHOLOGY', 'EMOTION',
            'FEAR', 'GREED', 'PANIC', 'EUPHORIA', 'OPTIMISM', 'PESSIMISM',
            
            # Additional common words that are often false positives
            'VS', 'VERSUS', 'CHECK', 'NO', 'YES', 'MAYBE', 'PERHAPS',
            'REALLY', 'QUITE', 'VERY', 'MUCH', 'MANY', 'SOME', 'ANY',
            'EACH', 'EVERY', 'BOTH', 'EITHER', 'NEITHER', 'NONE',
            'ONLY', 'JUST', 'EVEN', 'STILL', 'YET', 'ALREADY', 'SOON',
            'OFTEN', 'ALWAYS', 'NEVER', 'SOMETIMES', 'USUALLY', 'RARELY',
            'ALMOST', 'NEARLY', 'QUITE', 'RATHER', 'PRETTY', 'FAIRLY'
        }
    
    def _load_concepts(self):
        """Load VPA and Wyckoff concepts from YAML files"""
        try:
            # Load VPA concepts
            vpa_path = 'marketflow/concepts/vpa_concepts.yaml'
            with open(vpa_path, 'r') as file:
                self.vpa_concepts = yaml.safe_load(file)
            self.logger.info(f"Loaded VPA concepts: {len(self.vpa_concepts)}")
            
            # Load Wyckoff concepts  
            wyckoff_path = 'marketflow/concepts/wyckoff_concepts.yaml'
            with open(wyckoff_path, 'r') as file:
                self.wyckoff_concepts = yaml.safe_load(file)
            self.logger.info(f"Loaded Wyckoff concepts: {len(self.wyckoff_concepts)}")
            
            # Combine all concepts for easy lookup
            self.all_concepts = {**self.vpa_concepts, **self.wyckoff_concepts}
            
        except Exception as e:
            self.logger.warning(f"Failed to load concept files: {str(e)}")
            # Fallback to empty concepts
            self.vpa_concepts = {}
            self.wyckoff_concepts = {}
            self.all_concepts = {}
    
    def get_concept_explanation(self, concept_key: str) -> Optional[str]:
        """
        Get explanation for a specific concept
        
        Args:
            concept_key: Key for the concept to explain
            
        Returns:
            Concept explanation or None if not found
        """
        # Try exact match first
        if concept_key in self.all_concepts:
            return self.all_concepts[concept_key]
        
        # Try case-insensitive match
        concept_key_lower = concept_key.lower()
        for key, value in self.all_concepts.items():
            if key.lower() == concept_key_lower:
                return value
        
        # Try partial match
        for key, value in self.all_concepts.items():
            if concept_key_lower in key.lower() or key.lower() in concept_key_lower:
                return value
        
        return None
    
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
        Extract valid ticker symbols from text using context-aware patterns
        
        Args:
            text: Input text to search for tickers
            
        Returns:
            List of valid ticker symbols
        """
        valid_tickers = []
        text_upper = text.upper()
        
        # First, try context-aware patterns (higher confidence)
        for pattern in self.ticker_context_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                # Extract ticker symbols from the match groups
                for group in match.groups():
                    if group and re.match(r'^[A-Z]{1,5}$', group.upper()):
                        ticker = group.upper()
                        if (ticker not in self.ticker_blacklist and 
                            ticker not in valid_tickers and
                            len(ticker) >= 1):  # At least 1 character
                            valid_tickers.append(ticker)
        
        # If context patterns found tickers, return them (high confidence)
        if valid_tickers:
            return valid_tickers
        
        # Otherwise, try general pattern with very strict filtering
        potential_tickers = self.ticker_pattern.findall(text_upper)
        
        for ticker in potential_tickers:
            if (ticker not in self.ticker_blacklist and 
                ticker not in valid_tickers and
                len(ticker) >= 2 and  # At least 2 characters for general extraction
                len(ticker) <= 5 and  # Max 5 characters
                self._is_likely_ticker(ticker, text)):
                valid_tickers.append(ticker)
        
        return valid_tickers
    
    def _is_likely_ticker(self, ticker: str, original_text: str) -> bool:
        """
        Additional heuristics to determine if a word is likely a ticker symbol
        
        Args:
            ticker: Potential ticker symbol
            original_text: Original input text for context
            
        Returns:
            Boolean indicating if it's likely a ticker
        """
        # Strong financial context indicators
        strong_financial_words = [
            'analyze', 'analysis', 'stock', 'ticker', 'symbol', 'price', 
            'signal', 'buy', 'sell', 'trade', 'market', 'shares', 
            'investment', 'portfolio', 'earnings', 'dividend', 'chart',
            'vpa', 'wyckoff', 'compare', 'versus', 'vs'
        ]
        
        text_lower = original_text.lower()
        has_strong_financial_context = any(word in text_lower for word in strong_financial_words)
        
        # If no strong financial context, reject
        if not has_strong_financial_context:
            return False
        
        # Check if ticker appears in a financial context pattern
        ticker_in_context_patterns = [
            rf'\b(analyze|analysis|check|examine|look at|review)\s+{re.escape(ticker)}\b',
            rf'\b{re.escape(ticker)}\s+(stock|ticker|symbol|analysis|signal|price|vs|versus|and)\b',
            rf'\${re.escape(ticker)}\b',  # $AAPL format
            rf'\b{re.escape(ticker)}:\w+',  # AAPL:NASDAQ format
        ]
        
        for pattern in ticker_in_context_patterns:
            if re.search(pattern, original_text, re.IGNORECASE):
                return True
        
        # Additional check: if it's a reasonable ticker length and has financial context
        # but also check it's not a common verb or adjective
        common_verbs_adjectives = {
            'CHECK', 'LOOK', 'MAKE', 'TAKE', 'GIVE', 'TELL', 'KNOW', 'THINK',
            'FEEL', 'SEEM', 'TURN', 'KEEP', 'FIND', 'CALL', 'WORK', 'HELP',
            'SHOW', 'MOVE', 'PLAY', 'RUN', 'WALK', 'TALK', 'READ', 'WRITE',
            'LIKE', 'LOVE', 'WANT', 'NEED', 'HOPE', 'WISH', 'PLAN', 'TRY',
            'START', 'STOP', 'END', 'BEGIN', 'FINISH', 'CLOSE', 'OPEN',
            'GOOD', 'BAD', 'BIG', 'SMALL', 'LONG', 'SHORT', 'HIGH', 'LOW',
            'FAST', 'SLOW', 'HOT', 'COLD', 'OLD', 'NEW', 'YOUNG', 'NICE',
            'HARD', 'EASY', 'FULL', 'EMPTY', 'CLEAN', 'DIRTY', 'SAFE',
            'QUICK', 'SLOW', 'SMART', 'DUMB', 'RICH', 'POOR', 'HAPPY', 'SAD'
        }
        
        if ticker in common_verbs_adjectives:
            return False
        
        # Final check: reasonable length and strong context
        return (2 <= len(ticker) <= 5 and 
                has_strong_financial_context and
                ticker not in self.ticker_blacklist)
    
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
                            # Try to get the last group that contains the concept
                            concept = None
                            for group in reversed(match.groups()):
                                if group and group.strip():
                                    concept = group.strip()
                                    break
                            if concept:
                                matched_params['concept'] = concept
                        else:
                            # If no groups, try to extract concept from the original input
                            concept_words = ['spring', 'accumulation', 'distribution', 'climax', 'wyckoff', 'vpa']
                            for word in concept_words:
                                if word in user_input_lower:
                                    matched_params['concept'] = word
                                    break
                    
                    elif intent == QueryIntent.COMPARISON:
                        tickers = self.extract_tickers(user_input)
                        if len(tickers) >= 2:
                            matched_params['tickers'] = tickers[:2]  # Take first two
                    
                    elif intent == QueryIntent.PATTERN_RECOGNITION:
                        tickers = self.extract_tickers(user_input)
                        if tickers:
                            matched_params['tickers'] = tickers
                    
                    elif intent == QueryIntent.TIMEFRAME_SPECIFIC:
                        tickers = self.extract_tickers(user_input)
                        if tickers:
                            matched_params['tickers'] = tickers
                        
                        # Extract timeframe
                        timeframe_patterns = {
                            r'\b(daily|1d)\b': 'daily',
                            r'\b(weekly|1w)\b': 'weekly', 
                            r'\b(hourly|1h)\b': 'hourly',
                            r'\b(4h|4hour)\b': '4h',
                            r'\b(5m|5min)\b': '5m',
                            r'\b(15m|15min)\b': '15m',
                            r'\b(30m|30min)\b': '30m'
                        }
                        
                        for pattern, timeframe in timeframe_patterns.items():
                            if re.search(pattern, user_input_lower):
                                matched_params['timeframe'] = timeframe
                                break
                    
                    elif intent == QueryIntent.PORTFOLIO_ANALYSIS:
                        tickers = self.extract_tickers(user_input)
                        if tickers:
                            matched_params['tickers'] = tickers
                    
                    elif intent == QueryIntent.HISTORICAL_ANALYSIS:
                        tickers = self.extract_tickers(user_input)
                        if tickers:
                            matched_params['tickers'] = tickers
                        
                        # Extract time period
                        period_patterns = {
                            r'\blast\s+(week|month|quarter|year)': 'period',
                            r'\bpast\s+(week|month|quarter|year)': 'period',
                            r'\bytd\b': 'ytd',
                            r'\byear\s+to\s+date\b': 'ytd'
                        }
                        
                        for pattern, period_type in period_patterns.items():
                            match_period = re.search(pattern, user_input_lower)
                            if match_period:
                                matched_params['period'] = match_period.group(1) if period_type == 'period' else period_type
                                break
                    
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
            
            elif intent_result.intent == QueryIntent.MARKET_CONDITION:
                return self.handle_market_condition_query(intent_result.parameters, context)
            
            elif intent_result.intent == QueryIntent.PATTERN_RECOGNITION:
                return self.handle_pattern_recognition_query(intent_result.parameters, context)
            
            elif intent_result.intent == QueryIntent.TIMEFRAME_SPECIFIC:
                return self.handle_timeframe_specific_query(intent_result.parameters, context)
            
            elif intent_result.intent == QueryIntent.PORTFOLIO_ANALYSIS:
                return self.handle_portfolio_analysis_query(intent_result.parameters, context)
            
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
            
            # First, try to get explanation from loaded YAML concepts
            yaml_explanation = self.get_concept_explanation(concept)
            if yaml_explanation:
                self.logger.info(f"Found concept explanation in YAML: {concept}")
                return f"**{concept.title()}**\n\n{yaml_explanation}"
            
            # If not in YAML, try to get explanation from interface
            explanation = self.interface.explain_concept(concept)
            
            # If not found, try RAG search as fallback
            if "not found" in explanation.lower() and self.enable_rag:
                self.logger.info(f"Concept not found in interface, trying RAG search for: {concept}")
                rag_results = self._perform_rag_search(f"explain {concept}", top_k=3)
                
                if rag_results:
                    explanation = f"**{concept.title()}** (from knowledge base)\n\n{rag_results}"
                else:
                    # Provide helpful suggestions based on available concepts
                    available_concepts = list(self.all_concepts.keys())[:10]  # Show first 10
                    suggestion = f"I don't have specific information about '{concept}'. "
                    if available_concepts:
                        suggestion += f"\n\nAvailable concepts include: {', '.join(available_concepts)}"
                    suggestion += "\n\nCould you try asking about one of these or a related VPA/Wyckoff concept?"
                    explanation = suggestion
            
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
    
    def handle_market_condition_query(self, params: Dict[str, Any], 
                                    context: QueryContext) -> str:
        """
        Handle market condition and sentiment queries
        
        Args:
            params: Parsed parameters
            context: Conversation context
            
        Returns:
            Market condition analysis response
        """
        try:
            self.logger.info("Processing market condition query")
            
            # Try to get general market analysis from interface
            response = ("Market condition analysis is currently limited. "
                       "I can provide individual ticker analysis instead. "
                       "Try asking about specific tickers like 'Analyze SPY' for market overview.")
            
            # If RAG is enabled, try to get market insights from knowledge base
            if self.enable_rag:
                try:
                    rag_results = self._perform_rag_search("market conditions sentiment analysis", top_k=3)
                    if rag_results:
                        response = f"**Market Insights from Knowledge Base:**\n\n{rag_results}"
                except Exception as e:
                    self.logger.error(f"Error in market condition RAG search: {str(e)}")
            
            return response
            
        except Exception as e:
            self.logger.error(f"Error in market condition query: {str(e)}", exc_info=True)
            return f"I encountered an error analyzing market conditions: {str(e)}"
    
    def handle_pattern_recognition_query(self, params: Dict[str, Any], 
                                       context: QueryContext) -> str:
        """
        Handle pattern recognition queries
        
        Args:
            params: Parsed parameters
            context: Conversation context
            
        Returns:
            Pattern recognition response
        """
        try:
            self.logger.info("Processing pattern recognition query")
            
            # Extract tickers if any
            tickers = params.get('tickers', [])
            if not tickers and context.last_ticker:
                tickers = [context.last_ticker]
            
            if tickers:
                ticker = tickers[0]
                self.logger.info(f"Looking for patterns in {ticker}")
                
                # Get analysis from interface which includes pattern recognition
                analysis = self.interface.analyze_ticker(ticker)
                
                # Focus on pattern-related information
                pattern_info = f"**Pattern Analysis for {ticker.upper()}:**\n\n{analysis}"
                
                # Update context
                context.last_ticker = ticker
                
                return pattern_info
            else:
                # General pattern explanation
                if self.enable_rag:
                    try:
                        rag_results = self._perform_rag_search("chart patterns technical analysis", top_k=3)
                        if rag_results:
                            return f"**Chart Patterns Information:**\n\n{rag_results}"
                    except Exception as e:
                        self.logger.error(f"Error in pattern RAG search: {str(e)}")
                
                return ("For pattern recognition, please specify a ticker symbol. "
                       "For example: 'Show patterns in AAPL' or 'MSFT pattern analysis'.")
            
        except Exception as e:
            self.logger.error(f"Error in pattern recognition: {str(e)}", exc_info=True)
            return f"I encountered an error analyzing patterns: {str(e)}"
    
    def handle_timeframe_specific_query(self, params: Dict[str, Any], 
                                      context: QueryContext) -> str:
        """
        Handle timeframe-specific analysis queries
        
        Args:
            params: Parsed parameters
            context: Conversation context
            
        Returns:
            Timeframe-specific analysis response
        """
        try:
            self.logger.info("Processing timeframe-specific query")
            
            # Extract tickers and timeframe
            tickers = params.get('tickers', [])
            timeframe = params.get('timeframe', 'daily')
            
            if not tickers and context.last_ticker:
                tickers = [context.last_ticker]
            
            if tickers:
                ticker = tickers[0]
                self.logger.info(f"Analyzing {ticker} on {timeframe} timeframe")
                
                # Get analysis from interface
                analysis = self.interface.analyze_ticker(ticker)
                
                response = f"**{ticker.upper()} Analysis ({timeframe.title()} Timeframe):**\n\n{analysis}"
                
                # Update context
                context.last_ticker = ticker
                context.last_timeframes = [timeframe]
                
                return response
            else:
                return ("Please specify a ticker for timeframe-specific analysis. "
                       "For example: 'AAPL daily analysis' or 'MSFT on weekly chart'.")
            
        except Exception as e:
            self.logger.error(f"Error in timeframe-specific query: {str(e)}", exc_info=True)
            return f"I encountered an error with timeframe analysis: {str(e)}"
    
    def handle_portfolio_analysis_query(self, params: Dict[str, Any], 
                                      context: QueryContext) -> str:
        """
        Handle portfolio and watchlist analysis queries
        
        Args:
            params: Parsed parameters
            context: Conversation context
            
        Returns:
            Portfolio analysis response
        """
        try:
            self.logger.info("Processing portfolio analysis query")
            
            # Extract tickers from parameters or context
            tickers = params.get('tickers', [])
            
            if not tickers:
                # Try to get from conversation history
                recent_tickers = []
                for exchange in context.conversation_history[-10:]:  # Last 10 exchanges
                    if 'tickers' in exchange.get('metadata', {}):
                        recent_tickers.extend(exchange['metadata']['tickers'])
                
                if recent_tickers:
                    tickers = list(set(recent_tickers))  # Remove duplicates
            
            if tickers:
                self.logger.info(f"Analyzing portfolio tickers: {tickers}")
                
                analyses = []
                for ticker in tickers[:5]:  # Limit to 5 tickers
                    try:
                        analysis = self.interface.analyze_ticker(ticker)
                        analyses.append(f"**{ticker.upper()}:**\n{analysis[:300]}...")
                    except Exception as e:
                        analyses.append(f"**{ticker.upper()}:** Error - {str(e)}")
                
                response = "**Portfolio Analysis:**\n\n" + "\n\n".join(analyses)
                
                # Update context
                context.last_tickers = tickers
                
                return response
            else:
                return ("For portfolio analysis, please specify ticker symbols. "
                       "For example: 'Analyze my portfolio: AAPL, MSFT, GOOGL' or "
                       "'Portfolio analysis AAPL MSFT NVDA'.")
            
        except Exception as e:
            self.logger.error(f"Error in portfolio analysis: {str(e)}", exc_info=True)
            return f"I encountered an error analyzing the portfolio: {str(e)}"
    
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
        Enhanced RAG search with multiple fallback mechanisms
        
        Args:
            query: Search query
            top_k: Number of results to retrieve
            
        Returns:
            Formatted search results or None
        """
        try:
            # Primary RAG search using ChromaDB
            results = chroma_retrieve_top_chunks(query, top_k=top_k)
            
            if results:
                return self._format_rag_results(results)
            
        except Exception as e:
            self.logger.warning(f"Primary RAG search failed: {str(e)}")
        
        # Fallback 1: Try local concept search
        try:
            concept_result = self._search_local_concepts(query)
            if concept_result:
                return f"**From Local Knowledge Base:**\n\n{concept_result}"
        except Exception as e:
            self.logger.warning(f"Local concept search failed: {str(e)}")
        
        # Fallback 2: Try keyword-based search in loaded concepts
        try:
            keyword_result = self._keyword_search_concepts(query)
            if keyword_result:
                return f"**Related Concepts:**\n\n{keyword_result}"
        except Exception as e:
            self.logger.warning(f"Keyword search failed: {str(e)}")
        
        # Fallback 3: Return helpful guidance
        return self._generate_rag_fallback_response(query)
    
    def _format_rag_results(self, results: List) -> str:
        """
        Format RAG search results for better readability
        
        Args:
            results: List of search results
            
        Returns:
            Formatted results string
        """
        if not results:
            return None
        
        formatted_results = []
        for i, result in enumerate(results, 1):
            try:
                # Handle different result formats
                if isinstance(result, dict):
                    content = result.get('content', result.get('text', str(result)))
                    source = result.get('source', result.get('metadata', {}).get('source', 'Unknown'))
                    
                    # Clean and truncate content
                    content = content.strip()
                    if len(content) > 500:
                        content = content[:500] + "..."
                    
                    formatted_results.append(f"**Source {i}** ({source}):\n{content}")
                else:
                    content = str(result).strip()
                    if len(content) > 500:
                        content = content[:500] + "..."
                    formatted_results.append(f"**Result {i}**:\n{content}")
                    
            except Exception as e:
                self.logger.warning(f"Error formatting result {i}: {str(e)}")
                continue
        
        if not formatted_results:
            return None
        
        return "\n\n".join(formatted_results)
    
    def _search_local_concepts(self, query: str) -> Optional[str]:
        """
        Search through locally loaded VPA and Wyckoff concepts
        
        Args:
            query: Search query
            
        Returns:
            Matching concept explanation or None
        """
        query_lower = query.lower()
        
        # Search VPA concepts
        for concept_key, concept_data in self.vpa_concepts.items():
            if (concept_key.lower() in query_lower or 
                query_lower in concept_key.lower()):
                
                if isinstance(concept_data, dict):
                    explanation = concept_data.get('explanation', concept_data.get('description', ''))
                    return f"**VPA Concept - {concept_key}:**\n{explanation}"
                else:
                    return f"**VPA Concept - {concept_key}:**\n{concept_data}"
        
        # Search Wyckoff concepts
        for concept_key, concept_data in self.wyckoff_concepts.items():
            if (concept_key.lower() in query_lower or 
                query_lower in concept_key.lower()):
                
                if isinstance(concept_data, dict):
                    explanation = concept_data.get('explanation', concept_data.get('description', ''))
                    return f"**Wyckoff Concept - {concept_key}:**\n{explanation}"
                else:
                    return f"**Wyckoff Concept - {concept_key}:**\n{concept_data}"
        
        return None
    
    def _keyword_search_concepts(self, query: str) -> Optional[str]:
        """
        Perform keyword-based search across all concepts
        
        Args:
            query: Search query
            
        Returns:
            Related concepts or None
        """
        query_words = query.lower().split()
        matches = []
        
        # Search through all concepts for keyword matches
        all_concepts = {**self.vpa_concepts, **self.wyckoff_concepts}
        
        for concept_key, concept_data in all_concepts.items():
            concept_text = f"{concept_key} {concept_data}".lower()
            
            # Count keyword matches
            match_count = sum(1 for word in query_words if word in concept_text)
            
            if match_count > 0:
                concept_type = "VPA" if concept_key in self.vpa_concepts else "Wyckoff"
                matches.append({
                    'key': concept_key,
                    'type': concept_type,
                    'score': match_count,
                    'data': concept_data
                })
        
        if not matches:
            return None
        
        # Sort by match score and return top matches
        matches.sort(key=lambda x: x['score'], reverse=True)
        top_matches = matches[:3]
        
        result_parts = []
        for match in top_matches:
            if isinstance(match['data'], dict):
                explanation = match['data'].get('explanation', match['data'].get('description', ''))
            else:
                explanation = str(match['data'])
            
            if len(explanation) > 200:
                explanation = explanation[:200] + "..."
            
            result_parts.append(f"**{match['type']} - {match['key']}:**\n{explanation}")
        
        return "\n\n".join(result_parts)
    
    def _generate_rag_fallback_response(self, query: str) -> str:
        """
        Generate helpful fallback response when RAG search fails
        
        Args:
            query: Original search query
            
        Returns:
            Helpful fallback response
        """
        # Suggest available concepts
        available_vpa = list(self.vpa_concepts.keys())[:5]
        available_wyckoff = list(self.wyckoff_concepts.keys())[:5]
        
        response_parts = [
            f"I couldn't find specific information about '{query}' in the knowledge base.",
            "",
            "**Available VPA concepts:**",
            ", ".join(available_vpa),
            "",
            "**Available Wyckoff concepts:**", 
            ", ".join(available_wyckoff),
            "",
            "Try asking about one of these concepts, or ask for ticker analysis instead."
        ]
        
        return "\n".join(response_parts)
    
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

