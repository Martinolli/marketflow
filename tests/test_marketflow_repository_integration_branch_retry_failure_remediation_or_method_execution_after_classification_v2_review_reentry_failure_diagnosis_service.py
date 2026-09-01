from __future__ import annotations

from copy import deepcopy
import json

import pytest

from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_reentry_failure_diagnosis_service
    as service,
)


def build() -> dict:
    return service.build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_reentry_failure_diagnosis_v1()


def validate(diagnosis: dict) -> dict:
    return service.validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_reentry_failure_diagnosis_v1(diagnosis)


def test_diagnosis_builds_offline_and_has_identity() -> None:
    diagnosis = build()
    assert diagnosis["created_offline"] is True
    assert diagnosis["artifact_kind"] == service.ARTIFACT_KIND
    assert diagnosis["diagnosis_status"] == service.DIAGNOSIS_STATUS
    assert diagnosis["diagnosis_scope"] == service.DIAGNOSIS_SCOPE


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("source_reentry_execution_blocked_digest", service.SOURCE_BLOCKED_EXECUTION_DIGEST),
        ("source_reentry_execution_blocked_manifest_digest", service.SOURCE_BLOCKED_MANIFEST_DIGEST),
        ("blocked_reason", service.SOURCE_BLOCKED_REASON),
        ("source_after_v2_planning_reentry_digest", service.SOURCE_REENTRY_DIGEST),
        ("source_module_grouping_source_recovery_results_review_digest", service.SOURCE_RESULTS_REVIEW_DIGEST),
        ("source_module_grouping_source_recovery_results_review_manifest_digest", service.SOURCE_RESULTS_REVIEW_MANIFEST_DIGEST),
        ("source_module_grouping_source_recovery_execution_digest", service.SOURCE_RECOVERY_EXECUTION_DIGEST),
        ("source_module_grouping_source_recovery_detail_digest", service.SOURCE_RECOVERY_DETAIL_DIGEST),
        ("source_module_grouping_source_recovery_digest_manifest_digest", service.SOURCE_RECOVERY_DIGEST_MANIFEST_DIGEST),
        ("source_blocked_after_v2_execution_digest", service.SOURCE_BLOCKED_AFTER_V2_EXECUTION_DIGEST),
        ("source_blocked_after_v2_manifest_digest", service.SOURCE_BLOCKED_AFTER_V2_MANIFEST_DIGEST),
        ("source_after_v2_approval_digest", service.SOURCE_AFTER_V2_APPROVAL_DIGEST),
        ("source_results_review_v2_digest", service.SOURCE_RESULTS_REVIEW_V2_DIGEST),
        ("source_execution_v2_digest", service.SOURCE_EXECUTION_V2_DIGEST),
        ("source_module_grouping_digest", service.SOURCE_MODULE_GROUPING_DIGEST),
        ("retry_execution_commit", service.RETRY_EXECUTION_COMMIT),
    ],
)
def test_source_chain_is_digest_bound(field: str, expected: str) -> None:
    assert build()[field] == expected


def test_retry_and_recovered_module_summaries_are_bound() -> None:
    diagnosis = build()
    assert diagnosis["retry_failure_context"]["counts"] == {"passed": 24877, "failed": 1292, "errors": 112, "skipped": 7}
    assert diagnosis["recovered_module_grouping_source_summary"] == {
        "failed_or_errored_nodeids_count": 1404,
        "module_summary_module_count": 29,
        "largest_module_nodeid_counts": [136, 131, 122, 112, 111],
    }
    assert diagnosis["top_module_summary"] == service.TOP_FIVE
    assert diagnosis["top_5_count_sum"] == 612
    assert diagnosis["top_10_count_sum"] == 1069


def test_available_and_missing_detail_are_recorded_without_exposure() -> None:
    diagnosis = build()
    assert diagnosis["available_committed_reentry_detail"] == service.AVAILABLE_COMMITTED_DETAIL
    assert diagnosis["missing_committed_reentry_detail"] == service.MISSING_COMMITTED_DETAIL
    assert diagnosis["actual_live_reentry_source_lacks_complete_29_rows"] is True
    assert diagnosis["complete_29_row_detail_available_to_live_reentry_execution"] is False
    assert len(diagnosis["top_module_summary"]) == 5
    assert "module_rows" not in diagnosis


