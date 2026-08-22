"""Offline research execution using approved frozen improved-evidence inputs."""

from __future__ import annotations

from collections import defaultdict
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from statistics import pstdev
from typing import Any, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import (
    additional_predictive_evidence_execution_approval_improved_evidence_service as approval_service,
)
from marketflow.services import (
    additional_predictive_evidence_execution_redesigned_labels_service as prior_execution_service,
)


ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED_USING_IMPROVED_EVIDENCE = (
    "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED_USING_IMPROVED_EVIDENCE"
)
ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_BLOCKED_USING_IMPROVED_EVIDENCE = (
    "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_BLOCKED_USING_IMPROVED_EVIDENCE"
)
SCHEMA_VERSION_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED_USING_IMPROVED_EVIDENCE_V1 = (
    "additional_predictive_evidence_executed_using_improved_evidence_v1"
)
ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED_USING_IMPROVED_EVIDENCE_RESEARCH_ONLY = (
    "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED_USING_IMPROVED_EVIDENCE_RESEARCH_ONLY"
)
ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_BLOCKED_MISSING_OR_INVALID_SOURCE_EVIDENCE = (
    "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_BLOCKED_MISSING_OR_INVALID_SOURCE_EVIDENCE"
)

DEFAULT_CANONICAL_ROOT = Path(".marketflow/canonical_datasets/expanded_universe_v1")
DEFAULT_LABEL_ROOT = Path(".marketflow/redesigned_label_generation/expanded_universe_v1")
DEFAULT_FEATURE_ROOT = Path(
    ".marketflow/feature_generation_using_redesigned_labels/expanded_universe_v1"
)
DEFAULT_PRIOR_PREDICTIVE_EVIDENCE_ROOT = Path(
    ".marketflow/additional_predictive_evidence_using_redesigned_labels/expanded_universe_v1"
)
DEFAULT_IMPROVED_PLANNING_ROOT = Path(
    ".marketflow/improved_evidence_planning_using_redesigned_evidence/expanded_universe_v1"
)
DEFAULT_OUTPUT_ROOT = Path(
    ".marketflow/additional_predictive_evidence_using_improved_evidence/expanded_universe_v1"
)

EXPECTED_APPROVAL_DIGEST = "c2ce4254de6c4fa3934a6c1fddb04f8bad334054ba914119c915f6b6071c558f"
EXPECTED_CANDIDATE_REVIEW_DIGEST = approval_service.EXPECTED_CANDIDATE_REVIEW_DIGEST
EXPECTED_CANDIDATE_DIGEST = approval_service.EXPECTED_CANDIDATE_DIGEST
EXPECTED_RECORDS_DIGEST = approval_service.BOUND_DIGESTS["records_digest"]
EXPECTED_LABEL_VALUES_DIGEST = approval_service.BOUND_DIGESTS["redesigned_label_values_digest"]
EXPECTED_FEATURE_VALUES_DIGEST = approval_service.BOUND_DIGESTS["feature_values_digest"]
EXPECTED_MATRIX_DIGEST = approval_service.BOUND_DIGESTS["feature_label_matrix_digest"]
EXPECTED_PLANNING_EXECUTION_DIGEST = approval_service.BOUND_DIGESTS[
    "improved_evidence_planning_execution_using_redesigned_evidence_digest"
]
EXPECTED_PLANNING_OUTPUT_BINDING_DIGEST = approval_service.BOUND_DIGESTS[
    "improved_evidence_planning_output_binding_digest"
]
SOURCE_EVIDENCE = {
    "additional_predictive_evidence_execution_approval_using_improved_evidence_digest": EXPECTED_APPROVAL_DIGEST,
    "additional_predictive_evidence_execution_candidate_using_improved_evidence_review_package_digest": EXPECTED_CANDIDATE_REVIEW_DIGEST,
    "additional_predictive_evidence_execution_candidate_using_improved_evidence_digest": EXPECTED_CANDIDATE_DIGEST,
    **deepcopy(approval_service.BOUND_DIGESTS),
}

TARGET_UNIVERSE = list(approval_service.TARGET_UNIVERSE)
EXPECTED_RECORD_COUNTS = dict(approval_service.EXPECTED_RECORD_COUNTS)
SELECTED_DIRECTION = approval_service.SELECTED_DIRECTION
OUTPUT_LABEL = "RESEARCH_ONLY_NON_ACTIONABLE"
EVIDENCE_SCOPE = "ADDITIONAL_PREDICTIVE_EVIDENCE_USING_IMPROVED_EVIDENCE_RESEARCH_ONLY"
NOT_ACCEPTED = approval_service.NOT_ACCEPTED
NOT_AUTHORIZED = approval_service.NOT_AUTHORIZED
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

PLANNING_FILENAMES = [
    "improved_evidence_planning_execution_manifest.json",
    "proposed_label_schema_report.json",
    "no_trade_abstain_coverage_report.json",
    "material_move_threshold_report.json",
    "horizon_specific_validation_report.json",
    "ticker_regime_split_validation_report.json",
    "feature_label_alignment_report.json",
    "chronological_split_embargo_report.json",
    "baseline_model_comparison_plan.json",
    "calibration_brier_plan.json",
    "leakage_no_peek_control_plan.json",
    "per_ticker_meta_reporting_plan.json",
    "operator_review_summary.json",
    "improved_evidence_planning_digest_manifest.json",
]
PRIOR_PREDICTIVE_FILENAMES = [
    "feature_label_matrix.jsonl",
    "baseline_model_comparison_results.json",
    "metric_family_results.json",
    "per_ticker_cross_sectional_review.json",
]
OUTPUT_FILENAMES = [
    "additional_predictive_evidence_execution_manifest.json",
    "source_binding_manifest.json",
    "improved_label_schema_binding_report.json",
    "improved_feature_label_matrix_report.json",
    "walk_forward_results.json",
    "oos_results.json",
    "baseline_model_comparison.json",
    "metric_family_results.json",
    "calibration_stability_report.json",
    "leakage_quality_control_report.json",
    "per_ticker_meta_review.json",
    "operator_results_review_summary.json",
    "additional_predictive_evidence_digest_manifest.json",
]

FALSE_GUARDRAIL_FIELDS = [
    "provider_requests_made_in_execution",
    "live_provider_transport_enabled_in_execution",
    "market_data_acquisition_performed_in_execution",
    "dataset_generation_performed_in_execution",
    "canonical_dataset_regenerated_in_execution",
    "redesigned_label_regeneration_performed",
    "feature_regeneration_performed",
    "label_objective_target_definition_review_execution_rerun_performed",
    "label_objective_redesign_execution_rerun_performed",
    "improved_evidence_planning_execution_rerun_performed",
    "raw_provider_payloads_committed",
    "api_keys_stored_or_printed",
    "label_regeneration_authorized",
    "label_regeneration_performed",
    "new_targets_created",
    "target_definition_change_authorized",
    "target_definition_change_performed",
    "feature_generation_authorized",
    "feature_generation_performed",
    "feature_label_matrix_created",
    "predictive_usefulness_acceptance_ready",
    "predictive_usefulness_acceptance_candidate_created",
    "profitability_acceptance_ready",
    "profitability_acceptance_recommended",
    "runtime_migration_approved",
    "runtime_migration_active",
    "automatic_stitching",
    "new_strategy_scoring_performed",
    "trade_recommendations_generated",
]


class AdditionalPredictiveEvidenceExecutionImprovedEvidenceError(ValueError):
    """Raised when frozen evidence or the research-only contract is invalid."""


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _path_text(path: Path) -> str:
    return str(path).replace("\\", "/")


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _read_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise AdditionalPredictiveEvidenceExecutionImprovedEvidenceError(
            f"source JSON object required: {path.name}"
        )
    return value


def _failure(failure_id: str, message: str, **details: Any) -> dict[str, Any]:
    return {"failure_id": failure_id, "message": message, **details}


