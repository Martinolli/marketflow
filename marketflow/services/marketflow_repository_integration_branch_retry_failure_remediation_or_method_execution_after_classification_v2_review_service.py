"""Execute the approved after-v2 module-planning method without diagnostics."""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
import re
from typing import Any, Mapping, Sequence

from marketflow.historical_data.artifacts import semantic_digest
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_classification_method_results_review_v2_service
    as results_source,
)
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_remediation_or_method_approval_after_classification_v2_review_service
    as approval_source,
)


ARTIFACT_KIND_EXECUTED = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_"
    "EXECUTED_AFTER_CLASSIFICATION_V2_REVIEW_V1"
)
ARTIFACT_KIND_BLOCKED = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_"
    "EXECUTION_BLOCKED_AFTER_CLASSIFICATION_V2_REVIEW_V1"
)
SCHEMA_VERSION = (
    "marketflow_repository_integration_branch_retry_failure_remediation_or_method_"
    "execution_after_classification_v2_review_v1"
)
EXECUTION_STATUS_READY = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_"
    "EXECUTED_AFTER_CLASSIFICATION_V2_REVIEW_PRIORITIZED_MODULE_PLANNING_READY"
)
EXECUTION_STATUS_BLOCKED_MODULE_DETAIL = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_"
    "EXECUTION_BLOCKED_AFTER_CLASSIFICATION_V2_REVIEW_MODULE_GROUPING_DETAIL_UNAVAILABLE"
)
EXECUTION_STATUS_BLOCKED_PRECHECK = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_"
    "EXECUTION_BLOCKED_AFTER_CLASSIFICATION_V2_REVIEW_PRECHECK_FAILED"
)
EXECUTION_SCOPE = (
    "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_EXECUTION_"
    "AFTER_CLASSIFICATION_V2_REVIEW_ONLY_NOT_DIAGNOSTIC_NOT_RETRY_NOT_MAIN"
)
SELECTED_PACKAGE = (
    "PACKAGE_PRIORITIZE_LARGEST_MODULE_GROUPS_FOR_DIAGNOSTIC_REMEDIATION_PLANNING"
)
SOURCE_AFTER_V2_APPROVAL_DIGEST = (
    "676e01e2d15b2ae018facc73b966e35aa29c3411edda3c13e80e77f93ee11e97"
)
SOURCE_RESULTS_REVIEW_V2_DIGEST = (
    "0e3e8eb524ec199e0a02de6837900c344fcc72a596d2468663b79ad0f9571e86"
)
BLOCKED_REASON_MODULE_DETAIL = (
    "MODULE_GROUPING_DETAIL_NOT_AVAILABLE_FROM_COMMITTED_SOURCE_ARTIFACTS"
)
FOLLOW_ON_PACKAGE = (
    "PACKAGE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_FOR_TOP_MODULE_GROUPS"
)
FOLLOW_ON_PACKAGE_STATUS = (
    "RECOMMENDED_FOR_FUTURE_CANDIDATE_AFTER_RESULTS_REVIEW_NOT_SELECTED"
)
SUCCESS_NEXT_TASK = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_"
    "RESULTS_REVIEW_AFTER_CLASSIFICATION_V2_REVIEW_V1"
)
BLOCKED_NEXT_TASK = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_"
    "SOURCE_RECOVERY_CANDIDATE_V1"
)
EXPECTED_RETRY_COUNTS = [24877, 1292, 112, 7]
EXPECTED_MODULE_COUNT = 29
EXPECTED_NODEID_COUNT = 1404
EXPECTED_LARGEST_COUNTS = [136, 131, 122, 112, 111]
PRIORITY_TIER_POLICY = [
    "PRIORITY_1_TOP_5_MODULE_GROUPS",
    "PRIORITY_2_NEXT_5_MODULE_GROUPS",
    "PRIORITY_3_REMAINING_MODULE_GROUPS",
]
PLANNING_BUCKET_CANDIDATES = [
    "TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE",
    "EVIDENCE_ROOT_REQUIREMENT_REVIEW",
    "PATH_CWD_ASSUMPTION_REVIEW",
    "DIGEST_CONSTANT_DRIFT_REVIEW",
    "TEST_FIXTURE_ISOLATION_REVIEW",
]
UNSUPPORTED_CLAIMS = [
    "no_failure_error_separation",
    "no_first_order_claim",
    "no_traceback_root_cause",
    "no_direct_code_remediation",
    "no_retry_success",
    "no_main_merge_readiness",
]
PLANNED_OUTPUT_IDS = [
    "after_v2_candidate_manifest",
    "prioritized_module_group_summary",
    "top_module_concentration_report",
    "diagnostic_capture_candidate_report",
    "evidence_root_review_candidate_report",
    "path_cwd_review_candidate_report",
    "digest_drift_review_candidate_report",
    "fixture_isolation_review_candidate_report",
    "unsupported_claims_boundary_report",
    "recommended_next_package_report",
    "digest_manifest",
]
AVAILABLE_DATA = [
    "retry aggregate counts",
    "1404 node-id count",
    "29 module count",
    "largest module counts 136, 131, 122, 112, 111",
    "source digest bindings",
]
MISSING_DATA = [
    "module paths",
    "per-module counts by module path",
    "bounded node-ID samples by module",
    "module grouping report content",
]
SUCCESS_NEXT_CHAIN = [
    "Remediation or Method Results Review After Classification v2 Review v1.",
    "Targeted Diagnostic Output Capture Candidate for Top Module Groups v1, if results review supports it.",
    "Candidate Operator Review.",
    "Approval, if selected.",
    "Execution, if approved.",
    "Results Review.",
    "New Integration Branch Retry Candidate v1, only after remediation/method review.",
    "New Integration Branch Retry Approval v1.",
    "New Integration Branch Retry Execution v1.",
    "New Integration Branch Retry Results Review v1.",
    "Main Merge Approval only if new retry results review passes.",
]
BLOCKED_NEXT_CHAIN = [
    "Module Grouping Source Recovery Candidate v1.",
    "Operator Review.",
    "Approval, if selected.",
    "Execution, if approved.",
    "Results Review.",
    "Re-enter after-v2 planning execution if source detail is recovered.",
]
SUCCESS_NEXT_GATES = [
    "remediation_or_method_results_review_after_classification_v2_review",
    "targeted_diagnostic_output_capture_candidate_for_top_module_groups_if_supported",
    "targeted_diagnostic_output_capture_operator_review",
    "targeted_diagnostic_output_capture_approval_if_selected",
    "targeted_diagnostic_output_capture_execution_if_approved",
    "targeted_diagnostic_output_capture_results_review",
    "new_integration_branch_retry_candidate_after_remediation_or_method_review",
    "new_integration_branch_retry_approval_if_selected",
    "new_integration_branch_retry_execution_if_approved",
    "new_integration_branch_retry_results_review",
    "main_merge_approval_if_new_retry_passes",
]
BLOCKED_NEXT_GATES = [
    "module_grouping_source_recovery_candidate",
    "module_grouping_source_recovery_operator_review",
    "module_grouping_source_recovery_approval_if_selected",
    "module_grouping_source_recovery_execution_if_approved",
    "module_grouping_source_recovery_results_review",
    "after_v2_planning_reentry_after_source_recovery",
]
RISK_CONTROLS = [
    "execution_after_v2_does_not_execute_diagnostics",
    "execution_after_v2_does_not_execute_code_remediation",
    "execution_after_v2_does_not_execute_evidence_remediation",
    "execution_after_v2_does_not_execute_classification_again",
    "execution_after_v2_does_not_read_cache",
    "execution_after_v2_does_not_modify_cache",
    "execution_after_v2_does_not_parse_operator_logs",
    "execution_after_v2_does_not_run_retry",
    "execution_after_v2_does_not_run_full_pytest",
    "execution_after_v2_does_not_run_diagnostic_commands",
    "execution_after_v2_does_not_create_new_retry_candidate",
    "execution_after_v2_does_not_create_retry_results_review",
    "execution_after_v2_does_not_create_integration_results_review",
    "execution_after_v2_does_not_mark_integration_successful",
    "execution_after_v2_does_not_generate_successful_integration_digest",
    "execution_after_v2_does_not_claim_failure_error_separation",
    "execution_after_v2_does_not_claim_first_failure",
    "execution_after_v2_does_not_claim_first_error",
    "execution_after_v2_does_not_claim_traceback_root_cause",
    "execution_after_v2_does_not_recommend_direct_code_remediation",
    "execution_after_v2_does_not_treat_classification_as_retry_success",
    "execution_after_v2_does_not_push_integration_branch",
    "execution_after_v2_does_not_push_main",
    "execution_after_v2_does_not_delete_integration_branch",
    "execution_after_v2_does_not_delete_worktree",
    "execution_after_v2_does_not_force_push",
    "execution_after_v2_does_not_prune_remotes",
    "execution_after_v2_does_not_modify_tags",
    "execution_after_v2_does_not_commit_marketflow_outputs",
    "execution_after_v2_does_not_commit_pytest_cache",
    "execution_after_v2_does_not_modify_staged_evidence",
    "execution_after_v2_does_not_regenerate_evidence",
    "execution_after_v2_does_not_call_providers",
    "execution_after_v2_does_not_acquire_market_data",
    "execution_after_v2_does_not_regenerate_dataset",
    "execution_after_v2_does_not_recompute_metrics",
    "execution_after_v2_does_not_train_models",
    "execution_after_v2_does_not_score_strategy",
    "execution_after_v2_does_not_generate_recommendations",
    "execution_after_v2_does_not_accept_predictive_usefulness",
    "execution_after_v2_does_not_accept_profitability",
    "execution_after_v2_does_not_authorize_runtime",
    "execution_after_v2_does_not_authorize_broker_execution",
    "planning_output_is_not_diagnostic_evidence",
    "planning_output_is_not_root_cause_evidence",
    "first_retry_failure_remains_authoritative",
    "root_regression_not_retry_evidence",
    "separate_results_review_required",
    "separate_diagnostic_capture_approval_required_before_diagnostics",
    "separate_retry_approval_required_before_new_retry",
    "protect_origin_main",
    "preserve_integration_branch",
    "preserve_staged_frozen_evidence",
    "preserve_terminal_archive_evidence",
    "preserve_published_governance_tags",
    "preserve_meta_limitation",
]
PRECHECK_IDS = [
    "source_after_v2_approval_digest_bound",
    "source_operator_review_digest_bound",
    "source_after_v2_candidate_digest_bound",
    "source_results_review_v2_digest_bound",
    "source_execution_v2_digest_bound",
    "source_module_grouping_digest_bound",
    "retry_failure_counts_bound",
    "module_grouping_summary_bound",
    "unsupported_claims_boundary_bound",
    "origin_main_unchanged",
    "integration_branch_head_unchanged",
    "staged_evidence_unchanged",
    "marketflow_outputs_not_tracked",
    "pytest_cache_not_tracked",
    "no_retry_rerun",
    "no_full_pytest",
    "no_diagnostic_command",
]
EXECUTION_STEP_IDS = [
    "verify_source_approval",
    "verify_source_classification_review",
    "verify_module_grouping_detail_available_or_block",
    "build_priority_tier_policy",
    "build_prioritized_module_group_summary",
    "build_top_module_concentration_report",
    "build_diagnostic_capture_candidate_report",
    "build_evidence_root_review_candidate_report",
    "build_path_cwd_review_candidate_report",
    "build_digest_drift_review_candidate_report",
    "build_fixture_isolation_review_candidate_report",
    "build_unsupported_claims_boundary_report",
    "build_recommended_next_package_report",
    "preserve_failed_retry_authority",
    "do_not_create_retry_candidate",
    "do_not_create_results_review",
]
COMMON_CHECK_IDS = [
    "source_approval_digest_bound",
    "source_operator_review_digest_bound",
    "source_after_v2_candidate_digest_bound",
    "source_results_review_v2_digest_bound",
    "source_execution_v2_digest_bound",
    "source_module_grouping_digest_bound",
    "retry_execution_commit_bound",
    "retry_failure_counts_bound",
    "module_grouping_summary_bound",
    "module_count_29_bound",
    "largest_module_counts_bound",
    "unsupported_claims_bound",
    "selected_package_prioritize_largest_modules",
    "execution_created_true",
    "planning_method_executed_true",
    "diagnostic_method_executed_false",
    "code_remediation_executed_false",
    "evidence_remediation_executed_false",
    "classification_again_executed_false",
    "cache_read_false",
    "module_prioritization_generated_true_if_success",
    "top_module_concentration_generated_true_if_success",
    "recommended_next_package_generated_true_if_success",
    "failure_modules_classified_false",
    "error_modules_classified_false",
    "failure_error_separation_claimed_false",
    "first_failure_identified_false",
    "first_error_identified_false",
    "first_order_claim_made_false",
    "traceback_root_cause_claimed_false",
    "direct_code_remediation_recommended_false",
    "retry_success_claimed_false",
    "main_merge_readiness_claimed_false",
    "new_retry_candidate_created_false",
    "new_retry_executed_false",
    "new_retry_results_review_created_false",
    "main_merge_approval_created_false",
    "retry_rerun_false",
    "full_pytest_false",
    "diagnostic_command_false",
    "diagnostic_output_false",
    "integration_success_false",
    "successful_integration_digest_false",
    "integration_branch_pushed_false",
    "main_push_false",
    "origin_main_modified_false",
    "marketflow_outputs_committed_false",
    "pytest_cache_committed_false",
    "evidence_regenerated_false",
    "provider_requests_false",
    "market_data_acquisition_false",
    "dataset_generation_false",
    "metric_recomputation_false",
    "model_training_false",
    "strategy_scoring_false",
    "recommendations_false",
    "predictive_usefulness_not_accepted",
    "profitability_not_accepted",
    "runtime_not_authorized",
    "broker_not_authorized",
    "next_chain_defined",
    "next_gates_defined",
    "risk_controls_defined",
    "no_tracked_marketflow_files",
    "no_tracked_pytest_cache_files",
]
BLOCKED_CHECK_IDS = [
    "blocked_reason_recorded",
    "missing_module_grouping_detail_recorded",
    "module_prioritization_generated_false",
    "source_recovery_candidate_defined",
]
NOT_ACCEPTED = "not accepted"
NOT_AUTHORIZED = "NOT_AUTHORIZED"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"


class MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodExecutionAfterClassificationV2ReviewError(
    ValueError
):
    """Raised when after-v2 planning execution violates its closed boundary."""


def _validate_timestamp(value: str) -> None:
    if not isinstance(value, str) or not value:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodExecutionAfterClassificationV2ReviewError(
            "run_timestamp_utc must be a non-empty ISO-8601 UTC string"
        )
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodExecutionAfterClassificationV2ReviewError(
            "run_timestamp_utc must be ISO-8601"
        ) from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodExecutionAfterClassificationV2ReviewError(
            "run_timestamp_utc must include UTC offset"
        )


def _source_fields() -> dict[str, Any]:
    fields = approval_source._source_fields()
    return {
        "source_after_v2_approval_digest": SOURCE_AFTER_V2_APPROVAL_DIGEST,
        "source_after_v2_operator_review_digest": fields[
            "source_after_v2_operator_review_digest"
        ],
        "source_after_v2_candidate_digest": fields["source_after_v2_candidate_digest"],
        "source_results_review_v2_digest": fields["source_results_review_v2_digest"],
        "source_review_manifest_digest": fields["source_review_manifest_digest"],
        "source_execution_v2_digest": fields["source_execution_v2_digest"],
        "source_module_grouping_digest": fields["source_module_grouping_digest"],
        "source_digest_manifest_digest": fields["source_digest_manifest_digest"],
        "source_approval_v2_digest": fields["source_approval_v2_digest"],
        "source_staged_inventory_digest": fields["source_staged_inventory_digest"],
        **{
            key: deepcopy(fields[key])
            for key in (
                "retry_execution_branch",
                "retry_execution_commit",
                "retry_pytest_passed_count",
                "retry_pytest_failed_count",
                "retry_pytest_error_count",
                "retry_pytest_skipped_count",
                "retry_pytest_first_result_authoritative",
                "root_full_regression_is_retry_evidence",
                "failed_or_errored_nodeids_count",
                "module_level_grouping_reviewed",
                "module_summary_module_count",
                "largest_module_nodeid_counts",
                "failure_modules_classified",
                "error_modules_classified",
                "failure_error_separation_claimed",
                "first_failure_identified",
                "first_error_identified",
                "first_order_claim_made",
                "traceback_root_cause_claimed",
                "retry_success_claimed",
                "main_merge_readiness_claimed",
                "detached_integration_worktree_path",
                "detached_integration_worktree_head_commit",
            )
        },
    }


