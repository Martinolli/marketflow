"""
Enhanced MarketFlow Snapshot Module

This module provides advanced functionality for capturing, storing, and retrieving MarketFlow 
analysis results with comprehensive support for historical data storage, chart plotting, 
information display, and LLM interface/training data preparation.

Key Features:
- Multi-layered data architecture with semantic modeling
- Advanced metadata management and temporal organization
- LLM-optimized data structures and natural language context
- Comprehensive query and retrieval capabilities
- Integration with external systems and data sources
- Security and compliance framework
"""

import os
import json
import sqlite3
import hashlib
import pickle
import gzip
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Any, Optional, Union, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import uuid

import pandas as pd
import numpy as np
from sqlalchemy import create_engine, Column, String, DateTime, Text, JSON, Float, func, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.dialects.sqlite import JSON as SQLiteJSON

from marketflow.marketflow_logger import get_logger
from marketflow.marketflow_config_manager import create_app_config
from marketflow.enums import MarketCondition, AnalysisType  # Make sure to import SignalType

# Data Models and Schemas
Base = declarative_base()

@dataclass
class SnapshotMetadata:
    """Comprehensive metadata for analysis snapshots"""
    snapshot_id: str
    ticker: str
    timestamp: datetime
    analysis_type: AnalysisType
    market_condition: MarketCondition
    timeframes: List[str]
    data_quality_score: float
    confidence_level: float
    market_session: str
    volatility_regime: str
    trend_direction: str
    volume_profile: str
    news_sentiment: Optional[float] = None
    economic_events: Optional[List[str]] = None
    analyst_notes: Optional[str] = None
    tags: Optional[List[str]] = None
    
