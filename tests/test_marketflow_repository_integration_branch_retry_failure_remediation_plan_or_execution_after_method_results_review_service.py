from copy import deepcopy

import pytest

from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_after_method_results_review_service
    as target,
)


TIMESTAMP = "2026-08-23T00:00:00Z"


def success():
    return target.execute_marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_after_method_results_review_v1(
        run_timestamp_utc=TIMESTAMP
    )


def rejected(value):
    with pytest.raises(target.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationPlanOrExecutionAfterMethodResultsReviewError):
        target.validate_marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_after_method_results_review_v1(value)


def test_execution_generates_only_the_approved_targeted_plan(monkeypatch):
    monkeypatch.setattr(target.approval_source, "build_marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_approval_after_method_results_review_v1", lambda **kwargs: (_ for _ in ()).throw(AssertionError("source builder called")))
    execution = success()
    assert execution["artifact_kind"] == target.ARTIFACT_KIND_SUCCESS
    assert execution["execution_status"] == target.EXECUTION_STATUS_SUCCESS
    assert execution["execution_scope"] == target.EXECUTION_SCOPE
    assert execution["selected_remediation_plan_or_execution_package"] == target.SELECTED_PACKAGE
    assert execution["targeted_remediation_plan"]["plan_status"] == "GENERATED_PLAN_ONLY_NOT_REMEDIATION"
    assert execution["summary"]["failed_checks"] == 0


def test_source_approval_and_method_chain_are_bound():
    execution = success()
    assert execution["source_remediation_plan_or_execution_approval_after_method_results_review_commit"] == target.SOURCE_APPROVAL_COMMIT
    assert execution["source_remediation_plan_or_execution_approval_after_method_results_review_digest"] == target.SOURCE_APPROVAL_DIGEST
    assert execution["source_remediation_plan_or_execution_candidate_after_method_results_review_operator_review_digest"] == target.approval_source.SOURCE_OPERATOR_REVIEW_DIGEST
    assert execution["source_remediation_or_method_results_review_after_diagnostic_capture_digest"] == "0d498fe7db9110946ffdbd5aea2eb9f129643c5d309b3b2dffd2db4030a4aa2f"
    assert execution["source_remediation_or_method_execution_after_diagnostic_capture_digest"] == "1670927267782671afaa7aa784604580fd3c1efaf5331ab41585012ff8963d88"
    assert execution["source_durable_receipt_path"].endswith("EXECUTION_RECEIPT_V1.json")


def test_four_workstreams_map_reviewed_families_without_claims():
    execution = success()
    assert execution["workstream_count"] == 4
    assert [item["source_family_id"] for item in execution["workstreams"]] == target.FAMILY_IDS
    for workstream in execution["workstreams"]:
        assert workstream["source_observable_evidence_count"] == 47
        assert workstream["source_family_confidence"] == "HIGH"
        assert len(workstream["candidate_priority_1_modules"]) == 5
        assert workstream["root_cause_claimed"] is False
        assert workstream["direct_code_remediation_recommended"] is False
        assert workstream["remediation_execution_authorized"] is False
        assert workstream["retry_readiness_created"] is False


def test_plan_verification_and_future_approval_boundaries_are_complete():
    execution = success()
    assert len(execution["verification_evidence_requirements"]) == 6
    assert all(execution["future_approval_boundaries"].values())
    assert all(value is False for value in execution["unsupported_claims_boundary"].values())
    assert execution["outputs"] == target.SUCCESS_OUTPUTS
    assert execution["recommended_next_task"] == target.SUCCESS_NEXT_TASK


@pytest.mark.parametrize("field", target.SUCCESS_TRUE_FIELDS)
def test_success_facts_are_true(field):
    assert success()[field] is True


@pytest.mark.parametrize("field", target.COMMON_FALSE_FIELDS)
def test_execution_and_downstream_authority_facts_remain_false(field):
    assert success()[field] is False


def test_all_success_digests_are_deterministic():
    first, second = success(), success()
    for key in (target.EXECUTION_DIGEST_KEY, target.TARGETED_PLAN_DIGEST_KEY, target.WORKSTREAM_MAPPING_DIGEST_KEY, target.MANIFEST_DIGEST_KEY):
        assert first[key] == second[key]
        assert len(first[key]) == 64


def test_invalid_source_approval_returns_valid_blocked_artifact():
    execution = target.execute_marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_after_method_results_review_v1(
        source_approval={}, run_timestamp_utc=TIMESTAMP
    )
    assert execution["artifact_kind"] == target.ARTIFACT_KIND_BLOCKED
    assert execution["execution_status"] == target.EXECUTION_STATUS_BLOCKED
    assert execution["blocked_reason"]
    assert execution["workstreams"] == []
    assert len(execution[target.BLOCKED_MANIFEST_DIGEST_KEY]) == 64
    assert target.validate_marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_after_method_results_review_v1(execution)["failed_checks"] == 0


@pytest.mark.parametrize("field", [
    "artifact_kind", "execution_status", "execution_scope", "selected_remediation_plan_or_execution_package",
    "source_remediation_plan_or_execution_approval_after_method_results_review_digest",
    "source_remediation_plan_or_execution_candidate_after_method_results_review_operator_review_digest",
    "source_remediation_or_method_results_review_after_diagnostic_capture_digest",
    "source_remediation_or_method_execution_after_diagnostic_capture_digest", "source_stdout_sha256",
    "priority_1_target_modules", "reviewed_observable_failure_families", "targeted_remediation_plan",
    "verification_evidence_requirements", "future_approval_boundaries", "risk_controls",
])
def test_validator_rejects_bound_evidence_or_plan_tampering(field):
    execution = success()
    execution[field] = None
    rejected(execution)


@pytest.mark.parametrize("field", target.COMMON_FALSE_FIELDS[:24])
def test_validator_rejects_closed_boundary_becoming_true(field):
    execution = success()
    execution[field] = True
    rejected(execution)


def test_writer_generates_status_once_and_protects_runtime_directories(tmp_path):
    execution = target.write_marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_after_method_results_review_v1(
        tmp_path, run_timestamp_utc=TIMESTAMP
    )
    path = tmp_path / "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_PLAN_OR_EXECUTION_AFTER_METHOD_RESULTS_REVIEW_STATUS.md"
    assert path.is_file()
    assert execution["artifact_kind"] == target.ARTIFACT_KIND_SUCCESS
    with pytest.raises(target.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationPlanOrExecutionAfterMethodResultsReviewError):
        target.write_marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_after_method_results_review_v1(tmp_path, run_timestamp_utc=TIMESTAMP)
    with pytest.raises(target.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationPlanOrExecutionAfterMethodResultsReviewError):
        target.write_marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_after_method_results_review_v1(tmp_path / ".pytest_cache", run_timestamp_utc=TIMESTAMP)


def test_markdown_contains_required_sections():
    markdown = target.build_marketflow_repository_integration_branch_retry_failure_remediation_plan_or_execution_after_method_results_review_markdown_v1(success())
    for heading in ("Source Approval", "Source Method Results Review", "Targeted Remediation Plan", "Workstream Mapping", "Assertion/Value Mismatch Workstream", "Digest/Hash Boundary Workstream", "Fixture Isolation and Determinism Workstream", "Schema/Field Contract Workstream", "Verification Evidence Requirements", "Future Approval Boundaries", "Unsupported Claims Boundary", "Risk Controls", "Guardrails"):
        assert f"## {heading}" in markdown
