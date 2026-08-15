from __future__ import annotations

from copy import deepcopy
from datetime import date, timedelta
import json
from pathlib import Path
from unittest.mock import patch

import pytest

from marketflow.historical_data.artifacts import sha256_file
from marketflow.services import feature_label_refinement_execution_service as execution


FIXED_TIMESTAMP = "2026-08-15T16:00:00Z"


def _business_dates(count: int) -> list[str]:
    values: list[str] = []
    current = date(2022, 1, 3)
    while len(values) < count:
        if current.weekday() < 5:
            values.append(current.isoformat())
        current += timedelta(days=1)
    return values


@pytest.fixture(scope="module")
def fixture_rows() -> dict[str, list[dict]]:
    dates = _business_dates(1003)
    rows_by_ticker: dict[str, list[dict]] = {}
    for ticker_index, ticker in enumerate(execution.TARGET_UNIVERSE):
        count = execution.EXPECTED_RECORD_COUNTS[ticker]
        rows = []
        for index, date_text in enumerate(dates[:count]):
            direction = -1 if index % 5 == 0 else 1
            base = 100 + ticker_index + (index * 0.05)
            close = base + (direction * 0.3)
            rows.append(
                {
                    "ticker": ticker,
                    "date": date_text,
                    "timestamp_utc_or_session_date": f"{date_text}T05:00:00Z",
                    "open": f"{base:.4f}",
                    "high": f"{base + 1:.4f}",
                    "low": f"{base - 1:.4f}",
                    "close": f"{close:.4f}",
                    "volume": str(1_000_000 + index),
                    "vwap_if_available": f"{base:.4f}",
                    "adjustment_policy_status": (
                        "PROVIDER_ADJUSTED_TRUE_COMBINED_POLICY_NOT_DISAGGREGATED"
                    ),
                }
            )
        rows_by_ticker[ticker] = rows
    return rows_by_ticker


def _source_verification() -> dict:
    return {
        "source_root": "fixture",
        "required_source_file_count": len(execution.REQUIRED_SOURCE_FILENAMES),
        "required_source_files": list(execution.REQUIRED_SOURCE_FILENAMES),
        "records_digest_expected": execution.EXPECTED_RECORDS_DIGEST,
        "records_digest_actual": execution.EXPECTED_RECORDS_DIGEST,
        "records_digest_match": True,
        "canonical_dataset_generation_digest": (
            execution.EXPECTED_CANONICAL_DATASET_GENERATION_DIGEST
        ),
        "digest_manifest_self_reference_policy": (
            "SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE"
        ),
    }


def _execute(
    output_root: Path, fixture_rows: dict[str, list[dict]], monkeypatch
) -> dict:
    monkeypatch.setattr(
        execution,
        "_verify_source_root",
        lambda _root: (_source_verification(), []),
    )
    monkeypatch.setattr(
        execution,
        "_read_rows",
        lambda _root: (deepcopy(fixture_rows), []),
    )
    return execution.execute_feature_label_refinement_v1(
        source_root=output_root.parent / "source",
        output_root=output_root,
        run_timestamp_utc=FIXED_TIMESTAMP,
    )


@pytest.fixture(scope="module")
def executed_bundle(tmp_path_factory, fixture_rows):
    root = tmp_path_factory.mktemp("feature_label_refinement_execution")
    with (
        patch.object(
            execution,
            "_verify_source_root",
            return_value=(_source_verification(), []),
        ),
        patch.object(
            execution,
            "_read_rows",
            return_value=(deepcopy(fixture_rows), []),
        ),
    ):
        artifact = execution.execute_feature_label_refinement_v1(
            source_root=root / "source",
            output_root=root / "outputs",
            run_timestamp_utc=FIXED_TIMESTAMP,
        )
    return artifact, root / "outputs"


@pytest.fixture(scope="module")
def executed(executed_bundle) -> dict:
    return executed_bundle[0]


def test_execution_builds_offline_without_provider_calls(
    tmp_path, fixture_rows, monkeypatch
) -> None:
    def forbidden_connect(*_args, **_kwargs):
        raise AssertionError("network access is forbidden")

    monkeypatch.setattr("socket.socket.connect", forbidden_connect)
    artifact = _execute(tmp_path / "outputs", fixture_rows, monkeypatch)
    assert artifact["created_offline"] is True
    assert artifact["provider_requests_made_in_execution"] is False


