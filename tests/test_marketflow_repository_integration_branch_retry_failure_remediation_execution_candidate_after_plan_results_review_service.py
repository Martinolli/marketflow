from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import socket

import pytest

from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_remediation_execution_candidate_after_plan_results_review_service
    as target,
)


def valid_candidate() -> dict:
    return target.build_marketflow_repository_integration_branch_retry_failure_remediation_execution_candidate_after_plan_results_review_v1()


def assert_rejected(candidate: dict) -> None:
    with pytest.raises(target.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionCandidateAfterPlanResultsReviewError):
        target.validate_marketflow_repository_integration_branch_retry_failure_remediation_execution_candidate_after_plan_results_review_v1(candidate)


def test_candidate_builds_offline_without_source_builders_file_reads_or_network(monkeypatch: pytest.MonkeyPatch) -> None:
    def forbidden(*args, **kwargs):
        raise AssertionError("candidate attempted prohibited source execution or file/network access")

    monkeypatch.setattr(target.source, "build_marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_results_review_after_method_results_review_v1", forbidden)
    monkeypatch.setattr(Path, "read_text", forbidden)
    monkeypatch.setattr(Path, "read_bytes", forbidden)
    monkeypatch.setattr(socket, "create_connection", forbidden)
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
        ("source_plan_results_review_artifact_kind", target.source.ARTIFACT_KIND_SUCCESS),
        ("source_plan_results_review_status", target.source.REVIEW_STATUS_SUCCESS),
        ("source_plan_results_review_scope", target.source.REVIEW_SCOPE),
        ("source_plan_results_review_commit", target.SOURCE_PLAN_RESULTS_REVIEW_COMMIT),
        ("source_remediation_plan_or_execution_results_review_after_method_results_review_digest", target.SOURCE_PLAN_RESULTS_REVIEW_DIGEST),
        ("source_targeted_remediation_plan_review_digest", target.SOURCE_TARGETED_PLAN_REVIEW_DIGEST),
        ("source_workstream_mapping_review_digest", target.SOURCE_WORKSTREAM_MAPPING_REVIEW_DIGEST),
        ("source_plan_results_review_manifest_digest", target.SOURCE_PLAN_RESULTS_REVIEW_MANIFEST_DIGEST),
        ("source_plan_execution_commit", target.SOURCE_PLAN_EXECUTION_COMMIT),
        ("source_remediation_plan_or_execution_after_method_results_review_digest", target.SOURCE_PLAN_EXECUTION_DIGEST),
        ("source_targeted_remediation_plan_digest", target.SOURCE_TARGETED_REMEDIATION_PLAN_DIGEST),
        ("source_workstream_mapping_digest", target.SOURCE_WORKSTREAM_MAPPING_DIGEST),
        ("source_plan_execution_manifest_digest", target.SOURCE_PLAN_EXECUTION_MANIFEST_DIGEST),
        ("selected_source_plan_package", target.SELECTED_SOURCE_PLAN_PACKAGE),
        ("recommended_remediation_execution_package", target.RECOMMENDED_PACKAGE),
        ("recommended_next_task", target.RECOMMENDED_NEXT_TASK),
        ("priority_1_total_nodeids", 612),
        ("top_10_count_sum", 1069),
        ("module_summary_module_count", 29),
        ("failed_or_errored_nodeids_count", 1404),
        ("source_exit_code", 1),
        ("source_stdout_byte_count", 1231380),
        ("source_stderr_byte_count", 0),
        ("observable_failure_family_count", 4),
        ("total_observable_evidence_items", 188),
        ("source_workstream_count", 4),
        ("predictive_usefulness", "not accepted"),
        ("profitability", "not accepted"),
        ("runtime_use", "NOT_AUTHORIZED"),
        ("broker_execution", "NOT_AUTHORIZED"),
    ],
)
def test_required_identity_source_and_scalar_fields(field: str, expected: object) -> None:
    assert valid_candidate()[field] == expected


@pytest.mark.parametrize("field", sorted(target._source_bindings()))
def test_all_source_evidence_bindings_are_exact(field: str) -> None:
    assert valid_candidate()[field] == target._source_bindings()[field]


def test_retry_failure_priority_modules_and_diagnostic_metadata_are_bound() -> None:
    candidate = valid_candidate()
    assert candidate["retry_failure_context"]["counts"] == {"passed": 24877, "failed": 1292, "errors": 112, "skipped": 7}
    assert candidate["retry_failure_context"]["first_result_authoritative"] is True
    assert [item["module_path"] for item in candidate["priority_1_target_modules"]] == [
        "tests/test_marketflow_signal_or_feature_generation_results_review_service.py",
        "tests/test_post_identity_freeze_registry_inventory_approval_service.py",
        "tests/test_corporate_action_authority_plan_candidate_service.py",
        "tests/test_feature_generation_results_review_redesigned_labels_service.py",
        "tests/test_marketflow_objective_label_or_target_generation_results_review_service.py",
    ]
    assert [item["failed_or_errored_nodeid_count"] for item in candidate["priority_1_target_modules"]] == [136, 131, 122, 112, 111]
    assert candidate["source_exit_code_is_diagnostic_only"] is True
    assert candidate["source_stdout_sha256"] == "b5fb29f6cf8af77700da74c72f08b854c33bc1ad30c79c309c6eefee70171d2a"
    assert candidate["source_stderr_sha256"] == "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    assert candidate["source_stdout_excerpt_truncated"] is True
    assert candidate["source_stderr_excerpt_truncated"] is False
    assert candidate["source_redaction_checked"] is True