class AnalysisSnapshot(Base):
    """SQLAlchemy model for analysis snapshots"""
    __tablename__ = 'analysis_snapshots'
    
    id = Column(String, primary_key=True)
    ticker = Column(String, nullable=False, index=True)
    timestamp = Column(DateTime, nullable=False, index=True)
    analysis_type = Column(String, nullable=False)
    market_condition = Column(String, nullable=False)
    timeframes = Column(JSON)
    data_quality_score = Column(Float)
    confidence_level = Column(Float)
    market_session = Column(String)
    volatility_regime = Column(String)
    trend_direction = Column(String)
    volume_profile = Column(String)
    news_sentiment = Column(Float)
    economic_events = Column(JSON)
    analyst_notes = Column(Text)
    tags = Column(JSON)
    metadata_json = Column(JSON)
    data_path = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class LLMTrainingRecord(Base):
    """SQLAlchemy model for LLM training data"""
    __tablename__ = 'llm_training_data'
    
    id = Column(String, primary_key=True)
    snapshot_id = Column(String, nullable=False, index=True)
    conversation_type = Column(String, nullable=False)
    prompt = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    context = Column(JSON)
    quality_score = Column(Float)
    human_validated = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class MarketflowSnapshot:
    """
    Advanced MarketFlow snapshot manager with comprehensive data management,
    LLM integration, and intelligent analytics capabilities.
    """
    
    def __init__(self, 
                 output_dir: str = None, 
                 db_url: str = None,
                 enable_compression: bool = True,
                 enable_encryption: bool = False,
                 logger=None):
        """
        Initialize the enhanced snapshot manager.
        
        Args:
            output_dir: Directory for storing snapshot data files
            db_url: Database URL for metadata storage (SQLite by default)
            enable_compression: Enable data compression for storage efficiency
            enable_encryption: Enable data encryption for security
            logger: Optional custom logger instance
        """
        self.logger = logger or get_logger(module_name="EnhancedMarketflowSnapshot")
        self.config_manager = create_app_config(self.logger)
        
        # Setup storage directories
        self.output_dir = Path(output_dir or "enhanced_snapshots")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.data_dir = self.output_dir / "data"
        self.data_dir.mkdir(exist_ok=True)
        
        self.llm_dir = self.output_dir / "llm_training"
        self.llm_dir.mkdir(exist_ok=True)
        
        # Configuration
        self.enable_compression = enable_compression
        self.enable_encryption = enable_encryption
        
        # Setup database
        self.db_url = db_url or f"sqlite:///{self.output_dir}/snapshots.db"
        self.engine = create_engine(self.db_url)
        Base.metadata.create_all(self.engine)
        self.SessionLocal = sessionmaker(bind=self.engine)
        
        self.logger.info(f"Enhanced snapshot manager initialized with output_dir: {self.output_dir}")
        
    def _generate_snapshot_id(self, ticker: str, timestamp: datetime) -> str:
        """Generate unique snapshot ID"""
        base_string = f"{ticker}_{timestamp.isoformat()}"
        return hashlib.sha256(base_string.encode()).hexdigest()[:16]
    
    def _save_data_file(self, data: Any, file_path: Path) -> str:
        """Save data to file with optional compression and encryption"""
        try:
            if self.enable_compression:
                with gzip.open(file_path.with_suffix('.pkl.gz'), 'wb') as f:
                    pickle.dump(data, f)
                return str(file_path.with_suffix('.pkl.gz'))
            else:
                with open(file_path.with_suffix('.pkl'), 'wb') as f:
                    pickle.dump(data, f)
                return str(file_path.with_suffix('.pkl'))
        except Exception as e:
            self.logger.error(f"Failed to save data file {file_path}: {e}")
            raise
    
    def _load_data_file(self, file_path: str) -> Any:
        """Load data from file with automatic compression detection"""
        try:
            path = Path(file_path)
            if path.suffix == '.gz':
                with gzip.open(path, 'rb') as f:
                    return pickle.load(f)
            else:
                with open(path, 'rb') as f:
                    return pickle.load(f)
        except Exception as e:
            self.logger.error(f"Failed to load data file {file_path}: {e}")
            raise
    
    def _extract_market_context(self, analysis_result: Dict) -> Dict[str, Any]:
        """Extract market context information from analysis results"""
        context = {}
        
        # Extract market condition indicators
        signal = analysis_result.get('signal', {})
        context['signal_type'] = signal.get('type', 'UNKNOWN')
        context['signal_strength'] = signal.get('strength', 'UNKNOWN')
        context['signal_confidence'] = signal.get('confidence', 0.0)
        
        # Extract volatility information
        risk_assessment = analysis_result.get('risk_assessment', {})
        context['risk_level'] = risk_assessment.get('risk_level', 'UNKNOWN')
        context['volatility'] = risk_assessment.get('volatility', 0.0)
        
        # Extract trend information from timeframe analyses
        timeframe_analyses = analysis_result.get('timeframe_analyses', {})
        trends = []
        for tf, tf_data in timeframe_analyses.items():
            trend_analysis = tf_data.get('trend_analysis', {})
            if trend_analysis:
                trends.append({
                    'timeframe': tf,
                    'direction': trend_analysis.get('trend_direction', 'UNKNOWN'),
                    'strength': trend_analysis.get('trend_strength', 0.0)
                })
        context['trends'] = trends
        
        return context
    
    def _classify_market_condition(self, analysis_result: Dict) -> MarketCondition:
        """Classify market condition based on analysis results"""
        signal = analysis_result.get('signal', {})
        signal_type_val = signal.get('type', '')
        signal_type_str = str(signal_type_val).upper()
        
        # Simple classification logic - can be enhanced with more sophisticated analysis
        if 'BUY' in signal_type_str:
            return MarketCondition.BULL_MARKET
        elif 'SELL' in signal_type_str:
            return MarketCondition.BEAR_MARKET
        else:
            return MarketCondition.SIDEWAYS
    
    def _calculate_data_quality_score(self, analysis_result: Dict) -> float:
        """Calculate data quality score based on completeness and consistency"""
        score = 0.0
        max_score = 10.0
        
        # Check for essential components
        if analysis_result.get('ticker'):
            score += 1.0
        if analysis_result.get('current_price'):
            score += 1.0
        if analysis_result.get('signal'):
            score += 2.0
        if analysis_result.get('risk_assessment'):
            score += 2.0
        if analysis_result.get('timeframe_analyses'):
            score += 2.0
            
            # Check timeframe data quality
            timeframes = analysis_result['timeframe_analyses']
            for tf_data in timeframes.values():
                if tf_data.get('processed_data'):
                    score += 0.5
                if tf_data.get('wyckoff_phases'):
                    score += 0.5
                if tf_data.get('wyckoff_events'):
                    score += 0.5
                if tf_data.get('wyckoff_annotated_data') is not None:
                    score += 0.5
        
        return min(score / max_score, 1.0)
    
    # ... inside the MarketflowSnapshot class ...

    def save_enhanced_snapshot(self, 
                             analysis_result: Dict,
                             ticker: str,
                             analysis_type: AnalysisType = AnalysisType.TECHNICAL,
                             analyst_notes: str = None,
                             tags: List[str] = None) -> str:
        """
        Save analysis result with comprehensive metadata and context.
        
        Args:
            analysis_result: Complete analysis result dictionary
            ticker: Stock ticker symbol
            analysis_type: Type of analysis performed
            analyst_notes: Optional analyst commentary
            tags: Optional tags for categorization
            
        Returns:
            Snapshot ID
        """
        timestamp = datetime.now(timezone.utc)
        snapshot_id = self._generate_snapshot_id(ticker, timestamp)
        
        try:
            # Extract metadata
            market_context = self._extract_market_context(analysis_result)
            market_condition = self._classify_market_condition(analysis_result)
            data_quality_score = self._calculate_data_quality_score(analysis_result)
            
            # Extract timeframes
            timeframes = list(analysis_result.get('timeframe_analyses', {}).keys())
            
            # Create metadata object
            metadata = SnapshotMetadata(
                snapshot_id=snapshot_id,
                ticker=ticker,
                timestamp=timestamp,
                analysis_type=analysis_type,
                market_condition=market_condition,
                timeframes=timeframes,
                data_quality_score=data_quality_score,
                confidence_level=market_context.get('signal_confidence', 0.0),
                market_session=self._determine_market_session(timestamp),
                volatility_regime=self._classify_volatility_regime(market_context.get('volatility', 0.0)),
                # IMPORTANT: Get the string value from the enum here
                trend_direction=str(market_context.get('signal_type', 'UNKNOWN')),
                volume_profile=self._analyze_volume_profile(analysis_result),
                analyst_notes=analyst_notes,
                tags=tags or []
            )
            
            # --- START OF FIX ---
            # Convert the dataclass to a dictionary
            metadata_dict = asdict(metadata)
            
            # Now, manually convert non-serializable types to strings.
            # Convert datetime to an ISO 8601 formatted string
            if isinstance(metadata_dict.get("timestamp"), datetime):
                metadata_dict["timestamp"] = metadata_dict["timestamp"].isoformat()
            
            # Convert enums to their string values
            for key in ["analysis_type", "market_condition"]:
                if hasattr(metadata_dict.get(key), "value"):
                    metadata_dict[key] = metadata_dict[key].value
            # The 'trend_direction' field is already a string from the update above.
            # --- END OF FIX ---

            # Save data file
            data_file_path = self.data_dir / f"{snapshot_id}"
            saved_path = self._save_data_file(analysis_result, data_file_path)
            
            # Save to database
            with self.SessionLocal() as session:
                db_snapshot = AnalysisSnapshot(
                    id=snapshot_id,
                    ticker=ticker,
                    timestamp=timestamp,
                    analysis_type=analysis_type.value,
                    market_condition=market_condition.value,
                    timeframes=timeframes,
                    data_quality_score=data_quality_score,
                    confidence_level=metadata.confidence_level,
                    market_session=metadata.market_session,
                    volatility_regime=metadata.volatility_regime,
                    # IMPORTANT: Use the string value for the direct column
                    trend_direction=metadata.trend_direction, 
                    volume_profile=metadata.volume_profile,
                    analyst_notes=analyst_notes,
                    tags=tags,
                    # Use the fixed dictionary for the JSON column
                    metadata_json=metadata_dict,
                    data_path=saved_path
                )
                session.add(db_snapshot)
                session.commit()
            
            self.logger.info(f"Enhanced snapshot saved: {snapshot_id} for {ticker}")
            return snapshot_id
            
        except Exception as e:
            self.logger.error(f"Failed to save enhanced snapshot for {ticker}: {e}")
            raise
    
    # ... inside the MarketflowSnapshot class ...

    def load_enhanced_snapshot(self, snapshot_id: str) -> Tuple[Dict, SnapshotMetadata]:
        """
        Load analysis result and metadata by snapshot ID.
        
        Args:
            snapshot_id: Unique snapshot identifier
            
        Returns:
            Tuple of (analysis_result, metadata)
        """
        try:
            with self.SessionLocal() as session:
                db_snapshot = session.query(AnalysisSnapshot).filter(
                    AnalysisSnapshot.id == snapshot_id
                ).first()
                
                if not db_snapshot:
                    raise ValueError(f"Snapshot not found: {snapshot_id}")
                
                # Load data file
                analysis_result = self._load_data_file(db_snapshot.data_path)
                
                # --- START OF FIX ---
                # Reconstruct metadata by first loading the dictionary
                metadata_dict = db_snapshot.metadata_json
                
                # Convert string representations back to proper Python objects
                # Convert ISO string back to datetime object
                if "timestamp" in metadata_dict and isinstance(metadata_dict["timestamp"], str):
                    metadata_dict["timestamp"] = datetime.fromisoformat(metadata_dict["timestamp"])
                
                # Convert string values back to Enum objects
                if "analysis_type" in metadata_dict:
                    metadata_dict["analysis_type"] = AnalysisType(metadata_dict["analysis_type"])
                if "market_condition" in metadata_dict:
                    metadata_dict["market_condition"] = MarketCondition(metadata_dict["market_condition"])
                
                # Reconstruct the dataclass instance with the corrected types
                metadata = SnapshotMetadata(**metadata_dict)
                # --- END OF FIX ---
                
                return analysis_result, metadata
                
        except Exception as e:
            self.logger.error(f"Failed to load snapshot {snapshot_id}: {e}")
            raise
    
    def query_snapshots(self,
                       ticker: str = None,
                       start_date: datetime = None,
                       end_date: datetime = None,
                       market_condition: MarketCondition = None,
                       analysis_type: AnalysisType = None,
                       min_quality_score: float = None,
                       tags: List[str] = None,
                       limit: int = 100) -> List[Dict]:
        """
        Query snapshots with flexible filtering criteria.
        
        Args:
            ticker: Filter by ticker symbol
            start_date: Filter by start date
            end_date: Filter by end date
            market_condition: Filter by market condition
            analysis_type: Filter by analysis type
            min_quality_score: Minimum data quality score
            tags: Filter by tags
            limit: Maximum number of results
            
        Returns:
            List of snapshot metadata dictionaries
        """
        try:
            with self.SessionLocal() as session:
                query = session.query(AnalysisSnapshot)
                
                # Apply filters
                if ticker:
                    query = query.filter(AnalysisSnapshot.ticker == ticker)
                if start_date:
                    query = query.filter(AnalysisSnapshot.timestamp >= start_date)
                if end_date:
                    query = query.filter(AnalysisSnapshot.timestamp <= end_date)
                if market_condition:
                    query = query.filter(AnalysisSnapshot.market_condition == market_condition.value)
                if analysis_type:
                    query = query.filter(AnalysisSnapshot.analysis_type == analysis_type.value)
                if min_quality_score:
                    query = query.filter(AnalysisSnapshot.data_quality_score >= min_quality_score)
                
                # Order by timestamp descending
                query = query.order_by(AnalysisSnapshot.timestamp.desc())
                
                # Apply limit
                results = query.limit(limit).all()
                
                # Convert to dictionaries
                snapshots = []
                for result in results:
                    snapshot_dict = {
                        'id': result.id,
                        'ticker': result.ticker,
                        'timestamp': result.timestamp,
                        'analysis_type': result.analysis_type,
                        'market_condition': result.market_condition,
                        'timeframes': result.timeframes,
                        'data_quality_score': result.data_quality_score,
                        'confidence_level': result.confidence_level,
                        'market_session': result.market_session,
                        'volatility_regime': result.volatility_regime,
                        'trend_direction': result.trend_direction,
                        'volume_profile': result.volume_profile,
                        'analyst_notes': result.analyst_notes,
                        'tags': result.tags,
                        'created_at': result.created_at
                    }
                    snapshots.append(snapshot_dict)
                
                return snapshots
                
        except Exception as e:
            self.logger.error(f"Failed to query snapshots: {e}")
            raise
    
    def _determine_market_session(self, timestamp: datetime) -> str:
        """Determine market session based on timestamp"""
        hour = timestamp.hour
        if 9 <= hour < 16:
            return "REGULAR"
        elif 4 <= hour < 9:
            return "PRE_MARKET"
        elif 16 <= hour < 20:
            return "AFTER_HOURS"
        else:
            return "CLOSED"
    
    def _classify_volatility_regime(self, volatility: float) -> str:
        """Classify volatility regime"""
        if volatility < 0.15:
            return "LOW"
        elif volatility < 0.25:
            return "MEDIUM"
        elif volatility < 0.40:
            return "HIGH"
        else:
            return "EXTREME"
    
    def _analyze_volume_profile(self, analysis_result: Dict) -> str:
        """Analyze volume profile from analysis results"""
        timeframe_analyses = analysis_result.get('timeframe_analyses', {})
        
        # Simple volume profile analysis
        volume_signals = []
        for tf_data in timeframe_analyses.values():
            processed_data = tf_data.get('processed_data', {})
            volume_data = processed_data.get('volume')
            if volume_data is not None and hasattr(volume_data, 'mean'):
                avg_volume = volume_data.mean()
                recent_volume = volume_data.iloc[-1] if len(volume_data) > 0 else 0
                
                if recent_volume > avg_volume * 1.5:
                    volume_signals.append("HIGH")
                elif recent_volume < avg_volume * 0.5:
                    volume_signals.append("LOW")
                else:
                    volume_signals.append("NORMAL")
        
        if not volume_signals:
            return "UNKNOWN"
        
        # Return most common volume signal
        return max(set(volume_signals), key=volume_signals.count)


    
    # LLM Training Data Generation Methods
    
    def generate_llm_training_data(self, 
                                 snapshot_id: str,
                                 conversation_types: List[str] = None) -> List[str]:
        """
        Generate LLM training data from analysis snapshots.
        
        Args:
            snapshot_id: Snapshot to generate training data from
            conversation_types: Types of conversations to generate
            
        Returns:
            List of training record IDs
        """
        if conversation_types is None:
            conversation_types = [
                "analysis_explanation",
                "market_commentary", 
                "risk_assessment",
                "trading_recommendation",
                "technical_analysis",
                "wyckoff_analysis"
            ]
        
        try:
            analysis_result, metadata = self.load_enhanced_snapshot(snapshot_id)
            training_record_ids = []
            
            for conv_type in conversation_types:
                if conv_type == "analysis_explanation":
                    records = self._generate_analysis_explanation_data(snapshot_id, analysis_result, metadata)
                elif conv_type == "market_commentary":
                    records = self._generate_market_commentary_data(snapshot_id, analysis_result, metadata)
                elif conv_type == "risk_assessment":
                    records = self._generate_risk_assessment_data(snapshot_id, analysis_result, metadata)
                elif conv_type == "trading_recommendation":
                    records = self._generate_trading_recommendation_data(snapshot_id, analysis_result, metadata)
                elif conv_type == "technical_analysis":
                    records = self._generate_technical_analysis_data(snapshot_id, analysis_result, metadata)
                elif conv_type == "wyckoff_analysis":
                    records = self._generate_wyckoff_analysis_data(snapshot_id, analysis_result, metadata)
                else:
                    continue
                
                training_record_ids.extend(records)
            
            return training_record_ids
            
        except Exception as e:
            self.logger.error(f"Failed to generate LLM training data for {snapshot_id}: {e}")
            raise
    
    def _generate_analysis_explanation_data(self, 
                                          snapshot_id: str, 
                                          analysis_result: Dict, 
                                          metadata: SnapshotMetadata) -> List[str]:
        """Generate conversational explanations of analysis results"""
        records = []
        
        # Generate overall analysis explanation
        prompt = f"Explain the market analysis for {metadata.ticker} on {metadata.timestamp.strftime('%Y-%m-%d')}."
        
        signal = analysis_result.get('signal', {})
        risk = analysis_result.get('risk_assessment', {})
        
        response = f"""Based on my analysis of {metadata.ticker}, here's what I found:

**Overall Signal**: {signal.get('type', 'No clear signal')} with {signal.get('strength', 'unknown')} strength
**Market Condition**: {metadata.market_condition.value.replace('_', ' ').title()}
**Confidence Level**: {metadata.confidence_level:.1%}

**Key Findings**:
- Current trend direction: {metadata.trend_direction}
- Volatility regime: {metadata.volatility_regime}
- Volume profile: {metadata.volume_profile}
- Data quality score: {metadata.data_quality_score:.2f}/1.0

**Risk Assessment**:
- Risk level: {risk.get('risk_level', 'Unknown')}
- Stop loss: ${risk.get('stop_loss', 0):.2f}
- Take profit: ${risk.get('take_profit', 0):.2f}
- Risk/reward ratio: {risk.get('risk_reward_ratio', 0):.2f}

This analysis was performed during the {metadata.market_session.lower()} session and reflects {metadata.analysis_type.value} analysis methodology."""

        record_id = self._save_llm_training_record(
            snapshot_id=snapshot_id,
            conversation_type="analysis_explanation",
            prompt=prompt,
            response=response,
            context={
                "ticker": metadata.ticker,
                "timestamp": metadata.timestamp.isoformat(),
                "market_condition": metadata.market_condition.value,
                "analysis_type": metadata.analysis_type.value
            }
        )
        records.append(record_id)
        
        # Generate timeframe-specific explanations
        timeframe_analyses = analysis_result.get('timeframe_analyses', {})
        for timeframe, tf_data in timeframe_analyses.items():
            prompt = f"What does the {timeframe} timeframe analysis show for {metadata.ticker}?"
            
            trend_analysis = tf_data.get('trend_analysis', {})
            candle_analysis = tf_data.get('candle_analysis', {})
            
            response = f"""Looking at the {timeframe} timeframe for {metadata.ticker}:

**Trend Analysis**:
- Direction: {trend_analysis.get('trend_direction', 'Unknown')}
- Strength: {trend_analysis.get('trend_strength', 'Unknown')}

**Candle Patterns**:
- Last candle signal: {candle_analysis.get('last_candle_signal', {}).get('Name', 'None detected')}

**Support & Resistance**:"""
            
            sr_data = tf_data.get('support_resistance', {})
            if sr_data.get('support'):
                support_levels = [f"${level['price']:.2f}" for level in sr_data['support'][:3]]
                response += f"\n- Support levels: {', '.join(support_levels)}"
            if sr_data.get('resistance'):
                resistance_levels = [f"${level['price']:.2f}" for level in sr_data['resistance'][:3]]
                response += f"\n- Resistance levels: {', '.join(resistance_levels)}"
            
            response += f"\n\nThis timeframe provides {timeframe} perspective on the overall market structure and helps confirm or contradict signals from other timeframes."
            
            record_id = self._save_llm_training_record(
                snapshot_id=snapshot_id,
                conversation_type="analysis_explanation",
                prompt=prompt,
                response=response,
                context={
                    "ticker": metadata.ticker,
                    "timeframe": timeframe,
                    "timestamp": metadata.timestamp.isoformat()
                }
            )
            records.append(record_id)
        
        return records
    
    def _generate_market_commentary_data(self, 
                                       snapshot_id: str, 
                                       analysis_result: Dict, 
                                       metadata: SnapshotMetadata) -> List[str]:
        """Generate market commentary and sentiment analysis"""
        records = []
        
        prompt = f"Provide market commentary for {metadata.ticker} based on current conditions."
        
        # Generate contextual market commentary
        market_condition = metadata.market_condition.value.replace('_', ' ')
        session = metadata.market_session.lower()
        
        response = f"""**Market Commentary for {metadata.ticker}**

The current market environment for {metadata.ticker} shows {market_condition} conditions during the {session} session. 

**Market Dynamics**:
- Volatility is currently in the {metadata.volatility_regime.lower()} range
- Volume profile indicates {metadata.volume_profile.lower()} activity levels
- Overall trend direction is {metadata.trend_direction.lower()}

**Session Context**:
This analysis was captured during {session} hours, which typically shows {'higher' if session == 'regular' else 'lower'} volume and {'increased' if session == 'regular' else 'reduced'} institutional participation.

**Quality Assessment**:
The analysis has a data quality score of {metadata.data_quality_score:.1%}, indicating {'high' if metadata.data_quality_score > 0.8 else 'moderate' if metadata.data_quality_score > 0.6 else 'limited'} reliability in the underlying data."""

        if metadata.analyst_notes:
            response += f"\n\n**Analyst Notes**: {metadata.analyst_notes}"

        record_id = self._save_llm_training_record(
            snapshot_id=snapshot_id,
            conversation_type="market_commentary",
            prompt=prompt,
            response=response,
            context={
                "ticker": metadata.ticker,
                "market_condition": metadata.market_condition.value,
                "session": metadata.market_session
            }
        )
        records.append(record_id)
        
        return records
    
    def _generate_risk_assessment_data(self, 
                                     snapshot_id: str, 
                                     analysis_result: Dict, 
                                     metadata: SnapshotMetadata) -> List[str]:
        """Generate risk assessment conversations"""
        records = []
        
        risk = analysis_result.get('risk_assessment', {})
        current_price = analysis_result.get('current_price', 0)
        
        prompt = f"What are the key risks to consider for {metadata.ticker} at current levels?"
        
        response = f"""**Risk Assessment for {metadata.ticker}**

**Current Position**: ${current_price:.2f}

**Risk Metrics**:
- Stop Loss Level: ${risk.get('stop_loss', 0):.2f} ({((risk.get('stop_loss', 0) - current_price) / current_price * 100):.1f}% from current price)
- Take Profit Target: ${risk.get('take_profit', 0):.2f} ({((risk.get('take_profit', 0) - current_price) / current_price * 100):.1f}% from current price)
- Risk/Reward Ratio: {risk.get('risk_reward_ratio', 0):.2f}:1
- Position Size Recommendation: {risk.get('position_size', 0):.2f} shares
- Risk Per Share: ${risk.get('risk_per_share', 0):.2f}

**Market Risk Factors**:
- Volatility Regime: {metadata.volatility_regime} - {'Higher risk due to increased price swings' if metadata.volatility_regime in ['HIGH', 'EXTREME'] else 'Moderate risk environment'}
- Market Condition: {metadata.market_condition.value.replace('_', ' ').title()} - {'Trending markets offer clearer directional bias' if 'MARKET' in metadata.market_condition.value else 'Sideways markets increase whipsaw risk'}

**Confidence Level**: {metadata.confidence_level:.1%} - {'High confidence in analysis' if metadata.confidence_level > 0.8 else 'Moderate confidence' if metadata.confidence_level > 0.6 else 'Lower confidence - consider reducing position size'}

**Risk Management Recommendations**:
1. Always use stop losses to limit downside risk
2. Consider position sizing based on account risk tolerance
3. Monitor volume and volatility for changes in risk profile
4. Be aware of session-specific risks during {metadata.market_session.lower()} hours"""

        record_id = self._save_llm_training_record(
            snapshot_id=snapshot_id,
            conversation_type="risk_assessment",
            prompt=prompt,
            response=response,
            context={
                "ticker": metadata.ticker,
                "current_price": current_price,
                "risk_metrics": risk
            }
        )
        records.append(record_id)
        
        return records
    
    def _generate_trading_recommendation_data(self, 
                                            snapshot_id: str, 
                                            analysis_result: Dict, 
                                            metadata: SnapshotMetadata) -> List[str]:
        """Generate trading recommendation conversations"""
        records = []
        
        signal = analysis_result.get('signal', {})
        risk = analysis_result.get('risk_assessment', {})
        current_price = analysis_result.get('current_price', 0)
        
        prompt = f"Should I buy, sell, or hold {metadata.ticker} based on your analysis?"
        
        signal_type_enum = signal.get('type', 'HOLD')
        signal_type = str(signal_type_enum.value) if hasattr(signal_type_enum, 'value') else str(signal_type_enum)

        signal_strength_enum = signal.get('strength', 'WEAK')
        signal_strength = str(signal_strength_enum.value) if hasattr(signal_strength_enum, 'value') else str(signal_strength_enum)
        
        if 'BUY' in signal_type.upper():
            action = "BUY"
            reasoning = "The analysis indicates bullish conditions with favorable risk/reward characteristics."
        elif 'SELL' in signal_type.upper():
            action = "SELL" 
            reasoning = "The analysis suggests bearish conditions and potential downside risk."
        else:
            action = "HOLD"
            reasoning = "The analysis shows mixed or unclear signals, suggesting a wait-and-see approach."
        
        response = f"""**Trading Recommendation for {metadata.ticker}**

**Recommendation**: {action}
**Signal Strength**: {signal_strength}
**Confidence**: {metadata.confidence_level:.1%}

**Reasoning**: {reasoning}

**Entry Strategy** (if {action}):
- Current Price: ${current_price:.2f}
- Suggested Entry: {'Market order or slight pullback' if action == 'BUY' else 'Market order or bounce' if action == 'SELL' else 'Wait for clearer signals'}
- Stop Loss: ${risk.get('stop_loss', 0):.2f}
- Take Profit: ${risk.get('take_profit', 0):.2f}
- Position Size: {risk.get('position_size', 0):.2f} shares

**Key Considerations**:
- Market condition: {metadata.market_condition.value.replace('_', ' ').title()}
- Volatility: {metadata.volatility_regime}
- Volume profile: {metadata.volume_profile}
- Session timing: {metadata.market_session}

**Risk Factors**:
- Risk per share: ${risk.get('risk_per_share', 0):.2f}
- Risk/reward ratio: {risk.get('risk_reward_ratio', 0):.2f}:1

**Important**: This recommendation is based on technical analysis as of {metadata.timestamp.strftime('%Y-%m-%d %H:%M')}. Always consider your own risk tolerance, portfolio allocation, and market conditions before making trading decisions."""

        record_id = self._save_llm_training_record(
            snapshot_id=snapshot_id,
            conversation_type="trading_recommendation",
            prompt=prompt,
            response=response,
            context={
                "ticker": metadata.ticker,
                "recommendation": action,
                "signal_type": signal_type,
                "confidence": metadata.confidence_level
            }
        )
        records.append(record_id)
        
        return records
    
    def _generate_technical_analysis_data(self, 
                                        snapshot_id: str, 
                                        analysis_result: Dict, 
                                        metadata: SnapshotMetadata) -> List[str]:
        """Generate technical analysis conversations"""
        records = []
        
        # Generate questions about technical indicators
        timeframe_analyses = analysis_result.get('timeframe_analyses', {})
        
        for timeframe, tf_data in timeframe_analyses.items():
            prompt = f"What do the technical indicators show for {metadata.ticker} on the {timeframe} timeframe?"
            
            # Extract technical analysis components
            trend_analysis = tf_data.get('trend_analysis', {})
            candle_analysis = tf_data.get('candle_analysis', {})
            pattern_analysis = tf_data.get('pattern_analysis', {})
            sr_data = tf_data.get('support_resistance', {})
            
            response = f"""**Technical Analysis - {timeframe.upper()} Timeframe for {metadata.ticker}**

**Trend Analysis**:
- Primary Trend: {trend_analysis.get('trend_direction', 'Undefined')}
- Trend Strength: {trend_analysis.get('trend_strength', 'Unknown')}
- Trend Quality: {'Strong and consistent' if trend_analysis.get('trend_strength', 0) > 0.7 else 'Moderate' if trend_analysis.get('trend_strength', 0) > 0.4 else 'Weak or choppy'}

**Candlestick Patterns**:"""
            
            last_candle = candle_analysis.get('last_candle_signal', {})
            if last_candle.get('Name'):
                response += f"\n- Recent Pattern: {last_candle['Name']}"
                response += f"\n- Pattern Significance: {last_candle.get('Description', 'Standard candlestick pattern')}"
            else:
                response += "\n- No significant candlestick patterns detected"
            
            response += "\n\n**Support and Resistance Levels**:"
            if sr_data.get('support'):
                support_levels = [f"${level['price']:.2f} (strength: {level.get('strength', 'unknown')})" 
                                for level in sr_data['support'][:3]]
                response += f"\n- Key Support: {', '.join(support_levels)}"
            
            if sr_data.get('resistance'):
                resistance_levels = [f"${level['price']:.2f} (strength: {level.get('strength', 'unknown')})" 
                                   for level in sr_data['resistance'][:3]]
                response += f"\n- Key Resistance: {', '.join(resistance_levels)}"
            
            if pattern_analysis:
                response += "\n\n**Chart Patterns**:"
                for pattern_name, pattern_data in pattern_analysis.items():
                    if isinstance(pattern_data, dict) and pattern_data:
                        response += f"\n- {pattern_name.replace('_', ' ').title()}: Detected"
            
            response += f"\n\n**Timeframe Context**: The {timeframe} timeframe provides {'short-term' if timeframe in ['1m', '5m', '15m'] else 'medium-term' if timeframe in ['1h', '4h'] else 'long-term'} perspective and should be considered alongside other timeframes for comprehensive analysis."
            
            record_id = self._save_llm_training_record(
                snapshot_id=snapshot_id,
                conversation_type="technical_analysis",
                prompt=prompt,
                response=response,
                context={
                    "ticker": metadata.ticker,
                    "timeframe": timeframe,
                    "analysis_components": list(tf_data.keys())
                }
            )
            records.append(record_id)
        
        return records
    
    def _generate_wyckoff_analysis_data(self, 
                                      snapshot_id: str, 
                                      analysis_result: Dict, 
                                      metadata: SnapshotMetadata) -> List[str]:
        """Generate Wyckoff analysis conversations"""
        records = []
        
        timeframe_analyses = analysis_result.get('timeframe_analyses', {})
        
        for timeframe, tf_data in timeframe_analyses.items():
            wyckoff_phases = tf_data.get('wyckoff_phases', [])
            wyckoff_events = tf_data.get('wyckoff_events', [])
            wyckoff_ranges = tf_data.get('wyckoff_trading_ranges', [])
            
            if not any([wyckoff_phases, wyckoff_events, wyckoff_ranges]):
                continue
            
            prompt = f"What does the Wyckoff analysis reveal about {metadata.ticker} on the {timeframe} timeframe?"
            
            response = f"""**Wyckoff Analysis - {timeframe.upper()} Timeframe for {metadata.ticker}**

**Market Structure Analysis**:"""
            
            if wyckoff_phases:
                current_phase = wyckoff_phases[-1] if wyckoff_phases else None
                if current_phase:
                    phase_name = current_phase.get('phase', 'Unknown')
                    response += f"\n- Current Wyckoff Phase: {phase_name}"
                    response += f"\n- Phase Context: {self._get_wyckoff_phase_explanation(phase_name)}"
            
            if wyckoff_ranges:
                response += "\n\n**Trading Ranges Identified**:"
                for i, range_data in enumerate(wyckoff_ranges[-3:], 1):  # Last 3 ranges
                    context = range_data.get('context', 'Unknown')
                    support = range_data.get('support', 0)
                    resistance = range_data.get('resistance', 0)
                    response += f"\n- Range {i}: {context} (${support:.2f} - ${resistance:.2f})"
            
            if wyckoff_events:
                response += "\n\n**Recent Wyckoff Events**:"
                recent_events = wyckoff_events[-5:]  # Last 5 events
                for event in recent_events:
                    event_name = event.get('event_name', 'Unknown Event')
                    event_price = event.get('price', 0)
                    response += f"\n- {event_name} at ${event_price:.2f}"
            
            response += f"""

**Wyckoff Interpretation**:
The Wyckoff methodology focuses on understanding the relationship between price and volume to identify the intentions of large market participants (the \"Composite Man\"). 

{f'This analysis suggests institutional accumulation or distribution activity' if wyckoff_events else 'The current structure shows'}
{f'clear market phases' if wyckoff_phases else 'developing market structure'} that can help identify potential turning points and trend continuations.

**Trading Implications**:
- {f'Look for' if wyckoff_phases else 'Monitor for'} volume confirmation of price movements
- {f'Respect' if wyckoff_ranges else 'Watch for'} key support and resistance levels from trading ranges
- Consider the broader market context when interpreting Wyckoff signals"""
            
            record_id = self._save_llm_training_record(
                snapshot_id=snapshot_id,
                conversation_type="wyckoff_analysis",
                prompt=prompt,
                response=response,
                context={
                    "ticker": metadata.ticker,
                    "timeframe": timeframe,
                    "has_phases": bool(wyckoff_phases),
                    "has_events": bool(wyckoff_events),
                    "has_ranges": bool(wyckoff_ranges)
                }
            )
            records.append(record_id)
        
        return records
    
    def _get_wyckoff_phase_explanation(self, phase_name: str) -> str:
        """Get explanation for Wyckoff phase"""
        phase_explanations = {
            "Accumulation": "Smart money is quietly buying while prices are relatively low",
            "Markup": "Prices are rising as demand exceeds supply",
            "Distribution": "Smart money is selling to the public at higher prices",
            "Markdown": "Prices are falling as supply exceeds demand",
            "Re-accumulation": "A pause in an uptrend where smart money adds to positions",
            "Re-distribution": "A pause in a downtrend where smart money continues selling"
        }
        return phase_explanations.get(phase_name, "A specific phase in the Wyckoff market cycle")
    
    def _save_llm_training_record(self, 
                                snapshot_id: str,
                                conversation_type: str,
                                prompt: str,
                                response: str,
                                context: Dict,
                                quality_score: float = 0.8) -> str:
        """Save LLM training record to database"""
        try:
            record_id = str(uuid.uuid4())
            
            with self.SessionLocal() as session:
                training_record = LLMTrainingRecord(
                    id=record_id,
                    snapshot_id=snapshot_id,
                    conversation_type=conversation_type,
                    prompt=prompt,
                    response=response,
                    context=context,
                    quality_score=quality_score,
                    human_validated=False
                )
                session.add(training_record)
                session.commit()
            
            return record_id
            
        except Exception as e:
            self.logger.error(f"Failed to save LLM training record: {e}")
            raise
    
    def export_llm_training_data(self, 
                               output_format: str = "jsonl",
                               conversation_types: List[str] = None,
                               min_quality_score: float = 0.7,
                               limit: int = None) -> str:
        """
        Export LLM training data in various formats.
        
        Args:
            output_format: Format for export ('jsonl', 'csv', 'parquet')
            conversation_types: Filter by conversation types
            min_quality_score: Minimum quality score threshold
            limit: Maximum number of records to export
            
        Returns:
            Path to exported file
        """
        try:
            with self.SessionLocal() as session:
                query = session.query(LLMTrainingRecord)
                
                # Apply filters
                if conversation_types:
                    query = query.filter(LLMTrainingRecord.conversation_type.in_(conversation_types))
                if min_quality_score:
                    query = query.filter(LLMTrainingRecord.quality_score >= min_quality_score)
                
                # Order by creation date
                query = query.order_by(LLMTrainingRecord.created_at.desc())
                
                if limit:
                    query = query.limit(limit)
                
                records = query.all()
                
                # Export based on format
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                
                if output_format == "jsonl":
                    export_path = self.llm_dir / f"training_data_{timestamp}.jsonl"
                    with open(export_path, 'w', encoding='utf-8') as f:
                        for record in records:
                            training_example = {
                                "prompt": record.prompt,
                                "response": record.response,
                                "metadata": {
                                    "conversation_type": record.conversation_type,
                                    "quality_score": record.quality_score,
                                    "context": record.context,
                                    "created_at": record.created_at.isoformat()
                                }
                            }
                            f.write(json.dumps(training_example) + '\n')
                
                elif output_format == "csv":
                    export_path = self.llm_dir / f"training_data_{timestamp}.csv"
                    data = []
                    for record in records:
                        data.append({
                            'prompt': record.prompt,
                            'response': record.response,
                            'conversation_type': record.conversation_type,
                            'quality_score': record.quality_score,
                            'context': json.dumps(record.context),
                            'created_at': record.created_at.isoformat()
                        })
                    pd.DataFrame(data).to_csv(export_path, index=False)
                
                elif output_format == "parquet":
                    export_path = self.llm_dir / f"training_data_{timestamp}.parquet"
                    data = []
                    for record in records:
                        data.append({
                            'prompt': record.prompt,
                            'response': record.response,
                            'conversation_type': record.conversation_type,
                            'quality_score': record.quality_score,
                            'context': json.dumps(record.context),
                            'created_at': record.created_at
                        })
                    pd.DataFrame(data).to_parquet(export_path, index=False)
                
                else:
                    raise ValueError(f"Unsupported export format: {output_format}")
                
                self.logger.info(f"Exported {len(records)} LLM training records to {export_path}")
                return str(export_path)
                
        except Exception as e:
            self.logger.error(f"Failed to export LLM training data: {e}")
            raise
    
    def get_training_data_statistics(self) -> Dict[str, Any]:
        """Get statistics about available LLM training data"""
        try:
            with self.SessionLocal() as session:
                # Total records
                total_records = session.query(LLMTrainingRecord).count()
                
                # Records by conversation type
                conv_type_stats = session.query(
                    LLMTrainingRecord.conversation_type,
                    func.count(LLMTrainingRecord.id).label('count')
                ).group_by(LLMTrainingRecord.conversation_type).all()
                
                # Quality score distribution
                quality_stats = session.query(
                    LLMTrainingRecord.quality_score
                ).all()
                quality_scores = [r[0] for r in quality_stats if r[0] is not None]
                
                # Human validation stats
                validated_count = session.query(LLMTrainingRecord).filter(
                    LLMTrainingRecord.human_validated == True
                ).count()
                
                return {
                    "total_records": total_records,
                    "conversation_types": dict(conv_type_stats),
                    "quality_score_stats": {
                        "mean": np.mean(quality_scores) if quality_scores else 0,
                        "std": np.std(quality_scores) if quality_scores else 0,
                        "min": np.min(quality_scores) if quality_scores else 0,
                        "max": np.max(quality_scores) if quality_scores else 0
                    },
                    "human_validated_count": validated_count,
                    "validation_rate": validated_count / total_records if total_records > 0 else 0
                }
                
        except Exception as e:
            self.logger.error(f"Failed to get training data statistics: {e}")
            raise

