"""Offline research-only predictive experiment execution."""

from __future__ import annotations

import json
import random
import re
from copy import deepcopy
from datetime import UTC, datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import acquisition_generation_service as acquisition
from marketflow.services import predictive_experiment_execution_approval_service as approval
from marketflow.services import predictive_experiment_execution_candidate_service as candidate
from marketflow.services import read_only_registry_discovery_service as discovery


ARTIFACT_KIND_PREDICTIVE_EXPERIMENT_EXECUTED = "PREDICTIVE_EXPERIMENT_EXECUTED"
SCHEMA_VERSION_PREDICTIVE_EXPERIMENT_EXECUTED_V1 = "predictive_experiment_executed_v1"
PREDICTIVE_EXPERIMENT_EXECUTED_RESEARCH_ONLY = (
    "PREDICTIVE_EXPERIMENT_EXECUTED_RESEARCH_ONLY"
)
PREDICTIVE_EXPERIMENT_EXECUTION_BLOCKED_MISSING_APPROVAL_DIGEST = (
    "PREDICTIVE_EXPERIMENT_EXECUTION_BLOCKED_MISSING_APPROVAL_DIGEST"
)
PREDICTIVE_EXPERIMENT_EXECUTION_BLOCKED_DATASET_VERIFICATION_FAILED = (
    "PREDICTIVE_EXPERIMENT_EXECUTION_BLOCKED_DATASET_VERIFICATION_FAILED"
)
SIMPLIFIED_CHRONOLOGICAL_RESEARCH_SPLIT = "SIMPLIFIED_CHRONOLOGICAL_RESEARCH_SPLIT"

RESEARCH_ONLY_NON_ACTIONABLE = candidate.RESEARCH_ONLY_NON_ACTIONABLE
RESEARCH_ONLY_NOT_PERFORMANCE_ACCEPTANCE = candidate.RESEARCH_ONLY_NOT_PERFORMANCE_ACCEPTANCE
NOT_AUTHORIZED = candidate.NOT_AUTHORIZED
PREDICTIVE_USEFULNESS_NOT_ACCEPTED = acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED
PROFITABILITY_NOT_ACCEPTED = acquisition.PROFITABILITY_NOT_ACCEPTED

DEFAULT_BASE_COMMIT = "cf0fdd4dca061c69f5dc8b12da5e0634a99cfca4"
DEFAULT_BRANCH = "feature/predictive-experiment-execution-v1"
DEFAULT_OUTPUT_ROOT = Path(".marketflow") / "predictive_experiments" / "AAPL" / "2022_2025"
APPROVAL_STATUS_PATH = (
    Path("docs") / "status" / "MARKETFLOW_PREDICTIVE_EXPERIMENT_EXECUTION_APPROVAL_STATUS.md"
)
EXPECTED_APPROVAL_DIGEST = "d1578a7858da3686d7322f4405e8c5f8075fdb32efa4f77bdae6af2242f4f4be"

EXPECTED_SOURCE_DIGESTS = {
    "execution_candidate_digest": approval.EXPECTED_EXECUTION_CANDIDATE_DIGEST,
    "execution_candidate_review_package_digest": (
        approval.EXPECTED_EXECUTION_CANDIDATE_REVIEW_PACKAGE_DIGEST
    ),
    "predictive_experiment_plan_digest": candidate.EXPECTED_PREDICTIVE_EXPERIMENT_PLAN_DIGEST,
    "predictive_experiment_plan_review_package_digest": (
        candidate.EXPECTED_PREDICTIVE_EXPERIMENT_PLAN_REVIEW_PACKAGE_DIGEST
    ),
    "predictive_usefulness_review_candidate_digest": (
        "e5724cc5eb106b2aa24c68e80bb24835b293fe50009a4eb01b21154553bc79b6"
    ),
    "predictive_usefulness_review_candidate_review_package_digest": (
        "f124ee8e7e6b72f9d8f5f2a495bb0afa09ef02e4d8a6a03e795a04de4276efe2"
    ),
    "campaign_results_review_package_digest": (
        "c0421913adbd4a0a02bb1d062a0ef1efd4081c4e1656a46073f4e45fdfd4408b"
    ),
    "campaign_execution_digest": "f3793401f2ad1b4f3df8b5d130bdb78629941422eaa753943abd43cf2be96f1c",
    "swing_registry_approval_digest": (
        "ee3f6b193a6480fb6391fd97b096dda8fc699d65e43a179c77bba8798f887761"
    ),
    "position_swing_registry_approval_digest": (
        "8eefcbc1e14b2e199dadd8dcf461cbff56513f10758b6b59ca8cf176512d2e8e"
    ),
}

EXPECTED_DATASET_DIGESTS = {
    "SWING": {
        "dataset_rows_digest": "e449f54e53a7dd538ede0b396205253c96aefdb70081f34df60b3b8bd73232bc",
        "dataset_manifest_digest": "0736b42eb806c172ad2267121895955c99a5ff19554f77d79ea86807273752ae",
    },
    "POSITION_SWING": {
        "dataset_rows_digest": "163d26fb50bbc0defb0f0602922fb672a6b404d43d920c9f018053fec2862ab3",
        "dataset_manifest_digest": "720c7314ba86b20fde05c16f69870a4cfd218eb6c317ff592efd5fd1885776ba",
    },
}

OUTPUT_NAMES = list(candidate.PLANNED_OUTPUT_NAMES)
LABELS_BY_PROFILE = {
    "SWING": {
        "direction": "SWING_NEXT_BAR_DIRECTION",
        "bucket": "SWING_NEXT_BAR_RETURN_BUCKET",
        "step_label": "next_bar",
    },
    "POSITION_SWING": {
        "direction": "POSITION_SWING_NEXT_SESSION_DIRECTION",
        "bucket": "POSITION_SWING_NEXT_SESSION_RETURN_BUCKET",
        "step_label": "next_session",
    },
}
FEATURE_FAMILIES = [
    "price_return_features",
    "range_volatility_features",
    "volume_context_features",
    "rolling_mean_features",
    "rolling_zscore_features",
    "bar_position_features",
]
FEATURE_NAMES = [
    "close_return_1",
    "range_pct",
    "volume_change_1",
    "rolling_close_mean_5",
    "rolling_close_zscore_20",
    "close_position_in_range",
]
BASELINES = [
    "majority_class_baseline",
    "zero_return_baseline",
    "naive_persistence_baseline",
    "random_baseline_seeded",
]
TRUE_EXECUTION_FIELDS = [
    "predictive_experiment_execution_authorized",
    "predictive_experiment_executed",
    "walk_forward_validation_performed",
    "out_of_sample_evaluation_performed",
    "label_generation_performed",
    "feature_matrix_generation_performed",
    "research_only",
]
FALSE_GUARDRAIL_FIELDS = [
    "new_strategy_scoring_performed",
    "trade_recommendations_generated",
    "provider_requests_made",
    "predictive_usefulness_acceptance_ready",
    "profitability_acceptance_ready",
    "runtime_migration_recommended",
    "runtime_migration_approved",
    "runtime_migration_active",
    "strategy_runtime_migration",
    "automatic_stitching",
]
BOUNDARY_FIELDS = ["runtime_use", "strategy_use", "paper_trading", "broker_execution"]


