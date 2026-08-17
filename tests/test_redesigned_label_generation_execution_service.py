from __future__ import annotations

import json
from copy import deepcopy
from datetime import date, timedelta
from decimal import Decimal
from unittest.mock import patch

import pytest

from marketflow.historical_data.artifacts import sha256_file
from marketflow.services import redesigned_label_generation_execution_service as execution


FIXED_TIMESTAMP = "2026-08-17T12:00:00Z"


def _business_dates(count: int) -> list[str]:
    result: list[str] = []
    current = date(2022, 1, 3)
    while len(result) < count:
        if current.weekday() < 5:
            result.append(current.isoformat())
        current += timedelta(days=1)
    return result


def _records(*, full_contract: bool) -> list[dict]:
    dates = _business_dates(1003 if full_contract else 30)
    rows: list[dict] = []
    for ticker_index, ticker in enumerate(execution.TARGET_UNIVERSE, start=1):
        ticker_dates = (
            dates[90:]
            if full_contract and ticker == "META"
            else dates
        )
        for index, value in enumerate(ticker_dates):
            close = Decimal(100 + ticker_index * 7) * (
                Decimal("1.0004") ** index
            )
            close += Decimal((index % 11) - 5) / Decimal(100)
            rows.append(
                {
                    "ticker": ticker,
                    "date": value,
                    "close": str(close),
                }
            )
    return rows


def _canonical_verification() -> dict:
    return {
        "source_root": "isolated/canonical",
        "required_source_file_count": 9,
        "required_source_files": list(execution.CANONICAL_SOURCE_FILENAMES),
        "records_digest_expected": execution.EXPECTED_RECORDS_DIGEST,
        "records_digest_actual": execution.EXPECTED_RECORDS_DIGEST,
        "records_digest_match": True,
        "total_record_count_actual": 11946,
        "per_ticker_record_counts_actual": deepcopy(
            execution.EXPECTED_RECORD_COUNTS
        ),
    }


def _design_verification() -> dict:
    return {
        "design_root": "isolated/design",
        "required_design_source_file_count": 8,
        "required_design_source_files": list(execution.DESIGN_SOURCE_FILENAMES),
        "label_objective_redesign_execution_digest": (
            execution.EXPECTED_LABEL_OBJECTIVE_REDESIGN_EXECUTION_DIGEST
        ),
        "source_label_objective_redesign_output_count": 8,
        "source_label_objective_redesign_output_status": "REVIEWED_AND_VERIFIED",
        "design_source_digests": [],
    }


def _execute(output_root, *, full_contract: bool = True) -> dict:
    source_result = (
        _canonical_verification(),
        _design_verification(),
        _records(full_contract=full_contract),
        [],
    )
    with patch.object(
        execution, "_load_and_verify_sources", return_value=source_result
    ):
        return execution.execute_redesigned_label_generation_v1(
            canonical_root=output_root.parent / "canonical",
            design_root=output_root.parent / "design",
            output_root=output_root,
            run_timestamp_utc=FIXED_TIMESTAMP,
        )


@pytest.fixture(scope="module")
def executed(tmp_path_factory):
    root = tmp_path_factory.mktemp("redesigned_label_generation_execution")
    output_root = root / "outputs"
    artifact = _execute(output_root)
    return artifact, output_root


def _validate(artifact: dict) -> dict:
    return execution.validate_redesigned_label_generation_executed_v1(artifact)


def test_execution_builds_offline(
    tmp_path, monkeypatch: pytest.MonkeyPatch
) -> None:
    def forbidden_connect(*_args, **_kwargs):
        raise AssertionError("network access is forbidden")

    monkeypatch.setattr("socket.socket.connect", forbidden_connect)
    artifact = _execute(tmp_path / "outputs", full_contract=False)
    assert artifact["created_offline"] is True
    assert artifact["provider_requests_made_in_execution"] is False
    assert artifact["live_provider_transport_enabled_in_execution"] is False
    assert artifact["market_data_acquisition_performed_in_execution"] is False


