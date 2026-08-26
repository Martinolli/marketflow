"""Offline results review for VPA/Wyckoff rule-baseline outputs."""

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
    marketflow_vpa_wyckoff_rule_baseline_execution_service as execution,
)


ARTIFACT_KIND_MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_RESULTS_REVIEW_PACKAGE = (
    "MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_RESULTS_REVIEW_PACKAGE"
)
ARTIFACT_KIND_MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_RESULTS_REVIEW_BLOCKED = (
    "MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_RESULTS_REVIEW_BLOCKED"
)
SCHEMA_VERSION_MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_RESULTS_REVIEW_V1 = (
    "marketflow_vpa_wyckoff_rule_baseline_results_review_v1"
)
MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_RESULTS_REVIEW_PACKAGE_READY = (
    "MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_RESULTS_REVIEW_PACKAGE_READY"
)
MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_RESULTS_REVIEW_BLOCKED_MISSING_OR_INVALID_OUTPUTS = (
    "MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_RESULTS_REVIEW_BLOCKED_MISSING_OR_INVALID_OUTPUTS"
)
VPA_WYCKOFF_RULE_BASELINE_RESULTS_REVIEW_ONLY_NOT_BACKTEST_NOT_MODEL_TRAINING = (
    "VPA_WYCKOFF_RULE_BASELINE_RESULTS_REVIEW_ONLY_NOT_BACKTEST_NOT_MODEL_TRAINING"
)
MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_RESULTS_REVIEW_VALID = (
    "MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_RESULTS_REVIEW_VALID"
)
MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_RESULTS_REVIEW_BLOCKED_VALID = (
    "MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_RESULTS_REVIEW_BLOCKED_VALID"
)

EXPECTED_SOURCE_EXECUTION_DIGEST = (
    "5b453c45ddd39fa4a059cd78a02254a241876443794213f6238bde69a534eaec"
)
EXPECTED_SOURCE_OUTPUT_BINDING_DIGEST = (
    "3bcaa233d6dab9d13e85f9a80f3ef2c0503d6a64f4707560a3f117ba9ab6afc7"
)
EXPECTED_SOURCE_RULE_VALUES_DIGEST = (
    "bef559f34d42777b577a89a1842a2cffd6e7ff712b0c3191776901c12f4dbcad"
)
EXPECTED_SOURCE_APPROVAL_DIGEST = execution.EXPECTED_SOURCE_APPROVAL_DIGEST
EXPECTED_SOURCE_CANDIDATE_REVIEW_DIGEST = (
    execution.EXPECTED_SOURCE_CANDIDATE_REVIEW_DIGEST
)
EXPECTED_SOURCE_CANDIDATE_DIGEST = execution.EXPECTED_SOURCE_CANDIDATE_DIGEST
EXPECTED_SOURCE_MATRIX_RESULTS_REVIEW_DIGEST = (
    execution.EXPECTED_SOURCE_MATRIX_RESULTS_REVIEW_DIGEST
)
EXPECTED_SOURCE_MATRIX_EXECUTION_DIGEST = (
    execution.EXPECTED_SOURCE_MATRIX_EXECUTION_DIGEST
)
EXPECTED_SOURCE_MATRIX_OUTPUT_BINDING_DIGEST = (
    execution.EXPECTED_SOURCE_MATRIX_OUTPUT_BINDING_DIGEST
)
EXPECTED_SOURCE_MATRIX_ROWS_DIGEST = execution.EXPECTED_SOURCE_MATRIX_ROWS_DIGEST
EXPECTED_SOURCE_FEATURE_VALUES_DIGEST = execution.EXPECTED_SOURCE_FEATURE_VALUES_DIGEST
EXPECTED_SOURCE_TARGET_VALUES_DIGEST = execution.EXPECTED_SOURCE_TARGET_VALUES_DIGEST
EXPECTED_SOURCE_RECORDS_DIGEST = execution.EXPECTED_SOURCE_RECORDS_DIGEST

DEFAULT_OUTPUT_ROOT = execution.DEFAULT_OUTPUT_ROOT
DEFAULT_SOURCE_MATRIX_PATH = execution.DEFAULT_SOURCE_MATRIX_PATH
EXPECTED_OUTPUT_FILENAMES = list(execution.OUTPUT_FILENAMES)
TARGET_UNIVERSE = list(execution.TARGET_UNIVERSE)
EXPECTED_RECORD_COUNTS = dict(execution.EXPECTED_RECORD_COUNTS)
EXPECTED_SOURCE_MATRIX_ROW_COUNT = execution.EXPECTED_SOURCE_MATRIX_ROW_COUNT
EXPECTED_RULE_VALUE_ROW_COUNT = execution.EXPECTED_RULE_VALUE_ROW_COUNT
EXPECTED_STATE_VALUE_ROW_COUNT = execution.EXPECTED_STATE_VALUE_ROW_COUNT
EXPECTED_RULE_FAMILY_REFERENCE_COUNT = execution.EXPECTED_RULE_FAMILY_REFERENCE_COUNT
EXPECTED_STATE_FAMILY_REFERENCE_COUNT = execution.EXPECTED_STATE_FAMILY_REFERENCE_COUNT
EXPECTED_OUTPUT_COUNT = execution.EXPECTED_OUTPUT_COUNT
SELECTED_RULE_FAMILY_IDS = list(execution.SELECTED_RULE_FAMILY_IDS)
SUPPORTING_RULE_FAMILY_IDS = list(execution.SUPPORTING_RULE_FAMILY_IDS)
SELECTED_STATE_FAMILY_IDS = list(execution.SELECTED_STATE_FAMILY_IDS)
SUPPORTING_STATE_FAMILY_IDS = list(execution.SUPPORTING_STATE_FAMILY_IDS)
EXPECTED_RULE_ROW_FIELDS = set(execution.RULE_OUTPUT_ROW_FIELDS)
FORBIDDEN_RULE_OUTPUT_FIELDS = set(execution.FORBIDDEN_RULE_OUTPUT_FIELDS)
REVIEW_FORBIDDEN_FIELDS = FORBIDDEN_RULE_OUTPUT_FIELDS | {
    "future_outcome_value",
    "future_value",
    "prediction_value",
    "broker_order_id",
    "api_keys",
}
NOT_ACCEPTED = execution.NOT_ACCEPTED
NOT_AUTHORIZED = execution.NOT_AUTHORIZED
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

NEXT_CHAIN = [
    "Expectancy Backtest Lab Candidate v1.",
    "Expectancy Backtest Lab Candidate Operator Review v1.",
    "Expectancy Backtest Lab Approval v1.",
    "Expectancy Backtest Lab Execution v1.",
    "Expectancy Backtest Lab Results Review v1.",
    "Results review and readiness gates before predictive-usefulness acceptance.",
    "Runtime migration only if ever separately authorized.",
]
NEXT_GATES = [
    "expectancy_backtest_lab_candidate",
    "expectancy_backtest_lab_candidate_operator_review",
    "expectancy_backtest_lab_approval",
    "expectancy_backtest_lab_execution",
    "expectancy_backtest_lab_results_review",
    "expectancy_results_review_and_reassessment",
    "predictive_usefulness_acceptance_candidate_if_ready",
    "runtime_migration_chain_if_ever_authorized",
]
RISK_CONTROLS = [
    "review_does_not_create_expectancy_backtest_lab_candidate",
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
    "review_does_not_rerun_vpa_wyckoff_rule_baseline_execution",
    "review_does_not_rerun_feature_label_matrix_execution",
    "review_does_not_rerun_feature_label_matrix_results_review",
    "review_does_not_rerun_vpa_wyckoff_candidate_creation",
    "review_does_not_rerun_vpa_wyckoff_candidate_review",
    "review_does_not_rerun_vpa_wyckoff_approval",
    "do_not_mutate_frozen_dataset",
    "do_not_mutate_vpa_wyckoff_outputs",
    "do_not_mutate_matrix_outputs",
    "do_not_mutate_signal_or_feature_outputs",
    "do_not_mutate_target_outputs",
    "do_not_mutate_redesigned_label_outputs",
    "do_not_mutate_prior_feature_outputs",
    "do_not_mutate_predictive_evidence_outputs",
    "preserve_meta_record_limitation",
    "all_outputs_research_only",
]

