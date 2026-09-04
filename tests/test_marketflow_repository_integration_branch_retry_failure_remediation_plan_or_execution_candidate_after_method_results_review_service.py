from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import pytest

from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_candidate_after_method_results_review_service
    as target,
)


def valid_candidate() -> dict:
    return target.build_marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_candidate_after_method_results_review_v1()


def assert_rejected(candidate: dict) -> None:
    with pytest.raises(
        target.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationPlanOrExecutionCandidateAfterMethodResultsReviewError
    ):
        target.validate_marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_candidate_after_method_results_review_v1(
            candidate
        )


def test_candidate_builds_offline_without_source_builders_or_file_reads(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def forbidden(*args, **kwargs):
        raise AssertionError("candidate must not execute a source or read receipt/output files")

    monkeypatch.setattr(
        target.source,
        "build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_results_review_after_diagnostic_capture_v1",
        forbidden,
    )
    monkeypatch.setattr(Path, "read_text", forbidden)
    monkeypatch.setattr(Path, "read_bytes", forbidden)
    candidate = valid_candidate()
    assert candidate["created_offline"] is True
    assert candidate["governance_only"] is True
    assert candidate["candidate_only"] is True


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("artifact_kind", target.ARTIFACT_KIND),
        ("schema_version", target.SCHEMA_VERSION),
        ("candidate_status", target.CANDIDATE_STATUS),
        ("candidate_scope", target.CANDIDATE_SCOPE),
        ("source_method_results_review_artifact_kind", target.source.ARTIFACT_KIND),
        ("source_method_results_review_status", target.source.REVIEW_STATUS),
        ("source_method_results_review_scope", target.source.REVIEW_SCOPE),
        ("source_method_results_review_commit", target.SOURCE_RESULTS_REVIEW_COMMIT),
        (
            "source_remediation_or_method_results_review_after_diagnostic_capture_digest",
            target.SOURCE_RESULTS_REVIEW_DIGEST,
        ),
        ("source_failure_family_classification_review_digest", target.SOURCE_CLASSIFICATION_REVIEW_DIGEST),
        ("source_bounded_excerpt_analysis_review_digest", target.SOURCE_BOUNDED_REVIEW_DIGEST),
        ("source_results_review_manifest_digest", target.SOURCE_RESULTS_REVIEW_MANIFEST_DIGEST),
        ("source_method_execution_commit", target.source.SOURCE_EXECUTION_COMMIT),
        ("source_method_execution_manifest_digest", target.source.SOURCE_EXECUTION_MANIFEST_DIGEST),
        ("selected_source_method_package", target.source.SELECTED_PACKAGE),
        ("recommended_remediation_plan_or_execution_package", target.RECOMMENDED_PACKAGE),
        ("recommended_next_task", target.RECOMMENDED_NEXT_TASK),
    ],
)
def test_identity_source_and_recommendation_fields(field: str, expected: object) -> None:
    assert valid_candidate()[field] == expected


@pytest.mark.parametrize("field", list(target._source_bindings()))
def test_all_source_digest_and_evidence_bindings_are_exact(field: str) -> None:
    assert valid_candidate()[field] == target._source_bindings()[field]


def test_retry_failure_counts_priority_modules_and_diagnostic_evidence_are_bound() -> None:
    candidate = valid_candidate()
    assert candidate["retry_execution_commit"] == target.source.source.approval_source.source.RETRY_EXECUTION_COMMIT
    assert candidate["retry_failure_context"] == {
        "counts": {"passed": 24877, "failed": 1292, "errors": 112, "skipped": 7},
        "first_result_authoritative": True,
        "pytest_passed": False,
        "pytest_failed": True,
        "root_full_regression_is_retry_evidence": False,
    }
    assert [item["module_path"] for item in candidate["priority_1_target_modules"]] == [
        "tests/test_marketflow_signal_or_feature_generation_results_review_service.py",
        "tests/test_post_identity_freeze_registry_inventory_approval_service.py",
        "tests/test_corporate_action_authority_plan_candidate_service.py",
        "tests/test_feature_generation_results_review_redesigned_labels_service.py",
        "tests/test_marketflow_objective_label_or_target_generation_results_review_service.py",
    ]
    assert [item["failed_or_errored_nodeid_count"] for item in candidate["priority_1_target_modules"]] == [
        136,
        131,
        122,
        112,
        111,
    ]
    assert (candidate["priority_1_total_nodeids"], candidate["top_10_count_sum"]) == (612, 1069)
    assert (candidate["module_summary_module_count"], candidate["failed_or_errored_nodeids_count"]) == (29, 1404)
    assert (candidate["source_exit_code"], candidate["source_exit_code_is_diagnostic_only"]) == (1, True)
    assert (candidate["source_stdout_byte_count"], candidate["source_stderr_byte_count"]) == (1231380, 0)
    assert candidate["source_combined_output_byte_count"] == 1231380
    assert candidate["source_stdout_sha256"] == "b5fb29f6cf8af77700da74c72f08b854c33bc1ad30c79c309c6eefee70171d2a"
    assert candidate["source_stderr_sha256"] == "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    assert candidate["source_stdout_excerpt_truncated"] is True
    assert candidate["source_stderr_excerpt_truncated"] is False
    assert candidate["source_redaction_checked"] is True


