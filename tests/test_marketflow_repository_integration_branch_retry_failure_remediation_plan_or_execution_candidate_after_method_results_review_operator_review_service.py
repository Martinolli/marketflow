from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import pytest

from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_candidate_after_method_results_review_operator_review_service
    as target,
)


def valid_review() -> dict:
    return target.build_marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_candidate_after_method_results_review_operator_review_v1()


def assert_rejected(review: dict) -> None:
    with pytest.raises(
        target.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationPlanOrExecutionCandidateAfterMethodResultsReviewOperatorReviewError
    ):
        target.validate_marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_candidate_after_method_results_review_operator_review_v1(
            review
        )


def test_operator_review_builds_offline_without_source_builders_or_file_reads(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def forbidden(*args, **kwargs):
        raise AssertionError("operator review must not build sources or read receipt/output files")

    monkeypatch.setattr(
        target.source,
        "build_marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_candidate_after_method_results_review_v1",
        forbidden,
    )
    monkeypatch.setattr(Path, "read_text", forbidden)
    monkeypatch.setattr(Path, "read_bytes", forbidden)
    review = valid_review()
    assert review["created_offline"] is True
    assert review["governance_only"] is True
    assert review["operator_review_only"] is True


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("artifact_kind", target.ARTIFACT_KIND),
        ("schema_version", target.SCHEMA_VERSION),
        ("review_status", target.REVIEW_STATUS),
        ("review_scope", target.REVIEW_SCOPE),
        ("source_candidate_artifact_kind", target.source.ARTIFACT_KIND),
        ("source_candidate_status", target.source.CANDIDATE_STATUS),
        ("source_candidate_scope", target.source.CANDIDATE_SCOPE),
        (
            "source_remediation_plan_or_execution_candidate_after_method_results_review_digest",
            target.SOURCE_CANDIDATE_DIGEST,
        ),
        ("recommended_remediation_plan_or_execution_package", target.RECOMMENDED_PACKAGE),
        ("selected_source_method_package", target.source.source.SELECTED_PACKAGE),
        ("recommended_next_task", target.RECOMMENDED_NEXT_TASK),
    ],
)
def test_identity_source_candidate_and_recommendation_fields(field: str, expected: object) -> None:
    assert valid_review()[field] == expected


@pytest.mark.parametrize("field", list(target._source_bindings()))
def test_all_source_digest_and_evidence_bindings_are_exact(field: str) -> None:
    assert valid_review()[field] == target._source_bindings()[field]


def test_retry_failure_counts_priority_modules_and_diagnostic_evidence_are_bound() -> None:
    review = valid_review()
    assert review["retry_failure_context"] == {
        "counts": {"passed": 24877, "failed": 1292, "errors": 112, "skipped": 7},
        "first_result_authoritative": True,
        "pytest_passed": False,
        "pytest_failed": True,
        "root_full_regression_is_retry_evidence": False,
    }
    assert [item["module_path"] for item in review["priority_1_target_modules"]] == [
        "tests/test_marketflow_signal_or_feature_generation_results_review_service.py",
        "tests/test_post_identity_freeze_registry_inventory_approval_service.py",
        "tests/test_corporate_action_authority_plan_candidate_service.py",
        "tests/test_feature_generation_results_review_redesigned_labels_service.py",
        "tests/test_marketflow_objective_label_or_target_generation_results_review_service.py",
    ]
    assert [item["failed_or_errored_nodeid_count"] for item in review["priority_1_target_modules"]] == [136, 131, 122, 112, 111]
    assert (review["priority_1_total_nodeids"], review["top_10_count_sum"]) == (612, 1069)
    assert (review["module_summary_module_count"], review["failed_or_errored_nodeids_count"]) == (29, 1404)
    assert (review["source_exit_code"], review["source_exit_code_is_diagnostic_only"]) == (1, True)
    assert (review["source_stdout_byte_count"], review["source_stderr_byte_count"]) == (1231380, 0)
    assert review["source_stdout_sha256"] == "b5fb29f6cf8af77700da74c72f08b854c33bc1ad30c79c309c6eefee70171d2a"
    assert review["source_stderr_sha256"] == "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    assert review["source_stdout_excerpt_truncated"] is True
    assert review["source_stderr_excerpt_truncated"] is False
    assert review["source_redaction_checked"] is True


