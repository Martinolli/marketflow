from copy import deepcopy
import json

import pytest

from marketflow import services
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_approval_service
    as service,
)


_DELETE = object()


def _attestation_kwargs() -> dict:
    values = {field: True for field in service.ATTESTATION_BOOLEAN_FIELDS}
    values.update(
        operator_reference="TEST_OPERATOR",
        operator_attestation_timestamp_utc="2026-09-01T00:00:00Z",
        operator_attestation_phrase=service.REQUIRED_OPERATOR_ATTESTATION_PHRASE,
        operator_confirms_source_operator_review_digest=service.SOURCE_OPERATOR_REVIEW_DIGEST,
        operator_confirms_source_candidate_digest=service.source.SOURCE_CANDIDATE_DIGEST,
        operator_confirms_source_blocked_execution_digest=service.source.source.SOURCE_BLOCKED_EXECUTION_DIGEST,
        operator_confirms_source_blocked_manifest_digest=service.source.source.SOURCE_BLOCKED_MANIFEST_DIGEST,
        operator_confirms_blocked_reason=service.source.source.source.BLOCKED_REASON_MODULE_DETAIL,
        operator_confirms_source_results_review_v2_digest=service.source.source.source.SOURCE_RESULTS_REVIEW_V2_DIGEST,
        operator_confirms_source_execution_v2_digest=service.source.source.source.results_source.SOURCE_EXECUTION_V2_DIGEST,
        operator_confirms_source_module_grouping_digest=service.source.source.source.results_source.SOURCE_MODULE_GROUPING_DIGEST,
        operator_confirms_retry_execution_commit="ab178b65c69f0274b0abbf9c20df102d35e78d34",
        operator_confirms_selected_source_recovery_package=service.SELECTED_MODULE_GROUPING_SOURCE_RECOVERY_PACKAGE,
    )
    return values


@pytest.fixture(scope="module")
def attestation() -> dict:
    return service.build_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_approval_attestation_v1(
        **_attestation_kwargs()
    )


@pytest.fixture(scope="module")
def approval(attestation) -> dict:
    return service.build_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_approval_v1(
        operator_attestation=attestation
    )


def test_attestation_builder_creates_required_non_secret_fields(attestation):
    assert attestation["operator_reference"] == "TEST_OPERATOR"
    assert attestation["operator_decision"] == service.OPERATOR_DECISION
    assert attestation["operator_attestation_phrase"] == service.REQUIRED_OPERATOR_ATTESTATION_PHRASE
    assert attestation["operator_attestation_version"] == service.OPERATOR_ATTESTATION_VERSION
    assert all(attestation[field] is True for field in service.ATTESTATION_BOOLEAN_FIELDS)


def test_approval_builds_offline_and_is_publicly_exported(approval, attestation):
    assert approval["created_offline"] is True
    assert approval["governance_only"] is True
    assert approval["operator_attestation_required"] is True
    assert services.build_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_approval_v1(operator_attestation=attestation) == approval


@pytest.mark.parametrize(
    "field,expected",
    [
        ("artifact_kind", service.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_APPROVED_V1),
        ("approval_status", service.MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_APPROVED),
        ("approval_scope", service.REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_APPROVAL_ONLY_NOT_EXECUTION_NOT_CACHE_READ_NOT_RETRY_NOT_MAIN),
        ("selected_module_grouping_source_recovery_package", service.SELECTED_MODULE_GROUPING_SOURCE_RECOVERY_PACKAGE),
        ("source_module_grouping_source_recovery_operator_review_digest", service.SOURCE_OPERATOR_REVIEW_DIGEST),
        ("source_module_grouping_source_recovery_candidate_digest", service.source.SOURCE_CANDIDATE_DIGEST),
        ("source_blocked_after_v2_execution_digest", service.source.source.SOURCE_BLOCKED_EXECUTION_DIGEST),
        ("source_blocked_after_v2_manifest_digest", service.source.source.SOURCE_BLOCKED_MANIFEST_DIGEST),
        ("blocked_reason", service.source.source.source.BLOCKED_REASON_MODULE_DETAIL),
        ("source_results_review_v2_digest", service.source.source.source.SOURCE_RESULTS_REVIEW_V2_DIGEST),
        ("source_execution_v2_digest", service.source.source.source.results_source.SOURCE_EXECUTION_V2_DIGEST),
        ("source_module_grouping_digest", service.source.source.source.results_source.SOURCE_MODULE_GROUPING_DIGEST),
        ("retry_execution_commit", "ab178b65c69f0274b0abbf9c20df102d35e78d34"),
        ("failed_or_errored_nodeids_count", 1404),
        ("module_summary_module_count", 29),
        ("largest_module_nodeid_counts", [136, 131, 122, 112, 111]),
        ("known_missing_detail", service.source.source.KNOWN_MISSING_DETAIL),
        ("unsupported_claims_boundary", service.source.source.UNSUPPORTED_CLAIMS_BOUNDARY),
        ("module_grouping_source_recovery_approval_created", True),
        ("module_grouping_source_recovery_selected", True),
        ("module_grouping_source_recovery_approved", True),
        ("module_grouping_source_recovery_authorized", True),
        ("ready_for_module_grouping_source_recovery_execution", True),
        ("module_grouping_source_recovery_executed", False),
        ("module_grouping_detail_recovered", False),
        ("module_grouping_detail_exposed", False),
        ("module_paths_recovered", False),
        ("per_module_counts_recovered", False),
        ("bounded_nodeid_samples_recovered", False),
        ("cache_read", False), ("cache_modified", False),
        ("predictive_usefulness", "not accepted"), ("profitability", "not accepted"),
        ("runtime_use", "NOT_AUTHORIZED"), ("broker_execution", "NOT_AUTHORIZED"),
    ],
)
def test_required_bindings_and_boundaries(approval, field, expected):
    assert approval[field] == expected


