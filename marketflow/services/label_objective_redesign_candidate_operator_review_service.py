"""Offline operator review of the label-objective redesign candidate."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from marketflow.historical_data.artifacts import (
    canonical_json_bytes,
    semantic_digest,
    sha256_bytes,
)
from marketflow.services import label_objective_redesign_candidate_service as candidate_service


ARTIFACT_KIND_LABEL_OBJECTIVE_REDESIGN_CANDIDATE_REVIEW_PACKAGE = (
    "LABEL_OBJECTIVE_REDESIGN_CANDIDATE_REVIEW_PACKAGE"
)
SCHEMA_VERSION_LABEL_OBJECTIVE_REDESIGN_CANDIDATE_REVIEW_V1 = (
    "label_objective_redesign_candidate_review_v1"
)
LABEL_OBJECTIVE_REDESIGN_CANDIDATE_REVIEW_PACKAGE_READY = (
    "LABEL_OBJECTIVE_REDESIGN_CANDIDATE_REVIEW_PACKAGE_READY"
)
EXPECTED_CANDIDATE_DIGEST = (
    "c6ec4135b67d8c48c0358deda94ecf2672a90c666180cf26079dac1b3784ee89"
)

TARGET_UNIVERSE = list(candidate_service.TARGET_UNIVERSE)
NOT_ACCEPTED = candidate_service.NOT_ACCEPTED
NOT_AUTHORIZED = candidate_service.NOT_AUTHORIZED
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

REQUIRED_DIGEST_FIELDS = {
    "label_objective_redesign_candidate_digest": EXPECTED_CANDIDATE_DIGEST,
    **candidate_service.REQUIRED_DIGEST_FIELDS,
}

CHECK_IDS = [
    "candidate_kind_matches",
    "candidate_status_ready_for_review",
    "candidate_digest_matches_expected",
    "candidate_checklist_zero_blockers",
    "label_objective_redesign_candidate_digest_bound",
    "operator_method_path_selection_digest_bound",
    "method_diagnostic_digest_bound",
    "planning_tree_digest_bound",
    "latest_readiness_digest_bound",
    "research_registry_digest_bound",
    "records_digest_bound",
    "target_universe_12_preserved",
    "target_universe_matches_candidate_universe",
    "records_digest_preserved",
    "meta_913_preserved",
    "selected_method_path_label_objective_redesign",
    "label_objective_redesign_candidate_created_true",
    "label_objective_redesign_candidate_review_created_true",
    "label_objective_redesign_ready_for_operator_review_true",
    "label_objective_redesign_not_approved",
    "label_objective_redesign_not_authorized",
    "label_objective_redesign_not_executed",
    "redesigned_label_generation_not_authorized",
    "redesigned_label_generation_not_performed",
    "hypotheses_reviewed",
    "redesign_dimensions_reviewed",
    "label_family_candidates_reviewed",
    "evaluation_questions_reviewed",
    "per_ticker_entries_12",
    "per_ticker_candidate_digests_present",
    "per_ticker_review_digests_present",
    "future_chain_reviewed",
    "future_gates_reviewed",
    "risk_controls_reviewed",
    "planned_outputs_not_generated",
    "planned_outputs_research_only",
    "predictive_usefulness_not_accepted",
    "profitability_not_accepted",
    "runtime_not_authorized",
    "strategy_not_authorized",
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
    "no_label_objective_redesign_approval_created",
    "no_label_objective_redesign_execution_created",
    "no_additional_predictive_evidence_execution_candidate_created",
    "no_predictive_usefulness_acceptance_artifact_created",
    "no_profitability_acceptance_created",
    "no_runtime_migration_approval_created",
    "no_tracked_marketflow_files",
]


class LabelObjectiveRedesignCandidateReviewError(ValueError):
    """Raised when the review package violates its review-only boundary."""


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise LabelObjectiveRedesignCandidateReviewError(f"{field} mismatch")


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


def _source_candidate(candidate: dict | None) -> dict[str, Any]:
    source = (
        candidate_service.build_label_objective_redesign_candidate_v1()
        if candidate is None
        else deepcopy(candidate)
    )
    candidate_service.validate_label_objective_redesign_candidate_v1(source)
    _expect(
        source.get("label_objective_redesign_candidate_digest"),
        EXPECTED_CANDIDATE_DIGEST,
        "source label objective redesign candidate digest",
    )
    return source


def _per_ticker_digest_payload(entry: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(entry)
    payload.pop("per_ticker_label_objective_redesign_candidate_review_digest", None)
    return payload


def per_ticker_label_objective_redesign_candidate_review_digest_v1(
    entry: dict[str, Any],
) -> str:
    """Return the deterministic digest for one reviewed ticker entry."""
    return semantic_digest(_per_ticker_digest_payload(entry))


def _per_ticker_review_entries(source: dict[str, Any]) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for source_entry in source["per_ticker_entries"]:
        entry = {
            "ticker": source_entry["ticker"],
            "registry_approval_status": source_entry["registry_approval_status"],
            "canonical_dataset_status": source_entry["canonical_dataset_status"],
            "historical_record_count": source_entry["historical_record_count"],
            "meta_reduced_record_count_flag": source_entry[
                "meta_reduced_record_count_flag"
            ],
            "selected_method_path": source_entry["selected_method_path"],
            "label_objective_redesign_candidate_status": source_entry[
                "label_objective_redesign_candidate_status"
            ],
            "label_objective_redesign_candidate_review_status": (
                "READY_FOR_OPERATOR_ASSESSMENT"
            ),
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
            "source_label_objective_redesign_candidate_digest": source[
                "label_objective_redesign_candidate_digest"
            ],
            "per_ticker_label_objective_redesign_candidate_digest": source_entry[
                "per_ticker_label_objective_redesign_candidate_digest"
            ],
        }
        if source_entry["ticker"] == "META":
            entry["redesign_note"] = source_entry["redesign_note"]
        entry["per_ticker_label_objective_redesign_candidate_review_digest"] = (
            per_ticker_label_objective_redesign_candidate_review_digest_v1(entry)
        )
        entries.append(entry)
    return entries


def _base_review(source: dict[str, Any]) -> dict[str, Any]:
    source_summary = source["review_summary"]
    return {
        "artifact_kind": ARTIFACT_KIND_LABEL_OBJECTIVE_REDESIGN_CANDIDATE_REVIEW_PACKAGE,
        "schema_version": SCHEMA_VERSION_LABEL_OBJECTIVE_REDESIGN_CANDIDATE_REVIEW_V1,
        "review_status": LABEL_OBJECTIVE_REDESIGN_CANDIDATE_REVIEW_PACKAGE_READY,
        "created_offline": True,
        "research_only": True,
        "operator_review_required": True,
        "label_objective_redesign_candidate_created": True,
        "label_objective_redesign_candidate_review_created": True,
        "label_objective_redesign_ready_for_operator_review": True,
        "label_objective_redesign_approved": False,
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
        "label_objective_redesign_approval_created": False,
        "label_objective_redesign_execution_created": False,
        "predictive_usefulness_acceptance_artifact_created": False,
        "profitability_acceptance_created": False,
        "runtime_migration_approval_created": False,
        "tracked_marketflow_files": [],
        "no_tracked_marketflow_files": True,
        "reviewed_label_objective_redesign_candidate_kind": source["artifact_kind"],
        "reviewed_label_objective_redesign_candidate_status": source[
            "candidate_status"
        ],
        "reviewed_label_objective_redesign_candidate_digest": source[
            "label_objective_redesign_candidate_digest"
        ],
        "reviewed_label_objective_redesign_candidate_checklist_total": source_summary[
            "total_checks"
        ],
        "reviewed_label_objective_redesign_candidate_checklist_passed": source_summary[
            "passed_checks"
        ],
        "reviewed_label_objective_redesign_candidate_checklist_failed": source_summary[
            "failed_checks"
        ],
        "reviewed_label_objective_redesign_candidate_blocker_count": source_summary[
            "blocker_count"
        ],
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
        "label_objective_redesign_scope": source["label_objective_redesign_scope"],
        "label_objective_redesign_mode": source["label_objective_redesign_mode"],
        "label_objective_redesign_authority_status": source[
            "label_objective_redesign_authority_status"
        ],
        "problem_basis": deepcopy(source["problem_basis"]),
        "evidence_comparison": deepcopy(source["evidence_comparison"]),
        "reviewed_diagnostic_hypotheses": deepcopy(
            source["diagnostic_hypotheses"]
        ),
        "reviewed_redesign_dimensions": deepcopy(source["redesign_dimensions"]),
        "reviewed_label_family_candidates": deepcopy(
            source["label_family_candidates"]
        ),
        "reviewed_evaluation_questions": deepcopy(
            source["evaluation_questions"]
        ),
        "per_ticker_review_entries": _per_ticker_review_entries(source),
        "reviewed_future_chain": deepcopy(source["future_chain"]),
        "reviewed_future_gates": deepcopy(source["future_gates"]),
        "reviewed_risk_controls": deepcopy(source["risk_controls"]),
        "reviewed_planned_outputs": deepcopy(source["planned_outputs"]),
    }


def _derived_checks(review: dict[str, Any]) -> dict[str, bool]:
    entries = review.get("per_ticker_review_entries", [])
    outputs = review.get("reviewed_planned_outputs", [])
    counts = review.get("per_ticker_record_counts", {})
    return {
        "candidate_kind_matches": review.get("reviewed_label_objective_redesign_candidate_kind") == candidate_service.ARTIFACT_KIND_LABEL_OBJECTIVE_REDESIGN_CANDIDATE,
        "candidate_status_ready_for_review": review.get("reviewed_label_objective_redesign_candidate_status") == candidate_service.LABEL_OBJECTIVE_REDESIGN_READY_FOR_OPERATOR_REVIEW,
        "candidate_digest_matches_expected": review.get("reviewed_label_objective_redesign_candidate_digest") == EXPECTED_CANDIDATE_DIGEST,
        "candidate_checklist_zero_blockers": review.get("reviewed_label_objective_redesign_candidate_checklist_total") == 44 and review.get("reviewed_label_objective_redesign_candidate_checklist_passed") == 44 and review.get("reviewed_label_objective_redesign_candidate_checklist_failed") == 0 and review.get("reviewed_label_objective_redesign_candidate_blocker_count") == 0,
        "label_objective_redesign_candidate_digest_bound": review.get("label_objective_redesign_candidate_digest") == EXPECTED_CANDIDATE_DIGEST,
        "operator_method_path_selection_digest_bound": review.get("operator_method_path_selection_digest") == candidate_service.EXPECTED_OPERATOR_METHOD_PATH_SELECTION_DIGEST,
        "method_diagnostic_digest_bound": review.get("predictive_evidence_method_diagnostic_review_package_digest") == candidate_service.EXPECTED_METHOD_DIAGNOSTIC_REVIEW_DIGEST,
        "planning_tree_digest_bound": review.get("predictive_evidence_planning_tree_review_package_digest") == candidate_service.EXPECTED_PLANNING_TREE_REVIEW_DIGEST,
        "latest_readiness_digest_bound": review.get("latest_readiness_rerun_using_refined_evidence_digest") == candidate_service.EXPECTED_LATEST_READINESS_DIGEST,
        "research_registry_digest_bound": review.get("research_registry_approval_digest") == candidate_service.EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST,
        "records_digest_bound": review.get("records_digest") == candidate_service.EXPECTED_RECORDS_DIGEST,
        "target_universe_12_preserved": review.get("target_universe_count") == 12 and review.get("target_universe") == TARGET_UNIVERSE,
        "target_universe_matches_candidate_universe": review.get("target_universe") == TARGET_UNIVERSE,
        "records_digest_preserved": review.get("records_digest") == candidate_service.EXPECTED_RECORDS_DIGEST,
        "meta_913_preserved": review.get("meta_record_count") == 913 and counts.get("META") == 913 and review.get("meta_reduced_record_count_preserved") is True,
        "selected_method_path_label_objective_redesign": review.get("selected_method_path") == candidate_service.SELECTED_METHOD_PATH,
        "label_objective_redesign_candidate_created_true": review.get("label_objective_redesign_candidate_created") is True,
        "label_objective_redesign_candidate_review_created_true": review.get("label_objective_redesign_candidate_review_created") is True,
        "label_objective_redesign_ready_for_operator_review_true": review.get("label_objective_redesign_ready_for_operator_review") is True,
        "label_objective_redesign_not_approved": review.get("label_objective_redesign_approved") is False,
        "label_objective_redesign_not_authorized": review.get("label_objective_redesign_authorized") is False,
        "label_objective_redesign_not_executed": review.get("label_objective_redesign_executed") is False,
        "redesigned_label_generation_not_authorized": review.get("redesigned_label_generation_authorized") is False,
        "redesigned_label_generation_not_performed": review.get("redesigned_label_generation_performed") is False,
        "hypotheses_reviewed": [item.get("hypothesis_id") for item in review.get("reviewed_diagnostic_hypotheses", []) if isinstance(item, dict)] == candidate_service.DIAGNOSTIC_HYPOTHESES,
        "redesign_dimensions_reviewed": [item.get("dimension_id") for item in review.get("reviewed_redesign_dimensions", []) if isinstance(item, dict)] == candidate_service.REDESIGN_DIMENSIONS,
        "label_family_candidates_reviewed": [item.get("label_family_candidate_id") for item in review.get("reviewed_label_family_candidates", []) if isinstance(item, dict)] == candidate_service.LABEL_FAMILY_CANDIDATES,
        "evaluation_questions_reviewed": [item.get("question_id") for item in review.get("reviewed_evaluation_questions", []) if isinstance(item, dict)] == candidate_service.EVALUATION_QUESTIONS,
        "per_ticker_entries_12": isinstance(entries, list) and len(entries) == 12 and [item.get("ticker") for item in entries if isinstance(item, dict)] == TARGET_UNIVERSE,
        "per_ticker_candidate_digests_present": isinstance(entries, list) and len(entries) == 12 and all(isinstance(item.get("per_ticker_label_objective_redesign_candidate_digest"), str) and len(item["per_ticker_label_objective_redesign_candidate_digest"]) == 64 for item in entries if isinstance(item, dict)),
        "per_ticker_review_digests_present": isinstance(entries, list) and len(entries) == 12 and all(isinstance(item.get("per_ticker_label_objective_redesign_candidate_review_digest"), str) and len(item["per_ticker_label_objective_redesign_candidate_review_digest"]) == 64 and item["per_ticker_label_objective_redesign_candidate_review_digest"] == per_ticker_label_objective_redesign_candidate_review_digest_v1(item) for item in entries if isinstance(item, dict)),
        "future_chain_reviewed": review.get("reviewed_future_chain") == candidate_service.FUTURE_CHAIN,
        "future_gates_reviewed": review.get("reviewed_future_gates") == candidate_service.FUTURE_GATES,
        "risk_controls_reviewed": review.get("reviewed_risk_controls") == candidate_service.RISK_CONTROLS,
        "planned_outputs_not_generated": isinstance(outputs, list) and len(outputs) == len(candidate_service.PLANNED_OUTPUTS) and all(item.get("output_status") == "PLANNED_NOT_GENERATED" for item in outputs if isinstance(item, dict)),
        "planned_outputs_research_only": isinstance(outputs, list) and len(outputs) == len(candidate_service.PLANNED_OUTPUTS) and all(item.get("authority") == candidate_service.RESEARCH_ONLY_NON_ACTIONABLE for item in outputs if isinstance(item, dict)),
        "predictive_usefulness_not_accepted": review.get("predictive_usefulness") == NOT_ACCEPTED,
        "profitability_not_accepted": review.get("profitability") == NOT_ACCEPTED,
        "runtime_not_authorized": review.get("runtime_migration_approved") is False and review.get("runtime_migration_active") is False and review.get("runtime_use") == NOT_AUTHORIZED,
        "strategy_not_authorized": review.get("strategy_use") == NOT_AUTHORIZED,
        "broker_not_authorized": review.get("paper_trading") == NOT_AUTHORIZED and review.get("broker_execution") == NOT_AUTHORIZED,
        "trade_recommendations_false": review.get("trade_recommendations_generated") is False,
        "provider_requests_made_false": review.get("provider_requests_made") is False,
        "market_data_acquisition_false": review.get("market_data_acquisition_performed") is False,
        "dataset_regeneration_false": review.get("dataset_regeneration_performed") is False,
        "label_generation_false": review.get("label_generation_performed") is False and review.get("redesigned_label_generation_performed") is False,
        "feature_generation_false": review.get("feature_generation_performed") is False and review.get("redesigned_feature_generation_performed") is False,
        "metric_recomputation_false": review.get("metric_recomputation_performed") is False,
        "model_training_false": review.get("model_training_performed") is False,
        "strategy_scoring_false": review.get("new_strategy_scoring_performed") is False,
        "runtime_activation_false": review.get("runtime_migration_active") is False,
        "no_label_objective_redesign_approval_created": review.get("label_objective_redesign_approval_created") is False,
        "no_label_objective_redesign_execution_created": review.get("label_objective_redesign_execution_created") is False,
        "no_additional_predictive_evidence_execution_candidate_created": review.get("additional_predictive_evidence_execution_candidate_created") is False,
        "no_predictive_usefulness_acceptance_artifact_created": review.get("predictive_usefulness_acceptance_artifact_created") is False,
        "no_profitability_acceptance_created": review.get("profitability_acceptance_created") is False,
        "no_runtime_migration_approval_created": review.get("runtime_migration_approval_created") is False,
        "no_tracked_marketflow_files": review.get("no_tracked_marketflow_files") is True and review.get("tracked_marketflow_files") == [],
    }


def _checklist(review: dict[str, Any]) -> list[dict[str, Any]]:
    checks = _derived_checks(review)
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
        "ready_for_operator_assessment": blockers == 0,
        "ready_for_label_objective_redesign_approval": False,
        "ready_for_label_objective_redesign_execution": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_authorized": False,
        "trade_recommendations_generated": False,
    }


def _digest_payload(review: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(review)
    payload.pop("label_objective_redesign_candidate_review_package_digest", None)
    return payload


def label_objective_redesign_candidate_review_package_digest_v1(
    review_package: dict[str, Any],
) -> str:
    """Return the deterministic review-package digest."""
    return semantic_digest(_digest_payload(review_package))


def build_label_objective_redesign_candidate_review_package_v1(
    candidate: dict | None = None,
) -> dict:
    """Build a non-authorizing review of the exact redesign candidate."""
    source = _source_candidate(candidate)
    review = _base_review(source)
    review["review_checklist"] = _checklist(review)
    review["review_summary"] = _summary(review["review_checklist"])
    review["label_objective_redesign_candidate_review_package_digest"] = (
        label_objective_redesign_candidate_review_package_digest_v1(review)
    )
    validate_label_objective_redesign_candidate_review_package_v1(review)
    return review


def _reject_forbidden_authority(value: Any, *, path: str = "review_package") -> None:
    forbidden_true_fields = {
        "label_objective_redesign_approved",
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
        "label_objective_redesign_approval_created",
        "label_objective_redesign_execution_created",
        "predictive_usefulness_acceptance_artifact_created",
        "profitability_acceptance_created",
        "runtime_migration_approval_created",
    }
    if isinstance(value, dict):
        for key, item in value.items():
            current = f"{path}.{key}"
            if key in forbidden_true_fields and item is True:
                raise LabelObjectiveRedesignCandidateReviewError(
                    f"{current} must remain false"
                )
            if key in {
                "runtime_use",
                "strategy_use",
                "paper_trading",
                "broker_execution",
            } and item == "AUTHORIZED":
                raise LabelObjectiveRedesignCandidateReviewError(
                    f"{current} must not be AUTHORIZED"
                )
            if key in {"predictive_usefulness", "profitability"} and item == "accepted":
                raise LabelObjectiveRedesignCandidateReviewError(
                    f"{current} must not be accepted"
                )
            _reject_forbidden_authority(item, path=current)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _reject_forbidden_authority(item, path=f"{path}[{index}]")


def validate_label_objective_redesign_candidate_review_package_v1(
    review_package: dict,
) -> dict:
    """Validate exact source evidence and all closed downstream authorities."""
    if not isinstance(review_package, dict):
        raise LabelObjectiveRedesignCandidateReviewError(
            "review package must be a JSON object"
        )
    _reject_forbidden_authority(review_package)
    expected_base = _base_review(_source_candidate(None))
    for field, expected in expected_base.items():
        _expect(review_package.get(field), expected, field)
    checklist = review_package.get("review_checklist")
    if not isinstance(checklist, list):
        raise LabelObjectiveRedesignCandidateReviewError("review_checklist missing")
    _expect(
        [item.get("check_id") for item in checklist if isinstance(item, dict)],
        CHECK_IDS,
        "review_checklist check IDs",
    )
    expected_checklist = _checklist(review_package)
    _expect(checklist, expected_checklist, "review_checklist")
    if any(item["status"] != PASS for item in expected_checklist):
        raise LabelObjectiveRedesignCandidateReviewError(
            "review_checklist contains a failed check"
        )
    expected_summary = _summary(expected_checklist)
    _expect(review_package.get("review_summary"), expected_summary, "review_summary")
    digest = review_package.get(
        "label_objective_redesign_candidate_review_package_digest"
    )
    if not isinstance(digest, str) or len(digest) != 64:
        raise LabelObjectiveRedesignCandidateReviewError(
            "label objective redesign candidate review package digest missing"
        )
    _expect(
        digest,
        label_objective_redesign_candidate_review_package_digest_v1(review_package),
        "label_objective_redesign_candidate_review_package_digest",
    )
    return {
        "status": "LABEL_OBJECTIVE_REDESIGN_CANDIDATE_REVIEW_PACKAGE_VALID",
        "artifact_kind": review_package["artifact_kind"],
        "review_status": review_package["review_status"],
        "label_objective_redesign_candidate_review_package_digest": digest,
        "reviewed_label_objective_redesign_candidate_digest": EXPECTED_CANDIDATE_DIGEST,
        "ready_for_operator_assessment": True,
        "ready_for_label_objective_redesign_approval": False,
        "ready_for_label_objective_redesign_execution": False,
        "blocker_count": expected_summary["blocker_count"],
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED,
    }


def build_label_objective_redesign_candidate_review_markdown_v1(
    review_package: dict,
) -> str:
    """Render a validated, non-actionable review summary."""
    validate_label_objective_redesign_candidate_review_package_v1(review_package)
    summary = review_package["review_summary"]
    lines = [
        "# MarketFlow Label Objective Redesign Candidate Review Package",
        "",
        "## Title",
        "- Label Objective Redesign Candidate Operator Review Package v1.",
        "",
        "## Label Objective Redesign Candidate Review Package",
        f"- Artifact/status: `{review_package['artifact_kind']}` / `{review_package['review_status']}`.",
        "",
        "## Reviewed Candidate",
        f"- Kind/status: `{review_package['reviewed_label_objective_redesign_candidate_kind']}` / `{review_package['reviewed_label_objective_redesign_candidate_status']}`.",
        f"- Digest: `{review_package['reviewed_label_objective_redesign_candidate_digest']}`.",
        "- Candidate checklist: `44 / 44` passed; `0` blockers.",
        "",
        "## Bound Evidence",
    ]
    lines.extend(
        f"- {field}: `{review_package[field]}`."
        for field in REQUIRED_DIGEST_FIELDS
    )
    lines.extend(
        [
            "",
            "## Dataset and Universe",
            f"- Dataset: `{review_package['dataset_name']}`; records: `{review_package['total_canonical_record_count']}`.",
            f"- Universe: `{', '.join(review_package['target_universe'])}`; META records: `{review_package['meta_record_count']}`.",
            "",
            "## Problem Basis",
        ]
    )
    lines.extend(
        f"- {key}: `{value}`."
        for key, value in review_package["problem_basis"].items()
    )
    for heading, key, id_key in [
        ("Reviewed Diagnostic Hypotheses", "reviewed_diagnostic_hypotheses", "hypothesis_id"),
        ("Reviewed Redesign Dimensions", "reviewed_redesign_dimensions", "dimension_id"),
        ("Reviewed Label Family Candidates", "reviewed_label_family_candidates", "label_family_candidate_id"),
        ("Reviewed Evaluation Questions", "reviewed_evaluation_questions", "question_id"),
    ]:
        lines.extend(["", f"## {heading}"])
        lines.extend(f"- `{item[id_key]}`." for item in review_package[key])
    lines.extend(["", "## Per-Ticker Review Entries"])
    lines.extend(
        f"- `{item['ticker']}`: `{item['historical_record_count']}` records; review ready, redesign not authorized."
        for item in review_package["per_ticker_review_entries"]
    )
    for heading, key in [
        ("Future Chain", "reviewed_future_chain"),
        ("Future Gates", "reviewed_future_gates"),
        ("Risk Controls", "reviewed_risk_controls"),
    ]:
        lines.extend(["", f"## {heading}"])
        lines.extend(f"- {item}" for item in review_package[key])
    lines.extend(
        [
            "",
            "## Checklist Summary",
            f"- `{summary['passed_checks']} / {summary['total_checks']}` passed; `{summary['blocker_count']}` blockers.",
            "",
            "## Guardrails",
            "- Review only; no redesign approval, execution, label or feature generation, predictive acceptance, profitability acceptance, runtime, trading, or recommendations.",
        ]
    )
    return "\n".join(lines)


def write_label_objective_redesign_candidate_review_package_v1(
    output_dir: str | Path,
    *,
    candidate: dict | None = None,
    filename: str | None = None,
) -> dict:
    """Write one canonical review package without overwriting."""
    review = build_label_objective_redesign_candidate_review_package_v1(candidate)
    validation = validate_label_objective_redesign_candidate_review_package_v1(
        review
    )
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    output_name = (
        filename or "label_objective_redesign_candidate_review_package_v1.json"
    )
    if Path(output_name).name != output_name or not output_name.endswith(".json"):
        raise LabelObjectiveRedesignCandidateReviewError(
            "review package filename must be a simple JSON filename"
        )
    path = directory / output_name
    if path.exists():
        raise LabelObjectiveRedesignCandidateReviewError(
            "review package output already exists"
        )
    payload = canonical_json_bytes(review)
    with path.open("xb") as handle:
        handle.write(payload)
    return validation | {
        "path": str(path).replace("\\", "/"),
        "filename": path.name,
        "payload_byte_size": len(payload),
        "payload_sha256": sha256_bytes(payload),
    }
