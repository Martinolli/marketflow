"""Execute the approved label-objective review over frozen redesigned evidence."""

from __future__ import annotations

import json
from copy import deepcopy
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping

from marketflow.historical_data.artifacts import (
    canonical_json_bytes,
    semantic_digest,
    sha256_bytes,
    sha256_file,
)
from marketflow.services import (
    label_objective_target_definition_review_approval_redesigned_evidence_service as approval,
)


ARTIFACT_KIND_LABEL_OBJECTIVE_TARGET_DEFINITION_REVIEW_EXECUTED_USING_REDESIGNED_EVIDENCE = (
    "LABEL_OBJECTIVE_TARGET_DEFINITION_REVIEW_EXECUTED_USING_REDESIGNED_EVIDENCE"
)
ARTIFACT_KIND_LABEL_OBJECTIVE_TARGET_DEFINITION_REVIEW_BLOCKED_USING_REDESIGNED_EVIDENCE = (
    "LABEL_OBJECTIVE_TARGET_DEFINITION_REVIEW_BLOCKED_USING_REDESIGNED_EVIDENCE"
)
SCHEMA_VERSION_LABEL_OBJECTIVE_TARGET_DEFINITION_REVIEW_EXECUTED_USING_REDESIGNED_EVIDENCE_V1 = (
    "label_objective_target_definition_review_executed_using_redesigned_evidence_v1"
)
LABEL_OBJECTIVE_TARGET_DEFINITION_REVIEW_EXECUTED_USING_REDESIGNED_EVIDENCE_RESEARCH_ONLY = (
    "LABEL_OBJECTIVE_TARGET_DEFINITION_REVIEW_EXECUTED_USING_REDESIGNED_EVIDENCE_RESEARCH_ONLY"
)
LABEL_OBJECTIVE_TARGET_DEFINITION_REVIEW_BLOCKED_MISSING_OR_INVALID_SOURCE_EVIDENCE = (
    "LABEL_OBJECTIVE_TARGET_DEFINITION_REVIEW_BLOCKED_MISSING_OR_INVALID_SOURCE_EVIDENCE"
)
LABEL_OBJECTIVE_TARGET_DEFINITION_REVIEW_EXECUTION_USING_REDESIGNED_EVIDENCE_VALID = (
    "LABEL_OBJECTIVE_TARGET_DEFINITION_REVIEW_EXECUTION_USING_REDESIGNED_EVIDENCE_VALID"
)

DEFAULT_CANONICAL_ROOT = Path(".marketflow") / "canonical_datasets" / "expanded_universe_v1"
DEFAULT_LABEL_ROOT = Path(".marketflow") / "redesigned_label_generation" / "expanded_universe_v1"
DEFAULT_FEATURE_ROOT = Path(".marketflow") / "feature_generation_using_redesigned_labels" / "expanded_universe_v1"
DEFAULT_PREDICTIVE_EVIDENCE_ROOT = (
    Path(".marketflow") / "additional_predictive_evidence_using_redesigned_labels" / "expanded_universe_v1"
)
DEFAULT_OUTPUT_ROOT = (
    Path(".marketflow")
    / "label_objective_target_definition_review_using_redesigned_evidence"
    / "expanded_universe_v1"
)
DEFAULT_BRANCH = "feature/label-objective-target-definition-review-execution-redesigned-evidence-v1"
DEFAULT_BASE_COMMIT = "75dff4384a22ba6bf998ce50e5847c24fddbce1c"

EXPECTED_APPROVAL_DIGEST = "01f667deeea9a478dca8e1f326b672ffbcedbf9c0a0b3da93d3fac1714c622db"
EXPECTED_CANDIDATE_REVIEW_DIGEST = "ebf9f1dddddc37167c457c64f28baab021b50249987e888e1ea0a31c78102d45"
EXPECTED_CANDIDATE_DIGEST = "735d531f39c3eac771694b9044ed67f62c9aecbdc9ca0d5cd3e3368c45caf892"
EXPECTED_PATH_SELECTION_DIGEST = "d56519f9eb9dbb3249a365893db080d65fee8fcccbea2a8f0839300f8d006c22"
EXPECTED_READINESS_REVIEW_DIGEST = "6c6e5019a5ce312b12e4b792ce989524ba5bf16f82b5f6e532ec742f99eba4da"
EXPECTED_REASSESSMENT_DIGEST = "32cd6e52de25584df7b54866034fbb378fad8dfe1e3f1656994dbd554d1b4985"
EXPECTED_RESULTS_REVIEW_DIGEST = "90bc6627a315d1de48976c42ad88c93923ae9b2f43335187f0e9afdccf73e2ed"
EXPECTED_EXECUTION_DIGEST = "8d70be25979c7e7d8ffeedd5a6ee8f0e69c5f1015d186f39196a23ded6cf081b"
EXPECTED_MATRIX_DIGEST = "275f23fc57c8b033224ccc7c8de6c3388bc9d1792ff3a208ee40ec018707e6ad"
EXPECTED_FEATURE_VALUES_DIGEST = "63ff963b7856607730911c567860aa8aa95274295cf3cedc99ada7339eabe8f1"
EXPECTED_LABEL_VALUES_DIGEST = "2de373ca60ef8ec47b500444784d9851908b9a90837aa937c3716ade589f849f"
EXPECTED_RESEARCH_REGISTRY_DIGEST = "5f0ce29bd06f1a0d5f1ce3dd8e31b8c8e52d616673f119326377538228d3d958"
EXPECTED_RECORDS_DIGEST = "fbd7c1b17b42e5d4f82a9162b31b45fdfeef46f0e9ee7d29d74c926f0cf19044"

TARGET_UNIVERSE = ["MSFT", "NVDA", "AMZN", "GOOGL", "META", "TSLA", "JPM", "XOM", "JNJ", "WMT", "CAT", "LMT"]
EXPECTED_RECORD_COUNTS = {ticker: (913 if ticker == "META" else 1003) for ticker in TARGET_UNIVERSE}
DATASET_NAME = "expanded_universe_canonical_dataset_v1"
OUTPUT_LABEL = "RESEARCH_ONLY_NON_ACTIONABLE"
EVIDENCE_SCOPE = "LABEL_OBJECTIVE_TARGET_DEFINITION_REVIEW_USING_REDESIGNED_EVIDENCE_RESEARCH_ONLY"
NOT_ACCEPTED = "not accepted"
NOT_AUTHORIZED = "NOT_AUTHORIZED"
SELF_REFERENCE_POLICY = "SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE"

