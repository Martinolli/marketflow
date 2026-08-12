"""Offline review package for dividend provider evidence execution results."""

from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
from typing import Any, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import acquisition_generation_service as acquisition
from marketflow.services import dividend_provider_evidence_execution_service as execution
from marketflow.services import dividend_provider_evidence_request_approval_service as approval


ARTIFACT_KIND_DIVIDEND_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE = (
    "DIVIDEND_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE"
)
SCHEMA_VERSION_DIVIDEND_EVENT_EVIDENCE_RESULTS_REVIEW_V1 = (
    "dividend_event_evidence_results_review_v1"
)
DIVIDEND_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE_READY = (
    "DIVIDEND_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE_READY"
)
DIVIDEND_EVENT_EVIDENCE_RESULTS_REVIEW_BLOCKED_MISSING_OR_INVALID_OUTPUTS = (
    "DIVIDEND_EVENT_EVIDENCE_RESULTS_REVIEW_BLOCKED_MISSING_OR_INVALID_OUTPUTS"
)

RESEARCH_ONLY_NON_ACTIONABLE = execution.RESEARCH_ONLY_NON_ACTIONABLE
READ_ONLY_DIVIDEND_EVENT_EVIDENCE_REQUESTS_ONLY = (
    execution.READ_ONLY_DIVIDEND_EVENT_EVIDENCE_REQUESTS_ONLY
)
NOT_AUTHORIZED = execution.NOT_AUTHORIZED
PASS = execution.PASS
FAIL = execution.FAIL
BLOCKER = execution.BLOCKER

EXPECTED_DIVIDEND_PROVIDER_EVIDENCE_EXECUTION_DIGEST = (
    "4759a412411f7019090bd89ebc1d44040f5b2fe895074ccc9a08c21852b009d9"
)
EXPECTED_DIVIDEND_PROVIDER_EVIDENCE_REQUEST_APPROVAL_DIGEST = (
    execution.EXPECTED_DIVIDEND_PROVIDER_EVIDENCE_REQUEST_APPROVAL_DIGEST
)
EXPECTED_TARGET_UNIVERSE = list(execution.TARGET_UNIVERSE)
EXPECTED_OUTPUT_DIGESTS = {
    "dividend_provider_evidence_run_manifest.json": "af21c88ccbe48c0d58f0f39fc576abc65eea38f8df25d2a40bab1e3efa754928",
    "dividend_provider_request_receipts_sanitized.json": "2fd6e2a7d1098e862d84d8f2fcd677a1b1b1a8f4edb4b123eb8f7d94665a00f4",
    "dividend_event_results_sanitized.json": "4f13c7141dee6089c62b1e49ce9f5ead6b64c351bdf5462c47d05e31681811e7",
    "dividend_event_absence_inventory.json": "c0e1e61dc17a9fb810ce390612e217b42479ec111226c18c5e060bff134f6c70",
    "dividend_policy_reconciliation_report.json": "542b212d1343c105b8556a945056c6c59a1b505e39496482111e3caf2aa5f24c",
    "dividend_event_failure_reason_inventory.json": "e1fe0b1364f5afd66222bb36deaf631e06d3769db5e7f9a19c67bdf63b00a3e8",
    "operator_review_summary.json": "b71ebc584c6c00295fe3b2ceb7271ead69362dacecfbac0132af46ef112da234",
}
EXPECTED_OUTPUT_FILENAMES_SORTED = sorted(EXPECTED_OUTPUT_DIGESTS)
EXPECTED_RESULT_FACTS = {
    "endpoint": "/stocks/v1/dividends",
    "endpoint_mode": "CURRENT_STOCKS_V1_DIVIDENDS",
    "transport_mode": "LIVE_HTTP_TRANSPORT_READ_ONLY",
    "target_count": 12,
    "provider_request_count": 12,
    "successful_provider_response_count": 12,
    "failed_provider_response_count": 0,
    "dividend_evidence_collected_count": 10,
    "no_dividend_events_returned_count": 2,
    "generated_output_count": 7,
    "failure_count": 0,
    "warning_count": 12,
}
EXPECTED_PER_TICKER = {
    "MSFT": (execution.DIVIDEND_EVIDENCE_COLLECTED_READ_ONLY, 89),
    "NVDA": (execution.DIVIDEND_EVIDENCE_COLLECTED_READ_ONLY, 55),
    "AMZN": (execution.NO_DIVIDEND_EVENTS_RETURNED_BY_PROVIDER, 0),
    "GOOGL": (execution.DIVIDEND_EVIDENCE_COLLECTED_READ_ONLY, 9),
    "META": (execution.DIVIDEND_EVIDENCE_COLLECTED_READ_ONLY, 10),
    "TSLA": (execution.NO_DIVIDEND_EVENTS_RETURNED_BY_PROVIDER, 0),
    "JPM": (execution.DIVIDEND_EVIDENCE_COLLECTED_READ_ONLY, 91),
    "XOM": (execution.DIVIDEND_EVIDENCE_COLLECTED_READ_ONLY, 90),
    "JNJ": (execution.DIVIDEND_EVIDENCE_COLLECTED_READ_ONLY, 90),
    "WMT": (execution.DIVIDEND_EVIDENCE_COLLECTED_READ_ONLY, 92),
    "CAT": (execution.DIVIDEND_EVIDENCE_COLLECTED_READ_ONLY, 91),
    "LMT": (execution.DIVIDEND_EVIDENCE_COLLECTED_READ_ONLY, 90),
}
LIMITATIONS = [
    "dividend_evidence_read_only_provider_snapshot_at_execution_time",
    "zero_dividend_events_returned_requires_explicit_absence_policy_review",
    "dividend_policy_reconciliation_required_before_dividend_freeze",
    "dividend_adjustment_policy_not_approved",
    "total_return_not_assumed",
    "dividend_reinvestment_not_assumed",
    "dividend_authority_not_created",
    "dividend_freeze_not_created",
    "corporate_action_authority_not_created",
    "acquisition_authority_not_created",
    "dataset_generation_not_authorized",
    "operator_review_required_before_dividend_authority_freeze",
]
NEXT_GATES = [
    "dividend_event_evidence_results_operator_review",
    "dividend_policy_reconciliation_review",
    "dividend_event_discrepancy_triage_if_required",
    "dividend_event_authority_freeze_ceremony",
    "combined_split_dividend_corporate_action_readiness_review",
    "corporate_action_authority_approval_if_required",
    "acquisition_generation_chain_candidate",
    "canonical_dataset_chain_candidate",
    "research_registry_chain_candidate",
]
DIVIDEND_POLICY_RECONCILIATION_REQUIREMENTS = [
    "cash_dividend_adjustment_policy_requires_operator_review",
    "total_return_not_assumed",
    "dividend_reinvestment_not_assumed",
    "operator_review_required_before_dividend_freeze",
]
REQUIRED_CHECK_IDS = [
    "dividend_provider_evidence_execution_digest_bound",
    "dividend_provider_evidence_request_approval_digest_bound",
    "dividend_candidate_review_digest_bound",
    "dividend_candidate_digest_bound",
    "split_authority_freeze_digest_bound",
    "split_evidence_results_review_digest_bound",
    "corporate_action_plan_approval_digest_bound",
    "identity_freeze_digest_bound",
    "target_universe_count_12",
    "target_universe_matches_execution_universe",
    "provider_request_count_12",
    "successful_provider_response_count_12",
    "failed_provider_response_count_zero",
    "dividend_evidence_collected_count_10",
    "no_dividend_events_returned_count_2",
    "generated_output_count_7",
    "output_digests_bound",
    "outputs_research_only_non_actionable",
    "evidence_scope_read_only_dividend_event_evidence_requests_only",
    "raw_provider_payloads_not_committed",
    "api_keys_not_stored_or_printed",
    "provider_requests_made_in_review_false",
    "dividend_provider_evidence_rerun_performed_false",
    "live_provider_transport_enabled_in_review_false",
    "dividend_event_authority_created_false",
    "dividend_event_authority_frozen_false",
    "split_event_authority_created_true",
    "split_event_authority_frozen_true",
    "split_provider_evidence_rerun_performed_false",
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
    "dividend_evidence_supports_future_dividend_authority_planning_true",
    "dividend_policy_reconciliation_requires_operator_review_true",
    "dividend_evidence_creates_dividend_authority_false",
    "dividend_evidence_creates_corporate_action_authority_false",
    "dividend_evidence_creates_acquisition_authority_false",
    "dividend_evidence_creates_dataset_generation_authority_false",
    "limitations_recorded",
    "next_gates_defined",
    "no_dividend_event_authority_artifact_created",
    "no_dividend_event_authority_freeze_created",
    "no_corporate_action_authority_artifact_created",
    "no_acquisition_authorization_created",
    "no_dataset_generation_authorization_created",
    "no_predictive_usefulness_acceptance_artifact_created",
    "no_profitability_acceptance_created",
    "no_runtime_migration_approval_created",
]


