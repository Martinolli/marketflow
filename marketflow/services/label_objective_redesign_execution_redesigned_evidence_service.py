"""Execute approved label-objective redesign analysis over frozen evidence."""

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
    label_objective_redesign_approval_redesigned_evidence_service as approval,
)


ARTIFACT_KIND_LABEL_OBJECTIVE_REDESIGN_EXECUTED_USING_REDESIGNED_EVIDENCE = (
    "LABEL_OBJECTIVE_REDESIGN_EXECUTED_USING_REDESIGNED_EVIDENCE"
)
ARTIFACT_KIND_LABEL_OBJECTIVE_REDESIGN_BLOCKED_USING_REDESIGNED_EVIDENCE = (
    "LABEL_OBJECTIVE_REDESIGN_BLOCKED_USING_REDESIGNED_EVIDENCE"
)
SCHEMA_VERSION_LABEL_OBJECTIVE_REDESIGN_EXECUTED_USING_REDESIGNED_EVIDENCE_V1 = (
    "label_objective_redesign_executed_using_redesigned_evidence_v1"
)
LABEL_OBJECTIVE_REDESIGN_EXECUTED_USING_REDESIGNED_EVIDENCE_RESEARCH_ONLY = (
    "LABEL_OBJECTIVE_REDESIGN_EXECUTED_USING_REDESIGNED_EVIDENCE_RESEARCH_ONLY"
)
LABEL_OBJECTIVE_REDESIGN_BLOCKED_MISSING_OR_INVALID_SOURCE_EVIDENCE = (
    "LABEL_OBJECTIVE_REDESIGN_BLOCKED_MISSING_OR_INVALID_SOURCE_EVIDENCE"
)
LABEL_OBJECTIVE_REDESIGN_EXECUTION_USING_REDESIGNED_EVIDENCE_VALID = (
    "LABEL_OBJECTIVE_REDESIGN_EXECUTION_USING_REDESIGNED_EVIDENCE_VALID"
)

DEFAULT_CANONICAL_ROOT = Path(".marketflow") / "canonical_datasets" / "expanded_universe_v1"
DEFAULT_LABEL_ROOT = Path(".marketflow") / "redesigned_label_generation" / "expanded_universe_v1"
DEFAULT_FEATURE_ROOT = Path(".marketflow") / "feature_generation_using_redesigned_labels" / "expanded_universe_v1"
DEFAULT_PREDICTIVE_EVIDENCE_ROOT = Path(".marketflow") / "additional_predictive_evidence_using_redesigned_labels" / "expanded_universe_v1"
DEFAULT_LABEL_OBJECTIVE_REVIEW_ROOT = Path(".marketflow") / "label_objective_target_definition_review_using_redesigned_evidence" / "expanded_universe_v1"
DEFAULT_OUTPUT_ROOT = Path(".marketflow") / "label_objective_redesign_using_redesigned_evidence" / "expanded_universe_v1"
DEFAULT_BRANCH = "feature/label-objective-redesign-execution-redesigned-evidence-v1"
DEFAULT_BASE_COMMIT = "2273aa68601af216c378fefc746c6c4902fa6fff"

DATASET_NAME = "expanded_universe_canonical_dataset_v1"
OUTPUT_LABEL = "RESEARCH_ONLY_NON_ACTIONABLE"
EVIDENCE_SCOPE = "LABEL_OBJECTIVE_REDESIGN_USING_REDESIGNED_EVIDENCE_RESEARCH_ONLY"
SELF_REFERENCE_POLICY = "SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE"
NOT_ACCEPTED = "not accepted"
NOT_AUTHORIZED = "NOT_AUTHORIZED"
SELECTED_DIRECTION = "REDESIGN_OPTION_ADD_OR_FORMALIZE_NO_TRADE_ABSTAIN_CLASS"

EXPECTED_APPROVAL_DIGEST = "4ffb335cd01041c6db16974b2f9733b6235d96bfe941cd6c3739d99c45a894c7"
EXPECTED_CANDIDATE_REVIEW_DIGEST = approval.EXPECTED_CANDIDATE_REVIEW_DIGEST
EXPECTED_CANDIDATE_DIGEST = approval.EXPECTED_CANDIDATE_DIGEST
EXPECTED_RECORDS_DIGEST = "fbd7c1b17b42e5d4f82a9162b31b45fdfeef46f0e9ee7d29d74c926f0cf19044"
EXPECTED_LABEL_VALUES_DIGEST = "2de373ca60ef8ec47b500444784d9851908b9a90837aa937c3716ade589f849f"
EXPECTED_FEATURE_VALUES_DIGEST = "63ff963b7856607730911c567860aa8aa95274295cf3cedc99ada7339eabe8f1"
EXPECTED_MATRIX_DIGEST = "275f23fc57c8b033224ccc7c8de6c3388bc9d1792ff3a208ee40ec018707e6ad"
EXPECTED_REVIEW_EXECUTION_DIGEST = "7b5c299191abfd6aa8ef33ebed804757a2d57a6fb966ed1d51c78d1b233abe30"
EXPECTED_REVIEW_OUTPUT_BINDING_DIGEST = "7efd91b24e1af35f93e37dc9bbb5e90fe03f1080f6296abe57afdbd326d0fbee"

