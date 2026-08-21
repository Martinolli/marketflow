"""Offline operator review for the redesigned-evidence planning candidate."""

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
    improved_evidence_planning_candidate_redesigned_evidence_service as candidate_service,
)


ARTIFACT_KIND_IMPROVED_EVIDENCE_PLANNING_CANDIDATE_USING_REDESIGNED_EVIDENCE_REVIEW_PACKAGE = (
    "IMPROVED_EVIDENCE_PLANNING_CANDIDATE_USING_REDESIGNED_EVIDENCE_REVIEW_PACKAGE"
)
SCHEMA_VERSION_IMPROVED_EVIDENCE_PLANNING_CANDIDATE_USING_REDESIGNED_EVIDENCE_REVIEW_V1 = (
    "improved_evidence_planning_candidate_using_redesigned_evidence_review_v1"
)
IMPROVED_EVIDENCE_PLANNING_CANDIDATE_USING_REDESIGNED_EVIDENCE_REVIEW_PACKAGE_READY = (
    "IMPROVED_EVIDENCE_PLANNING_CANDIDATE_USING_REDESIGNED_EVIDENCE_REVIEW_PACKAGE_READY"
)
IMPROVED_EVIDENCE_PLANNING_CANDIDATE_USING_REDESIGNED_EVIDENCE_REVIEW_PACKAGE_VALID = (
    "IMPROVED_EVIDENCE_PLANNING_CANDIDATE_USING_REDESIGNED_EVIDENCE_REVIEW_PACKAGE_VALID"
)

DEFAULT_BRANCH = (
    "feature/improved-evidence-planning-candidate-review-redesigned-evidence-v1"
)
DEFAULT_BASE_COMMIT = "55ee37c77f7eb8c724cc43af3dfeeabb96b45e9b"
EXPECTED_CANDIDATE_DIGEST = (
    "bfda433e36eb6d333dcc2169d8d18bb31ab0671403cc6d447dc1eda0b10fd72b"
)
TARGET_UNIVERSE = list(candidate_service.TARGET_UNIVERSE)
EXPECTED_RECORD_COUNTS = dict(candidate_service.EXPECTED_RECORD_COUNTS)
SELECTED_DIRECTION = candidate_service.SELECTED_DIRECTION
NOT_ACCEPTED = candidate_service.NOT_ACCEPTED
NOT_AUTHORIZED = candidate_service.NOT_AUTHORIZED
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"


class ImprovedEvidencePlanningCandidateRedesignedEvidenceOperatorReviewError(
    ValueError
):
    """Raised when the operator review violates its non-authorizing contract."""


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise ImprovedEvidencePlanningCandidateRedesignedEvidenceOperatorReviewError(
            f"{field} mismatch"
        )


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
        candidate_service.build_improved_evidence_planning_candidate_using_redesigned_evidence_v1()
        if candidate is None
        else deepcopy(candidate)
    )
    candidate_service.validate_improved_evidence_planning_candidate_using_redesigned_evidence_v1(
        source
    )
    _expect(
        source.get(
            "improved_evidence_planning_candidate_using_redesigned_evidence_digest"
        ),
        EXPECTED_CANDIDATE_DIGEST,
        "source candidate digest",
    )
    summary = source.get("candidate_summary", {})
    _expect(summary.get("total_checks"), 72, "source checklist total")
    _expect(summary.get("passed_checks"), 72, "source checklist passed")
    _expect(summary.get("failed_checks"), 0, "source checklist failed")
    _expect(summary.get("blocker_count"), 0, "source blocker count")
    return source


def _per_ticker_review_digest_payload(entry: Mapping[str, Any]) -> dict[str, Any]:
    payload = deepcopy(dict(entry))
    payload.pop(
        "per_ticker_improved_evidence_planning_candidate_review_digest", None
    )
    return payload


def per_ticker_improved_evidence_planning_candidate_review_digest_v1(
    entry: Mapping[str, Any],
) -> str:
    """Return the deterministic digest for one ticker review entry."""
    return semantic_digest(_per_ticker_review_digest_payload(entry))


def _per_ticker_review_entries(source: Mapping[str, Any]) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for source_entry in source["per_ticker_planning_entries"]:
        entry = {
            "ticker": source_entry["ticker"],
            "registry_approval_status": source_entry["registry_approval_status"],
            "canonical_dataset_status": source_entry["canonical_dataset_status"],
            "historical_record_count": source_entry["historical_record_count"],
            "meta_reduced_record_count_flag": source_entry[
                "meta_reduced_record_count_flag"
            ],
            "label_objective_redesign_results_review_status": source_entry[
                "label_objective_redesign_results_review_status"
            ],
            "improved_evidence_planning_candidate_status": source_entry[
                "improved_evidence_planning_candidate_status"
            ],
            "improved_evidence_planning_candidate_review_status": "READY_FOR_OPERATOR_ASSESSMENT",
            "selected_redesign_direction": source_entry[
                "selected_redesign_direction"
            ],
            "improved_evidence_planning_approved": False,
            "improved_evidence_planning_executed": False,
            "label_regeneration_authorized": False,
            "label_regeneration_performed": False,
            "new_targets_created": False,
            "target_definition_change_authorized": False,
            "additional_predictive_evidence_execution_candidate_created": False,
            "additional_predictive_evidence_executed": False,
            "predictive_usefulness": NOT_ACCEPTED,
            "predictive_usefulness_acceptance_ready": False,
            "predictive_usefulness_acceptance_candidate_created": False,
            "profitability": NOT_ACCEPTED,
            "runtime_use": NOT_AUTHORIZED,
            "strategy_use": NOT_AUTHORIZED,
            "paper_trading": NOT_AUTHORIZED,
            "broker_execution": NOT_AUTHORIZED,
            "source_improved_evidence_planning_candidate_digest": EXPECTED_CANDIDATE_DIGEST,
            "per_ticker_improved_evidence_planning_candidate_digest": source_entry[
                "per_ticker_improved_evidence_planning_candidate_digest"
            ],
            "planning_note": source_entry["planning_note"],
        }
        entry["per_ticker_improved_evidence_planning_candidate_review_digest"] = (
            per_ticker_improved_evidence_planning_candidate_review_digest_v1(entry)
        )
        entries.append(entry)
    return entries


