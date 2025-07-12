"""
Marketflow Report Module
Handles the creation of all Marketflow and Wyckoff related data handling.
"""

import pandas as pd
from typing import Dict
from datetime import datetime
from pathlib import Path

from marketflow.marketflow_logger import get_logger
from marketflow.marketflow_config_manager import create_app_config
from marketflow.marketflow_results_extractor import MarketflowResultExtractor

class MarketflowReport:
    """
    Handles the creation of all Marketflow and Wyckoff related data.
    This class takes a MarketflowResultExtractor instance to access all analysis data.
    """
    
    def __init__(self, extractor, output_dir: str):
        """
        Initializes the Marketflow Report.
        
        Args:
            extractor: MarketflowResultExtractor instance or compatible object
            output_dir: Directory to save charts and reports
        """

         # Initialize logger and configuration manager
        self.logger = get_logger(module_name="MarketflowReport")

        # Create configuration manager for API keys and settings
        self.config_manager = create_app_config(self.logger)


        # Validate extractor
        if MarketflowResultExtractor and not isinstance(extractor, MarketflowResultExtractor):
            if not hasattr(extractor, 'get_price_data'):
                raise TypeError("extractor must have required methods like get_price_data")
        
        self.extractor = extractor
        self.logger.info(f"MarketflowReport initialized with extractor: {type(extractor).__name__}")


        # Validate and set output directory
        if not isinstance(output_dir, str) or not output_dir:
            self.logger.debug("Invalid output_dir provided: %s", output_dir)
            raise ValueError("output_dir must be a non-empty string")
        
        report_dir = Path(output_dir)
        self.logger.debug("Creating report directory at: %s", report_dir)
        report_dir.mkdir(parents=True, exist_ok=True)

        self.output_dir = report_dir

        self.logger.info("Output directory set to: %s", self.output_dir)

        self.report = self.generate_report_for_ticker
    
    def create_summary_report(self, ticker: str) -> bool:
        """
        Generates a detailed, comprehensive text-based summary report for a given ticker.
        """
        try:
            report_path = self.output_dir / f"{ticker}_summary_report.txt"
            self.logger.info(f"Generating detailed summary report for {ticker}")

            with open(report_path, 'w', encoding="utf-8") as f:
                f.write(f"{'='*80}\n")
                f.write(f"VPA & Wyckoff Analysis Report for: {ticker}\n")
                f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"{'='*80}\n\n")

                # --- Overall Signal and Risk ---
                f.write("--- OVERALL ASSESSMENT ---\n")
                signal = self.extractor.get_signal(ticker)
                risk = self.extractor.get_risk_assessment(ticker)
                current_price = self.extractor.get_current_price(ticker)
                
                f.write(f"  Signal Type:     {signal.get('type', 'N/A')}\n")
                f.write(f"  Signal Strength: {signal.get('strength', 'N/A')}\n")
                f.write(f"  Details:         {signal.get('details', 'N/A')}\n\n")
                f.write(f"  Current Price:   ${current_price:.2f}\n")
                f.write(f"  Stop Loss:       ${risk.get('stop_loss', 0):.2f}\n")
                f.write(f"  Take Profit:     ${risk.get('take_profit', 0):.2f}\n")
                f.write(f"  Risk/Reward:     {risk.get('risk_reward_ratio', 0):.2f}\n\n")

                # --- Detailed Timeframe Analysis ---
                timeframes = self.extractor.get_timeframes(ticker)
                for tf in timeframes:
                    f.write(f"{'-'*80}\n")
                    f.write(f"--- TIMEFRAME ANALYSIS: {tf.upper()} ---\n")
                    f.write(f"{'-'*80}\n\n")

                    # --- Trend, Candle, and Pattern Analysis ---
                    trend = self.extractor.get_trend_analysis(ticker, tf)
                    candle = self.extractor.get_candle_analysis(ticker, tf)
                    pattern = self.extractor.get_pattern_analysis(ticker, tf)
                    sr = self.extractor.get_support_resistance(ticker, tf)

                    f.write("  Conventional Analysis:\n")
                    if trend: f.write(f"    - Trend: {trend.get('trend_direction', 'N/A')} (Strength: {trend.get('trend_strength', 'N/A')})\n")
                    if candle: f.write(f"    - Last Candle Signal: {candle.get('last_candle_signal', {}).get('Name', 'None')}\n")
                    if pattern: f.write(f"    - Patterns Detected: {', '.join(pattern.keys()) if pattern else 'None'}\n")
                    
                    support_levels = [lvl['price'] for lvl in sr.get('support', [])]
                    resistance_levels = [lvl['price'] for lvl in sr.get('resistance', [])]
                    if support_levels: f.write(f"    - Support Levels: {', '.join(f'${lvl:.2f}' for lvl in support_levels)}\n")
                    if resistance_levels: f.write(f"    - Resistance Levels: {', '.join(f'${lvl:.2f}' for lvl in resistance_levels)}\n")
                    f.write("\n")

                    # --- Detailed Wyckoff Analysis ---
                    wyckoff_phases = self.extractor.get_wyckoff_phases(ticker, tf)
                    wyckoff_events = self.extractor.get_wyckoff_events(ticker, tf)
                    wyckoff_ranges = self.extractor.get_wyckoff_trading_ranges(ticker, tf)
                    
                    if not (wyckoff_phases or wyckoff_events or wyckoff_ranges):
                        f.write("  Wyckoff Analysis: No significant Wyckoff structures detected.\n\n")
                        continue

                    f.write("  Wyckoff Analysis:\n")
                    
                    # Wyckoff Phases
                    if wyckoff_phases:
                        latest_phase = wyckoff_phases[-1]
                        f.write(f"    - Current Phase: {latest_phase.get('phase', 'N/A')}\n")
                    
                    # Wyckoff Trading Ranges
                    if wyckoff_ranges:
                        f.write("    - Detected Trading Ranges:\n")
                        for i, wr in enumerate(wyckoff_ranges):
                            start_timestamp = wr.get('start_timestamp')
                            end_timestamp = wr.get('end_timestamp')
                            start = pd.to_datetime(start_timestamp).strftime('%Y-%m-%d') if start_timestamp else 'N/A'
                            end = pd.to_datetime(end_timestamp).strftime('%Y-%m-%d') if end_timestamp else 'Ongoing'
                            f.write(f"      - Range {i+1} ({wr.get('context', 'N/A')}):\n")
                            f.write(f"          Duration: {start} to {end}\n")
                            f.write(f"          Support: ${wr.get('support', 0):.2f}, Resistance: ${wr.get('resistance', 0):.2f}\n")
                    
                    # Wyckoff Events (last 10)
                    if wyckoff_events:
                        f.write("    - Recent Key Events (up to last 10):\n")
                        for event in wyckoff_events[-10:]:
                            timestamp = event.get('timestamp')
                            if timestamp:
                                try:
                                    ts = pd.to_datetime(timestamp).strftime('%Y-%m-%d %H:%M')
                                except (ValueError, TypeError):
                                    ts = str(timestamp)
                            else:
                                ts = 'N/A'
                            
                            event_name = event.get('event_name', 'N/A')
                            details = event.get('description') or event.get('subtype') or ''
                            details_str = f" ({details})" if details else ""
                            price = event.get('price', 0)
                            volume = event.get('volume', 0)
                            
                            f.write(f"        - {ts}: {event_name}{details_str} @ ${price:.2f} (Vol: {volume:.0f})\n")
                    f.write("\n")

                f.write(f"{'='*80}\n")
                f.write("End of Report\n")
                f.write(f"{'='*80}\n")

            self.logger.info(f"Detailed summary report saved to {report_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error creating detailed summary report for {ticker}: {e}", exc_info=True)
            return False

    def generate_report_for_ticker(self, ticker: str) -> Dict[str, bool]:
        """
        A convenient method to run all visualization generation for a single ticker.
        
        Returns:
            Dict[str, bool]: Results of each visualization attempt
        """
        self.logger.info(f"--- Generating all visuals for {ticker} ---")
        
        results = {}
        
        # Create summary report
        results['summary_report'] = self.create_summary_report(ticker)
        self.logger.info(f"Summary report generation for {ticker}: {results['summary_report']}")      
        self.logger.info(f"--- Finished generating report for {ticker}")
        
        return results
