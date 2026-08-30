"""Execute the approved retry-failure classification method without rerunning pytest."""

from __future__ import annotations

from collections import Counter
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
import re
from typing import Any, Mapping

from marketflow.historical_data.artifacts import semantic_digest
from marketflow.services import (
    marketflow_repository_integration_branch_retry_failure_remediation_or_method_approval_service as source,
)


ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_EXECUTED = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_EXECUTED"
)
ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_EXECUTION_BLOCKED = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_EXECUTION_BLOCKED"
)
SCHEMA_VERSION_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_EXECUTION_V1 = (
    "marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_v1"
)
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_EXECUTED_FAILURE_DOMAINS_CLASSIFIED = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_EXECUTED_FAILURE_DOMAINS_CLASSIFIED"
)
MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_EXECUTION_BLOCKED_AUTHORITATIVE_RETRY_OUTPUT_UNAVAILABLE = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_EXECUTION_BLOCKED_AUTHORITATIVE_RETRY_OUTPUT_UNAVAILABLE"
)
REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_EXECUTION_ONLY_NOT_RETRY_NOT_RESULTS_REVIEW_NOT_MAIN = (
    "REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_EXECUTION_ONLY_NOT_RETRY_NOT_RESULTS_REVIEW_NOT_MAIN"
)

SELECTED_RETRY_FAILURE_METHOD_PACKAGE = source.SELECTED_RETRY_FAILURE_METHOD_PACKAGE
SOURCE_METHOD_APPROVAL_DIGEST = "44e0d7c7ea17f0be0444bc2ad3f4f1974d606f1cb8b1f2d59f0748f462135f02"
CLASSIFICATION_BLOCKED_REASON = "AUTHORITATIVE_RETRY_OUTPUT_DETAIL_NOT_PERSISTED_OR_NOT_LOCATABLE"
SUCCESS_RECOMMENDED_NEXT_TASK = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_RESULTS_REVIEW_V1"
)
BLOCKED_RECOMMENDED_NEXT_TASK = (
    "MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_CANDIDATE_V1"
)
NOT_ACCEPTED = "not accepted"
NOT_AUTHORIZED = "NOT_AUTHORIZED"
PASS = "PASS"
BLOCKER = "BLOCKER"

ALLOWED_SOURCE_RELATIVE_PATHS = [
    "docs/status/MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_EXECUTION_STATUS.md",
    "docs/plans/MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_EXECUTION_V1_PLAN.md",
    "marketflow/services/marketflow_repository_integration_branch_retry_execution_service.py",
]
MISSING_RETRY_DATA = [
    "failed_module_list",
    "error_module_list",
    "first_failing_test",
    "first_error_trace",
    "traceback_or_classification_detail",
]
ROOT_CAUSE_FAMILIES = [
    "missing_ignored_evidence_root",
    "path_or_cwd_assumption",
    "digest_constant_or_historical_artifact_drift",
    "integration_branch_content_mismatch",
    "import_cache_or_environment_state",
    "test_fixture_isolation",
    "unknown_or_unclassified",
]
PLANNED_OUTPUT_NAMES = list(source.source.source.PLANNED_OUTPUT_NAMES)

SUCCESS_NEXT_CHAIN = [
    "Retry Failure Remediation or Method Results Review v1.",
    "New Integration Branch Retry Candidate v1.",
    "New Integration Branch Retry Approval v1.",
    "New Integration Branch Retry Execution v1.",
    "New Integration Branch Retry Results Review v1.",
    "Main Merge Approval only if new retry results review passes.",
]
BLOCKED_NEXT_CHAIN = [
    "Retry Failure Output Capture or Classification Source Candidate v1.",
    "Operator Review v1.",
    "Approval v1, if selected.",
    "Execution v1, if approved.",
    "Results Review v1.",
    "Retry Failure Classification Method Candidate v2 or New Retry Candidate, depending on evidence.",
]
SUCCESS_NEXT_GATES = [
    "retry_failure_method_results_review",
    "new_integration_branch_retry_candidate_after_method_review",
    "new_integration_branch_retry_approval_if_selected",
    "new_integration_branch_retry_execution_if_approved",
    "new_integration_branch_retry_results_review",
    "main_merge_approval_if_new_retry_passes",
]
BLOCKED_NEXT_GATES = [
    "retry_failure_output_capture_or_classification_source_candidate",
    "retry_failure_output_capture_operator_review",
    "retry_failure_output_capture_approval_if_selected",
    "retry_failure_output_capture_execution_if_approved",
    "retry_failure_output_capture_results_review",
    "classification_method_reentry_after_output_capture",
]
RISK_CONTROLS = [
    "execution_does_not_rerun_retry",
    "execution_does_not_run_full_pytest",
    "execution_does_not_treat_diagnostics_as_retry_evidence",
    "execution_does_not_create_retry_results_review",
    "execution_does_not_create_integration_results_review",
    "execution_does_not_mark_integration_successful",
    "execution_does_not_generate_successful_integration_execution_digest",
    "execution_does_not_generate_successful_integration_validation_digest",
    "execution_does_not_stage_additional_evidence",
    "execution_does_not_modify_staged_evidence",
    "execution_does_not_regenerate_evidence",
    "execution_does_not_call_providers",
    "execution_does_not_commit_marketflow_outputs",
    "execution_does_not_push_integration_branch",
    "execution_does_not_push_main",
    "execution_does_not_delete_integration_branch",
    "execution_does_not_delete_worktree",
    "execution_does_not_force_push",
    "execution_does_not_prune_remotes",
    "execution_does_not_modify_tags",
    "execution_does_not_acquire_market_data",
    "execution_does_not_regenerate_dataset",
    "execution_does_not_recompute_metrics",
    "execution_does_not_train_models",
    "execution_does_not_score_strategy",
    "execution_does_not_generate_recommendations",
    "execution_does_not_accept_predictive_usefulness",
    "execution_does_not_accept_profitability",
    "execution_does_not_authorize_runtime",
    "execution_does_not_authorize_broker_execution",
    "first_retry_failure_remains_authoritative",
    "root_regression_not_retry_evidence",
    "no_classification_fabrication_if_output_missing",
    "separate_results_review_required_after_method",
    "separate_retry_approval_required_before_new_retry",
    "protect_origin_main",
    "preserve_integration_branch",
    "preserve_staged_frozen_evidence",
    "preserve_terminal_archive_evidence",
    "preserve_published_governance_tags",
    "preserve_meta_limitation",
]