def test_reviewed_observable_families_and_classification_summary_are_bound() -> None:
    candidate = valid_candidate()
    families = candidate["reviewed_observable_failure_families"]
    assert [item["family_id"] for item in families] == target.source.FAMILY_IDS
    assert candidate["observable_failure_family_count"] == len(families) == 4
    assert candidate["total_observable_evidence_items"] == sum(
        item["observable_evidence_count"] for item in families
    ) == 188
    assert candidate["highest_confidence_family_ids"] == target.source.FAMILY_IDS
    assert all(item["observable_evidence_count"] == 47 for item in families)
    assert all(item["confidence"] == "HIGH" for item in families)
    assert candidate["additional_diagnostic_capture_may_be_needed"] is False
    assert candidate["direct_remediation_ready"] is False
    assert candidate["retry_ready"] is False
    assert candidate["main_merge_ready"] is False


def test_candidate_packages_are_reviewable_plan_first_and_unselected() -> None:
    candidate = valid_candidate()
    packages = candidate["proposed_remediation_plan_or_execution_packages"]
    assert packages == target.PROPOSED_PACKAGES
    assert len(packages) == 12
    assert sum(item["status"] == "BLOCKED_NOT_ALLOWED" for item in packages) == 6
    assert packages[0]["package_id"] == target.RECOMMENDED_PACKAGE
    assert packages[0]["status"] == "RECOMMENDED_FOR_OPERATOR_REVIEW_NOT_SELECTED"
    assert all(item["selected"] is item["approved"] is item["authorized"] is item["executed"] is False for item in packages)
    assert candidate["recommended_package"] == packages[0]
    assert candidate["recommended_package_selected"] is False


def test_future_requirements_plan_outputs_non_goals_chain_gates_and_controls() -> None:
    candidate = valid_candidate()
    assert candidate["future_remediation_requirements"] == target.FUTURE_REQUIREMENTS
    assert len(candidate["future_remediation_requirements"]) == 40
    assert all(item["required"] is True for item in candidate["future_remediation_requirements"])
    assert all(item["status"] == "REQUIRED_FOR_FUTURE_REMEDIATION_PLAN_OR_EXECUTION" for item in candidate["future_remediation_requirements"])
    assert all(item["execution_status"] == "NOT_EXECUTED" for item in candidate["future_remediation_requirements"])
    assert candidate["future_remediation_plan"] == target.FUTURE_PLAN
    assert len(candidate["future_remediation_plan"]) == 12
    assert all(item["status"] == "PLANNED_NOT_EXECUTED" for item in candidate["future_remediation_plan"])
    assert candidate["planned_outputs"] == target.PLANNED_OUTPUTS
    assert len(candidate["planned_outputs"]) == 17
    assert all(item["status"] == "PLANNED_NOT_GENERATED" for item in candidate["planned_outputs"])
    assert candidate["non_goals"] == target.NON_GOALS
    assert len(candidate["non_goals"]) == 50
    assert candidate["next_chain"] == target.NEXT_CHAIN
    assert len(candidate["next_chain"]) == 9
    assert candidate["next_gates"] == target.NEXT_GATES
    assert len(candidate["next_gates"]) == 9
    assert candidate["risk_controls"] == target.RISK_CONTROLS
    assert len(candidate["risk_controls"]) == 96


@pytest.mark.parametrize("field", target.TRUE_FIELDS)
def test_required_candidate_fact_true(field: str) -> None:
    assert valid_candidate()[field] is True


@pytest.mark.parametrize("field", target.FALSE_FIELDS)
def test_closed_authority_boundary_false(field: str) -> None:
    assert valid_candidate()[field] is False


def test_predictive_profitability_runtime_strategy_and_trading_stay_closed() -> None:
    candidate = valid_candidate()
    assert candidate["predictive_usefulness"] == candidate["profitability"] == "not accepted"
    assert candidate["runtime_use"] == candidate["strategy_use"] == "NOT_AUTHORIZED"
    assert candidate["paper_trading"] == candidate["broker_execution"] == "NOT_AUTHORIZED"