def test_reviewed_plan_families_and_workstreams_are_bound_without_claims() -> None:
    candidate = valid_candidate()
    assert candidate["highest_confidence_family_ids"] == target.source.FAMILY_IDS
    assert all(item["observable_evidence_count"] == 47 and item["confidence"] == "HIGH" for item in candidate["reviewed_observable_failure_families"])
    workstreams = candidate["reviewed_workstreams"]
    assert len(workstreams) == 4
    assert [item["source_family_id"] for item in workstreams] == target.source.FAMILY_IDS
    for item in workstreams:
        assert item["reviewed"] is True and item["required_fields_present"] is True
        for field in ("root_cause_claimed", "direct_code_remediation_recommended", "remediation_execution_authorized", "retry_readiness_created", "main_merge_readiness_created"):
            assert item[field] is False
    assert candidate["reviewed_targeted_remediation_plan"]["plan_only"] is True


def test_twelve_packages_are_reviewable_unselected_and_five_are_blocked() -> None:
    candidate = valid_candidate()
    packages = candidate["proposed_remediation_execution_packages"]
    assert packages == target.PROPOSED_PACKAGES
    assert len(packages) == 12
    assert sum(item["status"] == "BLOCKED_NOT_ALLOWED" for item in packages) == 5
    assert packages[0]["package_id"] == target.RECOMMENDED_PACKAGE
    assert packages[0]["status"] == "RECOMMENDED_FOR_OPERATOR_REVIEW_NOT_SELECTED"
    assert all(item["selected"] is item["approved"] is item["authorized"] is item["executed"] is False for item in packages)
    assert candidate["recommended_package"] == packages[0]


def test_requirements_plan_outputs_non_goals_chain_gates_and_risk_controls_are_exact() -> None:
    candidate = valid_candidate()
    assert candidate["future_remediation_execution_requirements"] == target.FUTURE_REQUIREMENTS
    assert len(target.FUTURE_REQUIREMENTS) == 46
    assert all(item["required"] is True and item["status"] == "REQUIRED_FOR_FUTURE_REMEDIATION_EXECUTION" and item["execution_status"] == "NOT_EXECUTED" for item in target.FUTURE_REQUIREMENTS)
    assert candidate["future_remediation_execution_plan"] == target.FUTURE_PLAN and len(target.FUTURE_PLAN) == 14
    assert all(item["status"] == "PLANNED_NOT_EXECUTED" for item in target.FUTURE_PLAN)
    assert candidate["planned_outputs"] == target.PLANNED_OUTPUTS and len(target.PLANNED_OUTPUTS) == 20
    assert all(item["status"] == "PLANNED_NOT_GENERATED" for item in target.PLANNED_OUTPUTS)
    assert candidate["non_goals"] == target.NON_GOALS and len(target.NON_GOALS) == 55
    assert candidate["next_chain"] == target.NEXT_CHAIN and len(target.NEXT_CHAIN) == 9
    assert candidate["next_gates"] == target.NEXT_GATES and len(target.NEXT_GATES) == 9
    assert candidate["risk_controls"] == target.RISK_CONTROLS and len(target.RISK_CONTROLS) == 107


@pytest.mark.parametrize("field", target.TRUE_FIELDS)
def test_required_candidate_facts_are_true(field: str) -> None:
    assert valid_candidate()[field] is True


@pytest.mark.parametrize("field", target.FALSE_FIELDS)
def test_closed_authority_boundaries_are_false(field: str) -> None:
    assert valid_candidate()[field] is False


def test_checklist_summary_and_digest_are_deterministic() -> None:
    first, second = valid_candidate(), valid_candidate()
    assert first[target.CANDIDATE_DIGEST_KEY] == second[target.CANDIDATE_DIGEST_KEY]
    assert len(first[target.CANDIDATE_DIGEST_KEY]) == 64
    assert first["summary"]["passed_checks"] == first["summary"]["total_checks"] == len(first["checklist"])
    assert first["summary"]["failed_checks"] == first["summary"]["blocker_count"] == 0
    assert all(set(item) == {"check_id", "status", "expected", "actual", "severity", "message"} for item in first["checklist"])


def test_validator_accepts_valid_candidate() -> None:
    result = target.validate_marketflow_repository_integration_branch_retry_failure_remediation_execution_candidate_after_plan_results_review_v1(valid_candidate())
    assert result["failed_checks"] == result["blocker_count"] == 0
    assert result["passed_checks"] == result["total_checks"]


