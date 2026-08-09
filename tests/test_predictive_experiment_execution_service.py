from __future__ import annotations

import csv
import json
from copy import deepcopy
from pathlib import Path
from typing import Any

import pytest

from marketflow.services import predictive_experiment_execution_service as execution


FIXED_TIMESTAMP = "2026-08-09T00:00:00Z"


def _write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def _base_row(
    *,
    profile: str,
    bar_rule: str,
    date_text: str,
    open_value: str,
    high: str,
    low: str,
    close: str,
    volume: str,
    bar_number: str | None = None,
) -> dict[str, str]:
    row = {
        "ticker": "AAPL",
        "dataset_profile": profile,
        "dataset_bar_rule": bar_rule,
        "session_date": date_text,
        "session_type": "FULL_ORDINARY_SESSION",
        "bar_start_utc": f"{date_text}T14:30:00Z",
        "bar_end_utc": f"{date_text}T21:00:00Z",
        "bar_start_local": f"{date_text}T09:30:00-05:00",
        "bar_end_local": f"{date_text}T16:00:00-05:00",
        "open": open_value,
        "high": high,
        "low": low,
        "close": close,
        "volume": volume,
        "transactions": "1000",
        "vwap": close,
        "source_row_count": "26",
        "source_first_timestamp_utc": f"{date_text}T14:30:00Z",
        "source_last_timestamp_utc": f"{date_text}T20:45:00Z",
        "source_session_date": date_text,
        "source_timeframe": "15m",
    }
    if bar_number is not None:
        row["bar_number_in_session"] = bar_number
    return row


def _swing_rows() -> list[dict[str, str]]:
    rows = []
    closes = ["101", "102", "101", "103", "102", "104"]
    for index, close in enumerate(closes, start=1):
        rows.append(
            _base_row(
                profile="SWING",
                bar_rule="RTH_HALF_SESSION_195M",
                date_text=f"2022-01-0{index}",
                open_value=str(int(close) - 1),
                high=str(int(close) + 2),
                low=str(int(close) - 3),
                close=close,
                volume=str(1000000 + index * 1000),
                bar_number=str(index),
            )
        )
    return rows


def _position_rows() -> list[dict[str, str]]:
    rows = []
    closes = ["200", "199", "201", "202", "201", "203"]
    for index, close in enumerate(closes, start=1):
        rows.append(
            _base_row(
                profile="POSITION_SWING",
                bar_rule="RTH_FULL_SESSION_1D",
                date_text=f"2022-02-0{index}",
                open_value=str(int(close) - 1),
                high=str(int(close) + 2),
                low=str(int(close) - 3),
                close=close,
                volume=str(2000000 + index * 1000),
            )
        )
    return rows


def _definition(
    *,
    profile: str,
    bar_rule: str,
    dataset_path: str,
    manifest_path: str,
    rows_digest: str,
    manifest_digest: str,
) -> dict[str, Any]:
    return {
        "registry_key": f"AAPL:{profile}:{bar_rule}:2022-01-01:2025-12-31:v1",
        "dataset_profile": profile,
        "dataset_bar_rule": bar_rule,
        "ticker": "AAPL",
        "range_start": "2022-01-01",
        "range_end": "2025-12-31",
        "registry_scope": "RESEARCH_DATASET",
        "registry_approval_digest": (
            execution.EXPECTED_SOURCE_DIGESTS["swing_registry_approval_digest"]
            if profile == "SWING"
            else execution.EXPECTED_SOURCE_DIGESTS["position_swing_registry_approval_digest"]
        ),
        "dataset_rows_digest": rows_digest,
        "dataset_manifest_digest": manifest_digest,
        "expected_dataset_path": dataset_path,
        "expected_manifest_path": manifest_path,
        "runtime_use": execution.NOT_AUTHORIZED,
        "strategy_use": execution.NOT_AUTHORIZED,
    }