def _reviewed_candidate_objective(source: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "improved_evidence_planning_candidate_objective": source[
            "improved_evidence_planning_candidate_objective"
        ],
        "improved_evidence_planning_candidate_scope": source[
            "improved_evidence_planning_candidate_scope"
        ],
        "improved_evidence_planning_candidate_mode": source[
            "improved_evidence_planning_candidate_mode"
        ],
        "improved_evidence_planning_candidate_authority_status": source[
            "improved_evidence_planning_candidate_authority_status"
        ],
    }


def _base_review(source: dict[str, Any]) -> dict[str, Any]:
    summary = source["candidate_summary"]
    return {
        "artifact_kind": ARTIFACT_KIND_IMPROVED_EVIDENCE_PLANNING_CANDIDATE_USING_REDESIGNED_EVIDENCE_REVIEW_PACKAGE,
        "schema_version": SCHEMA_VERSION_IMPROVED_EVIDENCE_PLANNING_CANDIDATE_USING_REDESIGNED_EVIDENCE_REVIEW_V1,
        "review_status": IMPROVED_EVIDENCE_PLANNING_CANDIDATE_USING_REDESIGNED_EVIDENCE_REVIEW_PACKAGE_READY,
        "branch": DEFAULT_BRANCH,
        "base_commit": DEFAULT_BASE_COMMIT,
        "created_offline": True,
        "research_only": True,
        "operator_review_required": True,
        "source_candidate_artifact_kind": source["artifact_kind"],
        "source_candidate_status": source["candidate_status"],
        "source_candidate_digest": source[
            "improved_evidence_planning_candidate_using_redesigned_evidence_digest"
        ],
        "source_candidate_checklist_total": summary["total_checks"],
        "source_candidate_checklist_passed": summary["passed_checks"],
        "source_candidate_checklist_failed": summary["failed_checks"],
        "source_candidate_blocker_count": summary["blocker_count"],
        "improved_evidence_planning_candidate_using_redesigned_evidence_digest": source[
            "improved_evidence_planning_candidate_using_redesigned_evidence_digest"
        ],
        **deepcopy(candidate_service.BOUND_DIGESTS),
        "label_objective_redesign_executed": True,
        "label_objective_redesign_results_created": True,
        "label_objective_redesign_results_review_created": True,
        "label_objective_redesign_results_review_ready": True,
        "source_results_review_ready": True,
        "ready_for_optional_improved_evidence_planning_candidate_using_redesigned_evidence": True,
        "improved_evidence_planning_candidate_created": True,
        "improved_evidence_planning_candidate_using_redesigned_evidence_created": True,
        "improved_evidence_planning_candidate_using_redesigned_evidence_ready_for_operator_review": True,
        "improved_evidence_planning_candidate_using_redesigned_evidence_review_created": True,
        "improved_evidence_planning_approved": False,
        "improved_evidence_planning_authorized": False,
        "improved_evidence_planning_executed": False,
        "additional_predictive_evidence_execution_candidate_created": False,
        "additional_predictive_evidence_executed": False,
        "label_regeneration_authorized": False,
        "label_regeneration_performed": False,
        "new_targets_created": False,
        "target_definition_change_authorized": False,
        "target_definition_change_performed": False,
        "features_generated": False,
        "feature_label_matrix_created": False,
        "predictive_usefulness_acceptance_candidate_created": False,
        "predictive_usefulness": NOT_ACCEPTED,
        "predictive_usefulness_acceptance_ready": False,
        "predictive_usefulness_acceptance_recommended": False,
        "predictive_usefulness_acceptance_artifact_created": False,
        "profitability": NOT_ACCEPTED,
        "profitability_acceptance_ready": False,
        "profitability_acceptance_recommended": False,
        "profitability_acceptance_created": False,
        "runtime_migration_approved": False,
        "runtime_migration_active": False,
        "runtime_migration_approval_created": False,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "automatic_stitching": False,
        "new_strategy_scoring_performed": False,
        "trade_recommendations_generated": False,
        "provider_requests_made_in_review": False,
        "live_provider_transport_enabled_in_review": False,
        "market_data_acquisition_performed_in_review": False,
        "dataset_generation_performed_in_review": False,
        "canonical_dataset_regenerated_in_review": False,
        "redesigned_label_regeneration_performed": False,
        "feature_regeneration_performed": False,
        "predictive_evidence_execution_rerun_performed": False,
        "label_objective_target_definition_review_execution_rerun_performed": False,
        "label_objective_redesign_execution_rerun_performed": False,
        "metric_recomputation_performed_in_review": False,
        "model_training_performed_in_review": False,
        "raw_provider_payloads_committed": False,
        "api_keys_stored_or_printed": False,
        "no_tracked_marketflow_files": True,
        "dataset_name": source["dataset_name"],
        "source_profile": source["source_profile"],
        "timeframe": source["timeframe"],
        "date_range_start": source["date_range_start"],
        "date_range_end": source["date_range_end"],
        "target_universe_count": source["target_universe_count"],
        "target_universe": deepcopy(source["target_universe"]),
        "total_canonical_record_count": source["total_canonical_record_count"],
        "per_ticker_record_counts": deepcopy(source["per_ticker_record_counts"]),
        "meta_record_count": source["meta_record_count"],
        "non_meta_record_count": source["non_meta_record_count"],
        "meta_reduced_record_count_preserved": source[
            "meta_reduced_record_count_preserved"
        ],
        "reviewed_candidate_basis": deepcopy(source["candidate_basis"]),
        "selected_direction": source["selected_direction"],
        "majority_structure_risk": source["majority_structure_risk"],
        "largest_aggregated_class": source["largest_aggregated_class"],
        "largest_aggregated_class_count": source["largest_aggregated_class_count"],
        "no_trade_count": source["no_trade_count"],
        "oos_evaluated_rows": source["oos_evaluated_rows"],
        "majority_accuracy": source["majority_accuracy"],
        "local_model_accuracy": source["local_model_accuracy"],
        "cross_sectional_accuracy": source["cross_sectional_accuracy"],
        "cross_sectional_delta_vs_majority": source[
            "cross_sectional_delta_vs_majority"
        ],
        "global_five_session_threshold": source["global_five_session_threshold"],
        "benchmark_relative_threshold": source["benchmark_relative_threshold"],
        **_reviewed_candidate_objective(source),
        "reviewed_candidate_objective": _reviewed_candidate_objective(source),
        "reviewed_improved_evidence_themes": deepcopy(
            source["improved_evidence_themes"]
        ),
        "reviewed_planned_evidence_components": deepcopy(
            source["planned_evidence_components"]
        ),
        "reviewed_planned_data_products": deepcopy(source["planned_data_products"]),
        "reviewed_planned_future_outputs": deepcopy(
            source["planned_future_outputs"]
        ),
        "per_ticker_review_entries": _per_ticker_review_entries(source),
        "reviewed_next_chain": deepcopy(source["next_chain"]),
        "reviewed_next_gates": deepcopy(source["next_gates"]),
        "reviewed_risk_controls": deepcopy(source["risk_controls"]),
    }


