from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import pytest

from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_candidate_after_blocked_execution_operator_review_service
    as service,
)


@pytest.fixture()
def review():
    return service.build_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_candidate_after_blocked_execution_operator_review_v1()


def _validate(review):
    return service.validate_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_candidate_after_blocked_execution_operator_review_v1(review)


def _assert_rejected(review):
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionSourceAuthorityOrNoChangeDispositionCandidateAfterBlockedExecutionOperatorReviewError):
        _validate(review)


def test_review_builds_offline_with_exact_identity(review):
    assert review["artifact_kind"] == service.ARTIFACT_KIND
    assert review["schema_version"] == service.SCHEMA_VERSION
    assert review["review_status"] == service.REVIEW_STATUS
    assert review["review_scope"] == service.REVIEW_SCOPE
    assert review["created_offline"] is review["governance_only"] is review["operator_review_only"] is True


def test_source_candidate_is_bound(review):
    assert review["source_candidate_artifact_kind"] == service.source.ARTIFACT_KIND
    assert review["source_candidate_status"] == service.source.CANDIDATE_STATUS
    assert review["source_candidate_scope"] == service.source.CANDIDATE_SCOPE
    assert review["source_candidate_commit"] == service.SOURCE_CANDIDATE_COMMIT
    assert review["source_authority_or_no_change_disposition_candidate_after_blocked_execution_digest"] == service.SOURCE_CANDIDATE_DIGEST
    assert review["source_candidate_summary"]["checklist"] == "267/267 PASS"


def test_all_prior_source_evidence_is_bound(review):
    for field, expected in service.SOURCE_BINDINGS.items():
        assert review[field] == expected


def test_failure_diagnosis_and_blocked_execution_remain_source_evidence(review):
    assert review["source_failure_diagnosis_commit"] == "954a3654bc6b1a485d2b13fe2462510ffebe1025"
    assert review["source_remediation_execution_after_plan_results_review_failure_diagnosis_digest"] == "0cdff5ed2e41e77a90c1be358428aaf74a3fcf04b82513771e64e01493381171"
    assert review["source_blocked_execution_commit"] == "65aab2f4a5cc699cc630756c4142dee12f96c838"
    assert review["source_blocked_reason"] == service.source.source.SOURCE_BLOCKED_REASON
    assert review["source_blocked_manifest_digest"] == "fcb2de55c19e4aac04f80612a252f38393ed13d8fb7a74d5db1452077da95002"


def test_failure_classification_is_exact(review):
    assert review["primary_failure_class"] == service.source.source.PRIMARY_FAILURE_CLASS
    assert review["secondary_failure_classes"] == list(service.source.source.SECONDARY_FAILURE_CLASSES)
    assert len(review["secondary_failure_classes"]) == 4


def test_retry_and_priority1_evidence_is_preserved(review):
    assert review["retry_failure_context"]["counts"] == {"passed": 24877, "failed": 1292, "errors": 112, "skipped": 7}
    assert review["priority_1_total_nodeids"] == 612
    assert review["top_10_count_sum"] == 1069
    assert review["module_summary_module_count"] == 29
    assert review["failed_or_errored_nodeids_count"] == 1404
    assert len(review["priority_1_target_modules"]) == 5
    assert review["priority1_pre_change_validation_passed_count"] == 675
    assert review["priority1_post_change_validation_passed_count"] == 675
    assert review["priority1_validation_summary"]["not_retry_evidence"] is True


def test_diagnostic_metadata_is_bound_without_analysis(review):
    assert review["source_exit_code"] == 1
    assert review["source_stdout_byte_count"] == 1231380
    assert review["source_stderr_byte_count"] == 0
    assert review["diagnostic_capture_evidence_summary"]["duration_seconds"] == "21.584361"
    assert review["diagnostic_receipt_parsed_in_review"] is False
    assert review["diagnostic_output_analyzed_in_review"] is False


def test_families_and_workstreams_are_preserved(review):
    assert {item["family_id"] for item in review["reviewed_observable_failure_families"]} == set(service.source.source.source.FAMILY_IDS)
    assert all(item["observable_evidence_count"] == 47 and item["confidence"] == "HIGH" for item in review["reviewed_observable_failure_families"])
    assert {item["workstream_id"] for item in review["reviewed_workstreams"]} == set(service.source.source.source.WORKSTREAM_IDS)
    assert review["observable_failure_family_count"] == review["source_workstream_count"] == 4
    assert review["total_observable_evidence_items"] == 188