class DividendEventEvidenceResultsReviewError(ValueError):
    """Raised when the dividend evidence results review package is invalid."""


def _not_accepted() -> str:
    return acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED


def _digest_payload(review_package: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(review_package)
    payload.pop("dividend_event_evidence_results_review_package_digest", None)
    return payload


def dividend_event_evidence_results_review_package_digest_v1(
    review_package: dict[str, Any],
) -> str:
    """Return the deterministic digest for a dividend evidence review package."""
    return semantic_digest(_digest_payload(review_package))


def _load_json_file(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise DividendEventEvidenceResultsReviewError(f"{path.name} is not readable JSON") from exc
    if not isinstance(payload, dict):
        raise DividendEventEvidenceResultsReviewError(f"{path.name} must contain a JSON object")
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


def _forbidden_output_field(payload: Mapping[str, Any]) -> str | None:
    forbidden_true = {
        "dividend_event_authority_created",
        "dividend_event_authority_frozen",
        "corporate_action_authority_created",
        "new_ticker_acquisition_authorized",
        "dataset_generation_authorized",
        "acquisition_generation_authorized",
        "canonical_dataset_authorized",
        "registry_approval_created",
        "raw_provider_payloads_committed",
        "raw_payload_committed",
        "raw_response_stored",
        "api_keys_stored_or_printed",
        "api_key_stored_or_printed",
    }
    for key, value in payload.items():
        if key in forbidden_true and value is True:
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
        "artifact_kind": ARTIFACT_KIND_DIVIDEND_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE,
        "schema_version": SCHEMA_VERSION_DIVIDEND_EVENT_EVIDENCE_RESULTS_REVIEW_V1,
        "created_offline": True,
        "provider_requests_made_in_review": False,
        "live_provider_transport_enabled_in_review": False,
        "dividend_provider_evidence_rerun_performed": False,
        "source_execution_artifact_kind": execution.ARTIFACT_KIND_DIVIDEND_PROVIDER_EVIDENCE_EXECUTED,
        "source_execution_status": execution.DIVIDEND_PROVIDER_EVIDENCE_EXECUTED_READ_ONLY,
        "source_dividend_provider_evidence_execution_digest": EXPECTED_DIVIDEND_PROVIDER_EVIDENCE_EXECUTION_DIGEST,
        "source_dividend_provider_evidence_request_approval_digest": EXPECTED_DIVIDEND_PROVIDER_EVIDENCE_REQUEST_APPROVAL_DIGEST,
        "dividend_provider_evidence_execution_digest": EXPECTED_DIVIDEND_PROVIDER_EVIDENCE_EXECUTION_DIGEST,
        "dividend_provider_evidence_request_approval_digest": EXPECTED_DIVIDEND_PROVIDER_EVIDENCE_REQUEST_APPROVAL_DIGEST,
        "dividend_provider_evidence_request_authorized": True,
        "ready_for_dividend_provider_evidence_execution": True,
        "provider_requests_made": True,
        "live_provider_transport_enabled": True,
        "dividend_provider_evidence_executed": True,
        "dividend_provider_evidence_results_created": True,
        "raw_provider_payloads_committed": False,
        "api_keys_stored_or_printed": False,
        "dividend_event_authority_candidate_created": True,
        "dividend_event_authority_review_created": True,
        "dividend_event_authority_created": False,
        "dividend_event_authority_frozen": False,
        "split_event_authority_created": True,
        "split_event_authority_frozen": True,
        "split_event_authority_scope": "SPLIT_EVENT_AUTHORITY_ONLY",
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
        "dividend_event_authority_candidate_review_package_digest": approval.EXPECTED_DIVIDEND_EVENT_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "dividend_event_authority_candidate_digest": approval.EXPECTED_DIVIDEND_EVENT_AUTHORITY_CANDIDATE_DIGEST,
        "split_event_authority_freeze_digest": approval.EXPECTED_SPLIT_EVENT_AUTHORITY_FREEZE_DIGEST,
        "split_event_evidence_results_review_package_digest": approval.EXPECTED_SPLIT_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST,
        "split_provider_evidence_execution_digest": approval.EXPECTED_SPLIT_PROVIDER_EVIDENCE_EXECUTION_DIGEST,
        "corporate_action_authority_plan_approval_digest": approval.EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_APPROVAL_DIGEST,
        "post_identity_freeze_registry_inventory_approval_digest": approval.EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_APPROVAL_DIGEST,
        "identity_authority_freeze_digest": approval.EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST,
        "ticker_universe_selection_approval_digest": approval.EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST,
        "target_universe": list(EXPECTED_TARGET_UNIVERSE),
        "target_universe_count": 12,
        "endpoint": EXPECTED_RESULT_FACTS["endpoint"],
        "endpoint_mode": EXPECTED_RESULT_FACTS["endpoint_mode"],
        "transport_mode": EXPECTED_RESULT_FACTS["transport_mode"],
        "expected_output_digests": dict(EXPECTED_OUTPUT_DIGESTS),
        "limitations": list(LIMITATIONS),
        "next_gates": list(NEXT_GATES),
        "dividend_policy_reconciliation_requirements": list(DIVIDEND_POLICY_RECONCILIATION_REQUIREMENTS),
        "dividend_evidence_results_available": True,
        "all_provider_requests_succeeded": True,
        "dividend_evidence_review_supports_future_dividend_authority_planning": True,
        "dividend_policy_reconciliation_requires_operator_review": True,
        "dividend_evidence_creates_dividend_authority": False,
        "dividend_evidence_creates_corporate_action_authority": False,
        "dividend_evidence_creates_acquisition_authority": False,
        "dividend_evidence_creates_dataset_generation_authority": False,
        "dividend_event_authority_artifact_created": False,
        "dividend_event_authority_freeze_created": False,
        "corporate_action_authority_artifact_created": False,
        "acquisition_authorization_created": False,
        "dataset_generation_authorization_created": False,
        "predictive_usefulness_acceptance_artifact_created": False,
        "profitability_acceptance_created": False,
        "runtime_migration_approval_created": False,
    }


def _blocked_package(reason: str) -> dict[str, Any]:
    package = _base_package()
    package.update(
        {
            "review_status": DIVIDEND_EVENT_EVIDENCE_RESULTS_REVIEW_BLOCKED_MISSING_OR_INVALID_OUTPUTS,
            "output_file_inspection_performed": False,
            "outputs_verified": False,
            "blocked_reason": reason,
            "output_digest_manifest": [],
            "review_checklist": [],
            "review_summary": _summary([]),
            "next_required_task": "RECREATE_OR_RESTORE_DIVIDEND_PROVIDER_EVIDENCE_OUTPUTS",
        }
    )
    package["dividend_event_evidence_results_review_package_digest"] = (
        dividend_event_evidence_results_review_package_digest_v1(package)
    )
    return package


def _verified_outputs(
    output_root: Path,
    *,
    expected_output_digests: Mapping[str, str],
) -> tuple[dict[str, dict[str, Any]], list[dict[str, Any]]]:
    payloads: dict[str, dict[str, Any]] = {}
    manifest: list[dict[str, Any]] = []
    if sorted(expected_output_digests) != EXPECTED_OUTPUT_FILENAMES_SORTED:
        raise DividendEventEvidenceResultsReviewError("expected output digest manifest mismatch")
    for filename in EXPECTED_OUTPUT_FILENAMES_SORTED:
        path = output_root / filename
        if not path.is_file():
            raise DividendEventEvidenceResultsReviewError(f"{filename} missing")
        data = path.read_bytes()
        digest = sha256_bytes(data)
        if digest != expected_output_digests[filename]:
            raise DividendEventEvidenceResultsReviewError(f"{filename} digest mismatch")
        payload = _load_json_file(path)
        if payload.get("output_label") != RESEARCH_ONLY_NON_ACTIONABLE:
            raise DividendEventEvidenceResultsReviewError(f"{filename} output_label mismatch")
        if payload.get("evidence_scope") != READ_ONLY_DIVIDEND_EVENT_EVIDENCE_REQUESTS_ONLY:
            raise DividendEventEvidenceResultsReviewError(f"{filename} evidence_scope mismatch")
        if payload.get("split_event_authority_created") is not True or payload.get("split_event_authority_frozen") is not True:
            raise DividendEventEvidenceResultsReviewError(f"{filename} split authority boundary mismatch")
        if _contains_unredacted_sensitive_value(payload):
            raise DividendEventEvidenceResultsReviewError(f"{filename} contains unredacted sensitive value")
        forbidden = _forbidden_output_field(payload)
        if forbidden:
            raise DividendEventEvidenceResultsReviewError(f"{filename} forbidden field {forbidden}")
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
    return payloads, manifest


def _per_ticker_summary(results_payload: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = results_payload.get("per_ticker_dividend_evidence_results")
    if not isinstance(rows, list):
        raise DividendEventEvidenceResultsReviewError("per_ticker_dividend_evidence_results missing")
    return [
        {
            "ticker": item.get("ticker"),
            "dividend_provider_evidence_status": item.get("dividend_provider_evidence_status"),
            "dividend_event_count": item.get("dividend_event_count"),
            "provider_response_digest": item.get("provider_response_digest"),
            "sanitized_dividend_evidence_digest": item.get("sanitized_dividend_evidence_digest"),
            "dividend_absence_policy_status": item.get("dividend_absence_policy_status"),
            "dividend_policy_reconciliation_status": item.get("dividend_policy_reconciliation_status"),
        }
        for item in rows
        if isinstance(item, Mapping)
    ]


def build_dividend_event_evidence_results_review_package_v1(
    *,
    output_root: str | Path | None = None,
    expected_output_digests: Mapping[str, str] | None = None,
) -> dict[str, Any]:
    """Build the offline review package from sanitized dividend outputs only."""
    root = Path(output_root) if output_root is not None else execution.OUTPUT_ROOT
    expected_digests = dict(expected_output_digests or EXPECTED_OUTPUT_DIGESTS)
    try:
        payloads, output_manifest = _verified_outputs(
            root, expected_output_digests=expected_digests
        )
        run_manifest = payloads["dividend_provider_evidence_run_manifest.json"]
        results_payload = payloads["dividend_event_results_sanitized.json"]
        failure_payload = payloads["dividend_event_failure_reason_inventory.json"]
        policy_payload = payloads["dividend_policy_reconciliation_report.json"]
        summary = run_manifest.get("execution_summary")
        if not isinstance(summary, dict):
            raise DividendEventEvidenceResultsReviewError("execution summary missing")
        per_ticker = _per_ticker_summary(results_payload)
        policy_rows = policy_payload.get("dividend_policy_reconciliation_report")
        if not isinstance(policy_rows, list) or len(policy_rows) != 12:
            raise DividendEventEvidenceResultsReviewError("dividend policy reconciliation rows mismatch")
        if any(
            not isinstance(row, Mapping)
            or row.get("dividend_policy_reconciliation_status") != "REQUIRES_OPERATOR_REVIEW"
            or row.get("cash_dividend_adjustment_policy") != "REQUIRES_OPERATOR_REVIEW"
            or row.get("total_return_assumption") != "NOT_ASSUMED"
            or row.get("authority_created") is not False
            for row in policy_rows
        ):
            raise DividendEventEvidenceResultsReviewError("dividend policy reconciliation requirements mismatch")
    except DividendEventEvidenceResultsReviewError as exc:
        return _blocked_package(str(exc))

    package = _base_package()
    failure_inventory = failure_payload.get("dividend_event_failure_reason_inventory", [])
    package.update(
        {
            "review_status": DIVIDEND_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE_READY,
            "output_root": root.as_posix(),
            "output_file_inspection_performed": True,
            "outputs_verified": True,
            "provider_request_count": summary.get("provider_request_count"),
            "successful_provider_response_count": summary.get("successful_provider_response_count"),
            "failed_provider_response_count": summary.get("failed_provider_response_count"),
            "dividend_evidence_collected_count": summary.get("dividend_evidence_collected_count"),
            "no_dividend_events_returned_count": summary.get("no_dividend_events_returned_count"),
            "not_evaluated_count": summary.get("not_evaluated_count"),
            "generated_output_count": summary.get("generated_output_count"),
            "failure_count": summary.get("failure_count"),
            "warning_count": summary.get("warning_count"),
            "per_ticker_dividend_evidence_summary": per_ticker,
            "zero_dividend_tickers": [
                item["ticker"] for item in per_ticker if item["dividend_event_count"] == 0
            ],
            "output_digest_manifest": output_manifest,
            "expected_output_digests": expected_digests,
            "reviewed_failure_inventory": failure_inventory,
            "ready_for_dividend_event_authority_freeze": False,
            "ready_for_dividend_policy_reconciliation_review": True,
            "ready_for_dividend_event_discrepancy_triage": bool(failure_inventory),
            "next_required_task": "DIVIDEND_EVENT_EVIDENCE_RESULTS_OPERATOR_REVIEW",
        }
    )
    checklist = _review_checklist(package)
    package["review_checklist"] = checklist
    package["review_summary"] = _summary(checklist, discrepancy=bool(failure_inventory))
    package["dividend_event_evidence_results_review_package_digest"] = (
        dividend_event_evidence_results_review_package_digest_v1(package)
    )
    validate_dividend_event_evidence_results_review_package_v1(package)
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


def _summary(checklist: list[dict[str, Any]], *, discrepancy: bool = False) -> dict[str, Any]:
    failed = [item for item in checklist if item.get("status") != PASS]
    return {
        "total_checks": len(checklist),
        "passed_checks": len(checklist) - len(failed),
        "failed_checks": len(failed),
        "blocker_count": sum(item.get("severity") == BLOCKER for item in failed),
        "ready_for_operator_review": not failed,
        "ready_for_dividend_event_authority_freeze": False,
        "ready_for_dividend_policy_reconciliation_review": not failed,
        "ready_for_dividend_event_discrepancy_triage": discrepancy,
        "dividend_event_authority_authorized": False,
        "dividend_event_authority_frozen": False,
        "split_event_authority_authorized": True,
        "split_event_authority_frozen": True,
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
    manifest = package.get("output_digest_manifest", [])
    checks = [
        ("dividend_provider_evidence_execution_digest_bound", EXPECTED_DIVIDEND_PROVIDER_EVIDENCE_EXECUTION_DIGEST, package.get("dividend_provider_evidence_execution_digest")),
        ("dividend_provider_evidence_request_approval_digest_bound", EXPECTED_DIVIDEND_PROVIDER_EVIDENCE_REQUEST_APPROVAL_DIGEST, package.get("dividend_provider_evidence_request_approval_digest")),
        ("dividend_candidate_review_digest_bound", approval.EXPECTED_DIVIDEND_EVENT_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST, package.get("dividend_event_authority_candidate_review_package_digest")),
        ("dividend_candidate_digest_bound", approval.EXPECTED_DIVIDEND_EVENT_AUTHORITY_CANDIDATE_DIGEST, package.get("dividend_event_authority_candidate_digest")),
        ("split_authority_freeze_digest_bound", approval.EXPECTED_SPLIT_EVENT_AUTHORITY_FREEZE_DIGEST, package.get("split_event_authority_freeze_digest")),
        ("split_evidence_results_review_digest_bound", approval.EXPECTED_SPLIT_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST, package.get("split_event_evidence_results_review_package_digest")),
        ("corporate_action_plan_approval_digest_bound", approval.EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_APPROVAL_DIGEST, package.get("corporate_action_authority_plan_approval_digest")),
        ("identity_freeze_digest_bound", approval.EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST, package.get("identity_authority_freeze_digest")),
        ("target_universe_count_12", 12, package.get("target_universe_count")),
        ("target_universe_matches_execution_universe", EXPECTED_TARGET_UNIVERSE, package.get("target_universe")),
        ("provider_request_count_12", 12, package.get("provider_request_count")),
        ("successful_provider_response_count_12", 12, package.get("successful_provider_response_count")),
        ("failed_provider_response_count_zero", 0, package.get("failed_provider_response_count")),
        ("dividend_evidence_collected_count_10", 10, package.get("dividend_evidence_collected_count")),
        ("no_dividend_events_returned_count_2", 2, package.get("no_dividend_events_returned_count")),
        ("generated_output_count_7", 7, package.get("generated_output_count")),
        ("output_digests_bound", EXPECTED_OUTPUT_FILENAMES_SORTED, sorted(item.get("filename") for item in manifest)),
        ("outputs_research_only_non_actionable", True, bool(manifest) and all(item.get("output_label") == RESEARCH_ONLY_NON_ACTIONABLE for item in manifest)),
        ("evidence_scope_read_only_dividend_event_evidence_requests_only", True, bool(manifest) and all(item.get("evidence_scope") == READ_ONLY_DIVIDEND_EVENT_EVIDENCE_REQUESTS_ONLY for item in manifest)),
        ("raw_provider_payloads_not_committed", False, package.get("raw_provider_payloads_committed")),
        ("api_keys_not_stored_or_printed", False, package.get("api_keys_stored_or_printed")),
        ("provider_requests_made_in_review_false", False, package.get("provider_requests_made_in_review")),
        ("dividend_provider_evidence_rerun_performed_false", False, package.get("dividend_provider_evidence_rerun_performed")),
        ("live_provider_transport_enabled_in_review_false", False, package.get("live_provider_transport_enabled_in_review")),
        ("dividend_event_authority_created_false", False, package.get("dividend_event_authority_created")),
        ("dividend_event_authority_frozen_false", False, package.get("dividend_event_authority_frozen")),
        ("split_event_authority_created_true", True, package.get("split_event_authority_created")),
        ("split_event_authority_frozen_true", True, package.get("split_event_authority_frozen")),
        ("split_provider_evidence_rerun_performed_false", False, package.get("split_provider_evidence_rerun_performed")),
        ("corporate_action_authority_created_false", False, package.get("corporate_action_authority_created")),
        ("new_ticker_acquisition_authorized_false", False, package.get("new_ticker_acquisition_authorized")),
        ("dataset_generation_authorized_false", False, package.get("dataset_generation_authorized")),
        ("acquisition_generation_authorized_false", False, package.get("acquisition_generation_authorized")),
        ("canonical_dataset_authorized_false", False, package.get("canonical_dataset_authorized")),
        ("registry_approval_created_false", False, package.get("registry_approval_created")),
        ("additional_predictive_evidence_execution_authorized_false", False, package.get("additional_predictive_evidence_execution_authorized")),
        ("additional_predictive_evidence_executed_false", False, package.get("additional_predictive_evidence_executed")),
        ("predictive_experiment_rerun_authorized_false", False, package.get("predictive_experiment_rerun_authorized")),
        ("predictive_experiment_rerun_performed_false", False, package.get("predictive_experiment_rerun_performed")),
        ("feature_matrix_regeneration_performed_false", False, package.get("feature_matrix_regeneration_performed")),
        ("new_strategy_scoring_performed_false", False, package.get("new_strategy_scoring_performed")),
        ("trade_recommendations_generated_false", False, package.get("trade_recommendations_generated")),
        ("predictive_usefulness_not_accepted", _not_accepted(), package.get("predictive_usefulness")),
        ("profitability_not_accepted", acquisition.PROFITABILITY_NOT_ACCEPTED, package.get("profitability")),
        ("runtime_migration_approved_false", False, package.get("runtime_migration_approved")),
        ("runtime_use_not_authorized", NOT_AUTHORIZED, package.get("runtime_use")),
        ("strategy_use_not_authorized", NOT_AUTHORIZED, package.get("strategy_use")),
        ("paper_trading_not_authorized", NOT_AUTHORIZED, package.get("paper_trading")),
        ("broker_execution_not_authorized", NOT_AUTHORIZED, package.get("broker_execution")),
        ("automatic_stitching_false", False, package.get("automatic_stitching")),
        ("dividend_evidence_supports_future_dividend_authority_planning_true", True, package.get("dividend_evidence_review_supports_future_dividend_authority_planning")),
        ("dividend_policy_reconciliation_requires_operator_review_true", True, package.get("dividend_policy_reconciliation_requires_operator_review")),
        ("dividend_evidence_creates_dividend_authority_false", False, package.get("dividend_evidence_creates_dividend_authority")),
        ("dividend_evidence_creates_corporate_action_authority_false", False, package.get("dividend_evidence_creates_corporate_action_authority")),
        ("dividend_evidence_creates_acquisition_authority_false", False, package.get("dividend_evidence_creates_acquisition_authority")),
        ("dividend_evidence_creates_dataset_generation_authority_false", False, package.get("dividend_evidence_creates_dataset_generation_authority")),
        ("limitations_recorded", LIMITATIONS, package.get("limitations")),
        ("next_gates_defined", NEXT_GATES, package.get("next_gates")),
        ("no_dividend_event_authority_artifact_created", False, package.get("dividend_event_authority_artifact_created")),
        ("no_dividend_event_authority_freeze_created", False, package.get("dividend_event_authority_freeze_created")),
        ("no_corporate_action_authority_artifact_created", False, package.get("corporate_action_authority_artifact_created")),
        ("no_acquisition_authorization_created", False, package.get("acquisition_authorization_created")),
        ("no_dataset_generation_authorization_created", False, package.get("dataset_generation_authorization_created")),
        ("no_predictive_usefulness_acceptance_artifact_created", False, package.get("predictive_usefulness_acceptance_artifact_created")),
        ("no_profitability_acceptance_created", False, package.get("profitability_acceptance_created")),
        ("no_runtime_migration_approval_created", False, package.get("runtime_migration_approval_created")),
    ]
    return [_check(*row) for row in checks]


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise DividendEventEvidenceResultsReviewError(f"{field} mismatch")


def _expect_true(actual: Any, field: str) -> None:
    if actual is not True:
        raise DividendEventEvidenceResultsReviewError(f"{field} must be true")


def _expect_false(actual: Any, field: str) -> None:
    if actual is not False:
        raise DividendEventEvidenceResultsReviewError(f"{field} must be false")


def _expect_digest(actual: Any, field: str) -> None:
    if not isinstance(actual, str) or len(actual) != 64:
        raise DividendEventEvidenceResultsReviewError(f"{field} missing")


def validate_dividend_event_evidence_results_review_package_v1(
    review_package: dict[str, Any],
) -> dict[str, Any]:
    """Validate review evidence, digest bindings, and closed authority boundaries."""
    if not isinstance(review_package, dict):
        raise DividendEventEvidenceResultsReviewError("review_package must be a JSON object")
    _expect(review_package.get("artifact_kind"), ARTIFACT_KIND_DIVIDEND_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE, "artifact_kind")
    _expect(review_package.get("schema_version"), SCHEMA_VERSION_DIVIDEND_EVENT_EVIDENCE_RESULTS_REVIEW_V1, "schema_version")
    if review_package.get("review_status") == DIVIDEND_EVENT_EVIDENCE_RESULTS_REVIEW_BLOCKED_MISSING_OR_INVALID_OUTPUTS:
        _expect_false(review_package.get("outputs_verified"), "outputs_verified")
        _expect_false(review_package.get("output_file_inspection_performed"), "output_file_inspection_performed")
        _expect_digest(review_package.get("dividend_event_evidence_results_review_package_digest"), "dividend_event_evidence_results_review_package_digest")
        _expect(review_package["dividend_event_evidence_results_review_package_digest"], dividend_event_evidence_results_review_package_digest_v1(review_package), "dividend_event_evidence_results_review_package_digest")
        return {"status": "DIVIDEND_EVENT_EVIDENCE_RESULTS_REVIEW_BLOCKED_VALID", "review_status": review_package["review_status"]}
    _expect(review_package.get("review_status"), DIVIDEND_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE_READY, "review_status")
    for field in (
        "created_offline", "dividend_provider_evidence_request_authorized",
        "ready_for_dividend_provider_evidence_execution", "provider_requests_made",
        "live_provider_transport_enabled", "dividend_provider_evidence_executed",
        "dividend_provider_evidence_results_created", "dividend_event_authority_candidate_created",
        "dividend_event_authority_review_created", "split_event_authority_created",
        "split_event_authority_frozen", "corporate_action_authority_plan_approved",
        "research_only", "operator_review_required", "output_file_inspection_performed",
        "outputs_verified", "dividend_evidence_results_available", "all_provider_requests_succeeded",
        "dividend_evidence_review_supports_future_dividend_authority_planning",
        "dividend_policy_reconciliation_requires_operator_review",
        "ready_for_dividend_policy_reconciliation_review",
    ):
        _expect_true(review_package.get(field), field)
    for field in (
        "provider_requests_made_in_review", "live_provider_transport_enabled_in_review",
        "dividend_provider_evidence_rerun_performed", "raw_provider_payloads_committed",
        "api_keys_stored_or_printed", "dividend_event_authority_created",
        "dividend_event_authority_frozen", "split_provider_evidence_rerun_performed",
        "corporate_action_authority_created", "new_ticker_acquisition_authorized",
        "dataset_generation_authorized", "acquisition_generation_authorized",
        "canonical_dataset_authorized", "registry_approval_created",
        "additional_predictive_evidence_execution_authorized", "additional_predictive_evidence_executed",
        "predictive_experiment_rerun_authorized", "predictive_experiment_rerun_performed",
        "feature_matrix_regeneration_performed", "new_strategy_scoring_performed",
        "trade_recommendations_generated", "predictive_usefulness_acceptance_ready",
        "predictive_usefulness_acceptance_recommended", "predictive_usefulness_acceptance_candidate_created",
        "profitability_acceptance_ready", "profitability_acceptance_recommended",
        "runtime_migration_recommended", "runtime_migration_approved", "runtime_migration_active",
        "strategy_runtime_migration", "automatic_stitching", "ready_for_dividend_event_authority_freeze",
        "dividend_evidence_creates_dividend_authority", "dividend_evidence_creates_corporate_action_authority",
        "dividend_evidence_creates_acquisition_authority", "dividend_evidence_creates_dataset_generation_authority",
        "dividend_event_authority_artifact_created", "dividend_event_authority_freeze_created",
        "corporate_action_authority_artifact_created", "acquisition_authorization_created",
        "dataset_generation_authorization_created", "predictive_usefulness_acceptance_artifact_created",
        "profitability_acceptance_created", "runtime_migration_approval_created",
    ):
        _expect_false(review_package.get(field), field)
    expected = {
        "source_execution_artifact_kind": execution.ARTIFACT_KIND_DIVIDEND_PROVIDER_EVIDENCE_EXECUTED,
        "source_execution_status": execution.DIVIDEND_PROVIDER_EVIDENCE_EXECUTED_READ_ONLY,
        "source_dividend_provider_evidence_execution_digest": EXPECTED_DIVIDEND_PROVIDER_EVIDENCE_EXECUTION_DIGEST,
        "source_dividend_provider_evidence_request_approval_digest": EXPECTED_DIVIDEND_PROVIDER_EVIDENCE_REQUEST_APPROVAL_DIGEST,
        "dividend_provider_evidence_execution_digest": EXPECTED_DIVIDEND_PROVIDER_EVIDENCE_EXECUTION_DIGEST,
        "dividend_provider_evidence_request_approval_digest": EXPECTED_DIVIDEND_PROVIDER_EVIDENCE_REQUEST_APPROVAL_DIGEST,
        "dividend_event_authority_candidate_review_package_digest": approval.EXPECTED_DIVIDEND_EVENT_AUTHORITY_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "dividend_event_authority_candidate_digest": approval.EXPECTED_DIVIDEND_EVENT_AUTHORITY_CANDIDATE_DIGEST,
        "split_event_authority_freeze_digest": approval.EXPECTED_SPLIT_EVENT_AUTHORITY_FREEZE_DIGEST,
        "split_event_evidence_results_review_package_digest": approval.EXPECTED_SPLIT_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST,
        "split_provider_evidence_execution_digest": approval.EXPECTED_SPLIT_PROVIDER_EVIDENCE_EXECUTION_DIGEST,
        "corporate_action_authority_plan_approval_digest": approval.EXPECTED_CORPORATE_ACTION_AUTHORITY_PLAN_APPROVAL_DIGEST,
        "post_identity_freeze_registry_inventory_approval_digest": approval.EXPECTED_POST_IDENTITY_FREEZE_REGISTRY_INVENTORY_APPROVAL_DIGEST,
        "identity_authority_freeze_digest": approval.EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST,
        "ticker_universe_selection_approval_digest": approval.EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST,
        "target_universe": EXPECTED_TARGET_UNIVERSE, "target_universe_count": 12,
        "endpoint": EXPECTED_RESULT_FACTS["endpoint"], "endpoint_mode": EXPECTED_RESULT_FACTS["endpoint_mode"],
        "transport_mode": EXPECTED_RESULT_FACTS["transport_mode"], "provider_request_count": 12,
        "successful_provider_response_count": 12, "failed_provider_response_count": 0,
        "dividend_evidence_collected_count": 10, "no_dividend_events_returned_count": 2,
        "generated_output_count": 7, "failure_count": 0, "warning_count": 12,
        "zero_dividend_tickers": ["AMZN", "TSLA"], "split_event_authority_scope": "SPLIT_EVENT_AUTHORITY_ONLY",
        "predictive_usefulness": _not_accepted(), "profitability": acquisition.PROFITABILITY_NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED, "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED, "broker_execution": NOT_AUTHORIZED,
        "limitations": LIMITATIONS, "next_gates": NEXT_GATES,
        "dividend_policy_reconciliation_requirements": DIVIDEND_POLICY_RECONCILIATION_REQUIREMENTS,
    }
    for field, value in expected.items():
        _expect(review_package.get(field), value, field)
    manifest = review_package.get("output_digest_manifest")
    if not isinstance(manifest, list) or len(manifest) != 7:
        raise DividendEventEvidenceResultsReviewError("output_digest_manifest mismatch")
    expected_output_digests = review_package.get("expected_output_digests")
    if not isinstance(expected_output_digests, dict) or sorted(expected_output_digests) != EXPECTED_OUTPUT_FILENAMES_SORTED:
        raise DividendEventEvidenceResultsReviewError("expected_output_digests mismatch")
    _expect({item.get("filename"): item.get("sha256") for item in manifest}, expected_output_digests, "output_digest_manifest")
    if any(item.get("output_label") != RESEARCH_ONLY_NON_ACTIONABLE for item in manifest):
        raise DividendEventEvidenceResultsReviewError("output labels must be research-only")
    if any(item.get("evidence_scope") != READ_ONLY_DIVIDEND_EVENT_EVIDENCE_REQUESTS_ONLY for item in manifest):
        raise DividendEventEvidenceResultsReviewError("output evidence_scope mismatch")
    per_ticker = review_package.get("per_ticker_dividend_evidence_summary")
    if not isinstance(per_ticker, list) or len(per_ticker) != 12:
        raise DividendEventEvidenceResultsReviewError("per_ticker_dividend_evidence_summary mismatch")
    _expect([item.get("ticker") for item in per_ticker], EXPECTED_TARGET_UNIVERSE, "per_ticker tickers")
    _expect(
        {item.get("ticker"): (item.get("dividend_provider_evidence_status"), item.get("dividend_event_count")) for item in per_ticker},
        EXPECTED_PER_TICKER,
        "per_ticker dividend evidence",
    )
    _expect([item.get("check_id") for item in review_package.get("review_checklist", [])], REQUIRED_CHECK_IDS, "review checklist check IDs")
    if any(item.get("status") != PASS for item in review_package["review_checklist"]):
        raise DividendEventEvidenceResultsReviewError("review checklist failed")
    _expect(review_package.get("review_summary"), _summary(review_package["review_checklist"], discrepancy=bool(review_package.get("reviewed_failure_inventory"))), "review_summary")
    digest = review_package.get("dividend_event_evidence_results_review_package_digest")
    _expect_digest(digest, "dividend_event_evidence_results_review_package_digest")
    _expect(digest, dividend_event_evidence_results_review_package_digest_v1(review_package), "dividend_event_evidence_results_review_package_digest")
    return {
        "status": "DIVIDEND_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE_VALID",
        "artifact_kind": review_package["artifact_kind"],
        "review_status": review_package["review_status"],
        "dividend_event_evidence_results_review_package_digest": digest,
        **{key: review_package[key] for key in ("provider_request_count", "successful_provider_response_count", "failed_provider_response_count", "dividend_evidence_collected_count", "no_dividend_events_returned_count", "generated_output_count", "failure_count", "warning_count")},
        **{key: review_package["review_summary"][key] for key in ("total_checks", "passed_checks", "failed_checks", "blocker_count")},
    }


def build_dividend_event_evidence_results_review_markdown_v1(
    review_package: dict[str, Any],
) -> str:
    """Render a sanitized Markdown status view for the ready review package."""
    validation = validate_dividend_event_evidence_results_review_package_v1(review_package)
    lines = [
        "# MarketFlow Dividend Event Evidence Results Review Status", "",
        "## Reviewed Dividend Provider Evidence Execution",
        f"- Review artifact: `{review_package['artifact_kind']}`",
        f"- Review status: `{review_package['review_status']}`",
        f"- Review package digest: `{validation['dividend_event_evidence_results_review_package_digest']}`",
        f"- Source execution digest: `{review_package['source_dividend_provider_evidence_execution_digest']}`", "",
        "## Source Evidence",
        f"- Dividend request approval digest: `{review_package['dividend_provider_evidence_request_approval_digest']}`",
        f"- Dividend candidate review digest: `{review_package['dividend_event_authority_candidate_review_package_digest']}`",
        f"- Dividend candidate digest: `{review_package['dividend_event_authority_candidate_digest']}`", "",
        "## Target Universe",
        f"- Target universe count: `{review_package['target_universe_count']}`",
        "- Target universe: " + ", ".join(f"`{ticker}`" for ticker in review_package["target_universe"]), "",
        "## Provider Request Summary",
        f"- Endpoint/mode: `{review_package['endpoint']}` / `{review_package['endpoint_mode']}` / `{review_package['transport_mode']}`",
        f"- Requests/successes/failures: `{review_package['provider_request_count']} / {review_package['successful_provider_response_count']} / {review_package['failed_provider_response_count']}`",
        f"- Failure/warning count: `{review_package['failure_count']} / {review_package['warning_count']}`", "",
        "## Per-Ticker Dividend Evidence Summary",
    ]
    lines.extend(
        f"- `{item['ticker']}`: `{item['dividend_provider_evidence_status']}`, events `{item['dividend_event_count']}`"
        for item in review_package["per_ticker_dividend_evidence_summary"]
    )
    lines.extend(["", "## Output Digest Manifest"])
    lines.extend(f"- `{item['filename']}`: `{item['sha256']}`" for item in review_package["output_digest_manifest"])
    lines.extend([
        "", "## Dividend Absence Policy Summary",
        "- AMZN and TSLA returned zero dividend rows; explicit absence-policy review is required.",
        "- Zero-row provider responses are read-only evidence, not dividend authority.", "",
        "## Dividend Policy Reconciliation Summary",
        "- Dividend adjustment and total-return policy require operator review before any dividend freeze.",
        "- Total return and dividend reinvestment are not assumed.", "",
        "## Limitations", *[f"- `{item}`" for item in review_package["limitations"]], "",
        "## Next Gates", *[f"- `{item}`" for item in review_package["next_gates"]], "",
        "## Dividend Authority Boundary",
        f"- Created/frozen: `{review_package['dividend_event_authority_created']} / {review_package['dividend_event_authority_frozen']}`", "",
        "## Split Authority Boundary",
        f"- Created/frozen: `{review_package['split_event_authority_created']} / {review_package['split_event_authority_frozen']}`; unchanged.", "",
        "## Corporate-Action Authority Boundary",
        f"- corporate_action_authority_created: `{review_package['corporate_action_authority_created']}`", "",
        "## Acquisition Boundary",
        f"- new_ticker_acquisition_authorized: `{review_package['new_ticker_acquisition_authorized']}`", "",
        "## Dataset Boundary",
        f"- dataset_generation_authorized: `{review_package['dataset_generation_authorized']}`", "",
        "## Predictive/Profitability Boundary",
        f"- Predictive usefulness/profitability: `{review_package['predictive_usefulness']} / {review_package['profitability']}`", "",
        "## Runtime Boundary",
        f"- Runtime/strategy/paper/broker: `{review_package['runtime_use']} / {review_package['strategy_use']} / {review_package['paper_trading']} / {review_package['broker_execution']}`", "",
        "## Checklist Summary",
        f"- Total/passed/failed/blockers: `{review_package['review_summary']['total_checks']} / {review_package['review_summary']['passed_checks']} / {review_package['review_summary']['failed_checks']} / {review_package['review_summary']['blocker_count']}`", "",
        "## Guardrails",
        "- No provider requests were made in review.",
        "- No dividend evidence rerun or live provider transport occurred in review.",
        "- No dividend or corporate-action authority, acquisition, dataset, predictive acceptance, or runtime activation was created.",
    ])
    return "\n".join(lines) + "\n"


def write_dividend_event_evidence_results_review_package_v1(
    output_dir: str | Path,
    *,
    output_root: str | Path | None = None,
    expected_output_digests: Mapping[str, str] | None = None,
) -> dict[str, Any]:
    """Write review JSON without overwriting an existing artifact."""
    package = build_dividend_event_evidence_results_review_package_v1(
        output_root=output_root, expected_output_digests=expected_output_digests
    )
    validation = validate_dividend_event_evidence_results_review_package_v1(package)
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "dividend_event_evidence_results_review_package_v1.json"
    if path.exists():
        raise DividendEventEvidenceResultsReviewError("dividend evidence results review package output already exists")
    payload = canonical_json_bytes(package)
    path.write_bytes(payload)
    return {
        "path": str(path),
        "artifact_kind": package["artifact_kind"],
        "review_status": package["review_status"],
        "dividend_event_evidence_results_review_package_digest": validation.get("dividend_event_evidence_results_review_package_digest"),
        "payload_sha256": sha256_bytes(payload),
    }