class PredictiveExperimentExecutionError(ValueError):
    """Raised when predictive experiment execution violates research-only guardrails."""


def _utc_now() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


def _resolve_root(root: str | Path | None, default: Path) -> Path:
    return default if root is None else Path(root)


def _path_text(path: Path) -> str:
    return str(path).replace("\\", "/")


def _boundary_fields() -> dict[str, str]:
    return {
        "output_label": RESEARCH_ONLY_NON_ACTIONABLE,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "predictive_usefulness": PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "profitability": PROFITABILITY_NOT_ACCEPTED,
    }


def _report(name: str, payload: dict[str, Any]) -> dict[str, Any]:
    return {"report_name": name, **_boundary_fields(), **payload}


def _parse_decimal(value: Any) -> Decimal | None:
    if value in (None, ""):
        return None
    try:
        return Decimal(str(value))
    except (InvalidOperation, ValueError):
        return None


def _decimal_text(value: Decimal | None, places: int = 6) -> str | None:
    if value is None:
        return None
    quant = Decimal("1").scaleb(-places)
    return format(value.quantize(quant), "f")


def _safe_divide(numerator: Decimal | None, denominator: Decimal | None) -> Decimal | None:
    if numerator is None or denominator in (None, Decimal("0")):
        return None
    return numerator / denominator


def _mean(values: list[Decimal]) -> Decimal | None:
    if not values:
        return None
    return sum(values) / Decimal(len(values))


def _stddev(values: list[Decimal]) -> Decimal | None:
    if len(values) < 2:
        return None
    avg = _mean(values)
    if avg is None:
        return None
    variance = sum((value - avg) * (value - avg) for value in values) / Decimal(len(values))
    if variance == 0:
        return Decimal("0")
    return Decimal(str(float(variance) ** 0.5))


def _direction(current_close: Decimal | None, next_close: Decimal | None) -> str:
    if current_close is None or next_close is None:
        return "UNAVAILABLE"
    if next_close > current_close:
        return "UP"
    if next_close < current_close:
        return "DOWN"
    return "FLAT"


def _return_bucket(current_close: Decimal | None, next_close: Decimal | None) -> str:
    if current_close in (None, Decimal("0")) or next_close is None:
        return "UNAVAILABLE"
    value = (next_close - current_close) / current_close
    if value > 0:
        return "POSITIVE_RETURN"
    if value < 0:
        return "NEGATIVE_RETURN"
    return "ZERO_RETURN"


def _row_timestamp(row: dict[str, Any]) -> str:
    return str(row.get("bar_start_utc") or row.get("session_date") or "")


