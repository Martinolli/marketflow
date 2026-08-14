from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

import pytest

import marketflow.services as services
from marketflow.services import canonical_dataset_freeze_service as freeze
from marketflow.services import canonical_dataset_results_review_service as review


def _source_review() -> dict:
    package = review._base_package({
        "canonical_dataset_generation_digest": review.EXPECTED_CANONICAL_DATASET_GENERATION_DIGEST
    })
    manifest = []
    for index, name in enumerate(review.EXPECTED_OUTPUT_FILENAMES):
        digest = review.EXPECTED_CANONICAL_RECORDS_SHA256 if name == "canonical_dataset_records.jsonl" else f"{index + 1:064x}"
        manifest.append({
            "filename": name,
            "sha256": digest,
            "output_label": review.OUTPUT_LABEL,
            "dataset_scope": review.DATASET_SCOPE,
            "verified": True,
            "source_manifest_digest_kind": "FILE_SHA256",
            "source_manifest_digest": digest,
        })
    package.update({
        "review_status": review.CANONICAL_DATASET_RESULTS_REVIEW_PACKAGE_READY,
        "output_root": review.DEFAULT_OUTPUT_ROOT.as_posix(),
        "output_file_inspection_performed": True,
        "output_digest_manifest": manifest,
        "records_digest": review.EXPECTED_CANONICAL_RECORDS_SHA256,
        "per_ticker_record_counts": deepcopy(review.EXPECTED_RECORD_COUNTS),
        "per_ticker_canonical_record_summary": [],
        "source_profile": deepcopy(review.EXPECTED_SOURCE_PROFILE),
        "digest_manifest_self_reference_non_applicable": True,
        "data_quality_summary": {
            "quality_status": "PASS_WITH_PRESERVED_SOURCE_LIMITATION",
            "failure_count": 0,
            "warning_count": 1,
            "warnings": ["META_REDUCED_BAR_COUNT_PRESERVED_EXACTLY_913_NO_REPAIR_OR_BACKFILL"],
            "no_missing_bars_fabricated": True,
            "no_backfill_performed": True,
            "meta_reduced_bar_count_preserved": True,
            "reviewed_failure_inventory": [],
        },
    })
    package["review_checklist"] = review._review_checklist(package)
    package["review_summary"] = review._summary(package["review_checklist"])
    package["canonical_dataset_results_review_package_digest"] = (
        review.canonical_dataset_results_review_package_digest_v1(package)
    )
    review.validate_canonical_dataset_results_review_package_v1(package)
    return package


def _attestation() -> dict:
    return freeze.build_canonical_dataset_freeze_attestation_v1(
        operator_reference="TEST_OPERATOR",
        operator_attestation_timestamp_utc="2026-08-14T17:30:00Z",
        operator_attestation_phrase=freeze.REQUIRED_CANONICAL_DATASET_FREEZE_ATTESTATION_PHRASE,
        operator_confirms_canonical_dataset_results_review_digest=freeze.EXPECTED_CANONICAL_DATASET_RESULTS_REVIEW_PACKAGE_DIGEST,
        operator_confirms_canonical_dataset_generation_digest=freeze.EXPECTED_CANONICAL_DATASET_GENERATION_DIGEST,
        operator_confirms_canonical_dataset_generation_approval_digest=freeze.EXPECTED_CANONICAL_DATASET_GENERATION_APPROVAL_DIGEST,
        operator_confirms_acquisition_generation_freeze_digest=freeze.EXPECTED_ACQUISITION_GENERATION_FREEZE_DIGEST,
        operator_confirms_corporate_action_authority_approval_digest=freeze.EXPECTED_CORPORATE_ACTION_AUTHORITY_APPROVAL_DIGEST,
        operator_confirms_identity_freeze_digest=freeze.EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST,
        operator_confirms_target_universe=list(freeze.TARGET_UNIVERSE),
        operator_confirms_target_count=12,
        operator_confirms_source_profile=True,
        operator_confirms_total_canonical_record_count=11946,
        operator_confirms_records_digest=freeze.EXPECTED_RECORDS_DIGEST,
        operator_confirms_meta_reduced_record_count_preserved=True,
        operator_confirms_freeze_scope_canonical_dataset_only=True,
        operator_confirms_canonical_dataset_generated=True,
        operator_confirms_canonical_dataset_freeze=True,
        operator_confirms_ready_for_research_registry_candidate=True,
        operator_confirms_no_registry_approval=True,
        operator_confirms_no_predictive_usefulness_acceptance=True,
        operator_confirms_no_profitability_acceptance=True,
        operator_confirms_no_runtime_migration_approval=True,
        operator_confirms_no_runtime_activation=True,
        operator_confirms_no_paper_trading=True,
        operator_confirms_no_broker_execution=True,
        operator_confirms_no_trade_recommendations=True,
        operator_confirms_no_api_key_storage_or_printing=True,
        operator_confirms_no_raw_payload_commit=True,
    )


