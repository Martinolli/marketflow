from __future__ import annotations

import json
from copy import deepcopy

import pytest

from marketflow.services import (
    marketflow_repository_integration_branch_retry_approval_service as service,
)
from marketflow.services import (
    marketflow_repository_integration_branch_retry_candidate_operator_review_service as review_service,
)


def _attestation_kwargs() -> dict:
    values = {
        "operator_reference": "TEST_OPERATOR",
        "operator_attestation_timestamp_utc": "2026-08-30T00:00:00Z",
        "operator_attestation_phrase": service.REQUIRED_OPERATOR_ATTESTATION_PHRASE,
        "operator_confirms_source_operator_review_digest": service.EXPECTED_SOURCE_OPERATOR_REVIEW_DIGEST,
        "operator_confirms_source_retry_candidate_digest": service.EXPECTED_SOURCE_RETRY_CANDIDATE_DIGEST,
        "operator_confirms_source_remediation_results_review_digest": service.EXPECTED_SOURCE_REMEDIATION_RESULTS_REVIEW_DIGEST,
        "operator_confirms_source_remediation_execution_digest": service.EXPECTED_SOURCE_REMEDIATION_EXECUTION_DIGEST,
        "operator_confirms_source_staged_inventory_digest": service.EXPECTED_SOURCE_STAGED_INVENTORY_DIGEST,
        "operator_confirms_attempted_execution_commit": service.ATTEMPTED_EXECUTION_COMMIT,
        "operator_confirms_original_blocked_status": service.ORIGINAL_BLOCKED_STATUS,
        "operator_confirms_origin_main_commit": service.EXPECTED_ORIGIN_MAIN_COMMIT,
        "operator_confirms_integration_branch_name": service.INTEGRATION_BRANCH_NAME,
        "operator_confirms_integration_branch_head": service.INTEGRATION_HEAD_COMMIT,
        "operator_confirms_detached_worktree_path": service.DETACHED_INTEGRATION_WORKTREE_PATH,
        "operator_confirms_detached_worktree_head": service.INTEGRATION_HEAD_COMMIT,
        "operator_confirms_staged_evidence_root_path": service.STAGED_EVIDENCE_ROOT_PATH,
        "operator_confirms_staged_evidence_digest": service.EXPECTED_SOURCE_STAGED_INVENTORY_DIGEST,
        "operator_confirms_selected_retry_package": service.SELECTED_INTEGRATION_BRANCH_RETRY_PACKAGE,
    }
    values.update({field: True for field in service.ATTESTATION_TRUE_FIELDS})
    return values


@pytest.fixture
def attestation():
    return service.build_marketflow_repository_integration_branch_retry_approval_attestation_v1(
        **_attestation_kwargs()
    )


@pytest.fixture
def approval(attestation):
    return service.build_marketflow_repository_integration_branch_retry_approval_v1(
        operator_attestation=attestation
    )


def test_attestation_builder_creates_required_fields(attestation):
    assert attestation["operator_decision"] == service.OPERATOR_DECISION
    assert (
        attestation["selected_integration_branch_retry_package"]
        == service.SELECTED_INTEGRATION_BRANCH_RETRY_PACKAGE
    )
    assert attestation["operator_attestation_phrase"] == service.REQUIRED_OPERATOR_ATTESTATION_PHRASE
    assert attestation["operator_reference"] == "TEST_OPERATOR"
    assert all(attestation[field] is True for field in service.ATTESTATION_TRUE_FIELDS)


