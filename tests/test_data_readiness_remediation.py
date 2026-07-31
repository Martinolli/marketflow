from __future__ import annotations

import ast
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from marketflow.research import data_readiness_remediation as remediation
from marketflow.research import applicability_readiness


def _write_csv(
    path: Path,
    rows: list[dict[str, object]],
    *,
    extra_columns: list[str] | None = None,
) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    columns = ["timestamp", "open", "high", "low", "close", "volume", *(extra_columns or [])]
    lines = [",".join(columns)]
    for row in rows:
        lines.append(",".join(str(row.get(column, "")) for column in columns))
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def _rows(
    count: int,
    *,
    start: int = 0,
    timestamp_offset: int = 0,
    annotation: str = "ACCUMULATION",
) -> list[dict[str, object]]:
    base = datetime(2026, 1, 1, tzinfo=timezone.utc)
    return [
        {
            "timestamp": (base + timedelta(hours=index + timestamp_offset)).isoformat().replace("+00:00", "Z"),
            "open": 10 + start + index,
            "high": 11 + start + index,
            "low": 9 + start + index,
            "close": 10 + start + index,
            "volume": 1000 + index,
            "wyckoff_phase": annotation,
            "tr_low": 9 + start + index,
            "tr_high": 11 + start + index,
        }
        for index in range(count)
    ]


def test_inventory_identity_safe_paths_deterministic_counts(tmp_path: Path) -> None:
    _write_csv(tmp_path / ".marketflow" / "reports" / "run2" / "AAA" / "AAA_4h_wyckoff_annotated.csv", _rows(2), extra_columns=["wyckoff_phase", "tr_low", "tr_high"])
    _write_csv(tmp_path / ".marketflow" / "reports" / "run1" / "AAA" / "AAA_4h_wyckoff_annotated.csv", _rows(2), extra_columns=["wyckoff_phase", "tr_low", "tr_high"])
    _write_csv(tmp_path / ".marketflow" / "reports" / "run1" / "AAA" / "AAA_1d_wyckoff_annotated.csv", _rows(2), extra_columns=["wyckoff_phase", "tr_low", "tr_high"])

    inventory = remediation.build_inventory(tmp_path)

    assert [item.safe_relative_reference for item in inventory] == sorted(item.safe_relative_reference for item in inventory)
    assert all(not Path(item.safe_relative_reference).is_absolute() for item in inventory)
    assert remediation.duplicate_count_summary(inventory) == {
        "total_dataset_file_count": 3,
        "unique_ticker_timeframe_identity_count": 2,
        "duplicate_identity_count": 1,
        "total_files_inside_duplicate_groups": 2,
        "excess_duplicate_file_count": 1,
    }


def test_scan_scope_matches_applicability_canonical_dataset_scope(tmp_path: Path) -> None:
    canonical = _write_csv(
        tmp_path / ".marketflow" / "reports" / "run" / "AAA" / "AAA_4h_wyckoff_annotated.csv",
        _rows(2),
    )
    _write_csv(tmp_path / ".marketflow" / "reports" / "run" / "AAA" / "AAA_4h.csv", _rows(2))
    _write_csv(tmp_path / ".marketflow" / "reports" / "run" / "AAA" / "AAA_4h_pv_eigen.csv", _rows(2))
    _write_csv(tmp_path / ".marketflow" / "reports" / "run" / "AAA" / "AAA_5m_wyckoff_annotated.csv", _rows(2))

    old_refs = {
        applicability_readiness.safe_relative_path(path, tmp_path)
        for path in applicability_readiness.discover_canonical_datasets(tmp_path)
    }
    new_refs = {remediation.safe_relative_reference(path, tmp_path) for path in remediation.discover_canonical_sources(tmp_path)}

    assert old_refs == new_refs == {remediation.safe_relative_reference(canonical, tmp_path)}


