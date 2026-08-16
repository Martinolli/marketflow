from __future__ import annotations

from copy import deepcopy

import pytest

from marketflow.services import (
    additional_predictive_evidence_execution_approval_for_refined_evidence_service as service,
)


def _attestation(**overrides):
    values = {
        "operator_reference": "TEST_OPERATOR",
        "operator_attestation_timestamp_utc": "2026-08-16T12:00:00Z",
        "operator_attestation_phrase": service.REQUIRED_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVAL_FOR_REFINED_EVIDENCE_ATTESTATION_PHRASE,
        **service.DIGEST_CONFIRMATIONS,
        **service.VALUE_CONFIRMATIONS,
        **{field: True for field in service.BOOLEAN_CONFIRMATIONS},
    }
    values.update(overrides)
    return service.build_additional_predictive_evidence_execution_approval_for_refined_evidence_attestation_v1(
        **values
    )


@pytest.fixture(scope="module")
def approved():
    return service.build_additional_predictive_evidence_execution_approved_for_refined_evidence_v1(
        operator_attestation=_attestation()
    )


def test_attestation_builder_creates_required_fields():
    attestation = _attestation()
    assert attestation["operator_reference"] == "TEST_OPERATOR"
    assert attestation["operator_decision"] == service.OPERATOR_DECISION_APPROVE_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_FOR_REFINED_EVIDENCE
    assert attestation["operator_attestation_version"] == service.OPERATOR_ATTESTATION_VERSION_V1
    assert set(service.DIGEST_CONFIRMATIONS) <= set(attestation)
    assert set(service.VALUE_CONFIRMATIONS) <= set(attestation)
    assert set(service.BOOLEAN_CONFIRMATIONS) <= set(attestation)


def test_artifact_builds_offline_without_provider_calls(approved):
    assert approved["created_offline"] is True
    assert approved["provider_requests_made_in_approval"] is False
    assert approved["live_provider_transport_enabled_in_approval"] is False


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("artifact_kind", service.ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVED_FOR_REFINED_EVIDENCE),
        ("approval_status", service.ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVED_FOR_REFINED_EVIDENCE),
        ("approval_scope", service.ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVAL_FOR_REFINED_EVIDENCE_ONLY),
        ("additional_predictive_evidence_execution_for_refined_evidence_approved", True),
        ("additional_predictive_evidence_execution_for_refined_evidence_authorized", True),
        ("ready_for_additional_predictive_evidence_execution_for_refined_evidence", True),
        ("additional_predictive_evidence_execution_for_refined_evidence_executed", False),
        ("additional_predictive_evidence_results_for_refined_evidence_created", False),
        ("additional_predictive_evidence_execution_candidate_for_refined_evidence_review_package_digest", service.EXPECTED_REFINED_EVIDENCE_CANDIDATE_REVIEW_PACKAGE_DIGEST),
        ("additional_predictive_evidence_execution_candidate_for_refined_evidence_digest", service.EXPECTED_REFINED_EVIDENCE_CANDIDATE_DIGEST),
        ("feature_label_refinement_results_review_package_digest", service.EXPECTED_FEATURE_LABEL_REFINEMENT_RESULTS_REVIEW_DIGEST),
        ("feature_label_refinement_execution_digest", service.EXPECTED_FEATURE_LABEL_REFINEMENT_EXECUTION_DIGEST),
        ("feature_label_refinement_execution_approval_digest", service.EXPECTED_FEATURE_LABEL_REFINEMENT_EXECUTION_APPROVAL_DIGEST),
        ("additional_predictive_evidence_results_review_package_digest", service.EXPECTED_ADDITIONAL_PREDICTIVE_EVIDENCE_RESULTS_REVIEW_DIGEST),
        ("additional_predictive_evidence_execution_digest", service.EXPECTED_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_DIGEST),
        ("research_registry_approval_digest", service.EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST),
        ("records_digest", service.EXPECTED_RECORDS_DIGEST),
        ("target_universe_count", 12),
        ("target_universe", service.TARGET_UNIVERSE),
        ("meta_record_count", 913),
        ("non_meta_record_count", 1003),
        ("refined_label_family_count", 7),
        ("refined_feature_group_count", 9),
        ("refined_feature_field_count", 19),
        ("refined_protocol_group_count", 6),
        ("model_comparison_group_count", 5),
        ("refined_leakage_status", "PASS"),
        ("predictive_usefulness", "not accepted"),
        ("predictive_usefulness_acceptance_ready", False),
        ("predictive_usefulness_acceptance_candidate_created", False),
        ("profitability", "not accepted"),
        ("runtime_migration_approved", False),
        ("runtime_use", "NOT_AUTHORIZED"),
        ("strategy_use", "NOT_AUTHORIZED"),
        ("paper_trading", "NOT_AUTHORIZED"),
        ("broker_execution", "NOT_AUTHORIZED"),
        ("new_strategy_scoring_performed", False),
        ("trade_recommendations_generated", False),
        ("raw_provider_payloads_committed", False),
        ("api_keys_stored_or_printed", False),
    ],
)
def test_approval_fields(approved, field, expected):
    assert approved[field] == expected


