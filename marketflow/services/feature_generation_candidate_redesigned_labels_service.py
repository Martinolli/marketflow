"""Offline feature-generation candidate using reviewed redesigned labels."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from marketflow.historical_data.artifacts import (
    canonical_json_bytes,
    semantic_digest,
    sha256_bytes,
)


ARTIFACT_KIND_FEATURE_GENERATION_CANDIDATE_USING_REDESIGNED_LABELS = (
    "FEATURE_GENERATION_CANDIDATE_USING_REDESIGNED_LABELS"
)
SCHEMA_VERSION_FEATURE_GENERATION_CANDIDATE_USING_REDESIGNED_LABELS_V1 = (
    "feature_generation_candidate_using_redesigned_labels_v1"
)
FEATURE_GENERATION_CANDIDATE_USING_REDESIGNED_LABELS_READY_FOR_OPERATOR_REVIEW = (
    "FEATURE_GENERATION_CANDIDATE_USING_REDESIGNED_LABELS_READY_FOR_OPERATOR_REVIEW"
)
FEATURE_GENERATION_CANDIDATE_USING_REDESIGNED_LABELS_VALID = (
    "FEATURE_GENERATION_CANDIDATE_USING_REDESIGNED_LABELS_VALID"
)

DEFAULT_BRANCH = "feature/feature-generation-candidate-redesigned-labels-v1"
DEFAULT_BASE_COMMIT = "e66380b10d49aa45dacc77097d3b641f565e2b69"

EXPECTED_PLANNING_APPROVAL_DIGEST = (
    "6f4c1ce989e76e2b2ee835056e146f362b6d7c70b44bb6fc864f3f125c9dc54d"
)
EXPECTED_PLANNING_CANDIDATE_REVIEW_DIGEST = (
    "82495e036e79777e6cb69935f98051e76c7b7296254cb82990e34217a82a67e8"
)
EXPECTED_PLANNING_CANDIDATE_DIGEST = (
    "6de09ba499a262d6c7a1e5a0a69fee875c855bed86b78f28db4e099109a78251"
)
EXPECTED_RESULTS_REVIEW_DIGEST = (
    "f596d19db635735137c5d7073675a52b51444fa90d6a3acf09cc2aa0bc4ddd42"
)
EXPECTED_EXECUTION_DIGEST = (
    "0c1151794d913ead1653e5641e70f731932da2e9059dd534a14eec0ca5307506"
)
EXPECTED_APPROVAL_DIGEST = (
    "280734ff469c4bfb07f67060e8077b173e034fa9b9dd6b7e82225eb881337247"
)
EXPECTED_RESEARCH_REGISTRY_DIGEST = (
    "5f0ce29bd06f1a0d5f1ce3dd8e31b8c8e52d616673f119326377538228d3d958"
)
EXPECTED_RECORDS_DIGEST = (
    "fbd7c1b17b42e5d4f82a9162b31b45fdfeef46f0e9ee7d29d74c926f0cf19044"
)
EXPECTED_LABEL_VALUES_DIGEST = (
    "2de373ca60ef8ec47b500444784d9851908b9a90837aa937c3716ade589f849f"
)

TARGET_UNIVERSE = [
    "MSFT",
    "NVDA",
    "AMZN",
    "GOOGL",
    "META",
    "TSLA",
    "JPM",
    "XOM",
    "JNJ",
    "WMT",
    "CAT",
    "LMT",
]
EXPECTED_RECORD_COUNTS = {ticker: (913 if ticker == "META" else 1003) for ticker in TARGET_UNIVERSE}

NOT_ACCEPTED = "not accepted"
NOT_AUTHORIZED = "NOT_AUTHORIZED"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"
PLANNED_NOT_GENERATED = "PLANNED_NOT_GENERATED"
PLANNED_NOT_EXECUTED = "PLANNED_NOT_EXECUTED"
PLANNED_READY_FOR_OPERATOR_REVIEW = "PLANNED_READY_FOR_OPERATOR_REVIEW"
SOURCE_REVIEWED_NOT_REGENERATED = "SOURCE_REVIEWED_NOT_REGENERATED"
RESEARCH_ONLY_NON_ACTIONABLE = "RESEARCH_ONLY_NON_ACTIONABLE"

FEATURE_GENERATION_CANDIDATE_OBJECTIVE = (
    "PREPARE_FEATURE_GENERATION_CANDIDATE_USING_REDESIGNED_LABELS"
)
FEATURE_GENERATION_CANDIDATE_SCOPE = "CANDIDATE_ONLY_NOT_APPROVAL_NOT_GENERATION"
FEATURE_GENERATION_CANDIDATE_MODE = PLANNED_NOT_GENERATED
FEATURE_GENERATION_CANDIDATE_AUTHORITY_STATUS = NOT_AUTHORIZED

SOURCE_INPUT_IDS = [
    "expanded_universe_canonical_dataset_v1",
    "redesigned_label_generation_results_review_package",
    "redesigned_label_values",
    "redesigned_label_family_coverage_report",
    "redesigned_threshold_generation_report",
    "redesigned_horizon_generation_report",
    "redesigned_label_availability_report",
    "per_ticker_redesigned_label_summary",
    "meta_limitation_preservation_report",
    "feature_predictive_evidence_planning_approval_using_redesigned_labels",
]

PLANNED_FEATURE_FAMILY_IDS = [
    "FEATURE_FAMILY_OHLCV_RETURNS_AND_RANGES",
    "FEATURE_FAMILY_VOLUME_PRICE_ANALYSIS",
    "FEATURE_FAMILY_VOLATILITY_AND_REALIZED_RANGE",
    "FEATURE_FAMILY_MOMENTUM_AND_TREND",
    "FEATURE_FAMILY_RELATIVE_STRENGTH_AND_CROSS_SECTIONAL_CONTEXT",
    "FEATURE_FAMILY_CALENDAR_AND_SESSION_CONTEXT",
    "FEATURE_FAMILY_LABEL_ALIGNED_HORIZON_CONTEXT",
    "FEATURE_FAMILY_QUALITY_MISSINGNESS_AND_META_LIMITATION_FLAGS",
    "FEATURE_FAMILY_REGIME_AND_INTERACTION_TERMS",
    "FEATURE_FAMILY_BASELINE_ERROR_CONTEXT",
]

FEATURE_GROUPS_BY_FAMILY = {
    "FEATURE_FAMILY_OHLCV_RETURNS_AND_RANGES": [
        ("ohlcv_return_lags", True, "Lagged close-to-close returns using history only."),
        ("ohlcv_range_features", True, "Historical OHLC range and gap designs."),
    ],
    "FEATURE_FAMILY_VOLUME_PRICE_ANALYSIS": [
        ("volume_effort_features", True, "Historical volume effort and normalization designs."),
        ("price_volume_spread_features", True, "Historical price-volume spread designs."),
    ],
    "FEATURE_FAMILY_VOLATILITY_AND_REALIZED_RANGE": [
        ("realized_volatility_windows", True, "Trailing realized-volatility window designs."),
    ],
    "FEATURE_FAMILY_MOMENTUM_AND_TREND": [
        ("momentum_return_windows", True, "Trailing momentum return window designs."),
        ("trend_slope_candidates", True, "History-only trend slope candidates."),
    ],
    "FEATURE_FAMILY_RELATIVE_STRENGTH_AND_CROSS_SECTIONAL_CONTEXT": [
        ("relative_strength_to_universe_median", True, "Same-date historical-universe relative strength."),
        ("cross_sectional_rank_candidates", True, "Same-date cross-sectional rank designs."),
    ],
    "FEATURE_FAMILY_CALENDAR_AND_SESSION_CONTEXT": [
        ("calendar_month_weekday_features", False, "Calendar fields derived from the feature date."),
        ("session_sequence_features", False, "Session sequence fields without forward information."),
    ],
    "FEATURE_FAMILY_LABEL_ALIGNED_HORIZON_CONTEXT": [
        ("label_horizon_alignment_flags", True, "Metadata-only horizon alignment flags."),
        ("label_family_alignment_flags", True, "Metadata-only label-family alignment flags."),
    ],
    "FEATURE_FAMILY_QUALITY_MISSINGNESS_AND_META_LIMITATION_FLAGS": [
        ("missingness_indicators", False, "Source-observation availability indicators."),
        ("meta_limitation_flag", False, "Preserves META's reduced 913-record limitation."),
    ],
    "FEATURE_FAMILY_REGIME_AND_INTERACTION_TERMS": [
        ("regime_interaction_candidates", True, "History-only regime interaction designs."),
    ],
    "FEATURE_FAMILY_BASELINE_ERROR_CONTEXT": [
        ("baseline_error_context_candidates", True, "Training-partition-only baseline-error context."),
    ],
}
PLANNED_FEATURE_GROUP_IDS = [
    group_id
    for family_id in PLANNED_FEATURE_FAMILY_IDS
    for group_id, _leakage_sensitive, _design_note in FEATURE_GROUPS_BY_FAMILY[family_id]
]

FEATURE_SCHEMA_FIELDS = [
    "ticker",
    "date",
    "record_index_for_ticker",
    "window_partition",
    "feature_family",
    "feature_group",
    "feature_name",
    "feature_value",
    "feature_available",
    "availability_reason",
    "source_history_window",
    "label_family_alignment",
    "label_horizon_alignment",
    "meta_reduced_record_count_flag",
    "research_only",
    "non_actionable",
]

ALIGNMENT_CONTROL_IDS = [
    "features_use_history_only",
    "future_labels_not_used_as_features",
    "forward_return_values_not_used_as_features",
    "threshold_values_used_only_as label_metadata_not_predictor unless separately approved",
    "feature_date_must_not_peek_forward",
    "chronological_split_preserved",
    "training_threshold_fit_not_recomputed",
    "redesigned_labels_bound_by_digest",
    "meta_limitation_flag_carried_forward",
    "unavailable_label_rows_preserved",
]

PLANNED_QUALITY_CHECK_IDS = [
    "records_digest_verification",
    "label_values_digest_verification",
    "target_universe_order_verification",
    "meta_record_count_verification",
    "feature_row_count_expectation_review",
    "feature_null_policy_review",
    "feature_leakage_control_review",
    "feature_label_alignment_review",
    "feature_schema_contract_review",
    "operator_review_summary",
]

PLANNED_OUTPUT_IDS = [
    "feature_generation_candidate_manifest",
    "source_data_and_label_binding_manifest",
    "planned_feature_family_matrix",
    "planned_feature_group_matrix",
    "planned_feature_schema_contract",
    "planned_feature_label_alignment_controls",
    "planned_feature_quality_checklist",
    "per_ticker_feature_generation_plan",
    "meta_limitation_feature_handling_plan",
    "operator_review_summary_template",
]

FUTURE_CHAIN = [
    "Feature Generation Candidate Operator Review Package Using Redesigned Labels v1.",
    "Feature Generation Approval Using Redesigned Labels v1, if selected.",
    "Feature Generation Execution Using Redesigned Labels v1.",
    "Feature Generation Results Review Using Redesigned Labels v1.",
    "Additional Predictive Evidence Execution Candidate Using Redesigned Labels v1.",
    "Additional Predictive Evidence Execution Approval and Execution, if separately approved.",
    "Additional Predictive Evidence Results Review.",
    "Predictive Usefulness Reassessment and Acceptance Readiness Review.",
    "Predictive Usefulness Acceptance Candidate, only if readiness passes.",
    "Profitability review chain, if separately required.",
    "Runtime migration chain, if ever separately authorized.",
]

FUTURE_GATES = [
    "feature_generation_candidate_operator_review_using_redesigned_labels",
    "feature_generation_approval_using_redesigned_labels_if_selected",
    "feature_generation_execution_using_redesigned_labels",
    "feature_generation_results_review_using_redesigned_labels",
    "additional_predictive_evidence_execution_candidate_using_redesigned_labels",
    "additional_predictive_evidence_execution_approval_if_required",
    "additional_predictive_evidence_execution_if_approved",
    "additional_predictive_evidence_results_review",
    "predictive_usefulness_reassessment_after_new_evidence",
    "predictive_usefulness_acceptance_readiness_after_new_evidence",
    "predictive_usefulness_acceptance_candidate_if_ready",
    "profitability_review_chain_if_required",
    "runtime_migration_chain_if_ever_authorized",
]

RISK_CONTROLS = [
    "candidate_does_not_generate_features",
    "candidate_does_not_authorize_feature_generation",
    "candidate_does_not_execute_predictive_evidence",
    "candidate_does_not_train_models",
    "candidate_does_not_recompute_metrics",
    "candidate_does_not_accept_predictive_usefulness",
    "candidate_does_not_accept_profitability",
    "candidate_does_not_authorize_runtime",
    "candidate_does_not_authorize_strategy",
    "candidate_does_not_authorize_paper_trading",
    "candidate_does_not_authorize_broker_execution",
    "candidate_does_not_generate_trade_recommendations",
    "do_not_mutate_frozen_dataset",
    "do_not_mutate_redesigned_label_outputs",
    "preserve_meta_record_limitation",
    "no_predictive_execution_without_operator_approval",
    "acceptance_candidate_not_allowed_currently",
    "all_outputs_research_only",
]


class FeatureGenerationCandidateRedesignedLabelsError(ValueError):
    """Raised when the candidate violates its frozen, non-authorizing contract."""


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise FeatureGenerationCandidateRedesignedLabelsError(f"{field} mismatch")


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


def _source_inputs() -> list[dict[str, Any]]:
    return [
        {
            "source_input_id": source_input_id,
            "source_input_status": SOURCE_REVIEWED_NOT_REGENERATED,
            "output_label": RESEARCH_ONLY_NON_ACTIONABLE,
            "research_only": True,
            "non_actionable": True,
        }
        for source_input_id in SOURCE_INPUT_IDS
    ]


def _feature_groups_for_family(family_id: str) -> list[dict[str, Any]]:
    return [
        {
            "feature_group_id": group_id,
            "design_note": design_note,
            "group_status": PLANNED_NOT_GENERATED,
            "feature_generation_authorized": False,
            "feature_generation_performed": False,
            "feature_values_created": False,
            "leakage_sensitive": leakage_sensitive,
            "research_only": True,
            "non_actionable": True,
        }
        for group_id, leakage_sensitive, design_note in FEATURE_GROUPS_BY_FAMILY[family_id]
    ]


def _feature_families() -> list[dict[str, Any]]:
    return [
        {
            "feature_family_id": family_id,
            "feature_generation_candidate_status": PLANNED_READY_FOR_OPERATOR_REVIEW,
            "feature_generation_authorized": False,
            "feature_generation_performed": False,
            "feature_values_created": False,
            "research_only": True,
            "non_actionable": True,
            "planned_feature_groups": _feature_groups_for_family(family_id),
        }
        for family_id in PLANNED_FEATURE_FAMILY_IDS
    ]


def _feature_schema_contract() -> dict[str, Any]:
    return {
        "feature_schema_contract_status": PLANNED_NOT_GENERATED,
        "planned_schema_fields": list(FEATURE_SCHEMA_FIELDS),
        "feature_values_created": False,
        "research_only": True,
        "non_actionable": True,
    }


def _alignment_controls() -> list[dict[str, Any]]:
    return [
        {
            "control_id": control_id,
            "control_status": "PLANNED_FOR_OPERATOR_REVIEW",
            "execution_status": "NOT_EXECUTED",
            "research_only": True,
            "non_actionable": True,
        }
        for control_id in ALIGNMENT_CONTROL_IDS
    ]


def _quality_checks() -> list[dict[str, Any]]:
    return [
        {
            "planned_check_id": check_id,
            "planned_check_status": PLANNED_NOT_EXECUTED,
            "research_only": True,
            "non_actionable": True,
        }
        for check_id in PLANNED_QUALITY_CHECK_IDS
    ]


def _planned_outputs() -> list[dict[str, Any]]:
    return [
        {
            "planned_output_id": output_id,
            "output_status": PLANNED_NOT_GENERATED,
            "output_label": RESEARCH_ONLY_NON_ACTIONABLE,
            "generated": False,
            "research_only": True,
            "non_actionable": True,
        }
        for output_id in PLANNED_OUTPUT_IDS
    ]


def _per_ticker_digest_payload(entry: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(entry)
    payload.pop("per_ticker_feature_generation_candidate_digest", None)
    return payload


def per_ticker_feature_generation_candidate_digest_v1(entry: dict[str, Any]) -> str:
    """Return the deterministic digest for one ticker's feature plan."""
    return semantic_digest(_per_ticker_digest_payload(entry))


