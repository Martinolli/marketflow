from __future__ import annotations

import json
from copy import deepcopy
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest

import marketflow.services as services
from marketflow.historical_data.artifacts import canonical_json_bytes, sha256_bytes
from marketflow.services import canonical_dataset_generation_execution_service as generation
from marketflow.services import canonical_dataset_results_review_service as review


def _build_synthetic_acquisition_source(root: Path) -> None:
    common = {"output_label": generation.OUTPUT_LABEL, "evidence_scope": generation.SOURCE_EVIDENCE_SCOPE}
    start = datetime(2022, 1, 3, 13, 0, tzinfo=UTC)
    result_rows = []
    for ticker in generation.TARGET_UNIVERSE:
        count = generation.EXPECTED_RECORD_COUNTS[ticker]
        bars = [
            {
                "bar_index": index,
                "timestamp": str(int((start + timedelta(days=index)).timestamp() * 1000)),
                "open": f"{100 + index / 100:.2f}",
                "high": f"{101 + index / 100:.2f}",
                "low": f"{99 + index / 100:.2f}",
                "close": f"{100.5 + index / 100:.2f}",
                "volume": str(1_000_000 + index),
                "volume_weighted_average_price": f"{100.25 + index / 100:.2f}",
                "transaction_count": str(10_000 + index),
            }
            for index in range(count)
        ]
        result_rows.append({
            "ticker": ticker,
            "historical_bar_count": count,
            "sanitized_bars": bars,
            "adjustment_policy_status": "PROVIDER_ADJUSTED_TRUE_SELECTED_ENDPOINT_LIMITATION_RECORDED",
            "calendar_alignment_status": "NOT_EVALUATED_SELECTED_ENDPOINT",
            "provider_request_metadata": {
                "provider_name": "SyntheticOfflineFixture",
                "provider_endpoint_stability": "CURRENT_STOCKS_V2_AGGS_RANGE_DAILY",
            },
        })
    payloads = {
        "acquisition_provider_evidence_run_manifest.json": common | {
            "target_universe": generation.TARGET_UNIVERSE,
            "acquisition_profile": {
                "date_range_start": "2022-01-01", "date_range_end": "2025-12-31",
                "timeframe": "1d", "session_profile": "RTH_FULL_SESSION_1D",
            },
        },
        "acquisition_provider_request_receipts_sanitized.json": common | {"request_receipts_sanitized": []},
        "acquisition_evidence_results_sanitized.json": common | {"per_ticker_acquisition_evidence_results": result_rows},
        "acquisition_data_quality_summary.json": common | {"acquisition_data_quality_summary": []},
        "acquisition_failure_reason_inventory.json": common | {"acquisition_failure_reason_inventory": []},
        "operator_review_summary.json": common | {"operator_review_required": True},
    }
    for name, payload in payloads.items():
        (root / name).write_bytes(canonical_json_bytes(payload))
    rows = [
        {"filename": name, "sha256": sha256_bytes((root / name).read_bytes())}
        for name in payloads if name != "operator_review_summary.json"
    ]
    (root / "acquisition_digest_manifest.json").write_bytes(canonical_json_bytes(common | {"output_digests": rows}))


@pytest.fixture(scope="module")
def ready_review(tmp_path_factory: pytest.TempPathFactory) -> tuple[dict, Path]:
    source = tmp_path_factory.mktemp("review_source")
    output = tmp_path_factory.mktemp("review_outputs_parent") / "outputs"
    _build_synthetic_acquisition_source(source)
    generated = generation.execute_canonical_dataset_generation_v1(
        source_root=source, output_root=output, run_timestamp_utc="2026-08-14T16:00:00Z"
    )
    assert generated["artifact_kind"] == generation.ARTIFACT_KIND_CANONICAL_DATASET_GENERATED
    records_digest = sha256_bytes((output / "canonical_dataset_records.jsonl").read_bytes())
    monkeypatch = pytest.MonkeyPatch()
    monkeypatch.setattr(review, "EXPECTED_CANONICAL_DATASET_GENERATION_DIGEST", generated["canonical_dataset_generation_digest"])
    monkeypatch.setattr(review, "EXPECTED_CANONICAL_RECORDS_SHA256", records_digest)
    package = review.build_canonical_dataset_results_review_package_v1(output_root=output)
    yield package, output
    monkeypatch.undo()


