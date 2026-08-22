from __future__ import annotations

import json
from copy import deepcopy

import pytest

from marketflow.historical_data.artifacts import sha256_file
from marketflow.services import (
    improved_evidence_planning_execution_redesigned_evidence_service as execution,
)


FIXED_TIMESTAMP = "2026-08-22T12:00:00Z"


def _verification() -> dict:
    return {
        "all_required_source_files_present": True,
        "all_required_source_digests_match": True,
        "all_required_source_bindings_match": True,
        "source_files_unchanged": True,
        "source_file_count": len(execution.SOURCE_FILES),
        "source_file_sha256": {},
        "verified_records_digest": execution.EXPECTED_RECORDS_DIGEST,
        "verified_redesigned_label_values_digest": execution.EXPECTED_LABEL_VALUES_DIGEST,
        "verified_feature_values_digest": execution.EXPECTED_FEATURE_VALUES_DIGEST,
        "verified_feature_label_matrix_digest": execution.EXPECTED_MATRIX_DIGEST,
        "verified_redesign_execution_digest": execution.EXPECTED_REDESIGN_EXECUTION_DIGEST,
        "verified_redesign_output_binding_digest": execution.EXPECTED_REDESIGN_OUTPUT_BINDING_DIGEST,
        "verified_review_execution_digest": execution.EXPECTED_REVIEW_EXECUTION_DIGEST,
        "verified_review_output_binding_digest": execution.EXPECTED_REVIEW_OUTPUT_BINDING_DIGEST,
    }


def _execute(monkeypatch: pytest.MonkeyPatch, output_root, source_root) -> dict:
    monkeypatch.setattr(
        execution,
        "_verify_sources",
        lambda _roots: (_verification(), {}, []),
    )
    return execution.execute_improved_evidence_planning_using_redesigned_evidence_v1(
        canonical_root=source_root / "canonical",
        label_root=source_root / "labels",
        feature_root=source_root / "features",
        predictive_evidence_root=source_root / "predictive",
        label_objective_review_root=source_root / "review",
        label_objective_redesign_root=source_root / "redesign",
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
    assert artifact["market_data_acquisition_performed_in_execution"] is False


def test_execution_blocks_if_required_source_root_is_missing(tmp_path) -> None:
    artifact = execution.execute_improved_evidence_planning_using_redesigned_evidence_v1(
        canonical_root=tmp_path / "canonical",
        label_root=tmp_path / "labels",
        feature_root=tmp_path / "features",
        predictive_evidence_root=tmp_path / "predictive",
        label_objective_review_root=tmp_path / "review",
        label_objective_redesign_root=tmp_path / "redesign",
        output_root=tmp_path / "outputs",
        run_timestamp_utc=FIXED_TIMESTAMP,
    )
    assert artifact["artifact_kind"] == (
        execution.ARTIFACT_KIND_IMPROVED_EVIDENCE_PLANNING_BLOCKED_USING_REDESIGNED_EVIDENCE
    )
    assert artifact["execution_status"] == (
        execution.IMPROVED_EVIDENCE_PLANNING_BLOCKED_MISSING_OR_INVALID_SOURCE_EVIDENCE
    )
    assert artifact["improved_evidence_planning_executed"] is False
    assert artifact["improved_evidence_planning_results_created"] is False
    assert artifact["generated_output_count"] == 0
    assert not (tmp_path / "outputs").exists()


def test_artifact_kind_is_correct(executed) -> None:
    artifact, _ = executed
    assert artifact["artifact_kind"] == (
        execution.ARTIFACT_KIND_IMPROVED_EVIDENCE_PLANNING_EXECUTED_USING_REDESIGNED_EVIDENCE
    )


def test_execution_status_is_correct(executed) -> None:
    artifact, _ = executed
    assert artifact["execution_status"] == (
        execution.IMPROVED_EVIDENCE_PLANNING_EXECUTED_USING_REDESIGNED_EVIDENCE_RESEARCH_ONLY
    )


@pytest.mark.parametrize(
    ("field", "expected"), list(execution._source_evidence().items())
)
def test_all_required_source_digests_are_bound(
    executed, field: str, expected: str
) -> None:
    artifact, _ = executed
    assert artifact["source_evidence"][field] == expected


def test_universe_count_and_order_are_preserved(executed) -> None:
    artifact, _ = executed
    assert artifact["target_universe"] == execution.TARGET_UNIVERSE
    assert artifact["target_universe_count"] == 12
    assert artifact["total_canonical_record_count"] == 11946


def test_meta_913_is_preserved(executed) -> None:
    artifact, _ = executed
    assert artifact["meta_record_count"] == 913
    assert artifact["non_meta_record_count"] == 1003
    assert artifact["meta_reduced_record_count_preserved"] is True


@pytest.mark.parametrize(
    "field",
    [
        "improved_evidence_planning_approved",
        "improved_evidence_planning_authorized",
        "ready_for_improved_evidence_planning_execution_using_redesigned_evidence",
    ],
)
def test_planning_approval_authorization_and_readiness_are_true(
    executed, field: str
) -> None:
    artifact, _ = executed
    assert artifact[field] is True


def test_planning_executed_and_results_created_are_true(executed) -> None:
    artifact, _ = executed
    assert artifact["improved_evidence_planning_executed"] is True
    assert artifact["improved_evidence_planning_results_created"] is True


def test_selected_redesign_direction_is_preserved(executed) -> None:
    artifact, _ = executed
    assert artifact["selected_redesign_direction"] == execution.SELECTED_DIRECTION


def test_generated_output_count_and_names_are_exact(executed) -> None:
    artifact, output_root = executed
    assert artifact["generated_output_count"] == 14
    assert artifact["generated_output_names"] == execution.OUTPUT_FILENAMES
    assert sorted(path.name for path in output_root.iterdir()) == sorted(
        execution.OUTPUT_FILENAMES
    )


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("improved_evidence_theme_count", 11),
        ("planned_evidence_component_count", 13),
        ("planned_data_product_count", 13),
        ("planned_future_output_count", 12),
    ],
)
def test_planning_collection_counts_are_exact(
    executed, field: str, expected: int
) -> None:
    artifact, _ = executed
    assert artifact[field] == expected


