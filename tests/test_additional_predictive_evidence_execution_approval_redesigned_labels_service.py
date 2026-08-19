from __future__ import annotations

from copy import deepcopy

import pytest

from marketflow.services import (
    additional_predictive_evidence_execution_approval_redesigned_labels_service as service,
)


def _attestation(**overrides):
    values = {
        "operator_reference": "TEST_OPERATOR",
        "operator_attestation_timestamp_utc": "2026-08-19T12:00:00Z",
        "operator_attestation_phrase": service.REQUIRED_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVAL_USING_REDESIGNED_LABELS_ATTESTATION_PHRASE,
        **service.DIGEST_CONFIRMATIONS,
        **service.VALUE_CONFIRMATIONS,
        **{field: True for field in service.BOOLEAN_CONFIRMATIONS},
    }
    values.update(overrides)
    return service.build_additional_predictive_evidence_execution_approval_using_redesigned_labels_attestation_v1(
        **values
    )


@pytest.fixture(scope="module")
def approval():
    return service.build_additional_predictive_evidence_execution_approved_using_redesigned_labels_v1(
        operator_attestation=_attestation()
    )


def _invalid(approval, field, value):
    changed = deepcopy(approval)
    changed[field] = value
    return changed


def test_attestation_builder_creates_required_fields():
    attestation = _attestation()
    assert attestation["operator_reference"] == "TEST_OPERATOR"
    assert attestation["operator_decision"] == service.OPERATOR_DECISION_APPROVE_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_USING_REDESIGNED_LABELS
    assert attestation["operator_attestation_version"] == service.OPERATOR_ATTESTATION_VERSION_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVAL_USING_REDESIGNED_LABELS_V1
    assert set(service.DIGEST_CONFIRMATIONS) <= set(attestation)
    assert set(service.VALUE_CONFIRMATIONS) <= set(attestation)
    assert set(service.BOOLEAN_CONFIRMATIONS) <= set(attestation)


def test_approval_package_builds_offline(approval):
    assert approval["created_offline"] is True
    assert approval["provider_requests_made"] is False
    assert approval["live_provider_transport_enabled"] is False


def test_artifact_kind_is_correct(approval):
    assert approval["artifact_kind"] == service.ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVED_USING_REDESIGNED_LABELS


def test_approval_status_is_correct(approval):
    assert approval["approval_status"] == service.ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVED_USING_REDESIGNED_LABELS


def test_approval_scope_is_correct(approval):
    assert approval["approval_scope"] == service.ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVAL_ONLY


def test_candidate_review_digest_is_bound(approval):
    assert approval["additional_predictive_evidence_execution_candidate_using_redesigned_labels_review_package_digest"] == service.EXPECTED_CANDIDATE_REVIEW_DIGEST


def test_candidate_digest_is_bound(approval):
    assert approval["additional_predictive_evidence_execution_candidate_using_redesigned_labels_digest"] == service.EXPECTED_CANDIDATE_DIGEST


def test_feature_generation_results_review_digest_is_bound(approval):
    assert approval["feature_generation_results_review_using_redesigned_labels_digest"] == service.EXPECTED_FEATURE_GENERATION_RESULTS_REVIEW_DIGEST


def test_feature_generation_execution_digest_is_bound(approval):
    assert approval["feature_generation_execution_using_redesigned_labels_digest"] == service.EXPECTED_FEATURE_GENERATION_EXECUTION_DIGEST


def test_feature_values_digest_is_bound(approval):
    assert approval["feature_values_digest"] == service.EXPECTED_FEATURE_VALUES_DIGEST


def test_redesigned_label_values_digest_is_bound(approval):
    assert approval["redesigned_label_values_digest"] == service.EXPECTED_REDESIGNED_LABEL_VALUES_DIGEST


def test_research_registry_digest_is_bound(approval):
    assert approval["research_registry_approval_digest"] == service.EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST


def test_records_digest_is_bound(approval):
    assert approval["records_digest"] == service.EXPECTED_RECORDS_DIGEST


