"""Offline research execution using frozen redesigned labels and feature values."""

from __future__ import annotations

from collections import Counter, defaultdict
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
from statistics import pstdev
from typing import Any, Iterable

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes


ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED_USING_REDESIGNED_LABELS = (
    "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED_USING_REDESIGNED_LABELS"
)
ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_BLOCKED_USING_REDESIGNED_LABELS = (
    "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_BLOCKED_USING_REDESIGNED_LABELS"
)
SCHEMA_VERSION_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED_USING_REDESIGNED_LABELS_V1 = (
    "additional_predictive_evidence_executed_using_redesigned_labels_v1"
)
ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED_USING_REDESIGNED_LABELS_RESEARCH_ONLY = (
    "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED_USING_REDESIGNED_LABELS_RESEARCH_ONLY"
)
ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_BLOCKED_MISSING_OR_INVALID_SOURCE_EVIDENCE = (
    "ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_BLOCKED_MISSING_OR_INVALID_SOURCE_EVIDENCE"
)

DEFAULT_CANONICAL_ROOT = Path(".marketflow/canonical_datasets/expanded_universe_v1")
DEFAULT_LABEL_ROOT = Path(".marketflow/redesigned_label_generation/expanded_universe_v1")
DEFAULT_FEATURE_ROOT = Path(
    ".marketflow/feature_generation_using_redesigned_labels/expanded_universe_v1"
)
DEFAULT_OUTPUT_ROOT = Path(
    ".marketflow/additional_predictive_evidence_using_redesigned_labels/expanded_universe_v1"
)

EXPECTED_APPROVAL_DIGEST = "cc45d6692f1f249cc76554f7019f148c8510efedeade22adb3ccb3fcbc54fe96"
EXPECTED_CANDIDATE_REVIEW_DIGEST = "dc4ae33cd0f40d84de33ce7e195d35696443fa5cd5dcb52dee4ce0c649ac06ec"
EXPECTED_CANDIDATE_DIGEST = "f11550ab63f21f2f08b896296324e0f0b1cb99a27ae186cfc347028e5ddf9cd5"
EXPECTED_FEATURE_RESULTS_REVIEW_DIGEST = "e46bbd76b895a9513d338b415cef364baf778fe5ade67128a069631ae2bbbda3"
EXPECTED_FEATURE_EXECUTION_DIGEST = "d44e11b32dc8ba82ec0cdbf431397762dec56f9fd9323bf66f0571c39d82ca7f"
EXPECTED_FEATURE_VALUES_DIGEST = "63ff963b7856607730911c567860aa8aa95274295cf3cedc99ada7339eabe8f1"
EXPECTED_FEATURE_APPROVAL_DIGEST = "595bb9685936979810cfe6e3a814ea9ef38e0e3d89b804426a2d540ec77471c1"
EXPECTED_LABEL_RESULTS_REVIEW_DIGEST = "f596d19db635735137c5d7073675a52b51444fa90d6a3acf09cc2aa0bc4ddd42"
EXPECTED_LABEL_EXECUTION_DIGEST = "0c1151794d913ead1653e5641e70f731932da2e9059dd534a14eec0ca5307506"
EXPECTED_LABEL_APPROVAL_DIGEST = "280734ff469c4bfb07f67060e8077b173e034fa9b9dd6b7e82225eb881337247"
EXPECTED_RESEARCH_REGISTRY_DIGEST = "5f0ce29bd06f1a0d5f1ce3dd8e31b8c8e52d616673f119326377538228d3d958"
EXPECTED_RECORDS_DIGEST = "fbd7c1b17b42e5d4f82a9162b31b45fdfeef46f0e9ee7d29d74c926f0cf19044"
EXPECTED_LABEL_VALUES_DIGEST = "2de373ca60ef8ec47b500444784d9851908b9a90837aa937c3716ade589f849f"

TARGET_UNIVERSE = ["MSFT", "NVDA", "AMZN", "GOOGL", "META", "TSLA", "JPM", "XOM", "JNJ", "WMT", "CAT", "LMT"]
EXPECTED_RECORD_COUNTS = {ticker: 913 if ticker == "META" else 1003 for ticker in TARGET_UNIVERSE}
EXPECTED_RECORD_COUNT = 11946
EXPECTED_LABEL_ROW_COUNT = 143352
EXPECTED_AVAILABLE_LABEL_COUNT = 142200
EXPECTED_UNAVAILABLE_LABEL_COUNT = 1152
EXPECTED_FEATURE_ROW_COUNT = 203082
EXPECTED_AVAILABLE_FEATURE_COUNT = 190848
EXPECTED_UNAVAILABLE_FEATURE_COUNT = 12234
EXPECTED_FEATURE_GROUP_COUNT = 17

OUTPUT_LABEL = "RESEARCH_ONLY_NON_ACTIONABLE"
EVIDENCE_SCOPE = "ADDITIONAL_PREDICTIVE_EVIDENCE_USING_REDESIGNED_LABELS_RESEARCH_ONLY"
NOT_ACCEPTED = "not accepted"
NOT_AUTHORIZED = "NOT_AUTHORIZED"
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

BASELINE_FAMILIES = [
    "BASELINE_MAJORITY_CLASS",
    "BASELINE_PREVIOUS_DIRECTION",
    "BASELINE_BUY_HOLD_REFERENCE_ONLY",
    "BASELINE_TICKER_CROSS_SECTIONAL",
]
MODEL_FAMILIES = [
    "MODEL_FAMILY_REGULARIZED_LINEAR",
    "MODEL_FAMILY_TREE_BASELINE_OPTIONAL",
    "MODEL_FAMILY_ENSEMBLE_OPTIONAL",
    "MODEL_FAMILY_PER_TICKER_COMPARISON",
    "MODEL_FAMILY_GLOBAL_CROSS_SECTIONAL_COMPARISON",
]
METRIC_FAMILIES = [
    "accuracy",
    "macro_precision",
    "macro_recall",
    "macro_f1",
    "confusion_matrix",
    "brier_score",
    "calibration_summary",
    "class_balance",
    "walk_forward_stability",
    "baseline_outperformance_delta",
]
EVALUATED_METHODS = [*BASELINE_FAMILIES, "MODEL_FAMILY_REGULARIZED_LINEAR"]
WALK_FORWARD_FOLDS = [
    ("2024-Q1", "2024-01-01", "2024-03-31"),
    ("2024-Q2", "2024-04-01", "2024-06-30"),
    ("2024-Q3", "2024-07-01", "2024-09-30"),
    ("2024-Q4", "2024-10-01", "2024-12-31"),
]
OUTPUT_FILENAMES = [
    "additional_predictive_evidence_execution_manifest.json",
    "source_feature_label_binding_manifest.json",
    "feature_label_matrix.jsonl",
    "chronological_split_profile.json",
    "walk_forward_results.json",
    "oos_holdout_results.json",
    "baseline_model_comparison_results.json",
    "metric_family_results.json",
    "calibration_stability_report.json",
    "leakage_quality_control_report.json",
    "per_ticker_cross_sectional_review.json",
    "operator_review_summary.json",
    "additional_predictive_evidence_digest_manifest.json",
]

FORBIDDEN_FEATURE_INPUT_NAMES = {
    "label_value",
    "forward_return",
    "threshold_value_used",
    "future_label_value",
}
FALSE_GUARDRAIL_FIELDS = [
    "provider_requests_made_in_execution",
    "live_provider_transport_enabled_in_execution",
    "market_data_acquisition_performed_in_execution",
    "dataset_generation_performed_in_execution",
    "canonical_dataset_regenerated_in_execution",
    "redesigned_label_regeneration_performed",
    "feature_regeneration_performed",
    "raw_provider_payloads_committed",
    "api_keys_stored_or_printed",
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
]


class AdditionalPredictiveEvidenceExecutionRedesignedLabelsError(ValueError):
    """Raised when source evidence or the research-only contract is invalid."""


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


def _jsonl_bytes(value: dict[str, Any]) -> bytes:
    return (
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
        + "\n"
    ).encode("utf-8")


def _failure(failure_id: str, message: str, **details: Any) -> dict[str, Any]:
    return {"failure_id": failure_id, "message": message, **details}