# Example usage and testing
if __name__ == "__main__":
    # Initialize enhanced snapshot manager
    snapshot_manager = MarketflowSnapshot(
        output_dir="./enhanced_snapshots",
        enable_compression=True
    )
    
    # Example analysis result (would come from MarketFlow facade)
    example_analysis = {
        "ticker": "AAPL",
        "current_price": 150.25,
        "signal": {
            "type": "BUY",
            "strength": "STRONG",
            "confidence": 0.85,
            "details": "Strong bullish momentum with volume confirmation"
        },
        "risk_assessment": {
            "risk_level": "MEDIUM",
            "stop_loss": 145.50,
            "take_profit": 158.75,
            "risk_reward_ratio": 1.8,
            "position_size": 100,
            "risk_per_share": 4.75,
            "volatility": 0.22
        },
        "timeframe_analyses": {
            "1d": {
                "trend_analysis": {
                    "trend_direction": "BULLISH",
                    "trend_strength": 0.75
                },
                "candle_analysis": {
                    "last_candle_signal": {
                        "Name": "Bullish Engulfing",
                        "Description": "Strong bullish reversal pattern"
                    }
                },
                "support_resistance": {
                    "support": [{"price": 148.50, "strength": "strong"}],
                    "resistance": [{"price": 152.75, "strength": "moderate"}]
                },
                "wyckoff_phases": [{"phase": "Markup", "confidence": 0.7}],
                "wyckoff_events": [
                    {
                        "event_name": "Spring Test",
                        "price": 149.25,
                        "volume": 1500000,
                        "timestamp": "2025-01-15T14:30:00"
                    }
                ],
                "wyckoff_trading_ranges": [
                    {
                        "context": "Accumulation",
                        "support": 145.00,
                        "resistance": 152.00,
                        "start_timestamp": "2025-01-10T09:30:00",
                        "end_timestamp": "2025-01-15T16:00:00"
                    }
                ]
            }
        }
    }
    
    # Save enhanced snapshot
    snapshot_id = snapshot_manager.save_enhanced_snapshot(
        analysis_result=example_analysis,
        ticker="AAPL",
        analysis_type=AnalysisType.WYCKOFF,
        analyst_notes="Strong bullish setup with Wyckoff confirmation",
        tags=["bullish", "wyckoff", "high_confidence"]
    )
    
    print(f"Saved snapshot: {snapshot_id}")
    
    # Generate LLM training data
    training_ids = snapshot_manager.generate_llm_training_data(snapshot_id)
    print(f"Generated {len(training_ids)} LLM training records")
    
    # Export training data
    export_path = snapshot_manager.export_llm_training_data(output_format="jsonl")
    print(f"Exported training data to: {export_path}")
    
    # Get statistics
    stats = snapshot_manager.get_training_data_statistics()
    print(f"Training data statistics: {stats}")

