"""Offline, attestation-gated approval for future explicit tag publication."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Iterable, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import marketflow_repository_tag_push_strategy_operator_review_service as source_service


ARTIFACT_KIND_MARKETFLOW_REPOSITORY_TAG_PUSH_STRATEGY_APPROVED = (
    "MARKETFLOW_REPOSITORY_TAG_PUSH_STRATEGY_APPROVED"
)
SCHEMA_VERSION_MARKETFLOW_REPOSITORY_TAG_PUSH_STRATEGY_APPROVAL_V1 = (
    "marketflow_repository_tag_push_strategy_approval_v1"
)
MARKETFLOW_REPOSITORY_TAG_PUSH_STRATEGY_APPROVED = (
    "MARKETFLOW_REPOSITORY_TAG_PUSH_STRATEGY_APPROVED"
)
REPOSITORY_TAG_PUSH_STRATEGY_APPROVAL_ONLY_NOT_PUSH_NOT_MERGE_NOT_DELETE_NOT_MAIN = (
    "REPOSITORY_TAG_PUSH_STRATEGY_APPROVAL_ONLY_NOT_PUSH_NOT_MERGE_NOT_DELETE_NOT_MAIN"
)
MARKETFLOW_REPOSITORY_TAG_PUSH_STRATEGY_APPROVAL_VALID = (
    "MARKETFLOW_REPOSITORY_TAG_PUSH_STRATEGY_APPROVAL_VALID"
)
PACKAGE_PUSH_TERMINAL_EXPECTANCY_LAB_ARCHIVE_TAGS_TO_ORIGIN = (
    source_service.source_service.PACKAGE_PUSH_TERMINAL_EXPECTANCY_LAB_ARCHIVE_TAGS_TO_ORIGIN
)

REQUIRED_OPERATOR_ATTESTATION_PHRASE = (
    "APPROVE REPOSITORY TAG PUSH STRATEGY "
    "PACKAGE_PUSH_TERMINAL_EXPECTANCY_LAB_ARCHIVE_TAGS_TO_ORIGIN "
    "MARKETFLOW EXPECTANCY LAB TAGS FINAL ARCHIVE NOT READY ARCHIVE RECORD NOT READY "
    "OPERATOR SELECTION OPTION A READINESS NOT READY "
    "REPOSITORY_TAG_PUSH_STRATEGY_APPROVAL_ONLY_NOT_PUSH_NOT_MERGE_NOT_DELETE_NOT_MAIN"
)
OPERATOR_DECISION = "APPROVE_REPOSITORY_TAG_PUSH_STRATEGY"
OPERATOR_ATTESTATION_VERSION = "marketflow_repository_tag_push_strategy_approval_attestation_v1"

EXPECTED_SOURCE_OPERATOR_REVIEW_DIGEST = (
    "2e97941cf486272f9cb12889f929ff51a69fe515ee73b90f6f4d76cba7039788"
)
EXPECTED_SOURCE_CANDIDATE_DIGEST = source_service.EXPECTED_SOURCE_CANDIDATE_DIGEST
EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST = source_service.EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST
EXPECTED_SOURCE_TAG_MANIFEST_REVIEW_DIGEST = source_service.EXPECTED_SOURCE_TAG_MANIFEST_REVIEW_DIGEST
EXPECTED_SOURCE_EXECUTION_DIGEST = source_service.EXPECTED_SOURCE_EXECUTION_DIGEST
EXPECTED_SOURCE_TAG_MANIFEST_DIGEST = source_service.EXPECTED_SOURCE_TAG_MANIFEST_DIGEST
EXPECTED_SOURCE_APPROVAL_DIGEST = source_service.EXPECTED_SOURCE_APPROVAL_DIGEST
EXPECTED_SOURCE_OPERATOR_REVIEW_RELEASE_DIGEST = source_service.EXPECTED_SOURCE_OPERATOR_REVIEW_DIGEST
EXPECTED_SOURCE_TAGGING_CANDIDATE_DIGEST = source_service.EXPECTED_SOURCE_TAGGING_CANDIDATE_DIGEST
EXPECTED_SOURCE_INVENTORY_PLAN_DIGEST = source_service.EXPECTED_SOURCE_INVENTORY_PLAN_DIGEST
EXPECTED_SOURCE_FINAL_ARCHIVE_DIGEST = source_service.EXPECTED_SOURCE_FINAL_ARCHIVE_DIGEST
EXPECTED_SOURCE_ARCHIVE_DIGEST = source_service.EXPECTED_SOURCE_ARCHIVE_DIGEST
EXPECTED_SOURCE_OPERATOR_SELECTION_DIGEST = source_service.EXPECTED_SOURCE_OPERATOR_SELECTION_DIGEST
EXPECTED_SOURCE_CLOSURE_DIGEST = source_service.EXPECTED_SOURCE_CLOSURE_DIGEST
EXPECTED_SOURCE_READINESS_DIGEST = source_service.EXPECTED_SOURCE_READINESS_DIGEST
EXPECTED_SOURCE_REASSESSMENT_DIGEST = source_service.EXPECTED_SOURCE_REASSESSMENT_DIGEST
EXPECTED_SOURCE_BACKTEST_ROWS_DIGEST = source_service.EXPECTED_SOURCE_BACKTEST_ROWS_DIGEST
EXPECTED_SOURCE_METRIC_REPORT_DIGEST = source_service.EXPECTED_SOURCE_METRIC_REPORT_DIGEST
EXPECTED_SOURCE_RECORDS_DIGEST = source_service.EXPECTED_SOURCE_RECORDS_DIGEST
EXPECTED_ORIGIN_MAIN_COMMIT = source_service.EXPECTED_ORIGIN_MAIN_COMMIT
EXPECTED_SOURCE_OPERATOR_REVIEW_COMMIT = "1f543e7067744d351a67bbab034abb643fa4c508"
SOURCE_EVIDENCE = deepcopy(source_service.SOURCE_EVIDENCE)

APPROVED_REMOTE_REFS = list(source_service.source_service.CANDIDATE_REMOTE_REFS)
APPROVED_TAG_OBJECT_SHAS = list(
    source_service.source_service.source_review_service.EXPECTED_TAG_OBJECT_SHAS
)
APPROVED_TARGET_COMMITS = [
    row["target_commit"]
    for row in source_service.source_service.source_review_service.EXPECTED_TAGS
]
APPROVED_TAG_PUSH_COUNT = 4
APPROVED_PUSH_COMMAND_TEMPLATE = source_service.source_service.CANDIDATE_PUSH_COMMAND_TEMPLATE

NOT_ACCEPTED = "not accepted"
NOT_AUTHORIZED = "NOT_AUTHORIZED"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

APPROVED_SELECTED_PACKAGE = {
    "package_id": PACKAGE_PUSH_TERMINAL_EXPECTANCY_LAB_ARCHIVE_TAGS_TO_ORIGIN,
    "approval_status": "APPROVED_FOR_FUTURE_TAG_PUSH_EXECUTION_ONLY",
    "selected": True,
    "approved": True,
    "authorized_for_future_execution": True,
    "executed": False,
    "tags_pushed": False,
    "main_push_required": False,
    "runtime_authority_created": False,
    "predictive_usefulness_accepted": False,
    "profitability_accepted": False,
}

SUPPORTING_PACKAGES = [
    {
        "package_id": package_id,
        "approval_status": "AVAILABLE_NOT_SELECTED",
        "selected": False,
        "approved": False,
        "authorized_for_future_execution": False,
        "executed": False,
        "tags_pushed": False,
    }
    for package_id in (
        source_service.source_service.PACKAGE_KEEP_TAGS_LOCAL_ONLY,
        source_service.source_service.PACKAGE_DELAY_REMOTE_TAG_PUBLICATION_UNTIL_MERGE_STRATEGY,
        source_service.source_service.PACKAGE_CREATE_BACKUP_OR_BUNDLE_BEFORE_REMOTE_TAG_PUBLICATION,
    )
]

APPROVED_TAG_PUSH_RECORDS = [
    {
        **deepcopy(record),
        "candidate_push_status": "APPROVED_NOT_PUSHED",
        "approval_status": "APPROVED_FOR_FUTURE_TAG_PUSH_EXECUTION_ONLY",
        "push_status": "APPROVED_NOT_PUSHED",
        "selected_for_push": True,
        "approved_for_push": True,
        "pushed": False,
        "separate_execution_required": True,
        "explicit_refspec_required": True,
    }
    for record in source_service.REVIEWED_PUSH_RECORDS
]

NEXT_CHAIN = [
    "Repository Tag Push Execution v1, if separately invoked.",
    "Repository Tag Push Results Review v1.",
    "Repository Merge Strategy Candidate v1, only after tag-push results review or explicit local-only decision.",
    "Repository Branch Cleanup Candidate v1, only after merge/tag strategy is settled.",
    "Cleanup execution only after separate approval, backup/bundle, and protected-branch confirmation.",
    "Main push only if separately approved and protected.",
]

NEXT_GATES = [
    "repository_tag_push_execution_if_approved",
    "repository_tag_push_results_review",
    "repository_merge_strategy_candidate_after_tag_push_decision",
    "repository_branch_cleanup_candidate_after_merge_tag_strategy",
    "repository_cleanup_approval_if_selected",
    "repository_cleanup_execution_if_approved",
    "main_push_only_if_separately_approved_and_protected",
]

RISK_CONTROLS = [
    "approval_does_not_push_tags",
    "approval_does_not_create_tags",
    "approval_does_not_modify_tags",
    "approval_does_not_delete_tags",
    "approval_does_not_push_all_tags",
    "approval_does_not_push_branches",
    "approval_does_not_push_main",
    "approval_does_not_force_push",
    "approval_does_not_merge",
    "approval_does_not_rebase",
    "approval_does_not_delete_branches",
    "approval_does_not_delete_remote_branches",
    "approval_does_not_prune_remotes",
    "approval_does_not_modify_origin_main",
    "approval_does_not_modify_marketflow_outputs",
    "approval_does_not_call_providers",
    "approval_does_not_acquire_market_data",
    "approval_does_not_regenerate_dataset",
    "approval_does_not_rerun_tag_push_candidate",
    "approval_does_not_rerun_tag_push_operator_review",
    "approval_does_not_rerun_tagging_results_review",
    "approval_does_not_rerun_tagging_execution",
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
    "selected_pushes_are_approved_for_future_execution_only",
    "separate_execution_required_before_tag_push",
    "explicit_refspec_required_for_future_push",
    "push_all_tags_forbidden",
    "protect_origin_main",
    "preserve_terminal_archive_evidence",
    "preserve_meta_limitation",
]

REQUIRED_CHECK_IDS = [
    "source_operator_review_digest_bound",
    "source_candidate_digest_bound",
    "source_results_review_digest_bound",
    "source_tag_manifest_review_digest_bound",
    "source_execution_digest_bound",
    "source_approval_digest_bound",
    "source_inventory_plan_digest_bound",
    "source_final_archive_digest_bound",
    "source_archive_digest_bound",
    "source_operator_selection_digest_bound",
    "source_closure_digest_bound",
    "source_readiness_digest_bound",
    "source_reassessment_digest_bound",
    "source_backtest_rows_digest_bound",
    "source_metric_report_digest_bound",
    "records_digest_bound",
    "origin_main_commit_bound",
    "operator_decision_matches",
    "operator_attestation_phrase_matches",
    "approval_scope_only",
    "selected_package_push_terminal_tags_to_origin",
    "approval_created_true",
    "strategy_selected_true",
    "strategy_approved_true",
    "strategy_authorized_true",
    "ready_for_tag_push_execution_true",
    "strategy_executed_false",
    "approved_tag_push_count_4",
    "approved_remote_refs_match",
    "approved_tag_object_shas_match",
    "approved_target_commits_match",
    "approved_push_command_template_present",
    "approved_push_command_not_executed",
    "tags_pushed_false",
    "git_tag_push_performed_false",
    "additional_tags_created_false",
    "tags_modified_false",
    "tags_deleted_false",
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

ATTESTATION_STRING_FIELDS = {
    "operator_decision": OPERATOR_DECISION,
    "selected_tag_push_package": PACKAGE_PUSH_TERMINAL_EXPECTANCY_LAB_ARCHIVE_TAGS_TO_ORIGIN,
    "operator_attestation_phrase": REQUIRED_OPERATOR_ATTESTATION_PHRASE,
    "operator_attestation_version": OPERATOR_ATTESTATION_VERSION,
    "operator_confirms_source_operator_review_digest": EXPECTED_SOURCE_OPERATOR_REVIEW_DIGEST,
    "operator_confirms_source_candidate_digest": EXPECTED_SOURCE_CANDIDATE_DIGEST,
    "operator_confirms_source_results_review_digest": EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST,
    "operator_confirms_source_tag_manifest_review_digest": EXPECTED_SOURCE_TAG_MANIFEST_REVIEW_DIGEST,
    "operator_confirms_source_execution_digest": EXPECTED_SOURCE_EXECUTION_DIGEST,
    "operator_confirms_source_approval_digest": EXPECTED_SOURCE_APPROVAL_DIGEST,
    "operator_confirms_origin_main_commit": EXPECTED_ORIGIN_MAIN_COMMIT,
    "operator_confirms_selected_tag_push_package": PACKAGE_PUSH_TERMINAL_EXPECTANCY_LAB_ARCHIVE_TAGS_TO_ORIGIN,
}

ATTESTATION_TRUE_FIELDS = [
    "operator_confirms_approval_scope_only",
    "operator_confirms_tags_not_pushed",
    "operator_confirms_no_additional_tags_created",
    "operator_confirms_no_tags_modified",
    "operator_confirms_no_tags_deleted",
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


class MarketFlowRepositoryTagPushStrategyApprovalError(ValueError):
    """Raised when approval evidence or attestation fails closed."""


def _validate_attestation(attestation: Mapping[str, Any]) -> None:
    if not isinstance(attestation, dict):
        raise MarketFlowRepositoryTagPushStrategyApprovalError(
            "operator_attestation must be an object"
        )
    for field, expected in ATTESTATION_STRING_FIELDS.items():
        if attestation.get(field) != expected:
            raise MarketFlowRepositoryTagPushStrategyApprovalError(
                f"operator attestation {field} mismatch"
            )
    for field in ("operator_reference", "operator_attestation_timestamp_utc"):
        if not isinstance(attestation.get(field), str) or not attestation[field].strip():
            raise MarketFlowRepositoryTagPushStrategyApprovalError(
                f"operator attestation {field} missing"
            )
    list_expectations = {
        "operator_confirms_approved_remote_refs": APPROVED_REMOTE_REFS,
        "operator_confirms_approved_tag_object_shas": APPROVED_TAG_OBJECT_SHAS,
        "operator_confirms_approved_target_commits": APPROVED_TARGET_COMMITS,
    }
    for field, expected in list_expectations.items():
        if attestation.get(field) != expected:
            raise MarketFlowRepositoryTagPushStrategyApprovalError(
                f"operator attestation {field} mismatch"
            )
    if attestation.get("operator_confirms_approved_tag_push_count") != APPROVED_TAG_PUSH_COUNT:
        raise MarketFlowRepositoryTagPushStrategyApprovalError(
            "operator attestation approved tag-push count mismatch"
        )
    for field in ATTESTATION_TRUE_FIELDS:
        if attestation.get(field) is not True:
            raise MarketFlowRepositoryTagPushStrategyApprovalError(
                f"operator attestation {field} must be true"
            )


def build_marketflow_repository_tag_push_strategy_approval_attestation_v1(
    *,
    operator_reference: str,
    operator_attestation_timestamp_utc: str,
    operator_attestation_phrase: str,
    operator_confirms_source_operator_review_digest: str,
    operator_confirms_source_candidate_digest: str,
    operator_confirms_source_results_review_digest: str,
    operator_confirms_source_tag_manifest_review_digest: str,
    operator_confirms_source_execution_digest: str,
    operator_confirms_source_approval_digest: str,
    operator_confirms_origin_main_commit: str,
    operator_confirms_selected_tag_push_package: str,
    operator_confirms_approved_remote_refs: list[str],
    operator_confirms_approved_tag_object_shas: list[str],
    operator_confirms_approved_target_commits: list[str],
    operator_confirms_approved_tag_push_count: int,
    operator_confirms_approval_scope_only: bool,
    operator_confirms_tags_not_pushed: bool,
    operator_confirms_no_additional_tags_created: bool,
    operator_confirms_no_tags_modified: bool,
    operator_confirms_no_tags_deleted: bool,
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
    selected_tag_push_package: str = PACKAGE_PUSH_TERMINAL_EXPECTANCY_LAB_ARCHIVE_TAGS_TO_ORIGIN,
    operator_decision: str = OPERATOR_DECISION,
) -> dict:
    """Build and validate the complete non-secret operator attestation."""
    supplied_values = locals().copy()
    attestation = {
        "operator_decision": operator_decision,
        "selected_tag_push_package": selected_tag_push_package,
        "operator_attestation_phrase": operator_attestation_phrase,
        "operator_attestation_timestamp_utc": operator_attestation_timestamp_utc,
        "operator_attestation_version": OPERATOR_ATTESTATION_VERSION,
        "operator_reference": operator_reference,
        "operator_confirms_source_operator_review_digest": operator_confirms_source_operator_review_digest,
        "operator_confirms_source_candidate_digest": operator_confirms_source_candidate_digest,
        "operator_confirms_source_results_review_digest": operator_confirms_source_results_review_digest,
        "operator_confirms_source_tag_manifest_review_digest": operator_confirms_source_tag_manifest_review_digest,
        "operator_confirms_source_execution_digest": operator_confirms_source_execution_digest,
        "operator_confirms_source_approval_digest": operator_confirms_source_approval_digest,
        "operator_confirms_origin_main_commit": operator_confirms_origin_main_commit,
        "operator_confirms_selected_tag_push_package": operator_confirms_selected_tag_push_package,
        "operator_confirms_approved_remote_refs": list(operator_confirms_approved_remote_refs),
        "operator_confirms_approved_tag_object_shas": list(operator_confirms_approved_tag_object_shas),
        "operator_confirms_approved_target_commits": list(operator_confirms_approved_target_commits),
        "operator_confirms_approved_tag_push_count": operator_confirms_approved_tag_push_count,
        **{
            field: supplied_values[field]
            for field in ATTESTATION_TRUE_FIELDS
        },
    }
    _validate_attestation(attestation)
    return attestation


def _source_evidence(source_review: Mapping[str, Any] | None) -> dict[str, Any]:
    if source_review is None:
        return deepcopy(SOURCE_EVIDENCE)
    if not isinstance(source_review, dict):
        raise MarketFlowRepositoryTagPushStrategyApprovalError(
            "source_review must be an object"
        )
    try:
        source_service.validate_marketflow_repository_tag_push_strategy_operator_review_v1(
            source_review
        )
    except (TypeError, ValueError, KeyError) as exc:
        raise MarketFlowRepositoryTagPushStrategyApprovalError(
            "source tag-push operator review is invalid"
        ) from exc
    if source_review.get(
        "marketflow_repository_tag_push_strategy_operator_review_digest"
    ) != EXPECTED_SOURCE_OPERATOR_REVIEW_DIGEST:
        raise MarketFlowRepositoryTagPushStrategyApprovalError(
            "source tag-push operator review digest mismatch"
        )
    return deepcopy(source_review["source_evidence"])


def _base_approval(
    source_review: Mapping[str, Any] | None,
    operator_attestation: Mapping[str, Any],
) -> dict[str, Any]:
    _validate_attestation(operator_attestation)
    return {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_REPOSITORY_TAG_PUSH_STRATEGY_APPROVED,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_REPOSITORY_TAG_PUSH_STRATEGY_APPROVAL_V1,
        "approval_status": MARKETFLOW_REPOSITORY_TAG_PUSH_STRATEGY_APPROVED,
        "approval_scope": REPOSITORY_TAG_PUSH_STRATEGY_APPROVAL_ONLY_NOT_PUSH_NOT_MERGE_NOT_DELETE_NOT_MAIN,
        "selected_tag_push_package": PACKAGE_PUSH_TERMINAL_EXPECTANCY_LAB_ARCHIVE_TAGS_TO_ORIGIN,
        "created_offline": True,
        "planning_only": True,
        "governance_only": True,
        "operator_attestation_required": True,
        "operator_attestation": deepcopy(dict(operator_attestation)),
        "source_tag_push_operator_review_artifact_kind": source_service.ARTIFACT_KIND_MARKETFLOW_REPOSITORY_TAG_PUSH_STRATEGY_OPERATOR_REVIEW_V1,
        "source_tag_push_operator_review_status": source_service.MARKETFLOW_REPOSITORY_TAG_PUSH_STRATEGY_OPERATOR_REVIEW_READY,
        "source_tag_push_operator_review_scope": source_service.REPOSITORY_TAG_PUSH_STRATEGY_OPERATOR_REVIEW_ONLY_NOT_APPROVAL_NOT_PUSH_NOT_MERGE_NOT_DELETE_NOT_MAIN,
        "source_tag_push_operator_review_digest": EXPECTED_SOURCE_OPERATOR_REVIEW_DIGEST,
        "source_tag_push_candidate_digest": EXPECTED_SOURCE_CANDIDATE_DIGEST,
        "source_tagging_results_review_digest": EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST,
        "source_tag_manifest_review_digest": EXPECTED_SOURCE_TAG_MANIFEST_REVIEW_DIGEST,
        "source_tagging_execution_digest": EXPECTED_SOURCE_EXECUTION_DIGEST,
        "source_tagging_execution_tag_manifest_digest": EXPECTED_SOURCE_TAG_MANIFEST_DIGEST,
        "source_tagging_approval_digest": EXPECTED_SOURCE_APPROVAL_DIGEST,
        "source_operator_review_digest": EXPECTED_SOURCE_OPERATOR_REVIEW_RELEASE_DIGEST,
        "source_candidate_digest": EXPECTED_SOURCE_TAGGING_CANDIDATE_DIGEST,
        "source_inventory_plan_digest": EXPECTED_SOURCE_INVENTORY_PLAN_DIGEST,
        "source_final_archive_digest": EXPECTED_SOURCE_FINAL_ARCHIVE_DIGEST,
        "source_archive_digest": EXPECTED_SOURCE_ARCHIVE_DIGEST,
        "source_operator_selection_digest": EXPECTED_SOURCE_OPERATOR_SELECTION_DIGEST,
        "source_closure_digest": EXPECTED_SOURCE_CLOSURE_DIGEST,
        "source_readiness_digest": EXPECTED_SOURCE_READINESS_DIGEST,
        "source_reassessment_digest": EXPECTED_SOURCE_REASSESSMENT_DIGEST,
        "source_backtest_rows_digest": EXPECTED_SOURCE_BACKTEST_ROWS_DIGEST,
        "source_metric_report_digest": EXPECTED_SOURCE_METRIC_REPORT_DIGEST,
        "source_records_digest": EXPECTED_SOURCE_RECORDS_DIGEST,
        "source_evidence": _source_evidence(source_review),
        "origin_main_commit": EXPECTED_ORIGIN_MAIN_COMMIT,
        "source_operator_review_commit": EXPECTED_SOURCE_OPERATOR_REVIEW_COMMIT,
        "source_repository_context": {
            "bound_source_context": {"local_branch_count": 296, "remote_branch_count": 268, "total_ref_count": 564},
            "pre_review_live_context": {"local_branch_count": 297, "remote_branch_count": 269, "total_ref_count": 566},
            "final_live_context_after_review_push": {"local_branch_count": 298, "remote_branch_count": 270, "total_ref_count": 568},
            "local_tag_count": 32,
            "candidate_namespace_tag_count": 4,
            "remote_approved_tag_count": 0,
        },
        "repository_tag_push_strategy_candidate_created": True,
        "repository_tag_push_strategy_operator_review_created": True,
        "repository_tag_push_strategy_operator_review_ready": True,
        "repository_tag_push_strategy_selected": True,
        "repository_tag_push_strategy_approved": True,
        "repository_tag_push_strategy_authorized": True,
        "repository_tag_push_strategy_approval_created": True,
        "ready_for_repository_tag_push_execution": True,
        "repository_tag_push_strategy_executed": False,
        "repository_tags_pushed": False,
        "git_tag_push_performed": False,
        "additional_tags_created": False,
        "tags_modified": False,
        "tags_deleted": False,
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
        "predictive_usefulness": NOT_ACCEPTED,
        "predictive_usefulness_accepted": False,
        "profitability": NOT_ACCEPTED,
        "profitability_accepted": False,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "approved_selected_package": deepcopy(APPROVED_SELECTED_PACKAGE),
        "supporting_packages": deepcopy(SUPPORTING_PACKAGES),
        "approved_tag_push_records": deepcopy(APPROVED_TAG_PUSH_RECORDS),
        "approved_tag_push_count": APPROVED_TAG_PUSH_COUNT,
        "approved_remote_refs": list(APPROVED_REMOTE_REFS),
        "approved_tag_object_shas": list(APPROVED_TAG_OBJECT_SHAS),
        "approved_target_commits": list(APPROVED_TARGET_COMMITS),
        "approved_future_push_command_template": APPROVED_PUSH_COMMAND_TEMPLATE,
        "command_approval_status": "APPROVED_FOR_FUTURE_EXECUTION_ONLY",
        "command_executed": False,
        "remote_publication_status": "APPROVED_NOT_PUSHED",
        "next_chain": list(NEXT_CHAIN),
        "next_gates": list(NEXT_GATES),
        "risk_controls": list(RISK_CONTROLS),
        "tracked_marketflow_file_count": 0,
        "no_tracked_marketflow_files": True,
        "recommended_next_task": "MARKETFLOW_REPOSITORY_TAG_PUSH_EXECUTION_V1",
    }


def _check_values(approval: Mapping[str, Any]) -> dict[str, bool]:
    attestation = approval.get("operator_attestation", {})
    return {
        "source_operator_review_digest_bound": approval.get("source_tag_push_operator_review_digest") == EXPECTED_SOURCE_OPERATOR_REVIEW_DIGEST,
        "source_candidate_digest_bound": approval.get("source_tag_push_candidate_digest") == EXPECTED_SOURCE_CANDIDATE_DIGEST,
        "source_results_review_digest_bound": approval.get("source_tagging_results_review_digest") == EXPECTED_SOURCE_RESULTS_REVIEW_DIGEST,
        "source_tag_manifest_review_digest_bound": approval.get("source_tag_manifest_review_digest") == EXPECTED_SOURCE_TAG_MANIFEST_REVIEW_DIGEST,
        "source_execution_digest_bound": approval.get("source_tagging_execution_digest") == EXPECTED_SOURCE_EXECUTION_DIGEST,
        "source_approval_digest_bound": approval.get("source_tagging_approval_digest") == EXPECTED_SOURCE_APPROVAL_DIGEST,
        "source_inventory_plan_digest_bound": approval.get("source_inventory_plan_digest") == EXPECTED_SOURCE_INVENTORY_PLAN_DIGEST,
        "source_final_archive_digest_bound": approval.get("source_final_archive_digest") == EXPECTED_SOURCE_FINAL_ARCHIVE_DIGEST,
        "source_archive_digest_bound": approval.get("source_archive_digest") == EXPECTED_SOURCE_ARCHIVE_DIGEST,
        "source_operator_selection_digest_bound": approval.get("source_operator_selection_digest") == EXPECTED_SOURCE_OPERATOR_SELECTION_DIGEST,
        "source_closure_digest_bound": approval.get("source_closure_digest") == EXPECTED_SOURCE_CLOSURE_DIGEST,
        "source_readiness_digest_bound": approval.get("source_readiness_digest") == EXPECTED_SOURCE_READINESS_DIGEST,
        "source_reassessment_digest_bound": approval.get("source_reassessment_digest") == EXPECTED_SOURCE_REASSESSMENT_DIGEST,
        "source_backtest_rows_digest_bound": approval.get("source_backtest_rows_digest") == EXPECTED_SOURCE_BACKTEST_ROWS_DIGEST,
        "source_metric_report_digest_bound": approval.get("source_metric_report_digest") == EXPECTED_SOURCE_METRIC_REPORT_DIGEST,
        "records_digest_bound": approval.get("source_records_digest") == EXPECTED_SOURCE_RECORDS_DIGEST,
        "origin_main_commit_bound": approval.get("origin_main_commit") == EXPECTED_ORIGIN_MAIN_COMMIT,
        "operator_decision_matches": attestation.get("operator_decision") == OPERATOR_DECISION,
        "operator_attestation_phrase_matches": attestation.get("operator_attestation_phrase") == REQUIRED_OPERATOR_ATTESTATION_PHRASE,
        "approval_scope_only": approval.get("approval_scope") == REPOSITORY_TAG_PUSH_STRATEGY_APPROVAL_ONLY_NOT_PUSH_NOT_MERGE_NOT_DELETE_NOT_MAIN,
        "selected_package_push_terminal_tags_to_origin": approval.get("selected_tag_push_package") == PACKAGE_PUSH_TERMINAL_EXPECTANCY_LAB_ARCHIVE_TAGS_TO_ORIGIN,
        "approval_created_true": approval.get("repository_tag_push_strategy_approval_created") is True,
        "strategy_selected_true": approval.get("repository_tag_push_strategy_selected") is True,
        "strategy_approved_true": approval.get("repository_tag_push_strategy_approved") is True,
        "strategy_authorized_true": approval.get("repository_tag_push_strategy_authorized") is True,
        "ready_for_tag_push_execution_true": approval.get("ready_for_repository_tag_push_execution") is True,
        "strategy_executed_false": approval.get("repository_tag_push_strategy_executed") is False,
        "approved_tag_push_count_4": approval.get("approved_tag_push_count") == APPROVED_TAG_PUSH_COUNT,
        "approved_remote_refs_match": approval.get("approved_remote_refs") == APPROVED_REMOTE_REFS,
        "approved_tag_object_shas_match": approval.get("approved_tag_object_shas") == APPROVED_TAG_OBJECT_SHAS,
        "approved_target_commits_match": approval.get("approved_target_commits") == APPROVED_TARGET_COMMITS,
        "approved_push_command_template_present": approval.get("approved_future_push_command_template") == APPROVED_PUSH_COMMAND_TEMPLATE,
        "approved_push_command_not_executed": approval.get("command_approval_status") == "APPROVED_FOR_FUTURE_EXECUTION_ONLY" and approval.get("command_executed") is False,
        "tags_pushed_false": approval.get("repository_tags_pushed") is False,
        "git_tag_push_performed_false": approval.get("git_tag_push_performed") is False,
        "additional_tags_created_false": approval.get("additional_tags_created") is False,
        "tags_modified_false": approval.get("tags_modified") is False,
        "tags_deleted_false": approval.get("tags_deleted") is False,
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
        "actual": actual,
        "severity": BLOCKER,
        "message": "approval evidence matches" if actual else "approval evidence mismatch",
    }


def _checklist(approval: Mapping[str, Any]) -> list[dict[str, Any]]:
    values = _check_values(approval)
    return [_check(check_id, values[check_id]) for check_id in REQUIRED_CHECK_IDS]


def _summary(checklist: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
    rows = list(checklist)
    failed = [row for row in rows if row.get("status") != PASS]
    return {
        "total_checks": len(rows),
        "passed_checks": len(rows) - len(failed),
        "failed_checks": len(failed),
        "blocker_count": sum(row.get("severity") == BLOCKER for row in failed),
        "repository_tag_push_strategy_selected": True,
        "repository_tag_push_strategy_approved": True,
        "repository_tag_push_strategy_authorized": True,
        "repository_tag_push_strategy_approval_created": True,
        "selected_tag_push_package": PACKAGE_PUSH_TERMINAL_EXPECTANCY_LAB_ARCHIVE_TAGS_TO_ORIGIN,
        "ready_for_repository_tag_push_execution": True,
        "approved_tag_push_count": APPROVED_TAG_PUSH_COUNT,
        "tags_pushed": False,
        "git_tag_push_performed": False,
        "merge_performed": False,
        "delete_performed": False,
        "main_pushed": False,
        "origin_main_modified": False,
        "recommended_next_task": "MARKETFLOW_REPOSITORY_TAG_PUSH_EXECUTION_V1",
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_authorized": False,
        "broker_execution_authorized": False,
    }


def marketflow_repository_tag_push_strategy_approval_digest_v1(
    approval: Mapping[str, Any],
) -> str:
    """Return the deterministic semantic digest for the approval."""
    payload = deepcopy(dict(approval))
    payload.pop("checklist", None)
    payload.pop("summary", None)
    payload.pop("marketflow_repository_tag_push_strategy_approval_digest", None)
    return semantic_digest(payload)


def build_marketflow_repository_tag_push_strategy_approval_v1(
    *,
    source_review: dict | None = None,
    operator_attestation: dict,
) -> dict:
    """Build future-execution approval from exact committed evidence and attestation."""
    approval = _base_approval(source_review, operator_attestation)
    approval["checklist"] = _checklist(approval)
    approval["summary"] = _summary(approval["checklist"])
    approval["marketflow_repository_tag_push_strategy_approval_digest"] = (
        marketflow_repository_tag_push_strategy_approval_digest_v1(approval)
    )
    validate_marketflow_repository_tag_push_strategy_approval_v1(approval)
    return approval


def validate_marketflow_repository_tag_push_strategy_approval_v1(
    approval: dict,
) -> dict:
    """Validate exact attestation, evidence, selection, and closed execution gates."""
    if not isinstance(approval, dict):
        raise MarketFlowRepositoryTagPushStrategyApprovalError(
            "approval must be an object"
        )
    attestation = approval.get("operator_attestation")
    _validate_attestation(attestation)
    expected = _base_approval(None, attestation)
    for field, value in expected.items():
        if approval.get(field) != value:
            raise MarketFlowRepositoryTagPushStrategyApprovalError(
                f"{field} mismatch"
            )
    checklist = approval.get("checklist")
    if not isinstance(checklist, list) or checklist != _checklist(approval):
        raise MarketFlowRepositoryTagPushStrategyApprovalError(
            "approval checklist mismatch"
        )
    if any(row.get("status") != PASS for row in checklist):
        raise MarketFlowRepositoryTagPushStrategyApprovalError(
            "approval checklist failed"
        )
    if approval.get("summary") != _summary(checklist):
        raise MarketFlowRepositoryTagPushStrategyApprovalError(
            "approval summary mismatch"
        )
    digest = approval.get("marketflow_repository_tag_push_strategy_approval_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise MarketFlowRepositoryTagPushStrategyApprovalError(
            "approval digest missing"
        )
    if digest != marketflow_repository_tag_push_strategy_approval_digest_v1(approval):
        raise MarketFlowRepositoryTagPushStrategyApprovalError(
            "approval digest mismatch"
        )
    return {
        "status": MARKETFLOW_REPOSITORY_TAG_PUSH_STRATEGY_APPROVAL_VALID,
        "artifact_kind": approval["artifact_kind"],
        "approval_status": approval["approval_status"],
        "marketflow_repository_tag_push_strategy_approval_digest": digest,
        **{
            key: approval["summary"][key]
            for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")
        },
    }


def build_marketflow_repository_tag_push_strategy_approval_markdown_v1(
    approval: dict,
) -> str:
    """Render a sanitized Markdown view without secrets or raw payloads."""
    validation = validate_marketflow_repository_tag_push_strategy_approval_v1(approval)
    sections = [
        ("Title", ["MarketFlow Repository Tag Push Strategy Approval v1"]),
        ("MarketFlow Repository Tag Push Strategy Approval v1", [f"Artifact/status: `{approval['artifact_kind']}` / `{approval['approval_status']}`.", f"Digest: `{validation['marketflow_repository_tag_push_strategy_approval_digest']}`."]),
        ("Operator Attestation", [f"Decision: `{approval['operator_attestation']['operator_decision']}`.", f"Reference: `{approval['operator_attestation']['operator_reference']}`.", f"Timestamp: `{approval['operator_attestation']['operator_attestation_timestamp_utc']}`."]),
        ("Source Tag Push Operator Review", [f"Source digest: `{approval['source_tag_push_operator_review_digest']}`.", f"Source commit: `{approval['source_operator_review_commit']}`."]),
        ("Bound Evidence", [f"Complete upstream evidence fields: {len(approval['source_evidence'])}."]),
        ("Repository Context", [f"Origin main: `{approval['origin_main_commit']}`.", "Bound/pre-review/post-review refs: 564 / 566 / 568; source tags: 32 total / 4 candidate / 0 approved remote."]),
        ("Approval Scope", [approval["approval_scope"]]),
        ("Selected Tag Push Package", [f"`{approval['selected_tag_push_package']}`: approved for future execution only."]),
        ("Approved Tag Push Records", [f"`{row['tag_name']}` -> `{row['candidate_remote_ref']}` ({row['push_status']})" for row in approval["approved_tag_push_records"]]),
        ("Approved Future Push Command", [approval["approved_future_push_command_template"], approval["command_approval_status"], approval["remote_publication_status"]]),
        ("Supporting Packages", [f"{row['package_id']}: {row['approval_status']}" for row in approval["supporting_packages"]]),
        ("Next Chain", list(approval["next_chain"])),
        ("Next Gates", list(approval["next_gates"])),
        ("Risk Controls", list(approval["risk_controls"])),
        ("Authority Boundaries", ["Approval authorizes only a separate future tag-push execution. Predictive usefulness and profitability are not accepted; runtime, strategy, paper trading, and broker execution remain NOT_AUTHORIZED."]),
        ("Checklist Summary", [f"{approval['summary']['passed_checks']} / {approval['summary']['total_checks']} checks pass; {approval['summary']['blocker_count']} blockers."]),
        ("Guardrails", ["No tag push, tag creation/modification/deletion, merge, rebase, deletion, main/force push, prune, provider, data, model, recommendation, runtime, broker, or trading action occurred."]),
    ]
    lines = ["# MarketFlow Repository Tag Push Strategy Approval v1", ""]
    for title, rows in sections:
        lines.extend([f"## {title}", *[f"- {row}" for row in rows], ""])
    return "\n".join(lines)


def write_marketflow_repository_tag_push_strategy_approval_v1(
    output_dir: str | Path,
    *,
    source_review: dict | None = None,
    operator_attestation: dict,
) -> dict:
    """Write canonical approval JSON without overwriting an existing artifact."""
    approval = build_marketflow_repository_tag_push_strategy_approval_v1(
        source_review=source_review,
        operator_attestation=operator_attestation,
    )
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "marketflow_repository_tag_push_strategy_approval_v1.json"
    if path.exists():
        raise MarketFlowRepositoryTagPushStrategyApprovalError(
            "approval output already exists"
        )
    payload = canonical_json_bytes(approval)
    path.write_bytes(payload)
    return {
        "path": str(path),
        "artifact_kind": approval["artifact_kind"],
        "approval_status": approval["approval_status"],
        "marketflow_repository_tag_push_strategy_approval_digest": approval[
            "marketflow_repository_tag_push_strategy_approval_digest"
        ],
        "payload_sha256": sha256_bytes(payload),
    }