TARGET_UNIVERSE = list(approval.TARGET_UNIVERSE)
EXPECTED_RECORD_COUNTS = {ticker: (913 if ticker == "META" else 1003) for ticker in TARGET_UNIVERSE}
REDESIGN_THEMES = list(approval.REDESIGN_THEME_IDS)
REDESIGN_OPTIONS = list(approval.REDESIGN_OPTION_IDS)
LABEL_FAMILIES = list(approval.LABEL_FAMILIES)
REDESIGN_QUESTIONS = list(approval.REDESIGN_QUESTIONS)

OUTPUT_FILENAMES = [
    "label_objective_redesign_execution_manifest.json",
    "flat_class_and_majority_structure_redesign_report.json",
    "no_trade_abstain_objective_report.json",
    "material_move_target_definition_report.json",
    "horizon_specific_target_design_report.json",
    "ticker_or_regime_split_target_report.json",
    "risk_adjusted_target_definition_report.json",
    "label_family_impact_review_report.json",
    "meta_target_limitation_review_report.json",
    "acceptance_threshold_prerequisite_report.json",
    "operator_review_summary.json",
    "label_objective_redesign_digest_manifest.json",
]

SOURCE_FILES = {
    "canonical_records": ("canonical", "canonical_dataset_records.jsonl"),
    "label_values": ("label", "redesigned_label_values.jsonl"),
    "label_family_coverage": ("label", "redesigned_label_family_coverage_report.json"),
    "label_availability": ("label", "redesigned_label_availability_report.json"),
    "per_ticker_label_summary": ("label", "per_ticker_redesigned_label_summary.json"),
    "feature_values": ("feature", "feature_values.jsonl"),
    "feature_label_matrix": ("predictive", "feature_label_matrix.jsonl"),
    "baseline_comparison": ("predictive", "baseline_model_comparison_results.json"),
    "metric_family_results": ("predictive", "metric_family_results.json"),
    "per_ticker_cross_sectional": ("predictive", "per_ticker_cross_sectional_review.json"),
    "review_execution_manifest": ("review", "label_objective_target_definition_review_execution_manifest.json"),
    "majority_structure": ("review", "target_definition_vs_majority_structure_report.json"),
    "cross_sectional_edge": ("review", "cross_sectional_edge_materiality_report.json"),
    "horizon_noise": ("review", "horizon_noise_review_report.json"),
    "threshold_materiality": ("review", "threshold_materiality_review_report.json"),
    "class_balance": ("review", "class_balance_target_distribution_report.json"),
    "per_ticker_behavior": ("review", "per_ticker_target_behavior_report.json"),
    "meta_behavior": ("review", "meta_target_behavior_report.json"),
    "decision_options": ("review", "target_decision_options_report.json"),
}

TRUE_EXECUTION_FIELDS = [
    "created_offline", "research_only", "operator_review_required",
    "label_objective_redesign_approved", "label_objective_redesign_authorized",
    "ready_for_label_objective_redesign_execution_using_redesigned_evidence",
    "label_objective_redesign_executed", "label_objective_redesign_results_created",
    "label_objective_redesign_execution_manifest_created",
    "flat_class_and_majority_structure_redesign_report_created",
    "no_trade_abstain_objective_report_created",
    "material_move_target_definition_report_created",
    "horizon_specific_target_design_report_created",
    "ticker_or_regime_split_target_report_created",
    "risk_adjusted_target_definition_report_created",
    "label_family_impact_review_report_created",
    "meta_target_limitation_review_report_created",
    "acceptance_threshold_prerequisite_report_created",
    "operator_review_summary_created", "digest_manifest_created",
    "meta_reduced_record_count_preserved",
]

FALSE_GUARDRAIL_FIELDS = [
    "provider_requests_made_in_execution", "live_provider_transport_enabled_in_execution",
    "market_data_acquisition_performed_in_execution", "dataset_generation_performed_in_execution",
    "canonical_dataset_regenerated_in_execution", "redesigned_label_regeneration_performed",
    "feature_regeneration_performed", "predictive_evidence_execution_rerun_performed",
    "label_objective_target_definition_review_execution_rerun_performed",
    "label_objective_target_definition_results_review_rerun_performed",
    "metric_recomputation_performed_in_execution", "model_training_performed_in_execution",
    "raw_provider_payloads_committed", "api_keys_stored_or_printed",
    "label_regeneration_authorized", "label_regeneration_performed", "new_targets_created",
    "target_definition_change_authorized", "target_definition_change_performed",
    "threshold_horizon_refinement_candidate_created", "improved_evidence_planning_candidate_created",
    "additional_predictive_evidence_execution_candidate_created",
    "additional_predictive_evidence_executed", "predictive_usefulness_acceptance_ready",
    "predictive_usefulness_acceptance_recommended",
    "predictive_usefulness_acceptance_candidate_created", "profitability_acceptance_ready",
    "profitability_acceptance_recommended", "runtime_migration_approved",
    "runtime_migration_active", "automatic_stitching", "new_strategy_scoring_performed",
    "trade_recommendations_generated",
]


