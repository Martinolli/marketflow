"""Offline results review for expectancy objective design outputs."""

from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
from typing import Any, Iterable, Mapping

from marketflow.historical_data.artifacts import (
    canonical_json_bytes,
    semantic_digest,
    sha256_bytes,
)
from marketflow.services import (
    marketflow_expectancy_objective_design_execution_service as execution_service,
)


ARTIFACT_KIND_MARKETFLOW_EXPECTANCY_OBJECTIVE_DESIGN_RESULTS_REVIEW_PACKAGE = (
    "MARKETFLOW_EXPECTANCY_OBJECTIVE_DESIGN_RESULTS_REVIEW_PACKAGE"
)
ARTIFACT_KIND_MARKETFLOW_EXPECTANCY_OBJECTIVE_DESIGN_RESULTS_REVIEW_BLOCKED = (
    "MARKETFLOW_EXPECTANCY_OBJECTIVE_DESIGN_RESULTS_REVIEW_BLOCKED"
)
SCHEMA_VERSION_MARKETFLOW_EXPECTANCY_OBJECTIVE_DESIGN_RESULTS_REVIEW_V1 = (
    "marketflow_expectancy_objective_design_results_review_v1"
)
MARKETFLOW_EXPECTANCY_OBJECTIVE_DESIGN_RESULTS_REVIEW_PACKAGE_READY = (
    "MARKETFLOW_EXPECTANCY_OBJECTIVE_DESIGN_RESULTS_REVIEW_PACKAGE_READY"
)
MARKETFLOW_EXPECTANCY_OBJECTIVE_DESIGN_RESULTS_REVIEW_BLOCKED_MISSING_OR_INVALID_OUTPUTS = (
    "MARKETFLOW_EXPECTANCY_OBJECTIVE_DESIGN_RESULTS_REVIEW_BLOCKED_MISSING_OR_INVALID_OUTPUTS"
)
EXPECTANCY_OBJECTIVE_DESIGN_RESULTS_REVIEW_ONLY_NOT_GENERATION = (
    "EXPECTANCY_OBJECTIVE_DESIGN_RESULTS_REVIEW_ONLY_NOT_GENERATION"
)

EXPECTED_SOURCE_DESIGN_EXECUTION_DIGEST = (
    "ba9661d34b57dbd464b6ec559c5b3e48df5ff78847102aa16d2d9e45f076ec11"
)
EXPECTED_SOURCE_DESIGN_OUTPUT_BINDING_DIGEST = (
    "3ee2acfb7461769fc054e1afb34e222302297b04d66a08b21fb411613e0585a4"
)
EXPECTED_SOURCE_APPROVAL_DIGEST = execution_service.EXPECTED_SOURCE_APPROVAL_DIGEST
EXPECTED_SOURCE_CANDIDATE_REVIEW_DIGEST = (
    execution_service.EXPECTED_SOURCE_CANDIDATE_REVIEW_DIGEST
)
EXPECTED_SOURCE_CANDIDATE_DIGEST = execution_service.EXPECTED_SOURCE_CANDIDATE_DIGEST

OUTPUT_LABEL = execution_service.OUTPUT_LABEL
EVIDENCE_SCOPE = execution_service.EVIDENCE_SCOPE
SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE = (
    execution_service.SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE
)
SELECTED_OBJECTIVE_PATH = execution_service.SELECTED_OBJECTIVE_PATH
NOT_ACCEPTED = execution_service.NOT_ACCEPTED
NOT_AUTHORIZED = execution_service.NOT_AUTHORIZED
PASS = execution_service.PASS
FAIL = execution_service.FAIL
BLOCKER = execution_service.BLOCKER
EXPECTED_OUTPUT_FILENAMES = list(execution_service.OUTPUT_FILENAMES)
DEFAULT_SOURCE_OUTPUT_ROOT = execution_service.DEFAULT_OUTPUT_ROOT

REVIEW_STATUSES = {
    "objective_family_selection_report_review": "REVIEWED_RESEARCH_ONLY",
    "expectancy_payoff_specification_review": "REVIEWED_RESEARCH_ONLY",
    "abstention_support_specification_review": "REVIEWED_RESEARCH_ONLY",
    "material_move_specification_review": "REVIEWED_RESEARCH_ONLY",
    "objective_label_generation_plan_review": "REVIEWED_PLAN_ONLY_NOT_EXECUTED",
    "objective_validation_metric_plan_review": "REVIEWED_PLAN_ONLY_NOT_COMPUTED",
    "objective_baseline_comparison_plan_review": "REVIEWED_PLAN_ONLY_NOT_EXECUTED",
    "per_ticker_objective_review_status": "REVIEWED_RESEARCH_ONLY",
    "operator_summary_review": "REVIEWED_RESEARCH_ONLY",
    "digest_manifest_review": "VERIFIED_ZERO_MISMATCHES",
}

NEXT_CHAIN = [
    "Objective Label or Target Generation Candidate v1.",
    "Objective Label or Target Generation Candidate Operator Review v1.",
    "Objective Label or Target Generation Approval v1.",
    "Objective label/target generation execution only after separate approval.",
    "Future signal/feature planning only after separate approval.",
    "Future VPA/Wyckoff baseline only after separate approval.",
    "Future expectancy backtest lab only after separate approval.",
    "Results review and readiness gates before any acceptance.",
    "Runtime migration only if ever separately authorized.",
]
NEXT_GATES = [
    "objective_label_or_target_generation_candidate",
    "objective_label_or_target_generation_candidate_operator_review",
    "objective_label_or_target_generation_approval",
    "objective_label_or_target_generation_execution",
    "signal_or_feature_generation_candidate",
    "vpa_wyckoff_rule_baseline_candidate",
    "expectancy_backtest_lab_candidate",
    "expectancy_results_review_and_reassessment",
    "runtime_migration_chain_if_ever_authorized",
]
RISK_CONTROLS = [
    "review_does_not_generate_labels",
    "review_does_not_create_targets",
    "review_does_not_generate_features",
    "review_does_not_create_feature_label_matrix",
    "review_does_not_run_backtest",
    "review_does_not_train_models",
    "review_does_not_compute_metrics",
    "review_does_not_score_strategy",
    "review_does_not_generate_trade_recommendations",
    "review_does_not_accept_predictive_usefulness",
    "review_does_not_accept_profitability",
    "review_does_not_authorize_runtime",
    "review_does_not_authorize_strategy",
    "review_does_not_authorize_paper_trading",
    "review_does_not_authorize_broker_execution",
    "review_does_not_call_providers",
    "review_does_not_acquire_market_data",
    "review_does_not_rerun_design_execution",
    "do_not_mutate_frozen_dataset",
    "do_not_mutate_redesigned_label_outputs",
    "do_not_mutate_feature_outputs",
    "do_not_mutate_predictive_evidence_outputs",
    "preserve_meta_record_limitation",
    "all_outputs_research_only",
]

