"""Dry offline CLI for MarketFlow historical-data readiness."""

from __future__ import annotations

import argparse
import json

from marketflow.historical_data.frozen_calendar import default_calendar_request, generate_frozen_calendar
from marketflow.research import acquisition_contract_v2 as contract_v2
from marketflow.research import acquisition_contract_v2_1 as contract_v21


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Emit a sanitized offline frozen-calendar/bar-engine readiness receipt.")
    parser.parse_args(argv)
    v2 = contract_v2.default_contract()
    v21 = contract_v21.default_contract()
    contract_v21.verify_base_contract_digest(v21)
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
