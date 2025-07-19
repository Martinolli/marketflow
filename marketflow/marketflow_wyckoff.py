"""
This module implements the Wyckoff Method for market analysis.
It detects Wyckoff events and phases based on price and volume data.
"""

# Import necessary libraries
import pandas as pd
from typing import Any, Dict, List, Optional

# Import custom modules
from marketflow.marketflow_logger import get_logger
from marketflow.marketflow_config_manager import create_app_config
from marketflow.marketflow_data_parameters import MarketFlowDataParameters
from marketflow.enums import WyckoffEvent, WyckoffPhase, MarketContext
# Define the WyckoffAnalyzer class

class WyckoffAnalyzer:
    def __init__(self, processed_data: Dict[str, Any], parameters=None):

        """
        Initialize the analyzer.
        All arguments should be outputs of their respective VPA modules.
        """
        # Validate processed_data format
        if not isinstance(processed_data, dict) or 'price' not in processed_data or 'volume' not in processed_data:
            raise ValueError("Invalid processed_data format")
        
        # Initialize logger
        self.logger = get_logger(module_name="WyckoffAnalyzer")

        # Create configuration manager for API keys and settings
        self.config_manager = create_app_config(self.logger)
        
        # Load parameters or use default MarketFlowDataParameters
        if parameters is None:
            self.logger.info("Using default MarketFlowDataParameters.")
        else:
            self.logger.info("Using provided MarketFlowDataParameters.")
        self.parameters = parameters or MarketFlowDataParameters()
        
        # Load Wyckoff parameters from the configuration
        self.vol_lookback = self.parameters.get_wyckoff_parameter('vol_lookback', 20)
        self.range_lookback = self.parameters.get_wyckoff_parameter('range_lookback', 20)
        
        # Climax event multipliers
        self.climax_vol_multiplier = self.parameters.get_wyckoff_parameter('climax_vol_multiplier', 2.0)
        self.climax_range_multiplier = self.parameters.get_wyckoff_parameter('climax_range_multiplier', 1.8)
        
        # SOS/SOW event multipliers
        self.breakout_vol_multiplier = self.parameters.get_wyckoff_parameter('breakout_vol_multiplier', 1.5)
        self.breakout_range_multiplier = self.parameters.get_wyckoff_parameter('breakout_range_multiplier', 1.2)
        
        # General parameters
        self.swing_point_n = self.parameters.get_wyckoff_parameter('swing_point_n', 5)
        self.tr_max_duration = self.parameters.get_wyckoff_parameter('tr_max_duration', 50) # Max bars in a TR

        self.logger.debug(
            f"WyckoffAnalyzer parameters: "
            f"vol_lookback={self.vol_lookback}, "
            f"range_lookback={self.range_lookback}, "
            f"climax_vol_multiplier={self.climax_vol_multiplier}, "
            f"climax_range_multiplier={self.climax_range_multiplier}, "
            f"breakout_vol_multiplier={self.breakout_vol_multiplier}, "
            f"breakout_range_multiplier={self.breakout_range_multiplier}, "
            f"swing_point_n={self.swing_point_n}, "
            f"tr_max_duration={self.tr_max_duration}"
        )


        price_df = processed_data.get("price")
        volume_series = processed_data.get("volume")
        self.logger.debug(f"Loaded price_df with shape: {None if price_df is None else price_df.shape}")
        self.logger.debug(f"Loaded volume_series with length: {None if volume_series is None else len(volume_series)}")

        if price_df is None or price_df.empty:
            self.logger.error("Price data is required for Wyckoff analysis.")
            raise ValueError("Price data is required for Wyckoff analysis.")

        if volume_series is None or volume_series.empty:
            self.logger.error("Volume data is required for Wyckoff analysis.")
            raise ValueError("Volume data is required for Wyckoff analysis.")

        self.price_data = price_df.copy()
        self.price_data['volume'] = volume_series

        self.events = []
        self.phases = []
        self.trading_ranges = []

    def run_analysis(self):
        """Runs the full Wyckoff analysis."""        
        self.logger.info("Running full Wyckoff analysis.")
        try:
            events = self.detect_events()
            self.logger.info(f"Detected {len(events)} Wyckoff events.")
            phases = self.detect_phases()
            self.logger.info(f"Detected {len(phases)} Wyckoff phases.")
            self.logger.info(f"Identified {len(self.trading_ranges)} trading ranges.")
            return phases, events, self.trading_ranges
        except Exception as e:
            self.logger.error(f"Error during Wyckoff analysis: {e}", exc_info=True)
            raise

    def _find_swing_points(self, data: pd.DataFrame, n: int) -> (List):
        """
        Identifies swing high and low points in the price data.
        A swing high is a candle that has a higher high than the `n` candles before and after it.
        A swing low is a candle that has a lower low than the `n` candles before and after it.
        """
        self.logger.info(f"Finding swing points with window size n={n} on {len(data)} bars.")
        highs = []
        lows = []
        # Use .iloc for performance and to avoid index alignment issues
        high_series = data['high'].values
        low_series = data['low'].values
        
        for i in range(n, len(data) - n):
            # Check for swing high
            is_high = high_series[i] >= max(high_series[i-n:i]) and \
                      high_series[i] > max(high_series[i+1:i+n+1])
            if is_high:
                highs.append(data.index[i])
                self.logger.debug(f"Swing high found at index {i} ({data.index[i]}) with high={high_series[i]}")

            # Check for swing low
            is_low = low_series[i] <= min(low_series[i-n:i]) and \
                     low_series[i] < min(low_series[i+1:i+n+1])
            if is_low:
                lows.append(data.index[i])
                self.logger.debug(f"Swing low found at index {i} ({data.index[i]}) with low={low_series[i]}")
        self.logger.info(f"Found {len(highs)} swing highs and {len(lows)} swing lows.")
        return highs, lows