def test_approval_builds_offline(monkeypatch, attestation):
    monkeypatch.setattr(
        review_service,
        "build_marketflow_repository_integration_branch_retry_candidate_operator_review_v1",
        lambda: pytest.fail("source review rebuilt"),
    )
    result = service.build_marketflow_repository_integration_branch_retry_approval_v1(
        operator_attestation=attestation
    )
    assert result["created_offline"] is True
    assert result["governance_only"] is True


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("artifact_kind", service.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_APPROVED),
        ("schema_version", service.SCHEMA_VERSION_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_APPROVAL_V1),
        ("approval_status", service.MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_APPROVED),
        ("approval_scope", service.REPOSITORY_INTEGRATION_BRANCH_RETRY_APPROVAL_ONLY_NOT_EXECUTION_NOT_RESULTS_REVIEW_NOT_MAIN),
        ("selected_integration_branch_retry_package", service.SELECTED_INTEGRATION_BRANCH_RETRY_PACKAGE),
        ("source_integration_branch_retry_operator_review_digest", service.EXPECTED_SOURCE_OPERATOR_REVIEW_DIGEST),
        ("source_integration_branch_retry_candidate_digest", service.EXPECTED_SOURCE_RETRY_CANDIDATE_DIGEST),
        ("source_remediation_results_review_digest", service.EXPECTED_SOURCE_REMEDIATION_RESULTS_REVIEW_DIGEST),
        ("source_remediation_execution_digest", service.EXPECTED_SOURCE_REMEDIATION_EXECUTION_DIGEST),
        ("source_staged_inventory_digest", service.EXPECTED_SOURCE_STAGED_INVENTORY_DIGEST),
        ("attempted_execution_commit", service.ATTEMPTED_EXECUTION_COMMIT),
        ("original_blocked_status", service.ORIGINAL_BLOCKED_STATUS),
        ("first_integration_pytest_authoritative", True),
        ("first_integration_pytest_passed", False),
        ("first_integration_pytest_passed_count", 24481),
        ("first_integration_pytest_failed_count", 1300),
        ("first_integration_pytest_error_count", 500),
        ("first_integration_pytest_skipped_count", 7),
        ("later_wrong_worktree_rerun_diagnostic_only", True),
        ("later_wrong_worktree_rerun_passed_count", 26842),
        ("later_wrong_worktree_rerun_skipped_count", 7),
        ("later_wrong_worktree_rerun_overrides_first_failure", False),
        ("origin_main_commit_at_approval", service.EXPECTED_ORIGIN_MAIN_COMMIT),
        ("integration_branch_head_commit_at_approval", service.INTEGRATION_HEAD_COMMIT),
        ("remote_integration_branch_exists_at_approval", False),
        ("detached_integration_worktree_path", service.DETACHED_INTEGRATION_WORKTREE_PATH),
        ("detached_integration_worktree_head_commit_at_approval", service.INTEGRATION_HEAD_COMMIT),
        ("detached_integration_worktree_is_detached_at_approval", True),
        ("detached_integration_worktree_clean_at_approval", True),
        ("staged_evidence_root_path", service.STAGED_EVIDENCE_ROOT_PATH),
        ("staged_required_manifest_path", service.STAGED_REQUIRED_MANIFEST_PATH),
        ("staged_evidence_file_count_at_approval", 7),
        ("staged_evidence_total_bytes_at_approval", 2458181),
        ("staged_evidence_manifest_digest_at_approval", service.EXPECTED_SOURCE_STAGED_INVENTORY_DIGEST),
        ("staged_evidence_root_untracked_at_approval", True),
        ("integration_branch_retry_selected", True),
        ("integration_branch_retry_approved", True),
        ("integration_branch_retry_authorized", True),
        ("integration_branch_retry_approval_created", True),
        ("ready_for_integration_branch_retry_execution", True),
        ("integration_branch_retry_executed", False),
        ("integration_branch_retry_results_review_created", False),
        ("integration_results_review_created", False),
        ("integration_execution_successful", False),
        ("successful_integration_execution_digest_generated", False),
        ("successful_integration_validation_digest_generated", False),
        ("integration_branch_pushed", False),
        ("remote_integration_branch_created", False),
        ("main_push_performed", False),
        ("origin_main_modified_by_this_task", False),
        ("marketflow_outputs_committed", False),
        ("evidence_regenerated", False),
        ("provider_requests_made_in_approval", False),
        ("market_data_acquisition_performed_in_approval", False),
        ("dataset_generation_performed_in_approval", False),
        ("metric_recomputation_from_raw_rows_performed", False),
        ("model_training_performed", False),
        ("strategy_scoring_performed", False),
        ("trade_recommendations_generated", False),
        ("predictive_usefulness", service.NOT_ACCEPTED),
        ("profitability", service.NOT_ACCEPTED),
        ("runtime_use", service.NOT_AUTHORIZED),
        ("broker_execution", service.NOT_AUTHORIZED),
        ("recommended_next_task", service.RECOMMENDED_NEXT_TASK),
    ],
)
def test_required_approval_fields(approval, field, expected):
    assert approval[field] == expected


