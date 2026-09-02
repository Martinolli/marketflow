from __future__ import annotations

from copy import deepcopy
import json

import pytest

from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_failure_diagnosis_service
    as svc,
)


@pytest.fixture
def diagnosis() -> dict:
    return svc.build_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_failure_diagnosis_v1()


def test_diagnosis_builds_offline(diagnosis: dict) -> None:
    assert diagnosis["created_offline"] is True
    assert diagnosis["governance_only"] is True
    assert diagnosis["diagnosis_only"] is True


def test_diagnosis_is_deterministic() -> None:
    first = svc.build_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_failure_diagnosis_v1()
    second = svc.build_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_failure_diagnosis_v1()
    assert first == second


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("artifact_kind", svc.ARTIFACT_KIND),
        ("diagnosis_status", svc.DIAGNOSIS_STATUS),
        ("diagnosis_scope", svc.DIAGNOSIS_SCOPE),
        ("source_detail_exposure_or_binding_execution_blocked_digest", svc.SOURCE_BLOCKED_EXECUTION_DIGEST),
        ("source_detail_exposure_or_binding_execution_blocked_manifest_digest", svc.SOURCE_BLOCKED_MANIFEST_DIGEST),
        ("blocked_reason", svc.SOURCE_BLOCKED_REASON),
        ("source_detail_exposure_or_binding_approval_digest", svc.SOURCE_APPROVAL_DIGEST),
        ("source_detail_exposure_or_binding_operator_review_digest", svc.SOURCE_OPERATOR_REVIEW_DIGEST),
        ("source_detail_exposure_or_binding_candidate_digest", svc.SOURCE_CANDIDATE_DIGEST),
        ("selected_detail_exposure_or_binding_package", svc.SELECTED_PACKAGE),
        ("source_reentry_failure_diagnosis_digest", svc.SOURCE_REENTRY_FAILURE_DIAGNOSIS_DIGEST),
        ("source_primary_failure_class", svc.SOURCE_PRIMARY_FAILURE_CLASS),
        ("source_reentry_execution_blocked_digest", svc.SOURCE_REENTRY_BLOCKED_DIGEST),
        ("source_reentry_execution_blocked_manifest_digest", svc.SOURCE_REENTRY_BLOCKED_MANIFEST_DIGEST),
        ("source_reentry_execution_blocked_reason", svc.SOURCE_REENTRY_BLOCKED_REASON),
        ("source_after_v2_planning_reentry_digest", svc.SOURCE_PLANNING_REENTRY_DIGEST),
        ("source_module_grouping_source_recovery_results_review_digest", svc.SOURCE_RECOVERY_RESULTS_REVIEW_DIGEST),
        ("source_module_grouping_source_recovery_results_review_manifest_digest", svc.SOURCE_RECOVERY_RESULTS_REVIEW_MANIFEST_DIGEST),
        ("source_module_grouping_source_recovery_execution_digest", svc.SOURCE_RECOVERY_EXECUTION_DIGEST),
        ("source_module_grouping_source_recovery_detail_digest", svc.SOURCE_RECOVERY_DETAIL_DIGEST),
        ("source_module_grouping_source_recovery_digest_manifest_digest", svc.SOURCE_RECOVERY_DIGEST_MANIFEST_DIGEST),
        ("source_blocked_after_v2_execution_digest", svc.SOURCE_BLOCKED_AFTER_V2_EXECUTION_DIGEST),
        ("source_after_v2_approval_digest", svc.SOURCE_AFTER_V2_APPROVAL_DIGEST),
        ("source_results_review_v2_digest", svc.SOURCE_RESULTS_REVIEW_V2_DIGEST),
        ("source_execution_v2_digest", svc.SOURCE_EXECUTION_V2_DIGEST),
        ("source_module_grouping_digest", svc.SOURCE_MODULE_GROUPING_DIGEST),
        ("retry_execution_commit", svc.RETRY_EXECUTION_COMMIT),
        ("top_5_count_sum", 612), ("top_10_count_sum", 1069),
        ("primary_failure_class", svc.PRIMARY_FAILURE_CLASS),
        ("detail_exposure_or_binding_execution_failure_diagnosis_created", True),
        ("detail_exposure_or_binding_execution_failure_diagnosis_ready", True),
        ("complete_29_row_source_availability_diagnosed", True),
        ("committed_complete_29_row_detail_source_gap_identified", True),
        ("actual_live_detail_binding_source_lacks_complete_29_rows", True),
        ("detail_binding_success_path_tested_with_complete_29_row_snapshot", True),
        ("recommended_next_package", svc.RECOMMENDED_NEXT_PACKAGE),
        ("recommended_next_task", svc.RECOMMENDED_NEXT_TASK),
        ("predictive_usefulness", svc.NOT_ACCEPTED), ("profitability", svc.NOT_ACCEPTED),
        ("runtime_use", svc.NOT_AUTHORIZED), ("broker_execution", svc.NOT_AUTHORIZED),
    ],
)
def test_required_fields_are_bound(diagnosis: dict, field: str, expected: object) -> None:
    assert diagnosis[field] == expected