def test_execution_blocks_when_canonical_source_is_missing(tmp_path) -> None:
    artifact = execution.execute_feature_label_refinement_v1(
        source_root=tmp_path / "missing",
        output_root=tmp_path / "outputs",
        run_timestamp_utc=FIXED_TIMESTAMP,
    )
    assert artifact["artifact_kind"] == (
        execution.ARTIFACT_KIND_FEATURE_LABEL_REFINEMENT_EXECUTION_BLOCKED
    )
    assert artifact["execution_status"] == (
        execution.FEATURE_LABEL_REFINEMENT_EXECUTION_BLOCKED_MISSING_OR_INVALID_CANONICAL_DATASET
    )
    assert artifact["feature_label_refinement_execution_digest"] == "NOT_CREATED"
    assert artifact["generated_output_count"] == 0
    assert not (tmp_path / "outputs").exists()


def test_artifact_kind_and_status(executed: dict) -> None:
    assert executed["artifact_kind"] == (
        execution.ARTIFACT_KIND_FEATURE_LABEL_REFINEMENT_EXECUTED
    )
    assert executed["execution_status"] == (
        execution.FEATURE_LABEL_REFINEMENT_EXECUTED_RESEARCH_ONLY
    )


@pytest.mark.parametrize(
    "field,expected",
    [
        ("feature_label_refinement_execution_approval_digest", execution.EXPECTED_EXECUTION_APPROVAL_DIGEST),
        ("feature_label_refinement_execution_candidate_review_package_digest", execution.EXPECTED_EXECUTION_CANDIDATE_REVIEW_PACKAGE_DIGEST),
        ("feature_label_refinement_execution_candidate_digest", execution.EXPECTED_EXECUTION_CANDIDATE_DIGEST),
        ("feature_label_refinement_plan_approval_digest", execution.EXPECTED_PLAN_APPROVAL_DIGEST),
        ("research_registry_approval_digest", execution.EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST),
        ("records_digest", execution.EXPECTED_RECORDS_DIGEST),
    ],
)
def test_source_evidence_is_bound(executed: dict, field: str, expected: str) -> None:
    assert executed["source_evidence"][field] == expected


def test_target_universe_and_record_counts_are_exact(executed: dict) -> None:
    assert executed["target_universe_count"] == 12
    assert executed["target_universe"] == execution.TARGET_UNIVERSE
    assert executed["total_canonical_record_count"] == 11946
    assert executed["meta_record_count"] == 913
    assert executed["non_meta_record_count"] == 1003
    assert executed["per_ticker_record_counts"] == execution.EXPECTED_RECORD_COUNTS


@pytest.mark.parametrize("field", execution.TRUE_EXECUTION_FIELDS)
def test_execution_and_refinement_performed_fields_are_true(
    executed: dict, field: str
) -> None:
    assert executed[field] is True


def test_refinement_group_and_output_counts(executed: dict) -> None:
    assert executed["refined_label_family_count"] == 7
    assert executed["refined_feature_group_count"] == 9
    assert executed["refined_protocol_group_count"] == 6
    assert executed["model_comparison_group_count"] == 5
    assert executed["generated_output_count"] == 12


def test_generated_output_count_and_digest_manifest(executed_bundle) -> None:
    artifact, output_root = executed_bundle
    paths = sorted(path.name for path in output_root.iterdir() if path.is_file())
    assert paths == sorted(execution.OUTPUT_FILENAMES)
    manifest = json.loads(
        (output_root / "feature_label_refinement_execution_digest_manifest.json").read_text(
            encoding="utf-8"
        )
    )
    assert manifest["generated_output_count"] == 12
    assert [row["filename"] for row in manifest["output_digest_entries"]] == (
        execution.OUTPUT_FILENAMES
    )
    for row in manifest["output_digest_entries"]:
        path = output_root / row["filename"]
        if row["digest_kind"] == "SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE":
            assert row["filename"] == manifest["report_name"] + ".json"
            assert row["sha256"] is None
        else:
            assert row["sha256"] == sha256_file(path)
    assert manifest["feature_label_refinement_execution_digest"] == artifact[
        "feature_label_refinement_execution_digest"
    ]


def test_all_generated_outputs_preserve_research_only_boundaries(
    executed_bundle,
) -> None:
    _artifact, output_root = executed_bundle
    for filename in execution.OUTPUT_FILENAMES:
        report = json.loads((output_root / filename).read_text(encoding="utf-8"))
        assert report["output_label"] == execution.OUTPUT_LABEL
        assert report["evidence_scope"] == execution.EVIDENCE_SCOPE
        assert report["records_digest"] == execution.EXPECTED_RECORDS_DIGEST
        assert report["feature_label_refinement_executed"] is True
        assert report["additional_predictive_evidence_execution_candidate_created"] is False
        assert report["predictive_usefulness"] == execution.NOT_ACCEPTED
        assert report["profitability"] == execution.NOT_ACCEPTED
        assert report["runtime_use"] == execution.NOT_AUTHORIZED
        assert report["trade_recommendations_generated"] is False