def test_injected_snapshot_success_path_is_only_recorded() -> None:
    diagnosis = build()
    assert diagnosis["reentry_success_path_implemented_with_injected_snapshot"] is True
    assert diagnosis["reentry_success_path_tested_with_complete_29_row_snapshot"] is True
    assert diagnosis["success_path_generates_tier_sums"] == {"tier_1": 612, "tier_2": 457, "tier_3": 335}
    assert diagnosis["after_v2_planning_execution_performed_by_diagnosis"] is False


def test_root_cause_classification_and_findings_are_complete() -> None:
    diagnosis = build()
    assert diagnosis["root_cause_classification_completed"] is True
    assert diagnosis["primary_failure_class"] == service.PRIMARY_FAILURE_CLASS
    assert diagnosis["root_cause_classification"]["primary_failure_class"] == service.PRIMARY_FAILURE_CLASS
    assert len(diagnosis["diagnosis_questions"]) == 12
    assert len(diagnosis["diagnosis_findings"]) == 10
    assert diagnosis["not_root_causes"] == service.NOT_ROOT_CAUSES


def test_next_package_options_chain_gates_and_controls_are_defined() -> None:
    diagnosis = build()
    assert diagnosis["recommended_next_package"] == service.RECOMMENDED_NEXT_PACKAGE
    assert diagnosis["recommended_next_task"] == service.RECOMMENDED_NEXT_TASK
    assert len(diagnosis["supporting_next_options"]) == 10
    assert diagnosis["next_chain"] == service.NEXT_CHAIN
    assert diagnosis["next_gates"] == service.NEXT_GATES
    assert diagnosis["risk_controls"] == service.RISK_CONTROLS


@pytest.mark.parametrize("field", service.FALSE_BOUNDARIES)
def test_all_execution_and_authority_boundaries_remain_false(field: str) -> None:
    assert build()[field] is False


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("predictive_usefulness", service.NOT_ACCEPTED),
        ("profitability", service.NOT_ACCEPTED),
        ("runtime_use", service.NOT_AUTHORIZED),
        ("strategy_use", service.NOT_AUTHORIZED),
        ("paper_trading", service.NOT_AUTHORIZED),
        ("broker_execution", service.NOT_AUTHORIZED),
    ],
)
def test_predictive_runtime_and_trading_authority_remains_closed(field: str, expected: str) -> None:
    assert build()[field] == expected


@pytest.mark.parametrize("output_id", service.OUTPUT_IDS)
def test_diagnosis_outputs_are_research_only(output_id: str) -> None:
    assert build()[output_id]["status"] == service.GENERATED_RESEARCH_ONLY


def test_checklist_summary_and_digest_are_deterministic() -> None:
    first = build()
    second = build()
    assert first == second
    assert first["summary"]["total_checks"] == 79
    assert first["summary"]["passed_checks"] == 79
    assert first["summary"]["failed_checks"] == 0
    assert first["summary"]["blocker_count"] == 0
    assert first["marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_reentry_failure_diagnosis_digest"] == second["marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_reentry_failure_diagnosis_digest"]


def test_validator_accepts_valid_diagnosis() -> None:
    result = validate(build())
    assert result["diagnosis_status"] == service.DIAGNOSIS_STATUS
    assert result["passed_checks"] == result["total_checks"]