REQUIRED_CHECK_IDS = [
    "source_design_execution_digest_bound",
    "source_design_output_binding_digest_bound",
    "source_expectancy_objective_approval_digest_bound",
    "source_candidate_review_digest_bound",
    "source_candidate_digest_bound",
    "source_strategy_charter_approval_digest_bound",
    "source_strategy_charter_digest_bound",
    "source_final_archive_digest_bound",
    "source_archive_digest_bound",
    "source_selection_digest_bound",
    "source_closure_digest_bound",
    "source_readiness_digest_bound",
    "source_reassessment_digest_bound",
    "source_results_review_digest_bound",
    "source_execution_digest_bound",
    "matrix_digest_bound",
    "feature_values_digest_bound",
    "label_values_digest_bound",
    "research_registry_digest_bound",
    "records_digest_bound",
    "target_universe_12_preserved",
    "records_digest_preserved",
    "meta_913_preserved",
    "design_execution_status_research_only",
    "design_scope_not_label_generation",
    "selected_objective_path_preserved",
    "expected_output_count_11",
    "observed_output_count_11",
    "output_digest_mismatch_count_zero",
    "output_files_inspected_true",
    "digest_manifest_self_reference_policy_verified",
    "objective_family_selection_report_verified",
    "expectancy_payoff_specification_verified",
    "abstention_support_specification_verified",
    "material_move_specification_verified",
    "label_generation_plan_verified_without_generation",
    "validation_metric_plan_verified_without_computation",
    "baseline_comparison_plan_verified_without_execution",
    "per_ticker_review_verified",
    "operator_summary_verified",
    "results_review_created_true",
    "results_review_ready_true",
    "ready_for_objective_label_or_target_generation_candidate_true",
    "objective_label_or_target_generation_candidate_created_false",
    "label_generation_authorized_false",
    "label_generation_performed_false",
    "new_targets_created_false",
    "target_definition_change_authorized_false",
    "feature_generation_authorized_false",
    "feature_generation_performed_false",
    "feature_label_matrix_created_false",
    "backtest_execution_authorized_false",
    "backtest_execution_performed_false",
    "model_training_authorized_false",
    "model_training_performed_false",
    "metric_computation_authorized_false",
    "metric_computation_performed_false",
    "strategy_scoring_false",
    "predictive_usefulness_not_accepted",
    "profitability_not_accepted",
    "runtime_not_authorized",
    "strategy_not_authorized",
    "broker_not_authorized",
    "trade_recommendations_false",
    "per_ticker_entries_12",
    "per_ticker_digests_present",
    "provider_requests_made_false",
    "market_data_acquisition_false",
    "dataset_regeneration_false",
    "design_execution_rerun_false",
    "raw_provider_payloads_not_committed",
    "api_keys_not_stored_or_printed",
    "next_chain_defined",
    "next_gates_defined",
    "risk_controls_defined",
    "no_tracked_marketflow_files",
]


class MarketFlowExpectancyObjectiveDesignResultsReviewError(ValueError):
    """Raised when the design-results review package is invalid."""


def _path_text(path: Path) -> str:
    return str(path).replace("\\", "/")


def _load_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise MarketFlowExpectancyObjectiveDesignResultsReviewError(
            f"{path.name} is not readable JSON"
        ) from exc
    if not isinstance(payload, dict):
        raise MarketFlowExpectancyObjectiveDesignResultsReviewError(
            f"{path.name} must contain a JSON object"
        )
    return payload


def _contains_sensitive_value(value: Any) -> bool:
    if isinstance(value, Mapping):
        for key, item in value.items():
            lowered_key = str(key).lower()
            if lowered_key in {
                "api_key",
                "access_token",
                "authorization",
                "provider_response_body",
                "raw_provider_payload",
                "raw_provider_payloads",
            }:
                return True
            if _contains_sensitive_value(item):
                return True
        return False
    if isinstance(value, list):
        return any(_contains_sensitive_value(item) for item in value)
    if isinstance(value, str):
        lowered = value.lower()
        return any(
            marker in lowered
            for marker in ("bearer ", "apikey=", "api_key=", "access_token=")
        )
    return False


def _forbidden_output_field(value: Any, *, prefix: str = "") -> str | None:
    closed_true_fields = {
        "expectancy_objective_generation_authorized",
        "expectancy_objective_generation_performed",
        "label_generation_authorized",
        "label_generation_performed",
        "new_targets_created",
        "target_definition_change_authorized",
        "target_definition_change_performed",
        "feature_generation_authorized",
        "feature_generation_performed",
        "feature_label_matrix_created",
        "backtest_execution_authorized",
        "backtest_execution_performed",
        "model_training_authorized",
        "model_training_performed",
        "metric_computation_authorized",
        "metric_computation_performed",
        "strategy_scoring_performed",
        "new_strategy_scoring_performed",
        "trade_recommendations_generated",
        "raw_provider_payloads_committed",
        "api_keys_stored_or_printed",
    }
    forbidden_data_fields = {
        "labels",
        "targets",
        "target_values",
        "feature_values",
        "feature_label_matrix_rows",
        "computed_metrics",
        "model_artifacts",
        "trained_models",
        "backtest_results",
        "strategy_scores",
        "trade_recommendations",
        "provider_payloads",
        "raw_provider_payloads",
    }
    if isinstance(value, Mapping):
        for key, item in value.items():
            key_text = str(key)
            path = f"{prefix}.{key_text}" if prefix else key_text
            if key_text in closed_true_fields and item is True:
                return path
            if key_text in forbidden_data_fields:
                return path
            if key_text in {"runtime_use", "strategy_use", "paper_trading", "broker_execution"} and item != NOT_AUTHORIZED:
                return path
            if key_text in {"predictive_usefulness", "profitability"} and item != NOT_ACCEPTED:
                return path
            nested = _forbidden_output_field(item, prefix=path)
            if nested:
                return nested
    elif isinstance(value, list):
        for index, item in enumerate(value):
            nested = _forbidden_output_field(item, prefix=f"{prefix}[{index}]")
            if nested:
                return nested
    return None