REVIEW_DIMENSIONS = list(approval.REVIEW_DIMENSION_IDS)
LABEL_FAMILIES = list(approval.LABEL_FAMILY_IDS)
DIAGNOSTIC_QUESTIONS = list(approval.DIAGNOSTIC_QUESTIONS)
DECISION_OPTIONS = list(approval.DECISION_OPTION_IDS)

OUTPUT_FILENAMES = [
    "label_objective_target_definition_review_execution_manifest.json",
    "current_label_family_objective_map.json",
    "target_definition_vs_majority_structure_report.json",
    "cross_sectional_edge_materiality_report.json",
    "horizon_noise_review_report.json",
    "threshold_materiality_review_report.json",
    "class_balance_target_distribution_report.json",
    "per_ticker_target_behavior_report.json",
    "meta_target_behavior_report.json",
    "target_decision_options_report.json",
    "operator_review_summary.json",
    "label_objective_target_definition_review_digest_manifest.json",
]

SOURCE_FILES = {
    "canonical_records": ("canonical", "canonical_dataset_records.jsonl"),
    "label_values": ("label", "redesigned_label_values.jsonl"),
    "label_family_coverage": ("label", "redesigned_label_family_coverage_report.json"),
    "threshold_report": ("label", "redesigned_threshold_generation_report.json"),
    "horizon_report": ("label", "redesigned_horizon_generation_report.json"),
    "availability_report": ("label", "redesigned_label_availability_report.json"),
    "per_ticker_label_summary": ("label", "per_ticker_redesigned_label_summary.json"),
    "feature_values": ("feature", "feature_values.jsonl"),
    "feature_label_matrix": ("predictive", "feature_label_matrix.jsonl"),
    "baseline_comparison": ("predictive", "baseline_model_comparison_results.json"),
    "metric_family_results": ("predictive", "metric_family_results.json"),
    "calibration_stability": ("predictive", "calibration_stability_report.json"),
    "per_ticker_cross_sectional": ("predictive", "per_ticker_cross_sectional_review.json"),
}

TRUE_EXECUTION_FIELDS = [
    "created_offline", "research_only", "operator_review_required",
    "label_objective_target_definition_review_approved",
    "label_objective_target_definition_review_authorized",
    "ready_for_label_objective_target_definition_review_execution_using_redesigned_evidence",
    "label_objective_target_definition_review_executed",
    "label_objective_target_definition_review_results_created",
    "label_objective_target_definition_review_execution_manifest_created",
    "current_label_family_objective_map_created",
    "target_definition_vs_majority_structure_report_created",
    "cross_sectional_edge_materiality_report_created",
    "horizon_noise_review_report_created", "threshold_materiality_review_report_created",
    "class_balance_target_distribution_report_created",
    "per_ticker_target_behavior_report_created", "meta_target_behavior_report_created",
    "target_decision_options_report_created", "operator_review_summary_created",
    "digest_manifest_created", "meta_reduced_record_count_preserved",
]
FALSE_GUARDRAIL_FIELDS = [
    "provider_requests_made_in_execution", "live_provider_transport_enabled_in_execution",
    "market_data_acquisition_performed_in_execution", "dataset_generation_performed_in_execution",
    "canonical_dataset_regenerated_in_execution", "redesigned_label_regeneration_performed",
    "feature_regeneration_performed", "predictive_evidence_execution_rerun_performed",
    "metric_recomputation_performed_in_execution", "model_training_performed_in_execution",
    "raw_provider_payloads_committed", "api_keys_stored_or_printed",
    "label_regeneration_authorized", "label_regeneration_performed", "new_targets_created",
    "target_definition_change_authorized", "target_definition_change_performed",
    "label_objective_redesign_candidate_created", "threshold_horizon_refinement_candidate_created",
    "improved_evidence_planning_candidate_created", "additional_predictive_evidence_execution_candidate_created",
    "additional_predictive_evidence_executed", "predictive_usefulness_acceptance_ready",
    "predictive_usefulness_acceptance_recommended", "predictive_usefulness_acceptance_candidate_created",
    "profitability_acceptance_ready", "profitability_acceptance_recommended",
    "runtime_migration_approved", "runtime_migration_active", "automatic_stitching",
    "new_strategy_scoring_performed", "trade_recommendations_generated",
]


class LabelObjectiveTargetDefinitionReviewExecutionRedesignedEvidenceError(ValueError):
    """Raised when execution evidence violates the research-only contract."""


def _utc_now() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


def _path_text(path: Path) -> str:
    return str(path).replace("\\", "/")


def _load_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path.name} must contain a JSON object")
    return payload


def _source_evidence() -> dict[str, str]:
    return {
        "label_objective_target_definition_review_approval_using_redesigned_evidence_digest": EXPECTED_APPROVAL_DIGEST,
        "label_objective_target_definition_review_candidate_using_redesigned_evidence_review_package_digest": EXPECTED_CANDIDATE_REVIEW_DIGEST,
        "label_objective_target_definition_review_candidate_using_redesigned_evidence_digest": EXPECTED_CANDIDATE_DIGEST,
        "method_evidence_improvement_path_selection_using_redesigned_evidence_digest": EXPECTED_PATH_SELECTION_DIGEST,
        "predictive_usefulness_acceptance_readiness_review_using_redesigned_evidence_digest": EXPECTED_READINESS_REVIEW_DIGEST,
        "predictive_usefulness_reassessment_using_redesigned_evidence_digest": EXPECTED_REASSESSMENT_DIGEST,
        "additional_predictive_evidence_results_review_using_redesigned_labels_digest": EXPECTED_RESULTS_REVIEW_DIGEST,
        "additional_predictive_evidence_execution_using_redesigned_labels_digest": EXPECTED_EXECUTION_DIGEST,
        "feature_label_matrix_digest": EXPECTED_MATRIX_DIGEST,
        "feature_values_digest": EXPECTED_FEATURE_VALUES_DIGEST,
        "redesigned_label_values_digest": EXPECTED_LABEL_VALUES_DIGEST,
        "research_registry_approval_digest": EXPECTED_RESEARCH_REGISTRY_DIGEST,
        "records_digest": EXPECTED_RECORDS_DIGEST,
    }


