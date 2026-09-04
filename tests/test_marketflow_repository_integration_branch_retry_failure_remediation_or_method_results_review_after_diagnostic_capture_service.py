from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import pytest

from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_remediation_or_method_results_review_after_diagnostic_capture_service
    as target,
)


def valid_review() -> dict:
    return target.build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_results_review_after_diagnostic_capture_v1()


def assert_rejected(review: dict) -> None:
    with pytest.raises(
        target.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodResultsReviewAfterDiagnosticCaptureError
    ):
        target.validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_results_review_after_diagnostic_capture_v1(
            review
        )


def test_results_review_builds_offline_without_source_execution_or_file_reads(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def forbidden(*args, **kwargs):
        raise AssertionError("review must not execute sources or read receipt/output files")

    monkeypatch.setattr(
        target.source,
        "execute_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_diagnostic_capture_v1",
        forbidden,
    )
    monkeypatch.setattr(Path, "read_text", forbidden)
    monkeypatch.setattr(Path, "read_bytes", forbidden)
    review = valid_review()
    assert review["created_offline"] is True
    assert review["governance_only"] is True
    assert review["results_review_only"] is True


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("artifact_kind", target.ARTIFACT_KIND), ("schema_version", target.SCHEMA_VERSION),
        ("review_status", target.REVIEW_STATUS), ("review_scope", target.REVIEW_SCOPE),
        ("source_execution_artifact_kind", target.source.ARTIFACT_KIND_SUCCESS),
        ("source_execution_status", target.source.EXECUTION_STATUS_SUCCESS),
        ("source_execution_scope", target.source.EXECUTION_SCOPE),
        ("source_execution_commit", target.SOURCE_EXECUTION_COMMIT),
        ("source_remediation_or_method_execution_after_diagnostic_capture_digest", target.SOURCE_EXECUTION_DIGEST),
        ("source_failure_family_classification_digest", target.SOURCE_CLASSIFICATION_DIGEST),
        ("source_bounded_excerpt_analysis_digest", target.SOURCE_BOUNDED_ANALYSIS_DIGEST),
        ("source_execution_manifest_digest", target.SOURCE_EXECUTION_MANIFEST_DIGEST),
        ("selected_remediation_or_method_package", target.SELECTED_PACKAGE),
    ],
)
def test_core_and_source_execution_fields(field: str, expected: object) -> None:
    assert valid_review()[field] == expected


@pytest.mark.parametrize("field", list(target._source_bindings()))
def test_all_source_bindings_are_exact(field: str) -> None:
    assert valid_review()[field] == target._source_bindings()[field]


def test_retry_priority_and_diagnostic_facts_are_bound() -> None:
    review = valid_review()
    assert review["retry_failure_context"]["counts"] == {"passed": 24877, "failed": 1292, "errors": 112, "skipped": 7}
    assert review["retry_failure_context"]["first_result_authoritative"] is True
    assert review["retry_failure_context"]["root_full_regression_is_retry_evidence"] is False
    assert review["retry_execution_commit"] == target.source.approval_source.source.RETRY_EXECUTION_COMMIT
    assert [row["module_path"] for row in review["priority_1_target_modules"]] == [
        row["module_path"] for row in target.source.approval_source.source.PRIORITY_1_TARGET_MODULES
    ]
    assert (review["priority_1_total_nodeids"], review["top_10_count_sum"]) == (612, 1069)
    assert (review["module_summary_module_count"], review["failed_or_errored_nodeids_count"]) == (29, 1404)
    assert (review["source_exit_code"], review["source_exit_code_is_diagnostic_only"]) == (1, True)
    assert (review["source_stdout_byte_count"], review["source_stderr_byte_count"]) == (1231380, 0)
    assert review["source_stdout_excerpt_truncated"] is True
    assert review["source_stderr_excerpt_truncated"] is False
    assert review["source_redaction_checked"] is True


def test_source_method_execution_facts_are_reviewed_not_reperformed() -> None:
    review = valid_review()
    for field in (
        "source_method_execution_performed", "source_method_analysis_executed",
        "source_diagnostic_receipt_parsed", "source_diagnostic_output_analyzed",
        "source_bounded_excerpt_analyzed", "source_failure_family_classification_performed",
        "source_observable_failure_families_generated",
    ):
        assert review[field] is True
    assert review["method_execution_rerun_performed"] is False
    assert review["diagnostic_receipt_parsed_in_review"] is False
    assert review["diagnostic_output_analyzed_in_review"] is False
    assert review["failure_family_classification_performed_in_review"] is False


def test_four_observable_families_and_188_matches_are_reviewed() -> None:
    review = valid_review()
    families = review["observable_failure_families_review"]
    assert [item["family_id"] for item in families] == target.FAMILY_IDS
    assert review["observable_failure_family_count"] == len(families) == 4
    assert review["total_observable_evidence_items"] == sum(item["observable_evidence_count"] for item in families) == 188
    assert review["highest_confidence_family_ids"] == target.FAMILY_IDS
    assert all(item["observable_evidence_count"] == 47 and item["confidence"] == "HIGH" for item in families)
    assert all(item["required_fields_present"] and item["representative_snippets_bounded"] for item in families)
    assert all(item["root_cause_claimed"] is False for item in families)
    assert all(item["direct_remediation_recommended"] is False for item in families)
    assert all(item["retry_success_claimed"] is False for item in families)


