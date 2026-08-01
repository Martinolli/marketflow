"""Dry offline CLI for MarketFlow historical-data readiness."""

from __future__ import annotations

import argparse
import json
import tempfile

from marketflow.historical_data.frozen_calendar import default_calendar_request, generate_frozen_calendar
from marketflow.historical_data.massive_transport import massive_transport_self_check
from marketflow.historical_data.monthly_acquisition import monthly_acquisition_self_check
from marketflow.historical_data.pipeline import run_offline_historical_pipeline, synthetic_self_check_fixture
from marketflow.research import acquisition_contract_v2 as contract_v2
from marketflow.research import acquisition_contract_v2_1 as contract_v21


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Emit a sanitized offline frozen-calendar/bar-engine readiness receipt.")
    parser.add_argument(
        "--pipeline-self-check",
        action="store_true",
        help="Run the synthetic historical-data artifact lineage self-check in an automatically removed temporary directory.",
    )
    parser.add_argument(
        "--monthly-acquisition-self-check",
        action="store_true",
        help="Run the scripted fake-transport monthly acquisition self-check in an automatically removed temporary directory.",
    )
    parser.add_argument(
        "--massive-transport-self-check",
        action="store_true",
        help="Run the Massive REST transport mock-HTTP self-check without provider network access.",
    )
    args = parser.parse_args(argv)
    v2 = contract_v2.default_contract()
    v21 = contract_v21.default_contract()
    contract_v21.verify_base_contract_digest(v21)
    selected_self_checks = sum(
        1 for selected in (args.pipeline_self_check, args.monthly_acquisition_self_check, args.massive_transport_self_check) if selected
    )
    if selected_self_checks > 1:
        parser.error("choose exactly one self-check")
    if args.pipeline_self_check:
        calendar, source_bars, dividend_events = synthetic_self_check_fixture()
        with tempfile.TemporaryDirectory(prefix="marketflow-historical-self-check-") as run_root:
            receipt = run_offline_historical_pipeline(
                calendar=calendar,
                source_bars=source_bars,
                dividend_events=dividend_events,
                run_root=run_root,
            )
        sanitized = {
            "status": "HISTORICAL_DATA_ARTIFACT_LINEAGE_SYNTHETIC_SELF_CHECK",
            "contract_v2_digest": contract_v2.contract_digest(v2),
            "contract_v2_1_digest": contract_v21.contract_digest(v21),
            "pipeline_status": receipt["pipeline_status"],
            "calendar_status": receipt["calendar_status"],
            "normalized_source_status": receipt["normalized_source_status"],
            "swing_derivation_status": receipt["swing_derivation_status"],
            "position_swing_derivation_status": receipt["position_swing_derivation_status"],
            "segment_map_statuses": receipt["segment_map_statuses"],
            "artifact_count": len(receipt["artifact_receipts"]),
            "synthetic_only": True,
            "provider_execution_enabled": False,
            "runtime_migration_performed": False,
            "readiness_note": "NO_PROVIDER_NO_SYMBOL_NO_DATA_DOWNLOAD_NO_REGISTRY_WRITE",
        }
        print(json.dumps(sanitized, sort_keys=True, indent=2))
        return 0
    if args.monthly_acquisition_self_check:
        with tempfile.TemporaryDirectory(prefix="marketflow-monthly-acquisition-self-check-") as run_root:
            receipt = monthly_acquisition_self_check(run_root)
        print(json.dumps(receipt, sort_keys=True, indent=2))
        return 0
    if args.massive_transport_self_check:
        receipt = massive_transport_self_check()
        print(json.dumps(receipt, sort_keys=True, indent=2))
        return 0
    calendar = generate_frozen_calendar(default_calendar_request())
    receipt = {
        "status": "HISTORICAL_DATA_ENGINE_READY_FOR_OFFLINE_SYNTHETIC_USE",
        "contract_v2_digest": contract_v2.contract_digest(v2),
        "contract_v2_1_digest": contract_v21.contract_digest(v21),
        "calendar_status": calendar.status,
        "calendar_digest": calendar.semantic_digest,
        "requested_primary_listing_mic": calendar.requested_primary_listing_mic,
        "requested_calendar_token": calendar.requested_calendar_token,
        "resolved_calendar": calendar.resolved_calendar,
        "exchange_calendars_version": calendar.exchange_calendars_version,
        "tzdata_version": calendar.tzdata_version,
        "normal_full_session_count": len(calendar.normal_sessions()),
        "early_close_session_count": len(calendar.early_close_sessions()),
        "frozen_calendar_engine": "IMPLEMENTED_OFFLINE_PREVIEW_NOT_OPERATOR_FROZEN",
        "bar_engine": "IMPLEMENTED_SYNTHETIC_INPUTS_ONLY",
        "acquisition_enabled": False,
        "provider_execution_enabled": False,
        "runtime_profile_migration_status": v21.runtime_profile_migration_status,
        "readiness_note": "NO_PROVIDER_NO_SYMBOL_NO_DATA_DOWNLOAD_NO_REGISTRY_WRITE",
    }
    print(json.dumps(receipt, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