def test_retry_failure_counts_are_bound(diagnosis: dict) -> None:
    assert diagnosis["retry_failure_context"]["counts"] == {"passed": 24877, "failed": 1292, "errors": 112, "skipped": 7}


def test_recovered_module_summary_is_bound(diagnosis: dict) -> None:
    assert diagnosis["recovered_module_grouping_source_summary"] == {
        "failed_or_errored_nodeids_count": 1404,
        "module_summary_module_count": 29,
        "largest_module_nodeid_counts": [136, 131, 122, 112, 111],
    }


def test_top_five_paths_and_counts_are_bound(diagnosis: dict) -> None:
    assert diagnosis["top_module_summary"] == svc.TOP_FIVE
    assert sum(row["failed_or_errored_nodeid_count"] for row in diagnosis["top_module_summary"]) == 612


def test_available_and_missing_data_are_recorded(diagnosis: dict) -> None:
    assert diagnosis["source_execution_available_data"] == svc.AVAILABLE_DATA
    assert diagnosis["source_execution_missing_data"] == svc.MISSING_DATA


def test_root_cause_and_not_root_causes_are_recorded(diagnosis: dict) -> None:
    assert diagnosis["root_cause_classification"]["primary_failure_class"] == svc.PRIMARY_FAILURE_CLASS
    assert diagnosis["not_root_causes"] == svc.NOT_ROOT_CAUSES


@pytest.mark.parametrize("field", svc.FALSE_BOUNDARIES)
def test_all_execution_boundaries_remain_false(diagnosis: dict, field: str) -> None:
    assert diagnosis[field] is False


@pytest.mark.parametrize("output_id", svc.OUTPUT_IDS)
def test_diagnosis_outputs_are_research_only(diagnosis: dict, output_id: str) -> None:
    assert diagnosis[output_id]["status"] == svc.GENERATED_RESEARCH_ONLY


def test_next_chain_gates_and_risk_controls_are_complete(diagnosis: dict) -> None:
    assert diagnosis["next_chain"] == svc.NEXT_CHAIN
    assert diagnosis["next_gates"] == svc.NEXT_GATES
    assert diagnosis["risk_controls"] == svc.RISK_CONTROLS


def test_checklist_passes(diagnosis: dict) -> None:
    assert diagnosis["summary"]["total_checks"] == len(diagnosis["checklist"])
    assert diagnosis["summary"]["passed_checks"] == len(diagnosis["checklist"])
    assert diagnosis["summary"]["failed_checks"] == 0
    assert diagnosis["summary"]["blocker_count"] == 0
    assert all(item["status"] == svc.PASS for item in diagnosis["checklist"])


def test_validator_accepts_valid_diagnosis(diagnosis: dict) -> None:
    result = svc.validate_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_failure_diagnosis_v1(diagnosis)
    assert result["passed_checks"] == result["total_checks"]