def test_four_observable_families_and_classification_summary_are_reviewed() -> None:
    review = valid_review()
    families = review["reviewed_observable_failure_families"]
    assert [item["family_id"] for item in families] == target.source.source.FAMILY_IDS
    assert review["observable_failure_family_count"] == len(families) == 4
    assert review["total_observable_evidence_items"] == sum(item["observable_evidence_count"] for item in families) == 188
    assert review["highest_confidence_family_ids"] == target.source.source.FAMILY_IDS
    assert all(item["observable_evidence_count"] == 47 and item["confidence"] == "HIGH" for item in families)
    assert review["additional_diagnostic_capture_may_be_needed"] is False
    assert review["direct_remediation_ready"] is False
    assert review["retry_ready"] is False
    assert review["main_merge_ready"] is False


def test_twelve_packages_are_reviewed_and_remain_unselected() -> None:
    review = valid_review()
    packages = review["reviewed_remediation_plan_or_execution_packages"]
    assert packages == target.REVIEWED_PACKAGES
    assert len(packages) == 12
    assert sum(item["review_status"] == "REVIEWED_BLOCKED_NOT_ALLOWED" for item in packages) == 6
    assert packages[0]["package_id"] == target.RECOMMENDED_PACKAGE
    assert packages[0]["review_status"] == "REVIEWED_RECOMMENDED_PACKAGE_FOR_OPERATOR_ASSESSMENT_NOT_SELECTED"
    assert all(item["selected"] is item["approved"] is item["authorized"] is item["executed"] is False for item in packages)
    assert review["recommendation_status"] == "REVIEWED_RECOMMENDED_FOR_OPERATOR_ASSESSMENT_NOT_SELECTED"


def test_requirements_plan_outputs_non_goals_chain_gates_and_controls_are_reviewed() -> None:
    review = valid_review()
    assert review["reviewed_future_remediation_requirements"] == target.REVIEWED_FUTURE_REQUIREMENTS
    assert len(review["reviewed_future_remediation_requirements"]) == 40
    assert all(item["review_status"] == "REVIEWED_REQUIRED_FOR_FUTURE_REMEDIATION_PLAN_OR_EXECUTION" for item in review["reviewed_future_remediation_requirements"])
    assert all(item["execution_status"] == "NOT_EXECUTED" for item in review["reviewed_future_remediation_requirements"])
    assert review["reviewed_future_remediation_plan"] == target.REVIEWED_FUTURE_PLAN
    assert len(review["reviewed_future_remediation_plan"]) == 12
    assert all(item["review_status"] == "REVIEWED_PLANNED_NOT_EXECUTED" and item["execution_status"] == "NOT_EXECUTED" for item in review["reviewed_future_remediation_plan"])
    assert review["reviewed_planned_outputs"] == target.REVIEWED_PLANNED_OUTPUTS
    assert len(review["reviewed_planned_outputs"]) == 17
    assert all(item["review_status"] == "REVIEWED_PLANNED_NOT_GENERATED" and item["generation_status"] == "NOT_GENERATED" for item in review["reviewed_planned_outputs"])
    assert review["reviewed_non_goals"] == target.REVIEWED_NON_GOALS
    assert len(review["reviewed_non_goals"]) == 50
    assert all(item["review_status"] == "REVIEWED_ACTIVE" for item in review["reviewed_non_goals"])
    assert review["next_chain"] == target.NEXT_CHAIN and len(review["next_chain"]) == 8
    assert review["next_gates"] == target.NEXT_GATES and len(review["next_gates"]) == 8
    assert review["risk_controls"] == target.RISK_CONTROLS and len(review["risk_controls"]) == 96


