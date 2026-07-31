"""MarketFlow package initialization with lazy public API exports."""

__all__ = [
    "MarketflowFacade",
    "MarketFlowDataParameters",
    "MarketflowResultExtractor",
]


def __getattr__(name: str):
    if name == "MarketflowFacade":
        from .marketflow_facade import MarketflowFacade

        return MarketflowFacade
    if name == "MarketFlowDataParameters":
        from .marketflow_data_parameters import MarketFlowDataParameters

        return MarketFlowDataParameters
    if name == "MarketflowResultExtractor":
        from .marketflow_results_extractor import MarketflowResultExtractor

        return MarketflowResultExtractor
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