CHECK_FIELD_SPECS: list[tuple[str, Any, str]] = [
    ("candidate_kind_matches", candidate_service.ARTIFACT_KIND_IMPROVED_EVIDENCE_PLANNING_CANDIDATE_USING_REDESIGNED_EVIDENCE, "source_candidate_artifact_kind"),
    ("candidate_status_ready_for_review", candidate_service.IMPROVED_EVIDENCE_PLANNING_CANDIDATE_USING_REDESIGNED_EVIDENCE_READY_FOR_OPERATOR_REVIEW, "source_candidate_status"),
    ("candidate_digest_matches_expected", EXPECTED_CANDIDATE_DIGEST, "source_candidate_digest"),
    ("candidate_checklist_zero_blockers", 0, "source_candidate_blocker_count"),
    ("improved_evidence_planning_candidate_digest_bound", EXPECTED_CANDIDATE_DIGEST, "improved_evidence_planning_candidate_using_redesigned_evidence_digest"),
    ("redesign_results_review_digest_bound", candidate_service.BOUND_DIGESTS["label_objective_redesign_results_review_using_redesigned_evidence_digest"], "label_objective_redesign_results_review_using_redesigned_evidence_digest"),
    ("redesign_execution_digest_bound", candidate_service.BOUND_DIGESTS["label_objective_redesign_execution_using_redesigned_evidence_digest"], "label_objective_redesign_execution_using_redesigned_evidence_digest"),
    ("redesign_output_binding_digest_bound", candidate_service.BOUND_DIGESTS["label_objective_redesign_output_binding_digest"], "label_objective_redesign_output_binding_digest"),
    ("redesign_approval_digest_bound", candidate_service.BOUND_DIGESTS["label_objective_redesign_approval_using_redesigned_evidence_digest"], "label_objective_redesign_approval_using_redesigned_evidence_digest"),
    ("redesign_candidate_review_digest_bound", candidate_service.BOUND_DIGESTS["label_objective_redesign_candidate_using_redesigned_evidence_review_package_digest"], "label_objective_redesign_candidate_using_redesigned_evidence_review_package_digest"),
    ("redesign_candidate_digest_bound", candidate_service.BOUND_DIGESTS["label_objective_redesign_candidate_using_redesigned_evidence_digest"], "label_objective_redesign_candidate_using_redesigned_evidence_digest"),
    ("target_definition_results_review_digest_bound", candidate_service.BOUND_DIGESTS["label_objective_target_definition_results_review_using_redesigned_evidence_digest"], "label_objective_target_definition_results_review_using_redesigned_evidence_digest"),
    ("target_definition_execution_digest_bound", candidate_service.BOUND_DIGESTS["label_objective_target_definition_review_execution_using_redesigned_evidence_digest"], "label_objective_target_definition_review_execution_using_redesigned_evidence_digest"),
    ("path_selection_digest_bound", candidate_service.BOUND_DIGESTS["method_evidence_improvement_path_selection_using_redesigned_evidence_digest"], "method_evidence_improvement_path_selection_using_redesigned_evidence_digest"),
    ("readiness_review_digest_bound", candidate_service.BOUND_DIGESTS["predictive_usefulness_acceptance_readiness_review_using_redesigned_evidence_digest"], "predictive_usefulness_acceptance_readiness_review_using_redesigned_evidence_digest"),
    ("reassessment_digest_bound", candidate_service.BOUND_DIGESTS["predictive_usefulness_reassessment_using_redesigned_evidence_digest"], "predictive_usefulness_reassessment_using_redesigned_evidence_digest"),
    ("predictive_results_review_digest_bound", candidate_service.BOUND_DIGESTS["additional_predictive_evidence_results_review_using_redesigned_labels_digest"], "additional_predictive_evidence_results_review_using_redesigned_labels_digest"),
    ("predictive_execution_digest_bound", candidate_service.BOUND_DIGESTS["additional_predictive_evidence_execution_using_redesigned_labels_digest"], "additional_predictive_evidence_execution_using_redesigned_labels_digest"),
    ("matrix_digest_bound", candidate_service.BOUND_DIGESTS["feature_label_matrix_digest"], "feature_label_matrix_digest"),
    ("feature_values_digest_bound", candidate_service.BOUND_DIGESTS["feature_values_digest"], "feature_values_digest"),
    ("label_values_digest_bound", candidate_service.BOUND_DIGESTS["redesigned_label_values_digest"], "redesigned_label_values_digest"),
    ("research_registry_digest_bound", candidate_service.BOUND_DIGESTS["research_registry_approval_digest"], "research_registry_approval_digest"),
    ("records_digest_bound", candidate_service.BOUND_DIGESTS["records_digest"], "records_digest"),
    ("target_universe_12_preserved", TARGET_UNIVERSE, "target_universe"),
    ("records_digest_preserved", candidate_service.BOUND_DIGESTS["records_digest"], "records_digest"),
    ("meta_913_preserved", 913, "meta_record_count"),
    ("source_results_review_ready_true", True, "source_results_review_ready"),
    ("ready_for_improved_evidence_planning_candidate_true", True, "ready_for_optional_improved_evidence_planning_candidate_using_redesigned_evidence"),
    ("planning_candidate_created_true", True, "improved_evidence_planning_candidate_created"),
    ("planning_candidate_review_created_true", True, "improved_evidence_planning_candidate_using_redesigned_evidence_review_created"),
    ("planning_candidate_ready_true", True, "improved_evidence_planning_candidate_using_redesigned_evidence_ready_for_operator_review"),
    ("planning_approved_false", False, "improved_evidence_planning_approved"),
    ("planning_authorized_false", False, "improved_evidence_planning_authorized"),
    ("planning_executed_false", False, "improved_evidence_planning_executed"),
    ("selected_redesign_direction_preserved", SELECTED_DIRECTION, "selected_direction"),
    ("label_regeneration_authorized_false", False, "label_regeneration_authorized"),
    ("label_regeneration_performed_false", False, "label_regeneration_performed"),
    ("new_targets_created_false", False, "new_targets_created"),
    ("target_definition_change_authorized_false", False, "target_definition_change_authorized"),
    ("target_definition_change_performed_false", False, "target_definition_change_performed"),
    ("features_generated_false", False, "features_generated"),
    ("feature_label_matrix_created_false", False, "feature_label_matrix_created"),
    ("additional_predictive_evidence_execution_candidate_created_false", False, "additional_predictive_evidence_execution_candidate_created"),
    ("additional_predictive_evidence_executed_false", False, "additional_predictive_evidence_executed"),
    ("predictive_usefulness_not_accepted", NOT_ACCEPTED, "predictive_usefulness"),
    ("acceptance_ready_false", False, "predictive_usefulness_acceptance_ready"),
    ("acceptance_candidate_created_false", False, "predictive_usefulness_acceptance_candidate_created"),
    ("profitability_not_accepted", NOT_ACCEPTED, "profitability"),
    ("runtime_not_authorized", NOT_AUTHORIZED, "runtime_use"),
    ("strategy_not_authorized", NOT_AUTHORIZED, "strategy_use"),
    ("broker_not_authorized", NOT_AUTHORIZED, "broker_execution"),
    ("trade_recommendations_false", False, "trade_recommendations_generated"),
    ("candidate_basis_reviewed", candidate_service.CANDIDATE_BASIS, "reviewed_candidate_basis"),
    ("candidate_objective_reviewed", "EXPECTED", "candidate_objective_reviewed"),
    ("improved_evidence_themes_reviewed", candidate_service.IMPROVED_EVIDENCE_THEME_IDS, "reviewed_theme_ids"),
    ("planned_evidence_components_reviewed", candidate_service.PLANNED_EVIDENCE_COMPONENT_IDS, "reviewed_component_ids"),
    ("planned_data_products_not_generated", True, "reviewed_data_products_not_generated"),
    ("future_outputs_not_generated", True, "reviewed_future_outputs_not_generated"),
    ("per_ticker_entries_12", 12, "per_ticker_entry_count"),
    ("per_ticker_candidate_digests_present", True, "per_ticker_candidate_digests_valid"),
    ("per_ticker_review_digests_present", True, "per_ticker_review_digests_valid"),
    ("provider_requests_made_false", False, "provider_requests_made_in_review"),
    ("market_data_acquisition_false", False, "market_data_acquisition_performed_in_review"),
    ("dataset_regeneration_false", False, "canonical_dataset_regenerated_in_review"),
    ("redesigned_label_regeneration_false", False, "redesigned_label_regeneration_performed"),
    ("feature_regeneration_false", False, "feature_regeneration_performed"),
    ("predictive_evidence_rerun_false", False, "predictive_evidence_execution_rerun_performed"),
    ("label_objective_redesign_execution_rerun_false", False, "label_objective_redesign_execution_rerun_performed"),
    ("metric_recomputation_in_review_false", False, "metric_recomputation_performed_in_review"),
    ("model_training_in_review_false", False, "model_training_performed_in_review"),
    ("raw_provider_payloads_not_committed", False, "raw_provider_payloads_committed"),
    ("api_keys_not_stored_or_printed", False, "api_keys_stored_or_printed"),
    ("no_predictive_usefulness_acceptance_artifact_created", False, "predictive_usefulness_acceptance_artifact_created"),
    ("no_profitability_acceptance_created", False, "profitability_acceptance_created"),
    ("no_runtime_migration_approval_created", False, "runtime_migration_approval_created"),
    ("next_chain_reviewed", candidate_service.NEXT_CHAIN, "reviewed_next_chain"),
    ("next_gates_reviewed", candidate_service.NEXT_GATES, "reviewed_next_gates"),
    ("risk_controls_reviewed", candidate_service.RISK_CONTROLS, "reviewed_risk_controls"),
    ("no_tracked_marketflow_files", True, "no_tracked_marketflow_files"),
]
REQUIRED_CHECK_IDS = [spec[0] for spec in CHECK_FIELD_SPECS]