## --- CHANGE START --- ##
    # DOC: New method to calculate quantitative market dynamics.
    # REASON: To translate the mathematical tools (Volume Spikes, Range Spikes, Divergence)
    # into concrete variables, making the event detection logic more robust and quantitative.
    
    def _calculate_market_dynamics(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Appends columns for quantitative analysis to the DataFrame.
        - volume_spike_ratio: Ratio of current volume to its moving average.
        - range_spike_ratio: Ratio of current bar range to its moving average.
        - pv_divergence: Flag for Price-Volume divergence.
        """
        self.logger.info("Calculating market dynamics (spikes and divergences).")
        df['rolling_vol'] = df['volume'].rolling(window=self.vol_lookback).mean()
        df['range'] = df['high'] - df['low']
        df['rolling_range_avg'] = df['range'].rolling(window=self.range_lookback).mean()

        # Calculate Spike Ratios, handling potential division by zero
        df['volume_spike_ratio'] = (df['volume'] / df['rolling_vol']).fillna(1.0)
        df['range_spike_ratio'] = (df['range'] / df['rolling_range_avg']).fillna(1.0)

        # Calculate Price-Volume Divergence
        # 1 = Bullish Divergence (lower low in price, lower volume)
        # -1 = Bearish Divergence (higher high in price, lower volume)
        # 0 = No divergence
        df['pv_divergence'] = 0
        
        # Get the index of the min/max in the lookback window to compare against
        df['vol_at_min_low'] = df['volume'].rolling(window=self.swing_point_n).apply(lambda x: x[df['low'][x.index].idxmin()], raw=False)
        df['vol_at_max_high'] = df['volume'].rolling(window=self.swing_point_n).apply(lambda x: x[df['high'][x.index].idxmax()], raw=False)

        # Conditions for divergence
        is_new_low = df['low'] < df['low'].rolling(window=self.swing_point_n).min().shift(1)
        is_lower_vol = df['volume'] < df['vol_at_min_low'].shift(1)
        df.loc[is_new_low & is_lower_vol, 'pv_divergence'] = 1
        
        is_new_high = df['high'] > df['high'].rolling(window=self.swing_point_n).max().shift(1)
        is_lower_vol_at_high = df['volume'] < df['vol_at_max_high'].shift(1)
        df.loc[is_new_high & is_lower_vol_at_high, 'pv_divergence'] = -1
        
        df.drop(columns=['vol_at_min_low', 'vol_at_max_high'], inplace=True)

        # Log the first few rows of the calculated metrics for debugging
        preview = df[['volume_spike_ratio', 'range_spike_ratio', 'pv_divergence']].head(10).to_string()
        self.logger.debug(f"Market dynamics preview:\n{preview}")

        return df
        ## --- CHANGE END --- ##

    ## --- CHANGE START --- ##
    # DOC: Major refactor of detect_events to support both Accumulation and Distribution.
    # REASON: This was the most critical improvement requested. The function now uses
    # a MarketContext state machine to look for either a Selling Climax or a Buying Climax
    # as the starting point, then applies the correct logic for the detected context.
    def detect_events(self) -> List[Dict[str, Any]]:
        """
        Identify Wyckoff events using a dual-logic state machine for Accumulation and Distribution.
        """
        print("Starting Wyckoff event detection.")
        df = self.price_data.copy()
        min_data_len = self.vol_lookback + self.swing_point_n
        if len(df) < min_data_len:
            self.logger.warning(f"Price data is too short ({len(df)} bars) for Wyckoff analysis. Need at least {min_data_len} bars.")
            return []

        for col in ['open', 'high', 'low', 'close', 'volume']:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        df.dropna(subset=['open', 'high', 'low', 'close', 'volume'], inplace=True)
        if df.empty:
            self.logger.warning("DataFrame is empty after cleaning price/volume columns.")
            return []

        self.logger.info(f"Detecting Wyckoff events on {len(df)} bars of data.")

        ## --- CHANGE START --- ##
        # DOC: Call the new method to prepare the DataFrame with quantitative metrics.
        # REASON: This integrates our mathematical tools directly into the analysis pipeline.
        df = self._calculate_market_dynamics(df)
        ## --- CHANGE END --- ##

        swing_highs, swing_lows = self._find_swing_points(df, n=self.swing_point_n)
        events = []
        added_events = {}

        def add_event(label: WyckoffEvent, idx: int, details: Optional[Dict] = None):
            timestamp = df.index[idx]
            if (timestamp, label.name) in added_events: return
            
            event_data = {
                "event": label.value, "event_name": label.name,
                "timestamp": timestamp, "price": float(df['close'].iloc[idx]),
                "volume": float(df['volume'].iloc[idx])
            }
            if details: event_data.update(details) # Add extra info like Spring Type
            
            events.append(event_data)
            added_events[(timestamp, label.name)] = True
            self.logger.debug(f"Detected {label.name} at {timestamp} with details: {details or {}}")

        # --- State Machine for Event Detection ---
        market_context = MarketContext.UNDEFINED
        trading_range = None
        last_climax_idx = None
        last_reaction_idx = None # For AR or AUTO_REACTION
        last_breakout_idx = None

        for i in range(self.vol_lookback, len(df)):
            current_row = df.iloc[i]

            if market_context == MarketContext.UNDEFINED:
                ## --- CHANGE START --- ##
                # DOC: Integrated new metrics into Climax detection logic.
                # REASON: Using volume_spike_ratio and range_spike_ratio makes the
                # conditions more meaningful and directly models the "big player" signature.
                is_sc_candidate = (
                    current_row['volume_spike_ratio'] > self.climax_vol_multiplier and
                    current_row['range_spike_ratio'] > self.climax_range_multiplier and
                    current_row['close'] <= df['low'].iloc[i-self.vol_lookback:i].min()
                )
                if is_sc_candidate:
                    market_context = MarketContext.ACCUMULATION
                    add_event(WyckoffEvent.SC, i, {"vol_spike": f"{current_row['volume_spike_ratio']:.1f}x"})
                    last_climax_idx = i
                    continue

                is_bc_candidate = (
                    current_row['volume_spike_ratio'] > self.climax_vol_multiplier and
                    current_row['range_spike_ratio'] > self.climax_range_multiplier and
                    current_row['close'] >= df['high'].iloc[i-self.vol_lookback:i].max()
                )
                if is_bc_candidate:
                    market_context = MarketContext.DISTRIBUTION
                    # A Buying Climax is even more significant if it occurs on bearish divergence
                    has_divergence = current_row['pv_divergence'] == -1
                    add_event(WyckoffEvent.BC, i, {"vol_spike": f"{current_row['volume_spike_ratio']:.1f}x", "bearish_divergence": has_divergence})
                    last_climax_idx = i
                    continue
            
            # --- 2. TRADING RANGE DEFINITION: After a climax, find the reaction to define the TR ---
            if last_climax_idx is not None and trading_range is None:
                if market_context == MarketContext.ACCUMULATION:
                    potential_ar_highs = [h for h in swing_highs if h > df.index[last_climax_idx]]
                    if potential_ar_highs:
                        ar_timestamp = potential_ar_highs[0]
                        ar_idx = df.index.get_loc(ar_timestamp)
                        if ar_idx > last_climax_idx and ar_idx - last_climax_idx < self.tr_max_duration:
                            add_event(WyckoffEvent.AR, ar_idx)
                            last_reaction_idx = ar_idx
                            trading_range = {'support': df['low'].iloc[last_climax_idx], 'resistance': df['high'].iloc[ar_idx]}
                            self.logger.info(f"Accumulation TR defined. Support: {trading_range['support']:.2f}, Resistance: {trading_range['resistance']:.2f}")
                
                elif market_context == MarketContext.DISTRIBUTION:
                    potential_ar_lows = [l for l in swing_lows if l > df.index[last_climax_idx]]
                    if potential_ar_lows:
                        ar_timestamp = potential_ar_lows[0]
                        ar_idx = df.index.get_loc(ar_timestamp)
                        if ar_idx > last_climax_idx and ar_idx - last_climax_idx < self.tr_max_duration:
                            add_event(WyckoffEvent.AUTO_REACTION, ar_idx)
                            last_reaction_idx = ar_idx
                            trading_range = {'support': df['low'].iloc[ar_idx], 'resistance': df['high'].iloc[last_climax_idx]}
                            self.logger.info(f"Distribution TR defined. Support: {trading_range['support']:.2f}, Resistance: {trading_range['resistance']:.2f}")
                
                if trading_range: # If a TR was just defined
                    tr_full = trading_range.copy()
                    tr_full.update({
                        'start_idx': last_climax_idx, 'start_timestamp': df.index[last_climax_idx],
                        'end_idx': None, 'end_timestamp': None, 'context': market_context.value
                    })
                    self.trading_ranges.append(tr_full)

            # --- 3. IN-RANGE AND POST-RANGE ANALYSIS ---
            if trading_range is not None and last_reaction_idx is not None:
                support, resistance = trading_range['support'], trading_range['resistance']

                # --- ACCUMULATION CONTEXT ---
                if market_context == MarketContext.ACCUMULATION:
                    # Spring (Phase C Test)
                    if current_row['low'] < support and current_row['close'] > support:
                        # DOC: Added nuanced Spring classification as requested.
                        spring_type = 'Type 3 (High Quality - Low Vol)'
                        if current_row['volume_spike_ratio'] > self.breakout_vol_multiplier:
                            spring_type = 'Type 1 (Terminal Shakeout - High Vol)'
                        elif current_row['volume_spike_ratio'] > 1.0:
                            spring_type = 'Type 2 (Needs Test - Med Vol)'
                        add_event(WyckoffEvent.SPRING, i, {"subtype": spring_type, "description": "Low below support, close back above."})

                    # Sign of Strength / JAC (Phase D Breakout)
                    if current_row['close'] > resistance and current_row['volume_spike_ratio'] > self.breakout_vol_multiplier:
                        add_event(WyckoffEvent.SOS, i); add_event(WyckoffEvent.JAC, i)
                        last_breakout_idx = i; market_context = MarketContext.UNDEFINED

                    ## --- CHANGE START --- ##
                    # DOC: Used divergence metric to identify a high-quality Secondary Test.
                    # REASON: A test of a prior low is most significant if it programmatically
                    # shows bullish price-volume divergence, confirming supply exhaustion.
                    is_test_of_low = abs(current_row['low'] - df['low'].iloc[last_climax_idx]) / df['low'].iloc[last_climax_idx] < 0.03
                    if is_test_of_low and current_row['pv_divergence'] == 1:
                        add_event(WyckoffEvent.ST, i, {"description": "Successful test of SC low with bullish PV divergence."})
                    ## --- CHANGE END --- ##

                # --- DISTRIBUTION CONTEXT ---
                elif market_context == MarketContext.DISTRIBUTION:
                    # Upthrust After Distribution (UTAD - Phase C Test)
                    if current_row['high'] > resistance and current_row['close'] < resistance:
                        add_event(WyckoffEvent.UTAD, i, {"description": "High above resistance, close back below."})
                    
                    # Sign of Weakness (SOW - Phase D Breakdown)
                    if current_row['close'] < support and current_row['volume_spike_ratio'] > self.breakout_vol_multiplier:
                        add_event(WyckoffEvent.SOW, i)
                        last_breakout_idx = i; market_context = MarketContext.UNDEFINED
                

                # DOC: Added logic for post-breakout confirmation events (LPS/LPSY).
                # REASON: This was a key missing feature identified in the MD file review.
                # It looks for low-volume tests of the old TR boundaries.
                if last_breakout_idx:
                    if market_context == MarketContext.ACCUMULATION and i > last_breakout_idx: # Look for LPS
                        is_lps_candidate = (
                            current_row['low'] > resistance and # Holds above old resistance
                            abs(current_row['low'] - resistance) / resistance < 0.05 and # Close to old resistance
                            current_row['volume'] < df['rolling_vol'].iloc[i]
                        )
                        if is_lps_candidate:
                            add_event(WyckoffEvent.LPS, i, {"description": "Low-volume pullback to old resistance after breakout."})
                            last_breakout_idx = None # Reset

                    elif market_context == MarketContext.DISTRIBUTION and i > last_breakout_idx: # Look for LPSY
                        is_lpsy_candidate = (
                            current_row['high'] < support and # Fails to rally back to old support
                            abs(current_row['high'] - support) / support < 0.05 and # Close to old support
                            current_row['volume'] < df['rolling_vol'].iloc[i]
                        )
                        if is_lpsy_candidate:
                            add_event(WyckoffEvent.LPSY, i, {"description": "Low-volume rally to old support after breakdown."})
                            last_breakout_idx = None # Reset
                
                # If context was reset, end the current TR
                if market_context == MarketContext.UNDEFINED:
                    if self.trading_ranges and self.trading_ranges[-1]['end_idx'] is None:
                        self.trading_ranges[-1]['end_idx'] = i
                        self.trading_ranges[-1]['end_timestamp'] = current_row.name
                    trading_range = None; last_reaction_idx = None; last_climax_idx = None
        self.events = sorted(events, key=lambda x: x['timestamp'])
        print(f"Detected {len(self.events)} Wyckoff events.")
        self.logger.info(f"Detected {len(self.events)} Wyckoff events.")
        return self.events
    
    def detect_phases(self) -> List[Dict[str, Any]]: 
        """
        Classify Wyckoff phases based on the sequence of detected events.
        This logic is more stateful and context-aware than the original implementation.
        """
        print("Starting Wyckoff phase detection.")
        self.logger.info("Starting stateful Wyckoff phase detection.")
        if not self.events:
            self.logger.warning("No events detected, cannot determine phases.")
            return []

        phases_by_timestamp = {}
        current_phase = WyckoffPhase.UNKNOWN
        context = MarketContext.UNDEFINED

        # Accumulation-defining event sequences
        phase_a_acc_events = {WyckoffEvent.SC, WyckoffEvent.AR, WyckoffEvent.ST}
        phase_c_acc_events = {WyckoffEvent.SPRING, WyckoffEvent.TEST}
        phase_d_acc_events = {WyckoffEvent.SOS, WyckoffEvent.JAC, WyckoffEvent.LPS}

        # Distribution-defining event sequences
        phase_a_dist_events = {WyckoffEvent.BC, WyckoffEvent.AUTO_REACTION, WyckoffEvent.ST_DIST}
        phase_c_dist_events = {WyckoffEvent.UTAD, WyckoffEvent.UT}
        phase_d_dist_events = {WyckoffEvent.SOW, WyckoffEvent.LPSY}
        
        last_event_ts = self.price_data.index[0]

        for event_dict in self.events:
            ts = event_dict['timestamp']
            event = WyckoffEvent[event_dict['event_name']]
            self.logger.debug(f"Processing event {event.name} at {ts}")
            self.logger.info(f"Processing event {event.name} at {ts}")

            # --- Step 1: Fill the gap between the last event and this one ---
            # This uses the 'current_phase' from the *previous* iteration, which is correct.
            for date in self.price_data.loc[last_event_ts:ts].index:
                if date not in phases_by_timestamp:
                    phases_by_timestamp[date] = current_phase
                    self.logger.debug(f"Filling phase {current_phase.name} for timestamp {date}")
                    self.logger.info(f"Filling phase {current_phase.name} for timestamp {date}")

            # --- Step 2: Check for a context reset AFTER filling the gap ---
            # A new climax event implies the old pattern is over and a new one is beginning.
            if event in {WyckoffEvent.SC, WyckoffEvent.BC} and current_phase != WyckoffPhase.UNKNOWN:
                self.logger.info(f"*** CONTEXT RESET *** triggered by new climatic event {event.name} at {ts}. Restarting phase analysis.")
                current_phase = WyckoffPhase.UNKNOWN # Reset the state
                context = MarketContext.UNDEFINED     # Reset the context
            
            # --- Step 3: Run the state machine to determine the phase for the current event ---
            if current_phase == WyckoffPhase.UNKNOWN:
                if event in phase_a_acc_events:
                    current_phase = WyckoffPhase.A
                    context = MarketContext.ACCUMULATION
                    self.logger.info(f"Entering Phase A (Accumulation) at {ts} due to {event.name}")
                    self.logger.debug(f"Entering Phase A (Accumulation) at {ts} due to {event.name}")
                elif event in phase_a_dist_events:
                    current_phase = WyckoffPhase.A
                    context = MarketContext.DISTRIBUTION
                    self.logger.info(f"Entering Phase A (Distribution) at {ts} due to {event.name}")
                    self.logger.debug(f"Entering Phase A (Distribution) at {ts} due to {event.name}")
            
            # Transition from A to B
            elif current_phase == WyckoffPhase.A:
                # Prioritize a jump to D if a strong breakout/breakdown occurs
                if (context == MarketContext.ACCUMULATION and event in phase_d_acc_events) or \
                   (context == MarketContext.DISTRIBUTION and event in phase_d_dist_events):
                    current_phase = WyckoffPhase.D
                    self.logger.warning(f"Jumping from Phase A to D at {ts} due to strong event {event.name}. Phase B/C may have been brief or missed.")
                elif (context == MarketContext.ACCUMULATION and event == WyckoffEvent.ST) or \
                     (context == MarketContext.DISTRIBUTION and event == WyckoffEvent.ST_DIST):
                    current_phase = WyckoffPhase.B
                    self.logger.info(f"Transitioning to Phase B at {ts} due to {event.name}")

            
            # Transition from B to C
            elif current_phase == WyckoffPhase.B:
                # Prioritize a jump to D here as well
                if (context == MarketContext.ACCUMULATION and event in phase_d_acc_events) or \
                   (context == MarketContext.DISTRIBUTION and event in phase_d_dist_events):
                    current_phase = WyckoffPhase.D
                    self.logger.warning(f"Jumping from Phase B to D at {ts} due to strong event {event.name}. Phase C may have been brief or missed.")
                elif (context == MarketContext.ACCUMULATION and event in phase_c_acc_events) or \
                     (context == MarketContext.DISTRIBUTION and event in phase_c_dist_events):
                    current_phase = WyckoffPhase.C
                    self.logger.info(f"Transitioning to Phase C at {ts} due to {event.name}")
            
            # Transition from C to D
            elif current_phase == WyckoffPhase.C:
                if (context == MarketContext.ACCUMULATION and event in phase_d_acc_events) or \
                   (context == MarketContext.DISTRIBUTION and event in phase_d_dist_events):
                    current_phase = WyckoffPhase.D
                    self.logger.info(f"Transitioning to Phase D at {ts} due to {event.name}")
                    self.logger.debug(f"Transitioning to Phase D at {ts} due to {event.name}")

            # Phase D represents the start of the trend. It remains in Phase D upon
            # confirmation events like LPS/LPSY or further SOS/SOW. The transition to
            # Phase E is a condition (sustained trend), not a simple event trigger.
            # For this implementation, we will let the phase persist as D.
            elif current_phase == WyckoffPhase.D:
                 if (context == MarketContext.ACCUMULATION and event in phase_d_acc_events) or \
                   (context == MarketContext.DISTRIBUTION and event in phase_d_dist_events):
                    # DO NOTHING - Stay in Phase D. This event confirms the phase.
                    self.logger.info(f"Confirming Phase D at {ts} with event {event.name}")
                    self.logger.debug(f"Confirming Phase D at {ts} with event {event.name}")

            phases_by_timestamp[ts] = current_phase
            last_event_ts = ts
        
        # Fill in the phase for the remaining data after the last event
        for date in self.price_data.loc[last_event_ts:].index:
             phases_by_timestamp[date] = current_phase
        
        # Convert the dictionary to the required list format
        self.phases = [{'timestamp': ts, 'phase': p.value, 'phase_name': p.name} for ts, p in phases_by_timestamp.items()]
        self.logger.info(f"Wyckoff phase detection completed. {len(self.phases)} phase entries generated.")
        print(f"Detected {len(self.phases)} Wyckoff phases.")
        return self.phases
    ## --- CHANGE END --- ##

    def annotate_chart(self) -> pd.DataFrame:
        """
        Adds annotations (events and phases) to the price data.
        Returns a DataFrame with 'wyckoff_event' and 'wyckoff_phase' columns.
        """
        self.logger.info("Starting annotation of chart with Wyckoff events and phases.")
        annotated_df = self.price_data.copy()

        annotated_df["wyckoff_event"] = ""
        annotated_df["wyckoff_phase"] = ""
        ## --- CHANGE START --- ##
        # DOC: Added wyckoff_event_details column.
        # REASON: To store the nuanced event information (like Spring type) in the final output.
        annotated_df["wyckoff_event_details"] = ""
        ## --- CHANGE END --- ##

        for event_dict in self.events:
            idx = event_dict['timestamp']
            event_name = event_dict['event_name']
            if idx in annotated_df.index:
                current_val = annotated_df.at[idx, "wyckoff_event"]
                annotated_df.at[idx, "wyckoff_event"] = f"{current_val}, {event_name}".strip(", ")
                
                # Add event details if they exist
                details = {k: v for k, v in event_dict.items() if k not in ['event', 'event_name', 'timestamp', 'price', 'volume']}
                if details:
                    annotated_df.at[idx, "wyckoff_event_details"] = str(details)

        # Use the more granular phase data
        phase_series = pd.Series({p['timestamp']: p['phase_name'] for p in self.phases})
        annotated_df['wyckoff_phase'] = phase_series.reindex(annotated_df.index).ffill().fillna("UNKNOWN")

        self.logger.info("Annotation of chart completed.")
        return annotated_df