def _output_manifest_binding_digest() -> str:
    return semantic_digest({"filenames": OUTPUT_FILENAMES, "self_reference_policy": SELF_REFERENCE_POLICY})


def label_objective_target_definition_review_execution_using_redesigned_evidence_digest_v1(
    artifact: Mapping[str, Any],
) -> str:
    clone = deepcopy(dict(artifact))
    clone.pop("label_objective_target_definition_review_execution_using_redesigned_evidence_digest", None)
    return semantic_digest(clone)


def per_ticker_label_objective_target_definition_review_execution_using_redesigned_evidence_digest_v1(
    entry: Mapping[str, Any],
) -> str:
    clone = deepcopy(dict(entry))
    clone.pop("per_ticker_label_objective_target_definition_review_execution_digest", None)
    return semantic_digest(clone)


def _common_output_fields(run_timestamp_utc: str) -> dict[str, Any]:
    return {
        "run_timestamp_utc": run_timestamp_utc,
        "output_label": OUTPUT_LABEL,
        "evidence_scope": EVIDENCE_SCOPE,
        "dataset_name": DATASET_NAME,
        "records_digest": EXPECTED_RECORDS_DIGEST,
        "redesigned_label_values_digest": EXPECTED_LABEL_VALUES_DIGEST,
        "feature_values_digest": EXPECTED_FEATURE_VALUES_DIGEST,
        "feature_label_matrix_digest": EXPECTED_MATRIX_DIGEST,
        "label_objective_target_definition_review_approved": True,
        "label_objective_target_definition_review_authorized": True,
        "ready_for_label_objective_target_definition_review_execution_using_redesigned_evidence": True,
        "label_objective_target_definition_review_executed": True,
        "label_objective_target_definition_review_results_created": True,
        "label_regeneration_authorized": False, "label_regeneration_performed": False,
        "new_targets_created": False, "target_definition_change_authorized": False,
        "target_definition_change_performed": False, "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED, "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED, "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED, "trade_recommendations_generated": False,
        "research_only": True, "non_actionable": True,
    }


def _verify_sources(roots: dict[str, Path]) -> tuple[dict[str, Any], dict[str, dict[str, Any]], list[dict[str, Any]]]:
    failures: list[dict[str, Any]] = []
    paths: dict[str, Path] = {}
    for source_id, (root_key, filename) in SOURCE_FILES.items():
        path = roots[root_key] / filename
        paths[source_id] = path
        if not path.is_file():
            failures.append({"failure_id": "missing_source_file", "source_id": source_id, "path": _path_text(path)})
    if failures:
        return {"all_required_source_files_present": False}, {}, failures

    before_hashes = {source_id: sha256_file(path) for source_id, path in paths.items()}
    expected_large = {
        "canonical_records": EXPECTED_RECORDS_DIGEST,
        "label_values": EXPECTED_LABEL_VALUES_DIGEST,
        "feature_values": EXPECTED_FEATURE_VALUES_DIGEST,
        "feature_label_matrix": EXPECTED_MATRIX_DIGEST,
    }
    for source_id, expected in expected_large.items():
        if before_hashes[source_id] != expected:
            failures.append({"failure_id": "source_digest_mismatch", "source_id": source_id,
                             "expected": expected, "actual": before_hashes[source_id]})

    reports: dict[str, dict[str, Any]] = {}
    for source_id, path in paths.items():
        if path.suffix != ".json":
            continue
        try:
            reports[source_id] = _load_json(path)
        except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
            failures.append({"failure_id": "invalid_source_json", "source_id": source_id, "message": str(exc)})
    required_reports = set(SOURCE_FILES) - {"canonical_records", "label_values", "feature_values", "feature_label_matrix"}
    if set(reports) != required_reports:
        return {"all_required_source_files_present": True, "source_file_sha256": before_hashes}, reports, failures

    for source_id, report in reports.items():
        if report.get("dataset_name") != DATASET_NAME:
            failures.append({"failure_id": "dataset_name_mismatch", "source_id": source_id})
        if report.get("records_digest") != EXPECTED_RECORDS_DIGEST:
            failures.append({"failure_id": "records_digest_binding_mismatch", "source_id": source_id})

    label_summary = reports["per_ticker_label_summary"].get("per_ticker_label_summary", [])
    label_tickers = [row.get("ticker") for row in label_summary if isinstance(row, dict)]
    label_counts = {row.get("ticker"): row.get("historical_record_count") for row in label_summary if isinstance(row, dict)}
    cross_entries = reports["per_ticker_cross_sectional"].get("per_ticker_entries", [])
    cross_tickers = [row.get("ticker") for row in cross_entries if isinstance(row, dict)]
    if label_tickers != TARGET_UNIVERSE or cross_tickers != TARGET_UNIVERSE:
        failures.append({"failure_id": "target_universe_mismatch"})
    if label_counts != EXPECTED_RECORD_COUNTS:
        failures.append({"failure_id": "record_count_mismatch", "actual": label_counts})
    if reports["label_family_coverage"].get("label_family_count") != 10:
        failures.append({"failure_id": "label_family_count_mismatch"})
    delta = reports["metric_family_results"].get("baseline_outperformance_delta", {})
    if delta.get("BASELINE_TICKER_CROSS_SECTIONAL") != "0.00309917":
        failures.append({"failure_id": "cross_sectional_delta_mismatch"})
    if delta.get("MODEL_FAMILY_REGULARIZED_LINEAR") != "0.00000000":
        failures.append({"failure_id": "local_model_delta_mismatch"})

    after_hashes = {source_id: sha256_file(path) for source_id, path in paths.items()}
    unchanged = before_hashes == after_hashes
    if not unchanged:
        failures.append({"failure_id": "source_artifact_mutated"})
    verification = {
        "all_required_source_files_present": True,
        "all_required_source_digests_match": not any(row["failure_id"] == "source_digest_mismatch" for row in failures),
        "source_files_unchanged": unchanged,
        "source_file_count": len(paths),
        "source_file_sha256": before_hashes,
        "verified_records_digest": before_hashes["canonical_records"],
        "verified_redesigned_label_values_digest": before_hashes["label_values"],
        "verified_feature_values_digest": before_hashes["feature_values"],
        "verified_feature_label_matrix_digest": before_hashes["feature_label_matrix"],
    }
    return verification, reports, failures