def test_approved_activity_and_output_counts(approved):
    assert len(approved["approved_refined_evidence_execution_activities"]) == 11
    assert all(item["authorization_status"] == "AUTHORIZED_NOT_EXECUTED" for item in approved["approved_refined_evidence_execution_activities"])
    assert all(item["execution_status"] == "NOT_EXECUTED" for item in approved["approved_refined_evidence_execution_activities"])
    assert len(approved["future_refined_execution_outputs"]) == 10
    assert all(item["output_status"] == "AUTHORIZED_NOT_GENERATED" for item in approved["future_refined_execution_outputs"])
    assert all(item["generated"] is False for item in approved["future_refined_execution_outputs"])


def test_per_ticker_entries_preserve_source_limitation(approved):
    entries = approved["per_ticker_execution_approval_entries"]
    assert [entry["ticker"] for entry in entries] == service.TARGET_UNIVERSE
    assert len(entries) == 12
    meta = next(entry for entry in entries if entry["ticker"] == "META")
    assert meta["historical_record_count"] == 913
    assert meta["meta_reduced_record_count_flag"] is True
    assert all(entry["historical_record_count"] == 1003 for entry in entries if entry["ticker"] != "META")
    assert all(entry["per_ticker_additional_predictive_evidence_execution_approval_for_refined_evidence_digest"] for entry in entries)


@pytest.mark.parametrize(
    "field",
    [
        *service.DIGEST_CONFIRMATIONS,
        "operator_confirms_target_universe",
        "operator_confirms_target_count",
        "operator_confirms_meta_record_count",
        "operator_confirms_non_meta_record_count",
        "operator_confirms_refined_label_family_count",
        "operator_confirms_refined_feature_group_count",
        "operator_confirms_refined_feature_field_count",
        "operator_confirms_refined_protocol_group_count",
        "operator_confirms_model_comparison_group_count",
        "operator_confirms_refined_leakage_status",
    ],
)
def test_wrong_attestation_value_is_rejected(field):
    wrong = [] if field == "operator_confirms_target_universe" else "WRONG"
    with pytest.raises(service.AdditionalPredictiveEvidenceExecutionApprovalForRefinedEvidenceError):
        service.build_additional_predictive_evidence_execution_approved_for_refined_evidence_v1(
            operator_attestation=_attestation(**{field: wrong})
        )


@pytest.mark.parametrize("field", service.BOOLEAN_CONFIRMATIONS)
def test_missing_boundary_confirmation_is_rejected(field):
    with pytest.raises(service.AdditionalPredictiveEvidenceExecutionApprovalForRefinedEvidenceError):
        service.build_additional_predictive_evidence_execution_approved_for_refined_evidence_v1(
            operator_attestation=_attestation(**{field: False})
        )


@pytest.mark.parametrize(
    ("field", "wrong"),
    [
        ("operator_attestation_phrase", "WRONG"),
        ("operator_decision", "WRONG"),
        ("operator_reference", ""),
        ("operator_attestation_timestamp_utc", ""),
    ],
)
def test_invalid_attestation_identity_or_decision_is_rejected(field, wrong):
    with pytest.raises(service.AdditionalPredictiveEvidenceExecutionApprovalForRefinedEvidenceError):
        service.build_additional_predictive_evidence_execution_approved_for_refined_evidence_v1(
            operator_attestation=_attestation(**{field: wrong})
        )


@pytest.mark.parametrize(
    ("field", "wrong"),
    [
        ("artifact_kind", "WRONG"),
        ("approval_status", "WRONG"),
        ("approval_scope", "WRONG"),
        ("additional_predictive_evidence_execution_for_refined_evidence_approved", False),
        ("additional_predictive_evidence_execution_for_refined_evidence_authorized", False),
        ("ready_for_additional_predictive_evidence_execution_for_refined_evidence", False),
        ("additional_predictive_evidence_execution_for_refined_evidence_executed", True),
        ("additional_predictive_evidence_results_for_refined_evidence_created", True),
        ("target_universe", ["META"]),
        ("target_universe_count", 11),
        ("records_digest", "WRONG"),
        ("meta_record_count", 1003),
        ("non_meta_record_count", 913),
        ("refined_label_family_count", 6),
        ("refined_feature_group_count", 8),
        ("refined_feature_field_count", 18),
        ("refined_protocol_group_count", 5),
        ("model_comparison_group_count", 4),
        ("refined_leakage_status", "FAIL"),
        ("provider_requests_made_in_approval", True),
        ("live_provider_transport_enabled_in_approval", True),
        ("market_data_acquisition_performed_in_approval", True),
        ("dataset_generation_performed_in_approval", True),
        ("canonical_dataset_regenerated_in_approval", True),
        ("feature_label_refinement_execution_rerun_performed", True),
        ("refined_label_generation_rerun_performed", True),
        ("refined_feature_generation_rerun_performed", True),
        ("refined_walk_forward_validation_rerun_performed", True),
        ("refined_out_of_sample_evaluation_rerun_performed", True),
        ("refined_metrics_recomputation_performed", True),
        ("model_comparison_rerun_performed", True),
        ("additional_predictive_evidence_execution_performed", True),
        ("predictive_usefulness", "accepted"),
        ("predictive_usefulness_acceptance_ready", True),
        ("predictive_usefulness_acceptance_recommended", True),
        ("predictive_usefulness_acceptance_candidate_created", True),
        ("profitability", "accepted"),
        ("profitability_acceptance_ready", True),
        ("profitability_acceptance_recommended", True),
        ("runtime_migration_approved", True),
        ("runtime_use", "AUTHORIZED"),
        ("strategy_use", "AUTHORIZED"),
        ("paper_trading", "AUTHORIZED"),
        ("broker_execution", "AUTHORIZED"),
        ("automatic_stitching", True),
        ("new_strategy_scoring_performed", True),
        ("trade_recommendations_generated", True),
        ("raw_provider_payloads_committed", True),
        ("api_keys_stored_or_printed", True),
    ],
)
def test_validator_rejects_contract_mutation(approved, field, wrong):
    mutated = deepcopy(approved)
    mutated[field] = wrong
    with pytest.raises(service.AdditionalPredictiveEvidenceExecutionApprovalForRefinedEvidenceError):
        service.validate_additional_predictive_evidence_execution_approved_for_refined_evidence_v1(mutated)


