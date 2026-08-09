"""Read-only live ticker validation execution service."""

from __future__ import annotations

import os
from copy import deepcopy
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Callable, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import acquisition_generation_service as acquisition
from marketflow.services import live_ticker_validation_approval_service as approval
from marketflow.services import live_ticker_validation_provider_adapter_service as provider


ARTIFACT_KIND_LIVE_TICKER_VALIDATION_PERFORMED = "LIVE_TICKER_VALIDATION_PERFORMED"
ARTIFACT_KIND_LIVE_TICKER_VALIDATION_BLOCKED = "LIVE_TICKER_VALIDATION_BLOCKED"
SCHEMA_VERSION_LIVE_TICKER_VALIDATION_PERFORMED_V1 = "live_ticker_validation_performed_v1"
LIVE_TICKER_VALIDATION_PERFORMED_READ_ONLY = "LIVE_TICKER_VALIDATION_PERFORMED_READ_ONLY"
LIVE_TICKER_VALIDATION_BLOCKED_LIVE_GATE_OR_API_KEY_MISSING = (
    "LIVE_TICKER_VALIDATION_BLOCKED_LIVE_GATE_OR_API_KEY_MISSING"
)
READ_ONLY_PROVIDER_TICKER_VALIDATION_ONLY = approval.READ_ONLY_PROVIDER_TICKER_VALIDATION_ONLY
RESEARCH_ONLY_NON_ACTIONABLE = "RESEARCH_ONLY_NON_ACTIONABLE"
NOT_AUTHORIZED = approval.NOT_AUTHORIZED
NOT_CREATED = approval.NOT_CREATED
VALIDATED_READ_ONLY = "VALIDATED_READ_ONLY"
VALIDATION_FAILED = "VALIDATION_FAILED"
PROVIDER_RESPONSE_UNAVAILABLE = "PROVIDER_RESPONSE_UNAVAILABLE"
NOT_EVALUATED_BY_SELECTED_ENDPOINT = "NOT_EVALUATED_BY_SELECTED_ENDPOINT"
PROVIDER_RESPONSE_AVAILABLE = "PROVIDER_RESPONSE_AVAILABLE"
PROVIDER_RESPONSE_FAILED = "PROVIDER_RESPONSE_FAILED"
DEFAULT_BRANCH = "feature/live-ticker-validation-execution-v1"
DEFAULT_BASE_COMMIT = "b57bce943703fe8d74ad83718a7f1c9365dccbfd"
DEFAULT_OUTPUT_ROOT = Path(".marketflow") / "live_ticker_validation" / "expanded_universe_v1"
GENERATED_OUTPUT_NAMES = [
    "live_ticker_validation_run_manifest.json",
    "ticker_validation_results.json",
    "provider_request_receipts_sanitized.json",
    "validation_summary.json",
    "validation_failure_reason_inventory.json",
    "operator_review_summary.json",
]

EXPECTED_LIVE_TICKER_VALIDATION_APPROVAL_DIGEST = (
    "2bf668bb4aae3756652ee5eea790b76d1ba73bdd7723efc1c31227c5c3e897e4"
)
EXPECTED_LIVE_TICKER_VALIDATION_CANDIDATE_DIGEST = (
    approval.EXPECTED_LIVE_TICKER_VALIDATION_CANDIDATE_DIGEST
)
EXPECTED_LIVE_TICKER_VALIDATION_CANDIDATE_REVIEW_PACKAGE_DIGEST = (
    approval.EXPECTED_LIVE_TICKER_VALIDATION_CANDIDATE_REVIEW_PACKAGE_DIGEST
)
EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST = (
    approval.EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST
)
VALIDATION_TARGET_UNIVERSE = list(approval.APPROVED_EXPANDED_TICKER_UNIVERSE)


class LiveTickerValidationExecutionError(ValueError):
    """Raised when read-only ticker validation execution violates guardrails."""


def _utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _path_text(path: Path) -> str:
    return str(path).replace("\\", "/")


def _api_key_from_environment() -> str | None:
    return os.environ.get("MASSIVE_API_KEY") or os.environ.get("POLYGON_API_KEY")


def _live_gate_enabled() -> bool:
    return os.environ.get(provider.LIVE_TICKER_VALIDATION_GATE_ENV) == "1"


