from copy import deepcopy
import json

import pytest

from marketflow.services import (
    marketflow_repository_integration_branch_validation_failure_remediation_approval_service as service,
)


def _attestation_kwargs():
    values = {
        "operator_reference": "TEST_OPERATOR",
        "operator_attestation_timestamp_utc": "2026-08-29T00:00:00Z",
        "operator_attestation_phrase": service.REQUIRED_OPERATOR_ATTESTATION_PHRASE,
        "operator_confirms_source_operator_review_digest": service.EXPECTED_SOURCE_OPERATOR_REVIEW_DIGEST,
        "operator_confirms_source_candidate_digest": service.EXPECTED_SOURCE_CANDIDATE_DIGEST,
        "operator_confirms_source_diagnosis_digest": service.EXPECTED_SOURCE_DIAGNOSIS_DIGEST,
        "operator_confirms_source_approval_digest": service.EXPECTED_SOURCE_APPROVAL_DIGEST,
        "operator_confirms_attempted_execution_commit": service.ATTEMPTED_EXECUTION_COMMIT,
        "operator_confirms_integration_branch_name": service.INTEGRATION_BRANCH_NAME,
        "operator_confirms_integration_head_commit": service.INTEGRATION_HEAD_COMMIT,
        "operator_confirms_selected_remediation_package": service.SELECTED_REMEDIATION_PACKAGE,
    }
    values.update({field: True for field in service.ATTESTATION_TRUE_FIELDS})
    return values


@pytest.fixture
def attestation():
    return service.build_marketflow_repository_integration_branch_validation_failure_remediation_approval_attestation_v1(
        **_attestation_kwargs()
    )


@pytest.fixture
def approval(attestation):
    return service.build_marketflow_repository_integration_branch_validation_failure_remediation_approval_v1(
        operator_attestation=attestation
    )


def test_attestation_builder_creates_all_required_fields(attestation):
    assert attestation["operator_reference"] == "TEST_OPERATOR"
    assert attestation["operator_decision"] == service.OPERATOR_DECISION
    assert attestation["operator_attestation_phrase"] == service.REQUIRED_OPERATOR_ATTESTATION_PHRASE
    assert attestation["operator_attestation_version"] == service.OPERATOR_ATTESTATION_VERSION
    assert attestation["selected_remediation_package"] == service.SELECTED_REMEDIATION_PACKAGE
    assert all(attestation[field] is True for field in service.ATTESTATION_TRUE_FIELDS)


def test_approval_builds_offline_and_deterministically(attestation, approval):
    assert service.build_marketflow_repository_integration_branch_validation_failure_remediation_approval_v1(operator_attestation=attestation) == approval
    assert approval["created_offline"] is True
    assert approval["governance_only"] is True


