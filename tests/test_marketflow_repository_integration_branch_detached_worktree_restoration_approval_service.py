from copy import deepcopy
import json

import pytest

from marketflow.services import (
    marketflow_repository_integration_branch_detached_worktree_restoration_approval_service as service,
)


def _attestation_kwargs():
    kwargs = {
        "operator_reference": "TEST_OPERATOR",
        "operator_attestation_timestamp_utc": "2026-08-29T00:00:00Z",
        "operator_attestation_phrase": service.REQUIRED_OPERATOR_ATTESTATION_PHRASE,
    }
    kwargs.update(
        {
            field: value
            for field, value in service.ATTESTATION_STRING_FIELDS.items()
            if field.startswith("operator_confirms_")
        }
    )
    kwargs.update({field: True for field in service.ATTESTATION_TRUE_FIELDS})
    return kwargs


@pytest.fixture
def attestation():
    return service.build_marketflow_repository_integration_branch_detached_worktree_restoration_approval_attestation_v1(
        **_attestation_kwargs()
    )


@pytest.fixture
def approval(attestation):
    return service.build_marketflow_repository_integration_branch_detached_worktree_restoration_approval_v1(
        operator_attestation=attestation
    )


def test_attestation_builder_creates_all_required_fields(attestation):
    assert attestation["operator_reference"] == "TEST_OPERATOR"
    assert attestation["operator_attestation_timestamp_utc"] == "2026-08-29T00:00:00Z"
    assert all(attestation[field] == expected for field, expected in service.ATTESTATION_STRING_FIELDS.items())
    assert all(attestation[field] is True for field in service.ATTESTATION_TRUE_FIELDS)


def test_approval_builds_offline_and_deterministically(approval, attestation):
    assert service.build_marketflow_repository_integration_branch_detached_worktree_restoration_approval_v1(operator_attestation=attestation) == approval
    assert approval["created_offline"] is True
    assert approval["governance_only"] is True
    assert approval["operator_attestation_required"] is True


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("artifact_kind", service.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_APPROVED),
        ("schema_version", service.SCHEMA_VERSION_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_APPROVAL_V1),
        ("approval_status", service.MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_APPROVED),
        ("approval_scope", service.REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_APPROVAL_ONLY_NOT_WORKTREE_CREATION_NOT_REMEDIATION_NOT_RETRY),
        ("selected_worktree_restoration_package", service.SELECTED_WORKTREE_RESTORATION_PACKAGE),
        ("source_worktree_restoration_operator_review_artifact_kind", service.source.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_CANDIDATE_OPERATOR_REVIEW_V1),
        ("source_worktree_restoration_operator_review_status", service.source.MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_CANDIDATE_OPERATOR_REVIEW_READY),
        ("source_worktree_restoration_operator_review_scope", service.source.REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_CANDIDATE_OPERATOR_REVIEW_ONLY_NOT_APPROVAL_NOT_WORKTREE_CREATION_NOT_REMEDIATION_NOT_RETRY),
        ("source_worktree_restoration_operator_review_digest", service.EXPECTED_SOURCE_OPERATOR_REVIEW_DIGEST),
        ("source_worktree_restoration_candidate_digest", service.EXPECTED_SOURCE_CANDIDATE_DIGEST),
        ("source_remediation_approval_digest", service.EXPECTED_SOURCE_REMEDIATION_APPROVAL_DIGEST),
        ("source_failure_diagnosis_digest", service.EXPECTED_SOURCE_DIAGNOSIS_DIGEST),
        ("blocked_remediation_execution_status", service.EXPECTED_BLOCKED_EXECUTION_STATUS),
        ("integration_branch_name", service.EXPECTED_INTEGRATION_BRANCH_NAME),
        ("integration_branch_head_commit", service.EXPECTED_INTEGRATION_HEAD_COMMIT),
        ("origin_main_commit", service.EXPECTED_ORIGIN_MAIN_COMMIT),
        ("source_evidence_root_exists", True),
        ("source_required_manifest_exists", True),
        ("source_evidence_file_count", 7),
        ("source_evidence_total_bytes", 2458181),
        ("marketflow_outputs_tracked", False),
        ("tracked_marketflow_file_count", 0),
        ("no_tracked_marketflow_files", True),
        ("worktree_restoration_selected", True),
        ("worktree_restoration_approved", True),
        ("worktree_restoration_authorized", True),
        ("worktree_restoration_approval_created", True),
        ("ready_for_worktree_restoration_execution", True),
        ("worktree_restoration_executed", False),
        ("detached_worktree_created", False),
        ("detached_worktree_restored", False),
        ("detached_worktree_deleted", False),
        ("integration_branch_deleted_or_reset", False),
        ("remediation_executed", False),
        ("evidence_staged", False),
        ("marketflow_outputs_copied", False),
        ("marketflow_outputs_committed", False),
        ("evidence_regenerated", False),
        ("integration_retry_candidate_created", False),
        ("integration_retry_executed", False),
        ("integration_results_review_created", False),
        ("integration_execution_successful", False),
        ("integration_branch_pushed", False),
        ("main_push_performed", False),
        ("origin_main_modified_by_this_task", False),
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
        ("strategy_use", "NOT_AUTHORIZED"),
        ("paper_trading", "NOT_AUTHORIZED"),
        ("broker_execution", "NOT_AUTHORIZED"),
        ("future_plan_approval_status", "APPROVED_FOR_FUTURE_WORKTREE_RESTORATION_EXECUTION_ONLY"),
        ("future_plan_execution_status", "NOT_EXECUTED"),
        ("remediation_execution_ready_now", False),
        ("recommended_next_task", service.RECOMMENDED_NEXT_TASK),
    ],
)
def test_required_approval_fields(approval, field, expected):
    assert approval[field] == expected


