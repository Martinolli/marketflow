from __future__ import annotations

import json
import os
from datetime import UTC, datetime
from functools import lru_cache
from pathlib import Path
from zoneinfo import ZoneInfo

import pytest

from marketflow.services import acquisition_generation_service as acquisition
from marketflow.services import acquisition_source_rows_materialization_service as materialization


def _epoch_ms(local_date: str, local_hhmm: str) -> int:
    hour, minute = (int(part) for part in local_hhmm.split(":", 1))
    local = datetime.fromisoformat(local_date).replace(hour=hour, minute=minute, tzinfo=ZoneInfo("America/New_York"))
    return int(local.astimezone(UTC).timestamp() * 1000)


def _body(timestamp: int, index: int) -> bytes:
    payload = {
        "adjusted": True,
        "queryCount": 1,
        "results": [
            {
                "o": 100 + index,
                "h": 101 + index,
                "l": 99 + index,
                "c": 100 + index,
                "v": 1000 + index,
                "vw": 100,
                "n": 10,
                "t": timestamp,
                "otc": False,
            }
        ],
        "resultsCount": 1,
        "count": 1,
        "status": "OK",
        "ticker": "AAPL",
    }
    return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")


@lru_cache(maxsize=1)
def _monthly_bodies() -> dict[str, bytes]:
    bodies = {}
    for index, chunk in enumerate(acquisition.build_acquisition_month_chunks_v1()):
        bodies[chunk["month"]] = _body(_epoch_ms(f"{chunk['month']}-01", "04:00"), index)
    return bodies


def _transport(request: dict) -> bytes:
    month = str(request["provider_query_start"])[:7]
    return _monthly_bodies()[month]


@lru_cache(maxsize=1)
def _fake_expected_digest() -> str:
    candidate = acquisition.build_acquisition_generation_live_candidate_v1(
        api_key="fake-materialization-key",
        transport=_transport,
        provider_request_timestamp_utc="2026-08-07T00:00:00Z",
    )
    return candidate["normalized_source_rows_digest"]


def _materialize(tmp_path: Path, *, expected: str | None = None) -> dict:
    return materialization.materialize_frozen_acquisition_source_rows_v1(
        output_root=tmp_path / ".marketflow" / "frozen_acquisition_sources" / "AAPL" / "2022_2025",
        api_key="fake-materialization-key",
        transport=_transport,
        request_timestamp_utc="2026-08-07T00:00:00Z",
        expected_normalized_source_rows_digest=expected or _fake_expected_digest(),
        require_monthly_reconciliation_digest_match=False,
    )


def test_locator_returns_blocked_missing_when_no_row_file_is_present(tmp_path: Path):
    result = materialization.locate_frozen_acquisition_source_rows_v1(search_root=tmp_path / ".marketflow")

    assert result["materialization_status"] == materialization.ACQUISITION_FROZEN_SOURCE_ROWS_MATERIALIZATION_REQUIRES_LIVE_PROVIDER_EXECUTION
    assert result["source_rows_verified_against_frozen_digest"] is False


def test_locator_verifies_existing_rows_file_when_digest_matches(tmp_path: Path):
    created = _materialize(tmp_path)
    located = materialization.locate_frozen_acquisition_source_rows_v1(
        search_root=tmp_path / ".marketflow",
        expected_normalized_source_rows_digest=created["actual_normalized_source_rows_digest"],
    )

    assert located["materialization_status"] == materialization.ACQUISITION_FROZEN_SOURCE_ROWS_ALREADY_AVAILABLE_VERIFIED
    assert located["digest_match"] is True


def test_validator_rejects_rows_file_with_wrong_normalized_source_rows_digest(tmp_path: Path):
    created = _materialize(tmp_path)

    with pytest.raises(materialization.AcquisitionSourceRowsMaterializationError, match="normalized_source_rows_digest"):
        materialization.validate_materialized_frozen_acquisition_source_rows_v1(
            rows_path=created["output_rows_path"],
            expected_normalized_source_rows_digest="0" * 64,
        )


def test_materialization_result_preserves_acquisition_generation_freeze_true(tmp_path: Path):
    assert _materialize(tmp_path)["acquisition_generation_freeze"] is True


def test_materialization_result_keeps_canonical_eligibility_false(tmp_path: Path):
    assert _materialize(tmp_path)["canonical_eligibility"] is False


def test_materialization_result_keeps_registry_eligibility_false(tmp_path: Path):
    assert _materialize(tmp_path)["registry_eligibility"] is False


def test_materialization_result_keeps_strategy_runtime_migration_false(tmp_path: Path):
    assert _materialize(tmp_path)["strategy_runtime_migration"] is False