def test_root_escape_rejected(tmp_path: Path) -> None:
    outside = tmp_path.parent / f"{tmp_path.name}_outside"
    outside.mkdir(exist_ok=True)
    try:
        with pytest.raises(ValueError, match="dataset roots must stay inside repository root"):
            remediation.build_inventory(tmp_path, [outside])
    finally:
        outside.rmdir()


def test_exact_byte_duplicate_and_same_size_different_bytes(tmp_path: Path) -> None:
    rows = _rows(2)
    first = _write_csv(tmp_path / "a" / "AAA_4h_wyckoff_annotated.csv", rows, extra_columns=["wyckoff_phase", "tr_low", "tr_high"])
    second = tmp_path / "b" / "AAA_4h_wyckoff_annotated.csv"
    second.parent.mkdir()
    second.write_bytes(first.read_bytes())
    sources = remediation.build_inventory(tmp_path, [tmp_path])

    exact = remediation.classify_duplicate_group(sources)
    assert exact["classification"] == remediation.EXACT_BYTE_DUPLICATES

    second.write_text(first.read_text(encoding="utf-8").replace("1000", "1001", 1), encoding="utf-8")
    changed = remediation.build_inventory(tmp_path, [tmp_path])
    pair = remediation.compare_source_pair(changed[0], changed[1])

    assert changed[0].byte_size == changed[1].byte_size
    assert pair["exact_byte_duplicate"] is False
    assert remediation.classify_duplicate_group(changed)["classification"] == remediation.OVERLAPPING_CONFLICTING


def test_semantically_identical_with_different_csv_formatting(tmp_path: Path) -> None:
    _write_csv(tmp_path / "a" / "AAA_4h_wyckoff_annotated.csv", _rows(2))
    formatted = [
        {"timestamp": "2026-01-01T00:00:00Z", "open": "10.0", "high": "11.00", "low": "9.000", "close": "10.0", "volume": "1000.0", "wyckoff_phase": "ACCUMULATION", "tr_low": "9.0", "tr_high": "11.0"},
        {"timestamp": "2026-01-01T01:00:00Z", "open": "11.0", "high": "12.00", "low": "10.000", "close": "11.0", "volume": "1001.0", "wyckoff_phase": "ACCUMULATION", "tr_low": "10.0", "tr_high": "12.0"},
    ]
    _write_csv(tmp_path / "b" / "AAA_4h_wyckoff_annotated.csv", formatted)

    sources = remediation.build_inventory(tmp_path, [tmp_path])

    assert remediation.classify_duplicate_group(sources)["classification"] == remediation.SEMANTICALLY_IDENTICAL


def test_same_ohlcv_different_annotations(tmp_path: Path) -> None:
    _write_csv(tmp_path / "a" / "AAA_4h_wyckoff_annotated.csv", _rows(2, annotation="ACCUMULATION"), extra_columns=["wyckoff_phase", "tr_low", "tr_high"])
    _write_csv(tmp_path / "b" / "AAA_4h_wyckoff_annotated.csv", _rows(2, annotation="DISTRIBUTION"), extra_columns=["wyckoff_phase", "tr_low", "tr_high"])

    sources = remediation.build_inventory(tmp_path, [tmp_path])

    assert remediation.classify_duplicate_group(sources)["classification"] == remediation.SAME_OHLCV_DIFFERENT_ANNOTATIONS


