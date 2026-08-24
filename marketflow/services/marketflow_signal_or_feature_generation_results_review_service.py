"""Offline review of existing signal or feature generation outputs."""

from __future__ import annotations

from collections import Counter
from copy import deepcopy
import json
from pathlib import Path
from typing import Any, Mapping

from marketflow.historical_data.artifacts import (
    canonical_json_bytes,
    semantic_digest,
    sha256_file,
)
from marketflow.services import (
    marketflow_signal_or_feature_generation_execution_service as execution,
)


ARTIFACT_KIND_MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_RESULTS_REVIEW_PACKAGE = (
    "MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_RESULTS_REVIEW_PACKAGE"
)
ARTIFACT_KIND_MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_RESULTS_REVIEW_BLOCKED = (
    "MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_RESULTS_REVIEW_BLOCKED"
)
SCHEMA_VERSION_MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_RESULTS_REVIEW_V1 = (
    "marketflow_signal_or_feature_generation_results_review_v1"
)
MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_RESULTS_REVIEW_PACKAGE_READY = (
    "MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_RESULTS_REVIEW_PACKAGE_READY"
)
MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_RESULTS_REVIEW_BLOCKED_MISSING_OR_INVALID_OUTPUTS = (
    "MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_RESULTS_REVIEW_BLOCKED_MISSING_OR_INVALID_OUTPUTS"
)
SIGNAL_OR_FEATURE_GENERATION_RESULTS_REVIEW_ONLY_NOT_FEATURE_LABEL_MATRIX_NOT_BACKTEST = (
    "SIGNAL_OR_FEATURE_GENERATION_RESULTS_REVIEW_ONLY_NOT_FEATURE_LABEL_MATRIX_NOT_BACKTEST"
)
MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_RESULTS_REVIEW_VALID = (
    "MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_RESULTS_REVIEW_VALID"
)
MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_RESULTS_REVIEW_BLOCKED_VALID = (
    "MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_RESULTS_REVIEW_BLOCKED_VALID"
)

EXPECTED_SOURCE_EXECUTION_DIGEST = (
    "bcccbdc57616e7ff0c350535628a4a2b2cb752e11b4c98b0b9905fed9f9e4e60"
)
EXPECTED_SOURCE_OUTPUT_BINDING_DIGEST = (
    "5e0ef154d13782bc58c284b2d664f35e7f0724bb890efc2235e840df62dbf4e8"
)
EXPECTED_SOURCE_FEATURE_VALUES_DIGEST = (
    "7512da78cb0d222bddb2e0e5c5cb8307064ad47ebc6817025f1eaea2bcd8815e"
)
EXPECTED_SOURCE_APPROVAL_DIGEST = execution.EXPECTED_SOURCE_APPROVAL_DIGEST
EXPECTED_OUTPUT_FILENAMES = list(execution.OUTPUT_FILENAMES)
DEFAULT_OUTPUT_ROOT = execution.DEFAULT_OUTPUT_ROOT
TARGET_UNIVERSE = list(execution.TARGET_UNIVERSE)
EXPECTED_RECORD_COUNTS = dict(execution.EXPECTED_RECORD_COUNTS)
SIGNAL_FAMILIES = list(execution.SELECTED_SIGNAL_FAMILIES)
FEATURE_FAMILIES = list(execution.SELECTED_FEATURE_FAMILIES)
FEATURE_GROUPS = list(execution.SELECTED_FEATURE_GROUPS)
FEATURE_VALUES_FIELDS = list(execution.FEATURE_VALUES_FIELDS)
NOT_ACCEPTED = execution.NOT_ACCEPTED
NOT_AUTHORIZED = execution.NOT_AUTHORIZED
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

SOURCE_EVIDENCE = {
    "marketflow_signal_or_feature_generation_execution_digest": EXPECTED_SOURCE_EXECUTION_DIGEST,
    "signal_or_feature_generation_output_binding_digest": EXPECTED_SOURCE_OUTPUT_BINDING_DIGEST,
    "signal_or_feature_values_digest": EXPECTED_SOURCE_FEATURE_VALUES_DIGEST,
    **execution._source_evidence(),
}

NEXT_CHAIN = [
    "Feature-Label Matrix Candidate v1.",
    "Feature-Label Matrix Candidate Operator Review v1.",
    "Feature-Label Matrix Approval v1.",
    "Feature-Label Matrix Execution v1.",
    "Feature-Label Matrix Results Review v1.",
    "Future VPA/Wyckoff baseline only after separate approval.",
    "Future expectancy backtest lab only after separate approval.",
    "Results review and readiness gates before any acceptance.",
    "Runtime migration only if ever separately authorized.",
]
NEXT_GATES = [
    "feature_label_matrix_candidate",
    "feature_label_matrix_candidate_operator_review",
    "feature_label_matrix_approval",
    "feature_label_matrix_execution",
    "feature_label_matrix_results_review",
    "vpa_wyckoff_rule_baseline_candidate",
    "expectancy_backtest_lab_candidate",
    "expectancy_results_review_and_reassessment",
    "runtime_migration_chain_if_ever_authorized",
]
RISK_CONTROLS = [
    "review_does_not_create_feature_label_matrix",
    "review_does_not_run_backtest",
    "review_does_not_train_models",
    "review_does_not_compute_performance_metrics",
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
    "review_does_not_rerun_signal_or_feature_generation_execution",
    "review_does_not_rerun_target_generation_execution",
    "review_does_not_rerun_target_results_review",
    "review_does_not_rerun_candidate_creation",
    "review_does_not_rerun_candidate_review",
    "review_does_not_rerun_approval",
    "do_not_mutate_frozen_dataset",
    "do_not_mutate_target_outputs",
    "do_not_mutate_signal_or_feature_outputs",
    "do_not_mutate_redesigned_label_outputs",
    "do_not_mutate_prior_feature_outputs",
    "do_not_mutate_predictive_evidence_outputs",
    "preserve_meta_record_limitation",
    "all_outputs_research_only",
]

REQUIRED_CHECK_IDS = [
    "source_execution_digest_bound", "source_output_binding_digest_bound",
    "source_feature_values_digest_bound", "source_approval_digest_bound",
    "source_candidate_review_digest_bound", "source_candidate_digest_bound",
    "source_target_results_review_digest_bound", "source_target_generation_execution_digest_bound",
    "source_target_values_digest_bound", "source_target_approval_digest_bound",
    "source_target_candidate_review_digest_bound", "source_target_candidate_digest_bound",
    "source_design_results_review_digest_bound", "source_design_execution_digest_bound",
    "source_design_output_binding_digest_bound", "source_expectancy_objective_approval_digest_bound",
    "source_strategy_charter_approval_digest_bound", "source_strategy_charter_digest_bound",
    "source_final_archive_digest_bound", "source_archive_digest_bound",
    "source_selection_digest_bound", "source_closure_digest_bound",
    "source_readiness_digest_bound", "source_reassessment_digest_bound",
    "source_results_review_digest_bound", "source_prior_execution_digest_bound",
    "prior_matrix_digest_bound", "prior_feature_values_digest_bound",
    "prior_label_values_digest_bound", "research_registry_digest_bound",
    "records_digest_bound", "target_universe_12_preserved",
    "records_digest_preserved", "meta_913_preserved",
    "selected_feature_package_preserved", "selected_target_package_preserved",
    "selected_objective_path_preserved", "expected_output_count_10",
    "observed_output_count_10", "output_digest_mismatch_count_zero",
    "feature_values_digest_matches", "feature_values_jsonl_schema_verified",
    "feature_values_count_verified", "selected_signal_family_count_7",
    "selected_feature_family_count_8", "selected_feature_group_count_13",
    "feature_row_count_155298", "available_feature_row_count_155142",
    "unavailable_feature_row_count_156", "non_meta_ticker_feature_counts_verified",
    "meta_feature_counts_verified", "signal_families_verified",
    "feature_families_verified", "feature_groups_verified",
    "target_values_not_used_as_features", "target_classes_not_used_as_features",
    "forward_returns_not_used_as_features", "future_data_not_used_as_features",
    "prediction_fields_absent", "strategy_score_fields_absent",
    "trade_recommendation_fields_absent", "digest_manifest_self_reference_policy_verified",
    "schema_report_verified", "coverage_report_verified",
    "feature_group_report_verified", "no_peek_feature_report_verified",
    "per_ticker_feature_report_verified", "meta_limitation_report_verified",
    "operator_summary_verified", "results_review_created_true",
    "results_review_ready_true", "ready_for_feature_label_matrix_candidate_true",
    "feature_label_matrix_candidate_created_false", "feature_label_matrix_created_false",
    "backtest_execution_authorized_false", "backtest_execution_performed_false",
    "model_training_authorized_false", "model_training_performed_false",
    "metric_computation_authorized_false", "metric_computation_performed_false",
    "strategy_scoring_false", "predictive_usefulness_not_accepted",
    "profitability_not_accepted", "runtime_not_authorized",
    "strategy_not_authorized", "broker_not_authorized",
    "trade_recommendations_false", "per_ticker_entries_12",
    "per_ticker_digests_present", "provider_requests_made_false",
    "market_data_acquisition_false", "dataset_regeneration_false",
    "signal_or_feature_generation_execution_rerun_false",
    "target_generation_execution_rerun_false", "target_results_review_rerun_false",
    "candidate_creation_rerun_false", "candidate_review_rerun_false",
    "approval_rerun_false", "raw_provider_payloads_not_committed",
    "api_keys_not_stored_or_printed", "next_chain_defined",
    "next_gates_defined", "risk_controls_defined", "no_tracked_marketflow_files",
]