REQUIRED_CHECK_IDS = [
    "source_execution_digest_bound",
    "source_output_binding_digest_bound",
    "source_rule_values_digest_bound",
    "source_approval_digest_bound",
    "source_candidate_review_digest_bound",
    "source_candidate_digest_bound",
    "source_matrix_results_review_digest_bound",
    "source_matrix_execution_digest_bound",
    "source_matrix_rows_digest_bound",
    "source_feature_values_digest_bound",
    "source_target_values_digest_bound",
    "records_digest_bound",
    "target_universe_12_preserved",
    "records_digest_preserved",
    "meta_913_preserved",
    "selected_vpa_wyckoff_package_preserved",
    "selected_matrix_package_preserved",
    "selected_feature_package_preserved",
    "selected_target_package_preserved",
    "selected_objective_path_preserved",
    "expected_output_count_10",
    "observed_output_count_10",
    "output_digest_mismatch_count_zero",
    "rule_values_digest_matches",
    "rule_values_jsonl_schema_verified",
    "rule_values_count_verified",
    "state_values_count_verified",
    "source_matrix_row_count_179190",
    "rule_value_row_count_179190",
    "state_value_row_count_179190",
    "selected_rule_family_count_8",
    "selected_state_family_count_6",
    "rule_family_reference_count_1433520",
    "state_family_reference_count_1075140",
    "non_meta_ticker_counts_verified",
    "meta_counts_verified",
    "rule_threshold_policy_static_not_optimized",
    "executed_rule_families_verified",
    "executed_state_families_verified",
    "supporting_families_not_executed",
    "target_values_absent",
    "target_classes_absent",
    "forward_returns_absent",
    "future_data_absent",
    "prediction_fields_absent",
    "strategy_score_fields_absent",
    "trade_recommendation_fields_absent",
    "broker_order_fields_absent",
    "provider_payload_fields_absent",
    "api_key_fields_absent",
    "digest_manifest_self_reference_policy_verified",
    "rule_schema_verified",
    "state_schema_verified",
    "coverage_report_verified",
    "per_ticker_report_verified",
    "meta_limitation_report_verified",
    "no_peek_report_verified",
    "operator_summary_verified",
    "results_review_created_true",
    "results_review_ready_true",
    "ready_for_expectancy_backtest_lab_candidate_true",
    "expectancy_backtest_lab_candidate_created_false",
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
    "vpa_wyckoff_rule_baseline_execution_rerun_false",
    "feature_label_matrix_execution_rerun_false",
    "feature_label_matrix_results_review_rerun_false",
    "vpa_wyckoff_candidate_creation_rerun_false",
    "vpa_wyckoff_candidate_review_rerun_false",
    "vpa_wyckoff_approval_rerun_false",
    "raw_provider_payloads_not_committed",
    "api_keys_not_stored_or_printed",
    "next_chain_defined",
    "next_gates_defined",
    "risk_controls_defined",
    "no_tracked_marketflow_files",
]


class MarketFlowVpaWyckoffRuleBaselineResultsReviewError(ValueError):
    """Raised when source results violate the review contract."""