def _per_ticker_entries() -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for ticker in TARGET_UNIVERSE:
        is_meta = ticker == "META"
        entry = {
            "ticker": ticker,
            "registry_approval_status": "APPROVED_FOR_RESEARCH_REGISTRY_ONLY",
            "canonical_dataset_status": "FROZEN",
            "historical_record_count": EXPECTED_RECORD_COUNTS[ticker],
            "meta_reduced_record_count_flag": is_meta,
            "redesigned_label_generation_results_status": "REVIEWED_RESEARCH_ONLY",
            "feature_predictive_evidence_planning_approval_status": "APPROVED_FOR_FUTURE_FEATURE_GENERATION_CANDIDATE_ONLY",
            "feature_generation_candidate_status": PLANNED_READY_FOR_OPERATOR_REVIEW,
            "feature_generation_authorized": False,
            "feature_generation_performed": False,
            "feature_values_created": False,
            "predictive_evidence_execution_authorized": False,
            "predictive_evidence_execution_performed": False,
            "predictive_usefulness": NOT_ACCEPTED,
            "predictive_usefulness_acceptance_candidate_created": False,
            "profitability": NOT_ACCEPTED,
            "runtime_use": NOT_AUTHORIZED,
            "strategy_use": NOT_AUTHORIZED,
            "paper_trading": NOT_AUTHORIZED,
            "broker_execution": NOT_AUTHORIZED,
            "source_feature_predictive_evidence_planning_approval_digest": EXPECTED_PLANNING_APPROVAL_DIGEST,
            "source_redesigned_label_generation_results_review_digest": EXPECTED_RESULTS_REVIEW_DIGEST,
        }
        if is_meta:
            entry["planning_note"] = (
                "PRESERVE_META_LIMITATION_IN_FEATURE_GENERATION_CANDIDATE"
            )
        entry["per_ticker_feature_generation_candidate_digest"] = (
            per_ticker_feature_generation_candidate_digest_v1(entry)
        )
        entries.append(entry)
    return entries


