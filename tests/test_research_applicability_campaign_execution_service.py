from __future__ import annotations

import csv
import json
from copy import deepcopy
from pathlib import Path
from typing import Any

import pytest

from marketflow.services import research_applicability_campaign_execution_service as execution


FIXED_TIMESTAMP = "2026-08-09T00:00:00Z"


def _write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def _swing_rows() -> list[dict[str, str]]:
    return [
        {
            "ticker": "AAPL",
            "dataset_profile": "SWING",
            "dataset_bar_rule": "RTH_HALF_SESSION_195M",
            "session_date": "2022-01-03",
            "session_type": "FULL_ORDINARY_SESSION",
            "bar_number_in_session": "1",
            "bar_start_utc": "2022-01-03T14:30:00Z",
            "bar_end_utc": "2022-01-03T17:45:00Z",
            "bar_start_local": "2022-01-03T09:30:00-05:00",
            "bar_end_local": "2022-01-03T12:45:00-05:00",
            "open": "177.83",
            "high": "182.1675",
            "low": "177.71",
            "close": "182.02",
            "volume": "47224260",
            "transactions": "444886",
            "vwap": "180.766",
            "source_row_count": "13",
            "source_first_timestamp_utc": "2022-01-03T14:30:00Z",
            "source_last_timestamp_utc": "2022-01-03T17:30:00Z",
            "source_session_date": "2022-01-03",
            "source_timeframe": "15m",
        },
        {
            "ticker": "AAPL",
            "dataset_profile": "SWING",
            "dataset_bar_rule": "RTH_HALF_SESSION_195M",
            "session_date": "2022-01-03",
            "session_type": "FULL_ORDINARY_SESSION",
            "bar_number_in_session": "2",
            "bar_start_utc": "2022-01-03T17:45:00Z",
            "bar_end_utc": "2022-01-03T21:00:00Z",
            "bar_start_local": "2022-01-03T12:45:00-05:00",
            "bar_end_local": "2022-01-03T16:00:00-05:00",
            "open": "182.02",
            "high": "182.88",
            "low": "181.195",
            "close": "182.00",
            "volume": "35126661",
            "transactions": "300199",
            "vwap": "182.035",
            "source_row_count": "13",
            "source_first_timestamp_utc": "2022-01-03T17:45:00Z",
            "source_last_timestamp_utc": "2022-01-03T20:45:00Z",
            "source_session_date": "2022-01-03",
            "source_timeframe": "15m",
        },
    ]


def _position_rows() -> list[dict[str, str]]:
    rows = []
    for date_text, open_value, close_value in (
        ("2022-01-03", "177.83", "182.00"),
        ("2022-01-04", "182.63", "179.69"),
    ):
        rows.append(
            {
                "ticker": "AAPL",
                "dataset_profile": "POSITION_SWING",
                "dataset_bar_rule": "RTH_FULL_SESSION_1D",
                "session_date": date_text,
                "session_type": "FULL_ORDINARY_SESSION",
                "bar_start_utc": f"{date_text}T14:30:00Z",
                "bar_end_utc": f"{date_text}T21:00:00Z",
                "bar_start_local": f"{date_text}T09:30:00-05:00",
                "bar_end_local": f"{date_text}T16:00:00-05:00",
                "open": open_value,
                "high": "182.94",
                "low": "177.71",
                "close": close_value,
                "volume": "82350921",
                "transactions": "745085",
                "vwap": "181.307",
                "source_row_count": "26",
                "source_first_timestamp_utc": f"{date_text}T14:30:00Z",
                "source_last_timestamp_utc": f"{date_text}T20:45:00Z",
                "source_session_date": date_text,
                "source_timeframe": "15m",
            }
        )
    return rows


def _definition(
    *,
    profile: str,
    bar_rule: str,
    dataset_path: str,
    manifest_path: str,
    registry_key: str,
    registry_approval_digest: str,
    rows_digest: str,
    manifest_digest: str,
) -> dict[str, Any]:
    return {
        "registry_key": registry_key,
        "dataset_profile": profile,
        "dataset_bar_rule": bar_rule,
        "ticker": "AAPL",
        "range_start": "2022-01-01",
        "range_end": "2025-12-31",
        "registry_scope": "RESEARCH_DATASET",
        "registry_approval_digest": registry_approval_digest,
        "dataset_rows_digest": rows_digest,
        "dataset_manifest_digest": manifest_digest,
        "expected_dataset_path": dataset_path,
        "expected_manifest_path": manifest_path,
        "runtime_use": execution.NOT_AUTHORIZED,
        "strategy_use": execution.NOT_AUTHORIZED,
    }


