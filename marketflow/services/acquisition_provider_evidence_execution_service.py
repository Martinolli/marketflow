"""Gated read-only acquisition provider evidence execution for the expanded universe."""

from __future__ import annotations

from copy import deepcopy
from datetime import UTC, datetime
import os
from pathlib import Path
from typing import Any, Callable, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import acquisition_provider_evidence_adapter_service as provider_adapter
from marketflow.services import acquisition_provider_evidence_request_approval_service as approval


ARTIFACT_KIND_ACQUISITION_PROVIDER_EVIDENCE_EXECUTED = "ACQUISITION_PROVIDER_EVIDENCE_EXECUTED"
ARTIFACT_KIND_ACQUISITION_PROVIDER_EVIDENCE_BLOCKED = "ACQUISITION_PROVIDER_EVIDENCE_BLOCKED"
SCHEMA_VERSION_ACQUISITION_PROVIDER_EVIDENCE_EXECUTED_V1 = "acquisition_provider_evidence_executed_v1"
ACQUISITION_PROVIDER_EVIDENCE_EXECUTED_READ_ONLY = "ACQUISITION_PROVIDER_EVIDENCE_EXECUTED_READ_ONLY"
ACQUISITION_PROVIDER_EVIDENCE_BLOCKED_LIVE_GATE_OR_API_KEY_MISSING = (
    "ACQUISITION_PROVIDER_EVIDENCE_BLOCKED_LIVE_GATE_OR_API_KEY_MISSING"
)
ACQUISITION_PROVIDER_EVIDENCE_BLOCKED_ENDPOINT_NOT_SELECTED = (
    "ACQUISITION_PROVIDER_EVIDENCE_BLOCKED_ENDPOINT_NOT_SELECTED"
)
MARKETFLOW_ENABLE_LIVE_ACQUISITION_PROVIDER_EVIDENCE = (
    provider_adapter.MARKETFLOW_ENABLE_LIVE_ACQUISITION_PROVIDER_EVIDENCE
)

READ_ONLY_HISTORICAL_MARKET_DATA_ACQUISITION_REQUESTS_ONLY = (
    approval.ACQUISITION_PROVIDER_EVIDENCE_REQUEST_SCOPE
)
RESEARCH_ONLY_NON_ACTIONABLE = approval.RESEARCH_ONLY_NON_ACTIONABLE
NOT_AUTHORIZED = approval.NOT_AUTHORIZED
NOT_ACCEPTED = approval.NOT_ACCEPTED
PROFITABILITY_NOT_ACCEPTED = approval.PROFITABILITY_NOT_ACCEPTED
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"
NOT_EVALUATED_BY_SELECTED_ENDPOINT = "NOT_EVALUATED_BY_SELECTED_ENDPOINT"

ACQUISITION_EVIDENCE_COLLECTED_READ_ONLY = "ACQUISITION_EVIDENCE_COLLECTED_READ_ONLY"
NO_HISTORICAL_BARS_RETURNED_BY_PROVIDER = "NO_HISTORICAL_BARS_RETURNED_BY_PROVIDER"
ACQUISITION_PROVIDER_RESPONSE_UNAVAILABLE = "ACQUISITION_PROVIDER_RESPONSE_UNAVAILABLE"
ACQUISITION_NOT_EVALUATED_BY_SELECTED_ENDPOINT = "ACQUISITION_NOT_EVALUATED_BY_SELECTED_ENDPOINT"

OUTPUT_ROOT = Path(".marketflow") / "acquisition_provider_evidence" / "expanded_universe_v1"
OUTPUT_FILENAMES = [
    "acquisition_provider_evidence_run_manifest.json",
    "acquisition_provider_request_receipts_sanitized.json",
    "acquisition_evidence_results_sanitized.json",
    "acquisition_data_quality_summary.json",
    "acquisition_failure_reason_inventory.json",
    "acquisition_digest_manifest.json",
    "operator_review_summary.json",
]
TARGET_UNIVERSE = list(approval.TARGET_UNIVERSE)
DATE_RANGE_START = "2022-01-01"
DATE_RANGE_END = "2025-12-31"
TIMEFRAME = "1d"
SESSION_PROFILE = "RTH_FULL_SESSION_1D"

EXPECTED_ACQUISITION_PROVIDER_EVIDENCE_REQUEST_APPROVAL_DIGEST = (
    "a83acdf0c64fa8d430274350c59b547a23e7a58fb897cc33982ab0444ec0993c"
)
EXPECTED_ACQUISITION_GENERATION_CHAIN_REVIEW_DIGEST = (
    "4df1f99cc3902219a658cb2459353e73b3be12cba22365cfec35c2170a75af3d"
)
EXPECTED_ACQUISITION_GENERATION_CHAIN_CANDIDATE_DIGEST = (
    "e0fb0b3f2ccd4bdac3d8f24a6888e8a97d5013bcc33f1dee1d49ccd59204b4ff"
)
EXPECTED_CORPORATE_ACTION_AUTHORITY_APPROVAL_DIGEST = (
    "93524b9bdc4641de4c6eb1cc8343b848ceff316241c92edab57a2062b8640644"
)
EXPECTED_COMBINED_READINESS_REVIEW_DIGEST = (
    "ee425cb1ee8b9e513d3ed4bc5ddc05ca7498a3003bc5820c5a2b5014f799d621"
)
EXPECTED_SPLIT_EVENT_AUTHORITY_FREEZE_DIGEST = (
    "37a06dceac17761319f9d5eb716d64dced765997b8d1e9d8a79166162bfdb303"
)
EXPECTED_DIVIDEND_EVENT_AUTHORITY_FREEZE_DIGEST = (
    "98b7e740b750701eb1e63e6e0ad88ffd4d665c44ece2e0e85e0a15e4a2a4d6ae"
)
EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST = (
    "55e33f7a0e7db13d289c76c53bead4edd319143d26d3082fbc7b24b61d60eb30"
)
EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST = (
    "e0b56da411ada20f40fbefdcf74c1cce75ca86d13931471f518ef970db23188c"
)


