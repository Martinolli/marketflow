from __future__ import annotations

from copy import deepcopy
import json

import pytest

from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_remediation_or_method_approval_after_diagnostic_capture_service
    as target,
)


def valid_attestation_kwargs() -> dict:
    return {
        "operator_reference": "TEST_OPERATOR",
        "operator_attestation_timestamp_utc": "2026-08-23T00:00:00Z",
        "operator_attestation_phrase": target.REQUIRED_REMEDIATION_OR_METHOD_APPROVAL_AFTER_DIAGNOSTIC_CAPTURE_ATTESTATION_PHRASE_V1,
        **deepcopy(target.SOURCE_ATTESTATION_FIELDS),
        **{field: True for field in target.ATTESTATION_BOOLEAN_FIELDS},
    }


def valid_attestation() -> dict:
    return target.build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_approval_after_diagnostic_capture_attestation_v1(
        **valid_attestation_kwargs()
    )


def valid_approval() -> dict:
    return target.build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_approval_after_diagnostic_capture_v1(
        operator_attestation=valid_attestation()
    )


def assert_rejected(approval: dict) -> None:
    with pytest.raises(target.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodApprovalAfterDiagnosticCaptureError):
        target.validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_approval_after_diagnostic_capture_v1(approval)


def test_attestation_builder_creates_required_fields() -> None:
    attestation = valid_attestation()
    assert attestation["operator_decision"] == target.OPERATOR_DECISION
    assert attestation["selected_remediation_or_method_package"] == target.SELECTED_PACKAGE
    assert attestation["operator_attestation_version"] == target.OPERATOR_ATTESTATION_VERSION
    assert all(attestation[field] is True for field in target.ATTESTATION_BOOLEAN_FIELDS)


def test_approval_builds_offline_without_source_builder(monkeypatch: pytest.MonkeyPatch) -> None:
    def forbidden(*args, **kwargs):
        raise AssertionError("source builder must not run")

    monkeypatch.setattr(
        target.source,
        "build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_candidate_after_diagnostic_capture_operator_review_v1",
        forbidden,
    )
    approval = valid_approval()
    assert approval["created_offline"] is True
    assert approval["governance_only"] is True
    assert approval["approval_only"] is True


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("artifact_kind", target.ARTIFACT_KIND), ("schema_version", target.SCHEMA_VERSION),
        ("approval_status", target.APPROVAL_STATUS), ("approval_scope", target.APPROVAL_SCOPE),
        ("selected_remediation_or_method_package", target.SELECTED_PACKAGE),
        ("source_operator_review_artifact_kind", target.source.ARTIFACT_KIND),
        ("source_operator_review_status", target.source.REVIEW_STATUS),
        ("source_operator_review_scope", target.source.REVIEW_SCOPE),
        ("source_operator_review_commit", target.SOURCE_OPERATOR_REVIEW_COMMIT),
        ("source_remediation_or_method_candidate_after_diagnostic_capture_operator_review_digest", target.SOURCE_OPERATOR_REVIEW_DIGEST),
        ("source_remediation_or_method_candidate_after_diagnostic_capture_digest", target.source.SOURCE_CANDIDATE_DIGEST),
        ("source_receipt_recovery_or_recapture_results_review_digest", target.source.SOURCE_RESULTS_REVIEW_DIGEST),
        ("source_receipt_recovery_or_recapture_payload_review_digest", target.source.SOURCE_PAYLOAD_REVIEW_DIGEST),
        ("source_receipt_recovery_or_recapture_durable_receipt_review_digest", target.source.SOURCE_DURABLE_RECEIPT_REVIEW_DIGEST),
        ("source_receipt_recovery_or_recapture_results_review_manifest_digest", target.source.SOURCE_RESULTS_REVIEW_MANIFEST_DIGEST),
        ("source_receipt_recovery_or_recapture_execution_commit", target.source.SOURCE_EXECUTION_COMMIT),
        ("source_receipt_recovery_or_recapture_execution_digest", target.source.SOURCE_EXECUTION_DIGEST),
        ("source_receipt_recovery_or_recapture_payload_digest", target.source.SOURCE_PAYLOAD_DIGEST),
        ("source_receipt_recovery_or_recapture_receipt_digest", target.source.SOURCE_RECEIPT_DIGEST),
        ("source_receipt_recovery_or_recapture_digest_manifest_digest", target.source.SOURCE_DIGEST_MANIFEST_DIGEST),
        ("source_durable_receipt_path", target.source.SOURCE_DURABLE_RECEIPT_PATH),
    ],
)
def test_core_and_source_fields(field: str, expected: object) -> None:
    assert valid_approval()[field] == expected