@pytest.fixture(scope="module")
def frozen_context() -> tuple[dict, dict, dict]:
    source = _source_review()
    monkeypatch = pytest.MonkeyPatch()
    monkeypatch.setattr(
        freeze,
        "EXPECTED_CANONICAL_DATASET_RESULTS_REVIEW_PACKAGE_DIGEST",
        source["canonical_dataset_results_review_package_digest"],
    )
    attestation = _attestation()
    artifact = freeze.build_canonical_dataset_frozen_v1(
        canonical_dataset_results_review_package=source,
        operator_attestation=attestation,
    )
    yield artifact, source, attestation
    monkeypatch.undo()


def test_attestation_builder_creates_required_fields(frozen_context: tuple[dict, dict, dict]) -> None:
    _, _, attestation = frozen_context
    assert attestation["operator_decision"] == freeze.OPERATOR_DECISION_FREEZE_CANONICAL_DATASET
    assert attestation["operator_attestation_version"] == freeze.OPERATOR_ATTESTATION_VERSION_CANONICAL_DATASET_FREEZE_V1
    assert attestation["operator_reference"] == "TEST_OPERATOR"
    assert all(attestation[field] is True for field in freeze.REQUIRED_TRUE_OPERATOR_CONFIRMATION_FIELDS)


def test_frozen_artifact_builds_offline_without_provider_calls(
    frozen_context: tuple[dict, dict, dict], monkeypatch: pytest.MonkeyPatch
) -> None:
    _, source, attestation = frozen_context
    monkeypatch.setattr(
        freeze.review,
        "build_canonical_dataset_results_review_package_v1",
        lambda *args, **kwargs: pytest.fail("implicit results review build was called"),
    )
    artifact = freeze.build_canonical_dataset_frozen_v1(
        canonical_dataset_results_review_package=source,
        operator_attestation=attestation,
    )
    assert artifact["created_offline"] is True
    assert artifact["provider_requests_made_in_freeze"] is False


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("artifact_kind", "CANONICAL_DATASET_FROZEN"),
        ("freeze_status", "CANONICAL_DATASET_FROZEN"),
        ("freeze_scope", "CANONICAL_DATASET_FREEZE_ONLY"),
        ("canonical_dataset_generated", True),
        ("canonical_dataset_frozen", True),
        ("ready_for_research_registry_candidate", True),
        ("registry_approval_created", False),
        ("target_universe_count", 12),
        ("target_universe", freeze.TARGET_UNIVERSE),
        ("total_canonical_record_count", 11946),
        ("records_digest", freeze.EXPECTED_RECORDS_DIGEST),
        ("per_ticker_record_counts", freeze.EXPECTED_RECORD_COUNTS),
        ("canonical_dataset_generation_digest", freeze.EXPECTED_CANONICAL_DATASET_GENERATION_DIGEST),
        ("canonical_dataset_generation_approval_digest", freeze.EXPECTED_CANONICAL_DATASET_GENERATION_APPROVAL_DIGEST),
        ("acquisition_generation_freeze_digest", freeze.EXPECTED_ACQUISITION_GENERATION_FREEZE_DIGEST),
        ("corporate_action_authority_approval_digest", freeze.EXPECTED_CORPORATE_ACTION_AUTHORITY_APPROVAL_DIGEST),
        ("identity_authority_freeze_digest", freeze.EXPECTED_IDENTITY_AUTHORITY_FREEZE_DIGEST),
        ("provider_requests_made_in_freeze", False),
        ("live_provider_transport_enabled_in_freeze", False),
        ("market_data_acquisition_performed_in_freeze", False),
        ("dataset_generation_performed_in_freeze", False),
        ("canonical_dataset_regenerated_in_freeze", False),
        ("raw_provider_payloads_committed", False),
        ("api_keys_stored_or_printed", False),
        ("additional_predictive_evidence_execution_authorized", False),
        ("additional_predictive_evidence_executed", False),
        ("predictive_usefulness", "not accepted"),
        ("profitability", "not accepted"),
        ("runtime_migration_approved", False),
        ("runtime_use", "NOT_AUTHORIZED"),
        ("strategy_use", "NOT_AUTHORIZED"),
        ("paper_trading", "NOT_AUTHORIZED"),
        ("broker_execution", "NOT_AUTHORIZED"),
        ("canonical_dataset_freeze_creates_registry_approval", False),
        ("canonical_dataset_freeze_creates_predictive_evidence_authority", False),
        ("canonical_dataset_freeze_creates_runtime_authority", False),
    ],
)
def test_frozen_artifact_contract(
    frozen_context: tuple[dict, dict, dict], field: str, expected: object
) -> None:
    artifact, _, _ = frozen_context
    assert artifact[field] == expected


