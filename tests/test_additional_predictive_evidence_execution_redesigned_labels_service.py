from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import pytest

from marketflow.services import (
    additional_predictive_evidence_execution_redesigned_labels_service as service,
)


def _summaries(**overrides):
    values = {
        "feature_label_matrix_row_count": 143352,
        "evaluable_matrix_row_count": 142200,
        "unavailable_target_matrix_row_count": 1152,
        "feature_label_matrix_digest": "a" * 64,
        "feature_input_names": ["safe_feature"],
        "walk_forward_fold_count": 4,
        "oos_holdout_year": 2025,
        "baseline_family_count": 4,
        "model_family_count": 5,
        "metric_family_count": 10,
        "leakage_control_status": "PASS",
        "leakage_failed_control_count": 0,
        "horizon_aware_training_embargo_applied": True,
        "warning_count": 2,
        "oos_method_metrics": {},
        "walk_forward_accuracy_stability": {},
    }
    values.update(overrides)
    return values


def _build(**summary_overrides):
    return service._build_executed_artifact(
        run_timestamp_utc="2026-08-19T13:00:00Z",
        canonical_root=Path("canonical"),
        label_root=Path("labels"),
        feature_root=Path("features"),
        output_root=Path("output"),
        summaries=_summaries(**summary_overrides),
    )


@pytest.fixture(scope="module")
def artifact():
    return _build()


def _invalid(artifact, field, value):
    changed = deepcopy(artifact)
    changed[field] = value
    return changed


def test_execution_builds_offline(monkeypatch, tmp_path, artifact):
    monkeypatch.setattr(service, "_verify_sources", lambda *args: ({"verified": True}, []))
    monkeypatch.setattr(service, "_run_verified_execution", lambda **kwargs: deepcopy(artifact))
    result = service.execute_additional_predictive_evidence_using_redesigned_labels_v1(
        canonical_root=tmp_path / "canonical",
        label_root=tmp_path / "labels",
        feature_root=tmp_path / "features",
        output_root=tmp_path / "output",
        run_timestamp_utc="2026-08-19T13:00:00Z",
    )
    assert result["created_offline"] is True
    assert result["provider_requests_made_in_execution"] is False


def test_execution_blocks_if_canonical_source_missing(tmp_path):
    result = service.execute_additional_predictive_evidence_using_redesigned_labels_v1(
        canonical_root=tmp_path / "canonical",
        label_root=tmp_path / "labels",
        feature_root=tmp_path / "features",
        output_root=tmp_path / "output",
        run_timestamp_utc="2026-08-19T13:00:00Z",
    )
    assert result["execution_status"] == service.ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_BLOCKED_MISSING_OR_INVALID_SOURCE_EVIDENCE
    assert any(row["failure_id"] == "canonical_source_missing" for row in result["failures"])


def test_execution_blocks_if_redesigned_label_source_missing(tmp_path):
    result = service.execute_additional_predictive_evidence_using_redesigned_labels_v1(
        canonical_root=tmp_path / "canonical",
        label_root=tmp_path / "labels",
        feature_root=tmp_path / "features",
        output_root=tmp_path / "output",
        run_timestamp_utc="2026-08-19T13:00:00Z",
    )
    assert any(row["failure_id"] == "labels_source_missing" for row in result["failures"])


def test_execution_blocks_if_feature_source_missing(tmp_path):
    result = service.execute_additional_predictive_evidence_using_redesigned_labels_v1(
        canonical_root=tmp_path / "canonical",
        label_root=tmp_path / "labels",
        feature_root=tmp_path / "features",
        output_root=tmp_path / "output",
        run_timestamp_utc="2026-08-19T13:00:00Z",
    )
    assert any(row["failure_id"] == "features_source_missing" for row in result["failures"])


def test_artifact_kind_is_correct(artifact):
    assert artifact["artifact_kind"] == service.ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED_USING_REDESIGNED_LABELS


def test_execution_status_is_correct(artifact):
    assert artifact["execution_status"] == service.ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED_USING_REDESIGNED_LABELS_RESEARCH_ONLY


def test_approval_digest_is_bound(artifact):
    assert artifact["additional_predictive_evidence_execution_approval_using_redesigned_labels_digest"] == service.EXPECTED_APPROVAL_DIGEST


def test_candidate_review_digest_is_bound(artifact):
    assert artifact["additional_predictive_evidence_execution_candidate_using_redesigned_labels_review_package_digest"] == service.EXPECTED_CANDIDATE_REVIEW_DIGEST