def test_reviewed_philosophy_and_recommendation_preserve_plan_first_boundary() -> None:
    review = valid_review()
    assert review["reviewed_remediation_plan_or_execution_candidate_after_method_results_review_philosophy"] == target.REVIEWED_PHILOSOPHY
    assert review["reviewed_candidate_philosophy"] == {
        "philosophy": target.REVIEWED_PHILOSOPHY,
        "reviewed_candidate_boundary": target.REVIEWED_CANDIDATE_BOUNDARY,
        "reviewed_candidate_goal": target.REVIEWED_CANDIDATE_GOAL,
        "review_status": "REVIEWED_PLANNING_ONLY",
    }
    assert review["recommendation"] == {
        "recommended_next_task": target.RECOMMENDED_NEXT_TASK,
        "recommended_next_task_status": "FUTURE_APPROVAL_NOT_CREATED",
        "recommended_action": "OPTIONAL_OPERATOR_SELECTION_AND_APPROVAL_REQUIRED_BEFORE_ANY_REMEDIATION_PLAN_OR_EXECUTION",
        "reason": target.NEXT_TASK_REASON,
    }


@pytest.mark.parametrize("field", target.TRUE_FIELDS)
def test_required_review_fact_true(field: str) -> None:
    assert valid_review()[field] is True


@pytest.mark.parametrize("field", target.FALSE_FIELDS)
def test_closed_authority_boundary_false(field: str) -> None:
    assert valid_review()[field] is False


def test_predictive_profitability_runtime_strategy_and_trading_stay_closed() -> None:
    review = valid_review()
    assert review["predictive_usefulness"] == review["profitability"] == "not accepted"
    assert review["runtime_use"] == review["strategy_use"] == "NOT_AUTHORIZED"
    assert review["paper_trading"] == review["broker_execution"] == "NOT_AUTHORIZED"


def test_checklist_and_summary_pass_with_exact_totals() -> None:
    review = valid_review()
    assert len(review["checklist"]) == 155
    assert all(item["status"] == "PASS" and item["severity"] == "BLOCKER" for item in review["checklist"])
    assert all(set(item) == {"check_id", "status", "expected", "actual", "severity", "message"} for item in review["checklist"])
    assert review["summary"]["total_checks"] == review["summary"]["passed_checks"] == 155
    assert review["summary"]["failed_checks"] == review["summary"]["blocker_count"] == 0


def test_operator_review_digest_is_deterministic() -> None:
    first, second = valid_review(), valid_review()
    assert first[target.OPERATOR_REVIEW_DIGEST_KEY] == second[target.OPERATOR_REVIEW_DIGEST_KEY]


def test_validator_accepts_valid_review() -> None:
    review = valid_review()
    result = target.validate_marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_candidate_after_method_results_review_operator_review_v1(review)
    assert result["operator_review_digest"] == review[target.OPERATOR_REVIEW_DIGEST_KEY]
    assert result["failed_checks"] == result["blocker_count"] == 0


