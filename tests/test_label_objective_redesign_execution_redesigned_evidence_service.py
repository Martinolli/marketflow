from __future__ import annotations

import json
from copy import deepcopy

import pytest

from marketflow.historical_data.artifacts import sha256_file
from marketflow.services import (
    label_objective_redesign_execution_redesigned_evidence_service as execution,
)


FIXED_TIMESTAMP = "2026-08-21T21:00:00Z"


def _reports() -> dict:
    per_ticker = [{"ticker": ticker} for ticker in execution.TARGET_UNIVERSE]
    return {
        "majority_structure": {
            "majority_class": "FLAT", "majority_class_count": 13600,
            "evaluated_class_count": 34848, "majority_baseline_accuracy": "0.58626033",
            "local_model_accuracy": "0.58626033",
        },
        "cross_sectional_edge": {
            "cross_sectional_accuracy": "0.58935950",
            "oos_cross_sectional_delta_vs_majority": "0.00309917",
            "cross_sectional_edge_materiality": "SMALL_NOT_ACCEPTANCE_EVIDENCE",
        },
        "horizon_noise": {
            "source_horizon_strategies": [
                "one_session_horizon_candidate", "five_session_horizon_candidate",
                "ten_session_horizon_candidate", "twenty_session_horizon_candidate",
                "multi_horizon_comparison_candidate",
            ],
            "source_multi_horizon_values": [5, 10, 20],
        },
        "threshold_materiality": {
            "global_threshold_5_session": "0.026556108631",
            "benchmark_relative_threshold_5_session": "0.02058653801",
        },
        "class_balance": {"source_class_balance": {"FLAT": 13600, "NO_TRADE": 1540}},
        "per_ticker_behavior": {"per_ticker_execution_entries": per_ticker},
    }


def _verification() -> dict:
    return {
        "all_required_source_files_present": True,
        "all_required_source_digests_match": True,
        "source_files_unchanged": True,
        "source_file_count": len(execution.SOURCE_FILES),
        "source_file_sha256": {},
        "verified_records_digest": execution.EXPECTED_RECORDS_DIGEST,
        "verified_redesigned_label_values_digest": execution.EXPECTED_LABEL_VALUES_DIGEST,
        "verified_feature_values_digest": execution.EXPECTED_FEATURE_VALUES_DIGEST,
        "verified_feature_label_matrix_digest": execution.EXPECTED_MATRIX_DIGEST,
        "verified_review_execution_digest": execution.EXPECTED_REVIEW_EXECUTION_DIGEST,
        "verified_review_output_binding_digest": execution.EXPECTED_REVIEW_OUTPUT_BINDING_DIGEST,
    }


def _execute(monkeypatch: pytest.MonkeyPatch, output_root, source_root) -> dict:
    monkeypatch.setattr(
        execution, "_verify_sources", lambda _roots: (_verification(), _reports(), [])
    )
    return execution.execute_label_objective_redesign_using_redesigned_evidence_v1(
        canonical_root=source_root / "canonical",
        label_root=source_root / "labels",
        feature_root=source_root / "features",
        predictive_evidence_root=source_root / "predictive",
        label_objective_review_root=source_root / "review",
        output_root=output_root,
        run_timestamp_utc=FIXED_TIMESTAMP,
    )


@pytest.fixture
def executed(tmp_path, monkeypatch: pytest.MonkeyPatch):
    output_root = tmp_path / "outputs"
    artifact = _execute(monkeypatch, output_root, tmp_path / "source")
    return artifact, output_root


def test_execution_builds_offline(tmp_path, monkeypatch: pytest.MonkeyPatch) -> None:
    def forbidden_connect(*_args, **_kwargs):
        raise AssertionError("network access is forbidden")

    monkeypatch.setattr("socket.socket.connect", forbidden_connect)
    artifact = _execute(monkeypatch, tmp_path / "outputs", tmp_path / "source")
    assert artifact["created_offline"] is True
    assert artifact["provider_requests_made_in_execution"] is False