class AcquisitionProviderEvidenceExecutionError(ValueError):
    """Raised when an executed artifact violates the approved boundary."""


def _utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _api_key_from_environment() -> str | None:
    return os.environ.get("MASSIVE_API_KEY") or os.environ.get("POLYGON_API_KEY")


def _base_output_fields() -> dict[str, Any]:
    return {
        "output_label": RESEARCH_ONLY_NON_ACTIONABLE,
        "evidence_scope": READ_ONLY_HISTORICAL_MARKET_DATA_ACQUISITION_REQUESTS_ONLY,
        "new_ticker_acquisition_authorized": False,
        "acquisition_generation_authorized": False,
        "acquisition_generation_executed": False,
        "dataset_generation_authorized": False,
        "canonical_dataset_authorized": False,
        "canonical_dataset_frozen": False,
        "registry_approval_created": False,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": PROFITABILITY_NOT_ACCEPTED,
    }


def acquisition_provider_evidence_execution_digest_v1(artifact: dict[str, Any]) -> str:
    """Return an output-root-independent deterministic execution digest."""
    clone = deepcopy(artifact)
    clone.pop("acquisition_provider_evidence_execution_digest", None)
    for item in clone.get("output_digest_manifest", []):
        if isinstance(item, dict):
            item["relative_path"] = item.get("filename")
    return semantic_digest(clone)


def _bar_date(timestamp: str | None) -> str | None:
    if timestamp is None:
        return None
    try:
        return datetime.fromtimestamp(int(timestamp) / 1000, tz=UTC).date().isoformat()
    except (ValueError, OverflowError):
        return None


def _ticker_result_from_provider(ticker: str, response: Mapping[str, Any]) -> dict[str, Any]:
    bars = response.get("sanitized_rows")
    if not isinstance(bars, list):
        raise AcquisitionProviderEvidenceExecutionError("adapter sanitized_rows mismatch")
    dates = [date for date in (_bar_date(bar.get("timestamp")) for bar in bars) if date is not None]
    ohlc_complete = bool(bars) and all(
        all(bar.get(field) is not None for field in ("open", "high", "low", "close")) for bar in bars
    )
    volume_complete = bool(bars) and all(bar.get("volume") is not None for bar in bars)
    timestamp_complete = bool(bars) and len(dates) == len(bars)
    not_evaluated = [
        "trading_calendar_alignment_status",
        "session_filter_status",
        "split_adjustment_policy_binding",
        "dividend_adjustment_policy_binding",
    ]
    status = ACQUISITION_EVIDENCE_COLLECTED_READ_ONLY if bars else NO_HISTORICAL_BARS_RETURNED_BY_PROVIDER
    coverage = "OBSERVED_BAR_RANGE_RECORDED" if dates else "NO_HISTORICAL_BARS_RETURNED_BY_PROVIDER"
    result = {
        "ticker": ticker,
        "provider_request_status": "REQUEST_PERFORMED_READ_ONLY",
        "acquisition_provider_evidence_status": status,
        "historical_bar_count": len(bars),
        "date_range_start": min(dates) if dates else None,
        "date_range_end": max(dates) if dates else None,
        "coverage_status": coverage,
        "ohlc_status": "AVAILABLE" if ohlc_complete else ("MISSING_OR_INCOMPLETE" if bars else "NOT_AVAILABLE"),
        "volume_status": "AVAILABLE" if volume_complete else ("MISSING_OR_INCOMPLETE" if bars else "NOT_AVAILABLE"),
        "timestamp_status": "AVAILABLE" if timestamp_complete else ("MISSING_OR_INCOMPLETE" if bars else "NOT_AVAILABLE"),
        "calendar_alignment_status": NOT_EVALUATED_BY_SELECTED_ENDPOINT,
        "session_filter_status": NOT_EVALUATED_BY_SELECTED_ENDPOINT,
        "adjustment_policy_status": "PROVIDER_ADJUSTED_TRUE_COMBINED_POLICY_NOT_DISAGGREGATED",
        "not_evaluated_fields": not_evaluated,
        "provider_request_metadata": deepcopy(response.get("provider_request_metadata")),
        "provider_response_digest": response.get("provider_response_digest"),
        "sanitized_bars": deepcopy(bars),
        "raw_response_stored": False,
        "raw_payload_committed": False,
        "api_key_stored_or_printed": False,
        "new_ticker_acquisition_authorized": False,
        "acquisition_generation_authorized": False,
        "acquisition_generation_executed": False,
        "dataset_generation_authorized": False,
        "canonical_dataset_authorized": False,
        "canonical_dataset_candidate_created": False,
        "canonical_dataset_frozen": False,
        "registry_approval_created": False,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "failure_reason_if_any": None,
    }
    result["sanitized_acquisition_evidence_digest"] = semantic_digest(
        {key: value for key, value in result.items() if key != "sanitized_acquisition_evidence_digest"}
    )
    return result