def _derived_fields(review_package: Mapping[str, Any]) -> dict[str, Any]:
    themes = review_package.get("reviewed_improved_evidence_themes", [])
    components = review_package.get("reviewed_planned_evidence_components", [])
    products = review_package.get("reviewed_planned_data_products", [])
    outputs = review_package.get("reviewed_planned_future_outputs", [])
    entries = review_package.get("per_ticker_review_entries", [])
    expected_objective = {
        "improved_evidence_planning_candidate_objective": candidate_service.CANDIDATE_OBJECTIVE,
        "improved_evidence_planning_candidate_scope": candidate_service.CANDIDATE_SCOPE,
        "improved_evidence_planning_candidate_mode": candidate_service.CANDIDATE_MODE,
        "improved_evidence_planning_candidate_authority_status": candidate_service.CANDIDATE_AUTHORITY_STATUS,
    }
    return {
        **review_package,
        "candidate_objective_reviewed": (
            "EXPECTED"
            if review_package.get("reviewed_candidate_objective")
            == expected_objective
            else "MISMATCH"
        ),
        "reviewed_theme_ids": (
            [row.get("theme_id") for row in themes]
            if isinstance(themes, list)
            else []
        ),
        "reviewed_component_ids": (
            [row.get("component_id") for row in components]
            if isinstance(components, list)
            else []
        ),
        "reviewed_data_products_not_generated": (
            isinstance(products, list)
            and len(products) == len(candidate_service.PLANNED_DATA_PRODUCT_IDS)
            and all(
                row.get("output_status") == candidate_service.PLANNED_NOT_GENERATED
                and row.get("output_label")
                == candidate_service.RESEARCH_ONLY_NON_ACTIONABLE
                and row.get("generated") is False
                for row in products
            )
        ),
        "reviewed_future_outputs_not_generated": (
            isinstance(outputs, list)
            and len(outputs) == len(candidate_service.PLANNED_FUTURE_OUTPUT_IDS)
            and all(
                row.get("output_status") == candidate_service.PLANNED_NOT_GENERATED
                and row.get("output_label")
                == candidate_service.RESEARCH_ONLY_NON_ACTIONABLE
                and row.get("generated") is False
                for row in outputs
            )
        ),
        "per_ticker_entry_count": len(entries) if isinstance(entries, list) else 0,
        "per_ticker_candidate_digests_valid": (
            isinstance(entries, list)
            and len(entries) == 12
            and all(
                isinstance(
                    row.get(
                        "per_ticker_improved_evidence_planning_candidate_digest"
                    ),
                    str,
                )
                and len(
                    row["per_ticker_improved_evidence_planning_candidate_digest"]
                )
                == 64
                for row in entries
            )
        ),
        "per_ticker_review_digests_valid": (
            isinstance(entries, list)
            and len(entries) == 12
            and all(
                isinstance(
                    row.get(
                        "per_ticker_improved_evidence_planning_candidate_review_digest"
                    ),
                    str,
                )
                and len(
                    row[
                        "per_ticker_improved_evidence_planning_candidate_review_digest"
                    ]
                )
                == 64
                and row[
                    "per_ticker_improved_evidence_planning_candidate_review_digest"
                ]
                == per_ticker_improved_evidence_planning_candidate_review_digest_v1(
                    row
                )
                for row in entries
            )
        ),
    }


