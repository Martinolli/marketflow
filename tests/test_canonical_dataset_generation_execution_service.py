from __future__ import annotations

import json
from copy import deepcopy
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest

import marketflow.services as services
from marketflow.historical_data.artifacts import canonical_json_bytes, sha256_bytes
from marketflow.services import canonical_dataset_generation_execution_service as execution_service


@pytest.fixture(scope="module")
def generated(tmp_path_factory: pytest.TempPathFactory) -> tuple[dict, Path, Path]:
    root = tmp_path_factory.mktemp("canonical_source")
    output = tmp_path_factory.mktemp("canonical_parent") / "outputs"
    common = {
        "output_label": "RESEARCH_ONLY_NON_ACTIONABLE",
        "evidence_scope": execution_service.SOURCE_EVIDENCE_SCOPE,
    }
    run_manifest = common | {
        "target_universe": execution_service.TARGET_UNIVERSE,
        "acquisition_profile": {
            "date_range_start": "2022-01-01",
            "date_range_end": "2025-12-31",
            "timeframe": "1d",
            "session_profile": "RTH_FULL_SESSION_1D",
        },
    }
    start = datetime(2022, 1, 3, 13, 0, tzinfo=UTC)
    rows = []
    for ticker in execution_service.TARGET_UNIVERSE:
        count = execution_service.EXPECTED_RECORD_COUNTS[ticker]
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
        rows.append({
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
    source_payloads = {
        "acquisition_provider_evidence_run_manifest.json": run_manifest,
        "acquisition_provider_request_receipts_sanitized.json": common | {"request_receipts_sanitized": []},
        "acquisition_evidence_results_sanitized.json": common | {"per_ticker_acquisition_evidence_results": rows},
        "acquisition_data_quality_summary.json": common | {"acquisition_data_quality_summary": []},
        "acquisition_failure_reason_inventory.json": common | {"acquisition_failure_reason_inventory": []},
        "operator_review_summary.json": common | {"operator_review_required": True},
    }
    for name, payload in source_payloads.items():
        (root / name).write_bytes(canonical_json_bytes(payload))
    digest_rows = [
        {"filename": name, "sha256": sha256_bytes((root / name).read_bytes())}
        for name in source_payloads
        if name != "operator_review_summary.json"
    ]
    (root / "acquisition_digest_manifest.json").write_bytes(
        canonical_json_bytes(common | {"output_digests": digest_rows})
    )
    artifact = execution_service.execute_canonical_dataset_generation_v1(
        source_root=root,
        output_root=output,
        run_timestamp_utc="2026-08-14T16:00:00Z",
    )
    return artifact, root, output


def test_execution_builds_offline_without_provider_calls(generated: tuple[dict, Path, Path]) -> None:
    artifact, _, _ = generated
    assert artifact["created_offline"] is True
    assert artifact["provider_requests_made_in_generation"] is False


def test_execution_blocks_when_source_evidence_is_missing(tmp_path: Path) -> None:
    artifact = execution_service.execute_canonical_dataset_generation_v1(
        source_root=tmp_path / "missing", output_root=tmp_path / "output", run_timestamp_utc="2026-08-14T16:00:00Z"
    )
    assert artifact["artifact_kind"] == execution_service.ARTIFACT_KIND_CANONICAL_DATASET_GENERATION_BLOCKED
    assert artifact["execution_status"] == execution_service.CANONICAL_DATASET_GENERATION_BLOCKED_MISSING_OR_INVALID_SOURCE_EVIDENCE
    assert artifact["canonical_dataset_generation_digest"] == "NOT_CREATED"
    assert artifact["generated_output_count"] == 0


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("artifact_kind", "CANONICAL_DATASET_GENERATED"),
        ("execution_status", "CANONICAL_DATASET_GENERATED_RESEARCH_ONLY"),
        ("dataset_generation_authorized", True),
        ("canonical_dataset_authorized", True),
        ("canonical_dataset_generation_approved", True),
        ("canonical_dataset_candidate_created", True),
        ("canonical_dataset_generation_executed", True),
        ("canonical_dataset_generated", True),
        ("canonical_dataset_frozen", False),
        ("registry_approval_created", False),
        ("target_universe_count", 12),
        ("target_universe", execution_service.TARGET_UNIVERSE),
        ("per_ticker_record_counts", execution_service.EXPECTED_RECORD_COUNTS),
        ("total_canonical_record_count", 11946),
        ("generated_output_count", 9),
        ("output_label", "RESEARCH_ONLY_NON_ACTIONABLE"),
        ("source_evidence_scope", "READ_ONLY_HISTORICAL_MARKET_DATA_ACQUISITION_REQUESTS_ONLY"),
        ("provider_requests_made_in_generation", False),
        ("live_provider_transport_enabled_in_generation", False),
        ("market_data_acquisition_performed_in_generation", False),
        ("raw_provider_payloads_committed", False),
        ("api_keys_stored_or_printed", False),
        ("predictive_usefulness", "not accepted"),
        ("profitability", "not accepted"),
        ("runtime_migration_approved", False),
        ("runtime_use", "NOT_AUTHORIZED"),
        ("strategy_use", "NOT_AUTHORIZED"),
        ("paper_trading", "NOT_AUTHORIZED"),
        ("broker_execution", "NOT_AUTHORIZED"),
    ],
)
def test_generated_artifact_contract(generated: tuple[dict, Path, Path], field: str, expected: object) -> None:
    artifact, _, _ = generated
    assert artifact[field] == expected