@pytest.mark.parametrize("field", service.FALSE_BOUNDARY_FIELDS)
def test_validator_rejects_every_false_boundary_when_true(approved, field):
    mutated = deepcopy(approved)
    mutated[field] = True
    with pytest.raises(service.AdditionalPredictiveEvidenceExecutionApprovalForRefinedEvidenceError):
        service.validate_additional_predictive_evidence_execution_approved_for_refined_evidence_v1(mutated)


def test_validator_accepts_valid_approval(approved):
    result = service.validate_additional_predictive_evidence_execution_approved_for_refined_evidence_v1(approved)
    assert result["valid"] is True
    assert result["failed_checks"] == 0
    assert result["blocker_count"] == 0


def test_missing_approval_digest_is_rejected(approved):
    mutated = deepcopy(approved)
    mutated.pop("additional_predictive_evidence_execution_approval_for_refined_evidence_digest")
    with pytest.raises(service.AdditionalPredictiveEvidenceExecutionApprovalForRefinedEvidenceError):
        service.validate_additional_predictive_evidence_execution_approved_for_refined_evidence_v1(mutated)


def test_missing_per_ticker_digest_is_rejected(approved):
    mutated = deepcopy(approved)
    mutated["per_ticker_execution_approval_entries"][0].pop(
        "per_ticker_additional_predictive_evidence_execution_approval_for_refined_evidence_digest"
    )
    with pytest.raises(service.AdditionalPredictiveEvidenceExecutionApprovalForRefinedEvidenceError):
        service.validate_additional_predictive_evidence_execution_approved_for_refined_evidence_v1(mutated)


def test_approval_and_per_ticker_digests_are_deterministic():
    first = service.build_additional_predictive_evidence_execution_approved_for_refined_evidence_v1(operator_attestation=_attestation())
    second = service.build_additional_predictive_evidence_execution_approved_for_refined_evidence_v1(operator_attestation=_attestation())
    assert first["additional_predictive_evidence_execution_approval_for_refined_evidence_digest"] == second["additional_predictive_evidence_execution_approval_for_refined_evidence_digest"]
    assert [item["per_ticker_additional_predictive_evidence_execution_approval_for_refined_evidence_digest"] for item in first["per_ticker_execution_approval_entries"]] == [item["per_ticker_additional_predictive_evidence_execution_approval_for_refined_evidence_digest"] for item in second["per_ticker_execution_approval_entries"]]


def test_markdown_includes_required_sections(approved):
    markdown = service.build_additional_predictive_evidence_execution_approved_for_refined_evidence_markdown_v1(approved)
    for title in (
        "Approved Additional Predictive Evidence Execution for Refined Evidence",
        "Operator Attestation",
        "Source Refined-Evidence Candidate Review",
        "Source Feature/Label Refinement Results Review",
        "Registry-Approved Dataset Metadata",
        "Target Universe",
        "Approved Refined Evidence Source Profile",
        "Approved Refined Evidence Facts",
        "Approved Execution Activities",
        "Future Execution Outputs",
        "Per-Ticker Approval Entries",
        "Execution Boundary",
        "Predictive Usefulness Boundary",
        "Profitability Boundary",
        "Runtime Boundary",
        "Checklist Summary",
        "Remaining Required Tasks",
        "Guardrails",
    ):
        assert f"## {title}" in markdown


def test_writer_uses_isolated_directory_and_refuses_overwrite(tmp_path):
    result = service.write_additional_predictive_evidence_execution_approved_for_refined_evidence_v1(
        tmp_path, operator_attestation=_attestation()
    )
    assert result["approved_artifact"]["artifact_kind"] == service.ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_APPROVED_FOR_REFINED_EVIDENCE
    assert result["json_sha256"]
    with pytest.raises(FileExistsError):
        service.write_additional_predictive_evidence_execution_approved_for_refined_evidence_v1(
            tmp_path, operator_attestation=_attestation()
        )