def test_approval_accepts_valid_explicit_source_review(attestation, approval):
    source_review = service.source.build_marketflow_repository_integration_branch_validation_failure_remediation_candidate_operator_review_v1()
    assert service.build_marketflow_repository_integration_branch_validation_failure_remediation_approval_v1(source_review=source_review, operator_attestation=attestation) == approval


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("artifact_kind", service.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_APPROVED),
        ("schema_version", service.SCHEMA_VERSION_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_APPROVAL_V1),
        ("approval_status", service.MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_APPROVED),
        ("approval_scope", service.REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_APPROVAL_ONLY_NOT_EXECUTION_NOT_RETRY_NOT_RESULTS_REVIEW),
        ("selected_remediation_package", service.SELECTED_REMEDIATION_PACKAGE),
        ("operator_attestation_required", True),
        ("source_remediation_operator_review_digest", service.EXPECTED_SOURCE_OPERATOR_REVIEW_DIGEST),
        ("source_remediation_candidate_digest", service.EXPECTED_SOURCE_CANDIDATE_DIGEST),
        ("source_failure_diagnosis_digest", service.EXPECTED_SOURCE_DIAGNOSIS_DIGEST),
        ("source_merge_strategy_approval_digest", service.EXPECTED_SOURCE_APPROVAL_DIGEST),
        ("attempted_execution_branch", "feature/marketflow-repository-integration-branch-execution-v1"),
        ("attempted_execution_commit", service.ATTEMPTED_EXECUTION_COMMIT),
        ("integration_branch_name", service.INTEGRATION_BRANCH_NAME),
        ("integration_branch_head_commit", service.INTEGRATION_HEAD_COMMIT),
        ("integration_base_commit", "eda58d9a56656641d4e0c2a80a6e572b6e949fc2"),
        ("integration_source_commit", "71ed7fa63b27e1572fe7ccfd9b05f38b73a23416"),
        ("first_integration_pytest_authoritative", True),
        ("first_integration_pytest_passed", False),
        ("first_integration_pytest_passed_count", 24481),
        ("first_integration_pytest_failed_count", 1300),
        ("first_integration_pytest_error_count", 500),
        ("first_integration_pytest_skipped_count", 7),
        ("later_isolated_rerun_passed", True),
        ("later_isolated_rerun_passed_count", 26842),
        ("later_isolated_rerun_skipped_count", 7),
        ("later_isolated_rerun_overrides_first_failure", False),
        ("diagnosed_root_cause", "DETACHED_INTEGRATION_WORKTREE_LACKED_IGNORED_ACQUISITION_EVIDENCE_ROOT"),
        ("remediation_selected", True),
        ("remediation_approved", True),
        ("remediation_authorized", True),
        ("remediation_approval_created", True),
        ("ready_for_remediation_execution", True),
        ("remediation_executed", False),
        ("evidence_staged", False),
        ("marketflow_outputs_copied", False),
        ("marketflow_outputs_committed", False),
        ("evidence_regenerated", False),
        ("integration_retry_candidate_created", False),
        ("integration_retry_executed", False),
        ("integration_results_review_created", False),
        ("integration_execution_successful", False),
        ("successful_execution_digest_generated", False),
        ("successful_validation_digest_generated", False),
        ("integration_branch_pushed", False),
        ("remote_integration_branch_created", False),
        ("main_merge_performed", False),
        ("main_push_performed", False),
        ("origin_main_modified_by_this_task", False),
        ("tracked_marketflow_file_count", 0),
        ("no_tracked_marketflow_files", True),
        ("provider_requests_made_in_approval", False),
        ("market_data_acquisition_performed_in_approval", False),
        ("dataset_generation_performed_in_approval", False),
        ("metric_recomputation_from_raw_rows_performed", False),
        ("model_training_performed", False),
        ("strategy_scoring_performed", False),
        ("trade_recommendations_generated", False),
        ("predictive_usefulness", "not accepted"),
        ("profitability", "not accepted"),
        ("runtime_use", "NOT_AUTHORIZED"),
        ("broker_execution", "NOT_AUTHORIZED"),
        ("future_plan_approval_status", "APPROVED_FOR_FUTURE_REMEDIATION_EXECUTION_ONLY"),
        ("future_plan_execution_status", "NOT_EXECUTED"),
        ("integration_retry_allowed_now", False),
        ("integration_results_review_ready", False),
        ("recommended_next_task", service.RECOMMENDED_NEXT_TASK),
    ],
)
def test_required_approval_fields(approval, field, expected):
    assert approval[field] == expected


def test_operator_attestation_is_bound_exactly(approval, attestation):
    assert approval["operator_attestation"] == attestation
    for field, expected in service.ATTESTATION_STRING_FIELDS.items():
        assert attestation[field] == expected
    assert all(attestation[field] is True for field in service.ATTESTATION_TRUE_FIELDS)


def test_selected_package_is_approved_for_future_execution_only(approval):
    assert approval["approved_selected_package"] == service.APPROVED_SELECTED_PACKAGE
    package = approval["approved_selected_package"]
    assert package["selected"] is True
    assert package["approved"] is True
    assert package["authorized_for_future_execution"] is True
    assert package["executed"] is False


def test_requirements_and_plan_are_approved_but_not_executed(approval):
    assert approval["approved_future_remediation_requirements"] == service.APPROVED_FUTURE_REMEDIATION_REQUIREMENTS
    assert len(approval["approved_future_remediation_requirements"]) == 16
    assert all(row["approval_status"] == "APPROVED_FOR_FUTURE_REMEDIATION_EXECUTION_ONLY" for row in approval["approved_future_remediation_requirements"])
    assert approval["approved_future_remediation_plan"] == service.APPROVED_FUTURE_REMEDIATION_PLAN
    assert len(approval["approved_future_remediation_plan"]) == 10
    assert all(row["execution_status"] == "NOT_EXECUTED" for row in approval["approved_future_remediation_plan"])


