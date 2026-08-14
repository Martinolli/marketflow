"""Offline, digest-bound review of generated canonical dataset outputs."""

from __future__ import annotations

from collections import Counter
from copy import deepcopy
import json
from pathlib import Path
from typing import Any, Mapping

from marketflow.historical_data.artifacts import canonical_json_bytes, semantic_digest, sha256_bytes
from marketflow.services import canonical_dataset_generation_execution_service as generation


ARTIFACT_KIND_CANONICAL_DATASET_RESULTS_REVIEW_PACKAGE = (
    "CANONICAL_DATASET_RESULTS_REVIEW_PACKAGE"
)
SCHEMA_VERSION_CANONICAL_DATASET_RESULTS_REVIEW_V1 = "canonical_dataset_results_review_v1"
CANONICAL_DATASET_RESULTS_REVIEW_PACKAGE_READY = (
    "CANONICAL_DATASET_RESULTS_REVIEW_PACKAGE_READY"
)
CANONICAL_DATASET_RESULTS_REVIEW_BLOCKED_MISSING_OR_INVALID_OUTPUTS = (
    "CANONICAL_DATASET_RESULTS_REVIEW_BLOCKED_MISSING_OR_INVALID_OUTPUTS"
)

OUTPUT_LABEL = generation.OUTPUT_LABEL
DATASET_SCOPE = generation.DATASET_SCOPE
SOURCE_EVIDENCE_SCOPE = generation.SOURCE_EVIDENCE_SCOPE
NOT_AUTHORIZED = generation.NOT_AUTHORIZED
NOT_ACCEPTED = generation.NOT_ACCEPTED
PASS = "PASS"
FAIL = "FAIL"
BLOCKER = "BLOCKER"

EXPECTED_CANONICAL_DATASET_GENERATION_DIGEST = (
    "9250ce29d7ba9754b43cfde07a5ded937a9402563691757a5aa6f7014f30fdbb"
)
EXPECTED_CANONICAL_DATASET_GENERATION_APPROVAL_DIGEST = (
    generation.EXPECTED_CANONICAL_DATASET_GENERATION_APPROVAL_DIGEST
)
EXPECTED_CANONICAL_RECORDS_SHA256 = (
    "fbd7c1b17b42e5d4f82a9162b31b45fdfeef46f0e9ee7d29d74c926f0cf19044"
)
EXPECTED_OUTPUT_FILE_SHA256 = {
    "canonical_dataset_generation_run_manifest.json": "6793d3c907a66b35c2ad27d27d34a024720a4d19310724726386e7117be8d207",
    "canonical_dataset_source_evidence_manifest.json": "43c56cdb5826515342e93259c82f9ba3bbadd6c867738ed5a1399eb7247e1ed8",
    "canonical_dataset_schema_contract.json": "ac4ba5f7c1b56e743d626363d1d45a3e71a0dcfd11f2e070fc02087b069b1435",
    "canonical_dataset_records.jsonl": EXPECTED_CANONICAL_RECORDS_SHA256,
    "per_ticker_canonical_dataset_summary.json": "4a9dbc104a7f0dc434cb9ba6f8b0687677a507b7aaf76c5005280b0172ec86a4",
    "canonical_dataset_data_quality_report.json": "3c384753577019b30929fc50dd4489fd9fa7b17fce652a2abdbd16620e020c2b",
    "canonical_dataset_digest_manifest.json": "002d57494d1afc00c09532c424ea8f60199208417e424783d0bf142ce82a376f",
    "canonical_dataset_failure_reason_inventory.json": "84eebb668914628c5a6bb2570310817619c4d817dae39a7c5b15e593a01ffeb8",
    "operator_review_summary.json": "f2101b6b84477eb92ea2c058a789ea4de19969334729ed6c38d5225adea2f193",
}
EXPECTED_OUTPUT_FILENAMES = list(generation.OUTPUT_FILENAMES)
EXPECTED_TARGET_UNIVERSE = list(generation.TARGET_UNIVERSE)
EXPECTED_RECORD_COUNTS = dict(generation.EXPECTED_RECORD_COUNTS)
EXPECTED_SOURCE_PROFILE = deepcopy(generation.SOURCE_PROFILE)
DEFAULT_OUTPUT_ROOT = generation.DEFAULT_OUTPUT_ROOT

LIMITATIONS = [
    "canonical_dataset_generated_research_only",
    "canonical_dataset_not_frozen",
    "registry_approval_not_created",
    "runtime_not_authorized",
    "strategy_use_not_authorized",
    "meta_reduced_record_count_preserved",
    "no_missing_bar_fabrication",
    "no_calendar_session_inference",
    "no_predictive_usefulness_acceptance",
    "no_profitability_acceptance",
    "operator_approval_required_before_canonical_dataset_freeze",
]
NEXT_GATES = [
    "canonical_dataset_results_operator_review",
    "canonical_dataset_freeze_ceremony",
    "research_registry_candidate",
    "research_registry_operator_review",
    "research_registry_approval",
    "additional_predictive_evidence_chain_if_required",
    "runtime_migration_chain_if_ever_authorized",
]
REQUIRED_CHECK_IDS = [
    "canonical_dataset_generation_digest_bound",
    "canonical_dataset_generation_approval_digest_bound",
    "canonical_dataset_chain_review_digest_bound",
    "acquisition_generation_freeze_digest_bound",
    "acquisition_evidence_results_review_digest_bound",
    "target_universe_count_12",
    "target_universe_matches_generation_universe",
    "generated_output_count_9",
    "canonical_records_digest_matches_expected",
    "total_canonical_record_count_11946",
    "per_ticker_record_counts_preserved",
    "meta_record_count_913_preserved",
    "non_meta_record_counts_1003_preserved",
    "source_profile_preserved",
    "dataset_scope_research_only",
    "outputs_verified",
    "output_digests_bound",
    "digest_manifest_self_reference_non_applicable",
    "provider_requests_made_in_review_false",
    "live_provider_transport_enabled_in_review_false",
    "market_data_acquisition_performed_in_review_false",
    "dataset_generation_performed_in_review_false",
    "canonical_dataset_regenerated_in_review_false",
    "raw_provider_payloads_not_committed",
    "api_keys_not_stored_or_printed",
    "canonical_dataset_generated_true",
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
    "canonical_dataset_results_support_future_freeze_true",
    "canonical_dataset_results_create_freeze_authority_false",
    "canonical_dataset_results_create_registry_approval_false",
    "canonical_dataset_results_create_runtime_authority_false",
    "limitations_recorded",
    "next_gates_defined",
    "no_canonical_dataset_freeze_artifact_created",
    "no_registry_approval_created",
    "no_predictive_usefulness_acceptance_artifact_created",
    "no_profitability_acceptance_created",
    "no_runtime_migration_approval_created",
]