def test_checklist_and_summary_pass_with_exact_totals() -> None:
    candidate = valid_candidate()
    assert len(candidate["checklist"]) == 154
    assert all(item["status"] == "PASS" and item["severity"] == "BLOCKER" for item in candidate["checklist"])
    assert all(set(item) == {"check_id", "status", "expected", "actual", "severity", "message"} for item in candidate["checklist"])
    assert candidate["summary"]["total_checks"] == candidate["summary"]["passed_checks"] == 154
    assert candidate["summary"]["failed_checks"] == candidate["summary"]["blocker_count"] == 0


def test_candidate_digest_is_deterministic() -> None:
    first = valid_candidate()
    second = valid_candidate()
    assert first[target.CANDIDATE_DIGEST_KEY] == second[target.CANDIDATE_DIGEST_KEY]


def test_validator_accepts_valid_candidate() -> None:
    candidate = valid_candidate()
    result = target.validate_marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_candidate_after_method_results_review_v1(
        candidate
    )
    assert result["candidate_digest"] == candidate[target.CANDIDATE_DIGEST_KEY]
    assert result["failed_checks"] == result["blocker_count"] == 0


@pytest.mark.parametrize(
    "field",
    [
        "artifact_kind",
        "candidate_status",
        "candidate_scope",
        "source_method_results_review_commit",
        "source_remediation_or_method_results_review_after_diagnostic_capture_digest",
        "source_failure_family_classification_review_digest",
        "source_bounded_excerpt_analysis_review_digest",
        "source_results_review_manifest_digest",
        "source_method_execution_commit",
        "source_remediation_or_method_execution_after_diagnostic_capture_digest",
        "source_failure_family_classification_digest",
        "source_bounded_excerpt_analysis_digest",
        "source_method_execution_manifest_digest",
        "recommended_remediation_plan_or_execution_package",
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
        "source_receipt_recovery_or_recapture_digest_manifest_digest",
        "source_durable_receipt_path",
        "source_receipt_recovery_or_recapture_approval_digest",
        "source_receipt_recovery_or_recapture_candidate_operator_review_digest",
        "source_receipt_recovery_or_recapture_candidate_digest",
        "source_targeted_diagnostic_output_capture_execution_failure_diagnosis_digest",
        "source_targeted_diagnostic_output_capture_execution_digest",
        "source_targeted_diagnostic_output_capture_execution_blocked_manifest_digest",
        "source_targeted_diagnostic_output_capture_execution_blocked_reason",
        "source_primary_failure_class",
        "source_secondary_failure_class",
        "source_targeted_diagnostic_output_capture_approval_digest",
        "source_targeted_diagnostic_output_capture_candidate_operator_review_digest",
        "source_targeted_diagnostic_output_capture_candidate_digest",
        "source_planning_results_review_digest",
        "source_prioritized_planning_review_digest",
        "source_planning_execution_digest",
        "source_prioritized_planning_digest",
        "source_detail_binding_results_review_digest",
        "source_complete_29_row_binding_digest",
        "source_materialized_payload_digest",
        "source_recovery_results_review_digest",
        "source_recovery_detail_digest",
        "source_after_v2_approval_digest",
        "source_module_grouping_digest",
        "retry_execution_commit",
        "priority_1_total_nodeids",
        "top_10_count_sum",
        "module_summary_module_count",
        "failed_or_errored_nodeids_count",
        "source_exit_code",
        "source_stdout_sha256",
        "source_stderr_sha256",
        "source_stdout_byte_count",
        "source_stderr_byte_count",
        "proposed_remediation_plan_or_execution_packages",
        "future_remediation_requirements",
        "future_remediation_plan",
        "planned_outputs",
        "non_goals",
        "next_chain",
        "next_gates",
        "risk_controls",
    ],
)
def test_validator_rejects_changed_or_missing_required_field(field: str) -> None:
    candidate = valid_candidate()
    candidate[field] = "changed"
    assert_rejected(candidate)
    candidate = valid_candidate()
    candidate.pop(field)
    assert_rejected(candidate)


@pytest.mark.parametrize("field", target.TRUE_FIELDS)
def test_validator_rejects_required_true_fact_set_false(field: str) -> None:
    candidate = valid_candidate()
    candidate[field] = False
    assert_rejected(candidate)


