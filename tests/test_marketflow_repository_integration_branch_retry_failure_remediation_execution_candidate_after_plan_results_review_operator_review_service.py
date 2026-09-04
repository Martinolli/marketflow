from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import pytest

from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_remediation_execution_candidate_after_plan_results_review_operator_review_service
    as target,
)


def valid_review() -> dict:
    return target.build_marketflow_repository_integration_branch_retry_failure_remediation_execution_candidate_after_plan_results_review_operator_review_v1()


def assert_rejected(review: dict) -> None:
    with pytest.raises(
        target.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionCandidateAfterPlanResultsReviewOperatorReviewError
    ):
        target.validate_marketflow_repository_integration_branch_retry_failure_remediation_execution_candidate_after_plan_results_review_operator_review_v1(
            review
        )


def test_operator_review_builds_offline_without_source_builders_or_file_reads(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def forbidden(*args, **kwargs):
        raise AssertionError("operator review must not build sources or read receipt/output files")

    monkeypatch.setattr(
        target.source,
        "build_marketflow_repository_integration_branch_retry_failure_remediation_execution_candidate_after_plan_results_review_v1",
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
        ("source_candidate_commit", target.SOURCE_CANDIDATE_COMMIT),
        ("source_remediation_execution_candidate_after_plan_results_review_digest", target.SOURCE_CANDIDATE_DIGEST),
        ("source_plan_results_review_commit", target.source.SOURCE_PLAN_RESULTS_REVIEW_COMMIT),
        ("source_remediation_plan_or_execution_results_review_after_method_results_review_digest", target.source.SOURCE_PLAN_RESULTS_REVIEW_DIGEST),
        ("source_targeted_remediation_plan_review_digest", target.source.SOURCE_TARGETED_PLAN_REVIEW_DIGEST),
        ("source_workstream_mapping_review_digest", target.source.SOURCE_WORKSTREAM_MAPPING_REVIEW_DIGEST),
        ("source_plan_results_review_manifest_digest", target.source.SOURCE_PLAN_RESULTS_REVIEW_MANIFEST_DIGEST),
        ("source_plan_execution_commit", target.source.SOURCE_PLAN_EXECUTION_COMMIT),
        ("source_remediation_plan_or_execution_after_method_results_review_digest", target.source.SOURCE_PLAN_EXECUTION_DIGEST),
        ("source_targeted_remediation_plan_digest", target.source.SOURCE_TARGETED_REMEDIATION_PLAN_DIGEST),
        ("source_workstream_mapping_digest", target.source.SOURCE_WORKSTREAM_MAPPING_DIGEST),
        ("source_plan_execution_manifest_digest", target.source.SOURCE_PLAN_EXECUTION_MANIFEST_DIGEST),
        ("selected_source_plan_package", target.source.SELECTED_SOURCE_PLAN_PACKAGE),
        ("recommended_remediation_execution_package", target.RECOMMENDED_PACKAGE),
        ("recommended_next_task", target.RECOMMENDED_NEXT_TASK),
    ],
)
def test_identity_source_candidate_plan_and_recommendation_fields(field: str, expected: object) -> None:
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


def test_four_observable_families_and_four_workstreams_are_reviewed() -> None:
    review = valid_review()
    families = review["reviewed_observable_failure_families"]
    assert [item["family_id"] for item in families] == target.source.source.FAMILY_IDS
    assert review["observable_failure_family_count"] == len(families) == 4
    assert review["total_observable_evidence_items"] == sum(item["observable_evidence_count"] for item in families) == 188
    assert all(item["observable_evidence_count"] == 47 and item["confidence"] == "HIGH" for item in families)
    assert review["source_workstream_count"] == len(review["reviewed_workstreams"]) == 4
    assert [item["source_family_id"] for item in review["reviewed_workstreams"]] == target.source.source.FAMILY_IDS
    assert review["additional_diagnostic_capture_may_be_needed"] is False
    assert review["direct_remediation_ready"] is False
    assert review["remediation_execution_ready"] is False
    assert review["retry_ready"] is False
    assert review["main_merge_ready"] is False


def test_twelve_packages_are_reviewed_and_remain_unselected() -> None:
    review = valid_review()
    packages = review["reviewed_remediation_execution_packages"]
    assert packages == target.REVIEWED_PACKAGES
    assert len(packages) == 12
    assert sum(item["review_status"] == "REVIEWED_BLOCKED_NOT_ALLOWED" for item in packages) == 5
    assert packages[0]["package_id"] == target.RECOMMENDED_PACKAGE
    assert packages[0]["review_status"] == "REVIEWED_RECOMMENDED_PACKAGE_FOR_OPERATOR_ASSESSMENT_NOT_SELECTED"
    assert all(item["selected"] is item["approved"] is item["authorized"] is item["executed"] is False for item in packages)
    assert review["recommendation_status"] == "REVIEWED_RECOMMENDED_FOR_OPERATOR_ASSESSMENT_NOT_SELECTED"