def _accuracy(metrics: Mapping[str, Any], family: str) -> Any:
    value = metrics.get(family, {})
    return value.get("accuracy") if isinstance(value, Mapping) else None


def _build_review_results(reports: dict[str, dict[str, Any]]) -> dict[str, Any]:
    family_report = reports["label_family_coverage"]
    threshold = reports["threshold_report"]
    horizon = reports["horizon_report"]
    availability = reports["availability_report"]
    label_summary = reports["per_ticker_label_summary"]["per_ticker_label_summary"]
    baseline = reports["baseline_comparison"]
    metric = reports["metric_family_results"]
    calibration = reports["calibration_stability"]
    cross_entries = reports["per_ticker_cross_sectional"]["per_ticker_entries"]
    cross_by_ticker = {row["ticker"]: row for row in cross_entries}

    objective_map = []
    source_families = family_report.get("label_families", [])
    for family in source_families:
        objective_map.append({
            "label_family": family,
            "review_status": "REVIEWED_RESEARCH_ONLY",
            "objective_mapping_status": "CURRENT_OBJECTIVE_REVIEWED_NOT_CHANGED",
            "label_regeneration_authorized": False,
            "target_definition_change_authorized": False,
            "research_only": True, "non_actionable": True,
        })

    class_balance = deepcopy(metric.get("class_balance", {}))
    total_classes = sum(int(value) for value in class_balance.values()) if class_balance else 0
    dominant_class = max(class_balance, key=lambda key: int(class_balance[key])) if class_balance else None
    dominant_count = int(class_balance[dominant_class]) if dominant_class else 0
    global_metrics = baseline.get("oos_method_metrics", {})
    deltas = deepcopy(metric.get("baseline_outperformance_delta", {}))
    majority_review = {
        "review_status": "REVIEWED_RESEARCH_ONLY",
        "majority_structure_risk": "PRESENT_REQUIRES_RESULTS_REVIEW",
        "majority_class": dominant_class, "majority_class_count": dominant_count,
        "evaluated_class_count": total_classes,
        "majority_fraction": f"{dominant_count / total_classes:.8f}" if total_classes else None,
        "majority_baseline_accuracy": _accuracy(global_metrics, "BASELINE_MAJORITY_CLASS"),
        "local_model_accuracy": _accuracy(global_metrics, "MODEL_FAMILY_REGULARIZED_LINEAR"),
        "target_change_authorized": False,
    }
    edge_review = {
        "review_status": "REVIEWED_RESEARCH_ONLY",
        "cross_sectional_edge_materiality": "SMALL_NOT_ACCEPTANCE_EVIDENCE",
        "oos_cross_sectional_delta_vs_majority": "0.00309917",
        "oos_local_model_delta_vs_majority": 0,
        "majority_baseline_accuracy": _accuracy(global_metrics, "BASELINE_MAJORITY_CLASS"),
        "cross_sectional_accuracy": _accuracy(global_metrics, "BASELINE_TICKER_CROSS_SECTIONAL"),
        "local_model_accuracy": _accuracy(global_metrics, "MODEL_FAMILY_REGULARIZED_LINEAR"),
        "source_baseline_outperformance_delta": deltas,
        "acceptance_evidence": False,
    }
    horizon_review = {
        "review_status": "REVIEWED_RESEARCH_ONLY",
        "horizon_noise_assessment": "REVIEWED_REQUIRES_RESULTS_REVIEW",
        "source_horizon_strategies": deepcopy(horizon.get("horizon_strategies", [])),
        "source_multi_horizon_values": deepcopy(horizon.get("multi_horizon_values", [])),
        "source_horizon_label_row_counts": deepcopy(horizon.get("horizon_label_row_counts", {})),
        "horizon_change_authorized": False,
    }
    threshold_review = {
        "review_status": "REVIEWED_RESEARCH_ONLY",
        "threshold_materiality_assessment": "REVIEWED_REQUIRES_RESULTS_REVIEW",
        "source_threshold_strategies": deepcopy(threshold.get("threshold_strategies", [])),
        "global_threshold_5_session": threshold.get("global_threshold_5_session"),
        "benchmark_relative_threshold_5_session": threshold.get("benchmark_relative_threshold_5_session"),
        "threshold_change_authorized": False,
    }
    class_balance_review = {
        "review_status": "REVIEWED_RESEARCH_ONLY",
        "class_balance_assessment": "REVIEWED_REQUIRES_RESULTS_REVIEW",
        "source_class_balance": class_balance,
        "source_label_value_row_count": availability.get("label_value_row_count"),
        "source_available_label_value_count": availability.get("available_label_value_count"),
        "source_unavailable_label_value_count": availability.get("unavailable_label_value_count"),
        "target_distribution_change_authorized": False,
    }

    per_ticker_entries = []
    for label_row in label_summary:
        ticker = label_row["ticker"]
        cross_row = cross_by_ticker[ticker]
        metrics = cross_row.get("oos_method_metrics", {})
        entry = {
            "ticker": ticker,
            "registry_approval_status": "APPROVED_FOR_RESEARCH_REGISTRY_ONLY",
            "canonical_dataset_status": "FROZEN",
            "historical_record_count": label_row["historical_record_count"],
            "meta_reduced_record_count_flag": ticker == "META",
            "label_objective_target_definition_review_execution_status": "EXECUTED_RESEARCH_ONLY",
            "label_objective_target_definition_review_results_status": "CREATED_RESEARCH_ONLY",
            "available_label_value_count": label_row.get("available_label_value_count"),
            "unavailable_label_value_count": label_row.get("unavailable_label_value_count"),
            "majority_baseline_accuracy": _accuracy(metrics, "BASELINE_MAJORITY_CLASS"),
            "cross_sectional_accuracy": _accuracy(metrics, "BASELINE_TICKER_CROSS_SECTIONAL"),
            "local_model_accuracy": _accuracy(metrics, "MODEL_FAMILY_REGULARIZED_LINEAR"),
            "label_regeneration_authorized": False, "label_regeneration_performed": False,
            "target_definition_change_authorized": False, "new_targets_created": False,
            "predictive_usefulness": NOT_ACCEPTED, "predictive_usefulness_acceptance_ready": False,
            "predictive_usefulness_acceptance_candidate_created": False,
            "profitability": NOT_ACCEPTED, "runtime_use": NOT_AUTHORIZED,
            "strategy_use": NOT_AUTHORIZED, "paper_trading": NOT_AUTHORIZED,
            "broker_execution": NOT_AUTHORIZED,
            "source_approval_digest": EXPECTED_APPROVAL_DIGEST,
            "source_candidate_review_digest": EXPECTED_CANDIDATE_REVIEW_DIGEST,
        }
        if ticker == "META":
            entry["execution_note"] = "PRESERVE_META_LIMITATION_IN_LABEL_OBJECTIVE_TARGET_DEFINITION_REVIEW_EXECUTION"
        entry["per_ticker_label_objective_target_definition_review_execution_digest"] = (
            per_ticker_label_objective_target_definition_review_execution_using_redesigned_evidence_digest_v1(entry)
        )
        per_ticker_entries.append(entry)

    questions = [{
        "question": question, "review_status": "REVIEWED_RESEARCH_ONLY",
        "answer_status": "PRELIMINARY_REVIEW_NOT_FINAL_DECISION",
        "target_change_authorized": False, "label_regeneration_authorized": False,
        "research_only": True, "non_actionable": True,
    } for question in DIAGNOSTIC_QUESTIONS]
    options = [{
        "decision_option": option, "review_status": "REVIEWED_RESEARCH_ONLY",
        "selected_for_target_change": False, "approved_for_target_change": False,
        "executed": False, "creates_new_labels": False,
        "research_only": True, "non_actionable": True,
    } for option in DECISION_OPTIONS]
    dimensions = [{
        "review_dimension": dimension, "review_status": "REVIEWED_RESEARCH_ONLY",
        "results_review_required": True, "target_change_authorized": False,
        "research_only": True, "non_actionable": True,
    } for dimension in REVIEW_DIMENSIONS]
    classifications = {
        "label_objective_review_classification": "COMPLETED_RESEARCH_ONLY",
        "target_definition_tradeable_signal_alignment": "REQUIRES_REVIEW_RESULTS_ASSESSMENT",
        "majority_structure_risk": "PRESENT_REQUIRES_RESULTS_REVIEW",
        "cross_sectional_edge_materiality": "SMALL_NOT_ACCEPTANCE_EVIDENCE",
        "local_model_equivalence_to_majority": "MATCHES_MAJORITY_BASELINE",
        "horizon_noise_assessment": "REVIEWED_REQUIRES_RESULTS_REVIEW",
        "threshold_materiality_assessment": "REVIEWED_REQUIRES_RESULTS_REVIEW",
        "class_balance_assessment": "REVIEWED_REQUIRES_RESULTS_REVIEW",
        "per_ticker_behavior_assessment": "REVIEWED_REQUIRES_RESULTS_REVIEW",
        "meta_limitation_assessment": "PRESERVED_REQUIRES_OPERATOR_AWARENESS",
        "target_decision_recommendation": "NO_TARGET_CHANGE_AUTHORIZED_BY_THIS_EXECUTION",
    }
    return {
        "review_dimensions": dimensions, "label_family_objective_map": objective_map,
        "majority_structure_review": majority_review,
        "cross_sectional_edge_materiality_review": edge_review,
        "horizon_noise_review": horizon_review, "threshold_materiality_review": threshold_review,
        "class_balance_target_distribution_review": class_balance_review,
        "per_ticker_execution_entries": per_ticker_entries,
        "meta_target_behavior_review": deepcopy(next(row for row in per_ticker_entries if row["ticker"] == "META")),
        "diagnostic_question_results": questions, "decision_options_review": options,
        "review_result_classification": classifications,
        "calibration_review_status": calibration.get("calibration_status"),
    }