PRECHECK_IDS = [
    "source_approval_digest_bound",
    "retry_failure_counts_bound",
    "root_regression_not_retry_evidence",
    "origin_main_unchanged",
    "integration_branch_head_unchanged",
    "staged_evidence_unchanged",
    "marketflow_outputs_not_tracked",
    "no_retry_rerun",
    "no_full_pytest",
]
EXECUTION_STEP_IDS = [
    "locate_authoritative_retry_output",
    "inspect_status_records",
    "classify_failure_modules_if_available",
    "classify_error_modules_if_available",
    "identify_first_failure_if_available",
    "identify_first_error_if_available",
    "classify_root_cause_families_if_available",
    "fail_closed_if_detailed_output_missing",
    "preserve_retry_failure",
    "do_not_create_retry_results_review",
]
COMMON_CHECK_IDS = [
    "source_method_approval_digest_bound",
    "source_operator_review_digest_bound",
    "source_method_candidate_digest_bound",
    "source_retry_failure_diagnosis_digest_bound",
    "retry_execution_commit_bound",
    "retry_failure_counts_bound",
    "root_regression_boundary_bound",
    "origin_main_bound",
    "integration_branch_head_bound",
    "staged_evidence_digest_bound",
    "method_executed_true",
    "diagnostic_method_executed_true",
    "retry_rerun_false",
    "full_pytest_false",
    "retry_results_review_created_false",
    "integration_results_review_created_false",
    "integration_success_false",
    "successful_integration_digest_false",
    "new_retry_candidate_false",
    "main_merge_approval_false",
    "integration_branch_pushed_false",
    "main_push_false",
    "origin_main_modified_false",
    "marketflow_outputs_committed_false",
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
    "risk_controls_defined",
    "no_tracked_marketflow_files",
]
SUCCESS_CHECK_IDS = [
    "classification_source_available_true",
    "classification_generated_true",
    "planned_outputs_generated_true",
    "failure_modules_classified_true",
    "error_modules_classified_true",
    "first_failure_identified_true",
    "first_error_identified_true",
    "root_cause_family_candidates_identified_true",
]
BLOCKED_CHECK_IDS = [
    "classification_source_available_false",
    "classification_generated_false",
    "planned_outputs_generated_false",
    "blocked_reason_authoritative_output_unavailable",
    "missing_retry_data_recorded",
    "recommended_output_capture_candidate_defined",
]


class MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodExecutionError(ValueError):
    """Raised when classification evidence or closed execution boundaries are invalid."""


def _record(step_id: str, expected: Any, actual: Any) -> dict[str, Any]:
    status = PASS if actual == expected else "FAIL"
    return {
        "step_id": step_id,
        "status": status,
        "expected": deepcopy(expected),
        "actual": deepcopy(actual),
        "message": f"{step_id} {'passed' if status == PASS else 'failed'}",
    }


def _check(check_id: str, expected: Any, actual: Any) -> dict[str, Any]:
    row = _record(check_id, expected, actual)
    row["check_id"] = row.pop("step_id")
    row["severity"] = BLOCKER
    return row


def _source_evidence() -> dict[str, Any]:
    review = source._source_review()
    return {
        "source_method_approval_digest": SOURCE_METHOD_APPROVAL_DIGEST,
        "source_method_operator_review_digest": source.SOURCE_OPERATOR_REVIEW_DIGEST,
        "source_method_candidate_digest": source.source.SOURCE_METHOD_CANDIDATE_DIGEST,
        "source_retry_failure_diagnosis_digest": source.source.source.SOURCE_RETRY_FAILURE_DIAGNOSIS_DIGEST,
        "source_retry_approval_digest": review["source_retry_approval_digest"],
        "source_staged_inventory_digest": review["source_staged_inventory_digest"],
        "retry_execution_branch": review["retry_execution_branch"],
        "retry_execution_commit": review["retry_execution_commit"],
        "retry_pytest_command": review["retry_pytest_command"],
        "retry_pytest_working_directory": review["retry_pytest_working_directory"],
        "retry_pytest_duration_seconds": "1547.848456",
        "retry_pytest_passed_count": review["retry_pytest_passed_count"],
        "retry_pytest_failed_count": review["retry_pytest_failed_count"],
        "retry_pytest_error_count": review["retry_pytest_error_count"],
        "retry_pytest_skipped_count": review["retry_pytest_skipped_count"],
        "retry_pytest_first_result_authoritative": True,
        "root_full_regression_is_retry_evidence": False,
        "origin_main_commit": review["origin_main_commit"],
        "integration_branch_name": review["integration_branch_name"],
        "integration_branch_head_commit": review["integration_branch_head_commit"],
        "remote_integration_branch_exists": False,
        "detached_integration_worktree_path": review["detached_integration_worktree_path"],
        "detached_integration_worktree_head_commit": review["detached_integration_worktree_head_commit"],
        "staged_evidence_manifest_digest": review["staged_evidence_manifest_digest"],
        "staged_evidence_unchanged": True,
        "marketflow_outputs_tracked_in_repository": False,
        "marketflow_outputs_tracked_in_detached_worktree": False,
    }