def _unavailable_ticker_result(ticker: str, reason: str) -> dict[str, Any]:
    result = {
        "ticker": ticker,
        "provider_request_status": "REQUEST_FAILED_READ_ONLY",
        "acquisition_provider_evidence_status": ACQUISITION_PROVIDER_RESPONSE_UNAVAILABLE,
        "historical_bar_count": 0,
        "date_range_start": None,
        "date_range_end": None,
        "coverage_status": "PROVIDER_RESPONSE_UNAVAILABLE",
        "ohlc_status": "NOT_AVAILABLE",
        "volume_status": "NOT_AVAILABLE",
        "timestamp_status": "NOT_AVAILABLE",
        "calendar_alignment_status": NOT_EVALUATED_BY_SELECTED_ENDPOINT,
        "session_filter_status": NOT_EVALUATED_BY_SELECTED_ENDPOINT,
        "adjustment_policy_status": NOT_EVALUATED_BY_SELECTED_ENDPOINT,
        "not_evaluated_fields": [
            "historical_price_bar_availability",
            "historical_volume_availability",
            "date_range_coverage",
            "trading_calendar_alignment_status",
            "session_filter_status",
            "adjusted_unadjusted_price_policy_binding",
            "split_adjustment_policy_binding",
            "dividend_adjustment_policy_binding",
        ],
        "provider_request_metadata": None,
        "provider_response_digest": None,
        "sanitized_bars": [],
        "raw_response_stored": False,
        "raw_payload_committed": False,
        "api_key_stored_or_printed": False,
        "new_ticker_acquisition_authorized": False,
        "acquisition_generation_authorized": False,
        "acquisition_generation_executed": False,
        "dataset_generation_authorized": False,
        "canonical_dataset_authorized": False,
        "canonical_dataset_candidate_created": False,
        "canonical_dataset_frozen": False,
        "registry_approval_created": False,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "failure_reason_if_any": reason,
    }
    result["sanitized_acquisition_evidence_digest"] = semantic_digest(
        {key: value for key, value in result.items() if key != "sanitized_acquisition_evidence_digest"}
    )
    return result


def _summary(results: list[dict[str, Any]], generated_output_count: int) -> dict[str, Any]:
    successful = [item for item in results if item["provider_request_status"] == "REQUEST_PERFORMED_READ_ONLY"]
    failed = [item for item in results if item["provider_request_status"] != "REQUEST_PERFORMED_READ_ONLY"]
    collected = [
        item for item in results
        if item["acquisition_provider_evidence_status"] == ACQUISITION_EVIDENCE_COLLECTED_READ_ONLY
    ]
    absent = [
        item for item in results
        if item["acquisition_provider_evidence_status"] == NO_HISTORICAL_BARS_RETURNED_BY_PROVIDER
    ]
    return {
        "target_count": len(TARGET_UNIVERSE),
        "date_range_start": DATE_RANGE_START,
        "date_range_end": DATE_RANGE_END,
        "timeframe": TIMEFRAME,
        "provider_request_count": len(results),
        "successful_provider_response_count": len(successful),
        "failed_provider_response_count": len(failed),
        "historical_bar_evidence_collected_count": len(collected),
        "no_historical_bars_returned_count": len(absent),
        "not_evaluated_count": sum(1 for item in results if item["not_evaluated_fields"]),
        "generated_output_count": generated_output_count,
        "failure_count": len(failed),
        "warning_count": sum(1 for item in results if item["not_evaluated_fields"]),
    }


