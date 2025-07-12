"""
Marketflow package initialization.

Exposes main user-facing APIs and hides internal modules from direct import.
"""

from .marketflow_facade import MarketflowFacade
from .marketflow_data_parameters import MarketFlowDataParameters
from .marketflow_results_extractor import MarketflowResultExtractor

# Optionally expose other top-level utilities/classes below:
# from .marketflow_processor import DataProcessor
# from .marketflow_wyckoff import WyckoffAnalyzer

__all__ = [
    "MarketflowFacade",
    "MarketFlowDataParameters",
    "MarketflowResultExtractor",
    # "DataProcessor",
    # "WyckoffAnalyzer",
]