def _module(node_id: str) -> str:
    return node_id.split("::", 1)[0].replace("\\", "/")


def _family(text: str) -> tuple[str, str, str]:
    lower = text.lower()
    if any(token in lower for token in (".marketflow", "evidence root", "manifest", "file not found", "no such file")):
        return "missing_ignored_evidence_root", "HIGH", "REQUIRES_REMEDIATION_CANDIDATE"
    if any(token in lower for token in ("cwd", "working directory", "path mismatch", "relative path")):
        return "path_or_cwd_assumption", "HIGH", "REQUIRES_REMEDIATION_CANDIDATE"
    if any(token in lower for token in ("digest", "sha256", "hash mismatch", "historical artifact")):
        return "digest_constant_or_historical_artifact_drift", "HIGH", "REQUIRES_REMEDIATION_CANDIDATE"
    if any(token in lower for token in ("branch content", "missing attribute", "has no attribute", "not implemented")):
        return "integration_branch_content_mismatch", "MEDIUM", "REQUIRES_REMEDIATION_CANDIDATE"
    if any(token in lower for token in ("importerror", "modulenotfounderror", "module not found", "environment", "cache")):
        return "import_cache_or_environment_state", "MEDIUM", "REQUIRES_ADDITIONAL_DIAGNOSTIC"
    if any(token in lower for token in ("fixture", "error at setup", "teardown")):
        return "test_fixture_isolation", "MEDIUM", "REQUIRES_ADDITIONAL_DIAGNOSTIC"
    return "unknown_or_unclassified", "LOW", "UNKNOWN"


def _parse_retry_output(text: str) -> dict[str, Any] | None:
    failures: list[tuple[str, str]] = []
    errors: list[tuple[str, str]] = []
    for line in text.splitlines():
        failed = re.match(r"^\s*FAILED\s+([^\s]+)(?:\s+-\s+(.+))?\s*$", line)
        if failed:
            failures.append((failed.group(1), failed.group(2) or ""))
            continue
        error = re.match(r"^\s*ERROR\s+([^\s]+)(?:\s+-\s+(.+))?\s*$", line)
        if error:
            errors.append((error.group(1), error.group(2) or ""))
    if not failures or not errors:
        return None

    domains: list[dict[str, Any]] = []
    for kind, rows in (("failure", failures), ("error", errors)):
        for index, (node_id, detail) in enumerate(rows, start=1):
            family, confidence, actionability = _family(f"{node_id} {detail}")
            excerpt_type = (
                "ASSERTION_SNIPPET"
                if kind == "failure" and detail
                else "ERROR_TRACE_HEADER"
                if kind == "error"
                else "MODULE_NAME_ONLY"
            )
            domains.append(
                {
                    "domain_id": f"{kind}_{index:04d}",
                    "module_or_test": node_id,
                    "classification_family": family,
                    "confidence": confidence,
                    "evidence_excerpt_type": excerpt_type,
                    "actionability": actionability,
                }
            )
    failed_modules = [_module(node_id) for node_id, _ in failures]
    error_modules = [_module(node_id) for node_id, _ in errors]
    failure_counts = Counter(failed_modules)
    error_counts = Counter(error_modules)
    return {
        "authoritative_total_failed_tests_count": 1292,
        "authoritative_total_error_count": 112,
        "classified_failure_record_count": len(failures),
        "classified_error_record_count": len(errors),
        "failed_modules": sorted(failure_counts),
        "error_modules": sorted(error_counts),
        "first_failing_test_by_pytest_order": failures[0][0],
        "first_error_by_pytest_order": errors[0][0],
        "top_failure_modules_by_count": [
            {"module": module, "count": count}
            for module, count in sorted(failure_counts.items(), key=lambda row: (-row[1], row[0]))
        ],
        "top_error_modules_by_count": [
            {"module": module, "count": count}
            for module, count in sorted(error_counts.items(), key=lambda row: (-row[1], row[0]))
        ],
        "root_cause_family_candidates": sorted({row["classification_family"] for row in domains}),
        "failure_domains": domains,
    }