def _fixture_definitions(tmp_path: Path) -> list[dict[str, Any]]:
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
    return [
        _definition(
            profile="SWING",
            bar_rule="RTH_HALF_SESSION_195M",
            dataset_path=swing_csv.as_posix(),
            manifest_path=swing_manifest.as_posix(),
            registry_key="AAPL:SWING:RTH_HALF_SESSION_195M:2022-01-01:2025-12-31:v1",
            registry_approval_digest=execution.candidate.plan_review.campaign_plan.availability_review.verification.discovery.runtime_planning.EXPECTED_SWING_REGISTRY_APPROVAL_DIGEST,
            rows_digest=swing_rows_digest,
            manifest_digest=swing_manifest_digest,
        ),
        _definition(
            profile="POSITION_SWING",
            bar_rule="RTH_FULL_SESSION_1D",
            dataset_path=position_csv.as_posix(),
            manifest_path=position_manifest.as_posix(),
            registry_key="AAPL:POSITION_SWING:RTH_FULL_SESSION_1D:2022-01-01:2025-12-31:v1",
            registry_approval_digest=execution.candidate.plan_review.campaign_plan.availability_review.verification.discovery.runtime_planning.EXPECTED_POSITION_SWING_REGISTRY_APPROVAL_DIGEST,
            rows_digest=position_rows_digest,
            manifest_digest=position_manifest_digest,
        ),
    ]


def _patch_definitions(monkeypatch: pytest.MonkeyPatch, definitions: list[dict[str, Any]]) -> None:
    monkeypatch.setattr(execution.discovery, "_registry_definitions", lambda: deepcopy(definitions))