def test_source_review_digest_is_bound(frozen_context: tuple[dict, dict, dict]) -> None:
    artifact, source, _ = frozen_context
    assert artifact["canonical_dataset_results_review_package_digest"] == source["canonical_dataset_results_review_package_digest"]


def test_meta_and_non_meta_counts_are_frozen_exactly(frozen_context: tuple[dict, dict, dict]) -> None:
    artifact, _, _ = frozen_context
    assert artifact["per_ticker_record_counts"]["META"] == 913
    assert all(count == 1003 for ticker, count in artifact["per_ticker_record_counts"].items() if ticker != "META")


def test_per_ticker_entries_and_digests_are_present(frozen_context: tuple[dict, dict, dict]) -> None:
    artifact, _, _ = frozen_context
    entries = artifact["per_ticker_frozen_canonical_datasets"]
    assert len(entries) == 12
    assert [row["ticker"] for row in entries] == freeze.TARGET_UNIVERSE
    assert all(len(row["per_ticker_canonical_dataset_freeze_digest"]) == 64 for row in entries)
    meta = next(row for row in entries if row["ticker"] == "META")
    assert meta["canonical_dataset_freeze_status"] == freeze.FROZEN_WITH_REDUCED_RECORD_COUNT_PRESERVED


@pytest.mark.parametrize(
    ("field", "invalid"),
    [
        ("operator_attestation_phrase", "wrong"),
        ("operator_decision", "WRONG"),
        ("operator_confirms_canonical_dataset_results_review_digest", "0" * 64),
        ("operator_confirms_canonical_dataset_generation_digest", "0" * 64),
        ("operator_confirms_canonical_dataset_generation_approval_digest", "0" * 64),
        ("operator_confirms_acquisition_generation_freeze_digest", "0" * 64),
        ("operator_confirms_corporate_action_authority_approval_digest", "0" * 64),
        ("operator_confirms_identity_freeze_digest", "0" * 64),
        ("operator_confirms_target_universe", list(reversed(freeze.TARGET_UNIVERSE))),
        ("operator_confirms_target_count", 11),
        ("operator_confirms_source_profile", False),
        ("operator_confirms_total_canonical_record_count", 11945),
        ("operator_confirms_records_digest", "0" * 64),
        ("operator_confirms_meta_reduced_record_count_preserved", False),
        ("operator_confirms_freeze_scope_canonical_dataset_only", False),
        ("operator_confirms_canonical_dataset_generated", False),
        ("operator_confirms_canonical_dataset_freeze", False),
        ("operator_confirms_ready_for_research_registry_candidate", False),
        ("operator_confirms_no_registry_approval", False),
        ("operator_confirms_no_predictive_usefulness_acceptance", False),
        ("operator_confirms_no_profitability_acceptance", False),
        ("operator_confirms_no_runtime_migration_approval", False),
        ("operator_confirms_no_runtime_activation", False),
        ("operator_confirms_no_paper_trading", False),
        ("operator_confirms_no_broker_execution", False),
        ("operator_confirms_no_trade_recommendations", False),
        ("operator_confirms_no_api_key_storage_or_printing", False),
        ("operator_confirms_no_raw_payload_commit", False),
        ("operator_reference", ""),
        ("operator_attestation_timestamp_utc", ""),
    ],
)
def test_invalid_operator_attestation_is_rejected(
    frozen_context: tuple[dict, dict, dict], field: str, invalid: object
) -> None:
    _, source, attestation = frozen_context
    changed = deepcopy(attestation)
    changed[field] = invalid
    with pytest.raises(freeze.CanonicalDatasetFreezeError):
        freeze.build_canonical_dataset_frozen_v1(
            canonical_dataset_results_review_package=source,
            operator_attestation=changed,
        )


def test_validator_accepts_valid_freeze(frozen_context: tuple[dict, dict, dict]) -> None:
    artifact, _, _ = frozen_context
    result = freeze.validate_canonical_dataset_frozen_v1(artifact)
    assert result["status"] == "CANONICAL_DATASET_FROZEN"
    assert result["blocker_count"] == 0