class CanonicalDatasetResultsReviewError(ValueError):
    """Raised when canonical dataset review evidence is invalid."""


def _expect(actual: Any, expected: Any, field: str) -> None:
    if actual != expected:
        raise CanonicalDatasetResultsReviewError(f"{field} mismatch")


def _expect_true(actual: Any, field: str) -> None:
    if actual is not True:
        raise CanonicalDatasetResultsReviewError(f"{field} must be true")


def _expect_false(actual: Any, field: str) -> None:
    if actual is not False:
        raise CanonicalDatasetResultsReviewError(f"{field} must be false")


def _expect_digest(actual: Any, field: str) -> None:
    if not isinstance(actual, str) or len(actual) != 64:
        raise CanonicalDatasetResultsReviewError(f"{field} missing")


def _load_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise CanonicalDatasetResultsReviewError(f"{path.name} is not readable JSON") from exc
    if not isinstance(payload, dict):
        raise CanonicalDatasetResultsReviewError(f"{path.name} must contain a JSON object")
    return payload


def _contains_sensitive_or_raw_payload(value: Any) -> bool:
    if isinstance(value, Mapping):
        for key, item in value.items():
            lowered = str(key).lower()
            if lowered in {
                "authorization", "api_key", "apikey", "access_token", "provider_response_body",
                "raw_provider_payload", "raw_provider_payloads", "raw_response_body",
            }:
                return True
            if _contains_sensitive_or_raw_payload(item):
                return True
        return False
    if isinstance(value, list):
        return any(_contains_sensitive_or_raw_payload(item) for item in value)
    if isinstance(value, str):
        lowered = value.lower()
        return any(token in lowered for token in ("bearer ", "apikey=", "api_key=", "access_token="))
    return False


def _inspect_records(path: Path) -> tuple[dict[str, int], int]:
    counts: Counter[str] = Counter()
    seen_order: list[str] = []
    last_timestamp: dict[str, str] = {}
    try:
        with path.open(encoding="utf-8") as handle:
            for line_number, line in enumerate(handle, start=1):
                if not line.strip():
                    raise CanonicalDatasetResultsReviewError("canonical records contain blank lines")
                record = json.loads(line)
                if not isinstance(record, dict):
                    raise CanonicalDatasetResultsReviewError("canonical record must be an object")
                ticker = record.get("ticker")
                if ticker not in EXPECTED_TARGET_UNIVERSE:
                    raise CanonicalDatasetResultsReviewError(f"record {line_number} ticker mismatch")
                if not seen_order or seen_order[-1] != ticker:
                    seen_order.append(ticker)
                timestamp = record.get("timestamp_utc_or_session_date")
                if not isinstance(timestamp, str) or (
                    ticker in last_timestamp and timestamp <= last_timestamp[ticker]
                ):
                    raise CanonicalDatasetResultsReviewError(f"{ticker} record ordering mismatch")
                last_timestamp[ticker] = timestamp
                _expect_digest(record.get("source_record_digest"), f"record {line_number} source_record_digest")
                _expect_digest(record.get("canonical_record_digest"), f"record {line_number} canonical_record_digest")
                digest_payload = dict(record)
                canonical_digest = digest_payload.pop("canonical_record_digest")
                _expect(canonical_digest, semantic_digest(digest_payload), f"record {line_number} canonical_record_digest")
                counts[ticker] += 1
    except (OSError, json.JSONDecodeError) as exc:
        raise CanonicalDatasetResultsReviewError("canonical records are not readable JSONL") from exc
    _expect(seen_order, EXPECTED_TARGET_UNIVERSE, "canonical record ticker order")
    result = {ticker: counts[ticker] for ticker in EXPECTED_TARGET_UNIVERSE}
    _expect(result, EXPECTED_RECORD_COUNTS, "canonical record counts")
    return result, sum(result.values())