def test_selected_package_is_approved_for_future_execution_only(approval):
    package = approval["approved_selected_package"]
    assert package == service.APPROVED_SELECTED_PACKAGE
    assert package["selected"] is True
    assert package["approved"] is True
    assert package["authorized_for_future_execution"] is True
    assert package["executed"] is False


def test_requirements_are_approved_for_future_execution_only(approval):
    requirements = approval["approved_future_retry_requirements"]
    assert len(requirements) == 18
    assert all(
        row["approval_status"]
        == service.APPROVED_FOR_FUTURE_INTEGRATION_RETRY_EXECUTION_ONLY
        for row in requirements
    )


def test_future_plan_is_approved_but_not_executed(approval):
    plan = approval["approved_future_retry_plan"]
    assert len(plan) == 12
    assert all(
        row["approval_status"]
        == service.APPROVED_FOR_FUTURE_INTEGRATION_RETRY_EXECUTION_ONLY
        for row in plan
    )
    assert all(row["execution_status"] == service.NOT_EXECUTED for row in plan)
    assert approval["future_plan_execution_status"] == service.NOT_EXECUTED


def test_supporting_packages_are_available_and_not_selected(approval):
    packages = approval["supporting_packages"]
    assert len(packages) == 3
    assert all(row["approval_status"] == service.AVAILABLE_NOT_SELECTED for row in packages)
    assert all(row["selected"] is False for row in packages)
    assert all(row["approved"] is False for row in packages)


def test_blocked_packages_are_not_approved(approval):
    packages = approval["blocked_packages"]
    assert len(packages) == 2
    assert all(row["approval_status"] == service.BLOCKED_NOT_APPROVED for row in packages)
    assert all(row["approved"] is False for row in packages)


def test_next_chain_gates_and_risk_controls_are_exact(approval):
    assert approval["next_chain"] == service.NEXT_CHAIN
    assert approval["next_gates"] == service.NEXT_GATES
    assert approval["risk_controls"] == service.RISK_CONTROLS


def test_checklist_and_summary_pass(approval):
    assert [row["check_id"] for row in approval["checklist"]] == service.REQUIRED_CHECK_IDS
    assert all(row["status"] == service.PASS for row in approval["checklist"])
    assert approval["summary"]["total_checks"] == len(service.REQUIRED_CHECK_IDS)
    assert approval["summary"]["passed_checks"] == len(service.REQUIRED_CHECK_IDS)
    assert approval["summary"]["failed_checks"] == 0
    assert approval["summary"]["blocker_count"] == 0


def test_approval_digest_is_deterministic(attestation, approval):
    other = service.build_marketflow_repository_integration_branch_retry_approval_v1(
        operator_attestation=attestation
    )
    assert approval == other
    assert (
        approval["marketflow_repository_integration_branch_retry_approval_digest"]
        == service.marketflow_repository_integration_branch_retry_approval_digest_v1(approval)
    )


def test_validator_accepts_valid_approval(approval):
    result = service.validate_marketflow_repository_integration_branch_retry_approval_v1(approval)
    assert result["status"] == service.MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_APPROVAL_VALID
    assert result["total_checks"] == len(service.REQUIRED_CHECK_IDS)


@pytest.mark.parametrize(
    ("field", "bad_value"),
    [
        ("artifact_kind", "wrong"),
        ("approval_status", "wrong"),
        ("approval_scope", "wrong"),
        ("selected_integration_branch_retry_package", "wrong"),
        ("source_integration_branch_retry_operator_review_digest", "0" * 64),
        ("source_integration_branch_retry_candidate_digest", "0" * 64),
        ("source_remediation_results_review_digest", "0" * 64),
        ("source_remediation_execution_digest", "0" * 64),
        ("source_staged_inventory_digest", "0" * 64),
        ("origin_main_commit_at_approval", "0" * 40),
        ("detached_integration_worktree_exists_at_approval", False),
        ("detached_integration_worktree_path", "missing"),
        ("staged_evidence_root_path", "missing"),
        ("first_integration_pytest_authoritative", False),
        ("first_integration_pytest_passed", True),
        ("later_wrong_worktree_rerun_diagnostic_only", False),
        ("later_wrong_worktree_rerun_overrides_first_failure", True),
        ("integration_branch_retry_approval_created", False),
        ("integration_branch_retry_selected", False),
        ("integration_branch_retry_approved", False),
        ("integration_branch_retry_authorized", False),
        ("ready_for_integration_branch_retry_execution", False),
        ("integration_branch_retry_executed", True),
        ("integration_branch_retry_results_review_created", True),
        ("integration_results_review_created", True),
        ("integration_execution_successful", True),
        ("successful_integration_execution_digest_generated", True),
        ("successful_integration_validation_digest_generated", True),
        ("integration_branch_pushed", True),
        ("remote_integration_branch_created", True),
        ("main_push_performed", True),
        ("origin_main_modified_by_this_task", True),
        ("marketflow_outputs_committed", True),
        ("evidence_regenerated", True),
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
        ("approved_future_retry_requirements", []),
        ("approved_future_retry_plan", []),
        ("supporting_packages", []),
        ("blocked_packages", []),
        ("next_chain", []),
        ("next_gates", []),
        ("risk_controls", []),
        ("no_tracked_marketflow_files", False),
    ],
)
def test_validator_rejects_invalid_approval_boundaries(approval, field, bad_value):
    changed = deepcopy(approval)
    changed[field] = bad_value
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryApprovalError):
        service.validate_marketflow_repository_integration_branch_retry_approval_v1(changed)