class LabelObjectiveRedesignExecutionRedesignedEvidenceError(ValueError):
    """Raised when redesign execution violates the research-only contract."""


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
    evidence = deepcopy(approval.SOURCE_EVIDENCE)
    return {
        "label_objective_redesign_approval_using_redesigned_evidence_digest": EXPECTED_APPROVAL_DIGEST,
        "label_objective_redesign_candidate_using_redesigned_evidence_review_package_digest": EXPECTED_CANDIDATE_REVIEW_DIGEST,
        "label_objective_redesign_candidate_using_redesigned_evidence_digest": EXPECTED_CANDIDATE_DIGEST,
        **evidence,
    }


def _output_manifest_binding_digest() -> str:
    return semantic_digest({"filenames": OUTPUT_FILENAMES, "self_reference_policy": SELF_REFERENCE_POLICY})


def label_objective_redesign_execution_using_redesigned_evidence_digest_v1(
    artifact: Mapping[str, Any],
) -> str:
    clone = deepcopy(dict(artifact))
    clone.pop("label_objective_redesign_execution_using_redesigned_evidence_digest", None)
    return semantic_digest(clone)


def per_ticker_label_objective_redesign_execution_using_redesigned_evidence_digest_v1(
    entry: Mapping[str, Any],
) -> str:
    clone = deepcopy(dict(entry))
    clone.pop("per_ticker_label_objective_redesign_execution_digest", None)
    return semantic_digest(clone)


def _verify_sources(
    roots: dict[str, Path],
) -> tuple[dict[str, Any], dict[str, dict[str, Any]], list[dict[str, Any]]]:
    failures: list[dict[str, Any]] = []
    paths = {source_id: roots[root_key] / filename for source_id, (root_key, filename) in SOURCE_FILES.items()}
    for source_id, path in paths.items():
        if not path.is_file():
            failures.append({"failure_id": "missing_source_file", "source_id": source_id, "path": _path_text(path)})
    if failures:
        return {"all_required_source_files_present": False}, {}, failures

    before_hashes = {source_id: sha256_file(path) for source_id, path in paths.items()}
    expected_hashes = {
        "canonical_records": EXPECTED_RECORDS_DIGEST,
        "label_values": EXPECTED_LABEL_VALUES_DIGEST,
        "feature_values": EXPECTED_FEATURE_VALUES_DIGEST,
        "feature_label_matrix": EXPECTED_MATRIX_DIGEST,
    }
    for source_id, expected in expected_hashes.items():
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

    expected_reports = set(SOURCE_FILES) - {"canonical_records", "label_values", "feature_values", "feature_label_matrix"}
    if set(reports) == expected_reports:
        for source_id, report in reports.items():
            if report.get("dataset_name") != DATASET_NAME:
                failures.append({"failure_id": "dataset_name_mismatch", "source_id": source_id})
            if report.get("records_digest") != EXPECTED_RECORDS_DIGEST:
                failures.append({"failure_id": "records_digest_binding_mismatch", "source_id": source_id})
        manifest = reports["review_execution_manifest"]
        if manifest.get("label_objective_target_definition_review_execution_using_redesigned_evidence_digest") != EXPECTED_REVIEW_EXECUTION_DIGEST:
            failures.append({"failure_id": "review_execution_digest_mismatch"})
        if manifest.get("output_digest_manifest_summary", {}).get("binding_digest") != EXPECTED_REVIEW_OUTPUT_BINDING_DIGEST:
            failures.append({"failure_id": "review_output_binding_digest_mismatch"})
        label_rows = reports["per_ticker_label_summary"].get("per_ticker_label_summary", [])
        tickers = [row.get("ticker") for row in label_rows if isinstance(row, dict)]
        counts = {row.get("ticker"): row.get("historical_record_count") for row in label_rows if isinstance(row, dict)}
        if tickers != TARGET_UNIVERSE:
            failures.append({"failure_id": "target_universe_mismatch"})
        if counts != EXPECTED_RECORD_COUNTS:
            failures.append({"failure_id": "record_count_mismatch", "actual": counts})
    else:
        failures.append({"failure_id": "source_report_set_incomplete"})

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
        "verified_review_execution_digest": reports.get("review_execution_manifest", {}).get(
            "label_objective_target_definition_review_execution_using_redesigned_evidence_digest"
        ),
        "verified_review_output_binding_digest": reports.get("review_execution_manifest", {}).get(
            "output_digest_manifest_summary", {}
        ).get("binding_digest"),
    }
    return verification, reports, failures