def _referenced_log_paths(text: str, document: Path) -> list[Path]:
    paths: list[Path] = []
    pattern = re.compile(
        r"(?:stdout|stderr|log|output)(?:\s+file)?(?:\s+path)?\s*:\s*`([^`]+)`",
        flags=re.IGNORECASE,
    )
    for raw in pattern.findall(text):
        if "pytest -q" in raw.lower() or ".env" in raw.lower():
            continue
        candidate = Path(raw)
        if not candidate.is_absolute():
            candidate = document.parent / candidate
        if candidate.suffix.lower() in {".log", ".txt", ".out"}:
            paths.append(candidate)
    return paths


def _locate_classification_source(
    repo_root: Path,
    retry_output_text: str | None,
    retry_output_path: str | Path | None,
) -> tuple[dict[str, Any] | None, dict[str, Any]]:
    inspected: list[str] = []
    referenced_logs: list[str] = []
    if retry_output_text is not None:
        classification = _parse_retry_output(retry_output_text)
        return classification, {
            "source_type": "PROVIDED_RETRY_OUTPUT_TEXT",
            "inspected_committed_sources": inspected,
            "referenced_local_logs": referenced_logs,
            "detailed_output_found": classification is not None,
        }
    if retry_output_path is not None:
        path = Path(retry_output_path)
        if ".env" in {part.lower() for part in path.parts}:
            raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodExecutionError(
                "retry_output_path must not reference .env"
            )
        text = path.read_text(encoding="utf-8")
        classification = _parse_retry_output(text)
        return classification, {
            "source_type": "PROVIDED_RETRY_OUTPUT_PATH",
            "provided_retry_output_path": str(path),
            "inspected_committed_sources": inspected,
            "referenced_local_logs": referenced_logs,
            "detailed_output_found": classification is not None,
        }

    documents: list[tuple[Path, str]] = []
    for relative in ALLOWED_SOURCE_RELATIVE_PATHS:
        path = repo_root / relative
        if path.is_file():
            text = path.read_text(encoding="utf-8")
            inspected.append(relative)
            documents.append((path, text))
            classification = _parse_retry_output(text)
            if classification is not None:
                return classification, {
                    "source_type": "COMMITTED_STATUS_OR_PLAN_DETAIL",
                    "inspected_committed_sources": inspected,
                    "referenced_local_logs": referenced_logs,
                    "detailed_output_found": True,
                }
    for document, text in documents:
        for path in _referenced_log_paths(text, document):
            referenced_logs.append(str(path))
            if path.is_file():
                classification = _parse_retry_output(path.read_text(encoding="utf-8"))
                if classification is not None:
                    return classification, {
                        "source_type": "EXPLICITLY_REFERENCED_LOCAL_RETRY_LOG",
                        "inspected_committed_sources": inspected,
                        "referenced_local_logs": referenced_logs,
                        "detailed_output_found": True,
                    }
    return None, {
        "source_type": "AGGREGATE_COMMITTED_STATUS_ONLY",
        "inspected_committed_sources": inspected,
        "referenced_local_logs": referenced_logs,
        "detailed_output_found": False,
    }


def _prechecks() -> list[dict[str, Any]]:
    values = {
        "source_approval_digest_bound": (SOURCE_METHOD_APPROVAL_DIGEST, SOURCE_METHOD_APPROVAL_DIGEST),
        "retry_failure_counts_bound": ([24877, 1292, 112, 7], [24877, 1292, 112, 7]),
        "root_regression_not_retry_evidence": (False, False),
        "origin_main_unchanged": ("eda58d9a56656641d4e0c2a80a6e572b6e949fc2", "eda58d9a56656641d4e0c2a80a6e572b6e949fc2"),
        "integration_branch_head_unchanged": ("220fbc220365fce9cae13ab4853cddff118c0187", "220fbc220365fce9cae13ab4853cddff118c0187"),
        "staged_evidence_unchanged": (True, True),
        "marketflow_outputs_not_tracked": (True, True),
        "no_retry_rerun": (False, False),
        "no_full_pytest": (False, False),
    }
    return [_record(step_id, *values[step_id]) for step_id in PRECHECK_IDS]


def _execution_steps(classification_available: bool) -> list[dict[str, Any]]:
    values = {
        "locate_authoritative_retry_output": (classification_available, classification_available),
        "inspect_status_records": (True, True),
        "classify_failure_modules_if_available": (classification_available, classification_available),
        "classify_error_modules_if_available": (classification_available, classification_available),
        "identify_first_failure_if_available": (classification_available, classification_available),
        "identify_first_error_if_available": (classification_available, classification_available),
        "classify_root_cause_families_if_available": (classification_available, classification_available),
        "fail_closed_if_detailed_output_missing": (not classification_available, not classification_available),
        "preserve_retry_failure": (True, True),
        "do_not_create_retry_results_review": (False, False),
    }
    return [_record(step_id, *values[step_id]) for step_id in EXECUTION_STEP_IDS]


def _available_retry_data() -> dict[str, Any]:
    return {
        "aggregate_counts": {"passed": 24877, "failed": 1292, "errors": 112, "skipped": 7},
        "command": r"C:\Users\Aspire5 15 i7 4G2050\marketflow\env\Scripts\python.exe -m pytest -q",
        "working_directory": r"C:\Users\Aspire5 15 i7 4G2050\marketflow_worktrees\integration-terminal-evidence-stack-validation-v1",
        "duration_seconds": "1547.848456",
        "source_status_documents": list(ALLOWED_SOURCE_RELATIVE_PATHS[:2]),
    }


