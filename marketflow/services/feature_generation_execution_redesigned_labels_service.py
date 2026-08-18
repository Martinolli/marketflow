"""Deterministic offline feature generation using frozen redesigned-label evidence."""

from __future__ import annotations

from collections import defaultdict
from copy import deepcopy
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path
from statistics import median, pstdev
from typing import Any
import json

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import feature_generation_approval_redesigned_labels_service as approval_service


ARTIFACT_KIND_FEATURE_GENERATION_EXECUTED_USING_REDESIGNED_LABELS = "FEATURE_GENERATION_EXECUTED_USING_REDESIGNED_LABELS"
ARTIFACT_KIND_FEATURE_GENERATION_BLOCKED_USING_REDESIGNED_LABELS = "FEATURE_GENERATION_BLOCKED_USING_REDESIGNED_LABELS"
FEATURE_GENERATION_EXECUTED_USING_REDESIGNED_LABELS_RESEARCH_ONLY = "FEATURE_GENERATION_EXECUTED_USING_REDESIGNED_LABELS_RESEARCH_ONLY"
FEATURE_GENERATION_BLOCKED_MISSING_OR_INVALID_SOURCE_EVIDENCE = "FEATURE_GENERATION_BLOCKED_MISSING_OR_INVALID_SOURCE_EVIDENCE"
SCHEMA_VERSION = "feature_generation_executed_using_redesigned_labels_v1"
DEFAULT_BRANCH = "feature/feature-generation-execution-redesigned-labels-v1"
DEFAULT_BASE_COMMIT = "1b539d71d83082f3544c1110129f2ccd5b521300"
DEFAULT_CANONICAL_ROOT = Path(".marketflow/canonical_datasets/expanded_universe_v1")
DEFAULT_LABEL_ROOT = Path(".marketflow/redesigned_label_generation/expanded_universe_v1")
DEFAULT_OUTPUT_ROOT = Path(".marketflow/feature_generation_using_redesigned_labels/expanded_universe_v1")
EXPECTED_APPROVAL_DIGEST = "595bb9685936979810cfe6e3a814ea9ef38e0e3d89b804426a2d540ec77471c1"
EXPECTED_RECORDS_DIGEST = approval_service.EXPECTED_RECORDS_DIGEST
EXPECTED_LABEL_VALUES_DIGEST = approval_service.EXPECTED_LABEL_VALUES_DIGEST
TARGET_UNIVERSE = list(approval_service.TARGET_UNIVERSE)
GROUP_IDS = list(approval_service.review_service.candidate_service.PLANNED_FEATURE_GROUP_IDS)
FAMILY_IDS = list(approval_service.review_service.candidate_service.PLANNED_FEATURE_FAMILY_IDS)
SCHEMA_FIELDS = list(approval_service.review_service.candidate_service.FEATURE_SCHEMA_FIELDS)
GROUP_TO_FAMILY = {
    group_id: family_id
    for family_id, groups in approval_service.review_service.candidate_service.FEATURE_GROUPS_BY_FAMILY.items()
    for group_id, _sensitive, _note in groups
}
OUTPUT_LABEL = "RESEARCH_ONLY_NON_ACTIONABLE"
EVIDENCE_SCOPE = "FEATURE_GENERATION_USING_REDESIGNED_LABELS_RESEARCH_ONLY"
OUTPUT_FILENAMES = [
    "feature_generation_execution_manifest.json",
    "feature_generation_input_manifest.json",
    "feature_values.jsonl",
    "feature_family_coverage_report.json",
    "feature_group_generation_report.json",
    "feature_schema_contract_report.json",
    "feature_label_alignment_report.json",
    "feature_quality_report.json",
    "per_ticker_feature_summary.json",
    "meta_limitation_feature_handling_report.json",
    "feature_generation_digest_manifest.json",
    "operator_review_summary.json",
]


class FeatureGenerationExecutionRedesignedLabelsError(ValueError):
    """Raised when executed output violates its research-only contract."""