@pytest.mark.parametrize(
    "field",
    [
        "artifact_kind", "review_status", "review_scope",
        "source_remediation_plan_or_execution_candidate_after_method_results_review_digest",
        "source_method_results_review_commit",
        "source_remediation_or_method_results_review_after_diagnostic_capture_digest",
        "source_failure_family_classification_review_digest",
        "source_bounded_excerpt_analysis_review_digest", "source_results_review_manifest_digest",
        "source_method_execution_commit", "source_remediation_or_method_execution_after_diagnostic_capture_digest",
        "source_failure_family_classification_digest", "source_bounded_excerpt_analysis_digest",
        "source_method_execution_manifest_digest", "recommended_remediation_plan_or_execution_package",
        "source_remediation_or_method_approval_after_diagnostic_capture_digest",
        "source_remediation_or_method_candidate_after_diagnostic_capture_operator_review_digest",
        "source_remediation_or_method_candidate_after_diagnostic_capture_digest",
        "source_receipt_recovery_or_recapture_results_review_digest",
        "source_receipt_recovery_or_recapture_payload_review_digest",
        "source_receipt_recovery_or_recapture_durable_receipt_review_digest",
        "source_receipt_recovery_or_recapture_results_review_manifest_digest",
        "source_receipt_recovery_or_recapture_execution_commit",
        "source_receipt_recovery_or_recapture_execution_digest",
        "source_receipt_recovery_or_recapture_payload_digest",
        "source_receipt_recovery_or_recapture_receipt_digest",
        "source_receipt_recovery_or_recapture_digest_manifest_digest", "source_durable_receipt_path",
        "source_receipt_recovery_or_recapture_approval_digest",
        "source_receipt_recovery_or_recapture_candidate_operator_review_digest",
        "source_receipt_recovery_or_recapture_candidate_digest",
        "source_targeted_diagnostic_output_capture_execution_failure_diagnosis_digest",
        "source_targeted_diagnostic_output_capture_execution_digest",
        "source_targeted_diagnostic_output_capture_execution_blocked_manifest_digest",
        "source_targeted_diagnostic_output_capture_execution_blocked_reason", "source_primary_failure_class",
        "source_secondary_failure_class", "source_targeted_diagnostic_output_capture_approval_digest",
        "source_targeted_diagnostic_output_capture_candidate_operator_review_digest",
        "source_targeted_diagnostic_output_capture_candidate_digest", "source_planning_results_review_digest",
        "source_prioritized_planning_review_digest", "source_planning_execution_digest",
        "source_prioritized_planning_digest", "source_detail_binding_results_review_digest",
        "source_complete_29_row_binding_digest", "source_materialized_payload_digest",
        "source_recovery_results_review_digest", "source_recovery_detail_digest",
        "source_after_v2_approval_digest", "source_module_grouping_digest", "retry_execution_commit",
        "priority_1_total_nodeids", "top_10_count_sum", "module_summary_module_count",
        "failed_or_errored_nodeids_count", "source_exit_code", "source_stdout_sha256",
        "source_stderr_sha256", "source_stdout_byte_count", "source_stderr_byte_count",
        "reviewed_remediation_plan_or_execution_packages", "reviewed_future_remediation_requirements",
        "reviewed_future_remediation_plan", "reviewed_planned_outputs", "reviewed_non_goals",
        "recommendation", "next_chain", "next_gates", "risk_controls",
    ],
)
def test_validator_rejects_changed_or_missing_required_field(field: str) -> None:
    review = valid_review()
    review[field] = "changed"
    assert_rejected(review)
    review = valid_review()
    review.pop(field)
    assert_rejected(review)


@pytest.mark.parametrize("field", target.TRUE_FIELDS)
def test_validator_rejects_required_true_fact_set_false(field: str) -> None:
    review = valid_review()
    review[field] = False
    assert_rejected(review)


@pytest.mark.parametrize("field", target.FALSE_FIELDS)
def test_validator_rejects_opened_boundary(field: str) -> None:
    review = valid_review()
    review[field] = True
    assert_rejected(review)


@pytest.mark.parametrize(
    ("field", "value"),
    [("predictive_usefulness", "accepted"), ("profitability", "accepted"), ("runtime_use", "AUTHORIZED"), ("broker_execution", "AUTHORIZED")],
)
def test_validator_rejects_opened_string_authority(field: str, value: str) -> None:
    review = valid_review()
    review[field] = value
    assert_rejected(review)


def test_validator_rejects_missing_retry_counts_and_priority_paths() -> None:
    review = valid_review()
    review["retry_failure_context"]["counts"] = {}
    assert_rejected(review)
    review = valid_review()
    review["priority_1_target_modules"] = []
    assert_rejected(review)