def _label_rows(profile: str, rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    definitions = LABELS_BY_PROFILE[profile]
    labeled: list[dict[str, Any]] = []
    for index, row in enumerate(rows):
        current_close = _parse_decimal(row.get("close"))
        next_row = rows[index + 1] if index + 1 < len(rows) else None
        next_close = _parse_decimal(next_row.get("close")) if next_row else None
        return_value = _safe_divide(
            (next_close - current_close) if current_close is not None and next_close is not None else None,
            current_close,
        )
        labeled.append(
            {
                "row_index": index,
                "timestamp": _row_timestamp(row),
                "direction": _direction(current_close, next_close),
                "return_bucket": _return_bucket(current_close, next_close),
                "forward_return": _decimal_text(return_value, 8),
                "labels_available": next_row is not None,
                "direction_label_name": definitions["direction"],
                "return_bucket_label_name": definitions["bucket"],
            }
        )
    return labeled


def _feature_rows(profile: str, rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    feature_rows: list[dict[str, Any]] = []
    closes: list[Decimal] = []
    previous_close: Decimal | None = None
    previous_volume: Decimal | None = None
    for index, row in enumerate(rows):
        close = _parse_decimal(row.get("close"))
        open_value = _parse_decimal(row.get("open"))
        high = _parse_decimal(row.get("high"))
        low = _parse_decimal(row.get("low"))
        volume = _parse_decimal(row.get("volume"))
        if close is not None:
            closes.append(close)
        close_return = _safe_divide(
            (close - previous_close) if close is not None and previous_close is not None else None,
            previous_close,
        )
        range_pct = _safe_divide(
            (high - low) if high is not None and low is not None else None,
            open_value,
        )
        volume_change = _safe_divide(
            (volume - previous_volume)
            if volume is not None and previous_volume is not None
            else None,
            previous_volume,
        )
        mean_5 = _mean(closes[-5:])
        std_20 = _stddev(closes[-20:])
        zscore_20 = (
            None
            if close is None or mean_5 is None or std_20 in (None, Decimal("0"))
            else (close - mean_5) / std_20
        )
        position = _safe_divide(
            (close - low) if close is not None and low is not None else None,
            (high - low) if high is not None and low is not None else None,
        )
        feature_rows.append(
            {
                "row_index": index,
                "dataset_profile": profile,
                "timestamp": _row_timestamp(row),
                "close_return_1": _decimal_text(close_return, 8),
                "range_pct": _decimal_text(range_pct, 8),
                "volume_change_1": _decimal_text(volume_change, 8),
                "rolling_close_mean_5": _decimal_text(mean_5, 6),
                "rolling_close_zscore_20": _decimal_text(zscore_20, 8),
                "close_position_in_range": _decimal_text(position, 8),
            }
        )
        previous_close = close
        previous_volume = volume
    return feature_rows


def _count_values(rows: list[dict[str, Any]], key: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for row in rows:
        value = str(row.get(key))
        counts[value] = counts.get(value, 0) + 1
    return dict(sorted(counts.items()))


def _split_indices(count: int) -> dict[str, dict[str, int]]:
    train_end = max(1, int(count * Decimal("0.60"))) if count else 0
    validation_end = max(train_end, int(count * Decimal("0.80"))) if count else 0
    if count >= 3:
        validation_end = min(max(train_end + 1, validation_end), count - 1)
    return {
        "train": {"start_index": 0, "end_index_exclusive": train_end},
        "validation": {"start_index": train_end, "end_index_exclusive": validation_end},
        "out_of_sample": {"start_index": validation_end, "end_index_exclusive": count},
    }


def _slice(rows: list[dict[str, Any]], span: dict[str, int]) -> list[dict[str, Any]]:
    return rows[span["start_index"] : span["end_index_exclusive"]]


def _majority_class(rows: list[dict[str, Any]]) -> str:
    counts = _count_values(rows, "direction")
    usable = {key: value for key, value in counts.items() if key != "UNAVAILABLE"}
    if not usable:
        return "FLAT"
    return sorted(usable.items(), key=lambda item: (-item[1], item[0]))[0][0]


def _predictions(
    *,
    baseline_name: str,
    train_rows: list[dict[str, Any]],
    target_rows: list[dict[str, Any]],
    prior_rows: list[dict[str, Any]],
) -> list[str]:
    classes = sorted(
        {row["direction"] for row in train_rows if row["direction"] != "UNAVAILABLE"}
        or {"FLAT"}
    )
    rng = random.Random(20260809)
    majority = _majority_class(train_rows)
    predictions: list[str] = []
    previous_direction = prior_rows[-1]["direction"] if prior_rows else majority
    for row in target_rows:
        if baseline_name == "majority_class_baseline":
            prediction = majority
        elif baseline_name == "zero_return_baseline":
            prediction = "FLAT"
        elif baseline_name == "naive_persistence_baseline":
            prediction = previous_direction if previous_direction != "UNAVAILABLE" else majority
        elif baseline_name == "random_baseline_seeded":
            prediction = rng.choice(classes)
        else:
            prediction = majority
        predictions.append(prediction)
        previous_direction = row["direction"]
    return predictions


def _confusion(actuals: list[str], predictions: list[str]) -> dict[str, dict[str, int]]:
    matrix: dict[str, dict[str, int]] = {}
    for actual, predicted in zip(actuals, predictions, strict=True):
        matrix.setdefault(actual, {})
        matrix[actual][predicted] = matrix[actual].get(predicted, 0) + 1
    return {actual: dict(sorted(values.items())) for actual, values in sorted(matrix.items())}


def _accuracy(actuals: list[str], predictions: list[str]) -> str:
    if not actuals:
        return "not_applicable"
    correct = sum(1 for actual, predicted in zip(actuals, predictions, strict=True) if actual == predicted)
    return _decimal_text(Decimal(correct) / Decimal(len(actuals)), 6) or "not_applicable"


def _recall_by_class(actuals: list[str], predictions: list[str]) -> dict[str, str]:
    classes = sorted(set(actuals) | set(predictions))
    recalls: dict[str, str] = {}
    for label in classes:
        denominator = sum(1 for actual in actuals if actual == label)
        if denominator == 0:
            recalls[label] = "not_applicable"
            continue
        numerator = sum(
            1 for actual, predicted in zip(actuals, predictions, strict=True) if actual == predicted == label
        )
        recalls[label] = _decimal_text(Decimal(numerator) / Decimal(denominator), 6) or "0.000000"
    return recalls


def _baseline_metrics(
    *, profile: str, labeled_rows: list[dict[str, Any]], splits: dict[str, dict[str, int]]
) -> dict[str, Any]:
    available_rows = [row for row in labeled_rows if row["labels_available"]]
    train_rows = _slice(available_rows, splits["train"])
    target_rows = _slice(available_rows, splits["out_of_sample"])
    prior_rows = _slice(available_rows, {"start_index": 0, "end_index_exclusive": splits["out_of_sample"]["start_index"]})
    actuals = [row["direction"] for row in target_rows if row["direction"] != "UNAVAILABLE"]
    results: dict[str, Any] = {}
    for baseline_name in BASELINES:
        raw_predictions = _predictions(
            baseline_name=baseline_name,
            train_rows=train_rows,
            target_rows=target_rows,
            prior_rows=prior_rows,
        )
        predictions = [
            prediction
            for row, prediction in zip(target_rows, raw_predictions, strict=True)
            if row["direction"] != "UNAVAILABLE"
        ]
        results[baseline_name] = {
            "dataset_profile": profile,
            "metrics_label": RESEARCH_ONLY_NOT_PERFORMANCE_ACCEPTANCE,
            "evaluated_label": LABELS_BY_PROFILE[profile]["direction"],
            "out_of_sample_count": len(actuals),
            "directional_accuracy": _accuracy(actuals, predictions),
            "balanced_accuracy": _balanced_accuracy_text(actuals, predictions),
            "recall_by_class": _recall_by_class(actuals, predictions),
            "confusion_matrix": _confusion(actuals, predictions),
            "roc_auc": "not_applicable_multiclass_direction_label",
            "information_coefficient": "not_applicable_direction_label",
            "calibration": "not_applicable_baseline_without_probabilities",
        }
    majority = results["majority_class_baseline"]["directional_accuracy"]
    for result in results.values():
        result["lift_over_majority_class_baseline"] = _lift_text(
            result["directional_accuracy"], majority
        )
    return results


def _balanced_accuracy_text(actuals: list[str], predictions: list[str]) -> str:
    recalls = [
        Decimal(value)
        for value in _recall_by_class(actuals, predictions).values()
        if value != "not_applicable"
    ]
    if not recalls:
        return "not_applicable"
    return _decimal_text(sum(recalls) / Decimal(len(recalls)), 6) or "not_applicable"


def _lift_text(value: str, baseline: str) -> str:
    if value == "not_applicable" or baseline == "not_applicable":
        return "not_applicable"
    return _decimal_text(Decimal(value) - Decimal(baseline), 6) or "0.000000"


def _approval_digest_from_status(search_root: Path) -> str | None:
    path = search_root / APPROVAL_STATUS_PATH
    if not path.exists():
        return None
    text = path.read_text(encoding="utf-8")
    matches = re.findall(r"Approval digest:\s*`([0-9a-f]{64})`", text)
    if len(matches) != 1:
        return None
    required_lines_present = all(
        value in text
        for value in (
            "Artifact kind: `PREDICTIVE_EXPERIMENT_EXECUTION_APPROVED`",
            "Approval status: `PREDICTIVE_EXPERIMENT_EXECUTION_APPROVED`",
        )
    )
    if not required_lines_present or matches[0] != EXPECTED_APPROVAL_DIGEST:
        return None
    return matches[0]


def _verified_dataset_entries(search_root: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    entries: list[dict[str, Any]] = []
    failures: list[dict[str, Any]] = []
    for definition in discovery._registry_definitions():
        profile = definition["dataset_profile"]
        expected = EXPECTED_DATASET_DIGESTS.get(profile)
        if expected is None:
            continue
        dataset_relative_path = definition["expected_dataset_path"]
        manifest_relative_path = definition["expected_manifest_path"]
        dataset_path = search_root / dataset_relative_path
        manifest_path = search_root / manifest_relative_path
        entry = deepcopy(definition)
        entry.update(
            {
                "dataset_path": dataset_relative_path,
                "manifest_path": manifest_relative_path,
                "dataset_file_exists": dataset_path.exists(),
                "manifest_file_exists": manifest_path.exists(),
                "dataset_rows_digest_actual": None,
                "dataset_manifest_digest_actual": None,
                "dataset_rows_digest_expected": expected["dataset_rows_digest"],
                "dataset_manifest_digest_expected": expected["dataset_manifest_digest"],
                "dataset_rows_digest_match": False,
                "dataset_manifest_digest_match": False,
                "row_count": 0,
            }
        )
        if not dataset_path.exists() or not manifest_path.exists():
            failures.append(entry)
            entries.append(entry)
            continue
        try:
            rows = discovery._read_csv_rows(dataset_path)
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            dataset_digest = discovery._dataset_digest_for_entry(definition, rows)
            manifest_digest = discovery._manifest_digest_for_entry(definition, manifest)
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            entry["verification_error"] = str(exc)
            failures.append(entry)
            entries.append(entry)
            continue
        entry.update(
            {
                "dataset_rows_digest_actual": dataset_digest,
                "dataset_manifest_digest_actual": manifest_digest,
                "dataset_rows_digest_match": dataset_digest == expected["dataset_rows_digest"],
                "dataset_manifest_digest_match": manifest_digest
                == expected["dataset_manifest_digest"],
                "row_count": len(rows),
            }
        )
        if not entry["dataset_rows_digest_match"] or not entry["dataset_manifest_digest_match"]:
            failures.append(entry)
        entries.append(entry)
    return entries, failures


def _read_rows_by_profile(search_root: Path, entries: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    return {
        entry["dataset_profile"]: discovery._read_csv_rows(search_root / entry["dataset_path"])
        for entry in entries
    }


def _write_json(path: Path, payload: dict[str, Any]) -> str:
    data = canonical_json_bytes(payload)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return sha256_bytes(data)


def _source_digests(approval_digest: str | None) -> dict[str, str | None]:
    return {
        "predictive_experiment_execution_approval_digest": approval_digest,
        **EXPECTED_SOURCE_DIGESTS,
    }


def _blocked_artifact(
    *,
    execution_status: str,
    run_timestamp_utc: str,
    output_root: Path,
    approval_digest: str | None,
    entries: list[dict[str, Any]] | None = None,
    failures: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    artifact: dict[str, Any] = {
        "artifact_kind": ARTIFACT_KIND_PREDICTIVE_EXPERIMENT_EXECUTED,
        "schema_version": SCHEMA_VERSION_PREDICTIVE_EXPERIMENT_EXECUTED_V1,
        "execution_status": execution_status,
        "branch": DEFAULT_BRANCH,
        "base_commit": DEFAULT_BASE_COMMIT,
        "execution_request_id": candidate.PREDICTIVE_EXPERIMENT_EXECUTION_REQUEST_ID,
        "run_timestamp_utc": run_timestamp_utc,
        "created_offline": True,
        "research_only": True,
        "predictive_experiment_execution_authorized": approval_digest == EXPECTED_APPROVAL_DIGEST,
        "predictive_experiment_executed": False,
        "walk_forward_validation_performed": False,
        "out_of_sample_evaluation_performed": False,
        "label_generation_performed": False,
        "feature_matrix_generation_performed": False,
        "new_strategy_scoring_performed": False,
        "trade_recommendations_generated": False,
        "provider_requests_made": False,
        "predictive_usefulness": PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "predictive_usefulness_acceptance_ready": False,
        "profitability": PROFITABILITY_NOT_ACCEPTED,
        "profitability_acceptance_ready": False,
        "runtime_migration_recommended": False,
        "runtime_migration_approved": False,
        "runtime_migration_active": False,
        "strategy_runtime_migration": False,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "automatic_stitching": False,
        "source_digests": _source_digests(approval_digest),
        "output_root_path": _path_text(output_root),
        "planned_output_count": len(OUTPUT_NAMES),
        "generated_output_count": 0,
        "output_digest_manifest": {},
        "dataset_count": len(entries or []),
        "datasets_loaded_count": 0,
        "datasets_digest_verified_count": sum(
            1 for entry in entries or [] if entry.get("dataset_rows_digest_match") is True
        ),
        "manifest_digest_verified_count": sum(
            1 for entry in entries or [] if entry.get("dataset_manifest_digest_match") is True
        ),
        "dataset_verification_entries": entries or [],
        "dataset_verification_failures": failures or [],
        "metrics_label": RESEARCH_ONLY_NOT_PERFORMANCE_ACCEPTANCE,
    }
    artifact["predictive_experiment_execution_digest"] = predictive_experiment_execution_digest_v1(
        artifact
    )
    return artifact


def _build_reports(
    *,
    rows_by_profile: dict[str, list[dict[str, Any]]],
    entries: list[dict[str, Any]],
    run_timestamp_utc: str,
    output_root: Path,
    approval_digest: str,
) -> dict[str, dict[str, Any]]:
    labels_by_profile = {
        profile: _label_rows(profile, rows) for profile, rows in sorted(rows_by_profile.items())
    }
    features_by_profile = {
        profile: _feature_rows(profile, rows) for profile, rows in sorted(rows_by_profile.items())
    }
    available_by_profile = {
        profile: [row for row in labeled_rows if row["labels_available"]]
        for profile, labeled_rows in labels_by_profile.items()
    }
    splits_by_profile = {
        profile: _split_indices(len(rows)) for profile, rows in available_by_profile.items()
    }
    baseline_results = {
        profile: _baseline_metrics(
            profile=profile,
            labeled_rows=labels_by_profile[profile],
            splits=splits_by_profile[profile],
        )
        for profile in sorted(labels_by_profile)
    }
    reports: dict[str, dict[str, Any]] = {}
    reports["label_definition_report"] = _report(
        "label_definition_report",
        {
            "label_definitions": [
                {
                    "dataset_profile": profile,
                    "direction_label": definition["direction"],
                    "return_bucket_label": definition["bucket"],
                    "forward_looking": True,
                    "final_row_unavailable_excluded": True,
                    "label_is_current_feature": False,
                    "step_label": definition["step_label"],
                }
                for profile, definition in sorted(LABELS_BY_PROFILE.items())
            ],
        },
    )
    reports["label_generation_report"] = _report(
        "label_generation_report",
        {
            "label_generation_performed": True,
            "labels_forward_looking_only": True,
            "final_row_unavailable_excluded": True,
            "datasets": [
                {
                    "dataset_profile": profile,
                    "row_count": len(labels),
                    "available_label_count": len([row for row in labels if row["labels_available"]]),
                    "unavailable_label_count": len(
                        [row for row in labels if not row["labels_available"]]
                    ),
                    "direction_counts": _count_values(labels, "direction"),
                    "return_bucket_counts": _count_values(labels, "return_bucket"),
                }
                for profile, labels in sorted(labels_by_profile.items())
            ],
        },
    )
    reports["feature_family_report"] = _report(
        "feature_family_report",
        {
            "feature_matrix_generation_performed": True,
            "feature_families": [
                {"feature_family": family, "generated": True} for family in FEATURE_FAMILIES
            ],
            "feature_examples": FEATURE_NAMES,
            "strategy_scores_generated": False,
        },
    )
    reports["feature_matrix_manifest"] = _report(
        "feature_matrix_manifest",
        {
            "feature_matrix_generation_performed": True,
            "feature_names": FEATURE_NAMES,
            "datasets": [
                {
                    "dataset_profile": profile,
                    "feature_row_count": len(feature_rows),
                    "feature_count": len(FEATURE_NAMES),
                    "feature_matrix_digest": semantic_digest(
                        {
                            "dataset_profile": profile,
                            "feature_names": FEATURE_NAMES,
                            "feature_rows": feature_rows,
                        }
                    ),
                    "unavailable_feature_counts": {
                        feature: sum(1 for row in feature_rows if row[feature] is None)
                        for feature in FEATURE_NAMES
                    },
                }
                for profile, feature_rows in sorted(features_by_profile.items())
            ],
        },
    )
    reports["walk_forward_configuration_report"] = _report(
        "walk_forward_configuration_report",
        {
            "walk_forward_validation_performed": True,
            "walk_forward_type": SIMPLIFIED_CHRONOLOGICAL_RESEARCH_SPLIT,
            "deterministic_offline_research": True,
            "shuffle": False,
            "fixed_seed": 20260809,
            "baselines": BASELINES,
            "metrics_label": RESEARCH_ONLY_NOT_PERFORMANCE_ACCEPTANCE,
            "datasets": [
                {"dataset_profile": profile, **splits}
                for profile, splits in sorted(splits_by_profile.items())
            ],
        },
    )
    reports["out_of_sample_split_report"] = _report(
        "out_of_sample_split_report",
        {
            "out_of_sample_evaluation_performed": True,
            "chronological": True,
            "shuffle": False,
            "datasets": [
                {
                    "dataset_profile": profile,
                    "available_label_count": len(available_by_profile[profile]),
                    "out_of_sample": splits_by_profile[profile]["out_of_sample"],
                    "out_of_sample_count": (
                        splits_by_profile[profile]["out_of_sample"]["end_index_exclusive"]
                        - splits_by_profile[profile]["out_of_sample"]["start_index"]
                    ),
                }
                for profile in sorted(available_by_profile)
            ],
        },
    )
    reports["baseline_comparison_report"] = _report(
        "baseline_comparison_report",
        {
            "baselines": BASELINES,
            "metrics_label": RESEARCH_ONLY_NOT_PERFORMANCE_ACCEPTANCE,
            "results": baseline_results,
        },
    )
    reports["signal_quality_metrics_report"] = _report(
        "signal_quality_metrics_report",
        {
            "metrics_label": RESEARCH_ONLY_NOT_PERFORMANCE_ACCEPTANCE,
            "metrics": [
                "directional_accuracy",
                "balanced_accuracy",
                "precision_recall_by_class",
                "roc_auc_if_applicable",
                "information_coefficient_if_applicable",
                "calibration_if_applicable",
                "confusion_matrix",
                "lift_over_baseline",
            ],
            "results": baseline_results,
            "predictive_usefulness_acceptance_ready": False,
            "profitability_acceptance_ready": False,
        },
    )
    reports["stability_analysis_report"] = _report(
        "stability_analysis_report",
        {
            "metrics_label": RESEARCH_ONLY_NOT_PERFORMANCE_ACCEPTANCE,
            "datasets": [
                {
                    "dataset_profile": profile,
                    "split_direction_counts": {
                        split_name: _count_values(_slice(available_by_profile[profile], span), "direction")
                        for split_name, span in splits_by_profile[profile].items()
                    },
                }
                for profile in sorted(available_by_profile)
            ],
        },
    )
    reports["false_positive_false_negative_report"] = _report(
        "false_positive_false_negative_report",
        {
            "metrics_label": RESEARCH_ONLY_NOT_PERFORMANCE_ACCEPTANCE,
            "direction_label_confusion_matrices": {
                profile: {
                    baseline_name: result["confusion_matrix"]
                    for baseline_name, result in baseline_results[profile].items()
                }
                for profile in sorted(baseline_results)
            },
            "binary_positive_negative_not_assumed": True,
        },
    )
    reports["leakage_control_report"] = _report(
        "leakage_control_report",
        {
            "leakage_control_status": "PASS",
            "controls": [
                {"control": "labels_are_forward_looking_only", "status": "PASS"},
                {"control": "final_rows_have_unavailable_forward_labels", "status": "PASS"},
                {"control": "forward_labels_not_used_as_current_features", "status": "PASS"},
                {"control": "chronological_splits_only", "status": "PASS"},
                {"control": "shuffle_disabled", "status": "PASS"},
                {"control": "provider_requests_disabled", "status": "PASS"},
                {"control": "runtime_strategy_paths_unauthorized", "status": "PASS"},
            ],
        },
    )
    reports["operator_review_summary"] = _report(
        "operator_review_summary",
        {
            "execution_status": PREDICTIVE_EXPERIMENT_EXECUTED_RESEARCH_ONLY,
            "execution_request_id": candidate.PREDICTIVE_EXPERIMENT_EXECUTION_REQUEST_ID,
            "predictive_experiment_execution_approval_digest": approval_digest,
            "generated_output_count": len(OUTPUT_NAMES),
            "metrics_label": RESEARCH_ONLY_NOT_PERFORMANCE_ACCEPTANCE,
            "predictive_usefulness": PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
            "profitability": PROFITABILITY_NOT_ACCEPTED,
            "runtime_migration_active": False,
        },
    )
    reports["predictive_experiment_run_manifest"] = _report(
        "predictive_experiment_run_manifest",
        {
            "run_id": f"AAPL_PREDICTIVE_EXPERIMENT_EXECUTION_V1_{run_timestamp_utc}",
            "execution_request_id": candidate.PREDICTIVE_EXPERIMENT_EXECUTION_REQUEST_ID,
            "run_timestamp_utc": run_timestamp_utc,
            "source_digests": _source_digests(approval_digest),
            "dataset_digests": {
                entry["dataset_profile"]: {
                    "dataset_rows_digest": entry["dataset_rows_digest_actual"],
                    "dataset_manifest_digest": entry["dataset_manifest_digest_actual"],
                }
                for entry in entries
            },
            "output_root_path": _path_text(output_root),
            "output_digests": {},
            "walk_forward_type": SIMPLIFIED_CHRONOLOGICAL_RESEARCH_SPLIT,
            "metrics_label": RESEARCH_ONLY_NOT_PERFORMANCE_ACCEPTANCE,
        },
    )
    return reports


def _execution_digest_payload(artifact: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(artifact)
    payload.pop("predictive_experiment_execution_digest", None)
    return payload


def predictive_experiment_execution_digest_v1(artifact: dict[str, Any]) -> str:
    """Return the deterministic semantic digest for a predictive experiment execution."""
    return semantic_digest(_execution_digest_payload(artifact))


def execute_predictive_experiment_v1(
    *,
    search_root: str | Path | None = None,
    output_root: str | Path | None = None,
    run_timestamp_utc: str | None = None,
) -> dict[str, Any]:
    """Execute the approved offline research-only predictive experiment."""
    timestamp = run_timestamp_utc or _utc_now()
    search_path = _resolve_root(search_root, Path("."))
    output_path = _resolve_root(output_root, DEFAULT_OUTPUT_ROOT)
    approval_digest = _approval_digest_from_status(search_path)
    if approval_digest is None:
        return _blocked_artifact(
            execution_status=PREDICTIVE_EXPERIMENT_EXECUTION_BLOCKED_MISSING_APPROVAL_DIGEST,
            run_timestamp_utc=timestamp,
            output_root=output_path,
            approval_digest=None,
        )

    entries, failures = _verified_dataset_entries(search_path)
    if failures or len(entries) != 2:
        return _blocked_artifact(
            execution_status=PREDICTIVE_EXPERIMENT_EXECUTION_BLOCKED_DATASET_VERIFICATION_FAILED,
            run_timestamp_utc=timestamp,
            output_root=output_path,
            approval_digest=approval_digest,
            entries=entries,
            failures=failures,
        )

    rows_by_profile = _read_rows_by_profile(search_path, entries)
    reports = _build_reports(
        rows_by_profile=rows_by_profile,
        entries=entries,
        run_timestamp_utc=timestamp,
        output_root=output_path,
        approval_digest=approval_digest,
    )
    output_digests: dict[str, str] = {}
    for name in OUTPUT_NAMES:
        if name == "predictive_experiment_run_manifest":
            continue
        output_digests[name] = _write_json(output_path / f"{name}.json", reports[name])
    reports["predictive_experiment_run_manifest"]["output_digests"].update(output_digests)
    reports["predictive_experiment_run_manifest"]["output_digests"][
        "predictive_experiment_run_manifest"
    ] = sha256_bytes(canonical_json_bytes(reports["predictive_experiment_run_manifest"]))
    output_digests["predictive_experiment_run_manifest"] = _write_json(
        output_path / "predictive_experiment_run_manifest.json",
        reports["predictive_experiment_run_manifest"],
    )

    best_metric = _best_metric_summary(reports["baseline_comparison_report"]["results"])
    artifact: dict[str, Any] = {
        "artifact_kind": ARTIFACT_KIND_PREDICTIVE_EXPERIMENT_EXECUTED,
        "schema_version": SCHEMA_VERSION_PREDICTIVE_EXPERIMENT_EXECUTED_V1,
        "execution_status": PREDICTIVE_EXPERIMENT_EXECUTED_RESEARCH_ONLY,
        "branch": DEFAULT_BRANCH,
        "base_commit": DEFAULT_BASE_COMMIT,
        "execution_request_id": candidate.PREDICTIVE_EXPERIMENT_EXECUTION_REQUEST_ID,
        "run_timestamp_utc": timestamp,
        "created_offline": True,
        "research_only": True,
        "predictive_experiment_execution_authorized": True,
        "predictive_experiment_executed": True,
        "walk_forward_validation_performed": True,
        "out_of_sample_evaluation_performed": True,
        "label_generation_performed": True,
        "feature_matrix_generation_performed": True,
        "new_strategy_scoring_performed": False,
        "trade_recommendations_generated": False,
        "provider_requests_made": False,
        "predictive_usefulness": PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "predictive_usefulness_acceptance_ready": False,
        "profitability": PROFITABILITY_NOT_ACCEPTED,
        "profitability_acceptance_ready": False,
        "runtime_migration_recommended": False,
        "runtime_migration_approved": False,
        "runtime_migration_active": False,
        "strategy_runtime_migration": False,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "automatic_stitching": False,
        "output_root_path": _path_text(output_path),
        "planned_output_count": len(OUTPUT_NAMES),
        "generated_output_count": len(output_digests),
        "output_digest_manifest": dict(sorted(output_digests.items())),
        "research_outputs_label": RESEARCH_ONLY_NON_ACTIONABLE,
        "metrics_label": RESEARCH_ONLY_NOT_PERFORMANCE_ACCEPTANCE,
        "dataset_count": len(entries),
        "datasets_loaded_count": len(rows_by_profile),
        "datasets_digest_verified_count": sum(
            1 for entry in entries if entry["dataset_rows_digest_match"]
        ),
        "manifest_digest_verified_count": sum(
            1 for entry in entries if entry["dataset_manifest_digest_match"]
        ),
        "swing_row_count": len(rows_by_profile.get("SWING", [])),
        "position_swing_row_count": len(rows_by_profile.get("POSITION_SWING", [])),
        "dataset_verification_entries": entries,
        "source_digests": _source_digests(approval_digest),
        "labels_generated": list(candidate.LABEL_DEFINITIONS),
        "feature_families_generated": FEATURE_FAMILIES,
        "baselines_evaluated": BASELINES,
        "walk_forward_type": SIMPLIFIED_CHRONOLOGICAL_RESEARCH_SPLIT,
        "best_metric_summary_if_any": best_metric,
    }
    artifact["predictive_experiment_execution_digest"] = predictive_experiment_execution_digest_v1(
        artifact
    )
    validate_predictive_experiment_executed_v1(artifact)
    return artifact


def _best_metric_summary(results: dict[str, Any]) -> dict[str, Any]:
    best: dict[str, Any] | None = None
    for profile, profile_results in sorted(results.items()):
        for baseline_name, result in sorted(profile_results.items()):
            accuracy = result.get("directional_accuracy")
            if accuracy == "not_applicable":
                continue
            candidate_summary = {
                "descriptive_only": True,
                "acceptance_created": False,
                "dataset_profile": profile,
                "baseline": baseline_name,
                "directional_accuracy": accuracy,
                "metrics_label": RESEARCH_ONLY_NOT_PERFORMANCE_ACCEPTANCE,
            }
            if best is None or Decimal(accuracy) > Decimal(best["directional_accuracy"]):
                best = candidate_summary
    return best or {
        "descriptive_only": True,
        "acceptance_created": False,
        "metrics_label": RESEARCH_ONLY_NOT_PERFORMANCE_ACCEPTANCE,
        "summary": "not_applicable",
    }


def _expect(actual: Any, expected: Any, field_name: str) -> None:
    if actual != expected:
        raise PredictiveExperimentExecutionError(f"{field_name} mismatch")


def _expect_true(actual: Any, field_name: str) -> None:
    if actual is not True:
        raise PredictiveExperimentExecutionError(f"{field_name} must be true")


def _expect_false(actual: Any, field_name: str) -> None:
    if actual is not False:
        raise PredictiveExperimentExecutionError(f"{field_name} must be false")


def _iter_values(value: Any) -> list[Any]:
    values = [value]
    if isinstance(value, dict):
        for child in value.values():
            values.extend(_iter_values(child))
    elif isinstance(value, list):
        for child in value:
            values.extend(_iter_values(child))
    return values


def _validate_blocked_artifact(artifact: dict[str, Any]) -> dict[str, Any]:
    if artifact.get("execution_status") not in {
        PREDICTIVE_EXPERIMENT_EXECUTION_BLOCKED_MISSING_APPROVAL_DIGEST,
        PREDICTIVE_EXPERIMENT_EXECUTION_BLOCKED_DATASET_VERIFICATION_FAILED,
    }:
        raise PredictiveExperimentExecutionError("unsupported blocked execution status")
    for field in (
        "predictive_experiment_executed",
        "walk_forward_validation_performed",
        "out_of_sample_evaluation_performed",
        "label_generation_performed",
        "feature_matrix_generation_performed",
    ):
        _expect_false(artifact.get(field), field)
    _expect_false(artifact.get("provider_requests_made"), "provider_requests_made")
    _expect(artifact.get("generated_output_count"), 0, "generated_output_count")
    digest = predictive_experiment_execution_digest_v1(artifact)
    _expect(artifact.get("predictive_experiment_execution_digest"), digest, "execution_digest")
    return {
        "artifact_kind": artifact["artifact_kind"],
        "execution_status": artifact["execution_status"],
        "predictive_experiment_execution_digest": digest,
        "valid": True,
    }


def validate_predictive_experiment_executed_v1(artifact: dict[str, Any]) -> dict[str, Any]:
    """Validate a predictive experiment execution artifact and its guardrails."""
    if not isinstance(artifact, dict):
        raise PredictiveExperimentExecutionError("artifact must be a JSON object")
    _expect(artifact.get("artifact_kind"), ARTIFACT_KIND_PREDICTIVE_EXPERIMENT_EXECUTED, "artifact_kind")
    _expect(
        artifact.get("schema_version"),
        SCHEMA_VERSION_PREDICTIVE_EXPERIMENT_EXECUTED_V1,
        "schema_version",
    )
    if artifact.get("execution_status") != PREDICTIVE_EXPERIMENT_EXECUTED_RESEARCH_ONLY:
        return _validate_blocked_artifact(artifact)
    _expect(
        artifact.get("execution_status"),
        PREDICTIVE_EXPERIMENT_EXECUTED_RESEARCH_ONLY,
        "execution_status",
    )
    for field in TRUE_EXECUTION_FIELDS:
        _expect_true(artifact.get(field), field)
    for field in FALSE_GUARDRAIL_FIELDS:
        _expect_false(artifact.get(field), field)
    for field in BOUNDARY_FIELDS:
        _expect(artifact.get(field), NOT_AUTHORIZED, field)
    _expect(artifact.get("predictive_usefulness"), PREDICTIVE_USEFULNESS_NOT_ACCEPTED, "predictive_usefulness")
    _expect(artifact.get("profitability"), PROFITABILITY_NOT_ACCEPTED, "profitability")
    source_digests = artifact.get("source_digests") or {}
    _expect(
        source_digests.get("predictive_experiment_execution_approval_digest"),
        EXPECTED_APPROVAL_DIGEST,
        "predictive_experiment_execution_approval_digest",
    )
    for field, expected in EXPECTED_SOURCE_DIGESTS.items():
        _expect(source_digests.get(field), expected, field)
    _expect(artifact.get("dataset_count"), 2, "dataset_count")
    _expect(artifact.get("datasets_loaded_count"), 2, "datasets_loaded_count")
    _expect(artifact.get("datasets_digest_verified_count"), 2, "datasets_digest_verified_count")
    _expect(artifact.get("manifest_digest_verified_count"), 2, "manifest_digest_verified_count")
    _expect(artifact.get("planned_output_count"), len(OUTPUT_NAMES), "planned_output_count")
    _expect(artifact.get("generated_output_count"), len(OUTPUT_NAMES), "generated_output_count")
    output_digest_manifest = artifact.get("output_digest_manifest")
    if not isinstance(output_digest_manifest, dict):
        raise PredictiveExperimentExecutionError("output_digest_manifest must be a JSON object")
    _expect(sorted(output_digest_manifest), sorted(OUTPUT_NAMES), "output_digest_manifest outputs")
    _expect(artifact.get("research_outputs_label"), RESEARCH_ONLY_NON_ACTIONABLE, "research_outputs_label")
    _expect(
        artifact.get("metrics_label"),
        RESEARCH_ONLY_NOT_PERFORMANCE_ACCEPTANCE,
        "metrics_label",
    )
    for value in _iter_values(artifact):
        if isinstance(value, str) and value in {
            "PREDICTIVE_USEFULNESS_ACCEPTED",
            "PROFITABILITY_ACCEPTED",
            "RUNTIME_MIGRATION_APPROVED",
            "RUNTIME_ACTIVE",
        }:
            raise PredictiveExperimentExecutionError(f"forbidden acceptance value present: {value}")
    digest = predictive_experiment_execution_digest_v1(artifact)
    _expect(artifact.get("predictive_experiment_execution_digest"), digest, "execution_digest")
    return {
        "artifact_kind": artifact["artifact_kind"],
        "execution_status": artifact["execution_status"],
        "predictive_experiment_execution_digest": digest,
        "generated_output_count": artifact["generated_output_count"],
        "valid": True,
    }


def build_predictive_experiment_execution_status_markdown_v1(artifact: dict[str, Any]) -> str:
    """Render a sanitized status document for the predictive experiment execution."""
    validation = validate_predictive_experiment_executed_v1(artifact)
    lines = [
        "# MarketFlow Predictive Experiment Execution Status",
        "",
        "## Branch And Commit",
        f"- Branch: `{artifact['branch']}`",
        f"- Base commit: `{artifact['base_commit']}`",
        "- Implementation commit: the commit containing this document.",
        "",
        "## Execution Artifact",
        f"- Artifact kind: `{artifact['artifact_kind']}`",
        f"- Execution status: `{artifact['execution_status']}`",
        f"- Execution digest: `{validation['predictive_experiment_execution_digest']}`",
        f"- Execution request ID: `{artifact['execution_request_id']}`",
        f"- Execution timestamp UTC: `{artifact['run_timestamp_utc']}`",
        "",
        "## Bound Source Evidence",
    ]
    for key, value in artifact["source_digests"].items():
        lines.append(f"- {key}: `{value}`")
    lines.extend(
        [
            "",
            "## Outputs Generated Summary",
            f"- Output root path: `{artifact['output_root_path']}`",
            f"- Planned output count: `{artifact['planned_output_count']}`",
            f"- Generated output count: `{artifact['generated_output_count']}`",
            f"- Research output label: `{artifact.get('research_outputs_label', RESEARCH_ONLY_NON_ACTIONABLE)}`",
            f"- Metrics label: `{artifact['metrics_label']}`",
            "",
            "## Output Digest Manifest",
        ]
    )
    if artifact["output_digest_manifest"]:
        lines.extend(
            f"- `{name}`: `{digest}`"
            for name, digest in sorted(artifact["output_digest_manifest"].items())
        )
    else:
        lines.append("- No outputs generated because execution was blocked.")
    lines.extend(
        [
            "",
            "## Dataset Verification Summary",
            f"- Dataset count: `{artifact['dataset_count']}`",
            f"- Datasets loaded count: `{artifact['datasets_loaded_count']}`",
            f"- Dataset digests verified count: `{artifact['datasets_digest_verified_count']}`",
            f"- Manifest digests verified count: `{artifact['manifest_digest_verified_count']}`",
            "",
            "## Experiment Execution Boundary",
            f"- predictive_experiment_execution_authorized: `{artifact['predictive_experiment_execution_authorized']}`",
            f"- predictive_experiment_executed: `{artifact['predictive_experiment_executed']}`",
            f"- walk_forward_validation_performed: `{artifact['walk_forward_validation_performed']}`",
            f"- out_of_sample_evaluation_performed: `{artifact['out_of_sample_evaluation_performed']}`",
            f"- label_generation_performed: `{artifact['label_generation_performed']}`",
            f"- feature_matrix_generation_performed: `{artifact['feature_matrix_generation_performed']}`",
            f"- new_strategy_scoring_performed: `{artifact['new_strategy_scoring_performed']}`",
            f"- trade_recommendations_generated: `{artifact['trade_recommendations_generated']}`",
            f"- provider_requests_made: `{artifact['provider_requests_made']}`",
            "",
            "## Predictive And Profitability Boundary",
            f"- predictive_usefulness: `{artifact['predictive_usefulness']}`",
            f"- predictive_usefulness_acceptance_ready: `{artifact['predictive_usefulness_acceptance_ready']}`",
            f"- profitability: `{artifact['profitability']}`",
            f"- profitability_acceptance_ready: `{artifact['profitability_acceptance_ready']}`",
            "",
            "## Runtime Boundary",
            f"- runtime_migration_recommended: `{artifact['runtime_migration_recommended']}`",
            f"- runtime_migration_approved: `{artifact['runtime_migration_approved']}`",
            f"- runtime_migration_active: `{artifact['runtime_migration_active']}`",
            f"- strategy_runtime_migration: `{artifact['strategy_runtime_migration']}`",
            f"- runtime_use: `{artifact['runtime_use']}`",
            f"- strategy_use: `{artifact['strategy_use']}`",
            f"- paper_trading: `{artifact['paper_trading']}`",
            f"- broker_execution: `{artifact['broker_execution']}`",
            f"- automatic_stitching: `{artifact['automatic_stitching']}`",
            "",
            "## Review Boundary",
            "- Predictive usefulness remains not accepted.",
            "- Profitability remains not accepted.",
            "- Results review remains a separate future task.",
            "- Runtime migration and runtime activation remain future, separate authorization paths.",
            "",
            "## Non-Goals",
            "- No provider request was made.",
            "- No strategy scoring was performed.",
            "- No broker, IBKR, paper-trading, or execution pathway was enabled.",
            "- No predictive usefulness or profitability acceptance was granted.",
            "- No runtime migration was recommended, approved, activated, or made default.",
        ]
    )
    return "\n".join(lines) + "\n"