def _fixture_definitions(tmp_path: Path) -> tuple[list[dict[str, Any]], dict[str, dict[str, str]]]:
    swing_csv = Path("fixtures/SWING/AAPL_SWING.csv")
    swing_manifest = Path("fixtures/SWING/AAPL_SWING_manifest.json")
    position_csv = Path("fixtures/POSITION_SWING/AAPL_POSITION_SWING.csv")
    position_manifest = Path("fixtures/POSITION_SWING/AAPL_POSITION_SWING_manifest.json")
    _write_csv(tmp_path / swing_csv, _swing_rows())
    _write_csv(tmp_path / position_csv, _position_rows())
    partial_definitions = [
        {
            "dataset_profile": "SWING",
            "dataset_bar_rule": "RTH_HALF_SESSION_195M",
            "expected_dataset_path": swing_csv.as_posix(),
            "expected_manifest_path": swing_manifest.as_posix(),
        },
        {
            "dataset_profile": "POSITION_SWING",
            "dataset_bar_rule": "RTH_FULL_SESSION_1D",
            "expected_dataset_path": position_csv.as_posix(),
            "expected_manifest_path": position_manifest.as_posix(),
        },
    ]
    swing_rows = execution.discovery._read_csv_rows(tmp_path / swing_csv)
    position_rows = execution.discovery._read_csv_rows(tmp_path / position_csv)
    swing_rows_digest = execution.discovery._dataset_digest_for_entry(partial_definitions[0], swing_rows)
    position_rows_digest = execution.discovery._dataset_digest_for_entry(
        partial_definitions[1],
        position_rows,
    )
    manifests = {
        "SWING": {
            "artifact_kind": "SWING_CANONICAL_DATASET_MANIFEST",
            "schema_version": "swing_canonical_dataset_manifest_v1",
            "dataset_profile": "SWING",
            "dataset_bar_rule": "RTH_HALF_SESSION_195M",
            "row_count": len(swing_rows),
            "dataset_rows_digest": swing_rows_digest,
            "dataset_manifest_digest": None,
            "canonical_dataset_frozen": False,
        },
        "POSITION_SWING": {
            "artifact_kind": "POSITION_SWING_CANONICAL_DATASET_MANIFEST",
            "schema_version": "position_swing_canonical_dataset_manifest_v1",
            "dataset_profile": "POSITION_SWING",
            "dataset_bar_rule": "RTH_FULL_SESSION_1D",
            "row_count": len(position_rows),
            "dataset_rows_digest": position_rows_digest,
            "dataset_manifest_digest": None,
            "registry_eligibility": False,
        },
    }
    swing_manifest_digest = execution.discovery._manifest_digest_for_entry(
        partial_definitions[0],
        manifests["SWING"],
    )
    position_manifest_digest = execution.discovery._manifest_digest_for_entry(
        partial_definitions[1],
        manifests["POSITION_SWING"],
    )
    manifests["SWING"]["dataset_manifest_digest"] = swing_manifest_digest
    manifests["POSITION_SWING"]["dataset_manifest_digest"] = position_manifest_digest
    (tmp_path / swing_manifest).write_text(json.dumps(manifests["SWING"]), encoding="utf-8")
    (tmp_path / position_manifest).write_text(
        json.dumps(manifests["POSITION_SWING"]),
        encoding="utf-8",
    )
    expected_digests = {
        "SWING": {
            "dataset_rows_digest": swing_rows_digest,
            "dataset_manifest_digest": swing_manifest_digest,
        },
        "POSITION_SWING": {
            "dataset_rows_digest": position_rows_digest,
            "dataset_manifest_digest": position_manifest_digest,
        },
    }
    return (
        [
            _definition(
                profile="SWING",
                bar_rule="RTH_HALF_SESSION_195M",
                dataset_path=swing_csv.as_posix(),
                manifest_path=swing_manifest.as_posix(),
                rows_digest=swing_rows_digest,
                manifest_digest=swing_manifest_digest,
            ),
            _definition(
                profile="POSITION_SWING",
                bar_rule="RTH_FULL_SESSION_1D",
                dataset_path=position_csv.as_posix(),
                manifest_path=position_manifest.as_posix(),
                rows_digest=position_rows_digest,
                manifest_digest=position_manifest_digest,
            ),
        ],
        expected_digests,
    )


def _write_approval_status(tmp_path: Path) -> None:
    path = tmp_path / execution.APPROVAL_STATUS_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "\n".join(
            [
                "# Approval",
                "- Artifact kind: `PREDICTIVE_EXPERIMENT_EXECUTION_APPROVED`",
                "- Approval status: `PREDICTIVE_EXPERIMENT_EXECUTION_APPROVED`",
                f"- Approval digest: `{execution.EXPECTED_APPROVAL_DIGEST}`",
                "",
            ]
        ),
        encoding="utf-8",
    )


def _patch_fixture(
    monkeypatch: pytest.MonkeyPatch,
    definitions: list[dict[str, Any]],
    expected_digests: dict[str, dict[str, str]],
) -> None:
    monkeypatch.setattr(execution.discovery, "_registry_definitions", lambda: deepcopy(definitions))
    monkeypatch.setattr(execution, "EXPECTED_DATASET_DIGESTS", deepcopy(expected_digests))


