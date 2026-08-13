"""Offline review package for acquisition provider evidence execution results."""

from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
from typing import Any, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import acquisition_provider_evidence_execution_service as execution


ARTIFACT_KIND_ACQUISITION_EVIDENCE_RESULTS_REVIEW_PACKAGE = (
    "ACQUISITION_EVIDENCE_RESULTS_REVIEW_PACKAGE"
)
SCHEMA_VERSION_ACQUISITION_EVIDENCE_RESULTS_REVIEW_V1 = (
    "acquisition_evidence_results_review_v1"
)
ACQUISITION_EVIDENCE_RESULTS_REVIEW_PACKAGE_READY = (
    "ACQUISITION_EVIDENCE_RESULTS_REVIEW_PACKAGE_READY"
)
ACQUISITION_EVIDENCE_RESULTS_REVIEW_BLOCKED_MISSING_OR_INVALID_OUTPUTS = (
    "ACQUISITION_EVIDENCE_RESULTS_REVIEW_BLOCKED_MISSING_OR_INVALID_OUTPUTS"
)

RESEARCH_ONLY_NON_ACTIONABLE = execution.RESEARCH_ONLY_NON_ACTIONABLE
READ_ONLY_HISTORICAL_MARKET_DATA_ACQUISITION_REQUESTS_ONLY = (
    execution.READ_ONLY_HISTORICAL_MARKET_DATA_ACQUISITION_REQUESTS_ONLY
)
NOT_AUTHORIZED = execution.NOT_AUTHORIZED
NOT_ACCEPTED = execution.NOT_ACCEPTED
PROFITABILITY_NOT_ACCEPTED = execution.PROFITABILITY_NOT_ACCEPTED
PASS = execution.PASS
FAIL = execution.FAIL
BLOCKER = execution.BLOCKER

EXPECTED_ACQUISITION_PROVIDER_EVIDENCE_EXECUTION_DIGEST = (
    "decc59a4a0ae91229ed527f9fcafd54e9d5af468d057d5200a67d2167939b02b"
)
EXPECTED_ACQUISITION_PROVIDER_EVIDENCE_REQUEST_APPROVAL_DIGEST = (
    execution.EXPECTED_ACQUISITION_PROVIDER_EVIDENCE_REQUEST_APPROVAL_DIGEST
)
EXPECTED_TARGET_UNIVERSE = list(execution.TARGET_UNIVERSE)
EXPECTED_OUTPUT_DIGESTS = {
    "acquisition_provider_evidence_run_manifest.json": "ad2de2a4493e7d0c7bd5d3bd62dce20b7a09b3c4dad1ab56008b468fddbfed07",
    "acquisition_provider_request_receipts_sanitized.json": "812677a5d378a5255c7e674ed416499e457bb69320dde8ab780ca07fdd547a66",
    "acquisition_evidence_results_sanitized.json": "51d970eedb72019c5d3fcffe1ccf10475a3480c9c9deb28b9a3d1e67442373fd",
    "acquisition_data_quality_summary.json": "147bbfbb96318a39b4c6b4ae4a865e593d4fa64369b7ac31ad8749af3af261c1",
    "acquisition_failure_reason_inventory.json": "98bbe551bc4bd1a1a7b6c9080f4967ab354652b8fe5c2f0d94a5152d2646978a",
    "acquisition_digest_manifest.json": "abbf00067830b06976c7f4bdf9396b6fe83f0edba306b7dc517994cae41270ed",
    "operator_review_summary.json": "c513a1ffb48ef8f124e4b466733f8fe2603d66887850b5f04cab9794f977e69b",
}
EXPECTED_OUTPUT_FILENAMES = list(execution.OUTPUT_FILENAMES)
EXPECTED_RESULT_FACTS = {
    "endpoint": "/v2/aggs/ticker/{stocksTicker}/range/1/day/{from}/{to}",
    "endpoint_mode": "CURRENT_STOCKS_V2_AGGS_RANGE_DAILY",
    "transport_mode": "LIVE_HTTP_TRANSPORT_READ_ONLY",
    "date_range_start": "2022-01-01",
    "date_range_end": "2025-12-31",
    "timeframe": "1d",
    "profile": "RTH_FULL_SESSION_1D",
    "target_count": 12,
    "provider_request_count": 12,
    "successful_provider_response_count": 12,
    "failed_provider_response_count": 0,
    "historical_bar_evidence_collected_count": 12,
    "no_historical_bars_returned_count": 0,
    "not_evaluated_count": 12,
    "generated_output_count": 7,
    "failure_count": 0,
    "warning_count": 12,
}
EXPECTED_PER_TICKER = {
    ticker: (execution.ACQUISITION_EVIDENCE_COLLECTED_READ_ONLY, 913 if ticker == "META" else 1003)
    for ticker in EXPECTED_TARGET_UNIVERSE
}