def test_subset_superset_compatible_overlap_conflict_and_disjoint(tmp_path: Path) -> None:
    _write_csv(tmp_path / "subset_a" / "AAA_4h_wyckoff_annotated.csv", _rows(2), extra_columns=["wyckoff_phase", "tr_low", "tr_high"])
    _write_csv(tmp_path / "subset_b" / "AAA_4h_wyckoff_annotated.csv", _rows(3), extra_columns=["wyckoff_phase", "tr_low", "tr_high"])
    subset = remediation.build_inventory(tmp_path, [tmp_path / "subset_a", tmp_path / "subset_b"])
    assert remediation.classify_duplicate_group(subset)["classification"] == remediation.STRICT_SUBSET_COMPATIBLE

    superset_root = tmp_path / "superset"
    _write_csv(superset_root / "a_super" / "EEE_4h_wyckoff_annotated.csv", _rows(3), extra_columns=["wyckoff_phase", "tr_low", "tr_high"])
    _write_csv(superset_root / "b_subset" / "EEE_4h_wyckoff_annotated.csv", _rows(2), extra_columns=["wyckoff_phase", "tr_low", "tr_high"])
    superset = remediation.build_inventory(tmp_path, [superset_root])
    assert remediation.classify_duplicate_group(superset)["classification"] == remediation.STRICT_SUPERSET_COMPATIBLE

    overlap_root = tmp_path / "overlap"
    _write_csv(overlap_root / "a" / "BBB_4h_wyckoff_annotated.csv", _rows(3), extra_columns=["wyckoff_phase", "tr_low", "tr_high"])
    _write_csv(overlap_root / "b" / "BBB_4h_wyckoff_annotated.csv", _rows(3)[1:] + _rows(1, start=10, timestamp_offset=10), extra_columns=["wyckoff_phase", "tr_low", "tr_high"])
    compatible = remediation.build_inventory(tmp_path, [overlap_root])
    assert remediation.classify_duplicate_group(compatible)["classification"] == remediation.OVERLAPPING_COMPATIBLE

    conflict_root = tmp_path / "conflict"
    conflict_rows = _rows(2)
    changed = [dict(conflict_rows[0], high=1000, close=999), conflict_rows[1]]
    _write_csv(conflict_root / "a" / "CCC_4h_wyckoff_annotated.csv", conflict_rows, extra_columns=["wyckoff_phase", "tr_low", "tr_high"])
    _write_csv(conflict_root / "b" / "CCC_4h_wyckoff_annotated.csv", changed, extra_columns=["wyckoff_phase", "tr_low", "tr_high"])
    conflicting = remediation.build_inventory(tmp_path, [conflict_root])
    assert remediation.classify_duplicate_group(conflicting)["classification"] == remediation.OVERLAPPING_CONFLICTING

    disjoint_root = tmp_path / "disjoint"
    _write_csv(disjoint_root / "a" / "DDD_4h_wyckoff_annotated.csv", _rows(2), extra_columns=["wyckoff_phase", "tr_low", "tr_high"])
    _write_csv(disjoint_root / "b" / "DDD_4h_wyckoff_annotated.csv", _rows(2, start=100, timestamp_offset=100), extra_columns=["wyckoff_phase", "tr_low", "tr_high"])
    disjoint = remediation.build_inventory(tmp_path, [disjoint_root])
    assert remediation.classify_duplicate_group(disjoint)["classification"] == remediation.DISJOINT_HISTORY_SAME_IDENTITY


def test_schema_timezone_and_provenance_conflicts(tmp_path: Path) -> None:
    schema_root = tmp_path / "schema"
    _write_csv(schema_root / "a" / "AAA_4h_wyckoff_annotated.csv", _rows(1), extra_columns=["wyckoff_phase"])
    (schema_root / "b").mkdir()
    (schema_root / "b" / "AAA_4h_wyckoff_annotated.csv").write_text("timestamp,open,high,low,close\n2026-01-01,1,2,1,1\n", encoding="utf-8")
    assert remediation.classify_duplicate_group(remediation.build_inventory(tmp_path, [schema_root]))["classification"] == remediation.SCHEMA_DIVERGENT

    timezone_root = tmp_path / "timezone"
    _write_csv(timezone_root / "a" / "BBB_4h_wyckoff_annotated.csv", _rows(1), extra_columns=["wyckoff_phase"])
    _write_csv(timezone_root / "b" / "BBB_4h_wyckoff_annotated.csv", [dict(_rows(1)[0], timestamp="2026-01-01T00:00:00")], extra_columns=["wyckoff_phase"])
    assert remediation.classify_duplicate_group(remediation.build_inventory(tmp_path, [timezone_root]))["classification"] == remediation.TIMESTAMP_NORMALIZATION_CONFLICT

    provenance_root = tmp_path / "provenance"
    _write_csv(provenance_root / "a" / "CCC_4h_wyckoff_annotated.csv", [dict(_rows(1)[0], provider="OTHER_VENDOR")], extra_columns=["provider"])
    _write_csv(provenance_root / "b" / "CCC_4h_wyckoff_annotated.csv", [dict(_rows(1)[0], provider="FICTIONAL_VENDOR")], extra_columns=["provider"])
    assert remediation.classify_duplicate_group(remediation.build_inventory(tmp_path, [provenance_root]))["classification"] == remediation.PROVENANCE_CONFLICT