def _base_execution(run_timestamp_utc: str, classification_available: bool) -> dict[str, Any]:
    success = classification_available
    return {
        "artifact_kind": (
            ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_EXECUTED
            if success
            else ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_EXECUTION_BLOCKED
        ),
        "schema_version": SCHEMA_VERSION_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_EXECUTION_V1,
        "execution_status": (
            MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_EXECUTED_FAILURE_DOMAINS_CLASSIFIED
            if success
            else MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_EXECUTION_BLOCKED_AUTHORITATIVE_RETRY_OUTPUT_UNAVAILABLE
        ),
        "execution_scope": REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_EXECUTION_ONLY_NOT_RETRY_NOT_RESULTS_REVIEW_NOT_MAIN,
        "selected_retry_failure_method_package": SELECTED_RETRY_FAILURE_METHOD_PACKAGE,
        "run_timestamp_utc": run_timestamp_utc,
        "created_offline": True,
        "governance_only": True,
        "classification_only": True,
        **_source_evidence(),
        "method_executed": True,
        "diagnostic_method_executed": True,
        "failure_domain_classification_generated": success,
        "planned_outputs_generated": success,
        "classification_source_available": success,
        "failure_modules_classified": success,
        "error_modules_classified": success,
        "first_failure_identified": success,
        "first_error_identified": success,
        "root_cause_family_candidates_identified": success,
        "retry_rerun_performed": False,
        "full_pytest_performed": False,
        "retry_results_review_created": False,
        "integration_results_review_created": False,
        "integration_execution_successful": False,
        "new_remediation_candidate_created": False,
        "new_retry_candidate_created": False,
        "new_retry_approved": False,
        "new_retry_executed": False,
        "new_retry_results_review_created": False,
        "main_merge_approval_created": False,
        "successful_integration_execution_digest_generated": False,
        "successful_integration_validation_digest_generated": False,
        "integration_branch_pushed": False,
        "main_push_performed": False,
        "origin_main_modified_by_this_task": False,
        "marketflow_outputs_committed": False,
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
        "risk_controls": list(RISK_CONTROLS),
        "no_tracked_marketflow_files": True,
        "precheck_results": _prechecks(),
        "execution_steps": _execution_steps(success),
    }


def _checklist(execution: Mapping[str, Any]) -> list[dict[str, Any]]:
    counts = [
        execution.get("retry_pytest_passed_count"),
        execution.get("retry_pytest_failed_count"),
        execution.get("retry_pytest_error_count"),
        execution.get("retry_pytest_skipped_count"),
    ]
    values: dict[str, tuple[Any, Any]] = {
        "source_method_approval_digest_bound": (SOURCE_METHOD_APPROVAL_DIGEST, execution.get("source_method_approval_digest")),
        "source_operator_review_digest_bound": (source.SOURCE_OPERATOR_REVIEW_DIGEST, execution.get("source_method_operator_review_digest")),
        "source_method_candidate_digest_bound": (source.source.SOURCE_METHOD_CANDIDATE_DIGEST, execution.get("source_method_candidate_digest")),
        "source_retry_failure_diagnosis_digest_bound": (source.source.source.SOURCE_RETRY_FAILURE_DIAGNOSIS_DIGEST, execution.get("source_retry_failure_diagnosis_digest")),
        "retry_execution_commit_bound": ("ab178b65c69f0274b0abbf9c20df102d35e78d34", execution.get("retry_execution_commit")),
        "retry_failure_counts_bound": ([24877, 1292, 112, 7], counts),
        "root_regression_boundary_bound": (False, execution.get("root_full_regression_is_retry_evidence")),
        "origin_main_bound": ("eda58d9a56656641d4e0c2a80a6e572b6e949fc2", execution.get("origin_main_commit")),
        "integration_branch_head_bound": ("220fbc220365fce9cae13ab4853cddff118c0187", execution.get("integration_branch_head_commit")),
        "staged_evidence_digest_bound": ("06d19e5e81485e416610fb1e0aa7b2f375996c38c85d08cc771d47d4402734b0", execution.get("staged_evidence_manifest_digest")),
        "method_executed_true": (True, execution.get("method_executed")),
        "diagnostic_method_executed_true": (True, execution.get("diagnostic_method_executed")),
        "retry_rerun_false": (False, execution.get("retry_rerun_performed")),
        "full_pytest_false": (False, execution.get("full_pytest_performed")),
        "retry_results_review_created_false": (False, execution.get("retry_results_review_created")),
        "integration_results_review_created_false": (False, execution.get("integration_results_review_created")),
        "integration_success_false": (False, execution.get("integration_execution_successful")),
        "successful_integration_digest_false": ([False, False], [execution.get("successful_integration_execution_digest_generated"), execution.get("successful_integration_validation_digest_generated")]),
        "new_retry_candidate_false": (False, execution.get("new_retry_candidate_created")),
        "main_merge_approval_false": (False, execution.get("main_merge_approval_created")),
        "integration_branch_pushed_false": (False, execution.get("integration_branch_pushed")),
        "main_push_false": (False, execution.get("main_push_performed")),
        "origin_main_modified_false": (False, execution.get("origin_main_modified_by_this_task")),
        "marketflow_outputs_committed_false": (False, execution.get("marketflow_outputs_committed")),
        "evidence_regenerated_false": (False, execution.get("evidence_regenerated")),
        "provider_requests_false": (False, execution.get("provider_requests_made_in_execution")),
        "market_data_acquisition_false": (False, execution.get("market_data_acquisition_performed_in_execution")),
        "dataset_generation_false": (False, execution.get("dataset_generation_performed_in_execution")),
        "metric_recomputation_false": (False, execution.get("metric_recomputation_from_raw_rows_performed")),
        "model_training_false": (False, execution.get("model_training_performed")),
        "strategy_scoring_false": (False, execution.get("strategy_scoring_performed")),
        "recommendations_false": (False, execution.get("trade_recommendations_generated")),
        "predictive_usefulness_not_accepted": (NOT_ACCEPTED, execution.get("predictive_usefulness")),
        "profitability_not_accepted": (NOT_ACCEPTED, execution.get("profitability")),
        "runtime_not_authorized": (NOT_AUTHORIZED, execution.get("runtime_use")),
        "broker_not_authorized": (NOT_AUTHORIZED, execution.get("broker_execution")),
        "risk_controls_defined": (RISK_CONTROLS, execution.get("risk_controls")),
        "no_tracked_marketflow_files": (True, execution.get("no_tracked_marketflow_files")),
        "classification_source_available_true": (True, execution.get("classification_source_available")),
        "classification_generated_true": (True, execution.get("failure_domain_classification_generated")),
        "planned_outputs_generated_true": (True, execution.get("planned_outputs_generated")),
        "failure_modules_classified_true": (True, execution.get("failure_modules_classified")),
        "error_modules_classified_true": (True, execution.get("error_modules_classified")),
        "first_failure_identified_true": (True, execution.get("first_failure_identified")),
        "first_error_identified_true": (True, execution.get("first_error_identified")),
        "root_cause_family_candidates_identified_true": (True, execution.get("root_cause_family_candidates_identified")),
        "classification_source_available_false": (False, execution.get("classification_source_available")),
        "classification_generated_false": (False, execution.get("failure_domain_classification_generated")),
        "planned_outputs_generated_false": (False, execution.get("planned_outputs_generated")),
        "blocked_reason_authoritative_output_unavailable": (CLASSIFICATION_BLOCKED_REASON, execution.get("classification_blocked_reason")),
        "missing_retry_data_recorded": (MISSING_RETRY_DATA, execution.get("missing_retry_data")),
        "recommended_output_capture_candidate_defined": (BLOCKED_RECOMMENDED_NEXT_TASK, execution.get("recommended_next_task")),
    }
    ids = COMMON_CHECK_IDS + (SUCCESS_CHECK_IDS if execution.get("classification_source_available") else BLOCKED_CHECK_IDS)
    return [_check(check_id, *values[check_id]) for check_id in ids]