def test_selected_package_is_approved_for_future_execution_only(approval):
    assert approval["approved_selected_package"] == service.APPROVED_SELECTED_PACKAGE
    assert approval["approved_selected_package"]["selected"] is True
    assert approval["approved_selected_package"]["approved"] is True
    assert approval["approved_selected_package"]["authorized_for_future_execution"] is True
    assert approval["approved_selected_package"]["executed"] is False


def test_all_requirements_are_approved_for_future_execution(approval):
    rows = approval["approved_future_worktree_restoration_requirements"]
    assert rows == service.APPROVED_FUTURE_WORKTREE_RESTORATION_REQUIREMENTS
    assert len(rows) == 17
    assert all(row["approval_status"] == "APPROVED_FOR_FUTURE_WORKTREE_RESTORATION_EXECUTION_ONLY" for row in rows)


def test_future_plan_is_approved_but_not_executed(approval):
    rows = approval["approved_future_worktree_restoration_plan"]
    assert rows == service.APPROVED_FUTURE_WORKTREE_RESTORATION_PLAN
    assert len(rows) == 10
    assert all(row["approval_status"] == "APPROVED_FOR_FUTURE_WORKTREE_RESTORATION_EXECUTION_ONLY" for row in rows)
    assert all(row["execution_status"] == "NOT_EXECUTED" for row in rows)


def test_supporting_packages_remain_unselected(approval):
    assert approval["supporting_packages"] == service.SUPPORTING_PACKAGES
    assert len(approval["supporting_packages"]) == 2
    assert all(row["approval_status"] == "AVAILABLE_NOT_SELECTED" for row in approval["supporting_packages"])
    assert all(row["selected"] is False for row in approval["supporting_packages"])


def test_blocked_packages_remain_not_approved(approval):
    assert approval["blocked_packages"] == service.BLOCKED_PACKAGES
    assert len(approval["blocked_packages"]) == 3
    assert all(row["approval_status"] == "BLOCKED_NOT_APPROVED" for row in approval["blocked_packages"])
    assert all(row["approved"] is False for row in approval["blocked_packages"])


