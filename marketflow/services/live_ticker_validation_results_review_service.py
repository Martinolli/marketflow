"""Offline results review for read-only live ticker validation outputs."""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import acquisition_generation_service as acquisition
from marketflow.services import live_ticker_validation_execution_service as execution
from marketflow.services import live_ticker_validation_provider_adapter_service as provider


ARTIFACT_KIND_LIVE_TICKER_VALIDATION_RESULTS_REVIEW_PACKAGE = (
    "LIVE_TICKER_VALIDATION_RESULTS_REVIEW_PACKAGE"
)
SCHEMA_VERSION_LIVE_TICKER_VALIDATION_RESULTS_REVIEW_V1 = (
    "live_ticker_validation_results_review_v1"
)
LIVE_TICKER_VALIDATION_RESULTS_REVIEW_PACKAGE_READY = (
    "LIVE_TICKER_VALIDATION_RESULTS_REVIEW_PACKAGE_READY"
)
LIVE_TICKER_VALIDATION_RESULTS_REVIEW_BLOCKED_MISSING_OUTPUTS = (
    "LIVE_TICKER_VALIDATION_RESULTS_REVIEW_BLOCKED_MISSING_OUTPUTS"
)

EXPECTED_SOURCE_EXECUTION_DIGEST = (
    "96cdb4e97ea6255ddd04bd578a893a28c7a689b5e6d8247f9a26c341226d1ace"
)
EXPECTED_SOURCE_EXECUTION_APPROVAL_DIGEST = (
    execution.EXPECTED_LIVE_TICKER_VALIDATION_APPROVAL_DIGEST
)
EXPECTED_SOURCE_CANDIDATE_DIGEST = execution.EXPECTED_LIVE_TICKER_VALIDATION_CANDIDATE_DIGEST
EXPECTED_SOURCE_CANDIDATE_REVIEW_PACKAGE_DIGEST = (
    execution.EXPECTED_LIVE_TICKER_VALIDATION_CANDIDATE_REVIEW_PACKAGE_DIGEST
)
EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST = (
    execution.EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST
)
EXPECTED_OUTPUT_COUNT = len(execution.GENERATED_OUTPUT_NAMES)
EXPECTED_OUTPUT_NAMES = list(execution.GENERATED_OUTPUT_NAMES)
DEFAULT_OUTPUT_ROOT = execution.DEFAULT_OUTPUT_ROOT
VALIDATION_TARGET_UNIVERSE = list(execution.VALIDATION_TARGET_UNIVERSE)
READ_ONLY_PROVIDER_TICKER_VALIDATION_ONLY = execution.READ_ONLY_PROVIDER_TICKER_VALIDATION_ONLY
RESEARCH_ONLY_NON_ACTIONABLE = execution.RESEARCH_ONLY_NON_ACTIONABLE
NOT_AUTHORIZED = execution.NOT_AUTHORIZED
NOT_EVALUATED_BY_SELECTED_ENDPOINT = execution.NOT_EVALUATED_BY_SELECTED_ENDPOINT
VALIDATED_READ_ONLY = execution.VALIDATED_READ_ONLY
PROVIDER_RESPONSE_AVAILABLE = execution.PROVIDER_RESPONSE_AVAILABLE
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

REQUIRED_LIMITATIONS = [
    "validation_endpoint_reference_details_only",
    "corporate_action_availability_not_evaluated_by_selected_endpoint",
    "historical_aggregate_availability_not_evaluated_by_selected_endpoint",
    "validation_is_provider_snapshot_at_execution_time",
    "no_identity_authority_created",
    "no_corporate_action_authority_created",
    "no_acquisition_authority_created",
    "no_dataset_authority_created",
    "operator_review_required_before_per_ticker_authority_chain",
]

NEXT_GATES = [
    "live_ticker_validation_results_operator_review",
    "per_ticker_identity_authority_candidate",
    "per_ticker_corporate_action_audit_candidate",
    "per_ticker_acquisition_generation_candidate",
    "per_ticker_canonical_dataset_candidate",
    "expanded_universe_research_registry_candidate",
    "additional_predictive_evidence_execution_candidate",
]

REQUIRED_CHECK_IDS = [
    "execution_digest_bound",
    "approval_digest_bound",
    "candidate_digest_bound",
    "candidate_review_digest_bound",
    "ticker_universe_approval_digest_bound",
    "endpoint_recorded",
    "validation_target_count_12",
    "provider_request_count_12",
    "successful_provider_response_count_12",
    "failed_provider_response_count_zero",
    "all_targets_validated_read_only",
    "not_evaluated_count_24",
    "generated_output_count_6",
    "output_digests_bound",
    "outputs_research_only_non_actionable",
    "validation_scope_read_only_provider_ticker_validation_only",
    "raw_provider_payloads_not_committed",
    "api_keys_not_stored_or_printed",
    "provider_requests_made_in_review_false",
    "live_validation_rerun_performed_false",
    "live_provider_transport_enabled_in_review_false",
    "new_ticker_authority_created_false",
    "new_ticker_acquisition_authorized_false",
    "dataset_generation_authorized_false",
    "additional_predictive_evidence_execution_authorized_false",
    "additional_predictive_evidence_executed_false",
    "predictive_experiment_rerun_authorized_false",
    "predictive_experiment_rerun_performed_false",
    "walk_forward_rerun_performed_false",
    "label_regeneration_performed_false",
    "feature_matrix_regeneration_performed_false",
    "new_strategy_scoring_performed_false",
    "trade_recommendations_generated_false",
    "predictive_usefulness_not_accepted",
    "predictive_usefulness_acceptance_ready_false",
    "predictive_usefulness_acceptance_recommended_false",
    "predictive_usefulness_acceptance_candidate_created_false",
    "profitability_not_accepted",
    "profitability_acceptance_ready_false",
    "profitability_acceptance_recommended_false",
    "runtime_migration_recommended_false",
    "runtime_migration_approved_false",
    "runtime_migration_active_false",
    "strategy_runtime_migration_false",
    "runtime_use_not_authorized",
    "strategy_use_not_authorized",
    "paper_trading_not_authorized",
    "broker_execution_not_authorized",
    "automatic_stitching_false",
    "validation_supports_future_authority_chain_planning_true",
    "validation_creates_new_ticker_authority_false",
    "validation_creates_acquisition_authority_false",
    "validation_creates_dataset_generation_authority_false",
    "validation_creates_predictive_evidence_authority_false",
    "limitations_recorded",
    "next_gates_defined",
    "no_new_ticker_authority_artifact_created",
    "no_acquisition_authorization_created",
    "no_dataset_generation_authorization_created",
    "no_predictive_usefulness_acceptance_artifact_created",
    "no_profitability_acceptance_created",
    "no_runtime_migration_approval_created",
]


