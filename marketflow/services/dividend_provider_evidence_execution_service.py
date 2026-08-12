"""Read-only dividend provider evidence execution for the expanded universe."""

from __future__ import annotations

from copy import deepcopy
from datetime import UTC, datetime
import os
from pathlib import Path
from typing import Any, Callable, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import acquisition_generation_service as acquisition
from marketflow.services import dividend_event_provider_adapter_service as provider_adapter
from marketflow.services import dividend_provider_evidence_request_approval_service as approval
from marketflow.services import split_event_authority_freeze_service as split_freeze


ARTIFACT_KIND_DIVIDEND_PROVIDER_EVIDENCE_EXECUTED = "DIVIDEND_EVENT_PROVIDER_EVIDENCE_EXECUTED"
ARTIFACT_KIND_DIVIDEND_PROVIDER_EVIDENCE_BLOCKED = "DIVIDEND_EVENT_PROVIDER_EVIDENCE_BLOCKED"
SCHEMA_VERSION_DIVIDEND_PROVIDER_EVIDENCE_EXECUTED_V1 = "dividend_provider_evidence_executed_v1"
DIVIDEND_PROVIDER_EVIDENCE_EXECUTED_READ_ONLY = "DIVIDEND_EVENT_PROVIDER_EVIDENCE_EXECUTED_READ_ONLY"
DIVIDEND_PROVIDER_EVIDENCE_BLOCKED_LIVE_GATE_OR_API_KEY_MISSING = (
    "DIVIDEND_EVENT_PROVIDER_EVIDENCE_BLOCKED_LIVE_GATE_OR_API_KEY_MISSING"
)
DIVIDEND_PROVIDER_EVIDENCE_BLOCKED_ENDPOINT_NOT_SELECTED = (
    "DIVIDEND_EVENT_PROVIDER_EVIDENCE_BLOCKED_ENDPOINT_NOT_SELECTED"
)
MARKETFLOW_ENABLE_LIVE_DIVIDEND_PROVIDER_EVIDENCE = "MARKETFLOW_ENABLE_LIVE_DIVIDEND_PROVIDER_EVIDENCE"

READ_ONLY_DIVIDEND_EVENT_EVIDENCE_REQUESTS_ONLY = approval.DIVIDEND_PROVIDER_EVIDENCE_REQUEST_SCOPE
RESEARCH_ONLY_NON_ACTIONABLE = approval.RESEARCH_ONLY_NON_ACTIONABLE
NOT_AUTHORIZED = approval.NOT_AUTHORIZED
NOT_CREATED = approval.NOT_CREATED
NOT_FROZEN = approval.NOT_FROZEN
PASS = approval.PASS
FAIL = approval.FAIL
BLOCKER = approval.BLOCKER

DIVIDEND_EVIDENCE_COLLECTED_READ_ONLY = "DIVIDEND_EVIDENCE_COLLECTED_READ_ONLY"
NO_DIVIDEND_EVENTS_RETURNED_BY_PROVIDER = "NO_DIVIDEND_EVENTS_RETURNED_BY_PROVIDER"
DIVIDEND_EVIDENCE_PROVIDER_RESPONSE_UNAVAILABLE = "DIVIDEND_EVIDENCE_PROVIDER_RESPONSE_UNAVAILABLE"
DIVIDEND_EVIDENCE_NOT_EVALUATED_BY_SELECTED_ENDPOINT = (
    "DIVIDEND_EVIDENCE_NOT_EVALUATED_BY_SELECTED_ENDPOINT"
)

OUTPUT_ROOT = Path(".marketflow") / "dividend_event_provider_evidence" / "expanded_universe_v1"
OUTPUT_FILENAMES = [
    "dividend_provider_evidence_run_manifest.json",
    "dividend_provider_request_receipts_sanitized.json",
    "dividend_event_results_sanitized.json",
    "dividend_event_absence_inventory.json",
    "dividend_policy_reconciliation_report.json",
    "dividend_event_failure_reason_inventory.json",
    "operator_review_summary.json",
]
TARGET_UNIVERSE = list(approval.TARGET_UNIVERSE)
EXPECTED_DIVIDEND_PROVIDER_EVIDENCE_REQUEST_APPROVAL_DIGEST = (
    "f2b96963ceced82579a647fa1e51ddca1dad91b3de66a35aad8fc389cdbbb2ff"
)
DIVIDEND_HISTORY_START_DATE = "1900-01-01"
PLANNED_DIVIDEND_EVIDENCE_CHECKS = [
    "dividend_event_history",
    "cash_dividend_amount",
    "dividend_currency",
    "dividend_ex_date",
    "dividend_record_date_if_available",
    "dividend_pay_date_if_available",
    "dividend_declaration_date_if_available",
    "dividend_provider_event_id_if_available",
    "dividend_frequency_if_available",
    "special_dividend_flag_if_available",
    "dividend_adjustment_implication",
    "dividend_adjusted_price_impact_policy",
    "dividend_source_endpoint",
    "provider_response_digest",
    "sanitized_dividend_event_digest",
    "dividend_event_absence_policy_if_no_dividends_returned",
]


class DividendProviderEvidenceExecutionError(ValueError):
    """Raised when dividend provider evidence execution violates the read-only contract."""


def _utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _date_from_timestamp(timestamp_utc: str) -> str:
    try:
        return datetime.fromisoformat(timestamp_utc.replace("Z", "+00:00")).date().isoformat()
    except ValueError as exc:
        raise DividendProviderEvidenceExecutionError("run_timestamp_utc must be ISO-8601 UTC text") from exc


def _api_key_from_environment() -> str | None:
    return os.environ.get("MASSIVE_API_KEY") or os.environ.get("POLYGON_API_KEY")


def _not_accepted() -> str:
    return acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED


def _base_output_fields() -> dict[str, Any]:
    return {
        "output_label": RESEARCH_ONLY_NON_ACTIONABLE,
        "evidence_scope": READ_ONLY_DIVIDEND_EVENT_EVIDENCE_REQUESTS_ONLY,
        "dividend_event_authority_created": False,
        "dividend_event_authority_frozen": False,
        "split_event_authority_created": True,
        "split_event_authority_frozen": True,
        "corporate_action_authority_created": False,
        "new_ticker_acquisition_authorized": False,
        "dataset_generation_authorized": False,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "predictive_usefulness": _not_accepted(),
        "profitability": acquisition.PROFITABILITY_NOT_ACCEPTED,
    }


