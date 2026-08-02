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
from marketflow.historical_data.massive_smoke import (
    LIVE_PROVIDER_SMOKE_PROVENANCE,
    SMOKE_CLASSIFICATION,
    SMOKE_RUNTIME_ROOT,
    MassiveSmokeError,
    MassiveSmokeSpec,
    default_smoke_spec,
    massive_smoke_plan,
    massive_smoke_self_check,
    smoke_spec_digest,
)
from marketflow.historical_data.massive_date_diagnostic import (
    DATE_DIAGNOSTIC_CLASSIFICATION,
    DATE_DIAGNOSTIC_SCHEMA_VERSION,
    MassiveDateDiagnosticError,
    MassiveDateDiagnosticSpec,
    date_diagnostic_spec_digest,
    default_date_diagnostic_spec,
    massive_date_diagnostic_2026_plan,
    massive_date_diagnostic_2026_self_check,
)
from marketflow.historical_data.massive_transport import (
    MASSIVE_REST_HOST,
    MassiveRestTransport,
    MassiveTransportError,
    ProviderApiKey,
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
    "MASSIVE_REST_HOST",
    "SMOKE_CLASSIFICATION",
    "DATE_DIAGNOSTIC_CLASSIFICATION",
    "DATE_DIAGNOSTIC_SCHEMA_VERSION",
    "SMOKE_RUNTIME_ROOT",
    "FAKE_FIXTURE_PROVENANCE",
    "LIVE_PROVIDER_SMOKE_PROVENANCE",
    "CalendarGenerationError",
    "DerivedBar",
    "DerivedDatasetResult",
    "FrozenCalendar",
    "FrozenCalendarRequest",
    "HistoricalArtifactError",
    "MonthChunkRequest",
    "MonthlyAcquisitionError",
    "MassiveSmokeError",
    "MassiveSmokeSpec",
    "MassiveDateDiagnosticError",
    "MassiveDateDiagnosticSpec",
    "MassiveRestTransport",
    "MassiveTransportError",
    "ProviderApiKey",
    "SourceBar",
    "assign_analytical_segments",
    "build_month_chunk_request",
    "create_historical_run",
    "current_segment_prefix",
    "date_diagnostic_spec_digest",
    "default_smoke_spec",
    "default_date_diagnostic_spec",
    "derive_profile_bars",
    "execute_fake_monthly_acquisition",
    "generate_frozen_calendar",
    "massive_date_diagnostic_2026_plan",
    "massive_date_diagnostic_2026_self_check",
    "massive_smoke_plan",
    "massive_smoke_self_check",
    "run_offline_historical_pipeline",
    "smoke_spec_digest",
]