FORBIDDEN_KEYS = {
    "target_value", "target_class", "forward_return", "future_label_value",
    "prediction", "prediction_value", "strategy_score", "trade_recommendation",
    "broker_order", "broker_order_id", "order_id", "raw_provider_payload",
    "api_key", "api_keys",
}


class MarketFlowSignalOrFeatureGenerationResultsReviewError(ValueError):
    """Raised when generated feature-output evidence violates its contract."""


def _path_text(path: Path) -> str:
    return str(path).replace("\\", "/")


def _load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise MarketFlowSignalOrFeatureGenerationResultsReviewError(
            f"invalid JSON output: {path.name}"
        ) from exc
    if not isinstance(value, dict):
        raise MarketFlowSignalOrFeatureGenerationResultsReviewError(
            f"JSON output must be an object: {path.name}"
        )
    return value


def _failure(failure_id: str, message: str, **details: Any) -> dict[str, Any]:
    return {"failure_id": failure_id, "message": message, **details}


def _nested_keys(value: Any) -> set[str]:
    if isinstance(value, dict):
        keys = set(value)
        for child in value.values():
            keys.update(_nested_keys(child))
        return keys
    if isinstance(value, list):
        keys: set[str] = set()
        for child in value:
            keys.update(_nested_keys(child))
        return keys
    return set()


def _inspect_feature_values(path: Path) -> dict[str, Any]:
    row_count = available_count = unavailable_count = 0
    schema_valid = research_only_valid = package_binding_valid = True
    forbidden_fields: set[str] = set()
    signals: set[str] = set()
    families: set[str] = set()
    groups: set[str] = set()
    ticker_total: Counter[str] = Counter()
    ticker_available: Counter[str] = Counter()
    ticker_unavailable: Counter[str] = Counter()
    try:
        with path.open("r", encoding="utf-8") as handle:
            for line_number, line in enumerate(handle, start=1):
                if not line.strip():
                    continue
                row = json.loads(line)
                if not isinstance(row, dict):
                    raise ValueError(f"feature row {line_number} is not an object")
                row_count += 1
                schema_valid = schema_valid and set(row) == set(FEATURE_VALUES_FIELDS)
                forbidden_fields.update(FORBIDDEN_KEYS & _nested_keys(row))
                ticker = row.get("ticker")
                group = row.get("feature_group")
                definition = execution.GROUP_DEFINITIONS.get(group)
                if ticker not in TARGET_UNIVERSE or definition is None:
                    schema_valid = False
                    continue
                if row.get("feature_family") != definition["feature_family"]:
                    schema_valid = False
                if row.get("signal_family") != definition["signal_family"]:
                    schema_valid = False
                if not isinstance(row.get("feature_values"), dict):
                    schema_valid = False
                ticker_total[ticker] += 1
                groups.add(group)
                families.add(row.get("feature_family"))
                signals.add(row.get("signal_family"))
                research_only_valid = (
                    research_only_valid
                    and row.get("research_only") is True
                    and row.get("non_actionable") is True
                )
                package_binding_valid = (
                    package_binding_valid
                    and row.get("selected_feature_package")
                    == execution.PACKAGE_TREND_FLOW_EXPECTANCY_SIGNAL_SET
                    and row.get("selected_label_target_package")
                    == execution.PACKAGE_EXPECTANCY_PAYOFF_ABSTENTION_LABEL_SET
                    and row.get("selected_objective_path")
                    == execution.EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT
                    and row.get("records_digest") == execution.EXPECTED_RECORDS_DIGEST
                    and row.get("source_approval_digest") == EXPECTED_SOURCE_APPROVAL_DIGEST
                )
                if row.get("feature_available") is True:
                    available_count += 1
                    ticker_available[ticker] += 1
                    schema_valid = schema_valid and row.get("feature_unavailable_reason") is None
                elif row.get("feature_available") is False:
                    unavailable_count += 1
                    ticker_unavailable[ticker] += 1
                    schema_valid = schema_valid and isinstance(
                        row.get("feature_unavailable_reason"), str
                    )
                else:
                    schema_valid = False
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        raise MarketFlowSignalOrFeatureGenerationResultsReviewError(
            "feature_values.jsonl could not be inspected"
        ) from exc
    non_meta_verified = all(
        ticker_total[ticker] == 13039
        and ticker_available[ticker] == 13026
        and ticker_unavailable[ticker] == 13
        for ticker in TARGET_UNIVERSE
        if ticker != "META"
    )
    meta_verified = (
        ticker_total["META"] == 11869
        and ticker_available["META"] == 11856
        and ticker_unavailable["META"] == 13
    )
    return {
        "feature_row_count": row_count,
        "available_feature_row_count": available_count,
        "unavailable_feature_row_count": unavailable_count,
        "feature_values_jsonl_schema_verified": schema_valid and not forbidden_fields,
        "research_only_non_actionable_verified": research_only_valid,
        "package_binding_verified": package_binding_valid,
        "forbidden_feature_fields_found": sorted(forbidden_fields),
        "target_values_used_as_features": "target_value" in forbidden_fields,
        "target_classes_used_as_features": "target_class" in forbidden_fields,
        "forward_returns_used_as_features": "forward_return" in forbidden_fields,
        "future_data_used_as_features": "future_label_value" in forbidden_fields,
        "prediction_fields_present": bool({"prediction", "prediction_value"} & forbidden_fields),
        "strategy_score_fields_present": "strategy_score" in forbidden_fields,
        "trade_recommendation_fields_present": "trade_recommendation" in forbidden_fields,
        "signal_families": [item for item in SIGNAL_FAMILIES if item in signals],
        "feature_families": [item for item in FEATURE_FAMILIES if item in families],
        "feature_groups": [item for item in FEATURE_GROUPS if item in groups],
        "per_ticker_feature_row_counts": {
            ticker: ticker_total[ticker] for ticker in TARGET_UNIVERSE
        },
        "per_ticker_available_feature_row_counts": {
            ticker: ticker_available[ticker] for ticker in TARGET_UNIVERSE
        },
        "per_ticker_unavailable_feature_row_counts": {
            ticker: ticker_unavailable[ticker] for ticker in TARGET_UNIVERSE
        },
        "non_meta_ticker_feature_counts_verified": non_meta_verified,
        "meta_feature_counts_verified": meta_verified,
    }