def test_reviewed_candidate_philosophy_is_exact(review):
    assert review["reviewed_candidate_philosophy"] == {
        "reviewed_source_authority_or_no_change_disposition_candidate_philosophy": service.REVIEWED_CANDIDATE_PHILOSOPHY,
        "reviewed_candidate_boundary": service.REVIEWED_CANDIDATE_BOUNDARY,
        "reviewed_candidate_goal": service.REVIEWED_CANDIDATE_GOAL,
        "review_status": "REVIEWED_PLANNING_ONLY",
    }


def test_all_twelve_packages_are_reviewed_without_selection(review):
    packages = review["reviewed_source_authority_or_no_change_disposition_packages"]
    assert len(packages) == 12
    assert sum(item["review_status"] == "REVIEWED_BLOCKED_NOT_ALLOWED" for item in packages) == 6
    assert sum(item["review_status"] == "REVIEWED_AVAILABLE_PACKAGE_NOT_SELECTED" for item in packages) == 5
    assert sum(item["review_status"] == "REVIEWED_RECOMMENDED_PACKAGE_FOR_OPERATOR_ASSESSMENT_NOT_SELECTED" for item in packages) == 1
    assert all(not item["selected"] and not item["approved"] and not item["authorized"] and not item["executed"] for item in packages)


def test_recommended_package_remains_unselected(review):
    assert review["recommended_source_authority_or_no_change_disposition_package"] == service.RECOMMENDED_PACKAGE
    assert review["recommendation_status"] == "REVIEWED_RECOMMENDED_FOR_OPERATOR_ASSESSMENT_NOT_SELECTED"
    assert review["recommendation"] == service._recommendation()
    assert review["recommendation"]["recommended_next_task_status"] == "FUTURE_APPROVAL_NOT_CREATED"


def test_all_future_governance_content_is_reviewed_only(review):
    assert review["reviewed_future_requirements"] == service._reviewed_requirements()
    assert review["reviewed_future_plan"] == service._reviewed_plan()
    assert review["reviewed_planned_outputs"] == service._reviewed_outputs()
    assert review["reviewed_non_goals"] == service._reviewed_non_goals()
    assert len(review["reviewed_future_requirements"]) == 50
    assert len(review["reviewed_future_plan"]) == 12
    assert len(review["reviewed_planned_outputs"]) == 21
    assert len(review["reviewed_non_goals"]) == 71


def test_chain_gates_and_risk_controls_are_exact(review):
    assert review["next_chain"] == list(service.NEXT_CHAIN)
    assert review["next_gates"] == list(service.NEXT_GATES)
    assert review["risk_controls"] == list(service.RISK_CONTROLS)
    assert len(review["next_chain"]) == len(review["next_gates"]) == 9
    assert len(review["risk_controls"]) == 95


def test_all_authority_boundaries_remain_closed(review):
    for field in service.FALSE_FIELDS:
        assert review[field] is False
    assert review["predictive_usefulness"] == review["profitability"] == service.NOT_ACCEPTED
    assert review["runtime_use"] == review["strategy_use"] == review["paper_trading"] == review["broker_execution"] == service.NOT_AUTHORIZED


def test_checklist_passes_without_blockers(review):
    assert review["summary"]["total_checks"] == len(review["checklist"])
    assert review["summary"]["passed_checks"] == len(review["checklist"])
    assert review["summary"]["failed_checks"] == review["summary"]["blocker_count"] == 0


def test_digest_is_deterministic():
    left = service.build_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_candidate_after_blocked_execution_operator_review_v1()
    right = service.build_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_candidate_after_blocked_execution_operator_review_v1()
    assert left[service.OPERATOR_REVIEW_DIGEST_KEY] == right[service.OPERATOR_REVIEW_DIGEST_KEY]


def test_validator_accepts_valid_review(review):
    result = _validate(review)
    assert result["operator_review_digest"] == review[service.OPERATOR_REVIEW_DIGEST_KEY]
    assert result["passed_checks"] == result["total_checks"]
    assert result["failed_checks"] == result["blocker_count"] == 0


def test_builder_accepts_exact_source_candidate():
    candidate = service.source.build_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_candidate_after_blocked_execution_v1()
    review = service.build_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_candidate_after_blocked_execution_operator_review_v1(source_candidate=candidate)
    assert review["source_authority_or_no_change_disposition_candidate_after_blocked_execution_digest"] == service.SOURCE_CANDIDATE_DIGEST


