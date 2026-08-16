from __future__ import annotations

import json
from copy import deepcopy
from unittest.mock import patch

import pytest

from marketflow.historical_data.artifacts import sha256_file
from marketflow.services import label_objective_redesign_execution_service as execution


FIXED_TIMESTAMP = "2026-08-16T13:00:00Z"


def _verified_source() -> dict:
    return {
        "source_root": "isolated/source",
        "required_source_file_count": 9,
        "required_source_files": list(execution.REQUIRED_SOURCE_FILENAMES),
        "records_digest_expected": execution.EXPECTED_RECORDS_DIGEST,
        "records_digest_actual": execution.EXPECTED_RECORDS_DIGEST,
        "records_digest_match": True,
        "total_record_count_actual": 11946,
        "per_ticker_record_counts_actual": deepcopy(
            execution.EXPECTED_RECORD_COUNTS
        ),
        "canonical_dataset_generation_digest": (
            execution.EXPECTED_CANONICAL_DATASET_GENERATION_DIGEST
        ),
        "digest_manifest_self_reference_policy": (
            "SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE"
        ),
    }


def _execute(output_root, source_root) -> dict:
    with patch.object(
        execution,
        "_verify_source_root",
        return_value=(_verified_source(), []),
    ):
        return execution.execute_label_objective_redesign_v1(
            source_root=source_root,
            output_root=output_root,
            run_timestamp_utc=FIXED_TIMESTAMP,
        )


@pytest.fixture(scope="module")
def executed(tmp_path_factory):
    root = tmp_path_factory.mktemp("label_objective_redesign_execution")
    output_root = root / "outputs"
    artifact = _execute(output_root, root / "source")
    return artifact, output_root


def test_execution_builds_offline(
    tmp_path, monkeypatch: pytest.MonkeyPatch
) -> None:
    def forbidden_connect(*_args, **_kwargs):
        raise AssertionError("network access is forbidden")

    monkeypatch.setattr("socket.socket.connect", forbidden_connect)
    artifact = _execute(tmp_path / "outputs", tmp_path / "source")
    assert artifact["created_offline"] is True
    assert artifact["provider_requests_made_in_execution"] is False
    assert artifact["live_provider_transport_enabled_in_execution"] is False


def test_execution_blocks_if_canonical_source_is_missing(tmp_path) -> None:
    artifact = execution.execute_label_objective_redesign_v1(
        source_root=tmp_path / "missing",
        output_root=tmp_path / "outputs",
        run_timestamp_utc=FIXED_TIMESTAMP,
    )
    assert artifact["artifact_kind"] == (
        "LABEL_OBJECTIVE_REDESIGN_EXECUTION_BLOCKED"
    )
    assert artifact["execution_status"] == (
        "LABEL_OBJECTIVE_REDESIGN_EXECUTION_BLOCKED_MISSING_OR_INVALID_CANONICAL_DATASET"
    )
    assert artifact["label_objective_redesign_execution_digest"] == "NOT_CREATED"
    assert artifact["label_objective_redesign_executed"] is False
    assert artifact["label_objective_redesign_results_created"] is False
    assert artifact["generated_output_count"] == 0
    assert artifact["failure_count"] == 9
    assert not (tmp_path / "outputs").exists()


def test_artifact_schema_and_execution_status_are_exact(executed) -> None:
    artifact, _ = executed
    assert artifact["artifact_kind"] == "LABEL_OBJECTIVE_REDESIGN_EXECUTED"
    assert artifact["schema_version"] == "label_objective_redesign_executed_v1"
    assert artifact["execution_status"] == (
        "LABEL_OBJECTIVE_REDESIGN_EXECUTED_RESEARCH_ONLY"
    )


@pytest.mark.parametrize(
    ("field", "expected"), list(execution._source_evidence().items())
)
def test_all_required_source_digests_are_bound(
    executed, field: str, expected: str
) -> None:
    artifact, _ = executed
    assert artifact["source_evidence"][field] == expected


def test_dataset_universe_and_record_counts_are_preserved(executed) -> None:
    artifact, _ = executed
    assert artifact["dataset_name"] == "expanded_universe_canonical_dataset_v1"
    assert artifact["target_universe"] == execution.TARGET_UNIVERSE
    assert artifact["target_universe_count"] == 12
    assert artifact["total_canonical_record_count"] == 11946
    assert artifact["records_digest"] == execution.EXPECTED_RECORDS_DIGEST
    assert artifact["meta_record_count"] == 913
    assert artifact["non_meta_record_count"] == 1003
    assert artifact["per_ticker_record_counts"] == execution.EXPECTED_RECORD_COUNTS
    assert artifact["meta_reduced_record_count_preserved"] is True