def test_requirements_plan_outputs_non_goals_chain_gates_and_controls_are_reviewed() -> None:
    review = valid_review()
    assert review["reviewed_future_remediation_execution_requirements"] == target.REVIEWED_FUTURE_REQUIREMENTS
    assert len(review["reviewed_future_remediation_execution_requirements"]) == 46
    assert all(item["review_status"] == "REVIEWED_REQUIRED_FOR_FUTURE_REMEDIATION_EXECUTION" and item["execution_status"] == "NOT_EXECUTED" for item in review["reviewed_future_remediation_execution_requirements"])
    assert review["reviewed_future_remediation_execution_plan"] == target.REVIEWED_FUTURE_PLAN
    assert len(review["reviewed_future_remediation_execution_plan"]) == 14
    assert all(item["review_status"] == "REVIEWED_PLANNED_NOT_EXECUTED" and item["execution_status"] == "NOT_EXECUTED" for item in review["reviewed_future_remediation_execution_plan"])
    assert review["reviewed_planned_outputs"] == target.REVIEWED_PLANNED_OUTPUTS
    assert len(review["reviewed_planned_outputs"]) == 20
    assert review["reviewed_non_goals"] == target.REVIEWED_NON_GOALS
    assert len(review["reviewed_non_goals"]) == 55
    assert review["next_chain"] == target.NEXT_CHAIN and len(review["next_chain"]) == 8
    assert review["next_gates"] == target.NEXT_GATES and len(review["next_gates"]) == 8
    assert review["risk_controls"] == target.RISK_CONTROLS and len(review["risk_controls"]) == 107


def test_reviewed_philosophy_recommendation_and_source_summaries_are_complete() -> None:
    review = valid_review()
    assert review["reviewed_candidate_philosophy"] == {
        "philosophy": target.REVIEWED_PHILOSOPHY,
        "reviewed_candidate_boundary": target.REVIEWED_CANDIDATE_BOUNDARY,
        "reviewed_candidate_goal": target.REVIEWED_CANDIDATE_GOAL,
        "review_status": "REVIEWED_PLANNING_ONLY",
    }
    assert review["recommendation"] == {
        "recommended_next_task": target.RECOMMENDED_NEXT_TASK,
        "recommended_next_task_status": "FUTURE_APPROVAL_NOT_CREATED",
        "recommended_action": "OPTIONAL_OPERATOR_SELECTION_AND_APPROVAL_REQUIRED_BEFORE_ANY_REMEDIATION_EXECUTION",
        "reason": target.NEXT_TASK_REASON,
    }
    for field in (
        "source_candidate_summary", "source_plan_results_review_summary", "source_plan_execution_summary",
        "source_targeted_remediation_plan_summary", "source_workstream_mapping_summary", "source_approval_summary",
        "source_operator_review_and_candidate_summary", "source_method_results_review_summary",
        "source_method_execution_summary", "source_failure_family_classification_summary",
        "source_diagnostic_results_review_summary", "source_controlled_recapture_execution_summary",
        "source_durable_receipt_summary", "source_receipt_loss_history_summary",
        "source_planning_and_detail_binding_summary",
    ):
        assert review[field]


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


def test_checklist_and_summary_pass() -> None:
    review = valid_review()
    assert set(target.REQUIRED_CHECK_IDS) <= {item["check_id"] for item in review["checklist"]}
    assert all(item["status"] == "PASS" and item["severity"] == "BLOCKER" for item in review["checklist"])
    assert all(set(item) == {"check_id", "status", "expected", "actual", "severity", "message"} for item in review["checklist"])
    assert review["summary"]["total_checks"] == review["summary"]["passed_checks"] == len(review["checklist"])
    assert review["summary"]["failed_checks"] == review["summary"]["blocker_count"] == 0


def test_operator_review_digest_is_deterministic() -> None:
    first, second = valid_review(), valid_review()
    assert first[target.OPERATOR_REVIEW_DIGEST_KEY] == second[target.OPERATOR_REVIEW_DIGEST_KEY]


