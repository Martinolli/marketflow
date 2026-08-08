from __future__ import annotations

from datetime import timedelta
from pathlib import Path

import pytest

from marketflow.services import position_swing_canonical_dataset_service as position


def _source_row(*, timestamp_utc: str, index: int, session_date: str, open_value: int = 100, vwap: str | None = "101") -> dict:
    return {
        "ticker": "AAPL",
        "timestamp_utc": timestamp_utc,
        "timestamp_source": index,
        "timestamp_source_timezone": "UTC",
        "open": str(open_value + index),
        "high": str(open_value + index + 2),
        "low": str(open_value + index - 1),
        "close": str(open_value + index + 1),
        "volume": str(10 + index),
        "vwap": vwap,
        "transactions": index + 1,
        "otc": None,
        "adjusted": True,
        "source_interval_minutes": 15,
        "source_row_index": index,
        "source_chunk_id": f"AAPL-{session_date[:7]}",
        "source_month": session_date[:7],
        "raw_row_digest": f"raw-{session_date}-{index}",
    }


def _full_session_rows(session: dict, *, start_index: int = 0, vwap: str | None = "101") -> list[dict]:
    start = position.swing._parse_utc(session["market_open_utc"])
    return [
        _source_row(
            timestamp_utc=position.swing._utc_text(start + timedelta(minutes=15 * offset)),
            index=start_index + offset,
            session_date=session["session_date"],
            vwap=vwap,
        )
        for offset in range(26)
    ]


def _january_2025_schedule() -> list[dict]:
    return [
        row
        for row in position.calendar_service.build_exchange_calendar_schedule_rows_v1()
        if row["session_date"].startswith("2025-01") and row["is_full_session"] is True
    ][:20]


def _january_2025_source_rows() -> tuple[list[dict], list[dict]]:
    schedule = _january_2025_schedule()
    rows: list[dict] = []
    for session_index, session in enumerate(schedule):
        rows.extend(_full_session_rows(session, start_index=session_index * 26))
    return rows, schedule


def _ready_candidate() -> dict:
    rows, schedule = _january_2025_source_rows()
    return position.build_position_swing_canonical_dataset_candidate_v1(
        source_rows=rows,
        source_rows_digest=position.EXPECTED_NORMALIZED_SOURCE_ROWS_DIGEST,
        fixture_mode=True,
        schedule_rows=schedule,
    )


def test_candidate_builds_offline_without_provider_calls(monkeypatch: pytest.MonkeyPatch):
    def fail_provider_call(*args, **kwargs):  # pragma: no cover
        raise AssertionError("provider path must not be called")

    monkeypatch.setattr(position.acquisition, "fetch_massive_custom_bars_v1", fail_provider_call)

    candidate = position.build_position_swing_canonical_dataset_candidate_from_local_artifact_v1("missing-root")

    assert candidate["created_offline"] is True
    assert candidate["provider_requests_made"] is False


def test_candidate_builds_from_verified_materialized_source_rows(monkeypatch: pytest.MonkeyPatch):
    rows, schedule = _january_2025_source_rows()
    source_path = ".marketflow/frozen_acquisition_sources/AAPL/2022_2025/AAPL_15m_adjusted_2022_2025_normalized_source_rows.csv"

    monkeypatch.setattr(position.calendar_service, "build_exchange_calendar_schedule_rows_v1", lambda: schedule)
    monkeypatch.setattr(
        position.acquisition,
        "normalized_source_rows_digest_v1",
        lambda _rows: position.EXPECTED_NORMALIZED_SOURCE_ROWS_DIGEST,
    )
    monkeypatch.setattr(
        position,
        "find_verified_frozen_acquisition_source_rows_v1",
        lambda _root=position.DEFAULT_SOURCE_ROWS_SEARCH_ROOT: {
            "path": source_path,
            "rows": rows,
            "normalized_source_rows_digest": position.EXPECTED_NORMALIZED_SOURCE_ROWS_DIGEST,
            "materialization_receipt_digest": position.EXPECTED_MATERIALIZATION_RECEIPT_DIGEST,
        },
    )

    candidate = position.build_position_swing_canonical_dataset_candidate_from_local_artifact_v1()

    assert candidate["candidate_status"] == position.POSITION_SWING_CANONICAL_DATASET_READY_FOR_OPERATOR_REVIEW
    assert candidate["source_row_artifact_path"] == source_path
    assert candidate["source_row_digest_verified"] is True
    assert candidate["materialization_receipt_digest"] == position.EXPECTED_MATERIALIZATION_RECEIPT_DIGEST


