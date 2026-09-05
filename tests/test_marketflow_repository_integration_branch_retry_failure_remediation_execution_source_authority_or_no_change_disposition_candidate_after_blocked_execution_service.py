from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import pytest

from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_candidate_after_blocked_execution_service
    as service,
)


@pytest.fixture()
def candidate():
    return service.build_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_candidate_after_blocked_execution_v1()


def _validate(candidate):
    return service.validate_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_candidate_after_blocked_execution_v1(
        candidate
    )


def _assert_rejected(candidate):
    with pytest.raises(
        service.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionSourceAuthorityOrNoChangeDispositionCandidateAfterBlockedExecutionError
    ):
        _validate(candidate)


def test_candidate_builds_offline_with_exact_identity(candidate):
    assert candidate["artifact_kind"] == service.ARTIFACT_KIND
    assert candidate["schema_version"] == service.SCHEMA_VERSION
    assert candidate["candidate_status"] == service.CANDIDATE_STATUS
    assert candidate["candidate_scope"] == service.CANDIDATE_SCOPE
    assert candidate["created_offline"] is True
    assert candidate["governance_only"] is True
    assert candidate["candidate_only"] is True
    assert candidate["operator_review_required"] is True


def test_failure_diagnosis_and_blocked_execution_are_bound(candidate):
    assert candidate["source_failure_diagnosis_commit"] == service.SOURCE_FAILURE_DIAGNOSIS_COMMIT
    assert candidate["source_remediation_execution_after_plan_results_review_failure_diagnosis_digest"] == service.SOURCE_FAILURE_DIAGNOSIS_DIGEST
    assert candidate["source_blocked_execution_commit"] == service.source.SOURCE_BLOCKED_EXECUTION_COMMIT
    assert candidate["source_blocked_execution_artifact_kind"] == service.source.source.BLOCKED_ARTIFACT_KIND
    assert candidate["source_blocked_execution_status"] == service.source.source.BLOCKED_STATUS
    assert candidate["source_blocked_execution_scope"] == service.source.source.EXECUTION_SCOPE
    assert candidate["source_blocked_reason"] == service.source.SOURCE_BLOCKED_REASON
    assert candidate["source_blocked_manifest_digest"] == service.source.SOURCE_BLOCKED_MANIFEST_DIGEST


def test_failure_classification_is_exact(candidate):
    assert candidate["primary_failure_class"] == service.source.PRIMARY_FAILURE_CLASS
    assert candidate["secondary_failure_classes"] == list(service.source.SECONDARY_FAILURE_CLASSES)
    assert candidate["safe_source_authority_bound_change_identified"] is False
    assert candidate["retained_change_records_available"] is False
    assert candidate["success_digests_generated"] is False


def test_all_prior_source_evidence_is_digest_bound(candidate):
    assert set(service.SOURCE_BINDINGS) <= set(candidate)
    for field, expected in service.SOURCE_BINDINGS.items():
        assert candidate[field] == expected


def test_retry_failure_and_priority1_context_are_preserved(candidate):
    assert candidate["retry_failure_context"]["counts"] == {
        "passed": 24877,
        "failed": 1292,
        "errors": 112,
        "skipped": 7,
    }
    assert candidate["retry_failure_context"]["first_result_authoritative"] is True
    assert candidate["priority_1_total_nodeids"] == 612
    assert candidate["top_10_count_sum"] == 1069
    assert candidate["module_summary_module_count"] == 29
    assert candidate["failed_or_errored_nodeids_count"] == 1404
    assert len(candidate["priority_1_target_modules"]) == 5


def test_priority1_evidence_remains_focused_current_root_evidence_only(candidate):
    assert candidate["priority1_pre_change_validation_passed"] is True
    assert candidate["priority1_pre_change_validation_passed_count"] == 675
    assert candidate["priority1_post_change_validation_passed"] is True
    assert candidate["priority1_post_change_validation_passed_count"] == 675
    assert candidate["priority1_validation_summary"]["post_change_duration_seconds"] == "41.88"
    assert candidate["priority1_validation_summary"]["not_retry_evidence"] is True
    assert candidate["priority1_post_change_stdout_sha256"] == "e3d3087f3ffa39552c5a1264c8043ed6fa8a875f62f6ed94cb8986425978b374"


def test_diagnostic_metadata_is_preserved_without_analysis(candidate):
    assert candidate["source_exit_code"] == 1
    assert candidate["source_stdout_byte_count"] == 1231380
    assert candidate["source_stderr_byte_count"] == 0
    assert candidate["diagnostic_capture_evidence_summary"]["duration_seconds"] == "21.584361"
    assert candidate["diagnostic_capture_evidence_summary"]["diagnostic_only"] is True
    assert candidate["diagnostic_receipt_parsed_in_candidate"] is False
    assert candidate["diagnostic_output_analyzed_in_candidate"] is False