@pytest.mark.parametrize(
    ("field", "replacement"),
    [
        ("artifact_kind", "WRONG"), ("diagnosis_status", "WRONG"), ("diagnosis_scope", "WRONG"),
        ("source_reentry_execution_blocked_digest", "0" * 64),
        ("source_reentry_execution_blocked_manifest_digest", "0" * 64),
        ("blocked_reason", ""), ("source_after_v2_planning_reentry_digest", "0" * 64),
        ("source_module_grouping_source_recovery_results_review_digest", "0" * 64),
        ("source_module_grouping_source_recovery_detail_digest", "0" * 64),
        ("source_blocked_after_v2_execution_digest", "0" * 64),
        ("source_after_v2_approval_digest", "0" * 64), ("source_results_review_v2_digest", "0" * 64),
        ("source_execution_v2_digest", "0" * 64), ("source_module_grouping_digest", "0" * 64),
        ("top_5_count_sum", 611), ("top_10_count_sum", 1068),
        ("actual_live_reentry_source_lacks_complete_29_rows", False),
        ("root_cause_classification_completed", False), ("primary_failure_class", "WRONG"),
        ("reentry_failure_diagnosis_created", False), ("reentry_failure_diagnosis_ready", False),
        ("source_detail_availability_diagnosed", False), ("committed_reentry_detail_gap_identified", False),
        ("ready_for_reentry_module_detail_exposure_or_binding_candidate", False),
        ("module_grouping_detail_exposed_by_diagnosis", True), ("module_paths_recovered_by_diagnosis", True),
        ("per_module_counts_recovered_by_diagnosis", True), ("bounded_nodeid_samples_recovered_by_diagnosis", True),
        ("after_v2_planning_execution_performed_by_diagnosis", True), ("diagnostic_method_executed", True),
        ("code_remediation_executed", True), ("evidence_remediation_executed", True),
        ("classification_execution_performed_in_diagnosis", True), ("cache_read_in_diagnosis", True),
        ("source_recovery_rerun_performed", True), ("retry_rerun_performed", True),
        ("full_pytest_performed", True), ("diagnostic_command_executed", True),
        ("diagnostic_output_captured", True), ("targeted_diagnostic_output_capture_candidate_created", True),
        ("new_retry_candidate_created", True), ("new_retry_executed", True),
        ("new_retry_results_review_created", True), ("main_merge_approval_created", True),
        ("integration_execution_successful", True), ("successful_integration_execution_digest_generated", True),
        ("integration_branch_pushed", True), ("main_push_performed", True),
        ("origin_main_modified_by_this_task", True), ("marketflow_outputs_committed", True),
        ("pytest_cache_committed", True), ("evidence_regenerated", True),
        ("provider_requests_made_in_diagnosis", True), ("market_data_acquisition_performed_in_diagnosis", True),
        ("dataset_generation_performed_in_diagnosis", True), ("metric_recomputation_from_raw_rows_performed", True),
        ("model_training_performed", True), ("strategy_scoring_performed", True),
        ("trade_recommendations_generated", True), ("predictive_usefulness", "accepted"),
        ("profitability", "accepted"), ("runtime_use", "AUTHORIZED"), ("broker_execution", "AUTHORIZED"),
    ],
)
def test_validator_rejects_tampered_scalar_fields(field: str, replacement: object) -> None:
    diagnosis = build()
    diagnosis[field] = replacement
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureReentryFailureDiagnosisError):
        validate(diagnosis)


@pytest.mark.parametrize(
    "field",
    [
        "retry_failure_context", "recovered_module_grouping_source_summary", "top_module_summary",
        "available_committed_reentry_detail", "missing_committed_reentry_detail",
        "root_cause_classification", "diagnosis_manifest", "next_chain", "risk_controls",
    ],
)
def test_validator_rejects_missing_required_structures(field: str) -> None:
    diagnosis = build()
    diagnosis.pop(field)
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureReentryFailureDiagnosisError):
        validate(diagnosis)


def test_builder_accepts_exact_committed_source_and_rejects_changed_source() -> None:
    committed = service._committed_source_blocked_execution()
    diagnosis = service.build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_reentry_failure_diagnosis_v1(source_blocked_execution=committed)
    assert diagnosis["blocked_reason"] == service.SOURCE_BLOCKED_REASON
    committed["blocked_reason"] = "WRONG"
    with pytest.raises(service.MarketFlowRepositoryIntegrationBranchRetryFailureReentryFailureDiagnosisError):
        service.build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_reentry_failure_diagnosis_v1(source_blocked_execution=committed)


def test_writer_round_trips_json_and_markdown_in_temporary_directory(tmp_path) -> None:
    result = service.write_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_reentry_failure_diagnosis_v1(tmp_path)
    loaded = json.loads((tmp_path / "marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_reentry_failure_diagnosis_v1.json").read_text(encoding="utf-8"))
    assert loaded == result["artifact"]
    assert "# MarketFlow Repository Integration Branch Retry Failure" in (tmp_path / "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_EXECUTION_AFTER_CLASSIFICATION_V2_REVIEW_REENTRY_FAILURE_DIAGNOSIS_V1.md").read_text(encoding="utf-8")


@pytest.mark.parametrize(
    "heading",
    [
        "Source Blocked Reentry Execution", "Source Planning Reentry", "Source Recovery Results Review",
        "Retry Failure Context", "Recovered Module Grouping Source Summary",
        "Available and Missing Committed Detail", "Diagnosis Questions", "Diagnosis Findings",
        "Root Cause Classification", "Not Root Causes", "Recommended Next Package", "Next Chain",
        "Next Gates", "Risk Controls", "Authority Boundaries", "Checklist Summary", "Guardrails",
    ],
)
def test_markdown_includes_required_sections(heading: str) -> None:
    markdown = service.build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_reentry_failure_diagnosis_markdown_v1(build())
    assert f"## {heading}" in markdown