def _boundary_fields() -> dict[str, Any]:
    return {
        "output_label": RESEARCH_ONLY_NON_ACTIONABLE,
        "validation_scope": READ_ONLY_PROVIDER_TICKER_VALIDATION_ONLY,
        "new_ticker_authority_created": False,
        "new_ticker_acquisition_authorized": False,
        "dataset_generation_authorized": False,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "predictive_usefulness": acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "profitability": acquisition.PROFITABILITY_NOT_ACCEPTED,
    }


def _status_from_bool(value: bool) -> str:
    return VALIDATED_READ_ONLY if value else VALIDATION_FAILED


def _ticker_result_from_response(ticker: str, response: Mapping[str, Any]) -> dict[str, Any]:
    details = response.get("sanitized_response")
    if not isinstance(details, Mapping):
        details = {}
    mapped_ticker = details.get("ticker")
    active = details.get("active")
    security_type = details.get("type")
    primary_exchange = details.get("primary_exchange")
    provider_response_digest = str(response.get("provider_response_digest") or "")
    result = {
        "ticker": ticker,
        "provider_request_status": PROVIDER_RESPONSE_AVAILABLE,
        "live_validation_status": VALIDATED_READ_ONLY,
        "listing_status": _status_from_bool(bool(mapped_ticker)),
        "security_type_status": _status_from_bool(isinstance(security_type, str) and bool(security_type)),
        "exchange_status": _status_from_bool(isinstance(primary_exchange, str) and bool(primary_exchange)),
        "active_status": _status_from_bool(active is True),
        "delisting_status": _status_from_bool(details.get("delisted_utc") in (None, "")),
        "tradability_status": _status_from_bool(active is True and bool(mapped_ticker)),
        "corporate_action_data_availability_status": NOT_EVALUATED_BY_SELECTED_ENDPOINT,
        "historical_aggregate_data_availability_status": NOT_EVALUATED_BY_SELECTED_ENDPOINT,
        "provider_symbol_mapping_status": _status_from_bool(mapped_ticker == ticker),
        "identity_authority_status": NOT_CREATED,
        "split_event_authority_status": NOT_CREATED,
        "dividend_event_authority_status": NOT_CREATED,
        "acquisition_authority_status": NOT_CREATED,
        "canonical_dataset_authority_status": NOT_CREATED,
        "registry_approval_status": NOT_CREATED,
        "research_use_status": NOT_AUTHORIZED,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "raw_response_stored": False,
        "raw_payload_committed": False,
        "api_key_stored_or_printed": False,
        "provider_response_digest": provider_response_digest,
        "failure_reason_if_any": None,
        "provider_endpoint": response.get("provider_endpoint"),
        "provider_endpoint_mode": response.get("provider_endpoint_mode"),
        "provider_request_mode": response.get("provider_request_mode"),
    }
    failed_statuses = [
        result["listing_status"],
        result["security_type_status"],
        result["exchange_status"],
        result["active_status"],
        result["delisting_status"],
        result["tradability_status"],
        result["provider_symbol_mapping_status"],
    ]
    if VALIDATION_FAILED in failed_statuses:
        result["live_validation_status"] = VALIDATION_FAILED
        result["failure_reason_if_any"] = "selected endpoint did not validate required ticker fields"
    result["sanitized_validation_digest"] = semantic_digest({key: value for key, value in result.items() if key != "sanitized_validation_digest"})
    return result


def _ticker_result_from_failure(ticker: str, reason: str) -> dict[str, Any]:
    result = {
        "ticker": ticker,
        "provider_request_status": PROVIDER_RESPONSE_FAILED,
        "live_validation_status": PROVIDER_RESPONSE_UNAVAILABLE,
        "listing_status": PROVIDER_RESPONSE_UNAVAILABLE,
        "security_type_status": PROVIDER_RESPONSE_UNAVAILABLE,
        "exchange_status": PROVIDER_RESPONSE_UNAVAILABLE,
        "active_status": PROVIDER_RESPONSE_UNAVAILABLE,
        "delisting_status": PROVIDER_RESPONSE_UNAVAILABLE,
        "tradability_status": PROVIDER_RESPONSE_UNAVAILABLE,
        "corporate_action_data_availability_status": NOT_EVALUATED_BY_SELECTED_ENDPOINT,
        "historical_aggregate_data_availability_status": NOT_EVALUATED_BY_SELECTED_ENDPOINT,
        "provider_symbol_mapping_status": PROVIDER_RESPONSE_UNAVAILABLE,
        "identity_authority_status": NOT_CREATED,
        "split_event_authority_status": NOT_CREATED,
        "dividend_event_authority_status": NOT_CREATED,
        "acquisition_authority_status": NOT_CREATED,
        "canonical_dataset_authority_status": NOT_CREATED,
        "registry_approval_status": NOT_CREATED,
        "research_use_status": NOT_AUTHORIZED,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "raw_response_stored": False,
        "raw_payload_committed": False,
        "api_key_stored_or_printed": False,
        "provider_response_digest": None,
        "failure_reason_if_any": reason,
        "provider_endpoint": None,
        "provider_endpoint_mode": provider.SELECTED_ENDPOINT_MODE,
        "provider_request_mode": None,
    }
    result["sanitized_validation_digest"] = semantic_digest({key: value for key, value in result.items() if key != "sanitized_validation_digest"})
    return result