@pytest.mark.parametrize(
    "field",
    [
        "artifact_kind", "candidate_status", "candidate_scope", "source_plan_results_review_commit",
        "source_remediation_plan_or_execution_results_review_after_method_results_review_digest",
        "source_targeted_remediation_plan_review_digest", "source_workstream_mapping_review_digest",
        "source_plan_results_review_manifest_digest", "source_plan_execution_commit",
        "source_remediation_plan_or_execution_after_method_results_review_digest",
        "source_targeted_remediation_plan_digest", "source_workstream_mapping_digest",
        "source_plan_execution_manifest_digest", "selected_source_plan_package",
        "source_remediation_plan_or_execution_approval_after_method_results_review_digest",
        "source_remediation_plan_or_execution_candidate_after_method_results_review_operator_review_digest",
        "source_remediation_plan_or_execution_candidate_after_method_results_review_digest",
        "source_remediation_or_method_results_review_after_diagnostic_capture_digest",
        "source_remediation_or_method_execution_after_diagnostic_capture_digest",
        "source_receipt_recovery_or_recapture_results_review_digest",
        "source_receipt_recovery_or_recapture_execution_digest",
        "source_receipt_recovery_or_recapture_receipt_digest", "source_durable_receipt_path",
        "source_targeted_diagnostic_output_capture_execution_failure_diagnosis_digest",
        "source_targeted_diagnostic_output_capture_execution_digest",
        "source_targeted_diagnostic_output_capture_execution_blocked_reason", "source_primary_failure_class",
        "source_secondary_failure_class", "source_targeted_diagnostic_output_capture_approval_digest",
        "source_planning_execution_digest", "source_complete_29_row_binding_digest", "source_materialized_payload_digest",
        "source_recovery_detail_digest", "source_module_grouping_digest", "retry_failure_context",
        "priority_1_target_modules", "source_stdout_sha256", "source_stdout_byte_count",
        "reviewed_observable_failure_families", "reviewed_targeted_remediation_plan", "reviewed_workstreams",
        "proposed_remediation_execution_packages", "recommended_remediation_execution_package",
        "future_remediation_execution_requirements", "future_remediation_execution_plan", "planned_outputs",
        "non_goals", "next_chain", "next_gates", "risk_controls", target.CANDIDATE_DIGEST_KEY,
    ],
)
def test_validator_rejects_evidence_package_plan_or_digest_tampering(field: str) -> None:
    candidate = valid_candidate()
    candidate[field] = None
    assert_rejected(candidate)


@pytest.mark.parametrize("field", target.FALSE_FIELDS)
def test_validator_rejects_any_closed_boundary_becoming_true(field: str) -> None:
    candidate = valid_candidate()
    candidate[field] = True
    assert_rejected(candidate)


def test_writer_uses_isolated_directory_once_and_rejects_protected_paths(tmp_path: Path) -> None:
    candidate = target.write_marketflow_repository_integration_branch_retry_failure_remediation_execution_candidate_after_plan_results_review_v1(tmp_path)
    output = tmp_path / "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_CANDIDATE_AFTER_PLAN_RESULTS_REVIEW_STATUS.md"
    assert output.is_file() and candidate["artifact_kind"] == target.ARTIFACT_KIND
    with pytest.raises(target.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionCandidateAfterPlanResultsReviewError):
        target.write_marketflow_repository_integration_branch_retry_failure_remediation_execution_candidate_after_plan_results_review_v1(tmp_path)
    with pytest.raises(target.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionCandidateAfterPlanResultsReviewError):
        target.write_marketflow_repository_integration_branch_retry_failure_remediation_execution_candidate_after_plan_results_review_v1(tmp_path / ".pytest_cache")


def test_markdown_contains_required_sections() -> None:
    markdown = target.build_marketflow_repository_integration_branch_retry_failure_remediation_execution_candidate_after_plan_results_review_markdown_v1(valid_candidate())
    for heading in (
        "Source Plan Results Review", "Source Plan Execution", "Source Targeted Remediation Plan",
        "Source Workstream Mapping", "Source Approval", "Source Operator Review and Candidate",
        "Source Method Results Review", "Source Method Execution", "Source Failure-Family Classification",
        "Source Diagnostic Results Review", "Source Controlled Recapture Execution", "Source Durable Receipt",
        "Source Receipt Loss History", "Source Planning and Detail Binding Evidence", "Retry Failure Context",
        "Candidate Scope", "Priority 1 Target Modules", "Diagnostic Capture Evidence Summary",
        "Reviewed Observable Failure Families", "Reviewed Workstreams", "Candidate Philosophy",
        "Proposed Remediation Execution Packages", "Recommended Package", "Future Remediation Execution Requirements",
        "Future Remediation Execution Plan", "Planned Outputs", "Non-Goals", "Next Chain", "Next Gates",
        "Risk Controls", "Authority Boundaries", "Checklist Summary", "Guardrails",
    ):
        assert f"## {heading}" in markdown