@pytest.mark.parametrize(
    ("path", "replacement"),
    [
        (("artifact_kind",), "WRONG"), (("diagnosis_status",), "WRONG"), (("diagnosis_scope",), "WRONG"),
        (("source_detail_exposure_or_binding_execution_blocked_digest",), "0" * 64),
        (("source_detail_exposure_or_binding_execution_blocked_manifest_digest",), "0" * 64),
        (("blocked_reason",), None), (("source_detail_exposure_or_binding_approval_digest",), "0" * 64),
        (("source_detail_exposure_or_binding_operator_review_digest",), "0" * 64),
        (("source_detail_exposure_or_binding_candidate_digest",), "0" * 64),
        (("source_reentry_failure_diagnosis_digest",), "0" * 64), (("source_primary_failure_class",), "WRONG"),
        (("source_reentry_execution_blocked_digest",), "0" * 64),
        (("source_reentry_execution_blocked_manifest_digest",), "0" * 64),
        (("source_after_v2_planning_reentry_digest",), "0" * 64),
        (("source_module_grouping_source_recovery_results_review_digest",), "0" * 64),
        (("source_module_grouping_source_recovery_detail_digest",), "0" * 64),
        (("source_blocked_after_v2_execution_digest",), "0" * 64),
        (("source_after_v2_approval_digest",), "0" * 64), (("source_results_review_v2_digest",), "0" * 64),
        (("source_execution_v2_digest",), "0" * 64), (("source_module_grouping_digest",), "0" * 64),
        (("retry_failure_context", "counts"), {}), (("recovered_module_grouping_source_summary",), {}),
        (("top_module_summary",), []), (("top_5_count_sum",), 611), (("top_10_count_sum",), 1068),
        (("source_execution_available_data",), []), (("source_execution_missing_data",), []),
        (("actual_live_detail_binding_source_lacks_complete_29_rows",), False),
        (("root_cause_classification",), {}), (("primary_failure_class",), "WRONG"),
        (("detail_exposure_or_binding_execution_failure_diagnosis_created",), False),
        (("detail_exposure_or_binding_execution_failure_diagnosis_ready",), False),
        (("complete_29_row_source_availability_diagnosed",), False),
        (("committed_complete_29_row_detail_source_gap_identified",), False),
        (("ready_for_complete_29_row_detail_source_materialization_candidate",), False),
        (("complete_29_row_detail_exposed_by_diagnosis",), True),
        (("complete_29_row_detail_bound_by_diagnosis",), True),
        (("module_grouping_detail_exposed_by_diagnosis",), True), (("module_paths_recovered_by_diagnosis",), True),
        (("source_recovery_rerun_performed",), True), (("cache_read_in_diagnosis",), True),
        (("after_v2_planning_execution_reentry_performed_by_diagnosis",), True),
        (("targeted_diagnostic_output_capture_candidate_created",), True), (("new_retry_candidate_created",), True),
        (("retry_rerun_performed",), True), (("full_pytest_performed",), True),
        (("diagnostic_command_executed",), True), (("diagnostic_method_executed",), True),
        (("integration_execution_successful",), True), (("main_push_performed",), True),
        (("marketflow_outputs_committed",), True), (("pytest_cache_committed",), True),
        (("provider_requests_made_in_diagnosis",), True), (("predictive_usefulness",), "accepted"),
        (("runtime_use",), "AUTHORIZED"), (("risk_controls",), []), (("diagnosis_manifest",), {}),
    ],
)
def test_validator_rejects_contract_mutations(diagnosis: dict, path: tuple[str, ...], replacement: object) -> None:
    changed = deepcopy(diagnosis)
    target = changed
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = replacement
    with pytest.raises(svc.MarketFlowRepositoryIntegrationBranchRetryFailureDetailBindingExecutionFailureDiagnosisError):
        svc.validate_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_failure_diagnosis_v1(changed)


def test_validator_rejects_missing_digest(diagnosis: dict) -> None:
    changed = deepcopy(diagnosis)
    changed.pop("marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_failure_diagnosis_digest")
    with pytest.raises(svc.MarketFlowRepositoryIntegrationBranchRetryFailureDetailBindingExecutionFailureDiagnosisError):
        svc.validate_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_failure_diagnosis_v1(changed)


def test_injected_committed_source_is_accepted() -> None:
    artifact = svc.build_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_failure_diagnosis_v1(
        source_blocked_execution=svc._committed_source_blocked_execution()
    )
    assert artifact["diagnosis_status"] == svc.DIAGNOSIS_STATUS


def test_injected_source_mutation_is_rejected() -> None:
    blocked = svc._committed_source_blocked_execution()
    blocked["top_5_count_sum"] = 611
    with pytest.raises(svc.MarketFlowRepositoryIntegrationBranchRetryFailureDetailBindingExecutionFailureDiagnosisError):
        svc.build_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_failure_diagnosis_v1(source_blocked_execution=blocked)


@pytest.mark.parametrize(
    "heading",
    [
        "Source Blocked Detail Exposure or Binding Execution", "Source Approval and Operator Review",
        "Source Reentry Failure Diagnosis", "Source Recovery Results Review", "Retry Failure Context",
        "Recovered Module Grouping Source Summary", "Available and Missing Detail Source", "Diagnosis Questions",
        "Diagnosis Findings", "Root Cause Classification", "Not Root Causes", "Recommended Next Package",
        "Next Chain", "Next Gates", "Risk Controls", "Authority Boundaries", "Checklist Summary", "Guardrails",
    ],
)
def test_markdown_includes_required_sections(diagnosis: dict, heading: str) -> None:
    markdown = svc.build_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_failure_diagnosis_markdown_v1(diagnosis)
    assert f"## {heading}" in markdown


def test_writer_round_trips_in_isolated_directory(tmp_path) -> None:
    result = svc.write_marketflow_repository_integration_branch_retry_failure_reentry_module_grouping_detail_exposure_or_binding_execution_failure_diagnosis_v1(tmp_path)
    with open(result["json_path"], encoding="utf-8") as handle:
        stored = json.load(handle)
    assert stored == result["artifact"]
    assert "# MarketFlow Repository" in (tmp_path / "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REENTRY_MODULE_GROUPING_DETAIL_EXPOSURE_OR_BINDING_EXECUTION_FAILURE_DIAGNOSIS_V1.md").read_text(encoding="utf-8")
