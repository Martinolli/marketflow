"""Offline frozen-calendar and deterministic RTH bar tooling for MarketFlow."""

from marketflow.historical_data.analytical_segments import (
    AnalyticalSegment,
    assign_analytical_segments,
    current_segment_prefix,
)
from marketflow.historical_data.frozen_calendar import (
    CalendarGenerationError,
    FrozenCalendar,
    FrozenCalendarRequest,
    generate_frozen_calendar,
)
from marketflow.historical_data.rth_bar_engine import (
    DerivedBar,
    DerivedDatasetResult,
    SourceBar,
    derive_profile_bars,
)
from marketflow.historical_data.monthly_acquisition import (
    FAKE_FIXTURE_PROVENANCE,
    MONTHLY_ACQUISITION_MANIFEST_SCHEMA_VERSION,
    MonthChunkRequest,
    MonthlyAcquisitionError,
    build_month_chunk_request,
    execute_fake_monthly_acquisition,
)
from marketflow.historical_data.artifacts import (
    HISTORICAL_MANIFEST_SCHEMA_VERSION,
    HistoricalArtifactError,
    create_historical_run,
)
from marketflow.historical_data.pipeline import run_offline_historical_pipeline

__all__ = [
    "AnalyticalSegment",
    "HISTORICAL_MANIFEST_SCHEMA_VERSION",
    "MONTHLY_ACQUISITION_MANIFEST_SCHEMA_VERSION",
    "FAKE_FIXTURE_PROVENANCE",
    "CalendarGenerationError",
    "DerivedBar",
    "DerivedDatasetResult",
    "FrozenCalendar",
    "FrozenCalendarRequest",
    "HistoricalArtifactError",
    "MonthChunkRequest",
    "MonthlyAcquisitionError",
    "SourceBar",
    "assign_analytical_segments",
    "build_month_chunk_request",
    "create_historical_run",
    "current_segment_prefix",
    "derive_profile_bars",
    "execute_fake_monthly_acquisition",
    "generate_frozen_calendar",
    "run_offline_historical_pipeline",
]
