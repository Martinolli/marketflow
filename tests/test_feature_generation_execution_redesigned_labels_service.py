from __future__ import annotations

from copy import deepcopy
import json

import pytest

from marketflow import services
from marketflow.services import feature_generation_execution_redesigned_labels_service as execution_service


@pytest.fixture(scope="module")
def execution_result(tmp_path_factory) -> tuple[dict, object]:
    output = tmp_path_factory.mktemp("feature_generation")
    artifact = execution_service.execute_feature_generation_using_redesigned_labels_v1(
        output_root=output,
        run_timestamp_utc="2026-08-18T17:00:00Z",
    )
    return artifact, output


@pytest.fixture(scope="module")
def artifact(execution_result) -> dict:
    return execution_result[0]


def test_execution_builds_offline(monkeypatch, tmp_path) -> None:
    monkeypatch.setattr("socket.socket.connect", lambda *_args, **_kwargs: (_ for _ in ()).throw(AssertionError("network forbidden")))
    artifact = execution_service.execute_feature_generation_using_redesigned_labels_v1(output_root=tmp_path, run_timestamp_utc="2026-08-18T17:00:00Z")
    assert artifact["created_offline"] is True
    assert artifact["provider_requests_made_in_execution"] is False


def test_execution_blocks_if_canonical_source_missing(tmp_path) -> None:
    artifact = execution_service.execute_feature_generation_using_redesigned_labels_v1(canonical_root=tmp_path / "missing", output_root=tmp_path / "out")
    assert artifact["artifact_kind"] == "FEATURE_GENERATION_BLOCKED_USING_REDESIGNED_LABELS"
    assert artifact["feature_generation_digest"] == "NOT_CREATED"
    assert artifact["generated_output_count"] == 0


def test_execution_blocks_if_label_source_missing(tmp_path) -> None:
    artifact = execution_service.execute_feature_generation_using_redesigned_labels_v1(label_root=tmp_path / "missing", output_root=tmp_path / "out")
    assert artifact["execution_status"] == "FEATURE_GENERATION_BLOCKED_MISSING_OR_INVALID_SOURCE_EVIDENCE"
    assert artifact["feature_values_created"] is False


def test_artifact_kind_and_status(artifact) -> None:
    assert artifact["artifact_kind"] == "FEATURE_GENERATION_EXECUTED_USING_REDESIGNED_LABELS"
    assert artifact["execution_status"] == "FEATURE_GENERATION_EXECUTED_USING_REDESIGNED_LABELS_RESEARCH_ONLY"


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("feature_generation_approval_using_redesigned_labels_digest", execution_service.EXPECTED_APPROVAL_DIGEST),
        ("feature_generation_candidate_using_redesigned_labels_review_package_digest", execution_service.approval_service.EXPECTED_CANDIDATE_REVIEW_DIGEST),
        ("feature_generation_candidate_using_redesigned_labels_digest", execution_service.approval_service.EXPECTED_CANDIDATE_DIGEST),
        ("feature_predictive_evidence_planning_approval_using_redesigned_labels_digest", execution_service.approval_service.EXPECTED_PLANNING_APPROVAL_DIGEST),
        ("redesigned_label_generation_results_review_package_digest", execution_service.approval_service.EXPECTED_RESULTS_REVIEW_DIGEST),
        ("label_values_digest", execution_service.EXPECTED_LABEL_VALUES_DIGEST),
        ("records_digest", execution_service.EXPECTED_RECORDS_DIGEST),
    ],
)
def test_bound_digest(artifact, field, expected) -> None:
    assert artifact[field] == expected


def test_universe_and_meta_preserved(artifact) -> None:
    assert artifact["target_universe"] == execution_service.TARGET_UNIVERSE
    assert artifact["target_universe_count"] == 12
    assert artifact["meta_record_count"] == 913
    assert artifact["meta_reduced_record_count_preserved"] is True


