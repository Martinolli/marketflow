"""Offline execution of approved label-objective redesign planning outputs."""

from __future__ import annotations

import json
from collections import Counter
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
    label_objective_redesign_execution_approval_service as approval,
)


ARTIFACT_KIND_LABEL_OBJECTIVE_REDESIGN_EXECUTED = (
    "LABEL_OBJECTIVE_REDESIGN_EXECUTED"
)
ARTIFACT_KIND_LABEL_OBJECTIVE_REDESIGN_EXECUTION_BLOCKED = (
    "LABEL_OBJECTIVE_REDESIGN_EXECUTION_BLOCKED"
)
SCHEMA_VERSION_LABEL_OBJECTIVE_REDESIGN_EXECUTED_V1 = (
    "label_objective_redesign_executed_v1"
)
LABEL_OBJECTIVE_REDESIGN_EXECUTED_RESEARCH_ONLY = (
    "LABEL_OBJECTIVE_REDESIGN_EXECUTED_RESEARCH_ONLY"
)
LABEL_OBJECTIVE_REDESIGN_EXECUTION_BLOCKED_MISSING_OR_INVALID_CANONICAL_DATASET = (
    "LABEL_OBJECTIVE_REDESIGN_EXECUTION_BLOCKED_MISSING_OR_INVALID_CANONICAL_DATASET"
)
LABEL_OBJECTIVE_REDESIGN_EXECUTION_VALID = (
    "LABEL_OBJECTIVE_REDESIGN_EXECUTION_VALID"
)

DEFAULT_SOURCE_ROOT = (
    Path(".marketflow") / "canonical_datasets" / "expanded_universe_v1"
)
DEFAULT_OUTPUT_ROOT = (
    Path(".marketflow") / "label_objective_redesign" / "expanded_universe_v1"
)
DEFAULT_BRANCH = "feature/label-objective-redesign-execution-v1"
DEFAULT_BASE_COMMIT = "20b92b7020ce97e328bc9a96ab75d44624371206"

EXPECTED_EXECUTION_APPROVAL_DIGEST = (
    "8ca1dee0aa2c175a1ab5bf7f9ba724b8dc0df6e2057e4f97721bad02f4adaff0"
)
EXPECTED_EXECUTION_CANDIDATE_REVIEW_PACKAGE_DIGEST = (
    approval.EXPECTED_EXECUTION_CANDIDATE_REVIEW_PACKAGE_DIGEST
)
EXPECTED_EXECUTION_CANDIDATE_DIGEST = (
    approval.EXPECTED_EXECUTION_CANDIDATE_DIGEST
)
EXPECTED_LABEL_OBJECTIVE_REDESIGN_APPROVAL_DIGEST = approval.REQUIRED_DIGEST_FIELDS[
    "label_objective_redesign_approval_digest"
]
EXPECTED_CANDIDATE_REVIEW_PACKAGE_DIGEST = approval.REQUIRED_DIGEST_FIELDS[
    "label_objective_redesign_candidate_review_package_digest"
]
EXPECTED_OPERATOR_METHOD_PATH_SELECTION_DIGEST = approval.REQUIRED_DIGEST_FIELDS[
    "operator_method_path_selection_digest"
]
EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST = approval.REQUIRED_DIGEST_FIELDS[
    "research_registry_approval_digest"
]
EXPECTED_RECORDS_DIGEST = approval.REQUIRED_DIGEST_FIELDS["records_digest"]
EXPECTED_CANONICAL_DATASET_GENERATION_DIGEST = (
    "9250ce29d7ba9754b43cfde07a5ded937a9402563691757a5aa6f7014f30fdbb"
)

TARGET_UNIVERSE = list(approval.TARGET_UNIVERSE)
EXPECTED_RECORD_COUNTS = {
    ticker: 913 if ticker == "META" else 1003 for ticker in TARGET_UNIVERSE
}
NOT_ACCEPTED = approval.NOT_ACCEPTED
NOT_AUTHORIZED = approval.NOT_AUTHORIZED
OUTPUT_LABEL = "RESEARCH_ONLY_NON_ACTIONABLE"
EVIDENCE_SCOPE = "LABEL_OBJECTIVE_REDESIGN_RESEARCH_ONLY"
NOT_GENERATED = "NOT_GENERATED"
NOT_EXECUTED = "NOT_EXECUTED"
NOT_AUTHORIZED_FOR_LABEL_GENERATION = "NOT_AUTHORIZED_FOR_LABEL_GENERATION"
DESIGN_ONLY_NOT_EXECUTED = "DESIGN_ONLY_NOT_EXECUTED"

REQUIRED_SOURCE_FILENAMES = [
    "canonical_dataset_generation_run_manifest.json",
    "canonical_dataset_source_evidence_manifest.json",
    "canonical_dataset_schema_contract.json",
    "canonical_dataset_records.jsonl",
    "per_ticker_canonical_dataset_summary.json",
    "canonical_dataset_data_quality_report.json",
    "canonical_dataset_digest_manifest.json",
    "canonical_dataset_failure_reason_inventory.json",
    "operator_review_summary.json",
]

OUTPUT_FILENAMES = [
    "label_objective_redesign_execution_manifest.json",
    "label_family_candidate_matrix.json",
    "threshold_design_matrix.json",
    "horizon_design_matrix.json",
    "per_ticker_label_objective_plan.json",
    "label_availability_boundary_plan.json",
    "meta_limitation_preservation_plan.json",
    "operator_review_summary_template.json",
]

LABEL_FAMILY_IDS = list(
    approval.review_service.candidate_service.candidate_service.LABEL_FAMILY_CANDIDATES
)
EXECUTION_ACTIVITY_IDS = list(
    approval.review_service.candidate_service.PLANNED_EXECUTION_ACTIVITIES
)
WORKSTREAM_IDS = list(
    approval.review_service.candidate_service.PLANNED_WORKSTREAMS
)

THRESHOLD_STRATEGY_IDS = [
    "global_threshold_candidate",
    "per_ticker_threshold_candidate",
    "training_window_only_threshold_candidate",
    "volatility_adjusted_threshold_candidate",
    "benchmark_relative_threshold_candidate",
    "flat_zone_threshold_candidate",
    "class_balance_review_candidate",
]

HORIZON_CANDIDATE_IDS = [
    "1_session",
    "5_session",
    "10_session",
    "20_session",
    "multi_horizon_comparison",
]