def test_supporting_and_blocked_packages_remain_closed(approval):
    assert approval["supporting_packages"] == service.SUPPORTING_PACKAGES
    assert len(approval["supporting_packages"]) == 3
    assert all(row["approval_status"] == "AVAILABLE_NOT_SELECTED" for row in approval["supporting_packages"])
    assert all(row["selected"] is False for row in approval["supporting_packages"])
    assert approval["blocked_packages"] == service.BLOCKED_PACKAGES
    assert len(approval["blocked_packages"]) == 2
    assert all(row["approval_status"] == "BLOCKED_NOT_APPROVED" for row in approval["blocked_packages"])
    assert all(row["approved"] is False for row in approval["blocked_packages"])


def test_next_chain_gates_and_risk_controls(approval):
    assert approval["next_chain"] == service.NEXT_CHAIN
    assert len(approval["next_chain"]) == 7
    assert approval["next_gates"] == service.NEXT_GATES
    assert len(approval["next_gates"]) == 7
    assert approval["risk_controls"] == service.RISK_CONTROLS
    assert len(approval["risk_controls"]) == 41


def test_checklist_and_summary_pass(approval):
    assert [row["check_id"] for row in approval["checklist"]] == service.REQUIRED_CHECK_IDS
    assert all(row["status"] == "PASS" for row in approval["checklist"])
    assert all(set(row) == {"check_id", "status", "expected", "actual", "severity", "message"} for row in approval["checklist"])
    assert approval["summary"]["total_checks"] == len(service.REQUIRED_CHECK_IDS) == 53
    assert approval["summary"]["passed_checks"] == 53
    assert approval["summary"]["failed_checks"] == 0
    assert approval["summary"]["blocker_count"] == 0
    assert approval["summary"]["ready_for_remediation_execution"] is True
    assert approval["summary"]["remediation_executed"] is False


def test_approval_digest_is_deterministic(approval):
    assert approval["marketflow_repository_integration_branch_validation_failure_remediation_approval_digest"] == service.marketflow_repository_integration_branch_validation_failure_remediation_approval_digest_v1(approval)


def test_validator_accepts_valid_approval(approval):
    result = service.validate_marketflow_repository_integration_branch_validation_failure_remediation_approval_v1(approval)
    assert result["status"] == service.MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_APPROVAL_VALID
    assert result["failed_checks"] == 0
    assert result["blocker_count"] == 0


@pytest.mark.parametrize(
    ("field", "bad_value"),
    [
        ("artifact_kind", "WRONG"),
        ("approval_status", "WRONG"),
        ("approval_scope", "WRONG"),
        ("selected_remediation_package", "WRONG"),
        ("source_remediation_operator_review_digest", "0" * 64),
        ("source_remediation_candidate_digest", "0" * 64),
        ("source_failure_diagnosis_digest", "0" * 64),
        ("source_merge_strategy_approval_digest", "0" * 64),
        ("attempted_execution_commit", ""),
        ("integration_branch_name", ""),
        ("integration_branch_head_commit", ""),
        ("first_integration_pytest_authoritative", False),
        ("later_isolated_rerun_overrides_first_failure", True),
        ("remediation_approval_created", False),
        ("remediation_selected", False),
        ("remediation_approved", False),
        ("remediation_authorized", False),
        ("ready_for_remediation_execution", False),
        ("remediation_executed", True),
        ("evidence_staged", True),
        ("marketflow_outputs_copied", True),
        ("marketflow_outputs_committed", True),
        ("evidence_regenerated", True),
        ("integration_retry_candidate_created", True),
        ("integration_retry_executed", True),
        ("integration_results_review_created", True),
        ("integration_execution_successful", True),
        ("successful_execution_digest_generated", True),
        ("successful_validation_digest_generated", True),
        ("integration_branch_pushed", True),
        ("main_push_performed", True),
        ("origin_main_modified_by_this_task", True),
        ("provider_requests_made_in_approval", True),
        ("market_data_acquisition_performed_in_approval", True),
        ("dataset_generation_performed_in_approval", True),
        ("metric_recomputation_from_raw_rows_performed", True),
        ("model_training_performed", True),
        ("strategy_scoring_performed", True),
        ("trade_recommendations_generated", True),
        ("predictive_usefulness", "accepted"),
        ("profitability", "accepted"),
        ("runtime_use", "AUTHORIZED"),
        ("broker_execution", "AUTHORIZED"),
        ("risk_controls", []),
    ],
)
def test_validator_rejects_invalid_approval_boundaries(approval, field, bad_value):
    invalid = deepcopy(approval)
    invalid[field] = bad_value
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchValidationFailureRemediationApprovalError):
        service.validate_marketflow_repository_integration_branch_validation_failure_remediation_approval_v1(invalid)


