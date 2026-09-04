from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import socket

import pytest

from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_results_review_service
    as service,
)


def _build() -> dict:
    return service.build_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_results_review_v1()


def _set_path(value: dict, path: str, replacement: object) -> None:
    target = value
    parts = path.split(".")
    for part in parts[:-1]:
        target = target[part]
    target[parts[-1]] = replacement


def test_results_review_builds_offline_without_execution_or_network(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(socket, "create_connection", lambda *args, **kwargs: pytest.fail("network attempted"))
    monkeypatch.setattr(
        service.source,
        "execute_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_execution_v1",
        lambda *args, **kwargs: pytest.fail("recapture execution called"),
    )
    review = _build()
    assert review["created_offline"] is True
    assert review["governance_only"] is True
    assert review["results_review_only"] is True


def test_committed_durable_receipt_is_read_and_verified() -> None:
    review = _build()
    assert service.DEFAULT_DURABLE_RECEIPT_PATH.is_file()
    assert review["source_durable_receipt_path"] == service.SOURCE_DURABLE_RECEIPT_PATH
    assert review["source_durable_receipt_file_reviewed"] is True
    assert review["durable_receipt_review"] == {
        "scaffold_prewritten": True,
        "finalized": True,
        "retained": True,
        "receipt_status": "FINALIZED_AFTER_COMMAND",
        "receipt_digest_verified": True,
    }


def test_receipt_can_be_verified_from_an_isolated_copy(tmp_path: Path) -> None:
    copy = tmp_path / "receipt.json"
    copy.write_bytes(service.DEFAULT_DURABLE_RECEIPT_PATH.read_bytes())
    review = service.build_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_results_review_v1(durable_receipt_path=copy)
    assert review["source_durable_receipt_digest_verified"] is True


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("artifact_kind", service.ARTIFACT_KIND),
        ("schema_version", service.SCHEMA_VERSION),
        ("review_status", service.REVIEW_STATUS),
        ("review_scope", service.REVIEW_SCOPE),
        ("source_execution_artifact_kind", service.source.ARTIFACT_KIND_SUCCESS),
        ("source_execution_status", service.source.EXECUTION_STATUS_SUCCESS),
        ("source_execution_scope", service.source.EXECUTION_SCOPE),
        ("source_execution_commit", service.SOURCE_EXECUTION_COMMIT),
        ("source_receipt_recovery_or_recapture_execution_digest", service.SOURCE_EXECUTION_DIGEST),
        ("source_receipt_recovery_or_recapture_payload_digest", service.SOURCE_PAYLOAD_DIGEST),
        ("source_receipt_recovery_or_recapture_receipt_digest", service.SOURCE_RECEIPT_DIGEST),
        ("source_receipt_recovery_or_recapture_digest_manifest_digest", service.SOURCE_DIGEST_MANIFEST_DIGEST),
        ("selected_receipt_recovery_or_recapture_package", service.SELECTED_PACKAGE),
        ("retry_execution_commit", service.RETRY_EXECUTION_COMMIT),
        ("priority_1_total_nodeids", 612),
        ("top_10_count_sum", 1069),
        ("module_summary_module_count", 29),
        ("failed_or_errored_nodeids_count", 1404),
        ("source_exit_code", 1),
        ("source_duration_seconds", "21.584361"),
        ("source_stdout_byte_count", 1231380),
        ("source_stderr_byte_count", 0),
        ("source_stdout_excerpt_truncated", True),
        ("source_stderr_excerpt_truncated", False),
        ("source_redaction_checked", True),
        ("predictive_usefulness", "not accepted"),
        ("profitability", "not accepted"),
        ("runtime_use", "NOT_AUTHORIZED"),
        ("broker_execution", "NOT_AUTHORIZED"),
    ],
)
def test_required_scalar_fields(field: str, expected: object) -> None:
    assert _build()[field] == expected


@pytest.mark.parametrize("field", sorted(service.SOURCE_BINDINGS))
def test_every_source_digest_and_classification_is_bound(field: str) -> None:
    assert _build()[field] == service.SOURCE_BINDINGS[field]