def test_execution_blocks_if_required_source_root_is_missing(tmp_path) -> None:
    artifact = execution.execute_label_objective_redesign_using_redesigned_evidence_v1(
        canonical_root=tmp_path / "canonical",
        label_root=tmp_path / "labels",
        feature_root=tmp_path / "features",
        predictive_evidence_root=tmp_path / "predictive",
        label_objective_review_root=tmp_path / "review",
        output_root=tmp_path / "outputs",
        run_timestamp_utc=FIXED_TIMESTAMP,
    )
    assert artifact["artifact_kind"] == "LABEL_OBJECTIVE_REDESIGN_BLOCKED_USING_REDESIGNED_EVIDENCE"
    assert artifact["execution_status"] == "LABEL_OBJECTIVE_REDESIGN_BLOCKED_MISSING_OR_INVALID_SOURCE_EVIDENCE"
    assert artifact["label_objective_redesign_executed"] is False
    assert artifact["label_objective_redesign_results_created"] is False
    assert artifact["generated_output_count"] == 0
    assert not (tmp_path / "outputs").exists()


def test_artifact_kind_status_and_schema_are_exact(executed) -> None:
    artifact, _ = executed
    assert artifact["artifact_kind"] == "LABEL_OBJECTIVE_REDESIGN_EXECUTED_USING_REDESIGNED_EVIDENCE"
    assert artifact["execution_status"] == "LABEL_OBJECTIVE_REDESIGN_EXECUTED_USING_REDESIGNED_EVIDENCE_RESEARCH_ONLY"
    assert artifact["schema_version"] == "label_objective_redesign_executed_using_redesigned_evidence_v1"


@pytest.mark.parametrize(("field", "expected"), list(execution._source_evidence().items()))
def test_all_required_source_digests_are_bound(executed, field: str, expected: str) -> None:
    artifact, _ = executed
    assert artifact["source_evidence"][field] == expected


def test_dataset_universe_and_meta_counts_are_preserved(executed) -> None:
    artifact, _ = executed
    assert artifact["target_universe"] == execution.TARGET_UNIVERSE
    assert artifact["target_universe_count"] == 12
    assert artifact["total_canonical_record_count"] == 11946
    assert artifact["records_digest"] == execution.EXPECTED_RECORDS_DIGEST
    assert artifact["meta_record_count"] == 913
    assert artifact["non_meta_record_count"] == 1003
    assert artifact["meta_reduced_record_count_preserved"] is True


@pytest.mark.parametrize(
    "field",
    [
        "label_objective_redesign_approved", "label_objective_redesign_authorized",
        "ready_for_label_objective_redesign_execution_using_redesigned_evidence",
        "label_objective_redesign_executed", "label_objective_redesign_results_created",
    ],
)
def test_execution_authority_fields_are_true(executed, field: str) -> None:
    artifact, _ = executed
    assert artifact[field] is True


def test_selected_direction_is_abstain_no_trade(executed) -> None:
    artifact, _ = executed
    assert artifact["selected_label_objective_redesign_direction"] == execution.SELECTED_DIRECTION


def test_exactly_twelve_outputs_are_written(executed) -> None:
    artifact, output_root = executed
    assert artifact["generated_output_count"] == 12
    assert artifact["generated_output_names"] == execution.OUTPUT_FILENAMES
    assert sorted(path.name for path in output_root.iterdir()) == sorted(execution.OUTPUT_FILENAMES)


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("redesign_theme_count", 11), ("redesign_option_count", 8),
        ("label_family_impact_review_count", 10), ("redesign_question_count", 10),
    ],
)
def test_required_analysis_counts_are_exact(executed, field: str, expected: int) -> None:
    artifact, _ = executed
    assert artifact[field] == expected


