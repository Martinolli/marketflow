from __future__ import annotations

import hashlib
from pathlib import Path

import pandas as pd
import pytest

from marketflow.services.artifact_service import list_report_artifacts
from marketflow.services.walk_forward_campaign_service import (
    build_walk_forward_campaign_grouped_summary,
    write_walk_forward_campaign_artifacts,
)
from marketflow.services.walk_forward_run_registry_service import (
    NO_EVENT_FILTER,
    WALK_FORWARD_RUN_REGISTRY_CSV_KIND,
    WALK_FORWARD_RUN_REGISTRY_JSON_KIND,
    build_source_csv_fingerprint,
    build_walk_forward_run_id,
    build_walk_forward_run_metadata,
    build_walk_forward_run_coverage_reason,
    build_walk_forward_run_registry_csv_filename,
    build_walk_forward_run_registry_json_filename,
    build_walk_forward_run_signature,
    read_walk_forward_run_registry,
    normalize_walk_forward_run_coverage_status,
    refresh_walk_forward_run_registry_staleness,
    upsert_walk_forward_run_registry,
    write_walk_forward_run_registry,
    write_walk_forward_run_registry_csv,
)
from marketflow.services.walk_forward_validation_artifact_service import (
    summarize_csv_to_walk_forward_validation_artifacts,
)


def _validation_result() -> dict:
    return {
        "success": True,
        "build_result": {
            "ticker": "IONQ",
            "timeframe": "1h",
            "profile_name": "intraday_tactical",
            "row_count": 300,
            "minimum_lookback_rows": 240,
            "horizon_bars": 40,
            "case_count": 2,
        },
        "evaluation_result": {"horizon_bars": 40, "evaluated_count": 2},
        "summary": {
            "scoreable_count": 2,
            "tp_first_count": 1,
            "sl_first_count": 1,
            "neither_count": 0,
            "invalid_count": 0,
            "ambiguous_count": 0,
            "mean_realized_R": 0.5,
            "median_realized_R": 0.5,
        },
        "warnings": [],
        "errors": [],
    }


def _metadata(source: Path, artifacts: list[dict] | None = None, event_filter: str = "SPRING_WEAK") -> dict:
    return build_walk_forward_run_metadata(
        validation_result=_validation_result(),
        source_csv_path=source,
        run_event_filter=event_filter,
        step=20,
        max_cases=25,
        require_mature_future=True,
        artifacts=artifacts,
        created_at="2026-07-04T11:00:00",
    )


def _signature(**overrides) -> str:
    values = {
        "ticker": "IONQ",
        "timeframe": "1h",
        "profile_name": "intraday_tactical",
        "source_csv_sha256": "abc123",
        "run_event_filter": "SPRING_WEAK",
        "step": 20,
        "max_cases": 25,
        "require_mature_future": True,
        "horizon_bars": 40,
        "min_lookback_rows": 240,
    }
    values.update(overrides)
    return build_walk_forward_run_signature(**values)


def test_registry_filename_builders_use_ticker_and_fallback() -> None:
    assert build_walk_forward_run_registry_json_filename(ticker="IONQ") == "IONQ_walk_forward_run_registry.json"
    assert build_walk_forward_run_registry_csv_filename(ticker="IONQ") == "IONQ_walk_forward_run_registry.csv"
    assert build_walk_forward_run_registry_json_filename() == "marketflow_walk_forward_run_registry.json"
    assert build_walk_forward_run_registry_csv_filename() == "marketflow_walk_forward_run_registry.csv"


def test_source_csv_fingerprint_returns_file_metadata_and_sha256(tmp_path: Path) -> None:
    source = tmp_path / "IONQ.csv"
    source.write_bytes(b"ticker,close\nIONQ,10\n")

    result = build_source_csv_fingerprint(source)

    assert result["source_csv_exists"] is True
    assert result["source_csv_size"] == source.stat().st_size
    assert result["source_csv_mtime"] == source.stat().st_mtime
    assert result["source_csv_sha256"] == hashlib.sha256(source.read_bytes()).hexdigest()