CHECK_IDS = [
    "artifact_kind_matches",
    "execution_status_matches",
    "execution_approval_digest_bound",
    "execution_candidate_review_digest_bound",
    "execution_candidate_digest_bound",
    "records_digest_bound",
    "target_universe_12_preserved",
    "total_record_count_11946",
    "meta_913_preserved",
    "execution_approved_true",
    "execution_authorized_true",
    "ready_for_execution_true",
    "execution_performed_true",
    "results_created_true",
    "generated_output_count_8",
    "all_planning_outputs_created",
    "candidate_label_family_count_10",
    "threshold_strategy_count_7",
    "horizon_candidate_count_5",
    "per_ticker_plan_count_12",
    "output_digest_manifest_complete",
    "outputs_research_only",
    "label_generation_false",
    "redesigned_label_generation_authorized_false",
    "redesigned_label_generation_performed_false",
    "feature_generation_false",
    "metric_recomputation_false",
    "model_training_false",
    "additional_predictive_evidence_candidate_false",
    "predictive_usefulness_not_accepted",
    "profitability_not_accepted",
    "runtime_not_authorized",
    "strategy_not_authorized",
    "paper_trading_not_authorized",
    "broker_not_authorized",
    "trade_recommendations_false",
    "provider_requests_false",
    "market_data_acquisition_false",
    "dataset_regeneration_false",
    "predictive_evidence_rerun_false",
    "refined_evidence_rerun_false",
    "raw_provider_payloads_not_committed",
    "api_keys_not_stored_or_printed",
    "no_tracked_marketflow_files",
]


class LabelObjectiveRedesignExecutionError(ValueError):
    """Raised when planning-output execution violates its guarded contract."""


def _utc_now() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


def _path_text(path: Path) -> str:
    return str(path).replace("\\", "/")


def _failure(failure_id: str, message: str, **details: Any) -> dict[str, Any]:
    return {"failure_id": failure_id, "message": message, **details}


def _source_evidence() -> dict[str, str]:
    return {
        "label_objective_redesign_execution_approval_digest": (
            EXPECTED_EXECUTION_APPROVAL_DIGEST
        ),
        "label_objective_redesign_execution_candidate_review_package_digest": (
            EXPECTED_EXECUTION_CANDIDATE_REVIEW_PACKAGE_DIGEST
        ),
        "label_objective_redesign_execution_candidate_digest": (
            EXPECTED_EXECUTION_CANDIDATE_DIGEST
        ),
        "label_objective_redesign_approval_digest": (
            EXPECTED_LABEL_OBJECTIVE_REDESIGN_APPROVAL_DIGEST
        ),
        "label_objective_redesign_candidate_review_package_digest": (
            EXPECTED_CANDIDATE_REVIEW_PACKAGE_DIGEST
        ),
        "operator_method_path_selection_digest": (
            EXPECTED_OPERATOR_METHOD_PATH_SELECTION_DIGEST
        ),
        "research_registry_approval_digest": (
            EXPECTED_RESEARCH_REGISTRY_APPROVAL_DIGEST
        ),
        "records_digest": EXPECTED_RECORDS_DIGEST,
    }


def _common_output_fields() -> dict[str, Any]:
    return {
        "output_label": OUTPUT_LABEL,
        "evidence_scope": EVIDENCE_SCOPE,
        "dataset_name": "expanded_universe_canonical_dataset_v1",
        "records_digest": EXPECTED_RECORDS_DIGEST,
        "label_objective_redesign_execution_approved": True,
        "label_objective_redesign_authorized": True,
        "ready_for_label_objective_redesign_execution": True,
        "label_objective_redesign_executed": True,
        "label_objective_redesign_results_created": True,
        "redesigned_label_generation_authorized": False,
        "redesigned_label_generation_performed": False,
        "redesigned_feature_generation_authorized": False,
        "redesigned_feature_generation_performed": False,
        "redesigned_protocol_evaluation_authorized": False,
        "redesigned_protocol_evaluation_performed": False,
        "additional_predictive_evidence_execution_candidate_created": False,
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "trade_recommendations_generated": False,
    }


def _report(
    report_name: str, run_timestamp_utc: str, payload: Mapping[str, Any]
) -> dict[str, Any]:
    return {
        "report_name": report_name,
        "run_timestamp_utc": run_timestamp_utc,
        **_common_output_fields(),
        **deepcopy(dict(payload)),
    }