@pytest.mark.parametrize("field", target.TRUE_FIELDS)
def test_required_approval_fact_true(field: str) -> None:
    assert valid_approval()[field] is True


@pytest.mark.parametrize("field", target.FALSE_FIELDS)
def test_closed_boundary_false(field: str) -> None:
    assert valid_approval()[field] is False


def test_retry_priority_and_diagnostic_facts_are_bound() -> None:
    approval = valid_approval()
    assert approval["retry_failure_context"]["counts"] == {"passed": 24877, "failed": 1292, "errors": 112, "skipped": 7}
    assert approval["retry_failure_context"]["first_result_authoritative"] is True
    assert approval["retry_failure_context"]["root_full_regression_is_retry_evidence"] is False
    assert [row["module_path"] for row in approval["priority_1_target_modules"]] == [row["module_path"] for row in target.source.PRIORITY_1_TARGET_MODULES]
    assert (approval["priority_1_total_nodeids"], approval["top_10_count_sum"]) == (612, 1069)
    assert (approval["module_summary_module_count"], approval["failed_or_errored_nodeids_count"]) == (29, 1404)
    assert (approval["source_exit_code"], approval["source_exit_code_is_diagnostic_only"]) == (1, True)
    assert (approval["source_stdout_byte_count"], approval["source_stderr_byte_count"]) == (1231380, 0)
    assert approval["source_stdout_sha256"] == target.SOURCE_ATTESTATION_FIELDS["operator_confirms_source_stdout_hash"]
    assert approval["source_stderr_sha256"] == target.SOURCE_ATTESTATION_FIELDS["operator_confirms_source_stderr_hash"]
    assert approval["source_stdout_excerpt_truncated"] is True
    assert approval["source_stderr_excerpt_truncated"] is False
    assert approval["source_redaction_checked"] is True


def test_package_and_future_execution_authority_is_exactly_bounded() -> None:
    approval = valid_approval()
    package = approval["approved_package"]
    assert package["package_id"] == target.SELECTED_PACKAGE
    assert package["approval_status"] == target.APPROVED_ONLY
    assert package["selected"] is package["approved"] is package["authorized_for_future_execution"] is True
    assert package["executed"] is False
    assert approval["future_method_execution_status"] == "APPROVED_FOR_FUTURE_EXECUTION_ONLY_NOT_EXECUTED"
    assert approval["future_method_input_source"] == "COMMITTED_DURABLE_RECEIPT_AND_REVIEWED_BOUNDED_DIAGNOSTIC_EXCERPTS_ONLY"
    assert approval["future_method_may_read_durable_receipt_if_executed"] is True
    assert approval["future_method_may_analyze_bounded_diagnostic_output_if_executed"] is True
    assert approval["future_method_may_classify_observable_failure_families_if_executed"] is True
    assert approval["future_method_may_claim_root_cause"] is False
    assert approval["future_method_may_identify_authoritative_first_failure"] is False
    assert approval["future_method_may_recommend_direct_code_remediation_without_results_review"] is False
    assert approval["future_method_may_create_retry_candidate"] is False
    assert approval["future_method_executed"] is False


