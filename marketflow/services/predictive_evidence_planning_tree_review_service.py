"""Offline review of the predictive-evidence planning tree (not authority)."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from marketflow.historical_data.artifacts import (
    canonical_json_bytes,
    semantic_digest,
    sha256_bytes,
)
from marketflow.services import (
    predictive_usefulness_acceptance_readiness_review_rerun_using_refined_evidence_service as latest_readiness,
)


ARTIFACT_KIND_PREDICTIVE_EVIDENCE_PLANNING_TREE_REVIEW_PACKAGE = (
    "PREDICTIVE_EVIDENCE_PLANNING_TREE_REVIEW_PACKAGE"
)
SCHEMA_VERSION_PREDICTIVE_EVIDENCE_PLANNING_TREE_REVIEW_V1 = (
    "predictive_evidence_planning_tree_review_v1"
)
PREDICTIVE_EVIDENCE_PLANNING_TREE_REVIEW_PACKAGE_READY = (
    "PREDICTIVE_EVIDENCE_PLANNING_TREE_REVIEW_PACKAGE_READY"
)

EXPECTED_LATEST_READINESS_DIGEST = (
    "1b7e9d447290330cbecb70ec5897791d51d187886ab9a8145e6ecaf0f61c2991"
)
EXPECTED_REFINED_REASSESSMENT_DIGEST = (
    "7520cd1c2f8d727ad7e94c0313c78e8bbb39bae410feeda539dd242ede28fcc0"
)
EXPECTED_REFINED_RESULTS_REVIEW_DIGEST = (
    "539d06be9b20edee5ff883030e4fd1091fdaefb468fa595001178bf7ec0740da"
)
EXPECTED_REFINED_EXECUTION_DIGEST = (
    "9cf962933620f066dfb105845428a262743f9f36dbc2850838321f23de10b5fd"
)
EXPECTED_FEATURE_LABEL_REFINEMENT_RESULTS_REVIEW_DIGEST = (
    "00604008d3c647f45896cd8b6707de519ed6eda4e32566b3c99910441ec6cc79"
)
EXPECTED_FEATURE_LABEL_REFINEMENT_EXECUTION_DIGEST = (
    "377d6d232dcdf4b94f9f2d66414ff994edca2d3d9d95f4fb97d9dbfaf2359b36"
)
EXPECTED_ORIGINAL_READINESS_DIGEST = (
    "d4ea4dc23590d9746727d5028116e2d0711fbc55dc8853f0b455d6ee4344a3e3"
)
EXPECTED_ORIGINAL_REASSESSMENT_DIGEST = (
    "71a1456fdef4ed9845c1a5264bc56eb9e362e43e88f2316d6700efe2d6f2bfab"
)
EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST = (
    "5f0ce29bd06f1a0d5f1ce3dd8e31b8c8e52d616673f119326377538228d3d958"
)
EXPECTED_RECORDS_DIGEST = (
    "fbd7c1b17b42e5d4f82a9162b31b45fdfeef46f0e9ee7d29d74c926f0cf19044"
)
EXPECTED_ORIGINAL_RESULTS_REVIEW_DIGEST = (
    "167a0399e99f46e895c9cdf6c70a3e650e20f60cb78641180de04e56f88caee8"
)
EXPECTED_ORIGINAL_EXECUTION_DIGEST = (
    "61a90d0b863da3ddfc3ef8eb744a1ef64c476a975d83faa2be19d0f199776ed3"
)

TARGET_UNIVERSE = list(latest_readiness.TARGET_UNIVERSE)
EXPECTED_RECORD_COUNTS = dict(latest_readiness.EXPECTED_RECORD_COUNTS)
REGISTRY_APPROVED_DATASET_METADATA = deepcopy(
    latest_readiness.REGISTRY_APPROVED_DATASET_METADATA
)
NOT_ACCEPTED = latest_readiness.NOT_ACCEPTED
NOT_AUTHORIZED = latest_readiness.NOT_AUTHORIZED

PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"
RESEARCH_ONLY_NON_ACTIONABLE = "RESEARCH_ONLY_NON_ACTIONABLE"
NOT_ALLOWED_CURRENTLY = "NOT_ALLOWED_CURRENTLY"
AVAILABLE_FOR_PLANNING_REVIEW = "AVAILABLE_FOR_PLANNING_REVIEW"
RECOMMENDED_NEXT_OPTION = "OPTION_B_METHOD_DIAGNOSTIC_REVIEW"
RECOMMENDATION_REASON = (
    "TWO_CONSECUTIVE_READINESS_GATES_NOT_READY_AFTER_ORIGINAL_AND_REFINED_EVIDENCE"
)
ORIGINAL_READINESS_DECISION = "PREDICTIVE_USEFULNESS_ACCEPTANCE_NOT_READY"
REFINED_READINESS_DECISION = (
    "PREDICTIVE_USEFULNESS_ACCEPTANCE_NOT_READY_USING_REFINED_EVIDENCE"
)

OPTION_IDS = [
    "OPTION_A_PAUSE_AND_ARCHIVE_RESEARCH_CHAIN",
    "OPTION_B_METHOD_DIAGNOSTIC_REVIEW",
    "OPTION_C_LABEL_OBJECTIVE_REDESIGN_CANDIDATE",
    "OPTION_D_FEATURE_METHOD_REDESIGN_CANDIDATE",
    "OPTION_E_DATA_SCOPE_EXPANSION_CANDIDATE",
    "OPTION_F_NEW_MODELING_APPROACH_CANDIDATE",
    "OPTION_G_ACCEPTANCE_CANDIDATE",
]

RISK_CONTROLS = [
    "no_acceptance_after_failed_readiness",
    "no_runtime_activation",
    "no_strategy_scoring",
    "no_trade_recommendations",
    "no_broker_execution",
    "no_paper_trading",
    "no_more_execution_without_new_review",
    "preserve_frozen_dataset",
    "preserve_meta_record_limitation",
    "research_outputs_non_actionable",
    "operator_review_required_for_any_new_path",
]

REQUIRED_DIGEST_FIELDS = {
    "predictive_usefulness_acceptance_readiness_review_rerun_using_refined_evidence_digest": EXPECTED_LATEST_READINESS_DIGEST,
    "predictive_usefulness_reassessment_review_rerun_using_refined_evidence_digest": EXPECTED_REFINED_REASSESSMENT_DIGEST,
    "additional_predictive_evidence_results_review_for_refined_evidence_digest": EXPECTED_REFINED_RESULTS_REVIEW_DIGEST,
    "additional_predictive_evidence_execution_for_refined_evidence_digest": EXPECTED_REFINED_EXECUTION_DIGEST,
    "feature_label_refinement_results_review_digest": EXPECTED_FEATURE_LABEL_REFINEMENT_RESULTS_REVIEW_DIGEST,
    "feature_label_refinement_execution_digest": EXPECTED_FEATURE_LABEL_REFINEMENT_EXECUTION_DIGEST,
    "original_predictive_usefulness_acceptance_readiness_review_digest": EXPECTED_ORIGINAL_READINESS_DIGEST,
    "original_predictive_usefulness_reassessment_review_digest": EXPECTED_ORIGINAL_REASSESSMENT_DIGEST,
    "research_registry_approval_digest": EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST,
    "records_digest": EXPECTED_RECORDS_DIGEST,
}

CHECK_IDS = [
    "all_required_digests_bound",
    "target_universe_12_preserved",
    "records_digest_preserved",
    "meta_913_preserved",
    "original_readiness_not_ready_bound",
    "refined_readiness_not_ready_bound",
    "predictive_usefulness_not_accepted",
    "profitability_not_accepted",
    "runtime_not_authorized",
    "strategy_not_authorized",
    "broker_not_authorized",
    "trade_recommendations_false",
    "options_defined",
    "acceptance_option_not_allowed",
    "method_diagnostic_review_recommended",
    "no_provider_requests",
    "no_market_data_acquisition",
    "no_dataset_regeneration",
    "no_predictive_rerun",
    "no_metric_recomputation",
    "no_runtime_activation",
    "no_tracked_marketflow_files",
]


class PredictiveEvidencePlanningTreeReviewError(ValueError):
    """Raised when a planning-tree review violates its closed-authority scope."""


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise PredictiveEvidencePlanningTreeReviewError(f"{field} mismatch")


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


def _planning_tree_sections() -> list[dict[str, Any]]:
    return [
        {
            "section_id": "research_registry_and_canonical_dataset_state",
            "status": "COMPLETED_RESEARCH_REGISTRY_ONLY",
            "summary": "The frozen canonical dataset is approved only for the research registry.",
            "bound_digests": [
                EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST,
                EXPECTED_RECORDS_DIGEST,
            ],
        },
        {
            "section_id": "original_additional_predictive_evidence_execution",
            "status": "COMPLETED_RESEARCH_ONLY",
            "summary": "The original evidence execution and results review completed without acceptance authority.",
            "bound_digests": [
                EXPECTED_ORIGINAL_EXECUTION_DIGEST,
                EXPECTED_ORIGINAL_RESULTS_REVIEW_DIGEST,
            ],
        },
        {
            "section_id": "original_predictive_usefulness_reassessment",
            "status": "COMPLETED_RESEARCH_ONLY",
            "summary": "The original reassessment remained research-only and not acceptance evidence.",
            "bound_digests": [EXPECTED_ORIGINAL_REASSESSMENT_DIGEST],
        },
        {
            "section_id": "original_acceptance_readiness_decision",
            "status": ORIGINAL_READINESS_DECISION,
            "summary": "The original readiness gate did not permit acceptance.",
            "bound_digests": [EXPECTED_ORIGINAL_READINESS_DIGEST],
        },
        {
            "section_id": "predictive_evidence_improvement_candidate_chain",
            "status": "COMPLETED_PLANNING_AND_REVIEW_CHAIN",
            "summary": "The improvement candidate chain planned refinements but created no execution or acceptance authority.",
            "bound_digests": [EXPECTED_ORIGINAL_READINESS_DIGEST],
        },
        {
            "section_id": "feature_label_refinement_chain",
            "status": "COMPLETED_RESEARCH_ONLY",
            "summary": "Feature and label planning, approval, execution, and results review completed as research-only evidence work.",
            "bound_digests": [
                EXPECTED_FEATURE_LABEL_REFINEMENT_EXECUTION_DIGEST,
                EXPECTED_FEATURE_LABEL_REFINEMENT_RESULTS_REVIEW_DIGEST,
            ],
        },
        {
            "section_id": "refined_additional_predictive_evidence_chain",
            "status": "COMPLETED_RESEARCH_ONLY",
            "summary": "The refined candidate, approval, execution, and results review remained non-actionable research.",
            "bound_digests": [
                EXPECTED_REFINED_EXECUTION_DIGEST,
                EXPECTED_REFINED_RESULTS_REVIEW_DIGEST,
            ],
        },
        {
            "section_id": "predictive_usefulness_reassessment_rerun_using_refined_evidence",
            "status": "COMPLETED_RESEARCH_ONLY",
            "summary": "The reassessment rerun classified the refined signal as weak or mixed.",
            "bound_digests": [EXPECTED_REFINED_REASSESSMENT_DIGEST],
        },
        {
            "section_id": "acceptance_readiness_rerun_using_refined_evidence",
            "status": REFINED_READINESS_DECISION,
            "summary": "The refined readiness gate also did not permit acceptance.",
            "bound_digests": [EXPECTED_LATEST_READINESS_DIGEST],
        },
        {
            "section_id": "final_decision_state",
            "status": "NOT_ACCEPTED",
            "summary": "Predictive usefulness and profitability remain not accepted; runtime remains unauthorized.",
            "bound_digests": [EXPECTED_LATEST_READINESS_DIGEST],
        },
        {
            "section_id": "current_blocked_downstream_authorities",
            "status": "ALL_DOWNSTREAM_AUTHORITIES_CLOSED",
            "summary": "Acceptance, profitability, runtime, strategy, paper, broker, and recommendations remain closed.",
            "bound_digests": [],
        },
        {
            "section_id": "recommended_next_planning_options",
            "status": "METHOD_DIAGNOSTIC_REVIEW_RECOMMENDED",
            "summary": "Review methodology before considering any additional evidence execution loop.",
            "bound_digests": [
                EXPECTED_ORIGINAL_READINESS_DIGEST,
                EXPECTED_LATEST_READINESS_DIGEST,
            ],
        },
    ]


def _recommended_options() -> list[dict[str, Any]]:
    return [
        {
            "option_id": option_id,
            "status": (
                NOT_ALLOWED_CURRENTLY
                if option_id == "OPTION_G_ACCEPTANCE_CANDIDATE"
                else AVAILABLE_FOR_PLANNING_REVIEW
            ),
            "recommended_immediately": option_id == RECOMMENDED_NEXT_OPTION,
            "authority": "NON_AUTHORIZING_PLANNING_OPTION_ONLY",
            "execution_authorized": False,
        }
        for option_id in OPTION_IDS
    ]


def _base_package() -> dict[str, Any]:
    package: dict[str, Any] = {
        "artifact_kind": ARTIFACT_KIND_PREDICTIVE_EVIDENCE_PLANNING_TREE_REVIEW_PACKAGE,
        "schema_version": SCHEMA_VERSION_PREDICTIVE_EVIDENCE_PLANNING_TREE_REVIEW_V1,
        "review_status": PREDICTIVE_EVIDENCE_PLANNING_TREE_REVIEW_PACKAGE_READY,
        "created_offline": True,
        "research_only": True,
        "operator_review_required": True,
        "planning_tree_review_created": True,
        "planning_tree_review_ready": True,
        "provider_requests_made_in_review": False,
        "live_provider_transport_enabled_in_review": False,
        "market_data_acquisition_performed_in_review": False,
        "dataset_regeneration_performed_in_review": False,
        "predictive_evidence_rerun_performed": False,
        "refined_evidence_rerun_performed": False,
        "label_generation_rerun_performed": False,
        "feature_generation_rerun_performed": False,
        "metrics_recomputation_performed": False,
        "new_strategy_scoring_performed": False,
        "trade_recommendations_generated": False,
        "runtime_migration_approved": False,
        "runtime_migration_active": False,
        "automatic_stitching": False,
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "predictive_usefulness_acceptance_candidate_created": False,
        "profitability_acceptance_created": False,
        "runtime_migration_approval_created": False,
        "tracked_marketflow_files": [],
        "no_tracked_marketflow_files": True,
        **REQUIRED_DIGEST_FIELDS,
        "original_additional_predictive_evidence_results_review_digest": EXPECTED_ORIGINAL_RESULTS_REVIEW_DIGEST,
        "original_additional_predictive_evidence_execution_digest": EXPECTED_ORIGINAL_EXECUTION_DIGEST,
        "target_universe": list(TARGET_UNIVERSE),
        "target_universe_count": 12,
        "per_ticker_record_counts": dict(EXPECTED_RECORD_COUNTS),
        "total_canonical_record_count": 11946,
        "meta_record_count": 913,
        "non_meta_record_count": 1003,
        "meta_reduced_record_count_preserved": True,
        "registry_approved_dataset_metadata": deepcopy(
            REGISTRY_APPROVED_DATASET_METADATA
        ),
        "planning_tree_sections": _planning_tree_sections(),
        "original_evidence_cycle": {
            "additional_predictive_evidence_execution_status": "COMPLETED_RESEARCH_ONLY",
            "predictive_usefulness_reassessment_status": "COMPLETED_RESEARCH_ONLY",
            "readiness_decision": ORIGINAL_READINESS_DECISION,
            "predictive_usefulness_accepted": False,
        },
        "refined_evidence_cycle": {
            "feature_label_refinement_status": "COMPLETED_RESEARCH_ONLY",
            "additional_predictive_evidence_status": "COMPLETED_RESEARCH_ONLY",
            "predictive_usefulness_reassessment_status": "COMPLETED_RESEARCH_ONLY",
            "readiness_decision": REFINED_READINESS_DECISION,
            "predictive_usefulness_accepted": False,
        },
        "original_readiness_decision": ORIGINAL_READINESS_DECISION,
        "refined_readiness_decision": REFINED_READINESS_DECISION,
        "final_predictive_usefulness_state": NOT_ACCEPTED,
        "final_profitability_state": NOT_ACCEPTED,
        "final_runtime_state": NOT_AUTHORIZED,
        "final_decision_summary": {
            "original_readiness_decision": ORIGINAL_READINESS_DECISION,
            "refined_readiness_decision": REFINED_READINESS_DECISION,
            "final_predictive_usefulness_state": NOT_ACCEPTED,
            "final_profitability_state": NOT_ACCEPTED,
            "final_runtime_state": NOT_AUTHORIZED,
        },
        "key_evidence_comparison": {
            "original_oos_majority_accuracy": "0.539491",
            "original_oos_previous_direction_accuracy": "0.495984",
            "original_oos_ticker_cross_sectional_accuracy": "0.502677",
            "original_oos_brier_score": "0.24875351",
            "refined_oos_accuracy_range": "0.119813 to 0.480924",
            "refined_signal_consistency": "WEAK_OR_MIXED",
            "refined_baseline_outperformance": "INSUFFICIENT_OR_MIXED",
            "refined_model_comparison": "RESEARCH_ONLY_NOT_ACCEPTANCE_EVIDENCE",
        },
        "refined_evidence_did_not_create_acceptance_readiness": True,
        "additional_improvement_loop_not_automatically_recommended": True,
        "methodology_review_recommended_before_more_execution": True,
        "recommended_next_options": _recommended_options(),
        "recommended_next_option": RECOMMENDED_NEXT_OPTION,
        "recommended_next_option_reason": RECOMMENDATION_REASON,
        "blocked_downstream_authorities": {
            "predictive_usefulness_acceptance": "BLOCKED_NOT_READY",
            "profitability_acceptance": "BLOCKED_REQUIRES_SEPARATE_REVIEW",
            "runtime_migration": NOT_AUTHORIZED,
            "strategy_use": NOT_AUTHORIZED,
            "paper_trading": NOT_AUTHORIZED,
            "broker_execution": NOT_AUTHORIZED,
            "trade_recommendations": NOT_AUTHORIZED,
        },
        "risk_controls": list(RISK_CONTROLS),
    }
    return package


def _derived_checks(package: dict[str, Any]) -> dict[str, Any]:
    options = package.get("recommended_next_options", [])
    option_map = {
        item.get("option_id"): item
        for item in options
        if isinstance(item, dict)
    } if isinstance(options, list) else {}
    return {
        "all_required_digests_bound": all(
            package.get(field) == expected
            for field, expected in REQUIRED_DIGEST_FIELDS.items()
        ),
        "target_universe_12_preserved": package.get("target_universe_count") == 12
        and package.get("target_universe") == TARGET_UNIVERSE,
        "records_digest_preserved": package.get("records_digest")
        == EXPECTED_RECORDS_DIGEST,
        "meta_913_preserved": package.get("meta_record_count") == 913
        and package.get("per_ticker_record_counts", {}).get("META") == 913,
        "original_readiness_not_ready_bound": package.get(
            "original_readiness_decision"
        )
        == ORIGINAL_READINESS_DECISION,
        "refined_readiness_not_ready_bound": package.get(
            "refined_readiness_decision"
        )
        == REFINED_READINESS_DECISION,
        "predictive_usefulness_not_accepted": package.get("predictive_usefulness")
        == NOT_ACCEPTED,
        "profitability_not_accepted": package.get("profitability")
        == NOT_ACCEPTED,
        "runtime_not_authorized": package.get("runtime_use") == NOT_AUTHORIZED,
        "strategy_not_authorized": package.get("strategy_use") == NOT_AUTHORIZED,
        "broker_not_authorized": package.get("broker_execution")
        == NOT_AUTHORIZED,
        "trade_recommendations_false": package.get(
            "trade_recommendations_generated"
        )
        is False,
        "options_defined": list(option_map) == OPTION_IDS,
        "acceptance_option_not_allowed": option_map.get(
            "OPTION_G_ACCEPTANCE_CANDIDATE", {}
        ).get("status")
        == NOT_ALLOWED_CURRENTLY,
        "method_diagnostic_review_recommended": package.get(
            "recommended_next_option"
        )
        == RECOMMENDED_NEXT_OPTION,
        "no_provider_requests": package.get("provider_requests_made_in_review")
        is False,
        "no_market_data_acquisition": package.get(
            "market_data_acquisition_performed_in_review"
        )
        is False,
        "no_dataset_regeneration": package.get(
            "dataset_regeneration_performed_in_review"
        )
        is False,
        "no_predictive_rerun": package.get("predictive_evidence_rerun_performed")
        is False
        and package.get("refined_evidence_rerun_performed") is False,
        "no_metric_recomputation": package.get("metrics_recomputation_performed")
        is False,
        "no_runtime_activation": package.get("runtime_migration_approved") is False
        and package.get("runtime_migration_active") is False,
        "no_tracked_marketflow_files": package.get("no_tracked_marketflow_files")
        is True
        and package.get("tracked_marketflow_files") == [],
    }


def _checklist(package: dict[str, Any]) -> list[dict[str, Any]]:
    derived = _derived_checks(package)
    return [_check(check_id, True, derived.get(check_id)) for check_id in CHECK_IDS]


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
        "planning_tree_review_ready": blockers == 0,
        "recommended_next_option": RECOMMENDED_NEXT_OPTION,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_authorized": False,
        "trade_recommendations_generated": False,
    }


def _digest_payload(package: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(package)
    payload.pop("predictive_evidence_planning_tree_review_package_digest", None)
    return payload


def predictive_evidence_planning_tree_review_package_digest_v1(
    package: dict[str, Any],
) -> str:
    """Return the deterministic semantic digest for the review package."""
    return semantic_digest(_digest_payload(package))


def build_predictive_evidence_planning_tree_review_package_v1() -> dict:
    """Build the offline, non-authorizing planning-tree review package."""
    package = _base_package()
    package["review_checklist"] = _checklist(package)
    package["review_summary"] = _summary(package["review_checklist"])
    package["predictive_evidence_planning_tree_review_package_digest"] = (
        predictive_evidence_planning_tree_review_package_digest_v1(package)
    )
    validate_predictive_evidence_planning_tree_review_package_v1(package)
    return package


def _reject_forbidden_authority(value: Any, *, path: str = "package") -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            current = f"{path}.{key}"
            if key in {
                "provider_requests_made_in_review",
                "live_provider_transport_enabled_in_review",
                "market_data_acquisition_performed_in_review",
                "dataset_regeneration_performed_in_review",
                "predictive_evidence_rerun_performed",
                "refined_evidence_rerun_performed",
                "label_generation_rerun_performed",
                "feature_generation_rerun_performed",
                "metrics_recomputation_performed",
                "new_strategy_scoring_performed",
                "trade_recommendations_generated",
                "runtime_migration_approved",
                "runtime_migration_active",
                "automatic_stitching",
                "predictive_usefulness_acceptance_candidate_created",
                "profitability_acceptance_created",
                "runtime_migration_approval_created",
                "execution_authorized",
            } and item is True:
                raise PredictiveEvidencePlanningTreeReviewError(
                    f"{current} must remain false"
                )
            if key in {
                "runtime_use",
                "strategy_use",
                "paper_trading",
                "broker_execution",
            } and item == "AUTHORIZED":
                raise PredictiveEvidencePlanningTreeReviewError(
                    f"{current} must not be AUTHORIZED"
                )
            if key in {
                "predictive_usefulness",
                "profitability",
                "final_predictive_usefulness_state",
                "final_profitability_state",
            } and item == "accepted":
                raise PredictiveEvidencePlanningTreeReviewError(
                    f"{current} must not be accepted"
                )
            _reject_forbidden_authority(item, path=current)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _reject_forbidden_authority(item, path=f"{path}[{index}]")


def validate_predictive_evidence_planning_tree_review_package_v1(
    package: dict,
) -> dict:
    """Validate exact evidence binding and reject any implied new authority."""
    if not isinstance(package, dict):
        raise PredictiveEvidencePlanningTreeReviewError(
            "planning-tree review package must be a JSON object"
        )
    _reject_forbidden_authority(package)
    expected_base = _base_package()
    for field, expected in expected_base.items():
        _expect(package.get(field), expected, field)
    checklist = package.get("review_checklist")
    if not isinstance(checklist, list):
        raise PredictiveEvidencePlanningTreeReviewError("review_checklist missing")
    _expect(
        [item.get("check_id") for item in checklist if isinstance(item, dict)],
        CHECK_IDS,
        "review_checklist check IDs",
    )
    expected_checklist = _checklist(package)
    _expect(checklist, expected_checklist, "review_checklist")
    if any(item["status"] != PASS for item in expected_checklist):
        raise PredictiveEvidencePlanningTreeReviewError(
            "review_checklist contains a failed check"
        )
    expected_summary = _summary(expected_checklist)
    _expect(package.get("review_summary"), expected_summary, "review_summary")
    digest = package.get("predictive_evidence_planning_tree_review_package_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise PredictiveEvidencePlanningTreeReviewError(
            "predictive evidence planning-tree review package digest missing"
        )
    _expect(
        digest,
        predictive_evidence_planning_tree_review_package_digest_v1(package),
        "predictive_evidence_planning_tree_review_package_digest",
    )
    return {
        "status": "PREDICTIVE_EVIDENCE_PLANNING_TREE_REVIEW_PACKAGE_VALID",
        "artifact_kind": package["artifact_kind"],
        "review_status": package["review_status"],
        "predictive_evidence_planning_tree_review_package_digest": digest,
        "planning_tree_section_count": len(package["planning_tree_sections"]),
        "recommended_next_option": package["recommended_next_option"],
        "blocker_count": expected_summary["blocker_count"],
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED,
    }


def build_predictive_evidence_planning_tree_review_markdown_v1(
    package: dict,
) -> str:
    """Render a sanitized Markdown summary of the planning-tree review."""
    validation = validate_predictive_evidence_planning_tree_review_package_v1(
        package
    )
    metadata = package["registry_approved_dataset_metadata"]
    comparison = package["key_evidence_comparison"]
    summary = package["review_summary"]
    lines = [
        "# MarketFlow Predictive Evidence Planning Tree Review",
        "",
        "## Title",
        "- Predictive Evidence Planning Tree Review v1.",
        "",
        "## Planning Tree Review",
        f"- Artifact/status: `{package['artifact_kind']}` / `{package['review_status']}`.",
        f"- Digest: `{validation['predictive_evidence_planning_tree_review_package_digest']}`.",
        "",
        "## Bound Evidence",
    ]
    lines.extend(
        f"- `{field}`: `{digest}`"
        for field, digest in REQUIRED_DIGEST_FIELDS.items()
    )
    lines.extend(
        [
            "",
            "## Dataset and Universe",
            f"- Dataset/scope: `{metadata['dataset_name']}` / `{metadata['dataset_scope']}`.",
            f"- Universe: `{', '.join(package['target_universe'])}`.",
            "- Records: `11946`; META remains `913`, every other ticker remains `1003`.",
            "",
            "## Original Evidence Cycle",
            f"- Status/readiness: `{package['original_evidence_cycle']['additional_predictive_evidence_execution_status']}` / `{package['original_readiness_decision']}`.",
            "",
            "## Refined Evidence Cycle",
            f"- Status/readiness: `{package['refined_evidence_cycle']['additional_predictive_evidence_status']}` / `{package['refined_readiness_decision']}`.",
            "",
            "## Readiness Decisions",
            f"- Original: `{package['original_readiness_decision']}`.",
            f"- Refined: `{package['refined_readiness_decision']}`.",
            "",
            "## Final Authority State",
            f"- Predictive/profitability/runtime: `{package['predictive_usefulness']}` / `{package['profitability']}` / `{package['runtime_use']}`.",
            "",
            "## Evidence Comparison",
            f"- Original majority/previous-direction/cross-sectional accuracy: `{comparison['original_oos_majority_accuracy']}` / `{comparison['original_oos_previous_direction_accuracy']}` / `{comparison['original_oos_ticker_cross_sectional_accuracy']}`.",
            f"- Original Brier score: `{comparison['original_oos_brier_score']}`.",
            f"- Refined OOS range/signal/baseline: `{comparison['refined_oos_accuracy_range']}` / `{comparison['refined_signal_consistency']}` / `{comparison['refined_baseline_outperformance']}`.",
            "",
            "## Recommended Options",
            f"- Immediate option/reason: `{package['recommended_next_option']}` / `{package['recommended_next_option_reason']}`.",
        ]
    )
    lines.extend(
        f"- `{item['option_id']}`: `{item['status']}`"
        for item in package["recommended_next_options"]
    )
    lines.extend(["", "## Risk Controls"])
    lines.extend(f"- `{control}`" for control in package["risk_controls"])
    lines.extend(
        [
            "",
            "## Checklist Summary",
            f"- Total/passed/failed/blockers: `{summary['total_checks']}` / `{summary['passed_checks']}` / `{summary['failed_checks']}` / `{summary['blocker_count']}`.",
            "",
            "## Guardrails",
            "- This package reviews the planning tree only. It does not approve execution, predictive usefulness, profitability, runtime, strategy, paper trading, broker execution, or recommendations.",
            "- No provider request, acquisition, dataset regeneration, predictive rerun, refined rerun, metric recomputation, scoring, or recommendation occurred.",
            "",
        ]
    )
    return "\n".join(lines)


def write_predictive_evidence_planning_tree_review_package_v1(
    output_dir: str | Path,
    *,
    filename: str | None = None,
) -> dict:
    """Write one canonical JSON package without overwriting an existing file."""
    package = build_predictive_evidence_planning_tree_review_package_v1()
    validation = validate_predictive_evidence_planning_tree_review_package_v1(
        package
    )
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    output_name = filename or "predictive_evidence_planning_tree_review_v1.json"
    if Path(output_name).name != output_name or not output_name.endswith(".json"):
        raise PredictiveEvidencePlanningTreeReviewError(
            "planning-tree review filename must be a simple JSON filename"
        )
    path = directory / output_name
    if path.exists():
        raise PredictiveEvidencePlanningTreeReviewError(
            "planning-tree review output already exists"
        )
    payload = canonical_json_bytes(package)
    with path.open("xb") as handle:
        handle.write(payload)
    return validation | {
        "path": str(path).replace("\\", "/"),
        "filename": path.name,
        "payload_byte_size": len(payload),
        "payload_sha256": sha256_bytes(payload),
    }