def test_candidate_digest_is_bound(artifact):
    assert artifact["additional_predictive_evidence_execution_candidate_using_redesigned_labels_digest"] == service.EXPECTED_CANDIDATE_DIGEST


def test_feature_results_review_digest_is_bound(artifact):
    assert artifact["feature_generation_results_review_using_redesigned_labels_digest"] == service.EXPECTED_FEATURE_RESULTS_REVIEW_DIGEST


def test_feature_values_digest_is_bound(artifact):
    assert artifact["feature_values_digest"] == service.EXPECTED_FEATURE_VALUES_DIGEST


def test_redesigned_label_values_digest_is_bound(artifact):
    assert artifact["redesigned_label_values_digest"] == service.EXPECTED_LABEL_VALUES_DIGEST


def test_records_digest_is_bound(artifact):
    assert artifact["records_digest"] == service.EXPECTED_RECORDS_DIGEST


def test_universe_count_and_order_are_preserved(artifact):
    assert artifact["target_universe_count"] == 12
    assert artifact["target_universe"] == service.TARGET_UNIVERSE


def test_meta_913_is_preserved(artifact):
    assert artifact["meta_record_count"] == 913
    assert artifact["per_ticker_record_counts"]["META"] == 913


def test_execution_approved_authorized_and_ready_are_true(artifact):
    assert artifact["additional_predictive_evidence_execution_approved"] is True
    assert artifact["additional_predictive_evidence_execution_authorized"] is True
    assert artifact["ready_for_additional_predictive_evidence_execution_using_redesigned_labels"] is True


def test_predictive_evidence_executed_and_results_are_true(artifact):
    assert artifact["additional_predictive_evidence_executed"] is True
    assert artifact["predictive_evidence_results_created"] is True


def test_metric_recomputation_is_true(artifact):
    assert artifact["metric_recomputation_performed"] is True


def test_model_training_is_true(artifact):
    assert artifact["model_training_performed"] is True


def test_generated_output_count_is_13(artifact):
    assert artifact["generated_output_count"] == 13


def test_feature_label_matrix_is_created(artifact):
    assert artifact["feature_label_matrix_created"] is True


def test_matrix_row_count_is_143352(artifact):
    assert artifact["feature_label_matrix_row_count"] == 143352


def test_evaluable_matrix_row_count_is_142200(artifact):
    assert artifact["evaluable_matrix_row_count"] == 142200


def test_unavailable_target_count_is_1152(artifact):
    assert artifact["unavailable_target_matrix_row_count"] == 1152


def test_walk_forward_fold_count_is_4(artifact):
    assert artifact["walk_forward_fold_count"] == 4


def test_oos_holdout_is_2025(artifact):
    assert artifact["oos_holdout_year"] == 2025


def test_baseline_family_count_is_4(artifact):
    assert artifact["baseline_family_count"] == 4


def test_model_family_count_is_5(artifact):
    assert artifact["model_family_count"] == 5


def test_metric_family_count_is_10(artifact):
    assert artifact["metric_family_count"] == 10


def test_leakage_control_status_is_pass(artifact):
    assert artifact["leakage_control_status"] == "PASS"
    assert artifact["leakage_failed_control_count"] == 0


def test_future_labels_are_not_used_as_features(artifact):
    assert artifact["future_label_values_used_as_features"] is False
    assert artifact["horizon_aware_training_embargo_applied"] is True


def test_forward_returns_are_not_used_as_features(artifact):
    assert artifact["forward_return_used_as_feature"] is False


def test_label_values_are_not_used_as_feature_inputs(artifact):
    assert artifact["label_value_used_as_feature_input"] is False


def test_threshold_values_are_not_numeric_predictors(artifact):
    assert artifact["threshold_value_used_as_numeric_predictor"] is False


def test_predictive_usefulness_remains_not_accepted(artifact):
    assert artifact["predictive_usefulness"] == "not accepted"


def test_profitability_remains_not_accepted(artifact):
    assert artifact["profitability"] == "not accepted"


def test_runtime_remains_not_authorized(artifact):
    assert artifact["runtime_use"] == "NOT_AUTHORIZED"
    assert artifact["strategy_use"] == "NOT_AUTHORIZED"
    assert artifact["paper_trading"] == "NOT_AUTHORIZED"
    assert artifact["broker_execution"] == "NOT_AUTHORIZED"


def test_trade_recommendations_remain_false(artifact):
    assert artifact["trade_recommendations_generated"] is False


def test_output_digest_manifest_is_present(artifact):
    assert artifact["digest_manifest_created"] is True
    assert artifact["generated_output_count"] == len(service.OUTPUT_FILENAMES)