def test_missing_source_csv_fingerprint_is_controlled(tmp_path: Path) -> None:
    result = build_source_csv_fingerprint(tmp_path / "missing.csv")

    assert result["source_csv_exists"] is False
    assert result["source_csv_sha256"] is None
    assert result["warnings"]


def test_run_signature_is_stable_for_normalized_inputs() -> None:
    first = _signature(ticker=" ionq ", profile_name="INTRADAY_TACTICAL")
    second = _signature(ticker="IONQ", profile_name="intraday_tactical")

    assert first == second
    assert len(first) == 64
    assert build_walk_forward_run_id(first) == first[:16]


def test_blank_event_filter_signature_normalizes_to_no_event_filter() -> None:
    assert _signature(run_event_filter="") == _signature(run_event_filter=NO_EVENT_FILTER)
    assert _signature(run_event_filter=None) == _signature(run_event_filter=NO_EVENT_FILTER)


@pytest.mark.parametrize(
    ("run", "expected_status", "expected_reason"),
    [
        (
            {"status": "failed", "errors": [], "case_count": 0, "run_event_filter": "SPRING_WEAK"},
            "no_matching_cases",
            "no mature rows matched requested event filter",
        ),
        (
            {"case_count": 0, "run_event_filter": "NO_EVENT_FILTER", "row_count": 100, "min_lookback_rows": 240},
            "insufficient_data",
            "insufficient source rows for selected profile/lookback",
        ),
        (
            {"case_count": 0, "run_event_filter": "NO_EVENT_FILTER", "row_count": 300, "min_lookback_rows": 240},
            "zero_cases",
            "validation completed with zero cases",
        ),
        (
            {"is_stale": True, "is_active": True},
            "stale",
            "source CSV changed or is missing",
        ),
        (
            {"is_stale": True, "is_active": False},
            "inactive",
            "run is inactive or superseded",
        ),
        (
            {"status": "failed", "errors": ["validation error"], "case_count": 0},
            "failed",
            "validation failed",
        ),
    ],
)
def test_coverage_status_and_reason_normalization(
    run: dict, expected_status: str, expected_reason: str
) -> None:
    assert normalize_walk_forward_run_coverage_status(run) == expected_status
    assert build_walk_forward_run_coverage_reason(run) == expected_reason


def test_run_metadata_contains_identity_filter_fingerprint_artifacts_and_counts(tmp_path: Path) -> None:
    source = tmp_path / "IONQ_1h_wyckoff_annotated.csv"
    source.write_text("close\n10\n", encoding="utf-8")
    artifacts = [
        {"kind": "walk_forward_results_csv", "path": str(tmp_path / "results.csv")},
        {"kind": "walk_forward_summary_csv", "path": str(tmp_path / "summary.csv")},
        {"kind": "walk_forward_cases_csv", "path": str(tmp_path / "cases.csv")},
        {"kind": "walk_forward_validation_summary_md", "path": str(tmp_path / "summary.md")},
    ]

    result = _metadata(source, artifacts)

    assert result["run_id"] == result["run_signature"][:16]
    assert result["run_event_filter"] == "SPRING_WEAK"
    assert result["source_csv_sha256"]
    assert result["artifact_paths"] == [artifact["path"] for artifact in artifacts]
    assert result["results_csv_path"].endswith("results.csv")
    assert result["case_count"] == result["evaluated_count"] == result["scoreable_count"] == 2
    assert result["status"] == "complete"
    assert result["is_stale"] is False
    assert result["is_active"] is True