def test_next_chain_gates_and_risk_controls_are_exact(approval):
    assert approval["next_chain"] == service.NEXT_CHAIN
    assert approval["next_gates"] == service.NEXT_GATES
    assert approval["risk_controls"] == service.RISK_CONTROLS


def test_checklist_and_summary_pass(approval):
    assert [row["check_id"] for row in approval["checklist"]] == service.REQUIRED_CHECK_IDS
    assert all(row["status"] == "PASS" for row in approval["checklist"])
    assert all(set(row) == {"check_id", "status", "expected", "actual", "severity", "message"} for row in approval["checklist"])
    assert approval["summary"]["total_checks"] == len(service.REQUIRED_CHECK_IDS) == 54
    assert approval["summary"]["passed_checks"] == 54
    assert approval["summary"]["failed_checks"] == 0
    assert approval["summary"]["blocker_count"] == 0


def test_approval_digest_is_deterministic(approval):
    assert approval["marketflow_repository_integration_branch_detached_worktree_restoration_approval_digest"] == service.marketflow_repository_integration_branch_detached_worktree_restoration_approval_digest_v1(approval)


def test_validator_accepts_valid_approval(approval):
    result = service.validate_marketflow_repository_integration_branch_detached_worktree_restoration_approval_v1(approval)
    assert result["status"] == service.MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_APPROVED
    assert result["failed_checks"] == 0
    assert result["blocker_count"] == 0


@pytest.mark.parametrize(
    ("field", "bad_value"),
    [
        ("artifact_kind", "WRONG"),
        ("approval_status", "WRONG"),
        ("approval_scope", "WRONG"),
        ("selected_worktree_restoration_package", "WRONG"),
        ("source_worktree_restoration_operator_review_digest", "0" * 64),
        ("source_worktree_restoration_candidate_digest", "0" * 64),
        ("source_remediation_approval_digest", "0" * 64),
        ("source_failure_diagnosis_digest", "0" * 64),
        ("blocked_remediation_execution_status", ""),
        ("integration_branch_name", ""),
        ("integration_branch_head_commit", ""),
        ("origin_main_commit", ""),
        ("source_evidence_root_exists", False),
        ("source_required_manifest_exists", False),
        ("worktree_restoration_approval_created", False),
        ("worktree_restoration_selected", False),
        ("worktree_restoration_approved", False),
        ("worktree_restoration_authorized", False),
        ("ready_for_worktree_restoration_execution", False),
        ("worktree_restoration_executed", True),
        ("detached_worktree_created", True),
        ("detached_worktree_restored", True),
        ("detached_worktree_deleted", True),
        ("integration_branch_deleted_or_reset", True),
        ("remediation_executed", True),
        ("evidence_staged", True),
        ("marketflow_outputs_copied", True),
        ("marketflow_outputs_committed", True),
        ("integration_retry_candidate_created", True),
        ("integration_retry_executed", True),
        ("integration_results_review_created", True),
        ("integration_execution_successful", True),
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
def test_validator_rejects_invalid_boundaries(approval, field, bad_value):
    invalid = deepcopy(approval)
    invalid[field] = bad_value
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchDetachedWorktreeRestorationApprovalError):
        service.validate_marketflow_repository_integration_branch_detached_worktree_restoration_approval_v1(invalid)


@pytest.mark.parametrize(
    ("field", "bad_value"),
    [
        ("operator_decision", "WRONG"),
        ("operator_attestation_phrase", "WRONG"),
        ("operator_confirms_source_operator_review_digest", "0" * 64),
        ("operator_confirms_source_candidate_digest", "0" * 64),
        ("operator_confirms_source_remediation_approval_digest", "0" * 64),
        ("operator_confirms_source_diagnosis_digest", "0" * 64),
        ("operator_confirms_blocked_execution_status", "WRONG"),
        ("operator_confirms_integration_branch_name", "WRONG"),
        ("operator_confirms_integration_head_commit", "0" * 40),
        ("operator_confirms_origin_main_commit", "0" * 40),
        ("operator_confirms_selected_worktree_restoration_package", "WRONG"),
        ("operator_reference", ""),
        ("operator_attestation_timestamp_utc", ""),
    ],
)
def test_attestation_builder_rejects_wrong_string_confirmations(field, bad_value):
    kwargs = _attestation_kwargs()
    kwargs[field] = bad_value
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchDetachedWorktreeRestorationApprovalError):
        service.build_marketflow_repository_integration_branch_detached_worktree_restoration_approval_attestation_v1(
            **kwargs
        )