def test_classification_summary_and_bounded_integrity_review() -> None:
    review = valid_review()
    summary = review["source_failure_family_classification_summary"]
    assert summary["total_families_detected"] == 4
    assert summary["total_observable_evidence_items"] == 188
    assert summary["additional_diagnostic_capture_may_be_needed"] is False
    assert summary["direct_remediation_ready"] is summary["retry_ready"] is summary["main_merge_ready"] is False
    bounded = review["bounded_excerpt_integrity_review"]
    assert bounded["source_bounded_stdout_excerpt_used"] is True
    assert bounded["source_bounded_stderr_excerpt_used"] is False
    assert bounded["source_stdout_excerpt_chars"] == 20000
    assert bounded["durable_receipt_parsed_in_review"] is False
    assert bounded["diagnostic_output_analyzed_in_review"] is False


@pytest.mark.parametrize("field", target.TRUE_FIELDS)
def test_required_review_fact_true(field: str) -> None:
    assert valid_review()[field] is True


@pytest.mark.parametrize("field", target.FALSE_FIELDS)
def test_closed_boundary_false(field: str) -> None:
    assert valid_review()[field] is False


def test_authority_strings_remain_closed() -> None:
    review = valid_review()
    assert review["predictive_usefulness"] == review["profitability"] == "not accepted"
    assert review["runtime_use"] == review["strategy_use"] == "NOT_AUTHORIZED"
    assert review["paper_trading"] == review["broker_execution"] == "NOT_AUTHORIZED"


def test_findings_outputs_recommendation_chain_gates_and_controls() -> None:
    review = valid_review()
    assert review["review_findings"] == target.REVIEW_FINDINGS
    assert len(review["review_findings"]) == 16
    assert review["review_outputs"] == target.REVIEW_OUTPUTS
    assert len(review["review_outputs"]) == 16
    assert all(item["status"] == "GENERATED_METHOD_RESULTS_REVIEW_ONLY" for item in review["review_outputs"])
    assert review["recommended_next_task"] == target.RECOMMENDED_NEXT_TASK
    assert review["recommended_next_task_status"] == "FUTURE_CANDIDATE_NOT_CREATED"
    assert review["next_chain"] == target.NEXT_CHAIN
    assert review["next_gates"] == target.NEXT_GATES
    assert review["risk_controls"] == target.RISK_CONTROLS


def test_checklist_and_summary_pass() -> None:
    review = valid_review()
    assert len(review["checklist"]) == 157
    assert all(item["status"] == "PASS" and item["severity"] == "BLOCKER" for item in review["checklist"])
    assert review["summary"]["passed_checks"] == review["summary"]["total_checks"] == 157
    assert review["summary"]["failed_checks"] == review["summary"]["blocker_count"] == 0


def test_all_four_review_digests_are_deterministic() -> None:
    first, second = valid_review(), valid_review()
    for field in (
        target.RESULTS_REVIEW_DIGEST_KEY, target.CLASSIFICATION_REVIEW_DIGEST_KEY,
        target.BOUNDED_ANALYSIS_REVIEW_DIGEST_KEY, target.MANIFEST_DIGEST_KEY,
    ):
        assert first[field] == second[field]


def test_validator_accepts_valid_review() -> None:
    result = target.validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_results_review_after_diagnostic_capture_v1(valid_review())
    assert result["failed_checks"] == result["blocker_count"] == 0
    assert result["results_review_digest"] == valid_review()[target.RESULTS_REVIEW_DIGEST_KEY]


@pytest.mark.parametrize(
    "field",
    [
        "artifact_kind", "schema_version", "review_status", "review_scope",
        "selected_remediation_or_method_package", "source_execution_commit",
        "source_remediation_or_method_execution_after_diagnostic_capture_digest",
        "source_failure_family_classification_digest", "source_bounded_excerpt_analysis_digest",
        "source_execution_manifest_digest", "source_remediation_or_method_approval_after_diagnostic_capture_digest",
        "source_remediation_or_method_candidate_after_diagnostic_capture_operator_review_digest",
        "source_remediation_or_method_candidate_after_diagnostic_capture_digest",
        "source_receipt_recovery_or_recapture_results_review_digest",
        "source_receipt_recovery_or_recapture_payload_review_digest",
        "source_receipt_recovery_or_recapture_durable_receipt_review_digest",
        "source_receipt_recovery_or_recapture_execution_digest",
        "source_receipt_recovery_or_recapture_payload_digest",
        "source_receipt_recovery_or_recapture_receipt_digest", "source_durable_receipt_path",
        "source_receipt_recovery_or_recapture_approval_digest",
        "source_targeted_diagnostic_output_capture_execution_failure_diagnosis_digest",
        "source_targeted_diagnostic_output_capture_execution_blocked_reason", "source_primary_failure_class",
        "source_targeted_diagnostic_output_capture_approval_digest", "source_planning_execution_digest",
        "source_complete_29_row_binding_digest", "source_materialized_payload_digest",
        "source_recovery_detail_digest", "source_module_grouping_digest", "retry_execution_commit",
        "priority_1_total_nodeids", "top_10_count_sum", "module_summary_module_count",
        "failed_or_errored_nodeids_count", "source_exit_code", "source_stdout_sha256",
        "source_stdout_byte_count", "review_findings", "review_outputs", "recommendation",
        "next_chain", "next_gates", "risk_controls",
    ],
)
def test_validator_rejects_changed_required_field(field: str) -> None:
    review = valid_review()
    review[field] = "changed"
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