def _blocked_artifact(*, roots: dict[str, Path], output_root: Path, run_timestamp_utc: str,
                      verification: dict[str, Any], failures: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_LABEL_OBJECTIVE_TARGET_DEFINITION_REVIEW_BLOCKED_USING_REDESIGNED_EVIDENCE,
        "schema_version": SCHEMA_VERSION_LABEL_OBJECTIVE_TARGET_DEFINITION_REVIEW_EXECUTED_USING_REDESIGNED_EVIDENCE_V1,
        "execution_status": LABEL_OBJECTIVE_TARGET_DEFINITION_REVIEW_BLOCKED_MISSING_OR_INVALID_SOURCE_EVIDENCE,
        "created_offline": True, "research_only": True, "run_timestamp_utc": run_timestamp_utc,
        "source_roots": {key: _path_text(value) for key, value in roots.items()},
        "output_root": _path_text(output_root), "source_evidence": _source_evidence(),
        "source_verification": verification,
        "label_objective_target_definition_review_approved": True,
        "label_objective_target_definition_review_authorized": True,
        "label_objective_target_definition_review_executed": False,
        "label_objective_target_definition_review_results_created": False,
        "generated_output_count": 0, "failure_count": len(failures), "failures": failures,
        "label_regeneration_authorized": False, "label_regeneration_performed": False,
        "new_targets_created": False, "target_definition_change_authorized": False,
        "target_definition_change_performed": False, "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED, "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED, "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED, "trade_recommendations_generated": False,
        "label_objective_target_definition_review_execution_using_redesigned_evidence_digest": "NOT_CREATED",
    }