def _artifact_seed(timestamp: str, transport_mode: str, results: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_ACQUISITION_PROVIDER_EVIDENCE_EXECUTED,
        "schema_version": SCHEMA_VERSION_ACQUISITION_PROVIDER_EVIDENCE_EXECUTED_V1,
        "execution_status": ACQUISITION_PROVIDER_EVIDENCE_EXECUTED_READ_ONLY,
        "evidence_scope": READ_ONLY_HISTORICAL_MARKET_DATA_ACQUISITION_REQUESTS_ONLY,
        "output_label": RESEARCH_ONLY_NON_ACTIONABLE,
        "created_offline": False,
        "run_timestamp_utc": timestamp,
        "selected_provider": provider_adapter.PROVIDER_NAME,
        "selected_endpoint": provider_adapter.MASSIVE_DAILY_BARS_ENDPOINT,
        "selected_endpoint_mode": provider_adapter.MASSIVE_DAILY_BARS_ENDPOINT_STABILITY,
        "transport_mode": transport_mode,
        "date_range_start": DATE_RANGE_START,
        "date_range_end": DATE_RANGE_END,
        "timeframe": TIMEFRAME,
        "session_profile": SESSION_PROFILE,
        "acquisition_provider_request_authorized": True,
        "ready_for_acquisition_provider_evidence_execution": True,
        "provider_requests_made": True,
        "live_provider_transport_enabled": True,
        "market_data_acquisition_performed": True,
        "acquisition_provider_evidence_executed": True,
        "acquisition_provider_evidence_results_created": True,
        "provider_requests_made_in_execution": True,
        "raw_provider_payloads_committed": False,
        "api_keys_stored_or_printed": False,
        "acquisition_generation_chain_candidate_created": True,
        "acquisition_generation_chain_candidate_review_created": True,
        "new_ticker_acquisition_authorized": False,
        "acquisition_generation_authorized": False,
        "acquisition_generation_executed": False,
        "acquisition_generation_results_created": False,
        "acquisition_generation_frozen": False,
        "dataset_generation_authorized": False,
        "canonical_dataset_authorized": False,
        "canonical_dataset_candidate_created": False,
        "canonical_dataset_frozen": False,
        "registry_approval_created": False,
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
        "acquisition_provider_evidence_request_approval_digest": EXPECTED_ACQUISITION_PROVIDER_EVIDENCE_REQUEST_APPROVAL_DIGEST,
        "acquisition_generation_chain_candidate_review_package_digest": EXPECTED_ACQUISITION_GENERATION_CHAIN_REVIEW_DIGEST,
        "acquisition_generation_chain_candidate_digest": EXPECTED_ACQUISITION_GENERATION_CHAIN_CANDIDATE_DIGEST,
        "corporate_action_authority_approval_digest": EXPECTED_CORPORATE_ACTION_AUTHORITY_APPROVAL_DIGEST,
        "combined_split_dividend_corporate_action_readiness_review_package_digest": EXPECTED_COMBINED_READINESS_REVIEW_DIGEST,
        "split_event_authority_freeze_digest": EXPECTED_SPLIT_EVENT_AUTHORITY_FREEZE_DIGEST,
        "dividend_event_authority_freeze_digest": EXPECTED_DIVIDEND_EVENT_AUTHORITY_FREEZE_DIGEST,
        "identity_authority_freeze_digest": EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST,
        "ticker_universe_selection_approval_digest": EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST,
        "target_universe": list(TARGET_UNIVERSE),
        "target_universe_count": len(TARGET_UNIVERSE),
        "per_ticker_acquisition_provider_evidence_results": results,
        "generated_output_count": len(OUTPUT_FILENAMES),
        "execution_summary": _summary(results, len(OUTPUT_FILENAMES)),
        "output_digest_manifest": [],
        "next_required_task": "ACQUISITION_EVIDENCE_RESULTS_REVIEW_PACKAGE_V1",
    }


def _output_payloads(artifact: dict[str, Any]) -> dict[str, dict[str, Any]]:
    base = _base_output_fields()
    results = artifact["per_ticker_acquisition_provider_evidence_results"]
    summary = artifact["execution_summary"]
    receipts = [
        {
            "ticker": item["ticker"],
            "provider_request_status": item["provider_request_status"],
            "provider_request_metadata": item["provider_request_metadata"],
            "provider_response_digest": item["provider_response_digest"],
            "raw_response_stored": False,
            "raw_payload_committed": False,
            "api_key_stored_or_printed": False,
        }
        for item in results
    ]
    quality = [
        {
            "ticker": item["ticker"],
            "historical_bar_count": item["historical_bar_count"],
            "coverage_status": item["coverage_status"],
            "ohlc_status": item["ohlc_status"],
            "volume_status": item["volume_status"],
            "timestamp_status": item["timestamp_status"],
            "not_evaluated_fields": item["not_evaluated_fields"],
        }
        for item in results
    ]
    failures = [
        {"ticker": item["ticker"], "failure_reason_if_any": item["failure_reason_if_any"]}
        for item in results if item["failure_reason_if_any"]
    ]
    return {
        OUTPUT_FILENAMES[0]: base | {
            "artifact_kind": artifact["artifact_kind"],
            "execution_status": artifact["execution_status"],
            "run_timestamp_utc": artifact["run_timestamp_utc"],
            "selected_endpoint": artifact["selected_endpoint"],
            "acquisition_profile": {
                "date_range_start": DATE_RANGE_START,
                "date_range_end": DATE_RANGE_END,
                "timeframe": TIMEFRAME,
                "session_profile": SESSION_PROFILE,
            },
            "target_universe": list(TARGET_UNIVERSE),
            "execution_summary": deepcopy(summary),
        },
        OUTPUT_FILENAMES[1]: base | {"request_receipts_sanitized": receipts},
        OUTPUT_FILENAMES[2]: base | {"per_ticker_acquisition_evidence_results": deepcopy(results)},
        OUTPUT_FILENAMES[3]: base | {"acquisition_data_quality_summary": quality},
        OUTPUT_FILENAMES[4]: base | {"acquisition_failure_reason_inventory": failures},
        OUTPUT_FILENAMES[6]: base | {
            "operator_review_required": True,
            "next_task": "ACQUISITION_EVIDENCE_RESULTS_REVIEW_PACKAGE_V1",
            "execution_summary": deepcopy(summary),
            "provider_evidence_is_dataset_authority": False,
        },
    }


