from __future__ import annotations

import json
from copy import deepcopy
from datetime import date, timedelta
from decimal import Decimal
from pathlib import Path

import pytest

from marketflow.historical_data.artifacts import canonical_json_bytes, sha256_file
from marketflow.services import additional_predictive_evidence_execution_service as execution


def _business_dates() -> list[str]:
    values: list[str] = []
    current = date(2022, 1, 3)
    while current <= date(2025, 12, 31):
        if current.weekday() < 5:
            values.append(current.isoformat())
        current += timedelta(days=1)
    return values


def _write_json(path: Path, payload: dict) -> None:
    path.write_bytes(canonical_json_bytes(payload))


def _build_synthetic_source(root: Path) -> tuple[str, dict[str, str]]:
    root.mkdir(parents=True)
    dates = _business_dates()
    records_path = root / "canonical_dataset_records.jsonl"
    with records_path.open("wb") as handle:
        for ticker_index, ticker in enumerate(execution.TARGET_UNIVERSE):
            count = execution.EXPECTED_RECORD_COUNTS[ticker]
            for index, session_date in enumerate(dates[:count]):
                close = Decimal("100") + Decimal(ticker_index * 7) + Decimal(index) / Decimal("10")
                close += Decimal((index % 11) - 5) / Decimal("20")
                open_value = close - Decimal((index % 3) - 1) / Decimal("10")
                row = {
                    "ticker": ticker,
                    "date": session_date,
                    "timestamp_utc_or_session_date": f"{session_date}T05:00:00Z",
                    "open": format(open_value, "f"),
                    "high": format(max(open_value, close) + Decimal("1"), "f"),
                    "low": format(min(open_value, close) - Decimal("1"), "f"),
                    "close": format(close, "f"),
                    "volume": str(1_000_000 + ticker_index * 1000 + index * 100),
                    "transactions_if_available": str(10_000 + index),
                    "vwap_if_available": format((open_value + close) / Decimal("2"), "f"),
                    "adjustment_policy_status": "PROVIDER_ADJUSTED_TRUE_COMBINED_POLICY_NOT_DISAGGREGATED",
                    "calendar_session_status": "NOT_EVALUATED_BY_SELECTED_ENDPOINT",
                    "source_profile": "RTH_FULL_SESSION_1D",
                    "source_provider": "SYNTHETIC_TEST_FIXTURE",
                    "source_endpoint_mode": "OFFLINE_TEST_FIXTURE",
                }
                handle.write(canonical_json_bytes(row) + b"\n")

    _write_json(
        root / "canonical_dataset_generation_run_manifest.json",
        {
            "canonical_dataset_generation_digest": execution.EXPECTED_CANONICAL_DATASET_GENERATION_DIGEST,
            "target_universe": execution.TARGET_UNIVERSE,
            "total_canonical_record_count": 11946,
        },
    )
    _write_json(root / "canonical_dataset_source_evidence_manifest.json", {"fixture": True})
    _write_json(root / "canonical_dataset_schema_contract.json", {"fixture": True})
    _write_json(
        root / "per_ticker_canonical_dataset_summary.json",
        {
            "target_universe": execution.TARGET_UNIVERSE,
            "total_canonical_record_count": 11946,
            "per_ticker_canonical_record_summary": [
                {
                    "ticker": ticker,
                    "canonical_record_count": execution.EXPECTED_RECORD_COUNTS[ticker],
                    "meta_reduced_bar_count_preserved": ticker == "META",
                }
                for ticker in execution.TARGET_UNIVERSE
            ],
        },
    )
    _write_json(
        root / "canonical_dataset_data_quality_report.json",
        {"quality_status": "PASS_WITH_PRESERVED_SOURCE_LIMITATION"},
    )
    _write_json(root / "canonical_dataset_failure_reason_inventory.json", {"failure_count": 0})
    _write_json(root / "operator_review_summary.json", {"operator_review_required": True})

    source_names = [
        name
        for name in execution.REQUIRED_SOURCE_FILENAMES
        if name != "canonical_dataset_digest_manifest.json"
    ]
    file_hashes = {name: sha256_file(root / name) for name in source_names}
    entries = [
        {"digest_kind": "FILE_SHA256", "filename": name, "sha256": file_hashes[name]}
        for name in source_names
    ]
    entries.append(
        {
            "digest_kind": "SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE",
            "filename": "canonical_dataset_digest_manifest.json",
            "sha256": None,
        }
    )
    _write_json(
        root / "canonical_dataset_digest_manifest.json",
        {"canonical_output_digest_manifest": entries},
    )
    file_hashes["canonical_dataset_digest_manifest.json"] = sha256_file(
        root / "canonical_dataset_digest_manifest.json"
    )
    return file_hashes["canonical_dataset_records.jsonl"], file_hashes