def test_planned_data_products_preserve_approved_execution_product_ids(executed) -> None:
    artifact, _ = executed
    assert [row["data_product_id"] for row in artifact["planned_data_products"]] == (
        execution.approval.APPROVED_DATA_PRODUCT_IDS
    )


@pytest.mark.parametrize("field", execution.FALSE_GUARDRAIL_FIELDS)
def test_closed_execution_and_authority_fields_remain_false(
    executed, field: str
) -> None:
    artifact, _ = executed
    assert artifact[field] is False


@pytest.mark.parametrize(
    "field", ["runtime_use", "strategy_use", "paper_trading", "broker_execution"]
)
def test_runtime_and_trading_fields_are_not_authorized(
    executed, field: str
) -> None:
    artifact, _ = executed
    assert artifact[field] == "NOT_AUTHORIZED"


def test_predictive_usefulness_and_profitability_are_not_accepted(executed) -> None:
    artifact, _ = executed
    assert artifact["predictive_usefulness"] == "not accepted"
    assert artifact["profitability"] == "not accepted"


def test_planning_execution_classification_is_conservative(executed) -> None:
    artifact, _ = executed
    classification = artifact["planning_execution_classification"]
    assert classification["improved_evidence_planning_classification"] == (
        "COMPLETED_RESEARCH_ONLY"
    )
    assert classification["planning_execution_scope"] == (
        "PLANNING_EXECUTION_ONLY_NOT_EVIDENCE_EXECUTION"
    )
    assert all(
        value == "PLANNED_REQUIRES_RESULTS_REVIEW"
        for key, value in classification.items()
        if key.endswith("_plan_status")
    )


def test_planning_decision_does_not_authorize_evidence_execution(executed) -> None:
    artifact, _ = executed
    assert artifact["planning_execution_classification"][
        "planning_decision_recommendation"
    ] == execution.PLANNING_DECISION_RECOMMENDATION
    assert "PREDICTIVE_EXECUTION_AUTHORIZED_BY_THIS_EXECUTION" in (
        execution.PLANNING_DECISION_RECOMMENDATION
    )