def _analysis_results(reports: dict[str, dict[str, Any]]) -> dict[str, Any]:
    majority = reports["majority_structure"]
    edge = reports["cross_sectional_edge"]
    horizon = reports["horizon_noise"]
    threshold = reports["threshold_materiality"]
    balance = reports["class_balance"]
    source_per_ticker = reports["per_ticker_behavior"]["per_ticker_execution_entries"]

    per_ticker_entries = []
    for source_row in source_per_ticker:
        ticker = source_row["ticker"]
        entry = {
            "ticker": ticker,
            "registry_approval_status": "APPROVED_FOR_RESEARCH_REGISTRY_ONLY",
            "canonical_dataset_status": "FROZEN",
            "historical_record_count": EXPECTED_RECORD_COUNTS[ticker],
            "meta_reduced_record_count_flag": ticker == "META",
            "label_objective_redesign_execution_status": "EXECUTED_RESEARCH_ONLY",
            "label_objective_redesign_results_status": "CREATED_RESEARCH_ONLY",
            "selected_redesign_direction": SELECTED_DIRECTION,
            "label_regeneration_authorized": False,
            "label_regeneration_performed": False,
            "target_definition_change_authorized": False,
            "new_targets_created": False,
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
        }
        if ticker == "META":
            entry["execution_note"] = "PRESERVE_META_LIMITATION_IN_LABEL_OBJECTIVE_REDESIGN_EXECUTION"
        entry["per_ticker_label_objective_redesign_execution_digest"] = (
            per_ticker_label_objective_redesign_execution_using_redesigned_evidence_digest_v1(entry)
        )
        per_ticker_entries.append(entry)

    label_family_impact = [{
        "label_family": family,
        "impact_assessment": "REVIEWED_REQUIRES_RESULTS_REVIEW",
        "regeneration_performed": False,
        "new_target_created": False,
        "research_only": True,
    } for family in LABEL_FAMILIES]

    return {
        "candidate_basis": deepcopy(approval.CANDIDATE_BASIS),
        "redesign_analysis_classification": {
            "label_objective_redesign_classification": "COMPLETED_RESEARCH_ONLY",
            "selected_direction_analysis_status": "ANALYZED_RESEARCH_ONLY",
            "selected_direction": SELECTED_DIRECTION,
            "no_trade_abstain_objective_assessment": "REVIEWED_REQUIRES_RESULTS_REVIEW",
            "flat_class_majority_structure_assessment": "REVIEWED_REQUIRES_RESULTS_REVIEW",
            "material_move_target_assessment": "REVIEWED_REQUIRES_RESULTS_REVIEW",
            "horizon_specific_target_assessment": "REVIEWED_REQUIRES_RESULTS_REVIEW",
            "ticker_or_regime_split_assessment": "REVIEWED_REQUIRES_RESULTS_REVIEW",
            "risk_adjusted_target_assessment": "REVIEWED_REQUIRES_RESULTS_REVIEW",
            "label_family_impact_assessment": "REVIEWED_REQUIRES_RESULTS_REVIEW",
            "meta_limitation_assessment": "PRESERVED_REQUIRES_OPERATOR_AWARENESS",
            "acceptance_threshold_prerequisite_assessment": "REVIEWED_REQUIRES_RESULTS_REVIEW",
            "redesign_decision_recommendation": "NO_LABEL_REGENERATION_OR_NEW_TARGETS_AUTHORIZED_BY_THIS_EXECUTION",
        },
        "flat_class_and_majority_structure_analysis": {
            "assessment": "REVIEWED_REQUIRES_RESULTS_REVIEW",
            "largest_aggregated_class": majority["majority_class"],
            "largest_aggregated_class_count": majority["majority_class_count"],
            "oos_evaluated_rows": majority["evaluated_class_count"],
            "majority_accuracy": majority["majority_baseline_accuracy"],
            "local_model_accuracy": majority["local_model_accuracy"],
            "analysis": "ABSTAIN_SEMANTICS_MAY_SEPARATE_NON_ACTIONABLE_ROWS_BUT_REQUIRE_RESULTS_REVIEW",
            "target_change_authorized": False,
        },
        "no_trade_abstain_objective_analysis": {
            "assessment": "REVIEWED_REQUIRES_RESULTS_REVIEW",
            "flat_count": balance["source_class_balance"]["FLAT"],
            "no_trade_count": balance["source_class_balance"]["NO_TRADE"],
            "selected_direction": SELECTED_DIRECTION,
            "design_considerations": [
                "define_abstain_semantics_without_relabeling_rows_in_this_execution",
                "separate_prediction_eligibility_from_directional_classification",
                "measure_coverage_and_class_balance_before any future acceptance decision".replace(" ", "_"),
            ],
            "new_label_rows_created": False,
        },
        "material_move_target_definition_analysis": {
            "assessment": "REVIEWED_REQUIRES_RESULTS_REVIEW",
            "source_global_threshold_5_session": threshold["global_threshold_5_session"],
            "source_benchmark_relative_threshold_5_session": threshold["benchmark_relative_threshold_5_session"],
            "threshold_change_authorized": False,
            "new_target_definition_created": False,
        },
        "horizon_specific_target_design_analysis": {
            "assessment": "REVIEWED_REQUIRES_RESULTS_REVIEW",
            "source_horizon_strategies": deepcopy(horizon["source_horizon_strategies"]),
            "source_multi_horizon_values": deepcopy(horizon["source_multi_horizon_values"]),
            "horizon_change_authorized": False,
        },
        "ticker_or_regime_split_target_analysis": {
            "assessment": "REVIEWED_REQUIRES_RESULTS_REVIEW",
            "target_universe": list(TARGET_UNIVERSE),
            "per_ticker_review_count": len(per_ticker_entries),
            "split_target_created": False,
            "regime_target_created": False,
        },
        "risk_adjusted_target_definition_analysis": {
            "assessment": "REVIEWED_REQUIRES_RESULTS_REVIEW",
            "reviewed_families": ["volatility_adjusted_return", "drawdown_avoidance", "asymmetric_risk_reward"],
            "risk_adjusted_target_created": False,
        },
        "label_family_impact_review": label_family_impact,
        "meta_target_limitation_review": {
            "assessment": "PRESERVED_REQUIRES_OPERATOR_AWARENESS",
            "ticker": "META", "historical_record_count": 913,
            "meta_reduced_record_count_flag": True,
            "execution_note": "PRESERVE_META_LIMITATION_IN_LABEL_OBJECTIVE_REDESIGN_EXECUTION",
            "repair_or_inference_performed": False,
        },
        "acceptance_threshold_prerequisite_review": {
            "assessment": "REVIEWED_REQUIRES_RESULTS_REVIEW",
            "cross_sectional_accuracy": edge["cross_sectional_accuracy"],
            "cross_sectional_delta_vs_majority": edge["oos_cross_sectional_delta_vs_majority"],
            "cross_sectional_edge_materiality": edge["cross_sectional_edge_materiality"],
            "prerequisites": [
                "results_review_completed", "objective_and_abstain_semantics_explicit",
                "coverage_and_class_balance_thresholds_defined", "no_peek_evidence_plan_separately_approved",
            ],
            "acceptance_ready": False,
        },
        "per_ticker_execution_entries": per_ticker_entries,
    }