def test_execution_blocks_if_canonical_source_missing(tmp_path) -> None:
    artifact = execution.execute_redesigned_label_generation_v1(
        canonical_root=tmp_path / "missing-canonical",
        design_root=tmp_path / "missing-design",
        output_root=tmp_path / "outputs",
        run_timestamp_utc=FIXED_TIMESTAMP,
    )
    assert artifact["artifact_kind"] == "REDESIGNED_LABEL_GENERATION_BLOCKED"
    assert artifact["execution_status"] == (
        "REDESIGNED_LABEL_GENERATION_BLOCKED_MISSING_OR_INVALID_SOURCE_EVIDENCE"
    )
    assert artifact["redesigned_label_generation_digest"] == "NOT_CREATED"
    assert artifact["redesigned_label_generation_performed"] is False
    assert artifact["actual_redesigned_labels_generated"] is False
    assert artifact["generated_output_count"] == 0
    assert not (tmp_path / "outputs").exists()


def test_execution_blocks_if_design_source_missing(tmp_path) -> None:
    with patch.object(
        execution.design_execution,
        "_verify_source_root",
        return_value=(_canonical_verification(), []),
    ):
        artifact = execution.execute_redesigned_label_generation_v1(
            canonical_root=tmp_path / "canonical",
            design_root=tmp_path / "missing-design",
            output_root=tmp_path / "outputs",
            run_timestamp_utc=FIXED_TIMESTAMP,
        )
    assert artifact["artifact_kind"] == "REDESIGNED_LABEL_GENERATION_BLOCKED"
    assert artifact["generated_output_count"] == 0
    assert any(
        row["failure_id"] == "missing_design_source_file"
        for row in artifact["failures"]
    )


def test_artifact_schema_and_execution_status_are_exact(executed) -> None:
    artifact, _ = executed
    assert artifact["artifact_kind"] == "REDESIGNED_LABEL_GENERATION_EXECUTED"
    assert artifact["schema_version"] == "redesigned_label_generation_executed_v1"
    assert artifact["execution_status"] == (
        "REDESIGNED_LABEL_GENERATION_EXECUTED_RESEARCH_ONLY"
    )


@pytest.mark.parametrize(
    ("field", "expected"), list(execution._source_evidence().items())
)
def test_all_required_source_digests_are_bound(
    executed, field: str, expected: str
) -> None:
    artifact, _ = executed
    assert artifact["source_evidence"][field] == expected


def test_dataset_universe_and_counts_are_preserved(executed) -> None:
    artifact, _ = executed
    assert artifact["dataset_name"] == "expanded_universe_canonical_dataset_v1"
    assert artifact["target_universe"] == execution.TARGET_UNIVERSE
    assert artifact["target_universe_count"] == 12
    assert artifact["total_canonical_record_count"] == 11946
    assert artifact["records_digest"] == execution.EXPECTED_RECORDS_DIGEST
    assert artifact["per_ticker_record_counts"] == execution.EXPECTED_RECORD_COUNTS
    assert artifact["meta_record_count"] == 913
    assert artifact["non_meta_record_count"] == 1003
    assert artifact["meta_reduced_record_count_preserved"] is True


@pytest.mark.parametrize(
    "field",
    [
        "redesigned_label_generation_approved",
        "redesigned_label_generation_authorized",
        "ready_for_redesigned_label_generation_execution",
        "redesigned_label_generation_performed",
        "actual_redesigned_labels_generated",
        "redesigned_label_generation_results_created",
    ],
)
def test_execution_approval_authorization_and_generation_flags_are_true(
    executed, field: str
) -> None:
    artifact, _ = executed
    assert artifact[field] is True


@pytest.mark.parametrize(
    "field",
    [
        "redesigned_label_generation_manifest_created",
        "redesigned_label_input_manifest_created",
        "redesigned_label_values_created",
        "redesigned_label_family_coverage_report_created",
        "redesigned_threshold_generation_report_created",
        "redesigned_horizon_generation_report_created",
        "redesigned_label_availability_report_created",
        "per_ticker_redesigned_label_summary_created",
        "meta_limitation_preservation_report_created",
        "redesigned_label_generation_digest_manifest_created",
        "operator_review_summary_created",
    ],
)
def test_all_output_creation_flags_are_true(executed, field: str) -> None:
    artifact, _ = executed
    assert artifact[field] is True


def test_exactly_eleven_named_outputs_are_written(executed) -> None:
    artifact, output_root = executed
    assert artifact["generated_output_count"] == 11
    assert artifact["generated_output_names"] == execution.OUTPUT_FILENAMES
    assert sorted(path.name for path in output_root.iterdir()) == sorted(
        execution.OUTPUT_FILENAMES
    )