def _write_outputs(output_root: Path, payloads: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    output_root.mkdir(parents=True, exist_ok=True)
    entries: dict[str, dict[str, Any]] = {}
    for filename in OUTPUT_FILENAMES:
        if filename == "acquisition_digest_manifest.json":
            continue
        data = canonical_json_bytes(payloads[filename])
        (output_root / filename).write_bytes(data)
        entries[filename] = {
            "filename": filename,
            "relative_path": str((output_root / filename).as_posix()),
            "sha256": sha256_bytes(data),
            "semantic_digest": semantic_digest(payloads[filename]),
            "output_label": RESEARCH_ONLY_NON_ACTIONABLE,
        }
    digest_entries = [deepcopy(entries[name]) for name in OUTPUT_FILENAMES if name in entries]
    for entry in digest_entries:
        entry["relative_path"] = entry["filename"]
    digest_payload = _base_output_fields() | {"output_digests": digest_entries}
    digest_filename = "acquisition_digest_manifest.json"
    digest_data = canonical_json_bytes(digest_payload)
    (output_root / digest_filename).write_bytes(digest_data)
    entries[digest_filename] = {
        "filename": digest_filename,
        "relative_path": str((output_root / digest_filename).as_posix()),
        "sha256": sha256_bytes(digest_data),
        "semantic_digest": semantic_digest(digest_payload),
        "output_label": RESEARCH_ONLY_NON_ACTIONABLE,
    }
    return [entries[filename] for filename in OUTPUT_FILENAMES]


def _blocked_artifact(timestamp: str, reason: str, status: str) -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_ACQUISITION_PROVIDER_EVIDENCE_BLOCKED,
        "schema_version": SCHEMA_VERSION_ACQUISITION_PROVIDER_EVIDENCE_EXECUTED_V1,
        "execution_status": status,
        "evidence_scope": READ_ONLY_HISTORICAL_MARKET_DATA_ACQUISITION_REQUESTS_ONLY,
        "output_label": RESEARCH_ONLY_NON_ACTIONABLE,
        "run_timestamp_utc": timestamp,
        "blocked_reason": reason,
        "required_live_gate": MARKETFLOW_ENABLE_LIVE_ACQUISITION_PROVIDER_EVIDENCE,
        "accepted_api_key_sources": ["explicit api_key argument", "MASSIVE_API_KEY", "POLYGON_API_KEY"],
        "selected_provider": provider_adapter.PROVIDER_NAME,
        "selected_endpoint": provider_adapter.MASSIVE_DAILY_BARS_ENDPOINT,
        "selected_endpoint_mode": "BLOCKED_NO_TRANSPORT",
        "date_range_start": DATE_RANGE_START,
        "date_range_end": DATE_RANGE_END,
        "timeframe": TIMEFRAME,
        "session_profile": SESSION_PROFILE,
        "acquisition_provider_request_authorized": True,
        "ready_for_acquisition_provider_evidence_execution": True,
        "provider_requests_made": False,
        "live_provider_transport_enabled": False,
        "market_data_acquisition_performed": False,
        "acquisition_provider_evidence_executed": False,
        "acquisition_provider_evidence_results_created": False,
        "raw_provider_payloads_committed": False,
        "api_keys_stored_or_printed": False,
        "new_ticker_acquisition_authorized": False,
        "acquisition_generation_authorized": False,
        "acquisition_generation_executed": False,
        "dataset_generation_authorized": False,
        "canonical_dataset_authorized": False,
        "canonical_dataset_candidate_created": False,
        "canonical_dataset_frozen": False,
        "registry_approval_created": False,
        "additional_predictive_evidence_execution_authorized": False,
        "additional_predictive_evidence_executed": False,
        "predictive_experiment_rerun_performed": False,
        "feature_matrix_regeneration_performed": False,
        "new_strategy_scoring_performed": False,
        "trade_recommendations_generated": False,
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": PROFITABILITY_NOT_ACCEPTED,
        "runtime_migration_approved": False,
        "runtime_migration_active": False,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "automatic_stitching": False,
        "acquisition_provider_evidence_request_approval_digest": EXPECTED_ACQUISITION_PROVIDER_EVIDENCE_REQUEST_APPROVAL_DIGEST,
        "target_universe": list(TARGET_UNIVERSE),
        "target_universe_count": len(TARGET_UNIVERSE),
        "per_ticker_acquisition_provider_evidence_results": [],
        "generated_output_count": 0,
        "output_digest_manifest": [],
        "acquisition_provider_evidence_execution_digest": "NOT_CREATED",
        "execution_summary": _summary([], 0) | {"target_count": len(TARGET_UNIVERSE), "failure_count": 1},
        "next_required_task": "ENVIRONMENT_OR_API_KEY_CORRECTION" if "ENDPOINT" not in reason else "ENDPOINT_SELECTION",
    }