def test_review_package_builds_offline_without_provider_calls(ready_review: tuple[dict, Path]) -> None:
    package, _ = ready_review
    assert package["created_offline"] is True
    assert package["provider_requests_made_in_review"] is False


def test_review_is_blocked_when_outputs_are_missing(tmp_path: Path) -> None:
    package = review.build_canonical_dataset_results_review_package_v1(output_root=tmp_path / "missing")
    assert package["review_status"] == review.CANONICAL_DATASET_RESULTS_REVIEW_BLOCKED_MISSING_OR_INVALID_OUTPUTS
    assert package["output_file_inspection_performed"] is False
    assert package["canonical_dataset_results_review_created"] is False
    assert package["ready_for_canonical_dataset_freeze"] is False
    assert package["review_summary"]["ready_for_operator_review"] is False
    assert review.validate_canonical_dataset_results_review_package_v1(package)["status"] == "CANONICAL_DATASET_RESULTS_REVIEW_BLOCKED_VALID"


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("artifact_kind", "CANONICAL_DATASET_RESULTS_REVIEW_PACKAGE"),
        ("review_status", "CANONICAL_DATASET_RESULTS_REVIEW_PACKAGE_READY"),
        ("source_canonical_dataset_generation_approval_digest", review.EXPECTED_CANONICAL_DATASET_GENERATION_APPROVAL_DIGEST),
        ("canonical_dataset_chain_candidate_review_package_digest", generation.approval_service.EXPECTED_CANONICAL_DATASET_CHAIN_CANDIDATE_REVIEW_PACKAGE_DIGEST),
        ("acquisition_generation_freeze_digest", generation.approval_service.EXPECTED_ACQUISITION_GENERATION_FREEZE_DIGEST),
        ("target_universe_count", 12),
        ("target_universe", review.EXPECTED_TARGET_UNIVERSE),
        ("generated_output_count", 9),
        ("total_canonical_record_count", 11946),
        ("per_ticker_record_counts", review.EXPECTED_RECORD_COUNTS),
        ("source_profile", review.EXPECTED_SOURCE_PROFILE),
        ("dataset_scope", "CANONICAL_DATASET_GENERATION_RESEARCH_ONLY"),
        ("canonical_dataset_outputs_verified", True),
        ("digest_manifest_self_reference_non_applicable", True),
        ("provider_requests_made_in_review", False),
        ("live_provider_transport_enabled_in_review", False),
        ("market_data_acquisition_performed_in_review", False),
        ("dataset_generation_performed_in_review", False),
        ("canonical_dataset_regenerated_in_review", False),
        ("raw_provider_payloads_committed", False),
        ("api_keys_stored_or_printed", False),
        ("canonical_dataset_generated", True),
        ("canonical_dataset_frozen", False),
        ("registry_approval_created", False),
        ("additional_predictive_evidence_execution_authorized", False),
        ("additional_predictive_evidence_executed", False),
        ("predictive_usefulness", "not accepted"),
        ("profitability", "not accepted"),
        ("runtime_migration_approved", False),
        ("runtime_use", "NOT_AUTHORIZED"),
        ("strategy_use", "NOT_AUTHORIZED"),
        ("paper_trading", "NOT_AUTHORIZED"),
        ("broker_execution", "NOT_AUTHORIZED"),
        ("canonical_dataset_results_support_future_freeze", True),
        ("canonical_dataset_results_create_freeze_authority", False),
        ("canonical_dataset_results_create_registry_approval", False),
        ("canonical_dataset_results_create_runtime_authority", False),
        ("limitations", review.LIMITATIONS),
        ("next_gates", review.NEXT_GATES),
    ],
)
def test_ready_review_contract(ready_review: tuple[dict, Path], field: str, expected: object) -> None:
    package, _ = ready_review
    assert package[field] == expected