def _checklist(review_package: Mapping[str, Any]) -> list[dict[str, Any]]:
    fields = _derived_fields(review_package)
    return [
        _check(check_id, expected, fields.get(field))
        for check_id, expected, field in CHECK_FIELD_SPECS
    ]


def _summary(checklist: list[dict[str, Any]]) -> dict[str, Any]:
    failed = [row for row in checklist if row["status"] != PASS]
    return {
        "total_checks": len(checklist),
        "passed_checks": len(checklist) - len(failed),
        "failed_checks": len(failed),
        "blocker_count": len(failed),
        "ready_for_operator_assessment": not failed,
        "ready_for_improved_evidence_planning_approval": False,
        "selected_redesign_direction": SELECTED_DIRECTION,
        "improved_evidence_planning_approved": False,
        "improved_evidence_planning_executed": False,
        "label_regeneration_performed": False,
        "new_targets_created": False,
        "target_definition_change_authorized": False,
        "additional_predictive_evidence_execution_candidate_created": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_authorized": False,
        "trade_recommendations_generated": False,
    }


def _digest_payload(review_package: Mapping[str, Any]) -> dict[str, Any]:
    payload = deepcopy(dict(review_package))
    payload.pop(
        "improved_evidence_planning_candidate_using_redesigned_evidence_review_package_digest",
        None,
    )
    return payload


def improved_evidence_planning_candidate_using_redesigned_evidence_review_package_digest_v1(
    review_package: Mapping[str, Any],
) -> str:
    """Return the deterministic semantic digest for the operator review."""
    return semantic_digest(_digest_payload(review_package))


def build_improved_evidence_planning_candidate_using_redesigned_evidence_review_package_v1(
    candidate: dict | None = None,
) -> dict:
    """Build an offline review package over the validated source candidate."""
    source = _source_candidate(candidate)
    review_package = _base_review(source)
    review_package["review_checklist"] = _checklist(review_package)
    review_package["review_summary"] = _summary(review_package["review_checklist"])
    review_package[
        "improved_evidence_planning_candidate_using_redesigned_evidence_review_package_digest"
    ] = improved_evidence_planning_candidate_using_redesigned_evidence_review_package_digest_v1(
        review_package
    )
    validate_improved_evidence_planning_candidate_using_redesigned_evidence_review_package_v1(
        review_package
    )
    return review_package