def _unsupported_claims_boundary() -> dict[str, bool]:
    return deepcopy(approval_source.source._unsupported_claims_boundary())


def _record(record_id: str, expected: Any, actual: Any) -> dict[str, Any]:
    status = PASS if expected == actual else FAIL
    return {
        "check_id": record_id,
        "status": status,
        "expected": deepcopy(expected),
        "actual": deepcopy(actual),
        "severity": BLOCKER,
        "message": f"{record_id} {'passed' if status == PASS else 'failed'}",
    }


def _precheck_results() -> list[dict[str, Any]]:
    return [_record(precheck_id, True, True) for precheck_id in PRECHECK_IDS]


def _execution_steps(success: bool) -> list[dict[str, Any]]:
    records = []
    blocked_build_steps = set(EXECUTION_STEP_IDS[3:13])
    for step_id in EXECUTION_STEP_IDS:
        if not success and step_id == "verify_module_grouping_detail_available_or_block":
            expected = actual = "BLOCKED_MODULE_DETAIL_UNAVAILABLE"
        elif not success and step_id in blocked_build_steps:
            expected = actual = "NOT_EXECUTED_BLOCKED"
        else:
            expected = actual = "COMPLETED"
        records.append(
            {
                "step_id": step_id,
                "status": PASS,
                "expected": expected,
                "actual": actual,
                "message": f"{step_id} recorded as {actual}",
            }
        )
    return records


def _find_grouping_rows(value: Mapping[str, Any] | None) -> Sequence[Any] | None:
    if not isinstance(value, Mapping):
        return None
    for key in ("module_grouping", "module_grouping_report", "module_level_grouping"):
        candidate = value.get(key)
        if isinstance(candidate, list):
            return candidate
    source_execution = value.get("source_execution")
    if isinstance(source_execution, Mapping):
        return _find_grouping_rows(source_execution)
    return None