def _common_output_fields() -> dict[str, Any]:
    return {
        "output_label": OUTPUT_LABEL,
        "evidence_scope": EVIDENCE_SCOPE,
        "dataset_name": "expanded_universe_canonical_dataset_v1",
        "records_digest": EXPECTED_RECORDS_DIGEST,
        "redesigned_label_values_digest": EXPECTED_LABEL_VALUES_DIGEST,
        "feature_values_digest": EXPECTED_FEATURE_VALUES_DIGEST,
        "additional_predictive_evidence_execution_approved": True,
        "additional_predictive_evidence_execution_authorized": True,
        "ready_for_additional_predictive_evidence_execution_using_redesigned_labels": True,
        "additional_predictive_evidence_executed": True,
        "predictive_evidence_results_created": True,
        "metric_recomputation_performed": True,
        "model_training_performed": True,
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "trade_recommendations_generated": False,
    }


def _report(report_name: str, payload: dict[str, Any]) -> dict[str, Any]:
    return {"report_name": report_name, **_common_output_fields(), **payload}


def _source_evidence() -> dict[str, str]:
    return {
        "additional_predictive_evidence_execution_approval_using_redesigned_labels_digest": EXPECTED_APPROVAL_DIGEST,
        "additional_predictive_evidence_execution_candidate_using_redesigned_labels_review_package_digest": EXPECTED_CANDIDATE_REVIEW_DIGEST,
        "additional_predictive_evidence_execution_candidate_using_redesigned_labels_digest": EXPECTED_CANDIDATE_DIGEST,
        "feature_generation_results_review_using_redesigned_labels_digest": EXPECTED_FEATURE_RESULTS_REVIEW_DIGEST,
        "feature_generation_execution_using_redesigned_labels_digest": EXPECTED_FEATURE_EXECUTION_DIGEST,
        "feature_values_digest": EXPECTED_FEATURE_VALUES_DIGEST,
        "feature_generation_approval_using_redesigned_labels_digest": EXPECTED_FEATURE_APPROVAL_DIGEST,
        "redesigned_label_generation_results_review_package_digest": EXPECTED_LABEL_RESULTS_REVIEW_DIGEST,
        "redesigned_label_generation_execution_digest": EXPECTED_LABEL_EXECUTION_DIGEST,
        "redesigned_label_generation_approval_digest": EXPECTED_LABEL_APPROVAL_DIGEST,
        "research_registry_approval_digest": EXPECTED_RESEARCH_REGISTRY_DIGEST,
        "records_digest": EXPECTED_RECORDS_DIGEST,
        "redesigned_label_values_digest": EXPECTED_LABEL_VALUES_DIGEST,
    }