def test_run_metadata_marks_event_filtered_zero_case_without_errors_as_no_matching(tmp_path: Path) -> None:
    source = tmp_path / "IONQ.csv"
    source.write_text("close\n10\n", encoding="utf-8")
    validation = _validation_result()
    validation["success"] = False
    validation["build_result"]["case_count"] = 0
    validation["evaluation_result"]["evaluated_count"] = 0
    validation["summary"]["scoreable_count"] = 0

    result = build_walk_forward_run_metadata(
        validation_result=validation,
        source_csv_path=source,
        run_event_filter="UT_WEAK",
        step=20,
        max_cases=25,
        require_mature_future=True,
    )

    assert result["errors"] == []
    assert result["status"] == "no_matching_cases"


def test_registry_read_returns_empty_runs_when_missing(tmp_path: Path) -> None:
    result = read_walk_forward_run_registry(tmp_path / "missing_registry.json")

    assert result["success"] is True
    assert result["runs"] == []


def test_registry_upsert_inserts_new_run(tmp_path: Path) -> None:
    source = tmp_path / "source.csv"
    source.write_text("close\n1\n", encoding="utf-8")
    registry = tmp_path / "IONQ_walk_forward_run_registry.json"

    result = upsert_walk_forward_run_registry(registry_path=registry, run_metadata=_metadata(source))

    assert result["success"] is True
    assert result["row_count"] == 1
    assert read_walk_forward_run_registry(registry)["runs"][0]["run_event_filter"] == "SPRING_WEAK"


def test_registry_upsert_replaces_same_run_id(tmp_path: Path) -> None:
    source = tmp_path / "source.csv"
    source.write_text("close\n1\n", encoding="utf-8")
    registry = tmp_path / "IONQ_walk_forward_run_registry.json"
    first = _metadata(source)
    upsert_walk_forward_run_registry(registry_path=registry, run_metadata=first)
    replacement = {**first, "created_at": "2026-07-04T12:00:00", "case_count": 9}

    result = upsert_walk_forward_run_registry(registry_path=registry, run_metadata=replacement)

    assert result["replaced"] is True
    assert result["row_count"] == 1
    assert result["runs"][0]["case_count"] == 9

    collision = {**replacement, "run_id": "collision-id"}
    collision_result = upsert_walk_forward_run_registry(
        registry_path=registry, run_metadata=collision
    )
    superseded = next(run for run in collision_result["runs"] if run["run_id"] == first["run_id"])
    assert collision_result["row_count"] == 2
    assert superseded["is_active"] is False
    assert superseded["status"] == "superseded"
    assert superseded["superseded_by"] == "collision-id"


def test_registry_csv_companion_is_written(tmp_path: Path) -> None:
    source = tmp_path / "source.csv"
    source.write_text("close\n1\n", encoding="utf-8")
    registry = tmp_path / "IONQ_walk_forward_run_registry.json"
    upsert_walk_forward_run_registry(registry_path=registry, run_metadata=_metadata(source))

    result = write_walk_forward_run_registry_csv(registry_json_path=registry)

    assert result["success"] is True
    assert result["kind"] == WALK_FORWARD_RUN_REGISTRY_CSV_KIND
    assert result["row_count"] == 1
    assert Path(result["path"]).exists()


def test_staleness_refresh_marks_run_stale_when_source_changes(tmp_path: Path) -> None:
    source = tmp_path / "source.csv"
    source.write_text("close\n1\n", encoding="utf-8")
    registry = tmp_path / "IONQ_walk_forward_run_registry.json"
    upsert_walk_forward_run_registry(registry_path=registry, run_metadata=_metadata(source))
    source.write_text("close\n2\n", encoding="utf-8")

    result = refresh_walk_forward_run_registry_staleness(registry)

    assert result["success"] is True
    assert result["stale_count"] == 1
    assert result["runs"][0]["is_stale"] is True


def test_artifact_classification_recognizes_registry_json_and_csv(tmp_path: Path) -> None:
    (tmp_path / "IONQ_walk_forward_run_registry.json").write_text('{"runs": []}', encoding="utf-8")
    (tmp_path / "IONQ_walk_forward_run_registry.csv").write_text("run_id\n", encoding="utf-8")

    kinds = {artifact["kind"] for artifact in list_report_artifacts(str(tmp_path))}

    assert WALK_FORWARD_RUN_REGISTRY_JSON_KIND in kinds
    assert WALK_FORWARD_RUN_REGISTRY_CSV_KIND in kinds