def _verified_outputs(root: Path) -> tuple[dict[str, dict[str, Any]], list[dict[str, Any]], dict[str, int]]:
    if not root.is_dir():
        raise CanonicalDatasetResultsReviewError("canonical dataset output root missing")
    actual_names = sorted(path.name for path in root.iterdir() if path.is_file())
    _expect(actual_names, sorted(EXPECTED_OUTPUT_FILENAMES), "canonical output filenames")
    is_default_root = root.resolve() == DEFAULT_OUTPUT_ROOT.resolve()
    file_digests = {name: sha256_bytes((root / name).read_bytes()) for name in EXPECTED_OUTPUT_FILENAMES}
    if is_default_root:
        _expect(file_digests, EXPECTED_OUTPUT_FILE_SHA256, "committed canonical output file digests")
        _expect(file_digests["canonical_dataset_records.jsonl"], EXPECTED_CANONICAL_RECORDS_SHA256, "records digest")

    payloads: dict[str, dict[str, Any]] = {}
    for name in EXPECTED_OUTPUT_FILENAMES:
        if name.endswith(".json"):
            payload = _load_json(root / name)
            _expect(payload.get("output_label"), OUTPUT_LABEL, f"{name}.output_label")
            _expect(payload.get("dataset_scope"), DATASET_SCOPE, f"{name}.dataset_scope")
            _expect_false(payload.get("canonical_dataset_frozen"), f"{name}.canonical_dataset_frozen")
            _expect_false(payload.get("registry_approval_created"), f"{name}.registry_approval_created")
            if _contains_sensitive_or_raw_payload(payload):
                raise CanonicalDatasetResultsReviewError(f"{name} contains sensitive or raw payload material")
            payloads[name] = payload

    run = payloads["canonical_dataset_generation_run_manifest.json"]
    generation.validate_canonical_dataset_generated_v1(run)
    _expect(run.get("canonical_dataset_generation_digest"), EXPECTED_CANONICAL_DATASET_GENERATION_DIGEST, "source generation digest")
    _expect(run.get("canonical_dataset_generation_approval_digest"), EXPECTED_CANONICAL_DATASET_GENERATION_APPROVAL_DIGEST, "source approval digest")
    source_manifest = run.get("canonical_output_digest_manifest")
    if not isinstance(source_manifest, list) or len(source_manifest) != 9:
        raise CanonicalDatasetResultsReviewError("source canonical output digest manifest mismatch")
    _expect([row.get("filename") for row in source_manifest], EXPECTED_OUTPUT_FILENAMES, "source digest filenames")
    source_by_name = {row["filename"]: row for row in source_manifest}
    digest_payload = payloads["canonical_dataset_digest_manifest.json"]
    _expect(
        digest_payload.get("canonical_output_digest_manifest"),
        source_manifest,
        "canonical digest manifest bindings",
    )
    _expect(
        digest_payload.get("canonical_dataset_generation_digest"),
        run["canonical_dataset_generation_digest"],
        "canonical digest manifest generation digest",
    )
    for name in EXPECTED_OUTPUT_FILENAMES:
        row = source_by_name[name]
        if name == "canonical_dataset_generation_run_manifest.json":
            _expect(row.get("digest_kind"), "CANONICAL_DATASET_GENERATION_DIGEST", "run manifest digest kind")
            _expect(row.get("sha256"), run["canonical_dataset_generation_digest"], "run manifest semantic digest")
        elif name == "canonical_dataset_digest_manifest.json":
            _expect(row.get("digest_kind"), "SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE", "digest manifest self-reference")
            _expect(row.get("sha256"), None, "digest manifest self-reference value")
        else:
            _expect(row.get("digest_kind"), "FILE_SHA256", f"{name}.digest_kind")
            _expect(row.get("sha256"), file_digests[name], f"{name}.source manifest digest")

    record_counts, total = _inspect_records(root / "canonical_dataset_records.jsonl")
    _expect(total, generation.EXPECTED_TOTAL_CANONICAL_RECORD_COUNT, "total canonical record count")
    manifest = [
        {
            "filename": name,
            "sha256": file_digests[name],
            "output_label": OUTPUT_LABEL,
            "dataset_scope": DATASET_SCOPE,
            "verified": True,
            "source_manifest_digest_kind": source_by_name[name].get("digest_kind"),
            "source_manifest_digest": source_by_name[name].get("sha256"),
        }
        for name in EXPECTED_OUTPUT_FILENAMES
    ]
    return payloads, manifest, record_counts