def test_planning_facts_are_preserved(executed) -> None:
    artifact, _ = executed
    facts = artifact["planning_facts"]
    assert facts["largest_aggregated_class"] == "FLAT"
    assert facts["largest_aggregated_class_count"] == 13600
    assert facts["no_trade_count"] == 1540
    assert facts["oos_evaluated_rows"] == 34848
    assert facts["majority_accuracy"] == "0.58626033"
    assert facts["cross_sectional_delta_vs_majority"] == "0.00309917"
    assert facts["global_five_session_threshold"] == "0.026556108631"
    assert facts["benchmark_relative_threshold"] == "0.02058653801"


@pytest.mark.parametrize(
    "field",
    [
        "proposed_label_schema_plan",
        "no_trade_abstain_coverage_plan",
        "material_move_threshold_plan",
        "horizon_specific_validation_plan",
        "ticker_regime_split_validation_plan",
        "feature_label_alignment_plan",
        "chronological_split_embargo_plan",
        "baseline_model_comparison_plan",
        "calibration_brier_plan",
        "leakage_no_peek_control_plan",
        "per_ticker_meta_reporting_plan",
    ],
)
def test_each_plan_requires_results_review_and_does_not_execute_evidence(
    executed, field: str
) -> None:
    artifact, _ = executed
    plan = artifact[field]
    assert plan["plan_status"] == "PLANNED_REQUIRES_RESULTS_REVIEW"
    assert plan["execution_performed"] is False
    assert plan["metric_computation_performed"] is False
    assert plan["model_training_performed"] is False
    assert plan["research_only"] is True
    assert plan["non_actionable"] is True


def test_per_ticker_execution_entries_and_digests_are_complete(executed) -> None:
    artifact, _ = executed
    rows = artifact["per_ticker_execution_entries"]
    assert [row["ticker"] for row in rows] == execution.TARGET_UNIVERSE
    assert len(rows) == 12
    assert all(
        len(row["per_ticker_improved_evidence_planning_execution_digest"]) == 64
        for row in rows
    )
    assert all(row["improved_evidence_planning_executed"] is True for row in rows)
    assert all(
        row["additional_predictive_evidence_execution_candidate_created"] is False
        for row in rows
    )
    meta = rows[4]
    assert meta["ticker"] == "META"
    assert meta["historical_record_count"] == 913
    assert meta["execution_note"] == (
        "PRESERVE_META_LIMITATION_IN_IMPROVED_EVIDENCE_PLANNING_EXECUTION"
    )
    assert all(
        row["historical_record_count"] == 1003
        for row in rows
        if row["ticker"] != "META"
    )


def test_output_digest_manifest_is_created_and_complete(executed) -> None:
    artifact, output_root = executed
    manifest_path = output_root / "improved_evidence_planning_digest_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    rows = manifest["output_digest_entries"]
    assert artifact["output_digest_manifest_summary"]["entry_count"] == 14
    assert [row["filename"] for row in rows] == execution.OUTPUT_FILENAMES
    assert len(rows) == 14
    assert rows[-1]["digest_kind"] == "SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE"
    assert rows[-1]["sha256"] is None
    for row in rows[:-1]:
        assert row["sha256"] == sha256_file(output_root / row["filename"])


def test_source_hashes_remain_bound(executed) -> None:
    artifact, _ = executed
    verification = artifact["source_verification"]
    assert verification["verified_records_digest"] == execution.EXPECTED_RECORDS_DIGEST
    assert verification["verified_redesigned_label_values_digest"] == (
        execution.EXPECTED_LABEL_VALUES_DIGEST
    )
    assert verification["verified_feature_values_digest"] == (
        execution.EXPECTED_FEATURE_VALUES_DIGEST
    )
    assert verification["verified_feature_label_matrix_digest"] == (
        execution.EXPECTED_MATRIX_DIGEST
    )
    assert verification["verified_redesign_output_binding_digest"] == (
        execution.EXPECTED_REDESIGN_OUTPUT_BINDING_DIGEST
    )
    assert verification["source_files_unchanged"] is True


def test_checklist_passes(executed) -> None:
    artifact, _ = executed
    assert all(row["status"] == "PASS" for row in artifact["execution_checklist"])
    assert artifact["execution_checklist_summary"] == {
        "total_checks": 32,
        "passed_checks": 32,
        "failed_checks": 0,
        "blocker_count": 0,
    }