def test_validation_counts_missing_duplicate_nonmonotonic_nan_geometry_volume(tmp_path: Path) -> None:
    rows = _rows(6)
    rows[1]["timestamp"] = rows[0]["timestamp"]
    rows[2]["timestamp"] = "2025-01-01T00:00:00Z"
    rows[3]["close"] = "NaN"
    rows[4]["high"] = 1
    rows[4]["low"] = 5
    rows[5]["volume"] = -1
    source = _write_csv(tmp_path / "AAA_4h_wyckoff_annotated.csv", rows, extra_columns=["wyckoff_phase", "tr_low", "tr_high"])

    inspected = remediation.inspect_source(source, tmp_path)

    assert inspected.duplicate_timestamp_count == 1
    assert inspected.non_monotonic_timestamp_count >= 1
    assert inspected.non_finite_ohlcv_count == 1
    assert inspected.invalid_high_low_geometry_count == 1
    assert inspected.invalid_volume_count == 1


def test_invalid_chronology_blocks_compatible_classification_and_safe_history(tmp_path: Path) -> None:
    bad_rows = _rows(3)
    bad_rows[2]["timestamp"] = bad_rows[1]["timestamp"]
    _write_csv(tmp_path / "a" / "AAA_4h_wyckoff_annotated.csv", bad_rows, extra_columns=["wyckoff_phase"])
    _write_csv(tmp_path / "b" / "AAA_4h_wyckoff_annotated.csv", bad_rows, extra_columns=["wyckoff_phase"])

    sources = remediation.build_inventory(tmp_path, [tmp_path])
    history = remediation.analyze_history_depth(sources)

    assert remediation.classify_duplicate_group(sources)["classification"] == remediation.TIMESTAMP_NORMALIZATION_CONFLICT
    assert history[0]["best_valid_single_source_rows"] == 0
    assert history[0]["approved_canonical_safe_rows"] == remediation.NOT_ESTABLISHED
    assert history[0]["estimated_shortfall_from_best_single_source"] == 390
    assert history[0]["data_readiness_status"] == "DATASET_INVALID"


def test_direct_inspect_source_does_not_read_unsafe_path(tmp_path: Path) -> None:
    outside = tmp_path.parent / f"{tmp_path.name}_outside.csv"
    outside.write_text("timestamp,open,high,low,close,volume\n2026-01-01,1,2,1,1,1\n", encoding="utf-8")
    try:
        inspected = remediation.inspect_source(outside, tmp_path)
    finally:
        outside.unlink()

    assert inspected.errors == ("SOURCE_PATH_UNSAFE",)
    assert inspected.byte_size == 0
    assert inspected.row_count == 0