def _build_artifact(*, roots: dict[str, Path], output_root: Path, run_timestamp_utc: str,
                    verification: dict[str, Any], results: dict[str, Any]) -> dict[str, Any]:
    artifact = {
        "artifact_kind": ARTIFACT_KIND_LABEL_OBJECTIVE_TARGET_DEFINITION_REVIEW_EXECUTED_USING_REDESIGNED_EVIDENCE,
        "schema_version": SCHEMA_VERSION_LABEL_OBJECTIVE_TARGET_DEFINITION_REVIEW_EXECUTED_USING_REDESIGNED_EVIDENCE_V1,
        "execution_status": LABEL_OBJECTIVE_TARGET_DEFINITION_REVIEW_EXECUTED_USING_REDESIGNED_EVIDENCE_RESEARCH_ONLY,
        "run_timestamp_utc": run_timestamp_utc, "branch": DEFAULT_BRANCH, "base_commit": DEFAULT_BASE_COMMIT,
        "source_roots": {key: _path_text(value) for key, value in roots.items()},
        "generated_output_root": _path_text(output_root), "output_label": OUTPUT_LABEL,
        "evidence_scope": EVIDENCE_SCOPE, "source_evidence": _source_evidence(),
        "source_verification": verification, "dataset_name": DATASET_NAME,
        "source_profile": "RTH_FULL_SESSION_1D", "timeframe": "1d",
        "date_range_start": "2022-01-01", "date_range_end": "2025-12-31",
        "target_universe": list(TARGET_UNIVERSE), "target_universe_count": 12,
        "total_canonical_record_count": 11946, "records_digest": EXPECTED_RECORDS_DIGEST,
        "meta_record_count": 913, "non_meta_record_count": 1003,
        "generated_output_count": 12, "generated_output_names": list(OUTPUT_FILENAMES),
        "review_dimension_count": 12, "label_family_review_count": 10,
        "diagnostic_question_count": 10, "decision_option_count": 7,
        "output_digest_manifest_summary": {
            "filename": "label_objective_target_definition_review_digest_manifest.json",
            "entry_count": 12, "self_reference_policy": SELF_REFERENCE_POLICY,
            "binding_digest": _output_manifest_binding_digest(),
        },
        "failure_count": 0, "warning_count": 1,
        "warnings": ["META_PRESERVED_REDUCED_RECORD_COUNT_913"],
        "predictive_usefulness": NOT_ACCEPTED, "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED, "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED, "broker_execution": NOT_AUTHORIZED,
        **{field: True for field in TRUE_EXECUTION_FIELDS},
        **{field: False for field in FALSE_GUARDRAIL_FIELDS},
        **deepcopy(results),
    }
    artifact["label_objective_target_definition_review_execution_using_redesigned_evidence_digest"] = (
        label_objective_target_definition_review_execution_using_redesigned_evidence_digest_v1(artifact)
    )
    return artifact


def _build_outputs(artifact: dict[str, Any]) -> dict[str, bytes]:
    common = _common_output_fields(artifact["run_timestamp_utc"])
    result_payloads: dict[str, dict[str, Any]] = {
        "label_objective_target_definition_review_execution_manifest.json": deepcopy(artifact),
        "current_label_family_objective_map.json": {**common, "report_name": "current_label_family_objective_map", "label_family_count": 10, "label_family_objective_map": deepcopy(artifact["label_family_objective_map"])},
        "target_definition_vs_majority_structure_report.json": {**common, "report_name": "target_definition_vs_majority_structure_report", **deepcopy(artifact["majority_structure_review"])},
        "cross_sectional_edge_materiality_report.json": {**common, "report_name": "cross_sectional_edge_materiality_report", **deepcopy(artifact["cross_sectional_edge_materiality_review"])},
        "horizon_noise_review_report.json": {**common, "report_name": "horizon_noise_review_report", **deepcopy(artifact["horizon_noise_review"])},
        "threshold_materiality_review_report.json": {**common, "report_name": "threshold_materiality_review_report", **deepcopy(artifact["threshold_materiality_review"])},
        "class_balance_target_distribution_report.json": {**common, "report_name": "class_balance_target_distribution_report", **deepcopy(artifact["class_balance_target_distribution_review"])},
        "per_ticker_target_behavior_report.json": {**common, "report_name": "per_ticker_target_behavior_report", "target_universe": list(TARGET_UNIVERSE), "per_ticker_execution_entries": deepcopy(artifact["per_ticker_execution_entries"])},
        "meta_target_behavior_report.json": {**common, "report_name": "meta_target_behavior_report", "meta_target_behavior_review": deepcopy(artifact["meta_target_behavior_review"])},
        "target_decision_options_report.json": {**common, "report_name": "target_decision_options_report", "diagnostic_question_results": deepcopy(artifact["diagnostic_question_results"]), "decision_options_review": deepcopy(artifact["decision_options_review"]), "target_decision_recommendation": "NO_TARGET_CHANGE_AUTHORIZED_BY_THIS_EXECUTION"},
        "operator_review_summary.json": {**common, "report_name": "operator_review_summary", "execution_status": artifact["execution_status"], "execution_digest": artifact["label_objective_target_definition_review_execution_using_redesigned_evidence_digest"], "review_result_classification": deepcopy(artifact["review_result_classification"]), "generated_output_count": 12, "next_task": "Label Objective / Target Definition Results Review Using Redesigned Evidence v1"},
    }
    payloads = {filename: canonical_json_bytes(payload) for filename, payload in result_payloads.items()}
    digest_entries = [
        ({"filename": filename, "digest_kind": SELF_REFERENCE_POLICY, "sha256": None}
         if filename == "label_objective_target_definition_review_digest_manifest.json"
         else {"filename": filename, "digest_kind": "FILE_SHA256", "sha256": sha256_bytes(payloads[filename])})
        for filename in OUTPUT_FILENAMES
    ]
    digest_manifest = {
        **common, "report_name": "label_objective_target_definition_review_digest_manifest",
        "generated_output_count": 12, "output_digest_entries": digest_entries,
        "all_non_self_output_digests_present": True, "self_reference_policy": SELF_REFERENCE_POLICY,
        "output_manifest_binding_digest": _output_manifest_binding_digest(),
        "execution_digest": artifact["label_objective_target_definition_review_execution_using_redesigned_evidence_digest"],
    }
    payloads["label_objective_target_definition_review_digest_manifest.json"] = canonical_json_bytes(digest_manifest)
    return payloads