def test_all_approved_and_carried_forward_inventories() -> None:
    approval = valid_approval()
    assert len(approval["approved_future_method_requirements"]) == 39
    assert all(row["approval_status"] == target.APPROVED_ONLY and row["execution_status"] == "NOT_EXECUTED" for row in approval["approved_future_method_requirements"])
    assert len(approval["approved_future_method_plan"]) == 12
    assert all(row["approval_status"] == target.APPROVED_ONLY and row["execution_status"] == "NOT_EXECUTED" for row in approval["approved_future_method_plan"])
    assert len(approval["authorized_planned_outputs"]) == 14
    assert all(row["authorization_status"] == "AUTHORIZED_NOT_GENERATED" for row in approval["authorized_planned_outputs"])
    assert len(approval["supporting_packages"]) == 5
    assert all(not row["selected"] and not row["approved"] for row in approval["supporting_packages"])
    assert len(approval["blocked_packages"]) == 6
    assert all(row["approval_status"] == "BLOCKED_NOT_APPROVED" for row in approval["blocked_packages"])


def test_chain_gates_risks_checklist_and_summary() -> None:
    approval = valid_approval()
    assert approval["next_chain"] == target.NEXT_CHAIN
    assert approval["next_gates"] == target.NEXT_GATES
    assert approval["risk_controls"] == target.RISK_CONTROLS
    assert len(target.RISK_CONTROLS) == 85
    assert all(row["status"] == "PASS" and row["severity"] == "BLOCKER" for row in approval["checklist"])
    assert approval["summary"]["passed_checks"] == approval["summary"]["total_checks"]
    assert approval["summary"]["blocker_count"] == 0
    assert approval["summary"]["recommended_next_task"] == target.RECOMMENDED_NEXT_TASK


def test_authority_strings_remain_closed() -> None:
    approval = valid_approval()
    assert approval["predictive_usefulness"] == "not accepted"
    assert approval["profitability"] == "not accepted"
    assert approval["runtime_use"] == approval["strategy_use"] == "NOT_AUTHORIZED"
    assert approval["paper_trading"] == approval["broker_execution"] == "NOT_AUTHORIZED"


def test_digest_is_deterministic_and_validator_accepts() -> None:
    first = valid_approval()
    second = valid_approval()
    assert first[target.APPROVAL_DIGEST_KEY] == second[target.APPROVAL_DIGEST_KEY]
    result = target.validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_approval_after_diagnostic_capture_v1(first)
    assert result["approval_digest"] == first[target.APPROVAL_DIGEST_KEY]
    assert result["failed_checks"] == result["blocker_count"] == 0


@pytest.mark.parametrize("field", list(target.SOURCE_ATTESTATION_FIELDS))
def test_attestation_rejects_changed_source_confirmation(field: str) -> None:
    kwargs = valid_attestation_kwargs()
    kwargs[field] = "changed"
    with pytest.raises(target.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodApprovalAfterDiagnosticCaptureError):
        target.build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_approval_after_diagnostic_capture_attestation_v1(**kwargs)


@pytest.mark.parametrize("field", target.ATTESTATION_BOOLEAN_FIELDS)
def test_attestation_rejects_false_confirmation(field: str) -> None:
    kwargs = valid_attestation_kwargs()
    kwargs[field] = False
    with pytest.raises(target.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodApprovalAfterDiagnosticCaptureError):
        target.build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_approval_after_diagnostic_capture_attestation_v1(**kwargs)


@pytest.mark.parametrize(
    ("field", "value"),
    [("operator_attestation_phrase", "wrong"), ("operator_attestation_timestamp_utc", "not-utc"),
     ("operator_reference", ""), ("selected_remediation_or_method_package", "wrong"),
     ("operator_decision", "wrong")],
)
def test_attestation_rejects_invalid_identity_or_decision(field: str, value: object) -> None:
    kwargs = valid_attestation_kwargs()
    kwargs[field] = value
    with pytest.raises(target.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodApprovalAfterDiagnosticCaptureError):
        target.build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_approval_after_diagnostic_capture_attestation_v1(**kwargs)


@pytest.mark.parametrize("field", list(target._source_fields()))
def test_validator_rejects_changed_source_binding(field: str) -> None:
    approval = valid_approval()
    approval[field] = "changed"
    assert_rejected(approval)


@pytest.mark.parametrize("field", target.TRUE_FIELDS)
def test_validator_rejects_required_fact_false(field: str) -> None:
    approval = valid_approval()
    approval[field] = False
    assert_rejected(approval)