def test_all_ten_label_families_are_generated(executed) -> None:
    artifact, output_root = executed
    report = json.loads(
        (output_root / "redesigned_label_family_coverage_report.json").read_text(
            encoding="utf-8"
        )
    )
    assert artifact["label_family_count"] == 10
    assert report["label_families"] == execution.LABEL_FAMILIES
    assert {row["label_family"] for row in report["coverage_entries"]} == set(
        execution.LABEL_FAMILIES
    )


def test_threshold_report_contains_seven_training_only_strategies(executed) -> None:
    artifact, output_root = executed
    report = json.loads(
        (output_root / "redesigned_threshold_generation_report.json").read_text(
            encoding="utf-8"
        )
    )
    assert artifact["threshold_strategy_count"] == 7
    assert report["threshold_strategies"] == execution.THRESHOLD_STRATEGIES
    assert report["thresholds_derived_from_training_window_only"] is True
    assert report["threshold_optimization_performed"] is False
    assert Decimal(report["global_threshold_5_session"]) > 0
    assert set(report["per_ticker_thresholds_5_session"]) == set(
        execution.TARGET_UNIVERSE
    )
    assert set(report["volatility_adjusted_thresholds_5_session"]) == set(
        execution.TARGET_UNIVERSE
    )


def test_horizon_report_contains_all_five_strategies(executed) -> None:
    artifact, output_root = executed
    report = json.loads(
        (output_root / "redesigned_horizon_generation_report.json").read_text(
            encoding="utf-8"
        )
    )
    assert artifact["horizon_strategy_count"] == 5
    assert report["horizon_strategies"] == execution.HORIZON_STRATEGIES
    assert set(report["horizon_label_row_counts"]) == {"1", "5", "10", "20"}
    assert report["multi_horizon_values"] == [5, 10, 20]


def test_label_values_output_is_nonempty_and_has_required_fields(executed) -> None:
    artifact, output_root = executed
    path = output_root / "redesigned_label_values.jsonl"
    first = json.loads(path.open("r", encoding="utf-8").readline())
    assert artifact["label_value_row_count"] == 143352
    assert path.stat().st_size > 0
    assert set(first) == {
        "ticker",
        "date",
        "record_index_for_ticker",
        "window_partition",
        "label_family",
        "horizon",
        "forward_return",
        "label_value",
        "label_available",
        "availability_reason",
        "threshold_strategy",
        "threshold_value_used",
        "benchmark_basis",
        "meta_reduced_record_count_flag",
        "research_only",
        "non_actionable",
    }
    assert first["research_only"] is True
    assert first["non_actionable"] is True


def test_available_and_unavailable_counts_are_recorded(executed) -> None:
    artifact, output_root = executed
    report = json.loads(
        (output_root / "redesigned_label_availability_report.json").read_text(
            encoding="utf-8"
        )
    )
    assert artifact["available_label_value_count"] == 142200
    assert artifact["unavailable_label_value_count"] == 1152
    assert report["available_label_value_count"] == 142200
    assert report["unavailable_label_value_count"] == 1152
    assert report["available_label_value_count"] + report[
        "unavailable_label_value_count"
    ] == artifact["label_value_row_count"]


def test_forward_tail_unavailable_labels_are_null(executed) -> None:
    _, output_root = executed
    found = False
    with (output_root / "redesigned_label_values.jsonl").open(
        "r", encoding="utf-8"
    ) as handle:
        for line in handle:
            row = json.loads(line)
            if not row["label_available"]:
                found = True
                assert row["forward_return"] is None
                assert row["label_value"] is None
                assert row["availability_reason"] == "INSUFFICIENT_FUTURE_BARS"
                break
    assert found is True


def test_window_partitions_are_date_bounded(executed) -> None:
    _, output_root = executed
    seen = set()
    with (output_root / "redesigned_label_values.jsonl").open(
        "r", encoding="utf-8"
    ) as handle:
        for line in handle:
            row = json.loads(line)
            seen.add(row["window_partition"])
    assert seen == {"TRAINING", "VALIDATION", "OOS"}