def _write_outputs_once(output_root: Path, payloads: dict[str, bytes]) -> None:
    existing = [name for name in OUTPUT_FILENAMES if (output_root / name).exists()]
    if existing:
        raise LabelObjectiveTargetDefinitionReviewExecutionRedesignedEvidenceError(
            f"review execution outputs already exist: {', '.join(existing)}"
        )
    output_root.mkdir(parents=True, exist_ok=True)
    for filename in OUTPUT_FILENAMES:
        try:
            with (output_root / filename).open("xb") as handle:
                handle.write(payloads[filename])
        except FileExistsError as exc:
            raise LabelObjectiveTargetDefinitionReviewExecutionRedesignedEvidenceError(
                f"refusing to overwrite review execution output: {filename}"
            ) from exc


def execute_label_objective_target_definition_review_using_redesigned_evidence_v1(
    *, canonical_root: str | Path | None = None, label_root: str | Path | None = None,
    feature_root: str | Path | None = None, predictive_evidence_root: str | Path | None = None,
    output_root: str | Path | None = None, run_timestamp_utc: str | None = None,
) -> dict[str, Any]:
    """Review existing evidence only and write 12 sanitized research outputs."""
    roots = {
        "canonical": DEFAULT_CANONICAL_ROOT if canonical_root is None else Path(canonical_root),
        "label": DEFAULT_LABEL_ROOT if label_root is None else Path(label_root),
        "feature": DEFAULT_FEATURE_ROOT if feature_root is None else Path(feature_root),
        "predictive": DEFAULT_PREDICTIVE_EVIDENCE_ROOT if predictive_evidence_root is None else Path(predictive_evidence_root),
    }
    output_path = DEFAULT_OUTPUT_ROOT if output_root is None else Path(output_root)
    timestamp = run_timestamp_utc or _utc_now()
    verification, reports, failures = _verify_sources(roots)
    if failures:
        return _blocked_artifact(roots=roots, output_root=output_path, run_timestamp_utc=timestamp,
                                 verification=verification, failures=failures)
    results = _build_review_results(reports)
    artifact = _build_artifact(roots=roots, output_root=output_path, run_timestamp_utc=timestamp,
                               verification=verification, results=results)
    validate_label_objective_target_definition_review_executed_using_redesigned_evidence_v1(artifact)
    _write_outputs_once(output_path, _build_outputs(artifact))
    return artifact


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise LabelObjectiveTargetDefinitionReviewExecutionRedesignedEvidenceError(
            f"{field} mismatch: expected {expected!r}, got {actual!r}"
        )