@pytest.mark.parametrize(
    "field",
    [
        "label_regeneration_authorized", "label_regeneration_performed", "new_targets_created",
        "target_definition_change_authorized", "target_definition_change_performed",
        "threshold_horizon_refinement_candidate_created", "improved_evidence_planning_candidate_created",
        "additional_predictive_evidence_execution_candidate_created",
        "predictive_usefulness_acceptance_ready", "predictive_usefulness_acceptance_candidate_created",
        "profitability_acceptance_ready", "runtime_migration_approved", "runtime_migration_active",
        "new_strategy_scoring_performed", "trade_recommendations_generated",
        "predictive_evidence_execution_rerun_performed", "metric_recomputation_performed_in_execution",
        "model_training_performed_in_execution",
    ],
)
def test_closed_authority_and_execution_fields_remain_false(executed, field: str) -> None:
    artifact, _ = executed
    assert artifact[field] is False


@pytest.mark.parametrize(
    "field", ["runtime_use", "strategy_use", "paper_trading", "broker_execution"]
)
def test_runtime_and_trading_fields_are_not_authorized(executed, field: str) -> None:
    artifact, _ = executed
    assert artifact[field] == "NOT_AUTHORIZED"


def test_predictive_usefulness_and_profitability_are_not_accepted(executed) -> None:
    artifact, _ = executed
    assert artifact["predictive_usefulness"] == "not accepted"
    assert artifact["profitability"] == "not accepted"


def test_redesign_analysis_classification_is_conservative(executed) -> None:
    artifact, _ = executed
    classification = artifact["redesign_analysis_classification"]
    assert classification["label_objective_redesign_classification"] == "COMPLETED_RESEARCH_ONLY"
    assert classification["selected_direction_analysis_status"] == "ANALYZED_RESEARCH_ONLY"
    assert all(
        value == "REVIEWED_REQUIRES_RESULTS_REVIEW"
        for key, value in classification.items()
        if key.endswith("_assessment") and key != "meta_limitation_assessment"
    )
    assert classification["meta_limitation_assessment"] == "PRESERVED_REQUIRES_OPERATOR_AWARENESS"


def test_decision_recommendation_does_not_authorize_labels_or_targets(executed) -> None:
    artifact, _ = executed
    assert artifact["redesign_analysis_classification"]["redesign_decision_recommendation"] == (
        "NO_LABEL_REGENERATION_OR_NEW_TARGETS_AUTHORIZED_BY_THIS_EXECUTION"
    )


def test_analysis_reports_preserve_source_facts(executed) -> None:
    artifact, _ = executed
    flat = artifact["flat_class_and_majority_structure_analysis"]
    assert flat["largest_aggregated_class"] == "FLAT"
    assert flat["largest_aggregated_class_count"] == 13600
    assert flat["oos_evaluated_rows"] == 34848
    assert artifact["no_trade_abstain_objective_analysis"]["no_trade_count"] == 1540
    assert artifact["acceptance_threshold_prerequisite_review"]["cross_sectional_delta_vs_majority"] == "0.00309917"


def test_per_ticker_execution_entries_and_digests_are_complete(executed) -> None:
    artifact, _ = executed
    rows = artifact["per_ticker_execution_entries"]
    assert [row["ticker"] for row in rows] == execution.TARGET_UNIVERSE
    assert len(rows) == 12
    assert all(len(row["per_ticker_label_objective_redesign_execution_digest"]) == 64 for row in rows)
    meta = rows[4]
    assert meta["ticker"] == "META"
    assert meta["historical_record_count"] == 913
    assert meta["execution_note"] == "PRESERVE_META_LIMITATION_IN_LABEL_OBJECTIVE_REDESIGN_EXECUTION"
    assert all(row["historical_record_count"] == 1003 for row in rows if row["ticker"] != "META")


def test_output_digest_manifest_is_complete(executed) -> None:
    artifact, output_root = executed
    payload = json.loads((output_root / "label_objective_redesign_digest_manifest.json").read_text(encoding="utf-8"))
    rows = payload["output_digest_entries"]
    assert [row["filename"] for row in rows] == execution.OUTPUT_FILENAMES
    assert len(rows) == 12
    self_row = rows[-1]
    assert self_row["digest_kind"] == "SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE"
    assert self_row["sha256"] is None
    for row in rows[:-1]:
        assert row["sha256"] == sha256_file(output_root / row["filename"])