@pytest.mark.parametrize("field", execution.FALSE_GUARDRAIL_FIELDS)
def test_all_execution_guardrail_fields_remain_false(
    executed: dict, field: str
) -> None:
    assert executed[field] is False


def test_downstream_authority_strings_remain_closed(executed: dict) -> None:
    assert executed["predictive_usefulness"] == execution.NOT_ACCEPTED
    assert executed["profitability"] == execution.NOT_ACCEPTED
    assert executed["runtime_use"] == execution.NOT_AUTHORIZED
    assert executed["strategy_use"] == execution.NOT_AUTHORIZED
    assert executed["paper_trading"] == execution.NOT_AUTHORIZED
    assert executed["broker_execution"] == execution.NOT_AUTHORIZED


def test_label_generation_report_covers_all_families(executed_bundle) -> None:
    _artifact, output_root = executed_bundle
    report = json.loads(
        (output_root / "refined_label_generation_report.json").read_text(
            encoding="utf-8"
        )
    )
    assert report["refined_label_families"] == execution.REFINED_LABEL_FAMILIES
    assert report["refined_label_family_count"] == 7
    assert report["forward_labels_only"] is True
    assert report["future_label_values_used_as_features"] is False
    assert report["flat_return_tolerance"] == "0.002000"
    assert len(report["per_ticker_label_family_coverage"]) == 84
    assert report["unavailable_label_boundary"]["value"] is None


def test_feature_generation_report_covers_all_groups(executed_bundle) -> None:
    _artifact, output_root = executed_bundle
    report = json.loads(
        (output_root / "refined_feature_generation_report.json").read_text(
            encoding="utf-8"
        )
    )
    assert report["approved_feature_refinement_groups"] == (
        execution.FEATURE_REFINEMENT_GROUPS
    )
    assert report["refined_feature_group_count"] == 9
    assert report["features_use_current_and_historical_information_only"] is True
    assert report["future_label_values_used_as_features"] is False
    assert len(report["per_ticker_feature_category_coverage"]) == 132


def test_protocol_walk_forward_oos_metrics_model_and_leakage_reports(
    executed_bundle,
) -> None:
    _artifact, output_root = executed_bundle
    protocol = json.loads((output_root / "refined_protocol_execution_report.json").read_text())
    walk = json.loads((output_root / "refined_walk_forward_report.json").read_text())
    oos = json.loads((output_root / "refined_out_of_sample_report.json").read_text())
    metrics = json.loads((output_root / "refined_metric_report.json").read_text())
    models = json.loads((output_root / "refined_model_comparison_report.json").read_text())
    leakage = json.loads((output_root / "refined_leakage_control_report.json").read_text())
    assert protocol["refined_protocol_group_count"] == 6
    assert protocol["no_shuffle"] is True
    assert walk["fold_count"] == 4 and walk["performed"] is True
    assert oos["performed"] is True and oos["results"]["evaluation_row_count"] > 0
    assert metrics["performed"] is True
    assert models["model_comparison_group_count"] == 5
    assert len(models["deterministic_comparison_ids"]) == 7
    assert leakage["leakage_control_status"] == "PASS"
    assert leakage["failed_control_count"] == 0


def test_validator_accepts_valid_artifact(executed: dict) -> None:
    validation = execution.validate_feature_label_refinement_executed_v1(
        deepcopy(executed)
    )
    assert validation["status"] == execution.FEATURE_LABEL_REFINEMENT_EXECUTION_VALID