class LiveTickerValidationResultsReviewError(ValueError):
    """Raised when the live ticker validation results review violates guardrails."""


def _check(
    check_id: str,
    expected: Any,
    actual: Any,
    *,
    severity: str = BLOCKER,
    message: str | None = None,
) -> dict[str, Any]:
    status = PASS if actual == expected else FAIL
    return {
        "check_id": check_id,
        "status": status,
        "expected": expected,
        "actual": actual,
        "severity": severity,
        "message": message or (f"{check_id} passed" if status == PASS else f"{check_id} failed"),
    }


def _expect(actual: Any, expected: Any, field_name: str) -> None:
    if actual != expected:
        raise LiveTickerValidationResultsReviewError(f"{field_name} mismatch")


def _expect_true(actual: Any, field_name: str) -> None:
    if actual is not True:
        raise LiveTickerValidationResultsReviewError(f"{field_name} must be true")


def _expect_false(actual: Any, field_name: str) -> None:
    if actual is not False:
        raise LiveTickerValidationResultsReviewError(f"{field_name} must be false")


def _resolve_output_root(output_root: str | Path | None) -> Path:
    return DEFAULT_OUTPUT_ROOT if output_root is None else Path(output_root)


def _path_text(path: Path) -> str:
    return str(path).replace("\\", "/")


def _load_json_file(path: Path) -> tuple[dict[str, Any] | None, str | None, int | None]:
    if not path.exists() or not path.is_file():
        return None, None, None
    payload = path.read_bytes()
    data = json.loads(payload.decode("utf-8"))
    if not isinstance(data, dict):
        raise LiveTickerValidationResultsReviewError("ticker validation output must be a JSON object")
    return data, sha256_bytes(payload), len(payload)


def _walk_items(value: Any):
    if isinstance(value, dict):
        for key, item in value.items():
            yield str(key), item
            yield from _walk_items(item)
    elif isinstance(value, list):
        for item in value:
            yield from _walk_items(item)


def _output_file_entries(output_root: Path) -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]]]:
    entries: list[dict[str, Any]] = []
    outputs: dict[str, dict[str, Any]] = {}
    for name in EXPECTED_OUTPUT_NAMES:
        path = output_root / name
        data, digest, byte_size = _load_json_file(path)
        exists = data is not None
        if data is not None:
            outputs[name] = data
        entries.append(
            {
                "name": name,
                "path": _path_text(path),
                "exists": exists,
                "file_sha256": digest,
                "file_byte_size": byte_size,
                "semantic_digest": semantic_digest(data) if data is not None else None,
                "output_label": data.get("output_label") if data else None,
                "validation_scope": data.get("validation_scope") if data else None,
                "raw_provider_payloads_included": data.get("raw_provider_payloads_included") if data else None,
                "report_name": data.get("report_name") if data else None,
            }
        )
    return entries, outputs


def _has_raw_provider_payloads(outputs: dict[str, dict[str, Any]]) -> bool:
    for output in outputs.values():
        for key, value in _walk_items(output):
            lowered = key.lower()
            if key in {"raw_payload_committed", "raw_response_stored"} and value is True:
                return True
            if key == "raw_provider_payloads_included" and value is True:
                return True
            if lowered in {"raw_provider_payload", "raw_provider_payloads", "raw_payload", "raw_response"}:
                if value not in (False, None, "", []):
                    return True
    return False


def _has_api_keys(outputs: dict[str, dict[str, Any]]) -> bool:
    for output in outputs.values():
        for key, value in _walk_items(output):
            lowered = key.lower()
            if key == "api_key_stored_or_printed" and value is True:
                return True
            if lowered in {"api_key", "token", "authorization", "authorization_header"}:
                if value not in (False, None, "", []):
                    return True
    return False


def _has_authority_or_acceptance_in_outputs(outputs: dict[str, dict[str, Any]]) -> dict[str, bool]:
    flags = {
        "new_ticker_authority": False,
        "acquisition_authority": False,
        "dataset_generation_authority": False,
        "predictive_evidence_authority": False,
        "runtime_authorization": False,
        "predictive_acceptance": False,
        "profitability_acceptance": False,
    }
    for output in outputs.values():
        for key, value in _walk_items(output):
            if key == "new_ticker_authority_created" and value is True:
                flags["new_ticker_authority"] = True
            if key in {"new_ticker_acquisition_authorized", "acquisition_authority_created"} and value is True:
                flags["acquisition_authority"] = True
            if key == "dataset_generation_authorized" and value is True:
                flags["dataset_generation_authority"] = True
            if key in {
                "additional_predictive_evidence_execution_authorized",
                "additional_predictive_evidence_executed",
            } and value is True:
                flags["predictive_evidence_authority"] = True
            if key in {"runtime_use", "strategy_use", "paper_trading", "broker_execution"} and value == "AUTHORIZED":
                flags["runtime_authorization"] = True
            if key in {
                "runtime_migration_recommended",
                "runtime_migration_approved",
                "runtime_migration_active",
                "strategy_runtime_migration",
                "automatic_stitching",
            } and value is True:
                flags["runtime_authorization"] = True
            if key == "predictive_usefulness" and value == "accepted":
                flags["predictive_acceptance"] = True
            if key == "profitability" and value == "accepted":
                flags["profitability_acceptance"] = True
    return flags