def test_validator_rejects_missing_retry_counts_and_priority_paths() -> None:
    review = valid_review()
    review["retry_failure_context"]["counts"] = {}
    assert_rejected(review)
    review = valid_review()
    review["priority_1_target_modules"] = []
    assert_rejected(review)


@pytest.mark.parametrize(
    ("family_index", "field", "value"),
    [
        (0, "confidence", "LOW"), (0, "root_cause_claimed", True),
        (1, "direct_remediation_recommended", True), (2, "retry_success_claimed", True),
        (3, "representative_snippets_bounded", False),
    ],
)
def test_validator_rejects_family_boundary_change(family_index: int, field: str, value: object) -> None:
    review = valid_review()
    review["observable_failure_families_review"][family_index][field] = value
    assert_rejected(review)


def test_validator_rejects_missing_family_and_wrong_counts() -> None:
    review = valid_review()
    review["observable_failure_families_review"].pop()
    assert_rejected(review)
    review = valid_review()
    review["observable_failure_family_count"] = 3
    assert_rejected(review)
    review = valid_review()
    review["total_observable_evidence_items"] = 187
    assert_rejected(review)


@pytest.mark.parametrize(
    "field",
    [
        target.RESULTS_REVIEW_DIGEST_KEY, target.CLASSIFICATION_REVIEW_DIGEST_KEY,
        target.BOUNDED_ANALYSIS_REVIEW_DIGEST_KEY, target.MANIFEST_DIGEST_KEY,
    ],
)
def test_validator_rejects_changed_or_missing_digest(field: str) -> None:
    review = valid_review()
    review[field] = "changed"
    assert_rejected(review)
    review = valid_review()
    review.pop(field)
    assert_rejected(review)


def test_invalid_supplied_source_execution_is_rejected() -> None:
    with pytest.raises(
        target.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodResultsReviewAfterDiagnosticCaptureError
    ):
        target.build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_results_review_after_diagnostic_capture_v1(
            source_execution={}
        )


def test_writer_writes_only_status_markdown(tmp_path: Path) -> None:
    review = target.write_marketflow_repository_integration_branch_retry_failure_remediation_or_method_results_review_after_diagnostic_capture_v1(
        tmp_path
    )
    assert review["artifact_kind"] == target.ARTIFACT_KIND
    assert [path.name for path in tmp_path.iterdir()] == [
        "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_RESULTS_REVIEW_AFTER_DIAGNOSTIC_CAPTURE_STATUS.md"
    ]


def test_writer_refuses_protected_output() -> None:
    with pytest.raises(
        target.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodResultsReviewAfterDiagnosticCaptureError
    ):
        target.write_marketflow_repository_integration_branch_retry_failure_remediation_or_method_results_review_after_diagnostic_capture_v1(
            Path(".marketflow")
        )


def test_markdown_contains_required_sections() -> None:
    markdown = target.build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_results_review_after_diagnostic_capture_markdown_v1(valid_review())
    required = [
        "# MarketFlow Repository Integration Branch Retry Failure Remediation or Method Results Review After Diagnostic Capture v1",
        "## Source Method Execution", "## Source Failure-Family Classification",
        "## Source Bounded Excerpt Analysis", "## Source Approval",
        "## Source Operator Review and Candidate", "## Source Diagnostic Results Review",
        "## Source Controlled Recapture Execution", "## Source Durable Receipt",
        "## Source Receipt Loss History", "## Source Planning and Detail Binding Evidence",
        "## Retry Failure Context", "## Review Scope", "## Selected Remediation or Method Package",
        "## Priority 1 Target Modules", "## Diagnostic Capture Evidence Summary",
        "## Method Results Review", "## Observable Failure Families Review",
        "## Family Confidence and Limitations", "## Bounded Excerpt Integrity Review",
        "## Unsupported Claims Boundary", "## Review Findings", "## Recommendation",
        "## Next Chain", "## Next Gates", "## Risk Controls", "## Authority Boundaries",
        "## Checklist Summary", "## Guardrails",
    ]
    assert all(item in markdown for item in required)
