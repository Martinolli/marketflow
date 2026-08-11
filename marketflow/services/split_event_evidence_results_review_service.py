"""Offline review package for split provider evidence execution results."""

from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
from typing import Any, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import acquisition_generation_service as acquisition
from marketflow.services import split_provider_evidence_execution_service as execution
from marketflow.services import split_provider_evidence_request_approval_service as approval


ARTIFACT_KIND_SPLIT_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE = (
    "SPLIT_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE"
)
SCHEMA_VERSION_SPLIT_EVENT_EVIDENCE_RESULTS_REVIEW_V1 = (
    "split_event_evidence_results_review_v1"
)
SPLIT_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE_READY = (
    "SPLIT_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE_READY"
)
SPLIT_EVENT_EVIDENCE_RESULTS_REVIEW_BLOCKED_MISSING_OR_INVALID_OUTPUTS = (
    "SPLIT_EVENT_EVIDENCE_RESULTS_REVIEW_BLOCKED_MISSING_OR_INVALID_OUTPUTS"
)

RESEARCH_ONLY_NON_ACTIONABLE = execution.RESEARCH_ONLY_NON_ACTIONABLE
READ_ONLY_SPLIT_EVENT_EVIDENCE_REQUESTS_ONLY = (
    execution.READ_ONLY_SPLIT_EVENT_EVIDENCE_REQUESTS_ONLY
)
NOT_AUTHORIZED = execution.NOT_AUTHORIZED
PASS = execution.PASS
FAIL = execution.FAIL
BLOCKER = execution.BLOCKER

EXPECTED_SPLIT_PROVIDER_EVIDENCE_EXECUTION_DIGEST = (
    "823bfb52b1623b8b9eb88b197da9b9943dfc1e14cb1d280160ba2cbe26eec4c4"
)
EXPECTED_SPLIT_PROVIDER_EVIDENCE_REQUEST_APPROVAL_DIGEST = (
    execution.EXPECTED_SPLIT_PROVIDER_EVIDENCE_REQUEST_APPROVAL_DIGEST
)
EXPECTED_TARGET_UNIVERSE = list(execution.TARGET_UNIVERSE)
EXPECTED_OUTPUT_DIGESTS = {
    "operator_review_summary.json": "f89f53463cb7e9c9ff71e1de04322226d018cbb6a66bcc3c3c4cf401327f0683",
    "split_event_absence_inventory.json": "e318894295993ffda91f7d5af394c3a0566f9ce12567b8da007ea7b43a74e88f",
    "split_event_failure_reason_inventory.json": "00f3d48bb60134a983f00ac54ac4086fe240bf010f79afb8a25b4005efdb4f8d",
    "split_event_results_sanitized.json": "af6de085ee34347b1c8188041dbc92d32183cc5af3c760df064f6c93d2470569",
    "split_provider_evidence_run_manifest.json": "3593c5aa1d0dd8d08a2f7f709de3d810610623b521684af536fca35c7cdb0847",
    "split_provider_request_receipts_sanitized.json": "a03e63633075a8d72fdd1cf9b7cffa5ddf13c2ba996a0b2c8e31b8c0c8cbb0e6",
}
EXPECTED_OUTPUT_FILENAMES = list(execution.OUTPUT_FILENAMES)
EXPECTED_OUTPUT_FILENAMES_SORTED = sorted(EXPECTED_OUTPUT_DIGESTS)

EXPECTED_RESULT_FACTS = {
    "endpoint": "/stocks/v1/splits",
    "endpoint_mode": "CURRENT_STOCKS_V1_SPLITS",
    "transport_mode": "LIVE_HTTP_TRANSPORT_READ_ONLY",
    "target_count": 12,
    "provider_request_count": 12,
    "successful_provider_response_count": 12,
    "failed_provider_response_count": 0,
    "split_evidence_collected_count": 7,
    "no_split_events_returned_count": 5,
    "generated_output_count": 6,
    "failure_count": 0,
    "warning_count": 12,
}
EXPECTED_PER_TICKER_STATUS = {
    "MSFT": execution.SPLIT_EVIDENCE_COLLECTED_READ_ONLY,
    "NVDA": execution.SPLIT_EVIDENCE_COLLECTED_READ_ONLY,
    "AMZN": execution.SPLIT_EVIDENCE_COLLECTED_READ_ONLY,
    "GOOGL": execution.SPLIT_EVIDENCE_COLLECTED_READ_ONLY,
    "META": execution.NO_SPLIT_EVENTS_RETURNED_BY_PROVIDER,
    "TSLA": execution.SPLIT_EVIDENCE_COLLECTED_READ_ONLY,
    "JPM": execution.NO_SPLIT_EVENTS_RETURNED_BY_PROVIDER,
    "XOM": execution.NO_SPLIT_EVENTS_RETURNED_BY_PROVIDER,
    "JNJ": execution.NO_SPLIT_EVENTS_RETURNED_BY_PROVIDER,
    "WMT": execution.SPLIT_EVIDENCE_COLLECTED_READ_ONLY,
    "CAT": execution.SPLIT_EVIDENCE_COLLECTED_READ_ONLY,
    "LMT": execution.NO_SPLIT_EVENTS_RETURNED_BY_PROVIDER,
}

