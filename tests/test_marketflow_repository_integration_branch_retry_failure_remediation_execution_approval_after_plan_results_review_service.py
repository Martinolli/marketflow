from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import pytest

from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_remediation_execution_approval_after_plan_results_review_service
    as target,
)


def confirmations() -> dict:
    values = deepcopy(target.SOURCE_ATTESTATION_FIELDS)
    values.update({field: True for field in target.ATTESTATION_BOOLEAN_FIELDS})
    return values


def valid_attestation() -> dict:
    return target.build_marketflow_repository_integration_branch_retry_failure_remediation_execution_approval_after_plan_results_review_attestation_v1(
        operator_reference="TEST_OPERATOR",
        operator_attestation_timestamp_utc="2026-08-23T00:00:00Z",
        operator_attestation_phrase=target.REQUIRED_REMEDIATION_EXECUTION_APPROVAL_AFTER_PLAN_RESULTS_REVIEW_ATTESTATION_PHRASE_V1,
        operator_confirmations=confirmations(),
    )


def valid_approval() -> dict:
    return target.build_marketflow_repository_integration_branch_retry_failure_remediation_execution_approval_after_plan_results_review_v1(
        operator_attestation=valid_attestation()
    )


def assert_rejected(approval: dict) -> None:
    with pytest.raises(
        target.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionApprovalAfterPlanResultsReviewError
    ):
        target.validate_marketflow_repository_integration_branch_retry_failure_remediation_execution_approval_after_plan_results_review_v1(
            approval
        )


def test_attestation_builder_creates_required_fields() -> None:
    attestation = valid_attestation()
    assert attestation["operator_decision"] == target.OPERATOR_DECISION
    assert attestation["selected_remediation_execution_package"] == target.SELECTED_PACKAGE
    assert attestation["operator_attestation_phrase"] == target.REQUIRED_REMEDIATION_EXECUTION_APPROVAL_AFTER_PLAN_RESULTS_REVIEW_ATTESTATION_PHRASE_V1
    assert attestation["operator_attestation_timestamp_utc"] == "2026-08-23T00:00:00Z"
    assert attestation["operator_attestation_version"] == target.OPERATOR_ATTESTATION_VERSION
    assert attestation["operator_reference"] == "TEST_OPERATOR"
    assert all(attestation[field] == value for field, value in target.SOURCE_ATTESTATION_FIELDS.items())
    assert all(attestation[field] is True for field in target.ATTESTATION_BOOLEAN_FIELDS)


def test_approval_builds_offline_without_source_builders_or_file_reads(monkeypatch: pytest.MonkeyPatch) -> None:
    def forbidden(*args, **kwargs):
        raise AssertionError("approval must not build sources or read evidence")

    monkeypatch.setattr(
        target.source,
        "build_marketflow_repository_integration_branch_retry_failure_remediation_execution_candidate_after_plan_results_review_operator_review_v1",
        forbidden,
    )
    monkeypatch.setattr(Path, "read_text", forbidden)
    monkeypatch.setattr(Path, "read_bytes", forbidden)
    approval = valid_approval()
    assert approval["created_offline"] is True
    assert approval["governance_only"] is True
    assert approval["approval_only"] is True


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("artifact_kind", target.ARTIFACT_KIND),
        ("schema_version", target.SCHEMA_VERSION),
        ("approval_status", target.APPROVAL_STATUS),
        ("approval_scope", target.APPROVAL_SCOPE),
        ("selected_remediation_execution_package", target.SELECTED_PACKAGE),
        ("source_operator_review_artifact_kind", target.source.ARTIFACT_KIND),
        ("source_operator_review_status", target.source.REVIEW_STATUS),
        ("source_operator_review_scope", target.source.REVIEW_SCOPE),
        ("source_operator_review_commit", target.SOURCE_OPERATOR_REVIEW_COMMIT),
        ("source_remediation_execution_candidate_after_plan_results_review_operator_review_digest", target.SOURCE_OPERATOR_REVIEW_DIGEST),
        ("source_candidate_commit", target.source.SOURCE_CANDIDATE_COMMIT),
        ("source_remediation_execution_candidate_after_plan_results_review_digest", target.source.SOURCE_CANDIDATE_DIGEST),
        ("selected_source_plan_package", target.source.source.SELECTED_SOURCE_PLAN_PACKAGE),
    ],
)
def test_identity_selection_and_source_fields(field: str, expected: object) -> None:
    assert valid_approval()[field] == expected