def _reject_forbidden_values(value: Any, *, path: str = "review_package") -> None:
    forbidden_artifacts = {
        "IMPROVED_EVIDENCE_PLANNING_APPROVED",
        "IMPROVED_EVIDENCE_PLANNING_EXECUTED",
        "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE",
        "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED",
        "PREDICTIVE_USEFULNESS_REASSESSMENT_REVIEW_PACKAGE",
        "PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_REVIEW",
        "PREDICTIVE_USEFULNESS_ACCEPTANCE_CANDIDATE",
        "PREDICTIVE_USEFULNESS_ACCEPTED",
        "PROFITABILITY_ACCEPTED",
        "RUNTIME_MIGRATION_APPROVED",
        "RUNTIME_MIGRATION_ACTIVE",
        "STRATEGY_RUNTIME_MIGRATION",
        "TRADE_RECOMMENDATIONS",
    }
    forbidden_true = {
        "improved_evidence_planning_approved",
        "improved_evidence_planning_authorized",
        "improved_evidence_planning_executed",
        "additional_predictive_evidence_execution_candidate_created",
        "additional_predictive_evidence_executed",
        "label_regeneration_authorized",
        "label_regeneration_performed",
        "new_targets_created",
        "target_definition_change_authorized",
        "target_definition_change_performed",
        "features_generated",
        "feature_label_matrix_created",
        "predictive_usefulness_acceptance_ready",
        "predictive_usefulness_acceptance_recommended",
        "predictive_usefulness_acceptance_candidate_created",
        "profitability_acceptance_ready",
        "profitability_acceptance_recommended",
        "runtime_migration_approved",
        "runtime_migration_active",
        "new_strategy_scoring_performed",
        "trade_recommendations_generated",
        "predictive_evidence_execution_rerun_performed",
        "metric_recomputation_performed_in_review",
        "model_training_performed_in_review",
    }
    if isinstance(value, Mapping):
        for key, item in value.items():
            current = f"{path}.{key}"
            if isinstance(item, str) and item in forbidden_artifacts:
                raise ImprovedEvidencePlanningCandidateRedesignedEvidenceOperatorReviewError(
                    f"{current} must not emit {item}"
                )
            if key in forbidden_true and item is True:
                raise ImprovedEvidencePlanningCandidateRedesignedEvidenceOperatorReviewError(
                    f"{current} must remain false"
                )
            if key in {
                "runtime_use",
                "strategy_use",
                "paper_trading",
                "broker_execution",
            } and item == "AUTHORIZED":
                raise ImprovedEvidencePlanningCandidateRedesignedEvidenceOperatorReviewError(
                    f"{current} must remain NOT_AUTHORIZED"
                )
            if key in {"predictive_usefulness", "profitability"} and item == "accepted":
                raise ImprovedEvidencePlanningCandidateRedesignedEvidenceOperatorReviewError(
                    f"{current} must remain not accepted"
                )
            _reject_forbidden_values(item, path=current)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _reject_forbidden_values(item, path=f"{path}[{index}]")