def test_universe_count_and_order_are_preserved(approval):
    assert approval["target_universe_count"] == 12
    assert approval["target_universe"] == service.TARGET_UNIVERSE


def test_meta_913_is_preserved(approval):
    assert approval["meta_record_count"] == 913
    assert approval["per_ticker_record_counts"]["META"] == 913
    assert all(count == 1003 for ticker, count in approval["per_ticker_record_counts"].items() if ticker != "META")


def test_source_feature_profile_is_confirmed(approval):
    assert approval["operator_attestation"]["operator_confirms_source_feature_profile"] is True
    assert approval["approved_source_feature_profile"]["feature_value_row_count"] == 203082


def test_source_label_profile_is_confirmed(approval):
    assert approval["operator_attestation"]["operator_confirms_source_label_profile"] is True
    assert approval["approved_source_redesigned_label_profile"]["label_value_row_count"] == 143352


def test_approval_authorization_and_ready_are_true(approval):
    assert approval["additional_predictive_evidence_execution_approved"] is True
    assert approval["additional_predictive_evidence_execution_approval_created"] is True
    assert approval["additional_predictive_evidence_execution_authorized"] is True
    assert approval["ready_for_additional_predictive_evidence_execution_using_redesigned_labels"] is True


def test_predictive_evidence_execution_performed_is_false(approval):
    assert approval["additional_predictive_evidence_executed"] is False


def test_predictive_evidence_results_created_is_false(approval):
    assert approval["predictive_evidence_results_created"] is False


def test_metric_recomputation_remains_false(approval):
    assert approval["metric_recomputation_performed"] is False


def test_model_training_remains_false(approval):
    assert approval["model_training_performed"] is False


def test_predictive_usefulness_is_not_accepted(approval):
    assert approval["predictive_usefulness"] == service.NOT_ACCEPTED


def test_profitability_is_not_accepted(approval):
    assert approval["profitability"] == service.NOT_ACCEPTED


def test_runtime_is_not_authorized(approval):
    assert approval["runtime_use"] == service.NOT_AUTHORIZED
    assert approval["strategy_use"] == service.NOT_AUTHORIZED
    assert approval["paper_trading"] == service.NOT_AUTHORIZED
    assert approval["broker_execution"] == service.NOT_AUTHORIZED


def test_trade_recommendations_are_false(approval):
    assert approval["trade_recommendations_generated"] is False


def test_approved_source_input_count_is_12(approval):
    assert len(approval["approved_source_inputs"]) == 12
    assert all(row["generation_status"] == service.NOT_REGENERATED for row in approval["approved_source_inputs"])


def test_approved_execution_activity_count_is_13(approval):
    assert len(approval["approved_execution_activities"]) == 13
    assert all(row["authorization_status"] == service.AUTHORIZED_NOT_EXECUTED for row in approval["approved_execution_activities"])
    assert all(row["execution_performed"] is False for row in approval["approved_execution_activities"])


def test_approved_feature_label_matrix_is_present(approval):
    matrix = approval["approved_feature_label_matrix"]
    assert matrix["matrix_status"] == service.AUTHORIZED_NOT_GENERATED
    assert matrix["matrix_created"] is False
    assert matrix["feature_row_count"] == 203082
    assert matrix["label_row_count"] == 143352


def test_approved_splits_are_present(approval):
    assert approval["approved_splits"] == service.APPROVED_SPLITS


def test_approved_model_baseline_family_count_is_9(approval):
    assert len(approval["approved_model_baseline_families"]) == 9
    assert all(row["training_performed"] is False for row in approval["approved_model_baseline_families"])


def test_approved_metric_family_count_is_10(approval):
    assert len(approval["approved_metric_families"]) == 10
    assert all(row["metric_computation_performed"] is False for row in approval["approved_metric_families"])


def test_approved_future_outputs_are_present(approval):
    assert [row["output_id"] for row in approval["approved_future_outputs"]] == service.FUTURE_OUTPUT_IDS
    assert all(row["output_status"] == service.AUTHORIZED_NOT_GENERATED for row in approval["approved_future_outputs"])