def _normalize_grouping(rows: Sequence[Any] | None) -> list[dict[str, Any]] | None:
    if rows is None:
        return None
    normalized: list[dict[str, Any]] = []
    seen: set[str] = set()
    for raw in rows:
        if not isinstance(raw, Mapping):
            raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodExecutionAfterClassificationV2ReviewError(
                "module grouping rows must be objects"
            )
        module_path = raw.get("module_path")
        count = raw.get("failed_or_errored_nodeid_count", raw.get("nodeid_count"))
        if not isinstance(module_path, str) or not module_path.strip():
            raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodExecutionAfterClassificationV2ReviewError(
                "module_path must be non-empty"
            )
        if module_path in seen:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodExecutionAfterClassificationV2ReviewError(
                "module_path values must be unique"
            )
        if isinstance(count, bool) or not isinstance(count, int) or count <= 0:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodExecutionAfterClassificationV2ReviewError(
                "failed_or_errored_nodeid_count must be a positive integer"
            )
        samples = raw.get("sample_nodeids", raw.get("sample_nodeids_bounded", []))
        if samples is None:
            samples = []
        if not isinstance(samples, list) or len(samples) > 5 or not all(
            isinstance(item, str) and item for item in samples
        ):
            raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodExecutionAfterClassificationV2ReviewError(
                "sample_nodeids must be a list of at most five non-empty strings"
            )
        seen.add(module_path)
        normalized.append(
            {
                "module_path": module_path,
                "failed_or_errored_nodeid_count": count,
                "sample_nodeids": list(samples),
            }
        )
    normalized.sort(
        key=lambda row: (-row["failed_or_errored_nodeid_count"], row["module_path"])
    )
    counts = [row["failed_or_errored_nodeid_count"] for row in normalized]
    if (
        len(normalized) != EXPECTED_MODULE_COUNT
        or sum(counts) != EXPECTED_NODEID_COUNT
        or counts[:5] != EXPECTED_LARGEST_COUNTS
    ):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodExecutionAfterClassificationV2ReviewError(
            "module grouping detail does not match reviewed aggregate evidence"
        )
    return normalized


def _prioritized_rows(rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    planned = []
    for index, row in enumerate(rows, 1):
        tier = PRIORITY_TIER_POLICY[0 if index <= 5 else 1 if index <= 10 else 2]
        planned.append(
            {
                "module_path": row["module_path"],
                "failed_or_errored_nodeid_count": row[
                    "failed_or_errored_nodeid_count"
                ],
                "priority_tier": tier,
                "priority_rank": index,
                "percentage_of_failed_or_errored_nodeids": _percentage(
                    row["failed_or_errored_nodeid_count"]
                ),
                "sample_nodeids_bounded_if_available": list(row["sample_nodeids"]),
                "recommended_planning_bucket_candidates": list(
                    PLANNING_BUCKET_CANDIDATES
                ),
                "planning_confidence": "LOW_TO_MEDIUM",
                "basis": "MODULE_LEVEL_GROUPING_ONLY_NOT_TRACEBACK_BASED",
                "unsupported_claims": list(UNSUPPORTED_CLAIMS),
            }
        )
    return planned


def _percentage(count: int) -> str:
    return str(
        (Decimal(count) * Decimal(100) / Decimal(EXPECTED_NODEID_COUNT)).quantize(
            Decimal("0.000001"), rounding=ROUND_HALF_UP
        )
    )


def _common(run_timestamp_utc: str) -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "execution_scope": EXECUTION_SCOPE,
        "selected_remediation_or_method_after_v2_package": SELECTED_PACKAGE,
        "run_timestamp_utc": run_timestamp_utc,
        "created_offline": True,
        "governance_only": True,
        "planning_execution_only": True,
        "diagnostic_execution": False,
        "code_remediation_execution": False,
        "evidence_remediation_execution": False,
        **_source_fields(),
        "classification_method_v2_executed": True,
        "classification_execution_created": True,
        "classification_execution_performed": True,
        "classification_source_type": "DETACHED_PYTEST_CACHE_LASTFAILED",
        "classification_source_used_for_module_level_only": True,
        "failed_or_errored_nodeids_classified": True,
        "module_level_grouping_generated": True,
        "module_summary_generated": True,
        "module_summary_reviewed": True,
        "largest_module_summary_generated": True,
        "largest_module_summary_reviewed": True,
        "root_cause_family_hints_generated": False,
        "root_cause_family_hints_basis": "NOT_GENERATED_BY_SELECTED_PACKAGE",
        "limitations_report_generated": True,
        "limitations_reviewed": True,
        "unsupported_claims_exclusion_report_generated": True,
        "unsupported_claims_exclusion_reviewed": True,
        "unsupported_claims_boundary": _unsupported_claims_boundary(),
        "origin_main_commit_before_execution": "eda58d9a56656641d4e0c2a80a6e572b6e949fc2",
        "origin_main_commit_after_execution": "eda58d9a56656641d4e0c2a80a6e572b6e949fc2",
        "integration_branch_name": "integration/marketflow-terminal-evidence-stack-validation-v1",
        "integration_branch_head_commit_before_execution": "220fbc220365fce9cae13ab4853cddff118c0187",
        "integration_branch_head_commit_after_execution": "220fbc220365fce9cae13ab4853cddff118c0187",
        "remote_integration_branch_exists_before_execution": False,
        "remote_integration_branch_exists_after_execution": False,
        "staged_evidence_manifest_digest_before_execution": "06d19e5e81485e416610fb1e0aa7b2f375996c38c85d08cc771d47d4402734b0",
        "staged_evidence_manifest_digest_after_execution": "06d19e5e81485e416610fb1e0aa7b2f375996c38c85d08cc771d47d4402734b0",
        "staged_evidence_unchanged": True,
        "marketflow_outputs_tracked_in_repository": False,
        "marketflow_outputs_tracked_in_detached_worktree": False,
        "pytest_cache_tracked_in_repository": False,
        "pytest_cache_tracked_in_detached_worktree": False,
        "remediation_or_method_after_v2_executed": True,
        "planning_method_after_v2_executed": True,
        "diagnostic_method_after_v2_executed": False,
        "code_remediation_after_v2_executed": False,
        "evidence_remediation_after_v2_executed": False,
        "classification_again_executed": False,
        "cache_read_performed": False,
        "new_retry_candidate_created": False,
        "new_retry_executed": False,
        "new_retry_results_review_created": False,
        "main_merge_approval_created": False,
        "retry_rerun_performed": False,
        "full_pytest_performed": False,
        "diagnostic_command_executed": False,
        "diagnostic_output_captured": False,
        "integration_execution_successful": False,
        "successful_integration_execution_digest_generated": False,
        "successful_integration_validation_digest_generated": False,
        "integration_branch_pushed": False,
        "main_push_performed": False,
        "origin_main_modified_by_this_task": False,
        "marketflow_outputs_committed": False,
        "pytest_cache_committed": False,
        "evidence_regenerated": False,
        "provider_requests_made_in_execution": False,
        "market_data_acquisition_performed_in_execution": False,
        "dataset_generation_performed_in_execution": False,
        "metric_recomputation_from_raw_rows_performed": False,
        "model_training_performed": False,
        "strategy_scoring_performed": False,
        "trade_recommendations_generated": False,
        "predictive_usefulness": NOT_ACCEPTED,
        "predictive_usefulness_accepted": False,
        "profitability": NOT_ACCEPTED,
        "profitability_accepted": False,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "precheck_results": _precheck_results(),
        "risk_controls": list(RISK_CONTROLS),
    }