def test_source_hashes_remain_bound(executed) -> None:
    artifact, _ = executed
    verification = artifact["source_verification"]
    assert verification["verified_records_digest"] == execution.EXPECTED_RECORDS_DIGEST
    assert verification["verified_redesigned_label_values_digest"] == execution.EXPECTED_LABEL_VALUES_DIGEST
    assert verification["verified_feature_values_digest"] == execution.EXPECTED_FEATURE_VALUES_DIGEST
    assert verification["verified_feature_label_matrix_digest"] == execution.EXPECTED_MATRIX_DIGEST


def test_validator_accepts_valid_artifact(executed) -> None:
    artifact, _ = executed
    result = execution.validate_label_objective_redesign_executed_using_redesigned_evidence_v1(artifact)
    assert result["status"] == "LABEL_OBJECTIVE_REDESIGN_EXECUTION_USING_REDESIGNED_EVIDENCE_VALID"


@pytest.mark.parametrize(
    ("field", "bad_value"),
    [
        ("artifact_kind", "WRONG"),
        ("execution_status", "WRONG"),
        ("label_objective_redesign_approved", False),
        ("label_objective_redesign_authorized", False),
        ("ready_for_label_objective_redesign_execution_using_redesigned_evidence", False),
        ("label_objective_redesign_executed", False),
        ("label_objective_redesign_results_created", False),
        ("generated_output_count", 11),
        ("target_universe", list(reversed(execution.TARGET_UNIVERSE))),
        ("target_universe_count", 11),
        ("records_digest", "0" * 64),
        ("meta_record_count", 1003),
        ("selected_label_objective_redesign_direction", "WRONG"),
        ("label_regeneration_performed", True),
        ("new_targets_created", True),
        ("target_definition_change_authorized", True),
        ("target_definition_change_performed", True),
        ("threshold_horizon_refinement_candidate_created", True),
        ("improved_evidence_planning_candidate_created", True),
        ("additional_predictive_evidence_execution_candidate_created", True),
        ("predictive_usefulness", "accepted"),
        ("profitability", "accepted"),
        ("runtime_use", "AUTHORIZED"),
        ("strategy_use", "AUTHORIZED"),
        ("paper_trading", "AUTHORIZED"),
        ("broker_execution", "AUTHORIZED"),
        ("trade_recommendations_generated", True),
        ("provider_requests_made_in_execution", True),
        ("canonical_dataset_regenerated_in_execution", True),
        ("redesigned_label_regeneration_performed", True),
        ("predictive_evidence_execution_rerun_performed", True),
        ("metric_recomputation_performed_in_execution", True),
        ("model_training_performed_in_execution", True),
    ],
)
def test_validator_rejects_invalid_contract_fields(executed, field: str, bad_value) -> None:
    artifact, _ = executed
    invalid = deepcopy(artifact)
    invalid[field] = bad_value
    with pytest.raises(execution.LabelObjectiveRedesignExecutionRedesignedEvidenceError):
        execution.validate_label_objective_redesign_executed_using_redesigned_evidence_v1(invalid)


def test_validator_rejects_missing_approval_digest(executed) -> None:
    artifact, _ = executed
    invalid = deepcopy(artifact)
    invalid["source_evidence"].pop("label_objective_redesign_approval_using_redesigned_evidence_digest")
    with pytest.raises(execution.LabelObjectiveRedesignExecutionRedesignedEvidenceError):
        execution.validate_label_objective_redesign_executed_using_redesigned_evidence_v1(invalid)


def test_validator_rejects_missing_output_manifest_digest(executed) -> None:
    artifact, _ = executed
    invalid = deepcopy(artifact)
    invalid["output_digest_manifest_summary"].pop("binding_digest")
    with pytest.raises(execution.LabelObjectiveRedesignExecutionRedesignedEvidenceError):
        execution.validate_label_objective_redesign_executed_using_redesigned_evidence_v1(invalid)


