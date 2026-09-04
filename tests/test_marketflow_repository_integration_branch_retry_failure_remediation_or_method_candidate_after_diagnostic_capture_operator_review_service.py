from __future__ import annotations

import json
from pathlib import Path

import pytest

from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_diagnostic_capture_operator_review_service
    as service,
)


def _build() -> dict:
    return service.build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_diagnostic_capture_operator_review_v1()


def test_review_builds_offline_without_source_builders_receipt_or_execution(monkeypatch: pytest.MonkeyPatch) -> None:
    def forbidden(*args: object, **kwargs: object) -> None:
        raise AssertionError("forbidden action")

    monkeypatch.setattr(
        service.source,
        "build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_diagnostic_capture_v1",
        forbidden,
    )
    monkeypatch.setattr(
        service.source.source,
        "build_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_results_review_v1",
        forbidden,
    )
    review = _build()
    assert review["created_offline"] is True
    assert review["diagnostic_receipt_parsed_in_review"] is False
    assert review["diagnostic_output_analyzed_in_review"] is False


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("artifact_kind", service.ARTIFACT_KIND), ("schema_version", service.SCHEMA_VERSION),
        ("review_status", service.REVIEW_STATUS), ("review_scope", service.REVIEW_SCOPE),
        ("source_candidate_artifact_kind", service.source.ARTIFACT_KIND),
        ("source_candidate_status", service.source.CANDIDATE_STATUS),
        ("source_candidate_scope", service.source.CANDIDATE_SCOPE),
        ("source_candidate_commit", service.SOURCE_CANDIDATE_COMMIT),
        ("source_remediation_or_method_candidate_after_diagnostic_capture_digest", service.SOURCE_CANDIDATE_DIGEST),
        ("source_results_review_commit", service.SOURCE_RESULTS_REVIEW_COMMIT),
        ("source_receipt_recovery_or_recapture_results_review_digest", service.SOURCE_RESULTS_REVIEW_DIGEST),
        ("source_receipt_recovery_or_recapture_payload_review_digest", service.SOURCE_PAYLOAD_REVIEW_DIGEST),
        ("source_receipt_recovery_or_recapture_durable_receipt_review_digest", service.SOURCE_DURABLE_RECEIPT_REVIEW_DIGEST),
        ("source_receipt_recovery_or_recapture_results_review_manifest_digest", service.SOURCE_RESULTS_REVIEW_MANIFEST_DIGEST),
        ("source_receipt_recovery_or_recapture_execution_commit", service.SOURCE_EXECUTION_COMMIT),
        ("source_receipt_recovery_or_recapture_execution_digest", service.SOURCE_EXECUTION_DIGEST),
        ("source_receipt_recovery_or_recapture_payload_digest", service.SOURCE_PAYLOAD_DIGEST),
        ("source_receipt_recovery_or_recapture_receipt_digest", service.SOURCE_RECEIPT_DIGEST),
        ("source_receipt_recovery_or_recapture_digest_manifest_digest", service.SOURCE_DIGEST_MANIFEST_DIGEST),
        ("source_durable_receipt_path", service.SOURCE_DURABLE_RECEIPT_PATH),
        ("retry_execution_commit", service.RETRY_EXECUTION_COMMIT),
        ("priority_1_total_nodeids", 612), ("top_10_count_sum", 1069),
        ("module_summary_module_count", 29), ("failed_or_errored_nodeids_count", 1404),
        ("source_exit_code", 1), ("source_duration_seconds", "21.584361"),
        ("source_stdout_byte_count", 1231380), ("source_stderr_byte_count", 0),
        ("source_stdout_sha256", "b5fb29f6cf8af77700da74c72f08b854c33bc1ad30c79c309c6eefee70171d2a"),
        ("source_stderr_sha256", "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"),
        ("source_stdout_excerpt_truncated", True), ("source_stderr_excerpt_truncated", False),
        ("source_redaction_checked", True),
        ("recommended_remediation_or_method_package", service.RECOMMENDED_PACKAGE),
        ("recommendation_status", service.RECOMMENDATION_STATUS),
        ("predictive_usefulness", "not accepted"), ("profitability", "not accepted"),
        ("runtime_use", "NOT_AUTHORIZED"), ("broker_execution", "NOT_AUTHORIZED"),
    ],
)
def test_required_scalar_fields(field: str, expected: object) -> None:
    assert _build()[field] == expected