def _verify_source_outputs(
    root: Path,
) -> tuple[dict[str, dict[str, Any]], list[dict[str, Any]], dict[str, str]]:
    if not root.is_dir():
        raise MarketFlowExpectancyObjectiveDesignResultsReviewError(
            "source output root missing"
        )
    observed_names = sorted(path.name for path in root.iterdir() if path.is_file())
    if observed_names != sorted(EXPECTED_OUTPUT_FILENAMES):
        raise MarketFlowExpectancyObjectiveDesignResultsReviewError(
            "source output filename set mismatch"
        )
    payloads: dict[str, dict[str, Any]] = {}
    local_hashes: dict[str, str] = {}
    for filename in EXPECTED_OUTPUT_FILENAMES:
        path = root / filename
        data = path.read_bytes()
        local_hashes[filename] = sha256_bytes(data)
        payload = _load_json(path)
        is_execution_manifest = (
            filename == "expectancy_objective_design_manifest.json"
        )
        if not is_execution_manifest and payload.get("output_label") != OUTPUT_LABEL:
            raise MarketFlowExpectancyObjectiveDesignResultsReviewError(
                f"{filename} output_label mismatch"
            )
        if not is_execution_manifest and payload.get("evidence_scope") != EVIDENCE_SCOPE:
            raise MarketFlowExpectancyObjectiveDesignResultsReviewError(
                f"{filename} evidence_scope mismatch"
            )
        if _contains_sensitive_value(payload):
            raise MarketFlowExpectancyObjectiveDesignResultsReviewError(
                f"{filename} contains API-key or provider-payload material"
            )
        forbidden = _forbidden_output_field(payload)
        if forbidden:
            raise MarketFlowExpectancyObjectiveDesignResultsReviewError(
                f"{filename} contains forbidden output field {forbidden}"
            )
        payloads[filename] = payload

    source = payloads["expectancy_objective_design_manifest.json"]
    try:
        execution_service.validate_marketflow_expectancy_objective_design_execution_v1(
            source
        )
    except (ValueError, TypeError, KeyError) as exc:
        raise MarketFlowExpectancyObjectiveDesignResultsReviewError(
            "source design execution artifact invalid"
        ) from exc
    if (
        source.get("marketflow_expectancy_objective_design_execution_digest")
        != EXPECTED_SOURCE_DESIGN_EXECUTION_DIGEST
    ):
        raise MarketFlowExpectancyObjectiveDesignResultsReviewError(
            "source design execution digest mismatch"
        )
    if (
        source.get("expectancy_objective_design_output_binding_digest")
        != EXPECTED_SOURCE_DESIGN_OUTPUT_BINDING_DIGEST
    ):
        raise MarketFlowExpectancyObjectiveDesignResultsReviewError(
            "source design output binding digest mismatch"
        )

    keyed_reports = {
        "objective_family_selection_report.json": (
            "objective_families",
            source["objective_family_selection_report"],
        ),
        "objective_validation_metric_plan.json": (
            "validation_metrics",
            source["objective_validation_metric_plan"],
        ),
        "objective_baseline_comparison_plan.json": (
            "baselines",
            source["objective_baseline_comparison_plan"],
        ),
        "per_ticker_objective_review.json": (
            "per_ticker_entries",
            source["per_ticker_objective_review"],
        ),
    }
    for filename, (field, expected_content) in keyed_reports.items():
        if payloads[filename].get(field) != expected_content:
            raise MarketFlowExpectancyObjectiveDesignResultsReviewError(
                f"{filename} content binding mismatch"
            )
    subset_reports = {
        "expectancy_payoff_objective_specification.json": source[
            "expectancy_payoff_objective_specification"
        ],
        "abstention_support_objective_specification.json": source[
            "abstention_support_objective_specification"
        ],
        "material_move_objective_specification.json": source[
            "material_move_objective_specification"
        ],
        "objective_label_generation_plan.json": source[
            "objective_label_generation_plan"
        ],
    }
    for filename, expected_content in subset_reports.items():
        if any(
            payloads[filename].get(field) != value
            for field, value in expected_content.items()
        ):
            raise MarketFlowExpectancyObjectiveDesignResultsReviewError(
                f"{filename} content binding mismatch"
            )

    digest_manifest = payloads[
        "expectancy_objective_design_digest_manifest.json"
    ]
    rows = digest_manifest.get("output_digest_entries")
    if not isinstance(rows, list) or len(rows) != 11:
        raise MarketFlowExpectancyObjectiveDesignResultsReviewError(
            "source digest manifest entry count mismatch"
        )
    if [row.get("filename") for row in rows if isinstance(row, Mapping)] != EXPECTED_OUTPUT_FILENAMES:
        raise MarketFlowExpectancyObjectiveDesignResultsReviewError(
            "source digest manifest filename order mismatch"
        )
    verified_files: list[dict[str, Any]] = []
    mismatch_count = 0
    for row in rows:
        if not isinstance(row, Mapping):
            raise MarketFlowExpectancyObjectiveDesignResultsReviewError(
                "source digest manifest row invalid"
            )
        filename = str(row["filename"])
        is_self = filename == "expectancy_objective_design_digest_manifest.json"
        expected_digest = row.get("sha256")
        expected_kind = (
            SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE if is_self else "FILE_SHA256"
        )
        if row.get("digest_kind") != expected_kind:
            raise MarketFlowExpectancyObjectiveDesignResultsReviewError(
                f"{filename} digest kind mismatch"
            )
        if is_self:
            if expected_digest is not None:
                raise MarketFlowExpectancyObjectiveDesignResultsReviewError(
                    "digest manifest self-entry must have null sha256"
                )
            verified = True
        else:
            verified = expected_digest == local_hashes[filename]
            mismatch_count += int(not verified)
        verified_files.append(
            {
                "filename": filename,
                "local_sha256": local_hashes[filename],
                "manifest_sha256": expected_digest,
                "digest_kind": expected_kind,
                "verified": verified,
            }
        )
    if digest_manifest.get("self_reference_policy") != SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE:
        raise MarketFlowExpectancyObjectiveDesignResultsReviewError(
            "digest manifest self-reference policy mismatch"
        )
    if mismatch_count:
        raise MarketFlowExpectancyObjectiveDesignResultsReviewError(
            f"source output digest mismatch count {mismatch_count}"
        )
    return payloads, verified_files, local_hashes


def per_ticker_expectancy_objective_design_results_review_digest_v1(
    entry: Mapping[str, Any],
) -> str:
    """Return the deterministic semantic digest for one reviewed ticker."""
    payload = deepcopy(dict(entry))
    payload.pop("per_ticker_expectancy_objective_design_results_review_digest", None)
    return semantic_digest(payload)


def _per_ticker_review(source_rows: Any) -> list[dict[str, Any]]:
    if not isinstance(source_rows, list) or len(source_rows) != 12:
        raise MarketFlowExpectancyObjectiveDesignResultsReviewError(
            "source per-ticker objective review mismatch"
        )
    reviewed: list[dict[str, Any]] = []
    for row in source_rows:
        if not isinstance(row, Mapping):
            raise MarketFlowExpectancyObjectiveDesignResultsReviewError(
                "source per-ticker objective review row invalid"
            )
        ticker = row.get("ticker")
        entry = {
            "ticker": ticker,
            "registry_approval_status": row.get("registry_approval_status"),
            "canonical_dataset_status": row.get("canonical_dataset_status"),
            "historical_record_count": row.get("historical_record_count"),
            "meta_reduced_record_count_flag": row.get(
                "meta_reduced_record_count_flag"
            ),
            "expectancy_objective_approval_status": row.get(
                "expectancy_objective_approval_status"
            ),
            "expectancy_objective_design_status": (
                execution_service.MARKETFLOW_EXPECTANCY_OBJECTIVE_DESIGN_EXECUTED_RESEARCH_ONLY
            ),
            "expectancy_objective_design_results_review_status": (
                "REVIEWED_RESEARCH_ONLY"
            ),
            "selected_objective_path": SELECTED_OBJECTIVE_PATH,
            "label_generation_authorized": False,
            "new_targets_created": False,
            "feature_generation_authorized": False,
            "feature_label_matrix_created": False,
            "backtest_execution_authorized": False,
            "model_training_authorized": False,
            "metric_computation_authorized": False,
            "predictive_usefulness": NOT_ACCEPTED,
            "profitability": NOT_ACCEPTED,
            "runtime_use": NOT_AUTHORIZED,
            "strategy_use": NOT_AUTHORIZED,
            "paper_trading": NOT_AUTHORIZED,
            "broker_execution": NOT_AUTHORIZED,
            "trade_recommendations_generated": False,
            "source_design_execution_digest": EXPECTED_SOURCE_DESIGN_EXECUTION_DIGEST,
            "source_design_output_binding_digest": (
                EXPECTED_SOURCE_DESIGN_OUTPUT_BINDING_DIGEST
            ),
            "review_note": (
                "PRESERVE_META_LIMITATION_IN_EXPECTANCY_OBJECTIVE_DESIGN_RESULTS_REVIEW"
                if ticker == "META"
                else "STANDARD_RECORD_COUNT_PRESERVED"
            ),
        }
        entry[
            "per_ticker_expectancy_objective_design_results_review_digest"
        ] = per_ticker_expectancy_objective_design_results_review_digest_v1(entry)
        reviewed.append(entry)
    return reviewed


def _source_evidence_digests(source: Mapping[str, Any]) -> dict[str, str]:
    return {
        key: value
        for key, value in source.items()
        if key.endswith("_digest") and isinstance(value, str) and len(value) == 64
    }