def test_source_row_digest_is_verified_before_generation(monkeypatch: pytest.MonkeyPatch):
    rows, _schedule = _january_2025_source_rows()

    def fail_generation(*_args, **_kwargs):  # pragma: no cover
        raise AssertionError("POSITION_SWING bars must not be generated before digest verification")

    monkeypatch.setattr(position, "build_position_swing_bars_from_normalized_source_rows_v1", fail_generation)

    candidate = position.build_position_swing_canonical_dataset_candidate_v1(
        source_rows=rows,
        source_rows_digest="0" * 64,
    )

    assert candidate["candidate_status"] == position.POSITION_SWING_CANONICAL_DATASET_SOURCE_ROWS_DIGEST_MISMATCH
    assert candidate["dataset_rows"] == []


def test_artifact_kind_is_position_swing_candidate():
    assert _ready_candidate()["artifact_kind"] == "POSITION_SWING_CANONICAL_DATASET_CANDIDATE"


def test_candidate_binds_acquisition_frozen_digest():
    assert _ready_candidate()["acquisition_generation_frozen_digest"] == position.EXPECTED_ACQUISITION_GENERATION_FROZEN_DIGEST


def test_candidate_binds_normalized_source_rows_digest():
    assert _ready_candidate()["normalized_source_rows_digest"] == position.EXPECTED_NORMALIZED_SOURCE_ROWS_DIGEST


def test_candidate_status_becomes_ready_for_operator_review():
    assert _ready_candidate()["candidate_status"] == position.POSITION_SWING_CANONICAL_DATASET_READY_FOR_OPERATOR_REVIEW


def test_candidate_keeps_canonical_dataset_frozen_false():
    assert _ready_candidate()["canonical_dataset_frozen"] is False


def test_candidate_keeps_canonical_eligibility_false():
    assert _ready_candidate()["canonical_eligibility"] is False


def test_candidate_keeps_registry_eligibility_false():
    assert _ready_candidate()["registry_eligibility"] is False


def test_candidate_keeps_strategy_runtime_migration_false():
    assert _ready_candidate()["strategy_runtime_migration"] is False


def test_candidate_keeps_runtime_and_strategy_use_not_authorized():
    candidate = _ready_candidate()

    assert candidate["runtime_use"] == "NOT_AUTHORIZED"
    assert candidate["strategy_use"] == "NOT_AUTHORIZED"


def test_full_ordinary_session_with_26_source_rows_produces_1_position_swing_bar():
    session = _january_2025_schedule()[0]
    result = position.build_position_swing_bars_from_normalized_source_rows_v1(
        _full_session_rows(session),
        schedule_rows=[session],
    )

    assert len(result["dataset_rows"]) == 1


def test_each_full_session_position_swing_bar_uses_26_source_rows():
    session = _january_2025_schedule()[0]
    result = position.build_position_swing_bars_from_normalized_source_rows_v1(
        _full_session_rows(session),
        schedule_rows=[session],
    )

    assert result["dataset_rows"][0]["source_row_count"] == 26


def test_position_swing_bar_records_source_session_and_timeframe():
    session = _january_2025_schedule()[0]
    result = position.build_position_swing_bars_from_normalized_source_rows_v1(
        _full_session_rows(session),
        schedule_rows=[session],
    )

    assert result["dataset_rows"][0]["source_session_date"] == session["session_date"]
    assert result["dataset_rows"][0]["source_timeframe"] == "15m"


def test_ohlc_aggregation_is_correct():
    session = _january_2025_schedule()[0]
    result = position.build_position_swing_bars_from_normalized_source_rows_v1(
        _full_session_rows(session),
        schedule_rows=[session],
    )
    bar = result["dataset_rows"][0]

    assert bar["open"] == "100"
    assert bar["high"] == "127"
    assert bar["low"] == "99"
    assert bar["close"] == "126"


def test_volume_aggregation_is_correct():
    session = _january_2025_schedule()[0]
    result = position.build_position_swing_bars_from_normalized_source_rows_v1(
        _full_session_rows(session),
        schedule_rows=[session],
    )

    assert result["dataset_rows"][0]["volume"] == str(sum(range(10, 36)))


def test_vwap_aggregation_is_deterministic_or_null_when_unavailable():
    session = _january_2025_schedule()[0]
    with_vwap = position.build_position_swing_bars_from_normalized_source_rows_v1(
        _full_session_rows(session),
        schedule_rows=[session],
    )
    without_vwap = position.build_position_swing_bars_from_normalized_source_rows_v1(
        _full_session_rows(session, vwap=None),
        schedule_rows=[session],
    )

    assert with_vwap["dataset_rows"][0]["vwap"] == "101"
    assert without_vwap["dataset_rows"][0]["vwap"] is None


