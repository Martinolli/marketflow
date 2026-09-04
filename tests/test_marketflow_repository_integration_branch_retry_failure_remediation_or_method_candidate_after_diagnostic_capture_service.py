from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

import pytest

from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_diagnostic_capture_service
    as service,
)


def _build() -> dict:
    return service.build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_diagnostic_capture_v1()


def test_candidate_builds_offline_without_source_builder_receipt_or_execution(monkeypatch: pytest.MonkeyPatch) -> None:
    def forbidden(*args: object, **kwargs: object) -> None:
        raise AssertionError("forbidden action")

    monkeypatch.setattr(
        service.source,
        "build_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_results_review_v1",
        forbidden,
    )
    monkeypatch.setattr(service.source.source, "execute_marketflow_repository_integration_branch_retry_failure_targeted_diagnostic_output_capture_receipt_recovery_or_recapture_execution_v1", forbidden)
    candidate = _build()
    assert candidate["created_offline"] is True
    assert candidate["diagnostic_receipt_parsed_in_candidate"] is False
    assert candidate["diagnostic_output_analyzed_in_candidate"] is False


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("artifact_kind", service.ARTIFACT_KIND), ("schema_version", service.SCHEMA_VERSION),
        ("candidate_status", service.CANDIDATE_STATUS), ("candidate_scope", service.CANDIDATE_SCOPE),
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
        ("recommended_next_task", service.RECOMMENDED_NEXT_TASK),
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
def test_candidate_only_readiness_facts_are_true(field: str) -> None:
    assert _build()[field] is True


@pytest.mark.parametrize("field", service.FALSE_FIELDS)
def test_all_prohibited_and_downstream_authority_facts_are_false(field: str) -> None:
    assert _build()[field] is False


def test_retry_and_priority_one_context_is_exact() -> None:
    candidate = _build()
    assert candidate["retry_failure_context"]["counts"] == {"passed": 24877, "failed": 1292, "errors": 112, "skipped": 7}
    assert candidate["retry_failure_context"]["first_result_authoritative"] is True
    assert candidate["retry_failure_context"]["root_full_regression_is_retry_evidence"] is False
    assert [item["module_path"] for item in candidate["priority_1_target_modules"]] == service.source.source.TARGET_MODULES
    assert [item["failed_or_errored_nodeid_count"] for item in candidate["priority_1_target_modules"]] == [136, 131, 122, 112, 111]


def test_diagnostic_capture_evidence_is_bound_but_not_analyzed() -> None:
    evidence = _build()["diagnostic_capture_evidence_summary"]
    assert evidence["exit_code"] == 1
    assert evidence["exit_code_is_diagnostic_only"] is True
    assert evidence["stdout_byte_count"] == 1231380
    assert evidence["stderr_byte_count"] == 0
    assert evidence["bounded_output"] is True
    assert evidence["redaction_checked"] is True
    assert evidence["receipt_parsed"] is False
    assert evidence["diagnostic_output_analyzed"] is False


def test_twelve_packages_include_six_blocked_and_no_selection() -> None:
    packages = _build()["proposed_remediation_or_method_packages"]
    assert packages == service.PROPOSED_PACKAGES
    assert len(packages) == 12
    assert sum(item["status"] == "BLOCKED_NOT_ALLOWED" for item in packages) == 6
    assert all(item["selected"] is False and item["approved"] is False and item["executed"] is False for item in packages)


def test_recommended_package_is_recommended_but_not_selected() -> None:
    candidate = _build()
    package = candidate["recommended_package"]
    assert package["package_id"] == service.RECOMMENDED_PACKAGE
    assert package["status"] == service.RECOMMENDATION_STATUS
    assert package["selected"] is False
    assert package["approved"] is False
    assert package["executed"] is False


def test_future_requirements_plan_outputs_and_governance_are_defined_not_executed() -> None:
    candidate = _build()
    assert candidate["future_method_requirements"] == service.FUTURE_METHOD_REQUIREMENTS
    assert all(candidate["future_method_requirements"].values())
    assert candidate["future_method_plan"] == {"status": "PLANNED_NOT_EXECUTED", "steps": service.FUTURE_METHOD_PLAN}
    assert candidate["planned_outputs"] == service.PLANNED_OUTPUTS
    assert set(candidate["planned_outputs"].values()) == {"PLANNED_NOT_GENERATED"}
    assert candidate["non_goals"] == service.NON_GOALS
    assert candidate["next_chain"] == service.NEXT_CHAIN
    assert candidate["next_gates"] == service.NEXT_GATES
    assert candidate["risk_controls"] == service.RISK_CONTROLS


def test_digest_and_checklist_are_deterministic() -> None:
    first = _build()
    second = _build()
    assert first == second
    assert first[service.CANDIDATE_DIGEST_KEY] == second[service.CANDIDATE_DIGEST_KEY]
    assert all(item["status"] == "PASS" for item in first["checklist"])
    assert first["summary"]["passed_checks"] == first["summary"]["total_checks"]
    assert first["summary"]["failed_checks"] == first["summary"]["blocker_count"] == 0


def test_validator_accepts_valid_candidate() -> None:
    validation = service.validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_diagnostic_capture_v1(_build())
    assert validation["candidate_digest"] == _build()[service.CANDIDATE_DIGEST_KEY]
    assert validation["failed_checks"] == validation["blocker_count"] == 0


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("artifact_kind", "WRONG"), ("candidate_status", "WRONG"), ("candidate_scope", "WRONG"),
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
    candidate = _build()
    candidate[field] = value
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodCandidateAfterDiagnosticCaptureError):
        service.validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_diagnostic_capture_v1(candidate)