def _base_review(source: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_EXPECTANCY_OBJECTIVE_DESIGN_RESULTS_REVIEW_PACKAGE,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_EXPECTANCY_OBJECTIVE_DESIGN_RESULTS_REVIEW_V1,
        "review_status": MARKETFLOW_EXPECTANCY_OBJECTIVE_DESIGN_RESULTS_REVIEW_PACKAGE_READY,
        "review_scope": EXPECTANCY_OBJECTIVE_DESIGN_RESULTS_REVIEW_ONLY_NOT_GENERATION,
        "created_offline": True,
        "research_only": True,
        "operator_review_required": True,
        "output_label": OUTPUT_LABEL,
        "evidence_scope": EVIDENCE_SCOPE,
        "source_expectancy_objective_design_execution_artifact_kind": execution_service.ARTIFACT_KIND_MARKETFLOW_EXPECTANCY_OBJECTIVE_DESIGN_EXECUTED,
        "source_expectancy_objective_design_execution_status": execution_service.MARKETFLOW_EXPECTANCY_OBJECTIVE_DESIGN_EXECUTED_RESEARCH_ONLY,
        "source_expectancy_objective_design_execution_scope": execution_service.EXPECTANCY_OBJECTIVE_DESIGN_EXECUTION_ONLY_NOT_LABEL_GENERATION,
        "source_expectancy_objective_design_execution_digest": EXPECTED_SOURCE_DESIGN_EXECUTION_DIGEST,
        "source_expectancy_objective_design_output_binding_digest": EXPECTED_SOURCE_DESIGN_OUTPUT_BINDING_DIGEST,
        "source_expectancy_objective_approval_digest": EXPECTED_SOURCE_APPROVAL_DIGEST,
        "source_expectancy_objective_candidate_review_digest": EXPECTED_SOURCE_CANDIDATE_REVIEW_DIGEST,
        "source_expectancy_objective_candidate_digest": EXPECTED_SOURCE_CANDIDATE_DIGEST,
        "source_strategy_charter_approval_digest": source[
            "source_strategy_charter_approval_digest"
        ],
        "source_strategy_charter_review_digest": source[
            "source_strategy_charter_review_digest"
        ],
        "source_strategy_charter_digest": source["source_strategy_charter_digest"],
        "source_final_archive_digest": source["source_final_archive_digest"],
        "source_archive_digest": source["source_archive_digest"],
        "source_selection_digest": source["source_selection_digest"],
        "source_closure_digest": source["source_closure_digest"],
        "source_readiness_digest": source["source_readiness_digest"],
        "source_reassessment_digest": source["source_reassessment_digest"],
        "source_results_review_digest": source["source_results_review_digest"],
        "source_execution_digest": source["source_execution_digest"],
        "source_output_binding_digest": source["source_output_binding_digest"],
        "feature_label_matrix_digest": source["feature_label_matrix_digest"],
        "feature_values_digest": source["feature_values_digest"],
        "redesigned_label_values_digest": source["redesigned_label_values_digest"],
        "research_registry_approval_digest": source[
            "research_registry_approval_digest"
        ],
        "records_digest": source["records_digest"],
        "source_evidence_digests": _source_evidence_digests(source),
        "dataset_name": source["dataset_name"],
        "source_profile": source["source_profile"],
        "timeframe": source["timeframe"],
        "date_range_start": source["date_range_start"],
        "date_range_end": source["date_range_end"],
        "target_universe": deepcopy(source["target_universe"]),
        "target_universe_count": source["target_universe_count"],
        "total_canonical_record_count": source["total_canonical_record_count"],
        "meta_record_count": source["meta_record_count"],
        "non_meta_record_count": source["non_meta_record_count"],
        "meta_reduced_record_count_preserved": source[
            "meta_reduced_record_count_preserved"
        ],
        "selected_objective_path": SELECTED_OBJECTIVE_PATH,
        "approved_primary_objective_cluster": source[
            "approved_primary_objective_cluster"
        ],
        "approved_supporting_objective_cluster": source[
            "approved_supporting_objective_cluster"
        ],
        "approved_secondary_objective_cluster": source[
            "approved_secondary_objective_cluster"
        ],
        "design_philosophy_review": (
            "Optimize future designs for tradable expectancy, risk-adjusted "
            "opportunity, payoff asymmetry, and abstention quality, not "
            "classification accuracy alone."
        ),
        "objective_design_philosophy": source["objective_design_philosophy"],
        "objective_design_primary_goal": source["objective_design_primary_goal"],
        "objective_design_boundary": source["objective_design_boundary"],
        "expectancy_objective_selected": True,
        "expectancy_objective_approved": True,
        "expectancy_objective_authorized": True,
        "ready_for_expectancy_objective_design_execution": True,
        "expectancy_objective_design_executed": True,
        "expectancy_objective_design_results_created": True,
        "expectancy_objective_design_results_review_created": True,
        "expectancy_objective_design_results_review_ready": True,
        "ready_for_objective_label_or_target_generation_candidate": True,
        "objective_label_or_target_generation_candidate_created": False,
        "objective_label_or_target_generation_approved": False,
        "objective_label_or_target_generation_performed": False,
        "expectancy_objective_generation_authorized": False,
        "expectancy_objective_generation_performed": False,
        "label_generation_authorized": False,
        "label_generation_performed": False,
        "new_targets_created": False,
        "target_definition_change_authorized": False,
        "target_definition_change_performed": False,
        "feature_generation_authorized": False,
        "feature_generation_performed": False,
        "feature_label_matrix_created": False,
        "backtest_execution_authorized": False,
        "backtest_execution_performed": False,
        "model_training_authorized": False,
        "model_training_performed": False,
        "metric_computation_authorized": False,
        "metric_computation_performed": False,
        "strategy_scoring_performed": False,
        "new_strategy_scoring_performed": False,
        "predictive_usefulness": NOT_ACCEPTED,
        "predictive_usefulness_acceptance_candidate_created": False,
        "predictive_usefulness_acceptance_ready": False,
        "predictive_usefulness_acceptance_recommended": False,
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
        "trade_recommendations_generated": False,
        "provider_requests_made_in_review": False,
        "live_provider_transport_enabled_in_review": False,
        "market_data_acquisition_performed_in_review": False,
        "dataset_generation_performed_in_review": False,
        "canonical_dataset_regenerated_in_review": False,
        "objective_design_execution_rerun_performed": False,
        "raw_provider_payloads_committed": False,
        "api_keys_stored_or_printed": False,
        "generated_output_count": 11,
        "expected_output_count": 11,
        "digest_manifest_self_reference_policy": SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE,
        "next_chain": list(NEXT_CHAIN),
        "next_gates": list(NEXT_GATES),
        "risk_controls": list(RISK_CONTROLS),
        "no_tracked_marketflow_files": True,
    }


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


def _per_ticker_digests_valid(rows: Any) -> bool:
    return isinstance(rows, list) and len(rows) == 12 and all(
        isinstance(row, Mapping)
        and row.get("per_ticker_expectancy_objective_design_results_review_digest")
        == per_ticker_expectancy_objective_design_results_review_digest_v1(row)
        for row in rows
    )