def test_materialization_result_keeps_predictive_and_profitability_not_accepted(tmp_path: Path):
    result = _materialize(tmp_path)

    assert result["predictive_usefulness"] == "not accepted"
    assert result["profitability"] == "not accepted"


def test_fake_transport_materialization_writes_rows_under_output_root(tmp_path: Path):
    result = _materialize(tmp_path)

    assert Path(result["output_rows_path"]).exists()
    assert ".marketflow" in Path(result["output_rows_path"]).parts


def test_fake_transport_materialization_computes_deterministic_digest(tmp_path: Path):
    first = _materialize(tmp_path / "one")
    second = _materialize(tmp_path / "two")

    assert first["actual_normalized_source_rows_digest"] == second["actual_normalized_source_rows_digest"]


def test_fake_transport_materialization_accepts_only_if_digest_matches_expected(tmp_path: Path):
    result = _materialize(tmp_path, expected=_fake_expected_digest())

    assert result["materialization_status"] == materialization.ACQUISITION_FROZEN_SOURCE_ROWS_MATERIALIZED
    assert result["digest_match"] is True


def test_digest_mismatch_produces_digest_mismatch_status(tmp_path: Path):
    result = _materialize(tmp_path, expected="0" * 64)

    assert result["materialization_status"] == materialization.ACQUISITION_FROZEN_SOURCE_ROWS_MATERIALIZATION_DIGEST_MISMATCH
    assert result["output_rows_path"] is None


def test_api_key_is_not_present_in_result_metadata_or_status_markdown(tmp_path: Path):
    secret = "fake-materialization-key"
    result = _materialize(tmp_path)
    text = materialization.build_acquisition_frozen_source_rows_materialization_status_markdown_v1(result)

    assert secret not in repr(result)
    assert secret not in text
    assert "API key stored: `False`" in text


def test_materialization_does_not_create_acquisition_generation_frozen(tmp_path: Path):
    result = _materialize(tmp_path)

    assert result["acquisition_generation_frozen_created"] is False
    assert result["artifact_kind"] != "ACQUISITION_GENERATION_FROZEN"


def test_materialization_does_not_create_swing_canonical_dataset_frozen(tmp_path: Path):
    result = _materialize(tmp_path)

    assert result["swing_canonical_dataset_frozen_created"] is False
    assert result["artifact_kind"] != "SWING_CANONICAL_DATASET_FROZEN"


def test_status_markdown_includes_digest_match_result_and_no_raw_ohlcv_rows(tmp_path: Path):
    result = _materialize(tmp_path)
    text = materialization.build_acquisition_frozen_source_rows_materialization_status_markdown_v1(result)

    assert "Digest match result: `True`" in text
    assert '"results"' not in text
    assert "| open |" not in text
    assert "| high |" not in text


def test_writer_manifest_writes_only_sanitized_manifest_not_raw_provider_payload(tmp_path: Path):
    result = _materialize(tmp_path)
    manifest_text = Path(result["output_manifest_path"]).read_text(encoding="utf-8")

    assert "provider_raw_response_digest" in manifest_text
    assert "provider_response_body" not in manifest_text
    assert '"results"' not in manifest_text


def test_live_materialization_without_gate_reports_blocked(tmp_path: Path):
    result = materialization.materialize_frozen_acquisition_source_rows_v1(
        output_root=tmp_path / ".marketflow" / "frozen_acquisition_sources" / "AAPL" / "2022_2025",
        api_key="fake-key",
        allow_live=False,
    )

    assert result["materialization_status"] == materialization.ACQUISITION_FROZEN_SOURCE_ROWS_MATERIALIZATION_REQUIRES_LIVE_PROVIDER_EXECUTION
    assert result["blocked_reason"] == materialization.ACQUISITION_SOURCE_ROWS_MATERIALIZATION_BLOCKED_GATE_NOT_ENABLED


@pytest.mark.skipif(
    os.environ.get("MARKETFLOW_ENABLE_LIVE_ACQUISITION_MATERIALIZATION") != "1"
    or not (os.environ.get("MASSIVE_API_KEY") or os.environ.get("POLYGON_API_KEY")),
    reason="live materialization requires explicit gate and provider API key",
)
def test_optional_live_materialization_is_explicitly_gated(tmp_path: Path):
    result = materialization.materialize_frozen_acquisition_source_rows_v1(
        output_root=tmp_path / ".marketflow" / "frozen_acquisition_sources" / "AAPL" / "2022_2025",
        allow_live=True,
    )

    assert result["provider_requests_made"] is True