def _verify_source_root(
    source_root: Path,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    failures: list[dict[str, Any]] = []
    for filename in REQUIRED_SOURCE_FILENAMES:
        if not (source_root / filename).is_file():
            failures.append(
                _failure(
                    "missing_source_file",
                    "required canonical source file missing",
                    filename=filename,
                )
            )
    if failures:
        return {}, failures

    records_path = source_root / "canonical_dataset_records.jsonl"
    records_digest = sha256_file(records_path)
    if records_digest != EXPECTED_RECORDS_DIGEST:
        failures.append(
            _failure(
                "records_digest_mismatch",
                "canonical records digest mismatch",
                expected=EXPECTED_RECORDS_DIGEST,
                actual=records_digest,
            )
        )
    try:
        digest_manifest = json.loads(
            (source_root / "canonical_dataset_digest_manifest.json").read_text(
                encoding="utf-8"
            )
        )
        generation_manifest = json.loads(
            (
                source_root / "canonical_dataset_generation_run_manifest.json"
            ).read_text(encoding="utf-8")
        )
        ticker_summary = json.loads(
            (source_root / "per_ticker_canonical_dataset_summary.json").read_text(
                encoding="utf-8"
            )
        )
    except (OSError, json.JSONDecodeError) as exc:
        failures.append(_failure("invalid_source_json", str(exc)))
        return {}, failures

    digest_entries = digest_manifest.get("canonical_output_digest_manifest", [])
    if not isinstance(digest_entries, list):
        failures.append(
            _failure("invalid_digest_manifest", "digest entries must be a list")
        )
        digest_entries = []
    for entry in digest_entries:
        filename = entry.get("filename")
        digest_kind = entry.get("digest_kind")
        expected_digest = entry.get("sha256")
        if digest_kind == "SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE":
            if (
                filename != "canonical_dataset_digest_manifest.json"
                or expected_digest is not None
            ):
                failures.append(
                    _failure(
                        "invalid_self_reference_policy",
                        "invalid digest-manifest self-reference",
                        filename=filename,
                    )
                )
            continue
        if digest_kind == "CANONICAL_DATASET_GENERATION_DIGEST":
            if (
                filename != "canonical_dataset_generation_run_manifest.json"
                or expected_digest != EXPECTED_CANONICAL_DATASET_GENERATION_DIGEST
            ):
                failures.append(
                    _failure(
                        "invalid_generation_digest_entry",
                        "canonical generation digest entry is invalid",
                        filename=filename,
                    )
                )
            continue
        if filename not in REQUIRED_SOURCE_FILENAMES or digest_kind != "FILE_SHA256":
            failures.append(
                _failure(
                    "invalid_digest_entry",
                    "canonical digest entry is invalid",
                    filename=filename,
                )
            )
            continue
        actual = sha256_file(source_root / filename)
        if actual != expected_digest:
            failures.append(
                _failure(
                    "source_output_digest_mismatch",
                    "canonical source output digest mismatch",
                    filename=filename,
                    expected=expected_digest,
                    actual=actual,
                )
            )

    if generation_manifest.get("canonical_dataset_generation_digest") != (
        EXPECTED_CANONICAL_DATASET_GENERATION_DIGEST
    ):
        failures.append(
            _failure(
                "generation_digest_mismatch",
                "canonical dataset generation digest mismatch",
            )
        )
    if ticker_summary.get("target_universe") != TARGET_UNIVERSE:
        failures.append(
            _failure("target_universe_mismatch", "target universe mismatch")
        )
    if ticker_summary.get("total_canonical_record_count") != 11946:
        failures.append(
            _failure(
                "summary_record_count_mismatch",
                "canonical summary record count mismatch",
            )
        )
    summary_counts = {
        row.get("ticker"): row.get("canonical_record_count")
        for row in ticker_summary.get("per_ticker_canonical_record_summary", [])
    }
    if summary_counts != EXPECTED_RECORD_COUNTS:
        failures.append(
            _failure(
                "summary_per_ticker_counts_mismatch",
                "canonical per-ticker summary counts mismatch",
            )
        )

    actual_counts: Counter[str] = Counter()
    total_records = 0
    try:
        with records_path.open("r", encoding="utf-8") as handle:
            for line_number, line in enumerate(handle, start=1):
                if not line.strip():
                    continue
                row = json.loads(line)
                ticker = row.get("ticker")
                if ticker not in TARGET_UNIVERSE:
                    failures.append(
                        _failure(
                            "unexpected_ticker",
                            "unexpected ticker in canonical records",
                            line_number=line_number,
                            ticker=ticker,
                        )
                    )
                else:
                    actual_counts[ticker] += 1
                total_records += 1
    except (OSError, json.JSONDecodeError) as exc:
        failures.append(_failure("invalid_records_file", str(exc)))
    if total_records != 11946:
        failures.append(
            _failure(
                "actual_record_count_mismatch",
                "canonical records line count mismatch",
                expected=11946,
                actual=total_records,
            )
        )
    if dict(actual_counts) != EXPECTED_RECORD_COUNTS:
        failures.append(
            _failure(
                "actual_per_ticker_counts_mismatch",
                "canonical records per-ticker counts mismatch",
                expected=EXPECTED_RECORD_COUNTS,
                actual=dict(actual_counts),
            )
        )
    verification = {
        "source_root": _path_text(source_root),
        "required_source_file_count": len(REQUIRED_SOURCE_FILENAMES),
        "required_source_files": list(REQUIRED_SOURCE_FILENAMES),
        "records_digest_expected": EXPECTED_RECORDS_DIGEST,
        "records_digest_actual": records_digest,
        "records_digest_match": records_digest == EXPECTED_RECORDS_DIGEST,
        "total_record_count_actual": total_records,
        "per_ticker_record_counts_actual": dict(actual_counts),
        "canonical_dataset_generation_digest": generation_manifest.get(
            "canonical_dataset_generation_digest"
        ),
        "digest_manifest_self_reference_policy": (
            "SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE"
        ),
    }
    return verification, failures


def _label_family_matrix() -> list[dict[str, Any]]:
    objective_types = {
        "LABEL_FAMILY_CANDIDATE_DIRECTION_WITH_FLAT_ZONE": "DIRECTION_CLASSIFICATION",
        "LABEL_FAMILY_CANDIDATE_RETURN_BUCKET_REDESIGNED_THRESHOLDS": "RETURN_BUCKET_CLASSIFICATION",
        "LABEL_FAMILY_CANDIDATE_MULTI_HORIZON_5_10_20": "MULTI_HORIZON_RETURN_CLASSIFICATION",
        "LABEL_FAMILY_CANDIDATE_BENCHMARK_RELATIVE_RETURN": "BENCHMARK_RELATIVE_RETURN",
        "LABEL_FAMILY_CANDIDATE_VOLATILITY_ADJUSTED_RETURN": "RISK_ADJUSTED_RETURN",
        "LABEL_FAMILY_CANDIDATE_DRAWDOWN_AVOIDANCE": "DRAWDOWN_AVOIDANCE",
        "LABEL_FAMILY_CANDIDATE_RISK_REWARD_ASYMMETRIC_TARGET": "ASYMMETRIC_RISK_REWARD",
        "LABEL_FAMILY_CANDIDATE_REGIME_CONDITIONED_DIRECTION": "REGIME_CONDITIONED_DIRECTION",
        "LABEL_FAMILY_CANDIDATE_PER_TICKER_CALIBRATED_TARGET": "PER_TICKER_CALIBRATED_TARGET",
        "LABEL_FAMILY_CANDIDATE_NO_TRADE_ZONE_CLASS": "NO_TRADE_ZONE_CLASSIFICATION",
    }
    horizons = {
        "LABEL_FAMILY_CANDIDATE_MULTI_HORIZON_5_10_20": "5_10_20_SESSIONS",
        "LABEL_FAMILY_CANDIDATE_DRAWDOWN_AVOIDANCE": "20_SESSIONS_CANDIDATE",
    }
    rows: list[dict[str, Any]] = []
    for family_id in LABEL_FAMILY_IDS:
        relative = "RELATIVE" if "BENCHMARK_RELATIVE" in family_id else "ABSOLUTE_OR_RELATIVE_TO_BE_REVIEWED"
        risk_adjusted = "REQUIRED" if any(token in family_id for token in ("VOLATILITY", "DRAWDOWN", "RISK_REWARD")) else "OPTIONAL_CANDIDATE"
        rows.append(
            {
                "candidate_family_id": family_id,
                "objective_type": objective_types[family_id],
                "prediction_horizon_candidate": horizons.get(
                    family_id, "1_5_10_20_SESSION_DESIGN_REVIEW"
                ),
                "threshold_style_candidate": "TRAINING_WINDOW_ONLY_DESIGN_CANDIDATE",
                "flat_no_trade_zone_candidate": (
                    "EXPLICIT_CANDIDATE"
                    if "FLAT_ZONE" in family_id or "NO_TRADE_ZONE" in family_id
                    else "REVIEW_FOR_APPLICABILITY"
                ),
                "absolute_vs_relative_basis": relative,
                "risk_adjusted_basis": risk_adjusted,
                "per_ticker_calibration_consideration": "DESIGN_REVIEW_ONLY_NOT_COMPUTED",
                "meta_limitation_handling": "PRESERVE_913_RECORD_LIMIT_AND_LABEL_AVAILABILITY_BOUNDARY",
                "generation_status": NOT_GENERATED,
                "authorization_status": NOT_AUTHORIZED_FOR_LABEL_GENERATION,
            }
        )
    return rows


def _threshold_design_matrix() -> list[dict[str, Any]]:
    return [
        {
            "threshold_strategy_id": strategy_id,
            "design_scope": strategy_id.upper(),
            "calibration_data_boundary": "TRAINING_WINDOW_ONLY_WHERE_APPLICABLE",
            "final_threshold_computed": False,
            "status": DESIGN_ONLY_NOT_EXECUTED,
        }
        for strategy_id in THRESHOLD_STRATEGY_IDS
    ]


def _horizon_design_matrix() -> list[dict[str, Any]]:
    return [
        {
            "horizon_candidate_id": horizon_id,
            "horizon_frequency_alignment_concern": (
                "ASSESS_DAILY_FEATURE_ALIGNMENT_WITH_FORWARD_SESSION_HORIZON"
            ),
            "comparison_required": True,
            "final_horizon_selected": False,
            "status": DESIGN_ONLY_NOT_EXECUTED,
        }
        for horizon_id in HORIZON_CANDIDATE_IDS
    ]


def _per_ticker_plan() -> list[dict[str, Any]]:
    return [
        {
            "ticker": ticker,
            "historical_record_count": EXPECTED_RECORD_COUNTS[ticker],
            "meta_reduced_record_count_flag": ticker == "META",
            "candidate_label_families_applicable": list(LABEL_FAMILY_IDS),
            "per_ticker_calibration_consideration": (
                "DESIGN_REVIEW_ONLY_NOT_COMPUTED"
            ),
            "label_availability_consideration": (
                "PRESERVE_REDUCED_RECORD_COUNT_AND_LABEL_AVAILABILITY_LIMITATION"
                if ticker == "META"
                else "PRESERVE_FORWARD_HORIZON_TAIL_AVAILABILITY_BOUNDARY"
            ),
            "execution_status": NOT_EXECUTED,
            "label_generation_performed": False,
        }
        for ticker in TARGET_UNIVERSE
    ]


def _build_reports(run_timestamp_utc: str) -> dict[str, dict[str, Any]]:
    family_matrix = _label_family_matrix()
    threshold_matrix = _threshold_design_matrix()
    horizon_matrix = _horizon_design_matrix()
    ticker_plan = _per_ticker_plan()
    return {
        "label_family_candidate_matrix.json": _report(
            "label_family_candidate_matrix",
            run_timestamp_utc,
            {
                "candidate_label_family_count": len(family_matrix),
                "label_family_candidates": family_matrix,
                "matrix_status": DESIGN_ONLY_NOT_EXECUTED,
            },
        ),
        "threshold_design_matrix.json": _report(
            "threshold_design_matrix",
            run_timestamp_utc,
            {
                "threshold_design_strategy_count": len(threshold_matrix),
                "threshold_design_strategies": threshold_matrix,
                "matrix_status": DESIGN_ONLY_NOT_EXECUTED,
            },
        ),
        "horizon_design_matrix.json": _report(
            "horizon_design_matrix",
            run_timestamp_utc,
            {
                "horizon_design_candidate_count": len(horizon_matrix),
                "horizon_design_candidates": horizon_matrix,
                "matrix_status": DESIGN_ONLY_NOT_EXECUTED,
            },
        ),
        "per_ticker_label_objective_plan.json": _report(
            "per_ticker_label_objective_plan",
            run_timestamp_utc,
            {
                "target_universe": list(TARGET_UNIVERSE),
                "per_ticker_plan_count": len(ticker_plan),
                "per_ticker_label_objective_plans": ticker_plan,
            },
        ),
        "label_availability_boundary_plan.json": _report(
            "label_availability_boundary_plan",
            run_timestamp_utc,
            {
                "availability_rules": [
                    "forward_horizon_tail_rows_remain_unavailable",
                    "threshold_calibration_must_use_training_window_only",
                    "no_future_information_may_cross_training_evaluation_boundary",
                    "missing_forward_outcomes_must_not_be_fabricated",
                    "meta_reduced_record_count_limits_label_availability",
                ],
                "label_generation_authorized": False,
                "label_generation_performed": False,
                "plan_status": DESIGN_ONLY_NOT_EXECUTED,
            },
        ),
        "meta_limitation_preservation_plan.json": _report(
            "meta_limitation_preservation_plan",
            run_timestamp_utc,
            {
                "ticker": "META",
                "historical_record_count": 913,
                "no_backfill": True,
                "no_repair": True,
                "no_synthetic_rows": True,
                "label_availability_limitation_carried_forward": True,
                "preservation_status": "PRESERVED_NOT_REPAIRED",
            },
        ),
        "operator_review_summary_template.json": _report(
            "operator_review_summary_template",
            run_timestamp_utc,
            {
                "review_status": "AWAITING_SEPARATE_RESULTS_REVIEW",
                "review_sections": [
                    "source_evidence_review",
                    "label_family_candidate_matrix_review",
                    "threshold_design_matrix_review",
                    "horizon_design_matrix_review",
                    "per_ticker_plan_review",
                    "label_availability_boundary_review",
                    "meta_limitation_preservation_review",
                    "authority_boundary_review",
                ],
                "operator_decision": None,
                "results_review_created": False,
            },
        ),
    }


def _blocked_artifact(
    *,
    source_root: Path,
    output_root: Path,
    run_timestamp_utc: str,
    failures: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_LABEL_OBJECTIVE_REDESIGN_EXECUTION_BLOCKED,
        "schema_version": SCHEMA_VERSION_LABEL_OBJECTIVE_REDESIGN_EXECUTED_V1,
        "execution_status": LABEL_OBJECTIVE_REDESIGN_EXECUTION_BLOCKED_MISSING_OR_INVALID_CANONICAL_DATASET,
        "run_timestamp_utc": run_timestamp_utc,
        "created_offline": True,
        "research_only": True,
        "source_root": _path_text(source_root),
        "generated_output_root": _path_text(output_root),
        "label_objective_redesign_execution_digest": "NOT_CREATED",
        "label_objective_redesign_execution_approved": True,
        "label_objective_redesign_authorized": True,
        "ready_for_label_objective_redesign_execution": True,
        "label_objective_redesign_executed": False,
        "label_objective_redesign_results_created": False,
        "redesigned_label_generation_authorized": False,
        "redesigned_label_generation_performed": False,
        "generated_output_count": 0,
        "failure_count": len(failures),
        "warning_count": 0,
        "failures": failures,
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "new_strategy_scoring_performed": False,
        "trade_recommendations_generated": False,
    }


def _check(check_id: str, expected: Any, actual: Any) -> dict[str, Any]:
    passed = actual == expected
    return {
        "check_id": check_id,
        "status": "PASS" if passed else "FAIL",
        "expected": expected,
        "actual": actual,
        "severity": "BLOCKER",
        "message": f"{check_id} {'passed' if passed else 'failed'}",
    }


def _derived_checks(artifact: dict[str, Any]) -> dict[str, bool]:
    manifest = artifact.get("output_digest_manifest", [])
    created_fields = [
        "label_objective_redesign_manifest_created",
        "label_family_candidate_matrix_created",
        "threshold_design_matrix_created",
        "horizon_design_matrix_created",
        "per_ticker_label_objective_plan_created",
        "label_availability_boundary_plan_created",
        "meta_limitation_preservation_plan_created",
        "operator_review_summary_template_created",
    ]
    return {
        "artifact_kind_matches": artifact.get("artifact_kind") == ARTIFACT_KIND_LABEL_OBJECTIVE_REDESIGN_EXECUTED,
        "execution_status_matches": artifact.get("execution_status") == LABEL_OBJECTIVE_REDESIGN_EXECUTED_RESEARCH_ONLY,
        "execution_approval_digest_bound": artifact.get("source_evidence", {}).get("label_objective_redesign_execution_approval_digest") == EXPECTED_EXECUTION_APPROVAL_DIGEST,
        "execution_candidate_review_digest_bound": artifact.get("source_evidence", {}).get("label_objective_redesign_execution_candidate_review_package_digest") == EXPECTED_EXECUTION_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "execution_candidate_digest_bound": artifact.get("source_evidence", {}).get("label_objective_redesign_execution_candidate_digest") == EXPECTED_EXECUTION_CANDIDATE_DIGEST,
        "records_digest_bound": artifact.get("records_digest") == EXPECTED_RECORDS_DIGEST,
        "target_universe_12_preserved": artifact.get("target_universe_count") == 12 and artifact.get("target_universe") == TARGET_UNIVERSE,
        "total_record_count_11946": artifact.get("total_canonical_record_count") == 11946,
        "meta_913_preserved": artifact.get("meta_record_count") == 913 and artifact.get("per_ticker_record_counts", {}).get("META") == 913 and artifact.get("meta_reduced_record_count_preserved") is True,
        "execution_approved_true": artifact.get("label_objective_redesign_execution_approved") is True,
        "execution_authorized_true": artifact.get("label_objective_redesign_authorized") is True,
        "ready_for_execution_true": artifact.get("ready_for_label_objective_redesign_execution") is True,
        "execution_performed_true": artifact.get("label_objective_redesign_executed") is True,
        "results_created_true": artifact.get("label_objective_redesign_results_created") is True,
        "generated_output_count_8": artifact.get("generated_output_count") == 8 and artifact.get("generated_output_names") == OUTPUT_FILENAMES,
        "all_planning_outputs_created": all(artifact.get(field) is True for field in created_fields),
        "candidate_label_family_count_10": artifact.get("candidate_label_family_count") == 10,
        "threshold_strategy_count_7": artifact.get("threshold_design_strategy_count") == 7,
        "horizon_candidate_count_5": artifact.get("horizon_design_candidate_count") == 5,
        "per_ticker_plan_count_12": artifact.get("per_ticker_plan_count") == 12,
        "output_digest_manifest_complete": isinstance(manifest, list) and len(manifest) == 8 and all((row.get("digest_kind") == "SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE" and row.get("sha256") is None) if row.get("filename") == OUTPUT_FILENAMES[0] else row.get("digest_kind") == "FILE_SHA256" and isinstance(row.get("sha256"), str) and len(row["sha256"]) == 64 for row in manifest if isinstance(row, dict)),
        "outputs_research_only": artifact.get("output_label") == OUTPUT_LABEL and artifact.get("evidence_scope") == EVIDENCE_SCOPE,
        "label_generation_false": artifact.get("label_generation_performed") is False,
        "redesigned_label_generation_authorized_false": artifact.get("redesigned_label_generation_authorized") is False,
        "redesigned_label_generation_performed_false": artifact.get("redesigned_label_generation_performed") is False,
        "feature_generation_false": artifact.get("feature_generation_performed") is False,
        "metric_recomputation_false": artifact.get("metric_recomputation_performed") is False,
        "model_training_false": artifact.get("model_training_performed") is False,
        "additional_predictive_evidence_candidate_false": artifact.get("additional_predictive_evidence_execution_candidate_created") is False,
        "predictive_usefulness_not_accepted": artifact.get("predictive_usefulness") == NOT_ACCEPTED,
        "profitability_not_accepted": artifact.get("profitability") == NOT_ACCEPTED,
        "runtime_not_authorized": artifact.get("runtime_migration_approved") is False and artifact.get("runtime_migration_active") is False and artifact.get("runtime_use") == NOT_AUTHORIZED,
        "strategy_not_authorized": artifact.get("strategy_use") == NOT_AUTHORIZED,
        "paper_trading_not_authorized": artifact.get("paper_trading") == NOT_AUTHORIZED,
        "broker_not_authorized": artifact.get("broker_execution") == NOT_AUTHORIZED,
        "trade_recommendations_false": artifact.get("trade_recommendations_generated") is False,
        "provider_requests_false": artifact.get("provider_requests_made_in_execution") is False,
        "market_data_acquisition_false": artifact.get("market_data_acquisition_performed_in_execution") is False,
        "dataset_regeneration_false": artifact.get("canonical_dataset_regenerated_in_execution") is False,
        "predictive_evidence_rerun_false": artifact.get("predictive_evidence_rerun_performed") is False,
        "refined_evidence_rerun_false": artifact.get("refined_evidence_rerun_performed") is False,
        "raw_provider_payloads_not_committed": artifact.get("raw_provider_payloads_committed") is False,
        "api_keys_not_stored_or_printed": artifact.get("api_keys_stored_or_printed") is False,
        "no_tracked_marketflow_files": artifact.get("no_tracked_marketflow_files") is True and artifact.get("tracked_marketflow_files") == [],
    }


def _checklist(artifact: dict[str, Any]) -> list[dict[str, Any]]:
    checks = _derived_checks(artifact)
    return [_check(check_id, True, checks.get(check_id)) for check_id in CHECK_IDS]


def _execution_summary(
    checklist: list[dict[str, Any]],
) -> dict[str, Any]:
    total = len(checklist)
    passed = sum(row.get("status") == "PASS" for row in checklist)
    failed = total - passed
    blockers = sum(
        row.get("status") == "FAIL" and row.get("severity") == "BLOCKER"
        for row in checklist
    )
    return {
        "total_checks": total,
        "passed_checks": passed,
        "failed_checks": failed,
        "blocker_count": blockers,
        "target_count": 12,
        "total_canonical_record_count": 11946,
        "generated_output_count": 8,
        "candidate_label_family_count": 10,
        "threshold_design_strategy_count": 7,
        "horizon_design_candidate_count": 5,
        "per_ticker_plan_count": 12,
        "failure_count": 0,
        "warning_count": 1,
        "label_objective_redesign_execution_digest": "PENDING",
    }


def _build_executed_artifact(
    *,
    run_timestamp_utc: str,
    source_root: Path,
    output_root: Path,
    source_verification: dict[str, Any],
    output_digest_manifest: list[dict[str, Any]],
) -> dict[str, Any]:
    artifact: dict[str, Any] = {
        "artifact_kind": ARTIFACT_KIND_LABEL_OBJECTIVE_REDESIGN_EXECUTED,
        "schema_version": SCHEMA_VERSION_LABEL_OBJECTIVE_REDESIGN_EXECUTED_V1,
        "execution_status": LABEL_OBJECTIVE_REDESIGN_EXECUTED_RESEARCH_ONLY,
        "branch": DEFAULT_BRANCH,
        "base_commit": DEFAULT_BASE_COMMIT,
        "run_timestamp_utc": run_timestamp_utc,
        "created_offline": True,
        "research_only": True,
        "operator_review_required": True,
        "output_label": OUTPUT_LABEL,
        "evidence_scope": EVIDENCE_SCOPE,
        "dataset_name": "expanded_universe_canonical_dataset_v1",
        "provider_requests_made_in_execution": False,
        "live_provider_transport_enabled_in_execution": False,
        "market_data_acquisition_performed_in_execution": False,
        "dataset_generation_performed_in_execution": False,
        "canonical_dataset_regenerated_in_execution": False,
        "predictive_evidence_rerun_performed": False,
        "refined_evidence_rerun_performed": False,
        "label_generation_performed": False,
        "redesigned_label_generation_performed": False,
        "feature_generation_performed": False,
        "metric_recomputation_performed": False,
        "model_training_performed": False,
        "raw_provider_payloads_committed": False,
        "api_keys_stored_or_printed": False,
        "label_objective_redesign_execution_approved": True,
        "label_objective_redesign_authorized": True,
        "ready_for_label_objective_redesign_execution": True,
        "label_objective_redesign_executed": True,
        "label_objective_redesign_results_created": True,
        "label_objective_redesign_manifest_created": True,
        "label_family_candidate_matrix_created": True,
        "threshold_design_matrix_created": True,
        "horizon_design_matrix_created": True,
        "per_ticker_label_objective_plan_created": True,
        "label_availability_boundary_plan_created": True,
        "meta_limitation_preservation_plan_created": True,
        "operator_review_summary_template_created": True,
        "redesigned_label_generation_authorized": False,
        "redesigned_feature_generation_authorized": False,
        "redesigned_feature_generation_performed": False,
        "redesigned_protocol_evaluation_authorized": False,
        "redesigned_protocol_evaluation_performed": False,
        "additional_predictive_evidence_execution_candidate_created": False,
        "additional_predictive_evidence_execution_authorized": False,
        "additional_predictive_evidence_executed": False,
        "generated_output_count": 8,
        "generated_output_names": list(OUTPUT_FILENAMES),
        "target_universe": list(TARGET_UNIVERSE),
        "target_universe_count": 12,
        "total_canonical_record_count": 11946,
        "records_digest": EXPECTED_RECORDS_DIGEST,
        "per_ticker_record_counts": deepcopy(EXPECTED_RECORD_COUNTS),
        "meta_record_count": 913,
        "non_meta_record_count": 1003,
        "meta_reduced_record_count_preserved": True,
        "candidate_label_family_count": 10,
        "threshold_design_strategy_count": 7,
        "horizon_design_candidate_count": 5,
        "per_ticker_plan_count": 12,
        "failure_count": 0,
        "warning_count": 1,
        "warnings": [
            "META_913_RECORD_LIMIT_AND_LABEL_AVAILABILITY_LIMITATION_PRESERVED"
        ],
        "source_root": _path_text(source_root),
        "generated_output_root": _path_text(output_root),
        "source_evidence": _source_evidence(),
        "source_verification": deepcopy(source_verification),
        "execution_activity_results": [
            {
                "activity_id": activity_id,
                "activity_status": "PLANNING_OUTPUT_PREPARATION_COMPLETED",
                "label_generation_performed": False,
                "research_only": True,
            }
            for activity_id in EXECUTION_ACTIVITY_IDS
        ],
        "approved_workstreams": list(WORKSTREAM_IDS),
        "label_family_candidate_matrix_summary": {
            "candidate_count": 10,
            "generation_status": NOT_GENERATED,
            "authorization_status": NOT_AUTHORIZED_FOR_LABEL_GENERATION,
        },
        "threshold_design_matrix_summary": {
            "strategy_count": 7,
            "status": DESIGN_ONLY_NOT_EXECUTED,
        },
        "horizon_design_matrix_summary": {
            "candidate_count": 5,
            "status": DESIGN_ONLY_NOT_EXECUTED,
        },
        "per_ticker_label_objective_plan_summary": {
            "plan_count": 12,
            "label_generation_performed": False,
        },
        "meta_limitation_preservation_summary": {
            "ticker": "META",
            "record_count": 913,
            "backfilled": False,
            "repaired": False,
            "synthetic_rows_created": False,
            "label_availability_limitation_carried_forward": True,
        },
        "output_digest_manifest_summary": {
            "filename": OUTPUT_FILENAMES[0],
            "entry_count": 8,
            "self_reference_policy": "SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE",
        },
        "output_digest_manifest": deepcopy(output_digest_manifest),
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
        "tracked_marketflow_files": [],
        "no_tracked_marketflow_files": True,
    }
    artifact["execution_checklist"] = _checklist(artifact)
    artifact["execution_summary"] = _execution_summary(
        artifact["execution_checklist"]
    )
    artifact["label_objective_redesign_execution_digest"] = (
        label_objective_redesign_execution_digest_v1(artifact)
    )
    artifact["execution_summary"]["label_objective_redesign_execution_digest"] = (
        artifact["label_objective_redesign_execution_digest"]
    )
    return artifact


def label_objective_redesign_execution_digest_v1(
    artifact: dict[str, Any],
) -> str:
    """Return a path-independent deterministic execution digest."""
    payload = deepcopy(artifact)
    payload.pop("label_objective_redesign_execution_digest", None)
    payload.pop("source_root", None)
    payload.pop("generated_output_root", None)
    if isinstance(payload.get("execution_summary"), dict):
        payload["execution_summary"].pop(
            "label_objective_redesign_execution_digest", None
        )
    return semantic_digest(payload)


def _write_bytes_once(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with path.open("xb") as handle:
            handle.write(payload)
    except FileExistsError as exc:
        raise LabelObjectiveRedesignExecutionError(
            f"label objective redesign execution output already exists: {path.name}"
        ) from exc


def execute_label_objective_redesign_v1(
    *,
    source_root: str | Path | None = None,
    output_root: str | Path | None = None,
    run_timestamp_utc: str | None = None,
) -> dict[str, Any]:
    """Generate eight sanitized planning outputs without generating labels."""
    source_path = DEFAULT_SOURCE_ROOT if source_root is None else Path(source_root)
    output_path = DEFAULT_OUTPUT_ROOT if output_root is None else Path(output_root)
    timestamp = run_timestamp_utc or _utc_now()
    source_verification, failures = _verify_source_root(source_path)
    if failures:
        return _blocked_artifact(
            source_root=source_path,
            output_root=output_path,
            run_timestamp_utc=timestamp,
            failures=failures,
        )
    if output_path.exists() and any(output_path.iterdir()):
        raise LabelObjectiveRedesignExecutionError(
            "label objective redesign execution output root is not empty"
        )

    reports = _build_reports(timestamp)
    report_bytes = {
        filename: canonical_json_bytes(report)
        for filename, report in reports.items()
    }
    report_digests = {
        filename: sha256_bytes(payload)
        for filename, payload in report_bytes.items()
    }
    output_digest_manifest = [
        (
            {
                "filename": filename,
                "digest_kind": "SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE",
                "sha256": None,
            }
            if filename == OUTPUT_FILENAMES[0]
            else {
                "filename": filename,
                "digest_kind": "FILE_SHA256",
                "sha256": report_digests[filename],
            }
        )
        for filename in OUTPUT_FILENAMES
    ]
    artifact = _build_executed_artifact(
        run_timestamp_utc=timestamp,
        source_root=source_path,
        output_root=output_path,
        source_verification=source_verification,
        output_digest_manifest=output_digest_manifest,
    )
    validate_label_objective_redesign_executed_v1(artifact)
    report_bytes[OUTPUT_FILENAMES[0]] = canonical_json_bytes(artifact)
    for filename in OUTPUT_FILENAMES:
        _write_bytes_once(output_path / filename, report_bytes[filename])
    return artifact


FORBIDDEN_ARTIFACT_VALUES = {
    "LABEL_GENERATION_EXECUTED",
    "REDESIGNED_LABEL_GENERATION_EXECUTED",
    "FEATURE_GENERATION_EXECUTED",
    "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_CANDIDATE",
    "PREDICTIVE_USEFULNESS_ACCEPTANCE_CANDIDATE",
    "PREDICTIVE_USEFULNESS_ACCEPTED",
    "PROFITABILITY_ACCEPTED",
    "RUNTIME_MIGRATION_APPROVED",
    "RUNTIME_MIGRATION_ACTIVE",
    "STRATEGY_RUNTIME_MIGRATION",
    "TRADE_RECOMMENDATIONS",
}


def _reject_forbidden_values(value: Any, *, path: str = "artifact") -> None:
    forbidden_true_fields = {
        "label_generation_performed",
        "redesigned_label_generation_authorized",
        "redesigned_label_generation_performed",
        "redesigned_feature_generation_authorized",
        "redesigned_feature_generation_performed",
        "redesigned_protocol_evaluation_authorized",
        "redesigned_protocol_evaluation_performed",
        "feature_generation_performed",
        "metric_recomputation_performed",
        "model_training_performed",
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
    }
    if isinstance(value, dict):
        for key, item in value.items():
            current = f"{path}.{key}"
            if isinstance(item, str) and item in FORBIDDEN_ARTIFACT_VALUES:
                raise LabelObjectiveRedesignExecutionError(
                    f"{current} must not emit {item}"
                )
            if key in forbidden_true_fields and item is True:
                raise LabelObjectiveRedesignExecutionError(
                    f"{current} must remain false"
                )
            if key in {
                "runtime_use",
                "strategy_use",
                "paper_trading",
                "broker_execution",
            } and item == "AUTHORIZED":
                raise LabelObjectiveRedesignExecutionError(
                    f"{current} must not be AUTHORIZED"
                )
            if key in {"predictive_usefulness", "profitability"} and item == "accepted":
                raise LabelObjectiveRedesignExecutionError(
                    f"{current} must not be accepted"
                )
            _reject_forbidden_values(item, path=current)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _reject_forbidden_values(item, path=f"{path}[{index}]")


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise LabelObjectiveRedesignExecutionError(f"{field} mismatch")


def validate_label_objective_redesign_executed_v1(
    artifact: dict,
) -> dict[str, Any]:
    """Validate planning execution and every closed downstream boundary."""
    if not isinstance(artifact, dict):
        raise LabelObjectiveRedesignExecutionError(
            "label objective redesign executed artifact must be a JSON object"
        )
    _reject_forbidden_values(artifact)
    _expect(
        artifact.get("artifact_kind"),
        ARTIFACT_KIND_LABEL_OBJECTIVE_REDESIGN_EXECUTED,
        "artifact_kind",
    )
    _expect(
        artifact.get("schema_version"),
        SCHEMA_VERSION_LABEL_OBJECTIVE_REDESIGN_EXECUTED_V1,
        "schema_version",
    )
    _expect(
        artifact.get("execution_status"),
        LABEL_OBJECTIVE_REDESIGN_EXECUTED_RESEARCH_ONLY,
        "execution_status",
    )
    _expect(artifact.get("source_evidence"), _source_evidence(), "source_evidence")
    for field in (
        "label_objective_redesign_execution_approved",
        "label_objective_redesign_authorized",
        "ready_for_label_objective_redesign_execution",
        "label_objective_redesign_executed",
        "label_objective_redesign_results_created",
        "label_objective_redesign_manifest_created",
        "label_family_candidate_matrix_created",
        "threshold_design_matrix_created",
        "horizon_design_matrix_created",
        "per_ticker_label_objective_plan_created",
        "label_availability_boundary_plan_created",
        "meta_limitation_preservation_plan_created",
        "operator_review_summary_template_created",
    ):
        _expect(artifact.get(field), True, field)
    for field in (
        "provider_requests_made_in_execution",
        "live_provider_transport_enabled_in_execution",
        "market_data_acquisition_performed_in_execution",
        "dataset_generation_performed_in_execution",
        "canonical_dataset_regenerated_in_execution",
        "predictive_evidence_rerun_performed",
        "refined_evidence_rerun_performed",
        "label_generation_performed",
        "redesigned_label_generation_authorized",
        "redesigned_label_generation_performed",
        "feature_generation_performed",
        "metric_recomputation_performed",
        "model_training_performed",
        "additional_predictive_evidence_execution_candidate_created",
        "new_strategy_scoring_performed",
        "trade_recommendations_generated",
    ):
        _expect(artifact.get(field), False, field)
    _expect(artifact.get("generated_output_count"), 8, "generated_output_count")
    _expect(artifact.get("generated_output_names"), OUTPUT_FILENAMES, "generated_output_names")
    _expect(artifact.get("target_universe"), TARGET_UNIVERSE, "target_universe")
    _expect(artifact.get("target_universe_count"), 12, "target_universe_count")
    _expect(artifact.get("total_canonical_record_count"), 11946, "total_canonical_record_count")
    _expect(artifact.get("records_digest"), EXPECTED_RECORDS_DIGEST, "records_digest")
    _expect(artifact.get("meta_record_count"), 913, "meta_record_count")
    _expect(artifact.get("non_meta_record_count"), 1003, "non_meta_record_count")
    _expect(artifact.get("per_ticker_record_counts"), EXPECTED_RECORD_COUNTS, "per_ticker_record_counts")
    _expect(artifact.get("candidate_label_family_count"), 10, "candidate_label_family_count")
    _expect(artifact.get("threshold_design_strategy_count"), 7, "threshold_design_strategy_count")
    _expect(artifact.get("horizon_design_candidate_count"), 5, "horizon_design_candidate_count")
    _expect(artifact.get("per_ticker_plan_count"), 12, "per_ticker_plan_count")
    _expect(artifact.get("predictive_usefulness"), NOT_ACCEPTED, "predictive_usefulness")
    _expect(artifact.get("profitability"), NOT_ACCEPTED, "profitability")
    for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
        _expect(artifact.get(field), NOT_AUTHORIZED, field)
    expected_checklist = _checklist(artifact)
    _expect(artifact.get("execution_checklist"), expected_checklist, "execution_checklist")
    if any(row["status"] != "PASS" for row in expected_checklist):
        raise LabelObjectiveRedesignExecutionError(
            "execution_checklist contains a failed check"
        )
    expected_summary = _execution_summary(expected_checklist)
    digest = artifact.get("label_objective_redesign_execution_digest")
    expected_summary["label_objective_redesign_execution_digest"] = digest
    _expect(artifact.get("execution_summary"), expected_summary, "execution_summary")
    if not isinstance(digest, str) or len(digest) != 64:
        raise LabelObjectiveRedesignExecutionError(
            "label_objective_redesign_execution_digest missing"
        )
    _expect(
        digest,
        label_objective_redesign_execution_digest_v1(artifact),
        "label_objective_redesign_execution_digest",
    )
    return {
        "status": LABEL_OBJECTIVE_REDESIGN_EXECUTION_VALID,
        "artifact_kind": artifact["artifact_kind"],
        "execution_status": artifact["execution_status"],
        "label_objective_redesign_execution_digest": digest,
        "generated_output_count": 8,
        "failure_count": 0,
        "warning_count": 1,
        "label_objective_redesign_executed": True,
        "label_generation_performed": False,
        "additional_predictive_evidence_execution_candidate_created": False,
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "runtime_migration_authorized": False,
    }


def build_label_objective_redesign_execution_status_markdown_v1(
    artifact: dict,
) -> str:
    """Render a sanitized status summary for planning-output execution."""
    validation = validate_label_objective_redesign_executed_v1(artifact)
    summary = artifact["execution_summary"]
    lines = [
        "# MarketFlow Label Objective Redesign Execution Status",
        "",
        "## Title",
        "- Label Objective Redesign Execution v1.",
        "",
        "## Label Objective Redesign Execution",
        f"- Artifact/status: `{artifact['artifact_kind']}` / `{artifact['execution_status']}`.",
        f"- Execution digest: `{validation['label_objective_redesign_execution_digest']}`.",
        "",
        "## Source Execution Approval",
        f"- Approval digest: `{artifact['source_evidence']['label_objective_redesign_execution_approval_digest']}`.",
        "",
        "## Dataset and Universe",
        f"- Records/digest: `{artifact['total_canonical_record_count']}` / `{artifact['records_digest']}`.",
        f"- Universe: `{', '.join(artifact['target_universe'])}`; META remains `{artifact['meta_record_count']}`.",
        "",
        "## Generated Planning Outputs",
        f"- `{artifact['generated_output_count']}` outputs under `{artifact['generated_output_root']}`.",
        "",
        "## Label Family Candidate Matrix",
        f"- `{artifact['candidate_label_family_count']}` design-only candidates; labels remain not generated.",
        "",
        "## Threshold Design Matrix",
        f"- `{artifact['threshold_design_strategy_count']}` design strategies; no final threshold computed.",
        "",
        "## Horizon Design Matrix",
        f"- `{artifact['horizon_design_candidate_count']}` horizon candidates; none selected or executed.",
        "",
        "## Per-Ticker Label Objective Plan",
        f"- `{artifact['per_ticker_plan_count']}` plans; label generation remains false.",
        "",
        "## META Limitation Preservation Plan",
        "- META remains at `913` records; no backfill, repair, or synthetic rows.",
        "",
        "## Output Digest Manifest",
        f"- `{artifact['output_digest_manifest_summary']['entry_count']}` entries with self-reference explicitly non-applicable.",
        "",
        "## Execution Boundary",
        "- Planning outputs were created; actual redesigned labels, features, metrics, models, and strategy scoring were not generated or run.",
        "",
        "## Predictive Usefulness Boundary",
        f"- `{artifact['predictive_usefulness']}`; no acceptance candidate was created.",
        "",
        "## Profitability Boundary",
        f"- `{artifact['profitability']}`.",
        "",
        "## Runtime Boundary",
        f"- Runtime/strategy/paper/broker: `{artifact['runtime_use']}` / `{artifact['strategy_use']}` / `{artifact['paper_trading']}` / `{artifact['broker_execution']}`.",
        "",
        "## Checklist Summary",
        f"- `{summary['passed_checks']} / {summary['total_checks']}` passed; `{summary['blocker_count']}` blockers.",
        "",
        "## Guardrails",
        "- Research-only, non-actionable planning execution. No provider, data acquisition, label generation, predictive acceptance, profitability acceptance, runtime activation, trading, or recommendations.",
    ]
    return "\n".join(lines)
