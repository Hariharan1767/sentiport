"""
Configuration loader and validator for Sentiment Portfolio Optimization System.

This module handles loading, parsing, and validating configuration files.
It ensures all required parameters are present and valid.
"""

import os
import yaml
import logging
from pathlib import Path
from typing import Dict, Any, List
from dataclasses import dataclass


logger = logging.getLogger(__name__)


@dataclass
class ConfigValidationError(Exception):
    """Custom exception for configuration validation errors."""
    message: str
    
    def __str__(self):
        return f"Configuration Validation Error: {self.message}"


class ConfigLoader:
    """
    Load and validate configuration from YAML files.
    
    This class handles:
    - Loading YAML configuration files
    - Validating required parameters
    - Type checking
    - Default value assignment
    - Parameter range validation
    
    Attributes:
        config (Dict): Loaded configuration dictionary
        config_path (Path): Path to configuration file
    """
    
    def __init__(self, config_path: str = "config/config.yaml"):
        """
        Initialize ConfigLoader.
        
        Args:
            config_path: Path to YAML configuration file
            
        Raises:
            FileNotFoundError: If config file does not exist
        """
        self.config_path = Path(config_path)
        
        if not self.config_path.exists():
            raise FileNotFoundError(
                f"Configuration file not found at {self.config_path}"
            )
        
        self.config = self._load_yaml()
        self._validate_config()
        logger.info(f"Configuration loaded from {config_path}")
    
    def _load_yaml(self) -> Dict[str, Any]:
        """
        Load YAML configuration file.
        
        Returns:
            Dictionary containing configuration
            
        Raises:
            yaml.YAMLError: If YAML parsing fails
        """
        try:
            with open(self.config_path, 'r') as f:
                config = yaml.safe_load(f)
                if config is None:
                    raise ConfigValidationError("Configuration file is empty")
                return config
        except yaml.YAMLError as e:
            raise ConfigValidationError(f"Failed to parse YAML: {str(e)}")
    
    def _validate_config(self) -> None:
        """
        Validate configuration structure and values.
        
        Raises:
            ConfigValidationError: If validation fails
        """
        required_sections = [
            'data_collection',
            'sentiment_analysis',
            'portfolio_optimization',
            'backtesting'
        ]
        
        for section in required_sections:
            if section not in self.config:
                raise ConfigValidationError(
                    f"Missing required section: {section}"
                )
        
        # Validate data collection
        self._validate_data_collection()
        
        # Validate sentiment analysis
        self._validate_sentiment_analysis()
        
        # Validate portfolio optimization
        self._validate_portfolio_optimization()
        
        # Validate backtesting
        self._validate_backtesting()
    
    def _validate_data_collection(self) -> None:
        """Validate data collection configuration."""
        dc = self.config['data_collection']
        
        if not dc.get('tickers') or len(dc['tickers']) < 2:
            raise ConfigValidationError(
                "data_collection.tickers must contain at least 2 tickers"
            )
        
        if not isinstance(dc['tickers'], list):
            raise ConfigValidationError(
                "data_collection.tickers must be a list"
            )
        
        # Validate date range
        start = dc.get('start_date')
        end = dc.get('end_date')
        
        if not start or not end:
            raise ConfigValidationError(
                "data_collection requires start_date and end_date"
            )
        
        logger.info(
            f"Data collection config valid: {len(dc['tickers'])} tickers, "
            f"period {start} to {end}"
        )
    
    def _validate_sentiment_analysis(self) -> None:
        """Validate sentiment analysis configuration."""
        sa = self.config['sentiment_analysis']
        
        # Validate model type
        valid_models = ['logistic_regression', 'naive_bayes', 'svm']
        model_type = sa['model'].get('type')
        
        if model_type not in valid_models:
            raise ConfigValidationError(
                f"Invalid sentiment model type: {model_type}. "
                f"Must be one of: {valid_models}"
            )
        
        # Validate vectorizer
        valid_vectorizers = ['tfidf', 'count', 'word2vec']
        vectorizer = sa['vectorizer'].get('type')
        
        if vectorizer not in valid_vectorizers:
            raise ConfigValidationError(
                f"Invalid vectorizer type: {vectorizer}. "
                f"Must be one of: {valid_vectorizers}"
            )
        
        # Validate max features
        max_features = sa['vectorizer'].get('max_features')
        if max_features < 100:
            logger.warning(
                f"max_features ({max_features}) seems low. "
                "Recommend at least 1000."
            )
        
        logger.info(
            f"Sentiment analysis config valid: "
            f"model={model_type}, vectorizer={vectorizer}"
        )
    
    def _validate_portfolio_optimization(self) -> None:
        """Validate portfolio optimization configuration."""
        po = self.config['portfolio_optimization']
        
        # Validate risk-free rate
        rfr = po.get('risk_free_rate')
        if not (0 <= rfr <= 0.1):
            logger.warning(
                f"Risk-free rate ({rfr}) outside typical range [0, 0.1]"
            )
        
        # Validate sentiment lambda values
        if po.get('sentiment_enhanced', {}).get('enabled'):
            lambdas = po['sentiment_enhanced'].get('lambda_values', [])
            if not lambdas:
                raise ConfigValidationError(
                    "sentiment_enhanced is enabled but lambda_values is empty"
                )
            
            for lam in lambdas:
                if not (0 <= lam <= 1):
                    raise ConfigValidationError(
                        f"Lambda value {lam} outside valid range [0, 1]"
                    )
        
        logger.info(
            f"Portfolio optimization config valid: "
            f"risk_free_rate={rfr}"
        )
    
    def _validate_backtesting(self) -> None:
        """Validate backtesting configuration."""
        bt = self.config['backtesting']
        
        # Validate strategies
        valid_strategies = [
            'equal_weighted',
            'market_index',
            'mean_variance_traditional',
            'sentiment_enhanced_lambda_0.1',
            'sentiment_enhanced_lambda_0.3',
            'sentiment_enhanced_lambda_0.5'
        ]
        
        strategies = bt.get('strategies', [])
        for strategy in strategies:
            if strategy not in valid_strategies:
                logger.warning(
                    f"Unknown strategy: {strategy}. "
                    f"Available: {valid_strategies}"
                )
        
        logger.info(
            f"Backtesting config valid: {len(strategies)} strategies"
        )
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value by key (supports nested keys).
        
        Args:
            key: Configuration key (use dots for nesting, e.g., 'data_collection.tickers')
            default: Default value if key not found
            
        Returns:
            Configuration value
            
        Example:
            >>> loader = ConfigLoader()
            >>> tickers = loader.get('data_collection.tickers')
            >>> model_type = loader.get('sentiment_analysis.model.type')
        """
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
            
            if value is None:
                return default
        
        return value
    
    def get_section(self, section: str) -> Dict[str, Any]:
        """
        Get entire configuration section.
        
        Args:
            section: Section name
            
        Returns:
            Dictionary with section configuration
        """
        return self.config.get(section, {})
    
    def create_directories(self) -> None:
        """Create necessary project directories if they don't exist."""
        paths = self.config.get('paths', {})
        
        directories = [
            paths.get('data_dir'),
            os.path.join(paths.get('data_dir'), 'raw'),
            os.path.join(paths.get('data_dir'), 'processed'),
            paths.get('results_dir'),
            os.path.join(paths.get('results_dir'), 'models'),
            os.path.join(paths.get('results_dir'), 'plots'),
            paths.get('notebooks_dir'),
        ]
        
        for directory in directories:
            if directory:
                Path(directory).mkdir(parents=True, exist_ok=True)
                logger.info(f"Ensured directory exists: {directory}")
    
    def validate_file_paths(self) -> None:
        """Validate that all required output paths are writable."""
        paths_to_check = [
            self.config['data_collection'].get('stock_prices_path'),
            self.config['sentiment_analysis'].get('daily_sentiment_path'),
            self.config['backtesting'].get('backtest_results_path'),
        ]
        
        for path in paths_to_check:
            if path:
                parent = Path(path).parent
                if not parent.exists():
                    logger.warning(f"Output directory does not exist: {parent}")
    
    def get_tickers(self) -> List[str]:
        """Get list of stock tickers."""
        return self.get('data_collection.tickers', [])
    
    def get_date_range(self) -> tuple:
        """
        Get date range for data collection.
        
        Returns:
            Tuple of (start_date, end_date) as strings
        """
        return (
            self.get('data_collection.start_date'),
            self.get('data_collection.end_date')
        )
    
    def get_sentiment_model_type(self) -> str:
        """Get sentiment analysis model type."""
        return self.get('sentiment_analysis.model.type')
    
    def get_risk_free_rate(self) -> float:
        """Get risk-free rate."""
        return self.get('portfolio_optimization.risk_free_rate', 0.02)
    
    def get_lambda_values(self) -> List[float]:
        """Get sentiment lambda values to test."""
        return self.get('portfolio_optimization.sentiment_enhanced.lambda_values', [])
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Return entire configuration as dictionary.
        
        Returns:
            Configuration dictionary
        """
        return self.config.copy()
    
    def __repr__(self) -> str:
        """String representation of ConfigLoader."""
        tickers = self.get_tickers()
        return (
            f"ConfigLoader(tickers={len(tickers)}, "
            f"model={self.get_sentiment_model_type()})"
        )


def setup_config(config_path: str = "config/config.yaml") -> ConfigLoader:
    """
    Setup and initialize configuration.
    
    This is a convenience function that:
    1. Loads configuration
    2. Creates necessary directories
    3. Validates file paths
    4. Sets up logging
    
    Args:
        config_path: Path to configuration file
        
    Returns:
        ConfigLoader instance
        
    Example:
        >>> config = setup_config()
        >>> tickers = config.get_tickers()
    """
    config = ConfigLoader(config_path)
    config.create_directories()
    config.validate_file_paths()
    
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(config.get('logging.log_file', 'sentiport.log')),
            logging.StreamHandler()
        ]
    )
    
    return config


if __name__ == "__main__":
    # Example usage
    try:
        config = setup_config("config/config.yaml")
        
        print("\n=== Configuration Loaded Successfully ===\n")
        print(f"Tickers: {config.get_tickers()}")
        print(f"Date Range: {config.get_date_range()}")
        print(f"Sentiment Model: {config.get_sentiment_model_type()}")
        print(f"Risk-Free Rate: {config.get_risk_free_rate()}")
        print(f"Lambda Values: {config.get_lambda_values()}")
        print(f"\n{config}")
        
    except ConfigValidationError as e:
        logger.error(f"Configuration error: {e}")
    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