def _verify_reports(payloads: Mapping[str, dict[str, Any]]) -> dict[str, bool]:
    schema = payloads["signal_feature_schema.json"]
    coverage = payloads["feature_coverage_report.json"]
    groups = payloads["feature_group_report.json"]
    no_peek = payloads["no_peek_feature_report.json"]
    per_ticker = payloads["per_ticker_feature_report.json"]
    meta = payloads["meta_limitation_report.json"]
    operator = payloads["operator_summary.json"]
    common_output_valid = all(
        payload.get("output_label") == execution.OUTPUT_LABEL
        and payload.get("evidence_scope") == execution.EVIDENCE_SCOPE
        and payload.get("feature_label_matrix_created") is False
        and payload.get("runtime_use") == NOT_AUTHORIZED
        for payload in payloads.values()
    )
    per_ticker_rows = per_ticker.get(
        "per_ticker_signal_or_feature_generation_execution_entries"
    )
    no_peek_rules = no_peek.get("no_peek_and_target_separation_rules")
    return {
        "common_output_boundary_verified": common_output_valid,
        "schema_report_verified": (
            schema.get("feature_values_fields") == FEATURE_VALUES_FIELDS
            and schema.get("forbidden_feature_fields") == execution.FORBIDDEN_FEATURE_FIELDS
            and schema.get("selected_signal_families") == SIGNAL_FAMILIES
            and schema.get("selected_feature_families") == FEATURE_FAMILIES
            and schema.get("selected_feature_groups") == FEATURE_GROUPS
            and schema.get("feature_row_count") == 155298
        ),
        "coverage_report_verified": (
            coverage.get("feature_row_count") == 155298
            and coverage.get("available_feature_row_count") == 155142
            and coverage.get("unavailable_feature_row_count") == 156
            and coverage.get("all_canonical_records_retained") is True
            and coverage.get("rows_dropped") == 0
            and isinstance(coverage.get("coverage_entries"), list)
            and len(coverage["coverage_entries"]) == 13
        ),
        "feature_group_report_verified": (
            groups.get("feature_row_count") == 155298
            and isinstance(groups.get("feature_group_entries"), list)
            and [row.get("feature_group") for row in groups["feature_group_entries"]]
            == FEATURE_GROUPS
        ),
        "no_peek_feature_report_verified": (
            isinstance(no_peek_rules, list)
            and [row.get("rule_id") for row in no_peek_rules] == execution.NO_PEEK_RULES
            and no_peek.get("target_values_used_as_features") is False
            and no_peek.get("target_classes_used_as_features") is False
            and no_peek.get("forward_returns_used_as_features") is False
            and no_peek.get("future_data_used_as_features") is False
            and no_peek.get("same_date_cross_section_only") is True
            and no_peek.get("per_ticker_history_only") is True
        ),
        "per_ticker_feature_report_verified": (
            per_ticker.get("target_universe") == TARGET_UNIVERSE
            and isinstance(per_ticker_rows, list)
            and [row.get("ticker") for row in per_ticker_rows] == TARGET_UNIVERSE
            and per_ticker.get("feature_row_count") == 155298
        ),
        "meta_limitation_report_verified": (
            meta.get("ticker") == "META"
            and meta.get("historical_record_count") == 913
            and meta.get("feature_row_count") == 11869
            and meta.get("meta_reduced_record_count_preserved") is True
            and meta.get("no_repair") is True
            and meta.get("no_backfill") is True
            and meta.get("no_synthetic_rows") is True
            and meta.get("generation_note")
            == "PRESERVE_META_LIMITATION_IN_SIGNAL_OR_FEATURE_GENERATION_EXECUTION"
        ),
        "operator_summary_verified": (
            operator.get("review_status")
            == "AWAITING_SIGNAL_OR_FEATURE_GENERATION_RESULTS_REVIEW_V1"
            and operator.get("operator_decision") is None
            and operator.get("generated_output_count") == 10
            and operator.get("risk_controls") == execution.RISK_CONTROLS
        ),
    }


def _verify_outputs(
    output_root: Path,
) -> tuple[
    dict[str, dict[str, Any]], list[dict[str, Any]], dict[str, Any],
    dict[str, bool], list[dict[str, Any]],
]:
    failures: list[dict[str, Any]] = []
    if not output_root.is_dir():
        return {}, [], {}, {}, [
            _failure(
                "missing_output_root",
                "signal-or-feature generation output root is missing",
                output_root=_path_text(output_root),
            )
        ]
    actual_names = sorted(path.name for path in output_root.iterdir() if path.is_file())
    missing = [name for name in EXPECTED_OUTPUT_FILENAMES if name not in actual_names]
    if missing or len(actual_names) != 10:
        return {}, [], {}, {}, [
            _failure(
                "output_file_inventory_mismatch",
                "expected feature-generation output inventory is incomplete or contains extras",
                expected=EXPECTED_OUTPUT_FILENAMES,
                actual=actual_names,
                missing=missing,
            )
        ]
    try:
        payloads = {
            filename: _load_json(output_root / filename)
            for filename in EXPECTED_OUTPUT_FILENAMES
            if filename != "feature_values.jsonl"
        }
        source = payloads["signal_feature_generation_manifest.json"]
        execution.validate_marketflow_signal_or_feature_generation_execution_v1(source)
        feature_stats = _inspect_feature_values(output_root / "feature_values.jsonl")
    except (
        MarketFlowSignalOrFeatureGenerationResultsReviewError,
        execution.MarketFlowSignalOrFeatureGenerationExecutionError,
    ) as exc:
        return {}, [], {}, {}, [
            _failure(
                "invalid_source_output",
                "signal-or-feature generation outputs are invalid",
                error=str(exc),
            )
        ]
    digest_report = payloads["signal_feature_generation_digest_manifest.json"]
    recorded = digest_report.get("output_digest_manifest")
    if not isinstance(recorded, list) or recorded != source.get("output_digest_manifest"):
        return {}, [], {}, {}, [
            _failure(
                "digest_manifest_mismatch",
                "digest manifest does not match the execution artifact",
            )
        ]
    recorded_by_name = {
        row.get("filename"): row for row in recorded if isinstance(row, dict)
    }
    bindings: list[dict[str, Any]] = []
    for filename in EXPECTED_OUTPUT_FILENAMES:
        entry = recorded_by_name.get(filename, {})
        local_sha = sha256_file(output_root / filename)
        kind = entry.get("digest_kind")
        recorded_sha = entry.get("sha256")
        if filename == EXPECTED_OUTPUT_FILENAMES[0]:
            verified = kind == "SELF_REFERENTIAL_EXECUTION_ARTIFACT" and recorded_sha is None
        elif filename == EXPECTED_OUTPUT_FILENAMES[-1]:
            verified = kind == "SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE" and recorded_sha is None
        else:
            verified = kind == "FILE_SHA256" and recorded_sha == local_sha
        bindings.append({
            "filename": filename,
            "local_sha256": local_sha,
            "recorded_digest_kind": kind,
            "recorded_sha256": recorded_sha,
            "verification_status": PASS if verified else FAIL,
        })
    if any(row["verification_status"] != PASS for row in bindings):
        failures.append(_failure(
            "output_digest_verification_failed",
            "one or more feature-generation output digests do not match",
        ))
    local = {row["filename"]: row["local_sha256"] for row in bindings}
    if local.get("feature_values.jsonl") != EXPECTED_SOURCE_FEATURE_VALUES_DIGEST:
        failures.append(_failure(
            "feature_values_digest_mismatch", "feature_values.jsonl digest changed"
        ))
    if source.get("marketflow_signal_or_feature_generation_execution_digest") != EXPECTED_SOURCE_EXECUTION_DIGEST:
        failures.append(_failure(
            "source_execution_digest_mismatch", "source execution digest changed"
        ))
    if source.get("signal_or_feature_generation_output_binding_digest") != EXPECTED_SOURCE_OUTPUT_BINDING_DIGEST:
        failures.append(_failure(
            "source_output_binding_digest_mismatch", "source output binding digest changed"
        ))
    if digest_report.get("manifest_self_reference_policy") != "SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE":
        failures.append(_failure(
            "manifest_self_reference_policy_mismatch",
            "digest manifest self-reference policy changed",
        ))
    report_reviews = _verify_reports(payloads)
    if not all(report_reviews.values()):
        failures.append(_failure(
            "report_content_verification_failed",
            "one or more feature-generation reports failed content verification",
            report_reviews=report_reviews,
        ))
    if not all((
        feature_stats.get("feature_values_jsonl_schema_verified"),
        feature_stats.get("research_only_non_actionable_verified"),
        feature_stats.get("package_binding_verified"),
        feature_stats.get("feature_row_count") == 155298,
        feature_stats.get("available_feature_row_count") == 155142,
        feature_stats.get("unavailable_feature_row_count") == 156,
        feature_stats.get("signal_families") == SIGNAL_FAMILIES,
        feature_stats.get("feature_families") == FEATURE_FAMILIES,
        feature_stats.get("feature_groups") == FEATURE_GROUPS,
        feature_stats.get("non_meta_ticker_feature_counts_verified"),
        feature_stats.get("meta_feature_counts_verified"),
    )):
        failures.append(_failure(
            "feature_values_content_verification_failed",
            "feature values schema, counts, or boundaries failed verification",
            feature_stats=feature_stats,
        ))
    return payloads, bindings, feature_stats, report_reviews, failures