def _common_output_fields(run_timestamp_utc: str) -> dict[str, Any]:
    return {
        "run_timestamp_utc": run_timestamp_utc, "output_label": OUTPUT_LABEL,
        "evidence_scope": EVIDENCE_SCOPE, "dataset_name": DATASET_NAME,
        "records_digest": EXPECTED_RECORDS_DIGEST,
        "redesigned_label_values_digest": EXPECTED_LABEL_VALUES_DIGEST,
        "feature_label_matrix_digest": EXPECTED_MATRIX_DIGEST,
        "label_objective_redesign_approved": True,
        "label_objective_redesign_authorized": True,
        "ready_for_label_objective_redesign_execution_using_redesigned_evidence": True,
        "label_objective_redesign_executed": True,
        "label_objective_redesign_results_created": True,
        "selected_label_objective_redesign_direction": SELECTED_DIRECTION,
        "label_regeneration_authorized": False, "label_regeneration_performed": False,
        "new_targets_created": False, "target_definition_change_authorized": False,
        "target_definition_change_performed": False, "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED, "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED, "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED, "trade_recommendations_generated": False,
        "research_only": True, "non_actionable": True,
    }


def _blocked_artifact(
    *, roots: dict[str, Path], output_root: Path, run_timestamp_utc: str,
    verification: dict[str, Any], failures: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_LABEL_OBJECTIVE_REDESIGN_BLOCKED_USING_REDESIGNED_EVIDENCE,
        "schema_version": SCHEMA_VERSION_LABEL_OBJECTIVE_REDESIGN_EXECUTED_USING_REDESIGNED_EVIDENCE_V1,
        "execution_status": LABEL_OBJECTIVE_REDESIGN_BLOCKED_MISSING_OR_INVALID_SOURCE_EVIDENCE,
        "run_timestamp_utc": run_timestamp_utc,
        "source_roots": {key: _path_text(value) for key, value in roots.items()},
        "generated_output_root": _path_text(output_root), "created_offline": True,
        "research_only": True, "source_verification": verification,
        "failure_count": len(failures), "failures": failures,
        "label_objective_redesign_executed": False,
        "label_objective_redesign_results_created": False,
        "generated_output_count": 0,
        "label_objective_redesign_execution_using_redesigned_evidence_digest": "NOT_CREATED",
        **{field: False for field in FALSE_GUARDRAIL_FIELDS},
    }