@pytest.mark.parametrize("field", target.FALSE_FIELDS)
def test_validator_rejects_opened_boundary(field: str) -> None:
    candidate = valid_candidate()
    candidate[field] = True
    assert_rejected(candidate)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("predictive_usefulness", "accepted"),
        ("profitability", "accepted"),
        ("runtime_use", "AUTHORIZED"),
        ("broker_execution", "AUTHORIZED"),
    ],
)
def test_validator_rejects_opened_string_authority(field: str, value: str) -> None:
    candidate = valid_candidate()
    candidate[field] = value
    assert_rejected(candidate)


def test_validator_rejects_missing_retry_counts_and_priority_paths() -> None:
    candidate = valid_candidate()
    candidate["retry_failure_context"]["counts"] = {}
    assert_rejected(candidate)
    candidate = valid_candidate()
    candidate["priority_1_target_modules"] = []
    assert_rejected(candidate)


@pytest.mark.parametrize("field", ["observable_failure_family_count", "total_observable_evidence_items"])
def test_validator_rejects_observable_family_summary_mismatch(field: str) -> None:
    candidate = valid_candidate()
    candidate[field] = 0
    assert_rejected(candidate)


def test_validator_rejects_missing_family_and_changed_confidence() -> None:
    candidate = valid_candidate()
    candidate["reviewed_observable_failure_families"].pop()
    assert_rejected(candidate)
    candidate = valid_candidate()
    candidate["reviewed_observable_failure_families"][0]["confidence"] = "LOW"
    assert_rejected(candidate)


def test_validator_rejects_recommended_package_selected() -> None:
    candidate = valid_candidate()
    candidate["recommended_package_selected"] = True
    assert_rejected(candidate)
    candidate = valid_candidate()
    candidate["recommended_package"]["selected"] = True
    assert_rejected(candidate)


def test_valid_and_invalid_supplied_source_results_review() -> None:
    source_review = target.source.build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_results_review_after_diagnostic_capture_v1()
    candidate = target.build_marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_candidate_after_method_results_review_v1(
        source_method_results_review=deepcopy(source_review)
    )
    assert candidate["source_method_results_review_commit"] == target.SOURCE_RESULTS_REVIEW_COMMIT
    with pytest.raises(
        target.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationPlanOrExecutionCandidateAfterMethodResultsReviewError
    ):
        target.build_marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_candidate_after_method_results_review_v1(
            source_method_results_review={}
        )


def test_writer_writes_only_status_markdown_and_refuses_overwrite(tmp_path: Path) -> None:
    candidate = target.write_marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_candidate_after_method_results_review_v1(
        tmp_path
    )
    assert candidate["artifact_kind"] == target.ARTIFACT_KIND
    assert [path.name for path in tmp_path.iterdir()] == [
        "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_PLAN_OR_EXECUTION_CANDIDATE_AFTER_METHOD_RESULTS_REVIEW_STATUS.md"
    ]
    with pytest.raises(
        target.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationPlanOrExecutionCandidateAfterMethodResultsReviewError
    ):
        target.write_marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_candidate_after_method_results_review_v1(
            tmp_path
        )


@pytest.mark.parametrize("path", [Path(".marketflow"), Path(".pytest_cache")])
def test_writer_refuses_protected_output(path: Path) -> None:
    with pytest.raises(
        target.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationPlanOrExecutionCandidateAfterMethodResultsReviewError
    ):
        target.write_marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_candidate_after_method_results_review_v1(
            path
        )


def test_markdown_contains_required_sections() -> None:
    markdown = target.build_marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_candidate_after_method_results_review_markdown_v1(
        valid_candidate()
    )
    required = [
        "# MarketFlow Repository Integration Branch Retry Failure Remediation Plan or Execution Candidate After Method Results Review v1",
        "## Source Method Results Review",
        "## Source Method Execution",
        "## Source Failure-Family Classification",
        "## Source Bounded Excerpt Analysis",
        "## Source Diagnostic Results Review",
        "## Source Controlled Recapture Execution",
        "## Source Durable Receipt",
        "## Source Receipt Loss History",
        "## Source Planning and Detail Binding Evidence",
        "## Retry Failure Context",
        "## Candidate Scope",
        "## Selected Source Method Package",
        "## Priority 1 Target Modules",
        "## Diagnostic Capture Evidence Summary",
        "## Reviewed Observable Failure Families",
        "## Candidate Philosophy",
        "## Proposed Remediation Plan or Execution Packages",
        "## Recommended Package",
        "## Future Remediation Requirements",
        "## Future Remediation Plan",
        "## Planned Outputs",
        "## Non-Goals",
        "## Next Chain",
        "## Next Gates",
        "## Risk Controls",
        "## Authority Boundaries",
        "## Checklist Summary",
        "## Guardrails",
    ]
    assert all(item in markdown for item in required)