def test_validator_accepts_valid_artifact(executed) -> None:
    artifact, _ = executed
    result = execution.validate_improved_evidence_planning_executed_using_redesigned_evidence_v1(
        artifact
    )
    assert result["status"] == (
        execution.IMPROVED_EVIDENCE_PLANNING_EXECUTION_USING_REDESIGNED_EVIDENCE_VALID
    )


@pytest.mark.parametrize(
    ("field", "bad_value"),
    [
        ("artifact_kind", "WRONG"),
        ("execution_status", "WRONG"),
        ("improved_evidence_planning_approved", False),
        ("improved_evidence_planning_authorized", False),
        ("ready_for_improved_evidence_planning_execution_using_redesigned_evidence", False),
        ("improved_evidence_planning_executed", False),
        ("improved_evidence_planning_results_created", False),
        ("generated_output_count", 13),
        ("target_universe", list(reversed(execution.TARGET_UNIVERSE))),
        ("target_universe_count", 11),
        ("records_digest", "0" * 64),
        ("meta_record_count", 1003),
        ("selected_redesign_direction", "WRONG"),
        ("label_regeneration_authorized", True),
        ("label_regeneration_performed", True),
        ("new_targets_created", True),
        ("target_definition_change_authorized", True),
        ("feature_generation_authorized", True),
        ("feature_generation_performed", True),
        ("feature_label_matrix_created", True),
        ("additional_predictive_evidence_execution_candidate_created", True),
        ("additional_predictive_evidence_executed", True),
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
        ("feature_regeneration_performed", True),
        ("predictive_evidence_execution_rerun_performed", True),
        ("metric_recomputation_performed_in_execution", True),
        ("model_training_performed_in_execution", True),
    ],
)
def test_validator_rejects_invalid_contract_fields(
    executed, field: str, bad_value
) -> None:
    artifact, _ = executed
    invalid = deepcopy(artifact)
    invalid[field] = bad_value
    with pytest.raises(
        execution.ImprovedEvidencePlanningExecutionRedesignedEvidenceError
    ):
        execution.validate_improved_evidence_planning_executed_using_redesigned_evidence_v1(
            invalid
        )


@pytest.mark.parametrize(
    "field",
    [
        "improved_evidence_planning_approval_using_redesigned_evidence_digest",
        "improved_evidence_planning_candidate_using_redesigned_evidence_review_package_digest",
        "improved_evidence_planning_candidate_using_redesigned_evidence_digest",
        "label_objective_redesign_results_review_using_redesigned_evidence_digest",
        "feature_label_matrix_digest",
        "feature_values_digest",
        "redesigned_label_values_digest",
        "research_registry_approval_digest",
        "records_digest",
    ],
)
def test_validator_rejects_missing_source_digest(executed, field: str) -> None:
    artifact, _ = executed
    invalid = deepcopy(artifact)
    invalid["source_evidence"].pop(field)
    with pytest.raises(
        execution.ImprovedEvidencePlanningExecutionRedesignedEvidenceError
    ):
        execution.validate_improved_evidence_planning_executed_using_redesigned_evidence_v1(
            invalid
        )


def test_validator_rejects_missing_execution_digest(executed) -> None:
    artifact, _ = executed
    invalid = deepcopy(artifact)
    invalid.pop(
        "improved_evidence_planning_execution_using_redesigned_evidence_digest"
    )
    with pytest.raises(
        execution.ImprovedEvidencePlanningExecutionRedesignedEvidenceError,
        match="execution digest missing",
    ):
        execution.validate_improved_evidence_planning_executed_using_redesigned_evidence_v1(
            invalid
        )


def test_validator_rejects_missing_output_manifest_digest(executed) -> None:
    artifact, _ = executed
    invalid = deepcopy(artifact)
    invalid["output_digest_manifest_summary"].pop("binding_digest")
    with pytest.raises(
        execution.ImprovedEvidencePlanningExecutionRedesignedEvidenceError,
        match="output manifest digest",
    ):
        execution.validate_improved_evidence_planning_executed_using_redesigned_evidence_v1(
            invalid
        )