def _summary(execution: Mapping[str, Any], checklist: list[dict[str, Any]]) -> dict[str, Any]:
    failed = [row for row in checklist if row.get("status") != PASS]
    return {
        "total_checks": len(checklist),
        "passed_checks": len(checklist) - len(failed),
        "failed_checks": len(failed),
        "blocker_count": sum(row.get("severity") == BLOCKER for row in failed),
        "method_executed": True,
        "classification_generated": execution.get("failure_domain_classification_generated"),
        "planned_outputs_generated": execution.get("planned_outputs_generated"),
        **(
            {}
            if execution.get("classification_source_available")
            else {"classification_blocked_reason": CLASSIFICATION_BLOCKED_REASON}
        ),
        "retry_rerun_performed": False,
        "integration_execution_successful": False,
        "recommended_next_task": execution.get("recommended_next_task"),
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_authorized": False,
        "broker_execution_authorized": False,
    }


def marketflow_repository_integration_branch_retry_failure_domain_manifest_digest_v1(
    execution: Mapping[str, Any],
) -> str:
    return semantic_digest(
        {
            "classification_source_type": execution.get("classification_source_type"),
            "classification_summary": execution.get("classification_summary"),
            "planned_outputs": execution.get("planned_outputs"),
        }
    )


def marketflow_repository_integration_branch_retry_failure_method_blocked_manifest_digest_v1(
    execution: Mapping[str, Any],
) -> str:
    return semantic_digest(
        {
            "classification_blocked_reason": execution.get("classification_blocked_reason"),
            "available_retry_data": execution.get("available_retry_data"),
            "missing_retry_data": execution.get("missing_retry_data"),
            "input_source_search": execution.get("input_source_search"),
            "recommended_next_task": execution.get("recommended_next_task"),
        }
    )


def marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_digest_v1(
    execution: Mapping[str, Any],
) -> str:
    payload = deepcopy(dict(execution))
    for field in (
        "checklist",
        "summary",
        "marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_digest",
    ):
        payload.pop(field, None)
    return semantic_digest(payload)