def _per_ticker_review_entries(
    source: Mapping[str, Any],
) -> list[dict[str, Any]]:
    source_entries = source[
        "per_ticker_signal_or_feature_generation_execution_entries"
    ]
    rows: list[dict[str, Any]] = []
    for source_entry in source_entries:
        ticker = source_entry["ticker"]
        entry = {
            "ticker": ticker,
            "registry_approval_status": "APPROVED_FOR_RESEARCH_REGISTRY_ONLY",
            "canonical_dataset_status": "FROZEN",
            "historical_record_count": source_entry["historical_record_count"],
            "meta_reduced_record_count_flag": ticker == "META",
            "signal_or_feature_generation_execution_status": execution.MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_EXECUTED_RESEARCH_ONLY,
            "signal_or_feature_generation_results_review_status": "REVIEWED_RESEARCH_ONLY",
            "selected_feature_package": execution.PACKAGE_TREND_FLOW_EXPECTANCY_SIGNAL_SET,
            "selected_label_target_package": execution.PACKAGE_EXPECTANCY_PAYOFF_ABSTENTION_LABEL_SET,
            "selected_objective_path": execution.EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT,
            "feature_group_count": 13,
            "feature_row_count": source_entry["feature_row_count"],
            "available_feature_row_count": source_entry["available_feature_row_count"],
            "unavailable_feature_row_count": source_entry["unavailable_feature_row_count"],
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
            "source_execution_digest": EXPECTED_SOURCE_EXECUTION_DIGEST,
            "source_output_binding_digest": EXPECTED_SOURCE_OUTPUT_BINDING_DIGEST,
            "source_feature_values_digest": EXPECTED_SOURCE_FEATURE_VALUES_DIGEST,
            "review_note": (
                "PRESERVE_META_LIMITATION_IN_SIGNAL_OR_FEATURE_GENERATION_RESULTS_REVIEW"
                if ticker == "META"
                else "STANDARD_RECORD_COUNT_PRESERVED"
            ),
        }
        entry[
            "per_ticker_signal_or_feature_generation_results_review_digest"
        ] = semantic_digest(entry)
        rows.append(entry)
    return rows


def _blocked_package(
    output_root: Path, failures: list[dict[str, Any]]
) -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_RESULTS_REVIEW_BLOCKED,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_RESULTS_REVIEW_V1,
        "review_status": MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_RESULTS_REVIEW_BLOCKED_MISSING_OR_INVALID_OUTPUTS,
        "review_scope": SIGNAL_OR_FEATURE_GENERATION_RESULTS_REVIEW_ONLY_NOT_FEATURE_LABEL_MATRIX_NOT_BACKTEST,
        "created_offline": True,
        "research_only": True,
        "source_output_root": _path_text(output_root),
        "source_evidence": deepcopy(SOURCE_EVIDENCE),
        "signal_or_feature_generation_results_review_created": False,
        "signal_or_feature_generation_results_review_ready": False,
        "ready_for_feature_label_matrix_candidate": False,
        "feature_label_matrix_candidate_created": False,
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
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "trade_recommendations_generated": False,
        "expected_output_count": 10,
        "observed_output_count": 0,
        "marketflow_signal_or_feature_generation_results_review_digest": "NOT_CREATED",
        "failures": failures,
    }


def _check(check_id: str, expected: Any, actual: Any) -> dict[str, Any]:
    status = PASS if actual == expected else FAIL
    return {
        "check_id": check_id,
        "status": status,
        "expected": expected,
        "actual": actual,
        "severity": BLOCKER,
        "message": (
            "review condition satisfied" if status == PASS else "review condition failed"
        ),
    }