def test_execution_approved_authorized_ready_performed_and_results_created(
    executed,
) -> None:
    artifact, _ = executed
    for field in (
        "label_objective_redesign_execution_approved",
        "label_objective_redesign_authorized",
        "ready_for_label_objective_redesign_execution",
        "label_objective_redesign_executed",
        "label_objective_redesign_results_created",
    ):
        assert artifact[field] is True


@pytest.mark.parametrize(
    "field",
    [
        "label_objective_redesign_manifest_created",
        "label_family_candidate_matrix_created",
        "threshold_design_matrix_created",
        "horizon_design_matrix_created",
        "per_ticker_label_objective_plan_created",
        "label_availability_boundary_plan_created",
        "meta_limitation_preservation_plan_created",
        "operator_review_summary_template_created",
    ],
)
def test_all_planning_outputs_are_marked_created(executed, field: str) -> None:
    artifact, _ = executed
    assert artifact[field] is True


def test_exactly_eight_named_outputs_are_written(executed) -> None:
    artifact, output_root = executed
    assert artifact["generated_output_count"] == 8
    assert artifact["generated_output_names"] == execution.OUTPUT_FILENAMES
    assert sorted(path.name for path in output_root.iterdir()) == sorted(
        execution.OUTPUT_FILENAMES
    )


def test_label_family_candidate_matrix_is_design_only(executed) -> None:
    artifact, output_root = executed
    payload = json.loads(
        (output_root / "label_family_candidate_matrix.json").read_text(
            encoding="utf-8"
        )
    )
    rows = payload["label_family_candidates"]
    assert artifact["candidate_label_family_count"] == 10
    assert payload["candidate_label_family_count"] == 10
    assert [row["candidate_family_id"] for row in rows] == execution.LABEL_FAMILY_IDS
    assert all(row["generation_status"] == "NOT_GENERATED" for row in rows)
    assert all(
        row["authorization_status"] == "NOT_AUTHORIZED_FOR_LABEL_GENERATION"
        for row in rows
    )
    assert all("meta_limitation_handling" in row for row in rows)


def test_threshold_design_matrix_describes_strategies_without_computing(
    executed,
) -> None:
    artifact, output_root = executed
    payload = json.loads(
        (output_root / "threshold_design_matrix.json").read_text(encoding="utf-8")
    )
    rows = payload["threshold_design_strategies"]
    assert artifact["threshold_design_strategy_count"] == 7
    assert [row["threshold_strategy_id"] for row in rows] == (
        execution.THRESHOLD_STRATEGY_IDS
    )
    assert all(row["final_threshold_computed"] is False for row in rows)
    assert all(row["status"] == "DESIGN_ONLY_NOT_EXECUTED" for row in rows)


def test_horizon_design_matrix_describes_five_candidates(executed) -> None:
    artifact, output_root = executed
    payload = json.loads(
        (output_root / "horizon_design_matrix.json").read_text(encoding="utf-8")
    )
    rows = payload["horizon_design_candidates"]
    assert artifact["horizon_design_candidate_count"] == 5
    assert [row["horizon_candidate_id"] for row in rows] == (
        execution.HORIZON_CANDIDATE_IDS
    )
    assert all(row["final_horizon_selected"] is False for row in rows)
    assert all(row["status"] == "DESIGN_ONLY_NOT_EXECUTED" for row in rows)


def test_per_ticker_label_objective_plan_preserves_counts_and_order(executed) -> None:
    artifact, output_root = executed
    payload = json.loads(
        (output_root / "per_ticker_label_objective_plan.json").read_text(
            encoding="utf-8"
        )
    )
    rows = payload["per_ticker_label_objective_plans"]
    assert artifact["per_ticker_plan_count"] == 12
    assert [row["ticker"] for row in rows] == execution.TARGET_UNIVERSE
    assert all(
        row["historical_record_count"]
        == execution.EXPECTED_RECORD_COUNTS[row["ticker"]]
        for row in rows
    )
    assert all(row["execution_status"] == "NOT_EXECUTED" for row in rows)
    assert all(row["label_generation_performed"] is False for row in rows)