def _digest_payload(payload: dict[str, Any], digest_field: str) -> dict[str, Any]:
    clone = deepcopy(payload)
    clone.pop(digest_field, None)
    return clone


def dividend_provider_evidence_execution_digest_v1(artifact: dict[str, Any]) -> str:
    """Return the deterministic digest for an executed read-only dividend evidence artifact."""
    return semantic_digest(_digest_payload(artifact, "dividend_provider_evidence_execution_digest"))


def _first_present(row: Mapping[str, Any], *names: str) -> Any:
    for name in names:
        if row.get(name) is not None:
            return row.get(name)
    return None


def _sanitized_event(row: Mapping[str, Any], *, index: int, ticker: str) -> dict[str, Any]:
    event = {
        "ticker": row.get("ticker") if isinstance(row.get("ticker"), str) else ticker,
        "cash_dividend_amount": _first_present(row, "cash_amount", "cashAmount", "amount", "dividend_amount"),
        "dividend_currency": _first_present(row, "currency", "cash_currency"),
        "dividend_ex_date": _first_present(row, "ex_dividend_date", "ex_date"),
        "dividend_record_date_if_available": _first_present(row, "record_date"),
        "dividend_pay_date_if_available": _first_present(row, "pay_date", "payable_date", "payment_date"),
        "dividend_declaration_date_if_available": _first_present(row, "declaration_date", "declared_date"),
        "dividend_provider_event_id_if_available": _first_present(row, "id", "event_id"),
        "dividend_frequency_if_available": _first_present(row, "frequency"),
        "special_dividend_flag_if_available": _first_present(row, "special_dividend", "is_special"),
        "raw_event_index": index,
    }
    event["sanitized_dividend_event_digest"] = semantic_digest(event)
    return event


def _result_digest_payload(result: dict[str, Any]) -> dict[str, Any]:
    clone = deepcopy(result)
    clone.pop("sanitized_dividend_evidence_digest", None)
    return clone


def _not_evaluated_fields(events: list[dict[str, Any]]) -> list[str]:
    if not events:
        return [
            "cash_dividend_amount",
            "dividend_currency",
            "dividend_ex_date",
            "dividend_record_date_if_available",
            "dividend_pay_date_if_available",
            "dividend_declaration_date_if_available",
            "dividend_provider_event_id_if_available",
            "dividend_frequency_if_available",
            "special_dividend_flag_if_available",
            "dividend_adjustment_implication",
            "dividend_adjusted_price_impact_policy",
        ]
    missing: set[str] = set()
    for field in (
        "cash_dividend_amount",
        "dividend_currency",
        "dividend_ex_date",
        "dividend_record_date_if_available",
        "dividend_pay_date_if_available",
        "dividend_declaration_date_if_available",
        "dividend_provider_event_id_if_available",
        "dividend_frequency_if_available",
        "special_dividend_flag_if_available",
    ):
        if any(event.get(field) is None for event in events):
            missing.add(field)
    missing.update({"dividend_adjustment_implication", "dividend_adjusted_price_impact_policy"})
    return sorted(missing)


def _dividend_check_statuses(result: dict[str, Any]) -> list[dict[str, Any]]:
    if result["dividend_provider_evidence_status"] == DIVIDEND_EVIDENCE_PROVIDER_RESPONSE_UNAVAILABLE:
        return [
            {"check": check, "status": DIVIDEND_EVIDENCE_PROVIDER_RESPONSE_UNAVAILABLE}
            for check in PLANNED_DIVIDEND_EVIDENCE_CHECKS
        ]
    statuses: list[dict[str, Any]] = []
    for check in PLANNED_DIVIDEND_EVIDENCE_CHECKS:
        if check in result["not_evaluated_fields"]:
            observed = DIVIDEND_EVIDENCE_NOT_EVALUATED_BY_SELECTED_ENDPOINT
        elif check == "dividend_event_absence_policy_if_no_dividends_returned" and result["dividend_event_count"] == 0:
            observed = NO_DIVIDEND_EVENTS_RETURNED_BY_PROVIDER
        else:
            observed = DIVIDEND_EVIDENCE_COLLECTED_READ_ONLY
        statuses.append({"check": check, "status": observed})
    return statuses


def _ticker_result_from_raw(ticker: str, raw: Mapping[str, Any]) -> dict[str, Any]:
    raw_results = raw.get("results")
    rows = raw_results if isinstance(raw_results, list) else []
    events = [_sanitized_event(row, index=index, ticker=ticker) for index, row in enumerate(rows) if isinstance(row, Mapping)]
    evidence_status = DIVIDEND_EVIDENCE_COLLECTED_READ_ONLY if events else NO_DIVIDEND_EVENTS_RETURNED_BY_PROVIDER
    result: dict[str, Any] = {
        "ticker": ticker,
        "provider_request_status": "REQUEST_PERFORMED_READ_ONLY",
        "dividend_provider_evidence_status": evidence_status,
        "dividend_event_count": len(events),
        "dividend_history_status": evidence_status,
        "dividend_absence_policy_status": (
            "NO_DIVIDEND_EVENT_ABSENCE_POLICY_APPLIED"
            if events
            else NO_DIVIDEND_EVENTS_RETURNED_BY_PROVIDER
        ),
        "dividend_event_results": events,
        "dividend_policy_reconciliation_status": "REQUIRES_OPERATOR_REVIEW",
        "not_evaluated_fields": _not_evaluated_fields(events),
        "provider_response_digest": raw.get("provider_raw_response_digest"),
        "provider_response_status": raw.get("provider_response_status"),
        "provider_response_page_count": raw.get("provider_response_page_count"),
        "provider_raw_response_row_count": raw.get("provider_raw_response_row_count"),
        "provider_request_metadata": deepcopy(raw.get("request")),
        "raw_response_stored": False,
        "raw_payload_committed": False,
        "api_key_stored_or_printed": False,
        "dividend_event_authority_status": NOT_CREATED,
        "dividend_event_freeze_status": NOT_FROZEN,
        "split_event_authority_status": "FROZEN",
        "corporate_action_authority_created": False,
        "acquisition_authorized": False,
        "dataset_generation_authorized": False,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "failure_reason_if_any": None,
    }
    result["dividend_evidence_checks"] = _dividend_check_statuses(result)
    result["sanitized_dividend_evidence_digest"] = semantic_digest(_result_digest_payload(result))
    return result


