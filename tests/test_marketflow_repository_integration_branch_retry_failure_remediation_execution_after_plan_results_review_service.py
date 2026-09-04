from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import pytest

from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_remediation_execution_after_plan_results_review_service
    as service,
)


def _record(**updates):
    record = {
        "change_id": "change-001",
        "path": "marketflow/services/example.py",
        "change_type": "modified",
        "workstream_ids": ["schema_field_contract_workstream"],
        "source_authority": "REVIEWED_ARTIFACT_FIELD_CONTRACT",
        "description": "Restore a source-authorized required field.",
        "pre_change_sha256": "1" * 64,
        "post_change_sha256": "2" * 64,
        "verification_evidence": "Focused contract test passed.",
        "focused_validation_covered": True,
        "expected_digest_updated": False,
        "digest_update_authority": "NOT_APPLICABLE",
        "test_modified": False,
        "test_change_authority": "NOT_APPLICABLE",
        "production_code_modified": True,
        "production_change_authority": "PLAN_DERIVED_SOURCE_AUTHORITY_RECORDED",
        "root_cause_claimed": False,
        "retry_success_claimed": False,
        "main_merge_readiness_claimed": False,
    }
    record.update(updates)
    return record


def _validation(**updates):
    validation = {
        "command": "python -m pytest -p no:cacheprovider -q tests/test_example.py",
        "exit_code": 0,
        "duration_seconds": 1.25,
        "stdout_byte_count": 18,
        "stderr_byte_count": 0,
        "stdout_sha256": "3" * 64,
        "stderr_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        "bounded_stdout_excerpt": "1 passed",
        "bounded_stderr_excerpt": None,
        "cacheprovider_disabled": True,
        "focused_validation_performed": True,
        "focused_validation_passed": True,
    }
    validation.update(updates)
    return validation


@pytest.fixture()
def success():
    return service.execute_marketflow_repository_integration_branch_retry_failure_remediation_execution_after_plan_results_review_v1(
        repository_root=Path("."),
        run_timestamp_utc="2026-08-23T00:00:00Z",
        remediation_change_records=[_record()],
        focused_validation_summary=_validation(),
    )


@pytest.fixture()
def blocked():
    return service.execute_marketflow_repository_integration_branch_retry_failure_remediation_execution_after_plan_results_review_v1(
        repository_root=Path("."), run_timestamp_utc="2026-08-23T00:00:00Z"
    )


def test_success_artifact_builds_with_injected_evidence(success):
    assert success["artifact_kind"] == service.SUCCESS_ARTIFACT_KIND
    assert success["execution_status"] == service.SUCCESS_STATUS
    assert success["remediation_execution_performed"] is True


def test_blocked_artifact_builds_without_change_authority(blocked):
    assert blocked["artifact_kind"] == service.BLOCKED_ARTIFACT_KIND
    assert blocked["execution_status"] == service.BLOCKED_STATUS
    assert blocked["blocked_reason"] == service.BLOCKED_NO_CHANGE_AUTHORITY


def test_scope_and_selected_package_are_fixed(success, blocked):
    for artifact in (success, blocked):
        assert artifact["execution_scope"] == service.EXECUTION_SCOPE
        assert artifact["selected_remediation_execution_package"] == service.SELECTED_PACKAGE


def test_source_approval_operator_review_and_candidate_are_bound(success):
    assert success["source_remediation_execution_approval_after_plan_results_review_commit"] == service.SOURCE_APPROVAL_COMMIT
    assert success["source_remediation_execution_approval_after_plan_results_review_digest"] == service.SOURCE_APPROVAL_DIGEST
    assert success["source_remediation_execution_candidate_after_plan_results_review_operator_review_digest"] == service.approval.SOURCE_OPERATOR_REVIEW_DIGEST
    assert success["source_remediation_execution_candidate_after_plan_results_review_digest"] == "6869b7642d8f90fd0273a7cbfdd069af85b23518778100ae19f3ebb6060fe4bd"