def test_validator_rejects_missing_execution_digest(executed) -> None:
    artifact, _ = executed
    invalid = deepcopy(artifact)
    invalid.pop("label_objective_redesign_execution_using_redesigned_evidence_digest")
    with pytest.raises(execution.LabelObjectiveRedesignExecutionRedesignedEvidenceError):
        execution.validate_label_objective_redesign_executed_using_redesigned_evidence_v1(invalid)


def test_validator_rejects_missing_per_ticker_digest(executed) -> None:
    artifact, _ = executed
    invalid = deepcopy(artifact)
    invalid["per_ticker_execution_entries"][0].pop("per_ticker_label_objective_redesign_execution_digest")
    with pytest.raises(execution.LabelObjectiveRedesignExecutionRedesignedEvidenceError):
        execution.validate_label_objective_redesign_executed_using_redesigned_evidence_v1(invalid)


def test_execution_digest_and_per_ticker_digests_are_deterministic(tmp_path, monkeypatch) -> None:
    first = _execute(monkeypatch, tmp_path / "first", tmp_path / "source")
    second = _execute(monkeypatch, tmp_path / "second", tmp_path / "source")
    # Output-root binding is intentionally part of the artifact digest.
    second["generated_output_root"] = first["generated_output_root"]
    second["label_objective_redesign_execution_using_redesigned_evidence_digest"] = (
        execution.label_objective_redesign_execution_using_redesigned_evidence_digest_v1(second)
    )
    assert first["label_objective_redesign_execution_using_redesigned_evidence_digest"] == second[
        "label_objective_redesign_execution_using_redesigned_evidence_digest"
    ]
    assert [row["per_ticker_label_objective_redesign_execution_digest"] for row in first["per_ticker_execution_entries"]] == [
        row["per_ticker_label_objective_redesign_execution_digest"] for row in second["per_ticker_execution_entries"]
    ]


def test_markdown_includes_required_sections(executed) -> None:
    artifact, _ = executed
    markdown = execution.build_label_objective_redesign_execution_status_markdown_v1(artifact)
    for heading in (
        "Title", "Optional Label Objective Redesign Execution Using Redesigned Evidence",
        "Source Approval", "Bound Evidence", "Dataset and Universe", "Redesign Execution Policy",
        "Candidate Basis", "Selected Redesign Direction",
        "Flat Class and Majority Structure Redesign Analysis", "No-Trade / Abstain Objective Analysis",
        "Material-Move Target Definition Analysis", "Horizon-Specific Target Design Analysis",
        "Ticker or Regime Split Target Analysis", "Risk-Adjusted Target Definition Analysis",
        "Label Family Impact Review", "META Target Limitation Review",
        "Acceptance Threshold Prerequisite Review", "Output Digest Manifest", "Authority Boundary",
        "Predictive Usefulness Boundary", "Profitability Boundary", "Runtime Boundary",
        "Checklist Summary", "Guardrails",
    ):
        assert f"## {heading}" in markdown


def test_public_exports_are_available() -> None:
    import marketflow.services as services

    assert services.ARTIFACT_KIND_LABEL_OBJECTIVE_REDESIGN_EXECUTED_USING_REDESIGNED_EVIDENCE == (
        execution.ARTIFACT_KIND_LABEL_OBJECTIVE_REDESIGN_EXECUTED_USING_REDESIGNED_EVIDENCE
    )
    assert services.LABEL_OBJECTIVE_REDESIGN_EXECUTED_USING_REDESIGNED_EVIDENCE_RESEARCH_ONLY == (
        execution.LABEL_OBJECTIVE_REDESIGN_EXECUTED_USING_REDESIGNED_EVIDENCE_RESEARCH_ONLY
    )
    assert services.execute_label_objective_redesign_using_redesigned_evidence_v1 is (
        execution.execute_label_objective_redesign_using_redesigned_evidence_v1
    )
    assert services.validate_label_objective_redesign_executed_using_redesigned_evidence_v1 is (
        execution.validate_label_objective_redesign_executed_using_redesigned_evidence_v1
    )
    assert services.build_label_objective_redesign_execution_status_markdown_v1 is (
        execution.build_label_objective_redesign_execution_status_markdown_v1
    )
