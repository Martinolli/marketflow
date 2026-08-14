"""Deterministic offline canonical-dataset generation from sanitized evidence."""

from __future__ import annotations

import json
from copy import deepcopy
from datetime import UTC, datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import canonical_dataset_generation_approval_service as approval_service


ARTIFACT_KIND_CANONICAL_DATASET_GENERATED = "CANONICAL_DATASET_GENERATED"
ARTIFACT_KIND_CANONICAL_DATASET_GENERATION_BLOCKED = "CANONICAL_DATASET_GENERATION_BLOCKED"
SCHEMA_VERSION_CANONICAL_DATASET_GENERATED_V1 = "canonical_dataset_generated_v1"
CANONICAL_DATASET_GENERATED_RESEARCH_ONLY = "CANONICAL_DATASET_GENERATED_RESEARCH_ONLY"
CANONICAL_DATASET_GENERATION_BLOCKED_MISSING_OR_INVALID_SOURCE_EVIDENCE = (
    "CANONICAL_DATASET_GENERATION_BLOCKED_MISSING_OR_INVALID_SOURCE_EVIDENCE"
)
OUTPUT_LABEL = "RESEARCH_ONLY_NON_ACTIONABLE"
DATASET_SCOPE = "CANONICAL_DATASET_GENERATION_RESEARCH_ONLY"
SOURCE_EVIDENCE_SCOPE = "READ_ONLY_HISTORICAL_MARKET_DATA_ACQUISITION_REQUESTS_ONLY"
NOT_AUTHORIZED = "NOT_AUTHORIZED"
NOT_ACCEPTED = "not accepted"
PROFITABILITY_NOT_ACCEPTED = "not accepted"
PASS = "PASS"
WARNING = "WARNING"

TARGET_UNIVERSE = list(approval_service.TARGET_UNIVERSE)
SOURCE_PROFILE = deepcopy(approval_service.SOURCE_PROFILE)
EXPECTED_RECORD_COUNTS = {ticker: (913 if ticker == "META" else 1003) for ticker in TARGET_UNIVERSE}
EXPECTED_TOTAL_CANONICAL_RECORD_COUNT = 11946
EXPECTED_GENERATED_OUTPUT_COUNT = 9
EXPECTED_CANONICAL_DATASET_GENERATION_APPROVAL_DIGEST = (
    "0b287370e8eddad522765a2ee77c39765f6690b27468bcc2f5b28587330a63b2"
)