def test_label_availability_plan_preserves_future_boundaries(executed) -> None:
    _, output_root = executed
    payload = json.loads(
        (output_root / "label_availability_boundary_plan.json").read_text(
            encoding="utf-8"
        )
    )
    assert "forward_horizon_tail_rows_remain_unavailable" in payload[
        "availability_rules"
    ]
    assert "missing_forward_outcomes_must_not_be_fabricated" in payload[
        "availability_rules"
    ]
    assert payload["label_generation_authorized"] is False
    assert payload["label_generation_performed"] is False


def test_meta_limitation_plan_prohibits_backfill_repair_and_synthetic_rows(
    executed,
) -> None:
    _, output_root = executed
    payload = json.loads(
        (output_root / "meta_limitation_preservation_plan.json").read_text(
            encoding="utf-8"
        )
    )
    assert payload["ticker"] == "META"
    assert payload["historical_record_count"] == 913
    assert payload["no_backfill"] is True
    assert payload["no_repair"] is True
    assert payload["no_synthetic_rows"] is True
    assert payload["label_availability_limitation_carried_forward"] is True


def test_operator_review_summary_remains_an_unfilled_template(executed) -> None:
    _, output_root = executed
    payload = json.loads(
        (output_root / "operator_review_summary_template.json").read_text(
            encoding="utf-8"
        )
    )
    assert payload["review_status"] == "AWAITING_SEPARATE_RESULTS_REVIEW"
    assert payload["operator_decision"] is None
    assert payload["results_review_created"] is False


def test_output_digest_manifest_is_complete_and_matches_files(executed) -> None:
    artifact, output_root = executed
    entries = artifact["output_digest_manifest"]
    assert len(entries) == 8
    assert [entry["filename"] for entry in entries] == execution.OUTPUT_FILENAMES
    assert entries[0] == {
        "filename": "label_objective_redesign_execution_manifest.json",
        "digest_kind": "SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE",
        "sha256": None,
    }
    for entry in entries[1:]:
        assert entry["digest_kind"] == "FILE_SHA256"
        assert entry["sha256"] == sha256_file(output_root / entry["filename"])


def test_every_generated_output_is_research_only_and_non_actionable(executed) -> None:
    _, output_root = executed
    for filename in execution.OUTPUT_FILENAMES:
        payload = json.loads((output_root / filename).read_text(encoding="utf-8"))
        assert payload["output_label"] == "RESEARCH_ONLY_NON_ACTIONABLE"
        assert payload["evidence_scope"] == (
            "LABEL_OBJECTIVE_REDESIGN_RESEARCH_ONLY"
        )
        assert payload["redesigned_label_generation_authorized"] is False
        assert payload["redesigned_label_generation_performed"] is False
        assert payload["trade_recommendations_generated"] is False


@pytest.mark.parametrize(
    "field",
    [
        "provider_requests_made_in_execution",
        "live_provider_transport_enabled_in_execution",
        "market_data_acquisition_performed_in_execution",
        "dataset_generation_performed_in_execution",
        "canonical_dataset_regenerated_in_execution",
        "predictive_evidence_rerun_performed",
        "refined_evidence_rerun_performed",
        "label_generation_performed",
        "redesigned_label_generation_authorized",
        "redesigned_label_generation_performed",
        "redesigned_feature_generation_authorized",
        "redesigned_feature_generation_performed",
        "redesigned_protocol_evaluation_authorized",
        "redesigned_protocol_evaluation_performed",
        "feature_generation_performed",
        "metric_recomputation_performed",
        "model_training_performed",
        "additional_predictive_evidence_execution_candidate_created",
        "additional_predictive_evidence_execution_authorized",
        "additional_predictive_evidence_executed",
        "new_strategy_scoring_performed",
        "trade_recommendations_generated",
    ],
)
def test_all_forbidden_execution_and_generation_actions_remain_false(
    executed, field: str
) -> None:
    artifact, _ = executed
    assert artifact[field] is False


def test_acceptance_profitability_runtime_and_trading_remain_closed(executed) -> None:
    artifact, _ = executed
    assert artifact["predictive_usefulness"] == "not accepted"
    assert artifact["predictive_usefulness_acceptance_candidate_created"] is False
    assert artifact["profitability"] == "not accepted"
    assert artifact["runtime_migration_approved"] is False
    assert artifact["runtime_migration_active"] is False
    for field in ("runtime_use", "strategy_use", "paper_trading", "broker_execution"):
        assert artifact[field] == "NOT_AUTHORIZED"