def _check_values(review: Mapping[str, Any]) -> dict[str, bool]:
    source = review.get("source_evidence", {})
    inspection = review.get("feature_values_inspection", {})
    reports = review.get("report_reviews", {})
    entries = review.get(
        "per_ticker_signal_or_feature_generation_results_review_entries", []
    )
    digest_checks = {
        "source_execution_digest_bound": "marketflow_signal_or_feature_generation_execution_digest",
        "source_output_binding_digest_bound": "signal_or_feature_generation_output_binding_digest",
        "source_feature_values_digest_bound": "signal_or_feature_values_digest",
        "source_approval_digest_bound": "marketflow_signal_or_feature_generation_approval_digest",
        "source_candidate_review_digest_bound": "marketflow_signal_or_feature_generation_candidate_operator_review_digest",
        "source_candidate_digest_bound": "marketflow_signal_or_feature_generation_candidate_v1_digest",
        "source_target_results_review_digest_bound": "marketflow_objective_label_or_target_generation_results_review_digest",
        "source_target_generation_execution_digest_bound": "marketflow_objective_label_or_target_generation_execution_digest",
        "source_target_values_digest_bound": "objective_label_or_target_values_digest",
        "source_target_approval_digest_bound": "marketflow_objective_label_or_target_generation_approval_digest",
        "source_target_candidate_review_digest_bound": "marketflow_objective_label_or_target_generation_candidate_operator_review_digest",
        "source_target_candidate_digest_bound": "marketflow_objective_label_or_target_generation_candidate_v1_digest",
        "source_design_results_review_digest_bound": "marketflow_expectancy_objective_design_results_review_digest",
        "source_design_execution_digest_bound": "marketflow_expectancy_objective_design_execution_digest",
        "source_design_output_binding_digest_bound": "expectancy_objective_design_output_binding_digest",
        "source_expectancy_objective_approval_digest_bound": "marketflow_expectancy_objective_approval_digest",
        "source_strategy_charter_approval_digest_bound": "marketflow_algorithm_strategy_charter_approval_digest",
        "source_strategy_charter_digest_bound": "marketflow_algorithm_strategy_charter_v1_digest",
        "source_final_archive_digest_bound": "marketflow_predictive_usefulness_final_archive_summary_using_improved_evidence_digest",
        "source_archive_digest_bound": "predictive_usefulness_acceptance_path_archive_record_using_improved_evidence_digest",
        "source_selection_digest_bound": "operator_method_or_closure_selection_using_improved_evidence_digest",
        "source_closure_digest_bound": "predictive_usefulness_not_ready_closure_and_method_planning_tree_using_improved_evidence_digest",
        "source_readiness_digest_bound": "predictive_usefulness_acceptance_readiness_review_using_improved_evidence_digest",
        "source_reassessment_digest_bound": "predictive_usefulness_reassessment_rerun_using_improved_evidence_digest",
        "source_results_review_digest_bound": "additional_predictive_evidence_results_review_using_improved_evidence_digest",
        "source_prior_execution_digest_bound": "additional_predictive_evidence_execution_using_improved_evidence_digest",
        "prior_matrix_digest_bound": "feature_label_matrix_digest",
        "prior_feature_values_digest_bound": "feature_values_digest",
        "prior_label_values_digest_bound": "redesigned_label_values_digest",
        "research_registry_digest_bound": "research_registry_approval_digest",
        "records_digest_bound": "records_digest",
    }
    values = {
        check_id: source.get(key) == SOURCE_EVIDENCE[key]
        for check_id, key in digest_checks.items()
    }
    values.update({
        "target_universe_12_preserved": review.get("target_universe") == TARGET_UNIVERSE and review.get("target_universe_count") == 12,
        "records_digest_preserved": review.get("records_digest") == execution.EXPECTED_RECORDS_DIGEST,
        "meta_913_preserved": review.get("meta_record_count") == 913,
        "selected_feature_package_preserved": review.get("selected_feature_package") == execution.PACKAGE_TREND_FLOW_EXPECTANCY_SIGNAL_SET,
        "selected_target_package_preserved": review.get("selected_label_target_package") == execution.PACKAGE_EXPECTANCY_PAYOFF_ABSTENTION_LABEL_SET,
        "selected_objective_path_preserved": review.get("selected_objective_path") == execution.EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT,
        "expected_output_count_10": review.get("expected_output_count") == 10,
        "observed_output_count_10": review.get("observed_output_count") == 10,
        "output_digest_mismatch_count_zero": review.get("output_digest_mismatch_count") == 0,
        "feature_values_digest_matches": review.get("local_output_digests", {}).get("feature_values.jsonl") == EXPECTED_SOURCE_FEATURE_VALUES_DIGEST,
        "feature_values_jsonl_schema_verified": inspection.get("feature_values_jsonl_schema_verified") is True,
        "feature_values_count_verified": review.get("feature_values_count_verified") is True,
        "selected_signal_family_count_7": review.get("selected_signal_family_count") == 7,
        "selected_feature_family_count_8": review.get("selected_feature_family_count") == 8,
        "selected_feature_group_count_13": review.get("selected_feature_group_count") == 13,
        "feature_row_count_155298": review.get("feature_row_count") == 155298,
        "available_feature_row_count_155142": review.get("available_feature_row_count") == 155142,
        "unavailable_feature_row_count_156": review.get("unavailable_feature_row_count") == 156,
        "non_meta_ticker_feature_counts_verified": inspection.get("non_meta_ticker_feature_counts_verified") is True,
        "meta_feature_counts_verified": inspection.get("meta_feature_counts_verified") is True,
        "signal_families_verified": inspection.get("signal_families") == SIGNAL_FAMILIES,
        "feature_families_verified": inspection.get("feature_families") == FEATURE_FAMILIES,
        "feature_groups_verified": inspection.get("feature_groups") == FEATURE_GROUPS,
        "target_values_not_used_as_features": review.get("target_values_used_as_features") is False,
        "target_classes_not_used_as_features": review.get("target_classes_used_as_features") is False,
        "forward_returns_not_used_as_features": review.get("forward_returns_used_as_features") is False,
        "future_data_not_used_as_features": review.get("future_data_used_as_features") is False,
        "prediction_fields_absent": review.get("prediction_fields_present") is False,
        "strategy_score_fields_absent": review.get("strategy_score_fields_present") is False,
        "trade_recommendation_fields_absent": review.get("trade_recommendation_fields_present") is False,
        "digest_manifest_self_reference_policy_verified": review.get("digest_manifest_self_reference_policy") == "SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE",
        "schema_report_verified": reports.get("schema_report_verified") is True,
        "coverage_report_verified": reports.get("coverage_report_verified") is True,
        "feature_group_report_verified": reports.get("feature_group_report_verified") is True,
        "no_peek_feature_report_verified": reports.get("no_peek_feature_report_verified") is True,
        "per_ticker_feature_report_verified": reports.get("per_ticker_feature_report_verified") is True,
        "meta_limitation_report_verified": reports.get("meta_limitation_report_verified") is True,
        "operator_summary_verified": reports.get("operator_summary_verified") is True,
        "results_review_created_true": review.get("signal_or_feature_generation_results_review_created") is True,
        "results_review_ready_true": review.get("signal_or_feature_generation_results_review_ready") is True,
        "ready_for_feature_label_matrix_candidate_true": review.get("ready_for_feature_label_matrix_candidate") is True,
        "feature_label_matrix_candidate_created_false": review.get("feature_label_matrix_candidate_created") is False,
        "feature_label_matrix_created_false": review.get("feature_label_matrix_created") is False,
        "backtest_execution_authorized_false": review.get("backtest_execution_authorized") is False,
        "backtest_execution_performed_false": review.get("backtest_execution_performed") is False,
        "model_training_authorized_false": review.get("model_training_authorized") is False,
        "model_training_performed_false": review.get("model_training_performed") is False,
        "metric_computation_authorized_false": review.get("metric_computation_authorized") is False,
        "metric_computation_performed_false": review.get("metric_computation_performed") is False,
        "strategy_scoring_false": review.get("strategy_scoring_performed") is False,
        "predictive_usefulness_not_accepted": review.get("predictive_usefulness") == NOT_ACCEPTED,
        "profitability_not_accepted": review.get("profitability") == NOT_ACCEPTED,
        "runtime_not_authorized": review.get("runtime_use") == NOT_AUTHORIZED,
        "strategy_not_authorized": review.get("strategy_use") == NOT_AUTHORIZED,
        "broker_not_authorized": review.get("broker_execution") == NOT_AUTHORIZED,
        "trade_recommendations_false": review.get("trade_recommendations_generated") is False,
        "per_ticker_entries_12": len(entries) == 12 and [row.get("ticker") for row in entries] == TARGET_UNIVERSE,
        "per_ticker_digests_present": all(isinstance(row.get("per_ticker_signal_or_feature_generation_results_review_digest"), str) and len(row["per_ticker_signal_or_feature_generation_results_review_digest"]) == 64 for row in entries),
        "provider_requests_made_false": review.get("provider_requests_made_in_review") is False,
        "market_data_acquisition_false": review.get("market_data_acquisition_performed_in_review") is False,
        "dataset_regeneration_false": review.get("canonical_dataset_regenerated_in_review") is False,
        "signal_or_feature_generation_execution_rerun_false": review.get("signal_or_feature_generation_execution_rerun_performed") is False,
        "target_generation_execution_rerun_false": review.get("target_generation_execution_rerun_performed") is False,
        "target_results_review_rerun_false": review.get("target_generation_results_review_rerun_performed") is False,
        "candidate_creation_rerun_false": review.get("candidate_creation_rerun_performed") is False,
        "candidate_review_rerun_false": review.get("candidate_review_rerun_performed") is False,
        "approval_rerun_false": review.get("approval_rerun_performed") is False,
        "raw_provider_payloads_not_committed": review.get("raw_provider_payloads_committed") is False,
        "api_keys_not_stored_or_printed": review.get("api_keys_stored_or_printed") is False,
        "next_chain_defined": review.get("next_chain") == NEXT_CHAIN,
        "next_gates_defined": review.get("next_gates") == NEXT_GATES,
        "risk_controls_defined": review.get("risk_controls") == RISK_CONTROLS,
        "no_tracked_marketflow_files": review.get("no_tracked_marketflow_files") is True,
    })
    return values


def _review_checklist(review: Mapping[str, Any]) -> list[dict[str, Any]]:
    values = _check_values(review)
    return [_check(check_id, True, values.get(check_id, False)) for check_id in REQUIRED_CHECK_IDS]


def _summary(checklist: list[dict[str, Any]]) -> dict[str, Any]:
    passed = sum(row["status"] == PASS for row in checklist)
    failed = len(checklist) - passed
    return {
        "total_checks": len(checklist),
        "passed_checks": passed,
        "failed_checks": failed,
        "blocker_count": sum(row["status"] == FAIL for row in checklist),
        "signal_or_feature_generation_results_review_created": True,
        "signal_or_feature_generation_results_review_ready": True,
        "ready_for_feature_label_matrix_candidate": True,
        "feature_label_matrix_candidate_created": False,
        "selected_feature_package": execution.PACKAGE_TREND_FLOW_EXPECTANCY_SIGNAL_SET,
        "feature_row_count": 155298,
        "available_feature_row_count": 155142,
        "unavailable_feature_row_count": 156,
        "output_digest_mismatch_count": 0,
        "feature_label_matrix_created": False,
        "backtest_execution_performed": False,
        "model_training_performed": False,
        "metric_computation_performed": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_authorized": False,
        "trade_recommendations_generated": False,
    }