@pytest.mark.parametrize("field", sorted(service.SOURCE_BINDINGS))
def test_every_source_approval_diagnosis_planning_and_recovery_binding(field: str) -> None:
    assert _build()[field] == service.SOURCE_BINDINGS[field]


@pytest.mark.parametrize("field", service.TRUE_FIELDS)
def test_operator_review_facts_are_true(field: str) -> None:
    assert _build()[field] is True


@pytest.mark.parametrize("field", service.FALSE_FIELDS)
def test_all_prohibited_and_downstream_authority_facts_are_false(field: str) -> None:
    assert _build()[field] is False


def test_retry_and_priority_one_context_is_exact() -> None:
    review = _build()
    assert review["retry_failure_context"]["counts"] == {"passed": 24877, "failed": 1292, "errors": 112, "skipped": 7}
    assert review["retry_failure_context"]["first_result_authoritative"] is True
    assert review["retry_failure_context"]["root_full_regression_is_retry_evidence"] is False
    assert [item["module_path"] for item in review["priority_1_target_modules"]] == service.source.source.source.TARGET_MODULES
    assert [item["failed_or_errored_nodeid_count"] for item in review["priority_1_target_modules"]] == [136, 131, 122, 112, 111]


def test_diagnostic_capture_evidence_is_reviewed_but_not_analyzed() -> None:
    evidence = _build()["diagnostic_capture_evidence_summary"]
    assert evidence["exit_code"] == 1
    assert evidence["exit_code_is_diagnostic_only"] is True
    assert evidence["stdout_byte_count"] == 1231380
    assert evidence["stderr_byte_count"] == 0
    assert evidence["bounded_output"] is True
    assert evidence["redaction_checked"] is True
    assert evidence["receipt_parsed"] is False
    assert evidence["diagnostic_output_analyzed"] is False


def test_all_twelve_packages_are_reviewed_without_authority() -> None:
    packages = _build()["reviewed_remediation_or_method_packages"]
    assert packages == service.REVIEWED_PACKAGES
    assert len(packages) == 12
    assert sum(item["source_status"] == "BLOCKED_NOT_ALLOWED" for item in packages) == 6
    assert sum(item["review_status"] == "REVIEWED_BLOCKED_NOT_ALLOWED" for item in packages) == 6
    assert all(
        item["selected"] is False and item["approved"] is False
        and item["authorized"] is False and item["executed"] is False
        for item in packages
    )


def test_recommended_package_is_reviewed_but_not_selected() -> None:
    review = _build()
    package = review["recommended_package"]
    assert package["package_id"] == service.RECOMMENDED_PACKAGE
    assert package["review_status"] == service.RECOMMENDATION_STATUS
    assert package["selected"] is False
    assert package["approved"] is False
    assert package["authorized"] is False
    assert package["executed"] is False


def test_future_requirements_plan_outputs_and_non_goals_are_reviewed() -> None:
    review = _build()
    assert review["reviewed_future_method_requirements"] == service.REVIEWED_FUTURE_METHOD_REQUIREMENTS
    assert len(review["reviewed_future_method_requirements"]) == 39
    assert {item["execution_status"] for item in review["reviewed_future_method_requirements"]} == {"NOT_EXECUTED"}
    assert review["reviewed_future_method_plan"] == service.REVIEWED_FUTURE_METHOD_PLAN
    assert len(review["reviewed_future_method_plan"]) == 12
    assert review["reviewed_planned_outputs"] == service.REVIEWED_PLANNED_OUTPUTS
    assert len(review["reviewed_planned_outputs"]) == 14
    assert {item["generation_status"] for item in review["reviewed_planned_outputs"]} == {"NOT_GENERATED"}
    assert review["reviewed_non_goals"] == service.REVIEWED_NON_GOALS
    assert {item["review_status"] for item in review["reviewed_non_goals"]} == {"REVIEWED_ACTIVE"}


def test_recommendation_requires_optional_selection_and_separate_approval() -> None:
    recommendation = _build()["recommendation"]
    assert recommendation["recommended_next_task"] == service.RECOMMENDED_NEXT_TASK
    assert recommendation["recommended_next_task_status"] == "FUTURE_APPROVAL_NOT_CREATED"
    assert recommendation["recommended_action"] == service.RECOMMENDED_ACTION
    assert _build()["ready_for_remediation_or_method_approval"] is False