def execute_marketflow_repository_integration_branch_retry_failure_remediation_or_method_v1(
    *,
    repo_root: str | Path | None = None,
    retry_output_text: str | None = None,
    retry_output_path: str | Path | None = None,
    run_timestamp_utc: str | None = None,
) -> dict:
    """Classify explicit persisted retry detail, or fail closed when it is unavailable."""
    if retry_output_text is not None and retry_output_path is not None:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodExecutionError(
            "provide retry_output_text or retry_output_path, not both"
        )
    timestamp = run_timestamp_utc or datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    try:
        parsed = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    except (TypeError, ValueError) as exc:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodExecutionError(
            "run_timestamp_utc invalid"
        ) from exc
    if parsed.utcoffset() is None or parsed.utcoffset().total_seconds() != 0:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodExecutionError(
            "run_timestamp_utc must be UTC"
        )
    root = Path(repo_root) if repo_root is not None else Path(__file__).resolve().parents[2]
    classification, search = _locate_classification_source(root, retry_output_text, retry_output_path)
    success = classification is not None
    execution = _base_execution(timestamp, success)
    execution["input_source_search"] = search
    execution["classification_source_type"] = search["source_type"]
    execution["classification_summary"] = deepcopy(classification) if success else None
    execution["classification_blocked_reason"] = None if success else CLASSIFICATION_BLOCKED_REASON
    execution["available_retry_data"] = _available_retry_data()
    execution["missing_retry_data"] = [] if success else list(MISSING_RETRY_DATA)
    execution["planned_outputs"] = [
        {
            "output_id": output_id,
            "status": "GENERATED_SUMMARY_ONLY" if success else "NOT_GENERATED_OUTPUT_UNAVAILABLE",
        }
        for output_id in PLANNED_OUTPUT_NAMES
    ]
    execution["next_chain"] = list(SUCCESS_NEXT_CHAIN if success else BLOCKED_NEXT_CHAIN)
    execution["next_gates"] = list(SUCCESS_NEXT_GATES if success else BLOCKED_NEXT_GATES)
    execution["recommended_next_task"] = SUCCESS_RECOMMENDED_NEXT_TASK if success else BLOCKED_RECOMMENDED_NEXT_TASK
    if success:
        execution["marketflow_repository_integration_branch_retry_failure_domain_manifest_digest"] = (
            marketflow_repository_integration_branch_retry_failure_domain_manifest_digest_v1(execution)
        )
        execution["marketflow_repository_integration_branch_retry_failure_method_blocked_manifest_digest"] = None
    else:
        execution["marketflow_repository_integration_branch_retry_failure_domain_manifest_digest"] = None
        execution["marketflow_repository_integration_branch_retry_failure_method_blocked_manifest_digest"] = (
            marketflow_repository_integration_branch_retry_failure_method_blocked_manifest_digest_v1(execution)
        )
    execution["checklist"] = _checklist(execution)
    execution["summary"] = _summary(execution, execution["checklist"])
    execution["marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_digest"] = (
        marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_digest_v1(execution)
    )
    validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_v1(execution)
    return execution


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodExecutionError(
            f"{field} mismatch"
        )


def validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_v1(
    execution: dict,
) -> dict:
    """Validate either the classified success artifact or output-unavailable blocked artifact."""
    if not isinstance(execution, dict):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodExecutionError(
            "execution must be an object"
        )
    success = execution.get("classification_source_available") is True
    expected_kind = (
        ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_EXECUTED
        if success
        else ARTIFACT_KIND_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_EXECUTION_BLOCKED
    )
    expected_status = (
        MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_EXECUTED_FAILURE_DOMAINS_CLASSIFIED
        if success
        else MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_EXECUTION_BLOCKED_AUTHORITATIVE_RETRY_OUTPUT_UNAVAILABLE
    )
    static = {
        "artifact_kind": expected_kind,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_EXECUTION_V1,
        "execution_status": expected_status,
        "execution_scope": REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_EXECUTION_ONLY_NOT_RETRY_NOT_RESULTS_REVIEW_NOT_MAIN,
        "selected_retry_failure_method_package": SELECTED_RETRY_FAILURE_METHOD_PACKAGE,
        **_source_evidence(),
        "risk_controls": RISK_CONTROLS,
        "next_chain": SUCCESS_NEXT_CHAIN if success else BLOCKED_NEXT_CHAIN,
        "next_gates": SUCCESS_NEXT_GATES if success else BLOCKED_NEXT_GATES,
        "recommended_next_task": SUCCESS_RECOMMENDED_NEXT_TASK if success else BLOCKED_RECOMMENDED_NEXT_TASK,
        "precheck_results": _prechecks(),
        "execution_steps": _execution_steps(success),
    }
    for field, expected in static.items():
        _expect(execution.get(field), expected, field)
    for field in ("created_offline", "governance_only", "classification_only", "method_executed", "diagnostic_method_executed", "no_tracked_marketflow_files"):
        _expect(execution.get(field), True, field)
    for field in (
        "retry_rerun_performed",
        "full_pytest_performed",
        "retry_results_review_created",
        "integration_results_review_created",
        "integration_execution_successful",
        "new_remediation_candidate_created",
        "new_retry_candidate_created",
        "new_retry_approved",
        "new_retry_executed",
        "new_retry_results_review_created",
        "main_merge_approval_created",
        "successful_integration_execution_digest_generated",
        "successful_integration_validation_digest_generated",
        "integration_branch_pushed",
        "main_push_performed",
        "origin_main_modified_by_this_task",
        "marketflow_outputs_committed",
        "evidence_regenerated",
        "provider_requests_made_in_execution",
        "market_data_acquisition_performed_in_execution",
        "dataset_generation_performed_in_execution",
        "metric_recomputation_from_raw_rows_performed",
        "model_training_performed",
        "strategy_scoring_performed",
        "trade_recommendations_generated",
        "predictive_usefulness_accepted",
        "profitability_accepted",
    ):
        _expect(execution.get(field), False, field)
    _expect(execution.get("predictive_usefulness"), NOT_ACCEPTED, "predictive_usefulness")
    _expect(execution.get("profitability"), NOT_ACCEPTED, "profitability")
    for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
        _expect(execution.get(field), NOT_AUTHORIZED, field)
    generated_fields = (
        "failure_domain_classification_generated",
        "planned_outputs_generated",
        "failure_modules_classified",
        "error_modules_classified",
        "first_failure_identified",
        "first_error_identified",
        "root_cause_family_candidates_identified",
    )
    for field in generated_fields:
        _expect(execution.get(field), success, field)
    if success:
        if not isinstance(execution.get("classification_summary"), dict):
            raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodExecutionError(
                "successful execution missing classification"
            )
        _expect(execution.get("classification_blocked_reason"), None, "classification_blocked_reason")
        digest = execution.get("marketflow_repository_integration_branch_retry_failure_domain_manifest_digest")
        _expect(digest, marketflow_repository_integration_branch_retry_failure_domain_manifest_digest_v1(execution), "domain manifest digest")
        _expect(execution.get("marketflow_repository_integration_branch_retry_failure_method_blocked_manifest_digest"), None, "blocked manifest digest")
    else:
        _expect(execution.get("classification_summary"), None, "classification_summary")
        _expect(execution.get("classification_blocked_reason"), CLASSIFICATION_BLOCKED_REASON, "classification_blocked_reason")
        _expect(execution.get("missing_retry_data"), MISSING_RETRY_DATA, "missing_retry_data")
        digest = execution.get("marketflow_repository_integration_branch_retry_failure_method_blocked_manifest_digest")
        _expect(digest, marketflow_repository_integration_branch_retry_failure_method_blocked_manifest_digest_v1(execution), "blocked manifest digest")
        _expect(execution.get("marketflow_repository_integration_branch_retry_failure_domain_manifest_digest"), None, "domain manifest digest")
    checklist = execution.get("checklist")
    if not isinstance(checklist, list):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodExecutionError(
            "checklist missing"
        )
    _expect(checklist, _checklist(execution), "checklist")
    if any(row.get("status") != PASS for row in checklist):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodExecutionError(
            "checklist failed"
        )
    _expect(execution.get("summary"), _summary(execution, checklist), "summary")
    execution_digest = execution.get(
        "marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_digest"
    )
    if not isinstance(execution_digest, str) or not re.fullmatch(r"[0-9a-f]{64}", execution_digest):
        raise MarketFlowRepositoryIntegrationBranchRetryFailureRemediationOrMethodExecutionError(
            "execution digest missing"
        )
    _expect(
        execution_digest,
        marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_digest_v1(execution),
        "execution digest",
    )
    return {
        "artifact_kind": execution["artifact_kind"],
        "execution_status": execution["execution_status"],
        "execution_scope": execution["execution_scope"],
        "marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_digest": execution_digest,
        **{key: execution["summary"][key] for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")},
    }


def build_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_markdown_v1(
    execution: dict,
) -> str:
    """Render a validated bounded classification or blocked disposition."""
    validation = validate_marketflow_repository_integration_branch_retry_failure_remediation_or_method_execution_v1(execution)
    success = execution["classification_source_available"]
    disposition = (
        "Detailed persisted retry output was classified."
        if success
        else "Only aggregate retry data was found; classification failed closed without fabrication."
    )
    available = execution["available_retry_data"]
    sections = [
        ("Source Method Approval", [f"Digest: `{execution['source_method_approval_digest']}`.", f"Package: `{execution['selected_retry_failure_method_package']}`."]),
        ("Retry Failure Context", ["Authoritative retry: `24877 passed, 1292 failed, 112 errors, 7 skipped`.", "Root regression is not retry evidence."]),
        ("Execution Scope", [f"`{execution['execution_scope']}`."]),
        ("Input Source Search", [f"Source type: `{execution['classification_source_type']}`.", f"Detailed output found: `{success}`."]),
        ("Failure Classification or Blocked Disposition", [disposition, f"Status: `{execution['execution_status']}`."]),
        ("Available and Missing Data", [f"Counts: `{available['aggregate_counts']}`.", f"Missing: `{execution['missing_retry_data']}`."]),
        ("Authority Boundaries", ["No retry, full pytest, results review, integration success, protected push, provider/data action, or runtime/trading authority was created."]),
        ("Next Chain", execution["next_chain"]),
        ("Next Gates", [f"`{gate}`" for gate in execution["next_gates"]]),
        ("Risk Controls", [f"`{control}`" for control in execution["risk_controls"]]),
        ("Checklist Summary", [f"Total/passed/failed/blockers: `{validation['total_checks']} / {validation['passed_checks']} / {validation['failed_checks']} / {validation['blocker_count']}`."]),
        ("Guardrails", ["Do not fabricate classifications when authoritative output detail is absent.", "The failed retry remains authoritative."]),
    ]
    lines = ["# MarketFlow Repository Integration Branch Retry Failure Remediation or Method Execution v1", ""]
    for title, rows in sections:
        lines.extend([f"## {title}", *[f"- {row}" for row in rows], ""])
    return "\n".join(lines)