EXPECTED_SOURCE_OUTPUT_SHA256 = {
    "acquisition_provider_evidence_run_manifest.json": "ad2de2a4493e7d0c7bd5d3bd62dce20b7a09b3c4dad1ab56008b468fddbfed07",
    "acquisition_provider_request_receipts_sanitized.json": "812677a5d378a5255c7e674ed416499e457bb69320dde8ab780ca07fdd547a66",
    "acquisition_evidence_results_sanitized.json": "51d970eedb72019c5d3fcffe1ccf10475a3480c9c9deb28b9a3d1e67442373fd",
    "acquisition_data_quality_summary.json": "147bbfbb96318a39b4c6b4ae4a865e593d4fa64369b7ac31ad8749af3af261c1",
    "acquisition_failure_reason_inventory.json": "98bbe551bc4bd1a1a7b6c9080f4967ab354652b8fe5c2f0d94a5152d2646978a",
    "acquisition_digest_manifest.json": "abbf00067830b06976c7f4bdf9396b6fe83f0edba306b7dc517994cae41270ed",
    "operator_review_summary.json": "c513a1ffb48ef8f124e4b466733f8fe2603d66887850b5f04cab9794f977e69b",
}
SOURCE_FILENAMES = list(EXPECTED_SOURCE_OUTPUT_SHA256)
OUTPUT_FILENAMES = [
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
DEFAULT_SOURCE_ROOT = Path(".marketflow/acquisition_provider_evidence/expanded_universe_v1")
DEFAULT_OUTPUT_ROOT = Path(".marketflow/canonical_datasets/expanded_universe_v1")


class CanonicalDatasetGenerationExecutionError(ValueError):
    """Raised when canonical generation or its evidence is invalid."""


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise CanonicalDatasetGenerationExecutionError(f"{field} mismatch")


def _expect_true(actual: Any, field: str) -> None:
    if actual is not True:
        raise CanonicalDatasetGenerationExecutionError(f"{field} must be true")


def _expect_false(actual: Any, field: str) -> None:
    if actual is not False:
        raise CanonicalDatasetGenerationExecutionError(f"{field} must be false")


def _expect_digest(actual: Any, field: str) -> None:
    if not isinstance(actual, str) or len(actual) != 64:
        raise CanonicalDatasetGenerationExecutionError(f"{field} missing")


def _common_output_fields() -> dict[str, Any]:
    return {
        "output_label": OUTPUT_LABEL,
        "dataset_scope": DATASET_SCOPE,
        "source_evidence_scope": SOURCE_EVIDENCE_SCOPE,
        "dataset_generation_authorized": True,
        "canonical_dataset_authorized": True,
        "canonical_dataset_generation_approved": True,
        "canonical_dataset_generation_executed": True,
        "canonical_dataset_generated": True,
        "canonical_dataset_frozen": False,
        "registry_approval_created": False,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": PROFITABILITY_NOT_ACCEPTED,
    }


def _blocked(reason: str) -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_CANONICAL_DATASET_GENERATION_BLOCKED,
        "schema_version": SCHEMA_VERSION_CANONICAL_DATASET_GENERATED_V1,
        "execution_status": CANONICAL_DATASET_GENERATION_BLOCKED_MISSING_OR_INVALID_SOURCE_EVIDENCE,
        "created_offline": True,
        "blocked_reason": reason,
        "canonical_dataset_generation_digest": "NOT_CREATED",
        "dataset_generation_performed": False,
        "canonical_dataset_candidate_created": False,
        "canonical_dataset_generation_executed": False,
        "canonical_dataset_generated": False,
        "canonical_dataset_frozen": False,
        "registry_approval_created": False,
        "generated_output_count": 0,
        "provider_requests_made_in_generation": False,
        "live_provider_transport_enabled_in_generation": False,
        "market_data_acquisition_performed_in_generation": False,
        "raw_provider_payloads_committed": False,
        "api_keys_stored_or_printed": False,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
    }


