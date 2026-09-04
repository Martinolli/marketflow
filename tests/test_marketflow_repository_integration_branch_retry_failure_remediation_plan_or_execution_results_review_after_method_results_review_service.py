from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import socket

import pytest

from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_results_review_after_method_results_review_service
    as target,
)


def success() -> dict:
    return target.build_marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_results_review_after_method_results_review_v1()


def rejected(value: dict) -> None:
    with pytest.raises(target.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationPlanOrExecutionResultsReviewAfterMethodResultsReviewError):
        target.validate_marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_results_review_after_method_results_review_v1(value)


def _set_path(value: dict, path: str, replacement: object) -> None:
    current = value
    parts = path.split(".")
    for part in parts[:-1]:
        current = current[part]
    current[parts[-1]] = replacement


def test_results_review_builds_offline_without_calling_source_execution_or_network(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(socket, "create_connection", lambda *args, **kwargs: pytest.fail("network attempted"))
    monkeypatch.setattr(
        target.source,
        "execute_marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_after_method_results_review_v1",
        lambda *args, **kwargs: pytest.fail("source execution called"),
    )
    review = success()
    assert review["created_offline"] is True
    assert review["governance_only"] is True
    assert review["results_review_only"] is True


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("artifact_kind", target.ARTIFACT_KIND_SUCCESS),
        ("schema_version", target.SCHEMA_VERSION),
        ("review_status", target.REVIEW_STATUS_SUCCESS),
        ("review_scope", target.REVIEW_SCOPE),
        ("source_execution_artifact_kind", target.source.ARTIFACT_KIND_SUCCESS),
        ("source_execution_status", target.source.EXECUTION_STATUS_SUCCESS),
        ("source_execution_scope", target.source.EXECUTION_SCOPE),
        ("source_plan_execution_commit", target.SOURCE_PLAN_EXECUTION_COMMIT),
        ("source_remediation_plan_or_execution_after_method_results_review_digest", target.SOURCE_EXECUTION_DIGEST),
        ("source_targeted_remediation_plan_digest", target.SOURCE_TARGETED_PLAN_DIGEST),
        ("source_workstream_mapping_digest", target.SOURCE_WORKSTREAM_MAPPING_DIGEST),
        ("source_plan_execution_manifest_digest", target.SOURCE_PLAN_EXECUTION_MANIFEST_DIGEST),
        ("selected_remediation_plan_or_execution_package", target.SELECTED_PACKAGE),
        ("priority_1_total_nodeids", 612),
        ("top_10_count_sum", 1069),
        ("module_summary_module_count", 29),
        ("failed_or_errored_nodeids_count", 1404),
        ("source_exit_code", 1),
        ("source_stdout_byte_count", 1231380),
        ("source_stderr_byte_count", 0),
        ("source_stdout_excerpt_truncated", True),
        ("source_stderr_excerpt_truncated", False),
        ("source_redaction_checked", True),
        ("observable_failure_family_count", 4),
        ("total_observable_evidence_items", 188),
        ("source_workstream_count", 4),
        ("predictive_usefulness", "not accepted"),
        ("profitability", "not accepted"),
        ("runtime_use", "NOT_AUTHORIZED"),
        ("broker_execution", "NOT_AUTHORIZED"),
    ],
)
def test_required_scalar_fields(field: str, expected: object) -> None:
    assert success()[field] == expected


@pytest.mark.parametrize("field", sorted(target.SOURCE_BINDINGS))
def test_all_source_chain_bindings_are_preserved(field: str) -> None:
    assert success()[field] == target.SOURCE_BINDINGS[field]


@pytest.mark.parametrize("field", target.TRUE_FIELDS)
def test_results_review_facts_are_true(field: str) -> None:
    assert success()[field] is True


@pytest.mark.parametrize("field", target.FALSE_FIELDS)
def test_execution_and_downstream_authority_facts_remain_false(field: str) -> None:
    assert success()[field] is False


def test_retry_failure_context_and_priority_one_modules_are_bound() -> None:
    review = success()
    assert review["retry_failure_context"]["counts"] == {"passed": 24877, "failed": 1292, "errors": 112, "skipped": 7}
    assert review["retry_failure_context"]["first_result_authoritative"] is True
    assert [item["module_path"] for item in review["priority_1_target_modules"]] == [
        "tests/test_marketflow_signal_or_feature_generation_results_review_service.py",
        "tests/test_post_identity_freeze_registry_inventory_approval_service.py",
        "tests/test_corporate_action_authority_plan_candidate_service.py",
        "tests/test_feature_generation_results_review_redesigned_labels_service.py",
        "tests/test_marketflow_objective_label_or_target_generation_results_review_service.py",
    ]
    assert [item["failed_or_errored_nodeid_count"] for item in review["priority_1_target_modules"]] == [136, 131, 122, 112, 111]