def test_per_ticker_summary_preserves_counts_and_order(executed) -> None:
    _, output_root = executed
    report = json.loads(
        (output_root / "per_ticker_redesigned_label_summary.json").read_text(
            encoding="utf-8"
        )
    )
    rows = report["per_ticker_label_summary"]
    assert [row["ticker"] for row in rows] == execution.TARGET_UNIVERSE
    assert all(
        row["historical_record_count"]
        == execution.EXPECTED_RECORD_COUNTS[row["ticker"]]
        for row in rows
    )
    assert sum(row["label_value_row_count"] for row in rows) == 143352


def test_meta_limitation_is_preserved_without_synthetic_rows(executed) -> None:
    _, output_root = executed
    report = json.loads(
        (output_root / "meta_limitation_preservation_report.json").read_text(
            encoding="utf-8"
        )
    )
    assert report["ticker"] == "META"
    assert report["historical_record_count"] == 913
    assert report["expected_historical_record_count"] == 913
    assert report["meta_reduced_record_count_preserved"] is True
    assert report["no_backfill"] is True
    assert report["no_repair"] is True
    assert report["no_synthetic_rows"] is True
    assert report["calendar_inference_performed"] is False


def test_output_digest_manifest_is_complete_and_matches_files(executed) -> None:
    artifact, output_root = executed
    entries = artifact["output_digest_manifest"]
    assert len(entries) == 11
    assert [row["filename"] for row in entries] == execution.OUTPUT_FILENAMES
    for row in entries:
        if row["filename"] in {
            "redesigned_label_generation_execution_manifest.json",
            "redesigned_label_generation_digest_manifest.json",
        }:
            assert row["sha256"] is None
        else:
            assert row["digest_kind"] == "FILE_SHA256"
            assert row["sha256"] == sha256_file(output_root / row["filename"])


def test_digest_manifest_file_records_execution_digest(executed) -> None:
    artifact, output_root = executed
    report = json.loads(
        (output_root / "redesigned_label_generation_digest_manifest.json").read_text(
            encoding="utf-8"
        )
    )
    assert report["redesigned_label_generation_execution_digest"] == artifact[
        "redesigned_label_generation_execution_digest"
    ]
    assert report["output_digest_manifest"] == artifact["output_digest_manifest"]


def test_operator_summary_awaits_separate_results_review(executed) -> None:
    _, output_root = executed
    report = json.loads(
        (output_root / "operator_review_summary.json").read_text(encoding="utf-8")
    )
    assert report["review_status"] == "AWAITING_SEPARATE_RESULTS_REVIEW"
    assert report["operator_decision"] is None
    assert report["results_review_created"] is False


@pytest.mark.parametrize(
    "field",
    [
        "provider_requests_made_in_execution",
        "live_provider_transport_enabled_in_execution",
        "market_data_acquisition_performed_in_execution",
        "dataset_generation_performed_in_execution",
        "canonical_dataset_regenerated_in_execution",
        "label_objective_redesign_execution_rerun_performed",
        "redesigned_feature_generation_authorized",
        "redesigned_feature_generation_performed",
        "redesigned_protocol_evaluation_authorized",
        "redesigned_protocol_evaluation_performed",
        "feature_generation_performed",
        "metric_recomputation_performed",
        "model_training_performed",
        "additional_predictive_evidence_execution_candidate_created",
        "additional_predictive_evidence_execution_authorized",
        "additional_predictive_evidence_executed",
        "new_strategy_scoring_performed",
        "trade_recommendations_generated",
    ],
)
def test_all_forbidden_execution_actions_remain_false(executed, field: str) -> None:
    artifact, _ = executed
    assert artifact[field] is False


def test_predictive_profitability_runtime_and_trading_remain_closed(
    executed,
) -> None:
    artifact, _ = executed
    assert artifact["predictive_usefulness"] == "not accepted"
    assert artifact["predictive_usefulness_acceptance_candidate_created"] is False
    assert artifact["profitability"] == "not accepted"
    assert artifact["runtime_migration_approved"] is False
    assert artifact["runtime_migration_active"] is False
    for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
        assert artifact[field] == "NOT_AUTHORIZED"


def test_execution_checklist_and_summary_pass(executed) -> None:
    artifact, _ = executed
    assert len(artifact["execution_checklist"]) == len(execution.CHECK_IDS) == 45
    assert all(row["status"] == "PASS" for row in artifact["execution_checklist"])
    summary = artifact["execution_summary"]
    assert summary["total_checks"] == 45
    assert summary["passed_checks"] == 45
    assert summary["failed_checks"] == 0
    assert summary["blocker_count"] == 0
    assert summary["failure_count"] == 0