def test_per_ticker_approval_entry_count_is_12(approval):
    assert len(approval["per_ticker_approval_entries"]) == 12
    assert [row["ticker"] for row in approval["per_ticker_approval_entries"]] == service.TARGET_UNIVERSE


def test_per_ticker_approval_digests_are_present(approval):
    assert all(len(row["per_ticker_additional_predictive_evidence_execution_approval_digest"]) == 64 for row in approval["per_ticker_approval_entries"])


def test_next_chain_is_defined(approval):
    assert approval["next_chain"] == service.NEXT_CHAIN
    assert approval["next_gates"] == service.NEXT_GATES


def test_risk_controls_are_defined(approval):
    assert approval["risk_controls"] == service.RISK_CONTROLS
    assert len(approval["risk_controls"]) == 17


def test_checklist_passes(approval):
    assert approval["approval_summary"]["total_checks"] == 59
    assert approval["approval_summary"]["passed_checks"] == 59
    assert approval["approval_summary"]["failed_checks"] == 0
    assert approval["approval_summary"]["blocker_count"] == 0
    assert all(set(row) == {"check_id", "status", "expected", "actual", "severity", "message"} for row in approval["approval_checklist"])


def test_approval_digest_is_deterministic(approval):
    rebuilt = service.build_additional_predictive_evidence_execution_approved_using_redesigned_labels_v1(operator_attestation=_attestation())
    assert rebuilt["additional_predictive_evidence_execution_approval_using_redesigned_labels_digest"] == approval["additional_predictive_evidence_execution_approval_using_redesigned_labels_digest"]


def test_per_ticker_approval_digests_are_deterministic(approval):
    rebuilt = service.build_additional_predictive_evidence_execution_approved_using_redesigned_labels_v1(operator_attestation=_attestation())
    assert [row["per_ticker_additional_predictive_evidence_execution_approval_digest"] for row in rebuilt["per_ticker_approval_entries"]] == [row["per_ticker_additional_predictive_evidence_execution_approval_digest"] for row in approval["per_ticker_approval_entries"]]


def test_validator_accepts_valid_approval(approval):
    result = service.validate_additional_predictive_evidence_execution_approved_using_redesigned_labels_v1(approval)
    assert result["valid"] is True
    assert result["blocker_count"] == 0


def test_validator_rejects_wrong_artifact_kind(approval):
    with pytest.raises(service.AdditionalPredictiveEvidenceExecutionApprovalRedesignedLabelsError):
        service.validate_additional_predictive_evidence_execution_approved_using_redesigned_labels_v1(_invalid(approval, "artifact_kind", "WRONG"))


def test_validator_rejects_wrong_approval_status(approval):
    with pytest.raises(service.AdditionalPredictiveEvidenceExecutionApprovalRedesignedLabelsError):
        service.validate_additional_predictive_evidence_execution_approved_using_redesigned_labels_v1(_invalid(approval, "approval_status", "WRONG"))


def test_validator_rejects_approval_false(approval):
    with pytest.raises(service.AdditionalPredictiveEvidenceExecutionApprovalRedesignedLabelsError):
        service.validate_additional_predictive_evidence_execution_approved_using_redesigned_labels_v1(_invalid(approval, "additional_predictive_evidence_execution_approved", False))


def test_validator_rejects_authorization_false(approval):
    with pytest.raises(service.AdditionalPredictiveEvidenceExecutionApprovalRedesignedLabelsError):
        service.validate_additional_predictive_evidence_execution_approved_using_redesigned_labels_v1(_invalid(approval, "additional_predictive_evidence_execution_authorized", False))


def test_validator_rejects_execution_performed_true(approval):
    with pytest.raises(service.AdditionalPredictiveEvidenceExecutionApprovalRedesignedLabelsError):
        service.validate_additional_predictive_evidence_execution_approved_using_redesigned_labels_v1(_invalid(approval, "additional_predictive_evidence_executed", True))