def _base_package(source: Mapping[str, Any] | None = None) -> dict[str, Any]:
    source = source or {}
    source_generation_digest = source.get(
        "canonical_dataset_generation_digest", EXPECTED_CANONICAL_DATASET_GENERATION_DIGEST
    )
    return {
        "artifact_kind": ARTIFACT_KIND_CANONICAL_DATASET_RESULTS_REVIEW_PACKAGE,
        "schema_version": SCHEMA_VERSION_CANONICAL_DATASET_RESULTS_REVIEW_V1,
        "created_offline": True,
        "provider_requests_made_in_review": False,
        "live_provider_transport_enabled_in_review": False,
        "market_data_acquisition_performed_in_review": False,
        "dataset_generation_performed_in_review": False,
        "canonical_dataset_regenerated_in_review": False,
        "raw_provider_payloads_committed": False,
        "api_keys_stored_or_printed": False,
        "source_execution_artifact_kind": generation.ARTIFACT_KIND_CANONICAL_DATASET_GENERATED,
        "source_execution_status": generation.CANONICAL_DATASET_GENERATED_RESEARCH_ONLY,
        "source_canonical_dataset_generation_digest": source_generation_digest,
        "source_canonical_dataset_generation_approval_digest": EXPECTED_CANONICAL_DATASET_GENERATION_APPROVAL_DIGEST,
        "canonical_dataset_generation_digest": source_generation_digest,
        "canonical_dataset_generation_approval_digest": EXPECTED_CANONICAL_DATASET_GENERATION_APPROVAL_DIGEST,
        "canonical_dataset_chain_candidate_review_package_digest": generation.approval_service.EXPECTED_CANONICAL_DATASET_CHAIN_CANDIDATE_REVIEW_PACKAGE_DIGEST,
        "canonical_dataset_chain_candidate_digest": generation.approval_service.EXPECTED_CANONICAL_DATASET_CHAIN_CANDIDATE_DIGEST,
        "acquisition_generation_freeze_digest": generation.approval_service.EXPECTED_ACQUISITION_GENERATION_FREEZE_DIGEST,
        "acquisition_generation_approval_digest": generation.approval_service.EXPECTED_ACQUISITION_GENERATION_APPROVAL_DIGEST,
        "acquisition_evidence_results_review_package_digest": generation.approval_service.EXPECTED_ACQUISITION_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST,
        "acquisition_provider_evidence_execution_digest": generation.approval_service.EXPECTED_ACQUISITION_PROVIDER_EVIDENCE_EXECUTION_DIGEST,
        "corporate_action_authority_approval_digest": generation.approval_service.EXPECTED_CORPORATE_ACTION_AUTHORITY_APPROVAL_DIGEST,
        "identity_authority_freeze_digest": generation.approval_service.EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST,
        "ticker_universe_selection_approval_digest": generation.approval_service.EXPECTED_TICKER_UNIVERSE_SELECTION_APPROVAL_DIGEST,
        "dataset_generation_authorized": True,
        "canonical_dataset_authorized": True,
        "canonical_dataset_generation_approved": True,
        "canonical_dataset_candidate_created": True,
        "canonical_dataset_generation_executed": True,
        "canonical_dataset_generated": True,
        "canonical_dataset_generation_results_created": True,
        "canonical_dataset_results_review_created": True,
        "canonical_dataset_results_review_ready": True,
        "ready_for_canonical_dataset_freeze": True,
        "canonical_dataset_frozen": False,
        "registry_approval_created": False,
        "canonical_dataset_chain_candidate_created": True,
        "canonical_dataset_chain_candidate_review_created": True,
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
        "profitability": NOT_ACCEPTED,
        "runtime_migration_approved": False,
        "runtime_migration_active": False,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
        "automatic_stitching": False,
        "operator_review_required": True,
        "target_universe": list(EXPECTED_TARGET_UNIVERSE),
        "target_universe_count": 12,
        "date_range_start": EXPECTED_SOURCE_PROFILE["date_range_start"],
        "date_range_end": EXPECTED_SOURCE_PROFILE["date_range_end"],
        "timeframe": EXPECTED_SOURCE_PROFILE["timeframe"],
        "profile": EXPECTED_SOURCE_PROFILE["profile"],
        "source_evidence_scope": SOURCE_EVIDENCE_SCOPE,
        "dataset_scope": DATASET_SCOPE,
        "generated_output_count": 9,
        "total_canonical_record_count": generation.EXPECTED_TOTAL_CANONICAL_RECORD_COUNT,
        "output_label": OUTPUT_LABEL,
        "limitations": list(LIMITATIONS),
        "next_gates": list(NEXT_GATES),
        "canonical_dataset_results_available": True,
        "canonical_dataset_outputs_verified": True,
        "canonical_dataset_record_count_verified": True,
        "canonical_dataset_results_support_future_freeze": True,
        "canonical_dataset_results_create_freeze_authority": False,
        "canonical_dataset_results_create_registry_approval": False,
        "canonical_dataset_results_create_predictive_evidence_authority": False,
        "canonical_dataset_results_create_runtime_authority": False,
        "canonical_dataset_freeze_artifact_created": False,
        "registry_approval_artifact_created": False,
        "predictive_usefulness_acceptance_artifact_created": False,
        "profitability_acceptance_created": False,
        "runtime_migration_approval_created": False,
    }