def test_digest_checklist_chain_gates_and_controls_are_deterministic() -> None:
    first = _build()
    second = _build()
    assert first == second
    assert first[service.OPERATOR_REVIEW_DIGEST_KEY] == second[service.OPERATOR_REVIEW_DIGEST_KEY]
    assert all(item["status"] == "PASS" for item in first["checklist"])
    assert first["summary"]["passed_checks"] == first["summary"]["total_checks"]
    assert first["summary"]["failed_checks"] == first["summary"]["blocker_count"] == 0
    assert first["next_chain"] == service.NEXT_CHAIN
    assert first["next_gates"] == service.NEXT_GATES
    assert first["risk_controls"] == service.RISK_CONTROLS


def test_validator_accepts_valid_review() -> None:
    validation = service.validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_diagnostic_capture_operator_review_v1(_build())
    assert validation["operator_review_digest"] == _build()[service.OPERATOR_REVIEW_DIGEST_KEY]
    assert validation["failed_checks"] == validation["blocker_count"] == 0


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("artifact_kind", "WRONG"), ("review_status", "WRONG"), ("review_scope", "WRONG"),
        ("source_remediation_or_method_candidate_after_diagnostic_capture_digest", "0" * 64),
        ("source_receipt_recovery_or_recapture_results_review_digest", "0" * 64),
        ("source_receipt_recovery_or_recapture_payload_review_digest", "0" * 64),
        ("source_receipt_recovery_or_recapture_durable_receipt_review_digest", "0" * 64),
        ("source_receipt_recovery_or_recapture_results_review_manifest_digest", "0" * 64),
        ("source_receipt_recovery_or_recapture_execution_digest", "0" * 64),
        ("source_receipt_recovery_or_recapture_payload_digest", "0" * 64),
        ("source_receipt_recovery_or_recapture_receipt_digest", "0" * 64),
        ("source_receipt_recovery_or_recapture_digest_manifest_digest", "0" * 64),
        ("source_durable_receipt_path", ""),
        ("recommended_remediation_or_method_package", "WRONG"),
        ("source_exit_code", 0), ("source_stdout_sha256", "0" * 64),
        ("source_stderr_sha256", "0" * 64), ("source_stdout_byte_count", 0),
        ("source_stderr_byte_count", 1), ("priority_1_total_nodeids", 611),
        ("top_10_count_sum", 1068), ("module_summary_module_count", 28),
        ("failed_or_errored_nodeids_count", 1403),
        ("predictive_usefulness", "accepted"), ("profitability", "accepted"),
        ("runtime_use", "AUTHORIZED"), ("broker_execution", "AUTHORIZED"),
    ],
)
def test_validator_rejects_changed_scalar_evidence_or_authority(field: str, value: object) -> None:
    review = _build()
    review[field] = value
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodCandidateAfterDiagnosticCaptureOperatorReviewError):
        service.validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_diagnostic_capture_operator_review_v1(review)


@pytest.mark.parametrize("field", sorted(service.SOURCE_BINDINGS))
def test_validator_rejects_changed_source_binding(field: str) -> None:
    review = _build()
    review[field] = "changed"
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodCandidateAfterDiagnosticCaptureOperatorReviewError):
        service.validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_diagnostic_capture_operator_review_v1(review)


@pytest.mark.parametrize("field", service.TRUE_FIELDS)
def test_validator_rejects_required_fact_false(field: str) -> None:
    review = _build()
    review[field] = False
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodCandidateAfterDiagnosticCaptureOperatorReviewError):
        service.validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_diagnostic_capture_operator_review_v1(review)


@pytest.mark.parametrize("field", service.FALSE_FIELDS)
def test_validator_rejects_closed_boundary_true(field: str) -> None:
    review = _build()
    review[field] = True
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodCandidateAfterDiagnosticCaptureOperatorReviewError):
        service.validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_diagnostic_capture_operator_review_v1(review)