@pytest.mark.parametrize("field", ["feature_generation_approved", "feature_generation_authorized", "redesigned_feature_generation_authorized", "ready_for_feature_generation_execution_using_redesigned_labels", "feature_generation_performed", "redesigned_feature_generation_performed", "feature_values_created", "feature_generation_results_created"])
def test_execution_state_true(artifact, field) -> None:
    assert artifact[field] is True


def test_output_and_contract_counts(artifact) -> None:
    assert artifact["generated_output_count"] == 12
    assert artifact["feature_family_count"] == 10
    assert artifact["feature_group_count"] == 17
    assert artifact["feature_schema_field_count"] == 16
    assert artifact["feature_value_row_count"] == 203082
    assert artifact["available_feature_value_count"] + artifact["unavailable_feature_value_count"] == 203082
    assert len(artifact["feature_values_digest"]) == 64


def test_all_expected_outputs_created(execution_result) -> None:
    _artifact, output = execution_result
    assert sorted(path.name for path in output.iterdir()) == sorted(execution_service.OUTPUT_FILENAMES)


def test_feature_rows_are_research_only_and_do_not_contain_future_values(execution_result) -> None:
    _artifact, output = execution_result
    with (output / "feature_values.jsonl").open(encoding="utf-8") as handle:
        rows = [json.loads(next(handle)) for _ in range(100)]
    forbidden = {"label_value", "forward_return", "threshold_value_used", "future_return_direction", "future_return_bucket"}
    assert all(row["research_only"] and row["non_actionable"] for row in rows)
    assert all(not forbidden.intersection(row) for row in rows)


def test_baseline_error_context_is_unavailable(execution_result) -> None:
    _artifact, output = execution_result
    found = None
    with (output / "feature_values.jsonl").open(encoding="utf-8") as handle:
        for line in handle:
            row = json.loads(line)
            if row["feature_group"] == "baseline_error_context_candidates":
                found = row
                break
    assert found["feature_value"] is None
    assert found["feature_available"] is False
    assert found["availability_reason"] == "BASELINE_ERROR_CONTEXT_REQUIRES_FUTURE_OUTCOME_REVIEW"


def test_alignment_and_quality_reports_created(execution_result) -> None:
    _artifact, output = execution_result
    alignment = json.loads((output / "feature_label_alignment_report.json").read_text(encoding="utf-8"))
    quality = json.loads((output / "feature_quality_report.json").read_text(encoding="utf-8"))
    assert alignment["label_values_used_as_features"] is False
    assert alignment["forward_returns_used_as_features"] is False
    assert quality["feature_value_row_count"] == 203082


def test_per_ticker_feature_counts_and_meta_limitation(execution_result) -> None:
    _artifact, output = execution_result
    report = json.loads((output / "per_ticker_feature_summary.json").read_text(encoding="utf-8"))
    rows = report["per_ticker_summary"]
    assert next(row for row in rows if row["ticker"] == "META")["feature_value_row_count"] == 15521
    assert all(row["feature_value_row_count"] == 17051 for row in rows if row["ticker"] != "META")
    meta = json.loads((output / "meta_limitation_feature_handling_report.json").read_text(encoding="utf-8"))
    assert meta["meta_limitation_preserved"] is True
    assert meta["records_repaired_or_inferred"] is False


def test_output_digest_manifest_present(execution_result) -> None:
    _artifact, output = execution_result
    manifest = json.loads((output / "feature_generation_digest_manifest.json").read_text(encoding="utf-8"))
    assert len(manifest["output_digest_manifest"]) == 12
    assert any(row["filename"] == "feature_values.jsonl" and len(row["sha256"]) == 64 for row in manifest["output_digest_manifest"])


@pytest.mark.parametrize("field", ["metric_recomputation_performed", "model_training_performed", "additional_predictive_evidence_execution_candidate_created", "additional_predictive_evidence_executed", "trade_recommendations_generated"])
def test_downstream_actions_false(artifact, field) -> None:
    assert artifact[field] is False


