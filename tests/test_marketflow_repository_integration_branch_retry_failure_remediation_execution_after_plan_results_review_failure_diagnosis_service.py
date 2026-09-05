from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import pytest

from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_remediation_execution_after_plan_results_review_failure_diagnosis_service
    as service,
)


@pytest.fixture()
def diagnosis():
    return service.build_marketflow_repository_integration_branch_retry_failure_remediation_execution_after_plan_results_review_failure_diagnosis_v1()


def test_diagnosis_builds_offline_with_fixed_identity(diagnosis):
    assert diagnosis["artifact_kind"] == service.ARTIFACT_KIND
    assert diagnosis["schema_version"] == service.SCHEMA_VERSION
    assert diagnosis["diagnosis_status"] == service.DIAGNOSIS_STATUS
    assert diagnosis["diagnosis_scope"] == service.DIAGNOSIS_SCOPE
    assert diagnosis["created_offline"] is diagnosis["governance_only"] is diagnosis["diagnosis_only"] is True


def test_source_blocked_execution_is_bound(diagnosis):
    assert diagnosis["source_blocked_execution_commit"] == service.SOURCE_BLOCKED_EXECUTION_COMMIT
    assert diagnosis["source_blocked_execution_artifact_kind"] == service.source.BLOCKED_ARTIFACT_KIND
    assert diagnosis["source_blocked_execution_status"] == service.source.BLOCKED_STATUS
    assert diagnosis["source_blocked_execution_scope"] == service.source.EXECUTION_SCOPE
    assert diagnosis["source_blocked_reason"] == service.SOURCE_BLOCKED_REASON
    assert diagnosis["source_blocked_manifest_digest"] == service.SOURCE_BLOCKED_MANIFEST_DIGEST


def test_approval_package_operator_review_and_candidate_are_bound(diagnosis):
    assert diagnosis["source_remediation_execution_approval_after_plan_results_review_commit"] == service.source.SOURCE_APPROVAL_COMMIT
    assert diagnosis["source_remediation_execution_approval_after_plan_results_review_digest"] == service.source.SOURCE_APPROVAL_DIGEST
    assert diagnosis["selected_remediation_execution_package"] == service.SELECTED_PACKAGE
    assert diagnosis["source_remediation_execution_candidate_after_plan_results_review_operator_review_commit"] == "999fab934370d16b24c5ed84876f06254fbacb9b"
    assert diagnosis["source_remediation_execution_candidate_after_plan_results_review_operator_review_digest"] == "8f7033f203707634413ba460ae5fcbf829bda5822eb379677515e02d6333a3b4"
    assert diagnosis["source_remediation_execution_candidate_after_plan_results_review_commit"] == "c12583bc41e7de16c371f36f4408a468108a8bc7"
    assert diagnosis["source_remediation_execution_candidate_after_plan_results_review_digest"] == "6869b7642d8f90fd0273a7cbfdd069af85b23518778100ae19f3ebb6060fe4bd"


def test_plan_method_diagnostic_and_recovery_bindings(diagnosis):
    for field in (
        "source_remediation_plan_or_execution_results_review_after_method_results_review_digest",
        "source_targeted_remediation_plan_review_digest", "source_workstream_mapping_review_digest",
        "source_remediation_plan_or_execution_after_method_results_review_digest",
        "source_targeted_remediation_plan_digest", "source_workstream_mapping_digest",
        "source_plan_execution_manifest_digest", "source_remediation_or_method_results_review_after_diagnostic_capture_digest",
        "source_remediation_or_method_execution_after_diagnostic_capture_digest",
        "source_receipt_recovery_or_recapture_results_review_digest",
        "source_receipt_recovery_or_recapture_execution_digest", "source_receipt_recovery_or_recapture_receipt_digest",
        "source_planning_execution_digest", "source_complete_29_row_binding_digest",
        "source_materialized_payload_digest", "source_recovery_detail_digest", "source_module_grouping_digest",
        "source_staged_inventory_digest",
    ):
        assert diagnosis[field] == service.SOURCE_BINDINGS[field]


def test_durable_receipt_is_bound_but_not_parsed(diagnosis):
    assert diagnosis["source_durable_receipt_path"].endswith("RECEIPT_V1.json")
    assert diagnosis["diagnostic_receipt_parsed_in_diagnosis"] is False
    assert diagnosis["diagnostic_output_analyzed_in_diagnosis"] is False