def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _file_digest(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _jsonl_bytes(rows: list[dict[str, Any]]) -> bytes:
    return b"".join(canonical_json_bytes(row) for row in rows)


def _common() -> dict[str, Any]:
    return {
        "output_label": OUTPUT_LABEL,
        "evidence_scope": EVIDENCE_SCOPE,
        "dataset_name": "expanded_universe_canonical_dataset_v1",
        "records_digest": EXPECTED_RECORDS_DIGEST,
        "label_values_digest": EXPECTED_LABEL_VALUES_DIGEST,
        "feature_generation_approved": True,
        "feature_generation_authorized": True,
        "redesigned_feature_generation_authorized": True,
        "ready_for_feature_generation_execution_using_redesigned_labels": True,
        "feature_generation_performed": True,
        "redesigned_feature_generation_performed": True,
        "feature_values_created": True,
        "additional_predictive_evidence_execution_candidate_created": False,
        "additional_predictive_evidence_executed": False,
        "metric_recomputation_performed": False,
        "model_training_performed": False,
        "predictive_usefulness": "not accepted",
        "profitability": "not accepted",
        "runtime_use": "NOT_AUTHORIZED",
        "strategy_use": "NOT_AUTHORIZED",
        "paper_trading": "NOT_AUTHORIZED",
        "broker_execution": "NOT_AUTHORIZED",
        "trade_recommendations_generated": False,
    }


def _blocked(reason: str) -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_FEATURE_GENERATION_BLOCKED_USING_REDESIGNED_LABELS,
        "schema_version": SCHEMA_VERSION,
        "execution_status": FEATURE_GENERATION_BLOCKED_MISSING_OR_INVALID_SOURCE_EVIDENCE,
        "created_offline": True,
        "research_only": True,
        "block_reason": reason,
        "feature_generation_digest": "NOT_CREATED",
        "feature_generation_performed": False,
        "redesigned_feature_generation_performed": False,
        "feature_values_created": False,
        "generated_output_count": 0,
        "provider_requests_made_in_execution": False,
        "market_data_acquisition_performed_in_execution": False,
        "metric_recomputation_performed": False,
        "model_training_performed": False,
        "additional_predictive_evidence_execution_candidate_created": False,
        "additional_predictive_evidence_executed": False,
        "predictive_usefulness": "not accepted",
        "profitability": "not accepted",
        "runtime_use": "NOT_AUTHORIZED",
        "strategy_use": "NOT_AUTHORIZED",
        "paper_trading": "NOT_AUTHORIZED",
        "broker_execution": "NOT_AUTHORIZED",
        "trade_recommendations_generated": False,
    }


def _verify_sources(canonical_root: Path, label_root: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]]] | None:
    canonical_files = {
        "canonical_dataset_generation_run_manifest.json", "canonical_dataset_source_evidence_manifest.json",
        "canonical_dataset_schema_contract.json", "canonical_dataset_records.jsonl",
        "per_ticker_canonical_dataset_summary.json", "canonical_dataset_data_quality_report.json",
        "canonical_dataset_digest_manifest.json", "canonical_dataset_failure_reason_inventory.json", "operator_review_summary.json",
    }
    label_files = {
        "redesigned_label_generation_execution_manifest.json", "redesigned_label_generation_input_manifest.json",
        "redesigned_label_values.jsonl", "redesigned_label_family_coverage_report.json",
        "redesigned_threshold_generation_report.json", "redesigned_horizon_generation_report.json",
        "redesigned_label_availability_report.json", "per_ticker_redesigned_label_summary.json",
        "meta_limitation_preservation_report.json", "redesigned_label_generation_digest_manifest.json", "operator_review_summary.json",
    }
    if not all((canonical_root / name).is_file() for name in canonical_files):
        return None
    if not all((label_root / name).is_file() for name in label_files):
        return None
    records_path = canonical_root / "canonical_dataset_records.jsonl"
    labels_path = label_root / "redesigned_label_values.jsonl"
    if _file_digest(records_path) != EXPECTED_RECORDS_DIGEST or _file_digest(labels_path) != EXPECTED_LABEL_VALUES_DIGEST:
        return None
    records = _read_jsonl(records_path)
    labels = _read_jsonl(labels_path)
    counts = {ticker: sum(row.get("ticker") == ticker for row in records) for ticker in TARGET_UNIVERSE}
    if len(records) != 11946 or counts != {ticker: (913 if ticker == "META" else 1003) for ticker in TARGET_UNIVERSE}:
        return None
    if len(labels) != 143352 or sum(bool(row.get("label_available")) for row in labels) != 142200:
        return None
    return records, labels