def _blocked_package(reason: str) -> dict[str, Any]:
    package = _base_package()
    blocked_summary = _summary([])
    blocked_summary.update({
        "ready_for_operator_review": False,
        "ready_for_canonical_dataset_freeze": False,
    })
    package.update({
        "review_status": CANONICAL_DATASET_RESULTS_REVIEW_BLOCKED_MISSING_OR_INVALID_OUTPUTS,
        "blocked_reason": reason,
        "output_file_inspection_performed": False,
        "canonical_dataset_outputs_verified": False,
        "canonical_dataset_record_count_verified": False,
        "canonical_dataset_results_available": False,
        "canonical_dataset_results_review_created": False,
        "canonical_dataset_results_review_ready": False,
        "ready_for_canonical_dataset_freeze": False,
        "canonical_dataset_results_support_future_freeze": False,
        "output_digest_manifest": [],
        "per_ticker_canonical_record_summary": [],
        "records_digest": "NOT_VERIFIED",
        "review_checklist": [],
        "review_summary": blocked_summary,
    })
    package["canonical_dataset_results_review_package_digest"] = (
        canonical_dataset_results_review_package_digest_v1(package)
    )
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
    counts = package.get("per_ticker_record_counts", {})
    values = {
        "canonical_dataset_generation_digest_bound": (EXPECTED_CANONICAL_DATASET_GENERATION_DIGEST, package.get("canonical_dataset_generation_digest")),
        "canonical_dataset_generation_approval_digest_bound": (EXPECTED_CANONICAL_DATASET_GENERATION_APPROVAL_DIGEST, package.get("canonical_dataset_generation_approval_digest")),
        "canonical_dataset_chain_review_digest_bound": (generation.approval_service.EXPECTED_CANONICAL_DATASET_CHAIN_CANDIDATE_REVIEW_PACKAGE_DIGEST, package.get("canonical_dataset_chain_candidate_review_package_digest")),
        "acquisition_generation_freeze_digest_bound": (generation.approval_service.EXPECTED_ACQUISITION_GENERATION_FREEZE_DIGEST, package.get("acquisition_generation_freeze_digest")),
        "acquisition_evidence_results_review_digest_bound": (generation.approval_service.EXPECTED_ACQUISITION_EVIDENCE_RESULTS_REVIEW_PACKAGE_DIGEST, package.get("acquisition_evidence_results_review_package_digest")),
        "target_universe_count_12": (12, package.get("target_universe_count")),
        "target_universe_matches_generation_universe": (EXPECTED_TARGET_UNIVERSE, package.get("target_universe")),
        "generated_output_count_9": (9, package.get("generated_output_count")),
        "canonical_records_digest_matches_expected": (EXPECTED_CANONICAL_RECORDS_SHA256, package.get("records_digest")),
        "total_canonical_record_count_11946": (11946, package.get("total_canonical_record_count")),
        "per_ticker_record_counts_preserved": (EXPECTED_RECORD_COUNTS, counts),
        "meta_record_count_913_preserved": (913, counts.get("META")),
        "non_meta_record_counts_1003_preserved": (True, bool(counts) and all(count == 1003 for ticker, count in counts.items() if ticker != "META")),
        "source_profile_preserved": (EXPECTED_SOURCE_PROFILE, package.get("source_profile")),
        "dataset_scope_research_only": (DATASET_SCOPE, package.get("dataset_scope")),
        "outputs_verified": (True, package.get("canonical_dataset_outputs_verified")),
        "output_digests_bound": (EXPECTED_OUTPUT_FILENAMES, [row.get("filename") for row in manifest]),
        "digest_manifest_self_reference_non_applicable": (True, package.get("digest_manifest_self_reference_non_applicable")),
        "provider_requests_made_in_review_false": (False, package.get("provider_requests_made_in_review")),
        "live_provider_transport_enabled_in_review_false": (False, package.get("live_provider_transport_enabled_in_review")),
        "market_data_acquisition_performed_in_review_false": (False, package.get("market_data_acquisition_performed_in_review")),
        "dataset_generation_performed_in_review_false": (False, package.get("dataset_generation_performed_in_review")),
        "canonical_dataset_regenerated_in_review_false": (False, package.get("canonical_dataset_regenerated_in_review")),
        "raw_provider_payloads_not_committed": (False, package.get("raw_provider_payloads_committed")),
        "api_keys_not_stored_or_printed": (False, package.get("api_keys_stored_or_printed")),
        "canonical_dataset_generated_true": (True, package.get("canonical_dataset_generated")),
        "canonical_dataset_frozen_false": (False, package.get("canonical_dataset_frozen")),
        "registry_approval_created_false": (False, package.get("registry_approval_created")),
        "additional_predictive_evidence_execution_authorized_false": (False, package.get("additional_predictive_evidence_execution_authorized")),
        "additional_predictive_evidence_executed_false": (False, package.get("additional_predictive_evidence_executed")),
        "predictive_experiment_rerun_authorized_false": (False, package.get("predictive_experiment_rerun_authorized")),
        "feature_matrix_regeneration_performed_false": (False, package.get("feature_matrix_regeneration_performed")),
        "new_strategy_scoring_performed_false": (False, package.get("new_strategy_scoring_performed")),
        "trade_recommendations_generated_false": (False, package.get("trade_recommendations_generated")),
        "predictive_usefulness_not_accepted": (NOT_ACCEPTED, package.get("predictive_usefulness")),
        "profitability_not_accepted": (NOT_ACCEPTED, package.get("profitability")),
        "runtime_migration_approved_false": (False, package.get("runtime_migration_approved")),
        "runtime_use_not_authorized": (NOT_AUTHORIZED, package.get("runtime_use")),
        "strategy_use_not_authorized": (NOT_AUTHORIZED, package.get("strategy_use")),
        "paper_trading_not_authorized": (NOT_AUTHORIZED, package.get("paper_trading")),
        "broker_execution_not_authorized": (NOT_AUTHORIZED, package.get("broker_execution")),
        "automatic_stitching_false": (False, package.get("automatic_stitching")),
        "canonical_dataset_results_support_future_freeze_true": (True, package.get("canonical_dataset_results_support_future_freeze")),
        "canonical_dataset_results_create_freeze_authority_false": (False, package.get("canonical_dataset_results_create_freeze_authority")),
        "canonical_dataset_results_create_registry_approval_false": (False, package.get("canonical_dataset_results_create_registry_approval")),
        "canonical_dataset_results_create_runtime_authority_false": (False, package.get("canonical_dataset_results_create_runtime_authority")),
        "limitations_recorded": (LIMITATIONS, package.get("limitations")),
        "next_gates_defined": (NEXT_GATES, package.get("next_gates")),
        "no_canonical_dataset_freeze_artifact_created": (False, package.get("canonical_dataset_freeze_artifact_created")),
        "no_registry_approval_created": (False, package.get("registry_approval_artifact_created")),
        "no_predictive_usefulness_acceptance_artifact_created": (False, package.get("predictive_usefulness_acceptance_artifact_created")),
        "no_profitability_acceptance_created": (False, package.get("profitability_acceptance_created")),
        "no_runtime_migration_approval_created": (False, package.get("runtime_migration_approval_created")),
    }
    return [_check(check_id, *values[check_id]) for check_id in REQUIRED_CHECK_IDS]


def _summary(checklist: list[dict[str, Any]]) -> dict[str, Any]:
    failed = [row for row in checklist if row.get("status") != PASS]
    return {
        "total_checks": len(checklist),
        "passed_checks": len(checklist) - len(failed),
        "failed_checks": len(failed),
        "blocker_count": sum(row.get("severity") == BLOCKER for row in failed),
        "ready_for_operator_review": not failed,
        "ready_for_canonical_dataset_freeze": not failed,
        "ready_for_research_registry_candidate": False,
        "canonical_dataset_generated": True,
        "canonical_dataset_frozen": False,
        "registry_approval_created": False,
        "additional_predictive_evidence_execution_authorized": False,
        "predictive_usefulness_accepted": False,
        "profitability_accepted": False,
        "runtime_migration_authorized": False,
        "software_runtime_activation_authorized": False,
    }