def test_bar_at_exact_session_close_is_not_included_in_rth_source_rows():
    session = _january_2025_schedule()[0]
    rows = _full_session_rows(session)
    close = position.swing._parse_utc(session["market_close_utc"])
    rows.append(_source_row(timestamp_utc=position.swing._utc_text(close), index=99, session_date=session["session_date"]))

    result = position.build_position_swing_bars_from_normalized_source_rows_v1(rows, schedule_rows=[session])

    assert result["source_rth_rows_total"] == 26
    assert len(result["dataset_rows"]) == 1


def test_special_session_is_excluded_under_conservative_policy():
    special = {
        "session_date": "2025-01-02",
        "market_open_utc": "2025-01-02T14:30:00Z",
        "market_close_utc": "2025-01-02T18:00:00Z",
        "market_open_local": "2025-01-02T09:30:00-05:00",
        "market_close_local": "2025-01-02T13:00:00-05:00",
        "session_minutes": 210,
        "is_full_session": False,
        "is_half_session": True,
    }
    result = position.build_position_swing_bars_from_normalized_source_rows_v1(
        _full_session_rows(special)[:14],
        schedule_rows=[special],
    )

    assert result["dataset_rows"] == []
    assert result["special_session_exclusion_count"] == 1


def test_special_session_exclusion_inventory_is_populated():
    special = {
        "session_date": "2025-01-02",
        "market_open_utc": "2025-01-02T14:30:00Z",
        "market_close_utc": "2025-01-02T18:00:00Z",
        "market_open_local": "2025-01-02T09:30:00-05:00",
        "market_close_local": "2025-01-02T13:00:00-05:00",
        "session_minutes": 210,
        "is_full_session": False,
        "is_half_session": True,
    }
    result = position.build_position_swing_bars_from_normalized_source_rows_v1(
        _full_session_rows(special)[:14],
        schedule_rows=[special],
    )

    assert result["special_session_exclusion_inventory"][0]["exclusion_reason"] == position._special_session_policy()["special_session_exclusion_reason"]


def test_2025_01_fixture_with_20_full_sessions_produces_20_position_swing_bars():
    assert _ready_candidate()["2025_01_position_swing_cross_check"]["actual_position_swing_bars"] == 20


def test_dataset_digest_is_deterministic():
    assert _ready_candidate()["dataset_rows_digest"] == _ready_candidate()["dataset_rows_digest"]


def test_manifest_digest_is_deterministic():
    assert _ready_candidate()["dataset_manifest_digest"] == _ready_candidate()["dataset_manifest_digest"]


def test_candidate_digest_is_deterministic():
    assert _ready_candidate()["position_swing_candidate_semantic_digest"] == _ready_candidate()["position_swing_candidate_semantic_digest"]


def test_validator_accepts_valid_ready_candidate():
    validation = position.validate_position_swing_canonical_dataset_candidate_v1(_ready_candidate())

    assert validation["candidate_status"] == position.POSITION_SWING_CANONICAL_DATASET_READY_FOR_OPERATOR_REVIEW
    assert validation["failed_checks"] == 0


def test_validator_rejects_missing_dataset_digest_in_ready_candidate():
    candidate = _ready_candidate()
    candidate["dataset_rows_digest"] = None

    with pytest.raises(position.PositionSwingCanonicalDatasetError, match="dataset_rows_digest missing"):
        position.validate_position_swing_canonical_dataset_candidate_v1(candidate)


@pytest.mark.parametrize(
    ("field", "value", "match"),
    [
        ("canonical_eligibility", True, "canonical_eligibility"),
        ("registry_eligibility", True, "registry_eligibility"),
        ("strategy_runtime_migration", True, "strategy_runtime_migration"),
        ("runtime_use", "AUTHORIZED", "runtime_use"),
        ("strategy_use", "AUTHORIZED", "strategy_use"),
        ("provider_requests_made", True, "provider_requests_made"),
        ("in_range_dividend_implication", None, "in_range_dividend_implication"),
        ("acquisition_generation_frozen_digest", "0" * 64, "acquisition_generation_frozen_digest"),
        ("normalized_source_rows_digest", "0" * 64, "normalized_source_rows_digest"),
        ("materialization_receipt_digest", None, "materialization_receipt_digest"),
    ],
)
def test_validator_rejects_invalid_candidate_fields(field: str, value, match: str):
    candidate = _ready_candidate()
    candidate[field] = value

    with pytest.raises(position.PositionSwingCanonicalDatasetError, match=match):
        position.validate_position_swing_canonical_dataset_candidate_v1(candidate)