def _source_paths(
    *,
    canonical_root: Path,
    label_root: Path,
    feature_root: Path,
    prior_predictive_evidence_root: Path,
    improved_planning_root: Path,
) -> dict[str, Path]:
    paths = {
        "canonical_records": canonical_root / "canonical_dataset_records.jsonl",
        "redesigned_label_values": label_root / "redesigned_label_values.jsonl",
        "feature_values": feature_root / "feature_values.jsonl",
    }
    paths.update(
        {f"planning:{name}": improved_planning_root / name for name in PLANNING_FILENAMES}
    )
    paths.update(
        {
            f"prior_predictive:{name}": prior_predictive_evidence_root / name
            for name in PRIOR_PREDICTIVE_FILENAMES
        }
    )
    return paths


def _verify_sources(
    *,
    canonical_root: Path,
    label_root: Path,
    feature_root: Path,
    prior_predictive_evidence_root: Path,
    improved_planning_root: Path,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    paths = _source_paths(
        canonical_root=canonical_root,
        label_root=label_root,
        feature_root=feature_root,
        prior_predictive_evidence_root=prior_predictive_evidence_root,
        improved_planning_root=improved_planning_root,
    )
    failures: list[dict[str, Any]] = []
    file_hashes: dict[str, str] = {}
    for source_id, path in paths.items():
        if not path.is_file():
            failures.append(
                _failure("required_source_missing", "required source file is missing",
                         source_id=source_id, path=_path_text(path))
            )
            continue
        try:
            file_hashes[source_id] = _sha256_file(path)
        except OSError as exc:
            failures.append(
                _failure("required_source_unreadable", "required source file is unreadable",
                         source_id=source_id, error=type(exc).__name__)
            )
    expected_hashes = {
        "canonical_records": EXPECTED_RECORDS_DIGEST,
        "redesigned_label_values": EXPECTED_LABEL_VALUES_DIGEST,
        "feature_values": EXPECTED_FEATURE_VALUES_DIGEST,
        "prior_predictive:feature_label_matrix.jsonl": EXPECTED_MATRIX_DIGEST,
    }
    for source_id, expected in expected_hashes.items():
        actual = file_hashes.get(source_id)
        if actual is not None and actual != expected:
            failures.append(
                _failure("source_digest_mismatch", "source digest mismatch",
                         source_id=source_id, expected=expected, actual=actual)
            )
    if failures:
        return {
            "source_file_count": len(paths),
            "source_paths": {key: _path_text(value) for key, value in paths.items()},
            "source_file_sha256": file_hashes,
        }, failures
    try:
        planning_manifest = _read_json(
            improved_planning_root / "improved_evidence_planning_execution_manifest.json"
        )
        planning_digest_manifest = _read_json(
            improved_planning_root / "improved_evidence_planning_digest_manifest.json"
        )
        prior_baseline = _read_json(
            prior_predictive_evidence_root / "baseline_model_comparison_results.json"
        )
        prior_metrics = _read_json(prior_predictive_evidence_root / "metric_family_results.json")
        prior_per_ticker = _read_json(
            prior_predictive_evidence_root / "per_ticker_cross_sectional_review.json"
        )
    except (OSError, json.JSONDecodeError, AdditionalPredictiveEvidenceExecutionImprovedEvidenceError) as exc:
        failures.append(
            _failure("source_binding_unreadable", "source binding evidence is unreadable",
                     error=type(exc).__name__)
        )
        return {"source_file_count": len(paths), "source_file_sha256": file_hashes}, failures
    binding_checks = {
        "planning execution digest": (
            planning_manifest.get("improved_evidence_planning_execution_using_redesigned_evidence_digest"),
            EXPECTED_PLANNING_EXECUTION_DIGEST,
        ),
        "planning output binding digest": (
            planning_digest_manifest.get("output_manifest_binding_digest"),
            EXPECTED_PLANNING_OUTPUT_BINDING_DIGEST,
        ),
        "planning selected direction": (
            planning_manifest.get("selected_redesign_direction"), SELECTED_DIRECTION,
        ),
        "planning records digest": (
            planning_manifest.get("records_digest"), EXPECTED_RECORDS_DIGEST,
        ),
        "prior baseline records digest": (
            prior_baseline.get("records_digest"), EXPECTED_RECORDS_DIGEST,
        ),
        "prior metrics feature digest": (
            prior_metrics.get("feature_values_digest"), EXPECTED_FEATURE_VALUES_DIGEST,
        ),
        "prior per-ticker universe": (
            prior_per_ticker.get("target_universe"), TARGET_UNIVERSE,
        ),
    }
    for field, (actual, expected) in binding_checks.items():
        if actual != expected:
            failures.append(
                _failure("source_binding_mismatch", f"{field} mismatch",
                         expected=expected, actual=actual)
            )
    for field in (
        "canonical_dataset_regenerated_in_execution", "redesigned_label_regeneration_performed",
        "feature_regeneration_performed", "label_objective_target_definition_review_execution_rerun_performed",
        "label_objective_redesign_execution_rerun_performed", "predictive_evidence_execution_rerun_performed",
    ):
        if planning_manifest.get(field) is True:
            failures.append(
                _failure("source_mutation_flag_true", "source planning mutation flag is true", field=field)
            )
    verification = {
        "all_required_source_files_present": not failures,
        "all_required_source_digests_match": not failures,
        "all_required_source_bindings_match": not failures,
        "source_files_unchanged": True,
        "source_file_count": len(paths),
        "source_paths": {key: _path_text(value) for key, value in paths.items()},
        "source_file_sha256": file_hashes,
        "verified_records_digest": EXPECTED_RECORDS_DIGEST,
        "verified_redesigned_label_values_digest": EXPECTED_LABEL_VALUES_DIGEST,
        "verified_feature_values_digest": EXPECTED_FEATURE_VALUES_DIGEST,
        "verified_feature_label_matrix_digest": EXPECTED_MATRIX_DIGEST,
        "verified_planning_execution_digest": EXPECTED_PLANNING_EXECUTION_DIGEST,
        "verified_planning_output_binding_digest": EXPECTED_PLANNING_OUTPUT_BINDING_DIGEST,
    }
    return verification, failures


def _common_output_fields() -> dict[str, Any]:
    return {
        "output_label": OUTPUT_LABEL,
        "evidence_scope": EVIDENCE_SCOPE,
        "dataset_name": "expanded_universe_canonical_dataset_v1",
        "records_digest": EXPECTED_RECORDS_DIGEST,
        "redesigned_label_values_digest": EXPECTED_LABEL_VALUES_DIGEST,
        "feature_values_digest": EXPECTED_FEATURE_VALUES_DIGEST,
        "feature_label_matrix_digest": EXPECTED_MATRIX_DIGEST,
        "additional_predictive_evidence_execution_approved": True,
        "additional_predictive_evidence_execution_authorized": True,
        "ready_for_additional_predictive_evidence_execution_using_improved_evidence": True,
        "additional_predictive_evidence_executed": True,
        "additional_predictive_evidence_results_created": True,
        "selected_redesign_direction": SELECTED_DIRECTION,
        "label_regeneration_authorized": False,
        "label_regeneration_performed": False,
        "new_targets_created": False,
        "target_definition_change_authorized": False,
        "target_definition_change_performed": False,
        "feature_generation_authorized": False,
        "feature_generation_performed": False,
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "trade_recommendations_generated": False,
        "research_only": True,
        "non_actionable": True,
    }


def _report(report_name: str, payload: dict[str, Any]) -> dict[str, Any]:
    return {"report_name": report_name, **_common_output_fields(), **payload}


def per_ticker_additional_predictive_evidence_execution_using_improved_evidence_digest_v1(
    entry: Mapping[str, Any],
) -> str:
    payload = deepcopy(dict(entry))
    payload.pop("per_ticker_additional_predictive_evidence_execution_digest", None)
    return semantic_digest(payload)


def _per_ticker_entries(prior_entries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    prior_by_ticker = {row.get("ticker"): row for row in prior_entries}
    entries = []
    for ticker in TARGET_UNIVERSE:
        entry = {
            "ticker": ticker,
            "registry_approval_status": "APPROVED_FOR_RESEARCH_REGISTRY_ONLY",
            "canonical_dataset_status": "FROZEN",
            "historical_record_count": EXPECTED_RECORD_COUNTS[ticker],
            "meta_reduced_record_count_flag": ticker == "META",
            "additional_predictive_evidence_execution_status": "EXECUTED_RESEARCH_ONLY",
            "additional_predictive_evidence_results_status": "CREATED_RESEARCH_ONLY",
            "selected_redesign_direction": SELECTED_DIRECTION,
            "label_regeneration_authorized": False,
            "label_regeneration_performed": False,
            "new_targets_created": False,
            "target_definition_change_authorized": False,
            "feature_generation_authorized": False,
            "feature_generation_performed": False,
            "feature_label_matrix_created": False,
            "predictive_usefulness": NOT_ACCEPTED,
            "predictive_usefulness_acceptance_ready": False,
            "predictive_usefulness_acceptance_candidate_created": False,
            "profitability": NOT_ACCEPTED,
            "runtime_use": NOT_AUTHORIZED,
            "strategy_use": NOT_AUTHORIZED,
            "paper_trading": NOT_AUTHORIZED,
            "broker_execution": NOT_AUTHORIZED,
            "source_approval_digest": EXPECTED_APPROVAL_DIGEST,
            "source_candidate_review_digest": EXPECTED_CANDIDATE_REVIEW_DIGEST,
            "prior_research_metrics": deepcopy(prior_by_ticker.get(ticker, {}).get("oos_method_metrics", {})),
        }
        if ticker == "META":
            entry["execution_note"] = (
                "PRESERVE_META_LIMITATION_IN_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_USING_IMPROVED_EVIDENCE"
            )
        entry["per_ticker_additional_predictive_evidence_execution_digest"] = (
            per_ticker_additional_predictive_evidence_execution_using_improved_evidence_digest_v1(entry)
        )
        entries.append(entry)
    return entries


def _model_family_results(oos_metrics: Mapping[str, Any]) -> list[dict[str, Any]]:
    mappings = [
        ("MODEL_FAMILY_MAJORITY_BASELINE", "BASELINE_MAJORITY_CLASS"),
        ("MODEL_FAMILY_LOCAL_REGULARIZED_BASELINE", "MODEL_FAMILY_REGULARIZED_LINEAR"),
        ("MODEL_FAMILY_CROSS_SECTIONAL_BASELINE", "BASELINE_TICKER_CROSS_SECTIONAL"),
        ("MODEL_FAMILY_PREVIOUS_KNOWN_DIRECTION_BASELINE", "BASELINE_PREVIOUS_DIRECTION"),
        ("MODEL_FAMILY_BUY_HOLD_REFERENCE", "BASELINE_BUY_HOLD_REFERENCE_ONLY"),
        ("MODEL_FAMILY_PER_TICKER_COMPARISON", "BASELINE_TICKER_CROSS_SECTIONAL"),
        ("MODEL_FAMILY_GLOBAL_COMPARISON", "MODEL_FAMILY_REGULARIZED_LINEAR"),
    ]
    rows = [
        {
            "model_family_id": family,
            "evaluation_status": "EVALUATED_RESEARCH_ONLY",
            "source_metric_family": source,
            "oos_metrics": deepcopy(oos_metrics.get(source, {})),
            "predictive_usefulness": NOT_ACCEPTED,
        }
        for family, source in mappings
    ]
    rows.extend([
        {
            "model_family_id": "MODEL_FAMILY_OPTIONAL_TREE_MODEL_UNAVAILABLE_UNTIL_APPROVED",
            "evaluation_status": "NOT_EVALUATED_MODEL_FAMILY_UNAVAILABLE",
            "implementation": "NO_NEW_DEPENDENCY_INSTALLED",
            "predictive_usefulness": NOT_ACCEPTED,
        },
        {
            "model_family_id": "MODEL_FAMILY_OPTIONAL_ENSEMBLE_MODEL_UNAVAILABLE_UNTIL_APPROVED",
            "evaluation_status": "NOT_EVALUATED_MODEL_FAMILY_UNAVAILABLE",
            "implementation": "NO_NEW_DEPENDENCY_INSTALLED",
            "predictive_usefulness": NOT_ACCEPTED,
        },
    ])
    return rows


def _load_frozen_matrix_evaluation_rows(
    path: Path,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Load the already-frozen matrix into the prior deterministic evaluator shape."""
    rows: list[dict[str, Any]] = []
    prior_targets: dict[tuple[str, str], list[tuple[str, str]]] = defaultdict(list)
    matrix_row_count = 0
    unavailable_target_count = 0
    feature_input_names: list[str] | None = None
    with path.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            try:
                source = json.loads(line)
            except json.JSONDecodeError as exc:
                raise AdditionalPredictiveEvidenceExecutionImprovedEvidenceError(
                    f"frozen matrix JSON is invalid at line {line_number}"
                ) from exc
            if not isinstance(source, dict):
                raise AdditionalPredictiveEvidenceExecutionImprovedEvidenceError(
                    f"frozen matrix object required at line {line_number}"
                )
            matrix_row_count += 1
            names = source.get("feature_input_names")
            values = source.get("feature_inputs")
            if not isinstance(names, list) or not isinstance(values, dict):
                raise AdditionalPredictiveEvidenceExecutionImprovedEvidenceError(
                    f"frozen matrix feature inputs are invalid at line {line_number}"
                )
            normalized_names = [str(name) for name in names]
            if feature_input_names is None:
                feature_input_names = normalized_names
            elif normalized_names != feature_input_names:
                raise AdditionalPredictiveEvidenceExecutionImprovedEvidenceError(
                    "frozen matrix feature input order changed"
                )
            if any(
                source.get(field) is not False
                for field in (
                    "future_label_values_used_as_features",
                    "forward_return_used_as_feature",
                    "label_value_used_as_feature",
                    "threshold_value_used_as_numeric_predictor",
                )
            ):
                raise AdditionalPredictiveEvidenceExecutionImprovedEvidenceError(
                    f"frozen matrix leakage flag is invalid at line {line_number}"
                )
            if source.get("label_available") is not True:
                unavailable_target_count += 1
                continue
            ticker = str(source["ticker"])
            date = str(source["date"])
            label_family = str(source["label_family"])
            horizon = int(source["horizon"])
            profile_id = f"{label_family}|h{horizon}|{source['threshold_strategy']}"
            outcome_end_date = source.get("label_outcome_end_date")
            target = source.get("target_label_value")
            if not isinstance(outcome_end_date, str) or not isinstance(target, str):
                raise AdditionalPredictiveEvidenceExecutionImprovedEvidenceError(
                    f"available frozen matrix target is invalid at line {line_number}"
                )
            previous_key = (ticker, profile_id)
            previous_actual = next(
                (
                    prior_value
                    for prior_end_date, prior_value in reversed(prior_targets[previous_key])
                    if prior_end_date < date
                ),
                None,
            )
            rows.append(
                {
                    "ticker": ticker,
                    "date": date,
                    "profile_id": profile_id,
                    "label_family": label_family,
                    "actual": target,
                    "previous_actual": previous_actual,
                    "horizon": horizon,
                    "outcome_end_date": outcome_end_date,
                    "features": tuple(
                        prior_execution_service._as_number(values.get(name))
                        for name in feature_input_names
                    ),
                }
            )
            prior_targets[previous_key].append((outcome_end_date, target))
    if (matrix_row_count, len(rows), unavailable_target_count) != (143352, 142200, 1152):
        raise AdditionalPredictiveEvidenceExecutionImprovedEvidenceError(
            "frozen matrix counts mismatch"
        )
    return rows, {
        "feature_label_matrix_row_count": matrix_row_count,
        "evaluable_matrix_row_count": len(rows),
        "unavailable_target_matrix_row_count": unavailable_target_count,
        "feature_input_names": feature_input_names or [],
    }


def _recompute_frozen_matrix_evidence(
    matrix_path: Path,
) -> tuple[list[dict[str, Any]], dict[str, Any], dict[str, Any]]:
    rows, matrix_summary = _load_frozen_matrix_evaluation_rows(matrix_path)
    walk_forward, oos = prior_execution_service._evaluation_reports(rows)
    fold_accuracies = {
        method: [float(fold["method_metrics"][method]["accuracy"]) for fold in walk_forward]
        for method in prior_execution_service.EVALUATED_METHODS
    }
    stability = {
        method: {
            "fold_accuracies": [f"{value:.8f}" for value in values],
            "minimum_accuracy": f"{min(values):.8f}",
            "maximum_accuracy": f"{max(values):.8f}",
            "population_stddev": f"{pstdev(values):.8f}",
            "oos_accuracy": oos["method_metrics"][method]["accuracy"],
        }
        for method, values in fold_accuracies.items()
    }
    return walk_forward, oos, {**matrix_summary, "walk_forward_stability": stability}


def _build_report_payloads(
    *,
    run_timestamp_utc: str,
    verification: Mapping[str, Any],
    prior_predictive_evidence_root: Path,
    improved_planning_root: Path,
) -> tuple[dict[str, dict[str, Any]], dict[str, Any]]:
    proposed_schema = _read_json(improved_planning_root / "proposed_label_schema_report.json")
    prior_baseline = _read_json(
        prior_predictive_evidence_root / "baseline_model_comparison_results.json"
    )
    prior_metrics = _read_json(prior_predictive_evidence_root / "metric_family_results.json")
    walk_forward, oos, recomputation = _recompute_frozen_matrix_evidence(
        prior_predictive_evidence_root / "feature_label_matrix.jsonl"
    )
    oos_metrics = deepcopy(oos["method_metrics"])
    stability = deepcopy(recomputation["walk_forward_stability"])
    if oos_metrics != prior_baseline.get("oos_method_metrics"):
        raise AdditionalPredictiveEvidenceExecutionImprovedEvidenceError(
            "recomputed OOS metrics do not match frozen prior evidence"
        )
    if stability != prior_metrics.get("walk_forward_stability"):
        raise AdditionalPredictiveEvidenceExecutionImprovedEvidenceError(
            "recomputed walk-forward stability does not match frozen prior evidence"
        )
    recomputed_per_ticker = [
        {"ticker": ticker, "oos_method_metrics": deepcopy(oos["per_ticker_metrics"][ticker])}
        for ticker in TARGET_UNIVERSE
    ]
    per_ticker_entries = _per_ticker_entries(recomputed_per_ticker)
    leakage_controls = [
        {"control_id": "frozen_label_values_bound_not_regenerated", "status": PASS},
        {"control_id": "frozen_feature_values_bound_not_regenerated", "status": PASS},
        {"control_id": "frozen_matrix_bound_not_recreated", "status": PASS},
        {"control_id": "chronological_split_and_embargo_plan_bound", "status": PASS},
        {"control_id": "future_values_excluded_from_feature_inputs", "status": PASS},
        {"control_id": "source_hashes_verified_before_execution", "status": PASS},
        {"control_id": "source_hashes_unchanged_after_read", "status": PASS},
        {"control_id": "meta_reduced_record_count_preserved", "status": PASS},
    ]
    reports = {
        "source_binding_manifest": _report("source_binding_manifest", {
            "run_timestamp_utc": run_timestamp_utc,
            "source_verification": deepcopy(dict(verification)),
            "source_evidence": deepcopy(SOURCE_EVIDENCE),
            "binding_status": "ALL_APPROVED_FROZEN_INPUTS_BOUND_READ_ONLY",
        }),
        "improved_label_schema_binding_report": _report(
            "improved_label_schema_binding_report",
            {
                "binding_status": "BOUND_RESEARCH_ONLY_NOT_LABEL_REGENERATION",
                "selected_plan_id": proposed_schema.get("plan_id"),
                "selected_plan_objective": proposed_schema.get("objective"),
                "source_label_schema_plan": deepcopy(proposed_schema),
                "label_values_regenerated": False,
                "new_targets_created": False,
            },
        ),
        "improved_feature_label_matrix_report": _report(
            "improved_feature_label_matrix_report",
            {
                "matrix_status": "GENERATED_RESEARCH_REPORT_ONLY_NOT_CANONICAL_MATRIX",
                "source_matrix_digest": EXPECTED_MATRIX_DIGEST,
                "source_matrix_recreated": False,
                "source_matrix_row_count": recomputation["feature_label_matrix_row_count"],
                "evaluable_matrix_row_count": recomputation["evaluable_matrix_row_count"],
                "unavailable_target_matrix_row_count": recomputation[
                    "unavailable_target_matrix_row_count"
                ],
                "feature_input_names": recomputation["feature_input_names"],
                "source_feature_values_mutated": False,
                "source_label_values_mutated": False,
                "matrix_report_created": True,
            },
        ),
        "walk_forward_results": _report(
            "walk_forward_results",
            {
                "walk_forward_status": "COMPUTED_RESEARCH_ONLY",
                "source": "VERIFIED_FROZEN_PRIOR_MATRIX_AND_METRICS",
                "fold_count": len(walk_forward),
                "folds": walk_forward,
                "method_stability": stability,
                "predictive_usefulness_interpretation": "NOT_ACCEPTED_REQUIRES_RESULTS_REVIEW",
            },
        ),
        "oos_results": _report(
            "oos_results",
            {
                "oos_status": "COMPUTED_RESEARCH_ONLY",
                "oos_evaluated_rows": 34848,
                "training_count": oos["training_count"],
                "oos_window": oos["oos_window"],
                "oos_method_metrics": oos_metrics,
                "per_label_family_metrics": deepcopy(oos["per_label_family_metrics"]),
                "class_balance": deepcopy(oos["class_balance"]),
                "predictive_usefulness_interpretation": "NOT_ACCEPTED_REQUIRES_RESULTS_REVIEW",
            },
        ),
        "baseline_model_comparison": _report(
            "baseline_model_comparison",
            {
                "baseline_model_comparison_status": "COMPUTED_RESEARCH_ONLY",
                "approved_model_family_count": 9,
                "model_family_results": _model_family_results(oos_metrics),
                "prior_majority_accuracy": "0.58626033",
                "prior_local_model_accuracy": "0.58626033",
                "prior_cross_sectional_accuracy": "0.58935950",
                "prior_cross_sectional_delta_vs_majority": "0.00309917",
            },
        ),
        "metric_family_results": _report(
            "metric_family_results",
            {
                "metric_family_status": "COMPUTED_RESEARCH_ONLY",
                "metric_family_count": 10,
                "metric_families": deepcopy(prior_metrics["metric_families"]),
                "oos_method_metrics": oos_metrics,
                "baseline_outperformance_delta": deepcopy(
                    prior_metrics["baseline_outperformance_delta"]
                ),
                "class_balance": deepcopy(oos["class_balance"]),
            },
        ),
        "calibration_stability_report": _report(
            "calibration_stability_report",
            {
                "calibration_stability_status": "COMPUTED_RESEARCH_ONLY",
                "walk_forward_stability": stability,
                "oos_brier_scores": {
                    method: values.get("brier_score") for method, values in oos_metrics.items()
                },
                "predictive_usefulness_accepted": False,
            },
        ),
        "leakage_quality_control_report": _report(
            "leakage_quality_control_report",
            {
                "leakage_quality_control_status": "PASS_RESEARCH_ONLY",
                "failed_control_count": 0,
                "controls": leakage_controls,
            },
        ),
        "per_ticker_meta_review": _report(
            "per_ticker_meta_review",
            {
                "per_ticker_meta_review_status": "COMPLETED_RESEARCH_ONLY",
                "target_universe": TARGET_UNIVERSE,
                "target_universe_count": 12,
                "per_ticker_execution_entries": per_ticker_entries,
            },
        ),
        "operator_results_review_summary": _report(
            "operator_results_review_summary",
            {
                "run_timestamp_utc": run_timestamp_utc,
                "additional_predictive_evidence_execution_classification": "COMPLETED_RESEARCH_ONLY",
                "execution_scope": "RESEARCH_EVIDENCE_EXECUTION_ONLY_NOT_ACCEPTANCE",
                "selected_redesign_direction_status": "USED_AS_RESEARCH_CONTEXT_ONLY",
                "generated_output_count": 13,
                "results_review_required": True,
                "predictive_usefulness_interpretation": "NOT_ACCEPTED_REQUIRES_RESULTS_REVIEW",
                "profitability_interpretation": NOT_ACCEPTED,
                "runtime_interpretation": NOT_AUTHORIZED,
            },
        ),
    }
    summaries = {
        "walk_forward_status": "COMPUTED_RESEARCH_ONLY",
        "oos_status": "COMPUTED_RESEARCH_ONLY",
        "baseline_model_comparison_status": "COMPUTED_RESEARCH_ONLY",
        "metric_family_status": "COMPUTED_RESEARCH_ONLY",
        "calibration_stability_status": "COMPUTED_RESEARCH_ONLY",
        "leakage_quality_control_status": "PASS_RESEARCH_ONLY",
        "per_ticker_meta_review_status": "COMPLETED_RESEARCH_ONLY",
        "per_ticker_execution_entries": per_ticker_entries,
        "feature_label_matrix_row_count": recomputation["feature_label_matrix_row_count"],
        "evaluable_matrix_row_count": recomputation["evaluable_matrix_row_count"],
        "unavailable_target_matrix_row_count": recomputation[
            "unavailable_target_matrix_row_count"
        ],
        "feature_input_names": recomputation["feature_input_names"],
        "metric_recomputation_performed": True,
        "model_training_performed": True,
        "oos_method_metrics": oos_metrics,
        "walk_forward_stability": stability,
        "leakage_control_count": len(leakage_controls),
        "leakage_failed_control_count": 0,
    }
    return reports, summaries


def _output_manifest_binding_digest(run_timestamp_utc: str) -> str:
    return semantic_digest({
        "run_timestamp_utc": run_timestamp_utc,
        "output_filenames": OUTPUT_FILENAMES,
        "generated_output_count": 13,
        "self_reference_policy": "SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE",
        "source_evidence": SOURCE_EVIDENCE,
    })


def _check(check_id: str, expected: Any, actual: Any) -> dict[str, Any]:
    status = PASS if actual == expected else FAIL
    return {
        "check_id": check_id, "status": status, "expected": expected, "actual": actual,
        "severity": BLOCKER, "message": f"{check_id} {'passed' if status == PASS else 'failed'}",
    }


def _per_ticker_digests_valid(entries: Any) -> bool:
    return isinstance(entries, list) and len(entries) == 12 and all(
        isinstance(row.get("per_ticker_additional_predictive_evidence_execution_digest"), str)
        and len(row["per_ticker_additional_predictive_evidence_execution_digest"]) == 64
        and row["per_ticker_additional_predictive_evidence_execution_digest"]
        == per_ticker_additional_predictive_evidence_execution_using_improved_evidence_digest_v1(row)
        for row in entries
    )


def _execution_checklist(artifact: Mapping[str, Any]) -> list[dict[str, Any]]:
    values = {
        "artifact_kind_matches": (ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED_USING_IMPROVED_EVIDENCE, artifact.get("artifact_kind")),
        "execution_status_matches": (ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED_USING_IMPROVED_EVIDENCE_RESEARCH_ONLY, artifact.get("execution_status")),
        "approval_digest_bound": (EXPECTED_APPROVAL_DIGEST, artifact.get("additional_predictive_evidence_execution_approval_using_improved_evidence_digest")),
        "candidate_review_digest_bound": (EXPECTED_CANDIDATE_REVIEW_DIGEST, artifact.get("additional_predictive_evidence_execution_candidate_using_improved_evidence_review_package_digest")),
        "candidate_digest_bound": (EXPECTED_CANDIDATE_DIGEST, artifact.get("additional_predictive_evidence_execution_candidate_using_improved_evidence_digest")),
        "planning_execution_digest_bound": (EXPECTED_PLANNING_EXECUTION_DIGEST, artifact.get("improved_evidence_planning_execution_using_redesigned_evidence_digest")),
        "planning_output_binding_digest_bound": (EXPECTED_PLANNING_OUTPUT_BINDING_DIGEST, artifact.get("improved_evidence_planning_output_binding_digest")),
        "matrix_digest_bound": (EXPECTED_MATRIX_DIGEST, artifact.get("feature_label_matrix_digest")),
        "feature_values_digest_bound": (EXPECTED_FEATURE_VALUES_DIGEST, artifact.get("feature_values_digest")),
        "label_values_digest_bound": (EXPECTED_LABEL_VALUES_DIGEST, artifact.get("redesigned_label_values_digest")),
        "records_digest_bound": (EXPECTED_RECORDS_DIGEST, artifact.get("records_digest")),
        "execution_approved_true": (True, artifact.get("additional_predictive_evidence_execution_approved")),
        "execution_authorized_true": (True, artifact.get("additional_predictive_evidence_execution_authorized")),
        "ready_for_execution_true": (True, artifact.get("ready_for_additional_predictive_evidence_execution_using_improved_evidence")),
        "execution_performed_true": (True, artifact.get("additional_predictive_evidence_executed")),
        "results_created_true": (True, artifact.get("additional_predictive_evidence_results_created")),
        "generated_output_count_13": (13, artifact.get("generated_output_count")),
        "source_input_count_15": (15, artifact.get("planned_source_input_count")),
        "activity_count_12": (12, artifact.get("execution_activity_count")),
        "model_family_count_9": (9, artifact.get("model_family_count")),
        "metric_family_count_10": (10, artifact.get("metric_family_count")),
        "target_universe_preserved": (TARGET_UNIVERSE, artifact.get("target_universe")),
        "meta_913_preserved": (913, artifact.get("meta_record_count")),
        "selected_direction_preserved": (SELECTED_DIRECTION, artifact.get("selected_redesign_direction")),
        "label_regeneration_false": (False, artifact.get("label_regeneration_performed")),
        "new_targets_false": (False, artifact.get("new_targets_created")),
        "target_change_false": (False, artifact.get("target_definition_change_authorized")),
        "feature_generation_false": (False, artifact.get("feature_generation_performed")),
        "source_files_unchanged": (True, artifact.get("source_files_unchanged")),
        "predictive_usefulness_not_accepted": (NOT_ACCEPTED, artifact.get("predictive_usefulness")),
        "profitability_not_accepted": (NOT_ACCEPTED, artifact.get("profitability")),
        "runtime_not_authorized": (NOT_AUTHORIZED, artifact.get("runtime_use")),
        "trade_recommendations_false": (False, artifact.get("trade_recommendations_generated")),
        "execution_classification_research_only": ("COMPLETED_RESEARCH_ONLY", artifact.get("additional_predictive_evidence_execution_classification")),
        "label_schema_binding_research_only": ("BOUND_RESEARCH_ONLY_NOT_LABEL_REGENERATION", artifact.get("label_schema_binding_status")),
        "matrix_report_not_canonical": ("GENERATED_RESEARCH_REPORT_ONLY_NOT_CANONICAL_MATRIX", artifact.get("improved_feature_label_matrix_status")),
        "walk_forward_research_only": ("COMPUTED_RESEARCH_ONLY", artifact.get("walk_forward_status")),
        "oos_research_only": ("COMPUTED_RESEARCH_ONLY", artifact.get("oos_status")),
        "metrics_research_only": ("COMPUTED_RESEARCH_ONLY", artifact.get("metric_family_status")),
        "leakage_controls_pass": ("PASS_RESEARCH_ONLY", artifact.get("leakage_quality_control_status")),
        "per_ticker_entries_12": (12, len(artifact.get("per_ticker_execution_entries", []))),
        "per_ticker_digests_valid": (True, _per_ticker_digests_valid(artifact.get("per_ticker_execution_entries"))),
        "output_manifest_digest_present": (True, isinstance(artifact.get("output_digest_manifest_digest"), str) and len(artifact["output_digest_manifest_digest"]) == 64),
        "no_provider_requests": (False, artifact.get("provider_requests_made_in_execution")),
        "no_market_data_acquisition": (False, artifact.get("market_data_acquisition_performed_in_execution")),
        "no_dataset_regeneration": (False, artifact.get("canonical_dataset_regenerated_in_execution")),
        "failure_count_zero": (0, artifact.get("failure_count")),
    }
    return [_check(check_id, expected, actual) for check_id, (expected, actual) in values.items()]


def additional_predictive_evidence_execution_using_improved_evidence_digest_v1(
    artifact: Mapping[str, Any],
) -> str:
    payload = deepcopy(dict(artifact))
    payload.pop("additional_predictive_evidence_execution_digest", None)
    if isinstance(payload.get("execution_summary"), dict):
        payload["execution_summary"].pop("additional_predictive_evidence_execution_digest", None)
    for field in (
        "canonical_root", "label_root", "feature_root", "prior_predictive_evidence_root",
        "improved_planning_root", "output_root",
    ):
        payload.pop(field, None)
    return semantic_digest(payload)


def _build_executed_artifact(
    *,
    run_timestamp_utc: str,
    canonical_root: Path,
    label_root: Path,
    feature_root: Path,
    prior_predictive_evidence_root: Path,
    improved_planning_root: Path,
    output_root: Path,
    verification: Mapping[str, Any],
    summaries: Mapping[str, Any],
) -> dict[str, Any]:
    artifact: dict[str, Any] = {
        "artifact_kind": ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED_USING_IMPROVED_EVIDENCE,
        "schema_version": SCHEMA_VERSION_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED_USING_IMPROVED_EVIDENCE_V1,
        "execution_status": ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED_USING_IMPROVED_EVIDENCE_RESEARCH_ONLY,
        "created_offline": True, "research_only": True, "operator_review_required": True,
        "run_timestamp_utc": run_timestamp_utc,
        "canonical_root": _path_text(canonical_root), "label_root": _path_text(label_root),
        "feature_root": _path_text(feature_root),
        "prior_predictive_evidence_root": _path_text(prior_predictive_evidence_root),
        "improved_planning_root": _path_text(improved_planning_root),
        "output_root": _path_text(output_root),
        **{field: False for field in FALSE_GUARDRAIL_FIELDS},
        **deepcopy(SOURCE_EVIDENCE),
        "additional_predictive_evidence_execution_approved": True,
        "additional_predictive_evidence_execution_authorized": True,
        "ready_for_additional_predictive_evidence_execution_using_improved_evidence": True,
        "additional_predictive_evidence_executed": True,
        "additional_predictive_evidence_results_created": True,
        "selected_redesign_direction": SELECTED_DIRECTION,
        "generated_output_count": 13,
        "planned_source_input_count": 15,
        "execution_activity_count": 12,
        "model_family_count": 9,
        "metric_family_count": 10,
        "target_universe": TARGET_UNIVERSE,
        "target_universe_count": 12,
        "total_canonical_record_count": 11946,
        "per_ticker_record_counts": EXPECTED_RECORD_COUNTS,
        "meta_record_count": 913,
        "non_meta_record_count": 1003,
        "meta_reduced_record_count_preserved": True,
        "additional_predictive_evidence_execution_manifest_created": True,
        "source_binding_manifest_created": True,
        "improved_label_schema_binding_report_created": True,
        "improved_feature_label_matrix_report_created": True,
        "walk_forward_results_created": True,
        "oos_results_created": True,
        "baseline_model_comparison_created": True,
        "metric_family_results_created": True,
        "calibration_stability_report_created": True,
        "leakage_quality_control_report_created": True,
        "per_ticker_meta_review_created": True,
        "operator_results_review_summary_created": True,
        "digest_manifest_created": True,
        "source_files_unchanged": verification.get("source_files_unchanged") is True,
        "source_verification": deepcopy(dict(verification)),
        "additional_predictive_evidence_execution_classification": "COMPLETED_RESEARCH_ONLY",
        "execution_scope": "RESEARCH_EVIDENCE_EXECUTION_ONLY_NOT_ACCEPTANCE",
        "selected_redesign_direction_status": "USED_AS_RESEARCH_CONTEXT_ONLY",
        "label_schema_binding_status": "BOUND_RESEARCH_ONLY_NOT_LABEL_REGENERATION",
        "improved_feature_label_matrix_status": "GENERATED_RESEARCH_REPORT_ONLY_NOT_CANONICAL_MATRIX",
        **deepcopy(dict(summaries)),
        "predictive_usefulness_interpretation": "NOT_ACCEPTED_REQUIRES_RESULTS_REVIEW",
        "predictive_usefulness": NOT_ACCEPTED,
        "predictive_usefulness_acceptance_ready": False,
        "predictive_usefulness_acceptance_candidate_created": False,
        "profitability_interpretation": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "profitability_acceptance_ready": False,
        "profitability_acceptance_recommended": False,
        "runtime_interpretation": NOT_AUTHORIZED,
        "runtime_migration_approved": False,
        "runtime_migration_active": False,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "automatic_stitching": False,
        "new_strategy_scoring_performed": False,
        "trade_recommendations_generated": False,
        "output_digest_manifest_digest": _output_manifest_binding_digest(run_timestamp_utc),
        "output_digest_manifest_self_reference_policy": "SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE",
        "failure_count": 0,
    }
    checklist = _execution_checklist(artifact)
    failed = [row for row in checklist if row["status"] != PASS]
    artifact["execution_checklist"] = checklist
    artifact["execution_summary"] = {
        "total_checks": len(checklist), "passed_checks": len(checklist) - len(failed),
        "failed_checks": len(failed), "blocker_count": len(failed),
        "generated_output_count": 13, "target_count": 12,
        "additional_predictive_evidence_executed": True,
        "additional_predictive_evidence_results_created": True,
        "predictive_usefulness_accepted": False, "profitability_accepted": False,
        "runtime_authorized": False,
    }
    artifact["additional_predictive_evidence_execution_digest"] = (
        additional_predictive_evidence_execution_using_improved_evidence_digest_v1(artifact)
    )
    artifact["execution_summary"]["additional_predictive_evidence_execution_digest"] = artifact[
        "additional_predictive_evidence_execution_digest"
    ]
    return artifact


def _blocked_artifact(
    *,
    run_timestamp_utc: str,
    output_root: Path,
    failures: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_BLOCKED_USING_IMPROVED_EVIDENCE,
        "schema_version": SCHEMA_VERSION_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED_USING_IMPROVED_EVIDENCE_V1,
        "execution_status": ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_BLOCKED_MISSING_OR_INVALID_SOURCE_EVIDENCE,
        "created_offline": True, "research_only": True, "operator_review_required": True,
        "run_timestamp_utc": run_timestamp_utc, "output_root": _path_text(output_root),
        "additional_predictive_evidence_execution_approval_using_improved_evidence_digest": EXPECTED_APPROVAL_DIGEST,
        "additional_predictive_evidence_execution_approved": True,
        "additional_predictive_evidence_execution_authorized": True,
        "ready_for_additional_predictive_evidence_execution_using_improved_evidence": True,
        "additional_predictive_evidence_executed": False,
        "additional_predictive_evidence_results_created": False,
        "additional_predictive_evidence_execution_digest": "NOT_CREATED",
        "output_digest_manifest_digest": "NOT_CREATED",
        "generated_output_count": 0,
        "failures": deepcopy(failures), "failure_count": len(failures),
        **{field: False for field in FALSE_GUARDRAIL_FIELDS},
        "predictive_usefulness": NOT_ACCEPTED, "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED, "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED, "broker_execution": NOT_AUTHORIZED,
    }


def _write_json_once(path: Path, payload: Mapping[str, Any]) -> str:
    data = canonical_json_bytes(dict(payload))
    try:
        with path.open("xb") as handle:
            handle.write(data)
    except FileExistsError as exc:
        raise AdditionalPredictiveEvidenceExecutionImprovedEvidenceError(
            f"execution output already exists: {path.name}"
        ) from exc
    return sha256_bytes(data)


def execute_additional_predictive_evidence_using_improved_evidence_v1(
    *,
    canonical_root: str | Path | None = None,
    label_root: str | Path | None = None,
    feature_root: str | Path | None = None,
    prior_predictive_evidence_root: str | Path | None = None,
    improved_planning_root: str | Path | None = None,
    output_root: str | Path | None = None,
    run_timestamp_utc: str | None = None,
) -> dict[str, Any]:
    """Execute the approved deterministic research run without provider access."""
    canonical_path = DEFAULT_CANONICAL_ROOT if canonical_root is None else Path(canonical_root)
    label_path = DEFAULT_LABEL_ROOT if label_root is None else Path(label_root)
    feature_path = DEFAULT_FEATURE_ROOT if feature_root is None else Path(feature_root)
    prior_path = (
        DEFAULT_PRIOR_PREDICTIVE_EVIDENCE_ROOT
        if prior_predictive_evidence_root is None else Path(prior_predictive_evidence_root)
    )
    planning_path = (
        DEFAULT_IMPROVED_PLANNING_ROOT if improved_planning_root is None else Path(improved_planning_root)
    )
    output_path = DEFAULT_OUTPUT_ROOT if output_root is None else Path(output_root)
    timestamp = run_timestamp_utc or _utc_now()
    verification, failures = _verify_sources(
        canonical_root=canonical_path, label_root=label_path, feature_root=feature_path,
        prior_predictive_evidence_root=prior_path, improved_planning_root=planning_path,
    )
    if failures:
        return _blocked_artifact(
            run_timestamp_utc=timestamp, output_root=output_path, failures=failures
        )
    if output_path.exists() and any(output_path.iterdir()):
        raise AdditionalPredictiveEvidenceExecutionImprovedEvidenceError(
            "additional predictive evidence output root is not empty"
        )
    reports, summaries = _build_report_payloads(
        run_timestamp_utc=timestamp, verification=verification,
        prior_predictive_evidence_root=prior_path, improved_planning_root=planning_path,
    )
    current_hashes = {
        key: _sha256_file(Path(path))
        for key, path in verification["source_paths"].items()
    }
    if current_hashes != verification["source_file_sha256"]:
        return _blocked_artifact(
            run_timestamp_utc=timestamp, output_root=output_path,
            failures=[_failure("source_changed_during_execution", "source hashes changed during execution")],
        )
    artifact = _build_executed_artifact(
        run_timestamp_utc=timestamp, canonical_root=canonical_path, label_root=label_path,
        feature_root=feature_path, prior_predictive_evidence_root=prior_path,
        improved_planning_root=planning_path, output_root=output_path,
        verification=verification, summaries=summaries,
    )
    validate_additional_predictive_evidence_executed_using_improved_evidence_v1(artifact)
    output_path.mkdir(parents=True, exist_ok=True)
    reports["additional_predictive_evidence_execution_manifest"] = artifact
    report_by_filename = {
        "additional_predictive_evidence_execution_manifest.json": "additional_predictive_evidence_execution_manifest",
        "source_binding_manifest.json": "source_binding_manifest",
        "improved_label_schema_binding_report.json": "improved_label_schema_binding_report",
        "improved_feature_label_matrix_report.json": "improved_feature_label_matrix_report",
        "walk_forward_results.json": "walk_forward_results",
        "oos_results.json": "oos_results",
        "baseline_model_comparison.json": "baseline_model_comparison",
        "metric_family_results.json": "metric_family_results",
        "calibration_stability_report.json": "calibration_stability_report",
        "leakage_quality_control_report.json": "leakage_quality_control_report",
        "per_ticker_meta_review.json": "per_ticker_meta_review",
        "operator_results_review_summary.json": "operator_results_review_summary",
    }
    output_hashes = {
        filename: _write_json_once(output_path / filename, reports[report_name])
        for filename, report_name in report_by_filename.items()
    }
    digest_entries = [
        (
            {"filename": filename, "digest_kind": "SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE", "sha256": None}
            if filename == "additional_predictive_evidence_digest_manifest.json"
            else {"filename": filename, "digest_kind": "FILE_SHA256", "sha256": output_hashes[filename]}
        )
        for filename in OUTPUT_FILENAMES
    ]
    digest_manifest = _report("additional_predictive_evidence_digest_manifest", {
        "run_timestamp_utc": timestamp, "generated_output_count": 13,
        "output_digest_entries": digest_entries,
        "all_non_self_output_digests_present": True,
        "self_reference_policy": "SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE",
        "output_digest_manifest_digest": artifact["output_digest_manifest_digest"],
        "additional_predictive_evidence_execution_digest": artifact[
            "additional_predictive_evidence_execution_digest"
        ],
    })
    _write_json_once(
        output_path / "additional_predictive_evidence_digest_manifest.json", digest_manifest
    )
    return artifact


FORBIDDEN_ARTIFACT_VALUES = {
    "PREDICTIVE_USEFULNESS_ACCEPTED", "PROFITABILITY_ACCEPTED",
    "RUNTIME_MIGRATION_APPROVED", "RUNTIME_MIGRATION_ACTIVE",
    "STRATEGY_RUNTIME_MIGRATION", "TRADE_RECOMMENDATIONS",
}


def _reject_forbidden(value: Any, path: str = "artifact") -> None:
    if isinstance(value, str) and value in FORBIDDEN_ARTIFACT_VALUES:
        raise AdditionalPredictiveEvidenceExecutionImprovedEvidenceError(
            f"{path} must not emit {value}"
        )
    if isinstance(value, Mapping):
        for key, item in value.items():
            child = f"{path}.{key}"
            if key in FALSE_GUARDRAIL_FIELDS and item is True:
                raise AdditionalPredictiveEvidenceExecutionImprovedEvidenceError(
                    f"{child} must remain false"
                )
            if key in {"runtime_use", "strategy_use", "paper_trading", "broker_execution"} and item == "AUTHORIZED":
                raise AdditionalPredictiveEvidenceExecutionImprovedEvidenceError(
                    f"{child} must remain NOT_AUTHORIZED"
                )
            if key in {"predictive_usefulness", "profitability"} and item == "accepted":
                raise AdditionalPredictiveEvidenceExecutionImprovedEvidenceError(
                    f"{child} must remain not accepted"
                )
            _reject_forbidden(item, child)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _reject_forbidden(item, f"{path}[{index}]")


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise AdditionalPredictiveEvidenceExecutionImprovedEvidenceError(f"{field} mismatch")


def validate_additional_predictive_evidence_executed_using_improved_evidence_v1(
    artifact: dict,
) -> dict[str, Any]:
    """Reject execution evidence that exceeds the research-only authority."""
    if not isinstance(artifact, dict):
        raise AdditionalPredictiveEvidenceExecutionImprovedEvidenceError(
            "artifact must be a JSON object"
        )
    _reject_forbidden(artifact)
    expected = {
        "artifact_kind": ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED_USING_IMPROVED_EVIDENCE,
        "schema_version": SCHEMA_VERSION_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED_USING_IMPROVED_EVIDENCE_V1,
        "execution_status": ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED_USING_IMPROVED_EVIDENCE_RESEARCH_ONLY,
        **SOURCE_EVIDENCE,
        "target_universe": TARGET_UNIVERSE, "target_universe_count": 12,
        "total_canonical_record_count": 11946, "per_ticker_record_counts": EXPECTED_RECORD_COUNTS,
        "meta_record_count": 913, "non_meta_record_count": 1003,
        "selected_redesign_direction": SELECTED_DIRECTION,
        "generated_output_count": 13, "planned_source_input_count": 15,
        "execution_activity_count": 12, "model_family_count": 9, "metric_family_count": 10,
        "additional_predictive_evidence_execution_classification": "COMPLETED_RESEARCH_ONLY",
        "execution_scope": "RESEARCH_EVIDENCE_EXECUTION_ONLY_NOT_ACCEPTANCE",
        "selected_redesign_direction_status": "USED_AS_RESEARCH_CONTEXT_ONLY",
        "label_schema_binding_status": "BOUND_RESEARCH_ONLY_NOT_LABEL_REGENERATION",
        "improved_feature_label_matrix_status": "GENERATED_RESEARCH_REPORT_ONLY_NOT_CANONICAL_MATRIX",
        "walk_forward_status": "COMPUTED_RESEARCH_ONLY", "oos_status": "COMPUTED_RESEARCH_ONLY",
        "baseline_model_comparison_status": "COMPUTED_RESEARCH_ONLY",
        "metric_family_status": "COMPUTED_RESEARCH_ONLY",
        "calibration_stability_status": "COMPUTED_RESEARCH_ONLY",
        "leakage_quality_control_status": "PASS_RESEARCH_ONLY",
        "per_ticker_meta_review_status": "COMPLETED_RESEARCH_ONLY",
        "predictive_usefulness": NOT_ACCEPTED, "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED, "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED, "broker_execution": NOT_AUTHORIZED,
    }
    for field, expected_value in expected.items():
        _expect(artifact.get(field), expected_value, field)
    true_fields = [
        "created_offline", "research_only", "operator_review_required",
        "additional_predictive_evidence_execution_approved",
        "additional_predictive_evidence_execution_authorized",
        "ready_for_additional_predictive_evidence_execution_using_improved_evidence",
        "additional_predictive_evidence_executed", "additional_predictive_evidence_results_created",
        "meta_reduced_record_count_preserved", "source_files_unchanged",
        "additional_predictive_evidence_execution_manifest_created", "source_binding_manifest_created",
        "improved_label_schema_binding_report_created", "improved_feature_label_matrix_report_created",
        "walk_forward_results_created", "oos_results_created", "baseline_model_comparison_created",
        "metric_family_results_created", "calibration_stability_report_created",
        "leakage_quality_control_report_created", "per_ticker_meta_review_created",
        "operator_results_review_summary_created", "digest_manifest_created",
    ]
    for field in true_fields:
        _expect(artifact.get(field), True, field)
    for field in FALSE_GUARDRAIL_FIELDS:
        _expect(artifact.get(field), False, field)
    entries = artifact.get("per_ticker_execution_entries")
    if not _per_ticker_digests_valid(entries):
        raise AdditionalPredictiveEvidenceExecutionImprovedEvidenceError(
            "per-ticker execution digests mismatch"
        )
    _expect([row["ticker"] for row in entries], TARGET_UNIVERSE, "per-ticker order")
    manifest_digest = artifact.get("output_digest_manifest_digest")
    if not isinstance(manifest_digest, str) or len(manifest_digest) != 64:
        raise AdditionalPredictiveEvidenceExecutionImprovedEvidenceError(
            "output manifest digest required"
        )
    _expect(
        manifest_digest, _output_manifest_binding_digest(artifact["run_timestamp_utc"]),
        "output manifest digest",
    )
    checklist = _execution_checklist(artifact)
    _expect(artifact.get("execution_checklist"), checklist, "execution_checklist")
    if any(row["status"] != PASS for row in checklist):
        raise AdditionalPredictiveEvidenceExecutionImprovedEvidenceError(
            "execution checklist must pass"
        )
    summary = artifact.get("execution_summary")
    if not isinstance(summary, dict):
        raise AdditionalPredictiveEvidenceExecutionImprovedEvidenceError(
            "execution_summary required"
        )
    _expect(summary.get("failed_checks"), 0, "execution_summary.failed_checks")
    _expect(summary.get("blocker_count"), 0, "execution_summary.blocker_count")
    digest = artifact.get("additional_predictive_evidence_execution_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise AdditionalPredictiveEvidenceExecutionImprovedEvidenceError(
            "execution digest required"
        )
    _expect(
        digest, additional_predictive_evidence_execution_using_improved_evidence_digest_v1(artifact),
        "execution digest",
    )
    _expect(
        summary.get("additional_predictive_evidence_execution_digest"), digest,
        "execution_summary.execution_digest",
    )
    return {
        "valid": True, "execution_status": artifact["execution_status"],
        "additional_predictive_evidence_execution_digest": digest,
        "output_digest_manifest_digest": manifest_digest,
        "generated_output_count": 13, "blocker_count": 0,
        "predictive_usefulness": NOT_ACCEPTED, "profitability": NOT_ACCEPTED,
        "runtime_authorized": False,
    }


def build_additional_predictive_evidence_execution_status_markdown_v1(
    artifact: dict,
) -> str:
    """Render research execution evidence without implying acceptance or runtime authority."""
    validation = validate_additional_predictive_evidence_executed_using_improved_evidence_v1(
        artifact
    )
    sections = [
        ("Title", "Optional Additional Predictive Evidence Execution Using Improved Evidence v1."),
        ("Optional Additional Predictive Evidence Execution Using Improved Evidence", f"Artifact/status: `{artifact['artifact_kind']}` / `{artifact['execution_status']}`."),
        ("Source Approval", f"Approval digest: `{artifact['additional_predictive_evidence_execution_approval_using_improved_evidence_digest']}`."),
        ("Bound Evidence", "The approval, candidate review, candidate, planning, frozen data, and prior research digests are bound."),
        ("Dataset and Universe", "The 12-ticker frozen daily dataset remains 11,946 records; META remains 913."),
        ("Execution Policy", "Research evidence execution only; no source regeneration or operational authority."),
        ("Selected Redesign Direction", f"`{artifact['selected_redesign_direction']}` is used as research context only."),
        ("Source Binding", "All required source files and hashes were verified read-only."),
        ("Improved Label Schema Binding", f"`{artifact['label_schema_binding_status']}`."),
        ("Improved Feature-Label Matrix Report", f"`{artifact['improved_feature_label_matrix_status']}`."),
        ("Walk-Forward Results", f"`{artifact['walk_forward_status']}`."),
        ("OOS Results", f"`{artifact['oos_status']}` over 34,848 prior OOS research rows."),
        ("Baseline and Model Comparison", f"`{artifact['baseline_model_comparison_status']}` across nine approved families."),
        ("Metric Family Results", f"`{artifact['metric_family_status']}` across ten families."),
        ("Calibration and Stability", f"`{artifact['calibration_stability_status']}`."),
        ("Leakage and Quality Controls", f"`{artifact['leakage_quality_control_status']}` with zero failed controls."),
        ("Per-Ticker and META Review", "Twelve digest-bound entries; META's 913-record limitation is preserved."),
        ("Output Digest Manifest", f"Thirteen outputs; binding digest `{validation['output_digest_manifest_digest']}`; self reference is not applicable."),
        ("Authority Boundary", "Execution/results are true; source mutation, scoring, recommendations, and trading remain false."),
        ("Predictive Usefulness Boundary", "Predictive usefulness remains `not accepted` pending separate results review."),
        ("Profitability Boundary", "Profitability remains `not accepted`."),
        ("Runtime Boundary", "Runtime, strategy, paper trading, and broker execution remain `NOT_AUTHORIZED`."),
        ("Checklist Summary", f"Checks: `{artifact['execution_summary']['total_checks']}` passed, zero failed, zero blockers."),
        ("Guardrails", "No provider, acquisition, regeneration, source mutation, acceptance, runtime, recommendation, or trading action occurred."),
    ]
    lines = ["# MarketFlow Additional Predictive Evidence Execution Using Improved Evidence", ""]
    for title, body in sections:
        lines.extend([f"## {title}", "", body, ""])
    return "\n".join(lines)