def test_validator_rejects_missing_per_ticker_execution_digest(executed) -> None:
    artifact, _ = executed
    invalid = deepcopy(artifact)
    invalid["per_ticker_execution_entries"][0].pop(
        "per_ticker_improved_evidence_planning_execution_digest"
    )
    with pytest.raises(
        execution.ImprovedEvidencePlanningExecutionRedesignedEvidenceError,
        match="per-ticker execution digest missing",
    ):
        execution.validate_improved_evidence_planning_executed_using_redesigned_evidence_v1(
            invalid
        )


def test_execution_digest_is_deterministic_for_fixed_timestamp_and_source(
    tmp_path, monkeypatch: pytest.MonkeyPatch
) -> None:
    first = _execute(monkeypatch, tmp_path / "first", tmp_path / "source-a")
    second = _execute(monkeypatch, tmp_path / "second", tmp_path / "source-b")
    assert first[
        "improved_evidence_planning_execution_using_redesigned_evidence_digest"
    ] == second[
        "improved_evidence_planning_execution_using_redesigned_evidence_digest"
    ]
    assert [
        row["per_ticker_improved_evidence_planning_execution_digest"]
        for row in first["per_ticker_execution_entries"]
    ] == [
        row["per_ticker_improved_evidence_planning_execution_digest"]
        for row in second["per_ticker_execution_entries"]
    ]


def test_execution_refuses_to_overwrite_outputs(
    tmp_path, monkeypatch: pytest.MonkeyPatch
) -> None:
    output_root = tmp_path / "outputs"
    _execute(monkeypatch, output_root, tmp_path / "source")
    with pytest.raises(
        execution.ImprovedEvidencePlanningExecutionRedesignedEvidenceError,
        match="outputs already exist",
    ):
        _execute(monkeypatch, output_root, tmp_path / "source")


def test_markdown_includes_required_sections(executed) -> None:
    artifact, _ = executed
    markdown = execution.build_improved_evidence_planning_execution_status_markdown_v1(
        artifact
    )
    for heading in (
        "Title",
        "Optional Improved Evidence Planning Execution Using Redesigned Evidence",
        "Source Approval",
        "Bound Evidence",
        "Dataset and Universe",
        "Planning Execution Policy",
        "Planning Facts",
        "Selected Redesign Direction",
        "Proposed Label Schema Plan",
        "No-Trade / Abstain Coverage Plan",
        "Material-Move Threshold Plan",
        "Horizon-Specific Validation Plan",
        "Ticker / Regime Split Validation Plan",
        "Feature-Label Alignment Plan",
        "Chronological Split and Embargo Plan",
        "Baseline and Model Comparison Plan",
        "Calibration / Brier Plan",
        "Leakage and No-Peek Control Plan",
        "Per-Ticker and META Reporting Plan",
        "Output Digest Manifest",
        "Authority Boundary",
        "Predictive Usefulness Boundary",
        "Profitability Boundary",
        "Runtime Boundary",
        "Checklist Summary",
        "Guardrails",
    ):
        assert f"## {heading}" in markdown


def test_public_exports_are_available() -> None:
    import marketflow.services as services

    assert (
        services.ARTIFACT_KIND_IMPROVED_EVIDENCE_PLANNING_EXECUTED_USING_REDESIGNED_EVIDENCE
        == execution.ARTIFACT_KIND_IMPROVED_EVIDENCE_PLANNING_EXECUTED_USING_REDESIGNED_EVIDENCE
    )
    assert (
        services.IMPROVED_EVIDENCE_PLANNING_EXECUTED_USING_REDESIGNED_EVIDENCE_RESEARCH_ONLY
        == execution.IMPROVED_EVIDENCE_PLANNING_EXECUTED_USING_REDESIGNED_EVIDENCE_RESEARCH_ONLY
    )
    assert services.execute_improved_evidence_planning_using_redesigned_evidence_v1 is (
        execution.execute_improved_evidence_planning_using_redesigned_evidence_v1
    )
    assert (
        services.validate_improved_evidence_planning_executed_using_redesigned_evidence_v1
        is execution.validate_improved_evidence_planning_executed_using_redesigned_evidence_v1
    )
    assert services.build_improved_evidence_planning_execution_status_markdown_v1 is (
        execution.build_improved_evidence_planning_execution_status_markdown_v1
    )