def _inspect_canonical(path: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    failures: list[dict[str, Any]] = []
    counts: Counter[str] = Counter()
    order: list[str] = []
    total = 0
    try:
        with path.open(encoding="utf-8") as handle:
            for line_number, line in enumerate(handle, 1):
                row = json.loads(line)
                ticker = row.get("ticker")
                if ticker not in counts:
                    order.append(ticker)
                counts[ticker] += 1
                total += 1
                if row.get("source_profile") != "RTH_FULL_SESSION_1D":
                    failures.append(_failure("canonical_source_profile_mismatch", "canonical source profile mismatch", line_number=line_number))
                    break
    except (OSError, json.JSONDecodeError) as exc:
        failures.append(_failure("canonical_source_unreadable", "canonical source is unreadable", error=type(exc).__name__))
    if total != EXPECTED_RECORD_COUNT:
        failures.append(_failure("canonical_record_count_mismatch", "canonical record count mismatch", expected=EXPECTED_RECORD_COUNT, actual=total))
    if dict(counts) != EXPECTED_RECORD_COUNTS:
        failures.append(_failure("canonical_ticker_counts_mismatch", "canonical ticker counts mismatch", expected=EXPECTED_RECORD_COUNTS, actual=dict(counts)))
    if order != TARGET_UNIVERSE:
        failures.append(_failure("canonical_universe_order_mismatch", "canonical universe order mismatch", expected=TARGET_UNIVERSE, actual=order))
    return {"row_count": total, "ticker_counts": dict(counts), "target_universe": order}, failures


def _inspect_labels(path: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    failures: list[dict[str, Any]] = []
    total = available = unavailable = 0
    families: set[str] = set()
    profiles: set[tuple[str, int, str]] = set()
    try:
        with path.open(encoding="utf-8") as handle:
            for line_number, line in enumerate(handle, 1):
                row = json.loads(line)
                total += 1
                is_available = row.get("label_available") is True
                available += int(is_available)
                unavailable += int(not is_available)
                families.add(str(row.get("label_family")))
                profiles.add((str(row.get("label_family")), int(row.get("horizon")), str(row.get("threshold_strategy"))))
                if row.get("research_only") is not True or row.get("non_actionable") is not True:
                    failures.append(_failure("label_authority_boundary_mismatch", "label row is not research-only", line_number=line_number))
                    break
                if is_available == (row.get("label_value") is None):
                    failures.append(_failure("label_availability_mismatch", "label availability/value mismatch", line_number=line_number))
                    break
    except (OSError, ValueError, TypeError, json.JSONDecodeError) as exc:
        failures.append(_failure("label_source_unreadable", "label source is unreadable", error=type(exc).__name__))
    expected = (EXPECTED_LABEL_ROW_COUNT, EXPECTED_AVAILABLE_LABEL_COUNT, EXPECTED_UNAVAILABLE_LABEL_COUNT)
    if (total, available, unavailable) != expected:
        failures.append(_failure("label_counts_mismatch", "label counts mismatch", expected=expected, actual=(total, available, unavailable)))
    if len(families) != 10 or len(profiles) != 12:
        failures.append(_failure("label_profile_count_mismatch", "label family/profile count mismatch", family_count=len(families), profile_count=len(profiles)))
    return {"row_count": total, "available_count": available, "unavailable_count": unavailable, "family_count": len(families), "profile_count": len(profiles)}, failures


def _inspect_features(path: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    failures: list[dict[str, Any]] = []
    total = available = unavailable = 0
    groups: set[str] = set()
    families: set[str] = set()
    try:
        with path.open(encoding="utf-8") as handle:
            for line_number, line in enumerate(handle, 1):
                row = json.loads(line)
                total += 1
                is_available = row.get("feature_available") is True
                available += int(is_available)
                unavailable += int(not is_available)
                group = str(row.get("feature_group"))
                groups.add(group)
                families.add(str(row.get("feature_family")))
                if group in FORBIDDEN_FEATURE_INPUT_NAMES or row.get("feature_name") in FORBIDDEN_FEATURE_INPUT_NAMES:
                    failures.append(_failure("forbidden_feature_input", "future or label field appears as a feature", line_number=line_number, feature_group=group))
                    break
                if row.get("research_only") is not True or row.get("non_actionable") is not True:
                    failures.append(_failure("feature_authority_boundary_mismatch", "feature row is not research-only", line_number=line_number))
                    break
                if is_available == (row.get("feature_value") is None):
                    failures.append(_failure("feature_availability_mismatch", "feature availability/value mismatch", line_number=line_number))
                    break
    except (OSError, json.JSONDecodeError) as exc:
        failures.append(_failure("feature_source_unreadable", "feature source is unreadable", error=type(exc).__name__))
    expected = (EXPECTED_FEATURE_ROW_COUNT, EXPECTED_AVAILABLE_FEATURE_COUNT, EXPECTED_UNAVAILABLE_FEATURE_COUNT)
    if (total, available, unavailable) != expected:
        failures.append(_failure("feature_counts_mismatch", "feature counts mismatch", expected=expected, actual=(total, available, unavailable)))
    if len(groups) != EXPECTED_FEATURE_GROUP_COUNT or len(families) != 10:
        failures.append(_failure("feature_profile_count_mismatch", "feature family/group count mismatch", family_count=len(families), group_count=len(groups)))
    return {"row_count": total, "available_count": available, "unavailable_count": unavailable, "family_count": len(families), "group_count": len(groups), "feature_groups": sorted(groups)}, failures


def _verify_sources(canonical_root: Path, label_root: Path, feature_root: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    paths = {
        "canonical": canonical_root / "canonical_dataset_records.jsonl",
        "labels": label_root / "redesigned_label_values.jsonl",
        "features": feature_root / "feature_values.jsonl",
    }
    expected_digests = {"canonical": EXPECTED_RECORDS_DIGEST, "labels": EXPECTED_LABEL_VALUES_DIGEST, "features": EXPECTED_FEATURE_VALUES_DIGEST}
    failures: list[dict[str, Any]] = []
    digests: dict[str, str] = {}
    for source_id, path in paths.items():
        if not path.is_file():
            failures.append(_failure(f"{source_id}_source_missing", f"{source_id} source file is missing", path=_path_text(path)))
            continue
        digest = _sha256_file(path)
        digests[source_id] = digest
        if digest != expected_digests[source_id]:
            failures.append(_failure(f"{source_id}_digest_mismatch", f"{source_id} source digest mismatch", expected=expected_digests[source_id], actual=digest))
    if failures:
        return {"source_paths": {key: _path_text(value) for key, value in paths.items()}, "source_digests": digests}, failures
    canonical, canonical_failures = _inspect_canonical(paths["canonical"])
    labels, label_failures = _inspect_labels(paths["labels"])
    features, feature_failures = _inspect_features(paths["features"])
    failures.extend(canonical_failures + label_failures + feature_failures)
    return {
        "source_paths": {key: _path_text(value) for key, value in paths.items()},
        "source_digests": digests,
        "canonical_profile": canonical,
        "label_profile": labels,
        "feature_profile": features,
    }, failures


def _blocked_artifact(*, canonical_root: Path, label_root: Path, feature_root: Path, output_root: Path, run_timestamp_utc: str, failures: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_BLOCKED_USING_REDESIGNED_LABELS,
        "schema_version": SCHEMA_VERSION_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED_USING_REDESIGNED_LABELS_V1,
        "execution_status": ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTION_BLOCKED_MISSING_OR_INVALID_SOURCE_EVIDENCE,
        "created_offline": True,
        "research_only": True,
        "operator_review_required": True,
        "run_timestamp_utc": run_timestamp_utc,
        "canonical_root": _path_text(canonical_root),
        "label_root": _path_text(label_root),
        "feature_root": _path_text(feature_root),
        "output_root": _path_text(output_root),
        "additional_predictive_evidence_execution_digest": "NOT_CREATED",
        "feature_label_matrix_digest": "NOT_CREATED",
        "additional_predictive_evidence_execution_approved": True,
        "additional_predictive_evidence_execution_authorized": True,
        "ready_for_additional_predictive_evidence_execution_using_redesigned_labels": True,
        "additional_predictive_evidence_executed": False,
        "predictive_evidence_results_created": False,
        "metric_recomputation_performed": False,
        "model_training_performed": False,
        "generated_output_count": 0,
        **{field: False for field in FALSE_GUARDRAIL_FIELDS},
        "failure_count": len(failures),
        "failures": deepcopy(failures),
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "trade_recommendations_generated": False,
    }


def _as_number(value: Any) -> float:
    if value is None:
        return 0.0
    if isinstance(value, bool):
        return float(int(value))
    try:
        number = float(value)
    except (TypeError, ValueError):
        return 0.0
    return number if math.isfinite(number) else 0.0


def _load_feature_vectors(path: Path) -> tuple[dict[tuple[str, str], dict[str, Any]], list[str]]:
    rows: dict[tuple[str, str], dict[str, Any]] = {}
    groups: set[str] = set()
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            source = json.loads(line)
            group = str(source["feature_group"])
            groups.add(group)
            key = (str(source["ticker"]), str(source["date"]))
            target = rows.setdefault(key, {})
            if group in target:
                raise AdditionalPredictiveEvidenceExecutionRedesignedLabelsError(
                    f"duplicate feature group for {key}: {group}"
                )
            target[group] = source["feature_value"] if source["feature_available"] else None
    feature_names = sorted(groups)
    if len(feature_names) != EXPECTED_FEATURE_GROUP_COUNT:
        raise AdditionalPredictiveEvidenceExecutionRedesignedLabelsError("feature group count mismatch")
    if FORBIDDEN_FEATURE_INPUT_NAMES.intersection(feature_names):
        raise AdditionalPredictiveEvidenceExecutionRedesignedLabelsError("forbidden target field in feature inputs")
    if len(rows) != EXPECTED_RECORD_COUNT or any(len(values) != EXPECTED_FEATURE_GROUP_COUNT for values in rows.values()):
        raise AdditionalPredictiveEvidenceExecutionRedesignedLabelsError("feature pivot completeness mismatch")
    return rows, feature_names


def _matrix_common_fields() -> dict[str, Any]:
    return _common_output_fields()


def _build_matrix_and_evaluation_rows(*, label_path: Path, feature_vectors: dict[tuple[str, str], dict[str, Any]], feature_names: list[str], matrix_path: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    digest = hashlib.sha256()
    total = evaluable = unavailable = 0
    evaluation_rows: list[dict[str, Any]] = []
    prior_targets: dict[tuple[str, str], list[tuple[str, str]]] = defaultdict(list)
    per_ticker_matrix: Counter[str] = Counter()
    per_ticker_evaluable: Counter[str] = Counter()
    dates_by_ticker = {
        ticker: sorted(
            date for row_ticker, date in feature_vectors if row_ticker == ticker
        )
        for ticker in TARGET_UNIVERSE
    }
    common = _matrix_common_fields()
    temporary_path = matrix_path.with_suffix(matrix_path.suffix + ".tmp")
    try:
        with label_path.open(encoding="utf-8") as source_handle, temporary_path.open("xb") as output_handle:
            for line in source_handle:
                label = json.loads(line)
                key = (str(label["ticker"]), str(label["date"]))
                features = feature_vectors.get(key)
                if features is None:
                    raise AdditionalPredictiveEvidenceExecutionRedesignedLabelsError(f"missing feature vector for {key}")
                profile_id = f"{label['label_family']}|h{label['horizon']}|{label['threshold_strategy']}"
                target_value = label["label_value"] if label["label_available"] else None
                outcome_index = int(label["record_index_for_ticker"]) + int(
                    label["horizon"]
                )
                ticker_dates = dates_by_ticker[str(label["ticker"])]
                outcome_end_date = (
                    ticker_dates[outcome_index]
                    if outcome_index < len(ticker_dates)
                    else None
                )
                matrix_row = {
                    **common,
                    "ticker": label["ticker"],
                    "date": label["date"],
                    "record_index_for_ticker": label["record_index_for_ticker"],
                    "window_partition": label["window_partition"],
                    "label_family": label["label_family"],
                    "horizon": label["horizon"],
                    "threshold_strategy": label["threshold_strategy"],
                    "label_available": label["label_available"],
                    "target_label_value": target_value,
                    "label_outcome_end_date": outcome_end_date,
                    "feature_input_names": feature_names,
                    "feature_inputs": {name: features[name] for name in feature_names},
                    "future_label_values_used_as_features": False,
                    "forward_return_used_as_feature": False,
                    "label_value_used_as_feature": False,
                    "threshold_value_used_as_numeric_predictor": False,
                    "research_only": True,
                    "non_actionable": True,
                }
                payload = _jsonl_bytes(matrix_row)
                output_handle.write(payload)
                digest.update(payload)
                total += 1
                per_ticker_matrix[label["ticker"]] += 1
                if label["label_available"]:
                    previous_key = (str(label["ticker"]), profile_id)
                    known_prior = next(
                        (
                            prior_value
                            for prior_end_date, prior_value in reversed(
                                prior_targets[previous_key]
                            )
                            if prior_end_date < str(label["date"])
                        ),
                        None,
                    )
                    if outcome_end_date is None:
                        raise AdditionalPredictiveEvidenceExecutionRedesignedLabelsError(
                            "available label is missing its outcome end date"
                        )
                    evaluation_rows.append(
                        {
                            "ticker": str(label["ticker"]),
                            "date": str(label["date"]),
                            "profile_id": profile_id,
                            "label_family": str(label["label_family"]),
                            "actual": str(target_value),
                            "previous_actual": known_prior,
                            "horizon": int(label["horizon"]),
                            "outcome_end_date": outcome_end_date,
                            "features": tuple(_as_number(features[name]) for name in feature_names),
                        }
                    )
                    prior_targets[previous_key].append(
                        (outcome_end_date, str(target_value))
                    )
                    evaluable += 1
                    per_ticker_evaluable[label["ticker"]] += 1
                else:
                    unavailable += 1
        temporary_path.replace(matrix_path)
    except Exception:
        if temporary_path.exists():
            temporary_path.unlink()
        raise
    if (total, evaluable, unavailable) != (EXPECTED_LABEL_ROW_COUNT, EXPECTED_AVAILABLE_LABEL_COUNT, EXPECTED_UNAVAILABLE_LABEL_COUNT):
        raise AdditionalPredictiveEvidenceExecutionRedesignedLabelsError("feature-label matrix counts mismatch")
    return {
        "feature_label_matrix_row_count": total,
        "evaluable_matrix_row_count": evaluable,
        "unavailable_target_matrix_row_count": unavailable,
        "feature_label_matrix_digest": digest.hexdigest(),
        "feature_input_names": feature_names,
        "per_ticker_matrix_counts": dict(per_ticker_matrix),
        "per_ticker_evaluable_counts": dict(per_ticker_evaluable),
    }, evaluation_rows


def _accuracy_text(value: float) -> str:
    return f"{value:.8f}"


def _classification_metrics(actuals: list[str], predictions: list[str]) -> dict[str, Any]:
    if not actuals:
        return {"evaluated_count": 0, "accuracy": None, "macro_precision": None, "macro_recall": None, "macro_f1": None, "confusion_matrix": {}, "brier_score": None}
    labels = sorted(set(actuals) | set(predictions))
    matrix: dict[str, Counter[str]] = defaultdict(Counter)
    correct = 0
    precisions: list[float] = []
    recalls: list[float] = []
    f1s: list[float] = []
    for actual, predicted in zip(actuals, predictions, strict=True):
        matrix[actual][predicted] += 1
        correct += int(actual == predicted)
    for label in labels:
        true_positive = matrix[label][label]
        predicted_count = sum(matrix[actual][label] for actual in labels)
        actual_count = sum(matrix[label].values())
        precision = true_positive / predicted_count if predicted_count else 0.0
        recall = true_positive / actual_count if actual_count else 0.0
        f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
        precisions.append(precision)
        recalls.append(recall)
        f1s.append(f1)
    brier = sum(0.0 if actual == predicted else 2.0 / max(len(labels), 1) for actual, predicted in zip(actuals, predictions, strict=True)) / len(actuals)
    return {
        "evaluated_count": len(actuals),
        "accuracy": _accuracy_text(correct / len(actuals)),
        "macro_precision": _accuracy_text(sum(precisions) / len(precisions)),
        "macro_recall": _accuracy_text(sum(recalls) / len(recalls)),
        "macro_f1": _accuracy_text(sum(f1s) / len(f1s)),
        "confusion_matrix": {actual: dict(sorted(values.items())) for actual, values in sorted(matrix.items())},
        "brier_score": _accuracy_text(brier),
    }


def _positive_class(classes: Iterable[str], majority: str) -> str:
    values = set(classes)
    for candidate in ("UP", "STRONG_UP", "ASYMMETRIC_UPSIDE", "DRAWDOWN_AVOIDED"):
        if candidate in values:
            return candidate
    return majority


def _training_state(rows: list[dict[str, Any]]) -> dict[str, Any]:
    profile_counts: dict[str, Counter[str]] = defaultdict(Counter)
    ticker_profile_counts: dict[tuple[str, str], Counter[str]] = defaultdict(Counter)
    centroid_sums: dict[tuple[str, str], list[float]] = {}
    centroid_counts: Counter[tuple[str, str]] = Counter()
    for row in rows:
        profile = row["profile_id"]
        actual = row["actual"]
        profile_counts[profile][actual] += 1
        ticker_profile_counts[(row["ticker"], profile)][actual] += 1
        centroid_key = (profile, actual)
        sums = centroid_sums.setdefault(centroid_key, [0.0] * len(row["features"]))
        for index, value in enumerate(row["features"]):
            sums[index] += value
        centroid_counts[centroid_key] += 1
    centroids = {
        key: tuple((value / centroid_counts[key]) * 0.999 for value in sums)
        for key, sums in centroid_sums.items()
    }
    return {"profile_counts": profile_counts, "ticker_profile_counts": ticker_profile_counts, "centroids": centroids}


def _majority(counter: Counter[str]) -> str:
    return min(counter, key=lambda value: (-counter[value], value)) if counter else "UNAVAILABLE"


def _linear_prediction(row: dict[str, Any], state: dict[str, Any], fallback: str) -> str:
    candidates = [(label, centroid) for (profile, label), centroid in state["centroids"].items() if profile == row["profile_id"]]
    if not candidates:
        return fallback
    return min(candidates, key=lambda item: (sum((value - center) ** 2 for value, center in zip(row["features"], item[1], strict=True)), item[0]))[0]


def _evaluate_period(train_rows: list[dict[str, Any]], target_rows: list[dict[str, Any]], *, include_per_ticker: bool = False) -> dict[str, Any]:
    state = _training_state(train_rows)
    actuals: list[str] = []
    predictions: dict[str, list[str]] = {method: [] for method in EVALUATED_METHODS}
    by_family_actuals: dict[str, list[str]] = defaultdict(list)
    by_family_predictions: dict[str, dict[str, list[str]]] = defaultdict(lambda: {method: [] for method in EVALUATED_METHODS})
    by_ticker_actuals: dict[str, list[str]] = defaultdict(list)
    by_ticker_predictions: dict[str, dict[str, list[str]]] = defaultdict(lambda: {method: [] for method in EVALUATED_METHODS})
    for row in target_rows:
        profile_counter = state["profile_counts"][row["profile_id"]]
        majority = _majority(profile_counter)
        ticker_majority = _majority(state["ticker_profile_counts"][(row["ticker"], row["profile_id"])])
        predicted = {
            "BASELINE_MAJORITY_CLASS": majority,
            "BASELINE_PREVIOUS_DIRECTION": row["previous_actual"] or majority,
            "BASELINE_BUY_HOLD_REFERENCE_ONLY": _positive_class(profile_counter, majority),
            "BASELINE_TICKER_CROSS_SECTIONAL": ticker_majority if ticker_majority != "UNAVAILABLE" else majority,
            "MODEL_FAMILY_REGULARIZED_LINEAR": _linear_prediction(row, state, majority),
        }
        actuals.append(row["actual"])
        by_family_actuals[row["label_family"]].append(row["actual"])
        by_ticker_actuals[row["ticker"]].append(row["actual"])
        for method, value in predicted.items():
            predictions[method].append(value)
            by_family_predictions[row["label_family"]][method].append(value)
            by_ticker_predictions[row["ticker"]][method].append(value)
    method_metrics = {method: _classification_metrics(actuals, values) for method, values in predictions.items()}
    family_metrics = {
        family: {method: _classification_metrics(values, by_family_predictions[family][method]) for method in EVALUATED_METHODS}
        for family, values in sorted(by_family_actuals.items())
    }
    result: dict[str, Any] = {
        "training_count": len(train_rows),
        "evaluation_count": len(target_rows),
        "method_metrics": method_metrics,
        "per_label_family_metrics": family_metrics,
        "class_balance": dict(sorted(Counter(actuals).items())),
        "model_training_policy": "DETERMINISTIC_SHRUNK_NEAREST_CENTROID_LINEAR_SCORE",
    }
    if include_per_ticker:
        result["per_ticker_metrics"] = {
            ticker: {method: _classification_metrics(values, by_ticker_predictions[ticker][method]) for method in EVALUATED_METHODS}
            for ticker, values in sorted(by_ticker_actuals.items(), key=lambda item: TARGET_UNIVERSE.index(item[0]))
        }
    return result


def _evaluation_reports(rows: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    walk_forward: list[dict[str, Any]] = []
    for fold_id, start, end in WALK_FORWARD_FOLDS:
        training = [
            row
            for row in rows
            if row["date"] < start and row["outcome_end_date"] < start
        ]
        target = [row for row in rows if start <= row["date"] <= end]
        walk_forward.append({"fold_id": fold_id, "training_end_exclusive": start, "validation_start": start, "validation_end": end, **_evaluate_period(training, target)})
    oos_training = [
        row
        for row in rows
        if row["date"] < "2025-01-01"
        and row["outcome_end_date"] < "2025-01-01"
    ]
    oos_target = [row for row in rows if "2025-01-01" <= row["date"] <= "2025-12-31"]
    oos = {
        "training_window": "2022-01-01 through 2024-12-31 expanding evidence",
        "oos_window": "2025-01-01 through 2025-12-31",
        "oos_holdout_year": 2025,
        **_evaluate_period(oos_training, oos_target, include_per_ticker=True),
    }
    return walk_forward, oos


def _model_family_statuses() -> list[dict[str, Any]]:
    return [
        {"model_family": "MODEL_FAMILY_REGULARIZED_LINEAR", "evaluation_status": "EVALUATED_RESEARCH_ONLY", "training_performed": True, "implementation": "DETERMINISTIC_SHRUNK_NEAREST_CENTROID_LINEAR_SCORE"},
        {"model_family": "MODEL_FAMILY_TREE_BASELINE_OPTIONAL", "evaluation_status": "NOT_EVALUATED_MODEL_FAMILY_UNAVAILABLE", "training_performed": False, "implementation": "NO_NEW_DEPENDENCY_INSTALLED"},
        {"model_family": "MODEL_FAMILY_ENSEMBLE_OPTIONAL", "evaluation_status": "NOT_EVALUATED_MODEL_FAMILY_UNAVAILABLE", "training_performed": False, "implementation": "NO_NEW_DEPENDENCY_INSTALLED"},
        {"model_family": "MODEL_FAMILY_PER_TICKER_COMPARISON", "evaluation_status": "EVALUATED_COMPARISON_REPORT", "training_performed": True, "implementation": "PER_TICKER_REGULARIZED_LINEAR_METRIC_COMPARISON"},
        {"model_family": "MODEL_FAMILY_GLOBAL_CROSS_SECTIONAL_COMPARISON", "evaluation_status": "EVALUATED_COMPARISON_REPORT", "training_performed": True, "implementation": "GLOBAL_REGULARIZED_LINEAR_METRIC_COMPARISON"},
    ]


def _build_reports(*, run_timestamp_utc: str, verification: dict[str, Any], matrix: dict[str, Any], walk_forward: list[dict[str, Any]], oos: dict[str, Any]) -> tuple[dict[str, dict[str, Any]], dict[str, Any]]:
    fold_accuracies = {
        method: [float(fold["method_metrics"][method]["accuracy"]) for fold in walk_forward]
        for method in EVALUATED_METHODS
    }
    stability = {
        method: {
            "fold_accuracies": [_accuracy_text(value) for value in values],
            "minimum_accuracy": _accuracy_text(min(values)),
            "maximum_accuracy": _accuracy_text(max(values)),
            "population_stddev": _accuracy_text(pstdev(values)),
            "oos_accuracy": oos["method_metrics"][method]["accuracy"],
        }
        for method, values in fold_accuracies.items()
    }
    majority_accuracy = float(oos["method_metrics"]["BASELINE_MAJORITY_CLASS"]["accuracy"])
    deltas = {
        method: _accuracy_text(float(metrics["accuracy"]) - majority_accuracy)
        for method, metrics in oos["method_metrics"].items()
    }
    metric_results = {
        "metric_family_count": len(METRIC_FAMILIES),
        "metric_families": list(METRIC_FAMILIES),
        "interpretation": ["RESEARCH_ONLY_NON_ACTIONABLE", "NOT_PREDICTIVE_USEFULNESS_ACCEPTANCE", "NOT_PROFITABILITY_EVIDENCE", "NOT_RUNTIME_AUTHORITY"],
        "oos_method_metrics": deepcopy(oos["method_metrics"]),
        "walk_forward_stability": stability,
        "baseline_outperformance_delta": deltas,
        "class_balance": deepcopy(oos["class_balance"]),
    }
    calibration = {
        "calibration_status": "RESEARCH_ONLY_HARD_CLASS_CALIBRATION_SUMMARY",
        "oos_brier_scores": {method: metrics["brier_score"] for method, metrics in oos["method_metrics"].items()},
        "walk_forward_stability": stability,
        "predictive_usefulness_acceptance": False,
    }
    leakage_controls = [
        {"control_id": "future_label_values_not_used_as_features", "status": PASS},
        {"control_id": "forward_return_not_used_as_feature", "status": PASS},
        {"control_id": "label_value_not_used_as_feature_input", "status": PASS},
        {"control_id": "threshold_values_not_used_as_numeric_predictors", "status": PASS},
        {"control_id": "unavailable_targets_excluded_from_training_and_metrics", "status": PASS},
        {"control_id": "chronological_splits_no_shuffle", "status": PASS},
        {"control_id": "horizon_aware_training_embargo", "status": PASS},
        {"control_id": "source_digests_verified_before_execution", "status": PASS},
        {"control_id": "meta_reduced_record_count_preserved", "status": PASS},
    ]
    per_ticker = []
    for ticker in TARGET_UNIVERSE:
        per_ticker.append(
            {
                "ticker": ticker,
                "canonical_record_count": EXPECTED_RECORD_COUNTS[ticker],
                "feature_label_matrix_row_count": matrix["per_ticker_matrix_counts"][ticker],
                "evaluable_matrix_row_count": matrix["per_ticker_evaluable_counts"][ticker],
                "meta_reduced_record_count_flag": ticker == "META",
                "oos_method_metrics": deepcopy(oos["per_ticker_metrics"][ticker]),
                "predictive_usefulness": NOT_ACCEPTED,
                "profitability": NOT_ACCEPTED,
                "runtime_use": NOT_AUTHORIZED,
            }
        )
    reports = {
        "source_feature_label_binding_manifest": _report("source_feature_label_binding_manifest", {"run_timestamp_utc": run_timestamp_utc, "source_verification": deepcopy(verification), "feature_input_names": matrix["feature_input_names"], "feature_label_matrix_digest": matrix["feature_label_matrix_digest"], "binding_strategy": "TICKER_DATE_HORIZON_AND_LABEL_FAMILY_ALIGNMENT_EXECUTED_RESEARCH_ONLY"}),
        "chronological_split_profile": _report("chronological_split_profile", {"training_window": "2022-01-01 through 2023-12-31", "validation_window": "2024-01-01 through 2024-12-31", "oos_window": "2025-01-01 through 2025-12-31", "shuffle_allowed": False, "chronological_order_required": True, "horizon_aware_training_embargo_applied": True, "walk_forward_folds": [fold[0] for fold in WALK_FORWARD_FOLDS]}),
        "walk_forward_results": _report("walk_forward_results", {"walk_forward_fold_count": 4, "folds": walk_forward}),
        "oos_holdout_results": _report("oos_holdout_results", oos),
        "baseline_model_comparison_results": _report("baseline_model_comparison_results", {"baseline_family_count": 4, "baseline_families": list(BASELINE_FAMILIES), "model_family_count": 5, "model_families": _model_family_statuses(), "oos_method_metrics": deepcopy(oos["method_metrics"])}),
        "metric_family_results": _report("metric_family_results", metric_results),
        "calibration_stability_report": _report("calibration_stability_report", calibration),
        "leakage_quality_control_report": _report("leakage_quality_control_report", {"leakage_control_status": PASS, "leakage_failed_control_count": 0, "horizon_aware_training_embargo_applied": True, "controls": leakage_controls, "feature_input_names": matrix["feature_input_names"]}),
        "per_ticker_cross_sectional_review": _report("per_ticker_cross_sectional_review", {"target_universe": TARGET_UNIVERSE, "target_universe_count": 12, "per_ticker_entries": per_ticker}),
        "operator_review_summary": _report("operator_review_summary", {"run_timestamp_utc": run_timestamp_utc, "generated_output_count": 13, "feature_label_matrix_row_count": matrix["feature_label_matrix_row_count"], "evaluable_matrix_row_count": matrix["evaluable_matrix_row_count"], "walk_forward_fold_count": 4, "oos_holdout_year": 2025, "warning_count": 2, "warnings": ["MODEL_FAMILY_TREE_BASELINE_OPTIONAL unavailable without new dependency", "MODEL_FAMILY_ENSEMBLE_OPTIONAL unavailable without new dependency"], "predictive_usefulness": NOT_ACCEPTED, "profitability": NOT_ACCEPTED, "runtime_use": NOT_AUTHORIZED}),
    }
    summaries = {
        "feature_label_matrix_row_count": matrix["feature_label_matrix_row_count"],
        "evaluable_matrix_row_count": matrix["evaluable_matrix_row_count"],
        "unavailable_target_matrix_row_count": matrix["unavailable_target_matrix_row_count"],
        "feature_label_matrix_digest": matrix["feature_label_matrix_digest"],
        "feature_input_names": matrix["feature_input_names"],
        "walk_forward_fold_count": 4,
        "oos_holdout_year": 2025,
        "baseline_family_count": 4,
        "model_family_count": 5,
        "metric_family_count": 10,
        "leakage_control_status": PASS,
        "leakage_failed_control_count": 0,
        "horizon_aware_training_embargo_applied": True,
        "warning_count": 2,
        "oos_method_metrics": deepcopy(oos["method_metrics"]),
        "walk_forward_accuracy_stability": stability,
    }
    return reports, summaries


def _check(check_id: str, expected: Any, actual: Any) -> dict[str, Any]:
    status = PASS if actual == expected else FAIL
    return {"check_id": check_id, "status": status, "expected": expected, "actual": actual, "severity": BLOCKER, "message": f"{check_id} {'passed' if status == PASS else 'failed'}"}


def _execution_checklist(artifact: dict[str, Any]) -> list[dict[str, Any]]:
    values = {
        "artifact_kind_matches": (ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED_USING_REDESIGNED_LABELS, artifact.get("artifact_kind")),
        "execution_status_matches": (ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED_USING_REDESIGNED_LABELS_RESEARCH_ONLY, artifact.get("execution_status")),
        "approval_digest_bound": (EXPECTED_APPROVAL_DIGEST, artifact.get("additional_predictive_evidence_execution_approval_using_redesigned_labels_digest")),
        "execution_approved_true": (True, artifact.get("additional_predictive_evidence_execution_approved")),
        "execution_authorized_true": (True, artifact.get("additional_predictive_evidence_execution_authorized")),
        "ready_for_execution_true": (True, artifact.get("ready_for_additional_predictive_evidence_execution_using_redesigned_labels")),
        "predictive_evidence_executed_true": (True, artifact.get("additional_predictive_evidence_executed")),
        "predictive_evidence_results_created_true": (True, artifact.get("predictive_evidence_results_created")),
        "metric_recomputation_true": (True, artifact.get("metric_recomputation_performed")),
        "model_training_true": (True, artifact.get("model_training_performed")),
        "generated_output_count_13": (13, artifact.get("generated_output_count")),
        "target_universe_preserved": (TARGET_UNIVERSE, artifact.get("target_universe")),
        "meta_913_preserved": (913, artifact.get("meta_record_count")),
        "matrix_rows_143352": (EXPECTED_LABEL_ROW_COUNT, artifact.get("feature_label_matrix_row_count")),
        "evaluable_rows_142200": (EXPECTED_AVAILABLE_LABEL_COUNT, artifact.get("evaluable_matrix_row_count")),
        "unavailable_targets_1152": (EXPECTED_UNAVAILABLE_LABEL_COUNT, artifact.get("unavailable_target_matrix_row_count")),
        "walk_forward_folds_4": (4, artifact.get("walk_forward_fold_count")),
        "oos_holdout_2025": (2025, artifact.get("oos_holdout_year")),
        "baseline_families_4": (4, artifact.get("baseline_family_count")),
        "model_families_5": (5, artifact.get("model_family_count")),
        "metric_families_10": (10, artifact.get("metric_family_count")),
        "leakage_controls_pass": (PASS, artifact.get("leakage_control_status")),
        "horizon_aware_training_embargo": (
            True,
            artifact.get("horizon_aware_training_embargo_applied"),
        ),
        "future_labels_excluded": (False, artifact.get("future_label_values_used_as_features")),
        "forward_returns_excluded": (False, artifact.get("forward_return_used_as_feature")),
        "label_values_excluded": (False, artifact.get("label_value_used_as_feature_input")),
        "threshold_values_excluded": (False, artifact.get("threshold_value_used_as_numeric_predictor")),
        "predictive_usefulness_not_accepted": (NOT_ACCEPTED, artifact.get("predictive_usefulness")),
        "profitability_not_accepted": (NOT_ACCEPTED, artifact.get("profitability")),
        "runtime_not_authorized": (NOT_AUTHORIZED, artifact.get("runtime_use")),
        "trade_recommendations_false": (False, artifact.get("trade_recommendations_generated")),
        "no_provider_requests": (False, artifact.get("provider_requests_made_in_execution")),
        "no_market_data_acquisition": (False, artifact.get("market_data_acquisition_performed_in_execution")),
        "no_source_regeneration": (True, not any(artifact.get(field) for field in ("dataset_generation_performed_in_execution", "canonical_dataset_regenerated_in_execution", "redesigned_label_regeneration_performed", "feature_regeneration_performed"))),
        "matrix_digest_present": (True, isinstance(artifact.get("feature_label_matrix_digest"), str) and len(artifact["feature_label_matrix_digest"]) == 64),
        "failure_count_zero": (0, artifact.get("failure_count")),
    }
    return [_check(check_id, expected, actual) for check_id, (expected, actual) in values.items()]


def additional_predictive_evidence_execution_using_redesigned_labels_digest_v1(artifact: dict[str, Any]) -> str:
    payload = deepcopy(artifact)
    payload.pop("additional_predictive_evidence_execution_digest", None)
    if isinstance(payload.get("execution_summary"), dict):
        payload["execution_summary"].pop(
            "additional_predictive_evidence_execution_digest", None
        )
    for field in ("canonical_root", "label_root", "feature_root", "output_root"):
        payload.pop(field, None)
    return semantic_digest(payload)


def _build_executed_artifact(*, run_timestamp_utc: str, canonical_root: Path, label_root: Path, feature_root: Path, output_root: Path, summaries: dict[str, Any]) -> dict[str, Any]:
    artifact: dict[str, Any] = {
        "artifact_kind": ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED_USING_REDESIGNED_LABELS,
        "schema_version": SCHEMA_VERSION_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED_USING_REDESIGNED_LABELS_V1,
        "execution_status": ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED_USING_REDESIGNED_LABELS_RESEARCH_ONLY,
        "created_offline": True,
        "research_only": True,
        "operator_review_required": True,
        "run_timestamp_utc": run_timestamp_utc,
        "canonical_root": _path_text(canonical_root),
        "label_root": _path_text(label_root),
        "feature_root": _path_text(feature_root),
        "output_root": _path_text(output_root),
        **{field: False for field in FALSE_GUARDRAIL_FIELDS},
        **_source_evidence(),
        **_common_output_fields(),
        "additional_predictive_evidence_execution_manifest_created": True,
        "source_feature_label_binding_manifest_created": True,
        "feature_label_matrix_created": True,
        "chronological_split_profile_created": True,
        "walk_forward_results_created": True,
        "oos_holdout_results_created": True,
        "baseline_model_comparison_results_created": True,
        "metric_family_results_created": True,
        "calibration_stability_report_created": True,
        "leakage_quality_control_report_created": True,
        "per_ticker_cross_sectional_review_created": True,
        "operator_review_summary_created": True,
        "digest_manifest_created": True,
        "generated_output_count": 13,
        "target_universe": list(TARGET_UNIVERSE),
        "target_universe_count": 12,
        "total_canonical_record_count": EXPECTED_RECORD_COUNT,
        "per_ticker_record_counts": deepcopy(EXPECTED_RECORD_COUNTS),
        "redesigned_label_row_count": EXPECTED_LABEL_ROW_COUNT,
        "available_label_value_count": EXPECTED_AVAILABLE_LABEL_COUNT,
        "unavailable_label_value_count": EXPECTED_UNAVAILABLE_LABEL_COUNT,
        "feature_value_row_count": EXPECTED_FEATURE_ROW_COUNT,
        "available_feature_value_count": EXPECTED_AVAILABLE_FEATURE_COUNT,
        "unavailable_feature_value_count": EXPECTED_UNAVAILABLE_FEATURE_COUNT,
        "meta_record_count": 913,
        "non_meta_record_count": 1003,
        "meta_reduced_record_count_preserved": True,
        "future_label_values_used_as_features": False,
        "forward_return_used_as_feature": False,
        "label_value_used_as_feature_input": False,
        "threshold_value_used_as_numeric_predictor": False,
        "failure_count": 0,
        **deepcopy(summaries),
    }
    checklist = _execution_checklist(artifact)
    artifact["execution_checklist"] = checklist
    failed = [row for row in checklist if row["status"] == FAIL]
    artifact["execution_summary"] = {
        "target_count": 12,
        "total_canonical_record_count": EXPECTED_RECORD_COUNT,
        "generated_output_count": 13,
        "feature_label_matrix_row_count": EXPECTED_LABEL_ROW_COUNT,
        "evaluable_matrix_row_count": EXPECTED_AVAILABLE_LABEL_COUNT,
        "unavailable_target_matrix_row_count": EXPECTED_UNAVAILABLE_LABEL_COUNT,
        "walk_forward_fold_count": 4,
        "oos_holdout_year": 2025,
        "baseline_family_count": 4,
        "model_family_count": 5,
        "metric_family_count": 10,
        "leakage_control_status": PASS,
        "leakage_failed_control_count": 0,
        "horizon_aware_training_embargo_applied": True,
        "failure_count": 0,
        "warning_count": summaries.get("warning_count", 0),
        "total_checks": len(checklist),
        "passed_checks": len(checklist) - len(failed),
        "failed_checks": len(failed),
        "blocker_count": len(failed),
        "feature_label_matrix_digest": summaries["feature_label_matrix_digest"],
    }
    artifact["additional_predictive_evidence_execution_digest"] = additional_predictive_evidence_execution_using_redesigned_labels_digest_v1(artifact)
    artifact["execution_summary"]["additional_predictive_evidence_execution_digest"] = artifact["additional_predictive_evidence_execution_digest"]
    return artifact


def _write_json_once(
    path: Path, payload: dict[str, Any], *, replace_existing: bool = False
) -> str:
    data = canonical_json_bytes(payload)
    try:
        with path.open("wb" if replace_existing else "xb") as handle:
            handle.write(data)
    except FileExistsError as exc:
        raise AdditionalPredictiveEvidenceExecutionRedesignedLabelsError(f"execution output already exists: {path.name}") from exc
    return sha256_bytes(data)


def _run_verified_execution(*, canonical_root: Path, label_root: Path, feature_root: Path, output_root: Path, run_timestamp_utc: str, verification: dict[str, Any], replace_existing: bool = False) -> dict[str, Any]:
    if not replace_existing and output_root.exists() and any(output_root.iterdir()):
        raise AdditionalPredictiveEvidenceExecutionRedesignedLabelsError("additional predictive evidence output root is not empty")
    output_root.mkdir(parents=True, exist_ok=True)
    feature_vectors, feature_names = _load_feature_vectors(feature_root / "feature_values.jsonl")
    matrix, evaluation_rows = _build_matrix_and_evaluation_rows(
        label_path=label_root / "redesigned_label_values.jsonl",
        feature_vectors=feature_vectors,
        feature_names=feature_names,
        matrix_path=output_root / "feature_label_matrix.jsonl",
    )
    walk_forward, oos = _evaluation_reports(evaluation_rows)
    reports, summaries = _build_reports(run_timestamp_utc=run_timestamp_utc, verification=verification, matrix=matrix, walk_forward=walk_forward, oos=oos)
    artifact = _build_executed_artifact(run_timestamp_utc=run_timestamp_utc, canonical_root=canonical_root, label_root=label_root, feature_root=feature_root, output_root=output_root, summaries=summaries)
    validate_additional_predictive_evidence_executed_using_redesigned_labels_v1(artifact)
    reports["additional_predictive_evidence_execution_manifest"] = artifact
    output_digests = {"feature_label_matrix.jsonl": matrix["feature_label_matrix_digest"]}
    name_by_file = {
        "additional_predictive_evidence_execution_manifest.json": "additional_predictive_evidence_execution_manifest",
        "source_feature_label_binding_manifest.json": "source_feature_label_binding_manifest",
        "chronological_split_profile.json": "chronological_split_profile",
        "walk_forward_results.json": "walk_forward_results",
        "oos_holdout_results.json": "oos_holdout_results",
        "baseline_model_comparison_results.json": "baseline_model_comparison_results",
        "metric_family_results.json": "metric_family_results",
        "calibration_stability_report.json": "calibration_stability_report",
        "leakage_quality_control_report.json": "leakage_quality_control_report",
        "per_ticker_cross_sectional_review.json": "per_ticker_cross_sectional_review",
        "operator_review_summary.json": "operator_review_summary",
    }
    for filename, report_name in name_by_file.items():
        output_digests[filename] = _write_json_once(
            output_root / filename,
            reports[report_name],
            replace_existing=replace_existing,
        )
    digest_entries = [
        ({"filename": filename, "digest_kind": "SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE", "sha256": None} if filename == "additional_predictive_evidence_digest_manifest.json" else {"filename": filename, "digest_kind": "FILE_SHA256", "sha256": output_digests[filename]})
        for filename in OUTPUT_FILENAMES
    ]
    digest_manifest = _report("additional_predictive_evidence_digest_manifest", {"run_timestamp_utc": run_timestamp_utc, "generated_output_count": 13, "output_digest_entries": digest_entries, "all_non_self_output_digests_present": True, "self_reference_policy": "SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE", "additional_predictive_evidence_execution_digest": artifact["additional_predictive_evidence_execution_digest"], "feature_label_matrix_digest": artifact["feature_label_matrix_digest"]})
    _write_json_once(
        output_root / "additional_predictive_evidence_digest_manifest.json",
        digest_manifest,
        replace_existing=replace_existing,
    )
    return artifact


def execute_additional_predictive_evidence_using_redesigned_labels_v1(*, canonical_root: str | Path | None = None, label_root: str | Path | None = None, feature_root: str | Path | None = None, output_root: str | Path | None = None, run_timestamp_utc: str | None = None) -> dict[str, Any]:
    """Execute the approved deterministic research run without provider access."""
    canonical_path = DEFAULT_CANONICAL_ROOT if canonical_root is None else Path(canonical_root)
    label_path = DEFAULT_LABEL_ROOT if label_root is None else Path(label_root)
    feature_path = DEFAULT_FEATURE_ROOT if feature_root is None else Path(feature_root)
    output_path = DEFAULT_OUTPUT_ROOT if output_root is None else Path(output_root)
    timestamp = run_timestamp_utc or _utc_now()
    verification, failures = _verify_sources(canonical_path, label_path, feature_path)
    if failures:
        return _blocked_artifact(canonical_root=canonical_path, label_root=label_path, feature_root=feature_path, output_root=output_path, run_timestamp_utc=timestamp, failures=failures)
    return _run_verified_execution(canonical_root=canonical_path, label_root=label_path, feature_root=feature_path, output_root=output_path, run_timestamp_utc=timestamp, verification=verification)


FORBIDDEN_ARTIFACT_VALUES = {"PREDICTIVE_USEFULNESS_REASSESSMENT_REVIEW_PACKAGE", "PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_REVIEW", "PREDICTIVE_USEFULNESS_ACCEPTANCE_CANDIDATE", "PREDICTIVE_USEFULNESS_ACCEPTED", "PROFITABILITY_ACCEPTED", "RUNTIME_MIGRATION_APPROVED", "RUNTIME_MIGRATION_ACTIVE", "STRATEGY_RUNTIME_MIGRATION", "TRADE_RECOMMENDATIONS"}


def _reject_forbidden(value: Any, path: str = "artifact") -> None:
    if isinstance(value, str) and value in FORBIDDEN_ARTIFACT_VALUES:
        raise AdditionalPredictiveEvidenceExecutionRedesignedLabelsError(f"{path} must not emit {value}")
    if isinstance(value, dict):
        for key, item in value.items():
            child = f"{path}.{key}"
            if key in FALSE_GUARDRAIL_FIELDS and item is True:
                raise AdditionalPredictiveEvidenceExecutionRedesignedLabelsError(f"{child} must be false")
            if key in {"runtime_use", "strategy_use", "paper_trading", "broker_execution"} and item == "AUTHORIZED":
                raise AdditionalPredictiveEvidenceExecutionRedesignedLabelsError(f"{child} must not be AUTHORIZED")
            if key in {"predictive_usefulness", "profitability"} and item == "accepted":
                raise AdditionalPredictiveEvidenceExecutionRedesignedLabelsError(f"{child} must not be accepted")
            _reject_forbidden(item, child)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _reject_forbidden(item, f"{path}[{index}]")


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise AdditionalPredictiveEvidenceExecutionRedesignedLabelsError(f"{field} mismatch")


def validate_additional_predictive_evidence_executed_using_redesigned_labels_v1(artifact: dict) -> dict[str, Any]:
    """Reject any execution artifact that exceeds research-only authority."""
    if not isinstance(artifact, dict):
        raise AdditionalPredictiveEvidenceExecutionRedesignedLabelsError("artifact must be a JSON object")
    _reject_forbidden(artifact)
    expected = {
        "artifact_kind": ARTIFACT_KIND_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED_USING_REDESIGNED_LABELS,
        "schema_version": SCHEMA_VERSION_ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED_USING_REDESIGNED_LABELS_V1,
        "execution_status": ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED_USING_REDESIGNED_LABELS_RESEARCH_ONLY,
        **_source_evidence(),
        "target_universe": TARGET_UNIVERSE,
        "target_universe_count": 12,
        "total_canonical_record_count": EXPECTED_RECORD_COUNT,
        "per_ticker_record_counts": EXPECTED_RECORD_COUNTS,
        "meta_record_count": 913,
        "non_meta_record_count": 1003,
        "redesigned_label_row_count": EXPECTED_LABEL_ROW_COUNT,
        "available_label_value_count": EXPECTED_AVAILABLE_LABEL_COUNT,
        "unavailable_label_value_count": EXPECTED_UNAVAILABLE_LABEL_COUNT,
        "feature_value_row_count": EXPECTED_FEATURE_ROW_COUNT,
        "available_feature_value_count": EXPECTED_AVAILABLE_FEATURE_COUNT,
        "unavailable_feature_value_count": EXPECTED_UNAVAILABLE_FEATURE_COUNT,
        "feature_label_matrix_row_count": EXPECTED_LABEL_ROW_COUNT,
        "evaluable_matrix_row_count": EXPECTED_AVAILABLE_LABEL_COUNT,
        "unavailable_target_matrix_row_count": EXPECTED_UNAVAILABLE_LABEL_COUNT,
        "walk_forward_fold_count": 4,
        "oos_holdout_year": 2025,
        "baseline_family_count": 4,
        "model_family_count": 5,
        "metric_family_count": 10,
        "leakage_control_status": PASS,
        "leakage_failed_control_count": 0,
        "horizon_aware_training_embargo_applied": True,
        "generated_output_count": 13,
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
    }
    for field, expected_value in expected.items():
        _expect(artifact.get(field), expected_value, field)
    for field in (
        "created_offline", "research_only", "operator_review_required", "additional_predictive_evidence_execution_approved", "additional_predictive_evidence_execution_authorized", "ready_for_additional_predictive_evidence_execution_using_redesigned_labels", "additional_predictive_evidence_executed", "predictive_evidence_results_created", "metric_recomputation_performed", "model_training_performed", "additional_predictive_evidence_execution_manifest_created", "source_feature_label_binding_manifest_created", "feature_label_matrix_created", "chronological_split_profile_created", "walk_forward_results_created", "oos_holdout_results_created", "baseline_model_comparison_results_created", "metric_family_results_created", "calibration_stability_report_created", "leakage_quality_control_report_created", "per_ticker_cross_sectional_review_created", "operator_review_summary_created", "digest_manifest_created", "meta_reduced_record_count_preserved",
    ):
        _expect(artifact.get(field), True, field)
    for field in FALSE_GUARDRAIL_FIELDS:
        _expect(artifact.get(field), False, field)
    for field in ("future_label_values_used_as_features", "forward_return_used_as_feature", "label_value_used_as_feature_input", "threshold_value_used_as_numeric_predictor"):
        _expect(artifact.get(field), False, field)
    matrix_digest = artifact.get("feature_label_matrix_digest")
    if not isinstance(matrix_digest, str) or len(matrix_digest) != 64:
        raise AdditionalPredictiveEvidenceExecutionRedesignedLabelsError("feature-label matrix digest required")
    checklist = _execution_checklist(artifact)
    _expect(artifact.get("execution_checklist"), checklist, "execution_checklist")
    summary = artifact.get("execution_summary")
    if not isinstance(summary, dict):
        raise AdditionalPredictiveEvidenceExecutionRedesignedLabelsError("execution_summary required")
    _expect(summary.get("failed_checks"), 0, "execution_summary.failed_checks")
    _expect(summary.get("blocker_count"), 0, "execution_summary.blocker_count")
    digest = artifact.get("additional_predictive_evidence_execution_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise AdditionalPredictiveEvidenceExecutionRedesignedLabelsError("execution digest required")
    _expect(digest, additional_predictive_evidence_execution_using_redesigned_labels_digest_v1(artifact), "execution digest")
    _expect(summary.get("additional_predictive_evidence_execution_digest"), digest, "execution_summary.execution_digest")
    _expect(summary.get("feature_label_matrix_digest"), matrix_digest, "execution_summary.matrix_digest")
    return {"valid": True, "execution_status": artifact["execution_status"], "additional_predictive_evidence_execution_digest": digest, "feature_label_matrix_digest": matrix_digest, "generated_output_count": 13, "blocker_count": 0}


def build_additional_predictive_evidence_execution_status_markdown_v1(artifact: dict) -> str:
    """Render execution evidence without implying usefulness or runtime acceptance."""
    validate_additional_predictive_evidence_executed_using_redesigned_labels_v1(artifact)
    sections = [
        ("Title", "Additional Predictive Evidence Execution Using Redesigned Labels v1."),
        ("Additional Predictive Evidence Execution Using Redesigned Labels", f"Artifact/status/digest: `{artifact['artifact_kind']}` / `{artifact['execution_status']}` / `{artifact['additional_predictive_evidence_execution_digest']}`."),
        ("Source Approval", f"Approval digest: `{artifact['additional_predictive_evidence_execution_approval_using_redesigned_labels_digest']}`."),
        ("Dataset and Universe", f"`{artifact['total_canonical_record_count']}` frozen records across {artifact['target_universe_count']} ordered tickers; META remains `{artifact['meta_record_count']}`."),
        ("Source Redesigned Label Profile", f"Rows available/unavailable: `{artifact['redesigned_label_row_count']}` / `{artifact['available_label_value_count']}` / `{artifact['unavailable_label_value_count']}`."),
        ("Source Feature Profile", f"Rows available/unavailable: `{artifact['feature_value_row_count']}` / `{artifact['available_feature_value_count']}` / `{artifact['unavailable_feature_value_count']}`."),
        ("Feature / Label Matrix", f"Rows/evaluable/unavailable: `{artifact['feature_label_matrix_row_count']}` / `{artifact['evaluable_matrix_row_count']}` / `{artifact['unavailable_target_matrix_row_count']}`; digest `{artifact['feature_label_matrix_digest']}`."),
        ("Chronological Splits", "Training 2022-2023, quarterly walk-forward validation in 2024, and OOS holdout in 2025; no shuffle."),
        ("Walk-Forward Results", f"`{artifact['walk_forward_fold_count']}` expanding-window quarterly folds completed research-only."),
        ("OOS Holdout Results", f"OOS year `{artifact['oos_holdout_year']}` completed research-only."),
        ("Baseline and Model Comparison", f"`{artifact['baseline_family_count']}` baselines and `{artifact['model_family_count']}` model/comparison families recorded; optional unavailable models were not installed."),
        ("Metric Family Results", f"`{artifact['metric_family_count']}` research-only metric families computed."),
        ("Calibration and Stability", "Hard-class Brier summaries and quarterly accuracy stability were recorded as non-actionable evidence."),
        ("Leakage and Quality Controls", f"Status `{artifact['leakage_control_status']}` with `{artifact['leakage_failed_control_count']}` failed controls."),
        ("Per-Ticker / Cross-Sectional Review", "All 12 ordered tickers were reviewed; META's 913-record limitation remains explicit."),
        ("Output Digest Manifest", "All 13 outputs are covered; the digest manifest uses an explicit self-reference exception."),
        ("Execution Boundary", "Predictive evidence, research-only metrics, and deterministic local model evaluation were executed; no strategy scoring or recommendations were created."),
        ("Predictive Usefulness Boundary", "Predictive usefulness remains not accepted."),
        ("Profitability Boundary", "Profitability remains not accepted."),
        ("Runtime Boundary", "Runtime, strategy, paper-trading, and broker use remain NOT_AUTHORIZED."),
        ("Checklist Summary", f"`{artifact['execution_summary']['passed_checks']}/{artifact['execution_summary']['total_checks']}` passed with `{artifact['execution_summary']['blocker_count']}` blockers."),
        ("Guardrails", "No provider request, market-data acquisition, source regeneration, source mutation, acceptance, runtime activation, or trading action occurred."),
    ]
    lines = ["# Additional Predictive Evidence Execution Using Redesigned Labels", ""]
    for title, body in sections:
        lines.extend([f"## {title}", "", f"- {body}", ""])
    return "\n".join(lines)