def test_validator_accepts_valid_review() -> None:
    review = valid_review()
    result = target.validate_marketflow_repository_integration_branch_retry_failure_remediation_execution_candidate_after_plan_results_review_operator_review_v1(review)
    assert result["operator_review_digest"] == review[target.OPERATOR_REVIEW_DIGEST_KEY]
    assert result["failed_checks"] == result["blocker_count"] == 0


@pytest.mark.parametrize("field", list(target._core()))
def test_validator_rejects_changed_or_missing_required_core_field(field: str) -> None:
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


def test_validator_rejects_missing_counts_priority_paths_family_workstream_and_package() -> None:
    mutations = [
        lambda review: review["retry_failure_context"].update(counts={}),
        lambda review: review.update(priority_1_target_modules=[]),
        lambda review: review["reviewed_observable_failure_families"].pop(),
        lambda review: review["reviewed_workstreams"].pop(),
        lambda review: review["reviewed_remediation_execution_packages"].pop(),
        lambda review: review["reviewed_remediation_execution_packages"][0].update(selected=True),
    ]
    for mutate in mutations:
        review = valid_review()
        mutate(review)
        assert_rejected(review)


def test_validator_rejects_missing_or_changed_digest() -> None:
    review = valid_review()
    review.pop(target.OPERATOR_REVIEW_DIGEST_KEY)
    assert_rejected(review)
    review = valid_review()
    review[target.OPERATOR_REVIEW_DIGEST_KEY] = "changed"
    assert_rejected(review)


def test_invalid_supplied_source_candidate_is_rejected() -> None:
    with pytest.raises(
        target.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionCandidateAfterPlanResultsReviewOperatorReviewError
    ):
        target.build_marketflow_repository_integration_branch_retry_failure_remediation_execution_candidate_after_plan_results_review_operator_review_v1(
            source_candidate={}
        )


def test_writer_writes_only_status_markdown_and_refuses_overwrite(tmp_path: Path) -> None:
    review = target.write_marketflow_repository_integration_branch_retry_failure_remediation_execution_candidate_after_plan_results_review_operator_review_v1(tmp_path)
    assert review["artifact_kind"] == target.ARTIFACT_KIND
    assert [path.name for path in tmp_path.iterdir()] == [
        "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_CANDIDATE_AFTER_PLAN_RESULTS_REVIEW_OPERATOR_REVIEW_STATUS.md"
    ]
    with pytest.raises(
        target.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionCandidateAfterPlanResultsReviewOperatorReviewError
    ):
        target.write_marketflow_repository_integration_branch_retry_failure_remediation_execution_candidate_after_plan_results_review_operator_review_v1(tmp_path)


@pytest.mark.parametrize("path", [Path(".marketflow"), Path(".pytest_cache"), Path(".env")])
def test_writer_refuses_protected_output(path: Path) -> None:
    with pytest.raises(
        target.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionCandidateAfterPlanResultsReviewOperatorReviewError
    ):
        target.write_marketflow_repository_integration_branch_retry_failure_remediation_execution_candidate_after_plan_results_review_operator_review_v1(path)


def test_markdown_contains_required_sections() -> None:
    markdown = target.build_marketflow_repository_integration_branch_retry_failure_remediation_execution_candidate_after_plan_results_review_operator_review_markdown_v1(valid_review())
    required = [
        "# MarketFlow Repository Integration Branch Retry Failure Remediation Execution Candidate After Plan Results Review Operator Review v1",
        "## Source Candidate", "## Source Plan Results Review", "## Source Plan Execution",
        "## Source Targeted Remediation Plan", "## Source Workstream Mapping", "## Source Approval",
        "## Source Operator Review and Candidate", "## Source Method Results Review", "## Source Method Execution",
        "## Source Failure-Family Classification", "## Source Diagnostic Results Review",
        "## Source Controlled Recapture Execution", "## Source Durable Receipt", "## Source Receipt Loss History",
        "## Source Planning and Detail Binding Evidence", "## Retry Failure Context", "## Review Scope",
        "## Priority 1 Target Modules", "## Diagnostic Capture Evidence Summary",
        "## Reviewed Observable Failure Families", "## Reviewed Workstreams", "## Reviewed Candidate Philosophy",
        "## Reviewed Remediation Execution Packages", "## Recommended Package",
        "## Reviewed Future Remediation Execution Requirements", "## Reviewed Future Remediation Execution Plan",
        "## Reviewed Planned Outputs", "## Reviewed Non-Goals", "## Recommendation", "## Next Chain",
        "## Next Gates", "## Risk Controls", "## Authority Boundaries", "## Checklist Summary", "## Guardrails",
    ]
    assert all(item in markdown for item in required)