def test_row_depth_best_single_source_and_potential_union_shortfalls(tmp_path: Path) -> None:
    _write_csv(tmp_path / "a" / "AAA_4h_wyckoff_annotated.csv", _rows(389), extra_columns=["wyckoff_phase", "tr_low", "tr_high"])
    _write_csv(tmp_path / "b" / "AAA_4h_wyckoff_annotated.csv", _rows(390), extra_columns=["wyckoff_phase", "tr_low", "tr_high"])
    _write_csv(tmp_path / "daily_a" / "BBB_1d_wyckoff_annotated.csv", _rows(559), extra_columns=["wyckoff_phase", "tr_low", "tr_high"])
    _write_csv(tmp_path / "daily_b" / "CCC_1d_wyckoff_annotated.csv", _rows(560), extra_columns=["wyckoff_phase", "tr_low", "tr_high"])

    history = remediation.analyze_history_depth(remediation.build_inventory(tmp_path, [tmp_path]))
    by_identity = {(row["ticker"], row["profile"]): row for row in history}

    assert by_identity[("AAA", "SWING")]["estimated_shortfall_from_best_single_source"] == 0
    assert by_identity[("AAA", "SWING")]["approved_canonical_safe_rows"] == remediation.NOT_ESTABLISHED
    assert by_identity[("AAA", "SWING")]["data_readiness_status"] == "DUPLICATE_REVIEW_REQUIRED"
    assert by_identity[("BBB", "POSITION_SWING")]["estimated_shortfall_from_best_single_source"] == 1
    assert by_identity[("CCC", "POSITION_SWING")]["estimated_shortfall_from_best_single_source"] == 0
    assert by_identity[("AAA", "SWING")]["potential_compatible_union_rows"] == 390