def _read_and_verify_source(root: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    missing = [name for name in SOURCE_FILENAMES if not (root / name).is_file()]
    if missing:
        raise CanonicalDatasetGenerationExecutionError("missing source evidence: " + ", ".join(missing))

    manifest = json.loads((root / "acquisition_digest_manifest.json").read_text(encoding="utf-8"))
    declared = {row.get("filename"): row.get("sha256") for row in manifest.get("output_digests", [])}
    source_digests: list[dict[str, Any]] = []
    is_default_root = root.resolve() == DEFAULT_SOURCE_ROOT.resolve()
    for name in SOURCE_FILENAMES:
        payload = (root / name).read_bytes()
        actual = sha256_bytes(payload)
        if is_default_root and actual != EXPECTED_SOURCE_OUTPUT_SHA256[name]:
            raise CanonicalDatasetGenerationExecutionError(f"{name} committed digest mismatch")
        if name not in {"acquisition_digest_manifest.json", "operator_review_summary.json"}:
            if declared.get(name) != actual:
                raise CanonicalDatasetGenerationExecutionError(f"{name} source manifest digest mismatch")
        source_digests.append({"filename": name, "sha256": actual, "verification_status": PASS})

    run_manifest = json.loads((root / "acquisition_provider_evidence_run_manifest.json").read_text(encoding="utf-8"))
    profile = run_manifest.get("acquisition_profile", {})
    _expect(profile.get("date_range_start"), SOURCE_PROFILE["date_range_start"], "source date_range_start")
    _expect(profile.get("date_range_end"), SOURCE_PROFILE["date_range_end"], "source date_range_end")
    _expect(profile.get("timeframe"), SOURCE_PROFILE["timeframe"], "source timeframe")
    _expect(profile.get("session_profile"), SOURCE_PROFILE["profile"], "source profile")
    _expect(run_manifest.get("target_universe"), TARGET_UNIVERSE, "source target_universe")
    _expect(run_manifest.get("evidence_scope"), SOURCE_EVIDENCE_SCOPE, "source evidence_scope")

    results = json.loads((root / "acquisition_evidence_results_sanitized.json").read_text(encoding="utf-8"))
    _expect(results.get("evidence_scope"), SOURCE_EVIDENCE_SCOPE, "results evidence_scope")
    rows = results.get("per_ticker_acquisition_evidence_results")
    if not isinstance(rows, list):
        raise CanonicalDatasetGenerationExecutionError("per-ticker source results missing")
    _expect([row.get("ticker") for row in rows], TARGET_UNIVERSE, "source result ticker order")
    for row in rows:
        ticker = row["ticker"]
        bars = row.get("sanitized_bars")
        if not isinstance(bars, list):
            raise CanonicalDatasetGenerationExecutionError(f"{ticker} sanitized bars missing")
        _expect(row.get("historical_bar_count"), EXPECTED_RECORD_COUNTS[ticker], f"{ticker} source bar count")
        _expect(len(bars), EXPECTED_RECORD_COUNTS[ticker], f"{ticker} sanitized bar count")
    return results, source_digests


def _decimal_string(value: Any, field: str) -> str | None:
    if value is None:
        return None
    try:
        number = Decimal(str(value))
    except (InvalidOperation, ValueError) as exc:
        raise CanonicalDatasetGenerationExecutionError(f"invalid numeric {field}") from exc
    if not number.is_finite():
        raise CanonicalDatasetGenerationExecutionError(f"non-finite numeric {field}")
    normalized = format(number.normalize(), "f")
    return "0" if Decimal(normalized) == 0 else normalized


def _timestamp_fields(value: Any) -> tuple[str, str]:
    try:
        timestamp_ms = int(str(value))
        instant = datetime.fromtimestamp(timestamp_ms / 1000, tz=UTC)
    except (ValueError, TypeError, OSError, OverflowError) as exc:
        raise CanonicalDatasetGenerationExecutionError("invalid source timestamp") from exc
    return instant.date().isoformat(), instant.isoformat().replace("+00:00", "Z")


def _canonical_records(results: Mapping[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    records: list[dict[str, Any]] = []
    summaries: list[dict[str, Any]] = []
    for source in results["per_ticker_acquisition_evidence_results"]:
        ticker = source["ticker"]
        metadata = source.get("provider_request_metadata", {})
        ticker_records: list[dict[str, Any]] = []
        previous_timestamp: str | None = None
        for source_bar in sorted(source["sanitized_bars"], key=lambda row: int(str(row["timestamp"]))):
            date, timestamp_utc = _timestamp_fields(source_bar.get("timestamp"))
            if previous_timestamp is not None and timestamp_utc <= previous_timestamp:
                raise CanonicalDatasetGenerationExecutionError(f"{ticker} timestamps are not unique ascending")
            previous_timestamp = timestamp_utc
            source_record_digest = semantic_digest({"ticker": ticker, "sanitized_source_bar": source_bar})
            record = {
                "ticker": ticker,
                "date": date,
                "timestamp_utc_or_session_date": timestamp_utc,
                "open": _decimal_string(source_bar.get("open"), "open"),
                "high": _decimal_string(source_bar.get("high"), "high"),
                "low": _decimal_string(source_bar.get("low"), "low"),
                "close": _decimal_string(source_bar.get("close"), "close"),
                "volume": _decimal_string(source_bar.get("volume"), "volume"),
                "vwap_if_available": _decimal_string(source_bar.get("volume_weighted_average_price"), "vwap"),
                "transactions_if_available": _decimal_string(source_bar.get("transaction_count"), "transactions"),
                "source_provider": metadata.get("provider_name") or "UNAVAILABLE_IN_SOURCE",
                "source_endpoint_mode": metadata.get("provider_endpoint_stability") or "UNAVAILABLE_IN_SOURCE",
                "source_profile": SOURCE_PROFILE["profile"],
                "adjustment_policy_status": source.get("adjustment_policy_status") or "UNAVAILABLE_IN_SOURCE",
                "calendar_session_status": source.get("calendar_alignment_status") or "UNAVAILABLE_IN_SOURCE",
                "source_record_digest": source_record_digest,
            }
            record["canonical_record_digest"] = semantic_digest(record)
            ticker_records.append(record)
        records.extend(ticker_records)
        summaries.append({
            "ticker": ticker,
            "canonical_record_count": len(ticker_records),
            "first_session_date": ticker_records[0]["date"],
            "last_session_date": ticker_records[-1]["date"],
            "meta_reduced_bar_count_preserved": ticker == "META",
            "per_ticker_canonical_records_digest": semantic_digest(ticker_records),
        })
    return records, summaries


def canonical_dataset_generation_digest_v1(artifact: dict[str, Any]) -> str:
    payload = deepcopy(artifact)
    payload.pop("canonical_dataset_generation_digest", None)
    payload.pop("canonical_output_digest_manifest", None)
    return semantic_digest(payload)


def _base_artifact(run_timestamp_utc: str, source_digests: list[dict[str, Any]], summaries: list[dict[str, Any]]) -> dict[str, Any]:
    counts = {row["ticker"]: row["canonical_record_count"] for row in summaries}
    return {
        "artifact_kind": ARTIFACT_KIND_CANONICAL_DATASET_GENERATED,
        "schema_version": SCHEMA_VERSION_CANONICAL_DATASET_GENERATED_V1,
        "execution_status": CANONICAL_DATASET_GENERATED_RESEARCH_ONLY,
        "run_timestamp_utc": run_timestamp_utc,
        "created_offline": True,
        "provider_requests_made_in_generation": False,
        "live_provider_transport_enabled_in_generation": False,
        "market_data_acquisition_performed_in_generation": False,
        "dataset_generation_performed": True,
        "raw_provider_payloads_committed": False,
        "api_keys_stored_or_printed": False,
        "canonical_dataset_chain_candidate_created": True,
        "canonical_dataset_chain_candidate_review_created": True,
        "canonical_dataset_chain_approved": True,
        "dataset_generation_authorized": True,
        "canonical_dataset_authorized": True,
        "canonical_dataset_generation_approved": True,
        "ready_for_canonical_dataset_generation_execution": True,
        "canonical_dataset_candidate_created": True,
        "canonical_dataset_generation_executed": True,
        "canonical_dataset_generated": True,
        "canonical_dataset_generation_results_created": True,
        "canonical_dataset_frozen": False,
        "registry_approval_created": False,
        "new_ticker_acquisition_authorized": True,
        "acquisition_generation_authorized": True,
        "acquisition_generation_approved": True,
        "acquisition_generation_frozen": True,
        "corporate_action_authority_created": True,
        "corporate_action_authority_approved": True,
        "corporate_action_authority_scope": "CORPORATE_ACTION_AUTHORITY_ONLY",
        "split_event_authority_created": True,
        "split_event_authority_frozen": True,
        "split_event_authority_scope": "SPLIT_EVENT_AUTHORITY_ONLY",
        "dividend_event_authority_created": True,
        "dividend_event_authority_frozen": True,
        "dividend_event_authority_scope": "DIVIDEND_EVENT_AUTHORITY_ONLY",
        "identity_authority_created": True,
        "identity_authority_frozen": True,
        "additional_predictive_evidence_execution_authorized": False,
        "additional_predictive_evidence_executed": False,
        "predictive_experiment_rerun_authorized": False,
        "predictive_experiment_rerun_performed": False,
        "feature_matrix_regeneration_performed": False,
        "new_strategy_scoring_performed": False,
        "trade_recommendations_generated": False,
        "research_only": True,
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": PROFITABILITY_NOT_ACCEPTED,
        "runtime_migration_approved": False,
        "runtime_migration_active": False,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "automatic_stitching": False,
        "output_label": OUTPUT_LABEL,
        "dataset_scope": DATASET_SCOPE,
        "source_evidence_scope": SOURCE_EVIDENCE_SCOPE,
        "canonical_dataset_generation_approval_digest": EXPECTED_CANONICAL_DATASET_GENERATION_APPROVAL_DIGEST,
        "canonical_dataset_chain_candidate_review_package_digest": approval_service.EXPECTED_CANONICAL_DATASET_CHAIN_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "canonical_dataset_chain_candidate_digest": approval_service.EXPECTED_CANONICAL_DATASET_CHAIN_CANDIDATE_DIGEST,
        "acquisition_generation_freeze_digest": approval_service.EXPECTED_ACQUISITION_GENERATION_FREEZE_DIGEST,
        "acquisition_generation_approval_digest": approval_service.EXPECTED_ACQUISITION_GENERATION_APPROVAL_DIGEST,
        "acquisition_evidence_results_review_package_digest": approval_service.EXPECTED_ACQUISITION_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST,
        "acquisition_provider_evidence_execution_digest": approval_service.EXPECTED_ACQUISITION_PROVIDER_EVIDENCE_EXECUTION_DIGEST,
        "corporate_action_authority_approval_digest": approval_service.EXPECTED_CORPORATE_ACTION_AUTHORITY_APPROVAL_DIGEST,
        "identity_authority_freeze_digest": approval_service.EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST,
        "ticker_universe_selection_approval_digest": approval_service.EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST,
        "target_universe": TARGET_UNIVERSE,
        "target_universe_count": 12,
        "canonical_dataset_source_profile": SOURCE_PROFILE,
        "per_ticker_record_counts": counts,
        "per_ticker_canonical_record_summary": summaries,
        "total_canonical_record_count": sum(counts.values()),
        "generated_output_count": EXPECTED_GENERATED_OUTPUT_COUNT,
        "source_output_digest_verification_status": PASS,
        "source_output_digest_manifest": source_digests,
        "failure_count": 0,
        "warning_count": 1,
        "warnings": ["META_REDUCED_BAR_COUNT_PRESERVED_EXACTLY_913_NO_REPAIR_OR_BACKFILL"],
    }


def _json_output(payload: Mapping[str, Any]) -> bytes:
    return canonical_json_bytes(dict(payload))


def _build_outputs(artifact: dict[str, Any], records: list[dict[str, Any]]) -> dict[str, bytes]:
    common = _common_output_fields()
    source_manifest = common | {
        "source_output_digest_verification_status": PASS,
        "source_output_digest_manifest": artifact["source_output_digest_manifest"],
        "bound_authority_digests": {
            key: artifact[key]
            for key in (
                "canonical_dataset_generation_approval_digest",
                "canonical_dataset_chain_candidate_review_package_digest",
                "canonical_dataset_chain_candidate_digest",
                "acquisition_generation_freeze_digest",
                "acquisition_generation_approval_digest",
                "acquisition_evidence_results_review_package_digest",
                "acquisition_provider_evidence_execution_digest",
                "corporate_action_authority_approval_digest",
                "identity_authority_freeze_digest",
                "ticker_universe_selection_approval_digest",
            )
        },
    }
    schema = common | {
        "schema_version": "canonical_dataset_record_schema_v1",
        "numeric_representation": "NORMALIZED_DECIMAL_STRING",
        "record_order": "APPROVED_TICKER_ORDER_THEN_TIMESTAMP_ASCENDING",
        "required_fields": [
            "ticker", "date", "timestamp_utc_or_session_date", "open", "high", "low", "close",
            "volume", "vwap_if_available", "transactions_if_available", "source_provider",
            "source_endpoint_mode", "source_profile", "adjustment_policy_status",
            "calendar_session_status", "source_record_digest", "canonical_record_digest",
        ],
        "optional_unavailable_representation": [None, "UNAVAILABLE_IN_SOURCE"],
    }
    ticker_summary = common | {
        "target_universe": TARGET_UNIVERSE,
        "per_ticker_canonical_record_summary": artifact["per_ticker_canonical_record_summary"],
        "total_canonical_record_count": artifact["total_canonical_record_count"],
    }
    quality = common | {
        "quality_status": "PASS_WITH_PRESERVED_SOURCE_LIMITATION",
        "failure_count": 0,
        "warning_count": 1,
        "warnings": artifact["warnings"],
        "no_missing_bars_fabricated": True,
        "no_backfill_performed": True,
        "meta_reduced_bar_count_preserved": True,
    }
    failures = common | {"failure_count": 0, "canonical_dataset_failure_reason_inventory": []}
    operator = common | {
        "operator_review_required": True,
        "execution_summary": {
            "target_count": 12,
            "date_range_start": SOURCE_PROFILE["date_range_start"],
            "date_range_end": SOURCE_PROFILE["date_range_end"],
            "timeframe": SOURCE_PROFILE["timeframe"],
            "profile": SOURCE_PROFILE["profile"],
            "per_ticker_record_counts": artifact["per_ticker_record_counts"],
            "total_canonical_record_count": artifact["total_canonical_record_count"],
            "generated_output_count": EXPECTED_GENERATED_OUTPUT_COUNT,
            "failure_count": 0,
            "warning_count": 1,
        },
        "next_task": "Canonical Dataset Results Review Package v1",
    }
    jsonl = b"".join(canonical_json_bytes(record) for record in records)
    return {
        "canonical_dataset_source_evidence_manifest.json": _json_output(source_manifest),
        "canonical_dataset_schema_contract.json": _json_output(schema),
        "canonical_dataset_records.jsonl": jsonl,
        "per_ticker_canonical_dataset_summary.json": _json_output(ticker_summary),
        "canonical_dataset_data_quality_report.json": _json_output(quality),
        "canonical_dataset_failure_reason_inventory.json": _json_output(failures),
        "operator_review_summary.json": _json_output(operator),
    }


def _digest_entries(artifact: dict[str, Any], outputs: Mapping[str, bytes]) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for name in OUTPUT_FILENAMES:
        if name == "canonical_dataset_generation_run_manifest.json":
            entries.append({"filename": name, "digest_kind": "CANONICAL_DATASET_GENERATION_DIGEST", "sha256": artifact["canonical_dataset_generation_digest"]})
        elif name == "canonical_dataset_digest_manifest.json":
            entries.append({"filename": name, "digest_kind": "SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE", "sha256": None})
        else:
            entries.append({"filename": name, "digest_kind": "FILE_SHA256", "sha256": sha256_bytes(outputs[name])})
    return entries


def execute_canonical_dataset_generation_v1(
    *, source_root: str | Path | None = None, output_root: str | Path | None = None,
    run_timestamp_utc: str | None = None,
) -> dict[str, Any]:
    """Generate the nine ignored canonical outputs without any provider access."""
    source = Path(source_root) if source_root is not None else DEFAULT_SOURCE_ROOT
    output = Path(output_root) if output_root is not None else DEFAULT_OUTPUT_ROOT
    try:
        results, source_digests = _read_and_verify_source(source)
        records, summaries = _canonical_records(results)
        if len(records) != EXPECTED_TOTAL_CANONICAL_RECORD_COUNT:
            raise CanonicalDatasetGenerationExecutionError("total canonical record count mismatch")
        timestamp = run_timestamp_utc or datetime.now(tz=UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
        artifact = _base_artifact(timestamp, source_digests, summaries)
        artifact["canonical_dataset_generation_digest"] = canonical_dataset_generation_digest_v1(artifact)
        outputs = _build_outputs(artifact, records)
        entries = _digest_entries(artifact, outputs)
        artifact["canonical_output_digest_manifest"] = entries
        outputs["canonical_dataset_generation_run_manifest.json"] = _json_output(artifact)
        digest_manifest = _common_output_fields() | {
            "generated_output_count": EXPECTED_GENERATED_OUTPUT_COUNT,
            "canonical_dataset_generation_digest": artifact["canonical_dataset_generation_digest"],
            "canonical_output_digest_manifest": entries,
        }
        outputs["canonical_dataset_digest_manifest.json"] = _json_output(digest_manifest)
        validate_canonical_dataset_generated_v1(artifact)
    except (CanonicalDatasetGenerationExecutionError, json.JSONDecodeError, OSError, KeyError, TypeError) as exc:
        return _blocked(str(exc))

    if output.exists() and any(output.iterdir()):
        return _blocked("canonical dataset output root is not empty")
    output.mkdir(parents=True, exist_ok=True)
    for name in OUTPUT_FILENAMES:
        (output / name).write_bytes(outputs[name])
    return artifact


def validate_canonical_dataset_generated_v1(artifact: dict[str, Any]) -> dict[str, Any]:
    """Reject generated artifacts that violate counts, evidence, or closed gates."""
    if not isinstance(artifact, dict):
        raise CanonicalDatasetGenerationExecutionError("artifact must be an object")
    expected = {
        "artifact_kind": ARTIFACT_KIND_CANONICAL_DATASET_GENERATED,
        "schema_version": SCHEMA_VERSION_CANONICAL_DATASET_GENERATED_V1,
        "execution_status": CANONICAL_DATASET_GENERATED_RESEARCH_ONLY,
        "output_label": OUTPUT_LABEL,
        "dataset_scope": DATASET_SCOPE,
        "source_evidence_scope": SOURCE_EVIDENCE_SCOPE,
        "target_universe": TARGET_UNIVERSE,
        "target_universe_count": 12,
        "per_ticker_record_counts": EXPECTED_RECORD_COUNTS,
        "total_canonical_record_count": EXPECTED_TOTAL_CANONICAL_RECORD_COUNT,
        "generated_output_count": EXPECTED_GENERATED_OUTPUT_COUNT,
        "canonical_dataset_generation_approval_digest": EXPECTED_CANONICAL_DATASET_GENERATION_APPROVAL_DIGEST,
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": PROFITABILITY_NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
    }
    for field, value in expected.items():
        _expect(artifact.get(field), value, field)
    for field in (
        "created_offline", "dataset_generation_performed", "canonical_dataset_chain_candidate_created",
        "canonical_dataset_chain_candidate_review_created", "canonical_dataset_chain_approved",
        "dataset_generation_authorized", "canonical_dataset_authorized", "canonical_dataset_generation_approved",
        "ready_for_canonical_dataset_generation_execution", "canonical_dataset_candidate_created",
        "canonical_dataset_generation_executed", "canonical_dataset_generated",
        "canonical_dataset_generation_results_created", "research_only",
    ):
        _expect_true(artifact.get(field), field)
    for field in (
        "provider_requests_made_in_generation", "live_provider_transport_enabled_in_generation",
        "market_data_acquisition_performed_in_generation", "raw_provider_payloads_committed",
        "api_keys_stored_or_printed", "canonical_dataset_frozen", "registry_approval_created",
        "additional_predictive_evidence_execution_authorized", "additional_predictive_evidence_executed",
        "predictive_experiment_rerun_authorized", "predictive_experiment_rerun_performed",
        "feature_matrix_regeneration_performed", "new_strategy_scoring_performed",
        "trade_recommendations_generated", "runtime_migration_approved", "runtime_migration_active",
        "automatic_stitching",
    ):
        _expect_false(artifact.get(field), field)
    for field in (
        "canonical_dataset_generation_approval_digest", "canonical_dataset_chain_candidate_review_package_digest",
        "canonical_dataset_chain_candidate_digest", "acquisition_generation_freeze_digest",
        "acquisition_generation_approval_digest", "acquisition_evidence_results_review_package_digest",
        "acquisition_provider_evidence_execution_digest", "corporate_action_authority_approval_digest",
        "identity_authority_freeze_digest", "ticker_universe_selection_approval_digest",
        "canonical_dataset_generation_digest",
    ):
        _expect_digest(artifact.get(field), field)
    _expect(artifact["canonical_dataset_generation_digest"], canonical_dataset_generation_digest_v1(artifact), "canonical_dataset_generation_digest")
    entries = artifact.get("canonical_output_digest_manifest")
    if not isinstance(entries, list):
        raise CanonicalDatasetGenerationExecutionError("canonical_output_digest_manifest missing")
    _expect([row.get("filename") for row in entries], OUTPUT_FILENAMES, "canonical output digest filenames")
    _expect(len(entries), EXPECTED_GENERATED_OUTPUT_COUNT, "canonical output digest count")
    return {
        "status": CANONICAL_DATASET_GENERATED_RESEARCH_ONLY,
        "canonical_dataset_generation_digest": artifact["canonical_dataset_generation_digest"],
        "total_canonical_record_count": artifact["total_canonical_record_count"],
        "generated_output_count": artifact["generated_output_count"],
    }


def build_canonical_dataset_generation_status_markdown_v1(artifact: dict[str, Any]) -> str:
    """Render the generated artifact and its unchanged authority boundaries."""
    validation = validate_canonical_dataset_generated_v1(artifact)
    sections = [
        ("Canonical Dataset Generation Execution", [f"Artifact/status: `{artifact['artifact_kind']}` / `{validation['status']}`.", f"Generation digest: `{validation['canonical_dataset_generation_digest']}`."]),
        ("Source Canonical Dataset Generation Approval", [f"Approval digest: `{artifact['canonical_dataset_generation_approval_digest']}`."]),
        ("Source Acquisition Generation Freeze", [f"Freeze digest: `{artifact['acquisition_generation_freeze_digest']}`."]),
        ("Target Universe", [", ".join(f"`{ticker}`" for ticker in artifact["target_universe"]) + "."]),
        ("Source Profile", [f"`{key}`: `{value}`." for key, value in artifact["canonical_dataset_source_profile"].items()]),
        ("Canonical Dataset Schema", ["Normalized decimal strings; approved ticker order; ascending UTC timestamps; per-record source and canonical digests."]),
        ("Per-Ticker Canonical Record Summary", [f"`{ticker}`: `{count}` records." for ticker, count in artifact["per_ticker_record_counts"].items()]),
        ("META Reduced Bar Count Preservation", ["META remains exactly `913`; no repair, inference, smoothing, or backfill occurred."]),
        ("Output Digest Manifest", [f"`{row['filename']}`: `{row['sha256'] or row['digest_kind']}`." for row in artifact["canonical_output_digest_manifest"]]),
        ("Data Quality Summary", ["Failures: `0`; warnings: `1` (preserved META source limitation)."]),
        ("Dataset Generation Boundary", ["The canonical dataset was generated offline from sanitized saved evidence only."]),
        ("Canonical Dataset Freeze Boundary", ["The canonical dataset is not frozen."]),
        ("Registry Boundary", ["No registry approval was created."]),
        ("Predictive/Profitability Boundary", ["Predictive usefulness and profitability remain not accepted."]),
        ("Runtime Boundary", ["Runtime, strategy, paper trading, and broker execution remain `NOT_AUTHORIZED`."]),
        ("Checklist Summary", ["Generation validation passed all required artifact, count, evidence, and authority-boundary checks."]),
        ("Guardrails", ["No provider request, acquisition, raw payload commit, secret access, experiment rerun, strategy scoring, or runtime activation occurred."]),
    ]
    lines = ["# MarketFlow Canonical Dataset Generation Execution v1", ""]
    for title, body in sections:
        lines.extend([f"## {title}", "", *[f"- {item}" for item in body], ""])
    return "\n".join(lines)