def test_observable_families_and_workstreams_remain_planning_evidence(candidate):
    families = candidate["reviewed_observable_failure_families"]
    workstreams = candidate["reviewed_workstreams"]
    assert {item["family_id"] for item in families} == set(service.source.source.FAMILY_IDS)
    assert all(item["observable_evidence_count"] == 47 and item["confidence"] == "HIGH" for item in families)
    assert {item["workstream_id"] for item in workstreams} == set(service.source.source.WORKSTREAM_IDS)
    assert candidate["observable_failure_family_count"] == candidate["source_workstream_count"] == 4
    assert candidate["total_observable_evidence_items"] == 188


def test_candidate_philosophy_is_exact(candidate):
    assert candidate["candidate_philosophy"] == {
        "source_authority_or_no_change_disposition_candidate_philosophy": service.CANDIDATE_PHILOSOPHY,
        "candidate_boundary": service.CANDIDATE_BOUNDARY,
        "candidate_goal": service.CANDIDATE_GOAL,
    }


def test_twelve_packages_are_defined_but_none_is_selected(candidate):
    packages = candidate["proposed_source_authority_or_no_change_disposition_packages"]
    assert packages == service._packages()
    assert len(packages) == 12
    assert sum(item["status"] == "BLOCKED_NOT_ALLOWED" for item in packages) == 6
    assert all(not item["selected"] and not item["approved"] and not item["authorized"] and not item["executed"] for item in packages)


def test_recommended_package_is_review_only(candidate):
    assert candidate["recommended_source_authority_or_no_change_disposition_package"] == service.RECOMMENDED_PACKAGE
    assert candidate["recommendation_status"] == "RECOMMENDED_FOR_OPERATOR_REVIEW_NOT_SELECTED"
    assert candidate["recommended_package"]["package_id"] == service.RECOMMENDED_PACKAGE
    assert candidate["recommended_package"]["status"] == "RECOMMENDED_FOR_OPERATOR_REVIEW_NOT_SELECTED"
    assert all(candidate["recommended_package"][field] is False for field in ("selected", "approved", "authorized", "executed"))


def test_future_contract_is_defined_not_executed(candidate):
    assert [item["requirement_id"] for item in candidate["future_requirements"]] == list(service.FUTURE_REQUIREMENT_IDS)
    assert all(item["status"] == "REQUIRED_FOR_FUTURE_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION" and item["execution_status"] == "NOT_EXECUTED" for item in candidate["future_requirements"])
    assert [item["action"] for item in candidate["future_plan"]] == list(service.FUTURE_PLAN)
    assert candidate["future_plan_status"] == "PLANNED_NOT_EXECUTED"
    assert [item["output_name"] for item in candidate["planned_outputs"]] == list(service.PLANNED_OUTPUT_NAMES)
    assert all(item["status"] == "PLANNED_NOT_GENERATED" for item in candidate["planned_outputs"])


def test_non_goals_chain_gates_and_risk_controls_are_exact(candidate):
    assert candidate["non_goals"] == list(service.NON_GOALS)
    assert candidate["next_chain"] == list(service.NEXT_CHAIN)
    assert candidate["next_gates"] == list(service.NEXT_GATES)
    assert candidate["risk_controls"] == list(service.RISK_CONTROLS)


def test_all_authority_boundaries_remain_closed(candidate):
    for field in service.FALSE_FIELDS:
        assert candidate[field] is False
    assert candidate["predictive_usefulness"] == candidate["profitability"] == service.NOT_ACCEPTED
    assert candidate["runtime_use"] == candidate["strategy_use"] == candidate["paper_trading"] == candidate["broker_execution"] == service.NOT_AUTHORIZED


def test_checklist_passes_without_blockers(candidate):
    assert candidate["summary"]["total_checks"] == len(candidate["checklist"])
    assert candidate["summary"]["passed_checks"] == len(candidate["checklist"])
    assert candidate["summary"]["failed_checks"] == candidate["summary"]["blocker_count"] == 0
    assert all(item["status"] == service.PASS for item in candidate["checklist"])


def test_digest_is_deterministic():
    left = service.build_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_candidate_after_blocked_execution_v1()
    right = service.build_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_candidate_after_blocked_execution_v1()
    assert left[service.CANDIDATE_DIGEST_KEY] == right[service.CANDIDATE_DIGEST_KEY]


def test_validator_accepts_valid_candidate(candidate):
    result = _validate(candidate)
    assert result["candidate_digest"] == candidate[service.CANDIDATE_DIGEST_KEY]
    assert result["passed_checks"] == result["total_checks"]
    assert result["failed_checks"] == result["blocker_count"] == 0