def _per_ticker_summary(outputs: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    results = (outputs.get("ticker_validation_results.json") or {}).get("results")
    if not isinstance(results, list):
        return []
    summary: list[dict[str, Any]] = []
    for item in results:
        if not isinstance(item, dict):
            continue
        summary.append(
            {
                "ticker": item.get("ticker"),
                "provider_request_status": item.get("provider_request_status"),
                "live_validation_status": item.get("live_validation_status"),
                "listing_status": item.get("listing_status"),
                "security_type_status": item.get("security_type_status"),
                "exchange_status": item.get("exchange_status"),
                "active_status": item.get("active_status"),
                "delisting_status": item.get("delisting_status"),
                "tradability_status": item.get("tradability_status"),
                "provider_symbol_mapping_status": item.get("provider_symbol_mapping_status"),
                "corporate_action_data_availability_status": item.get(
                    "corporate_action_data_availability_status"
                ),
                "historical_aggregate_data_availability_status": item.get(
                    "historical_aggregate_data_availability_status"
                ),
                "failure_reason_if_any": item.get("failure_reason_if_any"),
            }
        )
    return summary


def _output_digest_manifest(entries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "output_name": entry["name"],
            "path": entry["path"],
            "sha256_digest": entry["file_sha256"],
            "semantic_digest": entry["semantic_digest"],
            "output_label": entry["output_label"],
            "validation_scope": entry["validation_scope"],
            "raw_provider_payloads_included": entry["raw_provider_payloads_included"],
        }
        for entry in entries
    ]


def _base_package_context(output_root: Path) -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_LIVE_TICKER_VALIDATION_RESULTS_REVIEW_PACKAGE,
        "schema_version": SCHEMA_VERSION_LIVE_TICKER_VALIDATION_RESULTS_REVIEW_V1,
        "created_offline": True,
        "provider_requests_made_in_review": False,
        "live_validation_rerun_performed": False,
        "live_provider_transport_enabled_in_review": False,
        "source_execution_artifact_kind": execution.ARTIFACT_KIND_LIVE_TICKER_VALIDATION_PERFORMED,
        "source_execution_status": execution.LIVE_TICKER_VALIDATION_PERFORMED_READ_ONLY,
        "source_execution_digest": EXPECTED_SOURCE_EXECUTION_DIGEST,
        "source_execution_approval_digest": EXPECTED_SOURCE_EXECUTION_APPROVAL_DIGEST,
        "live_ticker_validation_execution_digest": EXPECTED_SOURCE_EXECUTION_DIGEST,
        "live_ticker_validation_approval_digest": EXPECTED_SOURCE_EXECUTION_APPROVAL_DIGEST,
        "live_ticker_validation_candidate_digest": EXPECTED_SOURCE_CANDIDATE_DIGEST,
        "live_ticker_validation_candidate_review_package_digest": (
            EXPECTED_SOURCE_CANDIDATE_REVIEW_PACKAGE_DIGEST
        ),
        "ticker_universe_selection_approval_digest": EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST,
        "provider_request_authorized": True,
        "provider_requests_made": True,
        "live_provider_transport_enabled": True,
        "live_ticker_validation_authorized": True,
        "live_ticker_validation_performed": True,
        "live_validation_results_created": True,
        "raw_provider_payloads_committed": False,
        "api_keys_stored_or_printed": False,
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
        "operator_review_required": True,
        "output_root": _path_text(output_root),
        "expected_output_count": EXPECTED_OUTPUT_COUNT,
        "expected_outputs": list(EXPECTED_OUTPUT_NAMES),
        "selected_endpoint": provider.MASSIVE_TICKER_DETAILS_ENDPOINT_TEMPLATE,
        "selected_endpoint_mode": provider.SELECTED_ENDPOINT_MODE,
        "validation_target_universe": list(VALIDATION_TARGET_UNIVERSE),
        "validation_target_count": len(VALIDATION_TARGET_UNIVERSE),
        "limitations": list(REQUIRED_LIMITATIONS),
        "next_gates": list(NEXT_GATES),
        "validation_supports_future_authority_chain_planning": True,
        "validation_creates_new_ticker_authority": False,
        "validation_creates_acquisition_authority": False,
        "validation_creates_dataset_generation_authority": False,
        "validation_creates_predictive_evidence_authority": False,
        "new_ticker_authority_artifact_created": False,
        "acquisition_authorization_created": False,
        "dataset_generation_authorization_created": False,
        "predictive_usefulness_acceptance_artifact_created": False,
        "profitability_acceptance_created": False,
        "runtime_migration_approval_created": False,
    }


def _summary(checklist: list[dict[str, Any]], *, review_status: str) -> dict[str, Any]:
    total = len(checklist)
    passed = sum(1 for item in checklist if item.get("status") == PASS)
    failed = total - passed
    blocker_count = sum(
        1 for item in checklist if item.get("status") == FAIL and item.get("severity") == BLOCKER
    )
    ready = review_status == LIVE_TICKER_VALIDATION_RESULTS_REVIEW_PACKAGE_READY and failed == 0
    return {
        "total_checks": total,
        "passed_checks": passed,
        "failed_checks": failed,
        "blocker_count": blocker_count,
        "ready_for_operator_review": ready,
        "ready_for_per_ticker_identity_authority_candidate": False,
        "ready_for_acquisition": False,
        "ready_for_dataset_generation": False,
        "ready_for_additional_predictive_evidence_execution_candidate": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_migration_authorized": False,
        "software_runtime_activation_authorized": False,
    }