def _check_definitions(review: Mapping[str, Any]) -> list[tuple[str, Any, Any]]:
    rows = review.get("per_ticker_objective_results_review", [])
    statuses = review.get("design_output_review_statuses", {})
    return [
        ("source_design_execution_digest_bound", EXPECTED_SOURCE_DESIGN_EXECUTION_DIGEST, review.get("source_expectancy_objective_design_execution_digest")),
        ("source_design_output_binding_digest_bound", EXPECTED_SOURCE_DESIGN_OUTPUT_BINDING_DIGEST, review.get("source_expectancy_objective_design_output_binding_digest")),
        ("source_expectancy_objective_approval_digest_bound", EXPECTED_SOURCE_APPROVAL_DIGEST, review.get("source_expectancy_objective_approval_digest")),
        ("source_candidate_review_digest_bound", EXPECTED_SOURCE_CANDIDATE_REVIEW_DIGEST, review.get("source_expectancy_objective_candidate_review_digest")),
        ("source_candidate_digest_bound", EXPECTED_SOURCE_CANDIDATE_DIGEST, review.get("source_expectancy_objective_candidate_digest")),
        ("source_strategy_charter_approval_digest_bound", review.get("source_evidence_digests", {}).get("source_strategy_charter_approval_digest"), review.get("source_strategy_charter_approval_digest")),
        ("source_strategy_charter_digest_bound", review.get("source_evidence_digests", {}).get("source_strategy_charter_digest"), review.get("source_strategy_charter_digest")),
        ("source_final_archive_digest_bound", review.get("source_evidence_digests", {}).get("source_final_archive_digest"), review.get("source_final_archive_digest")),
        ("source_archive_digest_bound", review.get("source_evidence_digests", {}).get("source_archive_digest"), review.get("source_archive_digest")),
        ("source_selection_digest_bound", review.get("source_evidence_digests", {}).get("source_selection_digest"), review.get("source_selection_digest")),
        ("source_closure_digest_bound", review.get("source_evidence_digests", {}).get("source_closure_digest"), review.get("source_closure_digest")),
        ("source_readiness_digest_bound", review.get("source_evidence_digests", {}).get("source_readiness_digest"), review.get("source_readiness_digest")),
        ("source_reassessment_digest_bound", review.get("source_evidence_digests", {}).get("source_reassessment_digest"), review.get("source_reassessment_digest")),
        ("source_results_review_digest_bound", review.get("source_evidence_digests", {}).get("source_results_review_digest"), review.get("source_results_review_digest")),
        ("source_execution_digest_bound", review.get("source_evidence_digests", {}).get("source_execution_digest"), review.get("source_execution_digest")),
        ("matrix_digest_bound", review.get("source_evidence_digests", {}).get("feature_label_matrix_digest"), review.get("feature_label_matrix_digest")),
        ("feature_values_digest_bound", review.get("source_evidence_digests", {}).get("feature_values_digest"), review.get("feature_values_digest")),
        ("label_values_digest_bound", review.get("source_evidence_digests", {}).get("redesigned_label_values_digest"), review.get("redesigned_label_values_digest")),
        ("research_registry_digest_bound", review.get("source_evidence_digests", {}).get("research_registry_approval_digest"), review.get("research_registry_approval_digest")),
        ("records_digest_bound", review.get("source_evidence_digests", {}).get("records_digest"), review.get("records_digest")),
        ("target_universe_12_preserved", 12, review.get("target_universe_count")),
        ("records_digest_preserved", review.get("source_evidence_digests", {}).get("records_digest"), review.get("records_digest")),
        ("meta_913_preserved", 913, review.get("meta_record_count")),
        ("design_execution_status_research_only", execution_service.MARKETFLOW_EXPECTANCY_OBJECTIVE_DESIGN_EXECUTED_RESEARCH_ONLY, review.get("source_expectancy_objective_design_execution_status")),
        ("design_scope_not_label_generation", execution_service.EXPECTANCY_OBJECTIVE_DESIGN_EXECUTION_ONLY_NOT_LABEL_GENERATION, review.get("source_expectancy_objective_design_execution_scope")),
        ("selected_objective_path_preserved", SELECTED_OBJECTIVE_PATH, review.get("selected_objective_path")),
        ("expected_output_count_11", 11, review.get("expected_output_count")),
        ("observed_output_count_11", 11, review.get("observed_output_count")),
        ("output_digest_mismatch_count_zero", 0, review.get("output_digest_mismatch_count")),
        ("output_files_inspected_true", True, review.get("output_file_inspection_performed")),
        ("digest_manifest_self_reference_policy_verified", SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE, review.get("digest_manifest_self_reference_policy")),
        ("objective_family_selection_report_verified", "REVIEWED_RESEARCH_ONLY", statuses.get("objective_family_selection_report_review")),
        ("expectancy_payoff_specification_verified", "REVIEWED_RESEARCH_ONLY", statuses.get("expectancy_payoff_specification_review")),
        ("abstention_support_specification_verified", "REVIEWED_RESEARCH_ONLY", statuses.get("abstention_support_specification_review")),
        ("material_move_specification_verified", "REVIEWED_RESEARCH_ONLY", statuses.get("material_move_specification_review")),
        ("label_generation_plan_verified_without_generation", "REVIEWED_PLAN_ONLY_NOT_EXECUTED", statuses.get("objective_label_generation_plan_review")),
        ("validation_metric_plan_verified_without_computation", "REVIEWED_PLAN_ONLY_NOT_COMPUTED", statuses.get("objective_validation_metric_plan_review")),
        ("baseline_comparison_plan_verified_without_execution", "REVIEWED_PLAN_ONLY_NOT_EXECUTED", statuses.get("objective_baseline_comparison_plan_review")),
        ("per_ticker_review_verified", "REVIEWED_RESEARCH_ONLY", statuses.get("per_ticker_objective_review_status")),
        ("operator_summary_verified", "REVIEWED_RESEARCH_ONLY", statuses.get("operator_summary_review")),
        ("results_review_created_true", True, review.get("expectancy_objective_design_results_review_created")),
        ("results_review_ready_true", True, review.get("expectancy_objective_design_results_review_ready")),
        ("ready_for_objective_label_or_target_generation_candidate_true", True, review.get("ready_for_objective_label_or_target_generation_candidate")),
        ("objective_label_or_target_generation_candidate_created_false", False, review.get("objective_label_or_target_generation_candidate_created")),
        ("label_generation_authorized_false", False, review.get("label_generation_authorized")),
        ("label_generation_performed_false", False, review.get("label_generation_performed")),
        ("new_targets_created_false", False, review.get("new_targets_created")),
        ("target_definition_change_authorized_false", False, review.get("target_definition_change_authorized")),
        ("feature_generation_authorized_false", False, review.get("feature_generation_authorized")),
        ("feature_generation_performed_false", False, review.get("feature_generation_performed")),
        ("feature_label_matrix_created_false", False, review.get("feature_label_matrix_created")),
        ("backtest_execution_authorized_false", False, review.get("backtest_execution_authorized")),
        ("backtest_execution_performed_false", False, review.get("backtest_execution_performed")),
        ("model_training_authorized_false", False, review.get("model_training_authorized")),
        ("model_training_performed_false", False, review.get("model_training_performed")),
        ("metric_computation_authorized_false", False, review.get("metric_computation_authorized")),
        ("metric_computation_performed_false", False, review.get("metric_computation_performed")),
        ("strategy_scoring_false", False, review.get("strategy_scoring_performed")),
        ("predictive_usefulness_not_accepted", NOT_ACCEPTED, review.get("predictive_usefulness")),
        ("profitability_not_accepted", NOT_ACCEPTED, review.get("profitability")),
        ("runtime_not_authorized", NOT_AUTHORIZED, review.get("runtime_use")),
        ("strategy_not_authorized", NOT_AUTHORIZED, review.get("strategy_use")),
        ("broker_not_authorized", NOT_AUTHORIZED, review.get("broker_execution")),
        ("trade_recommendations_false", False, review.get("trade_recommendations_generated")),
        ("per_ticker_entries_12", 12, len(rows) if isinstance(rows, list) else 0),
        ("per_ticker_digests_present", True, _per_ticker_digests_valid(rows)),
        ("provider_requests_made_false", False, review.get("provider_requests_made_in_review")),
        ("market_data_acquisition_false", False, review.get("market_data_acquisition_performed_in_review")),
        ("dataset_regeneration_false", False, review.get("canonical_dataset_regenerated_in_review")),
        ("design_execution_rerun_false", False, review.get("objective_design_execution_rerun_performed")),
        ("raw_provider_payloads_not_committed", False, review.get("raw_provider_payloads_committed")),
        ("api_keys_not_stored_or_printed", False, review.get("api_keys_stored_or_printed")),
        ("next_chain_defined", NEXT_CHAIN, review.get("next_chain")),
        ("next_gates_defined", NEXT_GATES, review.get("next_gates")),
        ("risk_controls_defined", RISK_CONTROLS, review.get("risk_controls")),
        ("no_tracked_marketflow_files", True, review.get("no_tracked_marketflow_files")),
    ]


def _review_checklist(review: Mapping[str, Any]) -> list[dict[str, Any]]:
    definitions = _check_definitions(review)
    if [definition[0] for definition in definitions] != REQUIRED_CHECK_IDS:
        raise MarketFlowExpectancyObjectiveDesignResultsReviewError(
            "internal checklist definition mismatch"
        )
    return [_check(*definition) for definition in definitions]