@pytest.mark.parametrize("field", service.ATTESTATION_TRUE_FIELDS)
def test_attestation_builder_rejects_missing_closed_boundary_confirmation(field):
    kwargs = _attestation_kwargs()
    kwargs[field] = False
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchDetachedWorktreeRestorationApprovalError):
        service.build_marketflow_repository_integration_branch_detached_worktree_restoration_approval_attestation_v1(
            **kwargs
        )


def test_validator_rejects_modified_attestation(approval):
    invalid = deepcopy(approval)
    invalid["operator_attestation"]["operator_confirms_no_worktree_creation"] = False
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchDetachedWorktreeRestorationApprovalError):
        service.validate_marketflow_repository_integration_branch_detached_worktree_restoration_approval_v1(invalid)


def test_builder_rejects_changed_source_review(attestation):
    review = service.source.build_marketflow_repository_integration_branch_detached_worktree_restoration_candidate_operator_review_v1()
    review["source_evidence_file_count"] = 8
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchDetachedWorktreeRestorationApprovalError):
        service.build_marketflow_repository_integration_branch_detached_worktree_restoration_approval_v1(
            source_review=review, operator_attestation=attestation
        )


def test_validator_rejects_missing_digest(approval):
    approval.pop("marketflow_repository_integration_branch_detached_worktree_restoration_approval_digest")
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchDetachedWorktreeRestorationApprovalError):
        service.validate_marketflow_repository_integration_branch_detached_worktree_restoration_approval_v1(approval)


def test_markdown_contains_required_sections(approval):
    markdown = service.build_marketflow_repository_integration_branch_detached_worktree_restoration_approval_markdown_v1(approval)
    for heading in (
        "# MarketFlow Repository Integration Branch Detached Worktree Restoration Approval v1",
        "## Operator Attestation", "## Source Operator Review",
        "## Blocked Remediation Execution Observation", "## Approval Scope",
        "## Selected Restoration Package", "## Approved Future Restoration Requirements",
        "## Approved Future Restoration Plan", "## Supporting Packages", "## Blocked Packages",
        "## Next Chain", "## Next Gates", "## Risk Controls", "## Authority Boundaries",
        "## Checklist Summary", "## Guardrails",
    ):
        assert heading in markdown


def test_writer_round_trips_and_refuses_overwrite(tmp_path, approval, attestation):
    receipt = service.write_marketflow_repository_integration_branch_detached_worktree_restoration_approval_v1(
        tmp_path, operator_attestation=attestation
    )
    payload = json.loads((tmp_path / "marketflow_repository_integration_branch_detached_worktree_restoration_approval_v1.json").read_text(encoding="utf-8"))
    assert payload == approval
    assert receipt["marketflow_repository_integration_branch_detached_worktree_restoration_approval_digest"] == approval["marketflow_repository_integration_branch_detached_worktree_restoration_approval_digest"]
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchDetachedWorktreeRestorationApprovalError):
        service.write_marketflow_repository_integration_branch_detached_worktree_restoration_approval_v1(
            tmp_path, operator_attestation=attestation
        )