def _artifact(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> dict[str, Any]:
    definitions, expected_digests = _fixture_definitions(tmp_path)
    _write_approval_status(tmp_path)
    _patch_fixture(monkeypatch, definitions, expected_digests)
    return execution.execute_predictive_experiment_v1(
        search_root=tmp_path,
        output_root=tmp_path / "outputs",
        run_timestamp_utc=FIXED_TIMESTAMP,
    )


def _read_output(tmp_path: Path, name: str) -> dict[str, Any]:
    return json.loads((tmp_path / "outputs" / f"{name}.json").read_text(encoding="utf-8"))


def _walk_values(value: Any):
    if isinstance(value, dict):
        for key, item in value.items():
            yield key
            yield from _walk_values(item)
    elif isinstance(value, list):
        for item in value:
            yield from _walk_values(item)
    else:
        yield value


def test_execution_blocks_when_approval_digest_status_document_is_missing(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    definitions, expected_digests = _fixture_definitions(tmp_path)
    _patch_fixture(monkeypatch, definitions, expected_digests)

    artifact = execution.execute_predictive_experiment_v1(
        search_root=tmp_path,
        output_root=tmp_path / "outputs",
        run_timestamp_utc=FIXED_TIMESTAMP,
    )

    assert artifact["execution_status"] == (
        execution.PREDICTIVE_EXPERIMENT_EXECUTION_BLOCKED_MISSING_APPROVAL_DIGEST
    )
    assert artifact["predictive_experiment_executed"] is False
    assert artifact["generated_output_count"] == 0


def test_execution_blocks_when_approval_digest_is_ambiguous(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    definitions, expected_digests = _fixture_definitions(tmp_path)
    _write_approval_status(tmp_path)
    path = tmp_path / execution.APPROVAL_STATUS_PATH
    path.write_text(
        path.read_text(encoding="utf-8")
        + f"- Approval digest: `{execution.EXPECTED_APPROVAL_DIGEST}`\n",
        encoding="utf-8",
    )
    _patch_fixture(monkeypatch, definitions, expected_digests)

    artifact = execution.execute_predictive_experiment_v1(
        search_root=tmp_path,
        output_root=tmp_path / "outputs",
        run_timestamp_utc=FIXED_TIMESTAMP,
    )

    assert artifact["execution_status"] == (
        execution.PREDICTIVE_EXPERIMENT_EXECUTION_BLOCKED_MISSING_APPROVAL_DIGEST
    )
    assert artifact["label_generation_performed"] is False


def test_execution_blocks_when_dataset_file_is_missing(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    definitions, expected_digests = _fixture_definitions(tmp_path)
    _write_approval_status(tmp_path)
    (tmp_path / definitions[0]["expected_dataset_path"]).unlink()
    _patch_fixture(monkeypatch, definitions, expected_digests)

    artifact = execution.execute_predictive_experiment_v1(
        search_root=tmp_path,
        output_root=tmp_path / "outputs",
        run_timestamp_utc=FIXED_TIMESTAMP,
    )

    assert artifact["execution_status"] == (
        execution.PREDICTIVE_EXPERIMENT_EXECUTION_BLOCKED_DATASET_VERIFICATION_FAILED
    )
    assert artifact["feature_matrix_generation_performed"] is False
    assert artifact["provider_requests_made"] is False


def test_execution_blocks_when_dataset_digest_mismatch_occurs(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    definitions, expected_digests = _fixture_definitions(tmp_path)
    _write_approval_status(tmp_path)
    expected_digests["SWING"]["dataset_rows_digest"] = "0" * 64
    _patch_fixture(monkeypatch, definitions, expected_digests)

    artifact = execution.execute_predictive_experiment_v1(
        search_root=tmp_path,
        output_root=tmp_path / "outputs",
        run_timestamp_utc=FIXED_TIMESTAMP,
    )

    assert artifact["execution_status"] == (
        execution.PREDICTIVE_EXPERIMENT_EXECUTION_BLOCKED_DATASET_VERIFICATION_FAILED
    )
    assert artifact["datasets_digest_verified_count"] == 1


def test_execution_builds_research_only_artifact(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    artifact = _artifact(tmp_path, monkeypatch)

    assert artifact["artifact_kind"] == execution.ARTIFACT_KIND_PREDICTIVE_EXPERIMENT_EXECUTED
    assert artifact["execution_status"] == execution.PREDICTIVE_EXPERIMENT_EXECUTED_RESEARCH_ONLY
    assert artifact["schema_version"] == execution.SCHEMA_VERSION_PREDICTIVE_EXPERIMENT_EXECUTED_V1


@pytest.mark.parametrize(
    "field",
    [
        "predictive_experiment_execution_authorized",
        "predictive_experiment_executed",
        "walk_forward_validation_performed",
        "out_of_sample_evaluation_performed",
        "label_generation_performed",
        "feature_matrix_generation_performed",
    ],
)
def test_approved_execution_flags_are_true(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    field: str,
):
    assert _artifact(tmp_path, monkeypatch)[field] is True


@pytest.mark.parametrize(
    "field",
    [
        "new_strategy_scoring_performed",
        "trade_recommendations_generated",
        "provider_requests_made",
        "predictive_usefulness_acceptance_ready",
        "profitability_acceptance_ready",
        "runtime_migration_recommended",
        "runtime_migration_approved",
        "runtime_migration_active",
        "strategy_runtime_migration",
        "automatic_stitching",
    ],
)
def test_guardrail_flags_remain_false(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    field: str,
):
    assert _artifact(tmp_path, monkeypatch)[field] is False


@pytest.mark.parametrize("field", ["runtime_use", "strategy_use", "paper_trading", "broker_execution"])
def test_runtime_strategy_paper_and_broker_remain_not_authorized(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    field: str,
):
    assert _artifact(tmp_path, monkeypatch)[field] == execution.NOT_AUTHORIZED


def test_predictive_usefulness_and_profitability_are_not_accepted(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    artifact = _artifact(tmp_path, monkeypatch)

    assert artifact["predictive_usefulness"] == "not accepted"
    assert artifact["profitability"] == "not accepted"


def test_source_digests_bind_approval_candidate_plan_and_registry_sources(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    artifact = _artifact(tmp_path, monkeypatch)

    assert artifact["source_digests"]["predictive_experiment_execution_approval_digest"] == (
        execution.EXPECTED_APPROVAL_DIGEST
    )
    for key, expected in execution.EXPECTED_SOURCE_DIGESTS.items():
        assert artifact["source_digests"][key] == expected


def test_dataset_digests_are_verified_before_execution(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    artifact = _artifact(tmp_path, monkeypatch)

    assert artifact["dataset_count"] == 2
    assert artifact["datasets_loaded_count"] == 2
    assert artifact["datasets_digest_verified_count"] == 2
    assert artifact["manifest_digest_verified_count"] == 2


def test_exact_thirteen_outputs_are_generated(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    artifact = _artifact(tmp_path, monkeypatch)

    assert artifact["planned_output_count"] == 13
    assert artifact["generated_output_count"] == 13
    assert sorted(artifact["output_digest_manifest"]) == sorted(execution.OUTPUT_NAMES)
    for name in execution.OUTPUT_NAMES:
        assert (tmp_path / "outputs" / f"{name}.json").exists()


@pytest.mark.parametrize("name", execution.OUTPUT_NAMES)
def test_every_output_has_research_only_boundaries(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    name: str,
):
    _artifact(tmp_path, monkeypatch)
    output = _read_output(tmp_path, name)

    assert output["output_label"] == execution.RESEARCH_ONLY_NON_ACTIONABLE
    assert output["runtime_use"] == execution.NOT_AUTHORIZED
    assert output["strategy_use"] == execution.NOT_AUTHORIZED
    assert output["paper_trading"] == execution.NOT_AUTHORIZED
    assert output["broker_execution"] == execution.NOT_AUTHORIZED
    assert output["predictive_usefulness"] == "not accepted"
    assert output["profitability"] == "not accepted"


def test_label_reports_include_forward_labels_and_exclude_final_rows(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    _artifact(tmp_path, monkeypatch)
    report = _read_output(tmp_path, "label_generation_report")

    assert report["labels_forward_looking_only"] is True
    assert report["final_row_unavailable_excluded"] is True
    assert {item["dataset_profile"]: item["unavailable_label_count"] for item in report["datasets"]} == {
        "POSITION_SWING": 1,
        "SWING": 1,
    }


def test_label_definition_report_contains_required_label_names(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    _artifact(tmp_path, monkeypatch)
    report = _read_output(tmp_path, "label_definition_report")
    labels = {
        item["direction_label"]
        for item in report["label_definitions"]
    } | {item["return_bucket_label"] for item in report["label_definitions"]}

    assert labels == set(execution.candidate.LABEL_DEFINITIONS)


def test_feature_manifest_contains_required_feature_examples(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    _artifact(tmp_path, monkeypatch)
    report = _read_output(tmp_path, "feature_matrix_manifest")

    assert report["feature_names"] == execution.FEATURE_NAMES
    assert {item["feature_count"] for item in report["datasets"]} == {len(execution.FEATURE_NAMES)}


def test_feature_family_report_does_not_create_strategy_scores(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    _artifact(tmp_path, monkeypatch)
    report = _read_output(tmp_path, "feature_family_report")

    assert report["strategy_scores_generated"] is False
    assert [item["feature_family"] for item in report["feature_families"]] == execution.FEATURE_FAMILIES


def test_walk_forward_and_oos_reports_use_chronological_split(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    _artifact(tmp_path, monkeypatch)
    walk_forward = _read_output(tmp_path, "walk_forward_configuration_report")
    oos = _read_output(tmp_path, "out_of_sample_split_report")

    assert walk_forward["walk_forward_type"] == execution.SIMPLIFIED_CHRONOLOGICAL_RESEARCH_SPLIT
    assert walk_forward["shuffle"] is False
    assert oos["chronological"] is True
    assert oos["shuffle"] is False


def test_baseline_report_contains_only_required_baselines(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    _artifact(tmp_path, monkeypatch)
    report = _read_output(tmp_path, "baseline_comparison_report")

    assert report["baselines"] == execution.BASELINES
    assert set(report["results"]["SWING"]) == set(execution.BASELINES)
    assert report["metrics_label"] == execution.RESEARCH_ONLY_NOT_PERFORMANCE_ACCEPTANCE


def test_signal_quality_metrics_are_not_performance_acceptance(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    _artifact(tmp_path, monkeypatch)
    report = _read_output(tmp_path, "signal_quality_metrics_report")

    assert report["metrics_label"] == execution.RESEARCH_ONLY_NOT_PERFORMANCE_ACCEPTANCE
    assert report["predictive_usefulness_acceptance_ready"] is False
    assert report["profitability_acceptance_ready"] is False


def test_leakage_controls_pass_without_future_features(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    _artifact(tmp_path, monkeypatch)
    report = _read_output(tmp_path, "leakage_control_report")

    assert report["leakage_control_status"] == "PASS"
    assert all(item["status"] == "PASS" for item in report["controls"])


def test_outputs_do_not_include_directional_action_words(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    _artifact(tmp_path, monkeypatch)

    forbidden = {"BUY", "SELL", "HOLD", "trade_recommendation", "trade_recommendations"}
    for name in execution.OUTPUT_NAMES:
        output = _read_output(tmp_path, name)
        values = {str(value) for value in _walk_values(output)}
        assert forbidden.isdisjoint(values)


def test_artifact_digest_is_deterministic_for_same_inputs(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    definitions, expected_digests = _fixture_definitions(tmp_path)
    _write_approval_status(tmp_path)
    _patch_fixture(monkeypatch, definitions, expected_digests)

    first = execution.execute_predictive_experiment_v1(
        search_root=tmp_path,
        output_root=tmp_path / "outputs",
        run_timestamp_utc=FIXED_TIMESTAMP,
    )
    second = execution.execute_predictive_experiment_v1(
        search_root=tmp_path,
        output_root=tmp_path / "outputs",
        run_timestamp_utc=FIXED_TIMESTAMP,
    )

    assert first["predictive_experiment_execution_digest"] == (
        second["predictive_experiment_execution_digest"]
    )


def test_validate_rejects_runtime_activation(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    artifact = _artifact(tmp_path, monkeypatch)
    artifact["runtime_migration_active"] = True
    artifact["predictive_experiment_execution_digest"] = (
        execution.predictive_experiment_execution_digest_v1(artifact)
    )

    with pytest.raises(execution.PredictiveExperimentExecutionError):
        execution.validate_predictive_experiment_executed_v1(artifact)


def test_status_markdown_preserves_research_boundaries(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    artifact = _artifact(tmp_path, monkeypatch)

    markdown = execution.build_predictive_experiment_execution_status_markdown_v1(artifact)

    assert "PREDICTIVE_EXPERIMENT_EXECUTED_RESEARCH_ONLY" in markdown
    assert "predictive_usefulness: `not accepted`" in markdown
    assert "runtime_use: `NOT_AUTHORIZED`" in markdown