CHECK_FIELD_SPECS = [
    ("feature_predictive_evidence_planning_approval_digest_bound", EXPECTED_PLANNING_APPROVAL_DIGEST, "feature_predictive_evidence_planning_approval_using_redesigned_labels_digest"),
    ("planning_candidate_review_digest_bound", EXPECTED_PLANNING_CANDIDATE_REVIEW_DIGEST, "feature_predictive_evidence_planning_candidate_using_redesigned_labels_review_package_digest"),
    ("redesigned_label_results_review_digest_bound", EXPECTED_RESULTS_REVIEW_DIGEST, "redesigned_label_generation_results_review_package_digest"),
    ("label_values_digest_bound", EXPECTED_LABEL_VALUES_DIGEST, "label_values_digest"),
    ("research_registry_digest_bound", EXPECTED_RESEARCH_REGISTRY_DIGEST, "research_registry_approval_digest"),
    ("records_digest_bound", EXPECTED_RECORDS_DIGEST, "records_digest"),
    ("target_universe_12_preserved", TARGET_UNIVERSE, "target_universe"),
    ("records_digest_preserved", EXPECTED_RECORDS_DIGEST, "records_digest"),
    ("meta_913_preserved", 913, "meta_record_count"),
    ("feature_predictive_evidence_planning_approved_true", True, "feature_predictive_evidence_planning_approved"),
    ("ready_for_feature_generation_candidate_true", True, "ready_for_feature_generation_candidate_using_redesigned_labels"),
    ("ready_for_additional_predictive_evidence_execution_candidate_false", False, "ready_for_additional_predictive_evidence_execution_candidate_using_redesigned_labels"),
    ("feature_generation_candidate_created_true", True, "feature_generation_candidate_created"),
    ("feature_generation_candidate_ready_for_operator_review_true", True, "feature_generation_candidate_using_redesigned_labels_ready_for_operator_review"),
    ("feature_generation_authorized_false", False, "feature_generation_authorized"),
    ("feature_generation_performed_false", False, "feature_generation_performed"),
    ("feature_values_created_false", False, "feature_values_created"),
    ("planned_feature_families_10", PLANNED_FEATURE_FAMILY_IDS, "planned_feature_family_ids"),
    ("planned_feature_groups_defined", PLANNED_FEATURE_GROUP_IDS, "planned_feature_group_ids"),
    ("planned_feature_schema_contract_defined", FEATURE_SCHEMA_FIELDS, "planned_feature_schema_fields"),
    ("planned_alignment_controls_defined", ALIGNMENT_CONTROL_IDS, "alignment_control_ids"),
    ("planned_quality_checks_defined", PLANNED_QUALITY_CHECK_IDS, "planned_quality_check_ids"),
    ("planned_outputs_not_generated", True, "planned_outputs_not_generated"),
    ("planned_outputs_research_only", True, "planned_outputs_research_only"),
    ("per_ticker_entries_12", 12, "per_ticker_entry_count"),
    ("per_ticker_digests_present", True, "per_ticker_digests_valid"),
    ("metric_recomputation_false", False, "metric_recomputation_performed"),
    ("model_training_false", False, "model_training_performed"),
    ("additional_predictive_evidence_execution_candidate_created_false", False, "additional_predictive_evidence_execution_candidate_created"),
    ("predictive_usefulness_not_accepted", NOT_ACCEPTED, "predictive_usefulness"),
    ("profitability_not_accepted", NOT_ACCEPTED, "profitability"),
    ("runtime_not_authorized", NOT_AUTHORIZED, "runtime_use"),
    ("strategy_not_authorized", NOT_AUTHORIZED, "strategy_use"),
    ("broker_not_authorized", NOT_AUTHORIZED, "broker_execution"),
    ("trade_recommendations_false", False, "trade_recommendations_generated"),
    ("provider_requests_made_false", False, "provider_requests_made"),
    ("market_data_acquisition_false", False, "market_data_acquisition_performed"),
    ("dataset_regeneration_false", False, "dataset_regeneration_performed"),
    ("redesigned_label_regeneration_false", False, "redesigned_label_regeneration_performed"),
    ("feature_generation_false", False, "feature_generation_performed"),
    ("no_predictive_usefulness_acceptance_artifact_created", False, "predictive_usefulness_acceptance_artifact_created"),
    ("no_profitability_acceptance_created", False, "profitability_acceptance_created"),
    ("no_runtime_migration_approval_created", False, "runtime_migration_approval_created"),
    ("future_chain_defined", FUTURE_CHAIN, "future_chain"),
    ("future_gates_defined", FUTURE_GATES, "future_gates"),
    ("risk_controls_defined", RISK_CONTROLS, "risk_controls"),
    ("no_tracked_marketflow_files", True, "no_tracked_marketflow_files"),
]
REQUIRED_CHECK_IDS = [spec[0] for spec in CHECK_FIELD_SPECS]