def test_validator_rejects_results_created_true(approval):
    with pytest.raises(service.AdditionalPredictiveEvidenceExecutionApprovalRedesignedLabelsError):
        service.validate_additional_predictive_evidence_execution_approved_using_redesigned_labels_v1(_invalid(approval, "predictive_evidence_results_created", True))


def test_validator_rejects_metric_recomputation_true(approval):
    with pytest.raises(service.AdditionalPredictiveEvidenceExecutionApprovalRedesignedLabelsError):
        service.validate_additional_predictive_evidence_execution_approved_using_redesigned_labels_v1(_invalid(approval, "metric_recomputation_performed", True))


def test_validator_rejects_model_training_true(approval):
    with pytest.raises(service.AdditionalPredictiveEvidenceExecutionApprovalRedesignedLabelsError):
        service.validate_additional_predictive_evidence_execution_approved_using_redesigned_labels_v1(_invalid(approval, "model_training_performed", True))


def test_validator_rejects_predictive_usefulness_accepted(approval):
    with pytest.raises(service.AdditionalPredictiveEvidenceExecutionApprovalRedesignedLabelsError):
        service.validate_additional_predictive_evidence_execution_approved_using_redesigned_labels_v1(_invalid(approval, "predictive_usefulness", "accepted"))


def test_validator_rejects_runtime_authorized(approval):
    with pytest.raises(service.AdditionalPredictiveEvidenceExecutionApprovalRedesignedLabelsError):
        service.validate_additional_predictive_evidence_execution_approved_using_redesigned_labels_v1(_invalid(approval, "runtime_use", "AUTHORIZED"))


def test_validator_rejects_trade_recommendations_true(approval):
    with pytest.raises(service.AdditionalPredictiveEvidenceExecutionApprovalRedesignedLabelsError):
        service.validate_additional_predictive_evidence_execution_approved_using_redesigned_labels_v1(_invalid(approval, "trade_recommendations_generated", True))


def test_validator_rejects_wrong_operator_decision(approval):
    changed = deepcopy(approval)
    changed["operator_attestation"]["operator_decision"] = "WRONG"
    with pytest.raises(service.AdditionalPredictiveEvidenceExecutionApprovalRedesignedLabelsError):
        service.validate_additional_predictive_evidence_execution_approved_using_redesigned_labels_v1(changed)


def test_validator_rejects_wrong_attestation_phrase(approval):
    changed = deepcopy(approval)
    changed["operator_attestation"]["operator_attestation_phrase"] = "WRONG"
    with pytest.raises(service.AdditionalPredictiveEvidenceExecutionApprovalRedesignedLabelsError):
        service.validate_additional_predictive_evidence_execution_approved_using_redesigned_labels_v1(changed)


def test_validator_rejects_missing_risk_controls(approval):
    changed = deepcopy(approval)
    changed.pop("risk_controls")
    with pytest.raises(service.AdditionalPredictiveEvidenceExecutionApprovalRedesignedLabelsError):
        service.validate_additional_predictive_evidence_execution_approved_using_redesigned_labels_v1(changed)


def test_markdown_includes_required_sections(approval):
    markdown = service.build_additional_predictive_evidence_execution_approved_using_redesigned_labels_markdown_v1(approval)
    for section in (
        "Title",
        "Additional Predictive Evidence Execution Approval Using Redesigned Labels",
        "Operator Attestation",
        "Bound Evidence",
        "Dataset and Universe",
        "Approved Source Redesigned Label Profile",
        "Approved Source Feature Profile",
        "Approved Source Inputs",
        "Approved Execution Activities",
        "Approved Feature / Label Matrix",
        "Approved Splits",
        "Approved Model and Baseline Families",
        "Approved Metric Families",
        "Approved Future Outputs",
        "Per-Ticker Approval Entries",
        "Next Chain",
        "Next Gates",
        "Risk Controls",
        "Checklist Summary",
        "Guardrails",
    ):
        assert f"## {section}" in markdown