def execute_acquisition_provider_evidence_v1(
    *,
    api_key: str | None = None,
    transport: Callable[[Mapping[str, Any]], Any] | None = None,
    output_root: str | Path | None = None,
    run_timestamp_utc: str | None = None,
) -> dict[str, Any]:
    """Execute approved evidence requests, or return a fail-closed blocked artifact."""
    timestamp = run_timestamp_utc or _utc_now()
    if not provider_adapter.MASSIVE_DAILY_BARS_ENDPOINT:
        return _blocked_artifact(
            timestamp,
            "ENDPOINT_NOT_SELECTED",
            ACQUISITION_PROVIDER_EVIDENCE_BLOCKED_ENDPOINT_NOT_SELECTED,
        )
    if transport is None and os.environ.get(MARKETFLOW_ENABLE_LIVE_ACQUISITION_PROVIDER_EVIDENCE) != "1":
        return _blocked_artifact(
            timestamp,
            "LIVE_GATE_MISSING",
            ACQUISITION_PROVIDER_EVIDENCE_BLOCKED_LIVE_GATE_OR_API_KEY_MISSING,
        )
    resolved_api_key = api_key or _api_key_from_environment()
    if resolved_api_key is None:
        return _blocked_artifact(
            timestamp,
            "API_KEY_MISSING",
            ACQUISITION_PROVIDER_EVIDENCE_BLOCKED_LIVE_GATE_OR_API_KEY_MISSING,
        )
    results: list[dict[str, Any]] = []
    for ticker in TARGET_UNIVERSE:
        try:
            response = provider_adapter.fetch_massive_daily_bars_evidence_v1(
                ticker=ticker,
                start_date=DATE_RANGE_START,
                end_date=DATE_RANGE_END,
                api_key=resolved_api_key,
                transport=transport,
                request_timestamp_utc=timestamp,
            )
        except provider_adapter.AcquisitionProviderEvidenceAdapterError as exc:
            results.append(_unavailable_ticker_result(ticker, str(exc)))
        else:
            results.append(_ticker_result_from_provider(ticker, response))
    artifact = _artifact_seed(
        timestamp,
        "INJECTED_TRANSPORT_READ_ONLY" if transport is not None else "LIVE_HTTP_TRANSPORT_READ_ONLY",
        results,
    )
    root = Path(output_root) if output_root is not None else OUTPUT_ROOT
    artifact["output_digest_manifest"] = _write_outputs(root, _output_payloads(artifact))
    artifact["acquisition_provider_evidence_execution_digest"] = (
        acquisition_provider_evidence_execution_digest_v1(artifact)
    )
    validate_acquisition_provider_evidence_executed_v1(artifact)
    return artifact


def _expect(actual: Any, expected: Any, field_name: str) -> None:
    if actual != expected:
        raise AcquisitionProviderEvidenceExecutionError(f"{field_name} mismatch")


def _expect_digest(actual: Any, field_name: str) -> None:
    if not isinstance(actual, str) or len(actual) != 64:
        raise AcquisitionProviderEvidenceExecutionError(f"{field_name} missing")


def _check(check_id: str, expected: Any, actual: Any) -> dict[str, Any]:
    return {
        "check_id": check_id,
        "status": PASS if actual == expected else FAIL,
        "expected": expected,
        "actual": actual,
        "severity": BLOCKER,
    }


def _execution_checklist(artifact: dict[str, Any]) -> list[dict[str, Any]]:
    expected = {
        "artifact_kind": ARTIFACT_KIND_ACQUISITION_PROVIDER_EVIDENCE_EXECUTED,
        "execution_status": ACQUISITION_PROVIDER_EVIDENCE_EXECUTED_READ_ONLY,
        "acquisition_provider_request_authorized": True,
        "ready_for_acquisition_provider_evidence_execution": True,
        "provider_requests_made": True,
        "live_provider_transport_enabled": True,
        "market_data_acquisition_performed": True,
        "acquisition_provider_evidence_executed": True,
        "acquisition_provider_evidence_results_created": True,
        "raw_provider_payloads_committed": False,
        "api_keys_stored_or_printed": False,
        "target_universe_count": 12,
        "target_universe": TARGET_UNIVERSE,
        "generated_output_count": 7,
        "new_ticker_acquisition_authorized": False,
        "acquisition_generation_authorized": False,
        "acquisition_generation_executed": False,
        "dataset_generation_authorized": False,
        "canonical_dataset_authorized": False,
        "canonical_dataset_candidate_created": False,
        "canonical_dataset_frozen": False,
        "registry_approval_created": False,
        "additional_predictive_evidence_execution_authorized": False,
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": PROFITABILITY_NOT_ACCEPTED,
        "runtime_migration_approved": False,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "automatic_stitching": False,
        "acquisition_provider_evidence_request_approval_digest": EXPECTED_ACQUISITION_PROVIDER_EVIDENCE_REQUEST_APPROVAL_DIGEST,
    }
    return [_check(field, value, artifact.get(field)) for field, value in expected.items()]