def test_plan_method_diagnostic_and_recovery_sources_are_bound(success):
    expected = service.SOURCE_BINDINGS
    for key in (
        "source_remediation_plan_or_execution_results_review_after_method_results_review_digest",
        "source_targeted_remediation_plan_review_digest",
        "source_workstream_mapping_review_digest",
        "source_remediation_plan_or_execution_after_method_results_review_digest",
        "source_targeted_remediation_plan_digest",
        "source_workstream_mapping_digest",
        "source_remediation_or_method_results_review_after_diagnostic_capture_digest",
        "source_remediation_or_method_execution_after_diagnostic_capture_digest",
        "source_receipt_recovery_or_recapture_results_review_digest",
        "source_receipt_recovery_or_recapture_execution_digest",
        "source_receipt_recovery_or_recapture_receipt_digest",
        "source_planning_execution_digest",
        "source_complete_29_row_binding_digest",
        "source_recovery_detail_digest",
        "source_module_grouping_digest",
    ):
        assert success[key] == expected[key]


def test_durable_receipt_path_is_bound_but_not_parsed(success):
    assert success["source_durable_receipt_path"].endswith("RECEIPT_V1.json")
    assert success["diagnostic_receipt_parsed_in_execution"] is False


def test_retry_failure_counts_and_priority_1_facts_are_bound(success):
    assert success["retry_failure_context"]["counts"] == {"passed": 24877, "failed": 1292, "errors": 112, "skipped": 7}
    assert len(success["priority_1_target_modules"]) == 5
    assert success["priority_1_total_nodeids"] == 612
    assert success["top_10_count_sum"] == 1069
    assert success["module_summary_module_count"] == 29
    assert success["failed_or_errored_nodeids_count"] == 1404


def test_diagnostic_stream_facts_are_bound_as_diagnostic_only(success):
    assert success["source_exit_code"] == 1
    assert success["source_exit_code_is_diagnostic_only"] is True
    assert success["source_stdout_byte_count"] == 1231380
    assert success["source_stderr_byte_count"] == 0
    assert success["source_stdout_excerpt_truncated"] is True
    assert success["source_stderr_excerpt_truncated"] is False
    assert success["source_redaction_checked"] is True


def test_four_observable_families_and_workstreams_are_bound(success):
    assert {item["family_id"] for item in success["reviewed_observable_failure_families"]} == set(service.FAMILY_IDS)
    assert all(item["confidence"] == "HIGH" and item["observable_evidence_count"] == 47 for item in success["reviewed_observable_failure_families"])
    assert {item["workstream_id"] for item in success["reviewed_workstreams"]} == set(service.WORKSTREAM_IDS)
    assert success["observable_failure_family_count"] == success["source_workstream_count"] == 4
    assert success["total_observable_evidence_items"] == 188


def test_success_records_inventory_snapshots_mapping_and_verification(success):
    assert success["file_impact_inventory_created"] is True
    assert success["pre_change_snapshot_created"] is True
    assert success["change_records_created"] is True
    assert success["post_change_snapshot_created"] is True
    assert success["verification_evidence_recorded"] is True
    assert success["focused_validation_performed"] is True
    assert success["focused_validation_passed"] is True
    assert success["workstream_to_change_mapping"][3]["change_ids"] == ["change-001"]


def test_blocked_records_unchanged_candidate_inventory_and_pre_snapshot(blocked):
    assert len(blocked["file_impact_inventory"]) == 10
    assert len(blocked["pre_change_snapshot"]) == 10
    assert blocked["change_records"] == []
    assert blocked["post_change_snapshot"] == []
    assert all(item["change_type"] == "unchanged_candidate" and item["changed"] is False for item in blocked["file_impact_inventory"])


def test_success_actual_change_booleans_and_gates(success):
    assert success["production_code_modified"] is True
    assert success["existing_tests_modified"] is False
    assert success["expected_digests_updated"] is False
    assert success["patch_generated"] is success["patch_applied"] is True
    assert success["ready_for_remediation_execution_results_review"] is True
    assert success["ready_for_retry_candidate"] is success["ready_for_main_merge_approval"] is False


def test_success_outputs_recommendation_chain_gates_and_risks(success):
    assert len(success["outputs"]) == len(service.SUCCESS_OUTPUT_NAMES)
    assert {item["status"] for item in success["outputs"]} == {"GENERATED_CONTROLLED_PLAN_DERIVED_REMEDIATION_EXECUTION_ONLY"}
    assert success["recommended_next_task"] == service.SUCCESS_NEXT_TASK
    assert success["next_chain"] and success["next_gates"] and success["risk_controls"]


def test_blocked_recommendation_and_gate_state(blocked):
    assert blocked["recommended_next_task"] == service.BLOCKED_NEXT_TASK
    assert blocked["ready_for_remediation_execution_results_review"] is False
    assert blocked["outputs"] == []