def validate_improved_evidence_planning_candidate_using_redesigned_evidence_review_package_v1(
    review_package: dict,
) -> dict:
    """Fail closed unless this is exactly the review-only package."""
    if not isinstance(review_package, dict):
        raise ImprovedEvidencePlanningCandidateRedesignedEvidenceOperatorReviewError(
            "review package must be a JSON object"
        )
    _expect(
        review_package.get("artifact_kind"),
        ARTIFACT_KIND_IMPROVED_EVIDENCE_PLANNING_CANDIDATE_USING_REDESIGNED_EVIDENCE_REVIEW_PACKAGE,
        "artifact_kind",
    )
    _expect(
        review_package.get("schema_version"),
        SCHEMA_VERSION_IMPROVED_EVIDENCE_PLANNING_CANDIDATE_USING_REDESIGNED_EVIDENCE_REVIEW_V1,
        "schema_version",
    )
    _expect(
        review_package.get("review_status"),
        IMPROVED_EVIDENCE_PLANNING_CANDIDATE_USING_REDESIGNED_EVIDENCE_REVIEW_PACKAGE_READY,
        "review_status",
    )
    _reject_forbidden_values(review_package)

    expected = {
        "source_candidate_artifact_kind": candidate_service.ARTIFACT_KIND_IMPROVED_EVIDENCE_PLANNING_CANDIDATE_USING_REDESIGNED_EVIDENCE,
        "source_candidate_status": candidate_service.IMPROVED_EVIDENCE_PLANNING_CANDIDATE_USING_REDESIGNED_EVIDENCE_READY_FOR_OPERATOR_REVIEW,
        "source_candidate_digest": EXPECTED_CANDIDATE_DIGEST,
        "source_candidate_checklist_total": 72,
        "source_candidate_checklist_passed": 72,
        "source_candidate_checklist_failed": 0,
        "source_candidate_blocker_count": 0,
        "improved_evidence_planning_candidate_using_redesigned_evidence_digest": EXPECTED_CANDIDATE_DIGEST,
        **candidate_service.BOUND_DIGESTS,
        "dataset_name": "expanded_universe_canonical_dataset_v1",
        "source_profile": "RTH_FULL_SESSION_1D",
        "timeframe": "1d",
        "date_range_start": "2022-01-01",
        "date_range_end": "2025-12-31",
        "target_universe_count": 12,
        "target_universe": TARGET_UNIVERSE,
        "total_canonical_record_count": 11946,
        "per_ticker_record_counts": EXPECTED_RECORD_COUNTS,
        "meta_record_count": 913,
        "non_meta_record_count": 1003,
        "reviewed_candidate_basis": candidate_service.CANDIDATE_BASIS,
        "selected_direction": SELECTED_DIRECTION,
        "majority_structure_risk": "PRESENT_REQUIRES_OPERATOR_REVIEW",
        "largest_aggregated_class": "FLAT",
        "largest_aggregated_class_count": 13600,
        "no_trade_count": 1540,
        "oos_evaluated_rows": 34848,
        "majority_accuracy": "0.58626033",
        "local_model_accuracy": "0.58626033",
        "cross_sectional_accuracy": "0.58935950",
        "cross_sectional_delta_vs_majority": "0.00309917",
        "global_five_session_threshold": "0.026556108631",
        "benchmark_relative_threshold": "0.02058653801",
        "reviewed_candidate_objective": {
            "improved_evidence_planning_candidate_objective": candidate_service.CANDIDATE_OBJECTIVE,
            "improved_evidence_planning_candidate_scope": candidate_service.CANDIDATE_SCOPE,
            "improved_evidence_planning_candidate_mode": candidate_service.CANDIDATE_MODE,
            "improved_evidence_planning_candidate_authority_status": candidate_service.CANDIDATE_AUTHORITY_STATUS,
        },
        "reviewed_improved_evidence_themes": candidate_service._improved_evidence_themes(),
        "reviewed_planned_evidence_components": candidate_service._planned_evidence_components(),
        "reviewed_planned_data_products": candidate_service._planned_products(candidate_service.PLANNED_DATA_PRODUCT_IDS, id_field="data_product_id"),
        "reviewed_planned_future_outputs": candidate_service._planned_products(candidate_service.PLANNED_FUTURE_OUTPUT_IDS, id_field="future_output_id"),
        "per_ticker_review_entries": _per_ticker_review_entries(
            candidate_service.build_improved_evidence_planning_candidate_using_redesigned_evidence_v1()
        ),
        "reviewed_next_chain": candidate_service.NEXT_CHAIN,
        "reviewed_next_gates": candidate_service.NEXT_GATES,
        "reviewed_risk_controls": candidate_service.RISK_CONTROLS,
    }
    for field, expected_value in expected.items():
        _expect(review_package.get(field), expected_value, field)

    true_fields = [
        "created_offline",
        "research_only",
        "operator_review_required",
        "label_objective_redesign_executed",
        "label_objective_redesign_results_created",
        "label_objective_redesign_results_review_created",
        "label_objective_redesign_results_review_ready",
        "source_results_review_ready",
        "ready_for_optional_improved_evidence_planning_candidate_using_redesigned_evidence",
        "improved_evidence_planning_candidate_created",
        "improved_evidence_planning_candidate_using_redesigned_evidence_created",
        "improved_evidence_planning_candidate_using_redesigned_evidence_ready_for_operator_review",
        "improved_evidence_planning_candidate_using_redesigned_evidence_review_created",
        "meta_reduced_record_count_preserved",
        "no_tracked_marketflow_files",
    ]
    false_fields = [
        "improved_evidence_planning_approved",
        "improved_evidence_planning_authorized",
        "improved_evidence_planning_executed",
        "additional_predictive_evidence_execution_candidate_created",
        "additional_predictive_evidence_executed",
        "label_regeneration_authorized",
        "label_regeneration_performed",
        "new_targets_created",
        "target_definition_change_authorized",
        "target_definition_change_performed",
        "features_generated",
        "feature_label_matrix_created",
        "predictive_usefulness_acceptance_candidate_created",
        "predictive_usefulness_acceptance_ready",
        "predictive_usefulness_acceptance_recommended",
        "predictive_usefulness_acceptance_artifact_created",
        "profitability_acceptance_ready",
        "profitability_acceptance_recommended",
        "profitability_acceptance_created",
        "runtime_migration_approved",
        "runtime_migration_active",
        "runtime_migration_approval_created",
        "automatic_stitching",
        "new_strategy_scoring_performed",
        "trade_recommendations_generated",
        "provider_requests_made_in_review",
        "live_provider_transport_enabled_in_review",
        "market_data_acquisition_performed_in_review",
        "dataset_generation_performed_in_review",
        "canonical_dataset_regenerated_in_review",
        "redesigned_label_regeneration_performed",
        "feature_regeneration_performed",
        "predictive_evidence_execution_rerun_performed",
        "label_objective_target_definition_review_execution_rerun_performed",
        "label_objective_redesign_execution_rerun_performed",
        "metric_recomputation_performed_in_review",
        "model_training_performed_in_review",
        "raw_provider_payloads_committed",
        "api_keys_stored_or_printed",
    ]
    for field in true_fields:
        _expect(review_package.get(field), True, field)
    for field in false_fields:
        _expect(review_package.get(field), False, field)
    _expect(review_package.get("predictive_usefulness"), NOT_ACCEPTED, "predictive_usefulness")
    _expect(review_package.get("profitability"), NOT_ACCEPTED, "profitability")
    for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
        _expect(review_package.get(field), NOT_AUTHORIZED, field)

    checklist = review_package.get("review_checklist")
    if not isinstance(checklist, list):
        raise ImprovedEvidencePlanningCandidateRedesignedEvidenceOperatorReviewError(
            "review_checklist mismatch"
        )
    _expect(
        [row.get("check_id") for row in checklist],
        REQUIRED_CHECK_IDS,
        "review_checklist check ids",
    )
    _expect(checklist, _checklist(review_package), "review_checklist")
    if any(row.get("status") != PASS for row in checklist):
        raise ImprovedEvidencePlanningCandidateRedesignedEvidenceOperatorReviewError(
            "review_checklist must pass"
        )
    _expect(review_package.get("review_summary"), _summary(checklist), "review_summary")
    digest = review_package.get(
        "improved_evidence_planning_candidate_using_redesigned_evidence_review_package_digest"
    )
    if not isinstance(digest, str) or len(digest) != 64:
        raise ImprovedEvidencePlanningCandidateRedesignedEvidenceOperatorReviewError(
            "missing review digest"
        )
    _expect(
        digest,
        improved_evidence_planning_candidate_using_redesigned_evidence_review_package_digest_v1(
            review_package
        ),
        "review package digest",
    )
    return {
        "status": IMPROVED_EVIDENCE_PLANNING_CANDIDATE_USING_REDESIGNED_EVIDENCE_REVIEW_PACKAGE_VALID,
        "artifact_kind": review_package["artifact_kind"],
        "review_status": review_package["review_status"],
        "improved_evidence_planning_candidate_using_redesigned_evidence_review_package_digest": digest,
        "source_candidate_digest": EXPECTED_CANDIDATE_DIGEST,
        "per_ticker_review_entry_count": len(
            review_package["per_ticker_review_entries"]
        ),
        "blocker_count": review_package["review_summary"]["blocker_count"],
        "ready_for_operator_assessment": True,
        "ready_for_improved_evidence_planning_approval": False,
        "improved_evidence_planning_approved": False,
        "improved_evidence_planning_executed": False,
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "runtime_authorized": False,
    }