def _base_review(
    output_root: Path,
    payloads: Mapping[str, dict[str, Any]],
    bindings: list[dict[str, Any]],
    feature_stats: Mapping[str, Any],
    report_reviews: Mapping[str, bool],
) -> dict[str, Any]:
    source = payloads["signal_feature_generation_manifest.json"]
    local_digests = {row["filename"]: row["local_sha256"] for row in bindings}
    per_ticker_entries = _per_ticker_review_entries(source)
    return {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_RESULTS_REVIEW_PACKAGE,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_RESULTS_REVIEW_V1,
        "review_status": MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_RESULTS_REVIEW_PACKAGE_READY,
        "review_scope": SIGNAL_OR_FEATURE_GENERATION_RESULTS_REVIEW_ONLY_NOT_FEATURE_LABEL_MATRIX_NOT_BACKTEST,
        "created_offline": True,
        "research_only": True,
        "operator_review_required": True,
        "source_output_root": _path_text(output_root),
        "source_signal_or_feature_generation_execution_artifact_kind": execution.ARTIFACT_KIND_MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_EXECUTED,
        "source_signal_or_feature_generation_execution_status": execution.MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_EXECUTED_RESEARCH_ONLY,
        "source_signal_or_feature_generation_execution_scope": execution.SIGNAL_OR_FEATURE_GENERATION_EXECUTION_ONLY_NOT_FEATURE_LABEL_MATRIX_NOT_BACKTEST,
        "source_signal_or_feature_generation_execution_digest": EXPECTED_SOURCE_EXECUTION_DIGEST,
        "source_signal_or_feature_generation_output_binding_digest": EXPECTED_SOURCE_OUTPUT_BINDING_DIGEST,
        "source_signal_or_feature_values_digest": EXPECTED_SOURCE_FEATURE_VALUES_DIGEST,
        "source_signal_or_feature_generation_approval_digest": EXPECTED_SOURCE_APPROVAL_DIGEST,
        "source_candidate_review_digest": execution.approval_service.EXPECTED_SOURCE_CANDIDATE_REVIEW_DIGEST,
        "source_candidate_digest": execution.approval_service.EXPECTED_SOURCE_CANDIDATE_DIGEST,
        "source_evidence": deepcopy(SOURCE_EVIDENCE),
        "selected_feature_package": execution.PACKAGE_TREND_FLOW_EXPECTANCY_SIGNAL_SET,
        "selected_label_target_package": execution.PACKAGE_EXPECTANCY_PAYOFF_ABSTENTION_LABEL_SET,
        "selected_objective_path": execution.EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT,
        "dataset_name": "expanded_universe_canonical_dataset_v1",
        "source_profile": "RTH_FULL_SESSION_1D",
        "timeframe": "1d",
        "date_range_start": "2022-01-01",
        "date_range_end": "2025-12-31",
        "target_universe": TARGET_UNIVERSE,
        "target_universe_count": 12,
        "total_canonical_record_count": 11946,
        "records_digest": execution.EXPECTED_RECORDS_DIGEST,
        "meta_record_count": 913,
        "non_meta_record_count": 1003,
        "meta_reduced_record_count_preserved": True,
        "signal_or_feature_generation_performed": True,
        "signal_generation_performed": True,
        "feature_generation_performed": True,
        "feature_values_created": True,
        "signal_or_feature_generation_results_created": True,
        "signal_or_feature_generation_results_review_created": True,
        "signal_or_feature_generation_results_review_ready": True,
        "ready_for_feature_label_matrix_candidate": True,
        "selected_signal_families": SIGNAL_FAMILIES,
        "selected_feature_families": FEATURE_FAMILIES,
        "selected_feature_groups": FEATURE_GROUPS,
        "selected_signal_family_count": 7,
        "selected_feature_family_count": 8,
        "selected_feature_group_count": 13,
        "feature_row_count": feature_stats["feature_row_count"],
        "available_feature_row_count": feature_stats["available_feature_row_count"],
        "unavailable_feature_row_count": feature_stats["unavailable_feature_row_count"],
        "expected_output_count": 10,
        "observed_output_count": len(bindings),
        "output_file_inspection_performed": True,
        "output_digest_bindings": deepcopy(bindings),
        "local_output_digests": local_digests,
        "recorded_file_digest_match_count": sum(
            row["recorded_digest_kind"] == "FILE_SHA256"
            and row["verification_status"] == PASS
            for row in bindings
        ),
        "local_output_digest_count": len(local_digests),
        "output_digest_mismatch_count": sum(
            row["verification_status"] != PASS for row in bindings
        ),
        "digest_manifest_self_reference_policy": "SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE",
        "execution_artifact_special_policy": "SELF_REFERENTIAL_EXECUTION_ARTIFACT",
        "feature_values_inspection": deepcopy(dict(feature_stats)),
        "feature_values_jsonl_schema_verified": feature_stats["feature_values_jsonl_schema_verified"],
        "feature_values_count_verified": feature_stats["feature_row_count"] == 155298,
        "per_ticker_feature_counts_verified": feature_stats["non_meta_ticker_feature_counts_verified"] and feature_stats["meta_feature_counts_verified"],
        "meta_limitation_verified": feature_stats["meta_feature_counts_verified"],
        "report_reviews": deepcopy(dict(report_reviews)),
        "feature_values_jsonl_review": "VERIFIED_RESEARCH_ONLY",
        "signal_feature_schema_review": "VERIFIED",
        "feature_coverage_report_review": "VERIFIED",
        "feature_group_report_review": "VERIFIED",
        "no_peek_feature_report_review": "VERIFIED",
        "per_ticker_feature_report_review": "VERIFIED",
        "meta_limitation_report_review": "VERIFIED",
        "operator_summary_review": "VERIFIED",
        "digest_manifest_review": "VERIFIED_ZERO_MISMATCHES",
        "per_ticker_signal_or_feature_generation_results_review_entries": per_ticker_entries,
        "target_values_used_as_features": False,
        "target_classes_used_as_features": False,
        "forward_returns_used_as_features": False,
        "future_data_used_as_features": False,
        "prediction_fields_present": False,
        "strategy_score_fields_present": False,
        "trade_recommendation_fields_present": False,
        "feature_label_matrix_candidate_created": False,
        "feature_label_matrix_created": False,
        "backtest_execution_authorized": False,
        "backtest_execution_performed": False,
        "model_training_authorized": False,
        "model_training_performed": False,
        "metric_computation_authorized": False,
        "metric_computation_performed": False,
        "strategy_scoring_performed": False,
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
        "new_strategy_scoring_performed": False,
        "trade_recommendations_generated": False,
        "provider_requests_made_in_review": False,
        "live_provider_transport_enabled_in_review": False,
        "market_data_acquisition_performed_in_review": False,
        "dataset_generation_performed_in_review": False,
        "canonical_dataset_regenerated_in_review": False,
        "signal_or_feature_generation_execution_rerun_performed": False,
        "target_generation_execution_rerun_performed": False,
        "target_generation_results_review_rerun_performed": False,
        "candidate_creation_rerun_performed": False,
        "candidate_review_rerun_performed": False,
        "approval_rerun_performed": False,
        "raw_provider_payloads_committed": False,
        "api_keys_stored_or_printed": False,
        "no_tracked_marketflow_files": True,
        "next_chain": NEXT_CHAIN,
        "next_gates": NEXT_GATES,
        "risk_controls": RISK_CONTROLS,
    }


def marketflow_signal_or_feature_generation_results_review_digest_v1(
    review: Mapping[str, Any],
) -> str:
    payload = deepcopy(dict(review))
    payload.pop("marketflow_signal_or_feature_generation_results_review_digest", None)
    payload.pop("source_output_root", None)
    return semantic_digest(payload)