def _artifact(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> dict[str, Any]:
    definitions = _fixture_definitions(tmp_path)
    _patch_definitions(monkeypatch, definitions)
    return execution.execute_research_applicability_campaign_v1(
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


def _walk_keys(value: Any):
    if isinstance(value, dict):
        for key, item in value.items():
            yield key
            yield from _walk_keys(item)
    elif isinstance(value, list):
        for item in value:
            yield from _walk_keys(item)


def test_execution_service_refuses_to_execute_when_dataset_file_is_missing(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    definitions = _fixture_definitions(tmp_path)
    (tmp_path / definitions[0]["expected_dataset_path"]).unlink()
    _patch_definitions(monkeypatch, definitions)

    artifact = execution.execute_research_applicability_campaign_v1(
        search_root=tmp_path,
        output_root=tmp_path / "outputs",
        run_timestamp_utc=FIXED_TIMESTAMP,
    )

    assert artifact["execution_status"] == (
        execution.RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_BLOCKED_DATASET_VERIFICATION_FAILED
    )
    assert artifact["campaign_execution_performed"] is False
    assert artifact["campaign_results_generated"] is False


def test_execution_service_refuses_to_execute_when_dataset_digest_mismatch_occurs(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    definitions = _fixture_definitions(tmp_path)
    definitions[0]["dataset_rows_digest"] = "0" * 64
    _patch_definitions(monkeypatch, definitions)

    artifact = execution.execute_research_applicability_campaign_v1(
        search_root=tmp_path,
        output_root=tmp_path / "outputs",
        run_timestamp_utc=FIXED_TIMESTAMP,
    )

    assert artifact["execution_status"] == (
        execution.RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_BLOCKED_DATASET_VERIFICATION_FAILED
    )
    assert artifact["campaign_execution_performed"] is False
    assert artifact["campaign_results_generated"] is False


def test_execution_builds_an_executed_artifact_from_fixture_datasets(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    assert _artifact(tmp_path, monkeypatch)["artifact_kind"] == (
        execution.ARTIFACT_KIND_RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTED
    )


def test_artifact_kind_is_research_applicability_campaign_executed(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    assert _artifact(tmp_path, monkeypatch)["artifact_kind"] == "RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTED"


def test_execution_status_is_research_only(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    assert _artifact(tmp_path, monkeypatch)["execution_status"] == (
        execution.RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTED_RESEARCH_ONLY
    )


def test_campaign_execution_authorized_performed_and_results_generated_are_true(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    artifact = _artifact(tmp_path, monkeypatch)

    assert artifact["campaign_execution_authorized"] is True
    assert artifact["campaign_execution_performed"] is True
    assert artifact["campaign_results_generated"] is True


def test_provider_and_runtime_boundaries_remain_false(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    artifact = _artifact(tmp_path, monkeypatch)

    assert artifact["provider_requests_made"] is False
    assert artifact["runtime_migration_approved"] is False
    assert artifact["runtime_migration_active"] is False
    assert artifact["strategy_runtime_migration"] is False
    assert artifact["automatic_stitching"] is False


def test_runtime_strategy_paper_and_broker_remain_not_authorized(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    artifact = _artifact(tmp_path, monkeypatch)

    assert artifact["runtime_use"] == execution.NOT_AUTHORIZED
    assert artifact["strategy_use"] == execution.NOT_AUTHORIZED
    assert artifact["paper_trading"] == execution.NOT_AUTHORIZED
    assert artifact["broker_execution"] == execution.NOT_AUTHORIZED


def test_predictive_usefulness_and_profitability_remain_not_accepted(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    artifact = _artifact(tmp_path, monkeypatch)

    assert artifact["predictive_usefulness"] == execution.acquisition.PREDICTIVE_USEFULNESS_NOT_ACCEPTED
    assert artifact["profitability"] == execution.acquisition.PROFITABILITY_NOT_ACCEPTED


def test_approval_and_source_digests_are_bound(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    artifact = _artifact(tmp_path, monkeypatch)

    assert artifact["research_campaign_execution_approval_digest"] == execution.EXPECTED_APPROVAL_DIGEST
    assert artifact["execution_candidate_digest"] == execution.approval.EXPECTED_EXECUTION_CANDIDATE_DIGEST
    assert artifact["execution_candidate_review_package_digest"] == (
        execution.approval.EXPECTED_EXECUTION_CANDIDATE_REVIEW_PACKAGE_DIGEST
    )
    assert artifact["dataset_availability_review_package_digest"] == (
        execution.candidate.EXPECTED_DATASET_FILE_AVAILABILITY_VERIFICATION_REVIEW_PACKAGE_DIGEST
    )


def test_registry_approval_digests_are_bound(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    artifact = _artifact(tmp_path, monkeypatch)

    assert artifact["swing_registry_approval_digest"] == (
        execution.candidate.plan_review.campaign_plan.availability_review.verification.discovery.runtime_planning.EXPECTED_SWING_REGISTRY_APPROVAL_DIGEST
    )
    assert artifact["position_swing_registry_approval_digest"] == (
        execution.candidate.plan_review.campaign_plan.availability_review.verification.discovery.runtime_planning.EXPECTED_POSITION_SWING_REGISTRY_APPROVAL_DIGEST
    )


def test_dataset_count_and_generated_output_count(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    artifact = _artifact(tmp_path, monkeypatch)

    assert artifact["dataset_count"] == 2
    assert artifact["generated_output_count"] == 12


def test_all_output_labels_are_research_only_non_actionable(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    artifact = _artifact(tmp_path, monkeypatch)

    assert {report["output_label"] for report in artifact["reports"].values()} == {
        execution.RESEARCH_ONLY_NON_ACTIONABLE
    }
    for name in execution.OUTPUT_NAMES:
        assert _read_output(tmp_path, name)["output_label"] == execution.RESEARCH_ONLY_NON_ACTIONABLE


def test_run_manifest_includes_all_output_digests(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    artifact = _artifact(tmp_path, monkeypatch)
    manifest = _read_output(tmp_path, "research_campaign_run_manifest")

    assert sorted(artifact["output_digest_manifest"]) == sorted(execution.OUTPUT_NAMES)
    assert sorted(manifest["output_digests"]) == sorted(execution.OUTPUT_NAMES)
    assert all(manifest["output_digests"].values())


def test_required_reports_are_generated(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    _artifact(tmp_path, monkeypatch)

    for report_name in (
        "schema_validation_report",
        "bar_count_consistency_report",
        "null_field_summary_report",
        "ohlc_consistency_report",
        "volume_consistency_report",
    ):
        assert (tmp_path / "outputs" / f"{report_name}.json").is_file()


def test_indicator_report_is_research_only_not_performance_acceptance(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    _artifact(tmp_path, monkeypatch)

    report = _read_output(tmp_path, "indicator_calculation_report")

    assert report["indicator_acceptance_label"] == execution.RESEARCH_ONLY_NOT_PERFORMANCE_ACCEPTANCE
    assert {item["calculation_label"] for item in report["datasets"]} == {
        execution.RESEARCH_ONLY_NOT_PERFORMANCE_ACCEPTANCE
    }


def test_no_trade_recommendation_fields_exist_in_outputs(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    _artifact(tmp_path, monkeypatch)

    for name in execution.OUTPUT_NAMES:
        output = _read_output(tmp_path, name)
        assert not any("recommendation" in str(key).lower() for key in _walk_keys(output))
        assert not any(str(value).upper() in {"BUY", "SELL", "HOLD"} for value in _walk_values(output))


def test_execution_digest_is_deterministic_for_fixed_timestamp_and_fixture_input(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    first = _artifact(tmp_path, monkeypatch)
    second = execution.execute_research_applicability_campaign_v1(
        search_root=tmp_path,
        output_root=tmp_path / "outputs",
        run_timestamp_utc=FIXED_TIMESTAMP,
    )

    assert first["research_applicability_campaign_execution_digest"] == second[
        "research_applicability_campaign_execution_digest"
    ]


def test_validator_accepts_valid_executed_artifact(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    validation = execution.validate_research_applicability_campaign_executed_v1(
        _artifact(tmp_path, monkeypatch)
    )

    assert validation["status"] == "RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTED_VALID"


@pytest.mark.parametrize(
    ("field", "value", "match"),
    [
        ("provider_requests_made", True, "provider_requests_made"),
        ("runtime_migration_approved", True, "runtime_migration_approved"),
        ("runtime_migration_active", True, "runtime_migration_active"),
        ("strategy_runtime_migration", True, "strategy_runtime_migration"),
        ("runtime_use", "AUTHORIZED", "runtime_use"),
        ("strategy_use", "AUTHORIZED", "strategy_use"),
        ("paper_trading", "AUTHORIZED", "paper_trading"),
        ("broker_execution", "AUTHORIZED", "broker_execution"),
    ],
)
def test_validator_rejects_forbidden_authorization_mutations(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    field: str,
    value,
    match: str,
):
    artifact = _artifact(tmp_path, monkeypatch)
    artifact[field] = value

    with pytest.raises(execution.ResearchApplicabilityCampaignExecutionError, match=match):
        execution.validate_research_applicability_campaign_executed_v1(artifact)


def test_validator_rejects_predictive_and_profitability_accepted(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    for field in ("predictive_usefulness", "profitability"):
        artifact = _artifact(tmp_path, monkeypatch)
        artifact[field] = "accepted"

        with pytest.raises(execution.ResearchApplicabilityCampaignExecutionError, match=field):
            execution.validate_research_applicability_campaign_executed_v1(artifact)


def test_validator_rejects_generated_output_count_not_twelve(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    artifact = _artifact(tmp_path, monkeypatch)
    artifact["generated_output_count"] = 11

    with pytest.raises(execution.ResearchApplicabilityCampaignExecutionError, match="generated_output_count"):
        execution.validate_research_applicability_campaign_executed_v1(artifact)


def test_validator_rejects_output_labels_not_research_only(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    artifact = _artifact(tmp_path, monkeypatch)
    artifact["reports"]["dataset_load_report"]["output_label"] = "OTHER"

    with pytest.raises(execution.ResearchApplicabilityCampaignExecutionError, match="output_label"):
        execution.validate_research_applicability_campaign_executed_v1(artifact)


def test_status_markdown_includes_required_sections_and_boundaries(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    markdown = execution.write_research_applicability_campaign_execution_status_markdown_v1(
        _artifact(tmp_path, monkeypatch)
    )

    for section in (
        "## Branch And Commit",
        "## Execution Artifact",
        "## Outputs Generated Summary",
        "## Output Digest Manifest",
        "## Dataset Load Summary",
        "## Schema Bar Date Null OHLC Volume Indicator Module Summaries",
        "## Failure Warning Count",
        "## Runtime Boundary",
        "## Predictive Profitability Boundary",
        "## Non-Goals",
        "## Next Task",
    ):
        assert section in markdown
    assert "runtime_use: `NOT_AUTHORIZED`" in markdown
    assert "predictive_usefulness: `not accepted`" in markdown


def test_research_applicability_campaign_execution_service_exports_are_public():
    import marketflow.services as services

    assert services.ARTIFACT_KIND_RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTED == (
        execution.ARTIFACT_KIND_RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTED
    )
    assert services.RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTED_RESEARCH_ONLY == (
        execution.RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTED_RESEARCH_ONLY
    )
    assert services.execute_research_applicability_campaign_v1 is (
        execution.execute_research_applicability_campaign_v1
    )
    assert services.validate_research_applicability_campaign_executed_v1 is (
        execution.validate_research_applicability_campaign_executed_v1
    )
    assert services.write_research_applicability_campaign_execution_status_markdown_v1 is (
        execution.write_research_applicability_campaign_execution_status_markdown_v1
    )