def test_four_reviewed_families_and_four_plan_workstreams_are_exact() -> None:
    review = success()
    assert review["highest_confidence_family_ids"] == target.FAMILY_IDS
    assert all(item["observable_evidence_count"] == 47 and item["confidence"] == "HIGH" for item in review["reviewed_observable_failure_families"])
    mapping = review["workstream_mapping_results_review"]
    assert [item["source_family_id"] for item in mapping] == target.FAMILY_IDS
    assert [item["workstream_id"] for item in mapping] == [
        "assertion_value_mismatch_workstream",
        "digest_hash_boundary_workstream",
        "fixture_isolation_determinism_workstream",
        "schema_field_contract_workstream",
    ]


@pytest.mark.parametrize(
    "workstream_id",
    [
        "assertion_value_mismatch_workstream",
        "digest_hash_boundary_workstream",
        "fixture_isolation_determinism_workstream",
        "schema_field_contract_workstream",
    ],
)
def test_each_workstream_review_contains_plan_evidence_and_no_authority(workstream_id: str) -> None:
    item = success()[f"{workstream_id}_review"]
    assert item["reviewed"] is True and item["required_fields_present"] is True
    assert len(item["candidate_priority_1_modules"]) == 5
    assert item["planned_actions"] and item["verification_evidence_required"] and item["prohibited_actions"]
    assert item["future_approval_required_before_change"] is True
    for field in ("root_cause_claimed", "direct_code_remediation_recommended", "remediation_execution_authorized", "retry_readiness_created", "main_merge_readiness_created"):
        assert item[field] is False


def test_verification_future_approval_and_unsupported_claim_reviews_are_complete() -> None:
    review = success()
    assert review["verification_evidence_requirements_review"]["requirements"] == target.source.VERIFICATION_EVIDENCE_REQUIREMENTS
    assert review["verification_evidence_requirements_review"]["code_change_approval_created"] is False
    assert all(review["future_approval_boundaries_review"]["boundaries"].values())
    assert all(value is False for value in review["unsupported_claims_boundary_review"]["claims"].values())


def test_review_findings_outputs_recommendation_chain_gates_and_controls_are_exact() -> None:
    review = success()
    assert review["review_findings"] == target.REVIEW_FINDINGS and len(review["review_findings"]) == 16
    assert review["review_outputs"] == target.REVIEW_OUTPUTS and len(review["review_outputs"]) == 23
    assert review["recommendation"]["recommended_next_task"] == target.SUCCESS_NEXT_TASK
    assert review["recommendation"]["recommended_next_task_status"] == "FUTURE_CANDIDATE_NOT_CREATED"
    assert review["next_chain"] == target.SUCCESS_NEXT_CHAIN
    assert review["next_gates"] == target.NEXT_GATES
    assert review["risk_controls"] == target.RISK_CONTROLS


def test_success_digests_and_checklist_are_deterministic() -> None:
    first, second = success(), success()
    for key in (target.RESULTS_REVIEW_DIGEST_KEY, target.TARGETED_PLAN_REVIEW_DIGEST_KEY, target.WORKSTREAM_MAPPING_REVIEW_DIGEST_KEY, target.RESULTS_REVIEW_MANIFEST_DIGEST_KEY):
        assert first[key] == second[key]
        assert len(first[key]) == 64
    assert first["summary"]["passed_checks"] == first["summary"]["total_checks"]
    assert first["summary"]["failed_checks"] == first["summary"]["blocker_count"] == 0
    assert all(set(item) == {"check_id", "status", "expected", "actual", "severity", "message"} for item in first["checklist"])


def test_invalid_source_execution_returns_a_valid_blocked_artifact() -> None:
    review = target.build_marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_results_review_after_method_results_review_v1(source_execution={})
    assert review["artifact_kind"] == target.ARTIFACT_KIND_BLOCKED
    assert review["review_status"] == target.REVIEW_STATUS_BLOCKED
    assert review["remediation_plan_or_execution_results_review_after_method_results_review_created"] is True
    assert review["remediation_plan_or_execution_results_review_after_method_results_review_ready"] is False
    assert review["review_outputs"] == []
    assert len(review[target.BLOCKED_MANIFEST_DIGEST_KEY]) == 64
    assert target.validate_marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_results_review_after_method_results_review_v1(review)["failed_checks"] == 0