def _review_summary(checklist: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
    rows = list(checklist)
    failed = [row for row in rows if row.get("status") != PASS]
    return {
        "total_checks": len(rows),
        "passed_checks": len(rows) - len(failed),
        "failed_checks": len(failed),
        "blocker_count": sum(row.get("severity") == BLOCKER for row in failed),
        "expectancy_objective_design_results_review_created": not failed,
        "expectancy_objective_design_results_review_ready": not failed,
        "ready_for_objective_label_or_target_generation_candidate": not failed,
        "objective_label_or_target_generation_candidate_created": False,
        "generated_output_count": 11,
        "output_digest_mismatch_count": 0,
        "label_generation_performed": False,
        "new_targets_created": False,
        "feature_generation_performed": False,
        "feature_label_matrix_created": False,
        "backtest_execution_performed": False,
        "model_training_performed": False,
        "metric_computation_performed": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_authorized": False,
        "trade_recommendations_generated": False,
    }


def _digest_payload(review: Mapping[str, Any]) -> dict[str, Any]:
    payload = deepcopy(dict(review))
    payload.pop("marketflow_expectancy_objective_design_results_review_digest", None)
    payload.pop("source_output_root", None)
    return payload


def marketflow_expectancy_objective_design_results_review_digest_v1(
    review: Mapping[str, Any],
) -> str:
    """Return the deterministic, source-location-independent review digest."""
    return semantic_digest(_digest_payload(review))


def _blocked_review(reason: str) -> dict[str, Any]:
    review = {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_EXPECTANCY_OBJECTIVE_DESIGN_RESULTS_REVIEW_BLOCKED,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_EXPECTANCY_OBJECTIVE_DESIGN_RESULTS_REVIEW_V1,
        "review_status": MARKETFLOW_EXPECTANCY_OBJECTIVE_DESIGN_RESULTS_REVIEW_BLOCKED_MISSING_OR_INVALID_OUTPUTS,
        "review_scope": EXPECTANCY_OBJECTIVE_DESIGN_RESULTS_REVIEW_ONLY_NOT_GENERATION,
        "created_offline": True,
        "research_only": True,
        "operator_review_required": True,
        "blocked_reason": reason,
        "source_expectancy_objective_design_execution_digest": EXPECTED_SOURCE_DESIGN_EXECUTION_DIGEST,
        "source_expectancy_objective_design_output_binding_digest": EXPECTED_SOURCE_DESIGN_OUTPUT_BINDING_DIGEST,
        "expected_output_count": 11,
        "observed_output_count": 0,
        "output_digest_mismatch_count": 11,
        "output_file_inspection_performed": False,
        "expectancy_objective_design_results_review_created": False,
        "expectancy_objective_design_results_review_ready": False,
        "ready_for_objective_label_or_target_generation_candidate": False,
        "objective_label_or_target_generation_candidate_created": False,
        "objective_label_or_target_generation_approved": False,
        "objective_label_or_target_generation_performed": False,
        "label_generation_authorized": False,
        "label_generation_performed": False,
        "new_targets_created": False,
        "target_definition_change_authorized": False,
        "target_definition_change_performed": False,
        "feature_generation_authorized": False,
        "feature_generation_performed": False,
        "feature_label_matrix_created": False,
        "backtest_execution_authorized": False,
        "backtest_execution_performed": False,
        "model_training_authorized": False,
        "model_training_performed": False,
        "metric_computation_authorized": False,
        "metric_computation_performed": False,
        "strategy_scoring_performed": False,
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "runtime_migration_approved": False,
        "runtime_migration_active": False,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "trade_recommendations_generated": False,
        "provider_requests_made_in_review": False,
        "live_provider_transport_enabled_in_review": False,
        "market_data_acquisition_performed_in_review": False,
        "dataset_generation_performed_in_review": False,
        "canonical_dataset_regenerated_in_review": False,
        "objective_design_execution_rerun_performed": False,
        "raw_provider_payloads_committed": False,
        "api_keys_stored_or_printed": False,
        "verified_output_files": [],
        "local_output_hashes": {},
        "per_ticker_objective_results_review": [],
        "review_checklist": [],
        "review_summary": {
            **_review_summary([]),
            "expectancy_objective_design_results_review_created": False,
            "expectancy_objective_design_results_review_ready": False,
            "ready_for_objective_label_or_target_generation_candidate": False,
            "generated_output_count": 0,
            "output_digest_mismatch_count": 11,
        },
    }
    review["marketflow_expectancy_objective_design_results_review_digest"] = (
        marketflow_expectancy_objective_design_results_review_digest_v1(review)
    )
    return review


def build_marketflow_expectancy_objective_design_results_review_v1(
    *,
    output_root: str | Path | None = None,
) -> dict[str, Any]:
    """Review existing design outputs offline; fail closed if evidence is invalid."""
    root = DEFAULT_SOURCE_OUTPUT_ROOT if output_root is None else Path(output_root)
    try:
        payloads, verified_files, local_hashes = _verify_source_outputs(root)
        source = payloads["expectancy_objective_design_manifest.json"]
        per_ticker = _per_ticker_review(source["per_ticker_objective_review"])
    except (MarketFlowExpectancyObjectiveDesignResultsReviewError, OSError) as exc:
        return _blocked_review(str(exc))

    review = _base_review(source)
    review.update(
        {
            "source_output_root": _path_text(root),
            "observed_output_count": len(verified_files),
            "output_digest_mismatch_count": 0,
            "output_file_inspection_performed": True,
            "local_output_hashes": local_hashes,
            "verified_output_files": verified_files,
            "output_verification": {
                "expected_output_count": 11,
                "observed_output_count": len(verified_files),
                "output_digest_mismatch_count": 0,
                "output_file_inspection_performed": True,
                "digest_manifest_self_reference_policy": SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE,
                "local_output_hashes": local_hashes,
                "verified_output_files": verified_files,
            },
            "design_output_review_statuses": dict(REVIEW_STATUSES),
            "reviewed_objective_family_selection_report": deepcopy(
                source["objective_family_selection_report"]
            ),
            "reviewed_expectancy_payoff_specification": deepcopy(
                source["expectancy_payoff_objective_specification"]
            ),
            "reviewed_abstention_support_specification": deepcopy(
                source["abstention_support_objective_specification"]
            ),
            "reviewed_material_move_specification": deepcopy(
                source["material_move_objective_specification"]
            ),
            "reviewed_objective_label_generation_plan": deepcopy(
                source["objective_label_generation_plan"]
            ),
            "reviewed_objective_validation_metric_plan": deepcopy(
                source["objective_validation_metric_plan"]
            ),
            "reviewed_objective_baseline_comparison_plan": deepcopy(
                source["objective_baseline_comparison_plan"]
            ),
            "per_ticker_objective_results_review": per_ticker,
            "reviewed_operator_summary": deepcopy(payloads["operator_summary.json"]),
            "reviewed_output_digest_manifest": deepcopy(
                payloads["expectancy_objective_design_digest_manifest.json"]
            ),
        }
    )
    checklist = _review_checklist(review)
    review["review_checklist"] = checklist
    review["review_summary"] = _review_summary(checklist)
    review["marketflow_expectancy_objective_design_results_review_digest"] = (
        marketflow_expectancy_objective_design_results_review_digest_v1(review)
    )
    validate_marketflow_expectancy_objective_design_results_review_v1(review)
    return review


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise MarketFlowExpectancyObjectiveDesignResultsReviewError(
            f"{field} mismatch"
        )


def _expect_true(actual: Any, field: str) -> None:
    if actual is not True:
        raise MarketFlowExpectancyObjectiveDesignResultsReviewError(
            f"{field} must be true"
        )


def _expect_false(actual: Any, field: str) -> None:
    if actual is not False:
        raise MarketFlowExpectancyObjectiveDesignResultsReviewError(
            f"{field} must be false"
        )


def _expect_digest(actual: Any, field: str) -> None:
    if not isinstance(actual, str) or len(actual) != 64:
        raise MarketFlowExpectancyObjectiveDesignResultsReviewError(
            f"{field} missing"
        )


def validate_marketflow_expectancy_objective_design_results_review_v1(
    review: dict,
) -> dict[str, Any]:
    """Validate source bindings, output verification, and closed authorities."""
    if not isinstance(review, dict):
        raise MarketFlowExpectancyObjectiveDesignResultsReviewError(
            "review must be a JSON object"
        )
    _expect(
        review.get("schema_version"),
        SCHEMA_VERSION_MARKETFLOW_EXPECTANCY_OBJECTIVE_DESIGN_RESULTS_REVIEW_V1,
        "schema_version",
    )
    _expect(
        review.get("review_scope"),
        EXPECTANCY_OBJECTIVE_DESIGN_RESULTS_REVIEW_ONLY_NOT_GENERATION,
        "review_scope",
    )
    if (
        review.get("review_status")
        == MARKETFLOW_EXPECTANCY_OBJECTIVE_DESIGN_RESULTS_REVIEW_BLOCKED_MISSING_OR_INVALID_OUTPUTS
    ):
        _expect(
            review.get("artifact_kind"),
            ARTIFACT_KIND_MARKETFLOW_EXPECTANCY_OBJECTIVE_DESIGN_RESULTS_REVIEW_BLOCKED,
            "artifact_kind",
        )
        for field in (
            "expectancy_objective_design_results_review_created",
            "expectancy_objective_design_results_review_ready",
            "ready_for_objective_label_or_target_generation_candidate",
            "output_file_inspection_performed",
            "label_generation_authorized",
            "feature_generation_authorized",
            "backtest_execution_authorized",
            "runtime_migration_approved",
            "provider_requests_made_in_review",
            "objective_design_execution_rerun_performed",
        ):
            _expect_false(review.get(field), field)
        digest = review.get(
            "marketflow_expectancy_objective_design_results_review_digest"
        )
        _expect_digest(digest, "review digest")
        _expect(
            digest,
            marketflow_expectancy_objective_design_results_review_digest_v1(review),
            "review digest",
        )
        return {
            "status": "MARKETFLOW_EXPECTANCY_OBJECTIVE_DESIGN_RESULTS_REVIEW_BLOCKED_VALID",
            "review_status": review["review_status"],
            "marketflow_expectancy_objective_design_results_review_digest": digest,
        }

    _expect(
        review.get("artifact_kind"),
        ARTIFACT_KIND_MARKETFLOW_EXPECTANCY_OBJECTIVE_DESIGN_RESULTS_REVIEW_PACKAGE,
        "artifact_kind",
    )
    _expect(
        review.get("review_status"),
        MARKETFLOW_EXPECTANCY_OBJECTIVE_DESIGN_RESULTS_REVIEW_PACKAGE_READY,
        "review_status",
    )
    fixed_fields = {
        "source_expectancy_objective_design_execution_digest": EXPECTED_SOURCE_DESIGN_EXECUTION_DIGEST,
        "source_expectancy_objective_design_output_binding_digest": EXPECTED_SOURCE_DESIGN_OUTPUT_BINDING_DIGEST,
        "source_expectancy_objective_approval_digest": EXPECTED_SOURCE_APPROVAL_DIGEST,
        "source_expectancy_objective_candidate_review_digest": EXPECTED_SOURCE_CANDIDATE_REVIEW_DIGEST,
        "source_expectancy_objective_candidate_digest": EXPECTED_SOURCE_CANDIDATE_DIGEST,
        "selected_objective_path": SELECTED_OBJECTIVE_PATH,
        "target_universe": list(execution_service._source_approval()["target_universe"]),
        "target_universe_count": 12,
        "records_digest": execution_service._source_approval()["records_digest"],
        "meta_record_count": 913,
        "non_meta_record_count": 1003,
        "expected_output_count": 11,
        "observed_output_count": 11,
        "output_digest_mismatch_count": 0,
        "digest_manifest_self_reference_policy": SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE,
        "design_output_review_statuses": REVIEW_STATUSES,
        "next_chain": NEXT_CHAIN,
        "next_gates": NEXT_GATES,
        "risk_controls": RISK_CONTROLS,
    }
    for field, expected in fixed_fields.items():
        _expect(review.get(field), expected, field)

    true_fields = (
        "created_offline",
        "research_only",
        "operator_review_required",
        "expectancy_objective_selected",
        "expectancy_objective_approved",
        "expectancy_objective_authorized",
        "ready_for_expectancy_objective_design_execution",
        "expectancy_objective_design_executed",
        "expectancy_objective_design_results_created",
        "expectancy_objective_design_results_review_created",
        "expectancy_objective_design_results_review_ready",
        "ready_for_objective_label_or_target_generation_candidate",
        "output_file_inspection_performed",
        "meta_reduced_record_count_preserved",
        "no_tracked_marketflow_files",
    )
    false_fields = (
        "objective_label_or_target_generation_candidate_created",
        "objective_label_or_target_generation_approved",
        "objective_label_or_target_generation_performed",
        "expectancy_objective_generation_authorized",
        "expectancy_objective_generation_performed",
        "label_generation_authorized",
        "label_generation_performed",
        "new_targets_created",
        "target_definition_change_authorized",
        "target_definition_change_performed",
        "feature_generation_authorized",
        "feature_generation_performed",
        "feature_label_matrix_created",
        "backtest_execution_authorized",
        "backtest_execution_performed",
        "model_training_authorized",
        "model_training_performed",
        "metric_computation_authorized",
        "metric_computation_performed",
        "strategy_scoring_performed",
        "new_strategy_scoring_performed",
        "predictive_usefulness_acceptance_candidate_created",
        "predictive_usefulness_acceptance_ready",
        "predictive_usefulness_acceptance_recommended",
        "profitability_acceptance_ready",
        "profitability_acceptance_recommended",
        "runtime_migration_approved",
        "runtime_migration_active",
        "automatic_stitching",
        "trade_recommendations_generated",
        "provider_requests_made_in_review",
        "live_provider_transport_enabled_in_review",
        "market_data_acquisition_performed_in_review",
        "dataset_generation_performed_in_review",
        "canonical_dataset_regenerated_in_review",
        "objective_design_execution_rerun_performed",
        "raw_provider_payloads_committed",
        "api_keys_stored_or_printed",
    )
    for field in true_fields:
        _expect_true(review.get(field), field)
    for field in false_fields:
        _expect_false(review.get(field), field)
    for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
        _expect(review.get(field), NOT_AUTHORIZED, field)
    for field in ("predictive_usefulness", "profitability"):
        _expect(review.get(field), NOT_ACCEPTED, field)

    _expect(len(review.get("reviewed_objective_family_selection_report", {})), 10, "objective family count")
    _expect(len(review.get("reviewed_expectancy_payoff_specification", {}).get("future_candidate_fields", [])), 7, "expectancy payoff field count")
    _expect(len(review.get("reviewed_abstention_support_specification", {}).get("future_candidate_fields", [])), 6, "abstention field count")
    _expect(len(review.get("reviewed_material_move_specification", {}).get("future_candidate_fields", [])), 5, "material move field count")
    _expect(review.get("reviewed_objective_label_generation_plan", {}).get("plan_status"), "PLANNED_NOT_EXECUTED", "label generation plan status")
    _expect(len(review.get("reviewed_objective_label_generation_plan", {}).get("planned_steps", [])), 10, "label generation planned steps")
    _expect(len(review.get("reviewed_objective_validation_metric_plan", {})), 14, "validation metric count")
    _expect(len(review.get("reviewed_objective_baseline_comparison_plan", {})), 7, "baseline count")

    verified_files = review.get("verified_output_files")
    if not isinstance(verified_files, list) or len(verified_files) != 11:
        raise MarketFlowExpectancyObjectiveDesignResultsReviewError(
            "verified_output_files mismatch"
        )
    _expect(
        [row.get("filename") for row in verified_files],
        EXPECTED_OUTPUT_FILENAMES,
        "verified output filename order",
    )
    for row in verified_files:
        _expect_digest(row.get("local_sha256"), "local output hash")
        _expect_true(row.get("verified"), "verified output")
        if row.get("filename") == "expectancy_objective_design_digest_manifest.json":
            _expect(row.get("manifest_sha256"), None, "self manifest digest")
            _expect(row.get("digest_kind"), SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE, "self manifest digest kind")
        else:
            _expect(row.get("manifest_sha256"), row.get("local_sha256"), "ordinary output digest")
            _expect(row.get("digest_kind"), "FILE_SHA256", "ordinary output digest kind")
    local_hashes = review.get("local_output_hashes")
    _expect(
        local_hashes,
        {row["filename"]: row["local_sha256"] for row in verified_files},
        "local_output_hashes",
    )
    output_verification = review.get("output_verification")
    if not isinstance(output_verification, dict):
        raise MarketFlowExpectancyObjectiveDesignResultsReviewError(
            "output verification missing"
        )
    for field in (
        "expected_output_count",
        "observed_output_count",
        "output_digest_mismatch_count",
        "output_file_inspection_performed",
        "digest_manifest_self_reference_policy",
        "local_output_hashes",
        "verified_output_files",
    ):
        _expect(output_verification.get(field), review.get(field), f"output verification {field}")

    per_ticker = review.get("per_ticker_objective_results_review")
    if not _per_ticker_digests_valid(per_ticker):
        raise MarketFlowExpectancyObjectiveDesignResultsReviewError(
            "per-ticker review digests mismatch"
        )
    _expect(
        [row.get("ticker") for row in per_ticker],
        review["target_universe"],
        "per-ticker universe",
    )
    for row in per_ticker:
        expected_count = 913 if row["ticker"] == "META" else 1003
        _expect(row.get("historical_record_count"), expected_count, "per-ticker record count")
        _expect(row.get("meta_reduced_record_count_flag"), row["ticker"] == "META", "per-ticker META flag")

    checklist = review.get("review_checklist")
    expected_checklist = _review_checklist(review)
    _expect(checklist, expected_checklist, "review checklist")
    if any(row.get("status") != PASS for row in expected_checklist):
        raise MarketFlowExpectancyObjectiveDesignResultsReviewError(
            "review checklist failed"
        )
    _expect(review.get("review_summary"), _review_summary(expected_checklist), "review summary")
    digest = review.get("marketflow_expectancy_objective_design_results_review_digest")
    _expect_digest(digest, "review digest")
    _expect(
        digest,
        marketflow_expectancy_objective_design_results_review_digest_v1(review),
        "review digest",
    )
    return {
        "status": "MARKETFLOW_EXPECTANCY_OBJECTIVE_DESIGN_RESULTS_REVIEW_VALID",
        "artifact_kind": review["artifact_kind"],
        "review_status": review["review_status"],
        "review_scope": review["review_scope"],
        "marketflow_expectancy_objective_design_results_review_digest": digest,
        **{
            key: review["review_summary"][key]
            for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")
        },
    }


def build_marketflow_expectancy_objective_design_results_review_markdown_v1(
    review: dict,
) -> str:
    """Render a sanitized Markdown view of a ready results-review package."""
    validation = validate_marketflow_expectancy_objective_design_results_review_v1(
        review
    )
    if review.get("review_status") != MARKETFLOW_EXPECTANCY_OBJECTIVE_DESIGN_RESULTS_REVIEW_PACKAGE_READY:
        raise MarketFlowExpectancyObjectiveDesignResultsReviewError(
            "Markdown requires a ready review package"
        )
    sections = [
        ("Title", ["Expectancy Objective Design Results Review v1"]),
        ("Expectancy Objective Design Results Review v1", [f"Artifact/status/scope: {review['artifact_kind']} / {review['review_status']} / {review['review_scope']}.", f"Review digest: {validation['marketflow_expectancy_objective_design_results_review_digest']}."]),
        ("Source Design Execution", [f"Execution/output-binding digests: {review['source_expectancy_objective_design_execution_digest']} / {review['source_expectancy_objective_design_output_binding_digest']}."]),
        ("Bound Evidence", [f"Approval/candidate-review/candidate: {review['source_expectancy_objective_approval_digest']} / {review['source_expectancy_objective_candidate_review_digest']} / {review['source_expectancy_objective_candidate_digest']}.", f"Matrix/features/labels/records: {review['feature_label_matrix_digest']} / {review['feature_values_digest']} / {review['redesigned_label_values_digest']} / {review['records_digest']}."]),
        ("Dataset and Universe", [f"{review['dataset_name']} / {review['total_canonical_record_count']} records.", "Universe: " + ", ".join(review["target_universe"]) + ".", "META remains 913; every non-META ticker remains 1003."]),
        ("Output Verification", [f"Expected/observed/mismatches: {review['expected_output_count']} / {review['observed_output_count']} / {review['output_digest_mismatch_count']}.", f"Self-reference policy: {review['digest_manifest_self_reference_policy']}."]),
        ("Selected Objective Path", [review["selected_objective_path"]]),
        ("Design Philosophy Review", [review["design_philosophy_review"]]),
        ("Objective Family Selection Report Review", [f"{name}: {value['design_role']}." for name, value in review["reviewed_objective_family_selection_report"].items()]),
        ("Expectancy Payoff Specification Review", review["reviewed_expectancy_payoff_specification"]["future_candidate_fields"]),
        ("Abstention Support Specification Review", review["reviewed_abstention_support_specification"]["future_candidate_fields"]),
        ("Material Move Specification Review", review["reviewed_material_move_specification"]["future_candidate_fields"]),
        ("Label Generation Plan Boundary", ["PLANNED_NOT_EXECUTED; no labels or targets were generated."]),
        ("Validation Metric Plan Boundary", ["14 metrics remain PLANNED_NOT_COMPUTED."]),
        ("Baseline Comparison Plan Boundary", ["7 baselines remain PLANNED_NOT_EXECUTED."]),
        ("Per-Ticker Objective Review", [f"{row['ticker']}: records {row['historical_record_count']}, digest {row['per_ticker_expectancy_objective_design_results_review_digest']}." for row in review["per_ticker_objective_results_review"]]),
        ("Output Digest Manifest", [f"{row['filename']}: {row['local_sha256']}." for row in review["verified_output_files"]]),
        ("Next Chain", review["next_chain"]),
        ("Next Gates", review["next_gates"]),
        ("Risk Controls", review["risk_controls"]),
        ("Predictive Usefulness Boundary", ["Predictive usefulness remains not accepted."]),
        ("Profitability Boundary", ["Profitability remains not accepted."]),
        ("Runtime Boundary", ["Runtime, strategy, paper trading, and broker execution remain NOT_AUTHORIZED."]),
        ("Checklist Summary", [f"Total/passed/failed/blockers: {review['review_summary']['total_checks']} / {review['review_summary']['passed_checks']} / {review['review_summary']['failed_checks']} / {review['review_summary']['blocker_count']}."]),
        ("Guardrails", ["Review only: no provider, acquisition, generation, backtest, training, metrics, recommendations, acceptance, runtime, or trading action occurred."]),
    ]
    lines = ["# Expectancy Objective Design Results Review v1", ""]
    for title, rows in sections:
        lines.extend([f"## {title}", *[f"- {row}" for row in rows], ""])
    return "\n".join(lines)


def write_marketflow_expectancy_objective_design_results_review_v1(
    output_dir: str | Path,
    *,
    output_root: str | Path | None = None,
) -> dict[str, Any]:
    """Write canonical review JSON once without modifying source outputs."""
    review = build_marketflow_expectancy_objective_design_results_review_v1(
        output_root=output_root
    )
    validation = validate_marketflow_expectancy_objective_design_results_review_v1(
        review
    )
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "marketflow_expectancy_objective_design_results_review_v1.json"
    payload = canonical_json_bytes(review)
    try:
        with path.open("xb") as handle:
            handle.write(payload)
    except FileExistsError as exc:
        raise MarketFlowExpectancyObjectiveDesignResultsReviewError(
            "expectancy objective design results review output already exists"
        ) from exc
    return {
        "path": str(path),
        "artifact_kind": review["artifact_kind"],
        "review_status": review["review_status"],
        "marketflow_expectancy_objective_design_results_review_digest": validation[
            "marketflow_expectancy_objective_design_results_review_digest"
        ],
        "payload_sha256": sha256_bytes(payload),
    }
