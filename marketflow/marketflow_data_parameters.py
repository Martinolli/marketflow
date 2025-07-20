"""
Marketflow Data Parameters Module Configuration Module

This module provides the configuration parameters for the Marketflow Data Parameters,

This module provides configuration management for the Marketflow algorithm.
"""
import json
from pathlib import Path
from marketflow.marketflow_logger import get_logger
from marketflow.marketflow_config_manager import create_app_config

class MarketFlowDataParameters:
    """Configuration Parameters for Marketflow analysis"""
    
    def __init__(self, config_file=None):

        # Initialize logger
        self.logger = get_logger(module_name="MarketflowDataParameters")

        # Create configuration manager for API keys and settings
        self.config_manager = create_app_config(self.logger)
    
        # Load configuration from file or use defaults
        self.config = self._load_config(config_file)
        # Initialize wyckoff_config from the loaded config
        self.wyckoff_config = self.config.get("wyckoff_config", {})

    def _load_config(self, config_file):
        """Load configuration from file or use defaults"""
        if config_file:
            import json
            try:
                with open(config_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading config file: {e}")
                print("Using default configuration instead.")
                return default_config
        return default_config
    
    def _validate_param(self, key, value):
        """Validate parameter updates, logging warnings for invalid values."""
        # Define validation rules for known parameters
        validation_rules = {
            # Volume thresholds
            "very_high_threshold": lambda v: isinstance(v, (float, int)) and v > 0,
            "high_threshold": lambda v: isinstance(v, (float, int)) and v > 0,
            "low_threshold": lambda v: isinstance(v, (float, int)) and v > 0,
            "very_low_threshold": lambda v: isinstance(v, (float, int)) and v > 0,
            "lookback_period": lambda v: isinstance(v, int) and v > 0,
            # Candle
            "wide_threshold": lambda v: isinstance(v, (float, int)) and v > 0,
            "narrow_threshold": lambda v: isinstance(v, (float, int)) and v > 0,
            "wick_threshold": lambda v: isinstance(v, (float, int)) and v > 0,
            # Trend
            "sideways_threshold": lambda v: isinstance(v, (float, int)) and v >= 0,
            "strong_trend_threshold": lambda v: isinstance(v, (float, int)) and v >= 0,
            "volume_change_threshold": lambda v: isinstance(v, (float, int)) and v >= 0,
            "min_trend_length": lambda v: isinstance(v, int) and v > 0,
            # Risk
            "default_stop_loss_percent": lambda v: isinstance(v, (float, int)) and 0 < v < 1,
            "default_take_profit_percent": lambda v: isinstance(v, (float, int)) and 0 < v < 1,
            "support_resistance_buffer": lambda v: isinstance(v, (float, int)) and 0 <= v < 1,
            "default_risk_percent": lambda v: isinstance(v, (float, int)) and 0 < v < 1,
            "default_risk_reward": lambda v: isinstance(v, (float, int)) and v >= 1,
            # Account
            "account_size": lambda v: isinstance(v, (float, int)) and v > 0,
            "risk_per_trade": lambda v: isinstance(v, (float, int)) and 0 < v < 1,
        }
        if key in validation_rules:
            if not validation_rules[key](value):
                self.logger.warning(f"Invalid value for parameter '{key}': {value}")
                return False
        return True

    def save_parameters(self, config_file=None) -> dict:
        """
        Save the current parameters to a JSON file.
        Uses the config manager path if not specified.
        """
        if not config_file:
            # Prefer first config manager path, fallback to default
            if self.config_manager.config_file_paths and self.config_manager.config_file_paths[0]:
                config_file = self.config_manager.config_file_paths[0]
            else:
                config_file = "marketflow_data_parameters.json"
        try:
            # Ensure any separate wyckoff_config is in sync
            self.config["wyckoff_config"] = self.wyckoff_config
            Path(config_file).parent.mkdir(parents=True, exist_ok=True)
            with open(config_file, "w") as f:
                json.dump(self.config, f, indent=4)
            self.logger.info(f"Parameters saved to {config_file}")
        except Exception as e:
            self.logger.error(f"Error saving parameters: {e}")

    def load_parameters(self, config_file=None) -> dict:
        """
        Load parameters from a JSON file.
        Uses the config manager path if not specified.
        """
        if not config_file:
            if self.config_manager.config_file_paths and self.config_manager.config_file_paths[0]:
                config_file = self.config_manager.config_file_paths[0]
            else:
                config_file = "marketflow_data_parameters.json"
        try:
            with open(config_file, "r") as f:
                self.config = json.load(f)
            self.wyckoff_config = self.config.get("wyckoff_config", {})
            self.logger.info(f"Parameters loaded from {config_file}")
        except Exception as e:
            self.logger.error(f"Error loading parameters: {e}")

    def get_volume_thresholds(self):
        """Get volume classification thresholds"""
        return self.config["volume"]
    
    def get_candle_thresholds(self):
        """Get candle classification thresholds"""
        return self.config["candle"]
    
    def get_trend_parameters(self):
        """Get trend analysis parameters"""
        return self.config["trend"]
    
    def get_pattern_parameters(self):
        """Get pattern recognition parameters"""
        return self.config["pattern"]
    
    def get_signal_parameters(self):
        """Get signal generation parameters"""
        return self.config["signal"]
    
    def get_risk_parameters(self):
        """Get risk assessment parameters"""
        return self.config["risk"]
    
    def get_timeframes(self):
        """Get default timeframes for analysis"""
        return self.config["timeframes"]
    
    def get_primary_timeframe(self):
        """Get primary timeframe for analysis"""
        if "timeframes" in self.config and self.config["timeframes"]:
            return self.config["timeframes"][0]["interval"]
        return "1d"  # Default to daily timeframe if none specified
    
    def get_all(self):
        """Get all configuration parameters"""
        return self.config
    
    def get_account_parameters(self):
        """Get account parameters"""
        return self.config.get("account", {})
    
    def get_wyckoff_parameter(self, param_name, default=None):
        """Get Wyckoff analysis parameters"""
        return self.wyckoff_config.get(param_name, default)

    def set_wyckoff_parameter(self, param_name, value):
        """Set Wyckoff analysis parameters"""
        self.wyckoff_config[param_name] = value
        # Also update the main config dictionary
        self.config["wyckoff_config"] = self.wyckoff_config

    def update_parameters(self, params):
        """
        Update configuration parameters with validation.
        
        Args:
            params: Dictionary of parameters to update
        """
        for key, value in params.items():
            # Handle nested parameters with dot notation
            if '.' in key:
                sections = key.split('.')
                config_section = self.config
                for section in sections[:-1]:
                    if section not in config_section:
                        config_section[section] = {}
                    config_section = config_section[section]
                # Only validate leaf keys
                if not self._validate_param(sections[-1], value):
                    self.logger.warning(f"Parameter '{key}' not updated due to validation failure.")
                    continue
                config_section[sections[-1]] = value
            else:
                # Handle top-level parameters
                if not self._validate_param(key, value):
                    self.logger.warning(f"Parameter '{key}' not updated due to validation failure.")
                    continue
                self.config[key] = value
        
        return self.config

# Default configuration
default_config = {
    "volume": {
        "very_high_threshold": 2.0, # 200% increase
        "high_threshold": 1.3, # 130% increase
        "low_threshold": 0.6, # 60% of average volume
        "very_low_threshold": 0.3, # 30% of average volume
        "lookback_period": 10 # Lookback period for volume analysis
    },
    "candle": {
        "wide_threshold": 1.3, # 30% wider than average
        "narrow_threshold": 0.6, # 60% of average width
        "wick_threshold": 1.5, # 50% longer than average wick
        "lookback_period": 10 # Lookback period for candle analysis
    },
    "trend": {
        "lookback_period": 5, # Lookback period for trend analysis
        "sideways_threshold": 2,  # 2% change for sideways movement
        "strong_trend_threshold": 5,  # 5% change for strong trend
        "volume_change_threshold": 10,  # 10% change for significant volume change
        "min_trend_length": 3 # Minimum number of candles for trend detection
    },
    "pattern": {
        "accumulation": {
            "price_volatility_threshold": 0.08, # 8% price volatility
            "high_volume_threshold": 1.5, # 150% of average volume
            "support_tests_threshold": 1 # Minimum number of support tests
        },
        "distribution": {
            "price_volatility_threshold": 0.08, # 8% price volatility
            "high_volume_threshold": 1.5, # 150% of average volume
            "resistance_tests_threshold": 1 # Minimum number of resistance tests
        },
        "buying_climax": {
            "near_high_threshold": 0.97, # 3% below the high
            "wide_up_threshold": 0.6, # 60% wider than average
            "upper_wick_threshold": 0.25 # 25% of the candle body
        },
        "selling_climax": {
            "near_low_threshold": 1.07, # 7% above the low
            "wide_down_threshold": 0.6, # 60% wider than average
            "lower_wick_threshold": 0.25 # 25% of the candle body
        }
    },
    "signal": {
        "strong_signal_threshold": 0.8, # 80% confidence for strong signals
        "bullish_confirmation_threshold": 1, # 100% confidence for bullish signals
        "bearish_confirmation_threshold": 1, # 100% confidence for bearish signals
        "bullish_candles_threshold": 2, # Minimum number of bullish candles for confirmation
        "bearish_candles_threshold": 2 # Minimum number of bearish candles for confirmation
    },
    "risk": {
        "default_stop_loss_percent": 0.02, # 2% stop loss
        "default_take_profit_percent": 0.05, # 5% take profit
        "support_resistance_buffer": 0.005, # 0.5% buffer for support/resistance
        "default_risk_percent": 0.01, # 1% risk per trade
        "default_risk_reward": 2.0 # 2:1 risk/reward ratio
    },
    "account": {
        "account_size": 10000, # Example account size
        "risk_per_trade": 0.02 # 2% risk per trade
    },
    "wyckoff_config": {
            'vol_lookback': 20,
            'swing_point_n': 5,
            'climax_vol_multiplier': 2.0,
            'climax_range_multiplier': 1.5,
            'breakout_vol_multiplier': 1.5,
            'tr_max_duration': 100
    },
    "timeframes": [
        {"interval": "1d", "period": "60d"},
        {"interval": "4h", "period": "30d"},
        {"interval": "1h", "period": "30d"},    
        {"interval": "30m", "period": "10d"},
        {"interval": "15m", "period": "10d"},
        {"interval": "5m", "period": "10d"},
        {"interval": "1m", "period": "10d"}
    ]
}