def validate_acquisition_provider_evidence_executed_v1(artifact: dict[str, Any]) -> dict[str, Any]:
    """Validate the executed artifact and all downstream closed gates."""
    checklist = _execution_checklist(artifact)
    failed = [item for item in checklist if item["status"] != PASS]
    if failed:
        raise AcquisitionProviderEvidenceExecutionError(f"execution checklist failed: {failed[0]['check_id']}")
    for field, expected in {
        "schema_version": SCHEMA_VERSION_ACQUISITION_PROVIDER_EVIDENCE_EXECUTED_V1,
        "evidence_scope": READ_ONLY_HISTORICAL_MARKET_DATA_ACQUISITION_REQUESTS_ONLY,
        "output_label": RESEARCH_ONLY_NON_ACTIONABLE,
        "date_range_start": DATE_RANGE_START,
        "date_range_end": DATE_RANGE_END,
        "timeframe": TIMEFRAME,
        "acquisition_generation_chain_candidate_review_package_digest": EXPECTED_ACQUISITION_GENERATION_CHAIN_REVIEW_DIGEST,
        "acquisition_generation_chain_candidate_digest": EXPECTED_ACQUISITION_GENERATION_CHAIN_CANDIDATE_DIGEST,
        "corporate_action_authority_approval_digest": EXPECTED_CORPORATE_ACTION_AUTHORITY_APPROVAL_DIGEST,
        "combined_split_dividend_corporate_action_readiness_review_package_digest": EXPECTED_COMBINED_READINESS_REVIEW_DIGEST,
        "split_event_authority_freeze_digest": EXPECTED_SPLIT_EVENT_AUTHORITY_FREEZE_DIGEST,
        "dividend_event_authority_freeze_digest": EXPECTED_DIVIDEND_EVENT_AUTHORITY_FREEZE_DIGEST,
        "identity_authority_freeze_digest": EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST,
        "ticker_universe_selection_approval_digest": EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST,
    }.items():
        _expect(artifact.get(field), expected, field)
    entries = artifact.get("per_ticker_acquisition_provider_evidence_results")
    if not isinstance(entries, list) or len(entries) != len(TARGET_UNIVERSE):
        raise AcquisitionProviderEvidenceExecutionError("per-ticker acquisition evidence results mismatch")
    _expect([item.get("ticker") for item in entries], TARGET_UNIVERSE, "per-ticker tickers")
    allowed = {
        ACQUISITION_EVIDENCE_COLLECTED_READ_ONLY,
        NO_HISTORICAL_BARS_RETURNED_BY_PROVIDER,
        ACQUISITION_PROVIDER_RESPONSE_UNAVAILABLE,
        ACQUISITION_NOT_EVALUATED_BY_SELECTED_ENDPOINT,
    }
    for item in entries:
        if item.get("acquisition_provider_evidence_status") not in allowed:
            raise AcquisitionProviderEvidenceExecutionError("acquisition provider evidence status mismatch")
        for field in ("raw_response_stored", "raw_payload_committed", "api_key_stored_or_printed"):
            _expect(item.get(field), False, field)
        for field in (
            "new_ticker_acquisition_authorized",
            "acquisition_generation_authorized",
            "acquisition_generation_executed",
            "dataset_generation_authorized",
            "canonical_dataset_authorized",
            "canonical_dataset_candidate_created",
            "canonical_dataset_frozen",
            "registry_approval_created",
        ):
            _expect(item.get(field), False, field)
        for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
            _expect(item.get(field), NOT_AUTHORIZED, field)
        _expect_digest(item.get("sanitized_acquisition_evidence_digest"), "sanitized_acquisition_evidence_digest")
        if item.get("provider_response_digest") is not None:
            _expect_digest(item.get("provider_response_digest"), "provider_response_digest")
    manifest = artifact.get("output_digest_manifest")
    if not isinstance(manifest, list) or len(manifest) != len(OUTPUT_FILENAMES):
        raise AcquisitionProviderEvidenceExecutionError("output_digest_manifest mismatch")
    _expect([item.get("filename") for item in manifest], OUTPUT_FILENAMES, "output filenames")
    for item in manifest:
        _expect(item.get("output_label"), RESEARCH_ONLY_NON_ACTIONABLE, "output label")
        _expect_digest(item.get("sha256"), "output sha256")
        _expect_digest(item.get("semantic_digest"), "output semantic_digest")
    digest = artifact.get("acquisition_provider_evidence_execution_digest")
    _expect_digest(digest, "acquisition_provider_evidence_execution_digest")
    _expect(digest, acquisition_provider_evidence_execution_digest_v1(artifact), "execution digest")
    return {
        "status": "ACQUISITION_PROVIDER_EVIDENCE_EXECUTED_VALID",
        "artifact_kind": artifact["artifact_kind"],
        "execution_status": artifact["execution_status"],
        "acquisition_provider_evidence_execution_digest": digest,
        "provider_request_count": artifact["execution_summary"]["provider_request_count"],
        "successful_provider_response_count": artifact["execution_summary"]["successful_provider_response_count"],
        "failed_provider_response_count": artifact["execution_summary"]["failed_provider_response_count"],
        "generated_output_count": artifact["generated_output_count"],
        "total_checks": len(checklist),
        "passed_checks": len(checklist),
        "failed_checks": 0,
        "blocker_count": 0,
    }