@pytest.mark.parametrize(
    ("path", "replacement"),
    [
        ("artifact_kind", "WRONG"),
        ("review_status", "WRONG"),
        ("review_scope", "WRONG"),
        ("selected_remediation_plan_or_execution_package", "WRONG"),
        ("source_plan_execution_commit", "0" * 40),
        ("source_remediation_plan_or_execution_after_method_results_review_digest", "0" * 64),
        ("source_targeted_remediation_plan_digest", "0" * 64),
        ("source_workstream_mapping_digest", "0" * 64),
        ("source_plan_execution_manifest_digest", "0" * 64),
        ("source_remediation_plan_or_execution_approval_after_method_results_review_digest", "0" * 64),
        ("source_remediation_plan_or_execution_candidate_after_method_results_review_operator_review_digest", "0" * 64),
        ("source_remediation_plan_or_execution_candidate_after_method_results_review_digest", "0" * 64),
        ("source_remediation_or_method_results_review_after_diagnostic_capture_digest", "0" * 64),
        ("source_failure_family_classification_review_digest", "0" * 64),
        ("source_bounded_excerpt_analysis_review_digest", "0" * 64),
        ("source_results_review_manifest_digest", "0" * 64),
        ("source_remediation_or_method_execution_after_diagnostic_capture_digest", "0" * 64),
        ("source_failure_family_classification_digest", "0" * 64),
        ("source_durable_receipt_path", ""),
        ("source_targeted_diagnostic_output_capture_execution_blocked_reason", "WRONG"),
        ("source_planning_execution_digest", "0" * 64),
        ("source_complete_29_row_binding_digest", "0" * 64),
        ("source_recovery_detail_digest", "0" * 64),
        ("source_module_grouping_digest", "0" * 64),
        ("retry_failure_context", {}),
        ("priority_1_target_modules", []),
        ("priority_1_total_nodeids", 611),
        ("top_10_count_sum", 1068),
        ("module_summary_module_count", 28),
        ("failed_or_errored_nodeids_count", 1403),
        ("source_exit_code", 0),
        ("source_stdout_sha256", "0" * 64),
        ("source_stdout_byte_count", 1),
        ("observable_failure_family_count", 3),
        ("highest_confidence_family_ids", []),
        ("direct_remediation_ready", True),
        ("retry_ready", True),
        ("main_merge_ready", True),
        ("source_workstream_count", 3),
        ("targeted_remediation_plan_results_review.root_cause_claimed", True),
        ("assertion_value_mismatch_workstream_review.remediation_execution_authorized", True),
        ("verification_evidence_requirements_review", None),
        ("future_approval_boundaries_review", None),
        ("review_findings", {}),
        ("review_outputs", []),
        ("recommendation", {}),
        ("next_chain", []),
        ("next_gates", []),
        ("risk_controls", []),
        (target.RESULTS_REVIEW_DIGEST_KEY, "0" * 64),
        (target.TARGETED_PLAN_REVIEW_DIGEST_KEY, "0" * 64),
        (target.WORKSTREAM_MAPPING_REVIEW_DIGEST_KEY, "0" * 64),
        (target.RESULTS_REVIEW_MANIFEST_DIGEST_KEY, "0" * 64),
    ],
)
def test_validator_rejects_bound_evidence_review_or_digest_tampering(path: str, replacement: object) -> None:
    review = success()
    _set_path(review, path, replacement)
    rejected(review)


@pytest.mark.parametrize("field", target.FALSE_FIELDS)
def test_validator_rejects_any_closed_boundary_becoming_true(field: str) -> None:
    review = success()
    review[field] = True
    rejected(review)


def test_validator_accepts_success_artifact() -> None:
    validation = target.validate_marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_results_review_after_method_results_review_v1(success())
    assert validation["failed_checks"] == validation["blocker_count"] == 0
    assert validation["passed_checks"] == validation["total_checks"]


def test_writer_uses_isolated_directory_once_and_protects_runtime_paths(tmp_path: Path) -> None:
    review = target.write_marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_results_review_after_method_results_review_v1(tmp_path)
    output = tmp_path / "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_PLAN_OR_EXECUTION_RESULTS_REVIEW_AFTER_METHOD_RESULTS_REVIEW_STATUS.md"
    assert output.is_file() and review["artifact_kind"] == target.ARTIFACT_KIND_SUCCESS
    with pytest.raises(target.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationPlanOrExecutionResultsReviewAfterMethodResultsReviewError):
        target.write_marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_results_review_after_method_results_review_v1(tmp_path)
    with pytest.raises(target.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationPlanOrExecutionResultsReviewAfterMethodResultsReviewError):
        target.write_marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_results_review_after_method_results_review_v1(tmp_path / ".pytest_cache")


def test_markdown_includes_all_required_sections() -> None:
    markdown = target.build_marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_results_review_after_method_results_review_markdown_v1(success())
    for heading in (
        "Source Plan Execution", "Source Targeted Remediation Plan", "Source Workstream Mapping", "Source Approval",
        "Source Operator Review and Candidate", "Source Method Results Review", "Source Method Execution",
        "Source Failure-Family Classification", "Source Diagnostic Results Review", "Source Controlled Recapture Execution",
        "Source Durable Receipt", "Source Receipt Loss History", "Source Planning and Detail Binding Evidence",
        "Retry Failure Context", "Review Scope", "Selected Remediation Plan or Execution Package",
        "Priority 1 Target Modules", "Diagnostic Capture Evidence Summary", "Reviewed Observable Failure Families",
        "Targeted Remediation Plan Results Review", "Workstream Mapping Results Review",
        "Assertion/Value Mismatch Workstream Review", "Digest/Hash Boundary Workstream Review",
        "Fixture Isolation and Determinism Workstream Review", "Schema/Field Contract Workstream Review",
        "Verification Evidence Requirements Review", "Future Approval Boundaries Review", "Unsupported Claims Boundary",
        "Success or Blocked Disposition", "Review Findings", "Recommendation", "Next Chain", "Next Gates",
        "Risk Controls", "Authority Boundaries", "Checklist Summary", "Guardrails",
    ):
        assert f"## {heading}" in markdown