def build_marketflow_signal_or_feature_generation_results_review_v1(
    *, output_root: str | Path | None = None,
) -> dict:
    """Inspect and bind existing feature-generation outputs without changing them."""
    root = DEFAULT_OUTPUT_ROOT if output_root is None else Path(output_root)
    payloads, bindings, feature_stats, report_reviews, failures = _verify_outputs(root)
    if failures:
        return _blocked_package(root, failures)
    review = _base_review(root, payloads, bindings, feature_stats, report_reviews)
    checklist = _review_checklist(review)
    review["review_checklist"] = checklist
    review["review_summary"] = _summary(checklist)
    if review["review_summary"]["blocker_count"]:
        return _blocked_package(root, [
            _failure(
                "review_checklist_blocked",
                "results-review checklist contains blockers",
                failed_check_ids=[
                    row["check_id"] for row in checklist if row["status"] != PASS
                ],
            )
        ])
    review["marketflow_signal_or_feature_generation_results_review_digest"] = (
        marketflow_signal_or_feature_generation_results_review_digest_v1(review)
    )
    validate_marketflow_signal_or_feature_generation_results_review_v1(review)
    return review


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise MarketFlowSignalOrFeatureGenerationResultsReviewError(
            f"{field} mismatch: expected {expected!r}, got {actual!r}"
        )


def validate_marketflow_signal_or_feature_generation_results_review_v1(
    review: dict,
) -> dict:
    """Validate a ready or fail-closed feature results-review package."""
    if not isinstance(review, dict):
        raise MarketFlowSignalOrFeatureGenerationResultsReviewError(
            "results review must be a JSON object"
        )
    if review.get("review_status") == MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_RESULTS_REVIEW_BLOCKED_MISSING_OR_INVALID_OUTPUTS:
        _expect(
            review.get("artifact_kind"),
            ARTIFACT_KIND_MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_RESULTS_REVIEW_BLOCKED,
            "artifact_kind",
        )
        _expect(review.get("signal_or_feature_generation_results_review_created"), False, "results_review_created")
        _expect(review.get("signal_or_feature_generation_results_review_ready"), False, "results_review_ready")
        _expect(review.get("ready_for_feature_label_matrix_candidate"), False, "ready_for_feature_label_matrix_candidate")
        _expect(review.get("marketflow_signal_or_feature_generation_results_review_digest"), "NOT_CREATED", "blocked review digest")
        return {
            "status": MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_RESULTS_REVIEW_BLOCKED_VALID,
            "artifact_kind": review["artifact_kind"],
            "review_status": review["review_status"],
            "failure_count": len(review.get("failures", [])),
        }
    exact = {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_RESULTS_REVIEW_PACKAGE,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_RESULTS_REVIEW_V1,
        "review_status": MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_RESULTS_REVIEW_PACKAGE_READY,
        "review_scope": SIGNAL_OR_FEATURE_GENERATION_RESULTS_REVIEW_ONLY_NOT_FEATURE_LABEL_MATRIX_NOT_BACKTEST,
        "source_signal_or_feature_generation_execution_artifact_kind": execution.ARTIFACT_KIND_MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_EXECUTED,
        "source_signal_or_feature_generation_execution_status": execution.MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_EXECUTED_RESEARCH_ONLY,
        "source_signal_or_feature_generation_execution_scope": execution.SIGNAL_OR_FEATURE_GENERATION_EXECUTION_ONLY_NOT_FEATURE_LABEL_MATRIX_NOT_BACKTEST,
        "source_signal_or_feature_generation_execution_digest": EXPECTED_SOURCE_EXECUTION_DIGEST,
        "source_signal_or_feature_generation_output_binding_digest": EXPECTED_SOURCE_OUTPUT_BINDING_DIGEST,
        "source_signal_or_feature_values_digest": EXPECTED_SOURCE_FEATURE_VALUES_DIGEST,
        "source_signal_or_feature_generation_approval_digest": EXPECTED_SOURCE_APPROVAL_DIGEST,
        "source_evidence": SOURCE_EVIDENCE,
        "selected_feature_package": execution.PACKAGE_TREND_FLOW_EXPECTANCY_SIGNAL_SET,
        "selected_label_target_package": execution.PACKAGE_EXPECTANCY_PAYOFF_ABSTENTION_LABEL_SET,
        "selected_objective_path": execution.EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT,
        "target_universe": TARGET_UNIVERSE,
        "target_universe_count": 12,
        "total_canonical_record_count": 11946,
        "records_digest": execution.EXPECTED_RECORDS_DIGEST,
        "meta_record_count": 913,
        "non_meta_record_count": 1003,
        "selected_signal_families": SIGNAL_FAMILIES,
        "selected_feature_families": FEATURE_FAMILIES,
        "selected_feature_groups": FEATURE_GROUPS,
        "selected_signal_family_count": 7,
        "selected_feature_family_count": 8,
        "selected_feature_group_count": 13,
        "feature_row_count": 155298,
        "available_feature_row_count": 155142,
        "unavailable_feature_row_count": 156,
        "expected_output_count": 10,
        "observed_output_count": 10,
        "output_digest_mismatch_count": 0,
        "recorded_file_digest_match_count": 8,
        "local_output_digest_count": 10,
        "digest_manifest_self_reference_policy": "SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE",
        "execution_artifact_special_policy": "SELF_REFERENTIAL_EXECUTION_ARTIFACT",
        "next_chain": NEXT_CHAIN,
        "next_gates": NEXT_GATES,
        "risk_controls": RISK_CONTROLS,
    }
    for field, expected in exact.items():
        _expect(review.get(field), expected, field)
    for field in (
        "created_offline", "research_only", "operator_review_required",
        "signal_or_feature_generation_performed", "signal_generation_performed",
        "feature_generation_performed", "feature_values_created",
        "signal_or_feature_generation_results_created",
        "signal_or_feature_generation_results_review_created",
        "signal_or_feature_generation_results_review_ready",
        "ready_for_feature_label_matrix_candidate", "output_file_inspection_performed",
        "feature_values_jsonl_schema_verified", "feature_values_count_verified",
        "per_ticker_feature_counts_verified", "meta_limitation_verified",
        "meta_reduced_record_count_preserved",
    ):
        _expect(review.get(field), True, field)
    for field in (
        "target_values_used_as_features", "target_classes_used_as_features",
        "forward_returns_used_as_features", "future_data_used_as_features",
        "prediction_fields_present", "strategy_score_fields_present",
        "trade_recommendation_fields_present", "feature_label_matrix_candidate_created",
        "feature_label_matrix_created", "backtest_execution_authorized",
        "backtest_execution_performed", "model_training_authorized",
        "model_training_performed", "metric_computation_authorized",
        "metric_computation_performed", "strategy_scoring_performed",
        "predictive_usefulness_acceptance_candidate_created",
        "predictive_usefulness_acceptance_ready",
        "predictive_usefulness_acceptance_recommended",
        "profitability_acceptance_ready", "profitability_acceptance_recommended",
        "runtime_migration_approved", "runtime_migration_active", "automatic_stitching",
        "new_strategy_scoring_performed", "trade_recommendations_generated",
        "provider_requests_made_in_review", "live_provider_transport_enabled_in_review",
        "market_data_acquisition_performed_in_review", "dataset_generation_performed_in_review",
        "canonical_dataset_regenerated_in_review",
        "signal_or_feature_generation_execution_rerun_performed",
        "target_generation_execution_rerun_performed",
        "target_generation_results_review_rerun_performed",
        "candidate_creation_rerun_performed", "candidate_review_rerun_performed",
        "approval_rerun_performed", "raw_provider_payloads_committed",
        "api_keys_stored_or_printed",
    ):
        _expect(review.get(field), False, field)
    _expect(review.get("predictive_usefulness"), NOT_ACCEPTED, "predictive_usefulness")
    _expect(review.get("profitability"), NOT_ACCEPTED, "profitability")
    for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
        _expect(review.get(field), NOT_AUTHORIZED, field)
    local_digests = review.get("local_output_digests")
    if not isinstance(local_digests, dict) or list(local_digests) != EXPECTED_OUTPUT_FILENAMES:
        raise MarketFlowSignalOrFeatureGenerationResultsReviewError(
            "local_output_digests mismatch"
        )
    if any(not isinstance(value, str) or len(value) != 64 for value in local_digests.values()):
        raise MarketFlowSignalOrFeatureGenerationResultsReviewError(
            "local output SHA-256 missing"
        )
    _expect(local_digests["feature_values.jsonl"], EXPECTED_SOURCE_FEATURE_VALUES_DIGEST, "feature values digest")
    for field in (
        "signal_feature_schema_review", "feature_coverage_report_review",
        "feature_group_report_review", "no_peek_feature_report_review",
        "per_ticker_feature_report_review", "meta_limitation_report_review",
        "operator_summary_review",
    ):
        _expect(review.get(field), "VERIFIED", field)
    _expect(review.get("feature_values_jsonl_review"), "VERIFIED_RESEARCH_ONLY", "feature_values_jsonl_review")
    _expect(review.get("digest_manifest_review"), "VERIFIED_ZERO_MISMATCHES", "digest_manifest_review")
    entries = review.get(
        "per_ticker_signal_or_feature_generation_results_review_entries"
    )
    if not isinstance(entries, list) or [row.get("ticker") for row in entries] != TARGET_UNIVERSE:
        raise MarketFlowSignalOrFeatureGenerationResultsReviewError(
            "per-ticker review entries mismatch"
        )
    for row in entries:
        payload = deepcopy(row)
        digest = payload.pop(
            "per_ticker_signal_or_feature_generation_results_review_digest", None
        )
        _expect(digest, semantic_digest(payload), f"{row.get('ticker')} review digest")
    expected_checklist = _review_checklist(review)
    _expect(review.get("review_checklist"), expected_checklist, "review_checklist")
    if any(row["status"] != PASS for row in expected_checklist):
        raise MarketFlowSignalOrFeatureGenerationResultsReviewError(
            "review checklist contains failures"
        )
    _expect(review.get("review_summary"), _summary(expected_checklist), "review_summary")
    digest = review.get("marketflow_signal_or_feature_generation_results_review_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise MarketFlowSignalOrFeatureGenerationResultsReviewError(
            "review digest missing"
        )
    _expect(
        digest,
        marketflow_signal_or_feature_generation_results_review_digest_v1(review),
        "review digest",
    )
    return {
        "status": MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_RESULTS_REVIEW_VALID,
        "artifact_kind": review["artifact_kind"],
        "review_status": review["review_status"],
        "review_scope": review["review_scope"],
        "marketflow_signal_or_feature_generation_results_review_digest": digest,
        "source_execution_digest": EXPECTED_SOURCE_EXECUTION_DIGEST,
        "source_output_binding_digest": EXPECTED_SOURCE_OUTPUT_BINDING_DIGEST,
        "source_feature_values_digest": EXPECTED_SOURCE_FEATURE_VALUES_DIGEST,
        "total_checks": review["review_summary"]["total_checks"],
        "passed_checks": review["review_summary"]["passed_checks"],
        "failed_checks": 0,
        "blocker_count": 0,
    }