def _unavailable_ticker_result(ticker: str, reason: str) -> dict[str, Any]:
    result: dict[str, Any] = {
        "ticker": ticker,
        "provider_request_status": "REQUEST_FAILED_READ_ONLY",
        "dividend_provider_evidence_status": DIVIDEND_EVIDENCE_PROVIDER_RESPONSE_UNAVAILABLE,
        "dividend_event_count": 0,
        "dividend_history_status": DIVIDEND_EVIDENCE_PROVIDER_RESPONSE_UNAVAILABLE,
        "dividend_absence_policy_status": "NOT_APPLIED_PROVIDER_RESPONSE_UNAVAILABLE",
        "dividend_event_results": [],
        "dividend_policy_reconciliation_status": "NOT_EVALUATED_PROVIDER_RESPONSE_UNAVAILABLE",
        "not_evaluated_fields": list(PLANNED_DIVIDEND_EVIDENCE_CHECKS),
        "provider_response_digest": None,
        "provider_response_status": None,
        "provider_response_page_count": 0,
        "provider_raw_response_row_count": 0,
        "provider_request_metadata": None,
        "raw_response_stored": False,
        "raw_payload_committed": False,
        "api_key_stored_or_printed": False,
        "dividend_event_authority_status": NOT_CREATED,
        "dividend_event_freeze_status": NOT_FROZEN,
        "split_event_authority_status": "FROZEN",
        "corporate_action_authority_created": False,
        "acquisition_authorized": False,
        "dataset_generation_authorized": False,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "failure_reason_if_any": reason,
    }
    result["dividend_evidence_checks"] = _dividend_check_statuses(result)
    result["sanitized_dividend_evidence_digest"] = semantic_digest(_result_digest_payload(result))
    return result


def _summary(results: list[dict[str, Any]]) -> dict[str, Any]:
    successful = [item for item in results if item["provider_request_status"] == "REQUEST_PERFORMED_READ_ONLY"]
    failed = [item for item in results if item["provider_request_status"] != "REQUEST_PERFORMED_READ_ONLY"]
    no_dividend = [item for item in results if item["dividend_provider_evidence_status"] == NO_DIVIDEND_EVENTS_RETURNED_BY_PROVIDER]
    collected = [item for item in results if item["dividend_provider_evidence_status"] == DIVIDEND_EVIDENCE_COLLECTED_READ_ONLY]
    return {
        "target_count": len(TARGET_UNIVERSE),
        "provider_request_count": len(results),
        "successful_provider_response_count": len(successful),
        "failed_provider_response_count": len(failed),
        "dividend_evidence_collected_count": len(collected),
        "no_dividend_events_returned_count": len(no_dividend),
        "not_evaluated_count": sum(1 for item in results if item["not_evaluated_fields"]),
        "generated_output_count": len(OUTPUT_FILENAMES),
        "failure_count": len(failed),
        "warning_count": sum(1 for item in results if item["not_evaluated_fields"]),
    }