def _summary(results: list[dict[str, Any]], output_root: Path, output_manifest: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    successful = sum(1 for item in results if item["provider_request_status"] == PROVIDER_RESPONSE_AVAILABLE)
    failed = len(results) - successful
    validated = sum(1 for item in results if item["live_validation_status"] == VALIDATED_READ_ONLY)
    validation_failed = sum(1 for item in results if item["live_validation_status"] == VALIDATION_FAILED)
    not_evaluated = sum(
        1
        for item in results
        for field in (
            "corporate_action_data_availability_status",
            "historical_aggregate_data_availability_status",
        )
        if item[field] == NOT_EVALUATED_BY_SELECTED_ENDPOINT
    )
    return {
        "validation_target_count": len(VALIDATION_TARGET_UNIVERSE),
        "provider_request_count": len(results),
        "successful_provider_response_count": successful,
        "failed_provider_response_count": failed,
        "validated_read_only_count": validated,
        "validation_failed_count": validation_failed,
        "not_evaluated_count": not_evaluated,
        "generated_output_root": _path_text(output_root),
        "generated_output_count": len(GENERATED_OUTPUT_NAMES),
        "output_digest_manifest": list(output_manifest or []),
        "failure_count": failed + validation_failed,
        "warning_count": not_evaluated,
    }


def _report(name: str, payload: dict[str, Any]) -> dict[str, Any]:
    return {"report_name": name, **_boundary_fields(), **payload}


def _output_payloads(
    *,
    run_timestamp_utc: str,
    results: list[dict[str, Any]],
    receipts: list[dict[str, Any]],
    output_root: Path,
) -> dict[str, dict[str, Any]]:
    summary = _summary(results, output_root)
    failures = [
        {
            "ticker": item["ticker"],
            "provider_request_status": item["provider_request_status"],
            "live_validation_status": item["live_validation_status"],
            "failure_reason_if_any": item["failure_reason_if_any"],
        }
        for item in results
        if item["failure_reason_if_any"]
    ]
    return {
        "live_ticker_validation_run_manifest.json": _report(
            "live_ticker_validation_run_manifest",
            {
                "schema_version": SCHEMA_VERSION_LIVE_TICKER_VALIDATION_PERFORMED_V1,
                "run_timestamp_utc": run_timestamp_utc,
                "selected_endpoint": provider.MASSIVE_TICKER_DETAILS_ENDPOINT_TEMPLATE,
                "selected_endpoint_mode": provider.SELECTED_ENDPOINT_MODE,
                "validation_target_universe": list(VALIDATION_TARGET_UNIVERSE),
                "source_approval_digest": EXPECTED_LIVE_TICKER_VALIDATION_APPROVAL_DIGEST,
                "raw_provider_payloads_included": False,
            },
        ),
        "ticker_validation_results.json": _report(
            "ticker_validation_results",
            {"results": results, "raw_provider_payloads_included": False},
        ),
        "provider_request_receipts_sanitized.json": _report(
            "provider_request_receipts_sanitized",
            {"provider_request_receipts": receipts, "raw_provider_payloads_included": False},
        ),
        "validation_summary.json": _report("validation_summary", summary),
        "validation_failure_reason_inventory.json": _report(
            "validation_failure_reason_inventory",
            {"failure_count": len(failures), "failures": failures},
        ),
        "operator_review_summary.json": _report(
            "operator_review_summary",
            {
                "operator_review_status": "LIVE_TICKER_VALIDATION_RESULTS_REVIEW_REQUIRED",
                "next_task": "live ticker validation results operator review package",
                "new_ticker_authority_created": False,
                "new_ticker_acquisition_authorized": False,
                "dataset_generation_authorized": False,
                "predictive_usefulness_acceptance_ready": False,
                "profitability_acceptance_ready": False,
                "runtime_migration_approved": False,
            },
        ),
    }


def _write_outputs(output_root: Path, payloads: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    output_root.mkdir(parents=True, exist_ok=True)
    manifest: list[dict[str, Any]] = []
    for name in GENERATED_OUTPUT_NAMES:
        path = output_root / name
        data = canonical_json_bytes(payloads[name])
        path.write_bytes(data)
        manifest.append(
            {
                "output_name": name,
                "path": _path_text(path),
                "sha256_digest": sha256_bytes(data),
                "semantic_digest": semantic_digest(payloads[name]),
                "output_label": RESEARCH_ONLY_NON_ACTIONABLE,
                "raw_provider_payloads_included": False,
            }
        )
    return manifest


def _blocked_artifact(*, run_timestamp_utc: str, output_root: Path, reason: str) -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_LIVE_TICKER_VALIDATION_BLOCKED,
        "schema_version": SCHEMA_VERSION_LIVE_TICKER_VALIDATION_PERFORMED_V1,
        "execution_status": LIVE_TICKER_VALIDATION_BLOCKED_LIVE_GATE_OR_API_KEY_MISSING,
        "validation_scope": READ_ONLY_PROVIDER_TICKER_VALIDATION_ONLY,
        "created_offline": False,
        "run_timestamp_utc": run_timestamp_utc,
        "blocker_reason": reason,
        "provider_request_authorized": True,
        "provider_requests_made": False,
        "live_provider_transport_enabled": False,
        "live_ticker_validation_authorized": True,
        "live_ticker_validation_performed": False,
        "live_validation_results_created": False,
        "provider_requests_made_in_execution": False,
        "raw_provider_payloads_committed": False,
        "api_keys_stored_or_printed": False,
        "validation_target_universe": list(VALIDATION_TARGET_UNIVERSE),
        "validation_target_count": len(VALIDATION_TARGET_UNIVERSE),
        "generated_output_root": _path_text(output_root),
        "generated_output_count": 0,
        "failure_count": 1,
        "warning_count": 0,
        "live_ticker_validation_approval_digest": EXPECTED_LIVE_TICKER_VALIDATION_APPROVAL_DIGEST,
        "live_ticker_validation_candidate_digest": EXPECTED_LIVE_TICKER_VALIDATION_CANDIDATE_DIGEST,
        "live_ticker_validation_candidate_review_package_digest": EXPECTED_LIVE_TICKER_VALIDATION_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "ticker_universe_selection_approval_digest": EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST,
        **_closed_authority_fields(),
    }


def _closed_authority_fields() -> dict[str, Any]:
    return {
        "ticker_universe_selection_approved": True,
        "expanded_ticker_universe_approved": True,
        "new_ticker_authority_created": False,
        "new_ticker_acquisition_authorized": False,
        "dataset_generation_authorized": False,
        "additional_predictive_evidence_execution_authorized": False,
        "additional_predictive_evidence_executed": False,
        "predictive_experiment_rerun_authorized": False,
        "predictive_experiment_rerun_performed": False,
        "walk_forward_rerun_performed": False,
        "label_regeneration_performed": False,
        "feature_matrix_regeneration_performed": False,
        "new_strategy_scoring_performed": False,
        "trade_recommendations_generated": False,
        "research_only": True,
        "predictive_usefulness": acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "predictive_usefulness_acceptance_ready": False,
        "predictive_usefulness_acceptance_recommended": False,
        "predictive_usefulness_acceptance_candidate_created": False,
        "profitability": acquisition.PROFITABILITY_NOT_ACCEPTED,
        "profitability_acceptance_ready": False,
        "profitability_acceptance_recommended": False,
        "runtime_migration_recommended": False,
        "runtime_migration_approved": False,
        "runtime_migration_active": False,
        "strategy_runtime_migration": False,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "automatic_stitching": False,
    }


def execute_live_ticker_validation_v1(
    *,
    api_key: str | None = None,
    transport: Callable[[Mapping[str, Any]], Any] | None = None,
    output_root: str | Path | None = None,
    run_timestamp_utc: str | None = None,
) -> dict[str, Any]:
    """Execute approved read-only ticker validation or return a blocked artifact."""
    timestamp = run_timestamp_utc or _utc_now()
    root = DEFAULT_OUTPUT_ROOT if output_root is None else Path(output_root)
    resolved_api_key = api_key or _api_key_from_environment()
    if transport is None and not _live_gate_enabled():
        return _blocked_artifact(
            run_timestamp_utc=timestamp,
            output_root=root,
            reason="live gate missing",
        )
    if transport is None and resolved_api_key is None:
        return _blocked_artifact(
            run_timestamp_utc=timestamp,
            output_root=root,
            reason="api key missing",
        )
    key_for_adapter = resolved_api_key or "injected-provider-response-key"
    results: list[dict[str, Any]] = []
    receipts: list[dict[str, Any]] = []
    for ticker in VALIDATION_TARGET_UNIVERSE:
        try:
            response = provider.fetch_massive_ticker_details_v1(
                ticker=ticker,
                api_key=key_for_adapter,
                transport=transport,
                request_timestamp_utc=timestamp,
            )
            results.append(_ticker_result_from_response(ticker, response))
            receipts.append(
                {
                    "ticker": ticker,
                    "provider_name": response["provider_name"],
                    "provider_endpoint": response["provider_endpoint"],
                    "provider_endpoint_mode": response["provider_endpoint_mode"],
                    "provider_request_mode": response["provider_request_mode"],
                    "provider_response_status": response["provider_response_status"],
                    "provider_response_digest": response["provider_response_digest"],
                    "raw_response_stored": False,
                    "raw_payload_committed": False,
                    "api_key_stored_or_printed": False,
                }
            )
        except provider.LiveTickerValidationProviderAdapterError as exc:
            results.append(_ticker_result_from_failure(ticker, str(exc)))
            receipts.append(
                {
                    "ticker": ticker,
                    "provider_name": provider.PROVIDER_NAME,
                    "provider_endpoint": provider.MASSIVE_TICKER_DETAILS_ENDPOINT_TEMPLATE,
                    "provider_endpoint_mode": provider.SELECTED_ENDPOINT_MODE,
                    "provider_request_mode": None,
                    "provider_response_status": PROVIDER_RESPONSE_UNAVAILABLE,
                    "provider_response_digest": None,
                    "failure_reason_if_any": str(exc),
                    "raw_response_stored": False,
                    "raw_payload_committed": False,
                    "api_key_stored_or_printed": False,
                }
            )
    payloads = _output_payloads(
        run_timestamp_utc=timestamp,
        results=results,
        receipts=receipts,
        output_root=root,
    )
    output_manifest = _write_outputs(root, payloads)
    summary = _summary(results, root, output_manifest)
    artifact = {
        "artifact_kind": ARTIFACT_KIND_LIVE_TICKER_VALIDATION_PERFORMED,
        "schema_version": SCHEMA_VERSION_LIVE_TICKER_VALIDATION_PERFORMED_V1,
        "execution_status": LIVE_TICKER_VALIDATION_PERFORMED_READ_ONLY,
        "validation_scope": READ_ONLY_PROVIDER_TICKER_VALIDATION_ONLY,
        "created_offline": False,
        "branch": DEFAULT_BRANCH,
        "base_commit": DEFAULT_BASE_COMMIT,
        "run_timestamp_utc": timestamp,
        "selected_endpoint": provider.MASSIVE_TICKER_DETAILS_ENDPOINT_TEMPLATE,
        "selected_endpoint_mode": provider.SELECTED_ENDPOINT_MODE,
        "selected_provider": provider.PROVIDER_NAME,
        "provider_request_authorized": True,
        "provider_requests_made": True,
        "live_provider_transport_enabled": True,
        "live_ticker_validation_authorized": True,
        "live_ticker_validation_performed": True,
        "live_validation_results_created": True,
        "provider_requests_made_in_execution": True,
        "raw_provider_payloads_committed": False,
        "api_keys_stored_or_printed": False,
        "validation_target_universe": list(VALIDATION_TARGET_UNIVERSE),
        "validation_target_count": len(VALIDATION_TARGET_UNIVERSE),
        "per_ticker_results": results,
        "provider_request_receipts_sanitized": receipts,
        "live_ticker_validation_approval_digest": EXPECTED_LIVE_TICKER_VALIDATION_APPROVAL_DIGEST,
        "live_ticker_validation_candidate_digest": EXPECTED_LIVE_TICKER_VALIDATION_CANDIDATE_DIGEST,
        "live_ticker_validation_candidate_review_package_digest": EXPECTED_LIVE_TICKER_VALIDATION_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "ticker_universe_selection_approval_digest": EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST,
        **summary,
        **_closed_authority_fields(),
    }
    artifact["live_ticker_validation_execution_digest"] = live_ticker_validation_execution_digest_v1(artifact)
    validate_live_ticker_validation_performed_v1(artifact)
    return artifact


def _digest_payload(artifact: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(artifact)
    payload.pop("live_ticker_validation_execution_digest", None)
    return payload


def live_ticker_validation_execution_digest_v1(artifact: dict[str, Any]) -> str:
    """Return the deterministic semantic digest for a performed validation artifact."""
    return semantic_digest(_digest_payload(artifact))


def _expect(actual: Any, expected: Any, field_name: str) -> None:
    if actual != expected:
        raise LiveTickerValidationExecutionError(f"{field_name} mismatch")


def _expect_true(actual: Any, field_name: str) -> None:
    if actual is not True:
        raise LiveTickerValidationExecutionError(f"{field_name} must be true")


def _expect_false(actual: Any, field_name: str) -> None:
    if actual is not False:
        raise LiveTickerValidationExecutionError(f"{field_name} must be false")


def _validate_outputs(artifact: dict[str, Any]) -> None:
    _expect(artifact.get("generated_output_count"), len(GENERATED_OUTPUT_NAMES), "generated_output_count")
    manifest = artifact.get("output_digest_manifest")
    if not isinstance(manifest, list) or len(manifest) != len(GENERATED_OUTPUT_NAMES):
        raise LiveTickerValidationExecutionError("output_digest_manifest missing")
    names = [item.get("output_name") for item in manifest if isinstance(item, Mapping)]
    _expect(names, GENERATED_OUTPUT_NAMES, "output_digest_manifest output names")
    if any(item.get("output_label") != RESEARCH_ONLY_NON_ACTIONABLE for item in manifest if isinstance(item, Mapping)):
        raise LiveTickerValidationExecutionError("output labels must be research-only")
    if any(item.get("raw_provider_payloads_included") is not False for item in manifest if isinstance(item, Mapping)):
        raise LiveTickerValidationExecutionError("raw provider payloads must not be included")


def _validate_per_ticker_results(artifact: dict[str, Any]) -> None:
    results = artifact.get("per_ticker_results")
    if not isinstance(results, list):
        raise LiveTickerValidationExecutionError("per_ticker_results missing")
    _expect([item.get("ticker") for item in results], VALIDATION_TARGET_UNIVERSE, "per_ticker_results ticker order")
    for item in results:
        if item.get("raw_payload_committed") is not False or item.get("api_key_stored_or_printed") is not False:
            raise LiveTickerValidationExecutionError("per-ticker raw payload or API key boundary failed")
        if item.get("provider_request_status") == PROVIDER_RESPONSE_AVAILABLE and not item.get("provider_response_digest"):
            raise LiveTickerValidationExecutionError("provider_response_digest missing")
        if item.get("provider_request_status") == PROVIDER_RESPONSE_FAILED and not item.get("failure_reason_if_any"):
            raise LiveTickerValidationExecutionError("provider failure reason missing")
        if not item.get("sanitized_validation_digest"):
            raise LiveTickerValidationExecutionError("sanitized_validation_digest missing")
        for field in (
            "identity_authority_status",
            "split_event_authority_status",
            "dividend_event_authority_status",
            "acquisition_authority_status",
            "canonical_dataset_authority_status",
            "registry_approval_status",
        ):
            _expect(item.get(field), NOT_CREATED, f"{item.get('ticker')}.{field}")
        for field in ("research_use_status", "runtime_use", "strategy_use", "paper_trading", "broker_execution"):
            _expect(item.get(field), NOT_AUTHORIZED, f"{item.get('ticker')}.{field}")


def validate_live_ticker_validation_performed_v1(artifact: dict[str, Any]) -> dict[str, Any]:
    """Validate performed read-only ticker validation guardrails."""
    if not isinstance(artifact, dict):
        raise LiveTickerValidationExecutionError("artifact must be a JSON object")
    for field, expected in {
        "artifact_kind": ARTIFACT_KIND_LIVE_TICKER_VALIDATION_PERFORMED,
        "schema_version": SCHEMA_VERSION_LIVE_TICKER_VALIDATION_PERFORMED_V1,
        "execution_status": LIVE_TICKER_VALIDATION_PERFORMED_READ_ONLY,
        "validation_scope": READ_ONLY_PROVIDER_TICKER_VALIDATION_ONLY,
        "validation_target_universe": VALIDATION_TARGET_UNIVERSE,
        "validation_target_count": len(VALIDATION_TARGET_UNIVERSE),
        "live_ticker_validation_approval_digest": EXPECTED_LIVE_TICKER_VALIDATION_APPROVAL_DIGEST,
        "live_ticker_validation_candidate_digest": EXPECTED_LIVE_TICKER_VALIDATION_CANDIDATE_DIGEST,
        "live_ticker_validation_candidate_review_package_digest": EXPECTED_LIVE_TICKER_VALIDATION_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "ticker_universe_selection_approval_digest": EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST,
    }.items():
        _expect(artifact.get(field), expected, field)
    for field in (
        "provider_request_authorized",
        "provider_requests_made",
        "live_provider_transport_enabled",
        "live_ticker_validation_authorized",
        "live_ticker_validation_performed",
        "live_validation_results_created",
        "provider_requests_made_in_execution",
        "ticker_universe_selection_approved",
        "expanded_ticker_universe_approved",
        "research_only",
    ):
        _expect_true(artifact.get(field), field)
    for field in (
        "raw_provider_payloads_committed",
        "api_keys_stored_or_printed",
        "new_ticker_authority_created",
        "new_ticker_acquisition_authorized",
        "dataset_generation_authorized",
        "additional_predictive_evidence_execution_authorized",
        "additional_predictive_evidence_executed",
        "predictive_experiment_rerun_authorized",
        "predictive_experiment_rerun_performed",
        "walk_forward_rerun_performed",
        "label_regeneration_performed",
        "feature_matrix_regeneration_performed",
        "new_strategy_scoring_performed",
        "trade_recommendations_generated",
        "predictive_usefulness_acceptance_ready",
        "predictive_usefulness_acceptance_recommended",
        "predictive_usefulness_acceptance_candidate_created",
        "profitability_acceptance_ready",
        "profitability_acceptance_recommended",
        "runtime_migration_recommended",
        "runtime_migration_approved",
        "runtime_migration_active",
        "strategy_runtime_migration",
        "automatic_stitching",
    ):
        _expect_false(artifact.get(field), field)
    for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
        _expect(artifact.get(field), NOT_AUTHORIZED, field)
    _expect(artifact.get("predictive_usefulness"), acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED, "predictive_usefulness")
    _expect(artifact.get("profitability"), acquisition.PROFITABILITY_NOT_ACCEPTED, "profitability")
    _validate_per_ticker_results(artifact)
    _validate_outputs(artifact)
    digest = artifact.get("live_ticker_validation_execution_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise LiveTickerValidationExecutionError("live_ticker_validation_execution_digest missing")
    _expect(digest, live_ticker_validation_execution_digest_v1(artifact), "live_ticker_validation_execution_digest")
    return {
        "status": "LIVE_TICKER_VALIDATION_PERFORMED_VALID",
        "artifact_kind": artifact["artifact_kind"],
        "execution_status": artifact["execution_status"],
        "live_ticker_validation_execution_digest": digest,
        "validation_target_count": artifact["validation_target_count"],
        "provider_request_count": artifact["provider_request_count"],
        "successful_provider_response_count": artifact["successful_provider_response_count"],
        "failed_provider_response_count": artifact["failed_provider_response_count"],
        "generated_output_count": artifact["generated_output_count"],
        "failure_count": artifact["failure_count"],
        "warning_count": artifact["warning_count"],
        "runtime_use": artifact["runtime_use"],
        "broker_execution": artifact["broker_execution"],
    }


def build_live_ticker_validation_execution_status_markdown_v1(artifact: dict[str, Any]) -> str:
    """Render a sanitized status document for live ticker validation execution."""
    if artifact.get("artifact_kind") == ARTIFACT_KIND_LIVE_TICKER_VALIDATION_PERFORMED:
        validation = validate_live_ticker_validation_performed_v1(artifact)
    else:
        validation = {"live_ticker_validation_execution_digest": "NOT_CREATED"}
    lines = [
        "# MarketFlow Live Ticker Validation Execution Status",
        "",
        "## Branch And Commit",
        f"- Branch: `{artifact.get('branch', DEFAULT_BRANCH)}`",
        f"- Base commit: `{artifact.get('base_commit', DEFAULT_BASE_COMMIT)}`",
        "- Implementation commit: the commit containing this document.",
        "",
        "## Execution Artifact",
        f"- Artifact kind: `{artifact['artifact_kind']}`",
        f"- Execution status: `{artifact['execution_status']}`",
        f"- Schema version: `{artifact['schema_version']}`",
        f"- Execution digest: `{validation['live_ticker_validation_execution_digest']}`",
        f"- Approval digest: `{artifact['live_ticker_validation_approval_digest']}`",
        f"- Validation scope: `{artifact['validation_scope']}`",
        "",
        "## Selected Endpoint And Mode",
        f"- Provider: `{artifact.get('selected_provider', provider.PROVIDER_NAME)}`",
        f"- Endpoint: `{artifact.get('selected_endpoint', provider.MASSIVE_TICKER_DETAILS_ENDPOINT_TEMPLATE)}`",
        f"- Mode: `{artifact.get('selected_endpoint_mode', provider.SELECTED_ENDPOINT_MODE)}`",
        "",
        "## Validation Target Universe",
        f"- Validation target count: `{artifact['validation_target_count']}`",
        "- Validation targets: " + ", ".join(f"`{ticker}`" for ticker in artifact["validation_target_universe"]),
        "",
        "## Provider Request Summary",
        f"- Provider request count: `{artifact.get('provider_request_count', 0)}`",
        f"- Successful provider response count: `{artifact.get('successful_provider_response_count', 0)}`",
        f"- Failed provider response count: `{artifact.get('failed_provider_response_count', 0)}`",
        f"- Failure count: `{artifact.get('failure_count', 0)}`",
        f"- Warning count: `{artifact.get('warning_count', 0)}`",
        "",
        "## Generated Outputs",
        f"- Generated output root: `{artifact.get('generated_output_root')}`",
        f"- Generated output count: `{artifact.get('generated_output_count')}`",
        "- Output digest manifest summary: "
        + ", ".join(item["output_name"] for item in artifact.get("output_digest_manifest", [])),
        "",
        "## API Key / Raw Payload Boundary",
        f"- raw_provider_payloads_committed: `{artifact['raw_provider_payloads_committed']}`",
        f"- api_keys_stored_or_printed: `{artifact['api_keys_stored_or_printed']}`",
        "- API keys, authorization headers, and raw provider payloads are not included in this status document.",
        "",
        "## Authority Boundaries",
        f"- provider_request_authorized: `{artifact['provider_request_authorized']}`",
        f"- provider_requests_made: `{artifact['provider_requests_made']}`",
        f"- live_provider_transport_enabled: `{artifact['live_provider_transport_enabled']}`",
        f"- live_ticker_validation_authorized: `{artifact['live_ticker_validation_authorized']}`",
        f"- live_ticker_validation_performed: `{artifact['live_ticker_validation_performed']}`",
        f"- live_validation_results_created: `{artifact['live_validation_results_created']}`",
        f"- new_ticker_authority_created: `{artifact['new_ticker_authority_created']}`",
        f"- new_ticker_acquisition_authorized: `{artifact['new_ticker_acquisition_authorized']}`",
        f"- dataset_generation_authorized: `{artifact['dataset_generation_authorized']}`",
        f"- additional_predictive_evidence_execution_authorized: `{artifact['additional_predictive_evidence_execution_authorized']}`",
        f"- additional_predictive_evidence_executed: `{artifact['additional_predictive_evidence_executed']}`",
        f"- predictive_usefulness: `{artifact['predictive_usefulness']}`",
        f"- profitability: `{artifact['profitability']}`",
        f"- runtime_migration_approved: `{artifact['runtime_migration_approved']}`",
        f"- runtime_use: `{artifact['runtime_use']}`",
        f"- strategy_use: `{artifact['strategy_use']}`",
        f"- paper_trading: `{artifact['paper_trading']}`",
        f"- broker_execution: `{artifact['broker_execution']}`",
        "",
        "## Non-Goals",
        "- No new ticker authority or acquisition authority is created.",
        "- No dataset generation authorization is created.",
        "- No predictive experiment, label, feature matrix, or strategy scoring execution is performed.",
        "- No predictive usefulness or profitability acceptance is created.",
        "- No runtime migration, runtime activation, paper trading, or broker execution is authorized.",
        "",
        "## Next Task",
        "1. Live ticker validation results operator review package.",
        "",
    ]
    if artifact.get("per_ticker_results"):
        lines.insert(
            34,
            "- Per-ticker validation summary: "
            + "; ".join(
                f"{item['ticker']}={item['live_validation_status']}"
                for item in artifact["per_ticker_results"]
            ),
        )
    return "\n".join(lines)