def test_validator_rejects_2025_01_position_swing_cross_check_mismatch():
    candidate = _ready_candidate()
    candidate["2025_01_position_swing_cross_check"]["actual_position_swing_bars"] = 19

    with pytest.raises(position.PositionSwingCanonicalDatasetError, match="2025-01 POSITION_SWING cross-check mismatch"):
        position.validate_position_swing_canonical_dataset_candidate_v1(candidate)


def test_validator_rejects_full_session_bar_with_wrong_source_row_count():
    candidate = _ready_candidate()
    candidate["dataset_rows"][0]["source_row_count"] = 25

    with pytest.raises(position.PositionSwingCanonicalDatasetError, match="source_row_count"):
        position.validate_position_swing_canonical_dataset_candidate_v1(candidate)


def test_validator_rejects_source_rth_consumed_exceeding_total():
    candidate = _ready_candidate()
    candidate["source_rth_rows_consumed"] = candidate["source_rth_rows_total"] + 1

    with pytest.raises(position.PositionSwingCanonicalDatasetError, match="source_rth_rows_consumed"):
        position.validate_position_swing_canonical_dataset_candidate_v1(candidate)


def test_validator_accepts_blocked_missing_source_candidate():
    candidate = position.build_position_swing_canonical_dataset_candidate_v1()
    validation = position.validate_position_swing_canonical_dataset_candidate_v1(candidate)

    assert candidate["candidate_status"] == position.POSITION_SWING_CANONICAL_DATASET_REQUIRES_FROZEN_ACQUISITION_ROWS
    assert validation["failed_checks"] == 0


def test_writer_writes_only_ignored_dataset_output_and_not_raw_provider_payload(tmp_path: Path):
    candidate = _ready_candidate()
    output_dir = tmp_path / ".marketflow" / "canonical_candidates" / "AAPL" / "POSITION_SWING"

    result = position.write_position_swing_canonical_dataset_candidate_outputs_v1(output_dir, candidate=candidate)

    assert Path(result["dataset_path"]).exists()
    assert ".marketflow" in Path(result["dataset_path"]).parts
    assert "raw_provider_payload" not in Path(result["dataset_path"]).read_text(encoding="utf-8")


def test_writer_requires_ignored_output(tmp_path: Path):
    with pytest.raises(position.PositionSwingCanonicalDatasetError, match=".marketflow"):
        position.write_position_swing_canonical_dataset_candidate_outputs_v1(tmp_path / "not_ignored", candidate=_ready_candidate())


def test_blocked_candidate_records_missing_row_artifact():
    candidate = position.build_position_swing_canonical_dataset_candidate_v1()

    assert candidate["source_row_artifact_available"] is False
    assert candidate["source_row_digest_matched"] is False
    assert candidate["dataset_rows_digest"] is None


def test_markdown_writer_includes_required_sections_and_guardrails():
    markdown = position.build_position_swing_canonical_dataset_candidate_markdown_v1(_ready_candidate())

    for section in (
        "## Candidate",
        "## Source Rows",
        "## Frozen Acquisition Binding",
        "## POSITION_SWING Dataset Summary",
        "## 2025-01 POSITION_SWING Cross-Check",
        "## Special-Session Policy",
        "## Dividend Implication",
        "## Authority Boundary",
        "## Guardrails",
    ):
        assert section in markdown


def test_position_swing_service_exports_are_public():
    import marketflow.services as services

    assert services.ARTIFACT_KIND_POSITION_SWING_CANONICAL_DATASET_CANDIDATE == "POSITION_SWING_CANONICAL_DATASET_CANDIDATE"
    assert services.POSITION_SWING_CANONICAL_DATASET_READY_FOR_OPERATOR_REVIEW == "POSITION_SWING_CANONICAL_DATASET_READY_FOR_OPERATOR_REVIEW"
    assert services.build_position_swing_canonical_dataset_candidate_v1 is position.build_position_swing_canonical_dataset_candidate_v1
    assert services.validate_position_swing_canonical_dataset_candidate_v1 is position.validate_position_swing_canonical_dataset_candidate_v1
    assert services.write_position_swing_canonical_dataset_candidate_outputs_v1 is position.write_position_swing_canonical_dataset_candidate_outputs_v1