def _label_metadata(labels: list[dict[str, Any]]) -> dict[tuple[str, str], dict[str, Any]]:
    grouped: dict[tuple[str, str], dict[str, Any]] = {}
    for row in labels:
        key = (row["ticker"], row["date"])
        item = grouped.setdefault(key, {"families": set(), "horizons": set(), "available": False, "unavailable": False, "window_partition": row["window_partition"]})
        item["families"].add(row["label_family"])
        item["horizons"].add(row["horizon"])
        item["available"] = item["available"] or bool(row["label_available"])
        item["unavailable"] = item["unavailable"] or not bool(row["label_available"])
    return grouped


def _numeric(row: dict[str, Any], field: str) -> float | None:
    try:
        return float(row[field])
    except (KeyError, TypeError, ValueError):
        return None


def _round(value: float | int | bool | None) -> Decimal | int | bool | None:
    return Decimal(f"{value:.12f}") if isinstance(value, float) else value


def _generate_feature_rows(records: list[dict[str, Any]], labels: list[dict[str, Any]]) -> list[dict[str, Any]]:
    metadata = _label_metadata(labels)
    by_ticker: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in records:
        by_ticker[record["ticker"]].append(record)
    calculations: dict[tuple[str, int], dict[str, tuple[Any, str, int]]] = {}
    date_returns: dict[str, list[tuple[str, float]]] = defaultdict(list)
    date_momentum: dict[str, list[tuple[str, float]]] = defaultdict(list)
    for ticker in TARGET_UNIVERSE:
        rows = by_ticker[ticker]
        closes = [_numeric(row, "close") for row in rows]
        volumes = [_numeric(row, "volume") for row in rows]
        returns: list[float | None] = []
        momentums: list[float | None] = []
        for index, row in enumerate(rows):
            close = closes[index]
            previous = closes[index - 1] if index else None
            ret = None if close is None or previous in (None, 0) else close / previous - 1
            momentum = None if index < 5 or close is None or closes[index - 5] in (None, 0) else close / closes[index - 5] - 1
            returns.append(ret)
            momentums.append(momentum)
            if ret is not None:
                date_returns[row["date"]].append((ticker, ret))
            if momentum is not None:
                date_momentum[row["date"]].append((ticker, momentum))
        for index, row in enumerate(rows):
            close, open_, high, low, volume = (_numeric(row, name) for name in ("close", "open", "high", "low", "volume"))
            ret = returns[index]
            momentum = momentums[index]
            trailing_returns = [value for value in returns[max(0, index - 4): index + 1] if value is not None]
            trailing_volumes = [value for value in volumes[max(0, index - 19): index + 1] if value is not None]
            volatility = pstdev(trailing_returns) if len(trailing_returns) >= 2 else None
            slope = None if index < 4 or close is None or closes[index - 4] is None else (close - closes[index - 4]) / 4
            volume_effort = None if volume is None or len(trailing_volumes) < 2 or median(trailing_volumes) == 0 else volume / median(trailing_volumes)
            range_value = None if None in (high, low, close) or close == 0 else (high - low) / close
            spread = None if None in (close, open_, high, low, volume) or high == low else ((close - open_) / (high - low)) * (1 if volume >= median(trailing_volumes) else -1)
            missing = int(any(value is None for value in (open_, high, low, close, volume)))
            calendar = datetime.fromisoformat(row["date"])
            calculations[(ticker, index)] = {
                "ohlcv_return_lags": (ret, "AVAILABLE" if ret is not None else "INSUFFICIENT_HISTORY", 1),
                "ohlcv_range_features": (range_value, "AVAILABLE" if range_value is not None else "SOURCE_OHLC_UNAVAILABLE", 0),
                "volume_effort_features": (volume_effort, "AVAILABLE" if volume_effort is not None else "INSUFFICIENT_HISTORY", min(index + 1, 20)),
                "price_volume_spread_features": (spread, "AVAILABLE" if spread is not None else "SOURCE_OHLCV_UNAVAILABLE", 0),
                "realized_volatility_windows": (volatility, "AVAILABLE" if volatility is not None else "INSUFFICIENT_HISTORY", min(index + 1, 5)),
                "momentum_return_windows": (momentum, "AVAILABLE" if momentum is not None else "INSUFFICIENT_HISTORY", 5),
                "trend_slope_candidates": (slope, "AVAILABLE" if slope is not None else "INSUFFICIENT_HISTORY", 5),
                "calendar_month_weekday_features": (calendar.month * 10 + calendar.weekday(), "AVAILABLE", 0),
                "session_sequence_features": (index, "AVAILABLE", index + 1),
                "missingness_indicators": (missing, "AVAILABLE", 0),
                "meta_limitation_flag": (ticker == "META", "AVAILABLE", 0),
                "regime_interaction_candidates": (None if momentum is None or volatility is None else momentum * volatility, "AVAILABLE" if momentum is not None and volatility is not None else "INSUFFICIENT_HISTORY", 5),
                "baseline_error_context_candidates": (None, "BASELINE_ERROR_CONTEXT_REQUIRES_FUTURE_OUTCOME_REVIEW", 0),
            }
    return_medians = {date: median(value for _ticker, value in values) for date, values in date_returns.items()}
    momentum_ranks: dict[tuple[str, str], float] = {}
    for date, values in date_momentum.items():
        ordered = sorted(values, key=lambda item: (item[1], item[0]))
        denominator = max(1, len(ordered) - 1)
        for rank, (ticker, _value) in enumerate(ordered):
            momentum_ranks[(ticker, date)] = rank / denominator
    output: list[dict[str, Any]] = []
    for ticker in TARGET_UNIVERSE:
        for index, record in enumerate(by_ticker[ticker]):
            meta = metadata[(ticker, record["date"])]
            ret = calculations[(ticker, index)]["ohlcv_return_lags"][0]
            relative = None if ret is None else ret - return_medians[record["date"]]
            rank = momentum_ranks.get((ticker, record["date"]))
            calculations[(ticker, index)].update({
                "relative_strength_to_universe_median": (relative, "AVAILABLE" if relative is not None else "INSUFFICIENT_HISTORY", 1),
                "cross_sectional_rank_candidates": (rank, "AVAILABLE" if rank is not None else "INSUFFICIENT_HISTORY_OR_UNIVERSE_COVERAGE", 5),
                "label_horizon_alignment_flags": (int(bool(meta["horizons"])), "AVAILABLE", 0),
                "label_family_alignment_flags": (int(bool(meta["families"])), "AVAILABLE", 0),
            })
            for group_id in GROUP_IDS:
                value, reason, history = calculations[(ticker, index)][group_id]
                output.append({
                    "ticker": ticker, "date": record["date"], "record_index_for_ticker": index,
                    "window_partition": meta["window_partition"], "feature_family": GROUP_TO_FAMILY[group_id],
                    "feature_group": group_id, "feature_name": f"{group_id}_v1", "feature_value": _round(value),
                    "feature_available": value is not None, "availability_reason": reason,
                    "source_history_window": history,
                    "label_family_alignment": sorted(meta["families"]),
                    "label_horizon_alignment": sorted(meta["horizons"]),
                    "meta_reduced_record_count_flag": ticker == "META", "research_only": True, "non_actionable": True,
                })
    return output