def _output_payloads(*, artifact_seed: dict[str, Any], results: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    base = _base_output_fields()
    summary = artifact_seed["execution_summary"]
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
    absences = [
        {
            "ticker": item["ticker"],
            "dividend_absence_policy_status": item["dividend_absence_policy_status"],
            "dividend_event_count": item["dividend_event_count"],
        }
        for item in results
        if item["dividend_provider_evidence_status"] == NO_DIVIDEND_EVENTS_RETURNED_BY_PROVIDER
    ]
    failures = [
        {
            "ticker": item["ticker"],
            "failure_reason_if_any": item["failure_reason_if_any"],
            "provider_request_status": item["provider_request_status"],
        }
        for item in results
        if item["failure_reason_if_any"]
    ]
    reconciliation = [
        {
            "ticker": item["ticker"],
            "dividend_policy_reconciliation_status": item["dividend_policy_reconciliation_status"],
            "cash_dividend_adjustment_policy": "REQUIRES_OPERATOR_REVIEW",
            "total_return_assumption": "NOT_ASSUMED",
            "authority_created": False,
        }
        for item in results
    ]
    return {
        OUTPUT_FILENAMES[0]: base | {
            "artifact_kind": artifact_seed["artifact_kind"],
            "execution_status": artifact_seed["execution_status"],
            "run_timestamp_utc": artifact_seed["run_timestamp_utc"],
            "selected_endpoint": artifact_seed["selected_endpoint"],
            "selected_endpoint_mode": artifact_seed["selected_endpoint_mode"],
            "target_universe": list(TARGET_UNIVERSE),
            "execution_summary": deepcopy(summary),
        },
        OUTPUT_FILENAMES[1]: base | {"request_receipts_sanitized": receipts},
        OUTPUT_FILENAMES[2]: base | {"per_ticker_dividend_evidence_results": deepcopy(results)},
        OUTPUT_FILENAMES[3]: base | {"dividend_event_absence_inventory": absences},
        OUTPUT_FILENAMES[4]: base | {"dividend_policy_reconciliation_report": reconciliation},
        OUTPUT_FILENAMES[5]: base | {"dividend_event_failure_reason_inventory": failures},
        OUTPUT_FILENAMES[6]: base | {
            "operator_review_required": True,
            "next_task": "DIVIDEND_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE",
            "execution_summary": deepcopy(summary),
            "authority_boundary": {
                "dividend_event_authority_created": False,
                "dividend_event_authority_frozen": False,
                "split_event_authority_created": True,
                "split_event_authority_frozen": True,
                "corporate_action_authority_created": False,
                "new_ticker_acquisition_authorized": False,
                "dataset_generation_authorized": False,
                "runtime_use": NOT_AUTHORIZED,
                "broker_execution": NOT_AUTHORIZED,
            },
        },
    }


def _write_outputs(output_root: Path, payloads: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    output_root.mkdir(parents=True, exist_ok=True)
    manifest: list[dict[str, Any]] = []
    for filename in OUTPUT_FILENAMES:
        path = output_root / filename
        data = canonical_json_bytes(payloads[filename])
        path.write_bytes(data)
        manifest.append(
            {
                "filename": filename,
                "relative_path": str(path.as_posix()),
                "sha256": sha256_bytes(data),
                "semantic_digest": semantic_digest(payloads[filename]),
                "output_label": RESEARCH_ONLY_NON_ACTIONABLE,
            }
        )
    return manifest


def _executed_artifact_seed(
    *,
    timestamp: str,
    end_date: str,
    selected_endpoint_mode: str,
    transport_mode: str,
    results: list[dict[str, Any]],
) -> dict[str, Any]:
    summary = _summary(results)
    return {
        "artifact_kind": ARTIFACT_KIND_DIVIDEND_PROVIDER_EVIDENCE_EXECUTED,
        "schema_version": SCHEMA_VERSION_DIVIDEND_PROVIDER_EVIDENCE_EXECUTED_V1,
        "execution_status": DIVIDEND_PROVIDER_EVIDENCE_EXECUTED_READ_ONLY,
        "evidence_scope": READ_ONLY_DIVIDEND_EVENT_EVIDENCE_REQUESTS_ONLY,
        "output_label": RESEARCH_ONLY_NON_ACTIONABLE,
        "run_timestamp_utc": timestamp,
        "dividend_history_start_date": DIVIDEND_HISTORY_START_DATE,
        "dividend_history_end_date": end_date,
        "selected_provider": provider_adapter.PROVIDER_NAME,
        "selected_endpoint": provider_adapter.MASSIVE_DIVIDEND_EVENTS_ENDPOINT,
        "selected_endpoint_stability": provider_adapter.MASSIVE_DIVIDEND_EVENTS_ENDPOINT_STABILITY,
        "selected_endpoint_mode": selected_endpoint_mode,
        "transport_mode": transport_mode,
        "created_offline": False,
        "dividend_provider_evidence_request_authorized": True,
        "ready_for_dividend_provider_evidence_execution": True,
        "provider_requests_made": True,
        "live_provider_transport_enabled": True,
        "dividend_provider_evidence_executed": True,
        "dividend_provider_evidence_results_created": True,
        "provider_requests_made_in_execution": True,
        "raw_provider_payloads_committed": False,
        "api_keys_stored_or_printed": False,
        "dividend_event_authority_candidate_created": True,
        "dividend_event_authority_review_created": True,
        "dividend_event_authority_created": False,
        "dividend_event_authority_frozen": False,
        "split_event_authority_candidate_created": True,
        "split_event_authority_review_created": True,
        "split_provider_evidence_request_authorized": True,
        "split_provider_evidence_executed": True,
        "split_provider_evidence_results_created": True,
        "split_event_authority_created": True,
        "split_event_authority_frozen": True,
        "split_event_authority_scope": split_freeze.SPLIT_EVENT_AUTHORITY_ONLY,
        "split_provider_evidence_rerun_performed": False,
        "corporate_action_authority_plan_approved": True,
        "corporate_action_authority_created": False,
        "new_ticker_acquisition_authorized": False,
        "dataset_generation_authorized": False,
        "acquisition_generation_authorized": False,
        "canonical_dataset_authorized": False,
        "registry_approval_created": False,
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
        "predictive_usefulness": _not_accepted(),
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
        "dividend_provider_evidence_request_approval_digest": (
            EXPECTED_DIVIDEND_PROVIDER_EVIDENCE_REQUEST_APPROVAL_DIGEST
        ),
        "dividend_event_authority_candidate_review_package_digest": (
            approval.EXPECTED_DIVIDEND_EVENT_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST
        ),
        "dividend_event_authority_candidate_digest": (
            approval.EXPECTED_DIVIDEND_EVENT_AUTHORITY_CANDIDATE_DIGEST
        ),
        "split_event_authority_freeze_digest": approval.EXPECTED_SPLIT_EVENT_AUTHORITY_FREEZE_DIGEST,
        "split_event_evidence_results_review_package_digest": (
            approval.EXPECTED_SPLIT_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST
        ),
        "split_provider_evidence_execution_digest": approval.EXPECTED_SPLIT_PROVIDER_EVIDENCE_EXECUTION_DIGEST,
        "split_provider_evidence_request_approval_digest": (
            approval.EXPECTED_SPLIT_PROVIDER_EVIDENCE_REQUEST_APPROVAL_DIGEST
        ),
        "corporate_action_authority_plan_approval_digest": (
            approval.EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_APPROVAL_DIGEST
        ),
        "post_identity_freeze_registry_inventory_approval_digest": (
            approval.EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_APPROVAL_DIGEST
        ),
        "identity_authority_freeze_digest": approval.EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST,
        "ticker_universe_selection_approval_digest": (
            approval.EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST
        ),
        "target_universe": list(TARGET_UNIVERSE),
        "target_universe_count": len(TARGET_UNIVERSE),
        "per_ticker_dividend_provider_evidence_results": results,
        "generated_output_count": len(OUTPUT_FILENAMES),
        "execution_summary": summary,
        "output_digest_manifest": [],
        "next_required_task": "DIVIDEND_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE",
    }


def _blocked_artifact(*, timestamp: str, reason: str) -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_DIVIDEND_PROVIDER_EVIDENCE_BLOCKED,
        "schema_version": SCHEMA_VERSION_DIVIDEND_PROVIDER_EVIDENCE_EXECUTED_V1,
        "execution_status": DIVIDEND_PROVIDER_EVIDENCE_BLOCKED_LIVE_GATE_OR_API_KEY_MISSING,
        "evidence_scope": READ_ONLY_DIVIDEND_EVENT_EVIDENCE_REQUESTS_ONLY,
        "output_label": RESEARCH_ONLY_NON_ACTIONABLE,
        "run_timestamp_utc": timestamp,
        "blocked_reason": reason,
        "required_live_gate": MARKETFLOW_ENABLE_LIVE_DIVIDEND_PROVIDER_EVIDENCE,
        "accepted_api_key_sources": ["explicit api_key argument", "MASSIVE_API_KEY", "POLYGON_API_KEY"],
        "provider_requests_made": False,
        "live_provider_transport_enabled": False,
        "dividend_provider_evidence_executed": False,
        "dividend_provider_evidence_results_created": False,
        "generated_output_count": 0,
        "dividend_provider_evidence_execution_digest": "NOT_CREATED",
        "dividend_provider_evidence_request_approval_digest": (
            EXPECTED_DIVIDEND_PROVIDER_EVIDENCE_REQUEST_APPROVAL_DIGEST
        ),
        "target_universe": list(TARGET_UNIVERSE),
        "target_universe_count": len(TARGET_UNIVERSE),
        "raw_provider_payloads_committed": False,
        "api_keys_stored_or_printed": False,
        "dividend_event_authority_created": False,
        "dividend_event_authority_frozen": False,
        "split_event_authority_created": True,
        "split_event_authority_frozen": True,
        "split_event_authority_scope": split_freeze.SPLIT_EVENT_AUTHORITY_ONLY,
        "split_provider_evidence_rerun_performed": False,
        "corporate_action_authority_created": False,
        "new_ticker_acquisition_authorized": False,
        "dataset_generation_authorized": False,
        "acquisition_generation_authorized": False,
        "canonical_dataset_authorized": False,
        "registry_approval_created": False,
        "additional_predictive_evidence_execution_authorized": False,
        "additional_predictive_evidence_executed": False,
        "predictive_usefulness": _not_accepted(),
        "profitability": acquisition.PROFITABILITY_NOT_ACCEPTED,
        "runtime_migration_approved": False,
        "runtime_migration_active": False,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "automatic_stitching": False,
        "execution_summary": {
            "target_count": len(TARGET_UNIVERSE),
            "provider_request_count": 0,
            "successful_provider_response_count": 0,
            "failed_provider_response_count": 0,
            "dividend_evidence_collected_count": 0,
            "no_dividend_events_returned_count": 0,
            "not_evaluated_count": 0,
            "generated_output_count": 0,
            "failure_count": 1,
            "warning_count": 0,
        },
        "next_required_task": "ENVIRONMENT_OR_API_KEY_CORRECTION",
    }


def execute_dividend_provider_evidence_v1(
    *,
    api_key: str | None = None,
    transport: Callable[[Mapping[str, Any]], Any] | None = None,
    output_root: str | Path | None = None,
    run_timestamp_utc: str | None = None,
) -> dict[str, Any]:
    """Execute the approved read-only dividend evidence request or return a blocked artifact."""
    timestamp = run_timestamp_utc or _utc_now()
    end_date = _date_from_timestamp(timestamp)
    selected_endpoint_mode = provider_adapter.MASSIVE_DIVIDEND_EVENTS_ENDPOINT_STABILITY
    transport_mode = "INJECTED_TRANSPORT_READ_ONLY" if transport is not None else "LIVE_HTTP_TRANSPORT_READ_ONLY"
    if transport is None and os.environ.get(MARKETFLOW_ENABLE_LIVE_DIVIDEND_PROVIDER_EVIDENCE) != "1":
        return _blocked_artifact(timestamp=timestamp, reason="LIVE_GATE_MISSING")
    resolved_api_key = api_key or _api_key_from_environment()
    if resolved_api_key is None:
        return _blocked_artifact(timestamp=timestamp, reason="API_KEY_MISSING")

    results: list[dict[str, Any]] = []
    for ticker in TARGET_UNIVERSE:
        try:
            raw = provider_adapter.fetch_massive_dividend_events_v1(
                ticker=ticker,
                start_date=DIVIDEND_HISTORY_START_DATE,
                end_date=end_date,
                api_key=resolved_api_key,
                transport=transport,
                request_timestamp_utc=timestamp,
            )
        except provider_adapter.DividendEventProviderAdapterError as exc:
            results.append(_unavailable_ticker_result(ticker, str(exc)))
        else:
            results.append(_ticker_result_from_raw(ticker, raw))

    root = Path(output_root) if output_root is not None else OUTPUT_ROOT
    artifact = _executed_artifact_seed(
        timestamp=timestamp,
        end_date=end_date,
        selected_endpoint_mode=selected_endpoint_mode,
        transport_mode=transport_mode,
        results=results,
    )
    artifact["output_digest_manifest"] = _write_outputs(root, _output_payloads(artifact_seed=artifact, results=results))
    artifact["dividend_provider_evidence_execution_digest"] = dividend_provider_evidence_execution_digest_v1(artifact)
    validate_dividend_provider_evidence_executed_v1(artifact)
    return artifact


def _check(check_id: str, expected: Any, actual: Any) -> dict[str, Any]:
    status = PASS if actual == expected else FAIL
    return {
        "check_id": check_id,
        "status": status,
        "expected": expected,
        "actual": actual,
        "severity": BLOCKER,
    }


def _expect(actual: Any, expected: Any, field_name: str) -> None:
    if actual != expected:
        raise DividendProviderEvidenceExecutionError(f"{field_name} mismatch")


def _expect_true(actual: Any, field_name: str) -> None:
    if actual is not True:
        raise DividendProviderEvidenceExecutionError(f"{field_name} must be true")


def _expect_false(actual: Any, field_name: str) -> None:
    if actual is not False:
        raise DividendProviderEvidenceExecutionError(f"{field_name} must be false")


def _expect_digest(actual: Any, field_name: str) -> None:
    if not isinstance(actual, str) or len(actual) != 64:
        raise DividendProviderEvidenceExecutionError(f"{field_name} missing")


def _validate_outputs(artifact: dict[str, Any]) -> None:
    manifest = artifact.get("output_digest_manifest")
    if not isinstance(manifest, list) or len(manifest) != len(OUTPUT_FILENAMES):
        raise DividendProviderEvidenceExecutionError("output_digest_manifest mismatch")
    _expect([item.get("filename") for item in manifest], OUTPUT_FILENAMES, "output_digest_manifest filenames")
    for item in manifest:
        _expect(item.get("output_label"), RESEARCH_ONLY_NON_ACTIONABLE, "output label")
        _expect_digest(item.get("sha256"), "output sha256")
        _expect_digest(item.get("semantic_digest"), "output semantic_digest")


def _validate_per_ticker_results(artifact: dict[str, Any]) -> None:
    entries = artifact.get("per_ticker_dividend_provider_evidence_results")
    if not isinstance(entries, list) or len(entries) != len(TARGET_UNIVERSE):
        raise DividendProviderEvidenceExecutionError("per-ticker dividend evidence results mismatch")
    _expect([entry.get("ticker") for entry in entries], TARGET_UNIVERSE, "per-ticker tickers")
    allowed_statuses = {
        DIVIDEND_EVIDENCE_COLLECTED_READ_ONLY,
        NO_DIVIDEND_EVENTS_RETURNED_BY_PROVIDER,
        DIVIDEND_EVIDENCE_PROVIDER_RESPONSE_UNAVAILABLE,
        DIVIDEND_EVIDENCE_NOT_EVALUATED_BY_SELECTED_ENDPOINT,
    }
    for entry in entries:
        if entry.get("dividend_provider_evidence_status") not in allowed_statuses:
            raise DividendProviderEvidenceExecutionError("dividend_provider_evidence_status mismatch")
        _expect_false(entry.get("raw_response_stored"), "raw_response_stored")
        _expect_false(entry.get("raw_payload_committed"), "raw_payload_committed")
        _expect_false(entry.get("api_key_stored_or_printed"), "api_key_stored_or_printed")
        _expect(entry.get("dividend_event_authority_status"), NOT_CREATED, "dividend_event_authority_status")
        _expect(entry.get("dividend_event_freeze_status"), NOT_FROZEN, "dividend_event_freeze_status")
        _expect(entry.get("split_event_authority_status"), "FROZEN", "split_event_authority_status")
        for field in ("corporate_action_authority_created", "acquisition_authorized", "dataset_generation_authorized"):
            _expect_false(entry.get(field), field)
        for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
            _expect(entry.get(field), NOT_AUTHORIZED, field)
        _expect_digest(entry.get("sanitized_dividend_evidence_digest"), "sanitized_dividend_evidence_digest")
        if entry.get("provider_response_digest") is not None:
            _expect_digest(entry.get("provider_response_digest"), "provider_response_digest")


def _execution_checklist(artifact: dict[str, Any]) -> list[dict[str, Any]]:
    summary = artifact.get("execution_summary", {})
    return [
        _check("artifact_kind_executed", ARTIFACT_KIND_DIVIDEND_PROVIDER_EVIDENCE_EXECUTED, artifact.get("artifact_kind")),
        _check("execution_status_read_only", DIVIDEND_PROVIDER_EVIDENCE_EXECUTED_READ_ONLY, artifact.get("execution_status")),
        _check("dividend_request_authorized_true", True, artifact.get("dividend_provider_evidence_request_authorized")),
        _check("provider_requests_made_true", True, artifact.get("provider_requests_made")),
        _check("live_provider_transport_enabled_true", True, artifact.get("live_provider_transport_enabled")),
        _check("dividend_evidence_executed_true", True, artifact.get("dividend_provider_evidence_executed")),
        _check("dividend_evidence_results_created_true", True, artifact.get("dividend_provider_evidence_results_created")),
        _check("raw_payloads_not_committed", False, artifact.get("raw_provider_payloads_committed")),
        _check("api_keys_not_stored_or_printed", False, artifact.get("api_keys_stored_or_printed")),
        _check("target_universe_count_12", 12, artifact.get("target_universe_count")),
        _check("target_universe_matches", TARGET_UNIVERSE, artifact.get("target_universe")),
        _check("generated_output_count_7", 7, artifact.get("generated_output_count")),
        _check("summary_generated_output_count_7", 7, summary.get("generated_output_count")),
        _check("dividend_authority_not_created", False, artifact.get("dividend_event_authority_created")),
        _check("dividend_authority_not_frozen", False, artifact.get("dividend_event_authority_frozen")),
        _check("split_authority_created", True, artifact.get("split_event_authority_created")),
        _check("split_authority_frozen", True, artifact.get("split_event_authority_frozen")),
        _check("split_provider_evidence_not_rerun", False, artifact.get("split_provider_evidence_rerun_performed")),
        _check("corporate_action_authority_not_created", False, artifact.get("corporate_action_authority_created")),
        _check("acquisition_not_authorized", False, artifact.get("new_ticker_acquisition_authorized")),
        _check("dataset_generation_not_authorized", False, artifact.get("dataset_generation_authorized")),
        _check("additional_predictive_evidence_not_authorized", False, artifact.get("additional_predictive_evidence_execution_authorized")),
        _check("predictive_usefulness_not_accepted", _not_accepted(), artifact.get("predictive_usefulness")),
        _check("profitability_not_accepted", acquisition.PROFITABILITY_NOT_ACCEPTED, artifact.get("profitability")),
        _check("runtime_migration_not_approved", False, artifact.get("runtime_migration_approved")),
        _check("runtime_use_not_authorized", NOT_AUTHORIZED, artifact.get("runtime_use")),
        _check("strategy_use_not_authorized", NOT_AUTHORIZED, artifact.get("strategy_use")),
        _check("paper_trading_not_authorized", NOT_AUTHORIZED, artifact.get("paper_trading")),
        _check("broker_execution_not_authorized", NOT_AUTHORIZED, artifact.get("broker_execution")),
        _check("automatic_stitching_false", False, artifact.get("automatic_stitching")),
    ]


def validate_dividend_provider_evidence_executed_v1(artifact: dict[str, Any]) -> dict[str, Any]:
    """Validate a performed dividend provider evidence execution artifact."""
    if not isinstance(artifact, dict):
        raise DividendProviderEvidenceExecutionError("artifact must be a JSON object")
    _expect(artifact.get("artifact_kind"), ARTIFACT_KIND_DIVIDEND_PROVIDER_EVIDENCE_EXECUTED, "artifact_kind")
    _expect(artifact.get("schema_version"), SCHEMA_VERSION_DIVIDEND_PROVIDER_EVIDENCE_EXECUTED_V1, "schema_version")
    _expect(artifact.get("execution_status"), DIVIDEND_PROVIDER_EVIDENCE_EXECUTED_READ_ONLY, "execution_status")
    for field in (
        "dividend_provider_evidence_request_authorized",
        "ready_for_dividend_provider_evidence_execution",
        "provider_requests_made",
        "live_provider_transport_enabled",
        "dividend_provider_evidence_executed",
        "dividend_provider_evidence_results_created",
        "provider_requests_made_in_execution",
        "dividend_event_authority_candidate_created",
        "dividend_event_authority_review_created",
        "split_event_authority_candidate_created",
        "split_event_authority_review_created",
        "split_provider_evidence_request_authorized",
        "split_provider_evidence_executed",
        "split_provider_evidence_results_created",
        "split_event_authority_created",
        "split_event_authority_frozen",
        "corporate_action_authority_plan_approved",
        "research_only",
    ):
        _expect_true(artifact.get(field), field)
    for field in (
        "raw_provider_payloads_committed",
        "api_keys_stored_or_printed",
        "dividend_event_authority_created",
        "dividend_event_authority_frozen",
        "split_provider_evidence_rerun_performed",
        "corporate_action_authority_created",
        "new_ticker_acquisition_authorized",
        "dataset_generation_authorized",
        "acquisition_generation_authorized",
        "canonical_dataset_authorized",
        "registry_approval_created",
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
    for field, expected in {
        "evidence_scope": READ_ONLY_DIVIDEND_EVENT_EVIDENCE_REQUESTS_ONLY,
        "output_label": RESEARCH_ONLY_NON_ACTIONABLE,
        "dividend_provider_evidence_request_approval_digest": EXPECTED_DIVIDEND_PROVIDER_EVIDENCE_REQUEST_APPROVAL_DIGEST,
        "dividend_event_authority_candidate_review_package_digest": approval.EXPECTED_DIVIDEND_EVENT_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "dividend_event_authority_candidate_digest": approval.EXPECTED_DIVIDEND_EVENT_AUTHORITY_CANDIDATE_DIGEST,
        "split_event_authority_freeze_digest": approval.EXPECTED_SPLIT_EVENT_AUTHORITY_FREEZE_DIGEST,
        "split_event_evidence_results_review_package_digest": approval.EXPECTED_SPLIT_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST,
        "split_provider_evidence_execution_digest": approval.EXPECTED_SPLIT_PROVIDER_EVIDENCE_EXECUTION_DIGEST,
        "split_event_authority_scope": split_freeze.SPLIT_EVENT_AUTHORITY_ONLY,
        "corporate_action_authority_plan_approval_digest": approval.EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_APPROVAL_DIGEST,
        "post_identity_freeze_registry_inventory_approval_digest": approval.EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_APPROVAL_DIGEST,
        "identity_authority_freeze_digest": approval.EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST,
        "ticker_universe_selection_approval_digest": approval.EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST,
        "target_universe": TARGET_UNIVERSE,
        "target_universe_count": 12,
        "generated_output_count": 7,
        "predictive_usefulness": _not_accepted(),
        "profitability": acquisition.PROFITABILITY_NOT_ACCEPTED,
    }.items():
        _expect(artifact.get(field), expected, field)
    _validate_per_ticker_results(artifact)
    _validate_outputs(artifact)
    digest = artifact.get("dividend_provider_evidence_execution_digest")
    _expect_digest(digest, "dividend_provider_evidence_execution_digest")
    _expect(digest, dividend_provider_evidence_execution_digest_v1(artifact), "dividend_provider_evidence_execution_digest")
    checklist = _execution_checklist(artifact)
    failed = [item for item in checklist if item["status"] != PASS]
    if failed:
        raise DividendProviderEvidenceExecutionError(f"execution checklist failed: {failed[0]['check_id']}")
    summary = artifact["execution_summary"]
    return {
        "status": "DIVIDEND_PROVIDER_EVIDENCE_EXECUTED_VALID",
        "artifact_kind": artifact["artifact_kind"],
        "execution_status": artifact["execution_status"],
        "dividend_provider_evidence_execution_digest": digest,
        "dividend_provider_evidence_request_approval_digest": artifact["dividend_provider_evidence_request_approval_digest"],
        "selected_endpoint": artifact["selected_endpoint"],
        "selected_endpoint_mode": artifact["selected_endpoint_mode"],
        "target_universe": list(artifact["target_universe"]),
        "provider_request_count": summary["provider_request_count"],
        "successful_provider_response_count": summary["successful_provider_response_count"],
        "failed_provider_response_count": summary["failed_provider_response_count"],
        "dividend_evidence_collected_count": summary["dividend_evidence_collected_count"],
        "no_dividend_events_returned_count": summary["no_dividend_events_returned_count"],
        "generated_output_count": summary["generated_output_count"],
        "failure_count": summary["failure_count"],
        "warning_count": summary["warning_count"],
        "total_checks": len(checklist),
        "passed_checks": len(checklist),
        "failed_checks": 0,
        "blocker_count": 0,
    }


def build_dividend_provider_evidence_execution_status_markdown_v1(artifact: dict[str, Any]) -> str:
    """Render a sanitized status document for dividend provider evidence execution."""
    blocked = artifact.get("artifact_kind") == ARTIFACT_KIND_DIVIDEND_PROVIDER_EVIDENCE_BLOCKED
    validation = None if blocked else validate_dividend_provider_evidence_executed_v1(artifact)
    summary = artifact["execution_summary"]
    per_ticker = artifact.get("per_ticker_dividend_provider_evidence_results", [])
    lines = [
        "# MarketFlow Dividend Provider Evidence Execution Status",
        "",
        "## Title",
        "- Dividend Provider Evidence Execution v1.",
        "",
        "## Dividend Provider Evidence Execution",
        f"- Artifact kind: `{artifact['artifact_kind']}`",
        f"- Execution status: `{artifact['execution_status']}`",
        f"- Execution digest: `{artifact.get('dividend_provider_evidence_execution_digest', 'NOT_CREATED')}`",
        f"- Evidence scope: `{artifact['evidence_scope']}`",
        f"- Output label: `{artifact['output_label']}`",
        "",
        "## Source Dividend Provider Evidence Request Approval",
        f"- Approval digest: `{artifact['dividend_provider_evidence_request_approval_digest']}`",
        "",
        "## Source Split Authority Freeze",
        f"- Split freeze digest: `{artifact.get('split_event_authority_freeze_digest', approval.EXPECTED_SPLIT_EVENT_AUTHORITY_FREEZE_DIGEST)}`",
        f"- Split authority scope: `{artifact.get('split_event_authority_scope', split_freeze.SPLIT_EVENT_AUTHORITY_ONLY)}`",
        "",
        "## Target Universe",
        f"- Target universe count: `{artifact['target_universe_count']}`",
        "- Target universe: " + ", ".join(f"`{ticker}`" for ticker in artifact["target_universe"]),
        "",
        "## Provider Request Summary",
        f"- Selected provider: `{artifact.get('selected_provider', provider_adapter.PROVIDER_NAME)}`",
        f"- Selected endpoint: `{artifact.get('selected_endpoint', provider_adapter.MASSIVE_DIVIDEND_EVENTS_ENDPOINT)}`",
        f"- Selected endpoint mode: `{artifact.get('selected_endpoint_mode', provider_adapter.MASSIVE_DIVIDEND_EVENTS_ENDPOINT_STABILITY)}`",
        f"- Provider request count: `{summary['provider_request_count']}`",
        f"- Successful provider response count: `{summary['successful_provider_response_count']}`",
        f"- Failed provider response count: `{summary['failed_provider_response_count']}`",
        f"- Generated output root: `{OUTPUT_ROOT.as_posix()}`",
        f"- Generated output count: `{summary['generated_output_count']}`",
        f"- Failure count: `{summary['failure_count']}`",
        f"- Warning count: `{summary['warning_count']}`",
        "",
        "## Per-Ticker Dividend Evidence Summary",
    ]
    if per_ticker:
        lines.extend(
            f"- `{item['ticker']}`: `{item['dividend_provider_evidence_status']}`, events `{item['dividend_event_count']}`, response digest `{item['provider_response_digest']}`"
            for item in per_ticker
        )
    else:
        lines.append("- No provider requests were made; no per-ticker provider evidence exists.")
    lines.extend(["", "## Output Digest Manifest"])
    if blocked:
        lines.append("- No generated outputs were created because the live gate/API key requirement was not satisfied.")
    else:
        lines.extend(f"- `{item['filename']}`: `{item['sha256']}`" for item in artifact["output_digest_manifest"])
    lines.extend(
        [
            "",
            "## Dividend Absence Policy Summary",
            "- A provider response with zero dividend rows is recorded as `NO_DIVIDEND_EVENTS_RETURNED_BY_PROVIDER`.",
            "- A no-dividend response is read-only evidence for review; it is not dividend authority.",
            "- Unsupported endpoint fields are recorded as `NOT_EVALUATED_BY_SELECTED_ENDPOINT`.",
            "",
            "## Dividend Policy Reconciliation Summary",
            "- Dividend adjustment and total-return policy remain operator-review items.",
            "- Dividend evidence results do not create dividend authority.",
            "",
            "## API Key and Raw Payload Boundary",
            f"- raw_provider_payloads_committed: `{artifact['raw_provider_payloads_committed']}`",
            f"- api_keys_stored_or_printed: `{artifact['api_keys_stored_or_printed']}`",
            "- API key values are never printed, stored, or written to generated artifacts.",
            "- Raw provider payloads are not committed.",
            "",
            "## Dividend Authority Boundary",
            f"- dividend_event_authority_created: `{artifact['dividend_event_authority_created']}`",
            f"- dividend_event_authority_frozen: `{artifact['dividend_event_authority_frozen']}`",
            "",
            "## Split Authority Boundary",
            f"- split_event_authority_created: `{artifact['split_event_authority_created']}`",
            f"- split_event_authority_frozen: `{artifact['split_event_authority_frozen']}`",
            f"- split_provider_evidence_rerun_performed: `{artifact['split_provider_evidence_rerun_performed']}`",
            "",
            "## Corporate-Action Authority Boundary",
            f"- corporate_action_authority_created: `{artifact['corporate_action_authority_created']}`",
            "",
            "## Acquisition Boundary",
            f"- new_ticker_acquisition_authorized: `{artifact['new_ticker_acquisition_authorized']}`",
            f"- acquisition_generation_authorized: `{artifact['acquisition_generation_authorized']}`",
            "",
            "## Dataset Boundary",
            f"- dataset_generation_authorized: `{artifact['dataset_generation_authorized']}`",
            f"- canonical_dataset_authorized: `{artifact['canonical_dataset_authorized']}`",
            "",
            "## Predictive/Profitability Boundary",
            f"- additional_predictive_evidence_execution_authorized: `{artifact['additional_predictive_evidence_execution_authorized']}`",
            f"- predictive_usefulness: `{artifact['predictive_usefulness']}`",
            f"- profitability: `{artifact['profitability']}`",
            "",
            "## Runtime Boundary",
            f"- runtime_migration_approved: `{artifact['runtime_migration_approved']}`",
            f"- runtime_use: `{artifact['runtime_use']}`",
            f"- strategy_use: `{artifact['strategy_use']}`",
            f"- paper_trading: `{artifact['paper_trading']}`",
            f"- broker_execution: `{artifact['broker_execution']}`",
            "",
            "## Checklist Summary",
        ]
    )
    if validation is None:
        lines.extend(["- Executed-artifact validation was not run for the blocked artifact.", "- Blocker count: `1`"])
    else:
        lines.extend(
            [
                f"- Total checks: `{validation['total_checks']}`",
                f"- Passed checks: `{validation['passed_checks']}`",
                f"- Failed checks: `{validation['failed_checks']}`",
                f"- Blocker count: `{validation['blocker_count']}`",
            ]
        )
    lines.extend(
        [
            "",
            "## Guardrails",
            "- No dividend authority approval or freeze is created.",
            "- Split authority remains frozen and unchanged.",
            "- No corporate-action authority is created.",
            "- No acquisition or dataset generation authorization is created.",
            "- No predictive experiment rerun, strategy scoring, runtime activation, paper trading, broker execution, or trade recommendation is performed.",
            "",
            "## Non-Goals",
            "- No dividend authority or corporate-action authority creation.",
            "- No acquisition, dataset generation, predictive acceptance, profitability acceptance, or runtime activation.",
            "",
            "## Next Task",
            f"1. `{artifact['next_required_task']}`",
        ]
    )
    return "\n".join(lines) + "\n"