def test_source_generation_and_records_digests_are_bound(ready_review: tuple[dict, Path]) -> None:
    package, _ = ready_review
    assert package["source_canonical_dataset_generation_digest"] == review.EXPECTED_CANONICAL_DATASET_GENERATION_DIGEST
    assert package["records_digest"] == review.EXPECTED_CANONICAL_RECORDS_SHA256


def test_meta_and_non_meta_counts_are_preserved(ready_review: tuple[dict, Path]) -> None:
    package, _ = ready_review
    assert package["per_ticker_record_counts"]["META"] == 913
    assert all(count == 1003 for ticker, count in package["per_ticker_record_counts"].items() if ticker != "META")


def test_output_digests_are_bound_for_all_outputs(ready_review: tuple[dict, Path]) -> None:
    package, output = ready_review
    assert [row["filename"] for row in package["output_digest_manifest"]] == review.EXPECTED_OUTPUT_FILENAMES
    assert all(row["verified"] is True and len(row["sha256"]) == 64 for row in package["output_digest_manifest"])
    assert {row["filename"]: row["sha256"] for row in package["output_digest_manifest"]} == {
        name: sha256_bytes((output / name).read_bytes()) for name in review.EXPECTED_OUTPUT_FILENAMES
    }


def test_checklist_contains_all_required_ids_and_passes(ready_review: tuple[dict, Path]) -> None:
    package, _ = ready_review
    assert [row["check_id"] for row in package["review_checklist"]] == review.REQUIRED_CHECK_IDS
    assert all(row["status"] == "PASS" and row["severity"] == "BLOCKER" for row in package["review_checklist"])


def test_summary_counts_are_correct(ready_review: tuple[dict, Path]) -> None:
    package, _ = ready_review
    summary = package["review_summary"]
    assert summary["total_checks"] == len(review.REQUIRED_CHECK_IDS) == 53
    assert summary["passed_checks"] == 53
    assert summary["failed_checks"] == 0
    assert summary["blocker_count"] == 0
    assert summary["ready_for_canonical_dataset_freeze"] is True
    assert summary["ready_for_research_registry_candidate"] is False


def test_review_package_digest_is_deterministic(ready_review: tuple[dict, Path]) -> None:
    package, output = ready_review
    repeated = review.build_canonical_dataset_results_review_package_v1(output_root=output)
    assert repeated["canonical_dataset_results_review_package_digest"] == package["canonical_dataset_results_review_package_digest"]


def test_validator_accepts_valid_review_package(ready_review: tuple[dict, Path]) -> None:
    package, _ = ready_review
    result = review.validate_canonical_dataset_results_review_package_v1(package)
    assert result["status"] == "CANONICAL_DATASET_RESULTS_REVIEW_PACKAGE_READY"
    assert result["blocker_count"] == 0


@pytest.mark.parametrize(
    ("field", "invalid"),
    [
        ("artifact_kind", "WRONG"),
        ("review_status", "WRONG"),
        ("source_canonical_dataset_generation_digest", "0" * 64),
        ("source_canonical_dataset_generation_approval_digest", "0" * 64),
        ("target_universe", list(reversed(review.EXPECTED_TARGET_UNIVERSE))),
        ("generated_output_count", 8),
        ("records_digest", "0" * 64),
        ("total_canonical_record_count", 11945),
        ("provider_requests_made_in_review", True),
        ("live_provider_transport_enabled_in_review", True),
        ("market_data_acquisition_performed_in_review", True),
        ("dataset_generation_performed_in_review", True),
        ("canonical_dataset_regenerated_in_review", True),
        ("raw_provider_payloads_committed", True),
        ("api_keys_stored_or_printed", True),
        ("canonical_dataset_frozen", True),
        ("registry_approval_created", True),
        ("additional_predictive_evidence_execution_authorized", True),
        ("predictive_usefulness", "accepted"),
        ("profitability", "accepted"),
        ("runtime_migration_approved", True),
        ("runtime_use", "AUTHORIZED"),
        ("strategy_use", "AUTHORIZED"),
        ("paper_trading", "AUTHORIZED"),
        ("broker_execution", "AUTHORIZED"),
        ("automatic_stitching", True),
        ("canonical_dataset_results_create_freeze_authority", True),
        ("canonical_dataset_results_create_registry_approval", True),
        ("canonical_dataset_results_create_runtime_authority", True),
        ("limitations", []),
        ("next_gates", []),
        ("canonical_dataset_results_review_package_digest", None),
    ],
)
def test_validator_rejects_invalid_contract_fields(
    ready_review: tuple[dict, Path], field: str, invalid: object
) -> None:
    package, _ = ready_review
    changed = deepcopy(package)
    changed[field] = invalid
    with pytest.raises(review.CanonicalDatasetResultsReviewError):
        review.validate_canonical_dataset_results_review_package_v1(changed)