def _checklist(package: dict[str, Any]) -> list[dict[str, Any]]:
    output_digests_bound = (
        isinstance(package.get("output_digest_manifest"), list)
        and len(package.get("output_digest_manifest", [])) == EXPECTED_OUTPUT_COUNT
        and all(item.get("sha256_digest") for item in package.get("output_digest_manifest", []))
    )
    return [
        _check("execution_digest_bound", EXPECTED_SOURCE_EXECUTION_DIGEST, package.get("source_execution_digest")),
        _check("approval_digest_bound", EXPECTED_SOURCE_EXECUTION_APPROVAL_DIGEST, package.get("source_execution_approval_digest")),
        _check("candidate_digest_bound", EXPECTED_SOURCE_CANDIDATE_DIGEST, package.get("live_ticker_validation_candidate_digest")),
        _check("candidate_review_digest_bound", EXPECTED_SOURCE_CANDIDATE_REVIEW_PACKAGE_DIGEST, package.get("live_ticker_validation_candidate_review_package_digest")),
        _check("ticker_universe_approval_digest_bound", EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST, package.get("ticker_universe_selection_approval_digest")),
        _check("endpoint_recorded", provider.MASSIVE_TICKER_DETAILS_ENDPOINT_TEMPLATE, package.get("selected_endpoint")),
        _check("validation_target_count_12", 12, package.get("validation_target_count")),
        _check("provider_request_count_12", 12, package.get("provider_request_count")),
        _check("successful_provider_response_count_12", 12, package.get("successful_provider_response_count")),
        _check("failed_provider_response_count_zero", 0, package.get("failed_provider_response_count")),
        _check("all_targets_validated_read_only", True, package.get("all_targets_validated_read_only")),
        _check("not_evaluated_count_24", 24, package.get("not_evaluated_count")),
        _check("generated_output_count_6", EXPECTED_OUTPUT_COUNT, package.get("generated_output_count")),
        _check("output_digests_bound", True, output_digests_bound),
        _check("outputs_research_only_non_actionable", True, package.get("all_outputs_research_only_non_actionable")),
        _check("validation_scope_read_only_provider_ticker_validation_only", True, package.get("all_outputs_scope_read_only")),
        _check("raw_provider_payloads_not_committed", False, package.get("raw_provider_payloads_committed")),
        _check("api_keys_not_stored_or_printed", False, package.get("api_keys_stored_or_printed")),
        _check("provider_requests_made_in_review_false", False, package.get("provider_requests_made_in_review")),
        _check("live_validation_rerun_performed_false", False, package.get("live_validation_rerun_performed")),
        _check("live_provider_transport_enabled_in_review_false", False, package.get("live_provider_transport_enabled_in_review")),
        _check("new_ticker_authority_created_false", False, package.get("new_ticker_authority_created")),
        _check("new_ticker_acquisition_authorized_false", False, package.get("new_ticker_acquisition_authorized")),
        _check("dataset_generation_authorized_false", False, package.get("dataset_generation_authorized")),
        _check("additional_predictive_evidence_execution_authorized_false", False, package.get("additional_predictive_evidence_execution_authorized")),
        _check("additional_predictive_evidence_executed_false", False, package.get("additional_predictive_evidence_executed")),
        _check("predictive_experiment_rerun_authorized_false", False, package.get("predictive_experiment_rerun_authorized")),
        _check("predictive_experiment_rerun_performed_false", False, package.get("predictive_experiment_rerun_performed")),
        _check("walk_forward_rerun_performed_false", False, package.get("walk_forward_rerun_performed")),
        _check("label_regeneration_performed_false", False, package.get("label_regeneration_performed")),
        _check("feature_matrix_regeneration_performed_false", False, package.get("feature_matrix_regeneration_performed")),
        _check("new_strategy_scoring_performed_false", False, package.get("new_strategy_scoring_performed")),
        _check("trade_recommendations_generated_false", False, package.get("trade_recommendations_generated")),
        _check("predictive_usefulness_not_accepted", acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED, package.get("predictive_usefulness")),
        _check("predictive_usefulness_acceptance_ready_false", False, package.get("predictive_usefulness_acceptance_ready")),
        _check("predictive_usefulness_acceptance_recommended_false", False, package.get("predictive_usefulness_acceptance_recommended")),
        _check("predictive_usefulness_acceptance_candidate_created_false", False, package.get("predictive_usefulness_acceptance_candidate_created")),
        _check("profitability_not_accepted", acquisition.PROFITABILITY_NOT_ACCEPTED, package.get("profitability")),
        _check("profitability_acceptance_ready_false", False, package.get("profitability_acceptance_ready")),
        _check("profitability_acceptance_recommended_false", False, package.get("profitability_acceptance_recommended")),
        _check("runtime_migration_recommended_false", False, package.get("runtime_migration_recommended")),
        _check("runtime_migration_approved_false", False, package.get("runtime_migration_approved")),
        _check("runtime_migration_active_false", False, package.get("runtime_migration_active")),
        _check("strategy_runtime_migration_false", False, package.get("strategy_runtime_migration")),
        _check("runtime_use_not_authorized", NOT_AUTHORIZED, package.get("runtime_use")),
        _check("strategy_use_not_authorized", NOT_AUTHORIZED, package.get("strategy_use")),
        _check("paper_trading_not_authorized", NOT_AUTHORIZED, package.get("paper_trading")),
        _check("broker_execution_not_authorized", NOT_AUTHORIZED, package.get("broker_execution")),
        _check("automatic_stitching_false", False, package.get("automatic_stitching")),
        _check("validation_supports_future_authority_chain_planning_true", True, package.get("validation_supports_future_authority_chain_planning")),
        _check("validation_creates_new_ticker_authority_false", False, package.get("validation_creates_new_ticker_authority")),
        _check("validation_creates_acquisition_authority_false", False, package.get("validation_creates_acquisition_authority")),
        _check("validation_creates_dataset_generation_authority_false", False, package.get("validation_creates_dataset_generation_authority")),
        _check("validation_creates_predictive_evidence_authority_false", False, package.get("validation_creates_predictive_evidence_authority")),
        _check("limitations_recorded", REQUIRED_LIMITATIONS, package.get("limitations")),
        _check("next_gates_defined", NEXT_GATES, package.get("next_gates")),
        _check("no_new_ticker_authority_artifact_created", False, package.get("new_ticker_authority_artifact_created")),
        _check("no_acquisition_authorization_created", False, package.get("acquisition_authorization_created")),
        _check("no_dataset_generation_authorization_created", False, package.get("dataset_generation_authorization_created")),
        _check("no_predictive_usefulness_acceptance_artifact_created", False, package.get("predictive_usefulness_acceptance_artifact_created")),
        _check("no_profitability_acceptance_created", False, package.get("profitability_acceptance_created")),
        _check("no_runtime_migration_approval_created", False, package.get("runtime_migration_approval_created")),
    ]