def test_meta_and_non_meta_counts_are_preserved(generated: tuple[dict, Path, Path]) -> None:
    artifact, _, _ = generated
    assert artifact["per_ticker_record_counts"]["META"] == 913
    assert all(
        count == 1003 for ticker, count in artifact["per_ticker_record_counts"].items() if ticker != "META"
    )


def test_output_digest_manifest_includes_all_outputs(generated: tuple[dict, Path, Path]) -> None:
    artifact, _, output = generated
    assert [row["filename"] for row in artifact["canonical_output_digest_manifest"]] == execution_service.OUTPUT_FILENAMES
    assert sorted(path.name for path in output.iterdir()) == sorted(execution_service.OUTPUT_FILENAMES)


def test_generated_json_outputs_are_research_only(generated: tuple[dict, Path, Path]) -> None:
    _, _, output = generated
    for path in output.glob("*.json"):
        payload = json.loads(path.read_text(encoding="utf-8"))
        assert payload["output_label"] == "RESEARCH_ONLY_NON_ACTIONABLE"
        assert payload["canonical_dataset_frozen"] is False
        assert payload["registry_approval_created"] is False


def test_records_are_ordered_and_digest_bound(generated: tuple[dict, Path, Path]) -> None:
    _, _, output = generated
    lines = (output / "canonical_dataset_records.jsonl").read_text(encoding="utf-8").splitlines()
    assert len(lines) == 11946
    records = [json.loads(line) for line in lines]
    first_indexes = [next(index for index, row in enumerate(records) if row["ticker"] == ticker) for ticker in execution_service.TARGET_UNIVERSE]
    assert first_indexes == sorted(first_indexes)
    assert all(len(row["source_record_digest"]) == 64 and len(row["canonical_record_digest"]) == 64 for row in records)


def test_validator_accepts_valid_generated_artifact(generated: tuple[dict, Path, Path]) -> None:
    artifact, _, _ = generated
    result = execution_service.validate_canonical_dataset_generated_v1(artifact)
    assert result["status"] == "CANONICAL_DATASET_GENERATED_RESEARCH_ONLY"


@pytest.mark.parametrize(
    ("field", "invalid"),
    [
        ("artifact_kind", "WRONG"),
        ("execution_status", "WRONG"),
        ("dataset_generation_authorized", False),
        ("canonical_dataset_authorized", False),
        ("canonical_dataset_generation_approved", False),
        ("canonical_dataset_candidate_created", False),
        ("canonical_dataset_generation_executed", False),
        ("canonical_dataset_generated", False),
        ("canonical_dataset_frozen", True),
        ("registry_approval_created", True),
        ("target_universe", list(reversed(execution_service.TARGET_UNIVERSE))),
        ("total_canonical_record_count", 11945),
        ("generated_output_count", 8),
        ("provider_requests_made_in_generation", True),
        ("live_provider_transport_enabled_in_generation", True),
        ("market_data_acquisition_performed_in_generation", True),
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
        ("canonical_dataset_generation_approval_digest", None),
        ("canonical_dataset_generation_digest", None),
    ],
)
def test_validator_rejects_invalid_contract_fields(
    generated: tuple[dict, Path, Path], field: str, invalid: object
) -> None:
    artifact, _, _ = generated
    changed = deepcopy(artifact)
    changed[field] = invalid
    with pytest.raises(execution_service.CanonicalDatasetGenerationExecutionError):
        execution_service.validate_canonical_dataset_generated_v1(changed)


@pytest.mark.parametrize(("ticker", "count"), [("META", 914), ("MSFT", 1002)])
def test_validator_rejects_wrong_per_ticker_count(
    generated: tuple[dict, Path, Path], ticker: str, count: int
) -> None:
    artifact, _, _ = generated
    changed = deepcopy(artifact)
    changed["per_ticker_record_counts"][ticker] = count
    with pytest.raises(execution_service.CanonicalDatasetGenerationExecutionError):
        execution_service.validate_canonical_dataset_generated_v1(changed)


def test_generation_digest_is_deterministic_for_fixed_source_and_timestamp(
    generated: tuple[dict, Path, Path], tmp_path: Path
) -> None:
    artifact, source, _ = generated
    repeated = execution_service.execute_canonical_dataset_generation_v1(
        source_root=source, output_root=tmp_path / "repeat", run_timestamp_utc="2026-08-14T16:00:00Z"
    )
    assert repeated["canonical_dataset_generation_digest"] == artifact["canonical_dataset_generation_digest"]


def test_status_markdown_includes_required_sections(generated: tuple[dict, Path, Path]) -> None:
    artifact, _, _ = generated
    markdown = execution_service.build_canonical_dataset_generation_status_markdown_v1(artifact)
    required = [
        "Canonical Dataset Generation Execution", "Source Canonical Dataset Generation Approval",
        "Source Acquisition Generation Freeze", "Target Universe", "Source Profile",
        "Canonical Dataset Schema", "Per-Ticker Canonical Record Summary",
        "META Reduced Bar Count Preservation", "Output Digest Manifest", "Data Quality Summary",
        "Dataset Generation Boundary", "Canonical Dataset Freeze Boundary", "Registry Boundary",
        "Predictive/Profitability Boundary", "Runtime Boundary", "Checklist Summary", "Guardrails",
    ]
    assert all(f"## {heading}" in markdown for heading in required)


def test_service_exports_are_available() -> None:
    assert services.execute_canonical_dataset_generation_v1 is execution_service.execute_canonical_dataset_generation_v1
    assert services.validate_canonical_dataset_generated_v1 is execution_service.validate_canonical_dataset_generated_v1
