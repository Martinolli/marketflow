"""Offline attestation-bound approval for future repository tag execution."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Iterable, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import (
    marketflow_repository_tagging_release_strategy_operator_review_service as source_review_service,
)


ARTIFACT_KIND_MARKETFLOW_REPOSITORY_TAGGING_RELEASE_STRATEGY_APPROVED = (
    "MARKETFLOW_REPOSITORY_TAGGING_RELEASE_STRATEGY_APPROVED"
)
SCHEMA_VERSION_MARKETFLOW_REPOSITORY_TAGGING_RELEASE_STRATEGY_APPROVAL_V1 = (
    "marketflow_repository_tagging_release_strategy_approval_v1"
)
MARKETFLOW_REPOSITORY_TAGGING_RELEASE_STRATEGY_APPROVED = (
    "MARKETFLOW_REPOSITORY_TAGGING_RELEASE_STRATEGY_APPROVED"
)
REPOSITORY_TAGGING_RELEASE_STRATEGY_APPROVAL_ONLY_NOT_TAGGING_NOT_MERGE_NOT_DELETE_NOT_MAIN = (
    "REPOSITORY_TAGGING_RELEASE_STRATEGY_APPROVAL_ONLY_NOT_TAGGING_NOT_MERGE_NOT_DELETE_NOT_MAIN"
)
MARKETFLOW_REPOSITORY_TAGGING_RELEASE_STRATEGY_APPROVAL_VALID = (
    "MARKETFLOW_REPOSITORY_TAGGING_RELEASE_STRATEGY_APPROVAL_VALID"
)

SELECTED_TAGGING_PACKAGE = (
    source_review_service.source_candidate_service.PACKAGE_TERMINAL_EXPECTANCY_LAB_ARCHIVE_TAGS
)
OPERATOR_DECISION_APPROVE_REPOSITORY_TAGGING_RELEASE_STRATEGY = (
    "APPROVE_REPOSITORY_TAGGING_RELEASE_STRATEGY"
)
OPERATOR_ATTESTATION_VERSION_MARKETFLOW_REPOSITORY_TAGGING_RELEASE_STRATEGY_APPROVAL_V1 = (
    "marketflow_repository_tagging_release_strategy_approval_operator_attestation_v1"
)
REQUIRED_MARKETFLOW_REPOSITORY_TAGGING_RELEASE_STRATEGY_APPROVAL_ATTESTATION_PHRASE = (
    "APPROVE REPOSITORY TAGGING RELEASE STRATEGY "
    "PACKAGE_TERMINAL_EXPECTANCY_LAB_ARCHIVE_TAGS MARKETFLOW EXPECTANCY LAB "
    "ARCHIVE TAGS FINAL ARCHIVE NOT READY ARCHIVE RECORD NOT READY OPERATOR "
    "SELECTION OPTION A READINESS NOT READY "
    "REPOSITORY_TAGGING_RELEASE_STRATEGY_APPROVAL_ONLY_NOT_TAGGING_NOT_MERGE_NOT_DELETE_NOT_MAIN"
)

EXPECTED_SOURCE_OPERATOR_REVIEW_DIGEST = (
    "8fbb5367af9cc114e9d4de40781cad351b73aa2cfb7581bb2e1b33d9b736922b"
)
EXPECTED_SOURCE_CANDIDATE_DIGEST = source_review_service.EXPECTED_SOURCE_CANDIDATE_DIGEST
EXPECTED_SOURCE_INVENTORY_OPERATOR_REVIEW_DIGEST = (
    source_review_service.EXPECTED_SOURCE_OPERATOR_REVIEW_DIGEST
)
EXPECTED_SOURCE_INVENTORY_PLAN_DIGEST = source_review_service.EXPECTED_SOURCE_INVENTORY_PLAN_DIGEST
EXPECTED_SOURCE_FINAL_ARCHIVE_DIGEST = source_review_service.EXPECTED_SOURCE_FINAL_ARCHIVE_DIGEST
EXPECTED_SOURCE_ARCHIVE_DIGEST = source_review_service.EXPECTED_SOURCE_ARCHIVE_DIGEST
EXPECTED_SOURCE_OPERATOR_SELECTION_DIGEST = source_review_service.EXPECTED_SOURCE_OPERATOR_SELECTION_DIGEST
EXPECTED_SOURCE_CLOSURE_DIGEST = source_review_service.EXPECTED_SOURCE_CLOSURE_DIGEST
EXPECTED_SOURCE_ACCEPTANCE_READINESS_DIGEST = (
    source_review_service.EXPECTED_SOURCE_ACCEPTANCE_READINESS_DIGEST
)
EXPECTED_SOURCE_REASSESSMENT_DIGEST = source_review_service.EXPECTED_SOURCE_REASSESSMENT_DIGEST
EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST = source_review_service.EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST
EXPECTED_SOURCE_BACKTEST_ROWS_DIGEST = source_review_service.EXPECTED_SOURCE_BACKTEST_ROWS_DIGEST
EXPECTED_SOURCE_METRIC_REPORT_DIGEST = source_review_service.EXPECTED_SOURCE_METRIC_REPORT_DIGEST
EXPECTED_SOURCE_RECORDS_DIGEST = source_review_service.EXPECTED_SOURCE_RECORDS_DIGEST
EXPECTED_ORIGIN_MAIN_COMMIT = source_review_service.EXPECTED_ORIGIN_MAIN_COMMIT
EXPECTED_SOURCE_OPERATOR_REVIEW_COMMIT = "deb8ad3e84c73e94880816e646bd2ee28f5b3769"
SOURCE_EVIDENCE = deepcopy(source_review_service.SOURCE_EVIDENCE)

APPROVED_TERMINAL_TAG_NAMES = list(
    source_review_service.source_candidate_service.TERMINAL_TAG_NAMES
)
NOT_ACCEPTED = "not accepted"
NOT_AUTHORIZED = "NOT_AUTHORIZED"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

REQUIRED_TRUE_OPERATOR_CONFIRMATION_FIELDS = [
    "operator_confirms_approval_scope_only",
    "operator_confirms_tags_not_created",
    "operator_confirms_tags_not_pushed",
    "operator_confirms_no_merge",
    "operator_confirms_no_branch_delete",
    "operator_confirms_no_remote_delete",
    "operator_confirms_no_main_push",
    "operator_confirms_no_force_push",
    "operator_confirms_no_remote_prune",
    "operator_confirms_origin_main_not_modified",
    "operator_confirms_no_provider_requests",
    "operator_confirms_no_market_data_acquisition",
    "operator_confirms_no_dataset_generation",
    "operator_confirms_no_metric_recomputation",
    "operator_confirms_no_model_training",
    "operator_confirms_no_strategy_scoring",
    "operator_confirms_no_trade_recommendations",
    "operator_confirms_no_predictive_usefulness_acceptance",
    "operator_confirms_no_profitability_acceptance",
    "operator_confirms_runtime_not_authorized",
    "operator_confirms_broker_not_authorized",
    "operator_confirms_no_api_key_storage_or_printing",
    "operator_confirms_no_raw_payload_commit",
]

NEXT_CHAIN = [
    "Repository Tagging Execution v1, if separately invoked.",
    "Repository Merge Strategy Candidate v1, only after tagging execution or explicit skip decision.",
    "Repository Branch Cleanup Candidate v1, only after merge/tag strategy is settled.",
    "Cleanup execution only after separate approval, backup/bundle, and protected-branch confirmation.",
    "Main push only if separately approved and protected.",
]

NEXT_GATES = [
    "repository_tagging_execution_if_approved",
    "repository_merge_strategy_candidate_after_tagging",
    "repository_branch_cleanup_candidate_after_merge_tag_strategy",
    "repository_cleanup_approval_if_selected",
    "repository_cleanup_execution_if_approved",
    "main_push_only_if_separately_approved_and_protected",
]

RISK_CONTROLS = [
    "approval_does_not_create_tags",
    "approval_does_not_push_tags",
    "approval_does_not_merge",
    "approval_does_not_rebase",
    "approval_does_not_delete_branches",
    "approval_does_not_delete_remote_branches",
    "approval_does_not_push_main",
    "approval_does_not_force_push",
    "approval_does_not_prune_remotes",
    "approval_does_not_modify_origin_main",
    "approval_does_not_modify_marketflow_outputs",
    "approval_does_not_call_providers",
    "approval_does_not_acquire_market_data",
    "approval_does_not_regenerate_dataset",
    "approval_does_not_rerun_candidate",
    "approval_does_not_rerun_operator_review",
    "approval_does_not_rerun_inventory",
    "approval_does_not_rerun_evidence",
    "approval_does_not_recompute_metrics",
    "approval_does_not_train_models",
    "approval_does_not_score_strategy",
    "approval_does_not_generate_recommendations",
    "approval_does_not_accept_predictive_usefulness",
    "approval_does_not_accept_profitability",
    "approval_does_not_authorize_runtime",
    "approval_does_not_authorize_broker_execution",
    "selected_tags_are_approved_for_future_execution_only",
    "separate_execution_required_before_tag_creation",
    "protect_origin_main",
    "preserve_terminal_archive_evidence",
    "preserve_meta_limitation",
]

REQUIRED_CHECK_IDS = [
    "source_operator_review_digest_bound",
    "source_candidate_digest_bound",
    "source_inventory_plan_digest_bound",
    "source_final_archive_digest_bound",
    "source_archive_digest_bound",
    "source_operator_selection_digest_bound",
    "source_closure_digest_bound",
    "source_readiness_digest_bound",
    "source_reassessment_digest_bound",
    "source_results_review_digest_bound",
    "source_backtest_rows_digest_bound",
    "source_metric_report_digest_bound",
    "records_digest_bound",
    "origin_main_commit_bound",
    "operator_decision_matches",
    "operator_attestation_phrase_matches",
    "approval_scope_only",
    "selected_package_terminal_archive_tags",
    "approval_created_true",
    "strategy_selected_true",
    "strategy_approved_true",
    "strategy_authorized_true",
    "ready_for_tagging_execution_true",
    "strategy_executed_false",
    "approved_terminal_tag_count_4",
    "approved_terminal_tag_names_match",
    "approved_terminal_tags_not_created",
    "approved_terminal_tags_not_pushed",
    "supporting_packages_available_not_selected",
    "governance_tags_not_approved",
    "protection_tags_not_approved",
    "future_tag_message_template_approved",
    "git_tag_created_false",
    "git_tag_push_performed_false",
    "merge_performed_false",
    "rebase_performed_false",
    "branch_delete_performed_false",
    "remote_delete_performed_false",
    "main_push_false",
    "force_push_false",
    "remote_prune_false",
    "origin_main_modified_false",
    "marketflow_outputs_not_tracked",
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
]


class MarketFlowRepositoryTaggingReleaseStrategyApprovalError(ValueError):
    """Raised when evidence or attestation violates the approval-only contract."""


def build_marketflow_repository_tagging_release_strategy_approval_attestation_v1(
    *,
    operator_reference: str,
    operator_attestation_timestamp_utc: str,
    operator_attestation_phrase: str,
    operator_confirms_source_operator_review_digest: str,
    operator_confirms_source_candidate_digest: str,
    operator_confirms_source_inventory_plan_digest: str,
    operator_confirms_source_final_archive_digest: str,
    operator_confirms_origin_main_commit: str,
    operator_confirms_selected_tagging_package: str,
    operator_confirms_approved_terminal_tag_names: list[str],
    operator_confirms_approved_terminal_tag_count: int,
    operator_confirms_approval_scope_only: bool,
    operator_confirms_tags_not_created: bool,
    operator_confirms_tags_not_pushed: bool,
    operator_confirms_no_merge: bool,
    operator_confirms_no_branch_delete: bool,
    operator_confirms_no_remote_delete: bool,
    operator_confirms_no_main_push: bool,
    operator_confirms_no_force_push: bool,
    operator_confirms_no_remote_prune: bool,
    operator_confirms_origin_main_not_modified: bool,
    operator_confirms_no_provider_requests: bool,
    operator_confirms_no_market_data_acquisition: bool,
    operator_confirms_no_dataset_generation: bool,
    operator_confirms_no_metric_recomputation: bool,
    operator_confirms_no_model_training: bool,
    operator_confirms_no_strategy_scoring: bool,
    operator_confirms_no_trade_recommendations: bool,
    operator_confirms_no_predictive_usefulness_acceptance: bool,
    operator_confirms_no_profitability_acceptance: bool,
    operator_confirms_runtime_not_authorized: bool,
    operator_confirms_broker_not_authorized: bool,
    operator_confirms_no_api_key_storage_or_printing: bool,
    operator_confirms_no_raw_payload_commit: bool,
    selected_tagging_package: str = SELECTED_TAGGING_PACKAGE,
    operator_decision: str = OPERATOR_DECISION_APPROVE_REPOSITORY_TAGGING_RELEASE_STRATEGY,
) -> dict[str, Any]:
    """Construct the exact non-secret operator attestation object."""
    return {
        "operator_decision": operator_decision,
        "selected_tagging_package": selected_tagging_package,
        "operator_attestation_phrase": operator_attestation_phrase,
        "operator_attestation_timestamp_utc": operator_attestation_timestamp_utc,
        "operator_attestation_version": OPERATOR_ATTESTATION_VERSION_MARKETFLOW_REPOSITORY_TAGGING_RELEASE_STRATEGY_APPROVAL_V1,
        "operator_reference": operator_reference,
        "operator_confirms_source_operator_review_digest": operator_confirms_source_operator_review_digest,
        "operator_confirms_source_candidate_digest": operator_confirms_source_candidate_digest,
        "operator_confirms_source_inventory_plan_digest": operator_confirms_source_inventory_plan_digest,
        "operator_confirms_source_final_archive_digest": operator_confirms_source_final_archive_digest,
        "operator_confirms_origin_main_commit": operator_confirms_origin_main_commit,
        "operator_confirms_selected_tagging_package": operator_confirms_selected_tagging_package,
        "operator_confirms_approved_terminal_tag_names": list(operator_confirms_approved_terminal_tag_names),
        "operator_confirms_approved_terminal_tag_count": operator_confirms_approved_terminal_tag_count,
        "operator_confirms_approval_scope_only": operator_confirms_approval_scope_only,
        "operator_confirms_tags_not_created": operator_confirms_tags_not_created,
        "operator_confirms_tags_not_pushed": operator_confirms_tags_not_pushed,
        "operator_confirms_no_merge": operator_confirms_no_merge,
        "operator_confirms_no_branch_delete": operator_confirms_no_branch_delete,
        "operator_confirms_no_remote_delete": operator_confirms_no_remote_delete,
        "operator_confirms_no_main_push": operator_confirms_no_main_push,
        "operator_confirms_no_force_push": operator_confirms_no_force_push,
        "operator_confirms_no_remote_prune": operator_confirms_no_remote_prune,
        "operator_confirms_origin_main_not_modified": operator_confirms_origin_main_not_modified,
        "operator_confirms_no_provider_requests": operator_confirms_no_provider_requests,
        "operator_confirms_no_market_data_acquisition": operator_confirms_no_market_data_acquisition,
        "operator_confirms_no_dataset_generation": operator_confirms_no_dataset_generation,
        "operator_confirms_no_metric_recomputation": operator_confirms_no_metric_recomputation,
        "operator_confirms_no_model_training": operator_confirms_no_model_training,
        "operator_confirms_no_strategy_scoring": operator_confirms_no_strategy_scoring,
        "operator_confirms_no_trade_recommendations": operator_confirms_no_trade_recommendations,
        "operator_confirms_no_predictive_usefulness_acceptance": operator_confirms_no_predictive_usefulness_acceptance,
        "operator_confirms_no_profitability_acceptance": operator_confirms_no_profitability_acceptance,
        "operator_confirms_runtime_not_authorized": operator_confirms_runtime_not_authorized,
        "operator_confirms_broker_not_authorized": operator_confirms_broker_not_authorized,
        "operator_confirms_no_api_key_storage_or_printing": operator_confirms_no_api_key_storage_or_printing,
        "operator_confirms_no_raw_payload_commit": operator_confirms_no_raw_payload_commit,
    }


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise MarketFlowRepositoryTaggingReleaseStrategyApprovalError(
            f"{field} mismatch: expected {expected!r}, got {actual!r}"
        )


def _validate_operator_attestation(attestation: Mapping[str, Any]) -> None:
    if not isinstance(attestation, Mapping):
        raise MarketFlowRepositoryTaggingReleaseStrategyApprovalError(
            "operator attestation must be an object"
        )
    exact = {
        "operator_decision": OPERATOR_DECISION_APPROVE_REPOSITORY_TAGGING_RELEASE_STRATEGY,
        "selected_tagging_package": SELECTED_TAGGING_PACKAGE,
        "operator_attestation_phrase": REQUIRED_MARKETFLOW_REPOSITORY_TAGGING_RELEASE_STRATEGY_APPROVAL_ATTESTATION_PHRASE,
        "operator_attestation_version": OPERATOR_ATTESTATION_VERSION_MARKETFLOW_REPOSITORY_TAGGING_RELEASE_STRATEGY_APPROVAL_V1,
        "operator_confirms_source_operator_review_digest": EXPECTED_SOURCE_OPERATOR_REVIEW_DIGEST,
        "operator_confirms_source_candidate_digest": EXPECTED_SOURCE_CANDIDATE_DIGEST,
        "operator_confirms_source_inventory_plan_digest": EXPECTED_SOURCE_INVENTORY_PLAN_DIGEST,
        "operator_confirms_source_final_archive_digest": EXPECTED_SOURCE_FINAL_ARCHIVE_DIGEST,
        "operator_confirms_origin_main_commit": EXPECTED_ORIGIN_MAIN_COMMIT,
        "operator_confirms_selected_tagging_package": SELECTED_TAGGING_PACKAGE,
        "operator_confirms_approved_terminal_tag_names": APPROVED_TERMINAL_TAG_NAMES,
        "operator_confirms_approved_terminal_tag_count": 4,
    }
    for field, expected in exact.items():
        _expect(attestation.get(field), expected, field)
    for field in REQUIRED_TRUE_OPERATOR_CONFIRMATION_FIELDS:
        _expect(attestation.get(field), True, field)
    for field in ("operator_reference", "operator_attestation_timestamp_utc"):
        value = attestation.get(field)
        if not isinstance(value, str) or not value.strip():
            raise MarketFlowRepositoryTaggingReleaseStrategyApprovalError(
                f"{field} is required"
            )
    expected_fields = set(exact) | set(REQUIRED_TRUE_OPERATOR_CONFIRMATION_FIELDS) | {
        "operator_reference",
        "operator_attestation_timestamp_utc",
    }
    if set(attestation) != expected_fields:
        raise MarketFlowRepositoryTaggingReleaseStrategyApprovalError(
            "operator attestation fields mismatch"
        )


def _source_evidence(source_review: Mapping[str, Any] | None) -> dict[str, Any]:
    if source_review is None:
        return deepcopy(SOURCE_EVIDENCE)
    if not isinstance(source_review, dict):
        raise MarketFlowRepositoryTaggingReleaseStrategyApprovalError(
            "source_review must be an object"
        )
    try:
        source_review_service.validate_marketflow_repository_tagging_release_strategy_operator_review_v1(
            source_review
        )
    except (TypeError, ValueError, KeyError) as exc:
        raise MarketFlowRepositoryTaggingReleaseStrategyApprovalError(
            "source tagging operator review is invalid"
        ) from exc
    if source_review.get(
        "marketflow_repository_tagging_release_strategy_operator_review_digest"
    ) != EXPECTED_SOURCE_OPERATOR_REVIEW_DIGEST:
        raise MarketFlowRepositoryTaggingReleaseStrategyApprovalError(
            "source tagging operator review digest mismatch"
        )
    return deepcopy(source_review["source_evidence"])


def _selected_package() -> dict[str, Any]:
    return {
        "package_id": SELECTED_TAGGING_PACKAGE,
        "approval_status": "APPROVED_FOR_FUTURE_TAGGING_EXECUTION_ONLY",
        "selected": True,
        "approved": True,
        "authorized_for_future_execution": True,
        "executed": False,
        "tags_created": False,
        "tags_pushed": False,
        "merge_required": False,
        "main_push_required": False,
        "runtime_authority_created": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
    }


def _supporting_packages() -> list[dict[str, Any]]:
    return [
        {
            "package_id": package_id,
            "approval_status": "AVAILABLE_NOT_SELECTED",
            "selected": False,
            "approved": False,
            "executed": False,
            "tags_created": False,
        }
        for package_id in (
            source_review_service.source_candidate_service.PACKAGE_GOVERNANCE_MILESTONE_TAGS,
            source_review_service.source_candidate_service.PACKAGE_SOURCE_PROTECTION_TAGS,
            source_review_service.source_candidate_service.PACKAGE_NO_TAGGING_ARCHIVE_ONLY,
        )
    ]


def _approved_terminal_tags() -> list[dict[str, Any]]:
    return [
        {
            "tag_name": row["tag_name"],
            "tag_target_branch": row["tag_target_branch"],
            "tag_target_commit": row["tag_target_commit"],
            "approval_status": "APPROVED_FOR_FUTURE_TAGGING_EXECUTION_ONLY",
            "tag_status": "APPROVED_NOT_CREATED",
            "tag_type": "ANNOTATED_TAG_APPROVED_FOR_FUTURE_EXECUTION",
            "tag_created": False,
            "tag_pushed": False,
            "operator_approval_required_before_creation": False,
            "separate_execution_required": True,
            "main_push_required": False,
            "runtime_authority_created": False,
            "predictive_usefulness_accepted": False,
            "profitability_accepted": False,
            "tag_message_must_include_not_ready_boundary": True,
            "tag_message_must_include_no_runtime_authority": True,
            "tag_message_must_include_no_trading_authority": True,
        }
        for row in source_review_service.REVIEWED_CANDIDATE_TAG_DEFINITIONS[:4]
    ]


def _unapproved_tags(names: list[str]) -> list[dict[str, Any]]:
    return [
        {
            "tag_name": name,
            "approval_status": "NOT_APPROVED_AVAILABLE_FOR_FUTURE_SELECTION",
            "tag_created": False,
            "tag_pushed": False,
        }
        for name in names
    ]


def _base_approval(
    source_review: Mapping[str, Any] | None,
    operator_attestation: Mapping[str, Any],
) -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_REPOSITORY_TAGGING_RELEASE_STRATEGY_APPROVED,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_REPOSITORY_TAGGING_RELEASE_STRATEGY_APPROVAL_V1,
        "approval_status": MARKETFLOW_REPOSITORY_TAGGING_RELEASE_STRATEGY_APPROVED,
        "approval_scope": REPOSITORY_TAGGING_RELEASE_STRATEGY_APPROVAL_ONLY_NOT_TAGGING_NOT_MERGE_NOT_DELETE_NOT_MAIN,
        "selected_tagging_package": SELECTED_TAGGING_PACKAGE,
        "created_offline": True,
        "research_only": True,
        "planning_only": True,
        "operator_attestation_required": True,
        "operator_attestation": deepcopy(dict(operator_attestation)),
        "source_tagging_operator_review_artifact_kind": source_review_service.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_TAGGING_RELEASE_STRATEGY_OPERATOR_REVIEW_V1,
        "source_tagging_operator_review_status": source_review_service.MARKETFLOW_REPOSITORY_TAGGING_RELEASE_STRATEGY_OPERATOR_REVIEW_READY,
        "source_tagging_operator_review_scope": source_review_service.REPOSITORY_TAGGING_RELEASE_STRATEGY_OPERATOR_REVIEW_ONLY_NOT_APPROVAL_NOT_TAGGING_NOT_MERGE_NOT_DELETE_NOT_MAIN,
        "source_tagging_operator_review_digest": EXPECTED_SOURCE_OPERATOR_REVIEW_DIGEST,
        "source_tagging_candidate_digest": EXPECTED_SOURCE_CANDIDATE_DIGEST,
        "source_inventory_operator_review_digest": EXPECTED_SOURCE_INVENTORY_OPERATOR_REVIEW_DIGEST,
        "source_inventory_plan_digest": EXPECTED_SOURCE_INVENTORY_PLAN_DIGEST,
        "source_final_archive_digest": EXPECTED_SOURCE_FINAL_ARCHIVE_DIGEST,
        "source_archive_digest": EXPECTED_SOURCE_ARCHIVE_DIGEST,
        "source_operator_selection_digest": EXPECTED_SOURCE_OPERATOR_SELECTION_DIGEST,
        "source_closure_digest": EXPECTED_SOURCE_CLOSURE_DIGEST,
        "source_readiness_digest": EXPECTED_SOURCE_ACCEPTANCE_READINESS_DIGEST,
        "source_reassessment_digest": EXPECTED_SOURCE_REASSESSMENT_DIGEST,
        "source_results_review_digest": EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST,
        "source_backtest_rows_digest": EXPECTED_SOURCE_BACKTEST_ROWS_DIGEST,
        "source_metric_report_digest": EXPECTED_SOURCE_METRIC_REPORT_DIGEST,
        "source_records_digest": EXPECTED_SOURCE_RECORDS_DIGEST,
        "source_evidence": _source_evidence(source_review),
        "origin_main_commit": EXPECTED_ORIGIN_MAIN_COMMIT,
        "source_operator_review_commit": EXPECTED_SOURCE_OPERATOR_REVIEW_COMMIT,
        "source_snapshot_local_branch_count": 290,
        "source_snapshot_remote_branch_count": 261,
        "source_snapshot_total_branch_ref_count": 551,
        "source_post_plan_push_live_local_branch_count": 290,
        "source_post_plan_push_live_remote_branch_count": 262,
        "source_post_plan_push_live_total_branch_ref_count": 552,
        "source_inventory_operator_review_live_local_branch_count": 291,
        "source_inventory_operator_review_live_remote_branch_count": 263,
        "source_inventory_operator_review_live_total_branch_ref_count": 554,
        "source_tagging_candidate_live_local_branch_count": 292,
        "source_tagging_candidate_live_remote_branch_count": 264,
        "source_tagging_candidate_live_total_branch_ref_count": 556,
        "source_tagging_operator_review_live_local_branch_count": 293,
        "source_tagging_operator_review_live_remote_branch_count": 265,
        "source_tagging_operator_review_live_total_branch_ref_count": 558,
        "existing_tag_count": 28,
        "candidate_namespace_tag_count": 0,
        "source_category_summary": deepcopy(source_review_service.SOURCE_CATEGORY_SUMMARY),
        "repository_tagging_release_strategy_candidate_created": True,
        "repository_tagging_release_strategy_operator_review_created": True,
        "repository_tagging_release_strategy_operator_review_ready": True,
        "repository_tagging_release_strategy_selected": True,
        "repository_tagging_release_strategy_approved": True,
        "repository_tagging_release_strategy_authorized": True,
        "repository_tagging_release_strategy_approval_created": True,
        "ready_for_repository_tagging_execution": True,
        "repository_tagging_release_strategy_executed": False,
        "repository_tags_created": False,
        "repository_tags_pushed": False,
        "git_tag_created": False,
        "git_tag_push_performed": False,
        "git_merge_performed": False,
        "git_rebase_performed": False,
        "git_branch_delete_performed": False,
        "git_remote_delete_performed": False,
        "git_main_push_performed": False,
        "git_force_push_performed": False,
        "git_remote_prune_performed": False,
        "origin_main_modified_by_this_task": False,
        "repository_merge_strategy_candidate_created": False,
        "repository_cleanup_candidate_created": False,
        "repository_cleanup_executed": False,
        "provider_requests_made_in_approval": False,
        "market_data_acquisition_performed_in_approval": False,
        "dataset_generation_performed_in_approval": False,
        "metric_recomputation_from_raw_rows_performed": False,
        "model_training_performed": False,
        "strategy_scoring_performed": False,
        "trade_recommendations_generated": False,
        "raw_provider_payloads_committed": False,
        "api_keys_stored_or_printed": False,
        "predictive_usefulness": NOT_ACCEPTED,
        "predictive_usefulness_accepted": False,
        "profitability": NOT_ACCEPTED,
        "profitability_accepted": False,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "approved_tagging_package": _selected_package(),
        "supporting_tagging_packages": _supporting_packages(),
        "approved_terminal_tag_count": 4,
        "approved_terminal_tag_names": list(APPROVED_TERMINAL_TAG_NAMES),
        "approved_terminal_tags": _approved_terminal_tags(),
        "unapproved_governance_tags": _unapproved_tags(
            source_review_service.source_candidate_service.GOVERNANCE_TAG_NAMES
        ),
        "unapproved_source_protection_tags": _unapproved_tags(
            source_review_service.source_candidate_service.SOURCE_PROTECTION_TAG_NAMES
        ),
        "future_tag_message_template": source_review_service.source_candidate_service.FUTURE_TAG_MESSAGE_TEMPLATE,
        "future_tag_message_template_status": "APPROVED_FOR_FUTURE_TAGGING_EXECUTION_ONLY",
        "recommended_next_task": "MARKETFLOW_REPOSITORY_TAGGING_EXECUTION_V1",
        "next_chain": list(NEXT_CHAIN),
        "next_gates": list(NEXT_GATES),
        "risk_controls": list(RISK_CONTROLS),
        "tracked_marketflow_file_count": 0,
        "no_tracked_marketflow_files": True,
    }


def _check_values(approval: Mapping[str, Any]) -> dict[str, bool]:
    attestation = approval.get("operator_attestation", {})
    approved_tags = approval.get("approved_terminal_tags", [])
    supporting = approval.get("supporting_tagging_packages", [])
    governance = approval.get("unapproved_governance_tags", [])
    protection = approval.get("unapproved_source_protection_tags", [])
    return {
        "source_operator_review_digest_bound": approval.get("source_tagging_operator_review_digest") == EXPECTED_SOURCE_OPERATOR_REVIEW_DIGEST,
        "source_candidate_digest_bound": approval.get("source_tagging_candidate_digest") == EXPECTED_SOURCE_CANDIDATE_DIGEST,
        "source_inventory_plan_digest_bound": approval.get("source_inventory_plan_digest") == EXPECTED_SOURCE_INVENTORY_PLAN_DIGEST,
        "source_final_archive_digest_bound": approval.get("source_final_archive_digest") == EXPECTED_SOURCE_FINAL_ARCHIVE_DIGEST,
        "source_archive_digest_bound": approval.get("source_archive_digest") == EXPECTED_SOURCE_ARCHIVE_DIGEST,
        "source_operator_selection_digest_bound": approval.get("source_operator_selection_digest") == EXPECTED_SOURCE_OPERATOR_SELECTION_DIGEST,
        "source_closure_digest_bound": approval.get("source_closure_digest") == EXPECTED_SOURCE_CLOSURE_DIGEST,
        "source_readiness_digest_bound": approval.get("source_readiness_digest") == EXPECTED_SOURCE_ACCEPTANCE_READINESS_DIGEST,
        "source_reassessment_digest_bound": approval.get("source_reassessment_digest") == EXPECTED_SOURCE_REASSESSMENT_DIGEST,
        "source_results_review_digest_bound": approval.get("source_results_review_digest") == EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST,
        "source_backtest_rows_digest_bound": approval.get("source_backtest_rows_digest") == EXPECTED_SOURCE_BACKTEST_ROWS_DIGEST,
        "source_metric_report_digest_bound": approval.get("source_metric_report_digest") == EXPECTED_SOURCE_METRIC_REPORT_DIGEST,
        "records_digest_bound": approval.get("source_records_digest") == EXPECTED_SOURCE_RECORDS_DIGEST,
        "origin_main_commit_bound": approval.get("origin_main_commit") == EXPECTED_ORIGIN_MAIN_COMMIT,
        "operator_decision_matches": attestation.get("operator_decision") == OPERATOR_DECISION_APPROVE_REPOSITORY_TAGGING_RELEASE_STRATEGY,
        "operator_attestation_phrase_matches": attestation.get("operator_attestation_phrase") == REQUIRED_MARKETFLOW_REPOSITORY_TAGGING_RELEASE_STRATEGY_APPROVAL_ATTESTATION_PHRASE,
        "approval_scope_only": approval.get("approval_scope") == REPOSITORY_TAGGING_RELEASE_STRATEGY_APPROVAL_ONLY_NOT_TAGGING_NOT_MERGE_NOT_DELETE_NOT_MAIN and attestation.get("operator_confirms_approval_scope_only") is True,
        "selected_package_terminal_archive_tags": approval.get("selected_tagging_package") == SELECTED_TAGGING_PACKAGE,
        "approval_created_true": approval.get("repository_tagging_release_strategy_approval_created") is True,
        "strategy_selected_true": approval.get("repository_tagging_release_strategy_selected") is True,
        "strategy_approved_true": approval.get("repository_tagging_release_strategy_approved") is True,
        "strategy_authorized_true": approval.get("repository_tagging_release_strategy_authorized") is True,
        "ready_for_tagging_execution_true": approval.get("ready_for_repository_tagging_execution") is True,
        "strategy_executed_false": approval.get("repository_tagging_release_strategy_executed") is False,
        "approved_terminal_tag_count_4": approval.get("approved_terminal_tag_count") == len(approved_tags) == 4,
        "approved_terminal_tag_names_match": approval.get("approved_terminal_tag_names") == APPROVED_TERMINAL_TAG_NAMES and [row.get("tag_name") for row in approved_tags] == APPROVED_TERMINAL_TAG_NAMES,
        "approved_terminal_tags_not_created": all(row.get("tag_created") is False and row.get("tag_status") == "APPROVED_NOT_CREATED" for row in approved_tags),
        "approved_terminal_tags_not_pushed": all(row.get("tag_pushed") is False for row in approved_tags),
        "supporting_packages_available_not_selected": supporting == _supporting_packages(),
        "governance_tags_not_approved": governance == _unapproved_tags(source_review_service.source_candidate_service.GOVERNANCE_TAG_NAMES),
        "protection_tags_not_approved": protection == _unapproved_tags(source_review_service.source_candidate_service.SOURCE_PROTECTION_TAG_NAMES),
        "future_tag_message_template_approved": approval.get("future_tag_message_template") == source_review_service.source_candidate_service.FUTURE_TAG_MESSAGE_TEMPLATE and approval.get("future_tag_message_template_status") == "APPROVED_FOR_FUTURE_TAGGING_EXECUTION_ONLY",
        "git_tag_created_false": approval.get("git_tag_created") is False and approval.get("repository_tags_created") is False,
        "git_tag_push_performed_false": approval.get("git_tag_push_performed") is False and approval.get("repository_tags_pushed") is False,
        "merge_performed_false": approval.get("git_merge_performed") is False,
        "rebase_performed_false": approval.get("git_rebase_performed") is False,
        "branch_delete_performed_false": approval.get("git_branch_delete_performed") is False,
        "remote_delete_performed_false": approval.get("git_remote_delete_performed") is False,
        "main_push_false": approval.get("git_main_push_performed") is False,
        "force_push_false": approval.get("git_force_push_performed") is False,
        "remote_prune_false": approval.get("git_remote_prune_performed") is False,
        "origin_main_modified_false": approval.get("origin_main_modified_by_this_task") is False,
        "marketflow_outputs_not_tracked": approval.get("tracked_marketflow_file_count") == 0,
        "provider_requests_false": approval.get("provider_requests_made_in_approval") is False,
        "market_data_acquisition_false": approval.get("market_data_acquisition_performed_in_approval") is False,
        "dataset_generation_false": approval.get("dataset_generation_performed_in_approval") is False,
        "metric_recomputation_false": approval.get("metric_recomputation_from_raw_rows_performed") is False,
        "model_training_false": approval.get("model_training_performed") is False,
        "strategy_scoring_false": approval.get("strategy_scoring_performed") is False,
        "recommendations_false": approval.get("trade_recommendations_generated") is False,
        "predictive_usefulness_not_accepted": approval.get("predictive_usefulness") == NOT_ACCEPTED and approval.get("predictive_usefulness_accepted") is False,
        "profitability_not_accepted": approval.get("profitability") == NOT_ACCEPTED and approval.get("profitability_accepted") is False,
        "runtime_not_authorized": approval.get("runtime_use") == NOT_AUTHORIZED,
        "broker_not_authorized": approval.get("broker_execution") == NOT_AUTHORIZED,
        "next_chain_defined": approval.get("next_chain") == NEXT_CHAIN,
        "next_gates_defined": approval.get("next_gates") == NEXT_GATES,
        "risk_controls_defined": approval.get("risk_controls") == RISK_CONTROLS,
        "no_tracked_marketflow_files": approval.get("no_tracked_marketflow_files") is True,
    }


def _check(check_id: str, actual: bool) -> dict[str, Any]:
    return {
        "check_id": check_id,
        "status": PASS if actual else FAIL,
        "expected": True,
        "actual": bool(actual),
        "severity": "INFO" if actual else BLOCKER,
        "message": "approval condition satisfied" if actual else "approval condition failed",
    }


def _checklist(approval: Mapping[str, Any]) -> list[dict[str, Any]]:
    values = _check_values(approval)
    return [_check(check_id, values[check_id]) for check_id in REQUIRED_CHECK_IDS]


def _summary(checklist: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
    rows = list(checklist)
    passed = sum(row.get("status") == PASS for row in rows)
    failed = len(rows) - passed
    return {
        "total_checks": len(rows),
        "passed_checks": passed,
        "failed_checks": failed,
        "blocker_count": failed,
        "repository_tagging_release_strategy_selected": True,
        "repository_tagging_release_strategy_approved": True,
        "repository_tagging_release_strategy_authorized": True,
        "repository_tagging_release_strategy_approval_created": True,
        "selected_tagging_package": SELECTED_TAGGING_PACKAGE,
        "ready_for_repository_tagging_execution": True,
        "approved_terminal_tag_count": 4,
        "tags_created": False,
        "tags_pushed": False,
        "merge_performed": False,
        "delete_performed": False,
        "main_pushed": False,
        "origin_main_modified": False,
        "recommended_next_task": "MARKETFLOW_REPOSITORY_TAGGING_EXECUTION_V1",
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_authorized": False,
        "broker_execution_authorized": False,
    }


def marketflow_repository_tagging_release_strategy_approval_digest_v1(
    approval: Mapping[str, Any],
) -> str:
    """Return the deterministic semantic digest for the attested approval."""
    payload = deepcopy(dict(approval))
    payload.pop("marketflow_repository_tagging_release_strategy_approval_digest", None)
    return semantic_digest(payload)


def build_marketflow_repository_tagging_release_strategy_approval_v1(
    *, source_review: dict | None = None, operator_attestation: dict,
) -> dict:
    """Approve future tag execution without creating or pushing tags."""
    _validate_operator_attestation(operator_attestation)
    approval = _base_approval(source_review, operator_attestation)
    approval["checklist"] = _checklist(approval)
    approval["summary"] = _summary(approval["checklist"])
    if approval["summary"]["blocker_count"]:
        raise MarketFlowRepositoryTaggingReleaseStrategyApprovalError(
            "tagging strategy approval contains blockers"
        )
    approval["marketflow_repository_tagging_release_strategy_approval_digest"] = (
        marketflow_repository_tagging_release_strategy_approval_digest_v1(approval)
    )
    validate_marketflow_repository_tagging_release_strategy_approval_v1(approval)
    return approval


def validate_marketflow_repository_tagging_release_strategy_approval_v1(
    approval: dict,
) -> dict:
    """Validate attestation, evidence, bounded approval, and closed execution gates."""
    if not isinstance(approval, dict):
        raise MarketFlowRepositoryTaggingReleaseStrategyApprovalError(
            "approval must be an object"
        )
    attestation = approval.get("operator_attestation")
    _validate_operator_attestation(attestation)
    expected = _base_approval(None, attestation)
    for field, value in expected.items():
        if approval.get(field) != value:
            raise MarketFlowRepositoryTaggingReleaseStrategyApprovalError(
                f"{field} mismatch"
            )
    checklist = approval.get("checklist")
    if not isinstance(checklist, list) or checklist != _checklist(approval):
        raise MarketFlowRepositoryTaggingReleaseStrategyApprovalError(
            "tagging strategy approval checklist mismatch"
        )
    if any(row.get("status") != PASS for row in checklist):
        raise MarketFlowRepositoryTaggingReleaseStrategyApprovalError(
            "tagging strategy approval checklist failed"
        )
    if approval.get("summary") != _summary(checklist):
        raise MarketFlowRepositoryTaggingReleaseStrategyApprovalError(
            "tagging strategy approval summary mismatch"
        )
    digest = approval.get("marketflow_repository_tagging_release_strategy_approval_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise MarketFlowRepositoryTaggingReleaseStrategyApprovalError(
            "tagging strategy approval digest missing"
        )
    if digest != marketflow_repository_tagging_release_strategy_approval_digest_v1(
        approval
    ):
        raise MarketFlowRepositoryTaggingReleaseStrategyApprovalError(
            "tagging strategy approval digest mismatch"
        )
    return {
        "status": MARKETFLOW_REPOSITORY_TAGGING_RELEASE_STRATEGY_APPROVAL_VALID,
        "artifact_kind": approval["artifact_kind"],
        "approval_status": approval["approval_status"],
        "marketflow_repository_tagging_release_strategy_approval_digest": digest,
        **{
            key: approval["summary"][key]
            for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")
        },
    }


def build_marketflow_repository_tagging_release_strategy_approval_markdown_v1(
    approval: dict,
) -> str:
    """Render a sanitized Markdown view of the validated approval."""
    validation = validate_marketflow_repository_tagging_release_strategy_approval_v1(
        approval
    )
    attestation = approval["operator_attestation"]
    sections = [
        ("Title", ["MarketFlow Repository Tagging / Release Strategy Approval v1"]),
        ("MarketFlow Repository Tagging / Release Strategy Approval v1", [f"Artifact/status: `{approval['artifact_kind']}` / `{approval['approval_status']}`.", f"Digest: `{validation['marketflow_repository_tagging_release_strategy_approval_digest']}`."]),
        ("Operator Attestation", [f"Decision: `{attestation['operator_decision']}`.", f"Reference: `{attestation['operator_reference']}`.", f"Timestamp: `{attestation['operator_attestation_timestamp_utc']}`."]),
        ("Source Operator Review", [f"Source digest: `{approval['source_tagging_operator_review_digest']}`.", f"Source commit: `{approval['source_operator_review_commit']}`."]),
        ("Bound Evidence", [f"Complete upstream evidence fields: {len(approval['source_evidence'])}."]),
        ("Repository Context", [f"Origin main: `{approval['origin_main_commit']}`.", "Frozen through source-review ref totals: 551 / 552 / 554 / 556 / 558.", "Existing/candidate-namespace tag counts: 28 / 0."]),
        ("Approval Scope", [approval["approval_scope"]]),
        ("Selected Tagging Package", [f"`{approval['selected_tagging_package']}` is approved for future tagging execution only."]),
        ("Approved Terminal Tags", [f"`{row['tag_name']}` -> `{row['tag_target_commit']}` ({row['tag_status']})" for row in approval["approved_terminal_tags"]]),
        ("Supporting Packages", [f"{row['package_id']}: {row['approval_status']}" for row in approval["supporting_tagging_packages"]]),
        ("Unapproved Tags", [f"Governance: {len(approval['unapproved_governance_tags'])}; source protection: {len(approval['unapproved_source_protection_tags'])}."]),
        ("Future Tag Message Template", [approval["future_tag_message_template"]]),
        ("Next Chain", list(approval["next_chain"])),
        ("Next Gates", list(approval["next_gates"])),
        ("Risk Controls", list(approval["risk_controls"])),
        ("Authority Boundaries", ["Only future terminal tag execution is authorized. No tags are created or pushed; predictive usefulness and profitability are not accepted; runtime, strategy, paper trading, and broker execution remain NOT_AUTHORIZED."]),
        ("Checklist Summary", [f"{approval['summary']['passed_checks']} / {approval['summary']['total_checks']} checks pass; {approval['summary']['blocker_count']} blockers."]),
        ("Guardrails", ["No tag, tag push, merge, rebase, deletion, main push, force-push, prune, provider, data, metric, model, recommendation, runtime, broker, or trading action occurred."]),
    ]
    lines = ["# MarketFlow Repository Tagging / Release Strategy Approval v1", ""]
    for title, rows in sections:
        lines.extend([f"## {title}", *[f"- {row}" for row in rows], ""])
    return "\n".join(lines)


def write_marketflow_repository_tagging_release_strategy_approval_v1(
    output_dir: str | Path,
    *,
    source_review: dict | None = None,
    operator_attestation: dict,
) -> dict:
    """Write canonical approval JSON without overwriting an existing approval."""
    approval = build_marketflow_repository_tagging_release_strategy_approval_v1(
        source_review=source_review,
        operator_attestation=operator_attestation,
    )
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "marketflow_repository_tagging_release_strategy_approval_v1.json"
    if path.exists():
        raise MarketFlowRepositoryTaggingReleaseStrategyApprovalError(
            "tagging strategy approval output already exists"
        )
    payload = canonical_json_bytes(approval)
    path.write_bytes(payload)
    return {
        "path": str(path),
        "artifact_kind": approval["artifact_kind"],
        "approval_status": approval["approval_status"],
        "marketflow_repository_tagging_release_strategy_approval_digest": approval[
            "marketflow_repository_tagging_release_strategy_approval_digest"
        ],
        "payload_sha256": sha256_bytes(payload),
    }