def test_builder_accepts_exact_source_diagnosis():
    diagnosis = service.source.build_marketflow_repository_integration_branch_retry_failure_remediation_execution_after_plan_results_review_failure_diagnosis_v1()
    candidate = service.build_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_candidate_after_blocked_execution_v1(source_failure_diagnosis=diagnosis)
    assert candidate["source_remediation_execution_after_plan_results_review_failure_diagnosis_digest"] == service.SOURCE_FAILURE_DIAGNOSIS_DIGEST


def test_builder_rejects_changed_source_diagnosis():
    diagnosis = service.source.build_marketflow_repository_integration_branch_retry_failure_remediation_execution_after_plan_results_review_failure_diagnosis_v1()
    diagnosis["source_blocked_reason"] = "CHANGED"
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionSourceAuthorityOrNoChangeDispositionCandidateAfterBlockedExecutionError):
        service.build_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_candidate_after_blocked_execution_v1(source_failure_diagnosis=diagnosis)


@pytest.mark.parametrize("field", sorted(service.SOURCE_BINDINGS))
def test_validator_rejects_changed_source_binding(candidate, field):
    changed = deepcopy(candidate)
    changed[field] = "changed"
    _assert_rejected(changed)


@pytest.mark.parametrize("field", service.TRUE_FIELDS)
def test_validator_rejects_required_true_fact_changed(candidate, field):
    changed = deepcopy(candidate)
    changed[field] = False
    _assert_rejected(changed)


@pytest.mark.parametrize("field", service.FALSE_FIELDS)
def test_validator_rejects_forbidden_fact_true(candidate, field):
    changed = deepcopy(candidate)
    changed[field] = True
    _assert_rejected(changed)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("artifact_kind", "WRONG"),
        ("schema_version", "WRONG"),
        ("candidate_status", "WRONG"),
        ("candidate_scope", "WRONG"),
        ("created_offline", False),
        ("governance_only", False),
        ("candidate_only", False),
        ("operator_review_required", False),
        ("selected_remediation_execution_package", "WRONG"),
        ("primary_failure_class", "WRONG"),
        ("secondary_failure_classes", []),
        ("recommended_source_authority_or_no_change_disposition_package", "WRONG"),
        ("recommendation_status", "WRONG"),
        ("priority_1_target_modules", []),
        ("priority_1_total_nodeids", 611),
        ("top_10_count_sum", 1068),
        ("module_summary_module_count", 28),
        ("failed_or_errored_nodeids_count", 1403),
        ("priority1_pre_change_validation_passed", False),
        ("priority1_pre_change_validation_passed_count", 674),
        ("priority1_post_change_validation_passed", False),
        ("priority1_post_change_validation_passed_count", 674),
        ("priority1_post_change_stdout_sha256", "0" * 64),
        ("source_exit_code", 0),
        ("source_stdout_byte_count", 0),
        ("source_stderr_byte_count", 1),
        ("source_stdout_sha256", "0" * 64),
        ("source_stderr_sha256", "0" * 64),
        ("observable_failure_family_count", 3),
        ("total_observable_evidence_items", 187),
        ("source_workstream_count", 3),
        ("predictive_usefulness", "accepted"),
        ("profitability", "accepted"),
        ("runtime_use", "AUTHORIZED"),
        ("strategy_use", "AUTHORIZED"),
        ("paper_trading", "AUTHORIZED"),
        ("broker_execution", "AUTHORIZED"),
        ("no_tracked_marketflow_files", False),
        ("no_tracked_pytest_cache_files", False),
    ],
)
def test_validator_rejects_changed_fixed_contract(candidate, field, value):
    changed = deepcopy(candidate)
    changed[field] = value
    _assert_rejected(changed)


@pytest.mark.parametrize("package_index", range(len(service.PACKAGE_DEFINITIONS)))
@pytest.mark.parametrize("field", ["status", "selected", "approved", "authorized", "executed"])
def test_validator_rejects_changed_package_contract(candidate, package_index, field):
    changed = deepcopy(candidate)
    package = changed["proposed_source_authority_or_no_change_disposition_packages"][package_index]
    package[field] = True if field != "status" else "CHANGED"
    _assert_rejected(changed)


@pytest.mark.parametrize("requirement_index", range(len(service.FUTURE_REQUIREMENT_IDS)))
def test_validator_rejects_changed_future_requirement(candidate, requirement_index):
    changed = deepcopy(candidate)
    changed["future_requirements"][requirement_index]["execution_status"] = "EXECUTED"
    _assert_rejected(changed)