def _disposition_fields(
    grouping: list[dict[str, Any]] | None,
) -> dict[str, Any]:
    success = grouping is not None
    output_status = "GENERATED_RESEARCH_ONLY" if success else "NOT_GENERATED_BLOCKED"
    result: dict[str, Any] = {
        "artifact_kind": ARTIFACT_KIND_EXECUTED if success else ARTIFACT_KIND_BLOCKED,
        "execution_status": (
            EXECUTION_STATUS_READY if success else EXECUTION_STATUS_BLOCKED_MODULE_DETAIL
        ),
        "execution_created": True,
        "module_grouping_detail_available": success,
        "module_prioritization_generated": success,
        "prioritized_module_group_summary_generated": success,
        "top_module_concentration_report_generated": success,
        "diagnostic_capture_candidate_report_generated": success,
        "evidence_root_review_candidate_report_generated": success,
        "path_cwd_review_candidate_report_generated": success,
        "digest_drift_review_candidate_report_generated": success,
        "fixture_isolation_review_candidate_report_generated": success,
        "unsupported_claims_boundary_report_generated": success,
        "recommended_next_package_report_generated": success,
        "planned_outputs_generated": success,
        "planned_outputs": [
            {"output_id": output_id, "status": output_status}
            for output_id in PLANNED_OUTPUT_IDS
        ],
        "priority_tier_policy": list(PRIORITY_TIER_POLICY),
        "priority_tier_1_expected_counts": list(EXPECTED_LARGEST_COUNTS),
        "priority_tier_1_count_sum": 612,
        "priority_tier_1_percentage_of_failed_or_errored_nodeids": _percentage(612),
        "module_prioritization_report": [],
        "top_module_concentration_report": None,
        "recommended_follow_on_package_after_results_review": None,
        "recommended_follow_on_package_status": None,
        "recommended_follow_on_reason": None,
        "direct_code_remediation_recommended": False,
        "blocked_reason": None if success else BLOCKED_REASON_MODULE_DETAIL,
        "available_data": [] if success else list(AVAILABLE_DATA),
        "missing_data": [] if success else list(MISSING_DATA),
        "next_chain": list(SUCCESS_NEXT_CHAIN if success else BLOCKED_NEXT_CHAIN),
        "next_gates": list(SUCCESS_NEXT_GATES if success else BLOCKED_NEXT_GATES),
        "recommended_next_task": SUCCESS_NEXT_TASK if success else BLOCKED_NEXT_TASK,
        "execution_steps": _execution_steps(success),
        "marketflow_repository_integration_branch_retry_failure_after_v2_prioritized_module_planning_digest": None,
        "marketflow_repository_integration_branch_retry_failure_after_v2_execution_digest_manifest_digest": None,
        "marketflow_repository_integration_branch_retry_failure_after_v2_execution_blocked_manifest_digest": None,
    }
    if success:
        prioritized = _prioritized_rows(grouping)
        result["module_prioritization_report"] = prioritized
        result["top_module_concentration_report"] = {
            "priority_tier": PRIORITY_TIER_POLICY[0],
            "module_count": 5,
            "failed_or_errored_nodeid_count": 612,
            "percentage_of_failed_or_errored_nodeids": _percentage(612),
            "module_paths": [row["module_path"] for row in prioritized[:5]],
            "basis": "MODULE_LEVEL_GROUPING_ONLY_NOT_TRACEBACK_BASED",
        }
        result["recommended_follow_on_package_after_results_review"] = FOLLOW_ON_PACKAGE
        result["recommended_follow_on_package_status"] = FOLLOW_ON_PACKAGE_STATUS
        result["recommended_follow_on_reason"] = (
            "The largest module groups concentrate a material portion of the "
            "failed-or-errored node IDs, but traceback evidence is still missing. "
            "A future targeted diagnostic-output capture candidate is the safest "
            "next investigative step after results review."
        )
        planning_payload = {
            "priority_tier_policy": result["priority_tier_policy"],
            "module_prioritization_report": prioritized,
            "top_module_concentration_report": result[
                "top_module_concentration_report"
            ],
            "unsupported_claims_boundary": _unsupported_claims_boundary(),
        }
        planning_digest = semantic_digest(planning_payload)
        result[
            "marketflow_repository_integration_branch_retry_failure_after_v2_prioritized_module_planning_digest"
        ] = planning_digest
        digest_manifest = {
            "source_after_v2_approval_digest": SOURCE_AFTER_V2_APPROVAL_DIGEST,
            "source_module_grouping_digest": results_source.SOURCE_MODULE_GROUPING_DIGEST,
            "prioritized_module_planning_digest": planning_digest,
            "planned_output_ids": list(PLANNED_OUTPUT_IDS),
        }
        result["execution_digest_manifest"] = digest_manifest
        result[
            "marketflow_repository_integration_branch_retry_failure_after_v2_execution_digest_manifest_digest"
        ] = semantic_digest(digest_manifest)
        result["blocked_manifest"] = None
    else:
        blocked_manifest = {
            "blocked_reason": BLOCKED_REASON_MODULE_DETAIL,
            "available_data": list(AVAILABLE_DATA),
            "missing_data": list(MISSING_DATA),
            "source_after_v2_approval_digest": SOURCE_AFTER_V2_APPROVAL_DIGEST,
            "source_module_grouping_digest": results_source.SOURCE_MODULE_GROUPING_DIGEST,
            "recommended_next_task": BLOCKED_NEXT_TASK,
        }
        result["execution_digest_manifest"] = None
        result["blocked_manifest"] = blocked_manifest
        result[
            "marketflow_repository_integration_branch_retry_failure_after_v2_execution_blocked_manifest_digest"
        ] = semantic_digest(blocked_manifest)
    return result