def _build_artifact(
    *, roots: dict[str, Path], output_root: Path, run_timestamp_utc: str,
    verification: dict[str, Any], results: dict[str, Any],
) -> dict[str, Any]:
    artifact = {
        "artifact_kind": ARTIFACT_KIND_LABEL_OBJECTIVE_REDESIGN_EXECUTED_USING_REDESIGNED_EVIDENCE,
        "schema_version": SCHEMA_VERSION_LABEL_OBJECTIVE_REDESIGN_EXECUTED_USING_REDESIGNED_EVIDENCE_V1,
        "execution_status": LABEL_OBJECTIVE_REDESIGN_EXECUTED_USING_REDESIGNED_EVIDENCE_RESEARCH_ONLY,
        "run_timestamp_utc": run_timestamp_utc, "branch": DEFAULT_BRANCH,
        "base_commit": DEFAULT_BASE_COMMIT,
        "source_roots": {key: _path_text(value) for key, value in roots.items()},
        "generated_output_root": _path_text(output_root), "output_label": OUTPUT_LABEL,
        "evidence_scope": EVIDENCE_SCOPE, "source_evidence": _source_evidence(),
        "source_verification": verification, "dataset_name": DATASET_NAME,
        "source_profile": "RTH_FULL_SESSION_1D", "timeframe": "1d",
        "date_range_start": "2022-01-01", "date_range_end": "2025-12-31",
        "target_universe": list(TARGET_UNIVERSE), "target_universe_count": 12,
        "total_canonical_record_count": 11946, "records_digest": EXPECTED_RECORDS_DIGEST,
        "meta_record_count": 913, "non_meta_record_count": 1003,
        "selected_label_objective_redesign_direction": SELECTED_DIRECTION,
        "generated_output_count": 12, "generated_output_names": list(OUTPUT_FILENAMES),
        "redesign_theme_count": 11, "redesign_option_count": 8,
        "label_family_impact_review_count": 10, "redesign_question_count": 10,
        "redesign_themes": list(REDESIGN_THEMES), "redesign_options": list(REDESIGN_OPTIONS),
        "redesign_questions": list(REDESIGN_QUESTIONS),
        "output_digest_manifest_summary": {
            "filename": "label_objective_redesign_digest_manifest.json",
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
    artifact["label_objective_redesign_execution_using_redesigned_evidence_digest"] = (
        label_objective_redesign_execution_using_redesigned_evidence_digest_v1(artifact)
    )
    return artifact


def _build_outputs(artifact: dict[str, Any]) -> dict[str, bytes]:
    common = _common_output_fields(artifact["run_timestamp_utc"])
    reports: dict[str, dict[str, Any]] = {
        "label_objective_redesign_execution_manifest.json": deepcopy(artifact),
        "flat_class_and_majority_structure_redesign_report.json": {
            **common, "report_name": "flat_class_and_majority_structure_redesign_report",
            **deepcopy(artifact["flat_class_and_majority_structure_analysis"]),
        },
        "no_trade_abstain_objective_report.json": {
            **common, "report_name": "no_trade_abstain_objective_report",
            **deepcopy(artifact["no_trade_abstain_objective_analysis"]),
        },
        "material_move_target_definition_report.json": {
            **common, "report_name": "material_move_target_definition_report",
            **deepcopy(artifact["material_move_target_definition_analysis"]),
        },
        "horizon_specific_target_design_report.json": {
            **common, "report_name": "horizon_specific_target_design_report",
            **deepcopy(artifact["horizon_specific_target_design_analysis"]),
        },
        "ticker_or_regime_split_target_report.json": {
            **common, "report_name": "ticker_or_regime_split_target_report",
            **deepcopy(artifact["ticker_or_regime_split_target_analysis"]),
            "per_ticker_execution_entries": deepcopy(artifact["per_ticker_execution_entries"]),
        },
        "risk_adjusted_target_definition_report.json": {
            **common, "report_name": "risk_adjusted_target_definition_report",
            **deepcopy(artifact["risk_adjusted_target_definition_analysis"]),
        },
        "label_family_impact_review_report.json": {
            **common, "report_name": "label_family_impact_review_report",
            "label_family_impact_review_count": 10,
            "label_family_impact_review": deepcopy(artifact["label_family_impact_review"]),
        },
        "meta_target_limitation_review_report.json": {
            **common, "report_name": "meta_target_limitation_review_report",
            **deepcopy(artifact["meta_target_limitation_review"]),
        },
        "acceptance_threshold_prerequisite_report.json": {
            **common, "report_name": "acceptance_threshold_prerequisite_report",
            **deepcopy(artifact["acceptance_threshold_prerequisite_review"]),
        },
        "operator_review_summary.json": {
            **common, "report_name": "operator_review_summary",
            "execution_status": artifact["execution_status"],
            "execution_digest": artifact["label_objective_redesign_execution_using_redesigned_evidence_digest"],
            "redesign_analysis_classification": deepcopy(artifact["redesign_analysis_classification"]),
            "generated_output_count": 12,
            "next_task": "Optional Label Objective Redesign Results Review Using Redesigned Evidence v1",
        },
    }
    payloads = {filename: canonical_json_bytes(payload) for filename, payload in reports.items()}
    entries = [
        ({"filename": filename, "digest_kind": SELF_REFERENCE_POLICY, "sha256": None}
         if filename == "label_objective_redesign_digest_manifest.json"
         else {"filename": filename, "digest_kind": "FILE_SHA256", "sha256": sha256_bytes(payloads[filename])})
        for filename in OUTPUT_FILENAMES
    ]
    manifest = {
        **common, "report_name": "label_objective_redesign_digest_manifest",
        "generated_output_count": 12, "output_digest_entries": entries,
        "all_non_self_output_digests_present": True,
        "self_reference_policy": SELF_REFERENCE_POLICY,
        "output_manifest_binding_digest": _output_manifest_binding_digest(),
        "execution_digest": artifact["label_objective_redesign_execution_using_redesigned_evidence_digest"],
    }
    payloads["label_objective_redesign_digest_manifest.json"] = canonical_json_bytes(manifest)
    return payloads


def _write_outputs_once(output_root: Path, payloads: dict[str, bytes]) -> None:
    existing = [name for name in OUTPUT_FILENAMES if (output_root / name).exists()]
    if existing:
        raise LabelObjectiveRedesignExecutionRedesignedEvidenceError(
            f"redesign execution outputs already exist: {', '.join(existing)}"
        )
    output_root.mkdir(parents=True, exist_ok=True)
    for filename in OUTPUT_FILENAMES:
        try:
            with (output_root / filename).open("xb") as handle:
                handle.write(payloads[filename])
        except FileExistsError as exc:
            raise LabelObjectiveRedesignExecutionRedesignedEvidenceError(
                f"refusing to overwrite redesign execution output: {filename}"
            ) from exc


def execute_label_objective_redesign_using_redesigned_evidence_v1(
    *, canonical_root: str | Path | None = None, label_root: str | Path | None = None,
    feature_root: str | Path | None = None, predictive_evidence_root: str | Path | None = None,
    label_objective_review_root: str | Path | None = None,
    output_root: str | Path | None = None, run_timestamp_utc: str | None = None,
) -> dict[str, Any]:
    """Analyze frozen evidence and write 12 research-only outputs once."""
    roots = {
        "canonical": DEFAULT_CANONICAL_ROOT if canonical_root is None else Path(canonical_root),
        "label": DEFAULT_LABEL_ROOT if label_root is None else Path(label_root),
        "feature": DEFAULT_FEATURE_ROOT if feature_root is None else Path(feature_root),
        "predictive": DEFAULT_PREDICTIVE_EVIDENCE_ROOT if predictive_evidence_root is None else Path(predictive_evidence_root),
        "review": DEFAULT_LABEL_OBJECTIVE_REVIEW_ROOT if label_objective_review_root is None else Path(label_objective_review_root),
    }
    output_path = DEFAULT_OUTPUT_ROOT if output_root is None else Path(output_root)
    timestamp = run_timestamp_utc or _utc_now()
    verification, reports, failures = _verify_sources(roots)
    if failures:
        return _blocked_artifact(roots=roots, output_root=output_path, run_timestamp_utc=timestamp,
                                 verification=verification, failures=failures)
    artifact = _build_artifact(
        roots=roots, output_root=output_path, run_timestamp_utc=timestamp,
        verification=verification, results=_analysis_results(reports),
    )
    validate_label_objective_redesign_executed_using_redesigned_evidence_v1(artifact)
    _write_outputs_once(output_path, _build_outputs(artifact))
    return artifact


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise LabelObjectiveRedesignExecutionRedesignedEvidenceError(
            f"{field} mismatch: expected {expected!r}, got {actual!r}"
        )


def validate_label_objective_redesign_executed_using_redesigned_evidence_v1(
    artifact: dict,
) -> dict[str, Any]:
    """Validate the execution and every closed downstream authority boundary."""
    if not isinstance(artifact, dict):
        raise LabelObjectiveRedesignExecutionRedesignedEvidenceError("artifact must be a JSON object")
    expected = {
        "artifact_kind": ARTIFACT_KIND_LABEL_OBJECTIVE_REDESIGN_EXECUTED_USING_REDESIGNED_EVIDENCE,
        "schema_version": SCHEMA_VERSION_LABEL_OBJECTIVE_REDESIGN_EXECUTED_USING_REDESIGNED_EVIDENCE_V1,
        "execution_status": LABEL_OBJECTIVE_REDESIGN_EXECUTED_USING_REDESIGNED_EVIDENCE_RESEARCH_ONLY,
        "source_evidence": _source_evidence(), "dataset_name": DATASET_NAME,
        "target_universe": TARGET_UNIVERSE, "target_universe_count": 12,
        "total_canonical_record_count": 11946, "records_digest": EXPECTED_RECORDS_DIGEST,
        "meta_record_count": 913, "non_meta_record_count": 1003,
        "selected_label_objective_redesign_direction": SELECTED_DIRECTION,
        "generated_output_count": 12, "generated_output_names": OUTPUT_FILENAMES,
        "redesign_theme_count": 11, "redesign_option_count": 8,
        "label_family_impact_review_count": 10, "redesign_question_count": 10,
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
        raise LabelObjectiveRedesignExecutionRedesignedEvidenceError("source verification missing")
    for field in ("all_required_source_files_present", "all_required_source_digests_match", "source_files_unchanged"):
        _expect(verification.get(field), True, field)
    manifest = artifact.get("output_digest_manifest_summary")
    if not isinstance(manifest, dict):
        raise LabelObjectiveRedesignExecutionRedesignedEvidenceError("output digest manifest missing")
    _expect(manifest.get("entry_count"), 12, "output digest manifest entry count")
    _expect(manifest.get("self_reference_policy"), SELF_REFERENCE_POLICY, "self reference policy")
    _expect(manifest.get("binding_digest"), _output_manifest_binding_digest(), "output manifest digest")
    for field, count in (
        ("redesign_themes", 11), ("redesign_options", 8), ("label_family_impact_review", 10),
        ("redesign_questions", 10), ("per_ticker_execution_entries", 12),
    ):
        value = artifact.get(field)
        if not isinstance(value, list) or len(value) != count:
            raise LabelObjectiveRedesignExecutionRedesignedEvidenceError(f"{field} mismatch")
    for entry in artifact["per_ticker_execution_entries"]:
        digest = entry.get("per_ticker_label_objective_redesign_execution_digest")
        if not isinstance(digest, str) or len(digest) != 64:
            raise LabelObjectiveRedesignExecutionRedesignedEvidenceError("per-ticker execution digest missing")
        _expect(digest, per_ticker_label_objective_redesign_execution_using_redesigned_evidence_digest_v1(entry),
                "per-ticker execution digest")
    classification = artifact.get("redesign_analysis_classification", {})
    _expect(classification.get("label_objective_redesign_classification"), "COMPLETED_RESEARCH_ONLY",
            "redesign classification")
    _expect(classification.get("redesign_decision_recommendation"),
            "NO_LABEL_REGENERATION_OR_NEW_TARGETS_AUTHORIZED_BY_THIS_EXECUTION",
            "redesign decision recommendation")
    _expect(artifact.get("failure_count"), 0, "failure_count")
    digest = artifact.get("label_objective_redesign_execution_using_redesigned_evidence_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise LabelObjectiveRedesignExecutionRedesignedEvidenceError("execution digest missing")
    _expect(digest, label_objective_redesign_execution_using_redesigned_evidence_digest_v1(artifact),
            "execution digest")
    return {
        "status": LABEL_OBJECTIVE_REDESIGN_EXECUTION_USING_REDESIGNED_EVIDENCE_VALID,
        "artifact_kind": artifact["artifact_kind"], "execution_status": artifact["execution_status"],
        "label_objective_redesign_execution_using_redesigned_evidence_digest": digest,
        "generated_output_count": 12, "failure_count": 0,
        "predictive_usefulness": NOT_ACCEPTED, "profitability": NOT_ACCEPTED,
        "runtime_authorized": False,
    }


def build_label_objective_redesign_execution_status_markdown_v1(artifact: dict) -> str:
    """Render a sanitized execution status document."""
    validation = validate_label_objective_redesign_executed_using_redesigned_evidence_v1(artifact)
    source = artifact["source_evidence"]
    sections = [
        ("Title", ["Optional Label Objective Redesign Execution Using Redesigned Evidence v1."]),
        ("Optional Label Objective Redesign Execution Using Redesigned Evidence", [
            f"Artifact/status: `{artifact['artifact_kind']}` / `{artifact['execution_status']}`.",
            f"Execution digest: `{validation['label_objective_redesign_execution_using_redesigned_evidence_digest']}`.",
        ]),
        ("Source Approval", [f"Approval digest: `{source['label_objective_redesign_approval_using_redesigned_evidence_digest']}`."]),
        ("Bound Evidence", [
            f"Records/labels/features/matrix: `{source['records_digest']}` / `{source['redesigned_label_values_digest']}` / `{source['feature_values_digest']}` / `{source['feature_label_matrix_digest']}`.",
        ]),
        ("Dataset and Universe", [f"`{DATASET_NAME}`; 11,946 records; META 913.", ", ".join(TARGET_UNIVERSE)]),
        ("Redesign Execution Policy", ["Frozen evidence was analyzed read-only; labels, target rows, models, and metrics were not regenerated or recomputed."]),
        ("Candidate Basis", [f"`{artifact['candidate_basis']}`"]),
        ("Selected Redesign Direction", [f"`{SELECTED_DIRECTION}`; analyzed research-only."]),
        ("Flat Class and Majority Structure Redesign Analysis", [f"`{artifact['flat_class_and_majority_structure_analysis']}`"]),
        ("No-Trade / Abstain Objective Analysis", [f"`{artifact['no_trade_abstain_objective_analysis']}`"]),
        ("Material-Move Target Definition Analysis", [f"`{artifact['material_move_target_definition_analysis']}`"]),
        ("Horizon-Specific Target Design Analysis", [f"`{artifact['horizon_specific_target_design_analysis']}`"]),
        ("Ticker or Regime Split Target Analysis", [f"`{artifact['ticker_or_regime_split_target_analysis']}`"]),
        ("Risk-Adjusted Target Definition Analysis", [f"`{artifact['risk_adjusted_target_definition_analysis']}`"]),
        ("Label Family Impact Review", [f"Research-only families reviewed: `{len(artifact['label_family_impact_review'])}`."]),
        ("META Target Limitation Review", [f"`{artifact['meta_target_limitation_review']}`"]),
        ("Acceptance Threshold Prerequisite Review", [f"`{artifact['acceptance_threshold_prerequisite_review']}`"]),
        ("Output Digest Manifest", [f"`{artifact['output_digest_manifest_summary']}`"]),
        ("Authority Boundary", ["Execution creates redesign analysis only; no label regeneration, new target, or target-definition authority is created."]),
        ("Predictive Usefulness Boundary", ["Predictive usefulness remains `not accepted`."]),
        ("Profitability Boundary", ["Profitability remains `not accepted`."]),
        ("Runtime Boundary", ["Runtime, strategy, paper, broker, and recommendations remain `NOT_AUTHORIZED`."]),
        ("Checklist Summary", [f"Failures/warnings: `{artifact['failure_count']}` / `{artifact['warning_count']}`."]),
        ("Guardrails", ["Offline, deterministic, research-only, non-actionable, and results-review-gated."]),
    ]
    lines = ["# MarketFlow Label Objective Redesign Execution Using Redesigned Evidence Status", ""]
    for title, body in sections:
        lines.extend([f"## {title}", *[f"- {item}" for item in body], ""])
    return "\n".join(lines)