@pytest.mark.parametrize("field", service.TRUE_FIELDS)
def test_review_facts_are_true(field: str) -> None:
    assert _build()[field] is True


@pytest.mark.parametrize("field", service.FALSE_FIELDS)
def test_closed_boundaries_are_false(field: str) -> None:
    assert _build()[field] is False


def test_retry_and_priority_one_facts_are_preserved() -> None:
    review = _build()
    assert review["retry_failure_context"]["counts"] == {"passed": 24877, "failed": 1292, "errors": 112, "skipped": 7}
    assert review["retry_failure_context"]["first_result_authoritative"] is True
    assert [item["module_path"] for item in review["priority_1_target_modules"]] == service.source.TARGET_MODULES
    assert [item["failed_or_errored_nodeid_count"] for item in review["priority_1_target_modules"]] == [136, 131, 122, 112, 111]


def test_controlled_recapture_result_is_exact_and_diagnostic_only() -> None:
    result = _build()["controlled_recapture_result_review"]
    assert result["exit_code"] == 1
    assert result["duration_seconds"] == "21.584361"
    assert result["stdout_sha256"] == "b5fb29f6cf8af77700da74c72f08b854c33bc1ad30c79c309c6eefee70171d2a"
    assert result["stderr_sha256"] == "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    assert result["stdout_byte_count"] == result["combined_output_byte_count"] == 1231380
    assert result["stderr_byte_count"] == 0
    assert result["stdout_excerpt_truncated"] is True
    assert result["stderr_excerpt_truncated"] is False
    assert result["nonzero_exit_code_is_diagnostic_evidence_only"] is True


def test_command_boundaries_are_reviewed_exactly() -> None:
    result = _build()["controlled_recapture_result_review"]
    assert result["python_executable"] == str(service.source.APPROVED_PYTHON_EXECUTABLE)
    assert result["cwd"] == str(service.source.APPROVED_WORKING_DIRECTORY)
    assert result["target_modules"] == service.source.TARGET_MODULES
    assert result["cacheprovider_disabled"] is True
    assert result["command_is_retry"] is False
    assert result["command_is_full_pytest"] is False


def test_review_does_not_copy_bounded_output_content() -> None:
    review = _build()
    assert "bounded_stdout_excerpt" not in review
    assert "bounded_stderr_excerpt" not in review
    assert review["bounded_output_review"]["bounded_excerpts_stored"] is True
    assert review["redaction_review"]["redaction_checked"] is True


def test_findings_outputs_recommendation_and_gates_are_exact() -> None:
    review = _build()
    assert review["review_findings"] == service.REVIEW_FINDINGS and len(service.REVIEW_FINDINGS) == 15
    assert review["review_outputs"] == service.REVIEW_OUTPUTS and len(service.REVIEW_OUTPUTS) == 17
    assert review["recommendation"]["recommended_next_task"] == service.NEXT_TASK
    assert review["recommendation"]["recommended_next_task_status"] == service.NEXT_TASK_STATUS
    assert review["next_chain"] == service.NEXT_CHAIN and len(service.NEXT_CHAIN) == 10
    assert review["next_gates"] == service.NEXT_GATES and len(service.NEXT_GATES) == 10
    assert review["risk_controls"] == service.RISK_CONTROLS


def test_review_digests_and_checklist_are_deterministic() -> None:
    first, second = _build(), _build()
    for field in (
        service.RESULTS_REVIEW_DIGEST_KEY,
        service.PAYLOAD_REVIEW_DIGEST_KEY,
        service.DURABLE_RECEIPT_REVIEW_DIGEST_KEY,
        service.RESULTS_REVIEW_MANIFEST_DIGEST_KEY,
    ):
        assert first[field] == second[field]
        assert len(first[field]) == 64
    assert first["summary"]["passed_checks"] == first["summary"]["total_checks"]
    assert first["summary"]["failed_checks"] == first["summary"]["blocker_count"] == 0
    assert all(set(item) == {"check_id", "status", "expected", "actual", "severity", "message"} for item in first["checklist"])