@pytest.fixture(scope="module")
def executed_run(tmp_path_factory: pytest.TempPathFactory):
    root = tmp_path_factory.mktemp("additional-predictive-source")
    source_root = root / "canonical"
    output_root = root / "output"
    records_digest, source_hashes = _build_synthetic_source(source_root)
    patcher = pytest.MonkeyPatch()
    patcher.setattr(execution, "EXPECTED_RECORDS_DIGEST", records_digest)
    artifact = execution.execute_additional_predictive_evidence_v1(
        source_root=source_root,
        output_root=output_root,
        run_timestamp_utc="2026-08-15T00:00:00Z",
    )
    yield {
        "artifact": artifact,
        "source_root": source_root,
        "output_root": output_root,
        "source_hashes": source_hashes,
        "records_digest": records_digest,
    }
    patcher.undo()


def test_execution_builds_offline_without_provider_calls(
    executed_run, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
):
    from marketflow.services import acquisition_generation_service as acquisition

    def fail_provider_call(*_args, **_kwargs):  # pragma: no cover
        raise AssertionError("provider path must not be called")

    monkeypatch.setattr(acquisition, "fetch_massive_custom_bars_v1", fail_provider_call)
    artifact = execution.execute_additional_predictive_evidence_v1(
        source_root=executed_run["source_root"],
        output_root=tmp_path / "second-output",
        run_timestamp_utc="2026-08-15T00:00:00Z",
    )

    assert artifact["created_offline"] is True
    assert artifact["provider_requests_made_in_execution"] is False
    assert artifact["live_provider_transport_enabled_in_execution"] is False


def test_execution_blocks_when_canonical_dataset_source_is_missing(tmp_path: Path):
    artifact = execution.execute_additional_predictive_evidence_v1(
        source_root=tmp_path / "missing",
        output_root=tmp_path / "output",
        run_timestamp_utc="2026-08-15T00:00:00Z",
    )

    assert artifact["artifact_kind"] == execution.ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_BLOCKED
    assert (
        artifact["execution_status"]
        == execution.ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_BLOCKED_MISSING_OR_INVALID_CANONICAL_DATASET
    )
    assert artifact["additional_predictive_evidence_execution_digest"] == "NOT_CREATED"
    assert artifact["additional_predictive_evidence_executed"] is False
    assert artifact["generated_output_count"] == 0
    assert not (tmp_path / "output").exists()


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("artifact_kind", execution.ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED),
        ("execution_status", execution.ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED_RESEARCH_ONLY),
        ("additional_predictive_evidence_execution_approved", True),
        ("additional_predictive_evidence_execution_authorized", True),
        ("additional_predictive_evidence_executed", True),
        ("additional_predictive_evidence_results_created", True),
        ("label_generation_authorized", True),
        ("label_generation_performed", True),
        ("feature_matrix_generation_authorized", True),
        ("feature_matrix_generation_performed", True),
        ("walk_forward_validation_authorized", True),
        ("walk_forward_validation_performed", True),
        ("out_of_sample_evaluation_authorized", True),
        ("out_of_sample_evaluation_performed", True),
        ("baseline_comparison_authorized", True),
        ("baseline_comparison_performed", True),
        ("signal_quality_metrics_authorized", True),
        ("signal_quality_metrics_performed", True),
        ("stability_analysis_authorized", True),
        ("stability_analysis_performed", True),
        ("leakage_control_review_authorized", True),
        ("leakage_control_review_performed", True),
        ("predictive_experiment_rerun_authorized", True),
        ("predictive_experiment_rerun_performed", True),
        ("label_family_count", 7),
        ("feature_family_count", 10),
        ("metric_family_count", 9),
        ("baseline_count", 6),
        ("generated_output_count", 15),
        ("target_universe_count", 12),
        ("total_canonical_record_count", 11946),
        ("meta_record_count", 913),
        ("non_meta_record_count", 1003),
        ("provider_requests_made_in_execution", False),
        ("live_provider_transport_enabled_in_execution", False),
        ("market_data_acquisition_performed_in_execution", False),
        ("dataset_generation_performed_in_execution", False),
        ("canonical_dataset_regenerated_in_execution", False),
        ("raw_provider_payloads_committed", False),
        ("api_keys_stored_or_printed", False),
        ("new_strategy_scoring_performed", False),
        ("trade_recommendations_generated", False),
        ("predictive_usefulness", execution.NOT_ACCEPTED),
        ("predictive_usefulness_acceptance_candidate_created", False),
        ("profitability", execution.NOT_ACCEPTED),
        ("runtime_migration_approved", False),
        ("runtime_migration_active", False),
        ("runtime_use", execution.NOT_AUTHORIZED),
        ("strategy_use", execution.NOT_AUTHORIZED),
        ("paper_trading", execution.NOT_AUTHORIZED),
        ("broker_execution", execution.NOT_AUTHORIZED),
        ("automatic_stitching", False),
    ],
)
def test_executed_artifact_fields(executed_run, field: str, expected):
    assert executed_run["artifact"][field] == expected


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("additional_predictive_evidence_execution_approval_digest", execution.EXPECTED_EXECUTION_APPROVAL_DIGEST),
        ("additional_predictive_evidence_execution_candidate_review_package_digest", execution.EXPECTED_EXECUTION_CANDIDATE_REVIEW_PACKAGE_DIGEST),
        ("additional_predictive_evidence_execution_candidate_digest", execution.EXPECTED_EXECUTION_CANDIDATE_DIGEST),
        ("additional_predictive_evidence_chain_candidate_review_package_digest", execution.EXPECTED_CHAIN_CANDIDATE_REVIEW_PACKAGE_DIGEST),
        ("additional_predictive_evidence_chain_candidate_digest", execution.EXPECTED_CHAIN_CANDIDATE_DIGEST),
        ("research_registry_approval_digest", execution.EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST),
        ("canonical_dataset_freeze_digest", execution.EXPECTED_CANONICAL_DATASET_FREEZE_DIGEST),
        ("canonical_dataset_generation_digest", execution.EXPECTED_CANONICAL_DATASET_GENERATION_DIGEST),
    ],
)
def test_source_evidence_digests_are_bound(executed_run, field: str, expected: str):
    assert executed_run["artifact"]["source_evidence"][field] == expected