@pytest.mark.parametrize("field", list(target._source_fields()))
def test_all_source_evidence_bindings_are_exact(field: str) -> None:
    assert valid_approval()[field] == target._source_fields()[field]


def test_retry_priority_and_diagnostic_facts_are_bound() -> None:
    approval = valid_approval()
    assert approval["retry_failure_context"] == {
        "counts": {"passed": 24877, "failed": 1292, "errors": 112, "skipped": 7},
        "first_result_authoritative": True,
        "pytest_passed": False,
        "pytest_failed": True,
        "root_full_regression_is_retry_evidence": False,
    }
    assert [item["failed_or_errored_nodeid_count"] for item in approval["priority_1_target_modules"]] == [136, 131, 122, 112, 111]
    assert (approval["priority_1_total_nodeids"], approval["top_10_count_sum"]) == (612, 1069)
    assert (approval["module_summary_module_count"], approval["failed_or_errored_nodeids_count"]) == (29, 1404)
    assert (approval["source_exit_code"], approval["source_exit_code_is_diagnostic_only"]) == (1, True)
    assert (approval["source_stdout_byte_count"], approval["source_stderr_byte_count"]) == (1231380, 0)
    assert approval["source_stdout_sha256"] == "b5fb29f6cf8af77700da74c72f08b854c33bc1ad30c79c309c6eefee70171d2a"
    assert approval["source_stderr_sha256"] == "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    assert approval["source_stdout_excerpt_truncated"] is True
    assert approval["source_stderr_excerpt_truncated"] is False
    assert approval["source_redaction_checked"] is True


def test_four_families_and_four_workstreams_are_bound_without_readiness() -> None:
    approval = valid_approval()
    families = approval["reviewed_observable_failure_families"]
    assert [item["family_id"] for item in families] == target.source.source.source.FAMILY_IDS
    assert approval["observable_failure_family_count"] == len(families) == 4
    assert approval["total_observable_evidence_items"] == 188
    assert all(item["observable_evidence_count"] == 47 and item["confidence"] == "HIGH" for item in families)
    assert approval["source_workstream_count"] == len(approval["reviewed_workstreams"]) == 4
    assert [item["source_family_id"] for item in approval["reviewed_workstreams"]] == target.source.source.source.FAMILY_IDS
    assert approval["additional_diagnostic_capture_may_be_needed"] is False
    assert approval["direct_remediation_ready"] is False
    assert approval["remediation_execution_ready"] is False
    assert approval["retry_ready"] is False
    assert approval["main_merge_ready"] is False


def test_selected_package_is_approved_for_future_execution_only() -> None:
    approval = valid_approval()
    package = approval["approved_package"]
    assert package["package_id"] == target.SELECTED_PACKAGE
    assert package["approval_status"] == target.APPROVED_ONLY
    assert package["selected"] is package["approved"] is package["authorized_for_future_execution"] is True
    assert package["executed"] is False
    assert approval["remediation_execution_package_selected"] is True
    assert approval["remediation_execution_package_approved"] is True
    assert approval["remediation_execution_package_authorized"] is True
    assert approval["ready_for_remediation_execution_after_plan_results_review"] is True


def test_future_requirements_plan_boundary_and_packages_are_exact() -> None:
    approval = valid_approval()
    assert approval["approved_future_remediation_execution_requirements"] == target.APPROVED_FUTURE_REMEDIATION_EXECUTION_REQUIREMENTS
    assert len(approval["approved_future_remediation_execution_requirements"]) == 46
    assert approval["approved_future_remediation_execution_plan"] == target.APPROVED_FUTURE_REMEDIATION_EXECUTION_PLAN
    assert len(approval["approved_future_remediation_execution_plan"]) == 14
    assert all(item["execution_status"] == "NOT_EXECUTED" for item in approval["approved_future_remediation_execution_requirements"] + approval["approved_future_remediation_execution_plan"])
    assert approval["future_remediation_execution_status"] == "APPROVED_FOR_FUTURE_EXECUTION_ONLY_NOT_EXECUTED"
    assert approval["future_remediation_execution_type"] == "CONTROLLED_PLAN_DERIVED_REMEDIATION_WITH_VERIFICATION"
    assert approval["future_remediation_execution_executed"] is False
    assert len(approval["authorized_planned_outputs"]) == 21
    assert all(item["authorization_status"] == "AUTHORIZED_NOT_GENERATED" for item in approval["authorized_planned_outputs"])
    assert approval["supporting_packages"] == target.SUPPORTING_PACKAGES and len(approval["supporting_packages"]) == 6
    assert approval["blocked_packages"] == target.BLOCKED_PACKAGES and len(approval["blocked_packages"]) == 5
    assert all(item["selected"] is item["approved"] is False for item in approval["supporting_packages"] + approval["blocked_packages"])