@pytest.mark.parametrize(
    ("field", "invalid"),
    [
        ("artifact_kind", "WRONG"),
        ("freeze_status", "WRONG"),
        ("freeze_scope", "WRONG"),
        ("canonical_dataset_generated", False),
        ("canonical_dataset_frozen", False),
        ("ready_for_research_registry_candidate", False),
        ("registry_approval_created", True),
        ("target_universe", list(reversed(freeze.TARGET_UNIVERSE))),
        ("total_canonical_record_count", 11945),
        ("records_digest", "0" * 64),
        ("provider_requests_made_in_freeze", True),
        ("live_provider_transport_enabled_in_freeze", True),
        ("market_data_acquisition_performed_in_freeze", True),
        ("dataset_generation_performed_in_freeze", True),
        ("canonical_dataset_regenerated_in_freeze", True),
        ("raw_provider_payloads_committed", True),
        ("api_keys_stored_or_printed", True),
        ("predictive_usefulness", "accepted"),
        ("profitability", "accepted"),
        ("runtime_migration_approved", True),
        ("runtime_use", "AUTHORIZED"),
        ("strategy_use", "AUTHORIZED"),
        ("paper_trading", "AUTHORIZED"),
        ("broker_execution", "AUTHORIZED"),
        ("automatic_stitching", True),
        ("canonical_dataset_freeze_creates_registry_approval", True),
        ("canonical_dataset_freeze_creates_predictive_evidence_authority", True),
        ("canonical_dataset_freeze_creates_runtime_authority", True),
        ("operator_attestation", {}),
        ("canonical_dataset_freeze_digest", None),
    ],
)
def test_validator_rejects_invalid_contract_fields(
    frozen_context: tuple[dict, dict, dict], field: str, invalid: object
) -> None:
    artifact, _, _ = frozen_context
    changed = deepcopy(artifact)
    changed[field] = invalid
    with pytest.raises(freeze.CanonicalDatasetFreezeError):
        freeze.validate_canonical_dataset_frozen_v1(changed)


@pytest.mark.parametrize(("ticker", "count"), [("META", 914), ("MSFT", 1002)])
def test_validator_rejects_wrong_per_ticker_count(
    frozen_context: tuple[dict, dict, dict], ticker: str, count: int
) -> None:
    artifact, _, _ = frozen_context
    changed = deepcopy(artifact)
    changed["per_ticker_record_counts"][ticker] = count
    with pytest.raises(freeze.CanonicalDatasetFreezeError):
        freeze.validate_canonical_dataset_frozen_v1(changed)


def test_freeze_digest_is_deterministic(frozen_context: tuple[dict, dict, dict]) -> None:
    artifact, source, attestation = frozen_context
    repeated = freeze.build_canonical_dataset_frozen_v1(
        canonical_dataset_results_review_package=source,
        operator_attestation=attestation,
    )
    assert repeated["canonical_dataset_freeze_digest"] == artifact["canonical_dataset_freeze_digest"]


def test_per_ticker_freeze_digests_are_deterministic(frozen_context: tuple[dict, dict, dict]) -> None:
    artifact, source, attestation = frozen_context
    repeated = freeze.build_canonical_dataset_frozen_v1(
        canonical_dataset_results_review_package=source,
        operator_attestation=attestation,
    )
    assert [row["per_ticker_canonical_dataset_freeze_digest"] for row in repeated["per_ticker_frozen_canonical_datasets"]] == [
        row["per_ticker_canonical_dataset_freeze_digest"] for row in artifact["per_ticker_frozen_canonical_datasets"]
    ]


def test_markdown_includes_required_sections(frozen_context: tuple[dict, dict, dict]) -> None:
    artifact, _, _ = frozen_context
    markdown = freeze.build_canonical_dataset_frozen_markdown_v1(artifact)
    required = [
        "Title", "Frozen Canonical Dataset", "Operator Attestation",
        "Source Canonical Dataset Results Review", "Source Canonical Dataset Generation",
        "Target Universe", "Source Profile", "Frozen Per-Ticker Canonical Dataset Summary",
        "META Reduced Record Count Preservation", "Records Digest", "Freeze Scope",
        "Registry Boundary", "Predictive/Profitability Boundary", "Runtime Boundary",
        "Freeze Checklist Summary", "Remaining Required Tasks", "Guardrails",
    ]
    assert all(f"## {heading}" in markdown for heading in required)


def test_writer_writes_once_without_overwrite(
    frozen_context: tuple[dict, dict, dict], tmp_path: Path
) -> None:
    artifact, source, attestation = frozen_context
    result = freeze.write_canonical_dataset_frozen_v1(
        tmp_path,
        canonical_dataset_results_review_package=source,
        operator_attestation=attestation,
    )
    written = json.loads(Path(result["path"]).read_text(encoding="utf-8"))
    assert written["canonical_dataset_freeze_digest"] == artifact["canonical_dataset_freeze_digest"]
    with pytest.raises(freeze.CanonicalDatasetFreezeError):
        freeze.write_canonical_dataset_frozen_v1(
            tmp_path,
            canonical_dataset_results_review_package=source,
            operator_attestation=attestation,
        )


def test_service_exports_are_available() -> None:
    assert services.build_canonical_dataset_freeze_attestation_v1 is freeze.build_canonical_dataset_freeze_attestation_v1
    assert services.build_canonical_dataset_frozen_v1 is freeze.build_canonical_dataset_frozen_v1
    assert services.validate_canonical_dataset_frozen_v1 is freeze.validate_canonical_dataset_frozen_v1