@pytest.mark.parametrize("field", target.FALSE_FIELDS)
def test_validator_rejects_closed_boundary_true(field: str) -> None:
    approval = valid_approval()
    approval[field] = True
    assert_rejected(approval)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("artifact_kind", "wrong"), ("schema_version", "wrong"), ("approval_status", "wrong"),
        ("approval_scope", "wrong"), ("selected_remediation_or_method_package", "wrong"),
        ("retry_execution_commit", "wrong"), ("priority_1_total_nodeids", 611),
        ("top_10_count_sum", 1068), ("module_summary_module_count", 28),
        ("failed_or_errored_nodeids_count", 1403), ("source_exit_code", 0),
        ("source_stdout_sha256", "0" * 64), ("source_stderr_sha256", "0" * 64),
        ("source_stdout_byte_count", 1), ("source_stderr_byte_count", 1),
        ("approved_future_method_requirements", []), ("approved_future_method_plan", []),
        ("authorized_planned_outputs", []), ("supporting_packages", []), ("blocked_packages", []),
        ("next_chain", []), ("next_gates", []), ("risk_controls", []),
        ("predictive_usefulness", "accepted"), ("profitability", "accepted"),
        ("runtime_use", "AUTHORIZED"), ("broker_execution", "AUTHORIZED"),
    ],
)
def test_validator_rejects_core_or_inventory_tamper(field: str, value: object) -> None:
    approval = valid_approval()
    approval[field] = value
    assert_rejected(approval)


def test_validator_rejects_nested_attestation_change_and_missing_digest() -> None:
    approval = valid_approval()
    approval["operator_attestation"]["operator_decision"] = "wrong"
    assert_rejected(approval)
    approval = valid_approval()
    del approval[target.APPROVAL_DIGEST_KEY]
    assert_rejected(approval)


def test_writer_round_trip_and_no_overwrite(tmp_path) -> None:
    result = target.write_marketflow_repository_integration_branch_retry_failure_remediation_or_method_approval_after_diagnostic_capture_v1(
        tmp_path, operator_attestation=valid_attestation()
    )
    payload = json.loads((tmp_path / "marketflow_repository_integration_branch_retry_failure_remediation_or_method_approval_after_diagnostic_capture_v1.json").read_text(encoding="utf-8"))
    target.validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_approval_after_diagnostic_capture_v1(payload)
    assert result["approval_digest"] == payload[target.APPROVAL_DIGEST_KEY]
    with pytest.raises(target.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodApprovalAfterDiagnosticCaptureError):
        target.write_marketflow_repository_integration_branch_retry_failure_remediation_or_method_approval_after_diagnostic_capture_v1(
            tmp_path, operator_attestation=valid_attestation()
        )


@pytest.mark.parametrize("protected", [".marketflow", ".pytest_cache"])
def test_writer_rejects_protected_runtime_directory(tmp_path, protected: str) -> None:
    with pytest.raises(target.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodApprovalAfterDiagnosticCaptureError):
        target.write_marketflow_repository_integration_branch_retry_failure_remediation_or_method_approval_after_diagnostic_capture_v1(
            tmp_path / protected, operator_attestation=valid_attestation()
        )


@pytest.mark.parametrize(
    "heading",
    ["Operator Attestation", "Source Operator Review", "Source Candidate", "Source Diagnostic Results Review",
     "Source Controlled Recapture Execution", "Source Durable Receipt", "Source Receipt Loss History",
     "Source Planning and Detail Binding Evidence", "Retry Failure Context", "Approval Scope",
     "Selected Remediation or Method Package", "Priority 1 Target Modules", "Diagnostic Capture Evidence Summary",
     "Approved Future Method Requirements", "Approved Future Method Plan", "Future Method Execution Boundary",
     "Planned Outputs", "Supporting Packages", "Blocked Packages", "Next Chain", "Next Gates", "Risk Controls",
     "Authority Boundaries", "Checklist Summary", "Guardrails"],
)
def test_markdown_contains_required_sections(heading: str) -> None:
    markdown = target.build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_approval_after_diagnostic_capture_markdown_v1(valid_approval())
    assert f"## {heading}" in markdown