@pytest.mark.parametrize("field", target.TRUE_FIELDS)
def test_approved_fact_true(field: str) -> None:
    assert valid_approval()[field] is True


@pytest.mark.parametrize("field", target.FALSE_FIELDS)
def test_closed_current_authority_false(field: str) -> None:
    assert valid_approval()[field] is False


def test_future_boundary_allows_only_separately_governed_controlled_work() -> None:
    approval = valid_approval()
    for field in (
        "future_execution_may_create_file_impact_inventory", "future_execution_may_create_pre_change_snapshot",
        "future_execution_may_perform_controlled_plan_derived_changes",
        "future_execution_may_record_post_change_snapshot_if_changes_occur",
        "future_execution_may_record_verification_evidence",
        "future_execution_may_run_focused_validation_if_required_by_future_execution_contract",
    ):
        assert approval[field] is True
    for field in (
        "future_execution_may_run_full_pytest", "future_execution_may_run_retry", "future_execution_may_push_main",
        "future_execution_may_push_integration_branch", "future_execution_may_create_retry_candidate",
        "future_execution_may_claim_root_cause", "future_execution_may_claim_retry_success",
        "future_execution_may_create_main_merge_approval",
    ):
        assert approval[field] is False


def test_predictive_profitability_runtime_and_trading_stay_closed() -> None:
    approval = valid_approval()
    assert approval["predictive_usefulness"] == approval["profitability"] == "not accepted"
    assert approval["runtime_use"] == approval["strategy_use"] == "NOT_AUTHORIZED"
    assert approval["paper_trading"] == approval["broker_execution"] == "NOT_AUTHORIZED"


def test_chain_gates_controls_checklist_and_summary_are_complete() -> None:
    approval = valid_approval()
    assert approval["next_chain"] == target.NEXT_CHAIN and len(approval["next_chain"]) == 7
    assert approval["next_gates"] == target.NEXT_GATES and len(approval["next_gates"]) == 7
    assert approval["risk_controls"] == target.RISK_CONTROLS and len(approval["risk_controls"]) == 107
    assert set(target.REQUIRED_CHECK_IDS) <= {item["check_id"] for item in approval["checklist"]}
    assert all(item["status"] == "PASS" and item["severity"] == "BLOCKER" for item in approval["checklist"])
    assert approval["summary"]["total_checks"] == approval["summary"]["passed_checks"] == len(approval["checklist"])
    assert approval["summary"]["failed_checks"] == approval["summary"]["blocker_count"] == 0
    assert approval["summary"]["recommended_next_task"] == target.RECOMMENDED_NEXT_TASK


def test_approval_digest_is_deterministic() -> None:
    assert valid_approval()[target.APPROVAL_DIGEST_KEY] == valid_approval()[target.APPROVAL_DIGEST_KEY]


def test_validator_accepts_valid_approval() -> None:
    approval = valid_approval()
    result = target.validate_marketflow_repository_integration_branch_retry_failure_remediation_execution_approval_after_plan_results_review_v1(approval)
    assert result["approval_digest"] == approval[target.APPROVAL_DIGEST_KEY]
    assert result["failed_checks"] == result["blocker_count"] == 0


@pytest.mark.parametrize("field", list(target._approval_body(valid_attestation())))
def test_validator_rejects_changed_or_missing_required_body_field(field: str) -> None:
    approval = valid_approval()
    approval[field] = "changed"
    assert_rejected(approval)
    approval = valid_approval()
    approval.pop(field)
    assert_rejected(approval)


@pytest.mark.parametrize("field", target.SOURCE_ATTESTATION_FIELDS)
def test_attestation_rejects_changed_digest_or_exact_confirmation(field: str) -> None:
    values = confirmations()
    values[field] = "changed"
    with pytest.raises(target.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionApprovalAfterPlanResultsReviewError):
        target.build_marketflow_repository_integration_branch_retry_failure_remediation_execution_approval_after_plan_results_review_attestation_v1(
            operator_reference="TEST_OPERATOR", operator_attestation_timestamp_utc="2026-08-23T00:00:00Z",
            operator_attestation_phrase=target.REQUIRED_REMEDIATION_EXECUTION_APPROVAL_AFTER_PLAN_RESULTS_REVIEW_ATTESTATION_PHRASE_V1,
            operator_confirmations=values,
        )