def test_registry_validation_rejects_duplicate_approval_digest_missing_unknown_and_unsafe_refs(tmp_path: Path) -> None:
    source = _write_csv(tmp_path / "data" / "AAA_4h_wyckoff_annotated.csv", _rows(1), extra_columns=["wyckoff_phase"])
    digest = remediation.sha256_bytes(source.read_bytes())
    semantic_digest = remediation.source_semantic_ohlcv_digest(remediation.inspect_source(source, tmp_path))

    def record(**overrides: object) -> dict[str, object]:
        base = {
            "registry_schema_version": remediation.REGISTRY_SCHEMA_VERSION,
            "canonical_ticker": "AAA",
            "canonical_timeframe": "4h",
            "status": "APPROVED",
            "approved_safe_relative_source_reference": "data/AAA_4h_wyckoff_annotated.csv",
            "approved_file_sha256": digest,
            "approved_semantic_ohlcv_digest": semantic_digest,
            "provenance_status": "EXPLICIT_PROVENANCE_CONFIRMED",
            "adjustment_status": "EXPLICIT_ADJUSTMENT_CONFIRMED",
            "approval_evidence_category": "MANUAL_DATA_GOVERNANCE_REVIEW",
            "decision_id": "DECISION-001",
            "decision_timestamp": "2026-07-31T00:00:00Z",
            "superseded_source_references": [],
            "notes_category": "NONE",
        }
        base.update(overrides)
        return base

    valid = {"schema_version": remediation.REGISTRY_SCHEMA_VERSION, "records": [record()]}
    assert remediation.validate_registry(valid, tmp_path)["success"] is True

    duplicate = {"schema_version": remediation.REGISTRY_SCHEMA_VERSION, "records": [record(), record(decision_id="DECISION-002")]}
    assert "REGISTRY_DUPLICATE_APPROVED_IDENTITY:AAA:4h" in remediation.validate_registry(duplicate, tmp_path)["errors"]

    mismatch = {"schema_version": remediation.REGISTRY_SCHEMA_VERSION, "records": [record(approved_file_sha256="bad")]}
    assert "REGISTRY_APPROVED_SOURCE_DIGEST_INVALID:0" in remediation.validate_registry(mismatch, tmp_path)["errors"]

    semantic_mismatch = {"schema_version": remediation.REGISTRY_SCHEMA_VERSION, "records": [record(approved_semantic_ohlcv_digest="0" * 64)]}
    assert "REGISTRY_APPROVED_SEMANTIC_DIGEST_MISMATCH:0" in remediation.validate_registry(semantic_mismatch, tmp_path)["errors"]

    missing = {"schema_version": remediation.REGISTRY_SCHEMA_VERSION, "records": [record(approved_safe_relative_source_reference="data/missing.csv")]}
    assert "REGISTRY_APPROVED_SOURCE_MISSING:0" in remediation.validate_registry(missing, tmp_path)["errors"]

    unknown = {"schema_version": remediation.REGISTRY_SCHEMA_VERSION, "records": [dict(record(), extra="nope")]}
    assert "REGISTRY_RECORD_FIELD_SET_INVALID:0" in remediation.validate_registry(unknown, tmp_path)["errors"]

    unsafe = {"schema_version": remediation.REGISTRY_SCHEMA_VERSION, "records": [record(approved_safe_relative_source_reference="../outside.csv")]}
    assert "REGISTRY_SOURCE_REF_UNSAFE:0" in remediation.validate_registry(unsafe, tmp_path)["errors"]

    device = {"schema_version": remediation.REGISTRY_SCHEMA_VERSION, "records": [record(status="UNRESOLVED", approved_safe_relative_source_reference="NUL/file.csv", approved_file_sha256="", approved_semantic_ohlcv_digest="")]}
    assert "REGISTRY_SOURCE_REF_UNSAFE:0" in remediation.validate_registry(device, tmp_path)["errors"]

    unresolved_unsafe = {"schema_version": remediation.REGISTRY_SCHEMA_VERSION, "records": [record(status="UNRESOLVED", approved_safe_relative_source_reference="../outside.csv", approved_file_sha256="", approved_semantic_ohlcv_digest="")]}
    assert "REGISTRY_SOURCE_REF_UNSAFE:0" in remediation.validate_registry(unresolved_unsafe, tmp_path)["errors"]

    superseded_unsafe = {"schema_version": remediation.REGISTRY_SCHEMA_VERSION, "records": [record(status="UNRESOLVED", approved_safe_relative_source_reference="", approved_file_sha256="", approved_semantic_ohlcv_digest="", superseded_source_references=["../outside.csv"])]}
    assert "REGISTRY_SUPERSEDED_SOURCE_REF_UNSAFE:0:0" in remediation.validate_registry(superseded_unsafe, tmp_path)["errors"]

    unresolved_approval = {
        "schema_version": remediation.REGISTRY_SCHEMA_VERSION,
        "records": [
            record(
                provenance_status="PENDING_REVIEW",
                adjustment_status=remediation.CORPORATE_ACTION_ADJUSTMENT_STATUS_UNKNOWN,
                approval_evidence_category=remediation.HUMAN_APPROVAL_REQUIRED,
                decision_timestamp=remediation.HUMAN_APPROVAL_REQUIRED,
            )
        ],
    }
    unresolved_errors = remediation.validate_registry(unresolved_approval, tmp_path)["errors"]
    assert "REGISTRY_APPROVED_PROVENANCE_INCOMPLETE:0" in unresolved_errors
    assert "REGISTRY_APPROVED_ADJUSTMENT_INCOMPLETE:0" in unresolved_errors
    assert "REGISTRY_APPROVED_EVIDENCE_CATEGORY_INCOMPLETE:0" in unresolved_errors
    assert "REGISTRY_APPROVED_DECISION_TIMESTAMP_INVALID:0" in unresolved_errors