def build_acquisition_provider_evidence_execution_status_markdown_v1(artifact: dict[str, Any]) -> str:
    """Render a sanitized execution or blocked status document."""
    blocked = artifact.get("artifact_kind") == ARTIFACT_KIND_ACQUISITION_PROVIDER_EVIDENCE_BLOCKED
    validation = None if blocked else validate_acquisition_provider_evidence_executed_v1(artifact)
    summary = artifact["execution_summary"]
    results = artifact.get("per_ticker_acquisition_provider_evidence_results", [])
    lines = [
        "# MarketFlow Acquisition Provider Evidence Execution Status",
        "",
        "## Title",
        "- Acquisition Provider Evidence Execution v1.",
        "",
        "## Acquisition Provider Evidence Execution",
        f"- Artifact kind: `{artifact['artifact_kind']}`",
        f"- Execution status: `{artifact['execution_status']}`",
        f"- Execution digest: `{artifact.get('acquisition_provider_evidence_execution_digest', 'NOT_CREATED')}`",
        f"- Evidence scope: `{artifact['evidence_scope']}`",
        "",
        "## Source Acquisition Provider Evidence Request Approval",
        f"- Approval digest: `{artifact['acquisition_provider_evidence_request_approval_digest']}`",
        "",
        "## Source Corporate-Action Authority Approval",
        f"- Approval digest: `{artifact.get('corporate_action_authority_approval_digest', EXPECTED_CORPORATE_ACTION_AUTHORITY_APPROVAL_DIGEST)}`",
        "",
        "## Target Universe",
        "- " + ", ".join(f"`{ticker}`" for ticker in artifact["target_universe"]),
        "",
        "## Acquisition Profile",
        f"- Date range: `{DATE_RANGE_START}` through `{DATE_RANGE_END}`.",
        f"- Timeframe/session: `{TIMEFRAME}` / `{SESSION_PROFILE}`.",
        "- Fields: sanitized OHLCV and provider-supported aggregate metadata.",
        "",
        "## Provider Request Summary",
        f"- Selected provider/endpoint: `{artifact.get('selected_provider')}` / `{artifact.get('selected_endpoint')}`.",
        f"- Selected endpoint mode: `{artifact.get('selected_endpoint_mode')}`.",
        f"- Provider requests/successes/failures: `{summary['provider_request_count']} / {summary['successful_provider_response_count']} / {summary['failed_provider_response_count']}`.",
        f"- Generated output root/count: `{OUTPUT_ROOT.as_posix()}` / `{artifact['generated_output_count']}`.",
        "",
        "## Per-Ticker Acquisition Evidence Summary",
    ]
    if results:
        lines.extend(
            f"- `{item['ticker']}`: `{item['acquisition_provider_evidence_status']}`, bars `{item['historical_bar_count']}`, digest `{item['provider_response_digest']}`."
            for item in results
        )
    else:
        lines.append("- No provider requests were made; no per-ticker acquisition evidence exists.")
    lines.extend(["", "## Output Digest Manifest"])
    if artifact.get("output_digest_manifest"):
        lines.extend(f"- `{item['filename']}`: `{item['sha256']}`." for item in artifact["output_digest_manifest"])
    else:
        lines.append("- No generated outputs were created because execution was blocked.")
    lines.extend(
        [
            "",
            "## Data Quality Summary",
            f"- Historical-bar evidence/no-bars/not-evaluated: `{summary['historical_bar_evidence_collected_count']} / {summary['no_historical_bars_returned_count']} / {summary['not_evaluated_count']}`.",
            f"- Failures/warnings: `{summary['failure_count']} / {summary['warning_count']}`.",
            "- Calendar, session, and split/dividend adjustment semantics unsupported by this endpoint remain `NOT_EVALUATED_BY_SELECTED_ENDPOINT`.",
            "",
            "## API Key and Raw Payload Boundary",
            "- API keys were neither printed nor stored; raw provider payloads were not committed.",
            "",
            "## Acquisition Authority Boundary",
            "- Evidence execution does not authorize new-ticker acquisition or acquisition generation/execution.",
            "",
            "## Dataset Boundary",
            "- Dataset generation remains unauthorized.",
            "",
            "## Canonical Dataset Boundary",
            "- No canonical dataset candidate, authorization, or freeze was created.",
            "",
            "## Registry Boundary",
            "- Registry approval remains false.",
            "",
            "## Predictive/Profitability Boundary",
            "- Predictive usefulness and profitability remain not accepted; no experiment or scoring rerun occurred.",
            "",
            "## Runtime Boundary",
            "- Runtime, strategy, paper trading, and broker execution remain `NOT_AUTHORIZED`.",
            "",
            "## Checklist Summary",
            (
                "- Executed-artifact checks: `"
                + (f"{validation['passed_checks']} / {validation['total_checks']} passing`." if validation else "NOT_RUN_BLOCKED`.")
            ),
            "",
            "## Guardrails",
            "- Research-only, non-actionable evidence; no acquisition generation, dataset, canonical dataset, registry, predictive, profitability, runtime, or trading authority.",
            "- Next task: `ACQUISITION_EVIDENCE_RESULTS_REVIEW_PACKAGE_V1` only after successful execution; otherwise correct the environment/API-key boundary.",
            "",
        ]
    )
    return "\n".join(lines)