def test_execution_checklist_and_summary_pass(executed) -> None:
    artifact, _ = executed
    assert len(artifact["execution_checklist"]) == len(execution.CHECK_IDS) == 44
    assert all(row["status"] == "PASS" for row in artifact["execution_checklist"])
    summary = artifact["execution_summary"]
    assert summary["total_checks"] == 44
    assert summary["passed_checks"] == 44
    assert summary["failed_checks"] == 0
    assert summary["blocker_count"] == 0
    assert summary["failure_count"] == 0
    assert summary["warning_count"] == 1
    assert summary["label_objective_redesign_execution_digest"] == artifact[
        "label_objective_redesign_execution_digest"
    ]


def test_validator_accepts_valid_artifact(executed) -> None:
    artifact, _ = executed
    result = execution.validate_label_objective_redesign_executed_v1(artifact)
    assert result["status"] == "LABEL_OBJECTIVE_REDESIGN_EXECUTION_VALID"
    assert result["label_objective_redesign_executed"] is True
    assert result["generated_output_count"] == 8
    assert result["label_generation_performed"] is False


@pytest.mark.parametrize(
    ("field", "bad_value"),
    [
        ("artifact_kind", "WRONG"),
        ("execution_status", "WRONG"),
        ("label_objective_redesign_execution_approved", False),
        ("label_objective_redesign_authorized", False),
        ("ready_for_label_objective_redesign_execution", False),
        ("label_objective_redesign_executed", False),
        ("label_objective_redesign_results_created", False),
        ("generated_output_count", 7),
        ("target_universe", list(reversed(execution.TARGET_UNIVERSE))),
        ("target_universe_count", 11),
        ("records_digest", "0" * 64),
        ("meta_record_count", 1003),
        ("label_generation_performed", True),
        ("redesigned_label_generation_authorized", True),
        ("redesigned_label_generation_performed", True),
        ("feature_generation_performed", True),
        ("metric_recomputation_performed", True),
        ("model_training_performed", True),
        ("additional_predictive_evidence_execution_candidate_created", True),
        ("predictive_usefulness", "accepted"),
        ("profitability", "accepted"),
        ("runtime_use", "AUTHORIZED"),
        ("strategy_use", "AUTHORIZED"),
        ("paper_trading", "AUTHORIZED"),
        ("broker_execution", "AUTHORIZED"),
        ("trade_recommendations_generated", True),
    ],
)
def test_validator_rejects_changed_or_forbidden_values(
    executed, field: str, bad_value: object
) -> None:
    artifact, _ = executed
    mutated = deepcopy(artifact)
    mutated[field] = bad_value
    with pytest.raises(execution.LabelObjectiveRedesignExecutionError):
        execution.validate_label_objective_redesign_executed_v1(mutated)


def test_validator_rejects_missing_execution_approval_digest(executed) -> None:
    artifact, _ = executed
    mutated = deepcopy(artifact)
    mutated["source_evidence"].pop(
        "label_objective_redesign_execution_approval_digest"
    )
    with pytest.raises(execution.LabelObjectiveRedesignExecutionError):
        execution.validate_label_objective_redesign_executed_v1(mutated)


def test_validator_rejects_missing_output_digest(executed) -> None:
    artifact, _ = executed
    mutated = deepcopy(artifact)
    mutated["output_digest_manifest"][1].pop("sha256")
    with pytest.raises(execution.LabelObjectiveRedesignExecutionError):
        execution.validate_label_objective_redesign_executed_v1(mutated)


def test_execution_digest_is_deterministic_for_fixed_timestamp_and_source(
    tmp_path, executed
) -> None:
    artifact, _ = executed
    second = _execute(tmp_path / "outputs", tmp_path / "source")
    assert second["label_objective_redesign_execution_digest"] == artifact[
        "label_objective_redesign_execution_digest"
    ]
    assert second["output_digest_manifest"] == artifact["output_digest_manifest"]


def test_markdown_includes_all_required_sections(executed) -> None:
    artifact, _ = executed
    markdown = execution.build_label_objective_redesign_execution_status_markdown_v1(
        artifact
    )
    headings = [
        "Title",
        "Label Objective Redesign Execution",
        "Source Execution Approval",
        "Dataset and Universe",
        "Generated Planning Outputs",
        "Label Family Candidate Matrix",
        "Threshold Design Matrix",
        "Horizon Design Matrix",
        "Per-Ticker Label Objective Plan",
        "META Limitation Preservation Plan",
        "Output Digest Manifest",
        "Execution Boundary",
        "Predictive Usefulness Boundary",
        "Profitability Boundary",
        "Runtime Boundary",
        "Checklist Summary",
        "Guardrails",
    ]
    assert all(f"## {heading}" in markdown for heading in headings)
    assert "actual redesigned labels" in markdown