def test_retry_counts_and_classification_summary_are_bound(approval):
    assert [approval[f"retry_pytest_{name}_count"] for name in ("passed", "failed", "error", "skipped")] == [24877, 1292, 112, 7]
    assert approval["classification_evidence_summary"] == service.source.source._classification_summary()


def test_selected_package_is_future_only(approval):
    package = approval["selected_package"]
    assert package == {
        "package_id": service.SELECTED_MODULE_GROUPING_SOURCE_RECOVERY_PACKAGE,
        "approval_status": service.APPROVED_ONLY,
        "selected": True, "approved": True, "authorized_for_future_execution": True,
        "executed": False,
    }


def test_requirements_plan_outputs_and_alternative_packages(approval):
    assert len(approval["approved_future_requirements"]) == 26
    assert all(item["requirement_value"] is True and item["approval_status"] == service.APPROVED_ONLY for item in approval["approved_future_requirements"])
    assert len(approval["approved_future_plan"]) == 10
    assert all(item["approval_status"] == service.APPROVED_ONLY and item["execution_status"] == "NOT_EXECUTED" for item in approval["approved_future_plan"])
    assert len(approval["authorized_planned_outputs"]) == 10
    assert all(item["authorization_status"] == "AUTHORIZED_NOT_GENERATED" for item in approval["authorized_planned_outputs"])
    assert len(approval["supporting_packages"]) == 4
    assert all(not item["selected"] and not item["approved"] for item in approval["supporting_packages"])
    assert len(approval["blocked_packages"]) == 5
    assert all(item["approval_status"].startswith("BLOCKED_NOT_APPROVED") and not item["approved"] for item in approval["blocked_packages"])


def test_all_execution_and_external_authority_fields_remain_closed(approval):
    false_fields = [
        "module_grouping_source_recovery_executed", "module_grouping_detail_recovered",
        "module_grouping_detail_exposed", "module_paths_recovered", "per_module_counts_recovered",
        "bounded_nodeid_samples_recovered", "cache_read", "cache_modified", "retry_rerun_performed",
        "full_pytest_performed", "diagnostic_command_executed", "diagnostic_execution_performed",
        "remediation_execution_performed", "classification_execution_performed",
        "remediation_or_method_after_v2_reentry_created", "new_retry_candidate_created", "new_retry_executed",
        "new_retry_results_review_created", "main_merge_approval_created", "integration_execution_successful",
        "successful_integration_execution_digest_generated", "successful_integration_validation_digest_generated",
        "integration_branch_pushed", "main_push_performed", "origin_main_modified_by_this_task",
        "marketflow_outputs_committed", "pytest_cache_committed", "evidence_regenerated",
        "provider_requests_made_in_approval", "market_data_acquisition_performed_in_approval",
        "dataset_generation_performed_in_approval", "metric_recomputation_from_raw_rows_performed",
        "model_training_performed", "strategy_scoring_performed", "trade_recommendations_generated",
    ]
    assert all(approval[field] is False for field in false_fields)
    assert approval["strategy_use"] == approval["paper_trading"] == approval["broker_execution"] == "NOT_AUTHORIZED"


def test_chain_gates_controls_and_checklist_pass(approval):
    assert approval["next_chain"] == service.NEXT_CHAIN and len(approval["next_chain"]) == 11
    assert approval["next_gates"] == service.NEXT_GATES and len(approval["next_gates"]) == 13
    assert approval["risk_controls"] == service.RISK_CONTROLS and len(approval["risk_controls"]) == 59
    assert approval["summary"]["passed_checks"] == approval["summary"]["total_checks"] == 71
    assert approval["summary"]["failed_checks"] == approval["summary"]["blocker_count"] == 0
    assert all(item["status"] == "PASS" for item in approval["checklist"])


def test_approval_digest_is_deterministic_and_accepts_exact_source_review(approval, attestation):
    source_review = service.source.build_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_candidate_operator_review_v1()
    rebuilt = service.build_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_approval_v1(source_review=source_review, operator_attestation=attestation)
    assert rebuilt == approval
    assert approval["marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_approval_digest"] == "3b2e00be71e6aa209520bba347397bc12134566adfd30ff29e432ba0c7ce4b76"