def _execution_digest_payload(artifact: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(artifact)
    payload.pop("feature_generation_execution_digest", None)
    return payload


def feature_generation_execution_digest_v1(artifact: dict[str, Any]) -> str:
    return semantic_digest(_execution_digest_payload(artifact))


def _artifact(timestamp: str, rows: list[dict[str, Any]], values_digest: str) -> dict[str, Any]:
    available = sum(row["feature_available"] for row in rows)
    artifact = {
        "artifact_kind": ARTIFACT_KIND_FEATURE_GENERATION_EXECUTED_USING_REDESIGNED_LABELS,
        "schema_version": SCHEMA_VERSION,
        "execution_status": FEATURE_GENERATION_EXECUTED_USING_REDESIGNED_LABELS_RESEARCH_ONLY,
        "branch": DEFAULT_BRANCH, "base_commit": DEFAULT_BASE_COMMIT, "run_timestamp_utc": timestamp,
        "created_offline": True, "research_only": True, "operator_review_required": True,
        "provider_requests_made_in_execution": False, "live_provider_transport_enabled_in_execution": False,
        "market_data_acquisition_performed_in_execution": False, "dataset_generation_performed_in_execution": False,
        "canonical_dataset_regenerated_in_execution": False, "redesigned_label_regeneration_performed": False,
        "metric_recomputation_performed": False, "model_training_performed": False,
        "raw_provider_payloads_committed": False, "api_keys_stored_or_printed": False,
        **_common(),
        "feature_generation_results_created": True,
        "feature_generation_manifest_created": True, "feature_generation_input_manifest_created": True,
        "feature_values_output_created": True, "feature_family_coverage_report_created": True,
        "feature_group_generation_report_created": True, "feature_schema_contract_report_created": True,
        "feature_label_alignment_report_created": True, "feature_quality_report_created": True,
        "per_ticker_feature_summary_created": True, "meta_limitation_feature_handling_report_created": True,
        "feature_generation_digest_manifest_created": True, "operator_review_summary_created": True,
        "additional_predictive_evidence_execution_authorized": False,
        "generated_output_count": 12, "feature_family_count": 10, "feature_group_count": 17,
        "feature_schema_field_count": 16, "feature_value_row_count": len(rows),
        "target_universe": TARGET_UNIVERSE, "target_universe_count": 12,
        "total_canonical_record_count": 11946, "meta_record_count": 913, "non_meta_record_count": 1003,
        "meta_reduced_record_count_preserved": True,
        "available_feature_value_count": available, "unavailable_feature_value_count": len(rows) - available,
        "feature_values_digest": values_digest,
        "feature_generation_approval_using_redesigned_labels_digest": EXPECTED_APPROVAL_DIGEST,
        "feature_generation_candidate_using_redesigned_labels_review_package_digest": approval_service.EXPECTED_CANDIDATE_REVIEW_DIGEST,
        "feature_generation_candidate_using_redesigned_labels_digest": approval_service.EXPECTED_CANDIDATE_DIGEST,
        "feature_predictive_evidence_planning_approval_using_redesigned_labels_digest": approval_service.EXPECTED_PLANNING_APPROVAL_DIGEST,
        "redesigned_label_generation_results_review_package_digest": approval_service.EXPECTED_RESULTS_REVIEW_DIGEST,
        "redesigned_label_generation_execution_digest": approval_service.EXPECTED_EXECUTION_DIGEST,
        "redesigned_label_generation_approval_digest": approval_service.EXPECTED_REDESIGNED_LABEL_APPROVAL_DIGEST,
        "research_registry_approval_digest": approval_service.EXPECTED_RESEARCH_REGISTRY_DIGEST,
        "records_digest": EXPECTED_RECORDS_DIGEST, "label_values_digest": EXPECTED_LABEL_VALUES_DIGEST,
        "predictive_usefulness_acceptance_ready": False, "predictive_usefulness_acceptance_recommended": False,
        "predictive_usefulness_acceptance_candidate_created": False, "profitability_acceptance_ready": False,
        "profitability_acceptance_recommended": False, "runtime_migration_approved": False,
        "runtime_migration_active": False, "automatic_stitching": False, "new_strategy_scoring_performed": False,
        "failure_count": 0, "warning_count": 0,
    }
    artifact["feature_generation_execution_digest"] = feature_generation_execution_digest_v1(artifact)
    return artifact


def _write_outputs(output_root: Path, artifact: dict[str, Any], rows: list[dict[str, Any]]) -> None:
    output_root.mkdir(parents=True, exist_ok=True)
    if any((output_root / name).exists() for name in OUTPUT_FILENAMES):
        raise FeatureGenerationExecutionRedesignedLabelsError("feature generation output already exists")
    common = _common()
    ticker_summary = [{"ticker": ticker, "canonical_record_count": 913 if ticker == "META" else 1003, "feature_value_row_count": 15521 if ticker == "META" else 17051, "meta_reduced_record_count_flag": ticker == "META"} for ticker in TARGET_UNIVERSE]
    reports: dict[str, bytes] = {
        "feature_generation_input_manifest.json": canonical_json_bytes({**common, "source_roots_verified": True, "source_approval_digest": EXPECTED_APPROVAL_DIGEST}),
        "feature_values.jsonl": _jsonl_bytes(rows),
        "feature_family_coverage_report.json": canonical_json_bytes({**common, "feature_families": FAMILY_IDS, "feature_family_count": 10}),
        "feature_group_generation_report.json": canonical_json_bytes({**common, "feature_groups": GROUP_IDS, "feature_group_count": 17}),
        "feature_schema_contract_report.json": canonical_json_bytes({**common, "schema_fields": SCHEMA_FIELDS, "feature_schema_field_count": 16}),
        "feature_label_alignment_report.json": canonical_json_bytes({**common, "label_values_used_as_features": False, "forward_returns_used_as_features": False, "threshold_values_used_as_features": False, "metadata_only": True}),
        "feature_quality_report.json": canonical_json_bytes({**common, "feature_value_row_count": 203082, "available_feature_value_count": artifact["available_feature_value_count"], "unavailable_feature_value_count": artifact["unavailable_feature_value_count"], "failure_count": 0, "warning_count": 0}),
        "per_ticker_feature_summary.json": canonical_json_bytes({**common, "per_ticker_summary": ticker_summary}),
        "meta_limitation_feature_handling_report.json": canonical_json_bytes({**common, "meta_record_count": 913, "meta_feature_value_row_count": 15521, "meta_limitation_preserved": True, "records_repaired_or_inferred": False}),
        "operator_review_summary.json": canonical_json_bytes({**common, "execution_status": artifact["execution_status"], "feature_generation_execution_digest": artifact["feature_generation_execution_digest"], "predictive_evidence_execution_authorized": False}),
        "feature_generation_execution_manifest.json": canonical_json_bytes(artifact),
    }
    digest_rows = [{"filename": name, "digest_kind": "FILE_SHA256", "sha256": sha256_bytes(payload)} for name, payload in reports.items()]
    digest_rows.append({"filename": "feature_generation_digest_manifest.json", "digest_kind": "SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE", "sha256": None})
    reports["feature_generation_digest_manifest.json"] = canonical_json_bytes({**common, "output_digest_manifest": digest_rows})
    for name in OUTPUT_FILENAMES:
        (output_root / name).write_bytes(reports[name])


def execute_feature_generation_using_redesigned_labels_v1(*, canonical_root: str | Path | None = None, label_root: str | Path | None = None, output_root: str | Path | None = None, run_timestamp_utc: str | None = None) -> dict[str, Any]:
    """Generate history-only research features from verified frozen local inputs."""
    canonical_path = Path(canonical_root) if canonical_root is not None else DEFAULT_CANONICAL_ROOT
    label_path = Path(label_root) if label_root is not None else DEFAULT_LABEL_ROOT
    output_path = Path(output_root) if output_root is not None else DEFAULT_OUTPUT_ROOT
    verified = _verify_sources(canonical_path, label_path)
    if verified is None:
        return _blocked("MISSING_OR_INVALID_SOURCE_EVIDENCE")
    records, labels = verified
    rows = _generate_feature_rows(records, labels)
    if len(rows) != 203082:
        return _blocked("FEATURE_ROW_COUNT_MISMATCH")
    values_bytes = _jsonl_bytes(rows)
    artifact = _artifact(run_timestamp_utc or _now(), rows, sha256_bytes(values_bytes))
    validate_feature_generation_executed_using_redesigned_labels_v1(artifact)
    _write_outputs(output_path, artifact, rows)
    return artifact


def validate_feature_generation_executed_using_redesigned_labels_v1(artifact: dict) -> dict[str, Any]:
    """Validate the exact executed research-only boundary."""
    if not isinstance(artifact, dict):
        raise FeatureGenerationExecutionRedesignedLabelsError("artifact must be an object")
    expected = {
        "artifact_kind": ARTIFACT_KIND_FEATURE_GENERATION_EXECUTED_USING_REDESIGNED_LABELS,
        "execution_status": FEATURE_GENERATION_EXECUTED_USING_REDESIGNED_LABELS_RESEARCH_ONLY,
        "feature_generation_approval_using_redesigned_labels_digest": EXPECTED_APPROVAL_DIGEST,
        "feature_generation_approved": True, "feature_generation_authorized": True,
        "redesigned_feature_generation_authorized": True,
        "ready_for_feature_generation_execution_using_redesigned_labels": True,
        "feature_generation_performed": True, "redesigned_feature_generation_performed": True,
        "feature_values_created": True, "generated_output_count": 12,
        "target_universe": TARGET_UNIVERSE, "target_universe_count": 12,
        "records_digest": EXPECTED_RECORDS_DIGEST, "label_values_digest": EXPECTED_LABEL_VALUES_DIGEST,
        "meta_record_count": 913, "feature_family_count": 10, "feature_group_count": 17,
        "feature_schema_field_count": 16, "feature_value_row_count": 203082,
        "metric_recomputation_performed": False, "model_training_performed": False,
        "additional_predictive_evidence_execution_candidate_created": False,
        "additional_predictive_evidence_executed": False, "predictive_usefulness": "not accepted",
        "profitability": "not accepted", "runtime_use": "NOT_AUTHORIZED",
        "strategy_use": "NOT_AUTHORIZED", "paper_trading": "NOT_AUTHORIZED",
        "broker_execution": "NOT_AUTHORIZED", "trade_recommendations_generated": False,
    }
    for field, value in expected.items():
        if artifact.get(field) != value:
            raise FeatureGenerationExecutionRedesignedLabelsError(f"{field} mismatch")
    for field in ("feature_values_digest", "feature_generation_execution_digest"):
        if not isinstance(artifact.get(field), str) or len(artifact[field]) != 64:
            raise FeatureGenerationExecutionRedesignedLabelsError(f"{field} missing")
    if artifact["available_feature_value_count"] + artifact["unavailable_feature_value_count"] != 203082:
        raise FeatureGenerationExecutionRedesignedLabelsError("feature availability counts mismatch")
    if artifact["feature_generation_execution_digest"] != feature_generation_execution_digest_v1(artifact):
        raise FeatureGenerationExecutionRedesignedLabelsError("execution digest mismatch")
    return {"status": artifact["execution_status"], "feature_generation_execution_digest": artifact["feature_generation_execution_digest"], "feature_values_digest": artifact["feature_values_digest"], "feature_value_row_count": 203082, "generated_output_count": 12, "runtime_authorized": False}


def build_feature_generation_execution_status_markdown_v1(artifact: dict) -> str:
    validation = validate_feature_generation_executed_using_redesigned_labels_v1(artifact)
    sections = ["Title", "Feature Generation Execution Using Redesigned Labels", "Source Approval", "Dataset and Universe", "Source Redesigned Label Profile", "Feature Generation Policy", "Generated Feature Families", "Feature Group Summary", "Feature Schema Contract", "Feature / Label Alignment Review", "Feature Quality Summary", "Per-Ticker Feature Summary", "META Limitation Preservation", "Output Digest Manifest", "Execution Boundary", "Predictive Evidence Boundary", "Predictive Usefulness Boundary", "Profitability Boundary", "Runtime Boundary", "Checklist Summary", "Guardrails"]
    lines = ["# MarketFlow Feature Generation Execution Status", ""]
    for section in sections:
        lines.extend([f"## {section}", f"- Research-only execution `{validation['feature_generation_execution_digest']}`; feature rows `{artifact['feature_value_row_count']}`, feature values digest `{artifact['feature_values_digest']}`. No predictive, acceptance, runtime, or trading authority was created.", ""])
    return "\n".join(lines)