@pytest.mark.parametrize(("ticker", "count"), [("META", 914), ("MSFT", 1002)])
def test_validator_rejects_wrong_per_ticker_count(
    ready_review: tuple[dict, Path], ticker: str, count: int
) -> None:
    package, _ = ready_review
    changed = deepcopy(package)
    changed["per_ticker_record_counts"][ticker] = count
    with pytest.raises(review.CanonicalDatasetResultsReviewError):
        review.validate_canonical_dataset_results_review_package_v1(changed)


def test_validator_rejects_non_research_output_label(ready_review: tuple[dict, Path]) -> None:
    package, _ = ready_review
    changed = deepcopy(package)
    changed["output_digest_manifest"][0]["output_label"] = "ACTIONABLE"
    with pytest.raises(review.CanonicalDatasetResultsReviewError):
        review.validate_canonical_dataset_results_review_package_v1(changed)


def test_validator_rejects_ready_status_without_verified_outputs(ready_review: tuple[dict, Path]) -> None:
    package, _ = ready_review
    changed = deepcopy(package)
    changed["output_file_inspection_performed"] = False
    changed["canonical_dataset_outputs_verified"] = False
    changed["output_digest_manifest"] = []
    with pytest.raises(review.CanonicalDatasetResultsReviewError):
        review.validate_canonical_dataset_results_review_package_v1(changed)


def test_markdown_includes_required_sections(ready_review: tuple[dict, Path]) -> None:
    package, _ = ready_review
    markdown = review.build_canonical_dataset_results_review_markdown_v1(package)
    required = [
        "Title", "Canonical Dataset Results Review Package", "Source Canonical Dataset Generation",
        "Target Universe", "Source Profile", "Per-Ticker Canonical Record Summary",
        "META Reduced Record Count Preservation", "Output Digest Manifest", "Data Quality Summary",
        "Limitations", "Next Gates", "Canonical Dataset Freeze Boundary", "Registry Boundary",
        "Predictive/Profitability Boundary", "Runtime Boundary", "Checklist Summary", "Guardrails",
    ]
    assert all(f"## {heading}" in markdown for heading in required)


def test_writer_writes_once_without_overwrite(ready_review: tuple[dict, Path], tmp_path: Path) -> None:
    package, output = ready_review
    result = review.write_canonical_dataset_results_review_package_v1(tmp_path, output_root=output)
    written = json.loads(Path(result["path"]).read_text(encoding="utf-8"))
    assert written["canonical_dataset_results_review_package_digest"] == package["canonical_dataset_results_review_package_digest"]
    with pytest.raises(review.CanonicalDatasetResultsReviewError):
        review.write_canonical_dataset_results_review_package_v1(tmp_path, output_root=output)


def test_service_exports_are_available() -> None:
    assert services.build_canonical_dataset_results_review_package_v1 is review.build_canonical_dataset_results_review_package_v1
    assert services.validate_canonical_dataset_results_review_package_v1 is review.validate_canonical_dataset_results_review_package_v1
    assert services.write_canonical_dataset_results_review_package_v1 is review.write_canonical_dataset_results_review_package_v1