@pytest.mark.parametrize("field", target.ATTESTATION_BOOLEAN_FIELDS)
def test_attestation_rejects_missing_or_false_boundary_confirmation(field: str) -> None:
    values = confirmations()
    values[field] = False
    with pytest.raises(target.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionApprovalAfterPlanResultsReviewError):
        target.build_marketflow_repository_integration_branch_retry_failure_remediation_execution_approval_after_plan_results_review_attestation_v1(
            operator_reference="TEST_OPERATOR", operator_attestation_timestamp_utc="2026-08-23T00:00:00Z",
            operator_attestation_phrase=target.REQUIRED_REMEDIATION_EXECUTION_APPROVAL_AFTER_PLAN_RESULTS_REVIEW_ATTESTATION_PHRASE_V1,
            operator_confirmations=values,
        )
    values = confirmations()
    values.pop(field)
    with pytest.raises(target.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionApprovalAfterPlanResultsReviewError):
        target.build_marketflow_repository_integration_branch_retry_failure_remediation_execution_approval_after_plan_results_review_attestation_v1(
            operator_reference="TEST_OPERATOR", operator_attestation_timestamp_utc="2026-08-23T00:00:00Z",
            operator_attestation_phrase=target.REQUIRED_REMEDIATION_EXECUTION_APPROVAL_AFTER_PLAN_RESULTS_REVIEW_ATTESTATION_PHRASE_V1,
            operator_confirmations=values,
        )


@pytest.mark.parametrize(
    ("keyword", "value"),
    [
        ("operator_attestation_phrase", "wrong"),
        ("selected_remediation_execution_package", "wrong"),
        ("operator_decision", "wrong"),
        ("operator_reference", ""),
        ("operator_attestation_timestamp_utc", "2026-08-23"),
    ],
)
def test_attestation_rejects_wrong_identity_field(keyword: str, value: str) -> None:
    kwargs = {
        "operator_reference": "TEST_OPERATOR",
        "operator_attestation_timestamp_utc": "2026-08-23T00:00:00Z",
        "operator_attestation_phrase": target.REQUIRED_REMEDIATION_EXECUTION_APPROVAL_AFTER_PLAN_RESULTS_REVIEW_ATTESTATION_PHRASE_V1,
        "selected_remediation_execution_package": target.SELECTED_PACKAGE,
        "operator_decision": target.OPERATOR_DECISION,
        "operator_confirmations": confirmations(),
    }
    kwargs[keyword] = value
    with pytest.raises(target.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionApprovalAfterPlanResultsReviewError):
        target.build_marketflow_repository_integration_branch_retry_failure_remediation_execution_approval_after_plan_results_review_attestation_v1(**kwargs)


def test_attestation_rejects_unexpected_secret_or_personal_field() -> None:
    values = confirmations()
    values["api_key"] = "must-not-be-stored"
    with pytest.raises(target.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionApprovalAfterPlanResultsReviewError):
        target.build_marketflow_repository_integration_branch_retry_failure_remediation_execution_approval_after_plan_results_review_attestation_v1(
            operator_reference="TEST_OPERATOR", operator_attestation_timestamp_utc="2026-08-23T00:00:00Z",
            operator_attestation_phrase=target.REQUIRED_REMEDIATION_EXECUTION_APPROVAL_AFTER_PLAN_RESULTS_REVIEW_ATTESTATION_PHRASE_V1,
            operator_confirmations=values,
        )


@pytest.mark.parametrize("field", target.TRUE_FIELDS)
def test_validator_rejects_approved_fact_set_false(field: str) -> None:
    approval = valid_approval()
    approval[field] = False
    assert_rejected(approval)


@pytest.mark.parametrize("field", target.FALSE_FIELDS)
def test_validator_rejects_opened_current_boundary(field: str) -> None:
    approval = valid_approval()
    approval[field] = True
    assert_rejected(approval)


@pytest.mark.parametrize(
    ("field", "value"),
    [("predictive_usefulness", "accepted"), ("profitability", "accepted"), ("runtime_use", "AUTHORIZED"), ("broker_execution", "AUTHORIZED")],
)
def test_validator_rejects_opened_string_authority(field: str, value: str) -> None:
    approval = valid_approval()
    approval[field] = value
    assert_rejected(approval)