def test_validator_accepts_valid_artifact(executed) -> None:
    artifact, _ = executed
    validation = _validate(deepcopy(artifact))
    assert validation["status"] == "REDESIGNED_LABEL_GENERATION_EXECUTION_VALID"
    assert validation["redesigned_label_generation_performed"] is True
    assert validation["actual_redesigned_labels_generated"] is True
    assert validation["feature_generation_performed"] is False


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("artifact_kind", "WRONG"),
        ("execution_status", "WRONG"),
        ("redesigned_label_generation_approved", False),
        ("redesigned_label_generation_authorized", False),
        ("ready_for_redesigned_label_generation_execution", False),
        ("redesigned_label_generation_performed", False),
        ("actual_redesigned_labels_generated", False),
        ("redesigned_label_generation_results_created", False),
        ("generated_output_count", 10),
        ("target_universe_count", 11),
        ("records_digest", "0" * 64),
        ("meta_record_count", 1003),
        ("label_family_count", 9),
        ("threshold_strategy_count", 6),
        ("horizon_strategy_count", 4),
        ("label_value_row_count", 0),
        ("redesigned_feature_generation_authorized", True),
        ("metric_recomputation_performed", True),
        ("model_training_performed", True),
        ("additional_predictive_evidence_execution_candidate_created", True),
        ("predictive_usefulness", "accepted"),
        ("profitability", "accepted"),
        ("runtime_use", "AUTHORIZED"),
        ("strategy_use", "AUTHORIZED"),
        ("paper_trading", "AUTHORIZED"),
        ("broker_execution", "AUTHORIZED"),
        ("trade_recommendations_generated", True),
    ],
)
def test_validator_rejects_wrong_or_forbidden_state(
    executed, field: str, value: object
) -> None:
    artifact, _ = executed
    mutated = deepcopy(artifact)
    mutated[field] = value
    with pytest.raises(execution.RedesignedLabelGenerationExecutionError):
        _validate(mutated)


def test_validator_rejects_missing_approval_digest(executed) -> None:
    artifact, _ = executed
    mutated = deepcopy(artifact)
    mutated["source_evidence"].pop(
        "redesigned_label_generation_approval_digest"
    )
    with pytest.raises(execution.RedesignedLabelGenerationExecutionError):
        _validate(mutated)


def test_validator_rejects_missing_execution_digest(executed) -> None:
    artifact, _ = executed
    mutated = deepcopy(artifact)
    mutated.pop("redesigned_label_generation_execution_digest")
    with pytest.raises(execution.RedesignedLabelGenerationExecutionError):
        _validate(mutated)


def test_execution_digest_is_deterministic_for_fixed_source_and_timestamp(
    tmp_path,
) -> None:
    first = _execute(tmp_path / "first", full_contract=False)
    second = _execute(tmp_path / "second", full_contract=False)
    assert first["redesigned_label_generation_execution_digest"] == second[
        "redesigned_label_generation_execution_digest"
    ]


def test_output_root_must_be_empty(tmp_path) -> None:
    root = tmp_path / "outputs"
    root.mkdir()
    (root / "existing.txt").write_text("occupied", encoding="utf-8")
    with pytest.raises(execution.RedesignedLabelGenerationExecutionError):
        _execute(root, full_contract=False)


def test_markdown_includes_required_sections(executed) -> None:
    artifact, _ = executed
    markdown = execution.build_redesigned_label_generation_execution_status_markdown_v1(
        artifact
    )
    for heading in [
        "## Title",
        "## Redesigned Label Generation Execution",
        "## Source Approval",
        "## Dataset and Universe",
        "## Source Design Artifacts",
        "## Label Generation Policy",
        "## Generated Label Families",
        "## Threshold Strategy Summary",
        "## Horizon Strategy Summary",
        "## Label Availability Summary",
        "## Per-Ticker Summary",
        "## META Limitation Preservation",
        "## Output Digest Manifest",
        "## Execution Boundary",
        "## Predictive Usefulness Boundary",
        "## Profitability Boundary",
        "## Runtime Boundary",
        "## Checklist Summary",
        "## Guardrails",
    ]:
        assert heading in markdown