def test_validator_accepts_valid_review() -> None:
    result = service.validate_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_results_review_v1(_build())
    assert result["failed_checks"] == result["blocker_count"] == 0
    assert result["passed_checks"] == result["total_checks"]


@pytest.mark.parametrize(
    ("path", "replacement", "message"),
    [
        ("artifact_kind", "WRONG", "artifact_kind"),
        ("review_status", "WRONG", "review_status"),
        ("review_scope", "WRONG", "review_scope"),
        ("source_execution_status", "WRONG", "source_execution_status"),
        ("source_receipt_recovery_or_recapture_execution_digest", "0" * 64, "source_receipt"),
        ("source_receipt_recovery_or_recapture_payload_digest", "0" * 64, "source_receipt"),
        ("source_receipt_recovery_or_recapture_receipt_digest", "0" * 64, "source_receipt"),
        ("source_receipt_recovery_or_recapture_digest_manifest_digest", "0" * 64, "source_receipt"),
        ("source_durable_receipt_path", "", "source_durable"),
        ("selected_receipt_recovery_or_recapture_package", "WRONG", "selected"),
        ("source_receipt_recovery_or_recapture_approval_digest", "0" * 64, "source_receipt"),
        ("source_targeted_diagnostic_output_capture_execution_failure_diagnosis_digest", "0" * 64, "source_targeted"),
        ("source_targeted_diagnostic_output_capture_execution_blocked_reason", "WRONG", "source_targeted"),
        ("source_primary_failure_class", "WRONG", "source_primary"),
        ("source_targeted_diagnostic_output_capture_approval_digest", "0" * 64, "source_targeted"),
        ("source_results_review_digest", "0" * 64, "source_results"),
        ("source_planning_execution_digest", "0" * 64, "source_planning"),
        ("source_complete_29_row_binding_digest", "0" * 64, "source_complete"),
        ("source_materialized_payload_digest", "0" * 64, "source_materialized"),
        ("source_recovery_detail_digest", "0" * 64, "source_recovery"),
        ("source_module_grouping_digest", "0" * 64, "source_module"),
        ("retry_failure_context.counts", {}, "retry failure"),
        ("priority_1_total_nodeids", 611, "priority_1"),
        ("top_10_count_sum", 1068, "top_10"),
        ("controlled_recapture_result_review.diagnostic_command_executed", False, "controlled recapture"),
        ("controlled_recapture_result_review.command_is_retry", True, "controlled recapture"),
        ("controlled_recapture_result_review.command_is_full_pytest", True, "controlled recapture"),
        ("controlled_recapture_result_review.exit_code", 0, "controlled recapture"),
        ("controlled_recapture_result_review.stdout_sha256", "0" * 64, "controlled recapture"),
        ("controlled_recapture_result_review.stderr_sha256", "0" * 64, "controlled recapture"),
        ("controlled_recapture_result_review.stdout_byte_count", 1, "controlled recapture"),
        ("durable_receipt_review.finalized", False, "durable receipt"),
        ("redaction_review.redaction_checked", False, "redaction review"),
        ("post_execution_boundary_review.reviewed", False, "post execution"),
        ("receipt_recovery_or_recapture_results_review_created", False, "required review"),
        ("ready_for_remediation_or_method_candidate_after_diagnostic_capture", False, "required review"),
        ("ready_for_retry_candidate", True, "closed boundary"),
        ("controlled_recapture_rerun_performed", True, "closed boundary"),
        ("diagnostic_command_rerun_performed", True, "closed boundary"),
        ("targeted_pytest_performed_in_review", True, "closed boundary"),
        ("full_pytest_performed", True, "closed boundary"),
        ("retry_rerun_performed", True, "closed boundary"),
        ("cache_read_in_review", True, "closed boundary"),
        ("cache_modified_in_review", True, "closed boundary"),
        ("pytest_cache_committed", True, "closed boundary"),
        ("marketflow_outputs_committed", True, "closed boundary"),
        ("terminal_logs_parsed", True, "closed boundary"),
        ("operator_logs_parsed", True, "closed boundary"),
        ("env_inspection_performed", True, "closed boundary"),
        ("prior_lost_values_reconstructed", True, "closed boundary"),
        ("remediation_or_method_candidate_after_diagnostic_capture_created", True, "closed boundary"),
        ("new_retry_candidate_created", True, "closed boundary"),
        ("classification_execution_performed_in_review", True, "closed boundary"),
        ("remediation_execution_performed", True, "closed boundary"),
        ("failure_error_separation_claimed", True, "closed boundary"),
        ("first_failure_identified", True, "closed boundary"),
        ("traceback_root_cause_claimed", True, "closed boundary"),
        ("direct_code_remediation_recommended", True, "closed boundary"),
        ("retry_success_claimed", True, "closed boundary"),
        ("integration_execution_successful", True, "closed boundary"),
        ("main_push_performed", True, "closed boundary"),
        ("provider_requests_made_in_review", True, "closed boundary"),
        ("predictive_usefulness", "accepted", "acceptance boundary"),
        ("runtime_use", "AUTHORIZED", "runtime boundary"),
        ("review_outputs", [], "review content"),
        ("risk_controls", [], "governance structure"),
    ],
)
def test_validator_rejects_tampering(path: str, replacement: object, message: str) -> None:
    review = _build()
    _set_path(review, path, replacement)
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureReceiptRecoveryOrRecaptureResultsReviewError, match=message):
        service.validate_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_results_review_v1(review)