def test_decision_register_append_only_and_no_performance_rationale() -> None:
    first = {
        "decision_id": "DECISION-001",
        "identity": {"ticker": "AAA", "timeframe": "4h"},
        "examined_source_digests": ["a" * 64],
        "duplicate_classification": remediation.EXACT_BYTE_DUPLICATES,
        "decision_status": "PENDING",
        "selected_canonical_source": None,
        "rationale_category": "DATA_REDUNDANCY",
        "operator_approval_status": "PENDING",
        "evidence_timestamp": "2026-07-31T00:00:00Z",
        "code_commit": "b" * 40,
        "remediation_action_status": "NONE",
    }
    existing = {"schema_version": remediation.DECISION_REGISTER_SCHEMA_VERSION, "decisions": [first]}
    proposed = {
        "schema_version": remediation.DECISION_REGISTER_SCHEMA_VERSION,
        "decisions": [
            first,
            dict(
                first,
                decision_id="DECISION-002",
                decision_status="APPROVED",
                selected_canonical_source="data/AAA_4h_wyckoff_annotated.csv",
                operator_approval_status="APPROVED",
            ),
        ],
    }

    assert remediation.validate_decision_register_append_only(existing, proposed)["success"] is True

    edited = {"schema_version": remediation.DECISION_REGISTER_SCHEMA_VERSION, "decisions": [dict(first, decision_status="APPROVED")]}
    assert "DECISION_REGISTER_RETROACTIVE_EDIT_NOT_ALLOWED" in remediation.validate_decision_register_append_only(existing, edited)["errors"]

    deleted = {"schema_version": remediation.DECISION_REGISTER_SCHEMA_VERSION, "decisions": []}
    assert "DECISION_REGISTER_DELETION_NOT_ALLOWED" in remediation.validate_decision_register_append_only(existing, deleted)["errors"]

    performance = {"schema_version": remediation.DECISION_REGISTER_SCHEMA_VERSION, "decisions": [dict(first, rationale_category="PERFORMANCE")]}
    assert "DECISION_PERFORMANCE_RATIONALE_FORBIDDEN:0" in remediation.validate_decision_register_append_only({}, performance)["errors"]

    profitability = {"schema_version": remediation.DECISION_REGISTER_SCHEMA_VERSION, "decisions": [dict(first, rationale_category="PROFITABILITY_REVIEW")]}
    assert "DECISION_PERFORMANCE_RATIONALE_FORBIDDEN:0" in remediation.validate_decision_register_append_only({}, profitability)["errors"]

    candidate_score = {"schema_version": remediation.DECISION_REGISTER_SCHEMA_VERSION, "decisions": [dict(first, rationale_category="CANDIDATE_SCORE_REVIEW")]}
    assert "DECISION_PERFORMANCE_RATIONALE_FORBIDDEN:0" in remediation.validate_decision_register_append_only({}, candidate_score)["errors"]

    approved_without_source = {"schema_version": remediation.DECISION_REGISTER_SCHEMA_VERSION, "decisions": [dict(first, decision_status="APPROVED")]}
    approved_errors = remediation.validate_decision_register_append_only({}, approved_without_source)["errors"]
    assert "DECISION_APPROVED_SOURCE_REQUIRED:0" in approved_errors
    assert "DECISION_OPERATOR_APPROVAL_REQUIRED:0" in approved_errors

    incomplete_evidence = {
        "schema_version": remediation.DECISION_REGISTER_SCHEMA_VERSION,
        "decisions": [
            dict(
                first,
                decision_status="APPROVED",
                selected_canonical_source="CON/source.csv",
                operator_approval_status="APPROVED",
                identity={"ticker": "aaa", "timeframe": "4h"},
                examined_source_digests=["abc"],
                evidence_timestamp="not-a-date",
                code_commit="abc123",
            )
        ],
    }
    evidence_errors = remediation.validate_decision_register_append_only({}, incomplete_evidence)["errors"]
    assert "DECISION_SELECTED_SOURCE_REF_UNSAFE:0" in evidence_errors
    assert "DECISION_APPROVED_IDENTITY_INVALID:0" in evidence_errors
    assert "DECISION_APPROVED_SOURCE_DIGESTS_INVALID:0" in evidence_errors
    assert "DECISION_APPROVED_EVIDENCE_TIMESTAMP_INVALID:0" in evidence_errors
    assert "DECISION_APPROVED_CODE_COMMIT_INVALID:0" in evidence_errors