@pytest.mark.parametrize("plan_index", range(len(service.FUTURE_PLAN)))
def test_validator_rejects_changed_future_plan(candidate, plan_index):
    changed = deepcopy(candidate)
    changed["future_plan"][plan_index]["action"] = "changed"
    _assert_rejected(changed)


@pytest.mark.parametrize("output_index", range(len(service.PLANNED_OUTPUT_NAMES)))
def test_validator_rejects_changed_planned_output(candidate, output_index):
    changed = deepcopy(candidate)
    changed["planned_outputs"][output_index]["status"] = "GENERATED"
    _assert_rejected(changed)


@pytest.mark.parametrize("non_goal", service.NON_GOALS)
def test_validator_rejects_missing_non_goal(candidate, non_goal):
    changed = deepcopy(candidate)
    changed["non_goals"].remove(non_goal)
    _assert_rejected(changed)


@pytest.mark.parametrize("risk_control", service.RISK_CONTROLS)
def test_validator_rejects_missing_risk_control(candidate, risk_control):
    changed = deepcopy(candidate)
    changed["risk_controls"].remove(risk_control)
    _assert_rejected(changed)


@pytest.mark.parametrize("field", ["candidate_philosophy", "recommended_package", "next_chain", "next_gates"])
def test_validator_rejects_changed_governance_content(candidate, field):
    changed = deepcopy(candidate)
    changed[field] = {} if isinstance(changed[field], dict) else []
    _assert_rejected(changed)


def test_validator_rejects_changed_retry_counts_families_or_workstreams(candidate):
    mutations = []
    counts = deepcopy(candidate)
    counts["retry_failure_context"]["counts"] = {}
    mutations.append(counts)
    families = deepcopy(candidate)
    families["reviewed_observable_failure_families"] = families["reviewed_observable_failure_families"][:-1]
    mutations.append(families)
    workstreams = deepcopy(candidate)
    workstreams["reviewed_workstreams"] = workstreams["reviewed_workstreams"][:-1]
    mutations.append(workstreams)
    for changed in mutations:
        _assert_rejected(changed)


def test_validator_rejects_changed_checklist_summary_or_digest(candidate):
    mutations = []
    checklist = deepcopy(candidate)
    checklist["checklist"] = []
    mutations.append(checklist)
    summary = deepcopy(candidate)
    summary["summary"]["total_checks"] = 0
    mutations.append(summary)
    digest = deepcopy(candidate)
    digest[service.CANDIDATE_DIGEST_KEY] = "0" * 64
    mutations.append(digest)
    for changed in mutations:
        _assert_rejected(changed)


def test_writer_writes_isolated_status_and_refuses_overwrite(tmp_path):
    artifact = service.write_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_candidate_after_blocked_execution_v1(tmp_path)
    path = tmp_path / "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_CANDIDATE_AFTER_BLOCKED_EXECUTION_STATUS.md"
    assert artifact["artifact_kind"] == service.ARTIFACT_KIND
    assert path.is_file()
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionSourceAuthorityOrNoChangeDispositionCandidateAfterBlockedExecutionError):
        service.write_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_candidate_after_blocked_execution_v1(tmp_path)


@pytest.mark.parametrize("protected", [".marketflow", ".pytest_cache", ".env"])
def test_writer_rejects_protected_output(protected):
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionSourceAuthorityOrNoChangeDispositionCandidateAfterBlockedExecutionError):
        service.write_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_candidate_after_blocked_execution_v1(Path(protected))


def test_markdown_contains_required_sections(candidate):
    markdown = service.build_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_candidate_after_blocked_execution_markdown_v1(candidate)
    assert markdown.startswith("# MarketFlow Repository Integration Branch Retry Failure Remediation Execution Source Authority or No-Change Disposition Candidate After Blocked Execution v1")
    for section in service.MARKDOWN_SECTIONS:
        assert f"## {section}" in markdown


def test_public_aliases_match_contract():
    assert service.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_CANDIDATE_AFTER_BLOCKED_EXECUTION_V1 == service.ARTIFACT_KIND
    assert service.MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_CANDIDATE_AFTER_BLOCKED_EXECUTION_READY_FOR_OPERATOR_REVIEW == service.CANDIDATE_STATUS
    assert service.REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_CANDIDATE_AFTER_BLOCKED_EXECUTION_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN == service.CANDIDATE_SCOPE
    assert service.NO_SAFE_SOURCE_AUTHORITY_BOUND_REMEDIATION_CHANGE_IDENTIFIED == service.source.PRIMARY_FAILURE_CLASS
    assert service.MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_CANDIDATE_AFTER_BLOCKED_EXECUTION_DIGEST_KEY == service.CANDIDATE_DIGEST_KEY