@pytest.mark.parametrize(
    "path,bad_value",
    [
        (("artifact_kind",), "WRONG"),
        (("execution_status",), "WRONG"),
        (("source_evidence", "feature_label_refinement_execution_approval_digest"), "0" * 64),
        (("feature_label_refinement_execution_authorized",), False),
        (("feature_label_refinement_executed",), False),
        (("feature_label_refinement_results_created",), False),
        (("refined_label_generation_performed",), False),
        (("refined_feature_generation_performed",), False),
        (("refined_walk_forward_validation_performed",), False),
        (("refined_out_of_sample_evaluation_performed",), False),
        (("refined_metrics_recomputation_performed",), False),
        (("model_comparison_performed",), False),
        (("refined_label_family_count",), 6),
        (("refined_feature_group_count",), 8),
        (("refined_protocol_group_count",), 5),
        (("model_comparison_group_count",), 4),
        (("generated_output_count",), 11),
        (("target_universe_count",), 11),
        (("target_universe",), ["MSFT"]),
        (("total_canonical_record_count",), 11945),
        (("records_digest",), "0" * 64),
        (("meta_record_count",), 1003),
        (("per_ticker_record_counts", "MSFT"), 1002),
        (("provider_requests_made_in_execution",), True),
        (("live_provider_transport_enabled_in_execution",), True),
        (("market_data_acquisition_performed_in_execution",), True),
        (("dataset_generation_performed_in_execution",), True),
        (("canonical_dataset_regenerated_in_execution",), True),
        (("raw_provider_payloads_committed",), True),
        (("api_keys_stored_or_printed",), True),
        (("additional_predictive_evidence_execution_candidate_created",), True),
        (("additional_predictive_evidence_execution_authorized",), True),
        (("additional_predictive_evidence_executed",), True),
        (("new_strategy_scoring_performed",), True),
        (("trade_recommendations_generated",), True),
        (("predictive_usefulness",), "accepted"),
        (("predictive_usefulness_acceptance_candidate_created",), True),
        (("profitability",), "accepted"),
        (("runtime_migration_approved",), True),
        (("runtime_use",), "AUTHORIZED"),
        (("strategy_use",), "AUTHORIZED"),
        (("paper_trading",), "AUTHORIZED"),
        (("broker_execution",), "AUTHORIZED"),
        (("automatic_stitching",), True),
    ],
)
def test_validator_rejects_contract_mutations(
    executed: dict, path: tuple[str, ...], bad_value
) -> None:
    mutated = deepcopy(executed)
    target = mutated
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = bad_value
    with pytest.raises(execution.FeatureLabelRefinementExecutionError):
        execution.validate_feature_label_refinement_executed_v1(mutated)


def test_validator_rejects_missing_execution_digest(executed: dict) -> None:
    mutated = deepcopy(executed)
    mutated.pop("feature_label_refinement_execution_digest")
    with pytest.raises(execution.FeatureLabelRefinementExecutionError):
        execution.validate_feature_label_refinement_executed_v1(mutated)


def test_execution_digest_is_deterministic_for_fixed_timestamp(
    tmp_path, fixture_rows
) -> None:
    with (
        patch.object(
            execution,
            "_verify_source_root",
            return_value=(_source_verification(), []),
        ),
        patch.object(
            execution,
            "_read_rows",
            side_effect=[
                (deepcopy(fixture_rows), []),
                (deepcopy(fixture_rows), []),
            ],
        ),
    ):
        first = execution.execute_feature_label_refinement_v1(
            source_root=tmp_path / "source",
            output_root=tmp_path / "first",
            run_timestamp_utc=FIXED_TIMESTAMP,
        )
        second = execution.execute_feature_label_refinement_v1(
            source_root=tmp_path / "source",
            output_root=tmp_path / "second",
            run_timestamp_utc=FIXED_TIMESTAMP,
        )
    assert first["feature_label_refinement_execution_digest"] == second[
        "feature_label_refinement_execution_digest"
    ]


def test_output_root_refuses_overwrite(executed_bundle, fixture_rows) -> None:
    _artifact, output_root = executed_bundle
    with (
        patch.object(
            execution,
            "_verify_source_root",
            return_value=(_source_verification(), []),
        ),
        patch.object(
            execution,
            "_read_rows",
            return_value=(deepcopy(fixture_rows), []),
        ),
        pytest.raises(execution.FeatureLabelRefinementExecutionError),
    ):
        execution.execute_feature_label_refinement_v1(
            source_root=output_root.parent / "source",
            output_root=output_root,
            run_timestamp_utc=FIXED_TIMESTAMP,
        )


def test_status_markdown_contains_required_sections(executed: dict) -> None:
    markdown = execution.build_feature_label_refinement_execution_status_markdown_v1(
        executed
    )
    for heading in (
        "Feature/Label Refinement Execution",
        "Source Execution Approval",
        "Registry-Approved Dataset Metadata",
        "Refined Label Generation Summary",
        "Refined Feature Generation Summary",
        "Refined Protocol Execution Summary",
        "Refined Walk-Forward Summary",
        "Refined OOS Summary",
        "Refined Metrics Summary",
        "Model Comparison Summary",
        "Refined Leakage-Control Summary",
        "Data Quality Summary",
        "Output Digest Manifest",
        "Predictive Usefulness Boundary",
        "Profitability Boundary",
        "Runtime Boundary",
        "Guardrails",
    ):
        assert f"## {heading}" in markdown