LIMITATIONS = [
    "acquisition_evidence_read_only_provider_snapshot_at_execution_time",
    "daily_aggregate_endpoint_does_not_evaluate_calendar_session_or_disaggregated_adjustment_checks",
    "meta_bar_count_differs_from_other_tickers_and_requires_future_review",
    "acquisition_authority_not_created",
    "acquisition_generation_not_authorized",
    "dataset_generation_not_authorized",
    "canonical_dataset_not_created",
    "registry_approval_not_created",
    "predictive_usefulness_not_accepted",
    "profitability_not_accepted",
    "runtime_not_authorized",
    "operator_approval_required_before_acquisition_generation_approval_or_freeze",
]
NEXT_GATES = [
    "acquisition_evidence_results_operator_review",
    "acquisition_data_quality_review_if_required",
    "acquisition_generation_approval_ceremony_if_required",
    "acquisition_generation_freeze_ceremony",
    "canonical_dataset_chain_candidate",
    "canonical_dataset_candidate_operator_review",
    "canonical_dataset_freeze",
    "research_registry_candidate",
    "research_registry_operator_review",
    "research_registry_approval",
    "additional_predictive_evidence_chain_if_required",
    "runtime_migration_chain_if_ever_authorized",
]
REQUIRED_CHECK_IDS = [
    "acquisition_provider_evidence_execution_digest_bound",
    "acquisition_provider_evidence_request_approval_digest_bound",
    "acquisition_chain_review_digest_bound",
    "acquisition_chain_candidate_digest_bound",
    "corporate_action_authority_approval_digest_bound",
    "target_universe_count_12",
    "target_universe_matches_execution_universe",
    "provider_request_count_12",
    "successful_provider_response_count_12",
    "failed_provider_response_count_zero",
    "historical_bar_evidence_collected_count_12",
    "no_historical_bars_returned_count_zero",
    "generated_output_count_7",
    "output_digests_bound",
    "outputs_research_only_non_actionable",
    "evidence_scope_read_only_historical_market_data_acquisition_only",
    "raw_provider_payloads_not_committed",
    "api_keys_not_stored_or_printed",
    "provider_requests_made_in_review_false",
    "live_provider_transport_enabled_in_review_false",
    "market_data_acquisition_performed_in_review_false",
    "acquisition_provider_evidence_rerun_performed_false",
    "new_ticker_acquisition_authorized_false",
    "acquisition_generation_authorized_false",
    "acquisition_generation_executed_false",
    "dataset_generation_authorized_false",
    "canonical_dataset_authorized_false",
    "canonical_dataset_candidate_created_false",
    "canonical_dataset_frozen_false",
    "registry_approval_created_false",
    "additional_predictive_evidence_execution_authorized_false",
    "additional_predictive_evidence_executed_false",
    "predictive_experiment_rerun_authorized_false",
    "feature_matrix_regeneration_performed_false",
    "new_strategy_scoring_performed_false",
    "trade_recommendations_generated_false",
    "predictive_usefulness_not_accepted",
    "profitability_not_accepted",
    "runtime_migration_approved_false",
    "runtime_use_not_authorized",
    "strategy_use_not_authorized",
    "paper_trading_not_authorized",
    "broker_execution_not_authorized",
    "automatic_stitching_false",
    "acquisition_evidence_supports_future_acquisition_generation_planning_true",
    "acquisition_evidence_creates_acquisition_authority_false",
    "acquisition_evidence_creates_dataset_generation_authority_false",
    "acquisition_evidence_creates_canonical_dataset_authority_false",
    "acquisition_evidence_creates_registry_approval_false",
    "meta_reduced_bar_count_recorded",
    "limitations_recorded",
    "next_gates_defined",
    "no_acquisition_authorization_artifact_created",
    "no_acquisition_generation_execution_created",
    "no_dataset_generation_authorization_created",
    "no_canonical_dataset_artifact_created",
    "no_registry_approval_created",
    "no_predictive_usefulness_acceptance_artifact_created",
    "no_profitability_acceptance_created",
    "no_runtime_migration_approval_created",
]


class AcquisitionEvidenceResultsReviewError(ValueError):
    """Raised when the acquisition evidence results review package is invalid."""