def _digest_payload(review_package: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(review_package)
    payload.pop("live_ticker_validation_results_review_package_digest", None)
    return payload


def live_ticker_validation_results_review_package_digest_v1(review_package: dict[str, Any]) -> str:
    """Return the deterministic semantic digest for the results review package."""
    return semantic_digest(_digest_payload(review_package))


def build_live_ticker_validation_results_review_package_v1(
    *,
    output_root: str | Path | None = None,
) -> dict[str, Any]:
    """Build an offline review package for already-generated ticker validation outputs."""
    root = _resolve_output_root(output_root)
    entries, outputs = _output_file_entries(root)
    missing_count = sum(1 for entry in entries if not entry["exists"])
    output_root_present = root.exists() and root.is_dir()
    actual_output_count = EXPECTED_OUTPUT_COUNT - missing_count
    summary = outputs.get("validation_summary.json") or {}
    run_manifest = outputs.get("live_ticker_validation_run_manifest.json") or {}
    per_ticker = _per_ticker_summary(outputs)
    authority_flags = _has_authority_or_acceptance_in_outputs(outputs)
    all_labeled = (
        missing_count == 0
        and all(entry["output_label"] == RESEARCH_ONLY_NON_ACTIONABLE for entry in entries)
    )
    all_scoped = (
        missing_count == 0
        and all(entry["validation_scope"] == READ_ONLY_PROVIDER_TICKER_VALIDATION_ONLY for entry in entries)
    )
    all_targets_validated = (
        [item.get("ticker") for item in per_ticker] == VALIDATION_TARGET_UNIVERSE
        and all(item.get("live_validation_status") == VALIDATED_READ_ONLY for item in per_ticker)
    )
    package = {
        **_base_package_context(root),
        "review_status": (
            LIVE_TICKER_VALIDATION_RESULTS_REVIEW_PACKAGE_READY
            if missing_count == 0
            else LIVE_TICKER_VALIDATION_RESULTS_REVIEW_BLOCKED_MISSING_OUTPUTS
        ),
        "output_file_inspection_performed": missing_count == 0,
        "output_root_present": output_root_present,
        "actual_output_count": actual_output_count,
        "missing_output_count": missing_count,
        "output_files": entries,
        "output_digest_manifest": _output_digest_manifest(entries),
        "all_outputs_research_only_non_actionable": all_labeled,
        "all_outputs_scope_read_only": all_scoped,
        "source_execution_run_timestamp_utc": run_manifest.get("run_timestamp_utc"),
        "provider_reference_details_available": actual_output_count == EXPECTED_OUTPUT_COUNT,
        "live_ticker_validation_results_available": actual_output_count == EXPECTED_OUTPUT_COUNT,
        "selected_endpoint": run_manifest.get("selected_endpoint", provider.MASSIVE_TICKER_DETAILS_ENDPOINT_TEMPLATE),
        "selected_endpoint_mode": run_manifest.get("selected_endpoint_mode", provider.SELECTED_ENDPOINT_MODE),
        "validation_target_universe": run_manifest.get("validation_target_universe", list(VALIDATION_TARGET_UNIVERSE)),
        "validation_target_count": summary.get("validation_target_count"),
        "provider_request_count": summary.get("provider_request_count"),
        "successful_provider_response_count": summary.get("successful_provider_response_count"),
        "failed_provider_response_count": summary.get("failed_provider_response_count"),
        "validated_read_only_count": summary.get("validated_read_only_count"),
        "validation_failed_count": summary.get("validation_failed_count"),
        "not_evaluated_count": summary.get("not_evaluated_count"),
        "generated_output_count": summary.get("generated_output_count"),
        "failure_count": summary.get("failure_count"),
        "warning_count": summary.get("warning_count"),
        "per_ticker_validation_summary": per_ticker,
        "all_targets_validated_read_only": all_targets_validated,
        "corporate_action_data_availability_status": NOT_EVALUATED_BY_SELECTED_ENDPOINT,
        "historical_aggregate_data_availability_status": NOT_EVALUATED_BY_SELECTED_ENDPOINT,
        "raw_provider_payloads_committed": _has_raw_provider_payloads(outputs),
        "api_keys_stored_or_printed": _has_api_keys(outputs),
        "validation_creates_new_ticker_authority": authority_flags["new_ticker_authority"],
        "validation_creates_acquisition_authority": authority_flags["acquisition_authority"],
        "validation_creates_dataset_generation_authority": authority_flags["dataset_generation_authority"],
        "validation_creates_predictive_evidence_authority": authority_flags["predictive_evidence_authority"],
        "runtime_authorization_present_in_outputs": authority_flags["runtime_authorization"],
        "predictive_acceptance_present_in_outputs": authority_flags["predictive_acceptance"],
        "profitability_acceptance_present_in_outputs": authority_flags["profitability_acceptance"],
    }
    checklist = _checklist(package)
    package["review_checklist"] = checklist
    package["review_summary"] = _summary(checklist, review_status=package["review_status"])
    package["live_ticker_validation_results_review_package_digest"] = (
        live_ticker_validation_results_review_package_digest_v1(package)
    )
    validate_live_ticker_validation_results_review_package_v1(package)
    return package


def _reject_forbidden_values(mapping: dict[str, Any], *, path: str = "review_package") -> None:
    forbidden_true_fields = {
        "provider_requests_made_in_review",
        "live_validation_rerun_performed",
        "live_provider_transport_enabled_in_review",
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
        "validation_creates_new_ticker_authority",
        "validation_creates_acquisition_authority",
        "validation_creates_dataset_generation_authority",
        "validation_creates_predictive_evidence_authority",
    }
    for key, value in mapping.items():
        current_path = f"{path}.{key}"
        if key in forbidden_true_fields and value is True:
            raise LiveTickerValidationResultsReviewError(f"{current_path} must be false")
        if key in {"runtime_use", "strategy_use", "paper_trading", "broker_execution"} and value == "AUTHORIZED":
            raise LiveTickerValidationResultsReviewError(f"{current_path} must not be AUTHORIZED")
        if key in {"predictive_usefulness", "profitability"} and value == "accepted":
            raise LiveTickerValidationResultsReviewError(f"{current_path} must not be accepted")
        if isinstance(value, dict):
            _reject_forbidden_values(value, path=current_path)
        elif isinstance(value, list):
            for index, item in enumerate(value):
                if isinstance(item, dict):
                    _reject_forbidden_values(item, path=f"{current_path}[{index}]")


def validate_live_ticker_validation_results_review_package_v1(
    review_package: dict[str, Any],
) -> dict[str, Any]:
    """Validate a ticker validation results review package without expanding authority."""
    if not isinstance(review_package, dict):
        raise LiveTickerValidationResultsReviewError("review package must be a JSON object")
    _reject_forbidden_values(review_package)
    _expect(
        review_package.get("artifact_kind"),
        ARTIFACT_KIND_LIVE_TICKER_VALIDATION_RESULTS_REVIEW_PACKAGE,
        "artifact_kind",
    )
    _expect(
        review_package.get("schema_version"),
        SCHEMA_VERSION_LIVE_TICKER_VALIDATION_RESULTS_REVIEW_V1,
        "schema_version",
    )
    status = review_package.get("review_status")
    if status not in {
        LIVE_TICKER_VALIDATION_RESULTS_REVIEW_PACKAGE_READY,
        LIVE_TICKER_VALIDATION_RESULTS_REVIEW_BLOCKED_MISSING_OUTPUTS,
    }:
        raise LiveTickerValidationResultsReviewError("review_status mismatch")
    if status == LIVE_TICKER_VALIDATION_RESULTS_REVIEW_PACKAGE_READY:
        _expect(review_package.get("missing_output_count"), 0, "missing_output_count")
    for field in (
        "created_offline",
        "provider_request_authorized",
        "provider_requests_made",
        "live_provider_transport_enabled",
        "live_ticker_validation_authorized",
        "live_ticker_validation_performed",
        "live_validation_results_created",
        "research_only",
        "operator_review_required",
    ):
        _expect_true(review_package.get(field), field)
    for field in (
        "provider_requests_made_in_review",
        "live_validation_rerun_performed",
        "live_provider_transport_enabled_in_review",
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
        "validation_creates_new_ticker_authority",
        "validation_creates_acquisition_authority",
        "validation_creates_dataset_generation_authority",
        "validation_creates_predictive_evidence_authority",
    ):
        _expect_false(review_package.get(field), field)
    for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
        _expect(review_package.get(field), NOT_AUTHORIZED, field)
    _expect(
        review_package.get("predictive_usefulness"),
        acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "predictive_usefulness",
    )
    _expect(review_package.get("profitability"), acquisition.PROFITABILITY_NOT_ACCEPTED, "profitability")
    for field, expected in {
        "source_execution_artifact_kind": execution.ARTIFACT_KIND_LIVE_TICKER_VALIDATION_PERFORMED,
        "source_execution_status": execution.LIVE_TICKER_VALIDATION_PERFORMED_READ_ONLY,
        "source_execution_digest": EXPECTED_SOURCE_EXECUTION_DIGEST,
        "source_execution_approval_digest": EXPECTED_SOURCE_EXECUTION_APPROVAL_DIGEST,
        "live_ticker_validation_execution_digest": EXPECTED_SOURCE_EXECUTION_DIGEST,
        "live_ticker_validation_approval_digest": EXPECTED_SOURCE_EXECUTION_APPROVAL_DIGEST,
        "live_ticker_validation_candidate_digest": EXPECTED_SOURCE_CANDIDATE_DIGEST,
        "live_ticker_validation_candidate_review_package_digest": (
            EXPECTED_SOURCE_CANDIDATE_REVIEW_PACKAGE_DIGEST
        ),
        "ticker_universe_selection_approval_digest": EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST,
        "selected_endpoint": provider.MASSIVE_TICKER_DETAILS_ENDPOINT_TEMPLATE,
        "selected_endpoint_mode": provider.SELECTED_ENDPOINT_MODE,
        "validation_target_universe": VALIDATION_TARGET_UNIVERSE,
        "validation_target_count": 12,
        "provider_request_count": 12,
        "successful_provider_response_count": 12,
        "failed_provider_response_count": 0,
        "validated_read_only_count": 12,
        "validation_failed_count": 0,
        "not_evaluated_count": 24,
        "generated_output_count": EXPECTED_OUTPUT_COUNT,
        "expected_output_count": EXPECTED_OUTPUT_COUNT,
        "failure_count": 0,
        "warning_count": 24,
        "corporate_action_data_availability_status": NOT_EVALUATED_BY_SELECTED_ENDPOINT,
        "historical_aggregate_data_availability_status": NOT_EVALUATED_BY_SELECTED_ENDPOINT,
        "limitations": REQUIRED_LIMITATIONS,
        "next_gates": NEXT_GATES,
    }.items():
        if status == LIVE_TICKER_VALIDATION_RESULTS_REVIEW_PACKAGE_READY or field not in {
            "validation_target_count",
            "provider_request_count",
            "successful_provider_response_count",
            "failed_provider_response_count",
            "validated_read_only_count",
            "validation_failed_count",
            "not_evaluated_count",
            "generated_output_count",
            "failure_count",
            "warning_count",
        }:
            _expect(review_package.get(field), expected, field)
    if status == LIVE_TICKER_VALIDATION_RESULTS_REVIEW_PACKAGE_READY:
        _expect(review_package.get("actual_output_count"), EXPECTED_OUTPUT_COUNT, "actual_output_count")
        _expect_true(
            review_package.get("all_outputs_research_only_non_actionable"),
            "all_outputs_research_only_non_actionable",
        )
        _expect_true(review_package.get("all_outputs_scope_read_only"), "all_outputs_scope_read_only")
        _expect_true(review_package.get("all_targets_validated_read_only"), "all_targets_validated_read_only")
        per_ticker = review_package.get("per_ticker_validation_summary")
        if not isinstance(per_ticker, list) or len(per_ticker) != 12:
            raise LiveTickerValidationResultsReviewError("per_ticker_validation_summary mismatch")
        _expect([item.get("ticker") for item in per_ticker], VALIDATION_TARGET_UNIVERSE, "per_ticker_validation_summary tickers")
        for item in per_ticker:
            _expect(item.get("provider_request_status"), PROVIDER_RESPONSE_AVAILABLE, f"{item.get('ticker')}.provider_request_status")
            _expect(item.get("live_validation_status"), VALIDATED_READ_ONLY, f"{item.get('ticker')}.live_validation_status")
            _expect(
                item.get("corporate_action_data_availability_status"),
                NOT_EVALUATED_BY_SELECTED_ENDPOINT,
                f"{item.get('ticker')}.corporate_action_data_availability_status",
            )
            _expect(
                item.get("historical_aggregate_data_availability_status"),
                NOT_EVALUATED_BY_SELECTED_ENDPOINT,
                f"{item.get('ticker')}.historical_aggregate_data_availability_status",
            )
        manifest = review_package.get("output_digest_manifest")
        if not isinstance(manifest, list) or len(manifest) != EXPECTED_OUTPUT_COUNT:
            raise LiveTickerValidationResultsReviewError("output_digest_manifest missing")
        _expect([item.get("output_name") for item in manifest], EXPECTED_OUTPUT_NAMES, "output_digest_manifest names")
        for item in manifest:
            if not item.get("sha256_digest") or not item.get("semantic_digest"):
                raise LiveTickerValidationResultsReviewError("output digests missing")
            _expect(item.get("output_label"), RESEARCH_ONLY_NON_ACTIONABLE, "output_label")
            _expect(item.get("validation_scope"), READ_ONLY_PROVIDER_TICKER_VALIDATION_ONLY, "validation_scope")
    checklist = review_package.get("review_checklist")
    if not isinstance(checklist, list):
        raise LiveTickerValidationResultsReviewError("review_checklist missing")
    _expect([item.get("check_id") for item in checklist], REQUIRED_CHECK_IDS, "review_checklist check IDs")
    expected_checklist = _checklist(review_package)
    if status == LIVE_TICKER_VALIDATION_RESULTS_REVIEW_PACKAGE_READY:
        failed = [item for item in expected_checklist if item["status"] != PASS]
        if failed:
            raise LiveTickerValidationResultsReviewError(
                f"review checklist contains failed check: {failed[0]['check_id']}"
            )
    _expect(checklist, expected_checklist, "review_checklist")
    expected_summary = _summary(expected_checklist, review_status=status)
    _expect(review_package.get("review_summary"), expected_summary, "review_summary")
    digest = review_package.get("live_ticker_validation_results_review_package_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise LiveTickerValidationResultsReviewError(
            "live_ticker_validation_results_review_package_digest missing"
        )
    _expect(
        digest,
        live_ticker_validation_results_review_package_digest_v1(review_package),
        "live_ticker_validation_results_review_package_digest",
    )
    return {
        "status": "LIVE_TICKER_VALIDATION_RESULTS_REVIEW_PACKAGE_VALID",
        "artifact_kind": review_package["artifact_kind"],
        "review_status": review_package["review_status"],
        "live_ticker_validation_results_review_package_digest": digest,
        "source_execution_digest": review_package["source_execution_digest"],
        "source_execution_approval_digest": review_package["source_execution_approval_digest"],
        "validation_target_count": review_package["validation_target_count"],
        "provider_request_count": review_package["provider_request_count"],
        "successful_provider_response_count": review_package["successful_provider_response_count"],
        "failed_provider_response_count": review_package["failed_provider_response_count"],
        "actual_output_count": review_package["actual_output_count"],
        "failure_count": review_package["failure_count"],
        "warning_count": review_package["warning_count"],
        "total_checks": review_package["review_summary"]["total_checks"],
        "passed_checks": review_package["review_summary"]["passed_checks"],
        "failed_checks": review_package["review_summary"]["failed_checks"],
        "blocker_count": review_package["review_summary"]["blocker_count"],
        "runtime_migration_authorized": False,
        "software_runtime_activation_authorized": False,
        "predictive_usefulness": acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED,
        "profitability": acquisition.PROFITABILITY_NOT_ACCEPTED,
    }


def build_live_ticker_validation_results_review_markdown_v1(review_package: dict[str, Any]) -> str:
    """Render a sanitized live ticker validation results review status document."""
    validation = validate_live_ticker_validation_results_review_package_v1(review_package)
    summary = review_package["review_summary"]
    lines = [
        "# MarketFlow Live Ticker Validation Results Review Status",
        "",
        "## Title",
        "- Live Ticker Validation Results Operator Review Package v1.",
        "",
        "## Reviewed Live Ticker Validation Execution",
        f"- Artifact kind: `{review_package['source_execution_artifact_kind']}`",
        f"- Execution status: `{review_package['source_execution_status']}`",
        f"- Execution digest: `{review_package['source_execution_digest']}`",
        f"- Results review package digest: `{validation['live_ticker_validation_results_review_package_digest']}`",
        "",
        "## Source Evidence",
        f"- Approval digest: `{review_package['source_execution_approval_digest']}`",
        f"- Candidate digest: `{review_package['live_ticker_validation_candidate_digest']}`",
        f"- Candidate review package digest: `{review_package['live_ticker_validation_candidate_review_package_digest']}`",
        f"- Ticker universe selection approval digest: `{review_package['ticker_universe_selection_approval_digest']}`",
        "",
        "## Validation Target Universe",
        f"- Validation target count: `{review_package['validation_target_count']}`",
        "- Validation targets: " + ", ".join(f"`{ticker}`" for ticker in review_package["validation_target_universe"]),
        "",
        "## Provider Request Summary",
        f"- Endpoint: `{review_package['selected_endpoint']}`",
        f"- Endpoint mode: `{review_package['selected_endpoint_mode']}`",
        f"- Provider request count: `{review_package['provider_request_count']}`",
        f"- Successful provider response count: `{review_package['successful_provider_response_count']}`",
        f"- Failed provider response count: `{review_package['failed_provider_response_count']}`",
        f"- Validated read-only count: `{review_package['validated_read_only_count']}`",
        f"- Not evaluated count: `{review_package['not_evaluated_count']}`",
        f"- Failure count: `{review_package['failure_count']}`",
        f"- Warning count: `{review_package['warning_count']}`",
        "",
        "## Per-Ticker Validation Summary",
    ]
    lines.extend(
        f"- `{item['ticker']}`: `{item['live_validation_status']}`; corporate action `{item['corporate_action_data_availability_status']}`; historical aggregate `{item['historical_aggregate_data_availability_status']}`"
        for item in review_package["per_ticker_validation_summary"]
    )
    lines.extend(
        [
            "",
            "## Output Digest Manifest",
        ]
    )
    lines.extend(
        f"- `{item['output_name']}`: `{item['sha256_digest']}`"
        for item in review_package["output_digest_manifest"]
    )
    lines.extend(
        [
            "",
            "## Limitations",
        ]
    )
    lines.extend(f"- `{item}`" for item in review_package["limitations"])
    lines.extend(["", "## Next Gates"])
    lines.extend(f"- `{item}`" for item in review_package["next_gates"])
    lines.extend(
        [
            "",
            "## Authority Boundary",
            f"- validation_supports_future_authority_chain_planning: `{review_package['validation_supports_future_authority_chain_planning']}`",
            f"- validation_creates_new_ticker_authority: `{review_package['validation_creates_new_ticker_authority']}`",
            f"- new_ticker_authority_created: `{review_package['new_ticker_authority_created']}`",
            "",
            "## Acquisition Boundary",
            f"- validation_creates_acquisition_authority: `{review_package['validation_creates_acquisition_authority']}`",
            f"- new_ticker_acquisition_authorized: `{review_package['new_ticker_acquisition_authorized']}`",
            "",
            "## Dataset Boundary",
            f"- validation_creates_dataset_generation_authority: `{review_package['validation_creates_dataset_generation_authority']}`",
            f"- dataset_generation_authorized: `{review_package['dataset_generation_authorized']}`",
            "",
            "## Predictive/Profitability Boundary",
            f"- validation_creates_predictive_evidence_authority: `{review_package['validation_creates_predictive_evidence_authority']}`",
            f"- additional_predictive_evidence_execution_authorized: `{review_package['additional_predictive_evidence_execution_authorized']}`",
            f"- additional_predictive_evidence_executed: `{review_package['additional_predictive_evidence_executed']}`",
            f"- predictive_usefulness: `{review_package['predictive_usefulness']}`",
            f"- profitability: `{review_package['profitability']}`",
            "",
            "## Runtime Boundary",
            f"- runtime_migration_recommended: `{review_package['runtime_migration_recommended']}`",
            f"- runtime_migration_approved: `{review_package['runtime_migration_approved']}`",
            f"- runtime_migration_active: `{review_package['runtime_migration_active']}`",
            f"- runtime_use: `{review_package['runtime_use']}`",
            f"- strategy_use: `{review_package['strategy_use']}`",
            f"- paper_trading: `{review_package['paper_trading']}`",
            f"- broker_execution: `{review_package['broker_execution']}`",
            "",
            "## Checklist Summary",
            f"- Total checks: `{summary['total_checks']}`",
            f"- Passed checks: `{summary['passed_checks']}`",
            f"- Failed checks: `{summary['failed_checks']}`",
            f"- Blocker count: `{summary['blocker_count']}`",
            f"- Ready for operator review: `{summary['ready_for_operator_review']}`",
            "",
            "## Guardrails",
            "- No Massive.com / Polygon provider request was made in review.",
            "- No live ticker validation rerun was performed.",
            "- No live provider transport was enabled in review.",
            "- No raw provider payloads or API keys are included in this status document.",
            "- No new ticker authority, acquisition authority, dataset generation authorization, predictive acceptance, profitability acceptance, runtime activation, paper trading, broker execution, or trade recommendation artifact was created.",
            "",
        ]
    )
    return "\n".join(lines)


def write_live_ticker_validation_results_review_package_v1(
    output_dir: str | Path,
    *,
    output_root: str | Path | None = None,
    filename: str | None = None,
) -> dict[str, Any]:
    """Write the live ticker validation results review JSON without overwriting output."""
    package = build_live_ticker_validation_results_review_package_v1(output_root=output_root)
    validation = validate_live_ticker_validation_results_review_package_v1(package)
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    output_name = filename or "live_ticker_validation_results_review_package_v1.json"
    if Path(output_name).name != output_name or not output_name.endswith(".json"):
        raise LiveTickerValidationResultsReviewError(
            "live ticker validation results review filename must be a simple JSON filename"
        )
    path = directory / output_name
    if path.exists():
        raise LiveTickerValidationResultsReviewError(
            "live ticker validation results review output already exists"
        )
    payload = canonical_json_bytes(package)
    with path.open("xb") as handle:
        handle.write(payload)
    return validation | {
        "path": _path_text(path),
        "filename": path.name,
        "payload_byte_size": len(payload),
        "payload_sha256": sha256_bytes(payload),
    }