LIMITATIONS = [
    "split_evidence_read_only_provider_snapshot_at_execution_time",
    "no_split_events_returned_requires_explicit_absence_policy_review",
    "split_authority_not_created",
    "split_freeze_not_created",
    "dividend_authority_not_created",
    "corporate_action_authority_not_created",
    "acquisition_authority_not_created",
    "dataset_generation_not_authorized",
    "operator_review_required_before_split_authority_freeze",
]
NEXT_GATES = [
    "split_event_evidence_results_operator_review",
    "split_event_discrepancy_triage_if_required",
    "split_event_authority_freeze_ceremony",
    "dividend_provider_evidence_request_approval",
    "dividend_provider_evidence_execution",
    "dividend_event_authority_freeze_ceremony",
    "combined_corporate_action_readiness_review",
    "corporate_action_authority_approval_if_required",
    "acquisition_generation_chain_candidate",
    "canonical_dataset_chain_candidate",
    "research_registry_chain_candidate",
]
REQUIRED_CHECK_IDS = [
    "split_provider_evidence_execution_digest_bound",
    "split_provider_evidence_request_approval_digest_bound",
    "split_candidate_review_digest_bound",
    "split_candidate_digest_bound",
    "dividend_candidate_review_digest_bound",
    "corporate_action_plan_approval_digest_bound",
    "identity_freeze_digest_bound",
    "target_universe_count_12",
    "target_universe_matches_execution_universe",
    "provider_request_count_12",
    "successful_provider_response_count_12",
    "failed_provider_response_count_zero",
    "split_evidence_collected_count_7",
    "no_split_events_returned_count_5",
    "generated_output_count_6",
    "output_digests_bound",
    "outputs_research_only_non_actionable",
    "evidence_scope_read_only_split_event_evidence_requests_only",
    "raw_provider_payloads_not_committed",
    "api_keys_not_stored_or_printed",
    "provider_requests_made_in_review_false",
    "split_provider_evidence_rerun_performed_false",
    "live_provider_transport_enabled_in_review_false",
    "split_event_authority_created_false",
    "split_event_authority_frozen_false",
    "dividend_provider_evidence_request_authorized_false",
    "dividend_provider_evidence_executed_false",
    "dividend_event_authority_created_false",
    "dividend_event_authority_frozen_false",
    "corporate_action_authority_created_false",
    "new_ticker_acquisition_authorized_false",
    "dataset_generation_authorized_false",
    "acquisition_generation_authorized_false",
    "canonical_dataset_authorized_false",
    "registry_approval_created_false",
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
    "profitability_not_accepted",
    "runtime_migration_approved_false",
    "runtime_use_not_authorized",
    "strategy_use_not_authorized",
    "paper_trading_not_authorized",
    "broker_execution_not_authorized",
    "automatic_stitching_false",
    "split_evidence_supports_future_split_authority_planning_true",
    "split_evidence_creates_split_authority_false",
    "split_evidence_creates_corporate_action_authority_false",
    "split_evidence_creates_acquisition_authority_false",
    "split_evidence_creates_dataset_generation_authority_false",
    "limitations_recorded",
    "next_gates_defined",
    "no_split_event_authority_artifact_created",
    "no_split_event_authority_freeze_created",
    "no_dividend_provider_evidence_request_created",
    "no_dividend_event_authority_artifact_created",
    "no_corporate_action_authority_artifact_created",
    "no_acquisition_authorization_created",
    "no_dataset_generation_authorization_created",
    "no_predictive_usefulness_acceptance_artifact_created",
    "no_profitability_acceptance_created",
    "no_runtime_migration_approval_created",
]


class SplitEventEvidenceResultsReviewError(ValueError):
    """Raised when the split evidence results review package is invalid."""


def _not_accepted() -> str:
    return acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED


def _digest_payload(review_package: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(review_package)
    payload.pop("split_event_evidence_results_review_package_digest", None)
    return payload


def split_event_evidence_results_review_package_digest_v1(
    review_package: dict[str, Any],
) -> str:
    """Return the deterministic digest for the split evidence results review package."""
    return semantic_digest(_digest_payload(review_package))


def _load_json_file(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SplitEventEvidenceResultsReviewError(f"{path.name} is not readable JSON") from exc
    if not isinstance(payload, dict):
        raise SplitEventEvidenceResultsReviewError(f"{path.name} must contain a JSON object")
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
        return "bearer " in lowered or "apikey=" in lowered or "api_key=" in lowered
    return False


def _forbidden_authority_or_raw_payload(payload: Mapping[str, Any]) -> str | None:
    forbidden_true_fields = {
        "split_event_authority_created",
        "split_event_authority_frozen",
        "corporate_action_authority_created",
        "new_ticker_acquisition_authorized",
        "dataset_generation_authorized",
        "raw_provider_payloads_committed",
        "raw_payload_committed",
        "raw_response_stored",
        "api_keys_stored_or_printed",
        "api_key_stored_or_printed",
    }
    for key, value in payload.items():
        if key in forbidden_true_fields and value is True:
            return key
        if key in {"runtime_use", "strategy_use", "paper_trading", "broker_execution"} and value == "AUTHORIZED":
            return key
        if key in {"predictive_usefulness", "profitability"} and value == "accepted":
            return key
        if isinstance(value, Mapping):
            found = _forbidden_authority_or_raw_payload(value)
            if found:
                return f"{key}.{found}"
        elif isinstance(value, list):
            for index, item in enumerate(value):
                if isinstance(item, Mapping):
                    found = _forbidden_authority_or_raw_payload(item)
                    if found:
                        return f"{key}[{index}].{found}"
    return None


def _blocked_package(reason: str) -> dict[str, Any]:
    package = _base_package()
    package.update(
        {
            "review_status": SPLIT_EVENT_EVIDENCE_RESULTS_REVIEW_BLOCKED_MISSING_OR_INVALID_OUTPUTS,
            "output_file_inspection_performed": False,
            "blocked_reason": reason,
            "outputs_verified": False,
            "output_digest_manifest": [],
            "review_checklist": [],
            "review_summary": _summary([]),
            "next_required_task": "RECREATE_OR_RESTORE_SPLIT_PROVIDER_EVIDENCE_OUTPUTS",
        }
    )
    package["split_event_evidence_results_review_package_digest"] = (
        split_event_evidence_results_review_package_digest_v1(package)
    )
    return package


def _verified_outputs(
    output_root: Path,
    *,
    expected_output_digests: Mapping[str, str],
) -> tuple[dict[str, dict[str, Any]], list[dict[str, Any]]]:
    payloads: dict[str, dict[str, Any]] = {}
    manifest: list[dict[str, Any]] = []
    for filename in EXPECTED_OUTPUT_FILENAMES_SORTED:
        path = output_root / filename
        if not path.is_file():
            raise SplitEventEvidenceResultsReviewError(f"{filename} missing")
        data = path.read_bytes()
        digest = sha256_bytes(data)
        expected_digest = expected_output_digests.get(filename)
        if digest != expected_digest:
            raise SplitEventEvidenceResultsReviewError(f"{filename} digest mismatch")
        payload = _load_json_file(path)
        if payload.get("output_label") != RESEARCH_ONLY_NON_ACTIONABLE:
            raise SplitEventEvidenceResultsReviewError(f"{filename} output_label mismatch")
        if payload.get("evidence_scope") != READ_ONLY_SPLIT_EVENT_EVIDENCE_REQUESTS_ONLY:
            raise SplitEventEvidenceResultsReviewError(f"{filename} evidence_scope mismatch")
        if _contains_unredacted_sensitive_value(payload):
            raise SplitEventEvidenceResultsReviewError(f"{filename} contains unredacted sensitive value")
        forbidden = _forbidden_authority_or_raw_payload(payload)
        if forbidden:
            raise SplitEventEvidenceResultsReviewError(f"{filename} forbidden field {forbidden}")
        payloads[filename] = payload
        manifest.append(
            {
                "filename": filename,
                "sha256": digest,
                "expected_sha256": expected_digest,
                "semantic_digest": semantic_digest(payload),
                "output_label": payload["output_label"],
                "evidence_scope": payload["evidence_scope"],
                "verified": True,
            }
        )
    return payloads, manifest


def _per_ticker_summary(results_payload: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = results_payload.get("per_ticker_split_evidence_results")
    if not isinstance(rows, list):
        raise SplitEventEvidenceResultsReviewError("per_ticker_split_evidence_results missing")
    summary: list[dict[str, Any]] = []
    for item in rows:
        if not isinstance(item, Mapping):
            raise SplitEventEvidenceResultsReviewError("per-ticker split result must be an object")
        summary.append(
            {
                "ticker": item.get("ticker"),
                "split_provider_evidence_status": item.get("split_provider_evidence_status"),
                "split_event_count": item.get("split_event_count"),
                "provider_response_digest": item.get("provider_response_digest"),
                "sanitized_split_evidence_digest": item.get("sanitized_split_evidence_digest"),
                "split_absence_policy_status": item.get("split_absence_policy_status"),
            }
        )
    return summary


def _base_package() -> dict[str, Any]:
    return {
        "artifact_kind": ARTIFACT_KIND_SPLIT_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE,
        "schema_version": SCHEMA_VERSION_SPLIT_EVENT_EVIDENCE_RESULTS_REVIEW_V1,
        "created_offline": True,
        "provider_requests_made_in_review": False,
        "live_provider_transport_enabled_in_review": False,
        "split_provider_evidence_rerun_performed": False,
        "source_execution_artifact_kind": execution.ARTIFACT_KIND_SPLIT_PROVIDER_EVIDENCE_EXECUTED,
        "source_execution_status": execution.SPLIT_PROVIDER_EVIDENCE_EXECUTED_READ_ONLY,
        "source_split_provider_evidence_execution_digest": EXPECTED_SPLIT_PROVIDER_EVIDENCE_EXECUTION_DIGEST,
        "source_split_provider_evidence_request_approval_digest": EXPECTED_SPLIT_PROVIDER_EVIDENCE_REQUEST_APPROVAL_DIGEST,
        "split_provider_evidence_request_authorized": True,
        "ready_for_split_provider_evidence_execution": True,
        "provider_requests_made": True,
        "live_provider_transport_enabled": True,
        "split_provider_evidence_executed": True,
        "split_provider_evidence_results_created": True,
        "raw_provider_payloads_committed": False,
        "api_keys_stored_or_printed": False,
        "split_event_authority_candidate_created": True,
        "split_event_authority_review_created": True,
        "split_event_authority_created": False,
        "split_event_authority_frozen": False,
        "dividend_event_authority_candidate_created": True,
        "dividend_event_authority_review_created": True,
        "dividend_provider_evidence_request_authorized": False,
        "dividend_provider_evidence_executed": False,
        "dividend_event_authority_created": False,
        "dividend_event_authority_frozen": False,
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
        "operator_review_required": True,
        "split_provider_evidence_execution_digest": EXPECTED_SPLIT_PROVIDER_EVIDENCE_EXECUTION_DIGEST,
        "split_provider_evidence_request_approval_digest": EXPECTED_SPLIT_PROVIDER_EVIDENCE_REQUEST_APPROVAL_DIGEST,
        "split_event_authority_candidate_review_package_digest": (
            approval.EXPECTED_SPLIT_EVENT_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST
        ),
        "split_event_authority_candidate_digest": approval.EXPECTED_SPLIT_EVENT_AUTHORITY_CANDIDATE_DIGEST,
        "dividend_event_authority_candidate_review_package_digest": (
            approval.EXPECTED_DIVIDEND_EVENT_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST
        ),
        "dividend_event_authority_candidate_digest": approval.EXPECTED_DIVIDEND_EVENT_AUTHORITY_CANDIDATE_DIGEST,
        "corporate_action_authority_plan_approval_digest": (
            approval.EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_APPROVAL_DIGEST
        ),
        "post_identity_freeze_registry_inventory_approval_digest": (
            approval.EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_APPROVAL_DIGEST
        ),
        "identity_authority_freeze_digest": approval.EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST,
        "ticker_universe_selection_approval_digest": approval.EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST,
        "target_universe": list(EXPECTED_TARGET_UNIVERSE),
        "target_universe_count": 12,
        "endpoint": EXPECTED_RESULT_FACTS["endpoint"],
        "endpoint_mode": EXPECTED_RESULT_FACTS["endpoint_mode"],
        "transport_mode": EXPECTED_RESULT_FACTS["transport_mode"],
        "limitations": list(LIMITATIONS),
        "next_gates": list(NEXT_GATES),
        "split_evidence_results_available": True,
        "all_provider_requests_succeeded": True,
        "split_evidence_review_supports_future_split_authority_planning": True,
        "split_evidence_creates_split_authority": False,
        "split_evidence_creates_corporate_action_authority": False,
        "split_evidence_creates_acquisition_authority": False,
        "split_evidence_creates_dataset_generation_authority": False,
        "split_event_authority_artifact_created": False,
        "split_event_authority_freeze_created": False,
        "dividend_provider_evidence_request_created": False,
        "dividend_event_authority_artifact_created": False,
        "corporate_action_authority_artifact_created": False,
        "acquisition_authorization_created": False,
        "dataset_generation_authorization_created": False,
        "predictive_usefulness_acceptance_artifact_created": False,
        "profitability_acceptance_created": False,
        "runtime_migration_approval_created": False,
    }


def build_split_event_evidence_results_review_package_v1(
    *,
    output_root: str | Path | None = None,
    expected_output_digests: Mapping[str, str] | None = None,
) -> dict[str, Any]:
    """Build the offline split evidence results review package from sanitized outputs."""
    root = Path(output_root) if output_root is not None else execution.OUTPUT_ROOT
    expected_digests = dict(expected_output_digests or EXPECTED_OUTPUT_DIGESTS)
    try:
        payloads, output_manifest = _verified_outputs(root, expected_output_digests=expected_digests)
    except SplitEventEvidenceResultsReviewError as exc:
        return _blocked_package(str(exc))

    run_manifest = payloads["split_provider_evidence_run_manifest.json"]
    results_payload = payloads["split_event_results_sanitized.json"]
    failure_payload = payloads["split_event_failure_reason_inventory.json"]
    summary = run_manifest.get("execution_summary")
    if not isinstance(summary, dict):
        return _blocked_package("execution summary missing")
    per_ticker = _per_ticker_summary(results_payload)
    package = _base_package()
    package.update(
        {
            "review_status": SPLIT_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE_READY,
            "output_root": root.as_posix(),
            "output_file_inspection_performed": True,
            "outputs_verified": True,
            "provider_request_count": summary.get("provider_request_count"),
            "successful_provider_response_count": summary.get("successful_provider_response_count"),
            "failed_provider_response_count": summary.get("failed_provider_response_count"),
            "split_evidence_collected_count": summary.get("split_evidence_collected_count"),
            "no_split_events_returned_count": summary.get("no_split_events_returned_count"),
            "not_evaluated_count": summary.get("not_evaluated_count"),
            "generated_output_count": summary.get("generated_output_count"),
            "failure_count": summary.get("failure_count"),
            "warning_count": summary.get("warning_count"),
            "per_ticker_split_evidence_summary": per_ticker,
            "output_digest_manifest": output_manifest,
            "reviewed_failure_inventory": failure_payload.get("split_event_failure_reason_inventory", []),
            "ready_for_split_event_discrepancy_triage": bool(failure_payload.get("split_event_failure_reason_inventory")),
            "ready_for_split_event_authority_freeze": False,
            "next_required_task": "SPLIT_EVENT_EVIDENCE_RESULTS_OPERATOR_REVIEW",
        }
    )
    checklist = _review_checklist(package)
    package["review_checklist"] = checklist
    package["review_summary"] = _summary(checklist)
    package["split_event_evidence_results_review_package_digest"] = (
        split_event_evidence_results_review_package_digest_v1(package)
    )
    validate_split_event_evidence_results_review_package_v1(package)
    return package


def _check(check_id: str, expected: Any, actual: Any, *, message: str | None = None) -> dict[str, Any]:
    status = PASS if actual == expected else FAIL
    return {
        "check_id": check_id,
        "status": status,
        "expected": expected,
        "actual": actual,
        "severity": BLOCKER,
        "message": message or ("review evidence matches" if status == PASS else "review evidence mismatch"),
    }


def _summary(checklist: list[dict[str, Any]]) -> dict[str, Any]:
    failed = [item for item in checklist if item.get("status") != PASS]
    blockers = [item for item in failed if item.get("severity") == BLOCKER]
    return {
        "total_checks": len(checklist),
        "passed_checks": len(checklist) - len(failed),
        "failed_checks": len(failed),
        "blocker_count": len(blockers),
        "ready_for_operator_review": not failed,
        "ready_for_split_event_authority_freeze": False,
        "ready_for_split_event_discrepancy_triage": False,
        "split_event_authority_authorized": False,
        "split_event_authority_frozen": False,
        "dividend_provider_evidence_request_authorized": False,
        "dividend_event_authority_authorized": False,
        "corporate_action_authority_authorized": False,
        "acquisition_authorized": False,
        "dataset_generation_authorized": False,
        "additional_predictive_evidence_execution_authorized": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_migration_authorized": False,
        "software_runtime_activation_authorized": False,
    }


def _review_checklist(package: dict[str, Any]) -> list[dict[str, Any]]:
    manifest_names = [item.get("filename") for item in package.get("output_digest_manifest", [])]
    return [
        _check("split_provider_evidence_execution_digest_bound", EXPECTED_SPLIT_PROVIDER_EVIDENCE_EXECUTION_DIGEST, package.get("split_provider_evidence_execution_digest")),
        _check("split_provider_evidence_request_approval_digest_bound", EXPECTED_SPLIT_PROVIDER_EVIDENCE_REQUEST_APPROVAL_DIGEST, package.get("split_provider_evidence_request_approval_digest")),
        _check("split_candidate_review_digest_bound", approval.EXPECTED_SPLIT_EVENT_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST, package.get("split_event_authority_candidate_review_package_digest")),
        _check("split_candidate_digest_bound", approval.EXPECTED_SPLIT_EVENT_AUTHORITY_CANDIDATE_DIGEST, package.get("split_event_authority_candidate_digest")),
        _check("dividend_candidate_review_digest_bound", approval.EXPECTED_DIVIDEND_EVENT_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST, package.get("dividend_event_authority_candidate_review_package_digest")),
        _check("corporate_action_plan_approval_digest_bound", approval.EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_APPROVAL_DIGEST, package.get("corporate_action_authority_plan_approval_digest")),
        _check("identity_freeze_digest_bound", approval.EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST, package.get("identity_authority_freeze_digest")),
        _check("target_universe_count_12", 12, package.get("target_universe_count")),
        _check("target_universe_matches_execution_universe", EXPECTED_TARGET_UNIVERSE, package.get("target_universe")),
        _check("provider_request_count_12", 12, package.get("provider_request_count")),
        _check("successful_provider_response_count_12", 12, package.get("successful_provider_response_count")),
        _check("failed_provider_response_count_zero", 0, package.get("failed_provider_response_count")),
        _check("split_evidence_collected_count_7", 7, package.get("split_evidence_collected_count")),
        _check("no_split_events_returned_count_5", 5, package.get("no_split_events_returned_count")),
        _check("generated_output_count_6", 6, package.get("generated_output_count")),
        _check("output_digests_bound", EXPECTED_OUTPUT_FILENAMES_SORTED, sorted(manifest_names)),
        _check("outputs_research_only_non_actionable", True, all(item.get("output_label") == RESEARCH_ONLY_NON_ACTIONABLE for item in package.get("output_digest_manifest", []))),
        _check("evidence_scope_read_only_split_event_evidence_requests_only", True, all(item.get("evidence_scope") == READ_ONLY_SPLIT_EVENT_EVIDENCE_REQUESTS_ONLY for item in package.get("output_digest_manifest", []))),
        _check("raw_provider_payloads_not_committed", False, package.get("raw_provider_payloads_committed")),
        _check("api_keys_not_stored_or_printed", False, package.get("api_keys_stored_or_printed")),
        _check("provider_requests_made_in_review_false", False, package.get("provider_requests_made_in_review")),
        _check("split_provider_evidence_rerun_performed_false", False, package.get("split_provider_evidence_rerun_performed")),
        _check("live_provider_transport_enabled_in_review_false", False, package.get("live_provider_transport_enabled_in_review")),
        _check("split_event_authority_created_false", False, package.get("split_event_authority_created")),
        _check("split_event_authority_frozen_false", False, package.get("split_event_authority_frozen")),
        _check("dividend_provider_evidence_request_authorized_false", False, package.get("dividend_provider_evidence_request_authorized")),
        _check("dividend_provider_evidence_executed_false", False, package.get("dividend_provider_evidence_executed")),
        _check("dividend_event_authority_created_false", False, package.get("dividend_event_authority_created")),
        _check("dividend_event_authority_frozen_false", False, package.get("dividend_event_authority_frozen")),
        _check("corporate_action_authority_created_false", False, package.get("corporate_action_authority_created")),
        _check("new_ticker_acquisition_authorized_false", False, package.get("new_ticker_acquisition_authorized")),
        _check("dataset_generation_authorized_false", False, package.get("dataset_generation_authorized")),
        _check("acquisition_generation_authorized_false", False, package.get("acquisition_generation_authorized")),
        _check("canonical_dataset_authorized_false", False, package.get("canonical_dataset_authorized")),
        _check("registry_approval_created_false", False, package.get("registry_approval_created")),
        _check("additional_predictive_evidence_execution_authorized_false", False, package.get("additional_predictive_evidence_execution_authorized")),
        _check("additional_predictive_evidence_executed_false", False, package.get("additional_predictive_evidence_executed")),
        _check("predictive_experiment_rerun_authorized_false", False, package.get("predictive_experiment_rerun_authorized")),
        _check("predictive_experiment_rerun_performed_false", False, package.get("predictive_experiment_rerun_performed")),
        _check("walk_forward_rerun_performed_false", False, package.get("walk_forward_rerun_performed")),
        _check("label_regeneration_performed_false", False, package.get("label_regeneration_performed")),
        _check("feature_matrix_regeneration_performed_false", False, package.get("feature_matrix_regeneration_performed")),
        _check("new_strategy_scoring_performed_false", False, package.get("new_strategy_scoring_performed")),
        _check("trade_recommendations_generated_false", False, package.get("trade_recommendations_generated")),
        _check("predictive_usefulness_not_accepted", _not_accepted(), package.get("predictive_usefulness")),
        _check("profitability_not_accepted", acquisition.PROFITABILITY_NOT_ACCEPTED, package.get("profitability")),
        _check("runtime_migration_approved_false", False, package.get("runtime_migration_approved")),
        _check("runtime_use_not_authorized", NOT_AUTHORIZED, package.get("runtime_use")),
        _check("strategy_use_not_authorized", NOT_AUTHORIZED, package.get("strategy_use")),
        _check("paper_trading_not_authorized", NOT_AUTHORIZED, package.get("paper_trading")),
        _check("broker_execution_not_authorized", NOT_AUTHORIZED, package.get("broker_execution")),
        _check("automatic_stitching_false", False, package.get("automatic_stitching")),
        _check("split_evidence_supports_future_split_authority_planning_true", True, package.get("split_evidence_review_supports_future_split_authority_planning")),
        _check("split_evidence_creates_split_authority_false", False, package.get("split_evidence_creates_split_authority")),
        _check("split_evidence_creates_corporate_action_authority_false", False, package.get("split_evidence_creates_corporate_action_authority")),
        _check("split_evidence_creates_acquisition_authority_false", False, package.get("split_evidence_creates_acquisition_authority")),
        _check("split_evidence_creates_dataset_generation_authority_false", False, package.get("split_evidence_creates_dataset_generation_authority")),
        _check("limitations_recorded", LIMITATIONS, package.get("limitations")),
        _check("next_gates_defined", NEXT_GATES, package.get("next_gates")),
        _check("no_split_event_authority_artifact_created", False, package.get("split_event_authority_artifact_created")),
        _check("no_split_event_authority_freeze_created", False, package.get("split_event_authority_freeze_created")),
        _check("no_dividend_provider_evidence_request_created", False, package.get("dividend_provider_evidence_request_created")),
        _check("no_dividend_event_authority_artifact_created", False, package.get("dividend_event_authority_artifact_created")),
        _check("no_corporate_action_authority_artifact_created", False, package.get("corporate_action_authority_artifact_created")),
        _check("no_acquisition_authorization_created", False, package.get("acquisition_authorization_created")),
        _check("no_dataset_generation_authorization_created", False, package.get("dataset_generation_authorization_created")),
        _check("no_predictive_usefulness_acceptance_artifact_created", False, package.get("predictive_usefulness_acceptance_artifact_created")),
        _check("no_profitability_acceptance_created", False, package.get("profitability_acceptance_created")),
        _check("no_runtime_migration_approval_created", False, package.get("runtime_migration_approval_created")),
    ]


def _expect(actual: Any, expected: Any, field_name: str) -> None:
    if actual != expected:
        raise SplitEventEvidenceResultsReviewError(f"{field_name} mismatch")


def _expect_true(actual: Any, field_name: str) -> None:
    if actual is not True:
        raise SplitEventEvidenceResultsReviewError(f"{field_name} must be true")


def _expect_false(actual: Any, field_name: str) -> None:
    if actual is not False:
        raise SplitEventEvidenceResultsReviewError(f"{field_name} must be false")


def _expect_digest(actual: Any, field_name: str) -> None:
    if not isinstance(actual, str) or len(actual) != 64:
        raise SplitEventEvidenceResultsReviewError(f"{field_name} missing")


def validate_split_event_evidence_results_review_package_v1(
    review_package: dict[str, Any],
) -> dict[str, Any]:
    """Validate the split evidence results review package and authority boundaries."""
    if not isinstance(review_package, dict):
        raise SplitEventEvidenceResultsReviewError("review_package must be a JSON object")
    _expect(review_package.get("artifact_kind"), ARTIFACT_KIND_SPLIT_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE, "artifact_kind")
    _expect(review_package.get("schema_version"), SCHEMA_VERSION_SPLIT_EVENT_EVIDENCE_RESULTS_REVIEW_V1, "schema_version")
    if review_package.get("review_status") == SPLIT_EVENT_EVIDENCE_RESULTS_REVIEW_BLOCKED_MISSING_OR_INVALID_OUTPUTS:
        return {
            "status": "SPLIT_EVENT_EVIDENCE_RESULTS_REVIEW_BLOCKED_VALID",
            "review_status": review_package["review_status"],
            "split_event_evidence_results_review_package_digest": review_package.get("split_event_evidence_results_review_package_digest"),
        }
    _expect(review_package.get("review_status"), SPLIT_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE_READY, "review_status")
    for field in (
        "created_offline",
        "split_provider_evidence_request_authorized",
        "ready_for_split_provider_evidence_execution",
        "provider_requests_made",
        "live_provider_transport_enabled",
        "split_provider_evidence_executed",
        "split_provider_evidence_results_created",
        "split_event_authority_candidate_created",
        "split_event_authority_review_created",
        "dividend_event_authority_candidate_created",
        "dividend_event_authority_review_created",
        "corporate_action_authority_plan_approved",
        "research_only",
        "operator_review_required",
        "output_file_inspection_performed",
        "outputs_verified",
        "split_evidence_results_available",
        "all_provider_requests_succeeded",
        "split_evidence_review_supports_future_split_authority_planning",
    ):
        _expect_true(review_package.get(field), field)
    for field in (
        "provider_requests_made_in_review",
        "live_provider_transport_enabled_in_review",
        "split_provider_evidence_rerun_performed",
        "raw_provider_payloads_committed",
        "api_keys_stored_or_printed",
        "split_event_authority_created",
        "split_event_authority_frozen",
        "dividend_provider_evidence_request_authorized",
        "dividend_provider_evidence_executed",
        "dividend_event_authority_created",
        "dividend_event_authority_frozen",
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
        "split_evidence_creates_split_authority",
        "split_evidence_creates_corporate_action_authority",
        "split_evidence_creates_acquisition_authority",
        "split_evidence_creates_dataset_generation_authority",
        "split_event_authority_artifact_created",
        "split_event_authority_freeze_created",
        "dividend_provider_evidence_request_created",
        "dividend_event_authority_artifact_created",
        "corporate_action_authority_artifact_created",
        "acquisition_authorization_created",
        "dataset_generation_authorization_created",
        "predictive_usefulness_acceptance_artifact_created",
        "profitability_acceptance_created",
        "runtime_migration_approval_created",
    ):
        _expect_false(review_package.get(field), field)
    for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
        _expect(review_package.get(field), NOT_AUTHORIZED, field)
    expected_fields = {
        "source_execution_artifact_kind": execution.ARTIFACT_KIND_SPLIT_PROVIDER_EVIDENCE_EXECUTED,
        "source_execution_status": execution.SPLIT_PROVIDER_EVIDENCE_EXECUTED_READ_ONLY,
        "source_split_provider_evidence_execution_digest": EXPECTED_SPLIT_PROVIDER_EVIDENCE_EXECUTION_DIGEST,
        "source_split_provider_evidence_request_approval_digest": EXPECTED_SPLIT_PROVIDER_EVIDENCE_REQUEST_APPROVAL_DIGEST,
        "split_provider_evidence_execution_digest": EXPECTED_SPLIT_PROVIDER_EVIDENCE_EXECUTION_DIGEST,
        "split_provider_evidence_request_approval_digest": EXPECTED_SPLIT_PROVIDER_EVIDENCE_REQUEST_APPROVAL_DIGEST,
        "split_event_authority_candidate_review_package_digest": approval.EXPECTED_SPLIT_EVENT_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "split_event_authority_candidate_digest": approval.EXPECTED_SPLIT_EVENT_AUTHORITY_CANDIDATE_DIGEST,
        "dividend_event_authority_candidate_review_package_digest": approval.EXPECTED_DIVIDEND_EVENT_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "corporate_action_authority_plan_approval_digest": approval.EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_APPROVAL_DIGEST,
        "identity_authority_freeze_digest": approval.EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST,
        "target_universe": EXPECTED_TARGET_UNIVERSE,
        "target_universe_count": 12,
        "endpoint": EXPECTED_RESULT_FACTS["endpoint"],
        "endpoint_mode": EXPECTED_RESULT_FACTS["endpoint_mode"],
        "transport_mode": EXPECTED_RESULT_FACTS["transport_mode"],
        "provider_request_count": 12,
        "successful_provider_response_count": 12,
        "failed_provider_response_count": 0,
        "split_evidence_collected_count": 7,
        "no_split_events_returned_count": 5,
        "generated_output_count": 6,
        "failure_count": 0,
        "warning_count": 12,
        "predictive_usefulness": _not_accepted(),
        "profitability": acquisition.PROFITABILITY_NOT_ACCEPTED,
        "limitations": LIMITATIONS,
        "next_gates": NEXT_GATES,
    }
    for field, expected in expected_fields.items():
        _expect(review_package.get(field), expected, field)
    if not review_package.get("output_digest_manifest"):
        raise SplitEventEvidenceResultsReviewError("output_digest_manifest missing")
    per_ticker = review_package.get("per_ticker_split_evidence_summary")
    if not isinstance(per_ticker, list) or len(per_ticker) != 12:
        raise SplitEventEvidenceResultsReviewError("per_ticker_split_evidence_summary mismatch")
    _expect([item.get("ticker") for item in per_ticker], EXPECTED_TARGET_UNIVERSE, "per_ticker tickers")
    _expect(
        {item.get("ticker"): item.get("split_provider_evidence_status") for item in per_ticker},
        EXPECTED_PER_TICKER_STATUS,
        "per_ticker split evidence status",
    )
    for item in review_package["output_digest_manifest"]:
        if item.get("output_label") != RESEARCH_ONLY_NON_ACTIONABLE:
            raise SplitEventEvidenceResultsReviewError("output labels must be research-only")
        if item.get("evidence_scope") != READ_ONLY_SPLIT_EVENT_EVIDENCE_REQUESTS_ONLY:
            raise SplitEventEvidenceResultsReviewError("output evidence_scope mismatch")
        _expect_digest(item.get("sha256"), "output sha256")
    if [item.get("check_id") for item in review_package.get("review_checklist", [])] != REQUIRED_CHECK_IDS:
        raise SplitEventEvidenceResultsReviewError("review checklist check IDs mismatch")
    failed = [item for item in review_package["review_checklist"] if item.get("status") != PASS]
    if failed:
        raise SplitEventEvidenceResultsReviewError(f"review checklist failed: {failed[0]['check_id']}")
    _expect(review_package.get("review_summary"), _summary(review_package["review_checklist"]), "review_summary")
    digest = review_package.get("split_event_evidence_results_review_package_digest")
    _expect_digest(digest, "split_event_evidence_results_review_package_digest")
    _expect(digest, split_event_evidence_results_review_package_digest_v1(review_package), "split_event_evidence_results_review_package_digest")
    return {
        "status": "SPLIT_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE_VALID",
        "artifact_kind": review_package["artifact_kind"],
        "review_status": review_package["review_status"],
        "split_event_evidence_results_review_package_digest": digest,
        "source_split_provider_evidence_execution_digest": review_package["source_split_provider_evidence_execution_digest"],
        "split_provider_evidence_request_approval_digest": review_package["split_provider_evidence_request_approval_digest"],
        "provider_request_count": review_package["provider_request_count"],
        "successful_provider_response_count": review_package["successful_provider_response_count"],
        "failed_provider_response_count": review_package["failed_provider_response_count"],
        "split_evidence_collected_count": review_package["split_evidence_collected_count"],
        "no_split_events_returned_count": review_package["no_split_events_returned_count"],
        "generated_output_count": review_package["generated_output_count"],
        "failure_count": review_package["failure_count"],
        "warning_count": review_package["warning_count"],
        "total_checks": review_package["review_summary"]["total_checks"],
        "passed_checks": review_package["review_summary"]["passed_checks"],
        "failed_checks": review_package["review_summary"]["failed_checks"],
        "blocker_count": review_package["review_summary"]["blocker_count"],
    }


def build_split_event_evidence_results_review_markdown_v1(review_package: dict[str, Any]) -> str:
    """Render a sanitized Markdown status view for the review package."""
    validation = validate_split_event_evidence_results_review_package_v1(review_package)
    lines = [
        "# MarketFlow Split Event Evidence Results Review Status",
        "",
        "## Title",
        "- Split Event Evidence Results Review Package v1.",
        "",
        "## Reviewed Split Provider Evidence Execution",
        f"- Review artifact: `{review_package['artifact_kind']}`",
        f"- Review status: `{review_package['review_status']}`",
        f"- Review package digest: `{validation['split_event_evidence_results_review_package_digest']}`",
        f"- Source execution digest: `{review_package['source_split_provider_evidence_execution_digest']}`",
        "",
        "## Source Evidence",
        f"- Split request approval digest: `{review_package['split_provider_evidence_request_approval_digest']}`",
        f"- Split candidate review digest: `{review_package['split_event_authority_candidate_review_package_digest']}`",
        f"- Split candidate digest: `{review_package['split_event_authority_candidate_digest']}`",
        "",
        "## Target Universe",
        f"- Target universe count: `{review_package['target_universe_count']}`",
        "- Target universe: " + ", ".join(f"`{ticker}`" for ticker in review_package["target_universe"]),
        "",
        "## Provider Request Summary",
        f"- Endpoint: `{review_package['endpoint']}`",
        f"- Endpoint mode: `{review_package['endpoint_mode']}`",
        f"- Transport mode: `{review_package['transport_mode']}`",
        f"- Provider request count: `{review_package['provider_request_count']}`",
        f"- Successful provider response count: `{review_package['successful_provider_response_count']}`",
        f"- Failed provider response count: `{review_package['failed_provider_response_count']}`",
        f"- Failure/warning count: `{review_package['failure_count']} / {review_package['warning_count']}`",
        "",
        "## Per-Ticker Split Evidence Summary",
    ]
    lines.extend(
        f"- `{item['ticker']}`: `{item['split_provider_evidence_status']}`, events `{item['split_event_count']}`"
        for item in review_package["per_ticker_split_evidence_summary"]
    )
    lines.extend(
        [
            "",
            "## Output Digest Manifest",
            *[
                f"- `{item['filename']}`: `{item['sha256']}`"
                for item in review_package["output_digest_manifest"]
            ],
            "",
            "## No-Split Event Policy Summary",
            "- No-split provider responses require explicit absence-policy review.",
            "- No-split responses are read-only evidence for review, not split authority.",
            "",
            "## Limitations",
            *[f"- `{item}`" for item in review_package["limitations"]],
            "",
            "## Next Gates",
            *[f"- `{item}`" for item in review_package["next_gates"]],
            "",
            "## Split Authority Boundary",
            f"- split_event_authority_created: `{review_package['split_event_authority_created']}`",
            f"- split_event_authority_frozen: `{review_package['split_event_authority_frozen']}`",
            "",
            "## Dividend Boundary",
            f"- dividend_provider_evidence_request_authorized: `{review_package['dividend_provider_evidence_request_authorized']}`",
            f"- dividend_event_authority_created: `{review_package['dividend_event_authority_created']}`",
            "",
            "## Corporate-Action Authority Boundary",
            f"- corporate_action_authority_created: `{review_package['corporate_action_authority_created']}`",
            "",
            "## Acquisition Boundary",
            f"- new_ticker_acquisition_authorized: `{review_package['new_ticker_acquisition_authorized']}`",
            "",
            "## Dataset Boundary",
            f"- dataset_generation_authorized: `{review_package['dataset_generation_authorized']}`",
            "",
            "## Predictive/Profitability Boundary",
            f"- predictive_usefulness: `{review_package['predictive_usefulness']}`",
            f"- profitability: `{review_package['profitability']}`",
            "",
            "## Runtime Boundary",
            f"- runtime_use: `{review_package['runtime_use']}`",
            f"- strategy_use: `{review_package['strategy_use']}`",
            f"- paper_trading: `{review_package['paper_trading']}`",
            f"- broker_execution: `{review_package['broker_execution']}`",
            "",
            "## Checklist Summary",
            f"- Total checks: `{review_package['review_summary']['total_checks']}`",
            f"- Passed checks: `{review_package['review_summary']['passed_checks']}`",
            f"- Failed checks: `{review_package['review_summary']['failed_checks']}`",
            f"- Blocker count: `{review_package['review_summary']['blocker_count']}`",
            "",
            "## Guardrails",
            "- No provider requests were made in review.",
            "- No split evidence rerun occurred.",
            "- No live provider transport was enabled in review.",
            "- No split authority or freeze was created.",
        ]
    )
    return "\n".join(lines) + "\n"


def write_split_event_evidence_results_review_package_v1(
    output_dir: str | Path,
    *,
    output_root: str | Path | None = None,
    expected_output_digests: Mapping[str, str] | None = None,
) -> dict[str, Any]:
    """Write the review package JSON without overwriting an existing artifact."""
    package = build_split_event_evidence_results_review_package_v1(
        output_root=output_root,
        expected_output_digests=expected_output_digests,
    )
    validation = validate_split_event_evidence_results_review_package_v1(package)
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "split_event_evidence_results_review_package_v1.json"
    if path.exists():
        raise SplitEventEvidenceResultsReviewError("split evidence results review package output already exists")
    payload = canonical_json_bytes(package)
    path.write_bytes(payload)
    return {
        "path": str(path),
        "artifact_kind": package["artifact_kind"],
        "review_status": package["review_status"],
        "split_event_evidence_results_review_package_digest": validation.get("split_event_evidence_results_review_package_digest"),
        "payload_sha256": sha256_bytes(payload),
    }
