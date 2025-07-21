"""
Enhanced Marketflow Configuration Manager Module

This module provides centralized API key and configuration management for the Marketflow system.
It supports multiple sources for configuration values (environment variables, config files, etc.)
with appropriate fallbacks and validation.

Enhanced to support LLM model specification for fine-tuned model integration and comprehensive
Marketflow system configuration including LLM providers, data sources, and application settings.

Fixed version addressing compatibility issues:
- Removed circular import dependency with logger
- Fixed hardcoded Windows-specific paths
- Improved cross-platform compatibility
- Better error handling and validation
- Dependency injection for logger
"""

import os
import json
from typing import Dict, Any, Optional
from dotenv import load_dotenv
from pathlib import Path

# Import the shared utility function
from .marketflow_utils import get_project_root

# Load .env file if it exists
load_dotenv()

class ConfigManager:
    """Manages API keys and configuration for the Marketflow system."""
    
    # Default LLM model to use if not specified
    DEFAULT_LLM_MODEL = "gpt-3.5-turbo"
    
    def __init__(self, config_file: Optional[str] = None, logger=None):
        """
        Initialize the configuration manager.
        
        Parameters:
        - config_file: Optional path to a JSON configuration file
        - logger: Optional logger instance (dependency injection to avoid circular imports)
        """
        self.logger = logger
        self.config_data = {}
        
        # Get project root for cross-platform compatibility
        self.project_root = get_project_root()
        
        # Default config file locations to check - cross-platform compatible
        self.config_file_paths = [
            config_file,  # User-provided path (if any)
            self.project_root / ".marketflow" / "config" / "config.json",  # Custom config path
            Path.home() / ".marketflow" / "config.json",  # User home directory
            Path.cwd() / "marketflow_config.json",  # Current working directory
            Path(__file__).parent / "config.json",  # Module directory
        ]
        
        # Convert Path objects to strings for compatibility
        self.config_file_paths = [str(path) if path else None for path in self.config_file_paths]
        
        # Load configuration from file
        self._load_config_from_file()
        
        # Initialize all configuration properties
        self._initialize_config_properties()
        
        if self.logger:
            self.logger.info("ConfigManager initialized successfully")
    
    def _log(self, level: str, message: str):
        """Internal logging method that works with or without logger"""
        if self.logger:
            getattr(self.logger, level.lower())(message)
        else:
            # Fallback to print for critical messages if no logger available
            if level.upper() in ['ERROR', 'CRITICAL', 'WARNING']:
                print(f"[{level.upper()}] ConfigManager: {message}")
    
    def _load_config_from_file(self) -> None:
        """Load configuration from the first available config file."""
        for file_path in self.config_file_paths:
            if file_path and os.path.isfile(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        self.config_data = json.load(f)
                    self._log("info", f"Loaded configuration from {file_path}")
                    return
                except Exception as e:
                    self._log("warning", f"Error loading config from {file_path}: {e}")
        
        self._log("info", "No configuration file found, using environment variables only")
    
    def _initialize_config_properties(self) -> None:
        """Initialize all configuration properties with defaults and environment variables."""
        # --- LLM Provider Configuration ---
        self.LLM_PROVIDER = self.get_config_value("llm_provider", os.getenv("LLM_PROVIDER", "openai")).lower()
        self.OPENAI_API_KEY = self.get_api_key_safe("openai")
        self.OPENAI_MODEL_NAME = self.get_config_value("openai_model_name", os.getenv("OPENAI_MODEL_NAME", "gpt-4-turbo-preview"))
        self.OLLAMA_BASE_URL = self.get_config_value("ollama_base_url", os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"))
        self.OLLAMA_MODEL_NAME = self.get_config_value("ollama_model_name", os.getenv("OLLAMA_MODEL_NAME", "llama3:instruct"))
        
        # --- Data Provider Configuration ---
        self.POLYGON_API_KEY = self.get_api_key_safe("polygon")
        
        # --- Application Configuration ---
        self.LOG_LEVEL = self.get_config_value("log_level", os.getenv("LOG_LEVEL", "INFO"))
        self.MAX_CONVERSATION_HISTORY = int(self.get_config_value("max_conversation_history", os.getenv("MAX_CONVERSATION_HISTORY", "10")))
        self.RAG_TOP_K = int(self.get_config_value("rag_top_k", os.getenv("RAG_TOP_K", "5")))
        
        # --- File Paths - Cross-platform compatible ---
        default_log_path = str(self.project_root / ".marketflow" / "logs" / "marketflow_engine.log")
        default_memory_path = str(self.project_root / ".marketflow" / "memory" / "marketflow_chat_history.db")
        
        self.LOG_FILE_PATH = self.get_config_value("log_file_path", os.getenv("LOG_FILE_PATH", default_log_path))
        self.MEMORY_DB_PATH = self.get_config_value("memory_db_path", os.getenv("MEMORY_DB_PATH", default_memory_path))

        # --- Reports and Output ---
        default_report_dir = str(self.project_root / ".marketflow" / "reports")
        self.REPORT_DIR = self.get_config_value("report_dir", os.getenv("REPORT_DIR", default_report_dir))

        # --- Snapshot Output Directory ---
        default_snapshot_dir = str(self.project_root / ".marketflow" / "snapshot_reports")
        self.SNAPSHOT_OUTPUT_DIR = self.get_config_value("snapshot_output_dir", os.getenv("SNAPSHOT_OUTPUT_DIR", default_snapshot_dir))
        self.config_data["snapshot_output_dir"] = self.SNAPSHOT_OUTPUT_DIR
        
        # Ensure output directories exist
        try:
            Path(self.REPORT_DIR).mkdir(parents=True, exist_ok=True)
            self._log("info", f"Report output directory created/verified: {self.REPORT_DIR}")
            Path(self.SNAPSHOT_OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
            self._log("info", f"Snapshot output directory created/verified: {self.SNAPSHOT_OUTPUT_DIR}")
        except Exception as e:
            self._log("error", f"Failed to create output directory: {e}")
            raise
    
    def get_api_key(self, service: str) -> str:
        """
        Get API key for the specified service with appropriate fallbacks.
        
        Parameters:
        - service: Service name (e.g., 'polygon', 'openai')
        
        Returns:
        - API key string
        
        Raises:
        - ValueError: If API key is not found in any source
        """
        # Map service names to environment variable names
        env_var_map = {
            'polygon': 'POLYGON_API_KEY',
            'openai': 'OPENAI_API_KEY',
        }
        
        # Map service names to config file keys
        config_key_map = {
            'polygon': 'polygon_api_key',
            'openai': 'openai_api_key',
        }
        
        # Check if service is supported
        if service not in env_var_map:
            raise ValueError(f"Unsupported service: {service}")
        
        # Try to get API key from environment variable
        env_var_name = env_var_map[service]
        api_key = os.getenv(env_var_name)
        
        # If not found in environment, try config file
        if not api_key and service in config_key_map:
            config_key = config_key_map[service]
            api_key = self.config_data.get(config_key)
        
        # If still not found, raise error with helpful message
        if not api_key:
            raise ValueError(
                f"API key for {service} not found. Please set the {env_var_name} environment variable "
                f"or add '{config_key_map[service]}' to your configuration file."
            )
        
        return api_key
    
    def get_api_key_safe(self, service: str) -> Optional[str]:
        """
        Get API key for the specified service without raising exceptions.
        
        Parameters:
        - service: Service name (e.g., 'polygon', 'openai')
        
        Returns:
        - API key string or None if not found
        """
        try:
            return self.get_api_key(service)
        except ValueError:
            return None
    
    def validate_api_key(self, service: str) -> bool:
        """
        Validate that the API key for the specified service exists and has the correct format.
        
        Parameters:
        - service: Service name (e.g., 'polygon', 'openai')
        
        Returns:
        - True if API key is valid, False otherwise
        """
        try:
            api_key = self.get_api_key(service)
            
            # Basic validation based on service
            if service == 'polygon':
                # Polygon.io API keys are typically alphanumeric
                return bool(api_key and len(api_key) > 10)
            elif service == 'openai':
                # OpenAI API keys typically start with 'sk-'
                return bool(api_key and api_key.startswith('sk-'))
            else:
                # For other services, just check if key exists
                return bool(api_key)
        except ValueError:
            return False
    
    def get_config_value(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value with fallback to default.
        
        Parameters:
        - key: Configuration key
        - default: Default value if key is not found
        
        Returns:
        - Configuration value or default
        """
        # Try to get from environment variable (uppercase with prefix MARKETFLOW_)
        env_var_name = f"MARKETFLOW_{key.upper()}"
        env_value = os.getenv(env_var_name)
        if env_value is not None:
            return env_value
        
        # Try to get from config file
        return self.config_data.get(key, default)
    
    def save_config(self, config_file: Optional[str] = None) -> None:
        """
        Save current configuration to file.
        
        Parameters:
        - config_file: Optional path to save configuration file
        """
        if not config_file:
            # Use first writable path from config_file_paths
            for path in self.config_file_paths:
                if path:
                    try:
                        # Ensure directory exists
                        Path(path).parent.mkdir(parents=True, exist_ok=True)
                        config_file = path
                        break
                    except Exception:
                        continue
        
        if not config_file:
            # Default to current directory if no writable path found
            config_file = str(Path.cwd() / "marketflow_config.json")
        
        try:
            # Ensure directory exists
            Path(config_file).parent.mkdir(parents=True, exist_ok=True)
            
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config_data, f, indent=4)
            
            self._log("info", f"Configuration saved to {config_file}")
        except Exception as e:
            self._log("error", f"Error saving configuration to {config_file}: {e}")
            raise
    
    def set_config_value(self, key: str, value: Any) -> None:
        """
        Set configuration value.
        
        Parameters:
        - key: Configuration key
        - value: Configuration value
        """
        self.config_data[key] = value
        # Update the corresponding property if it exists
        self._update_property_from_config(key, value)
    
    def _update_property_from_config(self, key: str, value: Any) -> None:
        """Update instance properties when config values change."""
        property_map = {
            'llm_provider': 'LLM_PROVIDER',
            'openai_model_name': 'OPENAI_MODEL_NAME',
            'ollama_base_url': 'OLLAMA_BASE_URL',
            'ollama_model_name': 'OLLAMA_MODEL_NAME',
            'log_level': 'LOG_LEVEL',
            'max_conversation_history': 'MAX_CONVERSATION_HISTORY',
            'rag_top_k': 'RAG_TOP_K',
            'log_file_path': 'LOG_FILE_PATH',
            'memory_db_path': 'MEMORY_DB_PATH',
        }
        
        if key in property_map:
            prop_name = property_map[key]
            if key in ['max_conversation_history', 'rag_top_k']:
                setattr(self, prop_name, int(value))
            elif key == 'llm_provider':
                setattr(self, prop_name, str(value).lower())
            else:
                setattr(self, prop_name, value)
    
    def set_api_key(self, service: str, api_key: str) -> None:
        """
        Set API key for the specified service.
        
        Parameters:
        - service: Service name (e.g., 'polygon', 'openai')
        - api_key: API key value
        """
        # Map service names to config file keys
        config_key_map = {
            'polygon': 'polygon_api_key',
            'openai': 'openai_api_key',
        }
        
        # Check if service is supported
        if service not in config_key_map:
            raise ValueError(f"Unsupported service: {service}")
        
        # Set API key in config data
        self.config_data[config_key_map[service]] = api_key
        
        # Update the corresponding property
        if service == 'polygon':
            self.POLYGON_API_KEY = api_key
        elif service == 'openai':
            self.OPENAI_API_KEY = api_key
    
    # New methods for LLM model configuration
    
    def get_llm_model(self) -> str:
        """
        Get the configured LLM model name with appropriate fallbacks.
        
        Returns:
        - Model name string (e.g., 'gpt-3.5-turbo', 'ft:gpt-3.5-turbo:marketflow:20250602')
        """
        # Try to get from environment variable
        model = os.getenv('MARKETFLOW_LLM_MODEL')
        
        # If not found in environment, try config file
        if not model:
            model = self.config_data.get('llm_model')
        
        # If still not found, use provider-specific default
        if not model:
            if self.LLM_PROVIDER == 'openai':
                model = self.OPENAI_MODEL_NAME
            elif self.LLM_PROVIDER == 'ollama':
                model = self.OLLAMA_MODEL_NAME
            else:
                model = self.DEFAULT_LLM_MODEL
            self._log("info", f"No LLM model specified, using default: {model}")
        
        return model
    
    def set_llm_model(self, model_name: str) -> None:
        """
        Set the LLM model to use.
        
        Parameters:
        - model_name: Model name (e.g., 'gpt-3.5-turbo', 'ft:gpt-3.5-turbo:marketflow:20250602')
        """
        self.config_data['llm_model'] = model_name
        self._log("info", f"LLM model set to: {model_name}")
    
    def get_available_models(self) -> list:
        """
        Get list of available models configured in the system.
        
        Returns:
        - List of model names
        """
        # Get from config file with fallback to default list
        models = self.config_data.get('available_models', [
            "gpt-3.5-turbo",
            "gpt-4",
            "gpt-4-turbo-preview",
            "llama3:instruct",
            # Add any fine-tuned models here
        ])
        
        # Always ensure the current model is in the list
        current_model = self.get_llm_model()
        if current_model not in models:
            models.append(current_model)
        
        return models
    
    def get_llm_provider_config(self) -> Dict[str, Any]:
        """
        Get LLM provider configuration for the current provider.
        
        Returns:
        - Dictionary with provider configuration
        """
        if self.LLM_PROVIDER == 'openai':
            return {
                'provider': 'openai',
                'api_key': self.OPENAI_API_KEY,
                'model': self.OPENAI_MODEL_NAME
            }
        elif self.LLM_PROVIDER == 'ollama':
            return {
                'provider': 'ollama',
                'base_url': self.OLLAMA_BASE_URL,
                'model': self.OLLAMA_MODEL_NAME
            }
        else:
            raise ValueError(f"Unsupported LLM provider: {self.LLM_PROVIDER}")
    
    def validate_configuration(self) -> Dict[str, bool]:
        """
        Validate the current configuration and return status for each component.
        
        Returns:
        - Dictionary with validation results
        """
        validation_results = {}
        
        # Validate API keys
        validation_results['openai_api_key'] = self.validate_api_key('openai')
        validation_results['polygon_api_key'] = self.validate_api_key('polygon')
        
        # Validate LLM provider configuration
        try:
            llm_config = self.get_llm_provider_config()
            validation_results['llm_provider_config'] = True
        except Exception:
            validation_results['llm_provider_config'] = False
        
        # Validate file paths
        validation_results['log_file_path'] = self._validate_file_path(self.LOG_FILE_PATH, create_dirs=True)
        validation_results['memory_db_path'] = self._validate_file_path(self.MEMORY_DB_PATH, create_dirs=True)
        
        return validation_results
    
    def _validate_file_path(self, file_path: str, create_dirs: bool = False) -> bool:
        """
        Validate that a file path is accessible.
        
        Parameters:
        - file_path: Path to validate
        - create_dirs: Whether to create directories if they don't exist
        
        Returns:
        - True if path is valid/accessible, False otherwise
        """
        try:
            path_obj = Path(file_path)
            dir_path = path_obj.parent
            if create_dirs and not dir_path.exists():
                dir_path.mkdir(parents=True, exist_ok=True)
            return dir_path.exists() or create_dirs
        except Exception:
            return False


# Backward compatibility class that mimics the original MARKETFLOWConfigManager
class MARKETFLOWConfigManager(ConfigManager):
    """
    Backward compatibility wrapper for the original MARKETFLOWConfigManager interface.
    This allows existing code to continue working without modification.
    """
    
    def __init__(self, config_file: Optional[str] = None, logger=None):
        super().__init__(config_file, logger)
        if self.logger:
            self.logger.info("MARKETFLOWConfigManager initialized with backward compatibility")


# Create singleton instances for both interfaces
_config_manager = None
_marketflow_config_manager = None

def get_config_manager(config_file: Optional[str] = None, logger=None) -> ConfigManager:
    """
    Get the singleton ConfigManager instance.
    
    Parameters:
    - config_file: Optional path to a JSON configuration file
    - logger: Optional logger instance
    
    Returns:
    - ConfigManager instance
    """
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigManager(config_file, logger)
    return _config_manager

def get_marketflow_config_manager(config_file: Optional[str] = None, logger=None) -> MARKETFLOWConfigManager:
    """
    Get the singleton MARKETFLOWConfigManager instance for backward compatibility.
    
    Parameters:
    - config_file: Optional path to a JSON configuration file
    - logger: Optional logger instance
    
    Returns:
    - MARKETFLOWConfigManager instance
    """
    global _marketflow_config_manager
    if _marketflow_config_manager is None:
        _marketflow_config_manager = MARKETFLOWConfigManager(config_file, logger)
    return _marketflow_config_manager

def create_app_config(logger=None):
    """
    Create the AppConfig singleton for backward compatibility.
    
    Parameters:
    - logger: Optional logger instance
    
    Returns:
    - MARKETFLOWConfigManager instance
    """
    return get_marketflow_config_manager(logger=logger)

# Note: AppConfig should be initialized with a logger in the main application
# Example: AppConfig = create_app_config(logger=get_logger("Config_Manager_Marketflow"))