def _derived_check_fields(candidate: dict[str, Any]) -> dict[str, Any]:
    families = candidate.get("planned_feature_families", [])
    groups = [
        group
        for family in families
        for group in family.get("planned_feature_groups", [])
    ] if isinstance(families, list) else []
    schema = candidate.get("planned_feature_schema_contract", {})
    controls = candidate.get("planned_feature_label_alignment_controls", [])
    quality_checks = candidate.get("planned_feature_quality_checks", [])
    outputs = candidate.get("planned_outputs", [])
    entries = candidate.get("per_ticker_candidate_entries", [])
    return {
        **candidate,
        "planned_feature_family_ids": [row.get("feature_family_id") for row in families] if isinstance(families, list) else [],
        "planned_feature_group_ids": [row.get("feature_group_id") for row in groups],
        "planned_feature_schema_fields": schema.get("planned_schema_fields", []) if isinstance(schema, dict) else [],
        "alignment_control_ids": [row.get("control_id") for row in controls] if isinstance(controls, list) else [],
        "planned_quality_check_ids": [row.get("planned_check_id") for row in quality_checks] if isinstance(quality_checks, list) else [],
        "planned_outputs_not_generated": isinstance(outputs, list) and len(outputs) == len(PLANNED_OUTPUT_IDS) and all(row.get("output_status") == PLANNED_NOT_GENERATED and row.get("generated") is False for row in outputs),
        "planned_outputs_research_only": isinstance(outputs, list) and len(outputs) == len(PLANNED_OUTPUT_IDS) and all(row.get("output_label") == RESEARCH_ONLY_NON_ACTIONABLE and row.get("research_only") is True and row.get("non_actionable") is True for row in outputs),
        "per_ticker_entry_count": len(entries) if isinstance(entries, list) else 0,
        "per_ticker_digests_valid": isinstance(entries, list) and len(entries) == 12 and all(isinstance(row.get("per_ticker_feature_generation_candidate_digest"), str) and len(row["per_ticker_feature_generation_candidate_digest"]) == 64 and row["per_ticker_feature_generation_candidate_digest"] == per_ticker_feature_generation_candidate_digest_v1(row) for row in entries),
    }