def test_retry_counts_priority_modules_and_totals_are_bound(diagnosis):
    assert diagnosis["retry_failure_context"]["counts"] == {"passed": 24877, "failed": 1292, "errors": 112, "skipped": 7}
    assert len(diagnosis["priority_1_target_modules"]) == 5
    assert diagnosis["priority_1_total_nodeids"] == 612
    assert diagnosis["top_10_count_sum"] == 1069
    assert diagnosis["module_summary_module_count"] == 29
    assert diagnosis["failed_or_errored_nodeids_count"] == 1404


def test_diagnostic_capture_facts_are_bound_only(diagnosis):
    assert diagnosis["source_exit_code"] == 1
    assert diagnosis["source_stdout_byte_count"] == 1231380
    assert diagnosis["source_stderr_byte_count"] == 0
    assert diagnosis["source_stdout_sha256"] == "b5fb29f6cf8af77700da74c72f08b854c33bc1ad30c79c309c6eefee70171d2a"
    assert diagnosis["source_stderr_sha256"] == "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    assert diagnosis["diagnostic_capture_evidence_summary"]["diagnostic_only"] is True


def test_priority1_validation_source_facts_are_bound(diagnosis):
    assert diagnosis["priority1_pre_change_validation_passed"] is True
    assert diagnosis["priority1_pre_change_validation_passed_count"] == 675
    assert diagnosis["priority1_post_change_validation_passed"] is True
    assert diagnosis["priority1_post_change_validation_passed_count"] == 675
    assert diagnosis["priority1_post_change_validation_duration_seconds"] == "41.88"
    assert diagnosis["priority1_post_change_stdout_sha256"] == "e3d3087f3ffa39552c5a1264c8043ed6fa8a875f62f6ed94cb8986425978b374"
    assert diagnosis["priority1_post_change_stderr_sha256"] == "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    assert diagnosis["priority1_validation_summary"]["not_retry_evidence"] is True


def test_observable_families_and_workstreams_are_bound(diagnosis):
    assert {item["family_id"] for item in diagnosis["reviewed_observable_failure_families"]} == set(service.source.FAMILY_IDS)
    assert all(item["confidence"] == "HIGH" and item["observable_evidence_count"] == 47 for item in diagnosis["reviewed_observable_failure_families"])
    assert {item["workstream_id"] for item in diagnosis["reviewed_workstreams"]} == set(service.source.WORKSTREAM_IDS)
    assert diagnosis["observable_failure_family_count"] == diagnosis["source_workstream_count"] == 4
    assert diagnosis["total_observable_evidence_items"] == 188


def test_failure_classification_is_exact(diagnosis):
    assert diagnosis["primary_failure_class"] == service.PRIMARY_FAILURE_CLASS
    assert diagnosis["secondary_failure_classes"] == list(service.SECONDARY_FAILURE_CLASSES)
    assert len(diagnosis["diagnosis_domains"]) == 11
    assert len(diagnosis["diagnosis_findings"]) == 12


def test_file_inventory_and_fail_closed_facts(diagnosis):
    inventory = diagnosis["file_impact_inventory_summary"]
    assert inventory["candidate_count"] == inventory["unchanged_candidate_count"] == 10
    assert inventory["changed_candidate_count"] == 0
    assert diagnosis["safe_source_authority_bound_change_identified"] is False
    assert diagnosis["retained_change_records_available"] is False
    assert diagnosis["remediation_execution_correctly_blocked"] is True
    assert diagnosis["success_digests_generated"] is False


def test_no_remediation_or_downstream_authority(diagnosis):
    for field in service.FALSE_FIELDS:
        assert diagnosis[field] is False
    assert diagnosis["predictive_usefulness"] == diagnosis["profitability"] == service.NOT_ACCEPTED
    assert diagnosis["runtime_use"] == diagnosis["strategy_use"] == diagnosis["paper_trading"] == diagnosis["broker_execution"] == service.NOT_AUTHORIZED