def _digest_payload(review_package: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(review_package)
    payload.pop("acquisition_evidence_results_review_package_digest", None)
    if "output_root" in payload:
        payload["output_root"] = execution.OUTPUT_ROOT.as_posix()
    return payload


def acquisition_evidence_results_review_package_digest_v1(review_package: dict[str, Any]) -> str:
    """Return a deterministic, output-location-independent package digest."""
    return semantic_digest(_digest_payload(review_package))


def _load_json_file(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise AcquisitionEvidenceResultsReviewError(f"{path.name} is not readable JSON") from exc
    if not isinstance(payload, dict):
        raise AcquisitionEvidenceResultsReviewError(f"{path.name} must contain a JSON object")
    return payload


def _contains_unredacted_sensitive_value(value: Any) -> bool:
    if isinstance(value, Mapping):
        for key, item in value.items():
            if str(key).lower() == "authorization" and item != "<redacted>":
                return True
            if _contains_unredacted_sensitive_value(item):
                return True
        return False
    if isinstance(value, list):
        return any(_contains_unredacted_sensitive_value(item) for item in value)
    if isinstance(value, str):
        lowered = value.lower()
        return any(token in lowered for token in ("bearer ", "apikey=", "api_key=", "access_token="))
    return False


def _forbidden_output_field(payload: Mapping[str, Any]) -> str | None:
    forbidden_true = {
        "new_ticker_acquisition_authorized",
        "acquisition_generation_authorized",
        "acquisition_generation_executed",
        "dataset_generation_authorized",
        "canonical_dataset_authorized",
        "canonical_dataset_candidate_created",
        "canonical_dataset_frozen",
        "registry_approval_created",
        "additional_predictive_evidence_execution_authorized",
        "raw_provider_payloads_committed",
        "raw_payload_committed",
        "raw_response_stored",
        "api_keys_stored_or_printed",
        "api_key_stored_or_printed",
    }
    forbidden_keys = {"provider_response_body", "raw_provider_payload", "raw_provider_payloads"}
    for key, value in payload.items():
        if key in forbidden_keys or (key in forbidden_true and value is True):
            return key
        if key in {"runtime_use", "strategy_use", "paper_trading", "broker_execution"} and value == "AUTHORIZED":
            return key
        if key in {"predictive_usefulness", "profitability"} and value == "accepted":
            return key
        if isinstance(value, Mapping):
            nested = _forbidden_output_field(value)
            if nested:
                return f"{key}.{nested}"
        elif isinstance(value, list):
            for index, item in enumerate(value):
                if isinstance(item, Mapping):
                    nested = _forbidden_output_field(item)
                    if nested:
                        return f"{key}[{index}].{nested}"
    return None


def _base_package() -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_ACQUISITION_EVIDENCE_RESULTS_REVIEW_PACKAGE,
        "schema_version": SCHEMA_VERSION_ACQUISITION_EVIDENCE_RESULTS_REVIEW_V1,
        "created_offline": True,
        "provider_requests_made_in_review": False,
        "live_provider_transport_enabled_in_review": False,
        "market_data_acquisition_performed_in_review": False,
        "acquisition_provider_evidence_rerun_performed": False,
        "raw_provider_payloads_committed": False,
        "api_keys_stored_or_printed": False,
        "source_execution_artifact_kind": execution.ARTIFACT_KIND_ACQUISITION_PROVIDER_EVIDENCE_EXECUTED,
        "source_execution_status": execution.ACQUISITION_PROVIDER_EVIDENCE_EXECUTED_READ_ONLY,
        "source_acquisition_provider_evidence_execution_digest": EXPECTED_ACQUISITION_PROVIDER_EVIDENCE_EXECUTION_DIGEST,
        "source_acquisition_provider_evidence_request_approval_digest": EXPECTED_ACQUISITION_PROVIDER_EVIDENCE_REQUEST_APPROVAL_DIGEST,
        "acquisition_provider_evidence_execution_digest": EXPECTED_ACQUISITION_PROVIDER_EVIDENCE_EXECUTION_DIGEST,
        "acquisition_provider_evidence_request_approval_digest": EXPECTED_ACQUISITION_PROVIDER_EVIDENCE_REQUEST_APPROVAL_DIGEST,
        "acquisition_provider_request_authorized": True,
        "ready_for_acquisition_provider_evidence_execution": True,
        "provider_requests_made": True,
        "live_provider_transport_enabled": True,
        "market_data_acquisition_performed": True,
        "acquisition_provider_evidence_executed": True,
        "acquisition_provider_evidence_results_created": True,
        "acquisition_evidence_results_review_created": True,
        "acquisition_evidence_results_review_ready": True,
        "acquisition_evidence_results_supports_future_acquisition_generation_planning": True,
        "ready_for_acquisition_generation_approval": True,
        "ready_for_acquisition_generation_freeze": False,
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
        "operator_review_required": True,
        "acquisition_generation_chain_candidate_review_package_digest": execution.EXPECTED_ACQUISITION_GENERATION_CHAIN_REVIEW_DIGEST,
        "acquisition_generation_chain_candidate_digest": execution.EXPECTED_ACQUISITION_GENERATION_CHAIN_CANDIDATE_DIGEST,
        "corporate_action_authority_approval_digest": execution.EXPECTED_CORPORATE_ACTION_AUTHORITY_APPROVAL_DIGEST,
        "combined_split_dividend_corporate_action_readiness_review_package_digest": execution.EXPECTED_COMBINED_READINESS_REVIEW_DIGEST,
        "split_event_authority_freeze_digest": execution.EXPECTED_SPLIT_EVENT_AUTHORITY_FREEZE_DIGEST,
        "dividend_event_authority_freeze_digest": execution.EXPECTED_DIVIDEND_EVENT_AUTHORITY_FREEZE_DIGEST,
        "identity_authority_freeze_digest": execution.EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST,
        "ticker_universe_selection_approval_digest": execution.EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST,
        "target_universe": list(EXPECTED_TARGET_UNIVERSE),
        "target_universe_count": 12,
        "endpoint": EXPECTED_RESULT_FACTS["endpoint"],
        "endpoint_mode": EXPECTED_RESULT_FACTS["endpoint_mode"],
        "transport_mode": EXPECTED_RESULT_FACTS["transport_mode"],
        "date_range_start": EXPECTED_RESULT_FACTS["date_range_start"],
        "date_range_end": EXPECTED_RESULT_FACTS["date_range_end"],
        "timeframe": EXPECTED_RESULT_FACTS["timeframe"],
        "profile": EXPECTED_RESULT_FACTS["profile"],
        "expected_output_digests": dict(EXPECTED_OUTPUT_DIGESTS),
        "limitations": list(LIMITATIONS),
        "next_gates": list(NEXT_GATES),
        "acquisition_evidence_results_available": True,
        "all_provider_requests_succeeded": True,
        "historical_bar_evidence_available_for_all_tickers": True,
        "acquisition_evidence_review_supports_future_acquisition_generation_planning": True,
        "acquisition_evidence_review_creates_acquisition_authority": False,
        "acquisition_evidence_review_creates_dataset_generation_authority": False,
        "acquisition_evidence_review_creates_canonical_dataset_authority": False,
        "acquisition_evidence_review_creates_registry_approval": False,
        "acquisition_evidence_review_creates_predictive_evidence_authority": False,
        "acquisition_evidence_review_creates_runtime_authority": False,
        "acquisition_authorization_artifact_created": False,
        "acquisition_generation_execution_created": False,
        "dataset_generation_authorization_created": False,
        "canonical_dataset_artifact_created": False,
        "registry_approval_artifact_created": False,
        "predictive_usefulness_acceptance_artifact_created": False,
        "profitability_acceptance_created": False,
        "runtime_migration_approval_created": False,
    }


def _summary(checklist: list[dict[str, Any]]) -> dict[str, Any]:
    failed = [row for row in checklist if row.get("status") != PASS]
    return {
        "total_checks": len(checklist),
        "passed_checks": len(checklist) - len(failed),
        "failed_checks": len(failed),
        "blocker_count": sum(1 for row in failed if row.get("severity") == BLOCKER),
        "ready_for_operator_review": not failed,
        "ready_for_acquisition_generation_approval": not failed,
        "ready_for_acquisition_generation_freeze": False,
        "ready_for_canonical_dataset_chain_candidate": False,
        "acquisition_authorized": False,
        "acquisition_generation_authorized": False,
        "acquisition_generation_executed": False,
        "dataset_generation_authorized": False,
        "canonical_dataset_authorized": False,
        "registry_approval_created": False,
        "additional_predictive_evidence_execution_authorized": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_migration_authorized": False,
        "software_runtime_activation_authorized": False,
    }


def _blocked_package(reason: str) -> dict[str, Any]:
    package = _base_package()
    package.update(
        {
            "review_status": ACQUISITION_EVIDENCE_RESULTS_REVIEW_BLOCKED_MISSING_OR_INVALID_OUTPUTS,
            "output_file_inspection_performed": False,
            "outputs_verified": False,
            "acquisition_evidence_results_review_ready": False,
            "acquisition_evidence_results_available": False,
            "all_provider_requests_succeeded": False,
            "historical_bar_evidence_available_for_all_tickers": False,
            "acquisition_evidence_results_supports_future_acquisition_generation_planning": False,
            "acquisition_evidence_review_supports_future_acquisition_generation_planning": False,
            "ready_for_acquisition_generation_approval": False,
            "blocked_reason": reason,
            "output_digest_manifest": [],
            "per_ticker_acquisition_evidence_summary": [],
            "review_checklist": [],
            "review_summary": _summary([]),
            "next_required_task": "RESTORE_OR_VERIFY_ACQUISITION_PROVIDER_EVIDENCE_OUTPUTS",
        }
    )
    package["acquisition_evidence_results_review_package_digest"] = (
        acquisition_evidence_results_review_package_digest_v1(package)
    )
    return package


def _verified_outputs(
    output_root: Path,
    *,
    expected_output_digests: Mapping[str, str],
) -> tuple[dict[str, dict[str, Any]], list[dict[str, Any]]]:
    if list(expected_output_digests) != EXPECTED_OUTPUT_FILENAMES:
        raise AcquisitionEvidenceResultsReviewError("expected output digest manifest mismatch")
    payloads: dict[str, dict[str, Any]] = {}
    manifest: list[dict[str, Any]] = []
    for filename in EXPECTED_OUTPUT_FILENAMES:
        path = output_root / filename
        if not path.is_file():
            raise AcquisitionEvidenceResultsReviewError(f"{filename} missing")
        data = path.read_bytes()
        digest = sha256_bytes(data)
        if digest != expected_output_digests[filename]:
            raise AcquisitionEvidenceResultsReviewError(f"{filename} digest mismatch")
        payload = _load_json_file(path)
        if payload.get("output_label") != RESEARCH_ONLY_NON_ACTIONABLE:
            raise AcquisitionEvidenceResultsReviewError(f"{filename} output_label mismatch")
        if payload.get("evidence_scope") != READ_ONLY_HISTORICAL_MARKET_DATA_ACQUISITION_REQUESTS_ONLY:
            raise AcquisitionEvidenceResultsReviewError(f"{filename} evidence_scope mismatch")
        if _contains_unredacted_sensitive_value(payload):
            raise AcquisitionEvidenceResultsReviewError(f"{filename} contains unredacted sensitive value")
        forbidden = _forbidden_output_field(payload)
        if forbidden:
            raise AcquisitionEvidenceResultsReviewError(f"{filename} forbidden field {forbidden}")
        payloads[filename] = payload
        manifest.append(
            {
                "filename": filename,
                "sha256": digest,
                "expected_sha256": expected_output_digests[filename],
                "semantic_digest": semantic_digest(payload),
                "output_label": payload["output_label"],
                "evidence_scope": payload["evidence_scope"],
                "verified": True,
            }
        )
    digest_rows = payloads["acquisition_digest_manifest.json"].get("output_digests")
    if not isinstance(digest_rows, list) or len(digest_rows) != 6:
        raise AcquisitionEvidenceResultsReviewError("acquisition_digest_manifest output_digests mismatch")
    expected_internal = {
        name: digest for name, digest in expected_output_digests.items()
        if name != "acquisition_digest_manifest.json"
    }
    actual_internal = {row.get("filename"): row.get("sha256") for row in digest_rows if isinstance(row, Mapping)}
    if actual_internal != expected_internal:
        raise AcquisitionEvidenceResultsReviewError("acquisition_digest_manifest digest binding mismatch")
    return payloads, manifest


def _per_ticker_summary(results_payload: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = results_payload.get("per_ticker_acquisition_evidence_results")
    if not isinstance(rows, list):
        raise AcquisitionEvidenceResultsReviewError("per_ticker_acquisition_evidence_results missing")
    return [
        {
            "ticker": row.get("ticker"),
            "acquisition_provider_evidence_status": row.get("acquisition_provider_evidence_status"),
            "historical_bar_count": row.get("historical_bar_count"),
            "date_range_start": row.get("date_range_start"),
            "date_range_end": row.get("date_range_end"),
            "coverage_status": row.get("coverage_status"),
            "ohlc_status": row.get("ohlc_status"),
            "volume_status": row.get("volume_status"),
            "calendar_alignment_status": row.get("calendar_alignment_status"),
            "session_filter_status": row.get("session_filter_status"),
            "adjustment_policy_status": row.get("adjustment_policy_status"),
            "not_evaluated_fields": deepcopy(row.get("not_evaluated_fields")),
            "provider_response_digest": row.get("provider_response_digest"),
            "sanitized_acquisition_evidence_digest": row.get("sanitized_acquisition_evidence_digest"),
        }
        for row in rows if isinstance(row, Mapping)
    ]


def build_acquisition_evidence_results_review_package_v1(
    *,
    output_root: str | Path | None = None,
    expected_output_digests: Mapping[str, str] | None = None,
) -> dict[str, Any]:
    """Build an offline review from verified sanitized acquisition outputs only."""
    root = Path(output_root) if output_root is not None else execution.OUTPUT_ROOT
    expected_digests = dict(expected_output_digests or EXPECTED_OUTPUT_DIGESTS)
    try:
        payloads, output_manifest = _verified_outputs(root, expected_output_digests=expected_digests)
        run_manifest = payloads["acquisition_provider_evidence_run_manifest.json"]
        results_payload = payloads["acquisition_evidence_results_sanitized.json"]
        quality_payload = payloads["acquisition_data_quality_summary.json"]
        failure_payload = payloads["acquisition_failure_reason_inventory.json"]
        summary = run_manifest.get("execution_summary")
        profile = run_manifest.get("acquisition_profile")
        quality_rows = quality_payload.get("acquisition_data_quality_summary")
        failure_rows = failure_payload.get("acquisition_failure_reason_inventory")
        if not isinstance(summary, dict) or not isinstance(profile, dict):
            raise AcquisitionEvidenceResultsReviewError("execution summary or acquisition profile missing")
        if not isinstance(quality_rows, list) or len(quality_rows) != 12:
            raise AcquisitionEvidenceResultsReviewError("acquisition data quality rows mismatch")
        if not isinstance(failure_rows, list):
            raise AcquisitionEvidenceResultsReviewError("acquisition failure inventory mismatch")
        per_ticker = _per_ticker_summary(results_payload)
        if len(per_ticker) != 12:
            raise AcquisitionEvidenceResultsReviewError("per-ticker acquisition evidence count mismatch")
    except AcquisitionEvidenceResultsReviewError as exc:
        return _blocked_package(str(exc))

    package = _base_package()
    package.update(
        {
            "review_status": ACQUISITION_EVIDENCE_RESULTS_REVIEW_PACKAGE_READY,
            "output_root": root.as_posix(),
            "output_file_inspection_performed": True,
            "outputs_verified": True,
            "provider_request_count": summary.get("provider_request_count"),
            "successful_provider_response_count": summary.get("successful_provider_response_count"),
            "failed_provider_response_count": summary.get("failed_provider_response_count"),
            "historical_bar_evidence_collected_count": summary.get("historical_bar_evidence_collected_count"),
            "no_historical_bars_returned_count": summary.get("no_historical_bars_returned_count"),
            "not_evaluated_count": summary.get("not_evaluated_count"),
            "generated_output_count": summary.get("generated_output_count"),
            "failure_count": summary.get("failure_count"),
            "warning_count": summary.get("warning_count"),
            "per_ticker_acquisition_evidence_summary": per_ticker,
            "output_digest_manifest": output_manifest,
            "expected_output_digests": expected_digests,
            "data_quality_summary": deepcopy(quality_rows),
            "reviewed_failure_inventory": deepcopy(failure_rows),
            "meta_reduced_bar_count_recorded": any(
                row["ticker"] == "META" and row["historical_bar_count"] == 913 for row in per_ticker
            ),
            "next_required_task": "ACQUISITION_EVIDENCE_RESULTS_OPERATOR_REVIEW",
        }
    )
    checklist = _review_checklist(package)
    package["review_checklist"] = checklist
    package["review_summary"] = _summary(checklist)
    package["acquisition_evidence_results_review_package_digest"] = (
        acquisition_evidence_results_review_package_digest_v1(package)
    )
    validate_acquisition_evidence_results_review_package_v1(package)
    return package


def _check(check_id: str, expected: Any, actual: Any) -> dict[str, Any]:
    status = PASS if actual == expected else FAIL
    return {
        "check_id": check_id,
        "status": status,
        "expected": expected,
        "actual": actual,
        "severity": BLOCKER,
        "message": "review evidence matches" if status == PASS else "review evidence mismatch",
    }


def _review_checklist(package: dict[str, Any]) -> list[dict[str, Any]]:
    manifest = package.get("output_digest_manifest", [])
    per_ticker = package.get("per_ticker_acquisition_evidence_summary", [])
    checks = [
        ("acquisition_provider_evidence_execution_digest_bound", EXPECTED_ACQUISITION_PROVIDER_EVIDENCE_EXECUTION_DIGEST, package.get("acquisition_provider_evidence_execution_digest")),
        ("acquisition_provider_evidence_request_approval_digest_bound", EXPECTED_ACQUISITION_PROVIDER_EVIDENCE_REQUEST_APPROVAL_DIGEST, package.get("acquisition_provider_evidence_request_approval_digest")),
        ("acquisition_chain_review_digest_bound", execution.EXPECTED_ACQUISITION_GENERATION_CHAIN_REVIEW_DIGEST, package.get("acquisition_generation_chain_candidate_review_package_digest")),
        ("acquisition_chain_candidate_digest_bound", execution.EXPECTED_ACQUISITION_GENERATION_CHAIN_CANDIDATE_DIGEST, package.get("acquisition_generation_chain_candidate_digest")),
        ("corporate_action_authority_approval_digest_bound", execution.EXPECTED_CORPORATE_ACTION_AUTHORITY_APPROVAL_DIGEST, package.get("corporate_action_authority_approval_digest")),
        ("target_universe_count_12", 12, package.get("target_universe_count")),
        ("target_universe_matches_execution_universe", EXPECTED_TARGET_UNIVERSE, package.get("target_universe")),
        ("provider_request_count_12", 12, package.get("provider_request_count")),
        ("successful_provider_response_count_12", 12, package.get("successful_provider_response_count")),
        ("failed_provider_response_count_zero", 0, package.get("failed_provider_response_count")),
        ("historical_bar_evidence_collected_count_12", 12, package.get("historical_bar_evidence_collected_count")),
        ("no_historical_bars_returned_count_zero", 0, package.get("no_historical_bars_returned_count")),
        ("generated_output_count_7", 7, package.get("generated_output_count")),
        ("output_digests_bound", EXPECTED_OUTPUT_FILENAMES, [row.get("filename") for row in manifest]),
        ("outputs_research_only_non_actionable", True, bool(manifest) and all(row.get("output_label") == RESEARCH_ONLY_NON_ACTIONABLE for row in manifest)),
        ("evidence_scope_read_only_historical_market_data_acquisition_only", True, bool(manifest) and all(row.get("evidence_scope") == READ_ONLY_HISTORICAL_MARKET_DATA_ACQUISITION_REQUESTS_ONLY for row in manifest)),
        ("raw_provider_payloads_not_committed", False, package.get("raw_provider_payloads_committed")),
        ("api_keys_not_stored_or_printed", False, package.get("api_keys_stored_or_printed")),
        ("provider_requests_made_in_review_false", False, package.get("provider_requests_made_in_review")),
        ("live_provider_transport_enabled_in_review_false", False, package.get("live_provider_transport_enabled_in_review")),
        ("market_data_acquisition_performed_in_review_false", False, package.get("market_data_acquisition_performed_in_review")),
        ("acquisition_provider_evidence_rerun_performed_false", False, package.get("acquisition_provider_evidence_rerun_performed")),
        ("new_ticker_acquisition_authorized_false", False, package.get("new_ticker_acquisition_authorized")),
        ("acquisition_generation_authorized_false", False, package.get("acquisition_generation_authorized")),
        ("acquisition_generation_executed_false", False, package.get("acquisition_generation_executed")),
        ("dataset_generation_authorized_false", False, package.get("dataset_generation_authorized")),
        ("canonical_dataset_authorized_false", False, package.get("canonical_dataset_authorized")),
        ("canonical_dataset_candidate_created_false", False, package.get("canonical_dataset_candidate_created")),
        ("canonical_dataset_frozen_false", False, package.get("canonical_dataset_frozen")),
        ("registry_approval_created_false", False, package.get("registry_approval_created")),
        ("additional_predictive_evidence_execution_authorized_false", False, package.get("additional_predictive_evidence_execution_authorized")),
        ("additional_predictive_evidence_executed_false", False, package.get("additional_predictive_evidence_executed")),
        ("predictive_experiment_rerun_authorized_false", False, package.get("predictive_experiment_rerun_authorized")),
        ("feature_matrix_regeneration_performed_false", False, package.get("feature_matrix_regeneration_performed")),
        ("new_strategy_scoring_performed_false", False, package.get("new_strategy_scoring_performed")),
        ("trade_recommendations_generated_false", False, package.get("trade_recommendations_generated")),
        ("predictive_usefulness_not_accepted", NOT_ACCEPTED, package.get("predictive_usefulness")),
        ("profitability_not_accepted", PROFITABILITY_NOT_ACCEPTED, package.get("profitability")),
        ("runtime_migration_approved_false", False, package.get("runtime_migration_approved")),
        ("runtime_use_not_authorized", NOT_AUTHORIZED, package.get("runtime_use")),
        ("strategy_use_not_authorized", NOT_AUTHORIZED, package.get("strategy_use")),
        ("paper_trading_not_authorized", NOT_AUTHORIZED, package.get("paper_trading")),
        ("broker_execution_not_authorized", NOT_AUTHORIZED, package.get("broker_execution")),
        ("automatic_stitching_false", False, package.get("automatic_stitching")),
        ("acquisition_evidence_supports_future_acquisition_generation_planning_true", True, package.get("acquisition_evidence_review_supports_future_acquisition_generation_planning")),
        ("acquisition_evidence_creates_acquisition_authority_false", False, package.get("acquisition_evidence_review_creates_acquisition_authority")),
        ("acquisition_evidence_creates_dataset_generation_authority_false", False, package.get("acquisition_evidence_review_creates_dataset_generation_authority")),
        ("acquisition_evidence_creates_canonical_dataset_authority_false", False, package.get("acquisition_evidence_review_creates_canonical_dataset_authority")),
        ("acquisition_evidence_creates_registry_approval_false", False, package.get("acquisition_evidence_review_creates_registry_approval")),
        ("meta_reduced_bar_count_recorded", True, package.get("meta_reduced_bar_count_recorded")),
        ("limitations_recorded", LIMITATIONS, package.get("limitations")),
        ("next_gates_defined", NEXT_GATES, package.get("next_gates")),
        ("no_acquisition_authorization_artifact_created", False, package.get("acquisition_authorization_artifact_created")),
        ("no_acquisition_generation_execution_created", False, package.get("acquisition_generation_execution_created")),
        ("no_dataset_generation_authorization_created", False, package.get("dataset_generation_authorization_created")),
        ("no_canonical_dataset_artifact_created", False, package.get("canonical_dataset_artifact_created")),
        ("no_registry_approval_created", False, package.get("registry_approval_artifact_created")),
        ("no_predictive_usefulness_acceptance_artifact_created", False, package.get("predictive_usefulness_acceptance_artifact_created")),
        ("no_profitability_acceptance_created", False, package.get("profitability_acceptance_created")),
        ("no_runtime_migration_approval_created", False, package.get("runtime_migration_approval_created")),
    ]
    return [_check(*row) for row in checks]


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise AcquisitionEvidenceResultsReviewError(f"{field} mismatch")


def _expect_true(actual: Any, field: str) -> None:
    if actual is not True:
        raise AcquisitionEvidenceResultsReviewError(f"{field} must be true")


def _expect_false(actual: Any, field: str) -> None:
    if actual is not False:
        raise AcquisitionEvidenceResultsReviewError(f"{field} must be false")


def _expect_digest(actual: Any, field: str) -> None:
    if not isinstance(actual, str) or len(actual) != 64:
        raise AcquisitionEvidenceResultsReviewError(f"{field} missing")


def validate_acquisition_evidence_results_review_package_v1(
    review_package: dict[str, Any],
) -> dict[str, Any]:
    """Validate source bindings, verified results, and every closed authority gate."""
    if not isinstance(review_package, dict):
        raise AcquisitionEvidenceResultsReviewError("review_package must be a JSON object")
    _expect(review_package.get("artifact_kind"), ARTIFACT_KIND_ACQUISITION_EVIDENCE_RESULTS_REVIEW_PACKAGE, "artifact_kind")
    _expect(review_package.get("schema_version"), SCHEMA_VERSION_ACQUISITION_EVIDENCE_RESULTS_REVIEW_V1, "schema_version")
    if review_package.get("review_status") == ACQUISITION_EVIDENCE_RESULTS_REVIEW_BLOCKED_MISSING_OR_INVALID_OUTPUTS:
        _expect_false(review_package.get("outputs_verified"), "outputs_verified")
        _expect_false(review_package.get("output_file_inspection_performed"), "output_file_inspection_performed")
        _expect_false(review_package.get("acquisition_evidence_results_review_ready"), "acquisition_evidence_results_review_ready")
        digest = review_package.get("acquisition_evidence_results_review_package_digest")
        _expect_digest(digest, "acquisition_evidence_results_review_package_digest")
        _expect(digest, acquisition_evidence_results_review_package_digest_v1(review_package), "acquisition_evidence_results_review_package_digest")
        return {"status": "ACQUISITION_EVIDENCE_RESULTS_REVIEW_BLOCKED_VALID", "review_status": review_package["review_status"]}
    _expect(review_package.get("review_status"), ACQUISITION_EVIDENCE_RESULTS_REVIEW_PACKAGE_READY, "review_status")
    for field in (
        "created_offline", "acquisition_provider_request_authorized",
        "ready_for_acquisition_provider_evidence_execution", "provider_requests_made",
        "live_provider_transport_enabled", "market_data_acquisition_performed",
        "acquisition_provider_evidence_executed", "acquisition_provider_evidence_results_created",
        "acquisition_evidence_results_review_created", "acquisition_evidence_results_review_ready",
        "acquisition_evidence_results_supports_future_acquisition_generation_planning",
        "ready_for_acquisition_generation_approval", "acquisition_generation_chain_candidate_created",
        "acquisition_generation_chain_candidate_review_created", "corporate_action_authority_created",
        "corporate_action_authority_approved", "split_event_authority_created",
        "split_event_authority_frozen", "dividend_event_authority_created",
        "dividend_event_authority_frozen", "identity_authority_created", "identity_authority_frozen",
        "research_only", "operator_review_required", "output_file_inspection_performed", "outputs_verified",
        "acquisition_evidence_results_available", "all_provider_requests_succeeded",
        "historical_bar_evidence_available_for_all_tickers",
        "acquisition_evidence_review_supports_future_acquisition_generation_planning",
        "meta_reduced_bar_count_recorded",
    ):
        _expect_true(review_package.get(field), field)
    for field in (
        "provider_requests_made_in_review", "live_provider_transport_enabled_in_review",
        "market_data_acquisition_performed_in_review", "acquisition_provider_evidence_rerun_performed",
        "raw_provider_payloads_committed", "api_keys_stored_or_printed",
        "ready_for_acquisition_generation_freeze", "new_ticker_acquisition_authorized",
        "acquisition_generation_authorized", "acquisition_generation_executed",
        "acquisition_generation_results_created", "acquisition_generation_frozen",
        "dataset_generation_authorized", "canonical_dataset_authorized",
        "canonical_dataset_candidate_created", "canonical_dataset_frozen", "registry_approval_created",
        "additional_predictive_evidence_execution_authorized", "additional_predictive_evidence_executed",
        "predictive_experiment_rerun_authorized", "predictive_experiment_rerun_performed",
        "feature_matrix_regeneration_performed", "new_strategy_scoring_performed",
        "trade_recommendations_generated", "runtime_migration_approved", "runtime_migration_active",
        "automatic_stitching", "acquisition_evidence_review_creates_acquisition_authority",
        "acquisition_evidence_review_creates_dataset_generation_authority",
        "acquisition_evidence_review_creates_canonical_dataset_authority",
        "acquisition_evidence_review_creates_registry_approval",
        "acquisition_evidence_review_creates_predictive_evidence_authority",
        "acquisition_evidence_review_creates_runtime_authority", "acquisition_authorization_artifact_created",
        "acquisition_generation_execution_created", "dataset_generation_authorization_created",
        "canonical_dataset_artifact_created", "registry_approval_artifact_created",
        "predictive_usefulness_acceptance_artifact_created", "profitability_acceptance_created",
        "runtime_migration_approval_created",
    ):
        _expect_false(review_package.get(field), field)
    expected = {
        "source_execution_artifact_kind": execution.ARTIFACT_KIND_ACQUISITION_PROVIDER_EVIDENCE_EXECUTED,
        "source_execution_status": execution.ACQUISITION_PROVIDER_EVIDENCE_EXECUTED_READ_ONLY,
        "source_acquisition_provider_evidence_execution_digest": EXPECTED_ACQUISITION_PROVIDER_EVIDENCE_EXECUTION_DIGEST,
        "source_acquisition_provider_evidence_request_approval_digest": EXPECTED_ACQUISITION_PROVIDER_EVIDENCE_REQUEST_APPROVAL_DIGEST,
        "acquisition_provider_evidence_execution_digest": EXPECTED_ACQUISITION_PROVIDER_EVIDENCE_EXECUTION_DIGEST,
        "acquisition_provider_evidence_request_approval_digest": EXPECTED_ACQUISITION_PROVIDER_EVIDENCE_REQUEST_APPROVAL_DIGEST,
        "acquisition_generation_chain_candidate_review_package_digest": execution.EXPECTED_ACQUISITION_GENERATION_CHAIN_REVIEW_DIGEST,
        "acquisition_generation_chain_candidate_digest": execution.EXPECTED_ACQUISITION_GENERATION_CHAIN_CANDIDATE_DIGEST,
        "corporate_action_authority_approval_digest": execution.EXPECTED_CORPORATE_ACTION_AUTHORITY_APPROVAL_DIGEST,
        "combined_split_dividend_corporate_action_readiness_review_package_digest": execution.EXPECTED_COMBINED_READINESS_REVIEW_DIGEST,
        "split_event_authority_freeze_digest": execution.EXPECTED_SPLIT_EVENT_AUTHORITY_FREEZE_DIGEST,
        "dividend_event_authority_freeze_digest": execution.EXPECTED_DIVIDEND_EVENT_AUTHORITY_FREEZE_DIGEST,
        "identity_authority_freeze_digest": execution.EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST,
        "ticker_universe_selection_approval_digest": execution.EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST,
        "target_universe": EXPECTED_TARGET_UNIVERSE,
        "target_universe_count": 12,
        "endpoint": EXPECTED_RESULT_FACTS["endpoint"],
        "endpoint_mode": EXPECTED_RESULT_FACTS["endpoint_mode"],
        "transport_mode": EXPECTED_RESULT_FACTS["transport_mode"],
        "date_range_start": EXPECTED_RESULT_FACTS["date_range_start"],
        "date_range_end": EXPECTED_RESULT_FACTS["date_range_end"],
        "timeframe": EXPECTED_RESULT_FACTS["timeframe"],
        "profile": EXPECTED_RESULT_FACTS["profile"],
        "provider_request_count": 12,
        "successful_provider_response_count": 12,
        "failed_provider_response_count": 0,
        "historical_bar_evidence_collected_count": 12,
        "no_historical_bars_returned_count": 0,
        "not_evaluated_count": 12,
        "generated_output_count": 7,
        "failure_count": 0,
        "warning_count": 12,
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": PROFITABILITY_NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "limitations": LIMITATIONS,
        "next_gates": NEXT_GATES,
    }
    for field, value in expected.items():
        _expect(review_package.get(field), value, field)
    manifest = review_package.get("output_digest_manifest")
    if not isinstance(manifest, list) or len(manifest) != 7:
        raise AcquisitionEvidenceResultsReviewError("output_digest_manifest mismatch")
    expected_digests = review_package.get("expected_output_digests")
    if not isinstance(expected_digests, dict) or list(expected_digests) != EXPECTED_OUTPUT_FILENAMES:
        raise AcquisitionEvidenceResultsReviewError("expected_output_digests mismatch")
    _expect({row.get("filename"): row.get("sha256") for row in manifest}, expected_digests, "output_digest_manifest")
    if any(row.get("output_label") != RESEARCH_ONLY_NON_ACTIONABLE for row in manifest):
        raise AcquisitionEvidenceResultsReviewError("output labels must be research-only")
    if any(row.get("evidence_scope") != READ_ONLY_HISTORICAL_MARKET_DATA_ACQUISITION_REQUESTS_ONLY for row in manifest):
        raise AcquisitionEvidenceResultsReviewError("output evidence_scope mismatch")
    per_ticker = review_package.get("per_ticker_acquisition_evidence_summary")
    if not isinstance(per_ticker, list) or len(per_ticker) != 12:
        raise AcquisitionEvidenceResultsReviewError("per_ticker_acquisition_evidence_summary mismatch")
    _expect([row.get("ticker") for row in per_ticker], EXPECTED_TARGET_UNIVERSE, "per_ticker tickers")
    _expect(
        {row.get("ticker"): (row.get("acquisition_provider_evidence_status"), row.get("historical_bar_count")) for row in per_ticker},
        EXPECTED_PER_TICKER,
        "per_ticker acquisition evidence",
    )
    checklist = review_package.get("review_checklist")
    if not isinstance(checklist, list):
        raise AcquisitionEvidenceResultsReviewError("review_checklist missing")
    _expect([row.get("check_id") for row in checklist], REQUIRED_CHECK_IDS, "review checklist check IDs")
    if any(row.get("status") != PASS for row in checklist):
        raise AcquisitionEvidenceResultsReviewError("review checklist failed")
    _expect(review_package.get("review_summary"), _summary(checklist), "review_summary")
    digest = review_package.get("acquisition_evidence_results_review_package_digest")
    _expect_digest(digest, "acquisition_evidence_results_review_package_digest")
    _expect(digest, acquisition_evidence_results_review_package_digest_v1(review_package), "acquisition_evidence_results_review_package_digest")
    return {
        "status": "ACQUISITION_EVIDENCE_RESULTS_REVIEW_PACKAGE_VALID",
        "artifact_kind": review_package["artifact_kind"],
        "review_status": review_package["review_status"],
        "acquisition_evidence_results_review_package_digest": digest,
        **{key: review_package[key] for key in (
            "provider_request_count", "successful_provider_response_count",
            "failed_provider_response_count", "historical_bar_evidence_collected_count",
            "generated_output_count", "failure_count", "warning_count",
        )},
        **{key: review_package["review_summary"][key] for key in (
            "total_checks", "passed_checks", "failed_checks", "blocker_count",
        )},
    }


def build_acquisition_evidence_results_review_markdown_v1(review_package: dict[str, Any]) -> str:
    """Render a sanitized Markdown view of a ready review package."""
    validation = validate_acquisition_evidence_results_review_package_v1(review_package)
    lines = [
        "# MarketFlow Acquisition Evidence Results Review Status", "",
        "## Title", "- Acquisition Evidence Results Review Package v1.", "",
        "## Reviewed Acquisition Provider Evidence Execution",
        f"- Review artifact/status: `{review_package['artifact_kind']}` / `{review_package['review_status']}`.",
        f"- Review package digest: `{validation['acquisition_evidence_results_review_package_digest']}`.",
        f"- Source execution digest: `{review_package['source_acquisition_provider_evidence_execution_digest']}`.", "",
        "## Source Evidence",
        f"- Request approval digest: `{review_package['acquisition_provider_evidence_request_approval_digest']}`.",
        f"- Acquisition chain review/candidate digests: `{review_package['acquisition_generation_chain_candidate_review_package_digest']}` / `{review_package['acquisition_generation_chain_candidate_digest']}`.",
        f"- Corporate-action authority approval digest: `{review_package['corporate_action_authority_approval_digest']}`.", "",
        "## Target Universe",
        f"- Target universe count: `{review_package['target_universe_count']}`.",
        "- Target universe: " + ", ".join(f"`{ticker}`" for ticker in review_package["target_universe"]) + ".", "",
        "## Acquisition Profile",
        f"- Date range: `{review_package['date_range_start']}` through `{review_package['date_range_end']}`.",
        f"- Timeframe/profile: `{review_package['timeframe']}` / `{review_package['profile']}`.", "",
        "## Provider Request Summary",
        f"- Endpoint/mode/transport: `{review_package['endpoint']}` / `{review_package['endpoint_mode']}` / `{review_package['transport_mode']}`.",
        f"- Requests/successes/failures: `{review_package['provider_request_count']} / {review_package['successful_provider_response_count']} / {review_package['failed_provider_response_count']}`.", "",
        "## Per-Ticker Acquisition Evidence Summary",
    ]
    lines.extend(
        f"- `{row['ticker']}`: `{row['acquisition_provider_evidence_status']}`, bars `{row['historical_bar_count']}`."
        for row in review_package["per_ticker_acquisition_evidence_summary"]
    )
    lines.extend(["", "## Output Digest Manifest"])
    lines.extend(f"- `{row['filename']}`: `{row['sha256']}`." for row in review_package["output_digest_manifest"])
    lines.extend([
        "", "## Data Quality Summary",
        f"- Historical evidence/no-bars/not-evaluated: `{review_package['historical_bar_evidence_collected_count']} / {review_package['no_historical_bars_returned_count']} / {review_package['not_evaluated_count']}`.",
        f"- Failures/warnings: `{review_package['failure_count']} / {review_package['warning_count']}`.",
        "- META has `913` bars while every other ticker has `1003`; this fact is preserved for future review.", "",
        "## Limitations", *[f"- `{item}`" for item in review_package["limitations"]], "",
        "## Next Gates", *[f"- `{item}`" for item in review_package["next_gates"]], "",
        "## Acquisition Boundary",
        "- Review supports future acquisition-generation planning but creates no acquisition authorization or execution.", "",
        "## Dataset Boundary", "- Dataset generation remains unauthorized.", "",
        "## Canonical Dataset Boundary", "- No canonical dataset candidate, authorization, or freeze was created.", "",
        "## Registry Boundary", "- No registry approval was created.", "",
        "## Predictive/Profitability Boundary", "- Predictive usefulness and profitability remain not accepted.", "",
        "## Runtime Boundary", f"- Runtime/strategy/paper/broker: `{review_package['runtime_use']} / {review_package['strategy_use']} / {review_package['paper_trading']} / {review_package['broker_execution']}`.", "",
        "## Checklist Summary", f"- Total/passed/failed/blockers: `{review_package['review_summary']['total_checks']} / {review_package['review_summary']['passed_checks']} / {review_package['review_summary']['failed_checks']} / {review_package['review_summary']['blocker_count']}`.", "",
        "## Guardrails",
        "- No provider request, live transport, market-data acquisition, or evidence rerun occurred in review.",
        "- No acquisition generation, dataset, canonical dataset, registry, predictive acceptance, profitability acceptance, runtime, or trading authority was created.",
    ])
    return "\n".join(lines) + "\n"


def write_acquisition_evidence_results_review_package_v1(
    output_dir: str | Path,
    *,
    output_root: str | Path | None = None,
    expected_output_digests: Mapping[str, str] | None = None,
) -> dict[str, Any]:
    """Write canonical review JSON without overwriting an existing artifact."""
    package = build_acquisition_evidence_results_review_package_v1(
        output_root=output_root,
        expected_output_digests=expected_output_digests,
    )
    validation = validate_acquisition_evidence_results_review_package_v1(package)
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "acquisition_evidence_results_review_package_v1.json"
    if path.exists():
        raise AcquisitionEvidenceResultsReviewError("acquisition evidence results review package output already exists")
    payload = canonical_json_bytes(package)
    path.write_bytes(payload)
    return {
        "path": str(path),
        "artifact_kind": package["artifact_kind"],
        "review_status": package["review_status"],
        "acquisition_evidence_results_review_package_digest": validation.get(
            "acquisition_evidence_results_review_package_digest"
        ),
        "payload_sha256": sha256_bytes(payload),
    }