def test_acceptance_profitability_and_runtime_closed(artifact) -> None:
    assert artifact["predictive_usefulness"] == "not accepted"
    assert artifact["profitability"] == "not accepted"
    for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
        assert artifact[field] == "NOT_AUTHORIZED"


def test_validator_accepts_valid_artifact(artifact) -> None:
    result = execution_service.validate_feature_generation_executed_using_redesigned_labels_v1(deepcopy(artifact))
    assert result["feature_value_row_count"] == 203082
    assert result["runtime_authorized"] is False


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("artifact_kind", "WRONG"), ("execution_status", "WRONG"),
        ("feature_generation_approval_using_redesigned_labels_digest", None),
        ("feature_generation_approved", False), ("feature_generation_authorized", False),
        ("ready_for_feature_generation_execution_using_redesigned_labels", False),
        ("feature_generation_performed", False), ("feature_values_created", False),
        ("generated_output_count", 11), ("target_universe", list(reversed(execution_service.TARGET_UNIVERSE))),
        ("target_universe_count", 11), ("records_digest", "0" * 64), ("label_values_digest", "0" * 64),
        ("meta_record_count", 1003), ("feature_family_count", 9), ("feature_group_count", 16),
        ("feature_schema_field_count", 15), ("feature_value_row_count", 1),
        ("model_training_performed", True), ("metric_recomputation_performed", True),
        ("additional_predictive_evidence_execution_candidate_created", True),
        ("predictive_usefulness", "accepted"), ("profitability", "accepted"),
        ("runtime_use", "AUTHORIZED"), ("strategy_use", "AUTHORIZED"),
        ("paper_trading", "AUTHORIZED"), ("broker_execution", "AUTHORIZED"),
        ("trade_recommendations_generated", True),
    ],
)
def test_validator_rejects_invalid_artifact(artifact, field, value) -> None:
    invalid = deepcopy(artifact)
    invalid[field] = value
    with pytest.raises(execution_service.FeatureGenerationExecutionRedesignedLabelsError):
        execution_service.validate_feature_generation_executed_using_redesigned_labels_v1(invalid)


def test_validator_rejects_missing_digests(artifact) -> None:
    for field in ("feature_values_digest", "feature_generation_execution_digest"):
        invalid = deepcopy(artifact)
        invalid.pop(field)
        with pytest.raises(execution_service.FeatureGenerationExecutionRedesignedLabelsError):
            execution_service.validate_feature_generation_executed_using_redesigned_labels_v1(invalid)


def test_execution_digest_deterministic_for_fixed_timestamp(tmp_path) -> None:
    first = execution_service.execute_feature_generation_using_redesigned_labels_v1(output_root=tmp_path / "one", run_timestamp_utc="2026-08-18T17:00:00Z")
    second = execution_service.execute_feature_generation_using_redesigned_labels_v1(output_root=tmp_path / "two", run_timestamp_utc="2026-08-18T17:00:00Z")
    assert first["feature_generation_execution_digest"] == second["feature_generation_execution_digest"]
    assert first["feature_values_digest"] == second["feature_values_digest"]


def test_markdown_includes_required_sections(artifact) -> None:
    markdown = execution_service.build_feature_generation_execution_status_markdown_v1(artifact)
    for section in ["Feature Generation Execution Using Redesigned Labels", "Feature Generation Policy", "Feature / Label Alignment Review", "META Limitation Preservation", "Predictive Evidence Boundary", "Runtime Boundary", "Guardrails"]:
        assert f"## {section}" in markdown


def test_public_exports_are_available() -> None:
    assert services.ARTIFACT_KIND_FEATURE_GENERATION_EXECUTED_USING_REDESIGNED_LABELS == execution_service.ARTIFACT_KIND_FEATURE_GENERATION_EXECUTED_USING_REDESIGNED_LABELS
    assert services.execute_feature_generation_using_redesigned_labels_v1 is execution_service.execute_feature_generation_using_redesigned_labels_v1
    assert services.validate_feature_generation_executed_using_redesigned_labels_v1 is execution_service.validate_feature_generation_executed_using_redesigned_labels_v1