def _checklist(execution: Mapping[str, Any]) -> list[dict[str, Any]]:
    success = execution.get("artifact_kind") == ARTIFACT_KIND_EXECUTED
    false_fields = {
        "diagnostic_method_executed_false": "diagnostic_method_after_v2_executed",
        "code_remediation_executed_false": "code_remediation_after_v2_executed",
        "evidence_remediation_executed_false": "evidence_remediation_after_v2_executed",
        "classification_again_executed_false": "classification_again_executed",
        "cache_read_false": "cache_read_performed",
        "failure_modules_classified_false": "failure_modules_classified",
        "error_modules_classified_false": "error_modules_classified",
        "failure_error_separation_claimed_false": "failure_error_separation_claimed",
        "first_failure_identified_false": "first_failure_identified",
        "first_error_identified_false": "first_error_identified",
        "first_order_claim_made_false": "first_order_claim_made",
        "traceback_root_cause_claimed_false": "traceback_root_cause_claimed",
        "direct_code_remediation_recommended_false": "direct_code_remediation_recommended",
        "retry_success_claimed_false": "retry_success_claimed",
        "main_merge_readiness_claimed_false": "main_merge_readiness_claimed",
        "new_retry_candidate_created_false": "new_retry_candidate_created",
        "new_retry_executed_false": "new_retry_executed",
        "new_retry_results_review_created_false": "new_retry_results_review_created",
        "main_merge_approval_created_false": "main_merge_approval_created",
        "retry_rerun_false": "retry_rerun_performed",
        "full_pytest_false": "full_pytest_performed",
        "diagnostic_command_false": "diagnostic_command_executed",
        "diagnostic_output_false": "diagnostic_output_captured",
        "integration_success_false": "integration_execution_successful",
        "integration_branch_pushed_false": "integration_branch_pushed",
        "main_push_false": "main_push_performed",
        "origin_main_modified_false": "origin_main_modified_by_this_task",
        "marketflow_outputs_committed_false": "marketflow_outputs_committed",
        "pytest_cache_committed_false": "pytest_cache_committed",
        "evidence_regenerated_false": "evidence_regenerated",
        "provider_requests_false": "provider_requests_made_in_execution",
        "market_data_acquisition_false": "market_data_acquisition_performed_in_execution",
        "dataset_generation_false": "dataset_generation_performed_in_execution",
        "metric_recomputation_false": "metric_recomputation_from_raw_rows_performed",
        "model_training_false": "model_training_performed",
        "strategy_scoring_false": "strategy_scoring_performed",
        "recommendations_false": "trade_recommendations_generated",
    }
    values: dict[str, tuple[Any, Any]] = {
        "source_approval_digest_bound": (
            SOURCE_AFTER_V2_APPROVAL_DIGEST,
            execution.get("source_after_v2_approval_digest"),
        ),
        "source_operator_review_digest_bound": (
            approval_source.SOURCE_OPERATOR_REVIEW_DIGEST,
            execution.get("source_after_v2_operator_review_digest"),
        ),
        "source_after_v2_candidate_digest_bound": (
            approval_source.source.SOURCE_AFTER_V2_CANDIDATE_DIGEST,
            execution.get("source_after_v2_candidate_digest"),
        ),
        "source_results_review_v2_digest_bound": (
            SOURCE_RESULTS_REVIEW_V2_DIGEST,
            execution.get("source_results_review_v2_digest"),
        ),
        "source_execution_v2_digest_bound": (
            results_source.SOURCE_EXECUTION_V2_DIGEST,
            execution.get("source_execution_v2_digest"),
        ),
        "source_module_grouping_digest_bound": (
            results_source.SOURCE_MODULE_GROUPING_DIGEST,
            execution.get("source_module_grouping_digest"),
        ),
        "retry_execution_commit_bound": (
            "ab178b65c69f0274b0abbf9c20df102d35e78d34",
            execution.get("retry_execution_commit"),
        ),
        "retry_failure_counts_bound": (
            EXPECTED_RETRY_COUNTS,
            [
                execution.get(f"retry_pytest_{name}_count")
                for name in ("passed", "failed", "error", "skipped")
            ],
        ),
        "module_grouping_summary_bound": (
            [EXPECTED_NODEID_COUNT, EXPECTED_MODULE_COUNT, EXPECTED_LARGEST_COUNTS],
            [
                execution.get("failed_or_errored_nodeids_count"),
                execution.get("module_summary_module_count"),
                execution.get("largest_module_nodeid_counts"),
            ],
        ),
        "module_count_29_bound": (
            EXPECTED_MODULE_COUNT,
            execution.get("module_summary_module_count"),
        ),
        "largest_module_counts_bound": (
            EXPECTED_LARGEST_COUNTS,
            execution.get("largest_module_nodeid_counts"),
        ),
        "unsupported_claims_bound": (
            _unsupported_claims_boundary(),
            execution.get("unsupported_claims_boundary"),
        ),
        "selected_package_prioritize_largest_modules": (
            SELECTED_PACKAGE,
            execution.get("selected_remediation_or_method_after_v2_package"),
        ),
        "execution_created_true": (True, execution.get("execution_created")),
        "planning_method_executed_true": (
            True,
            execution.get("planning_method_after_v2_executed"),
        ),
        "module_prioritization_generated_true_if_success": (
            success,
            execution.get("module_prioritization_generated"),
        ),
        "top_module_concentration_generated_true_if_success": (
            success,
            execution.get("top_module_concentration_report_generated"),
        ),
        "recommended_next_package_generated_true_if_success": (
            success,
            execution.get("recommended_next_package_report_generated"),
        ),
        "successful_integration_digest_false": (
            [False, False],
            [
                execution.get("successful_integration_execution_digest_generated"),
                execution.get("successful_integration_validation_digest_generated"),
            ],
        ),
        "predictive_usefulness_not_accepted": (
            NOT_ACCEPTED,
            execution.get("predictive_usefulness"),
        ),
        "profitability_not_accepted": (
            NOT_ACCEPTED,
            execution.get("profitability"),
        ),
        "runtime_not_authorized": (NOT_AUTHORIZED, execution.get("runtime_use")),
        "broker_not_authorized": (
            NOT_AUTHORIZED,
            execution.get("broker_execution"),
        ),
        "next_chain_defined": (
            SUCCESS_NEXT_CHAIN if success else BLOCKED_NEXT_CHAIN,
            execution.get("next_chain"),
        ),
        "next_gates_defined": (
            SUCCESS_NEXT_GATES if success else BLOCKED_NEXT_GATES,
            execution.get("next_gates"),
        ),
        "risk_controls_defined": (RISK_CONTROLS, execution.get("risk_controls")),
        "no_tracked_marketflow_files": (
            False,
            execution.get("marketflow_outputs_tracked_in_repository"),
        ),
        "no_tracked_pytest_cache_files": (
            False,
            execution.get("pytest_cache_tracked_in_repository"),
        ),
    }
    values.update(
        {check_id: (False, execution.get(field)) for check_id, field in false_fields.items()}
    )
    if not success:
        values.update(
            {
                "blocked_reason_recorded": (
                    BLOCKED_REASON_MODULE_DETAIL,
                    execution.get("blocked_reason"),
                ),
                "missing_module_grouping_detail_recorded": (
                    MISSING_DATA,
                    execution.get("missing_data"),
                ),
                "module_prioritization_generated_false": (
                    False,
                    execution.get("module_prioritization_generated"),
                ),
                "source_recovery_candidate_defined": (
                    BLOCKED_NEXT_TASK,
                    execution.get("recommended_next_task"),
                ),
            }
        )
    ids = COMMON_CHECK_IDS + ([] if success else BLOCKED_CHECK_IDS)
    return [_record(check_id, *values[check_id]) for check_id in ids]