def _digest_payload(package: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(package)
    payload.pop("canonical_dataset_results_review_package_digest", None)
    if "output_root" in payload:
        payload["output_root"] = DEFAULT_OUTPUT_ROOT.as_posix()
    return payload


def canonical_dataset_results_review_package_digest_v1(package: dict[str, Any]) -> str:
    """Return a deterministic, output-location-independent review digest."""
    return semantic_digest(_digest_payload(package))


def build_canonical_dataset_results_review_package_v1(
    *, output_root: str | Path | None = None,
) -> dict[str, Any]:
    """Build a review package by reading, never changing, all nine generated outputs."""
    root = Path(output_root) if output_root is not None else DEFAULT_OUTPUT_ROOT
    try:
        payloads, output_manifest, record_counts = _verified_outputs(root)
        run = payloads["canonical_dataset_generation_run_manifest.json"]
        quality = payloads["canonical_dataset_data_quality_report.json"]
        failures = payloads["canonical_dataset_failure_reason_inventory.json"]
        _expect(quality.get("quality_status"), "PASS_WITH_PRESERVED_SOURCE_LIMITATION", "quality status")
        _expect(quality.get("failure_count"), 0, "quality failure count")
        _expect(quality.get("warning_count"), 1, "quality warning count")
        _expect_true(quality.get("no_missing_bars_fabricated"), "no_missing_bars_fabricated")
        _expect_true(quality.get("no_backfill_performed"), "no_backfill_performed")
        _expect_true(quality.get("meta_reduced_bar_count_preserved"), "meta_reduced_bar_count_preserved")
        _expect(failures.get("canonical_dataset_failure_reason_inventory"), [], "failure inventory")
    except (CanonicalDatasetResultsReviewError, generation.CanonicalDatasetGenerationExecutionError) as exc:
        return _blocked_package(str(exc))

    package = _base_package(run)
    package.update({
        "review_status": CANONICAL_DATASET_RESULTS_REVIEW_PACKAGE_READY,
        "output_root": root.as_posix(),
        "output_file_inspection_performed": True,
        "output_digest_manifest": output_manifest,
        "records_digest": next(row["sha256"] for row in output_manifest if row["filename"] == "canonical_dataset_records.jsonl"),
        "per_ticker_record_counts": record_counts,
        "per_ticker_canonical_record_summary": deepcopy(run["per_ticker_canonical_record_summary"]),
        "source_profile": deepcopy(run["canonical_dataset_source_profile"]),
        "digest_manifest_self_reference_non_applicable": True,
        "data_quality_summary": {
            "quality_status": quality.get("quality_status"),
            "failure_count": quality.get("failure_count"),
            "warning_count": quality.get("warning_count"),
            "warnings": deepcopy(quality.get("warnings")),
            "no_missing_bars_fabricated": quality.get("no_missing_bars_fabricated"),
            "no_backfill_performed": quality.get("no_backfill_performed"),
            "meta_reduced_bar_count_preserved": quality.get("meta_reduced_bar_count_preserved"),
            "reviewed_failure_inventory": deepcopy(failures.get("canonical_dataset_failure_reason_inventory")),
        },
    })
    package["review_checklist"] = _review_checklist(package)
    package["review_summary"] = _summary(package["review_checklist"])
    package["canonical_dataset_results_review_package_digest"] = (
        canonical_dataset_results_review_package_digest_v1(package)
    )
    validate_canonical_dataset_results_review_package_v1(package)
    return package


def validate_canonical_dataset_results_review_package_v1(
    review_package: dict[str, Any],
) -> dict[str, Any]:
    """Validate result facts, digest bindings, and every closed authority boundary."""
    if not isinstance(review_package, dict):
        raise CanonicalDatasetResultsReviewError("review_package must be an object")
    _expect(review_package.get("artifact_kind"), ARTIFACT_KIND_CANONICAL_DATASET_RESULTS_REVIEW_PACKAGE, "artifact_kind")
    _expect(review_package.get("schema_version"), SCHEMA_VERSION_CANONICAL_DATASET_RESULTS_REVIEW_V1, "schema_version")
    if review_package.get("review_status") == CANONICAL_DATASET_RESULTS_REVIEW_BLOCKED_MISSING_OR_INVALID_OUTPUTS:
        _expect_false(review_package.get("output_file_inspection_performed"), "output_file_inspection_performed")
        _expect_false(review_package.get("canonical_dataset_outputs_verified"), "canonical_dataset_outputs_verified")
        _expect_false(review_package.get("canonical_dataset_results_review_ready"), "canonical_dataset_results_review_ready")
        _expect_false(review_package.get("canonical_dataset_results_review_created"), "canonical_dataset_results_review_created")
        _expect_false(review_package.get("ready_for_canonical_dataset_freeze"), "ready_for_canonical_dataset_freeze")
        digest = review_package.get("canonical_dataset_results_review_package_digest")
        _expect_digest(digest, "canonical_dataset_results_review_package_digest")
        _expect(digest, canonical_dataset_results_review_package_digest_v1(review_package), "review package digest")
        return {"status": "CANONICAL_DATASET_RESULTS_REVIEW_BLOCKED_VALID", "review_status": review_package["review_status"]}

    _expect(review_package.get("review_status"), CANONICAL_DATASET_RESULTS_REVIEW_PACKAGE_READY, "review_status")
    expected = {
        "source_execution_artifact_kind": generation.ARTIFACT_KIND_CANONICAL_DATASET_GENERATED,
        "source_execution_status": generation.CANONICAL_DATASET_GENERATED_RESEARCH_ONLY,
        "source_canonical_dataset_generation_digest": EXPECTED_CANONICAL_DATASET_GENERATION_DIGEST,
        "source_canonical_dataset_generation_approval_digest": EXPECTED_CANONICAL_DATASET_GENERATION_APPROVAL_DIGEST,
        "canonical_dataset_generation_digest": EXPECTED_CANONICAL_DATASET_GENERATION_DIGEST,
        "canonical_dataset_generation_approval_digest": EXPECTED_CANONICAL_DATASET_GENERATION_APPROVAL_DIGEST,
        "target_universe": EXPECTED_TARGET_UNIVERSE,
        "target_universe_count": 12,
        "date_range_start": EXPECTED_SOURCE_PROFILE["date_range_start"],
        "date_range_end": EXPECTED_SOURCE_PROFILE["date_range_end"],
        "timeframe": EXPECTED_SOURCE_PROFILE["timeframe"],
        "profile": EXPECTED_SOURCE_PROFILE["profile"],
        "source_profile": EXPECTED_SOURCE_PROFILE,
        "source_evidence_scope": SOURCE_EVIDENCE_SCOPE,
        "dataset_scope": DATASET_SCOPE,
        "output_label": OUTPUT_LABEL,
        "generated_output_count": 9,
        "records_digest": EXPECTED_CANONICAL_RECORDS_SHA256,
        "per_ticker_record_counts": EXPECTED_RECORD_COUNTS,
        "total_canonical_record_count": 11946,
        "limitations": LIMITATIONS,
        "next_gates": NEXT_GATES,
        "predictive_usefulness": NOT_ACCEPTED,
        "profitability": NOT_ACCEPTED,
        "runtime_use": NOT_AUTHORIZED,
        "strategy_use": NOT_AUTHORIZED,
        "paper_trading": NOT_AUTHORIZED,
        "broker_execution": NOT_AUTHORIZED,
    }
    for field, value in expected.items():
        _expect(review_package.get(field), value, field)
    for field in (
        "created_offline", "dataset_generation_authorized", "canonical_dataset_authorized",
        "canonical_dataset_generation_approved", "canonical_dataset_candidate_created",
        "canonical_dataset_generation_executed", "canonical_dataset_generated",
        "canonical_dataset_generation_results_created", "canonical_dataset_results_review_created",
        "canonical_dataset_results_review_ready", "ready_for_canonical_dataset_freeze",
        "canonical_dataset_chain_candidate_created", "canonical_dataset_chain_candidate_review_created",
        "new_ticker_acquisition_authorized", "acquisition_generation_authorized",
        "acquisition_generation_approved", "acquisition_generation_frozen",
        "corporate_action_authority_created", "corporate_action_authority_approved",
        "split_event_authority_created", "split_event_authority_frozen",
        "dividend_event_authority_created", "dividend_event_authority_frozen",
        "identity_authority_created", "identity_authority_frozen", "research_only",
        "operator_review_required", "output_file_inspection_performed",
        "canonical_dataset_results_available", "canonical_dataset_outputs_verified",
        "canonical_dataset_record_count_verified", "canonical_dataset_results_support_future_freeze",
        "digest_manifest_self_reference_non_applicable",
    ):
        _expect_true(review_package.get(field), field)
    for field in (
        "provider_requests_made_in_review", "live_provider_transport_enabled_in_review",
        "market_data_acquisition_performed_in_review", "dataset_generation_performed_in_review",
        "canonical_dataset_regenerated_in_review", "raw_provider_payloads_committed",
        "api_keys_stored_or_printed", "canonical_dataset_frozen", "registry_approval_created",
        "additional_predictive_evidence_execution_authorized", "additional_predictive_evidence_executed",
        "predictive_experiment_rerun_authorized", "predictive_experiment_rerun_performed",
        "feature_matrix_regeneration_performed", "new_strategy_scoring_performed",
        "trade_recommendations_generated", "runtime_migration_approved", "runtime_migration_active",
        "automatic_stitching", "canonical_dataset_results_create_freeze_authority",
        "canonical_dataset_results_create_registry_approval",
        "canonical_dataset_results_create_predictive_evidence_authority",
        "canonical_dataset_results_create_runtime_authority", "canonical_dataset_freeze_artifact_created",
        "registry_approval_artifact_created", "predictive_usefulness_acceptance_artifact_created",
        "profitability_acceptance_created", "runtime_migration_approval_created",
    ):
        _expect_false(review_package.get(field), field)
    for field in (
        "canonical_dataset_generation_digest", "canonical_dataset_generation_approval_digest",
        "canonical_dataset_chain_candidate_review_package_digest", "canonical_dataset_chain_candidate_digest",
        "acquisition_generation_freeze_digest", "acquisition_generation_approval_digest",
        "acquisition_evidence_results_review_package_digest", "acquisition_provider_evidence_execution_digest",
        "corporate_action_authority_approval_digest", "identity_authority_freeze_digest",
        "ticker_universe_selection_approval_digest", "canonical_dataset_results_review_package_digest",
    ):
        _expect_digest(review_package.get(field), field)
    manifest = review_package.get("output_digest_manifest")
    if not isinstance(manifest, list) or len(manifest) != 9:
        raise CanonicalDatasetResultsReviewError("output_digest_manifest mismatch")
    _expect([row.get("filename") for row in manifest], EXPECTED_OUTPUT_FILENAMES, "output digest filenames")
    for row in manifest:
        _expect_digest(row.get("sha256"), f"{row.get('filename')}.sha256")
        _expect(row.get("output_label"), OUTPUT_LABEL, f"{row.get('filename')}.output_label")
        _expect(row.get("dataset_scope"), DATASET_SCOPE, f"{row.get('filename')}.dataset_scope")
        _expect_true(row.get("verified"), f"{row.get('filename')}.verified")
    _expect(
        next(row["sha256"] for row in manifest if row["filename"] == "canonical_dataset_records.jsonl"),
        EXPECTED_CANONICAL_RECORDS_SHA256,
        "records output digest binding",
    )
    checklist = review_package.get("review_checklist")
    if not isinstance(checklist, list):
        raise CanonicalDatasetResultsReviewError("review_checklist missing")
    _expect([row.get("check_id") for row in checklist], REQUIRED_CHECK_IDS, "review checklist ids")
    _expect(checklist, _review_checklist(review_package), "review checklist")
    if any(row.get("status") != PASS or row.get("severity") != BLOCKER for row in checklist):
        raise CanonicalDatasetResultsReviewError("review checklist must pass")
    _expect(review_package.get("review_summary"), _summary(checklist), "review_summary")
    digest = review_package.get("canonical_dataset_results_review_package_digest")
    _expect(digest, canonical_dataset_results_review_package_digest_v1(review_package), "review package digest")
    return {
        "status": CANONICAL_DATASET_RESULTS_REVIEW_PACKAGE_READY,
        "canonical_dataset_results_review_package_digest": digest,
        "total_checks": review_package["review_summary"]["total_checks"],
        "passed_checks": review_package["review_summary"]["passed_checks"],
        "failed_checks": review_package["review_summary"]["failed_checks"],
        "blocker_count": review_package["review_summary"]["blocker_count"],
    }


def build_canonical_dataset_results_review_markdown_v1(review_package: dict[str, Any]) -> str:
    """Render a sanitized Markdown view of a ready canonical results review."""
    validation = validate_canonical_dataset_results_review_package_v1(review_package)
    sections = [
        ("Canonical Dataset Results Review Package", [f"Artifact/status: `{review_package['artifact_kind']}` / `{validation['status']}`.", f"Review digest: `{validation['canonical_dataset_results_review_package_digest']}`."]),
        ("Source Canonical Dataset Generation", [f"Generation/approval digests: `{review_package['canonical_dataset_generation_digest']}` / `{review_package['canonical_dataset_generation_approval_digest']}`."]),
        ("Target Universe", [", ".join(f"`{ticker}`" for ticker in review_package["target_universe"]) + "."]),
        ("Source Profile", [f"`{key}`: `{value}`." for key, value in review_package["source_profile"].items()]),
        ("Per-Ticker Canonical Record Summary", [f"`{ticker}`: `{count}` records." for ticker, count in review_package["per_ticker_record_counts"].items()]),
        ("META Reduced Record Count Preservation", ["META remains exactly `913`; no repair, inference, smoothing, or backfill occurred."]),
        ("Output Digest Manifest", [f"`{row['filename']}`: `{row['sha256']}`." for row in review_package["output_digest_manifest"]]),
        ("Data Quality Summary", [f"Status: `{review_package['data_quality_summary']['quality_status']}`; failures/warnings: `{review_package['data_quality_summary']['failure_count']} / {review_package['data_quality_summary']['warning_count']}`."]),
        ("Limitations", [f"`{item}`" for item in review_package["limitations"]]),
        ("Next Gates", [f"`{item}`" for item in review_package["next_gates"]]),
        ("Canonical Dataset Freeze Boundary", ["The review supports a future freeze ceremony but creates no freeze authority or freeze artifact."]),
        ("Registry Boundary", ["No registry approval was created."]),
        ("Predictive/Profitability Boundary", ["Predictive usefulness and profitability remain not accepted."]),
        ("Runtime Boundary", ["Runtime, strategy, paper trading, and broker execution remain `NOT_AUTHORIZED`."]),
        ("Checklist Summary", [f"Total/passed/failed/blockers: `{validation['total_checks']} / {validation['passed_checks']} / {validation['failed_checks']} / {validation['blocker_count']}`."]),
        ("Guardrails", ["No provider request, acquisition, dataset regeneration, raw payload commit, secret access, experiment rerun, strategy scoring, runtime activation, or trading action occurred."]),
    ]
    lines = ["# MarketFlow Canonical Dataset Results Review Status", "", "## Title", "", "- Canonical Dataset Results Review Package v1.", ""]
    for title, body in sections:
        lines.extend([f"## {title}", "", *[f"- {item}" for item in body], ""])
    return "\n".join(lines)


def write_canonical_dataset_results_review_package_v1(
    output_dir: str | Path, *, output_root: str | Path | None = None,
) -> dict[str, Any]:
    """Write canonical review JSON without overwriting an existing artifact."""
    package = build_canonical_dataset_results_review_package_v1(output_root=output_root)
    validation = validate_canonical_dataset_results_review_package_v1(package)
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "canonical_dataset_results_review_package_v1.json"
    if path.exists():
        raise CanonicalDatasetResultsReviewError("canonical dataset results review output already exists")
    payload = canonical_json_bytes(package)
    path.write_bytes(payload)
    return {
        "path": str(path),
        "artifact_kind": package["artifact_kind"],
        "review_status": package["review_status"],
        "canonical_dataset_results_review_package_digest": validation["canonical_dataset_results_review_package_digest"],
        "payload_sha256": sha256_bytes(payload),
    }