@pytest.mark.parametrize(
    ("field", "bad_value"),
    [
        ("operator_decision", "WRONG"),
        ("operator_attestation_phrase", "WRONG"),
        ("operator_confirms_source_operator_review_digest", "0" * 64),
        ("operator_confirms_source_candidate_digest", "0" * 64),
        ("operator_confirms_source_diagnosis_digest", "0" * 64),
        ("operator_confirms_source_approval_digest", "0" * 64),
        ("operator_confirms_attempted_execution_commit", "0" * 40),
        ("operator_confirms_integration_branch_name", "WRONG"),
        ("operator_confirms_integration_head_commit", "0" * 40),
        ("operator_confirms_selected_remediation_package", "WRONG"),
        ("selected_remediation_package", "WRONG"),
    ],
)
def test_attestation_builder_rejects_changed_string_confirmation(field, bad_value):
    kwargs = _attestation_kwargs()
    kwargs[field] = bad_value
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchValidationFailureRemediationApprovalError):
        service.build_marketflow_repository_integration_branch_validation_failure_remediation_approval_attestation_v1(**kwargs)


@pytest.mark.parametrize("field", service.ATTESTATION_TRUE_FIELDS)
def test_attestation_builder_rejects_each_missing_closed_boundary(field):
    kwargs = _attestation_kwargs()
    kwargs[field] = False
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchValidationFailureRemediationApprovalError):
        service.build_marketflow_repository_integration_branch_validation_failure_remediation_approval_attestation_v1(**kwargs)


def test_validator_rejects_mutated_bound_attestation(approval):
    invalid = deepcopy(approval)
    invalid["operator_attestation"]["operator_attestation_phrase"] = "WRONG"
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchValidationFailureRemediationApprovalError):
        service.validate_marketflow_repository_integration_branch_validation_failure_remediation_approval_v1(invalid)


def test_builder_rejects_invalid_source_review(attestation):
    source_review = service.source.build_marketflow_repository_integration_branch_validation_failure_remediation_candidate_operator_review_v1()
    source_review["source_remediation_candidate_digest"] = "0" * 64
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchValidationFailureRemediationApprovalError):
        service.build_marketflow_repository_integration_branch_validation_failure_remediation_approval_v1(source_review=source_review, operator_attestation=attestation)


def test_validator_rejects_missing_digest(approval):
    approval.pop("marketflow_repository_integration_branch_validation_failure_remediation_approval_digest")
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchValidationFailureRemediationApprovalError):
        service.validate_marketflow_repository_integration_branch_validation_failure_remediation_approval_v1(approval)


def test_markdown_includes_required_sections_without_secret_material(approval):
    markdown = service.build_marketflow_repository_integration_branch_validation_failure_remediation_approval_markdown_v1(approval)
    for title in (
        "MarketFlow Repository Integration Branch Validation Failure Remediation Approval v1",
        "Operator Attestation", "Source Operator Review", "Failure Summary", "Root Cause",
        "Approval Scope", "Selected Remediation Package", "Approved Future Requirements",
        "Approved Future Plan", "Supporting Packages", "Blocked Packages", "Next Chain",
        "Next Gates", "Risk Controls", "Authority Boundaries", "Checklist Summary", "Guardrails",
    ):
        assert title in markdown
    assert "API key" not in markdown
    assert "raw payload" not in markdown


def test_writer_round_trips_without_overwrite(tmp_path, attestation, approval):
    receipt = service.write_marketflow_repository_integration_branch_validation_failure_remediation_approval_v1(tmp_path, operator_attestation=attestation)
    payload = json.loads((tmp_path / "marketflow_repository_integration_branch_validation_failure_remediation_approval_v1.json").read_text(encoding="utf-8"))
    assert payload == approval
    assert receipt["marketflow_repository_integration_branch_validation_failure_remediation_approval_digest"] == approval["marketflow_repository_integration_branch_validation_failure_remediation_approval_digest"]
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchValidationFailureRemediationApprovalError):
        service.write_marketflow_repository_integration_branch_validation_failure_remediation_approval_v1(tmp_path, operator_attestation=attestation)