def test_success_and_blocked_checklists_pass(success, blocked):
    for artifact in (success, blocked):
        assert artifact["summary"]["total_checks"] == len(artifact["checklist"])
        assert artifact["summary"]["passed_checks"] == len(artifact["checklist"])
        assert artifact["summary"]["failed_checks"] == artifact["summary"]["blocker_count"] == 0


def test_success_digests_are_deterministic():
    kwargs = {
        "repository_root": Path("."), "run_timestamp_utc": "2026-08-23T00:00:00Z",
        "remediation_change_records": [_record()], "focused_validation_summary": _validation(),
    }
    left = service.execute_marketflow_repository_integration_branch_retry_failure_remediation_execution_after_plan_results_review_v1(**kwargs)
    right = service.execute_marketflow_repository_integration_branch_retry_failure_remediation_execution_after_plan_results_review_v1(**kwargs)
    for key in (
        service.EXECUTION_DIGEST_KEY, service.FILE_IMPACT_INVENTORY_DIGEST_KEY,
        service.CHANGE_RECORDS_DIGEST_KEY, service.VALIDATION_REPORT_DIGEST_KEY, service.MANIFEST_DIGEST_KEY,
    ):
        assert left[key] == right[key]


def test_blocked_manifest_digest_is_deterministic():
    kwargs = {"repository_root": Path("."), "run_timestamp_utc": "2026-08-23T00:00:00Z"}
    left = service.execute_marketflow_repository_integration_branch_retry_failure_remediation_execution_after_plan_results_review_v1(**kwargs)
    right = service.execute_marketflow_repository_integration_branch_retry_failure_remediation_execution_after_plan_results_review_v1(**kwargs)
    assert left[service.BLOCKED_MANIFEST_DIGEST_KEY] == right[service.BLOCKED_MANIFEST_DIGEST_KEY]


def test_validator_accepts_success_and_blocked(success, blocked):
    assert service.validate_marketflow_repository_integration_branch_retry_failure_remediation_execution_after_plan_results_review_v1(success)["failed_checks"] == 0
    assert service.validate_marketflow_repository_integration_branch_retry_failure_remediation_execution_after_plan_results_review_v1(blocked)["failed_checks"] == 0


@pytest.mark.parametrize("field", sorted(service.SOURCE_BINDINGS))
def test_validator_rejects_changed_source_binding(success, field):
    changed = deepcopy(success)
    changed[field] = "changed"
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionAfterPlanResultsReviewError):
        service.validate_marketflow_repository_integration_branch_retry_failure_remediation_execution_after_plan_results_review_v1(changed)


@pytest.mark.parametrize("field", service.FALSE_BOUNDARY_FIELDS)
def test_validator_rejects_forbidden_boundary_true(success, field):
    changed = deepcopy(success)
    changed[field] = True
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionAfterPlanResultsReviewError):
        service.validate_marketflow_repository_integration_branch_retry_failure_remediation_execution_after_plan_results_review_v1(changed)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("artifact_kind", "WRONG"), ("execution_status", "WRONG"), ("execution_scope", "WRONG"),
        ("selected_remediation_execution_package", "WRONG"), ("priority_1_total_nodeids", 611),
        ("top_10_count_sum", 1068), ("module_summary_module_count", 28),
        ("failed_or_errored_nodeids_count", 1403), ("source_exit_code", 0),
        ("source_stdout_sha256", "0" * 64), ("source_stderr_sha256", "0" * 64),
        ("observable_failure_family_count", 3), ("total_observable_evidence_items", 187),
        ("source_workstream_count", 3), ("predictive_usefulness", "accepted"),
        ("profitability", "accepted"), ("runtime_use", "AUTHORIZED"), ("broker_execution", "AUTHORIZED"),
    ],
)
def test_validator_rejects_changed_fixed_contract(success, field, value):
    changed = deepcopy(success)
    changed[field] = value
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionAfterPlanResultsReviewError):
        service.validate_marketflow_repository_integration_branch_retry_failure_remediation_execution_after_plan_results_review_v1(changed)


@pytest.mark.parametrize("field", ["file_impact_inventory", "pre_change_snapshot", "change_records", "post_change_snapshot", "verification_evidence_report", "outputs", "risk_controls", "next_chain", "next_gates"])
def test_validator_rejects_missing_success_evidence(success, field):
    changed = deepcopy(success)
    changed[field] = []
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionAfterPlanResultsReviewError):
        service.validate_marketflow_repository_integration_branch_retry_failure_remediation_execution_after_plan_results_review_v1(changed)