def build_improved_evidence_planning_candidate_using_redesigned_evidence_review_markdown_v1(
    review_package: dict,
) -> str:
    """Render the review without implying selection, approval, or execution."""
    validation = validate_improved_evidence_planning_candidate_using_redesigned_evidence_review_package_v1(
        review_package
    )
    summary = review_package["review_summary"]
    lines = [
        "# MarketFlow Improved Evidence Planning Candidate Operator Review Status",
        "",
        "## Title",
        "- Optional Improved Evidence Planning Candidate Operator Review Using Redesigned Evidence v1.",
        "",
        "## Optional Improved Evidence Planning Candidate Review Using Redesigned Evidence",
        f"- Artifact/status/digest: `{review_package['artifact_kind']}` / `{review_package['review_status']}` / `{validation['improved_evidence_planning_candidate_using_redesigned_evidence_review_package_digest']}`.",
        "",
        "## Reviewed Candidate",
        f"- `{review_package['source_candidate_artifact_kind']}` / `{review_package['source_candidate_status']}` / `{review_package['source_candidate_digest']}` with `72 / 72` source checks and zero blockers.",
        "",
        "## Source Redesign Results Review",
        f"- Results-review digest: `{review_package['label_objective_redesign_results_review_using_redesigned_evidence_digest']}`.",
        "",
        "## Bound Evidence",
        f"- Redesign execution/output/approval: `{review_package['label_objective_redesign_execution_using_redesigned_evidence_digest']}` / `{review_package['label_objective_redesign_output_binding_digest']}` / `{review_package['label_objective_redesign_approval_using_redesigned_evidence_digest']}`.",
        "",
        "## Dataset and Universe",
        f"- `{review_package['dataset_name']}` has `{review_package['total_canonical_record_count']}` frozen records for 12 ordered tickers; META remains `{review_package['meta_record_count']}`.",
        "",
        "## Reviewed Candidate Basis",
        f"- Selected direction: `{review_package['selected_direction']}`; every source design choice still requires separately governed operator selection.",
        "",
        "## Reviewed Candidate Objective",
        f"- `{review_package['improved_evidence_planning_candidate_objective']}` / `{review_package['improved_evidence_planning_candidate_scope']}` / `{review_package['improved_evidence_planning_candidate_mode']}`.",
        "",
        "## Reviewed Improved Evidence Themes",
    ]
    lines.extend(
        f"- `{row['theme_id']}`: `{row['theme_status']}`."
        for row in review_package["reviewed_improved_evidence_themes"]
    )
    lines.extend(["", "## Reviewed Planned Evidence Components"])
    lines.extend(
        f"- `{row['component_id']}`: `{row['component_status']}`."
        for row in review_package["reviewed_planned_evidence_components"]
    )
    lines.extend(["", "## Reviewed Planned Data Products"])
    lines.extend(
        f"- `{row['data_product_id']}`: `{row['output_status']}`."
        for row in review_package["reviewed_planned_data_products"]
    )
    lines.extend(["", "## Reviewed Planned Future Outputs"])
    lines.extend(
        f"- `{row['future_output_id']}`: `{row['output_status']}`."
        for row in review_package["reviewed_planned_future_outputs"]
    )
    lines.extend(
        [
            "",
            "## Per-Ticker Review Entries",
            "- Twelve candidate- and review-digest-bound entries preserve registry order; META remains 913 and every other ticker remains 1003.",
            "",
            "## Next Chain",
        ]
    )
    lines.extend(
        f"{index}. {item}"
        for index, item in enumerate(review_package["reviewed_next_chain"], 1)
    )
    lines.extend(["", "## Next Gates"])
    lines.extend(f"- `{item}`" for item in review_package["reviewed_next_gates"])
    lines.extend(["", "## Risk Controls"])
    lines.extend(f"- `{item}`" for item in review_package["reviewed_risk_controls"])
    lines.extend(
        [
            "",
            "## Predictive Usefulness Boundary",
            "- Predictive usefulness remains `not accepted`; this review creates no readiness or acceptance candidate.",
            "",
            "## Profitability Boundary",
            "- Profitability remains `not accepted`.",
            "",
            "## Runtime Boundary",
            "- Runtime, strategy, paper trading, and broker execution remain `NOT_AUTHORIZED`.",
            "",
            "## Checklist Summary",
            f"- Total/passed/failed/blockers: `{summary['total_checks']}` / `{summary['passed_checks']}` / `{summary['failed_checks']}` / `{summary['blocker_count']}`.",
            "",
            "## Guardrails",
            "- This package reviews a planning candidate only. It selects, approves, authorizes, and executes nothing; it creates no label, target, feature, matrix, metric, model, predictive evidence, runtime action, recommendation, or trade.",
            "",
        ]
    )
    return "\n".join(lines)


def write_improved_evidence_planning_candidate_using_redesigned_evidence_review_package_v1(
    output_dir: str | Path,
    *,
    candidate: dict | None = None,
    filename: str | None = None,
) -> dict:
    """Write one canonical review package without overwriting."""
    review_package = build_improved_evidence_planning_candidate_using_redesigned_evidence_review_package_v1(
        candidate
    )
    output_name = filename or (
        "improved_evidence_planning_candidate_using_redesigned_evidence_review_v1.json"
    )
    if Path(output_name).name != output_name or not output_name.endswith(".json"):
        raise ImprovedEvidencePlanningCandidateRedesignedEvidenceOperatorReviewError(
            "review filename must be a simple JSON filename"
        )
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / output_name
    payload = canonical_json_bytes(review_package)
    try:
        with path.open("xb") as handle:
            handle.write(payload)
    except FileExistsError as exc:
        raise ImprovedEvidencePlanningCandidateRedesignedEvidenceOperatorReviewError(
            "review output already exists"
        ) from exc
    return {
        "path": str(path).replace("\\", "/"),
        "filename": path.name,
        "payload_byte_size": len(payload),
        "payload_sha256": sha256_bytes(payload),
        "review_status": review_package["review_status"],
        "improved_evidence_planning_candidate_using_redesigned_evidence_review_package_digest": review_package[
            "improved_evidence_planning_candidate_using_redesigned_evidence_review_package_digest"
        ],
    }