def test_campaign_aggregator_uses_registry_when_available(tmp_path: Path) -> None:
    source = tmp_path / "IONQ_1h_wyckoff_annotated.csv"
    source.write_text("close\n1\n", encoding="utf-8")
    results = tmp_path / "IONQ_1h_intraday_tactical_walk_forward_results_1.csv"
    summary = tmp_path / "IONQ_1h_intraday_tactical_walk_forward_summary_1.csv"
    pd.DataFrame([{"ticker": "IONQ", "timeframe": "1h", "profile_name": "intraday_tactical", "wyckoff_event": "SPRING_WEAK", "outcome": "TP_FIRST", "realized_R": 2.0}]).to_csv(results, index=False)
    pd.DataFrame([{"ticker": "IONQ", "sample_count": 1}]).to_csv(summary, index=False)
    metadata = _metadata(
        source,
        [
            {"kind": "walk_forward_results_csv", "path": str(results)},
            {"kind": "walk_forward_summary_csv", "path": str(summary)},
        ],
        event_filter="UT_WEAK",
    )
    registry = tmp_path / "IONQ_walk_forward_run_registry.json"
    duplicate = {**metadata, "run_id": "duplicate-run-id"}
    write_walk_forward_run_registry(registry, [metadata, duplicate])

    campaign = write_walk_forward_campaign_artifacts(root_dir=tmp_path, save_results_csv=False, save_report_md=False)

    assert campaign["success"] is True
    assert campaign["campaign_metadata"]["registry_mode"] == "run_registry"
    assert campaign["registry_result"]["selected_run_count"] == 1
    assert campaign["registry_result"]["ignored_duplicate_count"] == 1
    assert campaign["coverage_result"]["total_run_count"] == 2
    assert campaign["coverage_result"]["included_run_count"] == 1
    assert campaign["coverage_result"]["excluded_run_count"] == 1
    row = campaign["grouped_summary_result"]["rows"][0]
    assert row["run_event_filter"] == "UT_WEAK"
    assert row["wyckoff_event"] == "SPRING_WEAK"
    assert row["run_count"] == 1


def test_campaign_aggregator_falls_back_without_registry(tmp_path: Path) -> None:
    results = tmp_path / "IONQ_1h_intraday_tactical_walk_forward_results_1.csv"
    summary = tmp_path / "IONQ_1h_intraday_tactical_walk_forward_summary_1.csv"
    pd.DataFrame([{"ticker": "IONQ", "timeframe": "1h", "outcome": "NEITHER"}]).to_csv(results, index=False)
    pd.DataFrame([{"ticker": "IONQ", "sample_count": 1}]).to_csv(summary, index=False)

    campaign = write_walk_forward_campaign_artifacts(root_dir=tmp_path, save_results_csv=False, save_report_md=False)

    assert campaign["success"] is True
    assert campaign["campaign_metadata"]["registry_mode"] == "file_discovery"
    assert campaign["grouped_summary_result"]["rows"][0]["run_event_filter"] == "UNKNOWN_RUN_FILTER"
    assert campaign["coverage_result"]["total_run_count"] == 1
    assert campaign["coverage_result"]["rows"][0]["coverage_status"] == "complete"
    assert "limited" in campaign["coverage_result"]["warnings"][0]