def validate_label_objective_target_definition_review_executed_using_redesigned_evidence_v1(
    artifact: dict,
) -> dict[str, Any]:
    """Validate execution evidence and every closed downstream authority boundary."""
    if not isinstance(artifact, dict):
        raise LabelObjectiveTargetDefinitionReviewExecutionRedesignedEvidenceError("artifact must be a JSON object")
    expected = {
        "artifact_kind": ARTIFACT_KIND_LABEL_OBJECTIVE_TARGET_DEFINITION_REVIEW_EXECUTED_USING_REDESIGNED_EVIDENCE,
        "schema_version": SCHEMA_VERSION_LABEL_OBJECTIVE_TARGET_DEFINITION_REVIEW_EXECUTED_USING_REDESIGNED_EVIDENCE_V1,
        "execution_status": LABEL_OBJECTIVE_TARGET_DEFINITION_REVIEW_EXECUTED_USING_REDESIGNED_EVIDENCE_RESEARCH_ONLY,
        "output_label": OUTPUT_LABEL, "evidence_scope": EVIDENCE_SCOPE,
        "source_evidence": _source_evidence(), "dataset_name": DATASET_NAME,
        "target_universe": TARGET_UNIVERSE, "target_universe_count": 12,
        "total_canonical_record_count": 11946, "records_digest": EXPECTED_RECORDS_DIGEST,
        "meta_record_count": 913, "non_meta_record_count": 1003,
        "generated_output_count": 12, "generated_output_names": OUTPUT_FILENAMES,
        "review_dimension_count": 12, "label_family_review_count": 10,
        "diagnostic_question_count": 10, "decision_option_count": 7,
        "predictive_usefulness": NOT_ACCEPTED, "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED, "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED, "broker_execution": NOT_AUTHORIZED,
    }
    for field, expected_value in expected.items():
        _expect(artifact.get(field), expected_value, field)
    for field in TRUE_EXECUTION_FIELDS:
        _expect(artifact.get(field), True, field)
    for field in FALSE_GUARDRAIL_FIELDS:
        _expect(artifact.get(field), False, field)
    verification = artifact.get("source_verification")
    if not isinstance(verification, dict):
        raise LabelObjectiveTargetDefinitionReviewExecutionRedesignedEvidenceError("source_verification missing")
    _expect(verification.get("all_required_source_files_present"), True, "source files present")
    _expect(verification.get("all_required_source_digests_match"), True, "source digests match")
    _expect(verification.get("source_files_unchanged"), True, "source files unchanged")
    manifest = artifact.get("output_digest_manifest_summary")
    if not isinstance(manifest, dict):
        raise LabelObjectiveTargetDefinitionReviewExecutionRedesignedEvidenceError("output digest manifest missing")
    _expect(manifest.get("entry_count"), 12, "output digest manifest entry count")
    _expect(manifest.get("self_reference_policy"), SELF_REFERENCE_POLICY, "self reference policy")
    binding_digest = manifest.get("binding_digest")
    if not isinstance(binding_digest, str) or len(binding_digest) != 64:
        raise LabelObjectiveTargetDefinitionReviewExecutionRedesignedEvidenceError("output manifest digest missing")
    _expect(binding_digest, _output_manifest_binding_digest(), "output manifest digest")
    for field, count in (("review_dimensions", 12), ("label_family_objective_map", 10),
                         ("diagnostic_question_results", 10), ("decision_options_review", 7),
                         ("per_ticker_execution_entries", 12)):
        value = artifact.get(field)
        if not isinstance(value, list) or len(value) != count:
            raise LabelObjectiveTargetDefinitionReviewExecutionRedesignedEvidenceError(f"{field} mismatch")
    for entry in artifact["per_ticker_execution_entries"]:
        digest = entry.get("per_ticker_label_objective_target_definition_review_execution_digest")
        if not isinstance(digest, str) or len(digest) != 64:
            raise LabelObjectiveTargetDefinitionReviewExecutionRedesignedEvidenceError("per-ticker execution digest missing")
        _expect(digest, per_ticker_label_objective_target_definition_review_execution_using_redesigned_evidence_digest_v1(entry), "per-ticker execution digest")
    classification = artifact.get("review_result_classification", {})
    _expect(classification.get("target_decision_recommendation"),
            "NO_TARGET_CHANGE_AUTHORIZED_BY_THIS_EXECUTION", "target decision recommendation")
    _expect(classification.get("cross_sectional_edge_materiality"),
            "SMALL_NOT_ACCEPTANCE_EVIDENCE", "edge materiality classification")
    _expect(artifact.get("failure_count"), 0, "failure_count")
    digest = artifact.get("label_objective_target_definition_review_execution_using_redesigned_evidence_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise LabelObjectiveTargetDefinitionReviewExecutionRedesignedEvidenceError("execution digest missing")
    _expect(digest, label_objective_target_definition_review_execution_using_redesigned_evidence_digest_v1(artifact), "execution digest")
    return {
        "status": LABEL_OBJECTIVE_TARGET_DEFINITION_REVIEW_EXECUTION_USING_REDESIGNED_EVIDENCE_VALID,
        "artifact_kind": artifact["artifact_kind"], "execution_status": artifact["execution_status"],
        "label_objective_target_definition_review_execution_using_redesigned_evidence_digest": digest,
        "generated_output_count": 12, "failure_count": 0, "warning_count": artifact["warning_count"],
        "predictive_usefulness": NOT_ACCEPTED, "profitability": NOT_ACCEPTED,
        "runtime_authorized": False,
    }


def build_label_objective_target_definition_review_execution_status_markdown_v1(
    artifact: dict,
) -> str:
    validation = validate_label_objective_target_definition_review_executed_using_redesigned_evidence_v1(artifact)
    source = artifact["source_evidence"]
    sections = [
        ("Title", ["Label Objective / Target Definition Review Execution Using Redesigned Evidence v1."]),
        ("Label Objective / Target Definition Review Execution Using Redesigned Evidence", [f"Artifact/status: `{artifact['artifact_kind']}` / `{artifact['execution_status']}`.", f"Execution digest: `{validation['label_objective_target_definition_review_execution_using_redesigned_evidence_digest']}`."]),
        ("Source Approval", [f"Approval digest: `{source['label_objective_target_definition_review_approval_using_redesigned_evidence_digest']}`."]),
        ("Bound Evidence", [f"Candidate review/candidate: `{source['label_objective_target_definition_review_candidate_using_redesigned_evidence_review_package_digest']}` / `{source['label_objective_target_definition_review_candidate_using_redesigned_evidence_digest']}`.", f"Records/labels/features/matrix: `{source['records_digest']}` / `{source['redesigned_label_values_digest']}` / `{source['feature_values_digest']}` / `{source['feature_label_matrix_digest']}`."]),
        ("Dataset and Universe", [f"`{artifact['dataset_name']}`; `{artifact['total_canonical_record_count']}` records; META `{artifact['meta_record_count']}`.", ", ".join(artifact["target_universe"])]),
        ("Review Execution Policy", ["Existing frozen label and predictive evidence was reviewed read-only; labels, targets, models, and metrics were not regenerated or recomputed."]),
        ("Reviewed Problem Basis", ["Readiness remains `NOT_READY`; cross-sectional delta is `0.00309917`; the local model delta is `0`."]),
        ("Review Dimensions", [f"Reviewed research-only dimensions: `{artifact['review_dimension_count']}`."]),
        ("Label Family Objective Map", [f"Current families reviewed without change: `{artifact['label_family_review_count']}`."]),
        ("Majority Structure Review", [f"`{artifact['majority_structure_review']}`"]),
        ("Cross-Sectional Edge Materiality Review", [f"`{artifact['cross_sectional_edge_materiality_review']}`"]),
        ("Horizon and Threshold Review", [f"Horizon: `{artifact['horizon_noise_review']}`", f"Threshold: `{artifact['threshold_materiality_review']}`"]),
        ("Class Balance and Target Distribution Review", [f"`{artifact['class_balance_target_distribution_review']}`"]),
        ("Per-Ticker Target Behavior Review", [f"Research-only entries: `{len(artifact['per_ticker_execution_entries'])}`."]),
        ("META Target Behavior Review", [f"`{artifact['meta_target_behavior_review']}`"]),
        ("Decision Options Review", [f"Options reviewed/unselected: `{len(artifact['decision_options_review'])}`.", "Recommendation: `NO_TARGET_CHANGE_AUTHORIZED_BY_THIS_EXECUTION`."]),
        ("Output Digest Manifest", [f"`{artifact['output_digest_manifest_summary']}`"]),
        ("Authority Boundary", ["Execution creates research review results only; it creates no target change, redesign/refinement candidate, or downstream authority."]),
        ("Predictive Usefulness Boundary", ["Predictive usefulness remains `not accepted`."]),
        ("Profitability Boundary", ["Profitability remains `not accepted`."]),
        ("Runtime Boundary", ["Runtime, strategy, paper, broker, recommendations, and trading remain `NOT_AUTHORIZED`."]),
        ("Checklist Summary", [f"Failures/warnings: `{artifact['failure_count']}` / `{artifact['warning_count']}`."]),
        ("Guardrails", ["Offline, deterministic, research-only, non-actionable, and results-review-gated."]),
    ]
    lines = ["# MarketFlow Label Objective / Target Definition Review Execution Using Redesigned Evidence Status", ""]
    for title, body in sections:
        lines.extend([f"## {title}", *[f"- {item}" for item in body], ""])
    return "\n".join(lines)