def test_target_universe_and_record_counts_are_exact(executed_run):
    artifact = executed_run["artifact"]

    assert artifact["target_universe"] == execution.TARGET_UNIVERSE
    assert artifact["per_ticker_record_counts"] == execution.EXPECTED_RECORD_COUNTS
    assert artifact["per_ticker_record_counts"]["META"] == 913
    assert all(
        count == 1003
        for ticker, count in artifact["per_ticker_record_counts"].items()
        if ticker != "META"
    )
    assert artifact["records_digest"] == executed_run["records_digest"]


def test_all_fifteen_outputs_are_written_and_labeled_research_only(executed_run):
    files = sorted(path.name for path in executed_run["output_root"].iterdir())

    assert files == sorted(execution.OUTPUT_FILENAMES)
    for filename in files:
        payload = json.loads((executed_run["output_root"] / filename).read_text(encoding="utf-8"))
        assert payload["output_label"] == execution.RESEARCH_ONLY_NON_ACTIONABLE
        assert payload["evidence_scope"] == execution.EVIDENCE_SCOPE
        assert payload["predictive_usefulness"] == execution.NOT_ACCEPTED
        assert payload["profitability"] == execution.NOT_ACCEPTED
        assert payload["runtime_use"] == execution.NOT_AUTHORIZED
        assert payload["trade_recommendations_generated"] is False


def test_output_digest_manifest_includes_every_output(executed_run):
    root = executed_run["output_root"]
    manifest = json.loads((root / "execution_digest_manifest.json").read_text(encoding="utf-8"))
    entries = manifest["output_digest_entries"]

    assert len(entries) == 15
    assert [entry["filename"] for entry in entries] == execution.OUTPUT_FILENAMES
    for entry in entries:
        if entry["filename"] == "execution_digest_manifest.json":
            assert entry["digest_kind"] == "SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE"
            assert entry["sha256"] is None
        else:
            assert entry["sha256"] == sha256_file(root / entry["filename"])


def test_label_generation_manifest_records_forward_only_labels_and_thresholds(executed_run):
    payload = json.loads(
        (executed_run["output_root"] / "label_generation_manifest.json").read_text(
            encoding="utf-8"
        )
    )

    assert payload["label_families"] == execution.LABEL_FAMILIES
    assert payload["forward_labels_only"] is True
    assert payload["future_label_values_used_as_features"] is False
    assert payload["threshold_policy"] == "FIXED_THRESHOLDS_RECORDED_EXPLICITLY"
    assert len(payload["label_coverage"]) == 84
    assert len(payload["label_generation_digest"]) == 64