def test_campaign_aggregator_writes_coverage_when_registered_run_has_no_result_rows(tmp_path: Path) -> None:
    source = tmp_path / "IONQ_1h_wyckoff_annotated.csv"
    source.write_text("close\n1\n", encoding="utf-8")
    results = tmp_path / "IONQ_1h_intraday_tactical_walk_forward_results_empty.csv"
    results.write_text("ticker,outcome,wyckoff_event\n", encoding="utf-8")
    summary = tmp_path / "IONQ_1h_intraday_tactical_walk_forward_summary_empty.csv"
    summary.write_text("ticker,sample_count\nIONQ,0\n", encoding="utf-8")
    metadata = _metadata(
        source,
        [
            {"kind": "walk_forward_results_csv", "path": str(results)},
            {"kind": "walk_forward_summary_csv", "path": str(summary)},
        ],
        event_filter="UT_WEAK",
    )
    metadata.update(
        {
            "status": "failed",
            "errors": [],
            "case_count": 0,
            "evaluated_count": 0,
            "scoreable_count": 0,
        }
    )
    registry = tmp_path / "IONQ_walk_forward_run_registry.json"
    write_walk_forward_run_registry(registry, [metadata])

    campaign = write_walk_forward_campaign_artifacts(
        root_dir=tmp_path,
        save_results_csv=False,
        save_summary_csv=False,
        save_report_md=False,
    )

    assert campaign["success"] is True
    assert campaign["grouped_summary_result"]["success"] is False
    assert campaign["coverage_result"]["no_matching_cases_count"] == 1
    assert campaign["coverage_result"]["rows"][0]["result_row_count"] == 0
    assert Path(campaign["coverage_artifact"]["path"]).exists()


def test_grouped_summary_separates_requested_filter_from_observed_event() -> None:
    frame = pd.DataFrame(
        [
            {"ticker": "IONQ", "timeframe": "1h", "profile_name": "p", "run_event_filter": "NO_EVENT_FILTER", "wyckoff_event": "SPRING_WEAK", "outcome": "TP_FIRST", "run_id": "a"},
            {"ticker": "IONQ", "timeframe": "1h", "profile_name": "p", "run_event_filter": "SPRING_WEAK", "wyckoff_event": "SPRING_WEAK", "outcome": "SL_FIRST", "run_id": "b"},
        ]
    )

    result = build_walk_forward_campaign_grouped_summary(frame)

    assert result["success"] is True
    assert len(result["rows"]) == 2
    assert {row["run_event_filter"] for row in result["rows"]} == {"NO_EVENT_FILTER", "SPRING_WEAK"}
    assert {row["wyckoff_event"] for row in result["rows"]} == {"SPRING_WEAK"}


def test_validation_artifact_save_writes_registry_and_result_run_columns(tmp_path: Path) -> None:
    source = tmp_path / "IONQ_30m_wyckoff_annotated.csv"
    rows = []
    for index in range(320):
        close = 100 + index * 0.1
        rows.append(
            {
                "timestamp": f"2026-01-{index % 28 + 1:02d} 10:{index % 60:02d}:00",
                "open": close - 0.2,
                "high": close + 2,
                "low": close - 1,
                "close": close,
                "wyckoff_phase": "C",
                "wyckoff_event": "SPRING_WEAK",
                "trend": "up",
            }
        )
    pd.DataFrame(rows).to_csv(source, index=False)

    result = summarize_csv_to_walk_forward_validation_artifacts(
        source,
        profile_name="fast_test",
        step=20,
        max_cases=3,
        event_filters=["SPRING_WEAK"],
        timestamp="20260704_120000",
    )

    assert result["success"] is True
    assert result["registry_result"]["kind"] == WALK_FORWARD_RUN_REGISTRY_JSON_KIND
    assert result["registry_csv_result"]["kind"] == WALK_FORWARD_RUN_REGISTRY_CSV_KIND
    registry_run = result["registry_result"]["runs"][0]
    assert registry_run["run_event_filter"] == "SPRING_WEAK"
    assert registry_run["step"] == 20
    assert registry_run["max_cases"] == 3
    results_path = Path(registry_run["results_csv_path"])
    result_columns = set(pd.read_csv(results_path).columns)
    assert {
        "run_id",
        "run_signature",
        "run_event_filter",
        "run_step",
        "run_max_cases",
        "run_require_mature_future",
        "source_csv_sha256",
    }.issubset(result_columns)