def _checklist(candidate: dict[str, Any]) -> list[dict[str, Any]]:
    fields = _derived_check_fields(candidate)
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
        "feature_generation_candidate_ready": not failed,
        "ready_for_operator_review": not failed,
        "ready_for_feature_generation_approval": False,
        "features_generated": False,
        "predictive_evidence_executed": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_authorized": False,
        "trade_recommendations_generated": False,
    }


def _base_candidate() -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_FEATURE_GENERATION_CANDIDATE_USING_REDESIGNED_LABELS,
        "schema_version": SCHEMA_VERSION_FEATURE_GENERATION_CANDIDATE_USING_REDESIGNED_LABELS_V1,
        "candidate_status": FEATURE_GENERATION_CANDIDATE_USING_REDESIGNED_LABELS_READY_FOR_OPERATOR_REVIEW,
        "branch": DEFAULT_BRANCH,
        "base_commit": DEFAULT_BASE_COMMIT,
        "created_offline": True,
        "research_only": True,
        "operator_review_required": True,
        "provider_requests_made": False,
        "live_provider_transport_enabled": False,
        "market_data_acquisition_performed": False,
        "dataset_regeneration_performed": False,
        "canonical_dataset_regenerated": False,
        "redesigned_label_regeneration_performed": False,
        "raw_provider_payloads_committed": False,
        "api_keys_stored_or_printed": False,
        "feature_predictive_evidence_planning_approval_using_redesigned_labels_digest": EXPECTED_PLANNING_APPROVAL_DIGEST,
        "feature_predictive_evidence_planning_candidate_using_redesigned_labels_review_package_digest": EXPECTED_PLANNING_CANDIDATE_REVIEW_DIGEST,
        "feature_predictive_evidence_planning_candidate_using_redesigned_labels_digest": EXPECTED_PLANNING_CANDIDATE_DIGEST,
        "redesigned_label_generation_results_review_package_digest": EXPECTED_RESULTS_REVIEW_DIGEST,
        "redesigned_label_generation_execution_digest": EXPECTED_EXECUTION_DIGEST,
        "redesigned_label_generation_approval_digest": EXPECTED_APPROVAL_DIGEST,
        "research_registry_approval_digest": EXPECTED_RESEARCH_REGISTRY_DIGEST,
        "records_digest": EXPECTED_RECORDS_DIGEST,
        "label_values_digest": EXPECTED_LABEL_VALUES_DIGEST,
        "feature_predictive_evidence_planning_approved": True,
        "feature_predictive_evidence_planning_approval_created": True,
        "ready_for_feature_generation_candidate_using_redesigned_labels": True,
        "ready_for_additional_predictive_evidence_execution_candidate_using_redesigned_labels": False,
        "feature_generation_candidate_created": True,
        "feature_generation_candidate_using_redesigned_labels_created": True,
        "feature_generation_candidate_using_redesigned_labels_ready_for_operator_review": True,
        "feature_generation_candidate_using_redesigned_labels_review_created": False,
        "feature_generation_authorized": False,
        "feature_generation_performed": False,
        "redesigned_feature_generation_authorized": False,
        "redesigned_feature_generation_performed": False,
        "feature_values_created": False,
        "additional_predictive_evidence_execution_candidate_created": False,
        "additional_predictive_evidence_execution_authorized": False,
        "additional_predictive_evidence_executed": False,
        "metric_recomputation_performed": False,
        "model_training_performed": False,
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
        "predictive_usefulness_acceptance_artifact_created": False,
        "profitability_acceptance_created": False,
        "runtime_migration_approval_created": False,
        "no_tracked_marketflow_files": True,
        "dataset_name": "expanded_universe_canonical_dataset_v1",
        "source_profile": "RTH_FULL_SESSION_1D",
        "timeframe": "1d",
        "date_range_start": "2022-01-01",
        "date_range_end": "2025-12-31",
        "target_universe": list(TARGET_UNIVERSE),
        "target_universe_count": 12,
        "total_canonical_record_count": 11946,
        "per_ticker_record_counts": dict(EXPECTED_RECORD_COUNTS),
        "meta_record_count": 913,
        "non_meta_record_count": 1003,
        "meta_reduced_record_count_preserved": True,
        "redesigned_label_output_count": 11,
        "redesigned_label_output_status": "REVIEWED_AND_VERIFIED",
        "label_family_count": 10,
        "threshold_strategy_count": 7,
        "horizon_strategy_count": 5,
        "label_value_row_count": 143352,
        "label_family_coverage_entries": 144,
        "available_label_value_count": 142200,
        "unavailable_label_value_count": 1152,
        "feature_generation_candidate_objective": FEATURE_GENERATION_CANDIDATE_OBJECTIVE,
        "feature_generation_candidate_scope": FEATURE_GENERATION_CANDIDATE_SCOPE,
        "feature_generation_candidate_mode": FEATURE_GENERATION_CANDIDATE_MODE,
        "feature_generation_candidate_authority_status": FEATURE_GENERATION_CANDIDATE_AUTHORITY_STATUS,
        "source_inputs": _source_inputs(),
        "planned_feature_families": _feature_families(),
        "planned_feature_schema_contract": _feature_schema_contract(),
        "planned_feature_label_alignment_controls": _alignment_controls(),
        "planned_feature_quality_checks": _quality_checks(),
        "planned_outputs": _planned_outputs(),
        "per_ticker_candidate_entries": _per_ticker_entries(),
        "future_chain": list(FUTURE_CHAIN),
        "future_gates": list(FUTURE_GATES),
        "risk_controls": list(RISK_CONTROLS),
    }