def test_feature_label_matrix_digest_is_present(artifact):
    assert len(artifact["feature_label_matrix_digest"]) == 64


def test_validator_accepts_valid_artifact(artifact):
    result = service.validate_additional_predictive_evidence_executed_using_redesigned_labels_v1(artifact)
    assert result["valid"] is True


def test_validator_rejects_wrong_artifact_kind(artifact):
    with pytest.raises(service.AdditionalPredictiveEvidenceExecutionRedesignedLabelsError):
        service.validate_additional_predictive_evidence_executed_using_redesigned_labels_v1(_invalid(artifact, "artifact_kind", "WRONG"))


def test_validator_rejects_wrong_execution_status(artifact):
    with pytest.raises(service.AdditionalPredictiveEvidenceExecutionRedesignedLabelsError):
        service.validate_additional_predictive_evidence_executed_using_redesigned_labels_v1(_invalid(artifact, "execution_status", "WRONG"))


def test_validator_rejects_approval_false(artifact):
    with pytest.raises(service.AdditionalPredictiveEvidenceExecutionRedesignedLabelsError):
        service.validate_additional_predictive_evidence_executed_using_redesigned_labels_v1(_invalid(artifact, "additional_predictive_evidence_execution_approved", False))


def test_validator_rejects_predictive_evidence_executed_false(artifact):
    with pytest.raises(service.AdditionalPredictiveEvidenceExecutionRedesignedLabelsError):
        service.validate_additional_predictive_evidence_executed_using_redesigned_labels_v1(_invalid(artifact, "additional_predictive_evidence_executed", False))


def test_validator_rejects_metric_recomputation_false(artifact):
    with pytest.raises(service.AdditionalPredictiveEvidenceExecutionRedesignedLabelsError):
        service.validate_additional_predictive_evidence_executed_using_redesigned_labels_v1(_invalid(artifact, "metric_recomputation_performed", False))


def test_validator_rejects_model_training_false(artifact):
    with pytest.raises(service.AdditionalPredictiveEvidenceExecutionRedesignedLabelsError):
        service.validate_additional_predictive_evidence_executed_using_redesigned_labels_v1(_invalid(artifact, "model_training_performed", False))


def test_validator_rejects_matrix_row_count_mismatch(artifact):
    with pytest.raises(service.AdditionalPredictiveEvidenceExecutionRedesignedLabelsError):
        service.validate_additional_predictive_evidence_executed_using_redesigned_labels_v1(_invalid(artifact, "feature_label_matrix_row_count", 1))


def test_validator_rejects_leakage_failure(artifact):
    with pytest.raises(service.AdditionalPredictiveEvidenceExecutionRedesignedLabelsError):
        service.validate_additional_predictive_evidence_executed_using_redesigned_labels_v1(_invalid(artifact, "leakage_control_status", "FAIL"))


def test_validator_rejects_predictive_usefulness_accepted(artifact):
    with pytest.raises(service.AdditionalPredictiveEvidenceExecutionRedesignedLabelsError):
        service.validate_additional_predictive_evidence_executed_using_redesigned_labels_v1(_invalid(artifact, "predictive_usefulness", "accepted"))


def test_validator_rejects_runtime_authorized(artifact):
    with pytest.raises(service.AdditionalPredictiveEvidenceExecutionRedesignedLabelsError):
        service.validate_additional_predictive_evidence_executed_using_redesigned_labels_v1(_invalid(artifact, "runtime_use", "AUTHORIZED"))


def test_execution_digest_is_deterministic_for_fixed_timestamp_and_source(artifact):
    rebuilt = _build()
    assert rebuilt["additional_predictive_evidence_execution_digest"] == artifact["additional_predictive_evidence_execution_digest"]


def test_markdown_includes_required_sections(artifact):
    markdown = service.build_additional_predictive_evidence_execution_status_markdown_v1(artifact)
    for section in (
        "Title",
        "Additional Predictive Evidence Execution Using Redesigned Labels",
        "Source Approval",
        "Dataset and Universe",
        "Source Redesigned Label Profile",
        "Source Feature Profile",
        "Feature / Label Matrix",
        "Chronological Splits",
        "Walk-Forward Results",
        "OOS Holdout Results",
        "Baseline and Model Comparison",
        "Metric Family Results",
        "Calibration and Stability",
        "Leakage and Quality Controls",
        "Per-Ticker / Cross-Sectional Review",
        "Output Digest Manifest",
        "Execution Boundary",
        "Predictive Usefulness Boundary",
        "Profitability Boundary",
        "Runtime Boundary",
        "Checklist Summary",
        "Guardrails",
    ):
        assert f"## {section}" in markdown