def test_recommendation_chain_gates_and_risks_are_defined(diagnosis):
    assert diagnosis["recommended_next_package"] == service.RECOMMENDED_NEXT_PACKAGE
    assert diagnosis["recommended_next_task"] == service.RECOMMENDED_NEXT_TASK
    assert diagnosis["recommendation"]["recommended_next_task_status"] == "FUTURE_CANDIDATE_NOT_CREATED"
    assert diagnosis["next_chain"] == list(service.NEXT_CHAIN)
    assert diagnosis["next_gates"] == list(service.NEXT_GATES)
    assert diagnosis["risk_controls"] == list(service.RISK_CONTROLS)


def test_checklist_passes(diagnosis):
    assert diagnosis["summary"]["total_checks"] == len(diagnosis["checklist"])
    assert diagnosis["summary"]["passed_checks"] == len(diagnosis["checklist"])
    assert diagnosis["summary"]["failed_checks"] == diagnosis["summary"]["blocker_count"] == 0


def test_digest_is_deterministic():
    left = service.build_marketflow_repository_integration_branch_retry_failure_remediation_execution_after_plan_results_review_failure_diagnosis_v1()
    right = service.build_marketflow_repository_integration_branch_retry_failure_remediation_execution_after_plan_results_review_failure_diagnosis_v1()
    assert left[service.DIAGNOSIS_DIGEST_KEY] == right[service.DIAGNOSIS_DIGEST_KEY]


def test_validator_accepts_valid_diagnosis(diagnosis):
    result = service.validate_marketflow_repository_integration_branch_retry_failure_remediation_execution_after_plan_results_review_failure_diagnosis_v1(diagnosis)
    assert result["diagnosis_digest"] == diagnosis[service.DIAGNOSIS_DIGEST_KEY]
    assert result["failed_checks"] == 0


@pytest.mark.parametrize("field", sorted(service.SOURCE_BINDINGS))
def test_validator_rejects_changed_source_binding(diagnosis, field):
    changed = deepcopy(diagnosis)
    changed[field] = "changed"
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionAfterPlanResultsReviewFailureDiagnosisError):
        service.validate_marketflow_repository_integration_branch_retry_failure_remediation_execution_after_plan_results_review_failure_diagnosis_v1(changed)


@pytest.mark.parametrize("field", service.TRUE_FIELDS)
def test_validator_rejects_required_true_fact_changed(diagnosis, field):
    changed = deepcopy(diagnosis)
    changed[field] = False
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionAfterPlanResultsReviewFailureDiagnosisError):
        service.validate_marketflow_repository_integration_branch_retry_failure_remediation_execution_after_plan_results_review_failure_diagnosis_v1(changed)


@pytest.mark.parametrize("field", service.FALSE_FIELDS)
def test_validator_rejects_forbidden_fact_true(diagnosis, field):
    changed = deepcopy(diagnosis)
    changed[field] = True
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionAfterPlanResultsReviewFailureDiagnosisError):
        service.validate_marketflow_repository_integration_branch_retry_failure_remediation_execution_after_plan_results_review_failure_diagnosis_v1(changed)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("artifact_kind", "WRONG"), ("diagnosis_status", "WRONG"), ("diagnosis_scope", "WRONG"),
        ("selected_remediation_execution_package", "WRONG"), ("primary_failure_class", "WRONG"),
        ("secondary_failure_classes", []), ("priority_1_target_modules", []), ("priority_1_total_nodeids", 611),
        ("top_10_count_sum", 1068), ("module_summary_module_count", 28),
        ("failed_or_errored_nodeids_count", 1403), ("source_exit_code", 0),
        ("source_stdout_sha256", "0" * 64), ("source_stderr_sha256", "0" * 64),
        ("priority1_pre_change_validation_passed_count", 674),
        ("priority1_post_change_validation_passed", False),
        ("priority1_post_change_validation_passed_count", 674),
        ("priority1_post_change_stdout_sha256", "0" * 64),
        ("observable_failure_family_count", 3), ("total_observable_evidence_items", 187),
        ("source_workstream_count", 3), ("predictive_usefulness", "accepted"),
        ("profitability", "accepted"), ("runtime_use", "AUTHORIZED"), ("broker_execution", "AUTHORIZED"),
    ],
)
def test_validator_rejects_changed_fixed_contract(diagnosis, field, value):
    changed = deepcopy(diagnosis)
    changed[field] = value
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionAfterPlanResultsReviewFailureDiagnosisError):
        service.validate_marketflow_repository_integration_branch_retry_failure_remediation_execution_after_plan_results_review_failure_diagnosis_v1(changed)