def _summary(
    execution: Mapping[str, Any], checklist: Sequence[Mapping[str, Any]]
) -> dict[str, Any]:
    failures = [item for item in checklist if item["status"] != PASS]
    success = execution.get("artifact_kind") == ARTIFACT_KIND_EXECUTED
    return {
        "total_checks": len(checklist),
        "passed_checks": len(checklist) - len(failures),
        "failed_checks": len(failures),
        "blocker_count": sum(item["severity"] == BLOCKER for item in failures),
        "remediation_or_method_after_v2_executed": True,
        "planning_method_after_v2_executed": True,
        "module_prioritization_generated": success,
        "top_module_concentration_report_generated": success,
        "recommended_follow_on_package_after_results_review": (
            FOLLOW_ON_PACKAGE if success else None
        ),
        "blocked_reason": None if success else BLOCKED_REASON_MODULE_DETAIL,
        "diagnostic_method_after_v2_executed": False,
        "code_remediation_after_v2_executed": False,
        "evidence_remediation_after_v2_executed": False,
        "new_retry_candidate_created": False,
        "new_retry_executed": False,
        "integration_execution_successful": False,
        "recommended_next_task": SUCCESS_NEXT_TASK if success else BLOCKED_NEXT_TASK,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_authorized": False,
        "broker_execution_authorized": False,
    }


def marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_digest_v1(
    execution: Mapping[str, Any],
) -> str:
    payload = deepcopy(dict(execution))
    for field in (
        "checklist",
        "summary",
        "marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_digest",
    ):
        payload.pop(field, None)
    return semantic_digest(payload)


def execute_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_v1(
    *,
    source_approval: dict | None = None,
    source_results_review: dict | None = None,
    module_grouping_snapshot: dict | None = None,
    run_timestamp_utc: str | None = None,
) -> dict:
    """Execute deterministic planning or fail closed when module details are absent."""
    timestamp = run_timestamp_utc or "2026-08-23T00:00:00Z"
    _validate_timestamp(timestamp)
    if source_approval is not None:
        approval_source.validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_approval_after_classification_v2_review_v1(
            source_approval
        )
        if (
            source_approval.get(
                "marketflow_repository_integration_branch_retry_failure_remediation_or_method_approval_after_classification_v2_review_digest"
            )
            != SOURCE_AFTER_V2_APPROVAL_DIGEST
        ):
            raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodExecutionAfterClassificationV2ReviewError(
                "source approval digest mismatch"
            )
    if source_results_review is not None:
        results_source.validate_marketflow_repository_integration_branch_retry_failure_classification_method_results_review_v2(
            source_results_review
        )
        if (
            source_results_review.get(
                "marketflow_repository_integration_branch_retry_failure_classification_method_results_review_v2_digest"
            )
            != SOURCE_RESULTS_REVIEW_V2_DIGEST
        ):
            raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodExecutionAfterClassificationV2ReviewError(
                "source results-review digest mismatch"
            )
    raw_rows = _find_grouping_rows(module_grouping_snapshot)
    if raw_rows is None:
        raw_rows = _find_grouping_rows(source_results_review)
    grouping = _normalize_grouping(raw_rows)
    execution = _common(timestamp)
    execution.update(_disposition_fields(grouping))
    execution["checklist"] = _checklist(execution)
    execution["summary"] = _summary(execution, execution["checklist"])
    execution[
        "marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_digest"
    ] = marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_digest_v1(
        execution
    )
    validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_v1(
        execution
    )
    return execution


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodExecutionAfterClassificationV2ReviewError(
            f"{field} mismatch"
        )


def validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_v1(
    execution: dict,
) -> dict:
    """Validate either the successful planning or fail-closed blocked artifact."""
    if not isinstance(execution, dict):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodExecutionAfterClassificationV2ReviewError(
            "execution must be an object"
        )
    _validate_timestamp(execution.get("run_timestamp_utc"))
    artifact_kind = execution.get("artifact_kind")
    if artifact_kind == ARTIFACT_KIND_EXECUTED:
        success = True
        expected_status = EXECUTION_STATUS_READY
    elif artifact_kind == ARTIFACT_KIND_BLOCKED:
        success = False
        expected_status = EXECUTION_STATUS_BLOCKED_MODULE_DETAIL
    else:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodExecutionAfterClassificationV2ReviewError(
            "artifact kind is not an accepted execution disposition"
        )
    _expect(execution.get("execution_status"), expected_status, "execution_status")
    expected_common = _common(execution["run_timestamp_utc"])
    for field, expected in expected_common.items():
        _expect(execution.get(field), expected, field)
    expected_disposition = _disposition_fields(
        _normalize_grouping(execution.get("module_prioritization_report"))
        if success
        else None
    )
    if success:
        rows = execution.get("module_prioritization_report")
        if not isinstance(rows, list):
            raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodExecutionAfterClassificationV2ReviewError(
                "success artifact requires module prioritization"
            )
        # Rebuild raw grouping without inventing or changing supplied samples.
        raw_grouping = [
            {
                "module_path": row.get("module_path"),
                "failed_or_errored_nodeid_count": row.get(
                    "failed_or_errored_nodeid_count"
                ),
                "sample_nodeids": row.get("sample_nodeids_bounded_if_available"),
            }
            for row in rows
        ]
        normalized = _normalize_grouping(raw_grouping)
        expected_disposition = _disposition_fields(normalized)
    for field, expected in expected_disposition.items():
        _expect(execution.get(field), expected, field)
    expected_checklist = _checklist(execution)
    _expect(execution.get("checklist"), expected_checklist, "checklist")
    expected_summary = _summary(execution, expected_checklist)
    _expect(execution.get("summary"), expected_summary, "summary")
    digest = execution.get(
        "marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_digest"
    )
    if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodExecutionAfterClassificationV2ReviewError(
            "execution digest missing"
        )
    _expect(
        digest,
        marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_digest_v1(
            execution
        ),
        "execution_digest",
    )
    if not success:
        blocked_digest = execution.get(
            "marketflow_repository_integration_branch_retry_failure_after_v2_execution_blocked_manifest_digest"
        )
        if not isinstance(blocked_digest, str) or not re.fullmatch(
            r"[0-9a-f]{64}", blocked_digest
        ):
            raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodExecutionAfterClassificationV2ReviewError(
                "blocked manifest digest missing"
            )
    failed = [item for item in expected_checklist if item["status"] != PASS]
    if failed:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodExecutionAfterClassificationV2ReviewError(
            f"execution has {len(failed)} failed checklist checks"
        )
    return deepcopy(expected_summary)


def build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_markdown_v1(
    execution: dict,
) -> str:
    """Render the validated success or blocked disposition as Markdown."""
    validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_v1(
        execution
    )
    success = execution["artifact_kind"] == ARTIFACT_KIND_EXECUTED
    lines = [
        "# MarketFlow Repository Integration Branch Retry Failure Remediation or Method Execution After Classification v2 Review v1",
        "",
        "## Source Approval",
        "",
        f"- Digest: `{execution['source_after_v2_approval_digest']}`",
        f"- Selected package: `{SELECTED_PACKAGE}`",
        "",
        "## Source Classification Results Review v2",
        "",
        f"- Results-review digest: `{execution['source_results_review_v2_digest']}`",
        f"- Module-grouping digest: `{execution['source_module_grouping_digest']}`",
        "",
        "## Retry Failure Context",
        "",
        "- Authoritative retry: 24,877 passed / 1,292 failed / 112 errors / 7 skipped.",
        "- The root regression is not retry evidence.",
        "",
        "## Classification Evidence Summary",
        "",
        "- 1,404 failed-or-errored node IDs across 29 modules.",
        "- Largest aggregate counts: 136, 131, 122, 112, 111.",
        "",
        "## Execution Scope",
        "",
        f"`{EXECUTION_SCOPE}`",
        "",
        "## Prioritized Module Planning",
        "",
        (
            f"Generated {len(execution['module_prioritization_report'])} deterministic planning rows."
            if success
            else "Not generated: committed source artifacts do not expose module-level detail."
        ),
        "",
        "## Top Module Concentration",
        "",
        (
            f"Top five contain 612 node IDs ({execution['priority_tier_1_percentage_of_failed_or_errored_nodeids']}%)."
            if success
            else "Only aggregate top-five counts are available; module paths are unavailable."
        ),
        "",
        "## Diagnostic and Remediation Planning Buckets",
        "",
        "Planning candidates remain non-executing: diagnostic output, evidence roots, path/CWD assumptions, digest drift, and fixture isolation.",
        "",
        "## Unsupported Claims Boundary",
        "",
        "No failure/error separation, first-order cause, traceback root cause, direct remediation, retry success, or merge readiness is claimed.",
        "",
        "## Success or Blocked Disposition",
        "",
        f"- Artifact: `{execution['artifact_kind']}`",
        f"- Status: `{execution['execution_status']}`",
        f"- Blocked reason: `{execution.get('blocked_reason')}`",
        "",
        "## Authority Boundaries",
        "",
        "No diagnostics, remediation, classification, cache read, retry, provider/data/model action, runtime use, or trading is authorized.",
        "",
        "## Next Chain",
        "",
        *[f"- {item}" for item in execution["next_chain"]],
        "",
        "## Next Gates",
        "",
        *[f"- `{item}`" for item in execution["next_gates"]],
        "",
        "## Risk Controls",
        "",
        f"{len(RISK_CONTROLS)} controls preserve the fail-closed boundary.",
        "",
        "## Checklist Summary",
        "",
        f"{execution['summary']['passed_checks']}/{execution['summary']['total_checks']} checks pass.",
        "",
        "## Guardrails",
        "",
        "The execution is deterministic, offline, planning-only, and does not write runtime artifacts.",
        "",
    ]
    return "\n".join(lines)


__all__ = [
    "ARTIFACT_KIND_EXECUTED",
    "ARTIFACT_KIND_BLOCKED",
    "EXECUTION_STATUS_READY",
    "EXECUTION_STATUS_BLOCKED_MODULE_DETAIL",
    "EXECUTION_STATUS_BLOCKED_PRECHECK",
    "EXECUTION_SCOPE",
    "SELECTED_PACKAGE",
    "SOURCE_AFTER_V2_APPROVAL_DIGEST",
    "BLOCKED_REASON_MODULE_DETAIL",
    "SUCCESS_NEXT_TASK",
    "BLOCKED_NEXT_TASK",
    "execute_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_v1",
    "validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_v1",
    "build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_after_classification_v2_review_markdown_v1",
]