@pytest.mark.parametrize("field", tuple(service.ATTESTATION_STRING_FIELDS))
def test_service_rejects_incorrect_attestation_string_fields(attestation, field):
    changed = deepcopy(attestation)
    changed[field] = "wrong"
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryApprovalError):
        service.build_marketflow_repository_integration_branch_retry_approval_v1(
            operator_attestation=changed
        )


@pytest.mark.parametrize("field", service.ATTESTATION_TRUE_FIELDS)
def test_service_rejects_missing_closed_boundary_confirmations(attestation, field):
    changed = deepcopy(attestation)
    changed[field] = False
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryApprovalError):
        service.build_marketflow_repository_integration_branch_retry_approval_v1(
            operator_attestation=changed
        )


def test_service_rejects_changed_source_review_digest(attestation):
    review = deepcopy(service.DEFAULT_SOURCE_REVIEW)
    review["marketflow_repository_integration_branch_retry_candidate_operator_review_digest"] = "0" * 64
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryApprovalError):
        service.build_marketflow_repository_integration_branch_retry_approval_v1(
            source_review=review,
            operator_attestation=attestation,
        )


def test_validator_rejects_missing_digest(approval):
    changed = deepcopy(approval)
    changed.pop("marketflow_repository_integration_branch_retry_approval_digest")
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryApprovalError):
        service.validate_marketflow_repository_integration_branch_retry_approval_v1(changed)


@pytest.mark.parametrize(
    "section",
    [
        "MarketFlow Repository Integration Branch Retry Approval v1",
        "Operator Attestation",
        "Source Retry Candidate Operator Review",
        "Source Remediation Results Review",
        "Failure Context",
        "Remediation Context",
        "Approval Scope",
        "Selected Retry Package",
        "Approved Future Retry Requirements",
        "Approved Future Retry Plan",
        "Supporting Packages",
        "Blocked Packages",
        "Next Chain",
        "Next Gates",
        "Risk Controls",
        "Authority Boundaries",
        "Checklist Summary",
        "Guardrails",
    ],
)
def test_markdown_includes_required_sections(approval, section):
    markdown = service.build_marketflow_repository_integration_branch_retry_approval_markdown_v1(
        approval
    )
    assert section in markdown


def test_writer_round_trips_canonical_json(tmp_path, attestation):
    receipt = service.write_marketflow_repository_integration_branch_retry_approval_v1(
        tmp_path,
        operator_attestation=attestation,
    )
    payload = json.loads((tmp_path / "marketflow_repository_integration_branch_retry_approval_v1.json").read_text(encoding="utf-8"))
    assert payload["artifact_kind"] == service.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_APPROVED
    assert receipt["marketflow_repository_integration_branch_retry_approval_digest"] == payload["marketflow_repository_integration_branch_retry_approval_digest"]


def test_writer_refuses_overwrite(tmp_path, attestation):
    service.write_marketflow_repository_integration_branch_retry_approval_v1(
        tmp_path,
        operator_attestation=attestation,
    )
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryApprovalError):
        service.write_marketflow_repository_integration_branch_retry_approval_v1(
            tmp_path,
            operator_attestation=attestation,
        )