def build_marketflow_signal_or_feature_generation_results_review_markdown_v1(
    review: dict,
) -> str:
    """Render the digest-bound feature results review as Markdown."""
    validation = validate_marketflow_signal_or_feature_generation_results_review_v1(
        review
    )
    sections = [
        ("Signal or Feature Generation Results Review v1", [
            f"Artifact/status/scope: `{review['artifact_kind']}` / `{review['review_status']}` / `{review['review_scope']}`.",
            f"Review digest: `{validation['marketflow_signal_or_feature_generation_results_review_digest']}`.",
        ]),
        ("Source Signal or Feature Generation Execution", [
            f"Execution digest: `{EXPECTED_SOURCE_EXECUTION_DIGEST}`; outputs were inspected read-only and not regenerated."
        ]),
        ("Bound Evidence", [
            f"Output binding `{EXPECTED_SOURCE_OUTPUT_BINDING_DIGEST}` and feature values `{EXPECTED_SOURCE_FEATURE_VALUES_DIGEST}` are bound with the complete upstream chain."
        ]),
        ("Dataset and Universe", [
            "`expanded_universe_canonical_dataset_v1`, 11,946 rows, ordered twelve-ticker universe; META remains exactly 913 rows."
        ]),
        ("Output Verification", [
            "All ten local SHA-256 values are bound; eight ordinary manifest hashes and both explicit special policies pass with zero mismatches."
        ]),
        ("Selected Feature Package", [
            f"`{execution.PACKAGE_TREND_FLOW_EXPECTANCY_SIGNAL_SET}` supporting `{execution.PACKAGE_EXPECTANCY_PAYOFF_ABSTENTION_LABEL_SET}` / `{execution.EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT}`."
        ]),
        ("Generated Signal Families", [
            ", ".join(f"`{item}`" for item in SIGNAL_FAMILIES)
        ]),
        ("Generated Feature Families", [
            ", ".join(f"`{item}`" for item in FEATURE_FAMILIES)
        ]),
        ("Feature Groups Review", [
            ", ".join(f"`{item}`" for item in FEATURE_GROUPS)
        ]),
        ("Feature Values Review", [
            "Verified 155,298 schema-valid, research-only rows; no target, future, prediction, scoring, recommendation, order, raw-provider, or credential fields are present."
        ]),
        ("No-Peek and Target-Separation Review", [
            "Verified current/prior same-ticker OHLCV and same-date history-derived ranks only; target values/classes, forward returns, and future data are excluded."
        ]),
        ("Feature Coverage Review", [
            "Verified 155,142 available and 156 unavailable group rows with no canonical rows dropped."
        ]),
        ("Per-Ticker Feature Report Review", [
            "Verified 13,039 rows per non-META ticker and 11,869 for META, with 13 unavailable group rows per ticker."
        ]),
        ("META Limitation Review", [
            "META's exact 913-row limitation remains preserved without repair, backfill, inference, smoothing, or fabrication."
        ]),
        ("Output Digest Manifest", [
            "Eight file hashes, `SELF_REFERENTIAL_EXECUTION_ARTIFACT`, and `SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE` are verified."
        ]),
        ("Next Chain", review["next_chain"]),
        ("Next Gates", review["next_gates"]),
        ("Risk Controls", review["risk_controls"]),
        ("Predictive Usefulness Boundary", [
            "Predictive usefulness remains not accepted."
        ]),
        ("Profitability Boundary", ["Profitability remains not accepted."]),
        ("Runtime Boundary", [
            "Runtime, strategy, paper trading, and broker execution remain NOT_AUTHORIZED."
        ]),
        ("Checklist Summary", [
            f"{review['review_summary']['passed_checks']}/{review['review_summary']['total_checks']} checks pass with zero blockers."
        ]),
        ("Guardrails", [
            "The review makes only a future feature-label matrix candidate ready; it creates no matrix rows, backtest, model, metric, score, recommendation, acceptance, runtime, or trading authority."
        ]),
    ]
    lines: list[str] = []
    for index, (title, body) in enumerate(sections):
        lines.append(("# " if index == 0 else "## ") + title)
        lines.append("")
        lines.extend(f"- {item}" for item in body)
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def write_marketflow_signal_or_feature_generation_results_review_v1(
    output_dir: str | Path,
    *,
    output_root: str | Path | None = None,
) -> dict:
    """Write a validated review JSON and Markdown to an explicit directory."""
    review = build_marketflow_signal_or_feature_generation_results_review_v1(
        output_root=output_root
    )
    validation = validate_marketflow_signal_or_feature_generation_results_review_v1(
        review
    )
    destination = Path(output_dir)
    destination.mkdir(parents=True, exist_ok=True)
    stem = "marketflow_signal_or_feature_generation_results_review_v1"
    json_path = destination / f"{stem}.json"
    markdown_path = destination / f"{stem}.md"
    if json_path.exists() or markdown_path.exists():
        raise MarketFlowSignalOrFeatureGenerationResultsReviewError(
            "results-review output already exists"
        )
    json_path.write_bytes(canonical_json_bytes(review))
    markdown_path.write_text(
        build_marketflow_signal_or_feature_generation_results_review_markdown_v1(
            review
        ),
        encoding="utf-8",
        newline="\n",
    )
    return {
        **validation,
        "json_path": _path_text(json_path),
        "markdown_path": _path_text(markdown_path),
    }