def test_report_digest_excludes_timestamp_and_report_has_no_ohlcv_values_or_absolute_paths(tmp_path: Path) -> None:
    _write_csv(tmp_path / ".marketflow" / "reports" / "AAA" / "AAA_4h_wyckoff_annotated.csv", _rows(2), extra_columns=["wyckoff_phase", "tr_low", "tr_high"])

    first = remediation.build_remediation_report(tmp_path, generated_at="2026-01-01T00:00:00Z", code_commit="abc")
    second = remediation.build_remediation_report(tmp_path, generated_at="2026-02-01T00:00:00Z", code_commit="abc")
    output = remediation.write_report(first, ".marketflow/data_readiness/report.json", tmp_path)
    public_text = output.read_text(encoding="utf-8")

    assert first["report_semantic_sha256"] == second["report_semantic_sha256"]
    assert str(tmp_path) not in public_text
    assert '"_ohlcv_by_timestamp"' not in public_text
    assert '"10"' not in public_text
    assert first["no_performance_inspected"] is True


def test_cli_writes_ignored_report_and_rejects_external_report_output(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    _write_csv(tmp_path / ".marketflow" / "reports" / "AAA" / "AAA_4h_wyckoff_annotated.csv", _rows(1), extra_columns=["wyckoff_phase"])

    assert remediation.main(["--repo-root", str(tmp_path)]) == 0
    captured = json.loads(capsys.readouterr().out)
    assert captured["report_ref"] == ".marketflow/data_readiness/data_readiness_remediation_report.json"
    assert (tmp_path / captured["report_ref"]).exists()

    with pytest.raises(ValueError, match="data readiness report output must stay under"):
        remediation.write_report(remediation.build_remediation_report(tmp_path), "docs/report.json", tmp_path)


def test_source_assurance_no_forbidden_imports_or_calls_and_no_normal_integration() -> None:
    module_path = Path(remediation.__file__)
    source = module_path.read_text(encoding="utf-8")
    tree = ast.parse(source)
    imported = {
        alias.name
        for node in ast.walk(tree)
        if isinstance(node, ast.Import)
        for alias in node.names
    } | {
        node.module or ""
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom)
    }
    forbidden_import_fragments = (
        "marketflow.marketflow_strategy",
        "marketflow_monte_carlo",
        "marketflow.marketflow_data_provider",
        "streamlit",
        "openai",
        "polygon",
        "outcome",
    )
    assert not any(fragment in module for module in imported for fragment in forbidden_import_fragments)

    called_names = {
        node.func.attr if isinstance(node.func, ast.Attribute) else node.func.id
        for node in ast.walk(tree)
        if isinstance(node, ast.Call) and isinstance(node.func, (ast.Attribute, ast.Name))
    }
    forbidden_calls = {
        "unlink",
        "rename",
        "rmdir",
        "remove",
        "rank_long_candidates",
        "build_candidate_from_prefix",
        "run_monte_carlo",
        "evaluate_outcomes",
    }
    assert called_names.isdisjoint(forbidden_calls)

    assert "APPROVED_CANONICAL_SOURCE" not in source
    schema_fields = remediation.REGISTRY_REQUIRED_FIELDS | remediation.DECISION_REQUIRED_FIELDS
    assert "win_rate" not in schema_fields
    assert "expectancy" not in schema_fields
    assert "sharpe" not in {field.lower() for field in schema_fields}
    assert "sortino" not in {field.lower() for field in schema_fields}
    assert "drawdown" not in {field.lower() for field in schema_fields}

    orchestrator_source = Path("marketflow/fixed_profile_orchestrator.py").read_text(encoding="utf-8")
    assert "data_readiness_remediation" not in orchestrator_source


def test_source_controlled_examples_are_fictional_and_parseable() -> None:
    registry = remediation.load_registry("config/canonical_dataset_registry.example.toml")
    assert registry["schema_version"] == remediation.REGISTRY_SCHEMA_VERSION
    assert {record["canonical_ticker"] for record in registry["records"]} == {"FICT", "MOCK"}
    assert all(not record["approved_safe_relative_source_reference"] for record in registry["records"])

    decision_register = json.loads(Path("config/dataset_decision_register.example.json").read_text(encoding="utf-8"))
    result = remediation.validate_decision_register_append_only({}, decision_register)

    assert result["success"] is True
    assert decision_register["decisions"][0]["identity"]["ticker"] == "FICT"