@pytest.mark.parametrize(
    "updates",
    [
        {"workstream_ids": []}, {"source_authority": ""}, {"focused_validation_covered": False},
        {"root_cause_claimed": True}, {"retry_success_claimed": True}, {"main_merge_readiness_claimed": True},
        {"expected_digest_updated": True, "digest_update_authority": "NOT_APPLICABLE"},
        {"test_modified": True, "test_change_authority": "NOT_APPLICABLE"},
        {"production_code_modified": True, "production_change_authority": "NOT_APPLICABLE"},
    ],
)
def test_builder_rejects_change_without_required_authority_or_boundary(updates):
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionAfterPlanResultsReviewError):
        service.execute_marketflow_repository_integration_branch_retry_failure_remediation_execution_after_plan_results_review_v1(
            remediation_change_records=[_record(**updates)], focused_validation_summary=_validation()
        )


def test_builder_blocks_when_change_validation_did_not_pass():
    artifact = service.execute_marketflow_repository_integration_branch_retry_failure_remediation_execution_after_plan_results_review_v1(
        remediation_change_records=[_record()], focused_validation_summary=_validation(exit_code=1, focused_validation_passed=False)
    )
    assert artifact["artifact_kind"] == service.BLOCKED_ARTIFACT_KIND
    assert artifact["blocked_reason"] == service.BLOCKED_VALIDATION


def test_builder_rejects_validation_that_uses_cacheprovider():
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionAfterPlanResultsReviewError):
        service.execute_marketflow_repository_integration_branch_retry_failure_remediation_execution_after_plan_results_review_v1(
            remediation_change_records=[_record()], focused_validation_summary=_validation(cacheprovider_disabled=False)
        )


def test_validator_rejects_blocked_without_reason_or_changed_manifest(blocked):
    no_reason = deepcopy(blocked)
    no_reason["blocked_reason"] = None
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionAfterPlanResultsReviewError):
        service.validate_marketflow_repository_integration_branch_retry_failure_remediation_execution_after_plan_results_review_v1(no_reason)
    changed_digest = deepcopy(blocked)
    changed_digest[service.BLOCKED_MANIFEST_DIGEST_KEY] = "0" * 64
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionAfterPlanResultsReviewError):
        service.validate_marketflow_repository_integration_branch_retry_failure_remediation_execution_after_plan_results_review_v1(changed_digest)


def test_writer_uses_isolated_output_and_refuses_overwrite(tmp_path):
    artifact = service.write_marketflow_repository_integration_branch_retry_failure_remediation_execution_after_plan_results_review_v1(
        tmp_path, repository_root=Path("."), run_timestamp_utc="2026-08-23T00:00:00Z"
    )
    output = tmp_path / "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_AFTER_PLAN_RESULTS_REVIEW_STATUS.md"
    assert artifact["artifact_kind"] == service.BLOCKED_ARTIFACT_KIND
    assert output.is_file()
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionAfterPlanResultsReviewError):
        service.write_marketflow_repository_integration_branch_retry_failure_remediation_execution_after_plan_results_review_v1(tmp_path)


@pytest.mark.parametrize("protected", [".marketflow", ".pytest_cache", ".env"])
def test_writer_rejects_protected_output_directories(protected):
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureRemediationExecutionAfterPlanResultsReviewError):
        service.write_marketflow_repository_integration_branch_retry_failure_remediation_execution_after_plan_results_review_v1(Path(protected))


def test_markdown_contains_all_required_sections(success):
    markdown = service.build_marketflow_repository_integration_branch_retry_failure_remediation_execution_after_plan_results_review_markdown_v1(success)
    assert markdown.startswith("# MarketFlow Repository Integration Branch Retry Failure Remediation Execution After Plan Results Review v1")
    for section in service.MARKDOWN_SECTIONS:
        assert f"## {section}" in markdown


def test_public_aliases_match_contract_constants():
    assert service.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_EXECUTED_AFTER_PLAN_RESULTS_REVIEW_V1 == service.SUCCESS_ARTIFACT_KIND
    assert service.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_BLOCKED_AFTER_PLAN_RESULTS_REVIEW_V1 == service.BLOCKED_ARTIFACT_KIND
    assert service.PACKAGE_EXECUTE_CONTROLLED_PLAN_DERIVED_REMEDIATION_WITH_VERIFICATION_ONLY == service.SELECTED_PACKAGE
