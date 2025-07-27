"""
Marketflow LLM Narratives
-------------------------
This module contains functions for generating natural language summaries,
markdown, or prompts for LLM outputs from Marketflow analysis results.

Each function takes in the relevant data dictionary (e.g., from the facade or extractor)
and returns a text/markdown string (or dict) ready for LLM use.
"""

from typing import Dict, Any, Optional

from marketflow.marketflow_logger import get_logger
from marketflow.marketflow_config_manager import create_app_config

logger = get_logger("MarketflowLLMNarrative")
app_config = create_app_config(logger=logger)

def generate_analysis_narrative(analysis: dict) -> str:
    """
    Synthesizes the VPA and Wyckoff analysis into a coherent narrative story.
    This is the core intelligence of the interface.
    """
    logger.info(f"Generating analysis narrative for ticker: {analysis.get('ticker', 'UNKNOWN')}")
    ticker = analysis["ticker"]
    signal = analysis["signal"]
    primary_tf_key = list(analysis["timeframe_analyses"].keys())[0]
    primary_tf_analysis = analysis["timeframe_analyses"][primary_tf_key]
    
    # Extract the latest Wyckoff context
    latest_phase = primary_tf_analysis.get("wyckoff_phases", [])[-1] if primary_tf_analysis.get("wyckoff_phases") else None
    latest_event = primary_tf_analysis.get("wyckoff_events", [])[-1] if primary_tf_analysis.get("wyckoff_events") else None
    
    narrative = f"**Narrative Analysis for {ticker} (Primary Timeframe: {primary_tf_key}):**\n\n"
    
    # 1. Start with the overall VPA Signal
    narrative += f"The primary VPA signal is **{signal['type']} ({signal['strength']})**. "
    narrative += f"Reasoning: {signal['details']}.\n\n"
    
    # 2. Connect to Wyckoff Context
    if latest_phase and latest_event:
        phase_val = latest_phase['phase']
        event_val = latest_event['event']
        logger.info(f"Wyckoff context: phase={phase_val}, event={event_val}, timestamp={latest_event['timestamp']}")
        narrative += f"This signal is supported by the current Wyckoff context. The market is in **{phase_val}**. "
        narrative += f"The most recent significant event was a **{event_val}** on {latest_event['timestamp']}.\n"
        
        # Add specific narrative based on phase and signal
        if signal['type'] == 'BUY' and latest_phase['phase_name'] in ['D', 'E'] and 'Accumulation' in latest_phase.get('context', ''):
            logger.info("Pattern: BUY signal with Accumulation phase D/E")
            narrative += f"This is a constructive pattern, suggesting that the accumulation phase has completed and the markup (uptrend) is underway. The {event_val} confirms buyer control.\n"
        elif signal['type'] == 'SELL' and latest_phase['phase_name'] in ['D', 'E'] and 'Distribution' in latest_phase.get('context', ''):
            logger.info("Pattern: SELL signal with Distribution phase D/E")
            narrative += f"This is a bearish pattern, suggesting that the distribution phase has completed and the markdown (downtrend) is in progress. The {event_val} confirms seller control.\n"
        elif signal['type'] == 'HOLD' or signal['type'] == 'NO_SIGNAL':
            logger.info("Pattern: HOLD or NO_SIGNAL in consolidation phase")
            narrative += f"The market appears to be in a consolidation or 'cause-building' phase. It's advisable to wait for a clear Sign of Strength (breakout) or Sign of Weakness (breakdown) before considering a new position.\n"
        else:
            logger.info(f"Conflict detected: VPA signal={signal['type']} vs Wyckoff context={latest_phase.get('context', 'unknown')}")
            # Highlight conflicts
            narrative += f"**Warning:** There is a potential conflict between the VPA signal ({signal['type']}) and the Wyckoff context ({latest_phase.get('context', 'unknown')}). This suggests uncertainty, and caution is advised.\n"

    elif latest_phase:
        logger.info(f"Wyckoff phase only: phase={latest_phase['phase']}")
        narrative += f"The market is currently in **{latest_phase['phase']}** according to Wyckoff analysis, but specific events are unclear. This indicates a period of consolidation.\n"
    else:
        logger.info("No Wyckoff phase or event identified")
        narrative += "Wyckoff analysis did not identify a clear phase or event, suggesting the market is in a random or non-structural state.\n"

    # 3. Discuss Trading Ranges
    if primary_tf_analysis.get("wyckoff_trading_ranges"):
        tr = primary_tf_analysis["wyckoff_trading_ranges"][-1]
        logger.info(f"Trading range identified: support={tr['support']}, resistance={tr['resistance']}")
        narrative += f"\nA trading range has been identified between **support at ~${tr['support']:.2f}** and **resistance at ~${tr['resistance']:.2f}**. "
        narrative += "This range represents the 'cause' being built for the next trend.\n"

    # 4. Conclude with risk assessment
    risk = analysis['risk_assessment']
    narrative += f"\n**Trade Management:** Based on this analysis, the suggested stop-loss is **${risk.get('stop_loss', 0):.2f}** and the take-profit target is **${risk.get('take_profit', 0):.2f}**, offering a risk-reward ratio of **{risk.get('risk_reward_ratio', 0):.2f}**."

    logger.info(f"Generated narrative for {ticker}: {narrative[:200]}...")  # Log first 200 chars
    return narrative.strip()