def test_validator_accepts_and_writer_round_trips(approval, attestation, tmp_path):
    result = service.validate_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_approval_v1(approval)
    assert result["failed_checks"] == 0
    written = service.write_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_approval_v1(tmp_path, operator_attestation=attestation)
    payload = json.loads((tmp_path / "marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_approval_v1.json").read_text(encoding="utf-8"))
    assert written["approval_status"] == approval["approval_status"]
    assert payload == approval


@pytest.mark.parametrize(
    "field,value",
    [
        ("artifact_kind", "WRONG"), ("approval_status", "WRONG"), ("approval_scope", "WRONG"),
        ("selected_module_grouping_source_recovery_package", "WRONG"),
        ("source_module_grouping_source_recovery_operator_review_digest", "0" * 64),
        ("source_module_grouping_source_recovery_candidate_digest", "0" * 64),
        ("source_blocked_after_v2_execution_digest", "0" * 64),
        ("source_blocked_after_v2_manifest_digest", "0" * 64), ("blocked_reason", _DELETE),
        ("source_results_review_v2_digest", "0" * 64), ("source_execution_v2_digest", "0" * 64),
        ("source_module_grouping_digest", "0" * 64), ("retry_pytest_failed_count", _DELETE),
        ("classification_evidence_summary", _DELETE), ("module_summary_module_count", 28),
        ("largest_module_nodeid_counts", [136]), ("known_missing_detail", _DELETE),
        ("unsupported_claims_boundary", _DELETE), ("module_grouping_source_recovery_approval_created", False),
        ("module_grouping_source_recovery_selected", False), ("module_grouping_source_recovery_approved", False),
        ("module_grouping_source_recovery_authorized", False), ("ready_for_module_grouping_source_recovery_execution", False),
        ("module_grouping_source_recovery_executed", True), ("module_grouping_detail_recovered", True),
        ("module_grouping_detail_exposed", True), ("module_paths_recovered", True), ("per_module_counts_recovered", True),
        ("bounded_nodeid_samples_recovered", True), ("cache_read", True), ("cache_modified", True),
        ("retry_rerun_performed", True), ("full_pytest_performed", True), ("diagnostic_command_executed", True),
        ("diagnostic_execution_performed", True), ("remediation_execution_performed", True),
        ("classification_execution_performed", True), ("new_retry_candidate_created", True),
        ("new_retry_executed", True), ("new_retry_results_review_created", True),
        ("main_merge_approval_created", True), ("integration_execution_successful", True),
        ("successful_integration_execution_digest_generated", True), ("integration_branch_pushed", True),
        ("main_push_performed", True), ("origin_main_modified_by_this_task", True),
        ("marketflow_outputs_committed", True), ("pytest_cache_committed", True),
        ("evidence_regenerated", True), ("provider_requests_made_in_approval", True),
        ("market_data_acquisition_performed_in_approval", True), ("dataset_generation_performed_in_approval", True),
        ("metric_recomputation_from_raw_rows_performed", True), ("model_training_performed", True),
        ("strategy_scoring_performed", True), ("trade_recommendations_generated", True),
        ("predictive_usefulness", "accepted"), ("profitability", "accepted"),
        ("runtime_use", "AUTHORIZED"), ("broker_execution", "AUTHORIZED"), ("risk_controls", []),
    ],
)
def test_validator_rejects_binding_or_boundary_changes(approval, field, value):
    changed = deepcopy(approval)
    if value is _DELETE:
        changed.pop(field)
    else:
        changed[field] = value
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureModuleGroupingSourceRecoveryApprovalError):
        service.validate_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_approval_v1(changed)


@pytest.mark.parametrize(
    "field,value",
    [
        ("operator_decision", "WRONG"),
        ("operator_attestation_phrase", "WRONG"),
        ("operator_confirms_no_cache_read", False),
        ("operator_confirms_source_operator_review_digest", "0" * 64),
    ],
)
def test_attestation_rejects_wrong_or_missing_confirmation(field, value):
    kwargs = _attestation_kwargs()
    kwargs[field] = value
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureModuleGroupingSourceRecoveryApprovalError):
        service.build_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_approval_attestation_v1(**kwargs)


def test_markdown_contains_required_sections(approval):
    markdown = service.build_marketflow_repository_integration_branch_retry_failure_module_grouping_source_recovery_approval_markdown_v1(approval)
    sections = [
        "Operator Attestation", "Source Operator Review", "Source Module Grouping Source Recovery Candidate",
        "Source Blocked After-v2 Execution", "Source Classification Results Review v2", "Retry Failure Context",
        "Known Available and Missing Detail", "Approval Scope", "Selected Source Recovery Package",
        "Approved Future Source Recovery Requirements", "Approved Future Source Recovery Plan", "Planned Outputs",
        "Supporting Packages", "Blocked Packages", "Next Chain", "Next Gates", "Risk Controls",
        "Authority Boundaries", "Checklist Summary", "Guardrails",
    ]
    assert all(f"## {section}" in markdown for section in sections)