def test_builder_rejects_changed_source_candidate():
    candidate = service.source.build_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_candidate_after_blocked_execution_v1()
    candidate["source_blocked_reason"] = "CHANGED"
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionSourceAuthorityOrNoChangeDispositionCandidateAfterBlockedExecutionOperatorReviewError):
        service.build_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_candidate_after_blocked_execution_operator_review_v1(source_candidate=candidate)


@pytest.mark.parametrize("field", sorted(service.SOURCE_BINDINGS))
def test_validator_rejects_changed_source_binding(review, field):
    changed = deepcopy(review)
    changed[field] = "changed"
    _assert_rejected(changed)


@pytest.mark.parametrize("field", service.TRUE_FIELDS)
def test_validator_rejects_required_true_fact_changed(review, field):
    changed = deepcopy(review)
    changed[field] = False
    _assert_rejected(changed)


@pytest.mark.parametrize("field", service.FALSE_FIELDS)
def test_validator_rejects_forbidden_fact_true(review, field):
    changed = deepcopy(review)
    changed[field] = True
    _assert_rejected(changed)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("artifact_kind", "WRONG"), ("schema_version", "WRONG"),
        ("review_status", "WRONG"), ("review_scope", "WRONG"),
        ("created_offline", False), ("governance_only", False), ("operator_review_only", False),
        ("selected_remediation_execution_package", "WRONG"), ("primary_failure_class", "WRONG"),
        ("secondary_failure_classes", []), ("recommended_source_authority_or_no_change_disposition_package", "WRONG"),
        ("recommendation_status", "WRONG"), ("priority_1_target_modules", []),
        ("priority_1_total_nodeids", 611), ("top_10_count_sum", 1068),
        ("module_summary_module_count", 28), ("failed_or_errored_nodeids_count", 1403),
        ("priority1_pre_change_validation_passed", False), ("priority1_pre_change_validation_passed_count", 674),
        ("priority1_post_change_validation_passed", False), ("priority1_post_change_validation_passed_count", 674),
        ("priority1_post_change_stdout_sha256", "0" * 64), ("source_exit_code", 0),
        ("source_stdout_byte_count", 0), ("source_stderr_byte_count", 1),
        ("source_stdout_sha256", "0" * 64), ("source_stderr_sha256", "0" * 64),
        ("observable_failure_family_count", 3), ("total_observable_evidence_items", 187),
        ("source_workstream_count", 3), ("predictive_usefulness", "accepted"),
        ("profitability", "accepted"), ("runtime_use", "AUTHORIZED"),
        ("strategy_use", "AUTHORIZED"), ("paper_trading", "AUTHORIZED"),
        ("broker_execution", "AUTHORIZED"), ("no_tracked_marketflow_files", False),
        ("no_tracked_pytest_cache_files", False),
    ],
)
def test_validator_rejects_changed_fixed_contract(review, field, value):
    changed = deepcopy(review)
    changed[field] = value
    _assert_rejected(changed)


@pytest.mark.parametrize("package_index", range(12))
@pytest.mark.parametrize("field", ["source_status", "review_status", "selected", "approved", "authorized", "executed"])
def test_validator_rejects_changed_reviewed_package(review, package_index, field):
    changed = deepcopy(review)
    changed["reviewed_source_authority_or_no_change_disposition_packages"][package_index][field] = True if field not in {"source_status", "review_status"} else "CHANGED"
    _assert_rejected(changed)


@pytest.mark.parametrize("requirement_index", range(50))
def test_validator_rejects_changed_reviewed_requirement(review, requirement_index):
    changed = deepcopy(review)
    changed["reviewed_future_requirements"][requirement_index]["execution_status"] = "EXECUTED"
    _assert_rejected(changed)


@pytest.mark.parametrize("plan_index", range(12))
def test_validator_rejects_changed_reviewed_plan(review, plan_index):
    changed = deepcopy(review)
    changed["reviewed_future_plan"][plan_index]["action"] = "changed"
    _assert_rejected(changed)


@pytest.mark.parametrize("output_index", range(21))
def test_validator_rejects_changed_reviewed_output(review, output_index):
    changed = deepcopy(review)
    changed["reviewed_planned_outputs"][output_index]["generation_status"] = "GENERATED"
    _assert_rejected(changed)


@pytest.mark.parametrize("non_goal_index", range(71))
def test_validator_rejects_changed_reviewed_non_goal(review, non_goal_index):
    changed = deepcopy(review)
    changed["reviewed_non_goals"][non_goal_index]["review_status"] = "INACTIVE"
    _assert_rejected(changed)


