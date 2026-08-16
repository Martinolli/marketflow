"""Offline operator-attested approval of label-objective redesign planning."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Mapping

from marketflow.historical_data.artifacts import (
    canonical_json_bytes,
    semantic_digest,
    sha256_bytes,
)
from marketflow.services import (
    label_objective_redesign_candidate_operator_review_service as review_service,
)


ARTIFACT_KIND_LABEL_OBJECTIVE_REDESIGN_APPROVED = "LABEL_OBJECTIVE_REDESIGN_APPROVED"
SCHEMA_VERSION_LABEL_OBJECTIVE_REDESIGN_APPROVAL_V1 = (
    "label_objective_redesign_approval_v1"
)
LABEL_OBJECTIVE_REDESIGN_APPROVED = "LABEL_OBJECTIVE_REDESIGN_APPROVED"
LABEL_OBJECTIVE_REDESIGN_APPROVAL_ONLY = "LABEL_OBJECTIVE_REDESIGN_APPROVAL_ONLY"
OPERATOR_DECISION_APPROVE_LABEL_OBJECTIVE_REDESIGN = (
    "APPROVE_LABEL_OBJECTIVE_REDESIGN"
)
OPERATOR_ATTESTATION_VERSION_LABEL_OBJECTIVE_REDESIGN_APPROVAL_V1 = (
    "label_objective_redesign_approval_operator_attestation_v1"
)
REQUIRED_LABEL_OBJECTIVE_REDESIGN_APPROVAL_ATTESTATION_PHRASE = (
    "APPROVE LABEL OBJECTIVE REDESIGN MSFT NVDA AMZN GOOGL META TSLA JPM XOM "
    "JNJ WMT CAT LMT LABEL_OBJECTIVE_REDESIGN_APPROVAL_ONLY"
)

EXPECTED_CANDIDATE_REVIEW_PACKAGE_DIGEST = (
    "bbc9fbda16145461b6b3c62a251e7267601f217a9ac8f7e2cc22dc6441f603a9"
)
EXPECTED_CANDIDATE_DIGEST = review_service.EXPECTED_CANDIDATE_DIGEST
candidate_service = review_service.candidate_service
TARGET_UNIVERSE = list(review_service.TARGET_UNIVERSE)
NOT_ACCEPTED = review_service.NOT_ACCEPTED
NOT_AUTHORIZED = review_service.NOT_AUTHORIZED
PASS = review_service.PASS
FAIL = review_service.FAIL
BLOCKER = review_service.BLOCKER

APPROVED_FOR_FUTURE_DESIGN_PLANNING_ONLY = (
    "APPROVED_FOR_FUTURE_DESIGN_PLANNING_ONLY"
)
APPROVED_FOR_FUTURE_EXECUTION_CANDIDATE_ONLY = (
    "APPROVED_FOR_FUTURE_EXECUTION_CANDIDATE_ONLY"
)
NOT_AUTHORIZED_FOR_EXECUTION = "NOT_AUTHORIZED_FOR_EXECUTION"

REQUIRED_DIGEST_FIELDS = {
    "label_objective_redesign_candidate_review_package_digest": EXPECTED_CANDIDATE_REVIEW_PACKAGE_DIGEST,
    "label_objective_redesign_candidate_digest": EXPECTED_CANDIDATE_DIGEST,
    **candidate_service.REQUIRED_DIGEST_FIELDS,
}

REQUIRED_TRUE_OPERATOR_CONFIRMATION_FIELDS = [
    "operator_confirms_two_readiness_gates_not_ready",
    "operator_confirms_label_objective_redesign_approval_scope_only",
    "operator_confirms_label_objective_redesign_approved",
    "operator_confirms_ready_for_label_objective_redesign_execution_candidate",
    "operator_confirms_no_label_objective_redesign_authorization",
    "operator_confirms_no_label_objective_redesign_execution",
    "operator_confirms_no_redesigned_label_generation_authorization",
    "operator_confirms_no_redesigned_label_generation",
    "operator_confirms_no_additional_predictive_evidence_execution_candidate",
    "operator_confirms_no_predictive_usefulness_acceptance",
    "operator_confirms_no_profitability_acceptance",
    "operator_confirms_no_runtime_migration_approval",
    "operator_confirms_no_strategy_authorization",
    "operator_confirms_no_paper_trading",
    "operator_confirms_no_broker_execution",
    "operator_confirms_no_trade_recommendations",
    "operator_confirms_no_api_key_storage_or_printing",
    "operator_confirms_no_raw_payload_commit",
]

NEXT_CHAIN = [
    "Label Objective Redesign Execution Candidate v1.",
    "Label Objective Redesign Execution Candidate Operator Review Package v1.",
    "Label Objective Redesign Execution Approval v1, if selected.",
    "Label Objective Redesign Execution v1.",
    "Label Objective Redesign Results Review v1.",
    "Additional Predictive Evidence Execution Candidate using redesigned labels, if results support it.",
    "Additional Predictive Evidence Execution and Results Review, if separately approved.",
    "Predictive Usefulness Reassessment and Readiness Review, only after new evidence.",
    "Predictive Usefulness Acceptance Candidate, only if readiness passes.",
    "Profitability review chain, if separately required.",
    "Runtime migration chain, if ever separately authorized.",
]

NEXT_GATES = [
    "label_objective_redesign_execution_candidate",
    "label_objective_redesign_execution_candidate_operator_review",
    "label_objective_redesign_execution_approval_if_selected",
    "label_objective_redesign_execution",
    "label_objective_redesign_results_review",
    "additional_predictive_evidence_execution_candidate_using_redesigned_labels",
    "additional_predictive_evidence_execution_approval_if_required",
    "additional_predictive_evidence_results_review",
    "predictive_usefulness_reassessment_after_new_evidence",
    "predictive_usefulness_acceptance_readiness_after_new_evidence",
    "predictive_usefulness_acceptance_candidate_if_ready",
    "profitability_review_chain_if_required",
    "runtime_migration_chain_if_ever_authorized",
]

RISK_CONTROLS = [
    "approval_does_not_authorize_label_generation",
    "approval_does_not_authorize_execution",
    "approval_does_not_accept_predictive_usefulness",
    "approval_does_not_accept_profitability",
    "approval_does_not_authorize_runtime",
    "approval_does_not_authorize_strategy",
    "approval_does_not_authorize_paper_trading",
    "approval_does_not_authorize_broker_execution",
    "approval_does_not_generate_trade_recommendations",
    "do_not_mutate_frozen_dataset",
    "preserve_meta_record_limitation",
    "no_more_execution_without_operator_approval",
    "acceptance_candidate_not_allowed_currently",
    "all_outputs_research_only",
]

CHECK_IDS = [
    "candidate_review_digest_bound",
    "candidate_digest_bound",
    "operator_method_path_selection_digest_bound",
    "method_diagnostic_digest_bound",
    "planning_tree_digest_bound",
    "latest_readiness_digest_bound",
    "research_registry_digest_bound",
    "records_digest_bound",
    "target_universe_12_preserved",
    "target_universe_matches_review_universe",
    "records_digest_preserved",
    "meta_913_preserved",
    "operator_decision_matches",
    "operator_attestation_phrase_matches",
    "operator_confirms_all_required_digests",
    "operator_confirms_selected_method_path",
    "operator_confirms_two_readiness_gates_not_ready",
    "approval_scope_label_objective_redesign_only",
    "label_objective_redesign_approved_true",
    "label_objective_redesign_approval_created_true",
    "ready_for_label_objective_redesign_execution_candidate_true",
    "label_objective_redesign_authorized_false",
    "label_objective_redesign_executed_false",
    "redesigned_label_generation_authorized_false",
    "redesigned_label_generation_performed_false",
    "additional_predictive_evidence_execution_candidate_created_false",
    "approved_hypotheses_13",
    "approved_redesign_dimensions_14",
    "approved_label_family_candidates_10",
    "approved_evaluation_questions_10",
    "per_ticker_approval_entries_12",
    "per_ticker_approval_digests_present",
    "next_chain_defined",
    "next_gates_defined",
    "risk_controls_defined",
    "predictive_usefulness_not_accepted",
    "profitability_not_accepted",
    "runtime_not_authorized",
    "strategy_not_authorized",
    "paper_trading_not_authorized",
    "broker_not_authorized",
    "trade_recommendations_false",
    "provider_requests_made_false",
    "market_data_acquisition_false",
    "dataset_regeneration_false",
    "label_generation_false",
    "feature_generation_false",
    "metric_recomputation_false",
    "model_training_false",
    "strategy_scoring_false",
    "runtime_activation_false",
    "raw_provider_payloads_not_committed",
    "api_keys_not_stored_or_printed",
    "no_label_objective_redesign_execution_created",
    "no_additional_predictive_evidence_execution_candidate_created",
    "no_predictive_usefulness_acceptance_artifact_created",
    "no_profitability_acceptance_created",
    "no_runtime_migration_approval_created",
    "no_tracked_marketflow_files",
]


class LabelObjectiveRedesignApprovalError(ValueError):
    """Raised when approval evidence or its scope is invalid."""


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise LabelObjectiveRedesignApprovalError(f"{field} mismatch")


def _expect_true(actual: Any, field: str) -> None:
    if actual is not True:
        raise LabelObjectiveRedesignApprovalError(f"{field} must be true")


def _check(check_id: str, expected: Any, actual: Any) -> dict[str, Any]:
    status = PASS if actual == expected else FAIL
    return {
        "check_id": check_id,
        "status": status,
        "expected": expected,
        "actual": actual,
        "severity": BLOCKER,
        "message": f"{check_id} {'passed' if status == PASS else 'failed'}",
    }


def build_label_objective_redesign_approval_attestation_v1(
    *,
    operator_reference: str,
    operator_attestation_timestamp_utc: str,
    operator_attestation_phrase: str,
    operator_confirms_label_objective_redesign_candidate_review_digest: str,
    operator_confirms_label_objective_redesign_candidate_digest: str,
    operator_confirms_operator_method_path_selection_digest: str,
    operator_confirms_method_diagnostic_review_digest: str,
    operator_confirms_planning_tree_review_digest: str,
    operator_confirms_latest_readiness_digest: str,
    operator_confirms_research_registry_approval_digest: str,
    operator_confirms_records_digest: str,
    operator_confirms_target_universe: list[str],
    operator_confirms_target_count: int,
    operator_confirms_meta_record_count: int,
    operator_confirms_non_meta_record_count: int,
    operator_confirms_selected_method_path: str,
    operator_confirms_two_readiness_gates_not_ready: bool,
    operator_confirms_label_objective_redesign_approval_scope_only: bool,
    operator_confirms_label_objective_redesign_approved: bool,
    operator_confirms_ready_for_label_objective_redesign_execution_candidate: bool,
    operator_confirms_no_label_objective_redesign_authorization: bool,
    operator_confirms_no_label_objective_redesign_execution: bool,
    operator_confirms_no_redesigned_label_generation_authorization: bool,
    operator_confirms_no_redesigned_label_generation: bool,
    operator_confirms_no_additional_predictive_evidence_execution_candidate: bool,
    operator_confirms_no_predictive_usefulness_acceptance: bool,
    operator_confirms_no_profitability_acceptance: bool,
    operator_confirms_no_runtime_migration_approval: bool,
    operator_confirms_no_strategy_authorization: bool,
    operator_confirms_no_paper_trading: bool,
    operator_confirms_no_broker_execution: bool,
    operator_confirms_no_trade_recommendations: bool,
    operator_confirms_no_api_key_storage_or_printing: bool,
    operator_confirms_no_raw_payload_commit: bool,
    operator_decision: str = OPERATOR_DECISION_APPROVE_LABEL_OBJECTIVE_REDESIGN,
) -> dict[str, Any]:
    """Build the explicit non-secret operator attestation."""
    return {name: deepcopy(value) for name, value in locals().items()} | {
        "operator_attestation_version": (
            OPERATOR_ATTESTATION_VERSION_LABEL_OBJECTIVE_REDESIGN_APPROVAL_V1
        )
    }


def _expected_digest_confirmations() -> dict[str, str]:
    return {
        "operator_confirms_label_objective_redesign_candidate_review_digest": EXPECTED_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "operator_confirms_label_objective_redesign_candidate_digest": EXPECTED_CANDIDATE_DIGEST,
        "operator_confirms_operator_method_path_selection_digest": candidate_service.EXPECTED_OPERATOR_METHOD_PATH_SELECTION_DIGEST,
        "operator_confirms_method_diagnostic_review_digest": candidate_service.EXPECTED_METHOD_DIAGNOSTIC_REVIEW_DIGEST,
        "operator_confirms_planning_tree_review_digest": candidate_service.EXPECTED_PLANNING_TREE_REVIEW_DIGEST,
        "operator_confirms_latest_readiness_digest": candidate_service.EXPECTED_LATEST_READINESS_DIGEST,
        "operator_confirms_research_registry_approval_digest": candidate_service.EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST,
        "operator_confirms_records_digest": candidate_service.EXPECTED_RECORDS_DIGEST,
    }


def _validate_attestation(attestation: Mapping[str, Any]) -> None:
    if not isinstance(attestation, Mapping):
        raise LabelObjectiveRedesignApprovalError("operator_attestation missing")
    expected = {
        "operator_decision": OPERATOR_DECISION_APPROVE_LABEL_OBJECTIVE_REDESIGN,
        "operator_attestation_phrase": REQUIRED_LABEL_OBJECTIVE_REDESIGN_APPROVAL_ATTESTATION_PHRASE,
        "operator_attestation_version": OPERATOR_ATTESTATION_VERSION_LABEL_OBJECTIVE_REDESIGN_APPROVAL_V1,
        "operator_confirms_target_universe": TARGET_UNIVERSE,
        "operator_confirms_target_count": 12,
        "operator_confirms_meta_record_count": 913,
        "operator_confirms_non_meta_record_count": 1003,
        "operator_confirms_selected_method_path": candidate_service.SELECTED_METHOD_PATH,
        **_expected_digest_confirmations(),
    }
    for field, value in expected.items():
        _expect(attestation.get(field), value, field)
    for field in REQUIRED_TRUE_OPERATOR_CONFIRMATION_FIELDS:
        _expect_true(attestation.get(field), field)
    for field in ("operator_reference", "operator_attestation_timestamp_utc"):
        if not isinstance(attestation.get(field), str) or not attestation[field].strip():
            raise LabelObjectiveRedesignApprovalError(f"{field} required")


def _source_review(source: dict[str, Any] | None) -> dict[str, Any]:
    package = (
        review_service.build_label_objective_redesign_candidate_review_package_v1()
        if source is None
        else deepcopy(source)
    )
    try:
        validation = (
            review_service.validate_label_objective_redesign_candidate_review_package_v1(
                package
            )
        )
    except review_service.LabelObjectiveRedesignCandidateReviewError as exc:
        raise LabelObjectiveRedesignApprovalError(
            "source label objective redesign candidate review is invalid"
        ) from exc
    _expect(
        package.get("label_objective_redesign_candidate_review_package_digest"),
        EXPECTED_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "source candidate review digest",
    )
    _expect(
        package.get("review_status"),
        review_service.LABEL_OBJECTIVE_REDESIGN_CANDIDATE_REVIEW_PACKAGE_READY,
        "source candidate review status",
    )
    _expect(package.get("review_summary", {}).get("blocker_count"), 0, "source blocker_count")
    _expect(
        validation.get("label_objective_redesign_candidate_review_package_digest"),
        EXPECTED_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "validated source candidate review digest",
    )
    return package


def _approved_hypotheses(source: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "hypothesis_id": row["hypothesis_id"],
            "approval_status": APPROVED_FOR_FUTURE_DESIGN_PLANNING_ONLY,
            "test_status": "NOT_TESTED",
            "execution_status": "NOT_EXECUTED",
            "research_only": True,
            "non_actionable": True,
        }
        for row in source["reviewed_diagnostic_hypotheses"]
    ]


def _approved_dimensions(source: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "dimension_id": row["dimension_id"],
            "approval_status": APPROVED_FOR_FUTURE_DESIGN_PLANNING_ONLY,
            "design_status": "NOT_DESIGNED",
            "authorization_status": NOT_AUTHORIZED_FOR_EXECUTION,
            "execution_status": "NOT_EXECUTED",
            "research_only": True,
            "non_actionable": True,
        }
        for row in source["reviewed_redesign_dimensions"]
    ]


def _approved_families(source: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "label_family_candidate_id": row["label_family_candidate_id"],
            "approval_status": APPROVED_FOR_FUTURE_DESIGN_PLANNING_ONLY,
            "candidate_status": "PLANNED_NOT_GENERATED",
            "design_status": "CANDIDATE_ONLY",
            "label_generation_authorized": False,
            "label_generation_performed": False,
            "research_only": True,
            "non_actionable": True,
        }
        for row in source["reviewed_label_family_candidates"]
    ]


def _approved_questions(source: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "question_id": row["question_id"],
            "approval_status": APPROVED_FOR_FUTURE_DESIGN_PLANNING_ONLY,
            "question_status": "PLANNED_FOR_FUTURE_REVIEW",
            "answer_status": "NOT_ANSWERED",
            "requires_execution": False,
            "research_only": True,
        }
        for row in source["reviewed_evaluation_questions"]
    ]


def per_ticker_label_objective_redesign_approval_digest_v1(
    entry: dict[str, Any],
) -> str:
    """Return the deterministic digest for one ticker approval entry."""
    payload = deepcopy(entry)
    payload.pop("per_ticker_label_objective_redesign_approval_digest", None)
    return semantic_digest(payload)


def _per_ticker_approvals(source: dict[str, Any]) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for row in source["per_ticker_review_entries"]:
        entry = {
            "ticker": row["ticker"],
            "registry_approval_status": row["registry_approval_status"],
            "canonical_dataset_status": row["canonical_dataset_status"],
            "historical_record_count": row["historical_record_count"],
            "meta_reduced_record_count_flag": row["meta_reduced_record_count_flag"],
            "selected_method_path": row["selected_method_path"],
            "label_objective_redesign_candidate_status": (
                "REVIEWED_READY_FOR_OPERATOR_ASSESSMENT"
            ),
            "label_objective_redesign_approval_status": (
                APPROVED_FOR_FUTURE_EXECUTION_CANDIDATE_ONLY
            ),
            "label_objective_redesign_approved": True,
            "label_objective_redesign_authorized": False,
            "label_objective_redesign_executed": False,
            "redesigned_label_generation_authorized": False,
            "redesigned_label_generation_performed": False,
            "predictive_usefulness": NOT_ACCEPTED,
            "predictive_usefulness_acceptance_candidate_created": False,
            "profitability": NOT_ACCEPTED,
            "runtime_use": NOT_AUTHORIZED,
            "strategy_use": NOT_AUTHORIZED,
            "paper_trading": NOT_AUTHORIZED,
            "broker_execution": NOT_AUTHORIZED,
            "source_label_objective_redesign_candidate_review_digest": source[
                "label_objective_redesign_candidate_review_package_digest"
            ],
            "source_label_objective_redesign_candidate_digest": source[
                "label_objective_redesign_candidate_digest"
            ],
        }
        if row["ticker"] == "META":
            entry["redesign_note"] = row["redesign_note"]
        entry["per_ticker_label_objective_redesign_approval_digest"] = (
            per_ticker_label_objective_redesign_approval_digest_v1(entry)
        )
        entries.append(entry)
    return entries


def _base_approval(
    source: dict[str, Any], attestation: Mapping[str, Any]
) -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_LABEL_OBJECTIVE_REDESIGN_APPROVED,
        "schema_version": SCHEMA_VERSION_LABEL_OBJECTIVE_REDESIGN_APPROVAL_V1,
        "approval_status": LABEL_OBJECTIVE_REDESIGN_APPROVED,
        "approval_scope": LABEL_OBJECTIVE_REDESIGN_APPROVAL_ONLY,
        "created_offline": True,
        "research_only": True,
        "operator_review_required": True,
        "label_objective_redesign_candidate_created": True,
        "label_objective_redesign_candidate_review_created": True,
        "label_objective_redesign_approved": True,
        "label_objective_redesign_approval_created": True,
        "ready_for_label_objective_redesign_execution_candidate": True,
        "label_objective_redesign_authorized": False,
        "label_objective_redesign_executed": False,
        "label_objective_redesign_results_created": False,
        "redesigned_label_generation_authorized": False,
        "redesigned_label_generation_performed": False,
        "redesigned_feature_generation_authorized": False,
        "redesigned_feature_generation_performed": False,
        "redesigned_protocol_evaluation_authorized": False,
        "redesigned_protocol_evaluation_performed": False,
        "additional_predictive_evidence_execution_candidate_created": False,
        "additional_predictive_evidence_execution_authorized": False,
        "additional_predictive_evidence_executed": False,
        "predictive_usefulness": NOT_ACCEPTED,
        "predictive_usefulness_acceptance_ready": False,
        "predictive_usefulness_acceptance_recommended": False,
        "predictive_usefulness_acceptance_candidate_created": False,
        "profitability": NOT_ACCEPTED,
        "profitability_acceptance_ready": False,
        "profitability_acceptance_recommended": False,
        "runtime_migration_approved": False,
        "runtime_migration_active": False,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "automatic_stitching": False,
        "new_strategy_scoring_performed": False,
        "trade_recommendations_generated": False,
        "provider_requests_made": False,
        "market_data_acquisition_performed": False,
        "dataset_regeneration_performed": False,
        "label_generation_performed": False,
        "feature_generation_performed": False,
        "metric_recomputation_performed": False,
        "model_training_performed": False,
        "raw_provider_payloads_committed": False,
        "api_keys_stored_or_printed": False,
        "label_objective_redesign_execution_created": False,
        "predictive_usefulness_acceptance_artifact_created": False,
        "profitability_acceptance_created": False,
        "runtime_migration_approval_created": False,
        "tracked_marketflow_files": [],
        "no_tracked_marketflow_files": True,
        **REQUIRED_DIGEST_FIELDS,
        "dataset_name": source["dataset_name"],
        "source_profile": source["source_profile"],
        "timeframe": source["timeframe"],
        "date_range_start": source["date_range_start"],
        "date_range_end": source["date_range_end"],
        "target_universe": deepcopy(source["target_universe"]),
        "target_universe_count": source["target_universe_count"],
        "total_canonical_record_count": source["total_canonical_record_count"],
        "per_ticker_record_counts": deepcopy(source["per_ticker_record_counts"]),
        "meta_record_count": source["meta_record_count"],
        "non_meta_record_count": source["non_meta_record_count"],
        "meta_reduced_record_count_preserved": source[
            "meta_reduced_record_count_preserved"
        ],
        "selected_method_path": source["selected_method_path"],
        "label_objective_redesign_objective": source[
            "label_objective_redesign_objective"
        ],
        "label_objective_redesign_scope": (
            "LABEL_OBJECTIVE_REDESIGN_APPROVAL_ONLY_NOT_EXECUTION"
        ),
        "label_objective_redesign_mode": "APPROVED_NOT_EXECUTED",
        "label_objective_redesign_authority_status": (
            APPROVED_FOR_FUTURE_EXECUTION_CANDIDATE_ONLY
        ),
        "approved_problem_basis": deepcopy(source["problem_basis"]),
        "approved_hypotheses": _approved_hypotheses(source),
        "approved_redesign_dimensions": _approved_dimensions(source),
        "approved_label_family_candidates": _approved_families(source),
        "approved_evaluation_questions": _approved_questions(source),
        "per_ticker_approval_entries": _per_ticker_approvals(source),
        "next_chain": list(NEXT_CHAIN),
        "next_gates": list(NEXT_GATES),
        "risk_controls": list(RISK_CONTROLS),
        "operator_attestation": deepcopy(dict(attestation)),
    }


def _derived_checks(approval: dict[str, Any]) -> dict[str, bool]:
    attestation = approval.get("operator_attestation", {})
    entries = approval.get("per_ticker_approval_entries", [])
    counts = approval.get("per_ticker_record_counts", {})
    digest_confirmations = _expected_digest_confirmations()
    return {
        "candidate_review_digest_bound": approval.get("label_objective_redesign_candidate_review_package_digest") == EXPECTED_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "candidate_digest_bound": approval.get("label_objective_redesign_candidate_digest") == EXPECTED_CANDIDATE_DIGEST,
        "operator_method_path_selection_digest_bound": approval.get("operator_method_path_selection_digest") == candidate_service.EXPECTED_OPERATOR_METHOD_PATH_SELECTION_DIGEST,
        "method_diagnostic_digest_bound": approval.get("predictive_evidence_method_diagnostic_review_package_digest") == candidate_service.EXPECTED_METHOD_DIAGNOSTIC_REVIEW_DIGEST,
        "planning_tree_digest_bound": approval.get("predictive_evidence_planning_tree_review_package_digest") == candidate_service.EXPECTED_PLANNING_TREE_REVIEW_DIGEST,
        "latest_readiness_digest_bound": approval.get("latest_readiness_rerun_using_refined_evidence_digest") == candidate_service.EXPECTED_LATEST_READINESS_DIGEST,
        "research_registry_digest_bound": approval.get("research_registry_approval_digest") == candidate_service.EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST,
        "records_digest_bound": approval.get("records_digest") == candidate_service.EXPECTED_RECORDS_DIGEST,
        "target_universe_12_preserved": approval.get("target_universe_count") == 12 and approval.get("target_universe") == TARGET_UNIVERSE,
        "target_universe_matches_review_universe": approval.get("target_universe") == TARGET_UNIVERSE,
        "records_digest_preserved": approval.get("records_digest") == candidate_service.EXPECTED_RECORDS_DIGEST,
        "meta_913_preserved": approval.get("meta_record_count") == 913 and counts.get("META") == 913 and approval.get("meta_reduced_record_count_preserved") is True,
        "operator_decision_matches": attestation.get("operator_decision") == OPERATOR_DECISION_APPROVE_LABEL_OBJECTIVE_REDESIGN,
        "operator_attestation_phrase_matches": attestation.get("operator_attestation_phrase") == REQUIRED_LABEL_OBJECTIVE_REDESIGN_APPROVAL_ATTESTATION_PHRASE,
        "operator_confirms_all_required_digests": all(attestation.get(field) == expected for field, expected in digest_confirmations.items()),
        "operator_confirms_selected_method_path": attestation.get("operator_confirms_selected_method_path") == candidate_service.SELECTED_METHOD_PATH,
        "operator_confirms_two_readiness_gates_not_ready": attestation.get("operator_confirms_two_readiness_gates_not_ready") is True,
        "approval_scope_label_objective_redesign_only": approval.get("approval_scope") == LABEL_OBJECTIVE_REDESIGN_APPROVAL_ONLY and attestation.get("operator_confirms_label_objective_redesign_approval_scope_only") is True,
        "label_objective_redesign_approved_true": approval.get("label_objective_redesign_approved") is True,
        "label_objective_redesign_approval_created_true": approval.get("label_objective_redesign_approval_created") is True,
        "ready_for_label_objective_redesign_execution_candidate_true": approval.get("ready_for_label_objective_redesign_execution_candidate") is True,
        "label_objective_redesign_authorized_false": approval.get("label_objective_redesign_authorized") is False,
        "label_objective_redesign_executed_false": approval.get("label_objective_redesign_executed") is False,
        "redesigned_label_generation_authorized_false": approval.get("redesigned_label_generation_authorized") is False,
        "redesigned_label_generation_performed_false": approval.get("redesigned_label_generation_performed") is False,
        "additional_predictive_evidence_execution_candidate_created_false": approval.get("additional_predictive_evidence_execution_candidate_created") is False,
        "approved_hypotheses_13": [item.get("hypothesis_id") for item in approval.get("approved_hypotheses", []) if isinstance(item, dict)] == candidate_service.DIAGNOSTIC_HYPOTHESES,
        "approved_redesign_dimensions_14": [item.get("dimension_id") for item in approval.get("approved_redesign_dimensions", []) if isinstance(item, dict)] == candidate_service.REDESIGN_DIMENSIONS,
        "approved_label_family_candidates_10": [item.get("label_family_candidate_id") for item in approval.get("approved_label_family_candidates", []) if isinstance(item, dict)] == candidate_service.LABEL_FAMILY_CANDIDATES,
        "approved_evaluation_questions_10": [item.get("question_id") for item in approval.get("approved_evaluation_questions", []) if isinstance(item, dict)] == candidate_service.EVALUATION_QUESTIONS,
        "per_ticker_approval_entries_12": isinstance(entries, list) and len(entries) == 12 and [item.get("ticker") for item in entries if isinstance(item, dict)] == TARGET_UNIVERSE,
        "per_ticker_approval_digests_present": isinstance(entries, list) and len(entries) == 12 and all(isinstance(item.get("per_ticker_label_objective_redesign_approval_digest"), str) and len(item["per_ticker_label_objective_redesign_approval_digest"]) == 64 and item["per_ticker_label_objective_redesign_approval_digest"] == per_ticker_label_objective_redesign_approval_digest_v1(item) for item in entries if isinstance(item, dict)),
        "next_chain_defined": approval.get("next_chain") == NEXT_CHAIN,
        "next_gates_defined": approval.get("next_gates") == NEXT_GATES,
        "risk_controls_defined": approval.get("risk_controls") == RISK_CONTROLS,
        "predictive_usefulness_not_accepted": approval.get("predictive_usefulness") == NOT_ACCEPTED,
        "profitability_not_accepted": approval.get("profitability") == NOT_ACCEPTED,
        "runtime_not_authorized": approval.get("runtime_migration_approved") is False and approval.get("runtime_migration_active") is False and approval.get("runtime_use") == NOT_AUTHORIZED,
        "strategy_not_authorized": approval.get("strategy_use") == NOT_AUTHORIZED,
        "paper_trading_not_authorized": approval.get("paper_trading") == NOT_AUTHORIZED,
        "broker_not_authorized": approval.get("broker_execution") == NOT_AUTHORIZED,
        "trade_recommendations_false": approval.get("trade_recommendations_generated") is False,
        "provider_requests_made_false": approval.get("provider_requests_made") is False,
        "market_data_acquisition_false": approval.get("market_data_acquisition_performed") is False,
        "dataset_regeneration_false": approval.get("dataset_regeneration_performed") is False,
        "label_generation_false": approval.get("label_generation_performed") is False and approval.get("redesigned_label_generation_performed") is False,
        "feature_generation_false": approval.get("feature_generation_performed") is False and approval.get("redesigned_feature_generation_performed") is False,
        "metric_recomputation_false": approval.get("metric_recomputation_performed") is False,
        "model_training_false": approval.get("model_training_performed") is False,
        "strategy_scoring_false": approval.get("new_strategy_scoring_performed") is False,
        "runtime_activation_false": approval.get("runtime_migration_active") is False,
        "raw_provider_payloads_not_committed": approval.get("raw_provider_payloads_committed") is False,
        "api_keys_not_stored_or_printed": approval.get("api_keys_stored_or_printed") is False,
        "no_label_objective_redesign_execution_created": approval.get("label_objective_redesign_execution_created") is False,
        "no_additional_predictive_evidence_execution_candidate_created": approval.get("additional_predictive_evidence_execution_candidate_created") is False,
        "no_predictive_usefulness_acceptance_artifact_created": approval.get("predictive_usefulness_acceptance_artifact_created") is False,
        "no_profitability_acceptance_created": approval.get("profitability_acceptance_created") is False,
        "no_runtime_migration_approval_created": approval.get("runtime_migration_approval_created") is False,
        "no_tracked_marketflow_files": approval.get("no_tracked_marketflow_files") is True and approval.get("tracked_marketflow_files") == [],
    }


def _checklist(approval: dict[str, Any]) -> list[dict[str, Any]]:
    checks = _derived_checks(approval)
    return [_check(check_id, True, checks.get(check_id)) for check_id in CHECK_IDS]


def _summary(checklist: list[dict[str, Any]]) -> dict[str, Any]:
    total = len(checklist)
    passed = sum(item.get("status") == PASS for item in checklist)
    failed = total - passed
    blockers = sum(
        item.get("status") == FAIL and item.get("severity") == BLOCKER
        for item in checklist
    )
    return {
        "total_checks": total,
        "passed_checks": passed,
        "failed_checks": failed,
        "blocker_count": blockers,
        "label_objective_redesign_approved_by_operator": blockers == 0,
        "label_objective_redesign_approved": blockers == 0,
        "approval_scope": LABEL_OBJECTIVE_REDESIGN_APPROVAL_ONLY,
        "ready_for_label_objective_redesign_execution_candidate": blockers == 0,
        "label_objective_redesign_authorized": False,
        "label_objective_redesign_executed": False,
        "redesigned_label_generation_authorized": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_authorized": False,
        "trade_recommendations_generated": False,
    }


def _digest_payload(approval: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(approval)
    payload.pop("label_objective_redesign_approval_digest", None)
    return payload


def label_objective_redesign_approval_digest_v1(
    approval: dict[str, Any],
) -> str:
    """Return the deterministic operator-attested approval digest."""
    return semantic_digest(_digest_payload(approval))


def build_label_objective_redesign_approved_v1(
    *,
    candidate_review_package: dict | None = None,
    operator_attestation: dict,
) -> dict:
    """Approve future execution-candidate planning, never execution itself."""
    _validate_attestation(operator_attestation)
    source = _source_review(candidate_review_package)
    approval = _base_approval(source, operator_attestation)
    approval["approval_checklist"] = _checklist(approval)
    approval["approval_summary"] = _summary(approval["approval_checklist"])
    approval["label_objective_redesign_approval_digest"] = (
        label_objective_redesign_approval_digest_v1(approval)
    )
    validate_label_objective_redesign_approved_v1(approval)
    return approval


def _reject_forbidden_authority(value: Any, *, path: str = "approval") -> None:
    forbidden_true_fields = {
        "label_objective_redesign_authorized",
        "label_objective_redesign_executed",
        "label_objective_redesign_results_created",
        "redesigned_label_generation_authorized",
        "redesigned_label_generation_performed",
        "redesigned_feature_generation_authorized",
        "redesigned_feature_generation_performed",
        "redesigned_protocol_evaluation_authorized",
        "redesigned_protocol_evaluation_performed",
        "additional_predictive_evidence_execution_candidate_created",
        "additional_predictive_evidence_execution_authorized",
        "additional_predictive_evidence_executed",
        "predictive_usefulness_acceptance_ready",
        "predictive_usefulness_acceptance_recommended",
        "predictive_usefulness_acceptance_candidate_created",
        "profitability_acceptance_ready",
        "profitability_acceptance_recommended",
        "runtime_migration_approved",
        "runtime_migration_active",
        "automatic_stitching",
        "new_strategy_scoring_performed",
        "trade_recommendations_generated",
        "provider_requests_made",
        "market_data_acquisition_performed",
        "dataset_regeneration_performed",
        "label_generation_authorized",
        "label_generation_performed",
        "feature_generation_authorized",
        "feature_generation_performed",
        "metric_recomputation_performed",
        "model_training_performed",
        "label_objective_redesign_execution_created",
        "predictive_usefulness_acceptance_artifact_created",
        "profitability_acceptance_created",
        "runtime_migration_approval_created",
    }
    if isinstance(value, dict):
        for key, item in value.items():
            current = f"{path}.{key}"
            if key in forbidden_true_fields and item is True:
                raise LabelObjectiveRedesignApprovalError(
                    f"{current} must remain false"
                )
            if key in {
                "runtime_use",
                "strategy_use",
                "paper_trading",
                "broker_execution",
            } and item == "AUTHORIZED":
                raise LabelObjectiveRedesignApprovalError(
                    f"{current} must not be AUTHORIZED"
                )
            if key in {"predictive_usefulness", "profitability"} and item == "accepted":
                raise LabelObjectiveRedesignApprovalError(
                    f"{current} must not be accepted"
                )
            _reject_forbidden_authority(item, path=current)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _reject_forbidden_authority(item, path=f"{path}[{index}]")


def validate_label_objective_redesign_approved_v1(approval: dict) -> dict:
    """Validate attestation, exact bindings, and approval-only authority."""
    if not isinstance(approval, dict):
        raise LabelObjectiveRedesignApprovalError("approval must be a JSON object")
    _reject_forbidden_authority(approval)
    attestation = approval.get("operator_attestation")
    _validate_attestation(attestation)
    expected_base = _base_approval(_source_review(None), attestation)
    for field, expected in expected_base.items():
        _expect(approval.get(field), expected, field)
    checklist = approval.get("approval_checklist")
    if not isinstance(checklist, list):
        raise LabelObjectiveRedesignApprovalError("approval_checklist missing")
    _expect(
        [item.get("check_id") for item in checklist if isinstance(item, dict)],
        CHECK_IDS,
        "approval_checklist check IDs",
    )
    expected_checklist = _checklist(approval)
    _expect(checklist, expected_checklist, "approval_checklist")
    if any(item["status"] != PASS for item in expected_checklist):
        raise LabelObjectiveRedesignApprovalError(
            "approval_checklist contains a failed check"
        )
    expected_summary = _summary(expected_checklist)
    _expect(approval.get("approval_summary"), expected_summary, "approval_summary")
    digest = approval.get("label_objective_redesign_approval_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise LabelObjectiveRedesignApprovalError(
            "label objective redesign approval digest missing"
        )
    _expect(
        digest,
        label_objective_redesign_approval_digest_v1(approval),
        "label_objective_redesign_approval_digest",
    )
    return {
        "status": "LABEL_OBJECTIVE_REDESIGN_APPROVAL_VALID",
        "artifact_kind": approval["artifact_kind"],
        "approval_status": approval["approval_status"],
        "approval_scope": approval["approval_scope"],
        "label_objective_redesign_approval_digest": digest,
        "label_objective_redesign_approved": True,
        "ready_for_label_objective_redesign_execution_candidate": True,
        "label_objective_redesign_authorized": False,
        "label_objective_redesign_executed": False,
        "blocker_count": expected_summary["blocker_count"],
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED,
    }


def build_label_objective_redesign_approved_markdown_v1(approval: dict) -> str:
    """Render a validated approval-only Markdown summary."""
    validate_label_objective_redesign_approved_v1(approval)
    summary = approval["approval_summary"]
    attestation = approval["operator_attestation"]
    lines = [
        "# MarketFlow Label Objective Redesign Approval",
        "",
        "## Title",
        "- Label Objective Redesign Approval Ceremony v1.",
        "",
        "## Label Objective Redesign Approval",
        f"- Artifact/status/scope: `{approval['artifact_kind']}` / `{approval['approval_status']}` / `{approval['approval_scope']}`.",
        "",
        "## Operator Attestation",
        f"- Reference: `{attestation['operator_reference']}`.",
        f"- Decision: `{attestation['operator_decision']}`.",
        f"- Timestamp: `{attestation['operator_attestation_timestamp_utc']}`.",
        "",
        "## Bound Evidence",
    ]
    lines.extend(f"- {field}: `{approval[field]}`." for field in REQUIRED_DIGEST_FIELDS)
    lines.extend([
        "",
        "## Dataset and Universe",
        f"- Dataset: `{approval['dataset_name']}`; records: `{approval['total_canonical_record_count']}`.",
        f"- Universe: `{', '.join(approval['target_universe'])}`; META records: `{approval['meta_record_count']}`.",
        "",
        "## Approved Problem Basis",
    ])
    lines.extend(f"- {key}: `{value}`." for key, value in approval["approved_problem_basis"].items())
    for heading, key, id_key in [
        ("Approved Hypotheses", "approved_hypotheses", "hypothesis_id"),
        ("Approved Redesign Dimensions", "approved_redesign_dimensions", "dimension_id"),
        ("Approved Label Family Candidates", "approved_label_family_candidates", "label_family_candidate_id"),
        ("Approved Evaluation Questions", "approved_evaluation_questions", "question_id"),
    ]:
        lines.extend(["", f"## {heading}"])
        lines.extend(f"- `{item[id_key]}`." for item in approval[key])
    lines.extend(["", "## Per-Ticker Approval Entries"])
    lines.extend(f"- `{item['ticker']}`: approved for future execution-candidate planning only; execution unauthorized." for item in approval["per_ticker_approval_entries"])
    for heading, key in [
        ("Next Chain", "next_chain"),
        ("Next Gates", "next_gates"),
        ("Risk Controls", "risk_controls"),
    ]:
        lines.extend(["", f"## {heading}"])
        lines.extend(f"- {item}" for item in approval[key])
    lines.extend([
        "",
        "## Checklist Summary",
        f"- `{summary['passed_checks']} / {summary['total_checks']}` passed; `{summary['blocker_count']}` blockers.",
        "",
        "## Guardrails",
        "- Approval permits future execution-candidate planning only; it does not authorize or perform redesign, label generation, predictive acceptance, runtime, trading, or recommendations.",
    ])
    return "\n".join(lines)


def write_label_objective_redesign_approved_v1(
    output_dir: str | Path,
    *,
    candidate_review_package: dict | None = None,
    operator_attestation: dict,
    filename: str | None = None,
) -> dict:
    """Write one canonical operator-attested approval without overwriting."""
    approval = build_label_objective_redesign_approved_v1(
        candidate_review_package=candidate_review_package,
        operator_attestation=operator_attestation,
    )
    validation = validate_label_objective_redesign_approved_v1(approval)
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    output_name = filename or "label_objective_redesign_approval_v1.json"
    if Path(output_name).name != output_name or not output_name.endswith(".json"):
        raise LabelObjectiveRedesignApprovalError(
            "approval filename must be a simple JSON filename"
        )
    path = directory / output_name
    if path.exists():
        raise LabelObjectiveRedesignApprovalError("approval output already exists")
    payload = canonical_json_bytes(approval)
    with path.open("xb") as handle:
        handle.write(payload)
    return validation | {
        "path": str(path).replace("\\", "/"),
        "filename": path.name,
        "payload_byte_size": len(payload),
        "payload_sha256": sha256_bytes(payload),
    }