def test_validator_rejects_missing_family_changed_confidence_and_wrong_totals() -> None:
    review = valid_review()
    review["reviewed_observable_failure_families"].pop()
    assert_rejected(review)
    review = valid_review()
    review["reviewed_observable_failure_families"][0]["confidence"] = "LOW"
    assert_rejected(review)
    for field in ("observable_failure_family_count", "total_observable_evidence_items"):
        review = valid_review()
        review[field] = 0
        assert_rejected(review)


def test_validator_rejects_changed_package_review_and_selection() -> None:
    review = valid_review()
    review["reviewed_remediation_plan_or_execution_packages"].pop()
    assert_rejected(review)
    review = valid_review()
    review["reviewed_remediation_plan_or_execution_packages"][0]["selected"] = True
    assert_rejected(review)


def test_valid_and_invalid_supplied_source_candidate() -> None:
    candidate = target.source.build_marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_candidate_after_method_results_review_v1()
    review = target.build_marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_candidate_after_method_results_review_operator_review_v1(
        source_candidate=deepcopy(candidate)
    )
    assert review["source_candidate_reviewed"] is True
    with pytest.raises(
        target.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationPlanOrExecutionCandidateAfterMethodResultsReviewOperatorReviewError
    ):
        target.build_marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_candidate_after_method_results_review_operator_review_v1(
            source_candidate={}
        )


def test_writer_writes_only_status_markdown_and_refuses_overwrite(tmp_path: Path) -> None:
    review = target.write_marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_candidate_after_method_results_review_operator_review_v1(tmp_path)
    assert review["artifact_kind"] == target.ARTIFACT_KIND
    assert [path.name for path in tmp_path.iterdir()] == [
        "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_PLAN_OR_EXECUTION_CANDIDATE_AFTER_METHOD_RESULTS_REVIEW_OPERATOR_REVIEW_STATUS.md"
    ]
    with pytest.raises(
        target.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationPlanOrExecutionCandidateAfterMethodResultsReviewOperatorReviewError
    ):
        target.write_marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_candidate_after_method_results_review_operator_review_v1(tmp_path)


@pytest.mark.parametrize("path", [Path(".marketflow"), Path(".pytest_cache")])
def test_writer_refuses_protected_output(path: Path) -> None:
    with pytest.raises(
        target.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationPlanOrExecutionCandidateAfterMethodResultsReviewOperatorReviewError
    ):
        target.write_marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_candidate_after_method_results_review_operator_review_v1(path)


def test_markdown_contains_required_sections() -> None:
    markdown = target.build_marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_candidate_after_method_results_review_operator_review_markdown_v1(valid_review())
    required = [
        "# MarketFlow Repository Integration Branch Retry Failure Remediation Plan or Execution Candidate After Method Results Review Operator Review v1",
        "## Source Candidate", "## Source Method Results Review", "## Source Method Execution",
        "## Source Failure-Family Classification", "## Source Bounded Excerpt Analysis",
        "## Source Diagnostic Results Review", "## Source Controlled Recapture Execution",
        "## Source Durable Receipt", "## Source Receipt Loss History",
        "## Source Planning and Detail Binding Evidence", "## Retry Failure Context", "## Review Scope",
        "## Priority 1 Target Modules", "## Diagnostic Capture Evidence Summary",
        "## Reviewed Observable Failure Families", "## Reviewed Candidate Philosophy",
        "## Reviewed Remediation Plan or Execution Packages", "## Recommended Package",
        "## Reviewed Future Remediation Requirements", "## Reviewed Future Remediation Plan",
        "## Reviewed Planned Outputs", "## Reviewed Non-Goals", "## Recommendation",
        "## Next Chain", "## Next Gates", "## Risk Controls", "## Authority Boundaries",
        "## Checklist Summary", "## Guardrails",
    ]
    assert all(item in markdown for item in required)