def _digest_payload(candidate: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(candidate)
    payload.pop("feature_generation_candidate_using_redesigned_labels_digest", None)
    return payload


def feature_generation_candidate_using_redesigned_labels_digest_v1(
    candidate: dict[str, Any],
) -> str:
    """Return the deterministic semantic digest for the candidate."""
    return semantic_digest(_digest_payload(candidate))


def build_feature_generation_candidate_using_redesigned_labels_v1() -> dict[str, Any]:
    """Build the candidate from committed reviewed facts without I/O or execution."""
    candidate = _base_candidate()
    candidate["candidate_checklist"] = _checklist(candidate)
    candidate["candidate_summary"] = _summary(candidate["candidate_checklist"])
    candidate["feature_generation_candidate_using_redesigned_labels_digest"] = (
        feature_generation_candidate_using_redesigned_labels_digest_v1(candidate)
    )
    validate_feature_generation_candidate_using_redesigned_labels_v1(candidate)
    return candidate


def _reject_forbidden_values(value: Any, *, path: str = "candidate") -> None:
    forbidden_artifacts = {
        "FEATURE_GENERATION_CANDIDATE_REVIEW_PACKAGE",
        "FEATURE_GENERATION_APPROVED",
        "FEATURE_GENERATION_EXECUTED",
        "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE",
        "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED",
        "PREDICTIVE_USEFULNESS_REASSESSMENT_REVIEW_PACKAGE",
        "PREDICTIVE_USEFULNESS_ACCEPTANCE_CANDIDATE",
        "PREDICTIVE_USEFULNESS_ACCEPTED",
        "PROFITABILITY_ACCEPTED",
        "RUNTIME_MIGRATION_APPROVED",
        "RUNTIME_MIGRATION_ACTIVE",
        "STRATEGY_RUNTIME_MIGRATION",
        "TRADE_RECOMMENDATIONS",
    }
    forbidden_true = {
        "feature_generation_authorized",
        "feature_generation_performed",
        "redesigned_feature_generation_authorized",
        "redesigned_feature_generation_performed",
        "feature_values_created",
        "additional_predictive_evidence_execution_candidate_created",
        "additional_predictive_evidence_execution_authorized",
        "additional_predictive_evidence_executed",
        "metric_recomputation_performed",
        "model_training_performed",
        "runtime_migration_approved",
        "runtime_migration_active",
        "new_strategy_scoring_performed",
        "trade_recommendations_generated",
        "predictive_usefulness_acceptance_candidate_created",
        "profitability_acceptance_ready",
        "profitability_acceptance_recommended",
    }
    if isinstance(value, dict):
        for key, item in value.items():
            if key in forbidden_true and item is True:
                raise FeatureGenerationCandidateRedesignedLabelsError(
                    f"{path}.{key} must remain false"
                )
            _reject_forbidden_values(item, path=f"{path}.{key}")
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _reject_forbidden_values(item, path=f"{path}[{index}]")
    elif isinstance(value, str):
        if value in forbidden_artifacts:
            raise FeatureGenerationCandidateRedesignedLabelsError(
                f"{path} contains forbidden downstream artifact"
            )
        if value == "accepted":
            raise FeatureGenerationCandidateRedesignedLabelsError(
                f"{path} must not accept predictive usefulness or profitability"
            )
        if value == "AUTHORIZED":
            raise FeatureGenerationCandidateRedesignedLabelsError(
                f"{path} must not grant runtime or trading authority"
            )


def validate_feature_generation_candidate_using_redesigned_labels_v1(
    candidate: dict,
) -> dict[str, Any]:
    """Fail closed unless the object is exactly the offline candidate contract."""
    if not isinstance(candidate, dict):
        raise FeatureGenerationCandidateRedesignedLabelsError(
            "candidate must be a JSON object"
        )
    _expect(candidate.get("artifact_kind"), ARTIFACT_KIND_FEATURE_GENERATION_CANDIDATE_USING_REDESIGNED_LABELS, "artifact_kind")
    _expect(candidate.get("schema_version"), SCHEMA_VERSION_FEATURE_GENERATION_CANDIDATE_USING_REDESIGNED_LABELS_V1, "schema_version")
    _expect(candidate.get("candidate_status"), FEATURE_GENERATION_CANDIDATE_USING_REDESIGNED_LABELS_READY_FOR_OPERATOR_REVIEW, "candidate_status")
    _reject_forbidden_values(candidate)
    expected = {
        "branch": DEFAULT_BRANCH,
        "base_commit": DEFAULT_BASE_COMMIT,
        "feature_predictive_evidence_planning_approval_using_redesigned_labels_digest": EXPECTED_PLANNING_APPROVAL_DIGEST,
        "feature_predictive_evidence_planning_candidate_using_redesigned_labels_review_package_digest": EXPECTED_PLANNING_CANDIDATE_REVIEW_DIGEST,
        "feature_predictive_evidence_planning_candidate_using_redesigned_labels_digest": EXPECTED_PLANNING_CANDIDATE_DIGEST,
        "redesigned_label_generation_results_review_package_digest": EXPECTED_RESULTS_REVIEW_DIGEST,
        "redesigned_label_generation_execution_digest": EXPECTED_EXECUTION_DIGEST,
        "redesigned_label_generation_approval_digest": EXPECTED_APPROVAL_DIGEST,
        "research_registry_approval_digest": EXPECTED_RESEARCH_REGISTRY_DIGEST,
        "records_digest": EXPECTED_RECORDS_DIGEST,
        "label_values_digest": EXPECTED_LABEL_VALUES_DIGEST,
        "dataset_name": "expanded_universe_canonical_dataset_v1",
        "source_profile": "RTH_FULL_SESSION_1D",
        "timeframe": "1d",
        "date_range_start": "2022-01-01",
        "date_range_end": "2025-12-31",
        "target_universe": TARGET_UNIVERSE,
        "target_universe_count": 12,
        "total_canonical_record_count": 11946,
        "per_ticker_record_counts": EXPECTED_RECORD_COUNTS,
        "meta_record_count": 913,
        "non_meta_record_count": 1003,
        "redesigned_label_output_count": 11,
        "redesigned_label_output_status": "REVIEWED_AND_VERIFIED",
        "label_family_count": 10,
        "threshold_strategy_count": 7,
        "horizon_strategy_count": 5,
        "label_value_row_count": 143352,
        "label_family_coverage_entries": 144,
        "available_label_value_count": 142200,
        "unavailable_label_value_count": 1152,
        "feature_generation_candidate_objective": FEATURE_GENERATION_CANDIDATE_OBJECTIVE,
        "feature_generation_candidate_scope": FEATURE_GENERATION_CANDIDATE_SCOPE,
        "feature_generation_candidate_mode": FEATURE_GENERATION_CANDIDATE_MODE,
        "feature_generation_candidate_authority_status": FEATURE_GENERATION_CANDIDATE_AUTHORITY_STATUS,
        "source_inputs": _source_inputs(),
        "planned_feature_families": _feature_families(),
        "planned_feature_schema_contract": _feature_schema_contract(),
        "planned_feature_label_alignment_controls": _alignment_controls(),
        "planned_feature_quality_checks": _quality_checks(),
        "planned_outputs": _planned_outputs(),
        "per_ticker_candidate_entries": _per_ticker_entries(),
        "future_chain": FUTURE_CHAIN,
        "future_gates": FUTURE_GATES,
        "risk_controls": RISK_CONTROLS,
    }
    for field, expected_value in expected.items():
        _expect(candidate.get(field), expected_value, field)
    true_fields = [
        "created_offline",
        "research_only",
        "operator_review_required",
        "feature_predictive_evidence_planning_approved",
        "feature_predictive_evidence_planning_approval_created",
        "ready_for_feature_generation_candidate_using_redesigned_labels",
        "feature_generation_candidate_created",
        "feature_generation_candidate_using_redesigned_labels_created",
        "feature_generation_candidate_using_redesigned_labels_ready_for_operator_review",
        "meta_reduced_record_count_preserved",
        "no_tracked_marketflow_files",
    ]
    false_fields = [
        "provider_requests_made",
        "live_provider_transport_enabled",
        "market_data_acquisition_performed",
        "dataset_regeneration_performed",
        "canonical_dataset_regenerated",
        "redesigned_label_regeneration_performed",
        "raw_provider_payloads_committed",
        "api_keys_stored_or_printed",
        "ready_for_additional_predictive_evidence_execution_candidate_using_redesigned_labels",
        "feature_generation_candidate_using_redesigned_labels_review_created",
        "feature_generation_authorized",
        "feature_generation_performed",
        "redesigned_feature_generation_authorized",
        "redesigned_feature_generation_performed",
        "feature_values_created",
        "additional_predictive_evidence_execution_candidate_created",
        "additional_predictive_evidence_execution_authorized",
        "additional_predictive_evidence_executed",
        "metric_recomputation_performed",
        "model_training_performed",
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
        "predictive_usefulness_acceptance_artifact_created",
        "profitability_acceptance_created",
        "runtime_migration_approval_created",
    ]
    for field in true_fields:
        _expect(candidate.get(field), True, field)
    for field in false_fields:
        _expect(candidate.get(field), False, field)
    _expect(candidate.get("predictive_usefulness"), NOT_ACCEPTED, "predictive_usefulness")
    _expect(candidate.get("profitability"), NOT_ACCEPTED, "profitability")
    for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
        _expect(candidate.get(field), NOT_AUTHORIZED, field)
    checklist = candidate.get("candidate_checklist")
    if not isinstance(checklist, list):
        raise FeatureGenerationCandidateRedesignedLabelsError("candidate_checklist mismatch")
    _expect([row.get("check_id") for row in checklist], REQUIRED_CHECK_IDS, "candidate_checklist check ids")
    _expect(checklist, _checklist(candidate), "candidate_checklist")
    if any(row.get("status") != PASS for row in checklist):
        raise FeatureGenerationCandidateRedesignedLabelsError(
            "candidate_checklist must pass"
        )
    _expect(candidate.get("candidate_summary"), _summary(checklist), "candidate_summary")
    digest = candidate.get("feature_generation_candidate_using_redesigned_labels_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise FeatureGenerationCandidateRedesignedLabelsError("missing candidate digest")
    _expect(digest, feature_generation_candidate_using_redesigned_labels_digest_v1(candidate), "candidate digest")
    return {
        "status": FEATURE_GENERATION_CANDIDATE_USING_REDESIGNED_LABELS_VALID,
        "artifact_kind": candidate["artifact_kind"],
        "candidate_status": candidate["candidate_status"],
        "feature_generation_candidate_using_redesigned_labels_digest": digest,
        "per_ticker_candidate_entry_count": len(candidate["per_ticker_candidate_entries"]),
        "blocker_count": candidate["candidate_summary"]["blocker_count"],
        "ready_for_operator_review": True,
        "ready_for_feature_generation_approval": False,
        "features_generated": False,
        "predictive_evidence_executed": False,
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "runtime_authorized": False,
    }


def build_feature_generation_candidate_using_redesigned_labels_markdown_v1(
    candidate: dict,
) -> str:
    """Render the candidate without implying approval or execution authority."""
    validation = validate_feature_generation_candidate_using_redesigned_labels_v1(candidate)
    summary = candidate["candidate_summary"]
    lines = [
        "# MarketFlow Feature Generation Candidate Using Redesigned Labels Status",
        "",
        "## Title",
        "- Feature Generation Candidate Using Redesigned Labels v1.",
        "",
        "## Feature Generation Candidate Using Redesigned Labels",
        f"- Artifact/status/digest: `{candidate['artifact_kind']}` / `{candidate['candidate_status']}` / `{validation['feature_generation_candidate_using_redesigned_labels_digest']}`.",
        "",
        "## Bound Evidence",
        f"- Planning approval/review/candidate: `{candidate['feature_predictive_evidence_planning_approval_using_redesigned_labels_digest']}` / `{candidate['feature_predictive_evidence_planning_candidate_using_redesigned_labels_review_package_digest']}` / `{candidate['feature_predictive_evidence_planning_candidate_using_redesigned_labels_digest']}`.",
        f"- Redesigned-label results review and label values: `{candidate['redesigned_label_generation_results_review_package_digest']}` / `{candidate['label_values_digest']}`.",
        "",
        "## Dataset and Universe",
        f"- `{candidate['dataset_name']}` contains `{candidate['total_canonical_record_count']}` frozen records for the ordered 12-ticker universe; META remains `{candidate['meta_record_count']}`.",
        "",
        "## Source Redesigned Label Profile",
        f"- Reviewed outputs/families/thresholds/horizons/rows: `{candidate['redesigned_label_output_count']}` / `{candidate['label_family_count']}` / `{candidate['threshold_strategy_count']}` / `{candidate['horizon_strategy_count']}` / `{candidate['label_value_row_count']}`.",
        "",
        "## Candidate Objective",
        f"- `{candidate['feature_generation_candidate_objective']}` / `{candidate['feature_generation_candidate_scope']}` / `{candidate['feature_generation_candidate_mode']}` / `{candidate['feature_generation_candidate_authority_status']}`.",
        "",
        "## Source Inputs",
    ]
    lines.extend(f"- `{row['source_input_id']}`: `{row['source_input_status']}`." for row in candidate["source_inputs"])
    lines.extend(["", "## Planned Feature Families"])
    lines.extend(f"- `{row['feature_family_id']}`: `{row['feature_generation_candidate_status']}`." for row in candidate["planned_feature_families"])
    lines.extend(["", "## Planned Feature Groups"])
    for family in candidate["planned_feature_families"]:
        lines.extend(f"- `{group['feature_group_id']}`: `{group['group_status']}`." for group in family["planned_feature_groups"])
    lines.extend(["", "## Planned Feature Schema Contract", f"- Status: `{candidate['planned_feature_schema_contract']['feature_schema_contract_status']}`; `{len(candidate['planned_feature_schema_contract']['planned_schema_fields'])}` fields are planned and no values exist."])
    lines.extend(["", "## Planned Feature / Label Alignment Controls"])
    lines.extend(f"- `{row['control_id']}`: `{row['execution_status']}`." for row in candidate["planned_feature_label_alignment_controls"])
    lines.extend(["", "## Planned Quality Checks"])
    lines.extend(f"- `{row['planned_check_id']}`: `{row['planned_check_status']}`." for row in candidate["planned_feature_quality_checks"])
    lines.extend(["", "## Per-Ticker Candidate Entries", "- Twelve deterministic entries preserve exact registry order and source digests; META remains 913 records and all other tickers remain 1003.", "", "## Future Chain"])
    lines.extend(f"{index}. {item}" for index, item in enumerate(candidate["future_chain"], 1))
    lines.extend(["", "## Future Gates"])
    lines.extend(f"- `{item}`" for item in candidate["future_gates"])
    lines.extend(["", "## Risk Controls"])
    lines.extend(f"- `{item}`" for item in candidate["risk_controls"])
    lines.extend([
        "",
        "## Checklist Summary",
        f"- Total/passed/failed/blockers: `{summary['total_checks']}` / `{summary['passed_checks']}` / `{summary['failed_checks']}` / `{summary['blocker_count']}`.",
        "",
        "## Guardrails",
        "- This candidate is research-only and design-only. It creates no feature values and grants no feature-generation, predictive-evidence, model-training, acceptance, profitability, runtime, strategy, paper-trading, broker, or recommendation authority.",
        "- Operator review and separate approval remain required before any feature-generation execution.",
        "",
    ])
    return "\n".join(lines)


def write_feature_generation_candidate_using_redesigned_labels_v1(
    output_dir: str | Path,
    *,
    filename: str | None = None,
) -> dict[str, Any]:
    """Write one canonical candidate without overwriting an existing file."""
    candidate = build_feature_generation_candidate_using_redesigned_labels_v1()
    output_name = filename or "feature_generation_candidate_using_redesigned_labels_v1.json"
    if Path(output_name).name != output_name or not output_name.endswith(".json"):
        raise FeatureGenerationCandidateRedesignedLabelsError(
            "candidate filename must be a simple JSON filename"
        )
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / output_name
    payload = canonical_json_bytes(candidate)
    try:
        with path.open("xb") as handle:
            handle.write(payload)
    except FileExistsError as exc:
        raise FeatureGenerationCandidateRedesignedLabelsError(
            "candidate output already exists"
        ) from exc
    return {
        "path": str(path).replace("\\", "/"),
        "filename": path.name,
        "payload_byte_size": len(payload),
        "payload_sha256": sha256_bytes(payload),
        "candidate_status": candidate["candidate_status"],
        "feature_generation_candidate_using_redesigned_labels_digest": candidate["feature_generation_candidate_using_redesigned_labels_digest"],
    }
