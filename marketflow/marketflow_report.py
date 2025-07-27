"""
Marketflow Report Module
Handles the creation of all Marketflow and Wyckoff related data handling.
"""

import pandas as pd
import json
import re
from typing import Dict, Any
from datetime import datetime
from pathlib import Path

from marketflow.marketflow_logger import get_logger
from marketflow.marketflow_config_manager import create_app_config
from marketflow.marketflow_results_extractor import MarketflowResultExtractor
from marketflow.marketflow_utils import sanitize_filename

class MarketflowReport:
    """
    Handles the creation of all Marketflow and Wyckoff related data.
    This class takes a MarketflowResultExtractor instance to access all analysis data.
    """
    
    def __init__(self, extractor: MarketflowResultExtractor, output_dir: str):
        """
        Initializes the Marketflow Report.
        
        Args:
            extractor: MarketflowResultExtractor instance.
            output_dir: Directory to save charts and reports.
        """
        self.logger = get_logger(module_name="MarketflowReport")
        self.config_manager = create_app_config(self.logger)

        if not isinstance(extractor, MarketflowResultExtractor):
            raise TypeError("extractor must be an instance of MarketflowResultExtractor")
        
        self.extractor = extractor
        self.logger.info(f"MarketflowReport initialized with extractor: {type(extractor).__name__}")

        if not isinstance(output_dir, str) or not output_dir:
            raise ValueError("output_dir must be a non-empty string")
        
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.logger.info(f"Output directory set to: {self.output_dir.resolve()}")

        self.logger.info("MarketflowReport initialized successfully")

    def _format_dict_for_text(self, data: dict, title: str, indent: str = "      ") -> str:
        """Helper to format a dictionary into a clean, aligned string for text reports."""
        if not data:
            return f"{indent}- {title}: None\n"
        
        text = f"{indent}- {title}:\n"
        # Find the longest key for alignment
        max_key_len = max(len(str(k)) for k in data.keys()) if data else 0
        
        for key, value in data.items():
            key_str = f"{key}:".ljust(max_key_len + 2)
            if isinstance(value, float):
                value_str = f"{value:.2f}"
            else:
                value_str = str(value)
            text += f"{indent}  {key_str} {value_str}\n"
        return text

    def create_summary_report(self, ticker: str) -> bool:
        """
        Generates a detailed, comprehensive text-based summary report for a given ticker.
        """
        try:
            current_date = datetime.now().strftime("%Y-%m-%d")
            sanitized_ticker = sanitize_filename(ticker)
            report_path = self.output_dir / f"{current_date}_{sanitized_ticker}_summary_report.txt"
            self.logger.info(f"Generating detailed summary report for {sanitized_ticker} at {report_path}")

            with open(report_path, 'w', encoding="utf-8") as f:
                f.write(f"{'='*80}\n")
                f.write(f"Marketflow Analysis Report for: {ticker}\n")
                f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"{'='*80}\n\n")

                # --- Overall Signal and Risk ---
                f.write("--- OVERALL ASSESSMENT ---\n")
                signal = self.extractor.get_signal(ticker)
                risk = self.extractor.get_risk_assessment(ticker)
                price = self.extractor.get_current_price(ticker)
                
                f.write(f"  {'Signal Type:'.ljust(20)} {signal.get('type', 'N/A')}\n")
                f.write(f"  {'Signal Strength:'.ljust(20)} {signal.get('strength', 'N/A')}\n")
                f.write(f"  {'Details:'.ljust(20)} {signal.get('details', 'N/A')}\n\n")
                f.write(f"  {'Current Price:'.ljust(20)} ${price:.2f}\n")
                f.write(f"  {'Stop Loss:'.ljust(20)} ${risk.get('stop_loss', 0):.2f}\n")
                f.write(f"  {'Take Profit:'.ljust(20)} ${risk.get('take_profit', 0):.2f}\n")
                f.write(f"  {'Risk/Reward Ratio:'.ljust(20)} {risk.get('risk_reward_ratio', 0):.2f}\n\n")
                f.write(f"  {'Position Size:'.ljust(20)} {risk.get('position_size', 0):.2f}\n\n")
                f.write(f"  {'Risk Per Share:'.ljust(20)} ${risk.get('risk_per_share', 0):.2f}\n\n")
                f.write(f"{'='*80}\n\n")

                # --- Detailed Timeframe Analysis ---
                timeframes = self.extractor.get_timeframes(ticker)
                for tf in timeframes:
                    f.write(f"{'-'*80}\n")
                    f.write(f"--- TIMEFRAME ANALYSIS: {tf.upper()} ---\n\n")

                    # --- Conventional Analysis ---
                    f.write("  Conventional Analysis:\n")
                    trend = self.extractor.get_trend_analysis(ticker, tf)
                    f.write(self._format_dict_for_text(trend, "Trend Analysis"))
                    
                    candle = self.extractor.get_candle_analysis(ticker, tf)
                    f.write(self._format_dict_for_text(candle.get('last_candle_signal', {}), "Last Candle Signal"))
                    
                    sr = self.extractor.get_support_resistance(ticker, tf)
                    s_levels = [f"${lvl['price']:.2f}" for lvl in sr.get('support', [])]
                    r_levels = [f"${lvl['price']:.2f}" for lvl in sr.get('resistance', [])]
                    f.write(f"    - Support:    {', '.join(s_levels) or 'None'}\n")
                    f.write(f"    - Resistance: {', '.join(r_levels) or 'None'}\n\n")

                    pattern = self.extractor.get_pattern_analysis(ticker, tf)
                    if not pattern:
                        f.write("    - Patterns:   None Detected\n")
                    else:
                        f.write("    - Pattern Analysis:\n")
                        for p_name, p_data in pattern.items():
                            f.write(f"      - {p_name.replace('_', ' ').title()}:\n")
                            if isinstance(p_data, dict):
                                for key, val in p_data.items():
                                    if key == "tests" and isinstance(val, list) and val:
                                        f.write(f"        - {str(key).ljust(15)}:\n")
                                        for test in val:
                                            test_type = test.get('type', 'N/A')
                                            index = test.get('index')
                                            if hasattr(index, 'strftime'):
                                                date_str = index.strftime('%Y-%m-%d')
                                            else:
                                                date_str = str(index)
                                            price = test.get('price', '')
                                            try:
                                                price_str = f"${float(price):.2f}"
                                            except Exception:
                                                price_str = str(price)
                                            f.write(f"            • {test_type.ljust(16)} Date: {date_str}  Price: {price_str}\n")
                                    else:
                                        f.write(f"        - {str(key).ljust(15)}: {val}\n")
                        f.write("\n")

                    # --- Wyckoff Analysis ---
                    f.write("  Wyckoff Analysis:\n")
                    wyckoff_phases = self.extractor.get_wyckoff_phases(ticker, tf)
                    wyckoff_events = self.extractor.get_wyckoff_events(ticker, tf)
                    wyckoff_ranges = self.extractor.get_wyckoff_trading_ranges(ticker, tf)
                    wyckoff_annotated = self.extractor.get_wyckoff_annotated_data(ticker, tf)

                    if not any([wyckoff_phases, wyckoff_events, wyckoff_ranges]) and wyckoff_annotated.empty:
                        f.write("    No significant Wyckoff structures detected on this timeframe.\n\n")
                        continue
                    
                    if wyckoff_phases:
                        f.write(f"    - Current Phase: {wyckoff_phases[-1].get('phase', 'N/A')}\n")
                    
                    if wyckoff_ranges:
                        f.write("    - Trading Ranges:\n")
                        for i, wr in enumerate(wyckoff_ranges):
                            start = pd.to_datetime(wr.get('start_timestamp')).strftime('%Y-%m-%d')
                            end = pd.to_datetime(wr.get('end_timestamp')).strftime('%Y-%m-%d') if wr.get('end_timestamp') else 'Ongoing'
                            f.write(f"      - Range {i+1} ({wr.get('context', 'N/A')}): {start} to {end} | Support: ${wr.get('support', 0):.2f}, Resistance: ${wr.get('resistance', 0):.2f}\n")
                    
                    if wyckoff_events:
                        f.write("    - Recent Key Events (up to last 10):\n")
                        for event in wyckoff_events[-10:]:
                            ts = pd.to_datetime(event.get('timestamp')).strftime('%Y-%m-%d %H:%M')
                            event_name = event.get('event_name', 'N/A').ljust(15)
                            price = event.get('price', 0)
                            volume = event.get('volume', 0)
                            f.write(f"      - {ts}: {event_name} @ ${price:<8.2f} (Vol: {volume:,.0f})\n")
                    
                    # --- Wyckoff Annotated Data Summary ---
                    if not wyckoff_annotated.empty:
                        f.write("    - Annotated Chart Data:\n")
                        f.write(f"      - Data Points: {len(wyckoff_annotated):,} rows\n")
                        f.write(f"      - Date Range: {wyckoff_annotated.index[0].strftime('%Y-%m-%d')} to {wyckoff_annotated.index[-1].strftime('%Y-%m-%d')}\n")
                        
                        # Show available annotation columns (excluding basic OHLCV)
                        basic_cols = {'open', 'high', 'low', 'close', 'volume'}
                        annotation_cols = [col for col in wyckoff_annotated.columns if col.lower() not in basic_cols]
                        if annotation_cols:
                            f.write(f"      - Annotation Columns: {', '.join(annotation_cols)}\n")
                        
                        # Show some statistics about annotations
                        for col in annotation_cols[:5]:  # Limit to first 5 annotation columns
                            if wyckoff_annotated[col].dtype == 'object':
                                unique_values = wyckoff_annotated[col].dropna().unique()
                                if len(unique_values) <= 10:  # Only show if reasonable number of unique values
                                    f.write(f"        - {col}: {', '.join(str(v) for v in unique_values[:5])}\n")
                            elif pd.api.types.is_numeric_dtype(wyckoff_annotated[col]):
                                non_null_count = wyckoff_annotated[col].count()
                                if non_null_count > 0:
                                    f.write(f"        - {col}: {non_null_count:,} annotated points\n")
                    
                    f.write("\n")

                f.write(f"\n{'='*80}\nEnd of Report\n{'='*80}\n")
            self.logger.info(f"Detailed summary report saved to {report_path}")
            return True
        except Exception as e:
            self.logger.error(f"Error creating summary report for {ticker}: {e}", exc_info=True)
            return False

    def _prepare_data_for_json(self, data: Any) -> Any:
        """Recursively prepares data for clean JSON serialization."""
        if isinstance(data, dict):
            return {key: self._prepare_data_for_json(value) for key, value in data.items()}
        if isinstance(data, list):
            return [self._prepare_data_for_json(item) for item in data]
        if isinstance(data, pd.DataFrame):
            if data.empty:
                return None
            # Convert the DataFrame to a dict, then recursively call this same
            # function on the result. This is crucial to handle non-serializable
            # values within the DataFrame (like NaN) and convert them to None (JSON null).
            df_as_dict = data.to_dict(orient='split')
            return self._prepare_data_for_json(df_as_dict)
        if isinstance(data, pd.Timestamp):
            return data.isoformat()
        if pd.isna(data):
            return None
        # Handle numpy numeric types just in case, converting them to native Python types
        if hasattr(data, 'item'):
            if pd.api.types.is_integer(data):
                return int(data)
            if pd.api.types.is_float(data):
                return float(data)
        return data

    def create_json_report(self, ticker: str) -> bool:
        """
        Export the full extracted analysis for a ticker as a clean JSON file.
        """
        try:
            current_date = datetime.now().strftime("%Y-%m-%d")
            sanitized_ticker = sanitize_filename(ticker)
            report_path = self.output_dir / f"{current_date}_{sanitized_ticker}_report.json"
            self.logger.info(f"Generating JSON report for {sanitized_ticker} at {report_path}")

            ticker_data = self.extractor.get_ticker_data(ticker)
            serializable_data = self._prepare_data_for_json(ticker_data)
            
            with open(report_path, "w", encoding="utf-8") as f:
                json.dump(serializable_data, f, indent=2, default=str)
            
            self.logger.info(f"JSON report saved to {report_path}")
            return True
        except Exception as e:
            self.logger.error(f"Error generating JSON report for {ticker}: {e}", exc_info=True)
            return False

    def create_html_report(self, ticker: str) -> bool:
        """
        Generate a human-readable HTML report with detailed tables.
        """
        try:
            current_date = datetime.now().strftime("%Y-%m-%d")
            sanitized_ticker = sanitize_filename(ticker)
            report_path = self.output_dir / f"{current_date}_{sanitized_ticker}_report.html"
            self.logger.info(f"Generating HTML report for {sanitized_ticker} at {report_path}")

            signal = self.extractor.get_signal(ticker)
            risk = self.extractor.get_risk_assessment(ticker)
            current_price = self.extractor.get_current_price(ticker)
            timeframes = self.extractor.get_timeframes(ticker)

            html = f"""
            <html><head><title>Marketflow Report for {ticker}</title><style>
            body {{ font-family: 'Segoe UI', Arial, sans-serif; margin: 2em; background-color: #f4f7f6; color: #333; }}
            h1, h2, h3 {{ color: #2c3e50; }} h1 {{ font-size: 2.5em; }} h2 {{ border-bottom: 2px solid #3498db; padding-bottom: 10px; }}
            .container {{ max-width: 1200px; margin: auto; }} .section {{ background: #fff; padding: 20px; margin-bottom: 20px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }}
            table {{ border-collapse: collapse; width: 100%; margin-top: 15px; }} th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
            th {{ background-color: #3498db; color: white; }} tr:nth-child(even) {{ background-color: #f2f2f2; }}
            .signal-BUY {{ color: #27ae60; font-weight: bold; }} .signal-SELL {{ color: #c0392b; font-weight: bold; }}
            .strength-STRONG {{ font-weight: bold; }}
            </style></head><body><div class="container">
            <h1>Marketflow Analysis Report for: {ticker}</h1>
            <div class="section"><h2>Overall Assessment</h2><table>
                <tr><th>Signal Type</th><td class="signal-{signal.get('type','')}">{signal.get('type', 'N/A')}</td></tr>
                <tr><th>Signal Strength</th><td class="strength-{signal.get('strength','')}">{signal.get('strength', 'N/A')}</td></tr>
                <tr><th>Details</th><td>{signal.get('details', 'N/A')}</td></tr>
                <tr><th>Current Price</th><td>${current_price:.2f}</td></tr>
                <tr><th>Stop Loss</th><td>${risk.get('stop_loss', 0):.2f}</td></tr>
                <tr><th>Take Profit</th><td>${risk.get('take_profit', 0):.2f}</td></tr>
                <tr><th>Risk/Reward Ratio</th><td>{risk.get('risk_reward_ratio', 0):.2f}</td></tr>
                <tr><th>Position Size</th><td>{risk.get('position_size', 0):.2f}</td></tr>
                <tr><th>Risk Per Share</th><td>${risk.get('risk_per_share', 0):.2f}</td></tr>
            </table></div>
            <div class="section"><h2>Detailed Timeframe Analysis</h2>
            </table></div>"""

            for tf in timeframes:
                html += f"<div class='section'><h2>Timeframe Analysis: {tf.upper()}</h2>"
                
                # Conventional Analysis Table
                trend = self.extractor.get_trend_analysis(ticker, tf)
                candle = self.extractor.get_candle_analysis(ticker, tf)
                sr = self.extractor.get_support_resistance(ticker, tf)
                html += "<h3>Conventional Analysis</h3><table>"
                html += f"<tr><th>Trend Direction</th><td>{trend.get('trend_direction', 'N/A')} (Strength: {trend.get('trend_strength', 'N/A')})</td></tr>"
                html += f"<tr><th>Last Candle Signal</th><td>{candle.get('last_candle_signal', {}).get('Name', 'None')}</td></tr>"
                html += f"<tr><th>Support</th><td>{', '.join(f'${lvl['price']:.2f}' for lvl in sr.get('support', [])) or 'None'}</td></tr>"
                html += f"<tr><th>Resistance</th><td>{', '.join(f'${lvl['price']:.2f}' for lvl in sr.get('resistance', [])) or 'None'}</td></tr>"
                html += "</table>"

                # Pattern Analysis Table
                pattern = self.extractor.get_pattern_analysis(ticker, tf)
                if pattern:
                    html += "<h4>Pattern Analysis</h4><table><tr><th>Pattern</th><th>Details</th></tr>"
                    for p_name, p_data in pattern.items():
                        details_lines = []
                        for k, v in p_data.items():
                            if k == "tests" and isinstance(v, list):
                                # Render tests as a sub-table for readability
                                if v:
                                    test_table = "<table style='margin:5px 0; border:1px solid #ccc;'><tr><th>Type</th><th>Date</th><th>Price</th></tr>"
                                    for test in v:
                                        test_type = test.get('type', 'N/A')
                                        # Format timestamp and price
                                        index = test.get('index')
                                        if hasattr(index, 'strftime'):
                                            date_str = index.strftime('%Y-%m-%d')
                                        else:
                                            date_str = str(index)
                                        price = test.get('price', '')
                                        try:
                                            price_str = f"${float(price):.2f}"
                                        except Exception:
                                            price_str = str(price)
                                        test_table += f"<tr><td>{test_type}</td><td>{date_str}</td><td>{price_str}</td></tr>"
                                    test_table += "</table>"
                                    details_lines.append(f"Tests:<br>{test_table}")
                                else:
                                    details_lines.append("Tests: None")
                            else:
                                details_lines.append(f"{k}: {v}")
                        details_str = '<br>'.join(details_lines)
                        html += f"<tr><td>{p_name.replace('_', ' ').title()}</td><td>{details_str}</td></tr>"
                    html += "</table>"

                # Wyckoff Analysis
                html += "<h3>Wyckoff Analysis</h3>"
                wyckoff_phases = self.extractor.get_wyckoff_phases(ticker, tf)
                wyckoff_events = self.extractor.get_wyckoff_events(ticker, tf)
                wyckoff_ranges = self.extractor.get_wyckoff_trading_ranges(ticker, tf)
                wyckoff_annotated = self.extractor.get_wyckoff_annotated_data(ticker, tf)

                if not any([wyckoff_phases, wyckoff_events, wyckoff_ranges]) and wyckoff_annotated.empty:
                    html += "<p>No significant Wyckoff structures detected.</p>"
                else:
                    if wyckoff_phases:
                        html += f"<p><strong>Current Phase:</strong> {wyckoff_phases[-1].get('phase', 'N/A')}</p>"
                    
                    if wyckoff_ranges:
                        html += "<h4>Trading Ranges</h4><table><tr><th>Context</th><th>Duration</th><th>Support</th><th>Resistance</th></tr>"
                        for wr in wyckoff_ranges:
                            start = pd.to_datetime(wr.get('start_timestamp')).strftime('%Y-%m-%d')
                            end = pd.to_datetime(wr.get('end_timestamp')).strftime('%Y-%m-%d') if wr.get('end_timestamp') else 'Ongoing'
                            html += f"<tr><td>{wr.get('context', 'N/A')}</td><td>{start} to {end}</td><td>${wr.get('support', 0):.2f}</td><td>${wr.get('resistance', 0):.2f}</td></tr>"
                        html += "</table>"

                    if wyckoff_events:
                        html += "<h4>Recent Key Events</h4><table><tr><th>Timestamp</th><th>Event</th><th>Price</th><th>Volume</th></tr>"
                        for event in wyckoff_events[-10:]:
                            ts = pd.to_datetime(event.get('timestamp')).strftime('%Y-%m-%d %H:%M')
                            html += f"<tr><td>{ts}</td><td>{event.get('event_name', 'N/A')}</td><td>${event.get('price', 0):.2f}</td><td>{event.get('volume', 0):,}</td></tr>"
                        html += "</table>"
                    
                    # --- Wyckoff Annotated Data Section ---
                    if not wyckoff_annotated.empty:
                        html += "<h4>Annotated Chart Data</h4>"
                        html += f"<p><strong>Data Points:</strong> {len(wyckoff_annotated):,} rows</p>"
                        html += f"<p><strong>Date Range:</strong> {wyckoff_annotated.index[0].strftime('%Y-%m-%d')} to {wyckoff_annotated.index[-1].strftime('%Y-%m-%d')}</p>"
                        
                        # Show available annotation columns
                        basic_cols = {'open', 'high', 'low', 'close', 'volume'}
                        annotation_cols = [col for col in wyckoff_annotated.columns if col.lower() not in basic_cols]
                        if annotation_cols:
                            html += f"<p><strong>Annotation Columns:</strong> {', '.join(annotation_cols)}</p>"
                            
                            # Create a summary table for annotation statistics
                            html += "<h5>Annotation Summary</h5><table><tr><th>Column</th><th>Type</th><th>Summary</th></tr>"
                            for col in annotation_cols[:10]:  # Limit to first 10 columns
                                col_type = str(wyckoff_annotated[col].dtype)
                                if wyckoff_annotated[col].dtype == 'object':
                                    unique_values = wyckoff_annotated[col].dropna().unique()
                                    if len(unique_values) <= 10:
                                        summary = f"Values: {', '.join(str(v) for v in unique_values[:5])}"
                                        if len(unique_values) > 5:
                                            summary += f" (+{len(unique_values)-5} more)"
                                    else:
                                        summary = f"{len(unique_values)} unique values"
                                elif pd.api.types.is_numeric_dtype(wyckoff_annotated[col]):
                                    non_null_count = wyckoff_annotated[col].count()
                                    if non_null_count > 0:
                                        summary = f"{non_null_count:,} annotated points"
                                    else:
                                        summary = "No data"
                                else:
                                    summary = f"{wyckoff_annotated[col].count():,} non-null values"
                                
                                html += f"<tr><td>{col}</td><td>{col_type}</td><td>{summary}</td></tr>"
                            html += "</table>"
                html += "</div>"

            html += "</div></body></html>"
            with open(report_path, "w", encoding="utf-8") as f:
                f.write(html)
            self.logger.info(f"HTML report saved to {report_path}")
            return True
        except Exception as e:
            self.logger.error(f"Error generating HTML report for {ticker}: {e}", exc_info=True)
            return False
        
    def export_wyckoff_annotated_data(self, ticker: str, timeframe: str, format: str = 'csv') -> bool:
        """
        Export Wyckoff annotated data to CSV or JSON format.
        
        Args:
            ticker: Stock symbol
            timeframe: Timeframe to export data for
            format: Export format ('csv' or 'json')
        
        Returns:
            bool: True if export successful, False otherwise
        """
        try:
            wyckoff_annotated = self.extractor.get_wyckoff_annotated_data(ticker, timeframe)
            
            if wyckoff_annotated.empty:
                self.logger.warning(f"No Wyckoff annotated data available for {ticker}-{timeframe}")
                return False
            
            # Sanitize the ticker HERE, just for the filename.
            sanitized_ticker = sanitize_filename(ticker)
            current_date = datetime.now().strftime("%Y-%m-%d")
            if format.lower() == 'csv':
                export_path = self.output_dir / f"{current_date}_{sanitized_ticker}_{timeframe}_wyckoff_annotated.csv"
                wyckoff_annotated.to_csv(export_path, index=True)
                self.logger.info(f"Wyckoff annotated data exported to CSV: {export_path}")
            elif format.lower() == 'json':
                # Use the sanitized_ticker for the path.
                export_path = self.output_dir / f"{current_date}_{sanitized_ticker}_{timeframe}_wyckoff_annotated.json"
                json_data = wyckoff_annotated.to_json(orient='index', date_format='iso', indent=2)
                with open(export_path, 'w', encoding='utf-8') as f:
                    f.write(json_data)
                self.logger.info(f"Wyckoff annotated data exported to JSON: {export_path}")
            else:
                raise ValueError(f"Unsupported format: {format}. Use 'csv' or 'json'.")
            
            return True
        except Exception as e:
            self.logger.error(f"Error exporting Wyckoff annotated data for {ticker}-{timeframe}: {e}", exc_info=True)
            return False

    def export_all_wyckoff_annotated_data(self, ticker: str, format: str = 'csv') -> Dict[str, bool]:
        """
        Export Wyckoff annotated data for all available timeframes of a ticker.
        
        Args:
            ticker: Stock symbol
            format: Export format ('csv' or 'json')
        
        Returns:
            Dict[str, bool]: Dictionary with timeframe as key and success status as value
        """
        timeframes = self.extractor.get_timeframes(ticker)
        results = {}
        
        for tf in timeframes:
            results[tf] = self.export_wyckoff_annotated_data(ticker, tf, format)

        self.logger.info(f"Wyckoff annotated data export completed for {ticker}. Results: {results}")
        return results
        
    def generate_all_reports_for_ticker(self, ticker: str, include_wyckoff_export: bool = True) -> Dict[str, bool]:
        """
        A convenient method to generate all reports for a single ticker.
        
        Args:
            ticker: Stock symbol
            include_wyckoff_export: Whether to export Wyckoff annotated data as CSV files
        
        Returns:
            Dict[str, bool]: A dictionary with the success status of each report type.
        """
        if not self.extractor.get_ticker_data(ticker):
            self.logger.error(f"No data found for ticker {ticker}. Cannot generate reports.")
            return {"error": True, "reason": f"No data available for {ticker}"}
            
        self.logger.info(f"--- Generating all reports for {ticker} ---")
        
        results = {
            "summary": self.create_summary_report(ticker),
            "json": self.create_json_report(ticker),
            "html": self.create_html_report(ticker)
        }
        
        # Optionally export Wyckoff annotated data
        if include_wyckoff_export:
            wyckoff_export_results = self.export_all_wyckoff_annotated_data(ticker, format='csv')
            results['wyckoff_annotated_exports'] = wyckoff_export_results
        
        self.logger.info(f"--- Finished generating reports for {ticker} ---")
        self.logger.info(f"Report Generation Status for {ticker}: {results}")
        return results