@pytest.mark.parametrize("risk_control", service.RISK_CONTROLS)
def test_validator_rejects_missing_risk_control(review, risk_control):
    changed = deepcopy(review)
    changed["risk_controls"].remove(risk_control)
    _assert_rejected(changed)


@pytest.mark.parametrize("field", ["source_candidate_summary", "source_failure_diagnosis_summary", "source_blocked_execution_summary", "source_approval_summary", "source_operator_review_and_candidate_summary", "source_plan_results_review_summary", "source_plan_execution_summary", "source_targeted_remediation_plan_summary", "source_workstream_mapping_summary", "source_method_results_review_summary", "source_method_execution_summary", "source_diagnostic_results_review_summary", "source_controlled_recapture_summary", "source_durable_receipt_summary", "source_receipt_loss_history_summary", "source_planning_and_detail_binding_summary", "priority1_validation_summary", "diagnostic_capture_evidence_summary", "reviewed_candidate_philosophy", "recommendation"])
def test_validator_rejects_changed_summary_or_review_content(review, field):
    changed = deepcopy(review)
    changed[field] = {}
    _assert_rejected(changed)


def test_validator_rejects_changed_retry_families_or_workstreams(review):
    mutations = []
    retry = deepcopy(review)
    retry["retry_failure_context"]["counts"] = {}
    mutations.append(retry)
    families = deepcopy(review)
    families["reviewed_observable_failure_families"] = families["reviewed_observable_failure_families"][:-1]
    mutations.append(families)
    workstreams = deepcopy(review)
    workstreams["reviewed_workstreams"] = workstreams["reviewed_workstreams"][:-1]
    mutations.append(workstreams)
    for changed in mutations:
        _assert_rejected(changed)


def test_validator_rejects_changed_checklist_summary_or_digest(review):
    mutations = []
    checklist = deepcopy(review)
    checklist["checklist"] = []
    mutations.append(checklist)
    summary = deepcopy(review)
    summary["summary"]["total_checks"] = 0
    mutations.append(summary)
    digest = deepcopy(review)
    digest[service.OPERATOR_REVIEW_DIGEST_KEY] = "0" * 64
    mutations.append(digest)
    for changed in mutations:
        _assert_rejected(changed)


def test_writer_writes_isolated_status_and_refuses_overwrite(tmp_path):
    artifact = service.write_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_candidate_after_blocked_execution_operator_review_v1(tmp_path)
    path = tmp_path / "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_CANDIDATE_AFTER_BLOCKED_EXECUTION_OPERATOR_REVIEW_STATUS.md"
    assert artifact["artifact_kind"] == service.ARTIFACT_KIND
    assert path.is_file()
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionSourceAuthorityOrNoChangeDispositionCandidateAfterBlockedExecutionOperatorReviewError):
        service.write_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_candidate_after_blocked_execution_operator_review_v1(tmp_path)


@pytest.mark.parametrize("protected", [".marketflow", ".pytest_cache", ".env"])
def test_writer_rejects_protected_output(protected):
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionSourceAuthorityOrNoChangeDispositionCandidateAfterBlockedExecutionOperatorReviewError):
        service.write_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_candidate_after_blocked_execution_operator_review_v1(Path(protected))


def test_markdown_contains_required_sections(review):
    markdown = service.build_marketflow_repository_integration_branch_retry_failure_remediation_execution_source_authority_or_no_change_disposition_candidate_after_blocked_execution_operator_review_markdown_v1(review)
    assert markdown.startswith("# MarketFlow Repository Integration Branch Retry Failure Remediation Execution Source Authority or No-Change Disposition Candidate After Blocked Execution Operator Review v1")
    for section in service.MARKDOWN_SECTIONS:
        assert f"## {section}" in markdown


def test_public_aliases_match_contract():
    assert service.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_CANDIDATE_AFTER_BLOCKED_EXECUTION_OPERATOR_REVIEW_V1 == service.ARTIFACT_KIND
    assert service.MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_CANDIDATE_AFTER_BLOCKED_EXECUTION_OPERATOR_REVIEW_READY == service.REVIEW_STATUS
    assert service.REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_CANDIDATE_AFTER_BLOCKED_EXECUTION_OPERATOR_REVIEW_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN == service.REVIEW_SCOPE
    assert service.MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_SOURCE_AUTHORITY_OR_NO_CHANGE_DISPOSITION_CANDIDATE_AFTER_BLOCKED_EXECUTION_OPERATOR_REVIEW_DIGEST_KEY == service.OPERATOR_REVIEW_DIGEST_KEY