def test_feature_manifest_and_quality_report_are_history_only(executed_run):
    root = executed_run["output_root"]
    manifest = json.loads((root / "feature_matrix_manifest.json").read_text(encoding="utf-8"))
    quality = json.loads((root / "feature_quality_report.json").read_text(encoding="utf-8"))

    assert manifest["feature_families"] == execution.FEATURE_FAMILIES
    assert manifest["feature_family_count"] == 10
    assert manifest["feature_matrix_row_count"] == 11946
    assert manifest["current_and_historical_inputs_only"] is True
    assert manifest["future_information_used"] is False
    assert len(manifest["feature_matrix_digest"]) == 64
    assert len(quality["feature_coverage"]) == 120


def test_walk_forward_and_out_of_sample_reports_are_chronological(executed_run):
    root = executed_run["output_root"]
    walk = json.loads((root / "walk_forward_results_report.json").read_text(encoding="utf-8"))
    oos = json.loads((root / "out_of_sample_results_report.json").read_text(encoding="utf-8"))

    assert walk["fold_count"] == 4
    assert walk["shuffle"] is False
    assert [fold["fold_id"] for fold in walk["folds"]] == [
        "2024_Q1",
        "2024_Q2",
        "2024_Q3",
        "2024_Q4",
    ]
    assert oos["chronological_holdout"] is True
    assert oos["shuffle"] is False
    assert oos["results"]["overall"]["evaluation_count"] > 0


def test_baselines_metrics_calibration_stability_and_leakage_are_recorded(executed_run):
    root = executed_run["output_root"]
    baseline = json.loads((root / "baseline_comparison_report.json").read_text(encoding="utf-8"))
    calibration = json.loads((root / "calibration_report.json").read_text(encoding="utf-8"))
    stability = json.loads((root / "stability_analysis_report.json").read_text(encoding="utf-8"))
    leakage = json.loads((root / "leakage_control_report.json").read_text(encoding="utf-8"))

    assert baseline["baselines"] == execution.BASELINES
    assert baseline["baseline_count"] == 6
    assert baseline["random_baseline_policy"] == "DETERMINISTIC_SHA256_CLASS_SELECTION"
    assert baseline["buy_hold_reference_only_is_trade_recommendation"] is False
    assert calibration["calibration_metrics"]["out_of_sample_brier_score"] is not None
    assert set(stability["stability_metrics"]) == set(execution.BASELINES)
    assert leakage["leakage_control_status"] == "PASS"
    assert leakage["failed_control_count"] == 0


def test_data_quality_preserves_meta_limitation_with_zero_failures(executed_run):
    payload = json.loads(
        (executed_run["output_root"] / "data_quality_report.json").read_text(
            encoding="utf-8"
        )
    )

    assert payload["quality_status"] == "PASS_WITH_PRESERVED_SOURCE_LIMITATION"
    assert payload["failure_count"] == 0
    assert payload["warning_count"] == 1
    assert payload["meta_record_count"] == 913
    assert payload["meta_reduced_record_count_preserved"] is True
    assert payload[
        "meta_records_repaired_inferred_smoothed_normalized_backfilled_or_fabricated"
    ] is False


def test_execution_does_not_modify_source_files(executed_run):
    after = {
        name: sha256_file(executed_run["source_root"] / name)
        for name in execution.REQUIRED_SOURCE_FILENAMES
    }
    assert after == executed_run["source_hashes"]