@pytest.mark.parametrize(
    "field",
    [
        "source_candidate_summary", "source_diagnostic_results_review_summary",
        "source_controlled_recapture_execution_summary", "source_durable_receipt_summary",
        "source_receipt_loss_history_summary", "source_planning_and_detail_binding_summary",
        "diagnostic_capture_evidence_summary", "reviewed_candidate_philosophy", "recommended_package",
        "recommendation",
    ],
)
def test_validator_rejects_changed_nested_evidence_or_governance(field: str) -> None:
    review = _build()
    review[field] = {}
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodCandidateAfterDiagnosticCaptureOperatorReviewError):
        service.validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_diagnostic_capture_operator_review_v1(review)


def test_validator_rejects_missing_retry_counts_or_priority_paths() -> None:
    no_counts = _build()
    no_counts["retry_failure_context"]["counts"] = {}
    no_paths = _build()
    no_paths["priority_1_target_modules"] = []
    for review in (no_counts, no_paths):
        with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodCandidateAfterDiagnosticCaptureOperatorReviewError):
            service.validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_diagnostic_capture_operator_review_v1(review)


def test_validator_rejects_missing_or_selected_package_review() -> None:
    missing = _build()
    missing["reviewed_remediation_or_method_packages"] = []
    selected = _build()
    selected["reviewed_remediation_or_method_packages"][0]["selected"] = True
    recommended = _build()
    recommended["recommended_package"]["selected"] = True
    for review in (missing, selected, recommended):
        with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodCandidateAfterDiagnosticCaptureOperatorReviewError):
            service.validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_diagnostic_capture_operator_review_v1(review)


@pytest.mark.parametrize(
    "field",
    ["reviewed_future_method_requirements", "reviewed_future_method_plan", "reviewed_planned_outputs", "reviewed_non_goals", "next_chain", "risk_controls"],
)
def test_validator_rejects_missing_reviewed_governance(field: str) -> None:
    review = _build()
    review[field] = []
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodCandidateAfterDiagnosticCaptureOperatorReviewError):
        service.validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_diagnostic_capture_operator_review_v1(review)


def test_validator_rejects_missing_or_changed_digest() -> None:
    for value in (None, "0" * 64):
        review = _build()
        review[service.OPERATOR_REVIEW_DIGEST_KEY] = value
        with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodCandidateAfterDiagnosticCaptureOperatorReviewError):
            service.validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_diagnostic_capture_operator_review_v1(review)


def test_writer_round_trips_and_refuses_overwrite(tmp_path: Path) -> None:
    receipt = service.write_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_diagnostic_capture_operator_review_v1(tmp_path)
    path = Path(receipt["path"])
    written = json.loads(path.read_text(encoding="utf-8"))
    assert written == _build()
    assert receipt["operator_review_digest"] == written[service.OPERATOR_REVIEW_DIGEST_KEY]
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodCandidateAfterDiagnosticCaptureOperatorReviewError):
        service.write_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_diagnostic_capture_operator_review_v1(tmp_path)


@pytest.mark.parametrize("directory", [".marketflow", ".pytest_cache"])
def test_writer_rejects_protected_runtime_directories(tmp_path: Path, directory: str) -> None:
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodCandidateAfterDiagnosticCaptureOperatorReviewError):
        service.write_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_diagnostic_capture_operator_review_v1(tmp_path / directory)


def test_markdown_contains_all_required_sections() -> None:
    markdown = service.build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_diagnostic_capture_operator_review_markdown_v1(_build())
    for heading in (
        "# MarketFlow Repository Integration Branch Retry Failure Remediation or Method Candidate After Diagnostic Capture Operator Review v1",
        "## Source Candidate", "## Source Diagnostic Results Review", "## Source Controlled Recapture Execution",
        "## Source Durable Receipt", "## Source Receipt Loss History",
        "## Source Planning and Detail Binding Evidence", "## Retry Failure Context", "## Review Scope",
        "## Priority 1 Target Modules", "## Diagnostic Capture Evidence Summary",
        "## Reviewed Candidate Philosophy", "## Reviewed Remediation or Method Packages",
        "## Recommended Package", "## Reviewed Future Method Requirements", "## Reviewed Future Method Plan",
        "## Reviewed Planned Outputs", "## Reviewed Non-Goals", "## Recommendation", "## Next Chain",
        "## Next Gates", "## Risk Controls", "## Authority Boundaries", "## Checklist Summary", "## Guardrails",
    ):
        assert heading in markdown