def _load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise MarketFlowVpaWyckoffRuleBaselineResultsReviewError(
            f"invalid JSON output: {path.name}"
        ) from exc
    if not isinstance(value, dict):
        raise MarketFlowVpaWyckoffRuleBaselineResultsReviewError(
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


def _inspect_rule_values(path: Path) -> dict[str, Any]:
    row_count = rule_references = state_references = 0
    ticker_counts: Counter[str] = Counter()
    schema_verified = package_binding_verified = family_schema_verified = True
    research_boundary_verified = True
    forbidden: set[str] = set()
    malformed_line_count = 0

    try:
        with path.open("r", encoding="utf-8") as handle:
            for line_number, line in enumerate(handle, start=1):
                try:
                    row = json.loads(line)
                except json.JSONDecodeError as exc:
                    raise MarketFlowVpaWyckoffRuleBaselineResultsReviewError(
                        f"invalid rule-values JSONL at line {line_number}"
                    ) from exc
                if not isinstance(row, dict):
                    malformed_line_count += 1
                    continue
                row_count += 1
                ticker_counts[str(row.get("ticker"))] += 1
                schema_verified &= set(row) == EXPECTED_RULE_ROW_FIELDS
                package_binding_verified &= (
                    row.get("dataset_name") == "expanded_universe_canonical_dataset_v1"
                    and row.get("records_digest") == EXPECTED_SOURCE_RECORDS_DIGEST
                    and row.get("selected_vpa_wyckoff_package")
                    == execution.PACKAGE_VPA_WYCKOFF_TRANSPARENT_RULE_BASELINE
                    and row.get("selected_matrix_package")
                    == execution.PACKAGE_EXPECTANCY_TARGET_PROFILE_WIDE_FEATURE_MATRIX
                    and row.get("selected_matrix_layout")
                    == execution.MATRIX_LAYOUT_TARGET_PROFILE_WITH_WIDE_FEATURE_BUNDLE
                    and row.get("selected_feature_package")
                    == execution.PACKAGE_TREND_FLOW_EXPECTANCY_SIGNAL_SET
                    and row.get("selected_label_target_package")
                    == execution.PACKAGE_EXPECTANCY_PAYOFF_ABSTENTION_LABEL_SET
                    and row.get("selected_objective_path")
                    == execution.EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT
                    and row.get("source_matrix_rows_digest")
                    == EXPECTED_SOURCE_MATRIX_ROWS_DIGEST
                )
                research_boundary_verified &= (
                    row.get("research_only") is True
                    and row.get("non_actionable") is True
                )
                rule_values = row.get("rule_values")
                state_values = row.get("state_values")
                if not isinstance(rule_values, dict) or not isinstance(state_values, dict):
                    family_schema_verified = False
                    continue
                rule_references += len(rule_values)
                state_references += len(state_values)
                family_schema_verified &= (
                    set(rule_values) == set(SELECTED_RULE_FAMILY_IDS)
                    and set(state_values) == set(SELECTED_STATE_FAMILY_IDS)
                    and row.get("rule_family_count") == len(SELECTED_RULE_FAMILY_IDS)
                    and row.get("state_family_count") == len(SELECTED_STATE_FAMILY_IDS)
                    and all(
                        isinstance(value, dict)
                        and set(value) == {"available", "tag"}
                        and isinstance(value.get("available"), bool)
                        and isinstance(value.get("tag"), str)
                        for value in rule_values.values()
                    )
                    and all(
                        isinstance(value, dict)
                        and set(value) == {"available", "value"}
                        and isinstance(value.get("available"), bool)
                        and (
                            value.get("value") is None
                            or isinstance(value.get("value"), bool)
                        )
                        for value in state_values.values()
                    )
                )
                forbidden.update(_nested_keys(row) & REVIEW_FORBIDDEN_FIELDS)
    except OSError as exc:
        raise MarketFlowVpaWyckoffRuleBaselineResultsReviewError(
            "rule-values JSONL could not be streamed"
        ) from exc

    expected_ticker_counts = {
        ticker: count * 15 for ticker, count in EXPECTED_RECORD_COUNTS.items()
    }
    return {
        "inspection_method": "STREAMING_JSONL_ONE_ROW_AT_A_TIME",
        "entire_jsonl_loaded_into_memory": False,
        "row_count": row_count,
        "rule_reference_count": rule_references,
        "state_reference_count": state_references,
        "ticker_row_counts": dict(ticker_counts),
        "rule_values_jsonl_schema_verified": schema_verified,
        "package_binding_verified": package_binding_verified,
        "research_only_non_actionable_verified": research_boundary_verified,
        "selected_family_schema_verified": family_schema_verified,
        "forbidden_fields": sorted(forbidden),
        "malformed_line_count": malformed_line_count,
        "non_meta_ticker_counts_verified": all(
            ticker_counts[ticker] == expected_ticker_counts[ticker]
            for ticker in TARGET_UNIVERSE
            if ticker != "META"
        ),
        "meta_counts_verified": (
            "META" not in expected_ticker_counts
            or ticker_counts["META"] == expected_ticker_counts["META"]
        ),
    }


def _common_report_boundary(payload: Mapping[str, Any]) -> bool:
    return (
        payload.get("output_label") == execution.OUTPUT_LABEL
        and payload.get("evidence_scope") == execution.EVIDENCE_SCOPE
        and payload.get("selected_vpa_wyckoff_package")
        == execution.PACKAGE_VPA_WYCKOFF_TRANSPARENT_RULE_BASELINE
        and payload.get("predictive_usefulness") == NOT_ACCEPTED
        and payload.get("profitability") == NOT_ACCEPTED
        and payload.get("runtime_use") == NOT_AUTHORIZED
        and payload.get("backtest_execution_authorized") is False
        and payload.get("model_training_authorized") is False
        and payload.get("metric_computation_authorized") is False
        and payload.get("trade_recommendations_generated") is False
    )


def _review_source_outputs(root: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    failures: list[dict[str, Any]] = []
    if not root.is_dir():
        return {}, [_failure("output_root_missing", "source output root is unavailable")]

    missing = [name for name in EXPECTED_OUTPUT_FILENAMES if not (root / name).is_file()]
    if missing:
        return {}, [_failure("source_outputs_missing", "expected outputs are missing", missing=missing)]

    local_before = {name: sha256_file(root / name) for name in EXPECTED_OUTPUT_FILENAMES}
    payloads: dict[str, dict[str, Any]] = {}
    try:
        for name in EXPECTED_OUTPUT_FILENAMES:
            if not name.endswith(".jsonl"):
                payloads[name] = _load_json(root / name)
        inspection = _inspect_rule_values(root / "vpa_wyckoff_rule_values.jsonl")
    except MarketFlowVpaWyckoffRuleBaselineResultsReviewError as exc:
        return {}, [_failure("source_output_invalid", str(exc))]

    source = payloads["vpa_wyckoff_baseline_manifest.json"]
    digest_report = payloads["vpa_wyckoff_digest_manifest.json"]
    recorded_rows = digest_report.get("output_digest_manifest")
    if not isinstance(recorded_rows, list):
        recorded_rows = []
        failures.append(_failure("digest_manifest_invalid", "digest manifest rows are missing"))
    recorded_by_name = {
        row.get("filename"): row for row in recorded_rows if isinstance(row, dict)
    }
    bindings: list[dict[str, Any]] = []
    mismatch_count = 0
    ordinary_match_count = 0
    for name in EXPECTED_OUTPUT_FILENAMES:
        recorded = recorded_by_name.get(name, {})
        kind = recorded.get("digest_kind")
        recorded_sha = recorded.get("sha256")
        local_sha = local_before[name]
        if kind == "FILE_SHA256":
            matched = recorded_sha == local_sha
            ordinary_match_count += int(matched)
        elif name == "vpa_wyckoff_baseline_manifest.json":
            matched = kind == "SELF_REFERENTIAL_EXECUTION_ARTIFACT" and recorded_sha is None
        elif name == "vpa_wyckoff_digest_manifest.json":
            matched = kind == execution.SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE and recorded_sha is None
        else:
            matched = False
        mismatch_count += int(not matched)
        bindings.append({
            "filename": name,
            "local_sha256": local_sha,
            "recorded_sha256": recorded_sha,
            "recorded_digest_kind": kind,
            "verification_status": PASS if matched else FAIL,
        })

    if mismatch_count:
        failures.append(_failure(
            "output_digest_mismatch", "one or more output digests do not match",
            mismatch_count=mismatch_count,
        ))
    if local_before["vpa_wyckoff_rule_values.jsonl"] != EXPECTED_SOURCE_RULE_VALUES_DIGEST:
        failures.append(_failure("rule_values_digest_mismatch", "rule-values digest changed"))

    expected_source_values = {
        "artifact_kind": execution.ARTIFACT_KIND_MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_EXECUTED,
        "execution_status": execution.MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_EXECUTED_RESEARCH_ONLY,
        "execution_scope": execution.VPA_WYCKOFF_RULE_BASELINE_EXECUTION_ONLY_NOT_BACKTEST_NOT_MODEL_TRAINING,
        "marketflow_vpa_wyckoff_rule_baseline_execution_digest": EXPECTED_SOURCE_EXECUTION_DIGEST,
        "vpa_wyckoff_rule_baseline_output_binding_digest": EXPECTED_SOURCE_OUTPUT_BINDING_DIGEST,
        "vpa_wyckoff_rule_values_digest": EXPECTED_SOURCE_RULE_VALUES_DIGEST,
        "source_vpa_wyckoff_rule_baseline_approval_digest": EXPECTED_SOURCE_APPROVAL_DIGEST,
        "source_candidate_review_digest": EXPECTED_SOURCE_CANDIDATE_REVIEW_DIGEST,
        "source_candidate_digest": EXPECTED_SOURCE_CANDIDATE_DIGEST,
        "source_matrix_results_review_digest": EXPECTED_SOURCE_MATRIX_RESULTS_REVIEW_DIGEST,
        "source_matrix_execution_digest": EXPECTED_SOURCE_MATRIX_EXECUTION_DIGEST,
        "source_matrix_output_binding_digest": EXPECTED_SOURCE_MATRIX_OUTPUT_BINDING_DIGEST,
        "source_matrix_rows_digest": EXPECTED_SOURCE_MATRIX_ROWS_DIGEST,
        "source_feature_values_digest": EXPECTED_SOURCE_FEATURE_VALUES_DIGEST,
        "source_target_values_digest": EXPECTED_SOURCE_TARGET_VALUES_DIGEST,
        "source_records_digest": EXPECTED_SOURCE_RECORDS_DIGEST,
        "source_matrix_row_count": EXPECTED_SOURCE_MATRIX_ROW_COUNT,
        "rule_value_row_count": EXPECTED_RULE_VALUE_ROW_COUNT,
        "state_value_row_count": EXPECTED_STATE_VALUE_ROW_COUNT,
        "selected_rule_family_count": len(SELECTED_RULE_FAMILY_IDS),
        "selected_state_family_count": len(SELECTED_STATE_FAMILY_IDS),
        "rule_family_reference_count": EXPECTED_RULE_FAMILY_REFERENCE_COUNT,
        "state_family_reference_count": EXPECTED_STATE_FAMILY_REFERENCE_COUNT,
        "generated_output_count": EXPECTED_OUTPUT_COUNT,
        "expected_output_count": EXPECTED_OUTPUT_COUNT,
        "observed_output_count": EXPECTED_OUTPUT_COUNT,
        "rule_threshold_policy": execution.RULE_THRESHOLD_POLICY,
    }
    source_mismatches = {
        key: {"expected": expected, "actual": source.get(key)}
        for key, expected in expected_source_values.items()
        if source.get(key) != expected
    }
    if source_mismatches:
        failures.append(_failure(
            "source_manifest_mismatch", "source execution manifest changed",
            mismatches=source_mismatches,
        ))

    if digest_report.get("vpa_wyckoff_rule_baseline_output_binding_digest") != EXPECTED_SOURCE_OUTPUT_BINDING_DIGEST:
        failures.append(_failure("output_binding_digest_mismatch", "output binding digest changed"))
    if digest_report.get("manifest_self_reference_policy") != execution.SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE:
        failures.append(_failure("self_reference_policy_mismatch", "digest self-reference policy changed"))

    if inspection["row_count"] != EXPECTED_RULE_VALUE_ROW_COUNT:
        failures.append(_failure("rule_row_count_mismatch", "rule row count changed"))
    if inspection["rule_reference_count"] != EXPECTED_RULE_FAMILY_REFERENCE_COUNT:
        failures.append(_failure("rule_reference_count_mismatch", "rule reference count changed"))
    if inspection["state_reference_count"] != EXPECTED_STATE_FAMILY_REFERENCE_COUNT:
        failures.append(_failure("state_reference_count_mismatch", "state reference count changed"))
    for field in (
        "rule_values_jsonl_schema_verified", "package_binding_verified",
        "research_only_non_actionable_verified", "selected_family_schema_verified",
        "non_meta_ticker_counts_verified", "meta_counts_verified",
    ):
        if inspection[field] is not True:
            failures.append(_failure(field, f"streaming inspection failed: {field}"))
    if inspection["forbidden_fields"] or inspection["malformed_line_count"]:
        failures.append(_failure(
            "rule_values_schema_or_leakage_invalid",
            "rule rows contain malformed or forbidden content",
            forbidden_fields=inspection["forbidden_fields"],
            malformed_line_count=inspection["malformed_line_count"],
        ))

    rule_schema = payloads["vpa_wyckoff_rule_schema.json"]
    state_schema = payloads["vpa_wyckoff_state_schema.json"]
    coverage = payloads["vpa_wyckoff_rule_coverage_report.json"]
    per_ticker = payloads["vpa_wyckoff_per_ticker_report.json"]
    meta = payloads["vpa_wyckoff_meta_limitation_report.json"]
    no_peek = payloads["vpa_wyckoff_no_peek_report.json"]
    operator = payloads["vpa_wyckoff_operator_summary.json"]

    executed_rules = [row.get("rule_family_id") for row in rule_schema.get("executed_rule_families", [])]
    supporting_rules = rule_schema.get("supporting_rule_families", [])
    executed_states = [row.get("state_family_id") for row in state_schema.get("executed_wyckoff_state_families", [])]
    supporting_states = state_schema.get("supporting_wyckoff_state_families", [])
    supporting_not_executed = (
        [row.get("rule_family_id") for row in supporting_rules] == SUPPORTING_RULE_FAMILY_IDS
        and [row.get("state_family_id") for row in supporting_states] == SUPPORTING_STATE_FAMILY_IDS
        and all(row.get("approval_status") == "AVAILABLE_NOT_SELECTED" and row.get("execution_performed") is False for row in supporting_rules + supporting_states)
    )
    coverage_counts = coverage.get("coverage", {})
    coverage_valid = (
        coverage.get("coverage_is_descriptive_not_performance_metric") is True
        and coverage.get("rule_family_reference_count") == EXPECTED_RULE_FAMILY_REFERENCE_COUNT
        and coverage.get("state_family_reference_count") == EXPECTED_STATE_FAMILY_REFERENCE_COUNT
        and set(coverage_counts) == set(SELECTED_RULE_FAMILY_IDS + SELECTED_STATE_FAMILY_IDS)
        and all(sum(values.values()) == EXPECTED_RULE_VALUE_ROW_COUNT for values in coverage_counts.values() if isinstance(values, dict))
    )
    per_ticker_entries = per_ticker.get("per_ticker_execution_entries", [])
    per_ticker_valid = (
        isinstance(per_ticker_entries, list)
        and len(per_ticker_entries) == len(TARGET_UNIVERSE)
        and [row.get("ticker") for row in per_ticker_entries] == TARGET_UNIVERSE
    )
    no_peek_controls = no_peek.get("no_peek_controls", {})
    no_peek_valid = (
        isinstance(no_peek_controls, dict)
        and all(value is True for value in no_peek_controls.values())
        and set(no_peek.get("rule_output_row_fields", [])) == EXPECTED_RULE_ROW_FIELDS
        and set(no_peek.get("forbidden_rule_output_fields", [])) == FORBIDDEN_RULE_OUTPUT_FIELDS
    )
    common_reports = [rule_schema, state_schema, coverage, per_ticker, meta, no_peek, operator, digest_report]
    report_reviews = {
        "common_output_boundary_verified": all(_common_report_boundary(report) for report in common_reports),
        "rule_schema_verified": (
            executed_rules == SELECTED_RULE_FAMILY_IDS
            and rule_schema.get("rule_threshold_policy") == execution.RULE_THRESHOLD_POLICY
        ),
        "state_schema_verified": executed_states == SELECTED_STATE_FAMILY_IDS,
        "coverage_report_verified": coverage_valid,
        "per_ticker_report_verified": per_ticker_valid,
        "meta_limitation_report_verified": (
            meta.get("ticker") == "META"
            and meta.get("historical_record_count") == EXPECTED_RECORD_COUNTS.get("META")
            and meta.get("rule_value_row_count") == EXPECTED_RECORD_COUNTS.get("META", 0) * 15
            and meta.get("state_value_row_count") == EXPECTED_RECORD_COUNTS.get("META", 0) * 15
            and meta.get("meta_reduced_record_count_flag") is True
            and meta.get("repair_or_inference_performed") is False
        ),
        "no_peek_report_verified": no_peek_valid,
        "operator_summary_verified": (
            operator.get("generated_output_count") == EXPECTED_OUTPUT_COUNT
            and operator.get("backtest_or_performance_evaluation_performed") is False
            and operator.get("rule_threshold_policy") == execution.RULE_THRESHOLD_POLICY
        ),
        "digest_manifest_verified": mismatch_count == 0,
        "executed_rule_families_verified": executed_rules == SELECTED_RULE_FAMILY_IDS,
        "executed_state_families_verified": executed_states == SELECTED_STATE_FAMILY_IDS,
        "supporting_families_not_executed": supporting_not_executed,
    }
    failed_report_reviews = [key for key, value in report_reviews.items() if not value]
    if failed_report_reviews:
        failures.append(_failure(
            "report_review_failed", "one or more reports failed review",
            failed_reviews=failed_report_reviews,
        ))

    source_matrix_digest_before = None
    source_matrix_digest_after = None
    if DEFAULT_SOURCE_MATRIX_PATH.is_file():
        source_matrix_digest_before = sha256_file(DEFAULT_SOURCE_MATRIX_PATH)
        source_matrix_digest_after = sha256_file(DEFAULT_SOURCE_MATRIX_PATH)
        if source_matrix_digest_before != EXPECTED_SOURCE_MATRIX_ROWS_DIGEST or source_matrix_digest_after != source_matrix_digest_before:
            failures.append(_failure("source_matrix_digest_mismatch", "source matrix changed"))
    else:
        failures.append(_failure("source_matrix_missing", "bound source matrix is unavailable"))

    local_after = {name: sha256_file(root / name) for name in EXPECTED_OUTPUT_FILENAMES}
    outputs_unchanged = local_after == local_before
    if not outputs_unchanged:
        failures.append(_failure("source_outputs_changed", "source outputs changed during review"))

    return {
        "source": source,
        "payloads": payloads,
        "local_output_digests": local_before,
        "output_digest_bindings": bindings,
        "output_digest_mismatch_count": mismatch_count,
        "recorded_file_digest_match_count": ordinary_match_count,
        "rule_values_inspection": {
            **inspection,
            "rule_values_digest_before_streaming": local_before["vpa_wyckoff_rule_values.jsonl"],
            "rule_values_digest_after_streaming": local_after["vpa_wyckoff_rule_values.jsonl"],
            "rule_values_output_unchanged_during_review": outputs_unchanged,
        },
        "report_reviews": report_reviews,
        "source_matrix_verification": {
            "source_matrix_path": str(DEFAULT_SOURCE_MATRIX_PATH).replace("\\", "/"),
            "digest_before_review": source_matrix_digest_before,
            "digest_after_review": source_matrix_digest_after,
            "source_matrix_output_unchanged_during_review": (
                source_matrix_digest_before == source_matrix_digest_after == EXPECTED_SOURCE_MATRIX_ROWS_DIGEST
            ),
        },
        "source_outputs_unchanged_during_review": outputs_unchanged,
    }, failures


def _closed_boundary() -> dict[str, Any]:
    return {
        "expectancy_backtest_lab_candidate_created": False,
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
        "vpa_wyckoff_rule_baseline_execution_rerun_performed": False,
        "feature_label_matrix_execution_rerun_performed": False,
        "feature_label_matrix_results_review_rerun_performed": False,
        "vpa_wyckoff_candidate_creation_rerun_performed": False,
        "vpa_wyckoff_candidate_review_rerun_performed": False,
        "vpa_wyckoff_approval_rerun_performed": False,
        "raw_provider_payloads_committed": False,
        "api_keys_stored_or_printed": False,
    }


def _blocked_package(root: Path, failures: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_RESULTS_REVIEW_BLOCKED,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_RESULTS_REVIEW_V1,
        "review_status": MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_RESULTS_REVIEW_BLOCKED_MISSING_OR_INVALID_OUTPUTS,
        "review_scope": VPA_WYCKOFF_RULE_BASELINE_RESULTS_REVIEW_ONLY_NOT_BACKTEST_NOT_MODEL_TRAINING,
        "created_offline": True,
        "research_only": True,
        "operator_review_required": True,
        "source_output_root": str(root).replace("\\", "/"),
        "review_failures": failures,
        "vpa_wyckoff_rule_baseline_results_review_created": False,
        "vpa_wyckoff_rule_baseline_results_review_ready": False,
        "ready_for_expectancy_backtest_lab_candidate": False,
        "marketflow_vpa_wyckoff_rule_baseline_results_review_digest": "NOT_CREATED",
        "risk_controls": list(RISK_CONTROLS),
        **_closed_boundary(),
    }


def _per_ticker_entries() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for ticker in TARGET_UNIVERSE:
        historical_count = EXPECTED_RECORD_COUNTS[ticker]
        row_count = historical_count * 15
        row = {
            "ticker": ticker,
            "registry_approval_status": "APPROVED_FOR_RESEARCH_REGISTRY_ONLY",
            "canonical_dataset_status": "FROZEN",
            "historical_record_count": historical_count,
            "meta_reduced_record_count_flag": ticker == "META",
            "vpa_wyckoff_rule_baseline_execution_status": execution.MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_EXECUTED_RESEARCH_ONLY,
            "vpa_wyckoff_rule_baseline_results_review_status": "REVIEWED_RESEARCH_ONLY",
            "selected_vpa_wyckoff_package": execution.PACKAGE_VPA_WYCKOFF_TRANSPARENT_RULE_BASELINE,
            "selected_matrix_package": execution.PACKAGE_EXPECTANCY_TARGET_PROFILE_WIDE_FEATURE_MATRIX,
            "selected_feature_package": execution.PACKAGE_TREND_FLOW_EXPECTANCY_SIGNAL_SET,
            "selected_label_target_package": execution.PACKAGE_EXPECTANCY_PAYOFF_ABSTENTION_LABEL_SET,
            "selected_objective_path": execution.EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT,
            "source_matrix_row_count": row_count,
            "rule_value_row_count": row_count,
            "state_value_row_count": row_count,
            "selected_rule_family_count": len(SELECTED_RULE_FAMILY_IDS),
            "selected_state_family_count": len(SELECTED_STATE_FAMILY_IDS),
            "expectancy_backtest_lab_candidate_created": False,
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
            "source_rule_values_digest": EXPECTED_SOURCE_RULE_VALUES_DIGEST,
            "review_note": (
                "PRESERVE_META_LIMITATION_IN_VPA_WYCKOFF_RULE_BASELINE_RESULTS_REVIEW"
                if ticker == "META" else "STANDARD_HISTORY_PRESERVED"
            ),
        }
        row["per_ticker_vpa_wyckoff_rule_baseline_results_review_digest"] = semantic_digest(row)
        rows.append(row)
    return rows


def _check(check_id: str, passed: bool, message: str) -> dict[str, Any]:
    return {
        "check_id": check_id,
        "status": PASS if passed else FAIL,
        "expected": True,
        "actual": bool(passed),
        "severity": "INFO" if passed else BLOCKER,
        "message": message,
    }


def _build_checklist(review: dict[str, Any]) -> list[dict[str, Any]]:
    inspection = review["rule_values_inspection"]
    reports = review["report_reviews"]
    per_ticker = review["per_ticker_vpa_wyckoff_rule_baseline_results_review_entries"]
    absent = not inspection["forbidden_fields"]
    conditions = {
        "source_execution_digest_bound": review["source_vpa_wyckoff_rule_baseline_execution_digest"] == EXPECTED_SOURCE_EXECUTION_DIGEST,
        "source_output_binding_digest_bound": review["source_vpa_wyckoff_rule_baseline_output_binding_digest"] == EXPECTED_SOURCE_OUTPUT_BINDING_DIGEST,
        "source_rule_values_digest_bound": review["source_vpa_wyckoff_rule_values_digest"] == EXPECTED_SOURCE_RULE_VALUES_DIGEST,
        "source_approval_digest_bound": review["source_vpa_wyckoff_rule_baseline_approval_digest"] == EXPECTED_SOURCE_APPROVAL_DIGEST,
        "source_candidate_review_digest_bound": review["source_candidate_review_digest"] == EXPECTED_SOURCE_CANDIDATE_REVIEW_DIGEST,
        "source_candidate_digest_bound": review["source_candidate_digest"] == EXPECTED_SOURCE_CANDIDATE_DIGEST,
        "source_matrix_results_review_digest_bound": review["source_matrix_results_review_digest"] == EXPECTED_SOURCE_MATRIX_RESULTS_REVIEW_DIGEST,
        "source_matrix_execution_digest_bound": review["source_matrix_execution_digest"] == EXPECTED_SOURCE_MATRIX_EXECUTION_DIGEST,
        "source_matrix_rows_digest_bound": review["source_matrix_rows_digest"] == EXPECTED_SOURCE_MATRIX_ROWS_DIGEST,
        "source_feature_values_digest_bound": review["source_feature_values_digest"] == EXPECTED_SOURCE_FEATURE_VALUES_DIGEST,
        "source_target_values_digest_bound": review["source_target_values_digest"] == EXPECTED_SOURCE_TARGET_VALUES_DIGEST,
        "records_digest_bound": review["source_records_digest"] == EXPECTED_SOURCE_RECORDS_DIGEST,
        "target_universe_12_preserved": review["target_universe"] == TARGET_UNIVERSE,
        "records_digest_preserved": review["records_digest"] == EXPECTED_SOURCE_RECORDS_DIGEST,
        "meta_913_preserved": review["meta_record_count"] == EXPECTED_RECORD_COUNTS.get("META"),
        "selected_vpa_wyckoff_package_preserved": review["selected_vpa_wyckoff_package"] == execution.PACKAGE_VPA_WYCKOFF_TRANSPARENT_RULE_BASELINE,
        "selected_matrix_package_preserved": review["selected_matrix_package"] == execution.PACKAGE_EXPECTANCY_TARGET_PROFILE_WIDE_FEATURE_MATRIX,
        "selected_feature_package_preserved": review["selected_feature_package"] == execution.PACKAGE_TREND_FLOW_EXPECTANCY_SIGNAL_SET,
        "selected_target_package_preserved": review["selected_label_target_package"] == execution.PACKAGE_EXPECTANCY_PAYOFF_ABSTENTION_LABEL_SET,
        "selected_objective_path_preserved": review["selected_objective_path"] == execution.EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT,
        "expected_output_count_10": review["expected_output_count"] == EXPECTED_OUTPUT_COUNT,
        "observed_output_count_10": review["observed_output_count"] == EXPECTED_OUTPUT_COUNT,
        "output_digest_mismatch_count_zero": review["output_digest_mismatch_count"] == 0,
        "rule_values_digest_matches": review["local_output_digests"]["vpa_wyckoff_rule_values.jsonl"] == EXPECTED_SOURCE_RULE_VALUES_DIGEST,
        "rule_values_jsonl_schema_verified": inspection["rule_values_jsonl_schema_verified"],
        "rule_values_count_verified": inspection["row_count"] == EXPECTED_RULE_VALUE_ROW_COUNT,
        "state_values_count_verified": inspection["row_count"] == EXPECTED_STATE_VALUE_ROW_COUNT,
        "source_matrix_row_count_179190": review["source_matrix_row_count"] == EXPECTED_SOURCE_MATRIX_ROW_COUNT,
        "rule_value_row_count_179190": review["rule_value_row_count"] == EXPECTED_RULE_VALUE_ROW_COUNT,
        "state_value_row_count_179190": review["state_value_row_count"] == EXPECTED_STATE_VALUE_ROW_COUNT,
        "selected_rule_family_count_8": review["selected_rule_family_count"] == len(SELECTED_RULE_FAMILY_IDS),
        "selected_state_family_count_6": review["selected_state_family_count"] == len(SELECTED_STATE_FAMILY_IDS),
        "rule_family_reference_count_1433520": review["rule_family_reference_count"] == EXPECTED_RULE_FAMILY_REFERENCE_COUNT,
        "state_family_reference_count_1075140": review["state_family_reference_count"] == EXPECTED_STATE_FAMILY_REFERENCE_COUNT,
        "non_meta_ticker_counts_verified": inspection["non_meta_ticker_counts_verified"],
        "meta_counts_verified": inspection["meta_counts_verified"],
        "rule_threshold_policy_static_not_optimized": review["rule_threshold_policy"] == execution.RULE_THRESHOLD_POLICY,
        "executed_rule_families_verified": reports["executed_rule_families_verified"],
        "executed_state_families_verified": reports["executed_state_families_verified"],
        "supporting_families_not_executed": reports["supporting_families_not_executed"],
        "target_values_absent": absent,
        "target_classes_absent": absent,
        "forward_returns_absent": absent,
        "future_data_absent": absent,
        "prediction_fields_absent": absent,
        "strategy_score_fields_absent": absent,
        "trade_recommendation_fields_absent": absent,
        "broker_order_fields_absent": absent,
        "provider_payload_fields_absent": absent,
        "api_key_fields_absent": absent,
        "digest_manifest_self_reference_policy_verified": review["digest_manifest_self_reference_policy"] == execution.SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE,
        "rule_schema_verified": reports["rule_schema_verified"],
        "state_schema_verified": reports["state_schema_verified"],
        "coverage_report_verified": reports["coverage_report_verified"],
        "per_ticker_report_verified": reports["per_ticker_report_verified"],
        "meta_limitation_report_verified": reports["meta_limitation_report_verified"],
        "no_peek_report_verified": reports["no_peek_report_verified"],
        "operator_summary_verified": reports["operator_summary_verified"],
        "results_review_created_true": review["vpa_wyckoff_rule_baseline_results_review_created"],
        "results_review_ready_true": review["vpa_wyckoff_rule_baseline_results_review_ready"],
        "ready_for_expectancy_backtest_lab_candidate_true": review["ready_for_expectancy_backtest_lab_candidate"],
        "expectancy_backtest_lab_candidate_created_false": not review["expectancy_backtest_lab_candidate_created"],
        "backtest_execution_authorized_false": not review["backtest_execution_authorized"],
        "backtest_execution_performed_false": not review["backtest_execution_performed"],
        "model_training_authorized_false": not review["model_training_authorized"],
        "model_training_performed_false": not review["model_training_performed"],
        "metric_computation_authorized_false": not review["metric_computation_authorized"],
        "metric_computation_performed_false": not review["metric_computation_performed"],
        "strategy_scoring_false": not review["strategy_scoring_performed"],
        "predictive_usefulness_not_accepted": review["predictive_usefulness"] == NOT_ACCEPTED,
        "profitability_not_accepted": review["profitability"] == NOT_ACCEPTED,
        "runtime_not_authorized": review["runtime_use"] == NOT_AUTHORIZED,
        "strategy_not_authorized": review["strategy_use"] == NOT_AUTHORIZED,
        "broker_not_authorized": review["broker_execution"] == NOT_AUTHORIZED,
        "trade_recommendations_false": not review["trade_recommendations_generated"],
        "per_ticker_entries_12": len(per_ticker) == len(TARGET_UNIVERSE),
        "per_ticker_digests_present": all(row.get("per_ticker_vpa_wyckoff_rule_baseline_results_review_digest") for row in per_ticker),
        "provider_requests_made_false": not review["provider_requests_made_in_review"],
        "market_data_acquisition_false": not review["market_data_acquisition_performed_in_review"],
        "dataset_regeneration_false": not review["canonical_dataset_regenerated_in_review"],
        "vpa_wyckoff_rule_baseline_execution_rerun_false": not review["vpa_wyckoff_rule_baseline_execution_rerun_performed"],
        "feature_label_matrix_execution_rerun_false": not review["feature_label_matrix_execution_rerun_performed"],
        "feature_label_matrix_results_review_rerun_false": not review["feature_label_matrix_results_review_rerun_performed"],
        "vpa_wyckoff_candidate_creation_rerun_false": not review["vpa_wyckoff_candidate_creation_rerun_performed"],
        "vpa_wyckoff_candidate_review_rerun_false": not review["vpa_wyckoff_candidate_review_rerun_performed"],
        "vpa_wyckoff_approval_rerun_false": not review["vpa_wyckoff_approval_rerun_performed"],
        "raw_provider_payloads_not_committed": not review["raw_provider_payloads_committed"],
        "api_keys_not_stored_or_printed": not review["api_keys_stored_or_printed"],
        "next_chain_defined": review["next_chain"] == NEXT_CHAIN,
        "next_gates_defined": review["next_gates"] == NEXT_GATES,
        "risk_controls_defined": review["risk_controls"] == RISK_CONTROLS,
        "no_tracked_marketflow_files": review["no_tracked_marketflow_files"],
    }
    return [_check(check_id, conditions[check_id], check_id.replace("_", " ")) for check_id in REQUIRED_CHECK_IDS]


def _ready_review(evidence: dict[str, Any], root: Path) -> dict[str, Any]:
    source = evidence["source"]
    inspection = evidence["rule_values_inspection"]
    forbidden = set(inspection["forbidden_fields"])
    review: dict[str, Any] = {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_RESULTS_REVIEW_PACKAGE,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_RESULTS_REVIEW_V1,
        "review_status": MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_RESULTS_REVIEW_PACKAGE_READY,
        "review_scope": VPA_WYCKOFF_RULE_BASELINE_RESULTS_REVIEW_ONLY_NOT_BACKTEST_NOT_MODEL_TRAINING,
        "created_offline": True,
        "research_only": True,
        "operator_review_required": True,
        "source_output_root": str(root).replace("\\", "/"),
        "source_vpa_wyckoff_rule_baseline_execution_artifact_kind": execution.ARTIFACT_KIND_MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_EXECUTED,
        "source_vpa_wyckoff_rule_baseline_execution_status": execution.MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_EXECUTED_RESEARCH_ONLY,
        "source_vpa_wyckoff_rule_baseline_execution_scope": execution.VPA_WYCKOFF_RULE_BASELINE_EXECUTION_ONLY_NOT_BACKTEST_NOT_MODEL_TRAINING,
        "source_vpa_wyckoff_rule_baseline_execution_digest": EXPECTED_SOURCE_EXECUTION_DIGEST,
        "source_vpa_wyckoff_rule_baseline_output_binding_digest": EXPECTED_SOURCE_OUTPUT_BINDING_DIGEST,
        "source_vpa_wyckoff_rule_values_digest": EXPECTED_SOURCE_RULE_VALUES_DIGEST,
        "source_vpa_wyckoff_rule_baseline_approval_digest": EXPECTED_SOURCE_APPROVAL_DIGEST,
        "source_candidate_review_digest": EXPECTED_SOURCE_CANDIDATE_REVIEW_DIGEST,
        "source_candidate_digest": EXPECTED_SOURCE_CANDIDATE_DIGEST,
        "source_matrix_results_review_digest": EXPECTED_SOURCE_MATRIX_RESULTS_REVIEW_DIGEST,
        "source_matrix_execution_digest": EXPECTED_SOURCE_MATRIX_EXECUTION_DIGEST,
        "source_matrix_output_binding_digest": EXPECTED_SOURCE_MATRIX_OUTPUT_BINDING_DIGEST,
        "source_matrix_rows_digest": EXPECTED_SOURCE_MATRIX_ROWS_DIGEST,
        "source_feature_values_digest": EXPECTED_SOURCE_FEATURE_VALUES_DIGEST,
        "source_target_values_digest": EXPECTED_SOURCE_TARGET_VALUES_DIGEST,
        "source_records_digest": EXPECTED_SOURCE_RECORDS_DIGEST,
        "source_evidence": deepcopy(source.get("source_evidence", {})),
        "dataset_name": "expanded_universe_canonical_dataset_v1",
        "source_profile": "RTH_FULL_SESSION_1D",
        "timeframe": "1d",
        "date_range_start": "2022-01-01",
        "date_range_end": "2025-12-31",
        "target_universe": list(TARGET_UNIVERSE),
        "target_universe_count": len(TARGET_UNIVERSE),
        "total_canonical_record_count": sum(EXPECTED_RECORD_COUNTS.values()),
        "records_digest": EXPECTED_SOURCE_RECORDS_DIGEST,
        "meta_record_count": EXPECTED_RECORD_COUNTS.get("META"),
        "non_meta_record_count": next((count for ticker, count in EXPECTED_RECORD_COUNTS.items() if ticker != "META"), None),
        "meta_reduced_record_count_preserved": True,
        "selected_vpa_wyckoff_package": execution.PACKAGE_VPA_WYCKOFF_TRANSPARENT_RULE_BASELINE,
        "selected_matrix_package": execution.PACKAGE_EXPECTANCY_TARGET_PROFILE_WIDE_FEATURE_MATRIX,
        "selected_matrix_layout": execution.MATRIX_LAYOUT_TARGET_PROFILE_WITH_WIDE_FEATURE_BUNDLE,
        "selected_feature_package": execution.PACKAGE_TREND_FLOW_EXPECTANCY_SIGNAL_SET,
        "selected_label_target_package": execution.PACKAGE_EXPECTANCY_PAYOFF_ABSTENTION_LABEL_SET,
        "selected_objective_path": execution.EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT,
        "vpa_wyckoff_rule_baseline_executed": True,
        "vpa_wyckoff_rule_values_created": True,
        "vpa_wyckoff_state_values_created": True,
        "vpa_wyckoff_baseline_outputs_created": True,
        "vpa_wyckoff_rule_baseline_results_created": True,
        "vpa_wyckoff_rule_baseline_results_review_created": True,
        "vpa_wyckoff_rule_baseline_results_review_ready": True,
        "ready_for_expectancy_backtest_lab_candidate": True,
        "source_matrix_row_count": EXPECTED_SOURCE_MATRIX_ROW_COUNT,
        "rule_value_row_count": EXPECTED_RULE_VALUE_ROW_COUNT,
        "state_value_row_count": EXPECTED_STATE_VALUE_ROW_COUNT,
        "selected_rule_family_count": len(SELECTED_RULE_FAMILY_IDS),
        "selected_state_family_count": len(SELECTED_STATE_FAMILY_IDS),
        "rule_family_reference_count": EXPECTED_RULE_FAMILY_REFERENCE_COUNT,
        "state_family_reference_count": EXPECTED_STATE_FAMILY_REFERENCE_COUNT,
        "expected_output_count": EXPECTED_OUTPUT_COUNT,
        "observed_output_count": len(evidence["local_output_digests"]),
        "output_digest_mismatch_count": evidence["output_digest_mismatch_count"],
        "output_file_inspection_performed": True,
        "local_output_digests": evidence["local_output_digests"],
        "local_output_digest_count": len(evidence["local_output_digests"]),
        "recorded_file_digest_match_count": evidence["recorded_file_digest_match_count"],
        "output_digest_bindings": evidence["output_digest_bindings"],
        "digest_manifest_self_reference_policy": execution.SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE,
        "rule_threshold_policy": execution.RULE_THRESHOLD_POLICY,
        "planned_rule_evaluation_scope": "RESEARCH_ONLY_RULE_TAGGING_NOT_BACKTEST",
        "executed_rule_families": list(SELECTED_RULE_FAMILY_IDS),
        "executed_wyckoff_state_families": list(SELECTED_STATE_FAMILY_IDS),
        "supporting_rule_families_not_executed": list(SUPPORTING_RULE_FAMILY_IDS),
        "supporting_state_families_not_executed": list(SUPPORTING_STATE_FAMILY_IDS),
        "rule_values_jsonl_review": "VERIFIED_RESEARCH_ONLY",
        "rule_schema_review": "VERIFIED",
        "state_schema_review": "VERIFIED",
        "coverage_report_review": "VERIFIED",
        "per_ticker_report_review": "VERIFIED",
        "meta_limitation_report_review": "VERIFIED",
        "no_peek_report_review": "VERIFIED",
        "operator_summary_review": "VERIFIED",
        "digest_manifest_review": "VERIFIED_ZERO_MISMATCHES",
        "rule_values_jsonl_schema_verified": inspection["rule_values_jsonl_schema_verified"],
        "rule_values_count_verified": inspection["row_count"] == EXPECTED_RULE_VALUE_ROW_COUNT,
        "state_values_count_verified": inspection["row_count"] == EXPECTED_STATE_VALUE_ROW_COUNT,
        "per_ticker_rule_counts_verified": inspection["non_meta_ticker_counts_verified"] and inspection["meta_counts_verified"],
        "per_ticker_state_counts_verified": inspection["non_meta_ticker_counts_verified"] and inspection["meta_counts_verified"],
        "meta_limitation_verified": evidence["report_reviews"]["meta_limitation_report_verified"],
        "target_values_present": "target_value" in forbidden,
        "target_classes_present": "target_class" in forbidden,
        "forward_returns_present": "forward_return" in forbidden,
        "future_data_present": bool(
            {"future_label_value", "future_outcome_value", "future_value"}
            & forbidden
        ),
        "prediction_fields_present": bool(
            {"prediction", "prediction_value"} & forbidden
        ),
        "strategy_score_fields_present": "strategy_score" in forbidden,
        "trade_recommendation_fields_present": "trade_recommendation" in forbidden,
        "broker_order_fields_present": bool(
            {"broker_order", "broker_order_id", "order_id"} & forbidden
        ),
        "provider_payload_fields_present": bool({"provider_payload", "raw_provider_payload"} & forbidden),
        "api_key_fields_present": bool({"api_key", "api_keys"} & forbidden),
        "rule_values_inspection": inspection,
        "report_reviews": evidence["report_reviews"],
        "source_matrix_verification": evidence["source_matrix_verification"],
        "source_outputs_unchanged_during_review": evidence["source_outputs_unchanged_during_review"],
        "per_ticker_vpa_wyckoff_rule_baseline_results_review_entries": _per_ticker_entries(),
        "next_chain": list(NEXT_CHAIN),
        "next_gates": list(NEXT_GATES),
        "risk_controls": list(RISK_CONTROLS),
        "no_tracked_marketflow_files": bool(source.get("no_tracked_marketflow_files")),
        **_closed_boundary(),
    }
    review["review_checklist"] = _build_checklist(review)
    passed = sum(row["status"] == PASS for row in review["review_checklist"])
    failed = len(review["review_checklist"]) - passed
    review["review_summary"] = {
        "total_checks": len(review["review_checklist"]),
        "passed_checks": passed,
        "failed_checks": failed,
        "blocker_count": sum(row["severity"] == BLOCKER for row in review["review_checklist"]),
        "vpa_wyckoff_rule_baseline_results_review_created": True,
        "vpa_wyckoff_rule_baseline_results_review_ready": True,
        "ready_for_expectancy_backtest_lab_candidate": True,
        "expectancy_backtest_lab_candidate_created": False,
        "source_matrix_row_count": EXPECTED_SOURCE_MATRIX_ROW_COUNT,
        "rule_value_row_count": EXPECTED_RULE_VALUE_ROW_COUNT,
        "state_value_row_count": EXPECTED_STATE_VALUE_ROW_COUNT,
        "output_digest_mismatch_count": evidence["output_digest_mismatch_count"],
        "backtest_execution_performed": False,
        "model_training_performed": False,
        "metric_computation_performed": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_authorized": False,
        "trade_recommendations_generated": False,
    }
    review["marketflow_vpa_wyckoff_rule_baseline_results_review_digest"] = semantic_digest(review)
    return review


def build_marketflow_vpa_wyckoff_rule_baseline_results_review_v1(
    *, output_root: str | Path | None = None,
) -> dict[str, Any]:
    """Build the deterministic review without rerunning any source execution."""

    root = Path(output_root) if output_root is not None else DEFAULT_OUTPUT_ROOT
    evidence, failures = _review_source_outputs(root)
    if failures:
        return _blocked_package(root, failures)
    review = _ready_review(evidence, root)
    if review["review_summary"]["blocker_count"]:
        return _blocked_package(root, [_failure(
            "review_checklist_blocked", "results-review checklist contains blockers"
        )])
    return review


def validate_marketflow_vpa_wyckoff_rule_baseline_results_review_v1(
    review: dict,
) -> dict[str, Any]:
    """Reject any review that changes evidence or opens adjacent authority."""

    if not isinstance(review, dict):
        raise MarketFlowVpaWyckoffRuleBaselineResultsReviewError("review must be an object")
    if review.get("artifact_kind") == ARTIFACT_KIND_MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_RESULTS_REVIEW_BLOCKED:
        if (
            review.get("review_status")
            != MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_RESULTS_REVIEW_BLOCKED_MISSING_OR_INVALID_OUTPUTS
            or review.get("vpa_wyckoff_rule_baseline_results_review_ready") is not False
            or review.get("ready_for_expectancy_backtest_lab_candidate") is not False
            or review.get("marketflow_vpa_wyckoff_rule_baseline_results_review_digest") != "NOT_CREATED"
        ):
            raise MarketFlowVpaWyckoffRuleBaselineResultsReviewError("invalid blocked review")
        return {
            "status": MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_RESULTS_REVIEW_BLOCKED_VALID,
            "artifact_kind": review["artifact_kind"],
            "blocker_count": len(review.get("review_failures", [])),
        }

    errors: list[str] = []

    def expect(field: str, expected: Any) -> None:
        if review.get(field) != expected:
            errors.append(f"{field} must equal {expected!r}")

    expected_values = {
        "artifact_kind": ARTIFACT_KIND_MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_RESULTS_REVIEW_PACKAGE,
        "schema_version": SCHEMA_VERSION_MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_RESULTS_REVIEW_V1,
        "review_status": MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_RESULTS_REVIEW_PACKAGE_READY,
        "review_scope": VPA_WYCKOFF_RULE_BASELINE_RESULTS_REVIEW_ONLY_NOT_BACKTEST_NOT_MODEL_TRAINING,
        "source_vpa_wyckoff_rule_baseline_execution_digest": EXPECTED_SOURCE_EXECUTION_DIGEST,
        "source_vpa_wyckoff_rule_baseline_output_binding_digest": EXPECTED_SOURCE_OUTPUT_BINDING_DIGEST,
        "source_vpa_wyckoff_rule_values_digest": EXPECTED_SOURCE_RULE_VALUES_DIGEST,
        "source_vpa_wyckoff_rule_baseline_approval_digest": EXPECTED_SOURCE_APPROVAL_DIGEST,
        "selected_vpa_wyckoff_package": execution.PACKAGE_VPA_WYCKOFF_TRANSPARENT_RULE_BASELINE,
        "selected_matrix_package": execution.PACKAGE_EXPECTANCY_TARGET_PROFILE_WIDE_FEATURE_MATRIX,
        "selected_matrix_layout": execution.MATRIX_LAYOUT_TARGET_PROFILE_WITH_WIDE_FEATURE_BUNDLE,
        "selected_feature_package": execution.PACKAGE_TREND_FLOW_EXPECTANCY_SIGNAL_SET,
        "selected_label_target_package": execution.PACKAGE_EXPECTANCY_PAYOFF_ABSTENTION_LABEL_SET,
        "selected_objective_path": execution.EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT,
        "target_universe": TARGET_UNIVERSE,
        "target_universe_count": len(TARGET_UNIVERSE),
        "records_digest": EXPECTED_SOURCE_RECORDS_DIGEST,
        "meta_record_count": EXPECTED_RECORD_COUNTS.get("META"),
        "expected_output_count": EXPECTED_OUTPUT_COUNT,
        "observed_output_count": EXPECTED_OUTPUT_COUNT,
        "output_digest_mismatch_count": 0,
        "source_matrix_row_count": EXPECTED_SOURCE_MATRIX_ROW_COUNT,
        "rule_value_row_count": EXPECTED_RULE_VALUE_ROW_COUNT,
        "state_value_row_count": EXPECTED_STATE_VALUE_ROW_COUNT,
        "selected_rule_family_count": len(SELECTED_RULE_FAMILY_IDS),
        "selected_state_family_count": len(SELECTED_STATE_FAMILY_IDS),
        "rule_family_reference_count": EXPECTED_RULE_FAMILY_REFERENCE_COUNT,
        "state_family_reference_count": EXPECTED_STATE_FAMILY_REFERENCE_COUNT,
        "vpa_wyckoff_rule_baseline_results_review_created": True,
        "vpa_wyckoff_rule_baseline_results_review_ready": True,
        "ready_for_expectancy_backtest_lab_candidate": True,
        "expectancy_backtest_lab_candidate_created": False,
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
        "provider_requests_made_in_review": False,
        "market_data_acquisition_performed_in_review": False,
        "canonical_dataset_regenerated_in_review": False,
        "vpa_wyckoff_rule_baseline_execution_rerun_performed": False,
        "feature_label_matrix_execution_rerun_performed": False,
        "feature_label_matrix_results_review_rerun_performed": False,
        "vpa_wyckoff_candidate_creation_rerun_performed": False,
        "vpa_wyckoff_candidate_review_rerun_performed": False,
        "vpa_wyckoff_approval_rerun_performed": False,
        "target_values_present": False,
        "target_classes_present": False,
        "forward_returns_present": False,
        "future_data_present": False,
        "prediction_fields_present": False,
        "strategy_score_fields_present": False,
        "trade_recommendation_fields_present": False,
        "broker_order_fields_present": False,
        "provider_payload_fields_present": False,
        "api_key_fields_present": False,
        "rule_values_jsonl_schema_verified": True,
        "rule_values_count_verified": True,
        "state_values_count_verified": True,
    }
    for field, expected in expected_values.items():
        expect(field, expected)

    if review.get("risk_controls") != RISK_CONTROLS:
        errors.append("risk_controls must preserve the complete review boundary")
    if not review.get("marketflow_vpa_wyckoff_rule_baseline_results_review_digest"):
        errors.append("review digest is required")
    else:
        payload = deepcopy(review)
        digest = payload.pop("marketflow_vpa_wyckoff_rule_baseline_results_review_digest")
        if digest != semantic_digest(payload):
            errors.append("review digest is invalid")
    checklist = review.get("review_checklist")
    if not isinstance(checklist, list) or {row.get("check_id") for row in checklist if isinstance(row, dict)} != set(REQUIRED_CHECK_IDS) or any(row.get("status") != PASS for row in checklist if isinstance(row, dict)):
        errors.append("complete passing review checklist is required")
    reports = review.get("report_reviews")
    if not isinstance(reports, dict) or not all(reports.get(key) is True for key in (
        "coverage_report_verified", "per_ticker_report_verified",
        "no_peek_report_verified", "rule_schema_verified", "state_schema_verified",
    )):
        errors.append("required output report reviews are missing")
    entries = review.get("per_ticker_vpa_wyckoff_rule_baseline_results_review_entries")
    if not isinstance(entries, list) or len(entries) != len(TARGET_UNIVERSE):
        errors.append("per-ticker review entries are incomplete")
    else:
        for row in entries:
            payload = deepcopy(row)
            digest = payload.pop("per_ticker_vpa_wyckoff_rule_baseline_results_review_digest", None)
            if not digest or digest != semantic_digest(payload):
                errors.append("per-ticker review digest is missing or invalid")
                break
    if errors:
        raise MarketFlowVpaWyckoffRuleBaselineResultsReviewError("; ".join(errors))
    return {
        "status": MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_RESULTS_REVIEW_VALID,
        "artifact_kind": review["artifact_kind"],
        "review_status": review["review_status"],
        "review_scope": review["review_scope"],
        "total_checks": review["review_summary"]["total_checks"],
        "passed_checks": review["review_summary"]["passed_checks"],
        "failed_checks": review["review_summary"]["failed_checks"],
        "blocker_count": review["review_summary"]["blocker_count"],
        "marketflow_vpa_wyckoff_rule_baseline_results_review_digest": review["marketflow_vpa_wyckoff_rule_baseline_results_review_digest"],
    }


def build_marketflow_vpa_wyckoff_rule_baseline_results_review_markdown_v1(
    review: dict,
) -> str:
    """Render the review package as an operator-readable Markdown report."""

    title = "# MarketFlow VPA/Wyckoff Rule Baseline Results Review v1"
    if review.get("artifact_kind") == ARTIFACT_KIND_MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_RESULTS_REVIEW_BLOCKED:
        return "\n".join([
            title, "", "## Review Status", "",
            f"`{review.get('review_status')}`", "",
            "## Guardrails", "", "Source evidence was not regenerated or fabricated.", "",
        ])
    summary = review["review_summary"]
    sections = [
        ("VPA/Wyckoff Rule Baseline Results Review v1", [f"Status: `{review['review_status']}`."]),
        ("Source VPA/Wyckoff Execution", [f"Execution digest: `{review['source_vpa_wyckoff_rule_baseline_execution_digest']}`."]),
        ("Bound Evidence", ["The execution, output-binding, rule-values, approval, matrix, feature, target, and records digest chain is bound."]),
        ("Dataset and Universe", [f"`{review['dataset_name']}` preserves {review['target_universe_count']} ordered tickers and META 913."]),
        ("Output Verification", [f"{review['observed_output_count']} outputs verified with {review['output_digest_mismatch_count']} mismatches."]),
        ("Selected VPA/Wyckoff Package", [f"`{review['selected_vpa_wyckoff_package']}`."]),
        ("Rule Threshold Policy", [f"`{review['rule_threshold_policy']}`."]),
        ("Executed Rule Families Review", [f"All {review['selected_rule_family_count']} selected rule families verified."]),
        ("Executed Wyckoff State Families Review", [f"All {review['selected_state_family_count']} selected state families verified."]),
        ("Rule Values Review", [f"{review['rule_value_row_count']} research-only rule rows verified by streaming inspection."]),
        ("State Values Review", [f"{review['state_value_row_count']} state rows and {review['state_family_reference_count']} references verified."]),
        ("No-Peek and Leakage Review", ["Target outcomes, future values, predictions, scores, recommendations, orders, provider payloads, and API keys are absent."]),
        ("Coverage Report Review", ["Descriptive coverage was verified and is not performance evidence."]),
        ("Per-Ticker Report Review", [f"{len(review['per_ticker_vpa_wyckoff_rule_baseline_results_review_entries'])} per-ticker entries verified."]),
        ("META Limitation Review", ["META remains at 913 records and 13,695 rule/state rows without repair or inference."]),
        ("Output Digest Manifest", [f"Self-reference policy: `{review['digest_manifest_self_reference_policy']}`."]),
        ("Next Chain", review["next_chain"]),
        ("Next Gates", review["next_gates"]),
        ("Risk Controls", review["risk_controls"]),
        ("Predictive Usefulness Boundary", ["Predictive usefulness remains not accepted."]),
        ("Profitability Boundary", ["Profitability remains not accepted."]),
        ("Runtime Boundary", ["Runtime, strategy, paper trading, and broker execution remain unauthorized."]),
        ("Checklist Summary", [f"{summary['passed_checks']} / {summary['total_checks']} checks passed; {summary['blocker_count']} blockers."]),
        ("Guardrails", ["This review creates no backtest candidate, backtest, model, metric, score, recommendation, acceptance, runtime authority, or trading authority."]),
    ]
    lines = [title, ""]
    for heading, values in sections:
        lines.extend([f"## {heading}", ""])
        lines.extend(f"- {value}" for value in values)
        lines.append("")
    return "\n".join(lines)


def write_marketflow_vpa_wyckoff_rule_baseline_results_review_v1(
    output_dir: str | Path,
    *,
    output_root: str | Path | None = None,
) -> dict[str, Any]:
    """Write only the review JSON and Markdown to an explicitly supplied directory."""

    destination = Path(output_dir)
    destination.mkdir(parents=True, exist_ok=True)
    review = build_marketflow_vpa_wyckoff_rule_baseline_results_review_v1(
        output_root=output_root
    )
    json_path = destination / "marketflow_vpa_wyckoff_rule_baseline_results_review_v1.json"
    markdown_path = destination / "marketflow_vpa_wyckoff_rule_baseline_results_review_v1.md"
    json_path.write_bytes(canonical_json_bytes(review))
    markdown_path.write_text(
        build_marketflow_vpa_wyckoff_rule_baseline_results_review_markdown_v1(review),
        encoding="utf-8",
    )
    return {
        "review": review,
        "json_path": str(json_path),
        "markdown_path": str(markdown_path),
    }