def test_validator_rejects_missing_family_workstream_counts_or_package_inventory() -> None:
    mutations = [
        lambda item: item["retry_failure_context"].update(counts={}),
        lambda item: item.update(priority_1_target_modules=[]),
        lambda item: item["reviewed_observable_failure_families"].pop(),
        lambda item: item["reviewed_workstreams"].pop(),
        lambda item: item.update(approved_future_remediation_execution_requirements=[]),
        lambda item: item.update(approved_future_remediation_execution_plan=[]),
        lambda item: item.update(authorized_planned_outputs=[]),
        lambda item: item.update(supporting_packages=[]),
        lambda item: item.update(blocked_packages=[]),
    ]
    for mutate in mutations:
        approval = valid_approval()
        mutate(approval)
        assert_rejected(approval)


def test_validator_rejects_missing_or_changed_approval_digest() -> None:
    approval = valid_approval()
    approval.pop(target.APPROVAL_DIGEST_KEY)
    assert_rejected(approval)
    approval = valid_approval()
    approval[target.APPROVAL_DIGEST_KEY] = "changed"
    assert_rejected(approval)


def test_invalid_supplied_source_operator_review_is_rejected() -> None:
    with pytest.raises(target.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionApprovalAfterPlanResultsReviewError):
        target.build_marketflow_repository_integration_branch_retry_failure_remediation_execution_approval_after_plan_results_review_v1(
            source_operator_review={}, operator_attestation=valid_attestation()
        )


def test_writer_writes_only_status_markdown_and_refuses_overwrite(tmp_path: Path) -> None:
    approval = target.write_marketflow_repository_integration_branch_retry_failure_remediation_execution_approval_after_plan_results_review_v1(
        tmp_path, operator_attestation=valid_attestation()
    )
    assert approval["artifact_kind"] == target.ARTIFACT_KIND
    assert [path.name for path in tmp_path.iterdir()] == [
        "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_APPROVAL_AFTER_PLAN_RESULTS_REVIEW_STATUS.md"
    ]
    with pytest.raises(target.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionApprovalAfterPlanResultsReviewError):
        target.write_marketflow_repository_integration_branch_retry_failure_remediation_execution_approval_after_plan_results_review_v1(
            tmp_path, operator_attestation=valid_attestation()
        )


@pytest.mark.parametrize("path", [Path(".marketflow"), Path(".pytest_cache"), Path(".env")])
def test_writer_refuses_protected_output(path: Path) -> None:
    with pytest.raises(target.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionApprovalAfterPlanResultsReviewError):
        target.write_marketflow_repository_integration_branch_retry_failure_remediation_execution_approval_after_plan_results_review_v1(
            path, operator_attestation=valid_attestation()
        )


def test_markdown_contains_required_sections() -> None:
    markdown = target.build_marketflow_repository_integration_branch_retry_failure_remediation_execution_approval_after_plan_results_review_markdown_v1(valid_approval())
    required = [
        "# MarketFlow Repository Integration Branch Retry Failure Remediation Execution Approval After Plan Results Review v1",
        "## Operator Attestation", "## Source Operator Review", "## Source Candidate",
        "## Source Plan Results Review", "## Source Plan Execution", "## Source Targeted Remediation Plan",
        "## Source Workstream Mapping", "## Source Approval", "## Source Method Results Review",
        "## Source Method Execution", "## Source Failure-Family Classification",
        "## Source Diagnostic Results Review", "## Source Controlled Recapture Execution", "## Source Durable Receipt",
        "## Source Receipt Loss History", "## Source Planning and Detail Binding Evidence", "## Retry Failure Context",
        "## Approval Scope", "## Selected Remediation Execution Package", "## Priority 1 Target Modules",
        "## Diagnostic Capture Evidence Summary", "## Reviewed Observable Failure Families", "## Reviewed Workstreams",
        "## Approved Future Remediation Execution Requirements", "## Approved Future Remediation Execution Plan",
        "## Future Remediation Execution Boundary", "## Planned Outputs", "## Supporting Packages",
        "## Blocked Packages", "## Next Chain", "## Next Gates", "## Risk Controls",
        "## Authority Boundaries", "## Checklist Summary", "## Guardrails",
    ]
    assert all(section in markdown for section in required)