def test_validator_accepts_valid_executed_artifact(executed_run):
    result = execution.validate_additional_predictive_evidence_executed_v1(
        executed_run["artifact"]
    )

    assert result["status"] == "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED_VALID"
    assert result["generated_output_count"] == 15
    assert result["failure_count"] == 0


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("artifact_kind", "WRONG"),
        ("execution_status", "WRONG"),
        ("additional_predictive_evidence_execution_approved", False),
        ("additional_predictive_evidence_execution_authorized", False),
        ("additional_predictive_evidence_executed", False),
        ("additional_predictive_evidence_results_created", False),
        ("label_generation_authorized", False),
        ("label_generation_performed", False),
        ("feature_matrix_generation_authorized", False),
        ("feature_matrix_generation_performed", False),
        ("walk_forward_validation_authorized", False),
        ("walk_forward_validation_performed", False),
        ("out_of_sample_evaluation_authorized", False),
        ("out_of_sample_evaluation_performed", False),
        ("baseline_comparison_authorized", False),
        ("baseline_comparison_performed", False),
        ("signal_quality_metrics_authorized", False),
        ("signal_quality_metrics_performed", False),
        ("stability_analysis_authorized", False),
        ("stability_analysis_performed", False),
        ("leakage_control_review_authorized", False),
        ("leakage_control_review_performed", False),
        ("predictive_experiment_rerun_authorized", False),
        ("predictive_experiment_rerun_performed", False),
        ("label_family_count", 6),
        ("feature_family_count", 9),
        ("metric_family_count", 8),
        ("baseline_count", 5),
        ("generated_output_count", 14),
        ("target_universe_count", 11),
        ("total_canonical_record_count", 11945),
        ("meta_record_count", 1003),
        ("provider_requests_made_in_execution", True),
        ("live_provider_transport_enabled_in_execution", True),
        ("dataset_generation_performed_in_execution", True),
        ("canonical_dataset_regenerated_in_execution", True),
        ("new_strategy_scoring_performed", True),
        ("trade_recommendations_generated", True),
        ("predictive_usefulness", "accepted"),
        ("predictive_usefulness_acceptance_candidate_created", True),
        ("profitability", "accepted"),
        ("runtime_migration_approved", True),
        ("runtime_use", "AUTHORIZED"),
        ("strategy_use", "AUTHORIZED"),
        ("paper_trading", "AUTHORIZED"),
        ("broker_execution", "AUTHORIZED"),
        ("automatic_stitching", True),
    ],
)
def test_validator_rejects_invalid_mutations(executed_run, field: str, value):
    artifact = deepcopy(executed_run["artifact"])
    artifact[field] = value

    with pytest.raises(execution.AdditionalPredictiveEvidenceExecutionError):
        execution.validate_additional_predictive_evidence_executed_v1(artifact)


def test_validator_rejects_records_digest_and_non_meta_count_mutations(executed_run):
    artifact = deepcopy(executed_run["artifact"])
    artifact["records_digest"] = "0" * 64
    with pytest.raises(execution.AdditionalPredictiveEvidenceExecutionError):
        execution.validate_additional_predictive_evidence_executed_v1(artifact)

    artifact = deepcopy(executed_run["artifact"])
    artifact["per_ticker_record_counts"]["MSFT"] = 1002
    with pytest.raises(execution.AdditionalPredictiveEvidenceExecutionError):
        execution.validate_additional_predictive_evidence_executed_v1(artifact)


def test_execution_digest_is_deterministic_for_fixed_timestamp_and_source(
    executed_run, tmp_path: Path
):
    second = execution.execute_additional_predictive_evidence_v1(
        source_root=executed_run["source_root"],
        output_root=tmp_path / "deterministic-output",
        run_timestamp_utc="2026-08-15T00:00:00Z",
    )
    assert (
        second["additional_predictive_evidence_execution_digest"]
        == executed_run["artifact"]["additional_predictive_evidence_execution_digest"]
    )


def test_execution_refuses_to_overwrite_existing_output(executed_run):
    with pytest.raises(
        execution.AdditionalPredictiveEvidenceExecutionError, match="not empty"
    ):
        execution.execute_additional_predictive_evidence_v1(
            source_root=executed_run["source_root"],
            output_root=executed_run["output_root"],
            run_timestamp_utc="2026-08-15T00:00:00Z",
        )


def test_status_markdown_includes_required_sections(executed_run):
    markdown = execution.build_additional_predictive_evidence_execution_status_markdown_v1(
        executed_run["artifact"]
    )

    for heading in (
        "## Title",
        "## Additional Predictive Evidence Execution",
        "## Source Execution Approval",
        "## Registry-Approved Dataset Metadata",
        "## Target Universe",
        "## Label Generation Summary",
        "## Feature Generation Summary",
        "## Walk-Forward Validation Summary",
        "## Out-of-Sample Evaluation Summary",
        "## Baseline Comparison Summary",
        "## Metric Summary",
        "## Calibration Summary",
        "## Stability Summary",
        "## Leakage-Control Summary",
        "## Data Quality Summary",
        "## Output Digest Manifest",
        "## Predictive Usefulness Boundary",
        "## Profitability Boundary",
        "## Runtime Boundary",
        "## Checklist Summary",
        "## Guardrails",
    ):
        assert heading in markdown


def test_execution_service_exports_are_public():
    import marketflow.services as services

    for name in (
        "ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED",
        "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED_RESEARCH_ONLY",
        "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_BLOCKED_MISSING_OR_INVALID_CANONICAL_DATASET",
        "execute_additional_predictive_evidence_v1",
        "validate_additional_predictive_evidence_executed_v1",
        "build_additional_predictive_evidence_execution_status_markdown_v1",
        "additional_predictive_evidence_execution_digest_v1",
    ):
        assert name in services.__all__
        assert hasattr(services, name)