@pytest.mark.parametrize("field", ["diagnosis_domains", "diagnosis_findings", "recommendation", "next_chain", "next_gates", "risk_controls"])
def test_validator_rejects_missing_governance_content(diagnosis, field):
    changed = deepcopy(diagnosis)
    changed[field] = [] if field != "recommendation" else {}
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionAfterPlanResultsReviewFailureDiagnosisError):
        service.validate_marketflow_repository_integration_branch_retry_failure_remediation_execution_after_plan_results_review_failure_diagnosis_v1(changed)


def test_validator_rejects_retry_counts_or_families_or_workstreams_missing(diagnosis):
    mutations = []
    missing_counts = deepcopy(diagnosis)
    missing_counts["retry_failure_context"]["counts"] = {}
    mutations.append(missing_counts)
    missing_family = deepcopy(diagnosis)
    missing_family["reviewed_observable_failure_families"] = missing_family["reviewed_observable_failure_families"][:-1]
    mutations.append(missing_family)
    missing_workstream = deepcopy(diagnosis)
    missing_workstream["reviewed_workstreams"] = missing_workstream["reviewed_workstreams"][:-1]
    mutations.append(missing_workstream)
    for changed in mutations:
        with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionAfterPlanResultsReviewFailureDiagnosisError):
            service.validate_marketflow_repository_integration_branch_retry_failure_remediation_execution_after_plan_results_review_failure_diagnosis_v1(changed)


def test_validator_rejects_changed_diagnosis_digest(diagnosis):
    changed = deepcopy(diagnosis)
    changed[service.DIAGNOSIS_DIGEST_KEY] = "0" * 64
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionAfterPlanResultsReviewFailureDiagnosisError):
        service.validate_marketflow_repository_integration_branch_retry_failure_remediation_execution_after_plan_results_review_failure_diagnosis_v1(changed)


def test_writer_writes_isolated_status_and_refuses_overwrite(tmp_path):
    artifact = service.write_marketflow_repository_integration_branch_retry_failure_remediation_execution_after_plan_results_review_failure_diagnosis_v1(tmp_path)
    path = tmp_path / "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_AFTER_PLAN_RESULTS_REVIEW_FAILURE_DIAGNOSIS_STATUS.md"
    assert artifact["artifact_kind"] == service.ARTIFACT_KIND
    assert path.is_file()
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionAfterPlanResultsReviewFailureDiagnosisError):
        service.write_marketflow_repository_integration_branch_retry_failure_remediation_execution_after_plan_results_review_failure_diagnosis_v1(tmp_path)


@pytest.mark.parametrize("protected", [".marketflow", ".pytest_cache", ".env"])
def test_writer_rejects_protected_output(protected):
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionAfterPlanResultsReviewFailureDiagnosisError):
        service.write_marketflow_repository_integration_branch_retry_failure_remediation_execution_after_plan_results_review_failure_diagnosis_v1(Path(protected))


def test_markdown_contains_required_sections(diagnosis):
    markdown = service.build_marketflow_repository_integration_branch_retry_failure_remediation_execution_after_plan_results_review_failure_diagnosis_markdown_v1(diagnosis)
    assert markdown.startswith("# MarketFlow Repository Integration Branch Retry Failure Remediation Execution After Plan Results Review Failure Diagnosis v1")
    for section in service.MARKDOWN_SECTIONS:
        assert f"## {section}" in markdown


def test_public_aliases_match_contract():
    assert service.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_AFTER_PLAN_RESULTS_REVIEW_FAILURE_DIAGNOSIS_V1 == service.ARTIFACT_KIND
    assert service.MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_AFTER_PLAN_RESULTS_REVIEW_FAILURE_DIAGNOSIS_READY == service.DIAGNOSIS_STATUS
    assert service.NO_SAFE_SOURCE_AUTHORITY_BOUND_REMEDIATION_CHANGE_IDENTIFIED == service.PRIMARY_FAILURE_CLASS