def test_missing_or_invalid_receipt_fails_closed(tmp_path: Path) -> None:
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureReceiptRecoveryOrRecaptureResultsReviewError, match="unavailable"):
        service.build_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_results_review_v1(durable_receipt_path=tmp_path / "missing.json")
    invalid = tmp_path / "invalid.json"
    invalid.write_text("[]", encoding="utf-8")
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureReceiptRecoveryOrRecaptureResultsReviewError, match="object"):
        service.build_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_results_review_v1(durable_receipt_path=invalid)


def test_tampered_receipt_fails_closed(tmp_path: Path) -> None:
    receipt = json.loads(service.DEFAULT_DURABLE_RECEIPT_PATH.read_text(encoding="utf-8"))
    receipt["receipt_finalized"] = False
    path = tmp_path / "receipt.json"
    path.write_text(json.dumps(receipt), encoding="utf-8")
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureReceiptRecoveryOrRecaptureResultsReviewError):
        service.build_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_results_review_v1(durable_receipt_path=path)


def test_writer_round_trips_to_isolated_output(tmp_path: Path) -> None:
    result = service.write_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_results_review_v1(tmp_path)
    payload = json.loads(Path(result["path"]).read_text(encoding="utf-8"))
    assert result["results_review_digest"] == payload[service.RESULTS_REVIEW_DIGEST_KEY]
    assert service.validate_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_results_review_v1(payload)["failed_checks"] == 0
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureReceiptRecoveryOrRecaptureResultsReviewError, match="output exists"):
        service.write_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_results_review_v1(tmp_path)


def test_writer_rejects_protected_output(tmp_path: Path) -> None:
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureTargetedDiagnosticOutputCaptureReceiptRecoveryOrRecaptureResultsReviewError, match="protected"):
        service.write_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_results_review_v1(tmp_path / ".pytest_cache")


def test_markdown_contains_all_required_sections() -> None:
    markdown = service.build_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_results_review_markdown_v1(_build())
    for heading in (
        "Source Receipt Recovery or Controlled Recapture Execution", "Source Durable Receipt",
        "Source Approval and Operator Review", "Source Execution Failure Diagnosis",
        "Source Planning and Detail Binding Evidence", "Retry Failure Context", "Review Scope",
        "Priority 1 Target Modules", "Controlled Recapture Result Review", "Durable Receipt Review",
        "Diagnostic Output Capture Review", "Bounded Output Review", "Redaction Review",
        "Post-Execution Boundary Review", "Unsupported Claims Boundary", "Review Findings",
        "Recommendation", "Next Chain", "Next Gates", "Risk Controls", "Authority Boundaries",
        "Checklist Summary", "Guardrails",
    ):
        assert f"## {heading}" in markdown