@pytest.mark.parametrize("field", sorted(service.SOURCE_BINDINGS))
def test_validator_rejects_changed_source_binding(field: str) -> None:
    candidate = _build()
    candidate[field] = "changed"
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodCandidateAfterDiagnosticCaptureError):
        service.validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_diagnostic_capture_v1(candidate)


@pytest.mark.parametrize("field", service.TRUE_FIELDS)
def test_validator_rejects_required_fact_false(field: str) -> None:
    candidate = _build()
    candidate[field] = False
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodCandidateAfterDiagnosticCaptureError):
        service.validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_diagnostic_capture_v1(candidate)


@pytest.mark.parametrize("field", service.FALSE_FIELDS)
def test_validator_rejects_closed_boundary_true(field: str) -> None:
    candidate = _build()
    candidate[field] = True
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodCandidateAfterDiagnosticCaptureError):
        service.validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_diagnostic_capture_v1(candidate)


def test_validator_rejects_missing_retry_counts() -> None:
    candidate = _build()
    candidate["retry_failure_context"]["counts"] = {}
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodCandidateAfterDiagnosticCaptureError):
        service.validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_diagnostic_capture_v1(candidate)


@pytest.mark.parametrize(
    "field",
    [
        "source_diagnostic_results_review_summary", "source_controlled_recapture_execution_summary",
        "source_durable_receipt_summary", "source_receipt_loss_history_summary",
        "source_planning_and_detail_binding_summary", "diagnostic_capture_evidence_summary",
        "candidate_philosophy", "recommended_package",
    ],
)
def test_validator_rejects_changed_nested_evidence_or_governance(field: str) -> None:
    candidate = _build()
    candidate[field] = {}
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodCandidateAfterDiagnosticCaptureError):
        service.validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_diagnostic_capture_v1(candidate)


def test_validator_rejects_missing_priority_one_paths() -> None:
    candidate = _build()
    candidate["priority_1_target_modules"] = []
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodCandidateAfterDiagnosticCaptureError):
        service.validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_diagnostic_capture_v1(candidate)


def test_validator_rejects_missing_or_selected_packages() -> None:
    missing = _build()
    missing["proposed_remediation_or_method_packages"] = []
    selected = _build()
    selected["proposed_remediation_or_method_packages"][0]["selected"] = True
    recommended = _build()
    recommended["recommended_package"]["selected"] = True
    for candidate in (missing, selected, recommended):
        with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodCandidateAfterDiagnosticCaptureError):
            service.validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_diagnostic_capture_v1(candidate)


@pytest.mark.parametrize("field", ["future_method_requirements", "future_method_plan", "planned_outputs", "next_chain", "risk_controls"])
def test_validator_rejects_missing_future_governance(field: str) -> None:
    candidate = _build()
    candidate[field] = {} if field in {"future_method_requirements", "future_method_plan", "planned_outputs"} else []
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodCandidateAfterDiagnosticCaptureError):
        service.validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_diagnostic_capture_v1(candidate)


def test_validator_rejects_missing_or_changed_digest() -> None:
    for value in (None, "0" * 64):
        candidate = _build()
        candidate[service.CANDIDATE_DIGEST_KEY] = value
        with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodCandidateAfterDiagnosticCaptureError):
            service.validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_diagnostic_capture_v1(candidate)


def test_writer_round_trips_and_refuses_overwrite(tmp_path: Path) -> None:
    receipt = service.write_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_diagnostic_capture_v1(tmp_path)
    path = Path(receipt["path"])
    written = json.loads(path.read_text(encoding="utf-8"))
    assert written == _build()
    assert receipt["candidate_digest"] == written[service.CANDIDATE_DIGEST_KEY]
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodCandidateAfterDiagnosticCaptureError):
        service.write_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_diagnostic_capture_v1(tmp_path)


@pytest.mark.parametrize("directory", [".marketflow", ".pytest_cache"])
def test_writer_rejects_protected_runtime_directories(tmp_path: Path, directory: str) -> None:
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodCandidateAfterDiagnosticCaptureError):
        service.write_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_diagnostic_capture_v1(tmp_path / directory)


def test_markdown_contains_all_required_sections() -> None:
    markdown = service.build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_diagnostic_capture_markdown_v1(_build())
    for heading in (
        "# MarketFlow Repository Integration Branch Retry Failure Remediation or Method Candidate After Diagnostic Capture v1",
        "## Source Diagnostic Results Review", "## Source Controlled Recapture Execution",
        "## Source Durable Receipt", "## Source Receipt Loss History",
        "## Source Planning and Detail Binding Evidence", "## Retry Failure Context",
        "## Candidate Scope", "## Priority 1 Target Modules", "## Diagnostic Capture Evidence Summary",
        "## Candidate Philosophy", "## Proposed Remediation or Method Packages", "## Recommended Package",
        "## Future Method Requirements", "## Future Method Plan", "## Planned Outputs", "## Non-Goals",
        "## Next Chain", "## Next Gates", "## Risk Controls", "## Authority Boundaries",
        "## Checklist Summary", "## Guardrails",
    ):
        assert heading in markdown
